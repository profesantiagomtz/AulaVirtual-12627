import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, BookOpen, CheckCircle2, Save, Send, ShieldCheck, Upload } from 'lucide-react'
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
  const [packetTracerFiles, setPacketTracerFiles] = useState({})
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
      setPacketTracerFiles(data?.answers?.packet_tracer || {})
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
    const payload = { assessment_id: assessment.id, student_id: authData.user.id, answers: { activity: assessment.activityCode, assigned_case: assignment, responses: answers, ...(Object.keys(packetTracerFiles).length ? { packet_tracer: packetTracerFiles } : {}) }, submitted_at: deliver ? new Date().toISOString() : null }
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

const ra11Checks = [
  { question: '¿Qué elemento solicita normalmente un servicio en la red?', options: ['Cliente', 'Medio', 'Router'], correct: 'Cliente' },
  { question: '¿Cuál es un dispositivo intermediario?', options: ['Switch', 'Teclado', 'Documento'], correct: 'Switch' },
  { question: '¿Qué permite que dos equipos interpreten la comunicación con las mismas reglas?', options: ['Un protocolo', 'El tamaño del monitor', 'La marca del equipo'], correct: 'Un protocolo' },
  { question: '¿Qué aspecto debe revisarse al planear una red inalámbrica?', options: ['Cobertura e interferencia', 'Color de los cables', 'Fondo de pantalla'], correct: 'Cobertura e interferencia' },
  { question: '¿Qué medio suele ser adecuado para movilidad?', options: ['Inalámbrico', 'Fibra sin equipos', 'Cable desconectado'], correct: 'Inalámbrico' },
  { question: '¿Para qué sirven las capas de un modelo de red?', options: ['Organizar funciones y localizar fallas', 'Aumentar el tamaño de archivos', 'Eliminar protocolos'], correct: 'Organizar funciones y localizar fallas' },
]

const ra11ExtraChecks = [
  [
    { question: '¿Qué necesita todo mensaje para llegar correctamente?', options: ['Origen, destino, medio y reglas', 'Solo electricidad', 'Únicamente Internet'], correct: 'Origen, destino, medio y reglas' },
    { question: '¿Qué situación puede disminuir el rendimiento?', options: ['Demasiado tráfico y alta latencia', 'Nombrar los equipos', 'Usar una carpeta'], correct: 'Demasiado tráfico y alta latencia' },
  ],
  [
    { question: '¿Cuál es un equipo final?', options: ['Computadora', 'Switch', 'Cable UTP'], correct: 'Computadora' },
    { question: '¿Qué elemento transporta físicamente o por ondas la información?', options: ['El medio', 'El usuario', 'La contraseña'], correct: 'El medio' },
  ],
  [
    { question: '¿Qué hace normalmente un servidor?', options: ['Proporciona recursos o servicios', 'Solo solicita servicios', 'Sustituye todo el cableado'], correct: 'Proporciona recursos o servicios' },
    { question: '¿Por qué son necesarios los protocolos?', options: ['Definen reglas comunes de comunicación', 'Cambian el tamaño del monitor', 'Eliminan las direcciones'], correct: 'Definen reglas comunes de comunicación' },
  ],
  [
    { question: '¿Qué puede afectar una señal Wi-Fi?', options: ['Distancia, obstáculos e interferencias', 'El nombre del usuario', 'El formato de un documento'], correct: 'Distancia, obstáculos e interferencias' },
    { question: '¿Qué acción mejora la seguridad inalámbrica?', options: ['Usar cifrado y una clave robusta', 'Compartir la clave públicamente', 'Desactivar toda autenticación'], correct: 'Usar cifrado y una clave robusta' },
  ],
  [
    { question: '¿Qué medio ofrece alta velocidad y resistencia a interferencias?', options: ['Fibra óptica', 'Papel', 'Bluetooth sin adaptador'], correct: 'Fibra óptica' },
    { question: '¿Qué criterio ayuda a elegir un medio?', options: ['Distancia, velocidad, ambiente y costo', 'El color favorito', 'La marca del escritorio'], correct: 'Distancia, velocidad, ambiente y costo' },
  ],
  [
    { question: 'Si falla el cable, ¿qué parte conviene revisar primero?', options: ['Acceso físico al medio', 'Aplicación de correo', 'Diseño del documento'], correct: 'Acceso físico al medio' },
    { question: '¿Qué ventaja ofrece trabajar por capas?', options: ['Diagnosticar una función a la vez', 'Evitar todos los dispositivos', 'No utilizar protocolos'], correct: 'Diagnosticar una función a la vez' },
  ],
]

const ra11Details = [
  ['Emisor: dispositivo que origina la información.', 'Receptor: dispositivo o servicio que debe recibirla.', 'Mensaje: datos que se desean comunicar.', 'Medio: camino por cable, fibra u ondas.', 'Protocolo: reglas que ordenan el intercambio.', 'Ancho de banda es capacidad; latencia es tiempo de respuesta. No significan lo mismo.'],
  ['Equipos finales: computadoras, celulares, impresoras y servidores.', 'Intermediarios: switches, routers y puntos de acceso.', 'El switch conecta equipos dentro de una red local.', 'El router comunica redes diferentes y selecciona rutas.', 'El punto de acceso permite que dispositivos inalámbricos entren a la red.'],
  ['El cliente inicia una solicitud; el servidor procesa y responde.', 'DNS traduce nombres comprensibles a direcciones IP.', 'DHCP entrega parámetros de red automáticamente.', 'HTTP y HTTPS permiten solicitar recursos web.', 'Una comunicación real utiliza varios protocolos de manera coordinada.'],
  ['La cobertura indica hasta dónde llega una señal útil.', 'Paredes, distancia y otros equipos pueden producir pérdida o interferencia.', 'Más usuarios simultáneos significan más capacidad compartida.', 'La autenticación controla quién entra; el cifrado protege la comunicación.', 'La ubicación del punto de acceso influye en cobertura y rendimiento.'],
  ['Cobre: económico y común, pero limitado por distancia e interferencias.', 'Fibra: alta velocidad y largas distancias, con mayor cuidado de instalación.', 'Inalámbrico: movilidad y rapidez de despliegue, pero comparte el aire.', 'La decisión correcta depende del problema, no de escoger siempre el medio más costoso.'],
  ['Las capas separan funciones para comprender y diagnosticar.', 'Las capas inferiores se relacionan con señal, medio y acceso.', 'Las capas intermedias identifican destinos y transportan información.', 'Las capas superiores atienden los servicios que utiliza el usuario.', 'Al diagnosticar se empieza por lo básico y se avanza de manera ordenada.'],
]

const packetTracerPractices = [
  {
    id: 'pt-componentes',
    title: 'Práctica 1 · Construcción de una red local básica',
    related: 'Temas 2 y 3: componentes, conexiones, clientes y servidores',
    goal: 'Construir una red local sencilla, asignar direcciones y comprobar la comunicación entre sus equipos.',
    steps: [
      'Abre Packet Tracer y crea un archivo nuevo.',
      'Agrega un switch 2960, tres computadoras y un servidor.',
      'Conecta cada equipo al switch con cable de cobre directo.',
      'Configura las direcciones 192.168.10.10, 192.168.10.11, 192.168.10.12 y 192.168.10.100 con máscara 255.255.255.0.',
      'Cambia al modo Simulation y envía una PDU simple entre dos computadoras.',
      'Desde una computadora ejecuta ping hacia las otras dos y hacia el servidor.',
      'Guarda el archivo con el formato: Grupo_Apellido_Practica1.pkt.',
    ],
    checks: ['Los cuatro equipos muestran enlace activo.', 'No existen direcciones IP repetidas.', 'Los cuatro destinos responden correctamente.'],
  },
  {
    id: 'pt-inalambrica',
    title: 'Práctica 2 · Red cableada e inalámbrica',
    related: 'Temas 4 y 5: redes inalámbricas, red doméstica y medios',
    goal: 'Integrar dispositivos cableados e inalámbricos y observar cómo cambia el medio de conexión.',
    steps: [
      'Crea una topología con un router inalámbrico, una computadora cableada, una laptop y un teléfono.',
      'Conecta la computadora por cable al router inalámbrico.',
      'Configura el nombre de la red como AULA-GRUPO y protege el acceso con WPA2-PSK.',
      'Conecta la laptop y el teléfono a la red inalámbrica usando la clave configurada.',
      'Comprueba que todos los dispositivos reciban una dirección válida.',
      'Ejecuta ping desde la computadora hacia la laptop y observa el recorrido en modo Simulation.',
      'Guarda el archivo con el formato: Grupo_Apellido_Practica2.pkt.',
    ],
    checks: ['El equipo cableado y los inalámbricos pertenecen a la misma red.', 'La red tiene seguridad configurada.', 'La prueba de comunicación es satisfactoria.'],
  },
  {
    id: 'pt-diagnostico',
    title: 'Práctica 3 · Diagnóstico y corrección de conectividad',
    related: 'Tema 6: modelos de comunicación y diagnóstico por capas',
    goal: 'Aplicar un orden de diagnóstico, localizar errores de configuración y comprobar la solución.',
    steps: [
      'Construye una red con un switch y cuatro computadoras.',
      'Configura tres equipos en la red 192.168.20.0/24.',
      'En el cuarto equipo coloca intencionalmente una dirección de otra red.',
      'Usa ipconfig y ping para identificar cuál equipo no se comunica y explica mentalmente la causa.',
      'Corrige la dirección sin cambiar el cableado ni los demás equipos.',
      'Repite las pruebas hasta obtener respuesta de los cuatro equipos.',
      'Agrega una nota dentro de la topología indicando el error encontrado y la corrección aplicada.',
      'Guarda el archivo con el formato: Grupo_Apellido_Practica3.pkt.',
    ],
    checks: ['El archivo conserva la nota del diagnóstico.', 'Las cuatro computadoras quedan en la misma red.', 'Todos los equipos responden después de la corrección.'],
  },
]

export function MtcsMaterialView({ code, session, onBack, onProgressUpdate }) {
  const definition = mtcsContent[code]
  if (!definition) return null
  if (code === 'MTCS-RA-1.1') return <Ra11LearningPath definition={definition} session={session} onBack={onBack} onProgressUpdate={onProgressUpdate} />
  return <GuidedMaterial definition={definition} code={code} onBack={onBack} />
}

const guidedExamples = {
  'MTCS-RA-1.2': [
    'Una laptop entrega una trama al switch para comunicarse dentro del salón. El switch utiliza las direcciones físicas para enviarla por el puerto correcto; todavía no necesita salir a otra red.',
    'En 192.168.10.25/24, los primeros 24 bits identifican la red. Por eso la red es 192.168.10.0 y el 25 identifica al equipo dentro de ella.',
    'Una impresión enviada a una sola impresora es unicast. Un aviso dirigido a todos los equipos de la red local es broadcast. Una transmisión para un grupo suscrito es multicast.',
    'Si una sola red tiene demasiados equipos, se divide. Cada nueva subred obtiene su propia dirección de red, rango de hosts y broadcast; ninguna dirección puede repetirse.',
    'El equipo 192.168.10.20 quiere comunicarse con 192.168.20.30. Como el destino no pertenece a su red, entrega el paquete a su puerta de enlace para que el router decida la ruta.',
    'Al conectarse, DHCP puede entregar dirección, prefijo, puerta de enlace y DNS. IPv6 ofrece un espacio de direcciones mucho mayor que IPv4 y utiliza una escritura hexadecimal separada por dos puntos.',
  ],
  'MTCS-RA-2.1': [
    'Una escuela protege expedientes, computadoras y servicios. Capacita usuarios, define procedimientos y configura tecnología: las tres partes trabajan juntas.',
    'Una contraseña escrita junto al monitor es una vulnerabilidad. Una persona que intenta usarla es la amenaza. El acceso indebido y la exposición de datos constituyen el riesgo.',
    'Leer calificaciones sin permiso afecta confidencialidad; modificarlas afecta integridad; impedir que el sistema abra durante evaluaciones afecta disponibilidad.',
    'Un empleado que comparte accidentalmente un archivo provoca una amenaza interna. Un atacante que intenta ingresar desde Internet representa una amenaza externa.',
    'Bloquear archivos peligrosos es preventivo; generar una alerta es detectivo; restaurar una copia limpia después del incidente es correctivo.',
  ],
}

const guidedExercises = {
  'MTCS-RA-1.2': [
    'Explica qué función cumple la capa de acceso cuando dos computadoras del mismo laboratorio se comunican.',
    'Para 192.168.40.18/24, identifica red, parte de host y cantidad máxima de hosts utilizables.',
    'Escribe un ejemplo propio de unicast, broadcast y multicast sin repetir los del ejemplo.',
    'Obtén red, primer host, último host y broadcast de 192.168.50.0/24.',
    'Explica el recorrido de un paquete que sale de una red local hacia otra red e identifica cuándo interviene el router.',
    'Compara una dirección IPv4 con una IPv6 e indica qué parámetros podría entregar DHCP.',
  ],
  'MTCS-RA-2.1': [
    'Selecciona un recurso del laboratorio y escribe cómo lo protegerías mediante personas, procesos y tecnología.',
    'Construye un ejemplo nuevo que identifique claramente amenaza, vulnerabilidad, impacto y riesgo.',
    'Clasifica tres situaciones propias según afecten confidencialidad, integridad o disponibilidad y justifica.',
    'Propón una amenaza interna accidental y una externa intencional para una escuela.',
    'Para un archivo infectado, propón un control preventivo, uno detectivo y uno correctivo.',
  ],
}

function GuidedMaterial({ definition, code, onBack }) {
  const examples = guidedExamples[code] || []
  const exercises = guidedExercises[code] || []
  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="activity-hero"><div><span className="eyebrow">{definition.label} · MATERIAL DIDÁCTICO</span><h1>{definition.materialTitle}</h1><p>{definition.intro}</p></div><div className="mtcs-value"><BookOpen size={25} /><span>APRENDE Y PRACTICA</span></div></div>
    <div className="mtcs-learning-route"><b>Ruta de aprendizaje</b><span>1. Lee cada tema</span><span>2. Analiza el ejemplo</span><span>3. Resuelve los ejercicios</span><span>4. Después abre la evaluación</span></div>
    <div className="guided-topic-list">{definition.lessons.map(([title, text], index) => <article key={title}><header><span>{index + 1}</span><h2>{title.replace(/^\d+\.\s*/, '')}</h2></header><section><small>PRIMERO: APRENDE</small><h3>Conceptos clave</h3><p>{text}</p></section><section className="guided-example"><small>DESPUÉS: OBSERVA</small><h3>Ejemplo práctico</h3><p>{examples[index]}</p></section><section className="guided-exercise"><small>AHORA: APLICA</small><h3>Ejercicio de refuerzo</h3><p>{exercises[index]}</p></section></article>)}</div>
    <PracticeExercises code={code} />
    <div className="info-note mtcs-ready-note"><CheckCircle2 size={18} /><span>Cuando puedas explicar estos conceptos y resolver los ejercicios sin copiar el ejemplo, continúa en <b>Evaluaciones</b>.</span></div>
  </section>
}

function Ra11LearningPath({ definition, session, onBack, onProgressUpdate }) {
  const [completed, setCompleted] = useState([])
  const [answers, setAnswers] = useState({})
  const [feedback, setFeedback] = useState({})
  const [command, setCommand] = useState('')
  const [terminal, setTerminal] = useState(['Escribe un comando para comenzar el diagnóstico.'])
  const [status, setStatus] = useState('loading')
  const [assessmentId, setAssessmentId] = useState(null)
  const [packetUploads, setPacketUploads] = useState({})
  const [uploadingPractice, setUploadingPractice] = useState('')
  const [practiceMessage, setPracticeMessage] = useState({})
  const totalSteps = definition.lessons.length + 1 + packetTracerPractices.length

  useEffect(() => {
    if (session?.preview) { setStatus('ready'); return undefined }
    let active = true
    Promise.all([
      supabase.from('learning_progress').select('completed_steps').eq('material_code', 'MTCS-RA-1.1').maybeSingle(),
      supabase.from('assessments').select('id').eq('activity_code', 'MTCS-RA-1.1').maybeSingle(),
    ]).then(([progressResult, assessmentResult]) => {
      if (!active) return
      if (!progressResult.error) setCompleted(Array.isArray(progressResult.data?.completed_steps) ? progressResult.data.completed_steps : [])
      if (!assessmentResult.error && assessmentResult.data?.id) {
        setAssessmentId(assessmentResult.data.id)
        supabase.from('submissions').select('answers').eq('assessment_id', assessmentResult.data.id).maybeSingle().then(({ data }) => {
          if (active) setPacketUploads(data?.answers?.packet_tracer || {})
        })
      }
      setStatus(progressResult.error || assessmentResult.error ? 'error' : 'ready')
    })
    return () => { active = false }
  }, [session?.id])

  async function completeStep(step) {
    if (completed.includes(step)) return
    const next = [...completed, step]
    setCompleted(next)
    if (session?.preview) { onProgressUpdate?.({ material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: next.length >= totalSteps ? new Date().toISOString() : null }); return }
    setStatus('saving')
    const done = next.length >= totalSteps
    const { error } = await supabase.from('learning_progress').upsert({ student_id: session.id, material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: done ? new Date().toISOString() : null, updated_at: new Date().toISOString() }, { onConflict: 'student_id,material_code' })
    setStatus(error ? 'error' : 'ready')
    if (!error) onProgressUpdate?.({ material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: done ? new Date().toISOString() : null })
  }

  function checkLesson(index) {
    const questions = [ra11Checks[index], ...ra11ExtraChecks[index]]
    const correct = questions.every((item, questionIndex) => answers[`${index}-${questionIndex}`] === item.correct)
    setFeedback(current => ({ ...current, [index]: correct ? '¡Correcto! Tema completado.' : 'Revisa nuevamente los apuntes y vuelve a intentarlo.' }))
    if (correct) completeStep(`tema-${index + 1}`)
  }

  function runCommand(event) {
    event.preventDefault()
    const clean = command.trim().toLowerCase()
    const outputs = {
      ipconfig: 'IPv4: 192.168.10.24  Máscara: 255.255.255.0  Puerta de enlace: 192.168.10.1',
      'ping 192.168.10.1': 'Respuesta desde 192.168.10.1: tiempo=2ms. Conexión local correcta.',
      'ping 8.8.8.8': 'Respuesta desde 8.8.8.8: tiempo=24ms. Hay salida a otra red.',
      'tracert 8.8.8.8': '1  192.168.10.1\n2  10.20.0.1\n3  8.8.8.8  Ruta completada.',
    }
    setTerminal(current => [...current, `> ${command}`, outputs[clean] || 'Comando no reconocido. Prueba: ipconfig, ping 192.168.10.1, ping 8.8.8.8 o tracert 8.8.8.8'])
    setCommand('')
    const history = [...terminal, clean].join(' ').toLowerCase()
    if (history.includes('ipconfig') && history.includes('ping 192.168.10.1') && history.includes('tracert 8.8.8.8')) completeStep('practica-comandos')
  }

  async function uploadPacketPractice(practice, file) {
    if (!file) return
    if (!file.name.toLowerCase().endsWith('.pkt')) { setPracticeMessage(current => ({ ...current, [practice.id]: 'Selecciona el archivo .pkt que guardaste en Packet Tracer.' })); return }
    if (file.size > 20 * 1024 * 1024) { setPracticeMessage(current => ({ ...current, [practice.id]: 'El archivo supera el límite de 20 MB.' })); return }
    if (session?.preview) { setPracticeMessage(current => ({ ...current, [practice.id]: 'En la vista previa no se generan entregas.' })); return }
    if (!assessmentId) { setPracticeMessage(current => ({ ...current, [practice.id]: 'No fue posible identificar la actividad. Actualiza la página e inténtalo nuevamente.' })); return }
    setUploadingPractice(practice.id)
    setPracticeMessage(current => ({ ...current, [practice.id]: '' }))
    try {
      const { data: authData, error: authError } = await supabase.auth.getUser()
      if (authError || !authData.user) throw authError || new Error('La sesión ya no está disponible.')
      const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_')
      const path = `${authData.user.id}/${assessmentId}/packet-tracer/${practice.id}-${safeName}`
      const { error: uploadError } = await supabase.storage.from('submissions').upload(path, file, { upsert: true, contentType: file.type || 'application/octet-stream' })
      if (uploadError) throw uploadError
      const { data: existing, error: readError } = await supabase.from('submissions').select('id, answers, submitted_at').eq('assessment_id', assessmentId).maybeSingle()
      if (readError) throw readError
      if (existing?.submitted_at) throw new Error('La evaluación final ya fue entregada y no admite cambios.')
      const entry = { path, filename: file.name, practice: practice.title, uploaded_at: new Date().toISOString() }
      const nextUploads = { ...(existing?.answers?.packet_tracer || packetUploads), [practice.id]: entry }
      const answers = { ...(existing?.answers || {}), packet_tracer: nextUploads }
      const query = existing?.id
        ? supabase.from('submissions').update({ answers }).eq('id', existing.id)
        : supabase.from('submissions').insert({ assessment_id: assessmentId, student_id: authData.user.id, answers })
      const { error: saveError } = await query
      if (saveError) throw saveError
      setPacketUploads(nextUploads)
      await completeStep(practice.id)
      setPracticeMessage(current => ({ ...current, [practice.id]: 'Práctica entregada correctamente. Puedes reemplazarla antes de entregar la evaluación final.' }))
    } catch (error) {
      setPracticeMessage(current => ({ ...current, [practice.id]: error.message || 'No fue posible entregar el archivo.' }))
    } finally { setUploadingPractice('') }
  }

  const percent = Math.round(completed.length / totalSteps * 100)
  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="activity-hero"><div><span className="eyebrow">MTCS · R.A. 1.1 · MATERIAL DIDÁCTICO</span><h1>{definition.materialTitle}</h1><p>Aprende un tema, contesta su ejercicio y continúa. La evaluación se desbloquea al completar toda la ruta.</p></div><div className="mtcs-progress-ring"><strong>{percent}%</strong><span>COMPLETADO</span></div></div>
    <div className="learning-progress-bar"><i style={{ width: `${percent}%` }} /></div>
    <div className="learning-topic-list">{definition.lessons.map(([title, text], index) => { const done = completed.includes(`tema-${index + 1}`); const questions = [ra11Checks[index], ...ra11ExtraChecks[index]]; const answered = questions.every((_, questionIndex) => answers[`${index}-${questionIndex}`]); return <article className={done ? 'topic-complete' : ''} key={title}><header><span>{done ? <CheckCircle2 size={18} /> : index + 1}</span><div><small>TEMA {index + 1}</small><h2>{title.replace(/^\d+\.\s*/, '')}</h2></div></header><div className="topic-notes"><h3>Conceptos clave</h3><p>{text}</p><ul className="concept-list">{ra11Details[index].map(detail => <li key={detail}>{detail}</li>)}</ul><TopicDiagram index={index} /><div className="topic-example"><b>Para visualizarlo:</b> {index === 0 ? 'la red funciona como un servicio de mensajería: necesita remitente, destino, camino y reglas.' : index === 1 ? 'el dispositivo final crea o recibe; el intermediario dirige; el medio transporta.' : index === 2 ? 'cliente pregunta, servidor responde y el protocolo define cómo conversan.' : index === 3 ? 'tener señal no basta: debe llegar bien, soportar usuarios y estar protegida.' : index === 4 ? 'no existe un medio perfecto; se elige el que mejor resuelve la necesidad.' : 'las capas permiten revisar una parte del problema a la vez.'}</div></div><div className="topic-check"><b>Ejercicios del tema</b>{questions.map((check, questionIndex) => <div className="topic-question" key={check.question}><p>{questionIndex + 1}. {check.question}</p><div className="check-options">{check.options.map(option => <label key={option}><input type="radio" name={`check-${index}-${questionIndex}`} checked={answers[`${index}-${questionIndex}`] === option} onChange={() => setAnswers(current => ({ ...current, [`${index}-${questionIndex}`]: option }))} />{option}</label>)}</div></div>)}<button className="secondary" onClick={() => checkLesson(index)} disabled={!answered || done}>{done ? 'Ejercicios completados' : 'Comprobar respuestas'}</button>{feedback[index] && <small className={done ? 'correct-feedback' : 'wrong-feedback'}>{feedback[index]}</small>}</div></article> })}</div>
    <CommandGuide />
    <section className={`network-simulator ${completed.includes('practica-comandos') ? 'topic-complete' : ''}`}><div className="stage-heading"><span>PRÁCTICA OBLIGATORIA</span><h2>Simulador de diagnóstico de red</h2><p>Obtén la configuración, comprueba la puerta de enlace y observa la ruta. Debes ejecutar <b>ipconfig</b>, <b>ping 192.168.10.1</b> y <b>tracert 8.8.8.8</b>.</p></div><div className="fake-terminal">{terminal.map((line, index) => <pre key={`${line}-${index}`}>{line}</pre>)}<form onSubmit={runCommand}><span>C:\AulaVirtual&gt;</span><input value={command} onChange={event => setCommand(event.target.value)} placeholder="Escribe un comando" autoComplete="off" /><button>Ejecutar</button></form></div>{completed.includes('practica-comandos') && <div className="submission-success"><CheckCircle2 size={17} /> Práctica completada.</div>}</section>
    <PacketTracerPractices completed={completed} uploads={packetUploads} uploading={uploadingPractice} messages={practiceMessage} preview={session?.preview} onUpload={uploadPacketPractice} />
    {status === 'error' && <div className="form-error">No fue posible guardar el avance. Revisa la conexión y vuelve a intentarlo.</div>}
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}><ShieldCheck size={24} /><div><strong>{percent === 100 ? 'Actividad de evaluación desbloqueada' : 'Actividad de evaluación bloqueada'}</strong><p>{percent === 100 ? 'Ya puedes ir a Evaluaciones y comenzar la actividad del R.A. 1.1.' : `Completa los ${totalSteps - completed.length} pasos pendientes para desbloquearla.`}</p></div></div>
  </section>
}

function PacketTracerPractices({ completed, uploads, uploading, messages, preview, onUpload }) {
  return <section className="packet-tracer-section"><div className="stage-heading"><span>PRÁCTICAS EN PACKET TRACER</span><h2>Construye, prueba y entrega tus redes</h2><p>Realiza únicamente estas prácticas en Cisco Packet Tracer. Sigue el orden, comprueba el funcionamiento y sube el mismo archivo <b>.pkt</b> que terminaste.</p></div><div className="packet-practice-list">{packetTracerPractices.map((practice, index) => { const delivered = Boolean(uploads[practice.id]) || completed.includes(practice.id); return <article className={delivered ? 'practice-delivered' : ''} key={practice.id}><header><span>{delivered ? <CheckCircle2 size={20} /> : index + 1}</span><div><small>{practice.related}</small><h3>{practice.title}</h3></div></header><div className="packet-practice-body"><div className="practice-goal"><b>Meta</b><p>{practice.goal}</p></div><div className="practice-columns"><div><h4>Pasos</h4><ol>{practice.steps.map(step => <li key={step}>{step}</li>)}</ol></div><div><h4>Antes de entregar, comprueba</h4><ul>{practice.checks.map(check => <li key={check}>{check}</li>)}</ul></div></div><label className="packet-upload"><Upload size={20} /><span><strong>{uploads[practice.id]?.filename || 'Selecciona tu archivo de Packet Tracer'}</strong><small>Formato permitido: .pkt · máximo 20 MB</small></span><input type="file" accept=".pkt,application/octet-stream" disabled={uploading === practice.id || preview} onChange={event => onUpload(practice, event.target.files?.[0])} /></label>{uploading === practice.id && <div className="upload-status">Subiendo y vinculando tu práctica…</div>}{messages[practice.id] && <div className={delivered ? 'submission-success' : 'form-error'}>{messages[practice.id]}</div>}{delivered && !messages[practice.id] && <div className="submission-success"><CheckCircle2 size={17} /> Archivo entregado. Puedes reemplazarlo mientras no hayas enviado la evaluación final.</div>}</div></article> })}</div></section>
}

function TopicDiagram({ index }) {
  if (index === 5) return <div className="layer-diagram"><span>Aplicación</span><span>Transporte</span><span>Red</span><span>Acceso y medio</span></div>
  const diagrams = [
    ['Emisor', 'Datos', 'Medio', 'Receptor'],
    ['Computadora', 'Switch', 'Router', 'Internet'],
    ['Cliente', 'Solicitud', 'Servidor', 'Respuesta'],
    ['Dispositivo', 'Punto de acceso', 'Router', 'Internet'],
    ['Necesidad', 'Distancia', 'Ambiente', 'Medio adecuado'],
  ]
  return <div className="flow-diagram" aria-label="Esquema del tema">{diagrams[index].map((item, itemIndex) => <span key={item}>{item}{itemIndex < diagrams[index].length - 1 && <i>→</i>}</span>)}</div>
}

function CommandGuide() {
  const commands = [
    { name: 'ipconfig', purpose: 'Muestra la configuración de red del equipo.', use: 'Úsalo primero para conocer la dirección IP, máscara y puerta de enlace.', example: 'ipconfig' },
    { name: 'ping', purpose: 'Comprueba si otro dispositivo responde y mide el tiempo de comunicación.', use: 'Úsalo para saber si alcanzas la puerta de enlace, otro equipo o un destino de Internet.', example: 'ping 192.168.10.1' },
    { name: 'tracert', purpose: 'Muestra los saltos que sigue la información hasta el destino.', use: 'Úsalo cuando hay conexión parcial y necesitas localizar en qué tramo se interrumpe la ruta.', example: 'tracert 8.8.8.8' },
  ]
  return <section className="command-guide"><div className="stage-heading"><span>ANTES DEL SIMULADOR</span><h2>Herramientas básicas de diagnóstico</h2><p>Los comandos no reparan por sí solos la red: proporcionan información para localizar el problema y decidir qué revisar.</p></div><div className="command-grid">{commands.map(command => <article key={command.name}><code>{command.name}</code><h3>¿Para qué sirve?</h3><p>{command.purpose}</p><h3>¿Cuándo se utiliza?</h3><p>{command.use}</p><div><span>Ejemplo</span><b>C:\&gt; {command.example}</b></div></article>)}</div><div className="diagnostic-order"><b>Orden recomendado</b><span>1. Revisar configuración con <code>ipconfig</code></span><span>2. Probar comunicación local con <code>ping</code></span><span>3. Seguir la ruta con <code>tracert</code></span></div></section>
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
