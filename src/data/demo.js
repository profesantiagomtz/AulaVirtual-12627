export const groups = [
  { id: '310', name: '310', semester: 3, career: 'Informática', students: 8 },
  { id: '311', name: '311', semester: 3, career: 'Informática', students: 5 },
  { id: '511', name: '511', semester: 5, career: 'Informática', students: 4 },
]

export const materials = [
  { id: 2, title: 'Riesgos de seguridad informática', type: 'Presentación', group: '310', unit: 'R.A. 1.1', date: '25 sep' },
  { id: 3, title: 'Configuración de comunicación en red', type: 'Video', group: '511', unit: 'R.A. 1.1', date: '22 sep' },
]

export const assessments = [
  { id: 2, title: 'R.A. 1.1 Seguridad informática', group: '310', due: '08 oct', submissions: 14, total: 30, average: 76, status: 'Activa' },
  { id: 3, title: 'R.A. 1.1 Documentos digitales', group: '311', due: '26 sep', submissions: 22, total: 22, average: 88, status: 'Cerrada' },
]

export const students = [
  { id: 2, name: 'Alumno de demostración 02', email: 'alumno02@institucional.edu.mx', group: '310', semester: 3, progress: 76, average: 78, pending: 1 },
  { id: 3, name: 'Alumno de demostración 03', email: 'alumno03@institucional.edu.mx', group: '311', semester: 3, progress: 84, average: 86, pending: 0 },
  { id: 4, name: 'Alumno de demostración 04', email: 'alumno04@institucional.edu.mx', group: '511', semester: 5, progress: 58, average: 69, pending: 2 },
]

// Alumnos y actividad de ejemplo para revisar «En vivo», «Avance» y «Asistencia» sin conexión.
const demoNames = {
  310: ['Ana Sofía Treviño Garza', 'Bruno Cárdenas Leal', 'Carla Ibarra Ruiz', 'Diego Salinas Mora', 'Elena Quintero Paz', 'Fernando Ríos Delgado', 'Gabriela Peña Solís', 'Hugo Zamora Villa'],
  311: ['Iris Medina Cantú', 'Jorge Lara Esquivel', 'Karen Olvera Rangel', 'Luis Navarro Tapia', 'Mariana Ochoa Silva'],
  511: ['Nicolás Fuentes Barrera', 'Olga Pineda Castro', 'Pablo Reyes Ávila', 'Regina Soto Luna'],
}
students.splice(0, students.length, ...Object.entries(demoNames).flatMap(([group, names]) => names.map((name, index) => ({
  id: `demo-${group}-${index + 1}`, name, email: `alumno${group}${index + 1}@tam.conalep.edu.mx`, enrollment: `2620002${group.slice(0, 1)}${index + 10}`, group,
}))))

const demoTotals = { 'ASIN-RA-1.2': 24, 'ASIN-RA-2.1': 20, 'MSII-RA-1.2': 29, 'MSII-RA-2.1': 8, 'EDOA-RA-1.1': 7, 'EDOA-RA-1.2': 5, 'EDOA-RA-1.3': 5, 'EDOA-RA-2.1': 6, 'EDOA-RA-2.2': 6, 'MTCS-RA-1.1': 10, 'MTCS-RA-1.2': 7, 'MTCS-RA-2.1': 6, 'MTCS-RA-2.2': 18 }
const seeded = (text, salt) => {
  let hash = 2166136261 ^ salt
  for (const char of `${text}:${salt}`) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619)
  hash ^= hash >>> 13; hash = Math.imul(hash, 1274126177); hash ^= hash >>> 16
  return (hash >>> 0) / 4294967296
}

export function demoLearningProgress() {
  return students.flatMap(student => Object.entries(demoTotals).filter(([code]) => ({ ASIN: '310', MSII: '310', EDOA: '311', MTCS: '511' })[code.slice(0, 4)] === student.group).map(([code, total]) => {
    const late = /2\.[12]$/.test(code)
    const ratio = Math.min(1, seeded(student.id + code, 3) * (late ? 1.1 : 1.6))
    const done = Math.round(total * ratio)
    return done ? { student_id: student.id, material_code: code, completed_steps: Array.from({ length: done }, (_, index) => `paso-${index + 1}`), total_steps: total, completed_at: done >= total ? new Date(Date.now() - 86400000 * 3).toISOString() : null, updated_at: new Date(Date.now() - 3600000 * (1 + seeded(student.id, 5) * 70)).toISOString() } : null
  }).filter(Boolean))
}

export function demoTracking() {
  const now = Date.now()
  const minute = 60000
  const online = students.filter(student => seeded(student.id, 11) > 0.45)
  const where = [['Material', 'ASIN · Material didáctico R.A. 2.1'], ['Material', 'MSII · Material didáctico R.A. 2.1'], ['Tareas', 'R.A. 2.1 Instala y configura herramientas'], ['Notas', ''], ['Material', 'EDOA · Material didáctico R.A. 2.2'], ['Inicio', ''], ['Cronograma', ''], ['Material', 'MTCS · Material didáctico R.A. 2.2']]
  const presence = students.map((student, index) => {
    const isOnline = online.includes(student)
    const spot = where[index % where.length]
    return { student_id: student.id, last_seen_at: new Date(now - (isOnline ? 20000 : minute * (40 + index * 95))).toISOString(), session_started_at: new Date(now - minute * (8 + index * 3)).toISOString(), current_view: spot[0], current_detail: spot[1] }
  })
  const kinds = [['avance', 'paso'], ['vista', ''], ['entrada', ''], ['completo', ''], ['entrega', ''], ['vista', ''], ['avance', 'paso'], ['inicio', '']]
  const log = students.flatMap((student, index) => kinds.slice(0, 3 + (index % 5)).map((_, step) => {
    const kind = kinds[(index * 3 + step) % kinds.length][0]
    const code = Object.keys(demoTotals).find(item => ({ ASIN: '310', MSII: '310', EDOA: '311', MTCS: '511' })[item.slice(0, 4)] === student.group && /2\.[12]$/.test(item)) || 'ASIN-RA-2.1'
    const titles = { entrada: 'entró a la plataforma', vista: where[(index + step) % where.length][0], avance: code, completo: code, inicio: 'R.A. 2.1 Actividad de evaluación', entrega: 'R.A. 2.1 Actividad de evaluación' }
    const details = { vista: where[(index + step) % where.length][1], avance: `paso ${2 + ((index * 5 + step * 3) % (demoTotals[code] - 2))} de ${demoTotals[code]}`, completo: 'terminó el material' }
    return { id: `${student.id}-${step}`, student_id: student.id, kind, title: titles[kind], detail: details[kind] || '', created_at: new Date(now - minute * (2 + index * 4 + step * 9)).toISOString() }
  })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  const summary = students.map((student, index) => ({ student_id: student.id, last_seen_at: presence[index].last_seen_at, total_minutes: Math.round(40 + seeded(student.id, 13) * 380), active_days: 4 + index % 9, today_minutes: online.includes(student) ? 12 + index * 3 : 0 }))
  return { presence, log, summary }
}

// Conexiones por día: la mayoría entra al empezar la clase, algunos tarde y otros no entran.
export function demoDailyActivity(dates) {
  return dates.flatMap(day => students.map(student => {
    const chance = seeded(student.id + day, 17)
    if (chance < 0.14) return null
    const start = chance < 0.24 ? 445 + Math.round(chance * 100) : 418 + Math.round(chance * 8)
    return { student_id: student.id, day, minutes: Array.from({ length: 45 }, (_, index) => start + index) }
  }).filter(Boolean))
}
