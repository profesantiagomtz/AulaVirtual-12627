-- Materiales y actividades PEAR para el grupo 111.
-- Ejecutar después de msii_activity.sql.

insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values (
  'materials','materials',false,20971520,
  array[
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ]
)
on conflict (id) do update set
  public=false,
  file_size_limit=excluded.file_size_limit,
  allowed_mime_types=excluded.allowed_mime_types;

drop policy if exists "staff uploads materials" on storage.objects;
create policy "staff uploads materials" on storage.objects
  for insert to authenticated
  with check (bucket_id='materials' and public.is_staff());

drop policy if exists "assigned users download materials" on storage.objects;
create policy "assigned users download materials" on storage.objects
  for select to authenticated
  using (bucket_id='materials');

update storage.buckets
set public=false,
    file_size_limit=20971520,
    allowed_mime_types=array[
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
where id='submissions';

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code
)
select teacher.id, groups.id,
  'PEAR · Actividad de evaluación 1.1',
  'Analiza el caso asignado, construye las tablas de verdad solicitadas y entrega en PDF tu postura fundamentada.',
  'published', 'PEAR-1.1.1'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='111'
on conflict (activity_code, group_id) where activity_code is not null
do update set
  title=excluded.title,
  instructions=excluded.instructions;

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'PEAR · Actividad de evaluación 1.2',
  'Construye tu ábaco, realiza la operación asignada y entrega en un solo PDF la explicación y las fotografías solicitadas.',
  'published', 'PEAR-1.2.1', '2026-10-06 04:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='111'
on conflict (activity_code, group_id) where activity_code is not null
do update set
  title=excluded.title,
  instructions=excluded.instructions,
  status=excluded.status,
  due_at=excluded.due_at;

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'PEAR · Actividad de evaluación 1.3',
  'Elabora el reporte de presupuesto con los datos asignados, muestra tus procedimientos y entrega el trabajo en un solo archivo PDF.',
  'published', 'PEAR-1.3.1', '2026-10-06 04:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='111'
on conflict (activity_code, group_id) where activity_code is not null
do update set
  title=excluded.title,
  instructions=excluded.instructions,
  status=excluded.status,
  due_at=excluded.due_at;
