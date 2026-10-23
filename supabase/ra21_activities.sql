-- Actividades de evaluación R.A. 2.1 de ASIN y MSII para el grupo 310.
-- Se entregan como un solo archivo (DOCX o PDF) y se desbloquean al completar el material integrado.
-- Ejecutar una sola vez en Supabase SQL Editor.

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'ASIN · Actividad de evaluación 2.1',
  'Elabora el manual de instalación y configuración de software: requerimientos, procedimiento de instalación, configuración local de seguridad, configuración de red, verificación y problemas comunes, siguiendo la lista de cotejo del material R.A. 2.1. Entrega un solo archivo PDF o Word.',
  'published', 'ASIN-RA-2.1', '2026-11-20 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'MSII · Actividad de evaluación 2.1',
  'Realiza la sesión práctica del Cibercafé Nova con CMD y PowerShell y entrega el reporte de la sesión con capturas explicadas y el listado de comandos ejecutados, siguiendo la lista de cotejo del material R.A. 2.1. Entrega un solo archivo PDF o Word.',
  'published', 'MSII-RA-2.1', '2026-11-14 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
