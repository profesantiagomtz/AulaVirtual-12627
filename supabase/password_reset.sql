-- Restablecer contraseñas (igual que en PEAR).
-- El docente asigna una contraseña temporal a un alumno; al entrar, el alumno debe cambiarla por una propia.
-- Ejecutar una vez en el SQL Editor de Supabase.

create extension if not exists pgcrypto with schema extensions;

alter table public.profiles add column if not exists must_change_password boolean not null default false;

create or replace function public.reset_student_password(p_student_id uuid, p_password text default null)
returns text
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_password text := nullif(trim(coalesce(p_password, '')), '');
begin
  if not public.is_staff() then
    raise exception 'Solo el docente puede restablecer contraseñas';
  end if;
  if not exists (select 1 from public.profiles where id = p_student_id and role = 'student') then
    raise exception 'No se encontró al alumno';
  end if;
  if v_password is null then
    v_password := 'Aula' || lpad(floor(random() * 10000)::int::text, 4, '0');
  end if;
  if length(v_password) < 6 then
    raise exception 'La contraseña temporal debe tener al menos 6 caracteres';
  end if;
  update auth.users
     set encrypted_password = extensions.crypt(v_password, extensions.gen_salt('bf')),
         updated_at = now()
   where id = p_student_id;
  update public.profiles set must_change_password = true where id = p_student_id;
  return v_password;
end;
$$;

-- El alumno avisa que ya cambió su contraseña temporal.
create or replace function public.password_changed()
returns void
language sql
security definer
set search_path = public
as $$
  update public.profiles set must_change_password = false where id = auth.uid();
$$;

revoke all on function public.reset_student_password(uuid, text) from public, anon;
revoke all on function public.password_changed() from public, anon;
grant execute on function public.reset_student_password(uuid, text) to authenticated;
grant execute on function public.password_changed() to authenticated;

-- Verificación: debe mostrar la columna nueva.
select column_name from information_schema.columns where table_schema = 'public' and table_name = 'profiles' and column_name = 'must_change_password';
