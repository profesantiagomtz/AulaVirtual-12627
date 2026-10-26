-- Material y actividad de evaluación EDOA R.A. 3.4 (tablas dinámicas y protección) para el grupo 311.
-- La actividad se desbloquea al completar el material. Ejecutar una sola vez en Supabase SQL Editor.

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 3.4','Tablas y gráficos dinámicos, vista preliminar y protección de hojas y libros.','R.A. 3.4','link','courseware://EDOA-RA-3.4',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-3.4');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 3.4',
  'Elabora un reporte ejecutivo en Excel con una lista de al menos 24 registros: una tabla dinámica con filtro, formato de moneda y orden; una segunda tabla con dos niveles de filas, promedio o cuenta y subtotales; un gráfico dinámico con la hoja lista para imprimir y tres conclusiones. Protege el libro: desbloquea solo las celdas de captura, protege la hoja sin permitir formato, protege la estructura y cifra el archivo con contraseña. Cifra el archivo con la contraseña de apertura EDOA34-311 y anota en una hoja «Evidencias» las contraseñas de la hoja y del libro. Entrega el archivo .xlsx.',
  'published', 'EDOA-RA-3.4', '2026-12-10 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
