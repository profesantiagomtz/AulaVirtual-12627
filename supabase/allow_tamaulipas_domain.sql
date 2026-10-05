-- Permite ambos dominios institucionales en perfiles y registros nuevos.
alter table public.profiles
  drop constraint if exists profiles_email_check;

alter table public.profiles
  add constraint profiles_email_check check (
    lower(email) like '%@tam.conalep.edu.mx'
    or lower(email) like '%@conaleptamaulipas.edu.mx'
  );

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  assigned_group uuid;
  incoming_enrollment text;
  incoming_group_code text;
begin
  if lower(new.email) not like '%@tam.conalep.edu.mx'
     and lower(new.email) not like '%@conaleptamaulipas.edu.mx' then
    raise exception 'Solo se permiten correos institucionales autorizados';
  end if;

  incoming_enrollment := nullif(trim(new.raw_user_meta_data ->> 'enrollment_number'), '');
  incoming_group_code := nullif(trim(new.raw_user_meta_data ->> 'group_code'), '');

  if incoming_group_code is not null then
    select g.id into assigned_group
    from public.groups g
    where g.active and g.code = incoming_group_code
    limit 1;
  end if;

  if assigned_group is null then
    select er.group_id into assigned_group
    from public.enrollment_rules er
    where er.active and (
      (er.enrollment_prefix is not null and incoming_enrollment like er.enrollment_prefix || '%') or
      (er.email_pattern is not null and lower(new.email) like lower(er.email_pattern))
    )
    order by er.priority desc
    limit 1;
  end if;

  if assigned_group is null then
    raise exception 'Selecciona un grupo válido para completar tu registro';
  end if;

  insert into public.profiles (id, email, full_name, enrollment_number, role, group_id)
  values (new.id, lower(new.email), coalesce(new.raw_user_meta_data ->> 'full_name', ''), incoming_enrollment, 'student', assigned_group);

  return new;
end;
$$;
