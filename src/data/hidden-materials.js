// Materiales cerrados: R.A. cuyo material didáctico YA NO ven los alumnos del grupo.
// El docente lo sigue viendo (marcado «Cerrado al alumno»); no se borra avance, entregas ni calificaciones.
// Para volver a mostrar un material, borra su código de la lista.
export const HIDDEN_MATERIALS = {
  // 2026-11-12: Profe pidió dejar visible solo el R.A. 2.1 de ASIN y MSII.
  '310': ['ASIN-RA-1.1', 'ASIN-RA-1.2', 'MSII-RA-1.1', 'MSII-RA-1.2'],
  // 2026-11-12: Profe pidió dejar visible solo el R.A. 2.1 de EDOA.
  '311': ['EDOA-RA-1.1', 'EDOA-RA-1.2', 'EDOA-RA-1.3'],
  // 2026-11-12/13: Profe pidió dejar visible solo el R.A. 2.2 de MTCS (también se ocultan 3.1 y 3.2 por ahora).
  '511': ['MTCS-RA-1.1', 'MTCS-RA-1.2', 'MTCS-RA-2.1', 'MTCS-RA-3.1', 'MTCS-RA-3.2'],
}

// Código «MATERIA-RA-x.y» de un material: por su enlace integrado o, si es un archivo, por su título y unidad.
export function materialRaCode(material = {}) {
  const url = String(material.url || '')
  if (url === 'edoa://EDOA-WORD-U1') return 'EDOA-RA-1.1'
  const linked = url.match(/^(?:mtcs|edoa|courseware):\/\/([A-Z]{4}-RA-\d\.\d)/)
  if (linked) return linked[1]
  const course = String(material.title || '').match(/\b(ASIN|MSII|EDOA|MTCS)\b/)
  const ra = `${material.unit || ''} ${material.title || ''}`.match(/R\.?\s?A\.?\s*(\d)\.(\d)/i)
  return course && ra ? `${course[1]}-RA-${ra[1]}.${ra[2]}` : null
}

export function materialClosedFor(material = {}, group = material.group) {
  const code = materialRaCode(material)
  return Boolean(code && HIDDEN_MATERIALS[String(group)]?.includes(code))
}

// Una actividad cuyo material ya se cerró: el alumno no puede ir a terminarlo.
export function activityMaterialClosed(activityCode = '', group = '') {
  const hidden = HIDDEN_MATERIALS[String(group)] || []
  // La evaluación de la Unidad 1 de EDOA depende de terminar los materiales 1.1, 1.2 y 1.3.
  if (activityCode === 'EDOA-UNIT-1') return ['EDOA-RA-1.1', 'EDOA-RA-1.2', 'EDOA-RA-1.3'].some(code => hidden.includes(code))
  const code = String(activityCode).match(/^([A-Z]{4}-RA-\d\.\d)/)?.[1]
  return Boolean(code && hidden.includes(code))
}

// Al alumno se le entrega el material cerrado como no publicado; el docente conserva el estado real.
export function applyClosedMaterials(materials, isTeacher) {
  return materials.map(material => {
    const closed = materialClosedFor(material)
    return { ...material, closed, studentVisible: Boolean(material.published) && !closed, published: isTeacher ? material.published : Boolean(material.published) && !closed }
  })
}
