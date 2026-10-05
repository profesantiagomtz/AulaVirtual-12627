-- Ejecuta este archivo completo en Supabase > SQL Editor.
create extension if not exists "uuid-ossp";

create type public.user_role as enum ('student', 'teacher', 'admin');
create type public.resource_type as enum ('file', 'link', 'video');
create type public.assessment_status as enum ('draft', 'published', 'closed');

create table public.groups (
  id uuid primary key default uuid_generate_v4(),
  code text unique not null,
  semester smallint not null check (semester between 1 and 6),
  career text not null,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table public.enrollment_rules (
  id uuid primary key default uuid_generate_v4(),
  email_pattern text,
  enrollment_prefix text,
  group_id uuid not null references public.groups(id) on delete cascade,
  priority integer not null default 0,
  active boolean not null default true,
  check (email_pattern is not null or enrollment_prefix is not null)
);

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique not null check (
    lower(email) like '%@tam.conalep.edu.mx'
    or lower(email) like '%@conaleptamaulipas.edu.mx'
  ),
  full_name text not null default '',
  enrollment_number text unique,
  role public.user_role not null default 'student',
  group_id uuid references public.groups(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.materials (
  id uuid primary key default uuid_generate_v4(),
  teacher_id uuid not null references public.profiles(id),
  group_id uuid references public.groups(id) on delete cascade,
  title text not null,
  description text not null default '',
  unit text,
  resource_type public.resource_type not null,
  resource_url text not null,
  published boolean not null default true,
  created_at timestamptz not null default now()
);

create table public.assessments (
  id uuid primary key default uuid_generate_v4(),
  teacher_id uuid not null references public.profiles(id),
  group_id uuid not null references public.groups(id) on delete cascade,
  title text not null,
  instructions text not null default '',
  status public.assessment_status not null default 'draft',
  opens_at timestamptz,
  due_at timestamptz,
  time_limit_minutes integer check (time_limit_minutes > 0),
  created_at timestamptz not null default now()
);

create table public.questions (
  id uuid primary key default uuid_generate_v4(),
  assessment_id uuid not null references public.assessments(id) on delete cascade,
  prompt text not null,
  options jsonb not null default '[]',
  correct_answer jsonb not null,
  points numeric(6,2) not null default 1,
  position integer not null
);

create table public.submissions (
  id uuid primary key default uuid_generate_v4(),
  assessment_id uuid not null references public.assessments(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  answers jsonb not null default '{}',
  score numeric(6,2),
  started_at timestamptz not null default now(),
  submitted_at timestamptz,
  unique (assessment_id, student_id)
);

create table public.material_views (
  material_id uuid references public.materials(id) on delete cascade,
  student_id uuid references public.profiles(id) on delete cascade,
  viewed_at timestamptz not null default now(),
  primary key (material_id, student_id)
);

-- Crea el perfil al registrarse y busca grupo por prefijo de matrícula o patrón de correo.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare assigned_group uuid;
declare incoming_enrollment text;
begin
  if lower(new.email) not like '%@tam.conalep.edu.mx'
     and lower(new.email) not like '%@conaleptamaulipas.edu.mx' then
    raise exception 'Solo se permiten correos institucionales autorizados';
  end if;
  incoming_enrollment := new.raw_user_meta_data ->> 'enrollment_number';
  select er.group_id into assigned_group
  from public.enrollment_rules er
  where er.active and (
    (er.enrollment_prefix is not null and incoming_enrollment like er.enrollment_prefix || '%') or
    (er.email_pattern is not null and lower(new.email) like lower(er.email_pattern))
  ) order by er.priority desc limit 1;
  insert into public.profiles (id,email,full_name,enrollment_number,role,group_id)
  values (new.id,lower(new.email),coalesce(new.raw_user_meta_data->>'full_name',''),incoming_enrollment,'student',assigned_group);
  return new;
end; $$;

create trigger on_auth_user_created after insert on auth.users
for each row execute procedure public.handle_new_user();

create or replace function public.is_staff()
returns boolean language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.profiles where id=auth.uid() and role in ('teacher','admin'));
$$;

alter table public.groups enable row level security;
alter table public.enrollment_rules enable row level security;
alter table public.profiles enable row level security;
alter table public.materials enable row level security;
alter table public.assessments enable row level security;
alter table public.questions enable row level security;
alter table public.submissions enable row level security;
alter table public.material_views enable row level security;

create policy "authenticated read groups" on public.groups for select to authenticated using (true);
create policy "staff manage groups" on public.groups for all to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "staff manage rules" on public.enrollment_rules for all to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "profile self or staff read" on public.profiles for select to authenticated using (id=auth.uid() or public.is_staff());
create policy "profile self update" on public.profiles for update to authenticated using (id=auth.uid()) with check (id=auth.uid());
create policy "materials by group" on public.materials for select to authenticated using (public.is_staff() or group_id is null or group_id=(select group_id from public.profiles where id=auth.uid()));
create policy "staff manage materials" on public.materials for all to authenticated using (public.is_staff()) with check (public.is_staff() and teacher_id=auth.uid());
create policy "assessments by group" on public.assessments for select to authenticated using (public.is_staff() or (status='published' and group_id=(select group_id from public.profiles where id=auth.uid())));
create policy "staff manage assessments" on public.assessments for all to authenticated using (public.is_staff()) with check (public.is_staff() and teacher_id=auth.uid());
create policy "questions for assigned assessment" on public.questions for select to authenticated using (exists(select 1 from public.assessments a where a.id=assessment_id and (public.is_staff() or a.group_id=(select group_id from public.profiles where id=auth.uid()))));
create policy "staff manage questions" on public.questions for all to authenticated using (public.is_staff()) with check (public.is_staff());
create policy "submission self or staff" on public.submissions for select to authenticated using (student_id=auth.uid() or public.is_staff());
create policy "student creates submission" on public.submissions for insert to authenticated with check (student_id=auth.uid());
create policy "student updates own submission" on public.submissions for update to authenticated using (student_id=auth.uid() and submitted_at is null) with check (student_id=auth.uid());
create policy "view self or staff" on public.material_views for select to authenticated using (student_id=auth.uid() or public.is_staff());
create policy "student records view" on public.material_views for insert to authenticated with check (student_id=auth.uid());

insert into storage.buckets (id,name,public,file_size_limit,allowed_mime_types)
values ('materials','materials',false,20971520,array['application/pdf','application/vnd.openxmlformats-officedocument.presentationml.presentation','application/vnd.openxmlformats-officedocument.wordprocessingml.document'])
on conflict (id) do nothing;
create policy "staff uploads materials" on storage.objects for insert to authenticated with check (bucket_id='materials' and public.is_staff());
create policy "assigned users download materials" on storage.objects for select to authenticated using (bucket_id='materials');

-- Datos iniciales de ejemplo. Cambia códigos, carreras y reglas por los de tu plantel.
insert into public.groups(code,semester,career) values
('111',1,'Formación básica'),('310',3,'Informática'),('311',3,'Informática'),('511',5,'Informática')
on conflict(code) do nothing;
