-- Actividad de evaluación R.A. 2.2 de MSII para el grupo 310.
-- Se entrega como un solo archivo (DOCX o PDF) y se desbloquea al completar el material integrado.
-- Ejecutar una sola vez en Supabase SQL Editor.

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'MSII · Actividad de evaluación 2.2',
  'Realiza la sesión práctica en Linux de la sucursal del Cibercafé Nova (archivos, discos, usuarios y permisos, programas, procesos y memoria) y entrega el reporte de la sesión con capturas explicadas y el listado de comandos ejecutados, siguiendo la lista de cotejo del material R.A. 2.2. Entrega un solo archivo PDF o Word.',
  'published', 'MSII-RA-2.2', '2027-01-09 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
