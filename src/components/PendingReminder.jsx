import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { Award, BookOpen, CalendarDays, ChevronRight, ClipboardCheck, Lock, X } from 'lucide-react'
import { assessmentState, buildRaSections, planFor, progressCodeFor, raStatus, shortDate } from './CoursePlan'

// Recordatorio que aparece al alumno al entrar: lo que tiene pendiente, con un botón para ir a cada cosa.
// Sale al iniciar sesión y, si la sesión sigue abierta, la primera vez de cada día.

const dayMs = 86400000
const todayKey = () => new Date().toLocaleDateString('en-CA')
const daysUntil = value => Math.round((new Date(`${value}T12:00:00`) - new Date(`${todayKey()}T12:00:00`)) / dayMs)
export const FRESH_LOGIN_KEY = 'aula-reminder-login'
const MAX_ITEMS = 5

function seenToday(key) { try { return localStorage.getItem(key) === todayKey() } catch { return false } }
function markSeen(key) { try { localStorage.setItem(key, todayKey()); sessionStorage.removeItem(FRESH_LOGIN_KEY) } catch { /* sin almacenamiento: puede volver a salir */ } }
function freshLogin() { try { return sessionStorage.getItem(FRESH_LOGIN_KEY) === '1' } catch { return false } }

const when = days => days < 0 ? `venció hace ${-days} ${days === -1 ? 'día' : 'días'}` : days === 0 ? 'vence hoy' : days === 1 ? 'vence mañana' : `vence en ${days} días`

// Lista ordenada por urgencia: vencidas, por entregar, material del R.A. en curso, evaluación cercana y notas nuevas.
export function pendingItems({ session, courses, materials, assessments, learningProgress: allProgress, isLocked, signals }) {
  const items = []
  // Solo el avance propio (RLS ya lo filtra; en la vista sin conexión vienen filas de varios alumnos).
  const learningProgress = allProgress.filter(row => !row.student_id || row.student_id === session.id)
  const active = assessments.filter(item => item.status === 'Activa' && courses.some(course => course.group === item.group))
  active.forEach(assessment => {
    const state = assessmentState({ ...assessment, locked: isLocked(assessment, learningProgress) }, session)
    if (!['pending', 'late', 'draft'].includes(state.key)) return
    const days = assessment.dueAt ? daysUntil(String(assessment.dueAt).slice(0, 10)) : null
    items.push({
      id: `tarea-${assessment.id}`, kind: 'task', tone: state.key === 'late' ? 'bad' : days !== null && days <= 2 ? 'warn' : 'info',
      rank: state.key === 'late' ? 0 : 1 + Math.min(days ?? 30, 30) / 100,
      title: assessment.title, detail: state.key === 'late' ? 'Fecha vencida, pero aún la puedes entregar' : `${state.key === 'draft' ? 'Ya tienes avance guardado · ' : ''}${days === null ? 'Sin fecha límite' : `Entrega ${assessment.due} · ${when(days)}`}`,
      action: 'Entregar', target: { view: 'evaluaciones', assessment },
    })
  })

  courses.forEach(course => {
    const sameGroup = courses.filter(candidate => candidate.group === course.group)
    const { sections } = buildRaSections(course, materials.filter(item => item.published), active, sameGroup)
    sections.filter(section => raStatus(section.ra) === 'actual').forEach(section => {
      section.materials.filter(material => progressCodeFor(material)).forEach(material => {
        const progress = learningProgress.find(row => row.material_code === progressCodeFor(material))
        if (progress?.completed_at) return
        const done = (progress?.completed_steps || []).length
        const percent = progress?.total_steps ? Math.round(done / progress.total_steps * 100) : null
        const locked = section.assessments.find(assessment => isLocked(assessment, learningProgress))
        items.push({
          id: `material-${material.id}`, kind: 'material', tone: locked ? 'warn' : 'info', rank: 2,
          title: `${course.code} · R.A. ${section.ra.code} · ${section.ra.title}`,
          detail: `${done ? `Llevas ${percent ?? done}${percent === null ? ` ${done === 1 ? 'paso' : 'pasos'}` : '%'}` : 'Aún no lo empiezas'}${locked ? ' · termínalo para desbloquear su tarea' : ''}`,
          percent, locked: Boolean(locked), action: done ? 'Continuar' : 'Empezar', target: { view: 'materiales', material },
        })
      })
    })
  })

  if (signals?.next && signals.nextDays <= 7) {
    const { course, ra } = signals.next
    items.push({ id: 'evaluacion', kind: 'exam', tone: signals.nextDays <= 3 ? 'bad' : 'warn', rank: 3, title: `Evaluación de ${course.code} · R.A. ${ra.code}`, detail: `${shortDate(ra.ae)} · ${signals.nextDays === 0 ? 'es hoy' : signals.nextDays === 1 ? 'es mañana' : `en ${signals.nextDays} días`}`, action: 'Ver fechas', target: { view: 'cronograma' } })
  }
  if (signals?.newGrades) items.push({ id: 'notas', kind: 'grade', tone: 'good', rank: 4, title: signals.newGrades === 1 ? 'Tienes una calificación nueva' : `Tienes ${signals.newGrades} calificaciones nuevas`, detail: 'Mira cómo te fue', action: 'Ver notas', target: { view: 'notas' } })
  return items.sort((a, b) => a.rank - b.rank)
}

export function usePendingReminder(session, enabled, count) {
  const key = `aula-reminder:${session?.id || session?.email}`
  const [open, setOpen] = useState(false)
  useEffect(() => {
    if (!enabled || !count || open) return
    if (freshLogin() || !seenToday(key)) { setOpen(true); markSeen(key) }
  }, [enabled, count, key])
  return [open, () => setOpen(false)]
}

const icons = { task: ClipboardCheck, material: BookOpen, exam: CalendarDays, grade: Award }

export function PendingReminder({ session, items, onGo, onClose }) {
  const dialog = useRef(null)
  const firstAction = useRef(null)
  useEffect(() => {
    firstAction.current?.focus()
    const onKey = event => { if (event.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])
  const shown = items.slice(0, MAX_ITEMS)
  const tasks = items.filter(item => item.kind === 'task').length
  const late = items.filter(item => item.tone === 'bad' && item.kind === 'task').length
  const name = String(session.name || '').split(' ')[0]
  const intro = late ? `Tienes ${late === 1 ? 'una tarea vencida' : `${late} tareas vencidas`} que aún puedes entregar. Empieza por ahí.`
    : tasks ? `Tienes ${tasks === 1 ? 'una tarea' : `${tasks} tareas`} por entregar. Con un poco cada día terminas a tiempo.`
    : 'Esto es lo que sigue para que no se te junte el trabajo.'
  // Se dibuja directo en <body> para quedar encima del menú inferior del celular.
  return createPortal(<div className="reminder-backdrop" onMouseDown={event => { if (event.target === event.currentTarget) onClose() }}>
    <section className="reminder" role="dialog" aria-modal="true" aria-labelledby="reminder-title" aria-describedby="reminder-intro" ref={dialog}>
      <span className="reminder-tape" aria-hidden="true" />
      <button type="button" className="icon-btn reminder-close" onClick={onClose} aria-label="Cerrar recordatorio"><X size={19} /></button>
      <header>
        <small>Recordatorio · {new Date().toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'long' })}</small>
        <h2 id="reminder-title">Hola, {name}. Esto tienes pendiente</h2>
        <p id="reminder-intro">{intro}</p>
      </header>
      <ol className="reminder-list">{shown.map((item, index) => {
        const Icon = item.locked ? Lock : icons[item.kind]
        return <li key={item.id} className={item.tone} style={{ '--i': index }}>
          <span className="reminder-icon"><Icon size={18} /></span>
          <div><strong>{item.title}</strong><small>{item.detail}</small>{item.percent !== null && item.percent !== undefined && <i className="reminder-bar"><b style={{ width: `${Math.max(4, item.percent)}%` }} /></i>}</div>
          <button type="button" ref={index === 0 ? firstAction : undefined} className={index === 0 ? 'primary small' : 'secondary small'} onClick={() => onGo(item.target)}>{item.action}<ChevronRight size={15} /></button>
        </li>
      })}</ol>
      {items.length > shown.length && <p className="reminder-more">Y {items.length - shown.length} {items.length - shown.length === 1 ? 'pendiente más' : 'pendientes más'} en Tareas y Material.</p>}
      <footer><button type="button" className="text-btn" onClick={onClose}>Después</button><span>Lo verás otra vez mañana o cuando vuelvas a iniciar sesión.</span></footer>
    </section>
  </div>, document.body)
}
