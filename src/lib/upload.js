import { supabase } from './supabase'

const networkProblem = error => /failed to fetch|networkerror|load failed|network request failed|fetch failed/i.test(error?.message || '') || error?.name === 'TypeError' || error?.name === 'StorageUnknownError'
const wait = ms => new Promise(resolve => setTimeout(resolve, ms))

// Sube un archivo de entrega al bucket privado "submissions".
// Lee el archivo una sola vez (evita fallas si el alumno lo vuelve a guardar después de elegirlo)
// y reintenta cuando la conexión se corta, que es lo que el navegador reporta como "Failed to fetch".
export async function uploadSubmissionFile(path, file, contentType = file.type || 'application/octet-stream') {
  let bytes
  try { bytes = await file.arrayBuffer() } catch {
    throw new Error('No se pudo leer el archivo. Ciérralo en el programa donde lo tienes abierto (por ejemplo Packet Tracer), vuelve a elegirlo e inténtalo de nuevo. Si está en OneDrive, cópialo primero al Escritorio.')
  }
  const body = new Blob([bytes], { type: contentType })
  let lastError
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const { error } = await supabase.storage.from('submissions').upload(path, body, { upsert: true, contentType })
      if (!error) return { bytes }
      if (!networkProblem(error)) throw error
      lastError = error
    } catch (error) {
      if (!networkProblem(error)) throw error
      lastError = error
    }
    await wait(1500 * (attempt + 1))
  }
  console.warn('Fallo de red al subir', lastError)
  throw new Error('Se cortó la conexión mientras se subía el archivo. Revisa tu internet e inténtalo otra vez. Si sigue fallando, prueba con datos del celular o desde otra red: algunas redes escolares bloquean la subida de archivos.')
}
