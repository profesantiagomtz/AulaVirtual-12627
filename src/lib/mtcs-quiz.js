// Evaluaciones MTCS 1.2 y 2.1 en versión sencilla (nov-2026): respuestas cortas o de opción,
// con datos distintos para cada alumno, revisión automática (50 pts) y foto del cuaderno (10 pts del docente).
import { hash } from './mtcs-assignment'

export const QUIZ_CODES = ['MTCS-RA-1.2', 'MTCS-RA-2.1']
export const AUTO_MAX = 50
export const TEACHER_MAX = 10

export function isQuiz(code) { return QUIZ_CODES.includes(code) }

// Baraja estable: el mismo alumno siempre ve el mismo orden.
function shuffle(list, seed) {
  const items = [...list]
  let value = seed || 1
  for (let index = items.length - 1; index > 0; index -= 1) {
    value = Math.imul(value ^ (value >>> 15), 2246822519) >>> 0
    const other = value % (index + 1)
    ;[items[index], items[other]] = [items[other], items[index]]
  }
  return items
}

function networkQuiz(seed) {
  const octet = 20 + (seed % 200)
  const base = `192.168.${octet}`
  const target = (seed >>> 3) % 4 // subred que le toca (0..3)
  const start = target * 64
  const probeSubnet = ((seed >>> 6) % 4)
  const probeHost = probeSubnet * 64 + 5 + ((seed >>> 9) % 50)
  const names = ['Subred 1', 'Subred 2', 'Subred 3', 'Subred 4']
  return {
    title: `Red ${String(seed % 997).padStart(3, '0')}`,
    lines: [
      `Tu red: ${base}.0/24`,
      'Divídela en 4 subredes del mismo tamaño (64 direcciones cada una).',
      `Tu subred para contestar: ${names[target]}`,
      `IP para revisar: ${base}.${probeHost}`,
    ],
    questions: [
      { key: 'prefix', type: 'text', label: '¿Cuál es el nuevo prefijo de cada subred?', placeholder: 'Ejemplo: /27', expected: '/26', points: 5 },
      { key: 'mask', type: 'text', label: '¿Cuál es la nueva máscara?', placeholder: 'Ejemplo: 255.255.255.224', expected: '255.255.255.192', points: 5 },
      { key: 'network', type: 'text', label: `Dirección de red de la ${names[target]}`, placeholder: `${base}.___`, expected: `${base}.${start}`, points: 8 },
      { key: 'first', type: 'text', label: `Primer host válido de la ${names[target]}`, placeholder: `${base}.___`, expected: `${base}.${start + 1}`, points: 8 },
      { key: 'last', type: 'text', label: `Último host válido de la ${names[target]}`, placeholder: `${base}.___`, expected: `${base}.${start + 62}`, points: 8 },
      { key: 'broadcast', type: 'text', label: `Broadcast de la ${names[target]}`, placeholder: `${base}.___`, expected: `${base}.${start + 63}`, points: 8 },
      { key: 'belongs', type: 'choice', label: `¿A qué subred pertenece la IP ${base}.${probeHost}?`, options: names, expected: names[probeSubnet], points: 8 },
    ],
    notebook: 'En tu cuaderno escribe tu nombre, la tabla de las 4 subredes (red, primer host, último host y broadcast) y cómo obtuviste la máscara.',
  }
}

const securityCases = [
  {
    text: place => `En ${place}, una persona abrió un archivo adjunto de un correo que no esperaba. Al día siguiente, los documentos de la carpeta compartida ya no abrían y apareció un mensaje pidiendo dinero.`,
    principle: 'Disponibilidad', origin: 'Externa',
    vulnerability: 'Abrir archivos adjuntos sin verificar quién los envía',
    prevent: 'Enseñar al personal a no abrir adjuntos desconocidos y tener antivirus actualizado',
    react: 'Restaurar los documentos desde un respaldo',
  },
  {
    text: place => `En ${place}, varias personas usan la misma cuenta de administrador con la misma contraseña. Se descubrió que alguien cambió datos importantes en la noche, fuera del horario de trabajo.`,
    principle: 'Integridad', origin: 'Interna',
    vulnerability: 'Compartir una cuenta de administrador entre varias personas',
    prevent: 'Dar a cada persona su propia cuenta con solo los permisos que necesita',
    react: 'Revisar la bitácora de accesos para saber quién hizo los cambios',
  },
  {
    text: place => `En ${place}, una laptop que no se actualiza desde hace meses se conectó al Wi-Fi abierto de una cafetería. Días después, alguien desconocido entró al correo del encargado y leyó mensajes privados.`,
    principle: 'Confidencialidad', origin: 'Externa',
    vulnerability: 'Usar un equipo sin actualizaciones en una red Wi-Fi abierta',
    prevent: 'Mantener el equipo actualizado y evitar redes Wi-Fi abiertas',
    react: 'Cambiar de inmediato las contraseñas del correo',
  },
  {
    text: place => `En ${place}, un empleado copió en su memoria USB la lista de clientes con nombres y teléfonos, y la publicó en un grupo de redes sociales.`,
    principle: 'Confidencialidad', origin: 'Interna',
    vulnerability: 'Cualquier empleado puede copiar información a una USB sin control',
    prevent: 'Bloquear los puertos USB y limitar quién puede ver la lista de clientes',
    react: 'Revisar los registros del equipo para confirmar quién copió el archivo',
  },
]
const places = ['una papelería', 'una clínica dental', 'una escuela', 'una tienda de celulares', 'un despacho contable', 'una farmacia']

function securityQuiz(seed) {
  const index = seed % securityCases.length
  const item = securityCases[index]
  const others = securityCases.filter((_, position) => position !== index)
  const place = places[(seed >>> 4) % places.length]
  const mix = (correct, wrong, salt) => shuffle([correct, ...wrong], seed ^ salt)
  return {
    title: `Caso ${String(seed % 997).padStart(3, '0')}`,
    lines: [item.text(place)],
    questions: [
      { key: 'principle', type: 'choice', label: '¿Qué principio de seguridad se afectó MÁS?', options: ['Confidencialidad', 'Integridad', 'Disponibilidad'], expected: item.principle, points: 10 },
      { key: 'origin', type: 'choice', label: '¿La amenaza es interna o externa?', options: ['Interna', 'Externa'], expected: item.origin, points: 10 },
      { key: 'vulnerability', type: 'choice', label: '¿Cuál es la vulnerabilidad (la debilidad) en este caso?', options: mix(item.vulnerability, others.map(other => other.vulnerability), 23), expected: item.vulnerability, points: 10 },
      { key: 'prevent', type: 'choice', label: '¿Qué control PREVENTIVO habría evitado el problema?', options: mix(item.prevent, [item.react, others[0].prevent, others[1].react], 37), expected: item.prevent, points: 10 },
      { key: 'react', type: 'choice', label: 'Ya pasó. ¿Qué control ayuda a DETECTAR o CORREGIR?', options: mix(item.react, [item.prevent, others[1].react, others[2].prevent], 53), expected: item.react, points: 10 },
      { key: 'first', type: 'open', label: 'Con tus palabras: si tú fueras el encargado, ¿qué harías primero y por qué? (2 o 3 renglones)', placeholder: 'Escribe tu respuesta…' },
    ],
    notebook: 'En tu cuaderno escribe tu nombre, copia el caso en una línea y responde a mano las 5 preguntas con una breve razón de cada una.',
  }
}

export function quizFor(code, studentId, assessmentId) {
  const seed = hash(`${studentId}-${assessmentId}-${code}-v2`)
  return code === 'MTCS-RA-1.2' ? networkQuiz(seed) : securityQuiz(seed)
}

function normalize(value = '') {
  return String(value).toLowerCase().replace(/\s+/g, '').replace(/^\/?/, '/').replace(/^\/(?=\d+\.)/, '')
}

export function isCorrect(question, value) {
  if (!value) return false
  if (question.type === 'choice') return value === question.expected
  if (question.type === 'text') return normalize(value) === normalize(question.expected)
  return false
}

export function gradeQuiz(quiz, responses = {}) {
  const items = quiz.questions.filter(question => question.type !== 'open').map(question => ({
    key: question.key, label: question.label, given: responses[question.key] || '', expected: question.expected,
    ok: isCorrect(question, responses[question.key]), max: question.points,
  }))
  const auto = items.reduce((sum, item) => sum + (item.ok ? item.max : 0), 0)
  return { version: 2, items, auto, autoMax: AUTO_MAX, teacherMax: TEACHER_MAX }
}
