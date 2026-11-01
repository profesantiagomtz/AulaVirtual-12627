-- Guarda en la nube el estado completo de cada material interactivo (respuestas, secciones
-- abiertas y simuladores) para que el alumno lo recupere al volver a entrar desde cualquier PC.
-- Solo agrega una columna; no borra ni cambia datos. Las políticas RLS existentes ya la cubren.
alter table public.learning_progress add column if not exists state jsonb;
