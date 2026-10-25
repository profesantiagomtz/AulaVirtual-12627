-- Material y actividad de evaluación MTCS R.A. 3.1 para el grupo 511.
-- La actividad se desbloquea al completar el material. Ejecutar una sola vez en Supabase SQL Editor.

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'MTCS · Material didáctico R.A. 3.1','Conceptos de programación, lenguajes, variables, tipos de datos, operadores y herramientas en Python.','R.A. 3.1','link','courseware://MTCS-RA-3.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='511'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://MTCS-RA-3.1');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'MTCS · Actividad de evaluación R.A. 3.1',
  'Elabora un reporte en PDF que demuestre el uso de fundamentos y lenguajes de programación en el sistema asignado: conceptos, lenguaje y herramientas, variables y tipos de datos, operadores con los datos asignados y errores corregidos. Incluye tu código en Python y capturas de la salida.',
  'published', 'MTCS-RA-3.1', '2026-12-05 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='511'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
