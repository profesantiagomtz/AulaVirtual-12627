-- Materiales y actividades de evaluación EDOA R.A. 4.1, 4.2 y 4.3 (internet, cliente de correo, correo y mensajería) para el grupo 311.
-- Cada actividad se desbloquea al completar su material. Ejecutar una sola vez en Supabase SQL Editor.

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 4.1','Internet, navegador, descargas seguras, phishing y búsqueda avanzada.','R.A. 4.1','link','courseware://EDOA-RA-4.1',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-4.1');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 4.1',
  'Elabora un trabajo documental (Word o PDF) sobre el tema que elijas (becas, uso de internet en México o cómo evitar fraudes en línea): capturas de la configuración segura de tu navegador (navegación segura, HTTPS y candado), una búsqueda simple y la misma con al menos tres operadores y un filtro, tres fuentes confiables con título, dirección, institución, fecha y por qué confías en ellas, un resumen con tus palabras con las fuentes citadas y tres medidas de seguridad.',
  'published', 'EDOA-RA-4.1', '2026-12-16 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 4.2','Servidores y clientes de correo, SMTP, POP3, IMAP y configuración segura de cuentas.','R.A. 4.2','link','courseware://EDOA-RA-4.2',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-4.2');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 4.2',
  'Elabora un documento ilustrado (Word o PDF) que describa la configuración de un cliente de correo: explica servidor, cliente de software y webmail; incluye una tabla de SMTP, POP3 e IMAP con su puerto seguro; muestra paso a paso con capturas la configuración de entrada, salida, puertos y seguridad (tapa tu contraseña), la prueba de envío y por qué elegiste ese protocolo.',
  'published', 'EDOA-RA-4.2', '2026-12-19 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;

insert into public.materials(teacher_id,group_id,title,description,unit,resource_type,resource_url,published)
select p.id,g.id,'EDOA · Material didáctico R.A. 4.3','Enviar, recibir y organizar correo con responsabilidad, y mensajería instantánea.','R.A. 4.3','link','courseware://EDOA-RA-4.3',true
from public.profiles p cross join public.groups g
where p.email='santiago.gonzalez@tam.conalep.edu.mx' and g.code='311'
  and not exists(select 1 from public.materials m where m.group_id=g.id and m.resource_url='courseware://EDOA-RA-4.3');

insert into public.assessments(teacher_id, group_id, title, instructions, status, activity_code, due_at)
select teacher.id, groups.id,
  'EDOA · Actividad de evaluación R.A. 4.3',
  'Entrega en un solo PDF el historial impreso de envío y recepción: un correo con Para, CC, CCO, asunto, formato, adjunto y acuses; una respuesta, una respuesta a todos y un reenvío con tu firma y disclaimer; capturas de tu carpeta con filtro y de la bandeja ordenada; capturas de un grupo de mensajería con tu estado y una llamada, sin datos personales, y tus cinco reglas de comunicación responsable.',
  'published', 'EDOA-RA-4.3', '2027-01-09 05:59:00+00'
from public.profiles teacher
cross join public.groups groups
where teacher.email='santiago.gonzalez@tam.conalep.edu.mx'
  and groups.code='311'
on conflict (activity_code, group_id) where activity_code is not null
do update set title=excluded.title, instructions=excluded.instructions, status=excluded.status, due_at=excluded.due_at;
