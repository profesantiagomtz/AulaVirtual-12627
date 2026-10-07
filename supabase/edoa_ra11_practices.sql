create table if not exists public.edoa_practice_submissions (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  practice_code text not null,
  file_path text not null,
  original_filename text,
  analysis jsonb not null default '{}'::jsonb,
  submitted_at timestamptz not null default now(),
  unique (student_id, practice_code)
);

alter table public.edoa_practice_submissions enable row level security;

drop policy if exists "Students manage own EDOA practices" on public.edoa_practice_submissions;
create policy "Students manage own EDOA practices"
on public.edoa_practice_submissions
for all
to authenticated
using (student_id = auth.uid())
with check (student_id = auth.uid());

drop policy if exists "Teachers read EDOA practices" on public.edoa_practice_submissions;
create policy "Teachers read EDOA practices"
on public.edoa_practice_submissions
for select
to authenticated
using (exists (
  select 1 from public.profiles
  where id = auth.uid() and role in ('teacher', 'admin')
));

insert into public.assessments (teacher_id, group_id, title, instructions, activity_code, status)
select
  teacher.id,
  class_group.id,
  'EDOA · Actividad de evaluación R.A. 1.1',
  'Elabora un documento con el formato establecido. Se desbloquea al completar las fichas y prácticas del R.A. 1.1.',
  'EDOA-RA-1.1',
  'published'
from public.profiles teacher
cross join public.groups class_group
where teacher.email = 'santiago.gonzalez@tam.conalep.edu.mx'
  and class_group.code = '311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title = excluded.title, instructions = excluded.instructions, status = excluded.status;
