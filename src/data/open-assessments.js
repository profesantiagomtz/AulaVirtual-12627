// Apertura de emergencia: actividades de evaluación que se muestran desbloqueadas a TODO el grupo,
// aunque el alumno no haya terminado el material. No cambia su avance ni marca nada como hecho.
// Para volver a bloquearlas, borra la entrada (o deja la lista vacía).
export const OPEN_ASSESSMENTS = {
  // 2026-11-09: Profe autorizó abrir la evaluación 1.2 de ASIN y MSII al 310.
  '310': ['ASIN-RA-1.2', 'MSII-RA-1.2'],
}

export function assessmentForcedOpen(activityCode = '', group = '') {
  return Boolean(OPEN_ASSESSMENTS[String(group)]?.includes(activityCode))
}
