import { useEffect, useMemo, useRef, useState } from 'react'
import { ArrowLeft, CheckCircle2, ExternalLink } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { assignmentFor } from '../lib/mtcs-assignment'
import PracticeCheck, { PracticeCheckButton, hasPracticeChecks } from './PracticeCheck'

const courseMaterials = {
  'EDOA-RA-1.2': {
    course: 'EDOA',
    label: 'R.A. 1.2',
    title: 'Inserción y formato de objetos',
    description: 'Tablas, imágenes, ajuste de texto y objetos de referencia en Word, con constructor de tablas, simulador de ajuste y prácticas.',
    file: 'courses/edoa-ra12-material.html',
  },
  'EDOA-RA-1.3': {
    course: 'EDOA',
    label: 'R.A. 1.3',
    title: 'Correspondencia y revisión colaborativa',
    description: 'Combinación de correspondencia, control de cambios y protección, con simuladores y prácticas en Word.',
    file: 'courses/edoa-ra13-material.html',
  },
  'EDOA-RA-2.1': {
    course: 'EDOA',
    label: 'R.A. 2.1',
    title: 'Formato de presentaciones electrónicas',
    description: 'Entorno de PowerPoint, diseño de diapositiva, formato y plantillas, con presentaciones simuladas, ejercicios y prácticas sobre la Feria de Carreras.',
    file: 'courses/edoa-ra21-material.html',
  },
  'EDOA-RA-2.2': {
    course: 'EDOA',
    label: 'R.A. 2.2',
    title: 'Objetos, animaciones y transiciones',
    description: 'Tablas, imágenes, vínculos, video y audio con formato, animaciones y transiciones, con presentaciones simuladas y prácticas.',
    file: 'courses/edoa-ra22-material.html',
  },
  'EDOA-RA-3.1': {
    course: 'EDOA',
    label: 'R.A. 3.1',
    title: 'Formato del libro y la hoja de cálculo',
    description: 'Lecciones, hojas de cálculo simuladas, ejercicios autocorregibles y prácticas con el caso de la cafetería del plantel.',
    file: 'courses/edoa-ra31-material.html',
  },
  'EDOA-RA-3.2': {
    course: 'EDOA',
    label: 'R.A. 3.2',
    title: 'Cálculos y funciones',
    description: 'Fórmulas, referencias, nombres y funciones de varias categorías, con cuatro hojas de cálculo simuladas, ejercicios y prácticas sobre la cafetería del plantel.',
    file: 'courses/edoa-ra32-material.html',
  },
  'EDOA-RA-3.3': {
    course: 'EDOA',
    label: 'R.A. 3.3',
    title: 'Gráficas y macros',
    description: 'Tipos, elementos, diseño y edición de gráficas, y macros con referencias absolutas y relativas, con seis simuladores sobre la cafetería del plantel.',
    file: 'courses/edoa-ra33-material.html',
  },
  'EDOA-RA-3.4': {
    course: 'EDOA',
    label: 'R.A. 3.4',
    title: 'Tablas dinámicas y protección',
    description: 'Tablas y gráficos dinámicos, vista preliminar y protección de hojas y libros, con cinco simuladores sobre las ventas de la cafetería.',
    file: 'courses/edoa-ra34-material.html',
  },
  'EDOA-RA-4.1': {
    course: 'EDOA',
    label: 'R.A. 4.1',
    title: 'Navegar y buscar seguro',
    description: 'Internet, IP, DNS y protocolos, partes del navegador, descargas seguras, phishing y búsqueda avanzada, con cuatro simuladores de navegador.',
    file: 'courses/edoa-ra41-material.html',
  },
  'EDOA-RA-4.2': {
    course: 'EDOA',
    label: 'R.A. 4.2',
    title: 'Configurar el cliente de correo',
    description: 'Servidores y clientes de correo, SMTP, POP3 e IMAP, puertos y seguridad, con dos simuladores de configuración de cuentas.',
    file: 'courses/edoa-ra42-material.html',
  },
  'EDOA-RA-4.3': {
    course: 'EDOA',
    label: 'R.A. 4.3',
    title: 'Correo y mensajería',
    description: 'Redactar con CC, CCO y adjuntos, filtros, carpetas, uso responsable, acuses y mensajería instantánea, con cuatro simuladores.',
    file: 'courses/edoa-ra43-material.html',
  },
  'MTCS-RA-1.2': {
    course: 'MTCS',
    label: 'R.A. 1.2',
    title: 'Direccionamiento y enrutamiento IPv4',
    description: 'Direcciones IPv4, máscaras, subredes, gateway, IPv6 y DHCP, con calculadora de subredes, revisor de gateway, ejercicios y prácticas.',
    file: 'courses/mtcs-ra12-material.html',
  },
  'MTCS-RA-2.1': {
    course: 'MTCS',
    label: 'R.A. 2.1',
    title: 'Fundamentos de ciberseguridad',
    description: 'Principios, amenazas, ataques y protección, con detective de phishing, medidor de contraseñas, ejercicios y prácticas sobre el caso de un gimnasio.',
    file: 'courses/mtcs-ra21-material.html',
  },
  'MTCS-RA-2.2': {
    course: 'MTCS',
    label: 'R.A. 2.2',
    title: 'Integridad, disponibilidad y defensa de sistemas',
    description: 'Lecciones, laboratorio de hash, ejercicios autocorregibles y prácticas sobre el caso de una clínica dental.',
    file: 'courses/mtcs-ra22-material.html',
  },
  'MTCS-RA-3.1': {
    course: 'MTCS',
    label: 'R.A. 3.1',
    title: 'Fundamentos y lenguajes de programación',
    description: 'Programación en Python: variables, tipos de datos, operadores, errores y herramientas, con un laboratorio que ejecuta tu código aquí mismo.',
    file: 'courses/mtcs-ra31-material.html',
  },
  'MTCS-RA-3.2': {
    course: 'MTCS',
    label: 'R.A. 3.2',
    title: 'Estructuras de flujo de control y funciones',
    description: 'Python con decisiones, ciclos, listas, operadores de bits, funciones y excepciones, con siete laboratorios que ejecutan tu código aquí mismo.',
    file: 'courses/mtcs-ra32-material.html',
  },
  'ASIN-RA-1.2': {
    course: 'ASIN',
    label: 'R.A. 1.2',
    title: 'Plan de seguridad en cómputo',
    description: 'Teoría, ejemplos, ejercicios autocorregibles, simulador y prácticas para elaborar un plan de seguridad.',
    file: 'courses/asin-ra12-material.html',
  },
  'MSII-RA-1.2': {
    course: 'MSII',
    label: 'R.A. 1.2',
    title: 'Gestión de recursos del sistema operativo',
    description: 'Ruta interactiva sobre datos, CPU, memoria, periféricos, almacenamiento y respaldos.',
    file: 'courses/msii-ra12-material.html',
  },
  'ASIN-RA-2.1': {
    course: 'ASIN',
    label: 'R.A. 2.1',
    title: 'Instala y configura herramientas de seguridad',
    description: 'Manual de instalación, configuración local (actualizaciones, cuentas, bitácoras, firewall, antivirus, permisos y cifrado) y seguridad en red.',
    file: 'courses/asin-ra21-material.html',
  },
  'MSII-RA-2.1': {
    course: 'MSII',
    label: 'R.A. 2.1',
    title: 'Opera el sistema operativo con comandos',
    description: 'Sistema operativo, rutas, CMD, variables de entorno y PowerShell, con consolas simuladas para practicar sin riesgo.',
    file: 'courses/msii-ra21-material.html',
  },
  'ASIN-RA-2.2': {
    course: 'ASIN',
    label: 'R.A. 2.2',
    title: 'Da seguimiento a las herramientas de seguridad',
    description: 'Reportes de estado, modificación de configuraciones con control de cambios y respaldo de configuraciones, con un centro de seguridad simulado.',
    file: 'courses/asin-ra22-material.html',
  },
  'ASIN-RA-2.3': {
    course: 'ASIN',
    label: 'R.A. 2.3',
    title: 'Controla parámetros de seguridad',
    description: 'Auditoría de equipos y red contra el plan de seguridad, métricas, nuevos requerimientos, planes de contingencia y actualizaciones, con una consola de auditoría simulada.',
    file: 'courses/asin-ra23-material.html',
  },
  'MSII-RA-2.2': {
    course: 'MSII',
    label: 'R.A. 2.2',
    title: 'Opera el sistema operativo multiusuario',
    description: 'Linux multiusuario: archivos, discos, usuarios, permisos, programas, procesos y memoria, con terminales simuladas.',
    file: 'courses/msii-ra22-material.html',
  },
}

// El material vive en un iframe: se le pasan los colores de la skin activa para que se vea como parte de la plataforma.
function platformTheme() {
  const root = document.documentElement
  const style = getComputedStyle(root)
  const get = name => style.getPropertyValue(name).trim()
  const dark = root.dataset.aulaTheme === 'oscuro'
  const cuaderno = root.dataset.aulaTheme === 'clasico'
  return {
    type: 'aula-theme',
    dark,
    // Con el tema Cuaderno, el material también toma su tipografía, la pasta y el marcatextos.
    skin: cuaderno ? 'cuaderno' : null,
    vars: {
      '--bg': get('--surface-soft') || '#f4f6fa',
      '--card': get('--surface') || '#ffffff',
      '--ink': get('--ink') || '#14213d',
      '--mut': get('--muted') || '#5b6b85',
      '--line': get('--line') || '#e2e8f0',
      '--pri': (dark ? get('--blue') : get('--navy-2')) || '#1b3fa0',
      '--on': dark ? '#07131f' : '#ffffff',
      '--ok': get('--green') || '#1e8e4e',
      '--bad': get('--red') || '#c62f3a',
      '--amb': dark ? '#f2b53a' : (get('--gold') || '#f2a900'),
      '--pasta': cuaderno ? get('--pasta') : '',
      '--marca': cuaderno ? get('--marcatextos') : '',
    },
  }
}

export default function IntegratedCourseMaterial({ code, session, assessment, onBack, onProgressUpdate }) {
  const material = courseMaterials[code]
  const [checking, setChecking] = useState(false)
  // «¿Voy bien?» usa los mismos datos asignados que la actividad de evaluación del R.A.
  const checkAssessmentId = assessment?.id ?? (session?.preview ? 'vista-previa' : null)
  const assignment = useMemo(() => hasPracticeChecks(code) && checkAssessmentId ? assignmentFor(session?.id, checkAssessmentId, code) : null, [code, checkAssessmentId, session?.id])
  const [progress, setProgress] = useState({ done: 0, total: 0, completed: false })
  const [message, setMessage] = useState('')
  const persisted = useRef(Promise.resolve({ done: 0, completed: false }))
  const frame = useRef(null)
  const source = useMemo(() => material ? new URL(`${material.file}?student=${encodeURIComponent(session?.id || 'preview')}`, document.baseURI).href : '', [material, session?.id])

  useEffect(() => {
    if (!material || !supabase || session?.preview || session?.role === 'teacher') return undefined
    let active = true
    persisted.current = supabase.from('learning_progress').select('completed_steps, completed_at').eq('student_id', session.id).eq('material_code', code).maybeSingle().then(({ data }) => {
      const steps = Array.isArray(data?.completed_steps) ? data.completed_steps : []
      const stored = { done: steps.length, completed: Boolean(data?.completed_at) }
      // El total de pasos no se guarda; se conoce hasta que el material envía su avance.
      if (active && data) setProgress({ ...stored, total: 0 })
      return stored
    })
    return () => { active = false }
  }, [code, material, session?.id, session?.preview, session?.role])

  useEffect(() => {
    let timer
    async function receive(event) {
      if (event.origin !== window.location.origin || event.data?.type !== 'aula-course-progress' || event.data?.source !== code) return
      const done = Number(event.data.done) || 0
      const total = Number(event.data.total) || 0
      const completed = Boolean(event.data.completed)
      const next = { done, total, completed }
      const record = {
        material_code: code,
        completed_steps: Array.from({ length: done }, (_, index) => `paso-${index + 1}`),
        completed_at: completed ? new Date().toISOString() : null,
        ...(total ? { total_steps: total } : {}),
        updated_at: new Date().toISOString(),
      }
      if (!supabase || session?.preview || session?.role === 'teacher') {
        setProgress(next)
        if (session?.role !== 'teacher') onProgressUpdate?.(record)
        return
      }
      clearTimeout(timer)
      timer = setTimeout(async () => {
        // El material guarda su estado en el navegador; en otro equipo inicia vacío y no debe borrar el avance guardado.
        const stored = await persisted.current
        if (!completed && (stored.completed || done < stored.done)) return
        persisted.current = Promise.resolve({ done, completed })
        setProgress(next)
        onProgressUpdate?.(record)
        let { error } = await supabase.from('learning_progress').upsert({ student_id: session.id, ...record }, { onConflict: 'student_id,material_code' })
        // Antes de correr supabase/seguimiento_asistencia.sql no existe total_steps; se guarda sin él.
        if (error && /total_steps/.test(error.message || '')) {
          const { total_steps: _total, ...withoutTotal } = record
          ;({ error } = await supabase.from('learning_progress').upsert({ student_id: session.id, ...withoutTotal }, { onConflict: 'student_id,material_code' }))
        }
        setMessage(error ? 'El contenido funciona, pero no se pudo sincronizar el avance. Revisa tu conexión.' : completed ? '¡R.A. completado! Ya puedes continuar con la actividad de evaluación.' : 'Avance guardado automáticamente.')
      }, 500)
    }
    window.addEventListener('message', receive)
    return () => { window.removeEventListener('message', receive); clearTimeout(timer) }
  }, [code, onProgressUpdate, session?.id, session?.preview, session?.role])

  const sendTheme = () => frame.current?.contentWindow?.postMessage(platformTheme(), window.location.origin)
  useEffect(() => {
    const observer = new MutationObserver(sendTheme)
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-aula-theme'] })
    const onRequest = event => { if (event.origin === window.location.origin && event.data?.type === 'aula-theme-request') sendTheme() }
    window.addEventListener('message', onRequest)
    return () => { observer.disconnect(); window.removeEventListener('message', onRequest) }
  }, [])

  if (!material) return null
  const percent = progress.completed ? 100 : progress.total ? Math.round(progress.done / progress.total * 100) : null
  return <section className="integrated-course-page">
    <div className="integrated-course-bar">
      <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Materiales</button>
      <div className="icb-title"><span>{material.course} · {material.label}</span><h1>{material.title}</h1></div>
      <div className={`icb-progress ${progress.completed ? 'complete' : ''}`} title="Avance del material">
        <i><b style={{ width: `${percent ?? 0}%` }} /></i>
        <strong>{progress.completed ? <><CheckCircle2 size={15} /> Completado</> : percent === null ? `${progress.done} ${progress.done === 1 ? 'paso' : 'pasos'}` : `${percent}%`}</strong>
      </div>
      {assignment && session?.role !== 'teacher' && <PracticeCheckButton compact onClick={() => setChecking(true)} />}
      <a className="icb-full" href={source} target="_blank" rel="noreferrer" title="Abrir en pantalla completa" aria-label="Abrir en pantalla completa"><ExternalLink size={16} /></a>
    </div>
    {message && <div className={message.startsWith('El contenido') ? 'form-error' : 'submission-success'}>{message}</div>}
    {checking && <PracticeCheck code={code} label={`${material.course} · ${material.label}`} assignment={assignment} session={session} onClose={() => setChecking(false)} />}
    <div className="integrated-course-frame"><iframe ref={frame} onLoad={sendTheme} title={`${material.course} ${material.label}`} src={source} /></div>
  </section>
}
