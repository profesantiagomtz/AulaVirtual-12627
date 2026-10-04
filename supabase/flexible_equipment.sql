-- Permite que el alumno registre el equipo que realmente está utilizando.

create or replace function public.set_current_equipment(
  p_assessment_id uuid,
  p_equipment text
) returns public.assessment_assignments
language plpgsql security definer set search_path=public as $$
declare
  result public.assessment_assignments;
begin
  if p_equipment !~ '^Equipo [0-9]{2,3}$' then
    raise exception 'Número de equipo no válido';
  end if;

  update public.assessment_assignments aa
  set variant=jsonb_set(aa.variant,'{equipment}',to_jsonb(p_equipment),true)
  from public.assessments a
  where aa.assessment_id=a.id
    and aa.assessment_id=p_assessment_id
    and aa.student_id=auth.uid()
    and a.status='published'
    and a.activity_code='MSII-RA-1.1'
  returning aa.* into result;

  if result.id is null then raise exception 'No fue posible registrar el equipo'; end if;
  return result;
end; $$;

revoke all on function public.set_current_equipment(uuid,text) from public;
grant execute on function public.set_current_equipment(uuid,text) to authenticated;
