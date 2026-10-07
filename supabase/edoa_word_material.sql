-- Material interactivo de Word 2019 para EDOA, grupo 311.
with teacher as (
  select id from public.profiles where email='santiago.gonzalez@tam.conalep.edu.mx' limit 1
), target_group as (
  select id from public.groups where code='311' limit 1
)
insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select teacher.id,target_group.id,
  'EDOA · Word 2019 · Unidad 1',
  'Fichas visuales y actividades prácticas sobre interfaz, diseño, formato, objetos, referencias y APA.',
  'R.A. 1.1 y 1.2',
  'link',
  'edoa://EDOA-WORD-U1',
  true
from teacher cross join target_group
where not exists (
  select 1 from public.materials current_material
  where current_material.group_id=target_group.id and current_material.resource_url='edoa://EDOA-WORD-U1'
);
