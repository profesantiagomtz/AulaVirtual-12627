-- Notas privadas del docente por alumno y módulo.
create table if not exists public.teacher_student_notes (
  id uuid primary key default gen_random_uuid(),
  teacher_id uuid not null references public.profiles(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  course_code text not null,
  note text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (teacher_id, student_id, course_code)
);

alter table public.teacher_student_notes enable row level security;

drop policy if exists "Teacher reads own private notes" on public.teacher_student_notes;
create policy "Teacher reads own private notes"
on public.teacher_student_notes for select to authenticated
using (teacher_id = auth.uid() and public.is_staff());

drop policy if exists "Teacher creates own private notes" on public.teacher_student_notes;
create policy "Teacher creates own private notes"
on public.teacher_student_notes for insert to authenticated
with check (teacher_id = auth.uid() and public.is_staff());

drop policy if exists "Teacher updates own private notes" on public.teacher_student_notes;
create policy "Teacher updates own private notes"
on public.teacher_student_notes for update to authenticated
using (teacher_id = auth.uid() and public.is_staff())
with check (teacher_id = auth.uid() and public.is_staff());

drop policy if exists "Teacher deletes own private notes" on public.teacher_student_notes;
create policy "Teacher deletes own private notes"
on public.teacher_student_notes for delete to authenticated
using (teacher_id = auth.uid() and public.is_staff());

create index if not exists teacher_student_notes_student_idx
on public.teacher_student_notes(student_id, course_code);
