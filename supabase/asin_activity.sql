-- Actividad ASIN R.A. 1.1 desarrollada dentro de Aula Virtual.
-- Ejecutar una sola vez en Supabase SQL Editor.

create or replace function public.get_or_create_asin_assignment(p_assessment_id uuid)
returns public.assessment_assignments
language plpgsql security definer set search_path=public as $$
declare
  existing public.assessment_assignments;
  profile_group uuid;
  assessment_group uuid;
  seed bigint;
begin
  select * into existing from public.assessment_assignments
    where assessment_id=p_assessment_id and student_id=auth.uid();
  if found then return existing; end if;

  select group_id into profile_group from public.profiles where id=auth.uid() and role='student';
  select group_id into assessment_group from public.assessments
    where id=p_assessment_id and status='published' and activity_code='ASIN-RA-1.1';
  if assessment_group is null or profile_group is distinct from assessment_group then
    raise exception 'Esta actividad no está asignada a tu grupo';
  end if;

  seed := abs(hashtextextended(auth.uid()::text || p_assessment_id::text, 12627));
  insert into public.assessment_assignments(assessment_id,student_id,variant)
  values (p_assessment_id,auth.uid(),jsonb_build_object(
    'equipment', 'Equipo ' || lpad(((seed % 20)+1)::text,2,'0')
  )) returning * into existing;
  return existing;
exception when unique_violation then
  select * into existing from public.assessment_assignments
    where assessment_id=p_assessment_id and student_id=auth.uid();
  return existing;
end; $$;

revoke all on function public.get_or_create_asin_assignment(uuid) from public;
grant execute on function public.get_or_create_asin_assignment(uuid) to authenticated;

create or replace function public.save_asin_progress(
  p_assessment_id uuid,
  p_answers jsonb,
  p_submit boolean default false
) returns public.submissions
language plpgsql security definer set search_path=public as $$
declare
  result public.submissions;
  current_submission public.submissions;
begin
  if not exists (
    select 1 from public.assessments a
    join public.profiles p on p.id=auth.uid() and p.group_id=a.group_id
    where a.id=p_assessment_id and a.status='published' and a.activity_code='ASIN-RA-1.1'
  ) then raise exception 'Esta actividad no está disponible'; end if;

  select * into current_submission from public.submissions
    where assessment_id=p_assessment_id and student_id=auth.uid();
  if current_submission.submitted_at is not null then
    raise exception 'La actividad ya fue entregada';
  end if;

  insert into public.submissions(assessment_id,student_id,answers,submitted_at)
  values (p_assessment_id,auth.uid(),p_answers,case when p_submit then now() else null end)
  on conflict (assessment_id,student_id) do update set
    answers=excluded.answers,
    submitted_at=case when p_submit then now() else public.submissions.submitted_at end
  returning * into result;
  return result;
end; $$;

revoke all on function public.save_asin_progress(uuid,jsonb,boolean) from public;
grant execute on function public.save_asin_progress(uuid,jsonb,boolean) to authenticated;

insert into public.assessments(teacher_id,group_id,title,instructions,status,activity_code)
select teacher.id, groups.id,
  'ASIN - Actividad de evaluación R.A. 1.1',
  'Completa las tres etapas directamente en Aula Virtual y entrega la actividad al finalizar.',
  'published','ASIN-RA-1.1'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
  and not exists (
    select 1 from public.assessments a where a.activity_code='ASIN-RA-1.1' and a.group_id=groups.id
  )
limit 1;
