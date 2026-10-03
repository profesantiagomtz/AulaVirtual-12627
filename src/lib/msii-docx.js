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
