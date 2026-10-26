-- Actividad de evaluación R.A. 2.2 de ASIN para el grupo 310.
-- Se entrega como un solo archivo (DOCX o PDF) y se desbloquea al completar el material integrado.
-- Ejecutar una sola vez en Supabase SQL Editor.

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'ASIN · Actividad de evaluación 2.2',
  'Elabora el portafolio de evidencias del seguimiento de las herramientas de seguridad de la Papelería Don Beto: reporte del estado de las aplicaciones, reporte de modificación de configuraciones (control de cambios) y respaldo digital de configuraciones, siguiendo la lista de cotejo del material R.A. 2.2. Entrega un solo archivo PDF o Word.',
  'published', 'ASIN-RA-2.2', '2026-12-08 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
