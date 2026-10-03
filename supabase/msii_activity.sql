-- Actividad individual MSII R.A. 1.1
-- Ejecutar una sola vez en Supabase SQL Editor.

alter table public.assessments add column if not exists activity_code text;
create unique index if not exists assessments_activity_code_group_key
  on public.assessments(activity_code, group_id) where activity_code is not null;

create table if not exists public.assessment_assignments (
  id uuid primary key default uuid_generate_v4(),
  assessment_id uuid not null references public.assessments(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  variant jsonb not null,
  created_at timestamptz not null default now(),
  unique (assessment_id, student_id)
);

alter table public.assessment_assignments enable row level security;
drop policy if exists "assignment self or staff" on public.assessment_assignments;
create policy "assignment self or staff" on public.assessment_assignments
  for select to authenticated using (student_id=auth.uid() or public.is_staff());

alter table public.submissions add column if not exists assignment_id uuid references public.assessment_assignments(id);
alter table public.submissions add column if not exists file_path text;
alter table public.submissions add column if not exists original_filename text;
alter table public.submissions add column if not exists document_token text;

insert into storage.buckets (id,name,public,file_size_limit,allowed_mime_types)
values (
  'submissions','submissions',false,20971520,
  array['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
)
on conflict (id) do update set
  public=false,
  file_size_limit=excluded.file_size_limit,
  allowed_mime_types=excluded.allowed_mime_types;

drop policy if exists "students upload own submissions" on storage.objects;
create policy "students upload own submissions" on storage.objects
  for insert to authenticated
  with check (bucket_id='submissions' and split_part(name,'/',1)=auth.uid()::text);
drop policy if exists "students replace own submissions" on storage.objects;
create policy "students replace own submissions" on storage.objects
  for update to authenticated
  using (bucket_id='submissions' and split_part(name,'/',1)=auth.uid()::text)
  with check (bucket_id='submissions' and split_part(name,'/',1)=auth.uid()::text);
drop policy if exists "students and staff read submissions" on storage.objects;
create policy "students and staff read submissions" on storage.objects
  for select to authenticated
  using (bucket_id='submissions' and (split_part(name,'/',1)=auth.uid()::text or public.is_staff()));

create or replace function public.get_or_create_msii_assignment(p_assessment_id uuid)
returns public.assessment_assignments
language plpgsql security definer set search_path=public as $$
declare
  existing public.assessment_assignments;
  profile_group uuid;
  assessment_group uuid;
  seed bigint;
  operating_systems text[] := array['Ubuntu 24.04 LTS','Linux Mint 22','Fedora Workstation 42','Debian 13'];
  characters text[] := array['A','C','E','G','J','L','M','P','R','T','V','X','Y','Z'];
begin
  select * into existing from public.assessment_assignments
    where assessment_id=p_assessment_id and student_id=auth.uid();
  if found then return existing; end if;

  select group_id into profile_group from public.profiles where id=auth.uid() and role='student';
  select group_id into assessment_group from public.assessments
    where id=p_assessment_id and status='published' and activity_code='MSII-RA-1.1';
  if assessment_group is null or profile_group is distinct from assessment_group then
    raise exception 'Esta actividad no está asignada a tu grupo';
  end if;

  seed := abs(hashtextextended(auth.uid()::text || p_assessment_id::text, 12627));
  insert into public.assessment_assignments(assessment_id,student_id,variant)
  values (p_assessment_id,auth.uid(),jsonb_build_object(
    'equipment', 'Equipo ' || lpad(((seed % 30)+1)::text,2,'0'),
    'compare_os', operating_systems[((seed / 31) % array_length(operating_systems,1))+1],
    'decimal_number', ((seed / 131) % 48)+80,
    'ascii_character', characters[((seed / 8191) % array_length(characters,1))+1],
    'capacity', (((seed / 65537) % 8)+2)::text || ' GB'
  )) returning * into existing;
  return existing;
exception when unique_violation then
  select * into existing from public.assessment_assignments
    where assessment_id=p_assessment_id and student_id=auth.uid();
  return existing;
end; $$;

revoke all on function public.get_or_create_msii_assignment(uuid) from public;
grant execute on function public.get_or_create_msii_assignment(uuid) to authenticated;

create or replace function public.submit_msii_document(
  p_assessment_id uuid,
  p_assignment_id uuid,
  p_file_path text,
  p_original_filename text,
  p_document_token text
) returns uuid
language plpgsql security definer set search_path=public as $$
declare result_id uuid;
begin
  if p_document_token <> p_assignment_id::text then raise exception 'La identificación del documento no es válida'; end if;
  if not exists (
    select 1 from public.assessment_assignments aa
    join public.assessments a on a.id=aa.assessment_id
    where aa.id=p_assignment_id and aa.assessment_id=p_assessment_id
      and aa.student_id=auth.uid() and a.status='published'
  ) then raise exception 'Este archivo no corresponde a tu cuenta'; end if;
  if p_file_path not like auth.uid()::text || '/%' then raise exception 'Ruta de entrega no válida'; end if;

  insert into public.submissions(assessment_id,student_id,assignment_id,answers,file_path,original_filename,document_token,submitted_at)
  values (p_assessment_id,auth.uid(),p_assignment_id,'{}',p_file_path,p_original_filename,p_document_token,now())
  on conflict (assessment_id,student_id) do update set
    assignment_id=excluded.assignment_id,
    file_path=excluded.file_path,
    original_filename=excluded.original_filename,
    document_token=excluded.document_token,
    submitted_at=excluded.submitted_at
  returning id into result_id;
  return result_id;
end; $$;

revoke all on function public.submit_msii_document(uuid,uuid,text,text,text) from public;
grant execute on function public.submit_msii_document(uuid,uuid,text,text,text) to authenticated;

insert into public.assessments(teacher_id,group_id,title,instructions,status,activity_code)
select teacher.id, groups.id,
  'MSII - Actividad de evaluación R.A. 1.1',
  'Descarga tu formato personalizado, complétalo en el laboratorio y entrega el mismo archivo DOCX.',
  'published','MSII-RA-1.1'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
  and not exists (
    select 1 from public.assessments a where a.activity_code='MSII-RA-1.1' and a.group_id=groups.id
  )
limit 1;
