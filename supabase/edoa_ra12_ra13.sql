-- EDOA R.A. 1.2 y 1.3: cambia al material integrado con pestañas Aprende / Diagnostica / Construye.
-- Ejecutar una sola vez en Supabase SQL Editor.
update public.materials set resource_url='courseware://EDOA-RA-1.2' where resource_url='edoa://EDOA-RA-1.2';
update public.materials set resource_url='courseware://EDOA-RA-1.3' where resource_url='edoa://EDOA-RA-1.3';

select title, resource_url from public.materials where resource_url like 'courseware://EDOA-RA-%';
