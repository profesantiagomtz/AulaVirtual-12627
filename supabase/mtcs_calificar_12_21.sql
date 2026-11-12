-- MTCS 511: guarda el % final (R.A. 1.2 + 2.1, pesos 15/20) como calificación de AMBAS evaluaciones.
-- La calificación se guarda sobre 60 (escala de la plataforma): 100 % = 60.
-- Solo toca entregas ya enviadas de MTCS-RA-1.2 y MTCS-RA-2.1 del grupo 511.
update public.submissions s set score = v.score
from (values
  ('alopez0424@tam.conalep.edu.mx', 57.43),  -- 95.7 %
  ('apuente0524@conaleptamaulipas.edu.mx', 60.0),  -- 100.0 %
  ('amargil2724@tam.conalep.edu.mx', 55.89),  -- 93.1 %
  ('fcastillo2724@tam.conalep.edu.mx', 60.0),  -- 100.0 %
  ('flopez2824@tam.conalep.edu.mx', 27.43),  -- 45.7 %
  ('jtrevino2724@tam.conalep.edu.mx', 53.14),  -- 88.6 %
  ('lmuniz2723@conaleptamaulipas.edu.mx', 47.66),  -- 79.4 %
  ('mmartinez0324@tam.conalep.edu.mx', 34.29),  -- 57.1 %
  ('msantiago2124@tam.conalep.edu.mx', 53.14),  -- 88.6 %
  ('osanchez2824@tam.conalep.edu.mx', 60.0),  -- 100.0 %
  ('rmuniz1222@tam.conalep.edu.mx', 49.03),  -- 81.7 %
  ('uromero1624@tam.conalep.edu.mx', 53.14)  -- 88.6 %
) as v(email, score),
public.profiles p, public.assessments a, public.groups g
where p.email = v.email and s.student_id = p.id
  and s.assessment_id = a.id and a.group_id = g.id and g.code = '511'
  and a.activity_code in ('MTCS-RA-1.2','MTCS-RA-2.1')
  and s.submitted_at is not null;

-- Verificación
select p.full_name, a.activity_code, s.score, round(s.score/60*100,1) as porcentaje
from public.submissions s join public.profiles p on p.id=s.student_id
join public.assessments a on a.id=s.assessment_id join public.groups g on g.id=a.group_id
where g.code='511' and a.activity_code in ('MTCS-RA-1.2','MTCS-RA-2.1')
order by p.full_name, a.activity_code;
