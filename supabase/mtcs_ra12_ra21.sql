-- MTCS R.A. 1.2 y 2.1: cambia al material integrado con pestañas Aprende / Diagnostica / Construye.
-- Ejecutar una sola vez en Supabase SQL Editor.
update public.materials set resource_url='courseware://MTCS-RA-1.2' where resource_url='mtcs://MTCS-RA-1.2';
update public.materials set resource_url='courseware://MTCS-RA-2.1' where resource_url='mtcs://MTCS-RA-2.1';

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'MTCS · Material didáctico R.A. 2.1','Principios, amenazas, ataques y protección en ciberseguridad.','R.A. 2.1','link','courseware://MTCS-RA-2.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='511'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://MTCS-RA-2.1');

select title, resource_url from public.materials where resource_url like 'courseware://MTCS-RA-%';
