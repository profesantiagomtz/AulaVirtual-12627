import { useMemo, useState } from 'react'
import { BookOpen, CalendarDays, CheckCircle2, ChevronRight, ClipboardCheck, Clock3, FileText, Lock, Star, Unlock } from 'lucide-react'
import { coursePlans } from '../data/plan'

// Organización por resultado de aprendizaje (R.A.), como en el programa de estudios:
// cada materia muestra sus R.A. con horas, ponderación y fechas, y dentro de cada uno su material y su evaluación.

export function itemBelongsToCourse(item, course, sameGroupCourses) {
  if (item.group !== course.group) return false
  const code = item.activityCode?.split('-')[0]
  if (code) return code === course.code
  if (String(item.title || '').toUpperCase().includes(course.code)) return true
  return sameGroupCourses.length === 1
}

const dayMs = 86400000
const parseDay = value => value ? new Date(`${value}T12:00:00`) : null
const todayKey = () => new Date().toLocaleDateString('en-CA')
export const shortDate = value => value ? parseDay(value).toLocaleDateString('es-MX', { day: 'numeric', month: 'short' }).replace('.', '') : '—'
const longDate = value => value ? parseDay(value).toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'long' }).replace(/^./, letter => letter.toUpperCase()) : '—'
const daysUntil = value => Math.round((parseDay(value) - parseDay(todayKey())) / dayMs)

export function planFor(course) { return coursePlans[course?.code] || null }

export function raStatus(ra) {
  const today = todayKey()
  if (ra.start && today < ra.start) return 'proximo'
  if (ra.ae && today > ra.ae) return 'concluido'
  return 'actual'
}

export function currentRa(course) {
  const plan = planFor(course)
  if (!plan) return null
  return plan.ra.find(ra => raStatus(ra) === 'actual') || plan.ra.find(ra => raStatus(ra) === 'proximo') || plan.ra.at(-1)
}

export function nextSession(course) {
  const plan = planFor(course)
  const today = todayKey()
  return plan?.sessions.find(day => day >= today) || null
}

// R.A. al que pertenece un material o una evaluación ("1.2"), a partir de su código, enlace, unidad o título.
export function raCodeOf(item, course) {
  const plan = planFor(course)
  const source = `${item.activityCode || ''} ${item.url || ''}`
  const direct = source.match(/[A-Z]{4}-(?:RA-)?(\d)\.(\d)/) || `${item.unit || ''} ${item.title || ''}`.match(/(?:R\.?\s?A\.?|propósito|proposito)\s*(\d)\.(\d)/i)
  if (direct) return `${direct[1]}.${direct[2]}`
  const unit = `${source} ${item.unit || ''}`.match(/(?:UNIT-|-U|Unidad\s*)(\d)/i)
  if (unit && plan) {
    const unitRas = plan.ra.filter(ra => ra.code.startsWith(`${unit[1]}.`))
    if (unitRas.length) return item.activityCode ? unitRas.at(-1).code : unitRas[0].code
  }
  return null
}

export function progressCodeFor(material) {
  if (material.url === 'edoa://EDOA-WORD-U1') return 'EDOA-RA-1.1'
  const match = String(material.url || '').match(/^(?:mtcs|edoa|courseware):\/\/(.+)$/)
  return match ? match[1] : null
}

export function ownSubmission(assessment, session) {
  const details = assessment.submissionDetails || []
  return details.find(item => item.student_id === session?.id) || (session?.role === 'student' ? details[0] : null) || null
}

export function assessmentState(assessment, session) {
  const submission = ownSubmission(assessment, session)
  if (submission?.score !== null && submission?.score !== undefined) return { key: 'graded', label: `Calificada · ${Number(submission.score)}/60`, submission }
  if (submission?.submitted_at) return { key: 'sent', label: 'Entregada', submission }
  if (assessment.locked) return { key: 'locked', label: 'Bloqueada' }
  if (assessment.overdue) return { key: 'late', label: 'Vencida · aún abierta' }
  if (submission) return { key: 'draft', label: 'Con avance' }
  return { key: 'pending', label: 'Pendiente' }
}

// Material y evaluaciones de una materia, agrupados por R.A. en el orden del programa.
export function buildRaSections(course, materials, assessments, sameGroupCourses) {
  const plan = planFor(course)
  const courseMaterials = materials.filter(item => itemBelongsToCourse(item, course, sameGroupCourses))
  const courseAssessments = assessments.filter(item => itemBelongsToCourse(item, course, sameGroupCourses))
  const sections = (plan?.ra || []).map(ra => ({ ra, materials: [], assessments: [] }))
  const extra = { ra: null, materials: [], assessments: [] }
  const place = (item, list) => {
    const code = raCodeOf(item, course)
    const section = sections.find(entry => entry.ra.code === code) || extra
    section[list].push(item)
  }
  courseMaterials.forEach(item => place(item, 'materials'))
  courseAssessments.forEach(item => place(item, 'assessments'))
  return { plan, sections, extra, courseMaterials, courseAssessments }
}

function DateChip({ ra }) {
  return <span className="ra-chip"><CalendarDays size={13} />{shortDate(ra.start)} – {shortDate(ra.ae || ra.end)}</span>
}

const statusLabels = { actual: 'En curso', proximo: 'Próximo', concluido: 'Concluido' }

export function RaCourseMap({ course, sameGroupCourses, materials, assessments, learningProgress = [], session, isTeacher, students = [], onOpenMaterial, onOpenAssessment, onToggleMaterial }) {
  const { sections, extra } = useMemo(() => buildRaSections(course, materials, assessments, sameGroupCourses), [course, materials, assessments, sameGroupCourses])
  const groupStudents = students.filter(student => student.group === course.group)
  const progressOf = material => {
    const code = progressCodeFor(material)
    if (!code) return null
    const rows = learningProgress.filter(item => item.material_code === code)
    if (isTeacher) return { finished: rows.filter(item => item.completed_at).length, started: rows.length }
    const row = rows[0]
    return row ? { done: Boolean(row.completed_at), steps: (row.completed_steps || []).length } : { done: false, steps: 0 }
  }
  const visibleSections = isTeacher ? sections : sections.filter(section => section.materials.length || section.assessments.length || raStatus(section.ra) !== 'proximo')
  let number = 0
  const materialRow = material => {
    number += 1
    const progress = progressOf(material)
    const state = isTeacher ? (material.system ? 'Integrado' : material.published ? 'Publicado' : 'Oculto') : progress?.done ? 'Terminado' : progress?.steps ? 'En curso' : progress ? 'Sin iniciar' : 'Recurso'
    return <li className={`ra-item material ${!material.published ? 'hidden-item' : ''} ${progress?.done ? 'done' : ''}`} key={`m-${material.id}`}>
      <span className="ra-num">{progress?.done ? <CheckCircle2 size={17} /> : number}</span>
      <div className="ra-item-icon"><BookOpen size={18} /></div>
      <div className="ra-item-main"><strong>{material.title}</strong><small>{material.description || material.type}{isTeacher && progress && groupStudents.length ? ` · ${progress.finished}/${groupStudents.length} lo terminaron` : ''}</small></div>
      <span className={`ra-badge ${isTeacher ? (material.published ? 'ok' : 'muted') : progress?.done ? 'ok' : progress?.steps ? 'warn' : 'muted'}`}>{state}</span>
      <div className="ra-item-actions">
        {isTeacher && !material.system && <button className="lock-btn" onClick={() => onToggleMaterial?.(material)}>{material.published ? <Lock size={14} /> : <Unlock size={14} />}{material.published ? 'Ocultar' : 'Publicar'}</button>}
        <button className={!isTeacher && !progress?.done ? 'primary small' : 'secondary small'} onClick={() => onOpenMaterial?.(material)}>{isTeacher ? 'Abrir' : progress?.done ? 'Repasar' : progress?.steps ? 'Continuar' : 'Iniciar'}<ChevronRight size={15} /></button>
      </div>
    </li>
  }
  const assessmentRow = assessment => {
    number += 1
    const state = isTeacher ? null : assessmentState(assessment, session)
    return <li className={`ra-item task ${state?.key || ''}`} key={`a-${assessment.id}`}>
      <span className="ra-num">{state?.key === 'graded' || state?.key === 'sent' ? <CheckCircle2 size={17} /> : number}</span>
      <div className="ra-item-icon task">{assessment.locked ? <Lock size={18} /> : <ClipboardCheck size={18} />}</div>
      <div className="ra-item-main"><strong>{assessment.title}</strong><small>Actividad de evaluación · Entrega {assessment.due}{isTeacher ? ` · ${assessment.submissions}/${assessment.total} entregas` : assessment.locked ? ' · Termina primero el material' : ''}</small></div>
      <span className={`ra-badge ${isTeacher ? (assessment.status === 'Activa' ? 'ok' : 'muted') : { graded: 'ok', sent: 'ok', locked: 'muted', late: 'bad', draft: 'warn', pending: 'warn' }[state.key]}`}>{isTeacher ? assessment.status : state.label}</span>
      <div className="ra-item-actions"><button className={!isTeacher && ['pending', 'late', 'draft'].includes(state?.key) ? 'primary small' : 'secondary small'} disabled={!isTeacher && assessment.locked} onClick={() => onOpenAssessment?.(assessment)}>{isTeacher ? 'Resultados' : state.key === 'locked' ? 'Bloqueada' : ['graded', 'sent'].includes(state.key) ? 'Ver' : 'Entregar'}<ChevronRight size={15} /></button></div>
    </li>
  }
  const section = ({ ra, materials: raMaterials, assessments: raAssessments }) => {
    const status = ra ? raStatus(ra) : 'actual'
    number = 0
    const finished = !isTeacher && raMaterials.length > 0 && raMaterials.every(material => progressOf(material)?.done)
    const pending = !isTeacher && raAssessments.some(item => ['pending', 'late', 'draft'].includes(assessmentState(item, session).key))
    return <details className={`ra-unit ${status}`} key={ra?.code || 'extra'} open={status === 'actual' || pending}>
      <summary>
        <span className="ra-code">{ra ? `R.A. ${ra.code}` : 'Extra'}</span>
        <span className="ra-title"><strong>{ra ? ra.title : 'Otros recursos'}</strong>{ra && <span className="ra-chips"><span className="ra-chip"><Clock3 size={13} />{ra.hours} h</span><span className="ra-chip"><Star size={13} />Vale {ra.weight}%</span><DateChip ra={ra} /></span>}</span>
        {ra && <span className={`ra-status ${pending ? 'pending' : finished ? 'done' : status}`}>{pending ? 'Tarea pendiente' : finished ? 'Material terminado' : statusLabels[status]}</span>}
        <ChevronRight className="ra-caret" size={18} />
      </summary>
      {raMaterials.length || raAssessments.length
        ? <ol className="ra-items">{raMaterials.map(materialRow)}{raAssessments.map(assessmentRow)}</ol>
        : <p className="ra-empty">{status === 'proximo' ? `Este R.A. inicia el ${longDate(ra.start)}. Su material se publicará entonces.` : 'Aún no hay material publicado para este R.A.'}</p>}
      {ra?.ae && <p className="ra-foot"><CalendarDays size={14} />Actividad de evaluación: <b>{longDate(ra.ae)}</b></p>}
    </details>
  }
  return <div className="ra-map">
    {visibleSections.map(section)}
    {(extra.materials.length > 0 || extra.assessments.length > 0) && section(extra)}
  </div>
}

// Notas: lo que vale cada R.A. y lo que el alumno lleva acumulado (las actividades se califican sobre 60).
export function gradeRows(course, assessments, sameGroupCourses, session) {
  const { sections } = buildRaSections(course, [], assessments, sameGroupCourses)
  return sections.map(({ ra, assessments: raAssessments }) => {
    const scores = raAssessments.map(item => ownSubmission(item, session)).filter(item => item?.score !== null && item?.score !== undefined).map(item => Number(item.score))
    const sent = raAssessments.some(item => ownSubmission(item, session)?.submitted_at)
    const score = scores.length ? scores.reduce((sum, value) => sum + value, 0) / scores.length : null
    return { ra, score, points: score === null ? null : score / 60 * ra.weight, sent, hasActivity: raAssessments.length > 0 }
  })
}

export function StudentGrades({ courses, assessments, session }) {
  const [courseCode, setCourseCode] = useState(courses[0]?.code)
  const course = courses.find(item => item.code === courseCode) || courses[0]
  if (!course) return <section className="panel page-panel"><p className="ra-empty">No tienes módulos asignados.</p></section>
  const sameGroup = courses.filter(item => item.group === course.group)
  const rows = gradeRows(course, assessments, sameGroup, session)
  const earned = rows.reduce((sum, row) => sum + (row.points || 0), 0)
  const evaluated = rows.filter(row => row.points !== null).reduce((sum, row) => sum + row.ra.weight, 0)
  return <section className="panel page-panel">
    <div className="list-toolbar"><div><span className="eyebrow">GRUPO {session.group}</span><h1>Mis notas</h1><p>Cada R.A. vale un porcentaje de tu calificación final. Aquí ves cuánto llevas.</p></div></div>
    <CourseChips courses={courses} value={course.code} onChange={setCourseCode} />
    <div className="grade-summary">
      <div><span>Puntos acumulados</span><strong>{earned.toFixed(1)}<small> / 100</small></strong></div>
      <div><span>Ya evaluado</span><strong>{evaluated}%<small> del curso</small></strong></div>
      <div><span>Promedio en lo evaluado</span><strong>{evaluated ? (earned / evaluated * 10).toFixed(1) : '—'}<small> / 10</small></strong></div>
    </div>
    <div className="table-wrap grade-table"><table><thead><tr><th>R.A.</th><th>Vale</th><th>Calificación</th><th>Puntos</th></tr></thead><tbody>
      {rows.map(row => <tr key={row.ra.code}><td data-label="R.A."><b>{row.ra.code}</b> {row.ra.title}</td><td data-label="Vale">{row.ra.weight}%</td><td data-label="Calificación">{row.score !== null ? `${row.score.toFixed(0)}/60` : row.sent ? <span className="ra-badge warn">Por calificar</span> : <span className="ra-badge muted">{raStatus(row.ra) === 'proximo' ? 'Próximo' : row.hasActivity ? 'Sin entregar' : 'Sin actividad'}</span>}</td><td data-label="Puntos">{row.points !== null ? `${row.points.toFixed(1)} / ${row.ra.weight}` : '—'}</td></tr>)}
    </tbody></table></div>
  </section>
}

export function TeacherGrades({ courses, students, assessments }) {
  const [courseKey, setCourseKey] = useState(`${courses[0]?.code}`)
  const course = courses.find(item => item.code === courseKey) || courses[0]
  if (!course) return null
  const sameGroup = courses.filter(item => item.group === course.group)
  const groupStudents = students.filter(student => student.group === course.group)
  const plan = planFor(course)
  const table = groupStudents.map(student => {
    const rows = gradeRows(course, assessments, sameGroup, { id: student.id })
    return { student, rows, total: rows.reduce((sum, row) => sum + (row.points || 0), 0) }
  })
  return <section className="panel page-panel">
    <div className="list-toolbar"><div><span className="eyebrow">CONTROL DE CALIFICACIONES</span><h1>Notas</h1><p>Puntos por R.A. según la ponderación del programa. Las actividades se califican sobre 60.</p></div></div>
    <CourseChips courses={courses} value={course.code} onChange={setCourseKey} showGroup />
    {groupStudents.length ? <div className="table-wrap grade-matrix"><table><thead><tr><th>Alumno</th>{plan?.ra.map(ra => <th key={ra.code} title={ra.title}>{ra.code}<small>{ra.weight}%</small></th>)}<th>Total</th></tr></thead><tbody>
      {table.map(({ student, rows, total }) => <tr key={student.id}><td>{student.name}</td>{rows.map(row => <td key={row.ra.code} className={row.points === null ? (row.sent ? 'pending' : 'empty') : ''}>{row.points !== null ? row.points.toFixed(1) : row.sent ? '●' : '—'}</td>)}<td><b>{total.toFixed(1)}</b></td></tr>)}
    </tbody></table><p className="ra-foot">● entregada sin calificar · — sin entrega</p></div> : <p className="ra-empty">No hay alumnos registrados en el grupo {course.group}.</p>}
  </section>
}

export function CourseChips({ courses, value, onChange, showGroup, allLabel }) {
  return <div className="student-course-switcher" aria-label="Elegir materia">
    {allLabel && <button className={value === 'Todos' ? 'active' : ''} onClick={() => onChange('Todos')}>{allLabel}</button>}
    {courses.map(course => <button key={`${course.code}-${course.group}`} className={value === course.code ? 'active' : ''} onClick={() => onChange(course.code)}><b>{course.code}{showGroup ? ` · ${course.group}` : ''}</b><span>{course.name}</span></button>)}
  </div>
}

// Cronograma: fechas de cada R.A. y próximas actividades de evaluación.
export function Schedule({ courses, session, isTeacher }) {
  const [courseCode, setCourseCode] = useState('Todos')
  const today = todayKey()
  const shown = courseCode === 'Todos' ? courses : courses.filter(course => course.code === courseCode)
  const upcoming = shown.flatMap(course => (planFor(course)?.ra || []).filter(ra => ra.ae && ra.ae >= today).map(ra => ({ course, ra }))).sort((a, b) => a.ra.ae.localeCompare(b.ra.ae)).slice(0, 6)
  return <section className="panel page-panel">
    <div className="list-toolbar"><div><span className="eyebrow">{isTeacher ? 'PLANEACIÓN DEL PERIODO' : `GRUPO ${session.group}`}</span><h1>Cronograma</h1><p>Fechas de cada resultado de aprendizaje y de sus actividades de evaluación.</p></div></div>
    <CourseChips courses={courses} value={courseCode} onChange={setCourseCode} allLabel="Todas" showGroup={isTeacher} />
    <div className="schedule-next"><h3>Próximas evaluaciones</h3>{upcoming.length ? <ul>{upcoming.map(({ course, ra }) => { const days = daysUntil(ra.ae); return <li key={`${course.code}-${ra.code}`}><span className="schedule-date"><b>{parseDay(ra.ae).getDate()}</b>{parseDay(ra.ae).toLocaleDateString('es-MX', { month: 'short' }).replace('.', '')}</span><div><strong>{course.code} · R.A. {ra.code}</strong><small>{ra.title}</small></div><span className={`ra-badge ${days <= 3 ? 'bad' : days <= 7 ? 'warn' : 'muted'}`}>{days === 0 ? 'Hoy' : days === 1 ? 'Mañana' : `En ${days} días`}</span></li> })}</ul> : <p className="ra-empty">No hay evaluaciones próximas.</p>}</div>
    {shown.map(course => {
      const plan = planFor(course)
      if (!plan) return null
      const next = nextSession(course)
      const first = plan.ra[0]?.start
      const last = plan.ra.at(-1)?.ae
      const span = parseDay(last) - parseDay(first) || 1
      const todayPos = Math.min(100, Math.max(0, (parseDay(today) - parseDay(first)) / span * 100))
      return <article className="schedule-course" key={`${course.code}-${course.group}`}>
        <header><div className="module-code">{course.code}</div><div><h2>{course.name}</h2><p>Grupo {course.group}{next ? ` · Próxima clase: ${longDate(next)}` : ''}</p></div></header>
        <div className="schedule-bar" aria-hidden="true">{plan.ra.map(ra => <i key={ra.code} className={raStatus(ra)} style={{ flex: Math.max(1, (parseDay(ra.ae || ra.end) - parseDay(ra.start)) / dayMs) }} title={`R.A. ${ra.code}`}>{ra.code}</i>)}<b style={{ left: `${todayPos}%` }} /></div>
        <ol className="schedule-list">{plan.ra.map(ra => <li key={ra.code} className={raStatus(ra)}><span className="ra-code">R.A. {ra.code}</span><div><strong>{ra.title}</strong><small>{shortDate(ra.start)} al {shortDate(ra.end)} · {ra.hours} h · vale {ra.weight}%</small></div><span className="schedule-ae"><FileText size={14} />A.E. {shortDate(ra.ae)}</span></li>)}</ol>
      </article>
    })}
  </section>
}

// Resumen para el inicio del alumno: qué R.A. se trabaja en cada materia, la próxima clase y la próxima evaluación.
export function WeekPlan({ courses, onOpenCourse }) {
  const rows = courses.map(course => ({ course, ra: currentRa(course), next: nextSession(course) })).filter(row => row.ra)
  if (!rows.length) return null
  return <section className="panel week-plan"><div className="panel-title"><h3>Esta semana en tus materias</h3></div><div className="week-plan-list">{rows.map(({ course, ra, next }) => {
    const days = ra.ae ? daysUntil(ra.ae) : null
    return <button key={`${course.code}-${course.group}`} onClick={() => onOpenCourse?.(course.code)}><div className="module-code">{course.code}</div><div><strong>R.A. {ra.code} · {ra.title}</strong><small>{next ? `Próxima clase: ${longDate(next)}` : 'Sin clases programadas'}</small></div>{days !== null && days >= 0 && <span className={`ra-badge ${days <= 3 ? 'bad' : days <= 7 ? 'warn' : 'muted'}`}>A.E. {days === 0 ? 'hoy' : `en ${days} d`}</span>}<ChevronRight size={17} /></button>
  })}</div></section>
}
