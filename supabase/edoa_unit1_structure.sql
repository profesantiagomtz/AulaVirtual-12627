-- Separa la Unidad 1 de EDOA por resultado de aprendizaje.
with teacher as (
  select id from public.profiles where email='santiago.gonzalez@tam.conalep.edu.mx' limit 1
), target_group as (
  select id from public.groups where code='311' limit 1
)
update public.materials m
set title='EDOA · Material didáctico R.A. 1.1',
    description='Opciones, diseño de página, formato, plantillas y respaldo de documentos.',
    unit='R.A. 1.1', resource_url='edoa://EDOA-RA-1.1'
from target_group g
where m.group_id=g.id and m.resource_url in ('edoa://EDOA-WORD-U1','edoa://EDOA-RA-1.1');

with teacher as (
  select id from public.profiles where email='santiago.gonzalez@tam.conalep.edu.mx' limit 1
), target_group as (
  select id from public.groups where code='311' limit 1
)
insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select teacher.id,target_group.id,title,description,unit,'link',url,true
from teacher cross join target_group cross join (values
  ('EDOA · Material didáctico R.A. 1.2','Tablas, imágenes, objetos de referencia y formato de objetos.','R.A. 1.2','edoa://EDOA-RA-1.2'),
  ('EDOA · Material didáctico R.A. 1.3','Combinación de correspondencia, revisión, control de cambios y protección.','R.A. 1.3','edoa://EDOA-RA-1.3')
) as resources(title,description,unit,url)
where not exists(select 1 from public.materials m where m.group_id=target_group.id and m.resource_url=resources.url);

with teacher as (
  select id from public.profiles where email='santiago.gonzalez@tam.conalep.edu.mx' limit 1
), target_group as (
  select id from public.groups where code='311' limit 1
)
insert into public.assessments(teacher_id,group_id,title,instructions,activity_code,status)
select teacher.id,target_group.id,title,instructions,code,'published'
from teacher cross join target_group cross join (values
  ('EDOA · Actividad de evaluación R.A. 1.2','Elabora un documento digital con tablas, imágenes, referencias y objetos correctamente formateados.','EDOA-RA-1.2'),
  ('EDOA · Actividad de evaluación R.A. 1.3','Elabora documentos mediante combinación de correspondencia y demuestra el uso de revisión y control de cambios.','EDOA-RA-1.3'),
  ('EDOA · Evaluación general de la Unidad 1','Integra en un solo producto las habilidades desarrolladas en los R.A. 1.1, 1.2 y 1.3.','EDOA-UNIT-1')
) as activities(title,instructions,code)
on conflict (activity_code,group_id) where activity_code is not null
do update set title=excluded.title,instructions=excluded.instructions,status=excluded.status;

update public.assessments
set title='EDOA · Actividad de evaluación R.A. 1.1',
    instructions='Elabora un documento con opciones, diseño de página, formato, estilos o plantillas y respaldo.'
where activity_code='EDOA-RA-1.1'
  and group_id=(select id from public.groups where code='311' limit 1);
