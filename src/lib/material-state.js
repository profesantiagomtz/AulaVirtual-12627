// Estado completo del material interactivo (respuestas, secciones abiertas, simuladores).
// Cada material lo guarda en localStorage con la clave «<material>-avance-<alumno>» y variantes
// «…-py-1», «…-xl-2», etc. Aquí se copia a Supabase para que el alumno lo recupere al
// volver a entrar en otro equipo o en una PC que borra los datos del navegador al cerrar.

const SYNC_MARK = 'aula-sync:'

export function materialStatePrefix(file, studentId) {
  const base = String(file).split('/').pop().replace(/-material\.html$/, '')
  return `${base}-avance-${studentId}`
}

// Devuelve { sufijo: valor } con todo lo que el material guardó bajo su clave.
export function readMaterialState(prefix) {
  const state = {}
  try {
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index)
      if (key && key.startsWith(prefix)) state[key.slice(prefix.length)] = localStorage.getItem(key)
    }
  } catch { /* sin almacenamiento: no hay nada que copiar */ }
  return state
}

export function writeMaterialState(prefix, state) {
  if (!state || typeof state !== 'object') return false
  try {
    for (const [suffix, value] of Object.entries(state)) if (typeof value === 'string') localStorage.setItem(prefix + suffix, value)
    return true
  } catch { return false }
}

// Marca de la última versión que este navegador comparte con Supabase.
export function lastSynced(prefix) {
  try { return localStorage.getItem(SYNC_MARK + prefix) || '' } catch { return '' }
}

export function markSynced(prefix, timestamp) {
  try { if (timestamp) localStorage.setItem(SYNC_MARK + prefix, timestamp) } catch { /* sin almacenamiento */ }
}

export function hasState(state) {
  return Boolean(state && typeof state === 'object' && Object.keys(state).length)
}

// La copia en la nube gana si es más reciente que lo último que este navegador sincronizó
// (otro equipo avanzó) o si aquí no hay nada guardado (el navegador se limpió).
export function shouldRestore(prefix, remote) {
  if (!hasState(remote?.state)) return false
  if (!hasState(readMaterialState(prefix))) return true
  const mark = lastSynced(prefix)
  return !mark || new Date(remote.updated_at) > new Date(mark)
}

// Cuántos pasos marca como hechos el estado guardado. Los materiales guardan cada actividad
// resuelta con su número («"12":1») y cada práctica terminada como «"pr1":1»; es la misma
// cuenta que envían como «done» a la plataforma.
export function countDone(state) {
  if (!hasState(state)) return 0
  let main
  try { main = typeof state[''] === 'string' ? JSON.parse(state['']) : null } catch { main = null }
  if (!main || typeof main !== 'object') return 0
  return Object.entries(main).filter(([key, value]) => /^(\d+|pr\d+)$/.test(key) && (value === 1 || value === true)).length
}

// El panel docente cuenta los pasos de completed_steps. Si el alumno trabajó con el material
// en pantalla completa, el estado se respaldó pero el conteo no: se toma el mayor de los dos.
export function withStateSteps(rows) {
  return (rows || []).map(({ state, ...row }) => {
    const steps = Array.isArray(row.completed_steps) ? row.completed_steps : []
    const done = countDone(state)
    return done > steps.length ? { ...row, completed_steps: Array.from({ length: done }, (_, index) => `paso-${index + 1}`) } : row
  })
}
