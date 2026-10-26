-- Material y actividad de evaluación EDOA R.A. 3.3 (gráficas y macros) para el grupo 311.
-- La actividad se desbloquea al completar el material. Ejecutar una sola vez en Supabase SQL Editor.

-- Permite entregar libros con macros (.xlsm) sin quitar los formatos que ya estaban permitidos.
update storage.buckets
set allowed_mime_types = array(
  select distinct unnest(coalesce(allowed_mime_types, '{}') || array['application/vnd.ms-excel.sheet.macroEnabled.12'])
)
where id = 'submissions';

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 3.3','Gráficas (tipos, elementos, diseño y edición) y macros con referencias absolutas y relativas.','R.A. 3.3','link','courseware://EDOA-RA-3.3',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-3.3');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 3.3',
  'Elabora un libro de trabajo con los datos de la cafetería (o de una situación real) que incluya: una gráfica de columnas con título, títulos de ejes, leyenda y etiquetas; una gráfica circular con porcentajes; una gráfica de líneas en hoja nueva, cada una con su conclusión; una macro con referencias absolutas probada en otra hoja y una macro con referencias relativas, con la captura del código de una macro modificada y explicada. Entrega el archivo .xlsm (o .xlsx/PDF con capturas si no tuviste computadora) y la versión impresa en clase.',
  'published', 'EDOA-RA-3.3', '2026-12-03 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
