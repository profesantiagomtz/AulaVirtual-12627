-- Seguimiento en vivo, avance real y asistencia automática.
-- Ejecuta este archivo completo una sola vez en Supabase > SQL Editor.
-- Solo crea tablas, funciones y disparadores nuevos; no modifica ni borra datos existentes.
-- La hora local de las clases se toma de Tamaulipas (America/Monterrey).

-- 1. Total de pasos de cada material, para calcular el % real de avance.
alter table public.learning_progress add column if not exists total_steps integer check (total_steps is null or total_steps > 0);

-- 2. Quién está conectado ahora y qué está viendo.
create table if not exists public.student_presence(
  student_id uuid primary key references public.profiles(id) on delete cascade,
  last_seen_at timestamptz not null default now(),
  session_started_at timestamptz not null default now(),
  current_view text,
  current_detail text
);

-- 3. Minutos conectados por día (hora local). Sirve para el tiempo de uso y para pasar lista.
create table if not exists public.student_daily_activity(
  student_id uuid not null references public.profiles(id) on delete cascade,
  day date not null,
  minutes smallint[] not null default '{}',
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  primary key(student_id, day)
);

-- 4. Bitácora de lo que hace cada alumno (entradas, páginas, avance, entregas).
create table if not exists public.student_activity_log(
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles(id) on delete cascade,
  kind text not null check (kind in ('entrada', 'vista', 'avance', 'completo', 'inicio', 'entrega')),
  title text not null default '',
  detail text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists student_activity_log_created_idx on public.student_activity_log(created_at desc);
create index if not exists student_activity_log_student_idx on public.student_activity_log(student_id, created_at desc);

-- 5. Pase de lista por módulo y fecha de clase.
create table if not exists public.attendance_records(
  student_id uuid not null references public.profiles(id) on delete cascade,
  course_code text not null,
  class_date date not null,
  status text not null check (status in ('asistio', 'retardo', 'falto', 'justifico')),
  updated_by uuid references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now(),
  primary key(student_id, course_code, class_date)
);

-- 6. Horario de cada clase (por módulo y día de la semana: 0 domingo … 6 sábado).
create table if not exists public.attendance_schedules(
  course_code text not null,
  weekday smallint not null check (weekday between 0 and 6),
  starts_at time not null,
  ends_at time not null,
  tolerance_minutes smallint not null default 10 check (tolerance_minutes between 0 and 120),
  primary key(course_code, weekday),
  check (ends_at > starts_at)
);

alter table public.student_presence enable row level security;
alter table public.student_daily_activity enable row level security;
alter table public.student_activity_log enable row level security;
alter table public.attendance_records enable row level security;
alter table public.attendance_schedules enable row level security;

-- Solo el docente consulta el seguimiento; los alumnos escriben a través de aula_heartbeat().
drop policy if exists "staff reads presence" on public.student_presence;
create policy "staff reads presence" on public.student_presence for select to authenticated using (public.is_staff());
drop policy if exists "staff reads daily activity" on public.student_daily_activity;
create policy "staff reads daily activity" on public.student_daily_activity for select to authenticated using (public.is_staff());
drop policy if exists "staff reads activity log" on public.student_activity_log;
create policy "staff reads activity log" on public.student_activity_log for select to authenticated using (public.is_staff());
drop policy if exists "staff manages attendance" on public.attendance_records;
create policy "staff manages attendance" on public.attendance_records for all to authenticated using (public.is_staff()) with check (public.is_staff());
drop policy if exists "staff manages schedules" on public.attendance_schedules;
create policy "staff manages schedules" on public.attendance_schedules for all to authenticated using (public.is_staff()) with check (public.is_staff());

-- Latido del alumno: la plataforma lo envía cada minuto mientras la pestaña está abierta.
create or replace function public.aula_heartbeat(p_view text default null, p_detail text default null, p_entry boolean default false)
returns void language plpgsql security definer set search_path = public as $$
declare
  uid uuid := auth.uid();
  local_now timestamp := now() at time zone 'America/Monterrey';
  minute_of_day smallint := (extract(hour from local_now) * 60 + extract(minute from local_now))::smallint;
  previous public.student_presence%rowtype;
  view_label text := left(coalesce(p_view, ''), 80);
  detail_label text := left(coalesce(p_detail, ''), 200);
begin
  if uid is null or not exists(select 1 from public.profiles where id = uid and role = 'student') then return; end if;
  select * into previous from public.student_presence where student_id = uid;

  insert into public.student_presence(student_id, last_seen_at, session_started_at, current_view, current_detail)
  values (uid, now(), now(), view_label, detail_label)
  on conflict (student_id) do update set
    last_seen_at = now(),
    session_started_at = case when p_entry or student_presence.last_seen_at < now() - interval '10 minutes' then now() else student_presence.session_started_at end,
    current_view = excluded.current_view,
    current_detail = excluded.current_detail;

  insert into public.student_daily_activity(student_id, day, minutes)
  values (uid, local_now::date, array[minute_of_day])
  on conflict (student_id, day) do update set
    minutes = case when minute_of_day = any(student_daily_activity.minutes) then student_daily_activity.minutes else student_daily_activity.minutes || minute_of_day end,
    last_seen_at = now();

  if p_entry and (previous.student_id is null or previous.last_seen_at < now() - interval '10 minutes') then
    insert into public.student_activity_log(student_id, kind, title) values (uid, 'entrada', 'entró a la plataforma');
  end if;
  if view_label <> '' and (previous.student_id is null or coalesce(previous.current_view, '') <> view_label or coalesce(previous.current_detail, '') <> detail_label) then
    insert into public.student_activity_log(student_id, kind, title, detail) values (uid, 'vista', view_label, detail_label);
  end if;
end; $$;
revoke all on function public.aula_heartbeat(text, text, boolean) from public, anon;
grant execute on function public.aula_heartbeat(text, text, boolean) to authenticated;

-- Avance en el material: se registra solo, sin importar qué parte de la plataforma lo guardó.
create or replace function public.log_learning_progress()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  steps integer := coalesce(jsonb_array_length(new.completed_steps), 0);
  old_steps integer := case when tg_op = 'UPDATE' then coalesce(jsonb_array_length(old.completed_steps), 0) else 0 end;
begin
  if new.completed_at is not null and (tg_op = 'INSERT' or old.completed_at is null) then
    insert into public.student_activity_log(student_id, kind, title, detail) values (new.student_id, 'completo', new.material_code, 'terminó el material');
  elsif steps > old_steps then
    insert into public.student_activity_log(student_id, kind, title, detail)
    values (new.student_id, 'avance', new.material_code, 'paso ' || steps || coalesce(' de ' || new.total_steps, ''));
  end if;
  return new;
end; $$;
drop trigger if exists learning_progress_activity on public.learning_progress;
create trigger learning_progress_activity after insert or update on public.learning_progress
for each row execute procedure public.log_learning_progress();

-- Tareas: cuando el alumno empieza y cuando entrega.
create or replace function public.log_submission_activity()
returns trigger language plpgsql security definer set search_path = public as $$
declare task_title text;
begin
  select title into task_title from public.assessments where id = new.assessment_id;
  if new.submitted_at is not null and (tg_op = 'INSERT' or old.submitted_at is null) then
    insert into public.student_activity_log(student_id, kind, title) values (new.student_id, 'entrega', coalesce(task_title, 'Tarea'));
  elsif tg_op = 'INSERT' then
    insert into public.student_activity_log(student_id, kind, title) values (new.student_id, 'inicio', coalesce(task_title, 'Tarea'));
  end if;
  return new;
end; $$;
drop trigger if exists submission_activity on public.submissions;
create trigger submission_activity after insert or update on public.submissions
for each row execute procedure public.log_submission_activity();

-- Resumen por alumno para la vista «Avance»: último acceso, tiempo total y días activos.
create or replace function public.aula_tracking_summary()
returns table(student_id uuid, last_seen_at timestamptz, total_minutes integer, active_days integer, today_minutes integer)
language sql stable security definer set search_path = public as $$
  select d.student_id,
         max(d.last_seen_at),
         sum(coalesce(array_length(d.minutes, 1), 0))::integer,
         count(*)::integer,
         sum(case when d.day = (now() at time zone 'America/Monterrey')::date then coalesce(array_length(d.minutes, 1), 0) else 0 end)::integer
  from public.student_daily_activity d
  where public.is_staff()
  group by d.student_id;
$$;
revoke all on function public.aula_tracking_summary() from public, anon;
grant execute on function public.aula_tracking_summary() to authenticated;
