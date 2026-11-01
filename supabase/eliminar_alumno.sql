-- Eliminar cuentas de alumnos (p. ej. cuentas duplicadas) desde el panel docente.
-- Ejecutar una vez en el SQL Editor de Supabase.
--
-- Qué hace:
--  1. student_account_summary: el docente ve cuánto trabajo tiene la cuenta antes de borrarla.
--  2. transfer_student_work (opcional): pasa entregas, avance, asistencia, etc. a la otra cuenta
--     del mismo alumno. Si la otra cuenta ya tiene algo de la misma actividad, se respeta lo de la otra.
--  3. delete_student_account: borra la cuenta de acceso (auth) y, en cascada, todo lo suyo.
--     Pide escribir el correo exacto como confirmación y deja un registro en deleted_student_accounts.
--     Devuelve la lista de archivos que ya nadie usa; el panel los borra del Storage
--     (Supabase no permite borrar archivos desde SQL).
-- Todo corre en la base de datos con permisos del dueño: la service key nunca llega al navegador.

-- Registro de cuentas eliminadas (solo lo ve el docente).
create table if not exists public.deleted_student_accounts (
  id bigint generated always as identity primary key,
  student_id uuid not null,
  full_name text,
  email text,
  group_code text,
  summary jsonb,
  transferred_to uuid,
  deleted_by uuid,
  deleted_at timestamptz not null default now()
);
alter table public.deleted_student_accounts enable row level security;
drop policy if exists "staff read deleted accounts" on public.deleted_student_accounts;
create policy "staff read deleted accounts" on public.deleted_student_accounts for select to authenticated using (public.is_staff());

-- El docente puede borrar archivos de entregas (solo los que devuelve delete_student_account).
drop policy if exists "staff delete submissions files" on storage.objects;
create policy "staff delete submissions files" on storage.objects for delete to authenticated
  using (bucket_id = 'submissions' and public.is_staff());

-- Si se pasó trabajo de una cuenta a otra, el alumno sigue viendo sus archivos aunque estén en la carpeta vieja.
drop policy if exists "students read transferred submissions" on storage.objects;
create policy "students read transferred submissions" on storage.objects for select to authenticated
  using (bucket_id = 'submissions' and exists (
    select 1 from public.submissions s where s.student_id = auth.uid() and (s.file_path = name or position(name in s.answers::text) > 0)
    union all
    select 1 from public.edoa_practice_submissions e where e.student_id = auth.uid() and e.file_path = name));

-- 1. Resumen de lo que tiene la cuenta.
create or replace function public.student_account_summary(p_student uuid)
returns jsonb
language plpgsql
stable
security definer
set search_path = public
as $$
begin
  if not public.is_staff() then raise exception 'Solo el docente puede consultar esto'; end if;
  if not exists (select 1 from public.profiles where id = p_student and role = 'student') then
    raise exception 'No se encontró al alumno';
  end if;
  return jsonb_build_object(
    'entregadas', (select count(*) from public.submissions where student_id = p_student and submitted_at is not null),
    'en_proceso', (select count(*) from public.submissions where student_id = p_student and submitted_at is null),
    'calificadas', (select count(*) from public.submissions where student_id = p_student and score is not null),
    'avance', (select count(*) from public.learning_progress where student_id = p_student),
    'practicas_edoa', (select count(*) from public.edoa_practice_submissions where student_id = p_student),
    'asistencias', (select count(*) from public.attendance_records where student_id = p_student),
    'notas', (select count(*) from public.teacher_student_notes where student_id = p_student),
    'archivos', (select count(*) from storage.objects where bucket_id = 'submissions' and split_part(name, '/', 1) = p_student::text),
    'ultimo_acceso', (select last_sign_in_at from auth.users where id = p_student),
    'creada', (select created_at from auth.users where id = p_student)
  );
end;
$$;

-- 2. Pasar el trabajo a la otra cuenta del alumno (no sobrescribe lo que la otra ya tenga).
create or replace function public.transfer_student_work(p_from uuid, p_to uuid)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_sub int; v_prog int; v_edoa int; v_att int; v_notes int;
begin
  if not public.is_staff() then raise exception 'Solo el docente puede pasar trabajo entre cuentas'; end if;
  if p_from = p_to then raise exception 'Elija una cuenta distinta'; end if;
  if (select count(*) from public.profiles where id in (p_from, p_to) and role = 'student') <> 2 then
    raise exception 'Ambas cuentas deben ser de alumnos';
  end if;

  -- Asignaciones (variante de la actividad) que la otra cuenta todavía no tiene.
  update public.assessment_assignments a set student_id = p_to
   where a.student_id = p_from
     and not exists (select 1 from public.assessment_assignments b where b.student_id = p_to and b.assessment_id = a.assessment_id);

  -- Entregas que la otra cuenta todavía no tiene.
  update public.submissions s
     set student_id = p_to,
         assignment_id = coalesce((select b.id from public.assessment_assignments b where b.student_id = p_to and b.assessment_id = s.assessment_id), s.assignment_id)
   where s.student_id = p_from
     and not exists (select 1 from public.submissions t where t.student_id = p_to and t.assessment_id = s.assessment_id);
  get diagnostics v_sub = row_count;

  update public.learning_progress l set student_id = p_to
   where l.student_id = p_from
     and not exists (select 1 from public.learning_progress t where t.student_id = p_to and t.material_code = l.material_code);
  get diagnostics v_prog = row_count;

  update public.edoa_practice_submissions e set student_id = p_to
   where e.student_id = p_from
     and not exists (select 1 from public.edoa_practice_submissions t where t.student_id = p_to and t.practice_code = e.practice_code);
  get diagnostics v_edoa = row_count;

  update public.attendance_records r set student_id = p_to
   where r.student_id = p_from
     and not exists (select 1 from public.attendance_records t where t.student_id = p_to and t.course_code = r.course_code and t.class_date = r.class_date);
  get diagnostics v_att = row_count;

  update public.teacher_student_notes n set student_id = p_to
   where n.student_id = p_from
     and not exists (select 1 from public.teacher_student_notes t where t.student_id = p_to and t.teacher_id = n.teacher_id and t.course_code = n.course_code);
  get diagnostics v_notes = row_count;

  update public.student_daily_activity d set student_id = p_to
   where d.student_id = p_from
     and not exists (select 1 from public.student_daily_activity t where t.student_id = p_to and t.day = d.day);
  update public.student_activity_log set student_id = p_to where student_id = p_from;

  return jsonb_build_object('entregas', v_sub, 'avance', v_prog, 'practicas_edoa', v_edoa, 'asistencias', v_att, 'notas', v_notes);
end;
$$;

-- 3. Borrar la cuenta. Devuelve los archivos que ya no usa nadie para que el panel los quite del Storage.
create or replace function public.delete_student_account(p_student uuid, p_confirm_email text, p_transferred_to uuid default null)
returns text[]
language plpgsql
security definer
set search_path = public
as $$
declare
  v_profile public.profiles%rowtype;
  v_group text;
  v_files text[];
begin
  if not public.is_staff() then raise exception 'Solo el docente puede eliminar cuentas'; end if;
  if p_student = auth.uid() then raise exception 'No puede eliminar su propia cuenta'; end if;
  select * into v_profile from public.profiles where id = p_student;
  if not found or v_profile.role <> 'student' then raise exception 'Solo se pueden eliminar cuentas de alumnos'; end if;
  if lower(trim(coalesce(p_confirm_email, ''))) <> lower(trim(coalesce(v_profile.email, ''))) then
    raise exception 'El correo escrito no coincide con el de la cuenta';
  end if;
  select code into v_group from public.groups where id = v_profile.group_id;

  insert into public.deleted_student_accounts (student_id, full_name, email, group_code, summary, transferred_to, deleted_by)
  values (p_student, v_profile.full_name, v_profile.email, v_group, public.student_account_summary(p_student), p_transferred_to, auth.uid());

  -- Borra la cuenta de acceso; profiles y todo lo del alumno se borran en cascada.
  delete from auth.users where id = p_student;

  -- Archivos de su carpeta que ya no usa ninguna entrega (los pasados a otra cuenta se conservan).
  select coalesce(array_agg(o.name), '{}') into v_files
    from storage.objects o
   where o.bucket_id = 'submissions'
     and split_part(o.name, '/', 1) = p_student::text
     and not exists (select 1 from public.submissions s where s.file_path = o.name or position(o.name in s.answers::text) > 0)
     and not exists (select 1 from public.edoa_practice_submissions e where e.file_path = o.name);
  return v_files;
end;
$$;

revoke all on function public.student_account_summary(uuid) from public, anon;
revoke all on function public.transfer_student_work(uuid, uuid) from public, anon;
revoke all on function public.delete_student_account(uuid, text, uuid) from public, anon;
grant execute on function public.student_account_summary(uuid) to authenticated;
grant execute on function public.transfer_student_work(uuid, uuid) to authenticated;
grant execute on function public.delete_student_account(uuid, text, uuid) to authenticated;

-- Verificación: deben aparecer las 3 funciones.
select proname from pg_proc where pronamespace = 'public'::regnamespace
 and proname in ('student_account_summary', 'transfer_student_work', 'delete_student_account');
