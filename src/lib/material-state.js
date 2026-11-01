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
