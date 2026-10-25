-- Material y actividad de evaluación EDOA R.A. 3.2 (cálculos y funciones) para el grupo 311.
-- La actividad se desbloquea al completar el material. Ejecutar una sola vez en Supabase SQL Editor.

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 3.2','Fórmulas básicas, referencias, nombres y funciones de varias categorías.','R.A. 3.2','link','courseware://EDOA-RA-3.2',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-3.2');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 3.2',
  'Elabora un libro de trabajo con datos de una situación real (por ejemplo, el inventario y las ventas de una tienda o los gastos de tu grupo) que calcule solo, sin cuentas hechas a mano. Incluye: fórmulas con operadores matemáticos y de comparación, referencias relativas y absolutas o mixtas, al menos un rango con nombre y una fórmula con datos de otra hoja, y funciones de varias categorías (SUMA, PROMEDIO, MAX, MIN, CONTAR.SI, SUMAR.SI, HOY, una de texto, BUSCARV y SI). Entrega el archivo .xlsx (o su PDF) y la versión impresa en clase, con una hoja que muestre las fórmulas.',
  'published', 'EDOA-RA-3.2', '2026-11-21 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
