-- Ajustes de productos finales MTCS y formatos permitidos para sus entregas.

update storage.buckets
set file_size_limit = 20971520,
    allowed_mime_types = array[
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      'application/pdf',
      'application/octet-stream',
      'application/x-pkt',
      'application/vnd.cisco.packet-tracer'
    ]
where id = 'submissions';

update public.assessments
set title = 'MTCS · Actividad de evaluación R.A. 1.1',
    instructions = 'Crea en Packet Tracer el diagrama de la red asignada, comprueba su funcionamiento y explica tus decisiones en la plataforma.'
where activity_code = 'MTCS-RA-1.1';

update public.assessments
set title = 'MTCS · Actividad de evaluación R.A. 1.2',
    instructions = 'Elabora y entrega un reporte en PDF sobre el direccionamiento y enrutamiento de la red asignada.'
where activity_code = 'MTCS-RA-1.2';

update public.assessments
set title = 'MTCS · Actividad de evaluación R.A. 2.1',
    instructions = 'Elabora una presentación electrónica sobre los fundamentos de ciberseguridad aplicados al caso asignado y entrégala como PPTX o PDF.'
where activity_code = 'MTCS-RA-2.1';

