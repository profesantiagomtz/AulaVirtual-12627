import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, BookOpen, CheckCircle2, Save, Send, ShieldCheck } from 'lucide-react'
import { supabase } from '../lib/supabase'

export const mtcsContent = {
  'MTCS-RA-1.1': {
    label: 'MTCS · R.A. 1.1',
    materialTitle: 'Comunicación y componentes de una red',
    intro: 'Revisa cada bloque antes de resolver la actividad. La información explica los conceptos; las decisiones del diseño las tomarás tú.',
    lessons: [
      ['1. ¿Cómo se comunica una red?', 'Una red conecta dispositivos para intercambiar información. El mensaje se divide en datos que viajan por un medio y siguen reglas llamadas protocolos. El rendimiento depende del ancho de banda, la latencia, el medio y la cantidad de tráfico.'],
      ['2. Componentes y conexiones', 'Los equipos finales generan o reciben datos. Los dispositivos intermediarios conectan y dirigen el tráfico. El medio puede ser cobre, fibra óptica o inalámbrico. Cada elección responde a distancia, velocidad, interferencia, costo y seguridad.'],
      ['3. Clientes, servidores y protocolos', 'Un cliente solicita un servicio y un servidor lo proporciona. Los protocolos permiten que ambos interpreten la información de la misma manera. En una comunicación intervienen varias reglas, no un solo protocolo.'],
      ['4. Redes inalámbricas y móviles', 'Una red inalámbrica facilita la movilidad, pero requiere planear cobertura, interferencias, capacidad y protección del acceso. La comodidad no sustituye una configuración segura.'],
      ['5. Red doméstica y medios', 'Una red doméstica suele integrar módem u ONT, router, punto de acceso, cableado y equipos finales. El medio adecuado se selecciona según el entorno y la necesidad de conexión.'],
      ['6. Modelos de comunicación', 'Los modelos organizan las funciones de red por capas. Esto ayuda a explicar el recorrido de la información y a localizar fallas sin revisar todo al mismo tiempo.'],
    ],
    example: 'Ejemplo: en un aula con computadoras fijas, impresora compartida y dispositivos móviles, el diseño puede combinar cableado para los equipos que requieren estabilidad y conexión inalámbrica para movilidad. La justificación debe explicar por qué cada componente y medio es adecuado.',
    taskTitle: 'Actividad de evaluación: diseña y explica una red funcional',
    taskIntro: 'Analiza el escenario asignado y responde con tus propias decisiones. Valor máximo: 60 puntos.',
    fields: [
      ['networkType', '¿Qué tipo de red implementarías y por qué?'],
      ['devices', 'Lista los dispositivos finales e intermediarios necesarios. Indica la función de cada uno.'],
      ['topology', 'Describe cómo conectarías los equipos. Incluye un diagrama usando texto, flechas o una descripción ordenada.'],
      ['media', 'Selecciona el medio de conexión para cada zona y justifica tus elecciones.'],
      ['protocols', 'Menciona los protocolos o servicios necesarios y explica para qué se usaría cada uno.'],
      ['wireless', 'Explica cómo configurarías la conexión inalámbrica y qué cuidados aplicarías.'],
      ['performance', 'Identifica dos factores que podrían disminuir el rendimiento y propón una solución para cada uno.'],
      ['test', 'Describe cómo comprobarías que la red funciona correctamente.'],
    ],
  },
  'MTCS-RA-1.2': {
    label: 'MTCS · R.A. 1.2',
    materialTitle: 'Direccionamiento y enrutamiento IPv4',
    intro: 'Avanza en orden. Los ejemplos muestran el procedimiento, pero deberás aplicarlo a una red diferente.',
    lessons: [
      ['1. Capa de acceso', 'La capa de acceso permite que un dispositivo se conecte al medio local y entregue tramas dentro de la red. Aquí intervienen las interfaces, direcciones físicas y dispositivos como switches y puntos de acceso.'],
      ['2. Propósito de IP', 'IP permite identificar origen y destino para transportar paquetes entre redes. Una dirección IPv4 tiene 32 bits divididos en cuatro octetos. La máscara separa la parte de red de la parte de host.'],
      ['3. Unicast, broadcast y multicast', 'Unicast comunica un origen con un destino; broadcast envía a todos los equipos de la red local; multicast entrega a un grupo específico de receptores.'],
      ['4. Segmentación', 'Dividir una red en subredes reduce dominios de broadcast, organiza equipos y permite aplicar controles. Cada subred necesita dirección de red, rango válido de hosts y dirección de broadcast.'],
      ['5. Puerta de enlace y enrutamiento', 'Un equipo envía a la puerta de enlace los paquetes cuyo destino está fuera de su red. El router consulta su tabla de enrutamiento para seleccionar el siguiente camino.'],
      ['6. IPv6 y DHCP', 'IPv6 amplía el espacio de direcciones y mejora la escalabilidad. DHCP asigna automáticamente parámetros como dirección IP, máscara, puerta de enlace y DNS.'],
    ],
    example: 'Ejemplo: para 192.168.10.0/24, la dirección de red es 192.168.10.0, los hosts válidos van de 192.168.10.1 a 192.168.10.254 y el broadcast es 192.168.10.255. Al crear subredes, esos límites cambian según la nueva máscara.',
    taskTitle: 'Actividad de evaluación: configura y diagnostica una red segmentada',
    taskIntro: 'Trabaja únicamente con los datos que te asignó la plataforma. Valor máximo: 60 puntos.',
    fields: [
      ['analysis', 'Explica qué información proporciona la dirección de red y la máscara asignadas.'],
      ['subnetA', 'Calcula para la Subred A: prefijo, máscara, dirección de red, primer host, último host y broadcast.'],
      ['subnetB', 'Calcula para la Subred B: prefijo, máscara, dirección de red, primer host, último host y broadcast.'],
      ['allocation', 'Asigna direcciones a router, servidor y dos equipos de cada subred. No repitas direcciones reservadas.'],
      ['gateway', 'Indica la puerta de enlace de cada subred y explica su función.'],
      ['traffic', 'Explica el recorrido de un paquete entre un equipo de la Subred A y otro de la Subred B.'],
      ['diagnosis', 'Un equipo tiene la dirección indicada en el caso, pero no navega. Propón un diagnóstico ordenado y una solución.'],
      ['ipv6', 'Explica dos razones para adoptar IPv6 y una diferencia respecto a IPv4.'],
    ],
  },
  'MTCS-RA-2.1': {
    label: 'MTCS · R.A. 2.1',
    materialTitle: 'Primeros fundamentos de ciberseguridad',
    intro: 'Este bloque inicia el R.A. 2.1. Lee los conceptos y aplícalos al análisis del caso asignado.',
    lessons: [
      ['1. Ciberseguridad', 'La ciberseguridad protege información, dispositivos, servicios y redes frente a acciones accidentales o intencionales. No depende de una sola herramienta: combina personas, procesos y tecnología.'],
      ['2. Amenaza, vulnerabilidad y riesgo', 'Una amenaza puede causar daño; una vulnerabilidad es una debilidad; el riesgo surge cuando una amenaza puede aprovechar una vulnerabilidad y producir un impacto. No son sinónimos.'],
      ['3. Principios de seguridad', 'La confidencialidad limita el acceso; la integridad evita alteraciones no autorizadas; la disponibilidad mantiene información y servicios accesibles cuando se requieren.'],
      ['4. Amenazas internas y externas', 'Una amenaza interna proviene de alguien con acceso legítimo o cercano a la organización. Una externa se origina fuera de ella. Ambas pueden ser deliberadas o accidentales.'],
      ['5. Controles de seguridad', 'Los controles preventivos buscan evitar incidentes; los detectivos identifican lo ocurrido; los correctivos ayudan a recuperar la operación y reducir las consecuencias.'],
    ],
    example: 'Ejemplo: compartir una contraseña es una vulnerabilidad de operación; el acceso indebido es la amenaza y la exposición o modificación de datos representa el posible impacto. Cambiar contraseñas, limitar permisos y revisar registros son controles distintos.',
    taskTitle: 'Práctica inicial: analiza un incidente de seguridad',
    taskIntro: 'Esta práctica permite comprobar que distingues los conceptos básicos antes de continuar.',
    fields: [
      ['summary', 'Resume el incidente con tus propias palabras.'],
      ['assets', 'Identifica los recursos o datos que necesitan protección.'],
      ['threats', 'Identifica las amenazas presentes y clasifícalas como internas o externas.'],
      ['vulnerabilities', 'Identifica las vulnerabilidades. Explica por qué cada una es una debilidad.'],
      ['principles', 'Indica qué principios de seguridad pueden resultar afectados y justifica.'],
      ['controls', 'Propón un control preventivo, uno detectivo y uno correctivo.'],
    ],
  },
}

function hash(text) {
  let value = 2166136261
  for (let index = 0; index < text.length; index += 1) value = Math.imul(value ^ text.charCodeAt(index), 16777619)
  return value >>> 0
}

function assignmentFor(studentId, assessmentId, code) {
  const seed = hash(`${studentId}-${assessmentId}-${code}`)
  if (code === 'MTCS-RA-1.1') {
    const places = ['laboratorio escolar', 'biblioteca', 'taller técnico', 'oficina administrativa']
    return {
      title: `Escenario ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Lugar: ${places[seed % places.length]}`, `Equipos cableados: ${12 + (seed % 9)}`, `Dispositivos inalámbricos: ${6 + (seed % 7)}`, `Servicios: archivos, impresión e Internet`, `Condición: dos zonas separadas y acceso para visitantes`],
    }
  }
  if (code === 'MTCS-RA-1.2') {
    const second = 20 + (seed % 170)
    const hostA = 28 + (seed % 17)
    const hostB = 12 + (seed % 9)
    return {
      title: `Datos de red ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Red base: 192.168.${second}.0/24`, `Subred A: ${hostA} hosts`, `Subred B: ${hostB} hosts`, `Equipo con falla: 192.168.${second}.${200 + (seed % 30)}/24`, `Gateway registrado en el equipo: 192.168.${second}.1`],
    }
  }
  const cases = [
    'Un usuario abrió un archivo adjunto inesperado y después varios documentos dejaron de abrir.',
    'Una cuenta con permisos administrativos fue compartida y se detectaron cambios fuera del horario laboral.',
    'Un equipo sin actualizaciones se conectó a una red pública y comenzó a enviar tráfico inusual.',
    'Una memoria USB desconocida fue conectada a un equipo que almacena información importante.',
  ]
  return { title: `Caso ${String(seed % 997).padStart(3, '0')}`, lines: [cases[seed % cases.length], 'Analiza únicamente la información disponible y señala también qué datos investigarías.'] }
}

export default function MtcsActivity({ assessment, session, onBack }) {
  const definition = mtcsContent[assessment.activityCode]
  const assignment = useMemo(() => assignmentFor(session.id, assessment.id, assessment.activityCode), [session.id, assessment.id, assessment.activityCode])
  const [tab, setTab] = useState('material')
  const [answers, setAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [status, setStatus] = useState('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (session.preview) { setStatus('ready'); return undefined }
    let active = true
    supabase.from('submissions').select('answers, submitted_at').eq('assessment_id', assessment.id).maybeSingle().then(({ data, error }) => {
      if (!active) return
      if (error) { setMessage(error.message); setStatus('error'); return }
      setAnswers(data?.answers?.responses || {})
      setSubmitted(Boolean(data?.submitted_at))
      setStatus('ready')
    })
    return () => { active = false }
  }, [assessment.id])

  const complete = definition.fields.every(([key]) => String(answers[key] || '').trim().length >= 12)

  async function save(deliver = false) {
    if (session.preview) { setMessage('Esta es una vista previa. Las respuestas no se guardan ni generan entregas.'); setStatus('ready'); return }
    if (deliver && !complete) { setMessage('Completa todas las respuestas antes de entregar. Revisa que estén explicadas, no solo contestadas con una palabra.'); setStatus('error'); return }
    setStatus('saving'); setMessage('')
    const { data: authData } = await supabase.auth.getUser()
    const payload = { assessment_id: assessment.id, student_id: authData.user.id, answers: { activity: assessment.activityCode, assigned_case: assignment, responses: answers }, submitted_at: deliver ? new Date().toISOString() : null }
    const { error } = await supabase.from('submissions').upsert(payload, { onConflict: 'assessment_id,student_id' })
    if (error) { setMessage(error.message || 'No fue posible guardar.'); setStatus('error'); return }
    setSubmitted(deliver)
    setMessage(deliver ? 'Actividad entregada correctamente.' : 'Avance guardado correctamente.')
    setStatus(deliver ? 'submitted' : 'ready')
  }

  if (!definition) return null
  if (status === 'loading') return <section className="panel page-panel activity-workspace"><div className="loading-state">Preparando MTCS…</div></section>

  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">{definition.label}</span><h1>{definition.materialTitle}</h1><p>{definition.intro}</p></div><div className="mtcs-value"><strong>{assessment.activityCode === 'MTCS-RA-2.1' ? 'PRÁCTICA' : '60'}</strong><span>{assessment.activityCode === 'MTCS-RA-2.1' ? 'INICIAL' : 'PUNTOS MÁX.'}</span></div></div>
    <nav className="mtcs-tabs"><button className={tab === 'material' ? 'active' : ''} onClick={() => setTab('material')}><BookOpen size={17} /> Material y ejemplo</button><button className={tab === 'activity' ? 'active' : ''} onClick={() => setTab('activity')}><ShieldCheck size={17} /> Actividad</button></nav>

    {tab === 'material' ? <div className="mtcs-material"><div className="lesson-grid">{definition.lessons.map(([title, text]) => <article key={title}><span>{title.split('.')[0]}</span><div><h3>{title.replace(/^\d+\.\s*/, '')}</h3><p>{text}</p></div></article>)}</div><div className="worked-example"><strong>Ejemplo para comprender</strong><p>{definition.example}</p></div><button className="primary mtcs-continue" onClick={() => { setTab('activity'); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>Continuar a la actividad</button></div> : <div className="mtcs-activity">
      <div className="assigned-case"><span className="eyebrow">DATOS ASIGNADOS</span><h2>{assignment.title}</h2><ul>{assignment.lines.map(line => <li key={line}>{line}</li>)}</ul></div>
      <div className="stage-heading"><h2>{definition.taskTitle}</h2><p>{definition.taskIntro}</p></div>
      <fieldset disabled={submitted || status === 'saving'} className="mtcs-form">{definition.fields.map(([key, label], index) => <label key={key}><span><b>{index + 1}</b>{label}</span><textarea rows="4" value={answers[key] || ''} onChange={event => setAnswers(current => ({ ...current, [key]: event.target.value }))} placeholder="Escribe y explica tu respuesta…" /></label>)}</fieldset>
      {message && <div className={status === 'error' ? 'form-error asin-message' : 'submission-success asin-message'}>{message}</div>}
      <footer className="activity-footer"><span className="mtcs-progress">{definition.fields.filter(([key]) => String(answers[key] || '').trim().length >= 12).length} de {definition.fields.length} respuestas completas</span><div className="activity-footer-actions">{!submitted && <button className="secondary" onClick={() => save(false)} disabled={status === 'saving'}><Save size={17} /> Guardar avance</button>}<button className="primary" onClick={() => save(true)} disabled={submitted || status === 'saving'}>{submitted ? <CheckCircle2 size={17} /> : <Send size={17} />}{submitted ? 'Actividad entregada' : 'Entregar actividad'}</button></div></footer>
    </div>}
  </section>
}

export function MtcsMaterialView({ code, onBack }) {
  const definition = mtcsContent[code]
  if (!definition) return null
  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="activity-hero"><div><span className="eyebrow">{definition.label} · MATERIAL DIDÁCTICO</span><h1>{definition.materialTitle}</h1><p>{definition.intro}</p></div><div className="mtcs-value"><BookOpen size={25} /><span>APRENDE Y PRACTICA</span></div></div>
    <div className="mtcs-learning-route"><b>Ruta de aprendizaje</b><span>1. Lee cada tema</span><span>2. Analiza el ejemplo</span><span>3. Resuelve los ejercicios</span><span>4. Después abre la evaluación</span></div>
    <div className="lesson-grid">{definition.lessons.map(([title, text]) => <article key={title}><span>{title.split('.')[0]}</span><div><h3>{title.replace(/^\d+\.\s*/, '')}</h3><p>{text}</p></div></article>)}</div>
    <div className="worked-example"><strong>Ejemplo explicado</strong><p>{definition.example}</p></div>
    <PracticeExercises code={code} />
    <div className="info-note mtcs-ready-note"><CheckCircle2 size={18} /><span>Cuando puedas explicar estos conceptos y resolver los ejercicios sin copiar el ejemplo, continúa en <b>Evaluaciones</b>.</span></div>
  </section>
}

function PracticeExercises({ code }) {
  const exercises = code === 'MTCS-RA-1.1' ? [
    'Clasifica cinco elementos de una red cercana como equipo final, dispositivo intermediario o medio.',
    'Compara cable de cobre, fibra óptica y conexión inalámbrica. Escribe una ventaja y una limitación de cada uno.',
    'Dibuja el recorrido de la información desde una computadora hasta un servicio de Internet e identifica los componentes que intervienen.',
    'Propón dos cambios para mejorar una red con señal inalámbrica débil y conexión inestable.',
  ] : code === 'MTCS-RA-1.2' ? [
    'En la red 192.168.50.0/24 identifica dirección de red, primer host, último host y broadcast.',
    'Explica qué ocurre cuando dos equipos de la misma red se comunican y qué cambia cuando el destino está en otra red.',
    'Determina si 192.168.20.15/24 y 192.168.21.15/24 pertenecen a la misma red. Justifica tu respuesta.',
    'Un equipo tiene dirección IP y máscara correctas, pero no puede salir de su red. Escribe un orden lógico de revisión.',
  ] : [
    'Escribe un ejemplo propio de amenaza, vulnerabilidad y riesgo sin utilizar el ejemplo del material.',
    'Clasifica tres situaciones como afectación a confidencialidad, integridad o disponibilidad y explica por qué.',
    'Propón un control preventivo, uno detectivo y uno correctivo para un equipo compartido.',
  ]
  return <section className="mtcs-practice"><div className="stage-heading"><span>PRACTICA ANTES DE EVALUARTE</span><h2>Ejercicios de comprobación</h2><p>Resuélvelos en tu libreta o coméntalos con tu docente. No se entregan en este apartado.</p></div><ol>{exercises.map(item => <li key={item}>{item}</li>)}</ol></section>
}
