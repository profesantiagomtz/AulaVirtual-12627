-- Habilita entregas de prácticas de Cisco Packet Tracer en el bucket privado existente.
-- Los archivos conservan las mismas políticas: cada alumno escribe en su carpeta y el docente puede leerlos.

update storage.buckets
set file_size_limit = 20971520,
    allowed_mime_types = array[
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/pdf',
      'application/octet-stream',
      'application/x-pkt',
      'application/vnd.cisco.packet-tracer'
    ]
where id = 'submissions';

