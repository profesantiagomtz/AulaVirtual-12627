-- Correcciones de seguridad (23 oct 2026).
-- Ejecutar una sola vez en Supabase > SQL Editor. Se puede volver a ejecutar sin problema.

-- 1) Un alumno ya no puede cambiar su rol, grupo, correo ni matrícula.
--    Solo puede editar su nombre. El docente sigue administrando todo con is_staff().
revoke update on public.profiles from authenticated, anon;
grant update (full_name, updated_at) on public.profiles to authenticated;

-- 2) Un alumno no puede ponerse calificación ni cambiar fechas de su entrega.
create or replace function public.protect_submission()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  -- SQL Editor / service_role (sin usuario) y docentes: sin restricciones.
  if auth.uid() is null or public.is_staff() then
    return new;
  end if;

  if tg_op = 'INSERT' then
    new.student_id := auth.uid();
    new.score := null;
    new.started_at := now();
    if new.submitted_at is not null then new.submitted_at := now(); end if;
  else
    new.student_id := old.student_id;
    new.assessment_id := old.assessment_id;
    new.score := old.score;
    new.started_at := old.started_at;
    if old.submitted_at is not null then
      new.submitted_at := old.submitted_at;          -- la fecha de entrega no se mueve
    elsif new.submitted_at is not null then
      new.submitted_at := now();                     -- la pone el servidor, no el navegador
    end if;
  end if;
  return new;
end; $$;

drop trigger if exists protect_submission on public.submissions;
create trigger protect_submission before insert or update on public.submissions
for each row execute function public.protect_submission();

-- 3) Los alumnos ya no pueden leer las respuestas correctas de las preguntas.
revoke select on public.questions from authenticated, anon;
grant select (id, assessment_id, prompt, options, points, position) on public.questions to authenticated;

-- 4) La función interna no se puede llamar desde el navegador.
revoke execute on function public.protect_submission() from public, anon, authenticated;

-- Revisión: confirma que solo tus cuentas tienen rol de docente.
-- Si aparece un alumno, cámbialo a 'student' desde el editor de tablas.
select email, role from public.profiles where role in ('teacher', 'admin') order by email;
