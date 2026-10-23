-- Retira PEAR de AulaVirtual (ahora vive en plataforma-pear).
-- No borra nada: oculta materiales, cierra evaluaciones y desactiva el grupo 111
-- para que no aparezca en registros nuevos. Las entregas anteriores se conservan.
update public.materials set published = false where resource_url like 'pear://%';
update public.assessments set status = 'closed' where activity_code like 'PEAR-%';
update public.groups set active = false where code = '111';

-- Revisión: cuántas cuentas de alumnos del grupo 111 quedan en esta plataforma.
select count(*) as alumnos_111 from public.profiles p join public.groups g on g.id = p.group_id where g.code = '111';
