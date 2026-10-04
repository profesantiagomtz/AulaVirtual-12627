-- Permite al personal docente registrar o corregir la calificación de una entrega.
drop policy if exists "staff grades submissions" on public.submissions;
create policy "staff grades submissions" on public.submissions
for update to authenticated
using (public.is_staff())
with check (public.is_staff());

