import { useEffect, useState } from 'react'
import { Award, CalendarDays, ChevronRight, ClipboardCheck, TrendingUp } from 'lucide-react'
import { assessmentState, planFor, progressCodeFor } from './CoursePlan'

// Avisos que llevan al alumno a revisar Inicio, Tareas, Notas y Cronograma:
// insignias en el menú y una franja "¿Cómo voy?" visible mientras estudia el material.

const dayMs = 86400000
const todayKey = () => new Date().toLocaleDateString('en-CA')
const daysUntil = value => Math.round((new Date(`${value}T12:00:00`) - new Date(`${todayKey()}T12:00:00`)) / dayMs)
const REVISIT_DAYS = 7

function readStore(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback } catch { return fallback }
}
function writeStore(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)) } catch { /* sin almacenamiento: solo se pierde el recordatorio */ }
}

// Recuerda qué secciones visitó el alumno y qué calificaciones ya vio.
export function useSectionVisits(session, view, gradedIds) {
  const key = `aula-section-visits:${session.id || session.email}`
  const [visits, setVisits] = useState(() => readStore(key, {}))
  useEffect(() => { setVisits(readStore(key, {})) }, [key])
  useEffect(() => {
    if (!['inicio', 'evaluaciones', 'notas', 'cronograma'].includes(view)) return
    setVisits(current => {
      const next = { ...current, [view]: Date.now(), ...(view === 'notas' ? { seenGrades: [...new Set([...(current.seenGrades || []), ...gradedIds])] } : {}) }
      writeStore(key, next)
      return next
    })
  }, [key, view, view === 'notas' ? gradedIds.join() : ''])
  return visits
}

export function studentSignals({ session, courses, materials, assessments, learningProgress, isLocked, visits = {} }) {
  const assigned = assessments.filter(item => item.status === 'Activa' && courses.some(course => course.group === item.group)).map(item => ({ ...item, locked: isLocked(item, learningProgress) }))
  const states = assigned.map(item => ({ item, state: assessmentState(item, session) }))
  const available = states.filter(({ state }) => ['pending', 'late', 'draft'].includes(state.key))
  const late = available.filter(({ state }) => state.key === 'late').length
  const gradedIds = states.filter(({ state }) => state.key === 'graded').map(({ item }) => item.id)
  const newGrades = gradedIds.filter(id => !(visits.seenGrades || []).includes(id)).length

  const interactive = materials.filter(item => item.published && progressCodeFor(item) && courses.some(course => course.group === item.group))
  const finished = interactive.filter(item => learningProgress.some(progress => progress.material_code === progressCodeFor(item) && progress.completed_at)).length
  const percent = interactive.length ? Math.round(finished / interactive.length * 100) : 0

  const today = todayKey()
  const next = courses.flatMap(course => (planFor(course)?.ra || []).filter(ra => ra.ae && ra.ae >= today).map(ra => ({ course, ra }))).sort((a, b) => a.ra.ae.localeCompare(b.ra.ae))[0]
  const nextDays = next ? daysUntil(next.ra.ae) : null

  const stale = id => !visits[id] || Date.now() - visits[id] > REVISIT_DAYS * dayMs
  const nav = {
    inicio: { badge: `${percent}%`, tone: 'info', title: `Llevas ${percent}% del material` },
    evaluaciones: available.length ? { badge: String(available.length), tone: late ? 'bad' : 'warn', pulse: true, title: `${available.length} por entregar` } : null,
    notas: newGrades ? { badge: newGrades === 1 ? 'Nueva' : `${newGrades} nuevas`, tone: 'good', pulse: true, title: 'Tienes calificaciones nuevas' } : stale('notas') ? { dot: true, tone: 'good', title: 'Revisa cómo vas' } : null,
    cronograma: nextDays !== null && nextDays <= 7 ? { badge: nextDays === 0 ? 'Hoy' : `${nextDays} d`, tone: nextDays <= 3 ? 'bad' : 'warn', pulse: nextDays <= 3, title: `Evaluación de ${next.course.code} R.A. ${next.ra.code}` } : stale('cronograma') ? { dot: true, tone: 'info', title: 'Revisa tus fechas' } : null,
  }
  return { nav, percent, finished, total: interactive.length, toDeliver: available.length, late, newGrades, gradedIds, next, nextDays }
}

export function NavSignal({ signal }) {
  if (!signal) return null
  if (signal.dot) return <em className={`nav-signal dot ${signal.tone}`} title={signal.title} aria-label={signal.title} />
  return <em className={`nav-signal ${signal.tone} ${signal.pulse ? 'pulse' : ''}`} title={signal.title} aria-label={signal.title}>{signal.badge}</em>
}

export function ProgressStrip({ signals, setView }) {
  const { percent, finished, total, toDeliver, late, newGrades, next, nextDays } = signals
  const when = nextDays === 0 ? 'hoy' : nextDays === 1 ? 'mañana' : `en ${nextDays} días`
  return <nav className="progress-strip" aria-label="¿Cómo voy?">
    <span className="progress-strip-label">¿Cómo voy?</span>
    <button className="info" onClick={() => setView('inicio')}><TrendingUp size={16} /><span><strong><b>{percent}%</b> del material</strong><small>{finished} de {total} terminados</small></span><i style={{ '--strip-progress': `${Math.max(4, percent)}%` }} /></button>
    <button className={toDeliver ? (late ? 'bad attention' : 'warn attention') : 'good'} onClick={() => setView('evaluaciones')}><ClipboardCheck size={16} /><span><strong><b>{toDeliver || 'Sin'}</b> {toDeliver === 1 ? 'tarea' : 'tareas'} por entregar</strong><small>{late ? `${late} con fecha vencida` : toDeliver ? 'Ábrelas en Tareas' : '¡Vas al día!'}</small></span><ChevronRight size={15} /></button>
    <button className={newGrades ? 'good attention' : 'neutral'} onClick={() => setView('notas')}><Award size={16} /><span><strong>{newGrades ? <><b>{newGrades}</b> {newGrades === 1 ? 'calificación nueva' : 'calificaciones nuevas'}</> : <>Mis <b>notas</b></>}</strong><small>{newGrades ? 'Mira tu resultado' : 'Puntos que llevas por R.A.'}</small></span><ChevronRight size={15} /></button>
    {next && <button className={nextDays <= 3 ? 'bad attention' : nextDays <= 7 ? 'warn' : 'neutral'} onClick={() => setView('cronograma')}><CalendarDays size={16} /><span><strong>Evaluación <b>{when}</b></strong><small>{next.course.code} · R.A. {next.ra.code}</small></span><ChevronRight size={15} /></button>}
  </nav>
}
