-- Materiales y actividades de evaluación EDOA R.A. 2.1 y 2.2 (presentaciones electrónicas) para el grupo 311.
-- Las actividades se desbloquean al completar cada material. Se publican sin fecha límite (son de recuperación);
-- si quieres ponerles fecha, cambia null por la fecha, por ejemplo '2026-11-07 05:59:00+00'.
-- Ejecutar una sola vez en Supabase SQL Editor.

-- Permite entregar presentaciones de PowerPoint (.pptx) sin quitar los formatos que ya estaban permitidos.
update storage.buckets
set allowed_mime_types = array(
  select distinct unnest(coalesce(allowed_mime_types, '{}') || array['application/vnd.openxmlformats-officedocument.presentationml.presentation'])
)
where id = 'submissions';

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,m.title,m.description,m.unit,'link',m.url,true
from public.profiles p cross join public.groups g
cross join (values
  ('EDOA · Material didáctico R.A. 2.1','Entorno de PowerPoint, diseño de diapositiva, formato y plantillas.','R.A. 2.1','courseware://EDOA-RA-2.1'),
  ('EDOA · Material didáctico R.A. 2.2','Objetos, formato de objeto, animaciones y transiciones.','R.A. 2.2','courseware://EDOA-RA-2.2')
) as m(title,description,unit,url)
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials x where x.group_id=g.id and x.resource_url=m.url);

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id, a.title, a.instructions, 'published', a.code, null
from public.profiles teacher
cross join public.groups groups
cross join (values
  ('EDOA · Actividad de evaluación R.A. 2.1',
   'Elabora una presentación de al menos 6 diapositivas (Feria de Carreras o el tema que te asigne tu docente) con: tamaño 16:9 y fondo uniforme, diseño de diapositiva adecuado en cada una, máximo dos fuentes legibles, viñetas, alineación e interlineado, notas del orador, un tema y el patrón de diapositivas con logotipo y pie. Entrega el archivo .pptx (o PDF).',
   'EDOA-RA-2.1'),
  ('EDOA · Actividad de evaluación R.A. 2.2',
   'Completa tu presentación con: una tabla con diseño, al menos dos imágenes con texto alternativo, hipervínculos a una página web y a otra diapositiva, video o audio y otro objeto (documento, hoja de cálculo o presentación), formato de objeto (tamaño, relleno y posición), animaciones con propósito y una transición pareja con intervalos. Entrega el archivo .pptx de máximo 20 MB.',
   'EDOA-RA-2.2')
) as a(title, instructions, code)
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status;

select title, resource_url from public.materials where resource_url like 'courseware://EDOA-RA-2.%';
