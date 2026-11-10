-- Limpiar una entrega para que el alumno la vuelva a hacer y subir (solo el docente).
-- Ejecutar una vez en el SQL Editor de Supabase. Se puede correr de nuevo sin problema.
--
-- Qué hace:
--  1. reset_submission: borra la entrega (respuestas, archivo y calificación) de UN alumno en UNA actividad.
--     Verifica que quien lo pide sea docente.
--     NO toca el avance del material, ni sus otras entregas, ni los datos asignados (misma variante).
--     Deja copia de lo borrado en submission_resets (por si hay que consultarlo después).
--     Devuelve los archivos que ya nadie usa; el panel los borra del Storage
--     (Supabase no permite borrar archivos desde SQL).

-- Registro de entregas limpiadas (solo lo ve el docente).
create table if not exists public.submission_resets (
  id bigint generated always as identity primary key,
  submission_id uuid not null,
  assessment_id uuid,
  assessment_title text,
  student_id uuid,
  student_name text,
  answers jsonb,
  score numeric(6,2),
  file_path text,
  original_filename text,
  started_at timestamptz,
  submitted_at timestamptz,
  files text[],
  reset_by uuid,
  reset_at timestamptz not null default now()
);
alter table public.submission_resets enable row level security;
drop policy if exists "staff read submission resets" on public.submission_resets;
create policy "staff read submission resets" on public.submission_resets for select to authenticated using (public.is_staff());

-- El docente puede borrar archivos de entregas (solo los que devuelve reset_submission).
drop policy if exists "staff delete submissions files" on storage.objects;
create policy "staff delete submissions files" on storage.objects for delete to authenticated
  using (bucket_id = 'submissions' and public.is_staff());

create or replace function public.reset_submission(p_submission uuid)
returns text[]
language plpgsql
security definer
set search_path = public
as $$
declare
  v_sub public.submissions%rowtype;
  v_title text;
  v_name text;
  v_files text[];
begin
  if not public.is_staff() then raise exception 'Solo el docente puede limpiar entregas'; end if;
  select * into v_sub from public.submissions where id = p_submission for update;
  if not found then raise exception 'La entrega ya no existe (quizá ya se limpió)'; end if;
  select title into v_title from public.assessments where id = v_sub.assessment_id;
  select full_name into v_name from public.profiles where id = v_sub.student_id;

  -- Archivos de esta entrega (archivo principal y los que aparecen en sus respuestas: Packet Tracer, fotos…).
  select coalesce(array_agg(o.name), '{}') into v_files
    from storage.objects o
   where o.bucket_id = 'submissions'
     and (o.name = v_sub.file_path or position(o.name in v_sub.answers::text) > 0)
     -- que ninguna otra entrega o práctica los use
     and not exists (select 1 from public.submissions s where s.id <> v_sub.id and (s.file_path = o.name or position(o.name in s.answers::text) > 0))
     and not exists (select 1 from public.edoa_practice_submissions e where e.file_path = o.name);

  insert into public.submission_resets (submission_id, assessment_id, assessment_title, student_id, student_name, answers, score,
    file_path, original_filename, started_at, submitted_at, files, reset_by)
  values (v_sub.id, v_sub.assessment_id, v_title, v_sub.student_id, v_name, v_sub.answers, v_sub.score,
    v_sub.file_path, v_sub.original_filename, v_sub.started_at, v_sub.submitted_at, v_files, auth.uid());

  delete from public.submissions where id = v_sub.id;
  return v_files;
end;
$$;

revoke all on function public.reset_submission(uuid) from public, anon;
grant execute on function public.reset_submission(uuid) to authenticated;
