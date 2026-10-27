import { useCallback, useEffect, useMemo, useState } from 'react'
import { AlarmClock, CalendarCheck, Check, CheckCircle2, ClipboardList, Download, Eye, FileCheck2, LogIn, PenLine, Search, Send, Sparkles, TrendingUp, Trophy, X } from 'lucide-react'
import { isSupabaseReady, supabase } from '../lib/supabase'
import * as demo from '../data/demo'
import { CourseChips, gradeRows, itemBelongsToCourse, planFor, progressCodeFor, raStatus, shortDate } from './CoursePlan'

// Seguimiento docente: quién está en línea, avance real por alumno y pase de lista automático.
// Los datos vienen de supabase/seguimiento_asistencia.sql; sin Supabase se muestran datos de ejemplo.

const ONLINE_MS = 150000
const todayKey = () => new Date().toLocaleDateString('en-CA')
const initials = name => name.split(' ').slice(0, 2).map(part => part[0]).join('')
const prettyCode = code => String(code || '').replace(/^([A-Z]{4})-RA-(\d\.\d)$/, '$1 R.A. $2').replace('EDOA-WORD-U1', 'EDOA R.A. 1.1')
const sortByName = (a, b) => a.name.localeCompare(b.name, 'es')

function ago(value, now = Date.now()) {
  if (!value) return 'nunca'
  const minutes = Math.round((now - new Date(value)) / 60000)
  if (minutes < 1) return 'ahora'
  if (minutes < 60) return `hace ${minutes} min`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `hace ${hours} h`
  return `hace ${Math.round(hours / 24)} d`
}

function duration(minutes) {
  if (!minutes) return '—'
  if (minutes < 60) return `${minutes} min`
  return `${Math.floor(minutes / 60)} h ${minutes % 60} min`
}

const clock = value => new Date(value).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
const minuteLabel = minute => `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(minute % 60).padStart(2, '0')}`
const minuteOf = time => { const [hours, minutes] = String(time || '').split(':').map(Number); return Number.isFinite(hours) ? hours * 60 + (minutes || 0) : null }
const isMissingTable = error => error && /PGRST20[25]|42P01|42883|does not exist|schema cache/i.test(`${error.code} ${error.message}`)

function SetupNotice() {
  return <div className="tracking-setup"><Sparkles size={18} /><div><strong>Falta activar el seguimiento en Supabase</strong><span>Corre una sola vez <code>supabase/seguimiento_asistencia.sql</code> en el SQL Editor. Desde ese momento se registra lo que hace cada alumno.</span></div></div>
}

function LiveBadge({ label }) {
  return <span className="tracking-live"><i />{label}</span>
}

// Presencia, bitácora y resumen de tiempo; se vuelve a pedir cada cierto tiempo.
function useTracking(intervalMs) {
  const [state, setState] = useState({ loading: true, missing: false, error: '', presence: [], log: [], summary: [] })
  const load = useCallback(async () => {
    if (!isSupabaseReady) { setState({ loading: false, missing: false, error: '', ...demo.demoTracking() }); return }
    const since = new Date(Date.now() - 3 * 86400000).toISOString()
    const [presence, log, summary] = await Promise.all([
      supabase.from('student_presence').select('student_id, last_seen_at, session_started_at, current_view, current_detail'),
      supabase.from('student_activity_log').select('id, student_id, kind, title, detail, created_at').gte('created_at', since).order('created_at', { ascending: false }).limit(300),
      supabase.rpc('aula_tracking_summary'),
    ])
    const failure = [presence, log, summary].find(result => result.error)?.error
    if (isMissingTable(failure)) { setState(current => ({ ...current, loading: false, missing: true })); return }
    setState({ loading: false, missing: false, error: failure?.message || '', presence: presence.data || [], log: log.data || [], summary: summary.data || [] })
  }, [])
  useEffect(() => {
    load()
    const timer = window.setInterval(() => { if (document.visibilityState === 'visible') load() }, intervalMs)
    return () => window.clearInterval(timer)
  }, [load, intervalMs])
  return state
}

const feedIcons = { entrada: LogIn, vista: Eye, avance: TrendingUp, completo: Trophy, inicio: PenLine, entrega: Send }

function feedText(item) {
  if (item.kind === 'entrada') return <>entró a la plataforma</>
  if (item.kind === 'vista') return <>abrió <b>{item.title}</b>{item.detail ? ` · ${item.detail}` : ''}</>
  if (item.kind === 'avance') return <>avanzó en el material de <b>{prettyCode(item.title)}</b>{item.detail ? ` · ${item.detail}` : ''}</>
  if (item.kind === 'completo') return <>terminó el material de <b>{prettyCode(item.title)}</b></>
  if (item.kind === 'inicio') return <>empezó la tarea <b>«{item.title}»</b></>
  if (item.kind === 'entrega') return <>entregó <b>«{item.title}»</b></>
  return item.title
}

export function LiveNow({ students, groups }) {
  const [group, setGroup] = useState('Todos')
  const [showPages, setShowPages] = useState(false)
  const [now, setNow] = useState(Date.now())
  const tracking = useTracking(15000)
  useEffect(() => { const timer = window.setInterval(() => setNow(Date.now()), 15000); return () => window.clearInterval(timer) }, [])
  const byId = useMemo(() => new Map(students.map(student => [student.id, student])), [students])
  const inGroup = id => { const student = byId.get(id); return student && (group === 'Todos' || student.group === group) }
  const online = tracking.presence.filter(item => inGroup(item.student_id) && now - new Date(item.last_seen_at) < ONLINE_MS)
    .map(item => ({ ...item, student: byId.get(item.student_id) })).sort((a, b) => sortByName(a.student, b.student))
  const feed = tracking.log.filter(item => inGroup(item.student_id) && (showPages || item.kind !== 'vista')).slice(0, 80)
  return <section className="panel page-panel tracking-page">
    <div className="list-toolbar"><div><span className="eyebrow">Seguimiento</span><h1>En vivo</h1><p>Quién está conectado ahora y lo que hace cada alumno. Se actualiza cada 15 segundos.</p></div><LiveBadge label="tiempo real" /></div>
    {tracking.missing && <SetupNotice />}
    {tracking.error && <div className="form-error">{tracking.error}</div>}
    <div className="tracking-filters">
      <select value={group} onChange={event => setGroup(event.target.value)} aria-label="Grupo"><option value="Todos">Todos los grupos</option>{groups.map(item => <option key={item.id} value={item.code}>Grupo {item.code}</option>)}</select>
      <label className="tracking-check"><input type="checkbox" checked={showPages} onChange={event => setShowPages(event.target.checked)} />Mostrar también cada página que visitan</label>
    </div>
    <div className="live-grid">
      <div className="live-card"><h2>En línea ahora <span>{online.length}</span></h2>
        {online.length ? <ul className="online-list">{online.map(item => <li key={item.student_id}><div className="avatar small">{initials(item.student.name)}<i /></div><div><strong>{item.student.name}</strong><span>Grupo {item.student.group} · conectado desde {clock(item.session_started_at)}</span><small>{item.current_view || 'Plataforma'}{item.current_detail ? ` · ${item.current_detail}` : ''}</small></div></li>)}</ul>
          : <p className="live-empty">{tracking.loading ? 'Cargando…' : 'Nadie conectado en este momento.'}</p>}
      </div>
      <div className="live-card"><h2>Lo que están haciendo</h2>
        {feed.length ? <ul className="feed-list">{feed.map(item => { const Icon = feedIcons[item.kind] || Eye; return <li key={item.id} className={`feed-${item.kind}`}><span className="feed-icon"><Icon size={16} /></span><p><b>{byId.get(item.student_id).name}</b> {feedText(item)}</p><time dateTime={item.created_at}>{ago(item.created_at, now)}</time></li> })}</ul>
          : <p className="live-empty">{tracking.loading ? 'Cargando…' : 'Todavía no hay actividad registrada en los últimos 3 días.'}</p>}
      </div>
    </div>
  </section>
}

// Avance real de cada material: pasos hechos entre el total de pasos de ese material.
function materialTotals(rows) {
  const totals = {}
  rows.forEach(row => {
    const steps = row.completed_steps?.length || 0
    const known = Number(row.total_steps) || 0
    const entry = totals[row.material_code] || { declared: 0, finished: 0, seen: 0 }
    totals[row.material_code] = { declared: Math.max(entry.declared, known), finished: row.completed_at ? Math.max(entry.finished, steps) : entry.finished, seen: Math.max(entry.seen, steps) }
  })
  return Object.fromEntries(Object.entries(totals).map(([code, entry]) => [code, entry.declared || entry.finished || entry.seen || 1]))
}

function courseMaterialCodes(course, materials, learningProgress) {
  const codes = new Set(learningProgress.map(row => row.material_code).filter(code => code.startsWith(`${course.code}-RA-`)))
  materials.forEach(material => { const code = progressCodeFor(material); if (code?.startsWith(`${course.code}-`) && material.group === course.group) codes.add(code) })
  const byRa = {}
  codes.forEach(code => { const ra = code.match(/-RA-(\d\.\d)$/)?.[1]; if (ra) (byRa[ra] ||= []).push(code) })
  return byRa
}

export function buildProgressRows({ course, courses, students, materials, assessments, learningProgress, summary = [], attendance = [] }) {
  const plan = planFor(course)
  const sameGroup = courses.filter(item => item.group === course.group)
  const groupStudents = students.filter(student => student.group === course.group)
  const codesByRa = courseMaterialCodes(course, materials, learningProgress)
  const totals = materialTotals(learningProgress)
  const courseAssessments = assessments.filter(item => itemBelongsToCourse(item, course, sameGroup) && (item.status === 'Activa' || item.submissionDetails?.length))
  const today = todayKey()
  return groupStudents.map(student => {
    const own = learningProgress.filter(row => row.student_id === student.id)
    const pctOf = code => { const row = own.find(item => item.material_code === code); return row ? (row.completed_at ? 100 : Math.min(100, Math.round((row.completed_steps?.length || 0) / totals[code] * 100))) : 0 }
    const raPct = Object.fromEntries((plan?.ra || []).map(ra => [ra.code, codesByRa[ra.code] ? Math.round(codesByRa[ra.code].reduce((sum, code) => sum + pctOf(code), 0) / codesByRa[ra.code].length) : null]))
    const counted = (plan?.ra || []).filter(ra => raPct[ra.code] !== null && raStatus(ra) !== 'proximo')
    const progress = counted.length ? Math.round(counted.reduce((sum, ra) => sum + raPct[ra.code], 0) / counted.length) : 0
    const grades = gradeRows(course, assessments, sameGroup, { id: student.id })
    const points = grades.reduce((sum, row) => sum + (row.points || 0), 0)
    const submissions = courseAssessments.map(item => item.submissionDetails?.find(submission => submission.student_id === student.id))
    const delivered = submissions.filter(item => item?.submitted_at).length
    const overdue = courseAssessments.filter((item, index) => item.dueAt && item.dueAt.slice(0, 10) < today && !submissions[index]?.submitted_at).length
    const time = summary.find(item => item.student_id === student.id)
    const lastAccess = [time?.last_seen_at, ...own.map(row => row.updated_at), ...submissions.map(item => item?.submitted_at || item?.started_at)].filter(Boolean).sort().at(-1) || null
    const absences = attendance.filter(item => item.student_id === student.id && item.status === 'falto').length
    const alerts = []
    const idleDays = lastAccess ? Math.floor((Date.now() - new Date(lastAccess)) / 86400000) : null
    if (idleDays === null) alerts.push({ level: 'high', text: 'Nunca ha entrado' })
    else if (idleDays >= 7) alerts.push({ level: 'high', text: `Sin entrar hace ${idleDays} días` })
    const behind = (plan?.ra || []).filter(ra => raStatus(ra) === 'concluido' && raPct[ra.code] !== null && raPct[ra.code] < 60)
    if (behind.length) alerts.push({ level: 'high', text: `Atrasado en R.A. ${behind.map(ra => ra.code).join(', ')}` })
    const current = (plan?.ra || []).find(ra => raStatus(ra) === 'actual' && raPct[ra.code] !== null)
    if (current && raPct[current.code] === 0 && idleDays !== null) alerts.push({ level: 'medium', text: `No ha empezado el R.A. ${current.code}` })
    if (overdue) alerts.push({ level: 'high', text: `${overdue} tarea${overdue === 1 ? '' : 's'} vencida${overdue === 1 ? '' : 's'} sin entregar` })
    if (absences >= 3) alerts.push({ level: 'medium', text: `${absences} faltas` })
    return { student, progress, raPct, points, delivered, assigned: courseAssessments.length, lastAccess, minutes: time?.total_minutes || 0, today: Boolean(time?.today_minutes) || Boolean(lastAccess && new Date(lastAccess).toLocaleDateString('en-CA') === today), alerts, attention: alerts.some(alert => alert.level === 'high') }
  })
}

const sorters = {
  atencion: (a, b) => Number(b.attention) - Number(a.attention) || b.alerts.length - a.alerts.length || a.progress - b.progress,
  menor: (a, b) => a.progress - b.progress,
  mayor: (a, b) => b.progress - a.progress,
  nombre: (a, b) => sortByName(a.student, b.student),
}

export function ProgressTracker({ courses, students, materials, assessments, learningProgress, onOpenStudent }) {
  const [courseCode, setCourseCode] = useState(courses[0]?.code)
  const [query, setQuery] = useState('')
  const [order, setOrder] = useState('atencion')
  const [progressRows, setProgressRows] = useState(learningProgress)
  const [attendance, setAttendance] = useState([])
  const tracking = useTracking(60000)
  const course = courses.find(item => item.code === courseCode) || courses[0]
  useEffect(() => { setProgressRows(learningProgress) }, [learningProgress])
  // El avance de los materiales también se vuelve a pedir cada minuto.
  useEffect(() => {
    if (!isSupabaseReady) return undefined
    const refresh = async () => {
      if (document.visibilityState === 'hidden') return
      const { data, error } = await supabase.from('learning_progress').select('student_id, material_code, completed_steps, total_steps, completed_at, updated_at')
      if (!error && data) setProgressRows(data)
    }
    refresh()
    const timer = window.setInterval(refresh, 60000)
    return () => window.clearInterval(timer)
  }, [])
  useEffect(() => {
    if (!isSupabaseReady || !course) return
    supabase.from('attendance_records').select('student_id, status').eq('course_code', course.code).then(({ data }) => setAttendance(data || []))
  }, [course?.code])
  if (!course) return null
  const plan = planFor(course)
  const rows = buildProgressRows({ course, courses, students, materials, assessments, learningProgress: progressRows, summary: tracking.summary, attendance })
  const shown = rows.filter(row => `${row.student.name} ${row.student.email} ${row.student.enrollment || ''}`.toLowerCase().includes(query.toLowerCase())).sort(sorters[order])
  const average = rows.length ? Math.round(rows.reduce((sum, row) => sum + row.progress, 0) / rows.length) : 0
  return <section className="panel page-panel tracking-page">
    <div className="list-toolbar"><div><span className="eyebrow">Seguimiento</span><h1>Avance de alumnos</h1><p>Avance real en el material de cada R.A., notas, tareas y tiempo en la plataforma.</p></div><LiveBadge label="se actualiza solo" /></div>
    {tracking.missing && <SetupNotice />}
    <CourseChips courses={courses} value={course.code} onChange={setCourseCode} showGroup />
    <div className="tracking-stats">
      <div><strong>{rows.length}</strong><span>Alumnos</span></div>
      <div><strong>{average} %</strong><span>Avance promedio</span></div>
      <div className={rows.some(row => row.attention) ? 'alert' : ''}><strong>{rows.filter(row => row.attention).length}</strong><span>Necesitan atención</span></div>
      <div><strong>{rows.filter(row => row.today).length}</strong><span>Activos hoy</span></div>
    </div>
    <div className="tracking-filters">
      <div className="search"><Search size={18} /><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Buscar nombre, correo o matrícula" /></div>
      <select value={order} onChange={event => setOrder(event.target.value)} aria-label="Ordenar"><option value="atencion">Ordenar: necesitan atención primero</option><option value="menor">Ordenar: menor avance</option><option value="mayor">Ordenar: mayor avance</option><option value="nombre">Ordenar: por nombre</option></select>
    </div>
    <p className="tracking-hint">Toca el nombre de un alumno para ver su <b>expediente completo</b>. Las columnas {plan?.ra[0]?.code} a {plan?.ra.at(-1)?.code} son el % de avance en el material de cada R.A.</p>
    {shown.length ? <div className="table-wrap progress-table"><table><thead><tr><th>Alumno</th><th>Avance</th><th>Nota</th><th>Tareas</th><th>Último acceso</th><th>Tiempo</th>{plan?.ra.map(ra => <th key={ra.code} className="ra-col" title={ra.title}>{ra.code}</th>)}<th>Alertas</th></tr></thead><tbody>
      {shown.map(row => <tr key={row.student.id} className={row.attention ? 'needs-attention' : ''}>
        <td data-label="Alumno"><button className="student-link" onClick={() => onOpenStudent?.(row.student)}>{row.student.name}</button><small>{row.student.enrollment || row.student.email}</small></td>
        <td data-label="Avance"><div className="progress-cell"><b>{row.progress} %</b><span><i style={{ width: `${row.progress}%` }} /></span></div></td>
        <td data-label="Nota" className="nowrap">{row.points.toFixed(1)} / 100</td>
        <td data-label="Tareas">{row.delivered}/{row.assigned}</td>
        <td data-label="Último acceso">{ago(row.lastAccess)}</td>
        <td data-label="Tiempo">{duration(row.minutes)}</td>
        {plan?.ra.map(ra => <td key={ra.code} data-label={`R.A. ${ra.code}`} className="ra-col">{row.raPct[ra.code] === null ? <span className="ra-none">·</span> : <span className={`ra-pct ${row.raPct[ra.code] >= 100 ? 'full' : row.raPct[ra.code] >= 60 ? 'good' : row.raPct[ra.code] > 0 ? 'low' : raStatus(ra) === 'proximo' ? 'future' : 'zero'}`}>{row.raPct[ra.code]}</span>}</td>)}
        <td data-label="Por R.A." className="ra-strip">{plan?.ra.filter(ra => row.raPct[ra.code] !== null).map(ra => <span key={ra.code}><small>{ra.code}</small>{row.raPct[ra.code]}%</span>)}</td>
        <td data-label="Alertas">{row.alerts.length ? <div className="alert-list">{row.alerts.map(alert => <span key={alert.text} className={`alert-chip ${alert.level}`}>{alert.text}</span>)}</div> : <span className="alert-chip ok"><Check size={13} />Al corriente</span>}</td>
      </tr>)}
    </tbody></table></div> : <p className="ra-empty">No hay alumnos que coincidan.</p>}
  </section>
}

// ── Asistencia ───────────────────────────────────────────────
const statusInfo = {
  asistio: { label: 'Asistió', icon: Check },
  retardo: { label: 'Retardo', icon: AlarmClock },
  falto: { label: 'Faltó', icon: X },
  justifico: { label: 'Justificó', icon: FileCheck2 },
}
const weekdayNames = ['domingos', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábados']
const longDay = day => new Date(`${day}T12:00:00`).toLocaleDateString('es-MX', { weekday: 'short', day: 'numeric', month: 'short' }).replace(/\./g, '')

// Estado automático según las conexiones de ese día dentro del horario de clase.
export function autoStatus(minutes = [], schedule, day) {
  const list = [...minutes].sort((a, b) => a - b)
  const now = new Date()
  const nowMinute = now.getHours() * 60 + now.getMinutes()
  const isToday = day === todayKey()
  if (!schedule) {
    if (list.length) return { status: 'asistio', first: list[0] }
    return { status: isToday ? null : 'falto' }
  }
  const start = minuteOf(schedule.starts_at)
  const end = minuteOf(schedule.ends_at)
  const inClass = list.filter(minute => minute >= start - 10 && minute <= end)
  if (!inClass.length) return { status: isToday && nowMinute <= end ? null : 'falto', outside: list[0] }
  return { status: inClass[0] > start + (schedule.tolerance_minutes ?? 10) ? 'retardo' : 'asistio', first: inClass[0] }
}

function csvDownload(name, rows) {
  const text = rows.map(row => row.map(cell => `"${String(cell ?? '').replace(/"/g, '""')}"`).join(',')).join('\r\n')
  const link = document.createElement('a')
  link.href = URL.createObjectURL(new Blob([`﻿${text}`], { type: 'text/csv;charset=utf-8' }))
  link.download = name
  link.click()
  URL.revokeObjectURL(link.href)
}

export function Attendance({ courses, students }) {
  const [tab, setTab] = useState('lista')
  const [courseCode, setCourseCode] = useState(courses[0]?.code)
  const course = courses.find(item => item.code === courseCode) || courses[0]
  const plan = planFor(course)
  const today = todayKey()
  const sessions = useMemo(() => (plan?.sessions || []).filter(day => day <= today).reverse(), [plan, today])
  const [day, setDay] = useState(sessions[0] || today)
  const [records, setRecords] = useState([])
  const [daily, setDaily] = useState([])
  const [schedules, setSchedules] = useState([])
  const [missing, setMissing] = useState(false)
  const [message, setMessage] = useState('')
  const [draftSchedule, setDraftSchedule] = useState(null)
  const roster = useMemo(() => students.filter(student => student.group === course?.group).sort((a, b) => a.name.localeCompare(b.name, 'es')), [students, course?.group])

  useEffect(() => { setDay(sessions[0] || today) }, [course?.code])

  const load = useCallback(async () => {
    if (!course) return
    if (!isSupabaseReady) { setDaily(current => current.length ? current : demo.demoDailyActivity(plan?.sessions?.filter(item => item <= today) || [])); return }
    const first = plan?.sessions?.[0] || today
    const ids = roster.map(student => student.id)
    const [recordResult, dailyResult, scheduleResult] = await Promise.all([
      supabase.from('attendance_records').select('student_id, class_date, status').eq('course_code', course.code),
      ids.length ? supabase.from('student_daily_activity').select('student_id, day, minutes').gte('day', first).in('student_id', ids) : Promise.resolve({ data: [] }),
      supabase.from('attendance_schedules').select('course_code, weekday, starts_at, ends_at, tolerance_minutes').eq('course_code', course.code),
    ])
    const failure = [recordResult, dailyResult, scheduleResult].find(result => result.error)?.error
    if (isMissingTable(failure)) { setMissing(true); return }
    if (failure) { setMessage(failure.message); return }
    setMissing(false)
    setRecords(recordResult.data || []); setDaily(dailyResult.data || []); setSchedules(scheduleResult.data || [])
  }, [course?.code, roster])
  useEffect(() => { load() }, [load])
  // Mientras se pasa lista del día de hoy, las conexiones se refrescan solas.
  useEffect(() => {
    if (day !== today || !isSupabaseReady) return undefined
    const timer = window.setInterval(() => { if (document.visibilityState === 'visible') load() }, 30000)
    return () => window.clearInterval(timer)
  }, [day, today, load])

  if (!course) return null
  const weekday = new Date(`${day}T12:00:00`).getDay()
  const scheduleFor = date => schedules.find(item => item.weekday === new Date(`${date}T12:00:00`).getDay()) || null
  const schedule = scheduleFor(day)
  const entryFor = (student, date) => {
    const record = records.find(item => item.student_id === student.id && item.class_date === date)
    const auto = autoStatus(daily.find(item => item.student_id === student.id && item.day === date)?.minutes, scheduleFor(date), date)
    return { record, auto, status: record?.status || auto.status }
  }
  const list = roster.map(student => ({ student, ...entryFor(student, day) }))
  const counts = Object.fromEntries(Object.keys(statusInfo).map(key => [key, list.filter(item => item.status === key).length]))
  const pending = list.filter(item => !item.status).length

  async function save(changes, removals = []) {
    const now = new Date().toISOString()
    setRecords(current => [...current.filter(item => !(item.class_date === day && [...changes.map(change => change.student_id), ...removals].includes(item.student_id))), ...changes.map(change => ({ ...change, class_date: day }))])
    if (!isSupabaseReady) { setMessage('Modo demostración: la lista no se guarda.'); return }
    const { data: auth } = await supabase.auth.getUser()
    const requests = []
    if (changes.length) requests.push(supabase.from('attendance_records').upsert(changes.map(change => ({ ...change, course_code: course.code, class_date: day, updated_by: auth.user?.id, updated_at: now })), { onConflict: 'student_id,course_code,class_date' }))
    if (removals.length) requests.push(supabase.from('attendance_records').delete().eq('course_code', course.code).eq('class_date', day).in('student_id', removals))
    const failure = (await Promise.all(requests)).find(result => result.error)?.error
    setMessage(failure ? failure.message : 'Guardado.')
    if (failure) load()
  }
  const mark = (item, status) => item.record?.status === status ? save([], [item.student.id]) : save([{ student_id: item.student.id, status }])
  const confirmAuto = () => save(list.filter(item => !item.record && item.auto.status).map(item => ({ student_id: item.student.id, status: item.auto.status })))
  const allPresent = () => save(list.map(item => ({ student_id: item.student.id, status: 'asistio' })))
  const clearDay = () => { if (window.confirm(`¿Quitar los cambios manuales del ${longDay(day)}? La lista vuelve a calcularse con las conexiones.`)) save([], list.filter(item => item.record).map(item => item.student.id)) }

  async function saveSchedule() {
    const value = { course_code: course.code, weekday, starts_at: draftSchedule.starts_at, ends_at: draftSchedule.ends_at, tolerance_minutes: Number(draftSchedule.tolerance_minutes) || 0 }
    if (minuteOf(value.ends_at) <= minuteOf(value.starts_at)) { setMessage('La hora de salida debe ser después de la de entrada.'); return }
    setSchedules(current => [...current.filter(item => item.weekday !== weekday), value]); setDraftSchedule(null)
    if (!isSupabaseReady) { setMessage('Modo demostración: el horario no se guarda.'); return }
    const { error } = await supabase.from('attendance_schedules').upsert(value, { onConflict: 'course_code,weekday' })
    setMessage(error ? error.message : `Horario guardado para todos los ${weekdayNames[weekday]}.`)
  }

  const summary = roster.map(student => {
    const entries = sessions.map(date => entryFor(student, date).status)
    const total = Object.fromEntries(Object.keys(statusInfo).map(key => [key, entries.filter(status => status === key).length]))
    const counted = entries.filter(Boolean).length
    return { student, ...total, counted, rate: counted ? Math.round((total.asistio + total.retardo + total.justifico) / counted * 100) : null }
  })
  const exportList = () => csvDownload(`asistencia-${course.code}-${course.group}-${day}.csv`, [['No.', 'Alumno', 'Matrícula', 'Asistencia', 'Origen'], ...list.map((item, index) => [index + 1, item.student.name, item.student.enrollment || '', statusInfo[item.status]?.label || 'Sin pasar', item.record ? 'Manual' : 'Automático'])])
  const exportSummary = () => csvDownload(`asistencia-resumen-${course.code}-${course.group}.csv`, [['Alumno', 'Matrícula', 'Asistencias', 'Retardos', 'Faltas', 'Justificadas', 'Clases', '% asistencia'], ...summary.map(row => [row.student.name, row.student.enrollment || '', row.asistio, row.retardo, row.falto, row.justifico, row.counted, row.rate ?? ''])])

  return <section className="panel page-panel tracking-page">
    <div className="list-toolbar"><div><span className="eyebrow">Seguimiento</span><h1>{tab === 'lista' ? 'Pase de lista' : 'Resumen de asistencia'}</h1><p>La lista se llena sola con los alumnos que se conectaron durante la clase. Ajuste lo que haga falta.</p></div><span className="tracking-hint-side">Lista del grupo {course.group}, en orden alfabético</span></div>
    {missing && <SetupNotice />}
    <div className="attendance-tabs" role="tablist"><button role="tab" aria-selected={tab === 'lista'} className={tab === 'lista' ? 'active' : ''} onClick={() => setTab('lista')}><CalendarCheck size={17} />Pasar lista</button><button role="tab" aria-selected={tab === 'resumen'} className={tab === 'resumen' ? 'active' : ''} onClick={() => setTab('resumen')}><ClipboardList size={17} />Resumen</button></div>
    <CourseChips courses={courses} value={course.code} onChange={code => { setCourseCode(code); setMessage('') }} showGroup />
    {tab === 'lista' ? <>
      <div className="tracking-filters attendance-actions">
        <select value={day} onChange={event => { setDay(event.target.value); setDraftSchedule(null); setMessage('') }} aria-label="Fecha de clase">{(sessions.length ? sessions : [today]).map(date => <option key={date} value={date}>{longDay(date)}{date === today ? ' · hoy' : ''}</option>)}</select>
        <button className="primary" onClick={confirmAuto} disabled={!list.some(item => !item.record && item.auto.status)}><CheckCircle2 size={17} />Guardar lista automática</button>
        <button className="secondary" onClick={allPresent}><Check size={17} />Todos presentes</button>
        <button className="secondary" onClick={clearDay} disabled={!list.some(item => item.record)}>Limpiar el día</button>
        <button className="secondary" onClick={exportList}><Download size={17} />Descargar</button>
      </div>
      <div className="schedule-row">
        {draftSchedule ? <>
          <span>Clase de los {weekdayNames[weekday]}:</span>
          <label>de <input type="time" value={draftSchedule.starts_at} onChange={event => setDraftSchedule({ ...draftSchedule, starts_at: event.target.value })} /></label>
          <label>a <input type="time" value={draftSchedule.ends_at} onChange={event => setDraftSchedule({ ...draftSchedule, ends_at: event.target.value })} /></label>
          <label>tolerancia <input type="number" min="0" max="120" value={draftSchedule.tolerance_minutes} onChange={event => setDraftSchedule({ ...draftSchedule, tolerance_minutes: event.target.value })} /> min</label>
          <button className="primary small" onClick={saveSchedule}>Guardar</button><button className="text-btn" onClick={() => setDraftSchedule(null)}>Cancelar</button>
        </> : <>
          <AlarmClock size={16} />
          {schedule ? <span>Clase de los {weekdayNames[weekday]} de <b>{schedule.starts_at.slice(0, 5)}</b> a <b>{schedule.ends_at.slice(0, 5)}</b>. Después de {schedule.tolerance_minutes} min cuenta como retardo.</span> : <span>Sin horario para los {weekdayNames[weekday]}: cuenta cualquier conexión de ese día. Ponga el horario para marcar retardos.</span>}
          <button className="text-btn" onClick={() => setDraftSchedule({ starts_at: schedule?.starts_at?.slice(0, 5) || '07:00', ends_at: schedule?.ends_at?.slice(0, 5) || '08:40', tolerance_minutes: schedule?.tolerance_minutes ?? 10 })}>{schedule ? 'Cambiar' : 'Poner horario'}</button>
        </>}
      </div>
      <div className="attendance-counts">
        <span className="asistio"><Check size={14} />Asistieron: <b>{counts.asistio}</b></span>
        <span className="retardo"><AlarmClock size={14} />Retardos: <b>{counts.retardo}</b></span>
        <span className="falto"><X size={14} />Faltas: <b>{counts.falto}</b></span>
        <span className="justifico"><FileCheck2 size={14} />Justificadas: <b>{counts.justifico}</b></span>
        <span>Sin pasar: <b>{pending}</b></span>
      </div>
      <p className="tracking-hint">Toque el estado de cada alumno. Se guarda al instante; si toca el mismo botón otra vez, vuelve al estado automático.</p>
      {message && <p className="tracking-message">{message}</p>}
      {list.length ? <div className="table-wrap attendance-table"><table><thead><tr><th>No.</th><th>Apellidos y nombre</th><th>Conexión</th><th>Asistencia</th></tr></thead><tbody>
        {list.map((item, index) => <tr key={item.student.id}>
          <td className="attendance-num">{index + 1}</td>
          <td><strong>{item.student.name}</strong><small>{item.student.enrollment || item.student.email}</small></td>
          <td className="attendance-source">{item.auto.first !== undefined ? <span className="conn on">Entró {minuteLabel(item.auto.first)}</span> : item.auto.outside !== undefined ? <span className="conn off">Fuera de clase ({minuteLabel(item.auto.outside)})</span> : <span className="conn off">Sin conexión</span>}{item.record ? <small>Manual</small> : item.auto.status ? <small>Automático</small> : null}</td>
          <td><div className="attendance-buttons">{Object.entries(statusInfo).map(([key, info]) => { const Icon = info.icon; return <button key={key} className={`${key} ${item.status === key ? 'active' : ''} ${item.status === key && !item.record ? 'auto' : ''}`} aria-pressed={item.status === key} onClick={() => mark(item, key)}><Icon size={17} /><span>{info.label}</span></button> })}</div></td>
        </tr>)}
      </tbody></table></div> : <p className="ra-empty">No hay alumnos registrados en el grupo {course.group}.</p>}
    </> : <>
      <div className="tracking-filters attendance-actions"><span className="tracking-hint">{sessions.length} clase{sessions.length === 1 ? '' : 's'} desde el {shortDate(plan?.sessions?.[0])}. Las clases sin pase de lista guardado usan el estado automático.</span><button className="secondary" onClick={exportSummary}><Download size={17} />Descargar resumen</button></div>
      <div className="table-wrap attendance-summary"><table><thead><tr><th>Alumno</th><th>Asistencias</th><th>Retardos</th><th>Faltas</th><th>Justificadas</th><th>% asistencia</th></tr></thead><tbody>
        {summary.map(row => <tr key={row.student.id} className={row.rate !== null && row.rate < 80 ? 'needs-attention' : ''}>
          <td data-label="Alumno"><strong>{row.student.name}</strong><small>{row.student.enrollment || row.student.email}</small></td>
          <td data-label="Asistencias">{row.asistio}</td><td data-label="Retardos">{row.retardo}</td><td data-label="Faltas">{row.falto}</td><td data-label="Justificadas">{row.justifico}</td>
          <td data-label="% asistencia">{row.rate === null ? '—' : <div className="progress-cell"><b>{row.rate} %</b><span><i style={{ width: `${row.rate}%` }} /></span></div>}</td>
        </tr>)}
      </tbody></table><p className="ra-foot">En rojo: menos de 80 % de asistencia.</p></div>
    </>}
  </section>
}

