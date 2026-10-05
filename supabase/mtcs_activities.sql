-- Material de estudio y actividades MTCS para el grupo 511.
-- El contenido didáctico se presenta dentro de cada espacio de trabajo.

create table if not exists public.learning_progress(
  id uuid primary key default uuid_generate_v4(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  material_code text not null,
  completed_steps jsonb not null default '[]'::jsonb,
  completed_at timestamptz,
  updated_at timestamptz not null default now(),
  unique(student_id,material_code)
);
alter table public.learning_progress enable row level security;
drop policy if exists "progress self or staff read" on public.learning_progress;
create policy "progress self or staff read" on public.learning_progress for select to authenticated using(student_id=auth.uid() or public.is_staff());
drop policy if exists "student creates progress" on public.learning_progress;
create policy "student creates progress" on public.learning_progress for insert to authenticated with check(student_id=auth.uid());
drop policy if exists "student updates progress" on public.learning_progress;
create policy "student updates progress" on public.learning_progress for update to authenticated using(student_id=auth.uid()) with check(student_id=auth.uid());

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'MTCS · Material didáctico R.A. 1.1','Comunicación, componentes, conexiones, medios y protocolos de red.','R.A. 1.1','link','mtcs://MTCS-RA-1.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='511'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='mtcs://MTCS-RA-1.1');

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'MTCS · Material didáctico R.A. 1.2','Direccionamiento IPv4, segmentación, puerta de enlace y enrutamiento.','R.A. 1.2','link','mtcs://MTCS-RA-1.2',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='511'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='mtcs://MTCS-RA-1.2');

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'MTCS · Introducción al R.A. 2.1','Primeros fundamentos, principios y controles de ciberseguridad.','R.A. 2.1','link','mtcs://MTCS-RA-2.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='511'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='mtcs://MTCS-RA-2.1');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code)
select teacher.id, groups.id,
  'MTCS · Actividad de evaluación R.A. 1.1',
  'Estudia el material, analiza tu escenario asignado y diseña una red funcional. Puedes guardar tu avance antes de entregar.',
  'published', 'MTCS-RA-1.1'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='511'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status;

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code)
select teacher.id, groups.id,
  'MTCS · Actividad de evaluación R.A. 1.2',
  'Estudia direccionamiento y enrutamiento, resuelve los datos de red asignados y explica tus procedimientos.',
  'published', 'MTCS-RA-1.2'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='511'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status;

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code)
select teacher.id, groups.id,
  'MTCS · Inicio del R.A. 2.1',
  'Revisa los primeros fundamentos de ciberseguridad y analiza el caso asignado.',
  'published', 'MTCS-RA-2.1'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='511'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status;
