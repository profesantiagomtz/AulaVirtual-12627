-- Actividad de evaluación R.A. 2.3 de ASIN para el grupo 310.
-- Se entrega como un solo archivo (DOCX o PDF) y se desbloquea al completar el material integrado.
-- Ejecutar una sola vez en Supabase SQL Editor.

insert into public.assessments(
  teacher_id, group_id, title, instructions, status, activity_code, due_at
)
select teacher.id, groups.id,
  'ASIN · Actividad de evaluación 2.3',
  'Elabora el portafolio de auditoría de la configuración de seguridad de una red (la del laboratorio o la de tu casa, con permiso): 1) informe del balance de resultados con inventario, lista de verificación contra la línea base del plan, porcentaje de cumplimiento y métricas (meta, obtenido y si cumple); 2) informe de nuevos requerimientos y riesgos con tabla de hallazgos (riesgo, requerimiento, medida y prioridad), medidas aplicadas, balance antes y después y un plan de contingencia para dos riesgos con escalamiento por niveles. Entrega un solo archivo PDF o Word.',
  'published', 'ASIN-RA-2.3', '2027-01-09 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='310'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
