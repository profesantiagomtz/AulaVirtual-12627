-- Evaluaciones MTCS 1.2 y 2.1 sencillas: permitir que el alumno suba la foto de su cuaderno (JPG, PNG, WEBP, HEIC).
update storage.buckets
set allowed_mime_types = (
  select array_agg(distinct mime) from unnest(coalesce(allowed_mime_types, '{}') || array['image/jpeg', 'image/png', 'image/webp', 'image/heic']) as mime
)
where id = 'submissions';
