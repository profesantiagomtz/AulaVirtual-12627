import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, CheckCircle2, ExternalLink } from 'lucide-react'
import { supabase } from '../lib/supabase'

const courseMaterials = {
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
}

export default function IntegratedCourseMaterial({ code, session, onBack, onProgressUpdate }) {
  const material = courseMaterials[code]
  const [progress, setProgress] = useState({ done: 0, total: 0, completed: false })
  const [message, setMessage] = useState('')
  const source = useMemo(() => material ? new URL(`${material.file}?student=${encodeURIComponent(session?.id || 'preview')}`, document.baseURI).href : '', [material, session?.id])

  useEffect(() => {
    if (!material || session?.preview || session?.role === 'teacher') return undefined
    let active = true
    supabase.from('learning_progress').select('completed_steps, completed_at').eq('student_id', session.id).eq('material_code', code).maybeSingle().then(({ data }) => {
      if (!active || !data) return
      const steps = Array.isArray(data.completed_steps) ? data.completed_steps : []
      setProgress({ done: steps.length, total: steps.length, completed: Boolean(data.completed_at) })
    })
    return () => { active = false }
  }, [code, material, session?.id, session?.preview])

  useEffect(() => {
    let timer
    async function receive(event) {
      if (event.origin !== window.location.origin || event.data?.type !== 'aula-course-progress' || event.data?.source !== code) return
      const done = Number(event.data.done) || 0
      const total = Number(event.data.total) || 0
      const completed = Boolean(event.data.completed)
      const next = { done, total, completed }
      setProgress(next)
      const record = {
        material_code: code,
        completed_steps: Array.from({ length: done }, (_, index) => `paso-${index + 1}`),
        completed_at: completed ? new Date().toISOString() : null,
        updated_at: new Date().toISOString(),
      }
      if (session?.role !== 'teacher') onProgressUpdate?.(record)
      if (session?.preview || session?.role === 'teacher') return
      clearTimeout(timer)
      timer = setTimeout(async () => {
        const { error } = await supabase.from('learning_progress').upsert({ student_id: session.id, ...record }, { onConflict: 'student_id,material_code' })
        setMessage(error ? 'El contenido funciona, pero no se pudo sincronizar el avance. Revisa tu conexión.' : completed ? '¡R.A. completado! Ya puedes continuar con la actividad de evaluación.' : 'Avance guardado automáticamente.')
      }, 500)
    }
    window.addEventListener('message', receive)
    return () => { window.removeEventListener('message', receive); clearTimeout(timer) }
  }, [code, onProgressUpdate, session?.id, session?.preview])

  if (!material) return null
  const percent = progress.total ? Math.round(progress.done / progress.total * 100) : progress.completed ? 100 : 0
  return <section className="integrated-course-page">
    <div className="integrated-course-toolbar">
      <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
      <a className="secondary" href={source} target="_blank" rel="noreferrer"><ExternalLink size={16} /> Abrir en pantalla completa</a>
    </div>
    <header className="integrated-course-header">
      <div><span className="eyebrow">{material.course} · {material.label} · MATERIAL DIDÁCTICO</span><h1>{material.title}</h1><p>{material.description}</p></div>
      <div className={progress.completed ? 'complete' : ''}><strong>{percent}%</strong><span>{progress.completed ? <><CheckCircle2 size={14} /> COMPLETADO</> : 'AVANCE'}</span></div>
    </header>
    {message && <div className={message.startsWith('El contenido') ? 'form-error' : 'submission-success'}>{message}</div>}
    <div className="integrated-course-frame"><iframe title={`${material.course} ${material.label}`} src={source} /></div>
  </section>
}
