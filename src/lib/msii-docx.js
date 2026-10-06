import JSZip from 'jszip'

const TEMPLATE_URL = `${import.meta.env.BASE_URL}templates/AE_1_1_MSII.docx`

function xmlEscape(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function replaceTokens(xml, values) {
  return Object.entries(values).reduce(
    (result, [key, value]) => result.replaceAll(`{{${key}}}`, xmlEscape(value)),
    xml,
  )
}

export async function buildMsiiDocument(assignment, student) {
  const response = await fetch(TEMPLATE_URL)
  if (!response.ok) throw new Error('No fue posible descargar la plantilla de MSII')
  const zip = await JSZip.loadAsync(await response.arrayBuffer())
  const values = {
    ASSIGNMENT_ID: assignment.id,
    ALUMNO: student.name,
    FECHA: new Date().toLocaleDateString('es-MX'),
    GRUPO: student.group,
    EQUIPO: assignment.variant.equipment,
    SO_COMPARAR: assignment.variant.compare_os,
    DECIMAL: assignment.variant.decimal_number,
    ASCII: assignment.variant.ascii_character,
    CAPACIDAD: assignment.variant.capacity,
  }
  for (const path of ['word/document.xml', 'docProps/custom.xml']) {
    const file = zip.file(path)
    if (!file) throw new Error('La plantilla no está disponible. Intenta nuevamente.')
    zip.file(path, replaceTokens(await file.async('string'), values))
  }
  return zip.generateAsync({ type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
}

export async function readAssignmentId(file) {
  const zip = await JSZip.loadAsync(file)
  const custom = zip.file('docProps/custom.xml')
  if (!custom) return null
  const xml = await custom.async('string')
  const match = xml.match(/name="AulaAssignmentId"[\s\S]*?<vt:lpwstr>([^<]+)<\/vt:lpwstr>/)
  return match?.[1]?.trim() || null
}

export async function analyzeMsiiDocument(file, assignment = {}) {
  const zip = await JSZip.loadAsync(file)
  const documentFile = zip.file('word/document.xml')
  if (!documentFile) throw new Error('El archivo no contiene un documento de Word válido.')
  const xml = await documentFile.async('string')
  const text = xml
    .replace(/<w:tab\/>/g, ' ')
    .replace(/<\/w:p>/g, '\n')
    .replace(/<\/w:tr>/g, '\n')
    .replace(/<[^>]+>/g, '')
    .replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&quot;', '"').replaceAll('&apos;', "'")
    .replace(/[ \t]+/g, ' ').replace(/\n+/g, '\n').trim()
  const remainingPlaceholders = (text.match(/Escribe aqu[ií]/gi) || []).length
  const initialPlaceholders = 30
  const completedFields = Math.max(0, initialPlaceholders - remainingPlaceholders)
  const expectedValues = [assignment.equipment, assignment.compare_os, assignment.decimal_number, assignment.ascii_character, assignment.capacity].filter(value => value !== undefined && value !== null && String(value).trim())
  const matchingValues = expectedValues.filter(value => text.toLocaleLowerCase('es-MX').includes(String(value).toLocaleLowerCase('es-MX')))
  const wordCount = text.split(/\s+/).filter(Boolean).length
  const conceptLabels = ['informática', 'sistema informático', 'red de computadoras', 'unidad de medida', 'sistemas numéricos', 'sistema operativo']
  const sectionsPresent = conceptLabels.filter(label => text.toLocaleLowerCase('es-MX').includes(label)).length
  const completionPercent = Math.round(completedFields / initialPlaceholders * 100)
  const suggested = Math.min(60, Math.round(completionPercent * .42 + (matchingValues.length / Math.max(1, expectedValues.length)) * 8 + Math.min(10, wordCount / 90)))
  return { text, remainingPlaceholders, completedFields, initialPlaceholders, completionPercent, wordCount, sectionsPresent, matchingValues: matchingValues.length, expectedValues: expectedValues.length, suggested }
}

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
