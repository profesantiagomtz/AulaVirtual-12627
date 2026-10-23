-- Material y actividad de evaluación EDOA R.A. 3.1 (formato del libro y la hoja de cálculo) para el grupo 311.
-- La actividad se desbloquea al completar el material. Ejecutar una sola vez en Supabase SQL Editor.

-- Permite entregar libros de Excel (.xlsx) sin quitar los formatos que ya estaban permitidos.
update storage.buckets
set allowed_mime_types = array(
  select distinct unnest(coalesce(allowed_mime_types, '{}') || array['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
)
where id = 'submissions';

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 3.1','Elementos del libro, opciones de la hoja, diseño de página y formato de celdas.','R.A. 3.1','link','edoa://EDOA-RA-3.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='edoa://EDOA-RA-3.1');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 3.1',
  'Da formato a un libro de trabajo con datos de una situación real (por ejemplo, el control de gastos de tu grupo o el inventario de una tienda). Incluye: título con celdas combinadas, encabezados con relleno y bordes, columnas ajustadas, formato de número (moneda, porcentaje o fecha), hojas con nombre, orientación y márgenes adecuados, y encabezado y pie de página con tu nombre, grupo y número de página. Entrega el archivo .xlsx (o su PDF) y la versión impresa en clase.',
  'published', 'EDOA-RA-3.1', '2026-11-04 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
