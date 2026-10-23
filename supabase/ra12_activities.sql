-- Actividades de evaluación R.A. 1.2 de ASIN y MSII para el grupo 310.
-- Se entregan como un solo archivo (DOCX o PDF) y se desbloquean al completar el material integrado.
-- Ejecutar una sola vez en Supabase SQL Editor.

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code
)
select teacher.id, groups.id,
  'ASIN · Actividad de evaluación 1.2',
  'Elabora el plan de seguridad informática y las políticas de seguridad de la organización que elegiste, siguiendo las instrucciones y la lista de cotejo del material R.A. 1.2. Junta ambas evidencias (Plan de seguridad a implementar y Políticas de seguridad a implementar) en un solo archivo PDF o Word.',
  'published', 'ASIN-RA-1.2'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set
  title=excluded.title,
  instructions=excluded.instructions;

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code
)
select teacher.id, groups.id,
  'MSII · Actividad de evaluación 1.2',
  'Instala y documenta tres periféricos, describe y valida las unidades funcionales y crea tus respaldos, siguiendo las instrucciones y la lista de cotejo del material R.A. 1.2. Junta las tres evidencias (procedimiento de instalación, descripción de unidades funcionales y soportes de información) en un solo archivo PDF o Word.',
  'published', 'MSII-RA-1.2'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set
  title=excluded.title,
  instructions=excluded.instructions;
