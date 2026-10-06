import { useEffect, useMemo, useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import {
  ArrowLeft, BookOpen, CheckCircle2, ChevronRight, ClipboardCheck, Download, Eye, FileText, GraduationCap,
  LayoutDashboard, Lock, LogOut, Menu, Plus, Search, Settings, TrendingUp, Unlock, Upload, Users, X
} from 'lucide-react'
import { courses } from './data/academic'
import AsinActivity from './components/AsinActivity'
import MtcsActivity, { MtcsMaterialView } from './components/MtcsActivity'
import { analyzeMsiiDocument, buildMsiiDocument, downloadBlob, readAssignmentId } from './lib/msii-docx'
import { isSupabaseReady, supabase } from './lib/supabase'

const navItems = [
  { id: 'inicio', label: 'Resumen', icon: LayoutDashboard },
  { id: 'modulos', label: 'Mis módulos', icon: GraduationCap },
  { id: 'materiales', label: 'Materiales', icon: BookOpen },
  { id: 'evaluaciones', label: 'Evaluaciones', icon: ClipboardCheck },
  { id: 'alumnos', label: 'Alumnos', icon: Users },
]

const lowercaseNameWords = new Set(['de', 'del', 'la', 'las', 'los', 'y'])
function formatPersonName(name = '') {
  return name.trim().toLocaleLowerCase('es-MX').split(/\s+/).map((word, index) => {
    if (index > 0 && lowercaseNameWords.has(word.replace(/[,.;:]$/u, ''))) return word
    return word.replace(/(^|[-'’])(\p{L})/gu, (_, separator, letter) => `${separator}${letter.toLocaleUpperCase('es-MX')}`)
  }).join(' ')
}

function App() {
  const [session, setSession] = useState(() => JSON.parse(localStorage.getItem('aula-session') || 'null'))
  useEffect(() => {
    if (!session || !isSupabaseReady) return
    let active = true
    supabase.auth.getUser().then(async ({ data }) => {
      if (!data.user) return
      const { data: profile } = await supabase.from('profiles').select('full_name, role, groups(code, semester)').eq('id', data.user.id).single()
      if (!active || !profile) return
      const current = JSON.parse(localStorage.getItem('aula-session') || 'null')
      const synced = { ...current, name: profile.full_name || current?.name, role: profile.role, group: profile.groups?.code || 'Sin asignar', semester: profile.groups?.semester || null }
      localStorage.setItem('aula-session', JSON.stringify(synced))
      setSession(previous => JSON.stringify(previous) === JSON.stringify(synced) ? previous : synced)
    })
    return () => { active = false }
  }, [session?.id, session?.group])
  return <Routes>
    <Route path="/acceso" element={session ? <Navigate to="/panel" /> : <Login onLogin={setSession} />} />
    <Route path="/panel/*" element={session ? <Dashboard session={session} onLogout={() => { localStorage.removeItem('aula-session'); setSession(null) }} /> : <Navigate to="/acceso" />} />
    <Route path="*" element={<Navigate to={session ? '/panel' : '/acceso'} />} />
  </Routes>
}

function Login({ onLogin }) {
  const navigate = useNavigate()
  const [mode, setMode] = useState('student')
  const [authMode, setAuthMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [enrollment, setEnrollment] = useState('')
  const [studentGroup, setStudentGroup] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setError('')
    const institutionalEmail = email.toLowerCase()
    const allowedStudentDomains = ['@tam.conalep.edu.mx', '@conaleptamaulipas.edu.mx']
    if (mode === 'student' && !allowedStudentDomains.some(domain => institutionalEmail.endsWith(domain))) {
      setError('Usa tu correo institucional autorizado')
      return
    }
    setBusy(true)
    try {
      if (isSupabaseReady) {
        const result = authMode === 'register'
          ? await supabase.auth.signUp({ email, password, options: { data: { full_name: fullName, enrollment_number: enrollment, group_code: studentGroup, role: 'student' } } })
          : await supabase.auth.signInWithPassword({ email, password })
        const { data, error: authError } = result
        if (authError) throw authError
        if (authMode === 'register' && !data.session) {
          setError('Cuenta creada. Revisa tu correo institucional para confirmarla y después inicia sesión.')
          setAuthMode('login'); setBusy(false); return
        }
        const { data: profile, error: profileError } = await supabase
          .from('profiles')
          .select('full_name, role, group_id, groups(code, semester)')
          .eq('id', data.user.id)
          .single()
        if (profileError) throw profileError
        const session = {
          id: data.user.id,
          email: data.user.email,
          role: profile.role,
          name: profile.full_name || data.user.user_metadata?.full_name || 'Usuario',
          group: profile.groups?.code || 'Sin asignar',
          semester: profile.groups?.semester || null,
        }
        localStorage.setItem('aula-session', JSON.stringify(session)); onLogin(session)
      } else {
        const session = mode === 'teacher'
          ? { email: email || 'docente@institucional.edu.mx', role: 'teacher', name: 'Profr. Santiago' }
          : { email, role: 'student', name: fullName || 'Alumno', group: '111', semester: 1 }
        localStorage.setItem('aula-session', JSON.stringify(session)); onLogin(session)
      }
      navigate('/panel')
    } catch (err) { setError(err.message || 'No fue posible iniciar sesión') }
    finally { setBusy(false) }
  }

  return <main className="login-page">
    <section className="brand-panel">
      <div className="brand-mark"><GraduationCap size={29} /><span>Aula Virtual</span></div>
      <div className="brand-copy">
        <span className="eyebrow light">TU ESPACIO DE APRENDIZAJE</span>
        <h1>Aprende, practica<br />y avanza.</h1>
        <p>Materiales, evaluaciones y seguimiento académico en un solo lugar.</p>
      </div>
      <div className="brand-foot">Ciclo escolar 2026–2027</div>
    </section>
    <section className="login-panel">
      <form className="login-card" onSubmit={submit}>
        <div className="mobile-brand"><GraduationCap size={25} /> Aula Virtual</div>
        <span className="eyebrow">{authMode === 'register' ? 'NUEVO ALUMNO' : 'BIENVENIDO'}</span>
        <h2>{authMode === 'register' ? 'Crea tu cuenta' : 'Ingresa a tu aula'}</h2>
        <p className="muted">{authMode === 'register' ? 'Tu grupo se asignará con la matrícula institucional.' : 'Selecciona tu perfil y escribe tus datos.'}</p>
        <div className="role-switch" aria-label="Tipo de usuario">
          <button type="button" className={mode === 'student' ? 'active' : ''} onClick={() => setMode('student')}>Alumno</button>
          <button type="button" className={mode === 'teacher' ? 'active' : ''} onClick={() => { setMode('teacher'); setAuthMode('login') }}>Docente</button>
        </div>
        {authMode === 'register' && <><label>Nombre completo<input value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Como aparece en tu expediente" required /></label><label>Matrícula<input value={enrollment} onChange={e => setEnrollment(e.target.value)} placeholder="Tu matrícula institucional" required /></label><label>Grupo<select value={studentGroup} onChange={e => setStudentGroup(e.target.value)} required><option value="">Selecciona tu grupo</option><option value="111">111</option><option value="310">310</option><option value="311">311</option><option value="511">511</option></select></label></>}
        <label>Correo institucional
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="correo institucional" required />
        </label>
        <label>Contraseña
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Tu contraseña" required={isSupabaseReady} />
        </label>
        {error && <div className="form-error">{error}</div>}
        <button className="primary full" disabled={busy}>{busy ? 'Procesando…' : authMode === 'register' ? 'Crear cuenta' : 'Ingresar al aula'} <ChevronRight size={18} /></button>
        {mode === 'student' && <button type="button" className="auth-link" onClick={() => { setAuthMode(authMode === 'login' ? 'register' : 'login'); setError('') }}>{authMode === 'login' ? '¿Eres alumno nuevo? Crea tu cuenta' : 'Ya tengo cuenta. Iniciar sesión'}</button>}
        {!isSupabaseReady && <p className="demo-note"><CheckCircle2 size={15} /> Modo demostración activo. Puedes ingresar con cualquier contraseña.</p>}
      </form>
    </section>
  </main>
}

function Dashboard({ session, onLogout }) {
  const isTeacher = ['teacher', 'admin'].includes(session.role)
  const profileLabel = session.role === 'admin' ? 'Administrador' : isTeacher ? 'Docente' : `Grupo ${session.group}`
  const assignedCourses = isTeacher ? courses : courses.filter(course => course.group === session.group)
  const [view, setView] = useState('inicio')
  const [mobileMenu, setMobileMenu] = useState(false)
  const [modal, setModal] = useState(null)
  const [toast, setToast] = useState('')
  const [groupList, setGroupList] = useState([])
  const [studentList, setStudentList] = useState([])
  const [materialList, setMaterialList] = useState([])
  const [assessmentList, setAssessmentList] = useState([])
  const [learningProgress, setLearningProgress] = useState([])
  const [selectedAssessment, setSelectedAssessment] = useState(null)
  const [studentPreview, setStudentPreview] = useState(false)
  const [previewGroup, setPreviewGroup] = useState('511')
  const [loading, setLoading] = useState(true)
  const [dataError, setDataError] = useState('')

  async function loadData() {
    setLoading(true); setDataError('')
    try {
      const materialsQuery = supabase.from('materials').select('id, title, description, unit, resource_type, resource_url, published, created_at, groups(code)').order('created_at', { ascending: false })
      const [groupResult, studentResult, materialResult, assessmentResult, progressResult] = await Promise.all([
        supabase.from('groups').select('id, code, semester, career').eq('active', true).order('code'),
        isTeacher ? supabase.from('profiles').select('id, full_name, email, enrollment_number, group_id, groups(code)').eq('role', 'student').order('full_name') : Promise.resolve({ data: [] }),
        isTeacher ? materialsQuery : materialsQuery.eq('published', true),
        supabase.from('assessments').select('id, title, instructions, activity_code, status, due_at, group_id, groups(code), submissions(id, student_id, score, started_at, submitted_at, answers, file_path, original_filename, assessment_assignments(variant), profiles!submissions_student_id_fkey(full_name, email, enrollment_number))').order('created_at', { ascending: false }),
        isTeacher ? Promise.resolve({ data: [] }) : supabase.from('learning_progress').select('material_code, completed_steps, completed_at'),
      ])
      const firstError = [groupResult, studentResult, materialResult, assessmentResult, progressResult].find(result => result.error)?.error
      if (firstError) throw firstError
      const directory = (studentResult.data || []).map(student => ({ ...student, group_code: student.groups?.code || 'Sin asignar', active: true }))
      setGroupList((groupResult.data || []).map(group => ({ ...group, students: directory.filter(student => student.group_code === group.code).length })))
      setStudentList(directory.map(student => ({ id: student.id, name: formatPersonName(student.full_name), email: student.email, enrollment: student.enrollment_number, group: student.group_code })))
      setMaterialList((materialResult.data || []).map(material => ({ id: material.id, title: material.title, description: material.description, unit: material.unit || 'Sin unidad', type: material.resource_type === 'file' ? 'Archivo' : material.resource_type, url: material.resource_url, published: material.published, group: material.groups?.code || 'Todos', date: new Date(material.created_at).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) })))
      setAssessmentList((assessmentResult.data || []).map(assessment => {
        const submissions = assessment.submissions || []
        const scored = submissions.filter(item => item.score !== null)
        return { id: assessment.id, title: assessment.title, instructions: assessment.instructions, activityCode: assessment.activity_code, group: assessment.groups?.code || '—', groupId: assessment.group_id, due: assessment.due_at ? new Date(assessment.due_at).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) : 'Sin fecha', submissions: submissions.filter(item => item.submitted_at).length, drafts: submissions.filter(item => !item.submitted_at).length, submissionDetails: submissions.map(item => ({ ...item, assignment: item.assessment_assignments?.variant || null, student: item.profiles ? { name: formatPersonName(item.profiles.full_name), email: item.profiles.email, enrollment: item.profiles.enrollment_number } : null })), total: directory.filter(student => student.group_code === assessment.groups?.code).length, average: scored.length ? Math.round(scored.reduce((sum, item) => sum + Number(item.score), 0) / scored.length) : null, status: assessment.status === 'published' ? 'Activa' : assessment.status === 'closed' ? 'Cerrada' : 'Borrador' }
      }))
      setLearningProgress(progressResult.data || [])
    } catch (err) { setDataError(err.message || 'No fue posible cargar la información') }
    finally { setLoading(false) }
  }

  useEffect(() => { if (isSupabaseReady) loadData() }, [])

  function saved(message) { setModal(null); setToast(message); setTimeout(() => setToast(''), 2600) }
  async function toggleMaterial(item) {
    const { error } = await supabase.from('materials').update({ published: !item.published }).eq('id', item.id)
    if (error) { setDataError(error.message); return }
    await loadData(); saved(item.published ? 'Material bloqueado para los alumnos' : 'Material publicado para los alumnos')
  }
  async function toggleAssessment(item) {
    const nextStatus = item.status === 'Activa' ? 'draft' : 'published'
    const { error } = await supabase.from('assessments').update({ status: nextStatus }).eq('id', item.id)
    if (error) { setDataError(error.message); return }
    await loadData(); saved(nextStatus === 'published' ? 'Actividad publicada para los alumnos' : 'Actividad bloqueada para los alumnos')
  }
  const pageTitle = studentPreview ? 'Vista del alumno' : view === 'configuracion' ? 'Configuración' : isTeacher && view === 'modulos' ? 'Módulos' : navItems.find(i => i.id === view)?.label || 'Resumen'
  const previewGroupData = groupList.find(group => group.code === previewGroup)
  const previewSession = { id: `preview-${previewGroup}`, email: 'vista.previa@tam.conalep.edu.mx', role: 'student', name: `Alumno Demo ${previewGroup}`, group: previewGroup, semester: previewGroupData?.semester || null, preview: true }

  return <div className="app-shell">
    <aside className={`sidebar ${mobileMenu ? 'open' : ''}`}>
      <div className="side-brand"><GraduationCap size={26} /><span>Aula <b>Virtual</b></span><button className="icon-btn close-menu" onClick={() => setMobileMenu(false)}><X /></button></div>
      <nav>{navItems.filter(item => isTeacher || item.id !== 'alumnos').map(({ id, label, icon: Icon }) =>
        <button key={id} className={view === id ? 'active' : ''} onClick={() => { setView(id); setMobileMenu(false) }}><Icon size={19} />{isTeacher && id === 'modulos' ? 'Módulos' : label}</button>
      )}</nav>
      <div className="side-bottom">
        {isTeacher && <button className={view === 'configuracion' ? 'active' : ''} onClick={() => { setView('configuracion'); setMobileMenu(false) }}><Settings size={19} />Configuración</button>}
        <div className="profile-mini"><div className="avatar">{session.name.slice(0, 2).toUpperCase()}</div><div><strong>{session.name}</strong><small>{profileLabel}</small></div><button className="logout" onClick={onLogout} title="Cerrar sesión"><LogOut size={18} /></button></div>
      </div>
    </aside>
    <div className="main-area">
      <header className="topbar">
        <button className="icon-btn menu-btn" onClick={() => setMobileMenu(true)}><Menu /></button>
        <div><span className="breadcrumb">Aula digital</span><h2>{pageTitle}</h2></div>
        <div className="top-actions">{isTeacher && studentPreview && <select className="preview-group-select" aria-label="Grupo para vista previa" value={previewGroup} onChange={event => setPreviewGroup(event.target.value)}>{groupList.map(group => <option key={group.id} value={group.code}>Grupo {group.code}</option>)}</select>}{isTeacher && <button className={studentPreview ? 'primary' : 'secondary'} onClick={() => setStudentPreview(current => !current)}>{studentPreview ? <ArrowLeft size={17} /> : <Eye size={17} />}<span>{studentPreview ? 'Volver al panel docente' : 'Vista del alumno'}</span></button>}{isTeacher && !studentPreview && view === 'inicio' && <button className="primary" aria-label="Publicar material" title="Publicar material" onClick={() => setModal('material')}><Plus size={18} /><span>Publicar material</span></button>}</div>
      </header>
      <main className="content">
        {dataError && <div className="form-error data-error">{dataError} <button className="text-btn" onClick={loadData}>Reintentar</button></div>}
        {loading ? <div className="loading-state">Cargando información real…</div> : studentPreview ? <StudentPreview session={previewSession} courses={courses.filter(course => course.group === previewGroup)} materials={materialList.filter(item => item.group === previewGroup && item.published)} assessments={assessmentList.filter(item => item.group === previewGroup && item.status === 'Activa')} /> : <>
        {view === 'inicio' && (isTeacher ? <TeacherHome setView={setView} groups={groupList} students={studentList} materials={materialList} assessments={assessmentList} onOpenAssessment={assessment => { setSelectedAssessment(assessment); setView('evaluaciones') }} /> : <StudentHome session={session} courses={assignedCourses} materials={materialList} assessments={assessmentList} setView={setView} />)}
        {view === 'modulos' && (isTeacher ? <TeacherModules courses={assignedCourses} students={studentList} materials={materialList} assessments={assessmentList} setView={setView} /> : <Modules courses={assignedCourses} session={session} setView={setView} />)}
        {view === 'materiales' && <Materials items={materialList} groups={groupList} courses={assignedCourses} session={session} isTeacher={isTeacher} onAdd={() => setModal('material')} onToggle={toggleMaterial} onProgressUpdate={progress => setLearningProgress(current => [...current.filter(item => item.material_code !== progress.material_code), progress])} />}
        {view === 'evaluaciones' && <Assessments items={assessmentList} session={session} isTeacher={isTeacher} learningProgress={learningProgress} onAdd={() => setModal('assessment')} onRefresh={loadData} onToggle={toggleAssessment} initialSelected={selectedAssessment} onClearSelected={() => setSelectedAssessment(null)} />}
        {view === 'alumnos' && isTeacher && <Students students={studentList} groups={groupList} assessments={assessmentList} onRefresh={loadData} />}
        {view === 'configuracion' && isTeacher && <SettingsPage session={session} groups={groupList} />}
        </>}
      </main>
    </div>
    {!isTeacher && <nav className="student-mobile-nav" aria-label="Navegación del alumno">{navItems.filter(item => ['inicio', 'modulos', 'materiales', 'evaluaciones'].includes(item.id)).map(({ id, label, icon: Icon }) => <button key={id} className={view === id ? 'active' : ''} onClick={() => { setView(id); setMobileMenu(false); window.scrollTo({ top: 0, behavior: 'smooth' }) }}><Icon size={20} /><span>{id === 'inicio' ? 'Inicio' : label}</span></button>)}</nav>}
    {mobileMenu && <div className="overlay mobile" onClick={() => setMobileMenu(false)} />}
    {modal === 'material' && <MaterialModal groups={groupList} onClose={() => setModal(null)} onSave={async (item) => {
      const { data: authData } = await supabase.auth.getUser()
      const extension = item.file.name.split('.').pop()
      const path = `${authData.user.id}/${crypto.randomUUID()}.${extension}`
      const { error: uploadError } = await supabase.storage.from('materials').upload(path, item.file)
      if (uploadError) throw uploadError
      const { error } = await supabase.from('materials').insert({ teacher_id: authData.user.id, group_id: item.groupId || null, title: item.title, description: item.description, unit: item.unit, resource_type: 'file', resource_url: path })
      if (error) throw error
      await loadData(); saved('Material publicado correctamente')
    }} />}
    {modal === 'assessment' && <AssessmentModal groups={groupList} onClose={() => setModal(null)} onSave={async (item) => {
      const { data: authData } = await supabase.auth.getUser()
      const { error } = await supabase.from('assessments').insert({ teacher_id: authData.user.id, group_id: item.groupId, title: item.title, instructions: item.instructions, activity_code: item.activityCode, status: 'published', due_at: item.dueAt })
      if (error) throw error
      await loadData(); saved('Evaluación creada correctamente')
    }} />}
    {toast && <div className="toast"><CheckCircle2 size={19} />{toast}</div>}
  </div>
}

function TeacherHome({ setView, groups, students, materials, assessments, onOpenAssessment }) {
  const [moduleFilter, setModuleFilter] = useState('Todos')
  const activeAssessments = assessments.filter(item => item.status === 'Activa')
  const submitted = assessments.reduce((sum, item) => sum + item.submissions, 0)
  const drafts = assessments.reduce((sum, item) => sum + item.drafts, 0)
  const scores = assessments.filter(item => item.average !== null).map(item => item.average)
  const overallAverage = scores.length ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : null
  const today = new Intl.DateTimeFormat('es-MX', { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date()).toLocaleUpperCase('es-MX')
  const recent = assessments.flatMap(assessment => assessment.submissionDetails.map(submission => ({ ...submission, assessment: assessment.title, group: assessment.group, date: submission.submitted_at || submission.started_at }))).sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 5)
  const metrics = buildModuleMetrics(courses, students, materials, assessments)
  const filteredMetrics = moduleFilter === 'Todos' ? metrics : metrics.filter(item => item.code === moduleFilter)
  const overdue = activeAssessments.reduce((sum, item) => sum + Math.max(0, item.total - item.submissions), 0)
  const ungraded = assessments.reduce((sum, item) => sum + item.submissionDetails.filter(submission => submission.submitted_at && submission.score === null).length, 0)
  return <>
    <section className="teacher-command-hero"><div><span className="eyebrow">{today}</span><h1>Centro de control docente</h1><p>Supervisa grupos, contenidos, entregas y resultados desde un solo lugar.</p></div><div className="command-actions"><button onClick={() => setView('alumnos')}><Users size={17} />Alumnos</button><button onClick={() => setView('materiales')}><BookOpen size={17} />Materiales</button><button onClick={() => setView('evaluaciones')}><ClipboardCheck size={17} />Evaluaciones</button></div></section>
    <section className="teacher-kpi-grid">
      <Stat icon={Users} value={students.length} label="Alumnos en padrón" note={`${groups.length} grupos`} color="blue" />
      <Stat icon={BookOpen} value={materials.filter(item => item.published).length} label="Materiales publicados" note="Información real" color="gold" />
      <Stat icon={ClipboardCheck} value={activeAssessments.length} label="Evaluaciones activas" note={`${submitted} entregas · ${drafts} avances`} color="purple" />
      <Stat icon={TrendingUp} value={overallAverage === null ? '—' : `${overallAverage} / 60`} label="Promedio general" note={overallAverage === null ? 'Sin calificaciones' : 'Calculado con entregas'} color="green" />
      <Stat icon={FileText} value={ungraded} label="Pendientes de calificar" note={ungraded ? 'Requieren revisión' : 'Todo revisado'} color="gold" />
    </section>
    <section className="dashboard-toolbar"><div><strong>Panorama por módulo</strong><span>Las gráficas se calculan con alumnos, actividades y calificaciones reales.</span></div><select value={moduleFilter} onChange={event => setModuleFilter(event.target.value)}><option value="Todos">Todos los módulos</option>{metrics.map(item => <option key={item.key} value={item.code}>{item.code} · Grupo {item.group}</option>)}</select></section>
    <section className="module-insight-grid">{filteredMetrics.map(metric => <ModuleInsight key={metric.key} metric={metric} onMaterials={() => setView('materiales')} onAssessments={() => setView('evaluaciones')} />)}</section>
    <section className="teacher-chart-grid">
      <div className="panel chart-panel"><PanelTitle title="Entregas por módulo" /><ModuleBarChart metrics={metrics} field="completion" suffix="%" /></div>
      <div className="panel chart-panel"><PanelTitle title="Promedio por módulo" /><ModuleBarChart metrics={metrics} field="average" suffix="/60" /></div>
      <div className="panel attention-panel"><PanelTitle title="Atención necesaria" /><div className="attention-list"><button onClick={() => setView('evaluaciones')}><span className="attention-number">{ungraded}</span><span><strong>Entregas sin calificar</strong><small>Abrir resultados y registrar calificación</small></span><ChevronRight size={18} /></button><button onClick={() => setView('evaluaciones')}><span className="attention-number amber">{overdue}</span><span><strong>Entregas pendientes</strong><small>Alumnos que aún no entregan actividades activas</small></span><ChevronRight size={18} /></button><button onClick={() => setView('materiales')}><span className="attention-number blue">{materials.filter(item => !item.published).length}</span><span><strong>Materiales bloqueados</strong><small>Listos para publicar cuando usted decida</small></span><ChevronRight size={18} /></button></div></div>
    </section>
    <section className="two-cols teacher-lower-grid">
      <div className="panel"><PanelTitle title="Actividad reciente" action="Ver alumnos" onClick={() => setView('alumnos')} />{recent.length ? <div className="recent-list">{recent.map(item => <Activity key={item.id} initials={(item.student?.name || 'Alumno').split(' ').slice(0, 2).map(part => part[0]).join('')} title={item.student?.name || 'Alumno'} meta={`${item.submitted_at ? 'Entregó' : 'Guardó avance'} · ${item.assessment} · Grupo ${item.group}`} color={item.submitted_at ? 'green' : 'blue'} />)}</div> : <EmptyState text="Todavía no hay actividad de alumnos registrada." />}</div>
      <div className="panel"><PanelTitle title="Avance por grupo" /><div className="group-progress">{groups.map(group => { const activeStudents = new Set(assessments.filter(item => item.group === group.code).flatMap(item => item.submissionDetails.map(submission => submission.student_id))).size; const progress = group.students ? Math.round(activeStudents / group.students * 100) : 0; return <div className="progress-row" key={group.id}><div><strong>Grupo {group.code}</strong><span>{group.students} alumnos · {group.semester}º semestre</span></div><div className="progress-meta"><b>{activeStudents ? `${activeStudents} con actividad` : 'Sin actividad'}</b><div className="bar"><i style={{ width: `${progress}%` }} /></div></div></div> })}</div></div>
    </section>
    <section className="panel"><PanelTitle title="Evaluaciones activas" action="Ver todas" onClick={() => setView('evaluaciones')} /><AssessmentTable items={activeAssessments} onOpen={onOpenAssessment} /></section>
  </>
}

function itemBelongsToCourse(item, course, sameGroupCourses) {
  if (item.group !== course.group) return false
  const code = item.activityCode?.split('-')[0]
  if (code) return code === course.code
  if (String(item.title || '').toUpperCase().includes(course.code)) return true
  return sameGroupCourses.length === 1
}

function buildModuleMetrics(courseList, students, materials, assessments) {
  return courseList.map(course => {
    const sameGroupCourses = courseList.filter(item => item.group === course.group)
    const moduleStudents = students.filter(student => student.group === course.group)
    const moduleMaterials = materials.filter(item => itemBelongsToCourse(item, course, sameGroupCourses))
    const moduleAssessments = assessments.filter(item => itemBelongsToCourse(item, course, sameGroupCourses))
    const possible = moduleStudents.length * moduleAssessments.length
    const delivered = moduleAssessments.reduce((sum, item) => sum + item.submissions, 0)
    const scores = moduleAssessments.flatMap(item => item.submissionDetails).filter(item => item.score !== null).map(item => Number(item.score))
    return { ...course, key: `${course.code}-${course.group}`, students: moduleStudents.length, materials: moduleMaterials.length, publishedMaterials: moduleMaterials.filter(item => item.published).length, assessments: moduleAssessments.length, activeAssessments: moduleAssessments.filter(item => item.status === 'Activa').length, delivered, possible, completion: possible ? Math.round(delivered / possible * 100) : 0, average: scores.length ? Math.round(scores.reduce((sum, value) => sum + value, 0) / scores.length) : 0, hasScores: scores.length > 0 }
  })
}

function ModuleInsight({ metric, onMaterials, onAssessments }) {
  return <article className="module-insight"><header><div className="module-code">{metric.code}</div><div><strong>{metric.name}</strong><span>Grupo {metric.group} · {metric.students} alumnos</span></div><div className="completion-donut" style={{ '--progress': `${metric.completion * 3.6}deg` }}><i>{metric.completion}%</i></div></header><div className="module-metric-row"><div><b>{metric.publishedMaterials}/{metric.materials}</b><span>Materiales visibles</span></div><div><b>{metric.activeAssessments}/{metric.assessments}</b><span>Evaluaciones activas</span></div><div><b>{metric.delivered}/{metric.possible || 0}</b><span>Entregas</span></div><div><b>{metric.hasScores ? `${metric.average}/60` : '—'}</b><span>Promedio</span></div></div><footer><button onClick={onMaterials}>Administrar materiales</button><button onClick={onAssessments}>Ver evaluaciones</button></footer></article>
}

function ModuleBarChart({ metrics, field, suffix }) {
  const max = field === 'average' ? 60 : 100
  return <div className="module-bar-chart">{metrics.map(metric => <div className="chart-row" key={metric.key}><span><b>{metric.code}</b><small>Gpo. {metric.group}</small></span><div><i style={{ width: `${Math.min(100, metric[field] / max * 100)}%` }} /></div><strong>{field === 'average' && !metric.hasScores ? '—' : `${metric[field]}${suffix}`}</strong></div>)}</div>
}

function StudentHome({ session, courses, materials, assessments, setView }) {
  const nextAssessment = assessments.find(item => item.status === 'Activa')
  const latestMaterial = materials[0]
  return <>
    <section className="welcome-row"><div><span className="eyebrow">GRUPO {session.group} · {session.semester}º SEMESTRE</span><h1>Hola, {session.name}.</h1><p>Continúa con tus actividades y revisa lo nuevo de tu clase.</p></div><div className="student-score"><span>Tu promedio</span><strong>—</strong><small>Sin calificaciones todavía</small></div></section>
    <section className="stat-grid student-stats"><Stat icon={GraduationCap} value={courses.length} label={courses.length === 1 ? 'Módulo asignado' : 'Módulos asignados'} note={`Grupo ${session.group}`} color="purple" /><Stat icon={BookOpen} value={materials.length} label="Materiales disponibles" note="Información real" color="blue" /><Stat icon={ClipboardCheck} value={assessments.filter(item => item.status === 'Activa').length} label="Evaluaciones activas" note="Revisa las fechas" color="gold" /></section>
    <section className="panel student-modules-preview"><PanelTitle title="Tus módulos" action="Ver todos" onClick={() => setView('modulos')} /><div className="module-mini-list">{courses.map(course => <div className="module-mini" key={course.code}><div className="module-code">{course.code}</div><div><strong>{course.name}</strong><span>{course.hoursPerWeek} horas por semana</span></div></div>)}</div></section>
    <section className="two-cols"><div className="panel"><PanelTitle title="Próxima entrega" />{nextAssessment ? <div className="next-task"><div><span className="tag active">ACTIVA</span><h3>{nextAssessment.title}</h3><p>Entrega: {nextAssessment.due}</p></div></div> : <EmptyState text="No tienes evaluaciones activas." />}</div><div className="panel"><PanelTitle title="Material nuevo" />{latestMaterial ? <div className="featured-material"><div className="file-icon"><FileText /></div><div><h3>{latestMaterial.title}</h3><p>{latestMaterial.type} · {latestMaterial.unit}</p></div></div> : <EmptyState text="Todavía no hay materiales publicados." />}</div></section>
  </>
}

function StudentPreview({ session, courses, materials, assessments }) {
  const [previewView, setPreviewView] = useState('inicio')
  const [previewProgress, setPreviewProgress] = useState([])
  useEffect(() => { setPreviewView('inicio'); setPreviewProgress([]) }, [session.group])
  return <div className="student-preview-shell">
    <div className="preview-banner"><div><span className="eyebrow">VISTA PREVIA · GRUPO {session.group}</span><strong>Así verá el alumno únicamente el contenido publicado.</strong></div><div className="preview-avatar">AD</div></div>
    <nav className="preview-nav">
      <button className={previewView === 'inicio' ? 'active' : ''} onClick={() => setPreviewView('inicio')}><LayoutDashboard size={17} />Resumen</button>
      <button className={previewView === 'modulos' ? 'active' : ''} onClick={() => setPreviewView('modulos')}><GraduationCap size={17} />Mis módulos</button>
      <button className={previewView === 'materiales' ? 'active' : ''} onClick={() => setPreviewView('materiales')}><BookOpen size={17} />Materiales</button>
      <button className={previewView === 'evaluaciones' ? 'active' : ''} onClick={() => setPreviewView('evaluaciones')}><ClipboardCheck size={17} />Evaluaciones</button>
    </nav>
    {previewView === 'inicio' && <StudentHome session={session} courses={courses} materials={materials} assessments={assessments} setView={setPreviewView} />}
    {previewView === 'modulos' && <Modules courses={courses} session={session} setView={setPreviewView} />}
    {previewView === 'materiales' && <Materials items={materials} groups={[]} courses={courses} session={session} isTeacher={false} onProgressUpdate={progress => setPreviewProgress(current => [...current.filter(item => item.material_code !== progress.material_code), progress])} />}
    {previewView === 'evaluaciones' && <Assessments items={assessments} session={session} isTeacher={false} learningProgress={previewProgress} />}
  </div>
}

function Modules({ courses, session, setView }) {
  return <section className="panel page-panel"><div className="list-toolbar"><div><span className="eyebrow">GRUPO {session.group} · {session.semester}º SEMESTRE</span><h1>Mis módulos</h1><p>Materias que cursas durante el periodo actual.</p></div></div><div className="module-grid">{courses.map(course => <article className="module-card" key={course.code}><div className="module-card-head"><div className="module-code large">{course.code}</div><span>{course.hoursPerWeek} h/semana</span></div><h3>{course.name}</h3><p>Grupo {course.group} · {course.semester}º semestre</p>{course.outcomes?.length ? <small>{course.outcomes.length} resultados de aprendizaje</small> : <small>Programa académico asignado</small>}<div className="module-actions"><button className="secondary" onClick={() => setView('materiales')}>Ver materiales</button><button className="text-btn" onClick={() => setView('evaluaciones')}>Evaluaciones <ChevronRight size={15} /></button></div></article>)}</div></section>
}

function TeacherModules({ courses, students, materials, assessments, setView }) {
  const metrics = buildModuleMetrics(courses, students, materials, assessments)
  return <section className="teacher-modules-page"><div className="list-toolbar"><div><span className="eyebrow">CONTROL ACADÉMICO</span><h1>Módulos asignados</h1><p>Consulta el estado de cada materia y entra directamente a sus recursos.</p></div></div><div className="module-insight-grid expanded">{metrics.map(metric => <ModuleInsight key={metric.key} metric={metric} onMaterials={() => setView('materiales')} onAssessments={() => setView('evaluaciones')} />)}</div><div className="panel module-comparison"><PanelTitle title="Comparación general" /><div className="comparison-grid"><div><h3>Porcentaje de entregas</h3><ModuleBarChart metrics={metrics} field="completion" suffix="%" /></div><div><h3>Promedio registrado</h3><ModuleBarChart metrics={metrics} field="average" suffix="/60" /></div></div></div></section>
}

function Materials({ items, groups, courses, session, isTeacher, onAdd, onToggle, onProgressUpdate }) {
  const [query, setQuery] = useState('')
  const [group, setGroup] = useState('Todos')
  const [selectedMaterial, setSelectedMaterial] = useState(null)
  const filtered = items.filter(m => (group === 'Todos' || m.group === group) && m.title.toLowerCase().includes(query.toLowerCase()))
  async function openMaterial(material) {
    if (material.url?.startsWith('mtcs://')) { setSelectedMaterial(material); return }
    if (material.type !== 'Archivo') return window.open(material.url, '_blank', 'noopener,noreferrer')
    const preview = window.open('about:blank', '_blank')
    const { data, error } = await supabase.storage.from('materials').createSignedUrl(material.url, 300)
    if (error) { preview?.close(); return }
    if (preview) preview.location.href = data.signedUrl
    else window.location.href = data.signedUrl
  }
  if (selectedMaterial) return <MtcsMaterialView code={selectedMaterial.url.replace('mtcs://', '')} session={session} onProgressUpdate={onProgressUpdate} onBack={() => setSelectedMaterial(null)} />
  return <section className="panel page-panel"><div className="list-toolbar"><div>{!isTeacher && <span className="eyebrow">GRUPO {session.group}</span>}<h1>{isTeacher ? 'Material didáctico' : 'Mis materiales'}</h1><p>{isTeacher ? 'Recursos organizados por grupo y unidad.' : `Recursos de ${courses.map(course => course.name).join(' y ')}.`}</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Upload size={18} />Publicar material</button>}</div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar material…" /></div>{isTeacher ? <select value={group} onChange={e => setGroup(e.target.value)}><option value="Todos">Todos los grupos</option>{groups.map(item => <option key={item.id} value={item.code}>Grupo {item.code}</option>)}</select> : <div className="group-chip">Grupo {session.group}</div>}</div>{filtered.length ? <div className="card-grid">{filtered.map(m => <article className={`material-card ${!m.published ? 'locked-card' : ''}`} key={m.id}><div className="material-icon"><FileText /></div><span className={`tag ${m.published ? 'active' : ''}`}>{isTeacher ? (m.published ? 'PUBLICADO' : 'BLOQUEADO') : m.unit}</span><h3>{m.title}</h3><p>{m.type} · Grupo {m.group} · {m.unit}</p><footer><span>{m.published ? 'Visible para alumnos' : 'Oculto para alumnos'}</span><div className="card-actions"><button className="text-btn" onClick={() => openMaterial(m)}>Abrir <ChevronRight size={15} /></button>{isTeacher && <button className="lock-btn" onClick={() => onToggle?.(m)}>{m.published ? <Lock size={15} /> : <Unlock size={15} />}{m.published ? 'Bloquear' : 'Publicar'}</button>}</div></footer></article>)}</div> : <EmptyState text={isTeacher ? 'No hay materiales con estos filtros.' : 'Todavía no hay materiales publicados para tu grupo.'} />}</section>
}

function Assessments({ items, session, isTeacher, learningProgress = [], onAdd, onRefresh, onToggle, initialSelected, onClearSelected }) {
  const [selected, setSelected] = useState(initialSelected || null)
  function clearSelected() { setSelected(null); onClearSelected?.() }
  if (selected && isTeacher) return <AssessmentResults assessment={selected} onBack={clearSelected} onRefresh={onRefresh} />
  if (selected) {
    if (selected.activityCode === 'ASIN-RA-1.1') return <AsinActivity assessment={selected} onBack={clearSelected} />
    if (selected.activityCode === 'MSII-RA-1.1') return <MsiiActivity assessment={selected} session={session} onBack={clearSelected} />
    if (selected.activityCode?.startsWith('PEAR-')) return <PearActivity assessment={selected} session={session} onBack={clearSelected} />
    if (selected.activityCode?.startsWith('MTCS-')) return <MtcsActivity assessment={selected} session={session} onBack={clearSelected} />
    return <GenericActivity assessment={selected} onBack={clearSelected} />
  }
  const visibleItems = items.map(item => ({ ...item, locked: !isTeacher && item.activityCode?.startsWith('MTCS-RA-') && !learningProgress.some(progress => progress.material_code === item.activityCode && progress.completed_at) }))
  return <section className="panel page-panel"><div className="list-toolbar"><div>{!isTeacher && <span className="eyebrow">GRUPO {session.group}</span>}<h1>{isTeacher ? 'Evaluaciones' : 'Mis evaluaciones'}</h1><p>{isTeacher ? 'Actividades y resultados de tus grupos.' : 'Evaluaciones asignadas a tus módulos.'}</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Plus size={18} />Nueva evaluación</button>}</div><AssessmentTable items={visibleItems} student={!isTeacher} onOpen={setSelected} onToggle={onToggle} /></section>
}

function AssessmentTable({ items, student, onOpen, onToggle }) { if (!items.length) return <EmptyState text="Todavía no hay evaluaciones registradas." />; return <div className={`table-wrap ${student ? 'student-assessment-table' : ''}`}><table><thead><tr><th>Evaluación</th><th>Grupo</th><th>Entrega</th>{!student && <th>Actividad</th>}<th>{student ? 'Estado' : 'Publicación'}</th><th /></tr></thead><tbody>{items.map(a => <tr key={a.id} className={a.locked ? 'locked-assessment' : ''}><td data-label="Evaluación"><div className="title-cell"><div className="mini-icon">{a.locked ? <Lock size={17} /> : <ClipboardCheck size={17} />}</div><strong>{a.title}</strong></div></td><td data-label="Grupo">{a.group}</td><td data-label="Entrega">{a.due}</td>{!student && <td data-label="Actividad"><strong>{a.submissions}</strong> entregas · {a.drafts} avances</td>}<td data-label="Estado"><span className={`tag ${a.status === 'Activa' && !a.locked ? 'active' : ''}`}>{a.locked ? 'BLOQUEADA' : a.status}</span></td><td className="assessment-open"><div className="table-actions"><button className="text-btn" disabled={a.locked} onClick={() => !a.locked && onOpen?.(a)}>{a.locked ? 'Completa los materiales' : student ? 'Abrir actividad' : 'Resultados'} {!a.locked && <ChevronRight size={15} />}</button>{!student && onToggle && <button className="lock-btn" onClick={() => onToggle(a)}>{a.status === 'Activa' ? <Lock size={15} /> : <Unlock size={15} />}{a.status === 'Activa' ? 'Bloquear' : 'Publicar'}</button>}</div></td></tr>)}</tbody></table></div> }

function GenericActivity({ assessment, onBack }) {
  return <section className="panel page-panel activity-workspace"><button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button><div className="activity-hero"><div><span className="eyebrow">ACTIVIDAD</span><h1>{assessment.title}</h1><p>{assessment.instructions || 'Consulta con tu docente las indicaciones de esta actividad.'}</p></div></div><div className="info-note">Esta actividad es informativa y no solicita una entrega dentro de la plataforma.</div></section>
}

function AssessmentResults({ assessment, onBack, onRefresh }) {
  const [rows, setRows] = useState(assessment.submissionDetails)
  const [scores, setScores] = useState(() => Object.fromEntries(assessment.submissionDetails.map(item => [item.id, item.score ?? ''])))
  const [busy, setBusy] = useState('')
  const [message, setMessage] = useState('')

  async function saveScore(submission) {
    const score = Number(scores[submission.id])
    if (!Number.isFinite(score) || score < 0 || score > 60) { setMessage('La calificación debe estar entre 0 y 60 puntos.'); return }
    setBusy(submission.id); setMessage('')
    const { error } = await supabase.from('submissions').update({ score }).eq('id', submission.id)
    if (error) setMessage(error.message || 'No fue posible guardar la calificación.')
    else {
      setRows(current => current.map(item => item.id === submission.id ? { ...item, score } : item))
      setMessage('Calificación guardada correctamente.')
      await onRefresh?.()
    }
    setBusy('')
  }

  async function downloadSubmission(submission) {
    if (!submission.file_path) return
    const { data, error } = await supabase.storage.from('submissions').createSignedUrl(submission.file_path, 300)
    if (error) setMessage(error.message || 'No fue posible abrir el archivo.')
    else window.open(data.signedUrl, '_blank', 'noopener,noreferrer')
  }

  async function downloadPractice(practice) {
    if (!practice?.path) return
    const { data, error } = await supabase.storage.from('submissions').createSignedUrl(practice.path, 300)
    if (error) setMessage(error.message || 'No fue posible abrir la práctica.')
    else window.open(data.signedUrl, '_blank', 'noopener,noreferrer')
  }

  const checksumStudents = new Map()
  rows.forEach(submission => Object.values(submission.answers?.packet_tracer || {}).forEach(practice => {
    if (!practice.checksum) return
    if (!checksumStudents.has(practice.checksum)) checksumStudents.set(practice.checksum, new Set())
    checksumStudents.get(practice.checksum).add(submission.student_id)
  }))
  const duplicatedChecksums = new Set([...checksumStudents.entries()].filter(([, students]) => students.size > 1).map(([checksum]) => checksum))

  return <section className="panel page-panel results-page">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="results-head"><div><span className="eyebrow">GRUPO {assessment.group}</span><h1>{assessment.title}</h1><p>{assessment.submissions} entregas y {assessment.drafts} avances guardados.</p></div><div className="result-total"><strong>{rows.length}</strong><span>{rows.length === 1 ? 'alumno con actividad' : 'alumnos con actividad'}</span></div></div>
    {message && <div className={message.includes('correctamente') ? 'submission-success' : 'form-error'}>{message}</div>}
    {rows.length ? <div className="submission-list">{rows.map(submission => <article className="submission-card" key={submission.id}>
      <header><div className="student-cell"><div className="avatar small">{(submission.student?.name || 'A').split(' ').slice(0, 2).map(part => part[0]).join('')}</div><div><strong>{submission.student?.name || 'Alumno'}</strong><span>{submission.student?.enrollment || submission.student?.email || 'Sin matrícula'}</span></div></div><span className={`tag ${submission.submitted_at ? 'active' : ''}`}>{submission.submitted_at ? 'ENTREGADA' : 'EN PROCESO'}</span></header>
      <div className="submission-meta"><span>Inicio: {formatDateTime(submission.started_at)}</span>{submission.submitted_at && <span>Entrega: {formatDateTime(submission.submitted_at)}</span>}</div>
      {Object.values(submission.answers?.packet_tracer || {}).some(practice => duplicatedChecksums.has(practice.checksum)) && <div className="duplicate-warning">Revisión sugerida: uno o más archivos de Packet Tracer coinciden exactamente con la entrega de otro alumno.</div>}
      <div className="submission-actions">{submission.file_path && <button className="secondary" onClick={() => downloadSubmission(submission)}><Download size={16} /> {submission.original_filename || 'Descargar archivo'}</button>}{Object.values(submission.answers?.packet_tracer || {}).map(practice => <button className="secondary packet-download" key={practice.path} onClick={() => downloadPractice(practice)}><Download size={16} /> {practice.practice || practice.filename}</button>)}{submission.answers && Object.keys(submission.answers).length > 0 && <details><summary><Eye size={16} /> Ver respuestas capturadas</summary><AnswerPreview answers={submission.answers} /></details>}</div>
      {submission.submitted_at && <div className="score-box"><label>Calificación de la actividad (máximo 60 puntos)<input type="number" min="0" max="60" step="1" value={scores[submission.id]} onChange={e => setScores(current => ({ ...current, [submission.id]: e.target.value }))} /></label><button className="primary" disabled={busy === submission.id} onClick={() => saveScore(submission)}>{busy === submission.id ? 'Guardando…' : 'Guardar calificación'}</button></div>}
    </article>)}</div> : <EmptyState text="Ningún alumno ha iniciado esta actividad todavía." />}
  </section>
}

function formatDateTime(value) {
  return value ? new Intl.DateTimeFormat('es-MX', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }).format(new Date(value)) : '—'
}

function AnswerPreview({ answers }) {
  const risks = answers.risks || []
  const equipment = answers.equipment || {}
  const questions = [...(answers.questionnaires?.users || []), ...(answers.questionnaires?.administrators || [])]
  const responses = answers.responses || {}
  const packetTracer = Object.values(answers.packet_tracer || {})
  const hasContent = risks.some(item => item.risk || item.description) || Object.values(equipment).some(Boolean) || questions.some(item => item.text) || Object.values(responses).some(Boolean) || packetTracer.length > 0
  if (!hasContent) return <div className="answer-preview empty">El alumno inició la actividad, pero todavía no ha capturado respuestas.</div>
  return <div className="answer-preview">
    {risks.some(item => item.risk || item.description) && <section><h4>Matrices de riesgo</h4>{risks.map((risk, index) => (risk.risk || risk.description) && <article key={index}><strong>{index + 1}. {risk.risk || 'Riesgo sin nombre'}</strong><p>{risk.description || 'Sin descripción'}</p><small>Probabilidad: {risk.probability || '—'} · Impacto: {risk.impact || '—'} · Medidas: {risk.measures || '—'}</small></article>)}</section>}
    {Object.values(equipment).some(Boolean) && <section><h4>Ficha técnica</h4><div className="answer-grid">{Object.entries(equipment).filter(([, value]) => value).map(([key, value]) => <div key={key}><span>{equipmentLabels[key] || key}</span><strong>{value}</strong></div>)}</div></section>}
    {questions.some(item => item.text) && <section><h4>Cuestionarios</h4><ol>{questions.filter(item => item.text).map((item, index) => <li key={index}>{item.text} <small>{item.type}</small></li>)}</ol></section>}
    {packetTracer.length > 0 && <section><h4>Prácticas de Packet Tracer</h4>{packetTracer.map(practice => <article key={practice.path}><strong>{practice.practice}</strong><p>{practice.filename}</p><small>Datos asignados: {practice.assigned_code || '—'} · Entregada: {formatDateTime(practice.uploaded_at)}</small></article>)}</section>}
    {Object.values(responses).some(Boolean) && <section><h4>Actividad MTCS</h4>{answers.assigned_case?.lines?.length > 0 && <article><strong>{answers.assigned_case.title || 'Caso asignado'}</strong><p>{answers.assigned_case.lines.join(' · ')}</p></article>}<div className="mtcs-answer-list">{Object.entries(responses).map(([key, value], index) => value && <article key={key}><strong>{index + 1}. Respuesta</strong><p>{value}</p></article>)}</div></section>}
  </div>
}

const equipmentLabels = { stationNumber: 'Número de PC', brandModel: 'Marca y modelo', operatingSystem: 'Sistema operativo', processor: 'Procesador', ram: 'Memoria RAM', storage: 'Almacenamiento', antivirus: 'Antivirus', network: 'Conectividad', observations: 'Observaciones' }

function MsiiActivity({ assessment, session, onBack }) {
  const [assignment, setAssignment] = useState(null)
  const [equipmentNumber, setEquipmentNumber] = useState('')
  const [status, setStatus] = useState('loading')
  const [message, setMessage] = useState('')
  const [file, setFile] = useState(null)

  useEffect(() => {
    let active = true
    async function loadAssignment() {
      try {
        const { data, error } = await supabase.rpc('get_or_create_msii_assignment', { p_assessment_id: assessment.id })
        if (error) throw error
        if (active) {
          const current = Array.isArray(data) ? data[0] : data
          setAssignment(current)
          setEquipmentNumber(String(current?.variant?.equipment || '').replace(/\D/g, ''))
          setStatus('ready')
        }
      } catch (error) {
        if (active) { setMessage(error.message || 'No fue posible preparar tu actividad'); setStatus('error') }
      }
    }
    loadAssignment()
    return () => { active = false }
  }, [assessment.id])

  async function downloadActivity() {
    try {
      setStatus('working'); setMessage('')
      if (!equipmentNumber || Number(equipmentNumber) < 1) throw new Error('Escribe el número de la PC que estás utilizando.')
      const equipment = `Equipo ${String(Number(equipmentNumber)).padStart(2, '0')}`
      const { data, error } = await supabase.rpc('set_current_equipment', { p_assessment_id: assessment.id, p_equipment: equipment })
      if (error) throw error
      const updatedAssignment = Array.isArray(data) ? data[0] : data
      setAssignment(updatedAssignment)
      const blob = await buildMsiiDocument(updatedAssignment, session)
      const surname = session.name.trim().split(/\s+/).at(-1) || 'Alumno'
      downloadBlob(blob, `MSII_310_${surname}_RA_1.1.docx`)
      setStatus('ready')
    } catch (error) { setMessage(error.message); setStatus('error') }
  }

  async function submitActivity(event) {
    event.preventDefault()
    if (!file) return
    try {
      setStatus('working'); setMessage('')
      const token = await readAssignmentId(file)
      if (!token) throw new Error('No fue posible reconocer este archivo. Descarga nuevamente la actividad y trabaja en ese documento.')
      if (token !== assignment.id) throw new Error('No es posible entregar este archivo. Descarga nuevamente tu actividad.')
      const { data: authData } = await supabase.auth.getUser()
      const path = `${authData.user.id}/${assessment.id}/${assignment.id}.docx`
      const { error: uploadError } = await supabase.storage.from('submissions').upload(path, file, { upsert: true, contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
      if (uploadError) throw uploadError
      const { error } = await supabase.rpc('submit_msii_document', {
        p_assessment_id: assessment.id,
        p_assignment_id: assignment.id,
        p_file_path: path,
        p_original_filename: file.name,
        p_document_token: token,
      })
      if (error) throw error
      setMessage('Actividad entregada correctamente.')
      setStatus('submitted')
    } catch (error) { setMessage(error.message || 'No fue posible entregar la actividad'); setStatus('error') }
  }

  return <section className="panel page-panel activity-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">MSII · R.A. 1.1</span><h1>{assessment.title}</h1><p>{assessment.instructions || 'Descarga tu formato, complétalo y entrega el mismo archivo DOCX.'}</p></div></div>
    {status === 'loading' ? <div className="loading-state">Preparando tus datos individuales…</div> : assignment && <>
      <div className="assigned-grid">
        <label className="assigned-value equipment-input"><span>Número de PC que estás utilizando</span><input type="number" min="1" inputMode="numeric" value={equipmentNumber} onChange={event => setEquipmentNumber(event.target.value)} required /></label>
        <AssignedValue label="Sistema para comparar" value={assignment.variant.compare_os} />
        <AssignedValue label="Número decimal" value={assignment.variant.decimal_number} />
        <AssignedValue label="Carácter ASCII" value={assignment.variant.ascii_character} />
        <AssignedValue label="Capacidad" value={assignment.variant.capacity} />
      </div>
      <div className="activity-steps">
        <article><span>1</span><div><h3>Descarga tu archivo</h3><p>Descarga el formato preparado para esta actividad.</p><button className="primary" onClick={downloadActivity} disabled={status === 'working'}><Download size={17} /> Descargar actividad DOCX</button></div></article>
        <article><span>2</span><div><h3>Completa la actividad</h3><p>Trabaja en el mismo documento. No cambies los datos asignados ni lo conviertas a otro formato.</p></div></article>
        <article><span>3</span><div><h3>Entrega el mismo archivo</h3><form onSubmit={submitActivity}><input type="file" accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document" onChange={e => setFile(e.target.files[0] || null)} required /><button className="primary" disabled={status === 'working' || status === 'submitted'}><Upload size={17} /> {status === 'submitted' ? 'Entregado' : 'Subir actividad'}</button></form></div></article>
      </div>
    </>}
    {message && <div className={status === 'submitted' ? 'submission-success' : 'form-error'}>{message}</div>}
  </section>
}

function AssignedValue({ label, value }) { return <div className="assigned-value"><span>{label}</span><strong>{value}</strong></div> }

function PearActivity({ assessment, session, onBack }) {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('loading')
  const [message, setMessage] = useState('')
  const assignment = useMemo(() => buildPearAssignment(`${session.id}-${assessment.id}`, assessment.activityCode), [session.id, assessment.id, assessment.activityCode])

  useEffect(() => {
    let active = true
    supabase.from('submissions').select('submitted_at').eq('assessment_id', assessment.id).maybeSingle().then(({ data, error }) => {
      if (!active) return
      if (error) { setMessage(error.message); setStatus('error') }
      else setStatus(data?.submitted_at ? 'submitted' : 'ready')
    })
    return () => { active = false }
  }, [assessment.id])

  async function submit(event) {
    event.preventDefault()
    if (!file) return
    try {
      setStatus('working'); setMessage('')
      if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) throw new Error('Entrega un archivo en formato PDF.')
      if (file.size > 20 * 1024 * 1024) throw new Error('El archivo no debe superar 20 MB.')
      const { data: authData } = await supabase.auth.getUser()
      const path = `${authData.user.id}/${assessment.id}/entrega.pdf`
      const { error: uploadError } = await supabase.storage.from('submissions').upload(path, file, { upsert: true, contentType: 'application/pdf' })
      if (uploadError) throw uploadError
      const { error } = await supabase.from('submissions').insert({ assessment_id: assessment.id, student_id: authData.user.id, answers: { assigned_case: assignment }, file_path: path, original_filename: file.name, submitted_at: new Date().toISOString() })
      if (error) throw error
      setStatus('submitted'); setMessage('Actividad entregada correctamente.')
    } catch (error) { setStatus('error'); setMessage(error.message || 'No fue posible entregar la actividad.') }
  }

  return <section className="panel page-panel activity-workspace pear-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">PEAR · {assessment.activityCode.includes('1.2') ? 'PROPÓSITO 1.2' : 'PROPÓSITO 1.3'}</span><h1>{assessment.title}</h1><p>{assessment.instructions}</p></div></div>
    <div className="assigned-case"><h2>Datos asignados para tu trabajo</h2><p>Utiliza estos datos en el reporte que entregarás.</p><div className="assigned-grid">{assignment.map(item => <AssignedValue key={item.label} label={item.label} value={item.value} />)}</div></div>
    <form className="pear-submit" onSubmit={submit}><label>Entrega tu archivo PDF<input type="file" accept=".pdf,application/pdf" disabled={status === 'submitted' || status === 'working'} required onChange={event => setFile(event.target.files[0] || null)} /></label><button className="primary" disabled={!file || status === 'submitted' || status === 'working'}><Upload size={17} /> {status === 'submitted' ? 'Actividad entregada' : status === 'working' ? 'Subiendo…' : 'Entregar actividad'}</button></form>
    {message && <div className={status === 'submitted' ? 'submission-success' : 'form-error'}>{message}</div>}
  </section>
}

function buildPearAssignment(seedText, activityCode) {
  let seed = 0
  for (const char of seedText) seed = (seed * 31 + char.charCodeAt(0)) >>> 0
  const pick = (min, max, offset = 0) => min + ((seed >>> offset) % (max - min + 1))
  if (activityCode.includes('1.1')) {
    const cases = [
      ['Derecho a la educación', 'Todas las personas tienen acceso a la educación.', 'La escuela ofrece condiciones de igualdad.', 'La comunidad participa en las decisiones escolares.'],
      ['Privacidad digital', 'Los datos personales están protegidos.', 'Las aplicaciones solicitan autorización informada.', 'Las personas conocen cómo se utiliza su información.'],
      ['Igualdad y no discriminación', 'Todas las personas reciben un trato digno.', 'Las reglas se aplican sin distinciones injustificadas.', 'Existen mecanismos para denunciar la discriminación.'],
      ['Libertad de expresión', 'Las personas pueden expresar sus ideas.', 'Las opiniones respetan los derechos de otras personas.', 'El diálogo permite responder a los desacuerdos.'],
      ['Derecho a un ambiente sano', 'La comunidad reduce la generación de residuos.', 'Las autoridades atienden los reportes ambientales.', 'La población participa en el cuidado de los espacios comunes.'],
    ]
    const selected = cases[seed % cases.length]
    return [{ label: 'Tema del debate', value: selected[0] }, { label: 'Proposición p', value: selected[1] }, { label: 'Proposición q', value: selected[2] }, { label: 'Proposición r', value: selected[3] }, { label: 'Expresiones para las tablas', value: '¬p, p ∧ q, (p ∨ q) → r, p ↔ q' }]
  }
  if (activityCode.includes('1.2')) {
    const first = pick(240, 780)
    const second = pick(110, Math.min(390, first - 20), 8)
    const operation = seed % 2 ? 'Suma' : 'Resta'
    return [{ label: 'Operación que debes representar', value: operation }, { label: 'Primera cantidad', value: first }, { label: 'Segunda cantidad', value: second }]
  }
  const income = pick(680, 980) * 10
  return [{ label: 'Ingreso mensual', value: `$${income.toLocaleString('es-MX')}` }, { label: 'Integrantes del hogar', value: pick(3, 6, 6) }, { label: 'Compra de higiene', value: `Cada ${pick(12, 20, 10)} días` }, { label: 'Compra de alimentos base', value: `Cada ${pick(5, 9, 14)} días` }]
}

function Students({ students, groups, assessments, onRefresh }) {
  const [query, setQuery] = useState('')
  const [group, setGroup] = useState('Todos')
  const [selectedStudent, setSelectedStudent] = useState(null)
  const rows = useMemo(() => students.filter(s => (group === 'Todos' || s.group === group) && `${s.name} ${s.email}`.toLowerCase().includes(query.toLowerCase())), [query, group])
  function progressFor(student) {
    const submissions = assessments.filter(item => item.group === student.group).flatMap(item => item.submissionDetails).filter(item => item.student?.email === student.email)
    const delivered = submissions.filter(item => item.submitted_at)
    const scores = delivered.filter(item => item.score !== null).map(item => Number(item.score))
    return { label: delivered.length ? `${delivered.length} entregada${delivered.length === 1 ? '' : 's'}` : submissions.length ? 'En proceso' : '—', average: scores.length ? `${Math.round(scores.reduce((sum, value) => sum + value, 0) / scores.length)} / 60` : '—' }
  }
  if (selectedStudent) return <StudentRecord student={selectedStudent} assessments={assessments.filter(item => item.group === selectedStudent.group)} onBack={() => setSelectedStudent(null)} onRefresh={onRefresh} />
  return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Alumnos registrados</h1><p>Cuentas reales creadas en Aula Virtual, organizadas por grupo.</p></div></div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar alumno…" /></div><select value={group} onChange={e => setGroup(e.target.value)}><option>Todos</option>{groups.map(item => <option key={item.id}>{item.code}</option>)}</select></div><div className="table-wrap"><table><thead><tr><th>Alumno</th><th>Grupo</th><th>Matrícula</th><th>Cuenta</th><th>Progreso</th><th>Promedio</th><th /></tr></thead><tbody>{rows.map(student => { const progress = progressFor(student); return <tr key={student.id}><td><div className="student-cell"><div className="avatar small">{student.name.split(' ').slice(0,2).map(part => part[0]).join('')}</div><div><strong>{student.name}</strong><span>{student.email}</span></div></div></td><td>{student.group}</td><td>{student.enrollment || 'Sin matrícula'}</td><td><span className="tag active">Registrada</span></td><td>{progress.label}</td><td>{progress.average}</td><td><button className="text-btn" onClick={() => setSelectedStudent(student)}>Ver expediente <ChevronRight size={15} /></button></td></tr> })}</tbody></table></div></section>
}

function evidenceReview(assessment, submission) {
  if (!submission) return { suggested: 0, checks: [{ label: 'El alumno todavía no inicia la actividad', ok: false }] }
  const answers = submission.answers || {}
  const responses = Object.values(answers.responses || {}).filter(value => String(value).trim().length >= 12)
  const risks = (answers.risks || []).filter(item => item.risk && item.description && item.probability && item.impact)
  const equipment = Object.values(answers.equipment || {}).filter(Boolean)
  const questions = [...(answers.questionnaires?.users || []), ...(answers.questionnaires?.administrators || [])].filter(item => item.text)
  const packetFiles = Object.values(answers.packet_tracer || {})
  if (assessment.activityCode === 'ASIN-RA-1.1') {
    const completeRisks = (answers.risks || []).filter(item => item.risk && item.description && item.probability && item.impact && item.actionNeeded && item.measures)
    const equipmentFields = Object.values(answers.equipment || {}).filter(value => String(value || '').trim())
    const userQuestions = (answers.questionnaires?.users || []).filter(item => item.text && item.type)
    const adminQuestions = (answers.questionnaires?.administrators || []).filter(item => item.text && item.type)
    const suggested = Math.min(60, (submission.submitted_at ? 5 : 0) + completeRisks.length * 8 + Math.round(equipmentFields.length / 9 * 11) + userQuestions.length * 2 + adminQuestions.length * 2)
    return { suggested, checks: [
      { label: `${completeRisks.length} de 3 matrices de riesgo completas`, ok: completeRisks.length === 3 },
      { label: `${equipmentFields.length} de 9 datos de la ficha técnica`, ok: equipmentFields.length === 9 },
      { label: `${userQuestions.length} de 5 preguntas para usuarios`, ok: userQuestions.length === 5 },
      { label: `${adminQuestions.length} de 5 preguntas para administradores`, ok: adminQuestions.length === 5 },
      { label: submission.submitted_at ? 'Actividad entregada formalmente' : 'La actividad permanece en proceso', ok: Boolean(submission.submitted_at) },
    ] }
  }
  if (assessment.activityCode === 'MSII-RA-1.1') return { suggested: submission.submitted_at && submission.file_path ? 10 : 0, checks: [
    { label: submission.submitted_at ? 'Documento entregado formalmente' : 'La actividad permanece en proceso', ok: Boolean(submission.submitted_at) },
    { label: submission.file_path ? `Documento recibido: ${submission.original_filename || 'archivo DOCX'}` : 'No contiene documento DOCX', ok: Boolean(submission.file_path) },
  ] }
  const hasStructured = responses.length || risks.length || equipment.length || questions.length
  let suggested = submission.submitted_at ? 10 : 4
  if (submission.file_path) suggested += 20
  if (responses.length) suggested += Math.min(30, responses.length * 4)
  if (risks.length) suggested += Math.min(15, risks.length * 5)
  if (equipment.length) suggested += Math.min(10, equipment.length)
  if (questions.length) suggested += Math.min(15, questions.length)
  if (packetFiles.length && !submission.file_path) suggested += Math.min(20, packetFiles.length * 7)
  if (!hasStructured && submission.file_path) suggested = submission.submitted_at ? 40 : 25
  return { suggested: Math.min(60, suggested), checks: [
    { label: submission.submitted_at ? 'Actividad entregada formalmente' : 'La actividad permanece en proceso', ok: Boolean(submission.submitted_at) },
    { label: submission.file_path ? `Archivo adjunto: ${submission.original_filename || 'evidencia'}` : 'No contiene archivo final', ok: Boolean(submission.file_path) },
    { label: hasStructured ? 'Contiene respuestas o evidencias capturadas' : 'Sin respuestas capturadas en la plataforma', ok: Boolean(hasStructured) },
    ...(assessment.activityCode?.startsWith('MTCS-') ? [{ label: packetFiles.length ? `${packetFiles.length} práctica(s) de Packet Tracer registrada(s)` : 'Sin prácticas de Packet Tracer asociadas', ok: packetFiles.length > 0 }] : []),
  ] }
}

function StudentRecord({ student, assessments, onBack, onRefresh }) {
  const [scores, setScores] = useState({})
  const [documentAnalyses, setDocumentAnalyses] = useState({})
  const [busy, setBusy] = useState('')
  const [message, setMessage] = useState('')
  const records = assessments.map(assessment => ({ assessment, submission: assessment.submissionDetails.find(item => item.student_id === student.id || item.student?.email === student.email) }))
  const delivered = records.filter(item => item.submission?.submitted_at)
  const scored = delivered.filter(item => item.submission.score !== null)
  const average = scored.length ? Math.round(scored.reduce((sum, item) => sum + Number(item.submission.score), 0) / scored.length) : null

  async function saveScore(record) {
    const value = Number(scores[record.submission.id] ?? record.submission.score)
    if (!Number.isFinite(value) || value < 0 || value > 60) { setMessage('La calificación debe estar entre 0 y 60 puntos.'); return }
    setBusy(record.submission.id); setMessage('')
    const { error } = await supabase.from('submissions').update({ score: value }).eq('id', record.submission.id)
    if (error) setMessage(error.message || 'No fue posible guardar la calificación.')
    else { record.submission.score = value; setMessage('Calificación guardada correctamente.'); await onRefresh?.() }
    setBusy('')
  }

  async function download(path) {
    const { data, error } = await supabase.storage.from('submissions').createSignedUrl(path, 300)
    if (error) setMessage(error.message || 'No fue posible abrir el archivo.')
    else window.open(data.signedUrl, '_blank', 'noopener,noreferrer')
  }

  async function analyzeDocument(record) {
    const submission = record.submission
    if (!submission?.file_path) return
    setBusy(`analysis-${submission.id}`); setMessage('')
    try {
      const { data, error } = await supabase.storage.from('submissions').createSignedUrl(submission.file_path, 300)
      if (error) throw error
      const response = await fetch(data.signedUrl)
      if (!response.ok) throw new Error('No fue posible descargar el documento para analizarlo.')
      const analysis = await analyzeMsiiDocument(await response.blob(), submission.assignment || {})
      setDocumentAnalyses(current => ({ ...current, [submission.id]: analysis }))
    } catch (error) { setMessage(error.message || 'No fue posible analizar el documento.') }
    finally { setBusy('') }
  }

  return <section className="student-record-page"><button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver al directorio</button><div className="student-record-hero"><div className="record-avatar">{student.name.split(' ').slice(0, 2).map(part => part[0]).join('')}</div><div><span className="eyebrow">EXPEDIENTE INDIVIDUAL · GRUPO {student.group}</span><h1>{student.name}</h1><p>{student.enrollment || 'Sin matrícula'} · {student.email}</p></div><div className="record-average"><strong>{average === null ? '—' : `${average}/60`}</strong><span>Promedio</span></div></div><div className="record-summary"><div><b>{assessments.length}</b><span>Evaluaciones asignadas</span></div><div><b>{delivered.length}</b><span>Entregadas</span></div><div><b>{scored.length}</b><span>Calificadas</span></div><div><b>{assessments.length - delivered.length}</b><span>Pendientes</span></div></div>{message && <div className={message.includes('correctamente') ? 'submission-success' : 'form-error'}>{message}</div>}<div className="student-evaluation-list">{records.map(record => { const review = evidenceReview(record.assessment, record.submission); const docAnalysis = record.submission ? documentAnalyses[record.submission.id] : null; const suggested = docAnalysis?.suggested ?? review.suggested; return <article key={record.assessment.id}><header><div><span className="eyebrow">{record.assessment.activityCode || 'ACTIVIDAD'}</span><h2>{record.assessment.title}</h2><small>Entrega: {record.assessment.due}</small></div><span className={`tag ${record.submission?.submitted_at ? 'active' : ''}`}>{record.submission?.submitted_at ? 'ENTREGADA' : record.submission ? 'EN PROCESO' : 'NO INICIADA'}</span></header><div className="individual-review-grid"><section><h3>Evidencias</h3>{review.checks.map(check => <div className={check.ok ? 'review-check ok' : 'review-check'} key={check.label}>{check.ok ? <CheckCircle2 size={16} /> : <X size={16} />}<span>{check.label}</span></div>)}{record.submission?.file_path && <button className="secondary" onClick={() => download(record.submission.file_path)}><Download size={16} /> Descargar archivo final</button>}{record.assessment.activityCode === 'MSII-RA-1.1' && record.submission?.file_path && <button className="secondary analyze-doc" disabled={busy === `analysis-${record.submission.id}`} onClick={() => analyzeDocument(record)}><Search size={16} /> {busy === `analysis-${record.submission.id}` ? 'Analizando…' : 'Analizar contenido DOCX'}</button>}{Object.values(record.submission?.answers?.packet_tracer || {}).map(practice => <button className="secondary" key={practice.path} onClick={() => download(practice.path)}><Download size={16} /> {practice.practice}</button>)}</section><section><h3>Apoyo para evaluar</h3><div className="suggested-score"><span>{docAnalysis ? 'Referencia después de analizar el DOCX' : 'Completitud documental estimada'}</span><strong>{suggested}/60</strong><small>Es una referencia. Revise la calidad y el contenido antes de calificar.</small></div>{docAnalysis && <div className="doc-analysis"><div><b>{docAnalysis.completedFields}/{docAnalysis.initialPlaceholders}</b><span>Campos respondidos</span></div><div><b>{docAnalysis.completionPercent}%</b><span>Formato completado</span></div><div><b>{docAnalysis.wordCount}</b><span>Palabras detectadas</span></div><div><b>{docAnalysis.matchingValues}/{docAnalysis.expectedValues}</b><span>Datos asignados presentes</span></div>{docAnalysis.remainingPlaceholders > 0 && <p>Quedaron {docAnalysis.remainingPlaceholders} espacios con “Escribe aquí”. Conviene revisarlos antes de asignar la calificación.</p>}</div>}{record.submission?.answers && Object.keys(record.submission.answers).length > 0 && <details className="individual-answers"><summary><Eye size={16} /> Revisar respuestas</summary><AnswerPreview answers={record.submission.answers} /></details>}</section></div>{record.submission?.submitted_at && <footer><label>Calificación final<input type="number" min="0" max="60" value={scores[record.submission.id] ?? record.submission.score ?? ''} onChange={event => setScores(current => ({ ...current, [record.submission.id]: event.target.value }))} /></label><button className="secondary" onClick={() => setScores(current => ({ ...current, [record.submission.id]: suggested }))}>Usar referencia</button><button className="primary" disabled={busy === record.submission.id} onClick={() => saveScore(record)}>{busy === record.submission.id ? 'Guardando…' : 'Guardar calificación'}</button></footer>}</article> })}</div></section>
}

function SettingsPage({ session, groups }) {
  return <section className="panel page-panel settings-page"><div className="list-toolbar"><div><h1>Configuración</h1><p>Información general de la cuenta y del periodo activo.</p></div></div><div className="settings-grid"><article><span>Cuenta administradora</span><strong>{session.name}</strong><small>{session.email}</small></article><article><span>Periodo escolar</span><strong>Agosto 2026 – Enero 2027</strong><small>Periodo activo</small></article><article><span>Grupos habilitados</span><strong>{groups.map(group => group.code).join(', ')}</strong><small>{groups.length} grupos activos</small></article><article><span>Acceso</span><strong>Administrador</strong><small>Permisos de seguimiento y publicación</small></article></div><div className="info-note">Los cambios de cuenta, grupos y seguridad se administran de forma protegida para evitar modificaciones accidentales.</div></section>
}

function MaterialModal({ groups, onClose, onSave }) {
  const [data, setData] = useState({ title: '', description: '', groupId: groups[0]?.id || '', unit: 'Unidad 1', file: null })
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  async function submit(event) { event.preventDefault(); setBusy(true); setError(''); try { await onSave(data) } catch (err) { setError(err.message || 'No fue posible publicar el material') } finally { setBusy(false) } }
  return <Modal title="Publicar material" onClose={onClose}><form onSubmit={submit}><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre del recurso" /></label><label>Descripción<textarea value={data.description} onChange={e => setData({...data,description:e.target.value})} placeholder="Descripción breve" rows="3" /></label><div className="form-row"><label>Grupo<select required value={data.groupId} onChange={e => setData({...data,groupId:e.target.value})}>{groups.map(group=><option key={group.id} value={group.id}>{group.code}</option>)}</select></label><label>Unidad<input value={data.unit} onChange={e => setData({...data,unit:e.target.value})} /></label></div><label className="upload-zone"><Upload /><strong>{data.file?.name || 'Selecciona un archivo'}</strong><span>PDF, documento o presentación · máximo 20 MB</span><input type="file" accept=".pdf,.docx,.pptx" required onChange={e => setData({...data,file:e.target.files[0]})} /></label>{error && <div className="form-error">{error}</div>}<ModalActions onClose={onClose} label={busy ? 'Publicando…' : 'Publicar'} disabled={busy} /></form></Modal>
}

function AssessmentModal({ groups, onClose, onSave }) {
  const [data, setData] = useState({ title: '', groupId: groups[0]?.id || '', dueAt: '', instructions: '', activityCode: 'ASIN-RA-1.1' })
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  async function submit(event) { event.preventDefault(); setBusy(true); setError(''); try { await onSave(data) } catch (err) { setError(err.message || 'No fue posible crear la evaluación') } finally { setBusy(false) } }
  return <Modal title="Nueva evaluación" onClose={onClose}><form onSubmit={submit}><label>Tipo de actividad<select required value={data.activityCode} onChange={e => setData({...data,activityCode:e.target.value})}><option value="ASIN-RA-1.1">ASIN · Actividad en plataforma</option><option value="MSII-RA-1.1">MSII · Documento DOCX</option></select></label><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre de la evaluación" /></label><div className="form-row"><label>Grupo<select required value={data.groupId} onChange={e => setData({...data,groupId:e.target.value})}>{groups.map(group=><option key={group.id} value={group.id}>{group.code}</option>)}</select></label><label>Fecha límite<input type="datetime-local" required value={data.dueAt} onChange={e => setData({...data,dueAt:e.target.value})} /></label></div><label>Instrucciones<textarea value={data.instructions} onChange={e => setData({...data,instructions:e.target.value})} placeholder="Indicaciones para los alumnos" rows="4" /></label><div className="info-note compact">Solo se muestran tipos de actividad que ya cuentan con un espacio de trabajo funcional para el alumno.</div>{error && <div className="form-error">{error}</div>}<ModalActions onClose={onClose} label={busy ? 'Creando…' : 'Crear evaluación'} disabled={busy} /></form></Modal>
}

function Modal({ title, onClose, children }) { return <div className="modal-backdrop" onMouseDown={e => e.target === e.currentTarget && onClose()}><div className="modal"><header><div><span className="eyebrow">AULA DIGITAL</span><h2>{title}</h2></div><button className="icon-btn" onClick={onClose}><X /></button></header>{children}</div></div> }
function ModalActions({ onClose, label, disabled }) { return <div className="modal-actions"><button type="button" className="secondary" onClick={onClose}>Cancelar</button><button className="primary" disabled={disabled}>{label}</button></div> }
function EmptyState({ text }) { return <div className="empty-state">{text}</div> }
function Stat({ icon: Icon, value, label, note, color }) { return <div className="stat-card"><div className={`stat-icon ${color}`}><Icon size={21} /></div><div><strong>{value}</strong><span>{label}</span><small>{note}</small></div></div> }
function PanelTitle({ title, action, onClick }) { return <div className="panel-title"><h3>{title}</h3>{action && <button className="text-btn" onClick={onClick}>{action}<ChevronRight size={16} /></button>}</div> }
function Activity({ initials, title, meta, color }) { return <div className="activity"><div className={`activity-avatar ${color}`}>{initials}</div><div><strong>{title}</strong><span>{meta}</span></div></div> }

export default App
