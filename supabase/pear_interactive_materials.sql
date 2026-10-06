-- Recorrido didáctico interactivo de PEAR, propósitos 1.1 a 1.4.

with teacher as (
  select id from public.profiles where email='santiago.gonzalez@tam.conalep.edu.mx' limit 1
), target_group as (
  select id from public.groups where code='111' limit 1
), resources(title, description, unit, resource_url) as (
  values
    ('PEAR · Propósito 1.1 · Lógica matemática', 'Teoría, ejemplos, esquemas, ejercicios y práctica final sobre proposiciones y tablas de verdad.', 'Propósito 1.1', 'pear://PEAR-1.1'),
    ('PEAR · Propósito 1.2 · Sistemas de numeración', 'Recorrido guiado por la historia de los números, valor posicional, cero y uso del ábaco.', 'Propósito 1.2', 'pear://PEAR-1.2'),
    ('PEAR · Propósito 1.3 · Números y operaciones', 'Clasificación de números, operaciones, propiedades, factorización, MCD y MCM.', 'Propósito 1.3', 'pear://PEAR-1.3'),
    ('PEAR · Propósito 1.4 · Fracciones, proporciones y porcentajes', 'Explicaciones y práctica aplicada a equivalencias, proporciones y porcentajes.', 'Propósito 1.4', 'pear://PEAR-1.4')
)
insert into public.materials(teacher_id, group_id, title, description, unit, resource_type, resource_url, published)
select teacher.id, target_group.id, resources.title, resources.description, resources.unit, 'link', resources.resource_url, true
from teacher cross join target_group cross join resources
where not exists (
  select 1 from public.materials current_material
  where current_material.group_id=target_group.id and current_material.resource_url=resources.resource_url
);

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, student_group.id,
  'PEAR · Actividad de evaluación 1.4',
  'Realiza la simulación de mercado con los datos asignados. Incluye las operaciones, explica tus decisiones y entrega el reporte completo en un solo archivo PDF.',
  'published', 'PEAR-1.4.1', '2026-10-17 04:59:00+00'
from public.profiles teacher
cross join public.groups student_group
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx' and student_group.code='111'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, due_at=excluded.due_at;
