import { useEffect, useMemo, useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import {
  Bell, BookOpen, CheckCircle2, ChevronRight, ClipboardCheck, FileText, GraduationCap,
  LayoutDashboard, LogOut, Menu, Plus, Search, Settings, TrendingUp, Upload, Users, X
} from 'lucide-react'
import { isSupabaseReady, supabase } from './lib/supabase'

const navItems = [
  { id: 'inicio', label: 'Resumen', icon: LayoutDashboard },
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
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setError('')
    if (mode === 'student' && !email.toLowerCase().endsWith('@tam.conalep.edu.mx')) {
      setError('Usa tu correo institucional autorizado')
      return
    }
    setBusy(true)
    try {
      if (isSupabaseReady) {
        const result = authMode === 'register'
          ? await supabase.auth.signUp({ email, password, options: { data: { full_name: fullName, enrollment_number: enrollment, role: 'student' } } })
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
        {authMode === 'register' && <><label>Nombre completo<input value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Como aparece en tu expediente" required /></label><label>Matrícula<input value={enrollment} onChange={e => setEnrollment(e.target.value)} placeholder="Tu matrícula institucional" required /></label></>}
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
  const [view, setView] = useState('inicio')
  const [mobileMenu, setMobileMenu] = useState(false)
  const [modal, setModal] = useState(null)
  const [toast, setToast] = useState('')
  const [groupList, setGroupList] = useState([])
  const [studentList, setStudentList] = useState([])
  const [materialList, setMaterialList] = useState([])
  const [assessmentList, setAssessmentList] = useState([])
  const [loading, setLoading] = useState(true)
  const [dataError, setDataError] = useState('')

  async function loadData() {
    setLoading(true); setDataError('')
    try {
      const [groupResult, studentResult, materialResult, assessmentResult] = await Promise.all([
        supabase.from('groups').select('id, code, semester, career').eq('active', true).order('code'),
        isTeacher ? supabase.from('student_directory').select('id, full_name, email, enrollment_number, group_code, active').eq('active', true).order('full_name') : Promise.resolve({ data: [] }),
        supabase.from('materials').select('id, title, description, unit, resource_type, resource_url, created_at, groups(code)').eq('published', true).order('created_at', { ascending: false }),
        supabase.from('assessments').select('id, title, instructions, status, due_at, group_id, groups(code), submissions(score, submitted_at)').order('created_at', { ascending: false }),
      ])
      const firstError = [groupResult, studentResult, materialResult, assessmentResult].find(result => result.error)?.error
      if (firstError) throw firstError
      const directory = studentResult.data || []
      setGroupList((groupResult.data || []).map(group => ({ ...group, students: directory.filter(student => student.group_code === group.code).length })))
      setStudentList(directory.map(student => ({ id: student.id, name: formatPersonName(student.full_name), email: student.email || 'Cuenta pendiente', enrollment: student.enrollment_number, group: student.group_code })))
      setMaterialList((materialResult.data || []).map(material => ({ id: material.id, title: material.title, description: material.description, unit: material.unit || 'Sin unidad', type: material.resource_type === 'file' ? 'Archivo' : material.resource_type, url: material.resource_url, group: material.groups?.code || 'Todos', date: new Date(material.created_at).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) })))
      setAssessmentList((assessmentResult.data || []).map(assessment => {
        const submissions = assessment.submissions || []
        const scored = submissions.filter(item => item.score !== null)
        return { id: assessment.id, title: assessment.title, group: assessment.groups?.code || '—', groupId: assessment.group_id, due: assessment.due_at ? new Date(assessment.due_at).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) : 'Sin fecha', submissions: submissions.filter(item => item.submitted_at).length, total: directory.filter(student => student.group_code === assessment.groups?.code).length, average: scored.length ? Math.round(scored.reduce((sum, item) => sum + Number(item.score), 0) / scored.length) : null, status: assessment.status === 'published' ? 'Activa' : assessment.status === 'closed' ? 'Cerrada' : 'Borrador' }
      }))
    } catch (err) { setDataError(err.message || 'No fue posible cargar la información') }
    finally { setLoading(false) }
  }

  useEffect(() => { if (isSupabaseReady) loadData() }, [])

  function saved(message) { setModal(null); setToast(message); setTimeout(() => setToast(''), 2600) }
  const pageTitle = navItems.find(i => i.id === view)?.label || 'Resumen'

  return <div className="app-shell">
    <aside className={`sidebar ${mobileMenu ? 'open' : ''}`}>
      <div className="side-brand"><GraduationCap size={26} /><span>Aula <b>Virtual</b></span><button className="icon-btn close-menu" onClick={() => setMobileMenu(false)}><X /></button></div>
      <nav>{navItems.filter(i => isTeacher || i.id !== 'alumnos').map(({ id, label, icon: Icon }) =>
        <button key={id} className={view === id ? 'active' : ''} onClick={() => { setView(id); setMobileMenu(false) }}><Icon size={19} />{label}</button>
      )}</nav>
      <div className="side-bottom">
        <button><Settings size={19} />Configuración</button>
        <div className="profile-mini"><div className="avatar">{session.name.slice(0, 2).toUpperCase()}</div><div><strong>{session.name}</strong><small>{profileLabel}</small></div><button className="logout" onClick={onLogout} title="Cerrar sesión"><LogOut size={18} /></button></div>
      </div>
    </aside>
    <div className="main-area">
      <header className="topbar">
        <button className="icon-btn menu-btn" onClick={() => setMobileMenu(true)}><Menu /></button>
        <div><span className="breadcrumb">Aula digital</span><h2>{pageTitle}</h2></div>
        <div className="top-actions"><button className="icon-btn"><Bell size={20} /><span className="notification-dot" /></button>{isTeacher && <button className="primary" onClick={() => setModal(view === 'evaluaciones' ? 'assessment' : 'material')}><Plus size={18} /> {view === 'evaluaciones' ? 'Nueva evaluación' : 'Publicar material'}</button>}</div>
      </header>
      <main className="content">
        {dataError && <div className="form-error data-error">{dataError} <button className="text-btn" onClick={loadData}>Reintentar</button></div>}
        {loading ? <div className="loading-state">Cargando información real…</div> : <>
        {view === 'inicio' && (isTeacher ? <TeacherHome setView={setView} groups={groupList} students={studentList} materials={materialList} assessments={assessmentList} /> : <StudentHome session={session} materials={materialList} assessments={assessmentList} />)}
        {view === 'materiales' && <Materials items={materialList} groups={groupList} isTeacher={isTeacher} onAdd={() => setModal('material')} />}
        {view === 'evaluaciones' && <Assessments items={assessmentList} isTeacher={isTeacher} onAdd={() => setModal('assessment')} />}
        {view === 'alumnos' && isTeacher && <Students students={studentList} groups={groupList} />}
        </>}
      </main>
    </div>
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
      const { error } = await supabase.from('assessments').insert({ teacher_id: authData.user.id, group_id: item.groupId, title: item.title, instructions: item.instructions, status: 'published', due_at: item.dueAt })
      if (error) throw error
      await loadData(); saved('Evaluación creada correctamente')
    }} />}
    {toast && <div className="toast"><CheckCircle2 size={19} />{toast}</div>}
  </div>
}

function TeacherHome({ setView, groups, students, materials, assessments }) {
  const activeAssessments = assessments.filter(item => item.status === 'Activa')
  const submitted = assessments.reduce((sum, item) => sum + item.submissions, 0)
  const scores = assessments.filter(item => item.average !== null).map(item => item.average)
  const overallAverage = scores.length ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : null
  return <>
    <section className="welcome-row"><div><span className="eyebrow">JUEVES, 1 DE OCTUBRE</span><h1>Buenos días, profesor.</h1><p>Esto es lo que sucede hoy con tus grupos.</p></div><div className="term-card"><span>Periodo actual</span><strong>Agosto 2026 – Enero 2027</strong></div></section>
    <section className="stat-grid">
      <Stat icon={Users} value={students.length} label="Alumnos en padrón" note={`${groups.length} grupos`} color="blue" />
      <Stat icon={BookOpen} value={materials.length} label="Materiales publicados" note="Información real" color="gold" />
      <Stat icon={ClipboardCheck} value={activeAssessments.length} label="Evaluaciones activas" note={`${submitted} entregas registradas`} color="purple" />
      <Stat icon={TrendingUp} value={overallAverage === null ? '—' : `${overallAverage}%`} label="Promedio general" note={overallAverage === null ? 'Sin calificaciones' : 'Calculado con entregas'} color="green" />
    </section>
    <section className="two-cols">
      <div className="panel"><PanelTitle title="Actividad reciente" action="Ver alumnos" onClick={() => setView('alumnos')} />
        <EmptyState text="Todavía no hay actividad de alumnos registrada." />
      </div>
      <div className="panel"><PanelTitle title="Avance por grupo" />
        <div className="group-progress">{groups.map(group => <div className="progress-row" key={group.id}><div><strong>Grupo {group.code}</strong><span>{group.students} alumnos · {group.semester}º semestre</span></div><div className="progress-meta"><b>Sin actividad</b><div className="bar"><i style={{ width: '0%' }} /></div></div></div>)}</div>
      </div>
    </section>
    <section className="panel"><PanelTitle title="Evaluaciones activas" action="Ver todas" onClick={() => setView('evaluaciones')} /><AssessmentTable items={activeAssessments} /></section>
  </>
}

function StudentHome({ session, materials, assessments }) {
  const nextAssessment = assessments.find(item => item.status === 'Activa')
  const latestMaterial = materials[0]
  return <>
    <section className="welcome-row"><div><span className="eyebrow">GRUPO {session.group} · {session.semester}º SEMESTRE</span><h1>Hola, {session.name}.</h1><p>Continúa con tus actividades y revisa lo nuevo de tu clase.</p></div><div className="student-score"><span>Tu promedio</span><strong>91</strong><small>Excelente avance</small></div></section>
    <section className="stat-grid student-stats"><Stat icon={BookOpen} value={materials.length} label="Materiales disponibles" note="Información real" color="blue" /><Stat icon={ClipboardCheck} value={assessments.filter(item => item.status === 'Activa').length} label="Evaluaciones activas" note="Revisa las fechas" color="gold" /><Stat icon={TrendingUp} value="—" label="Promedio" note="Sin calificaciones" color="green" /></section>
    <section className="two-cols"><div className="panel"><PanelTitle title="Próxima entrega" />{nextAssessment ? <div className="next-task"><div><span className="tag active">ACTIVA</span><h3>{nextAssessment.title}</h3><p>Entrega: {nextAssessment.due}</p></div></div> : <EmptyState text="No tienes evaluaciones activas." />}</div><div className="panel"><PanelTitle title="Material nuevo" />{latestMaterial ? <div className="featured-material"><div className="file-icon"><FileText /></div><div><h3>{latestMaterial.title}</h3><p>{latestMaterial.type} · {latestMaterial.unit}</p></div></div> : <EmptyState text="Todavía no hay materiales publicados." />}</div></section>
  </>
}

function Materials({ items, groups, isTeacher, onAdd }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(m => m.title.toLowerCase().includes(query.toLowerCase()))
  async function openMaterial(material) {
    if (material.type !== 'Archivo') return window.open(material.url, '_blank', 'noopener,noreferrer')
    const { data, error } = await supabase.storage.from('materials').createSignedUrl(material.url, 300)
    if (!error) window.open(data.signedUrl, '_blank', 'noopener,noreferrer')
  }
  return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Material didáctico</h1><p>Recursos organizados por grupo y unidad.</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Upload size={18} />Publicar material</button>}</div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar material…" /></div><select><option>Todos los grupos</option>{groups.map(group => <option key={group.id}>Grupo {group.code}</option>)}</select></div>{filtered.length ? <div className="card-grid">{filtered.map(m => <article className="material-card" key={m.id}><div className="material-icon"><FileText /></div><span className="tag">{m.unit}</span><h3>{m.title}</h3><p>{m.type} · Grupo {m.group}</p><footer><span>Publicado {m.date}</span><button className="text-btn" onClick={() => openMaterial(m)}>Abrir <ChevronRight size={15} /></button></footer></article>)}</div> : <EmptyState text="Todavía no hay materiales publicados." />}</section>
}

function Assessments({ items, isTeacher, onAdd }) { return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Evaluaciones</h1><p>Actividades y resultados de tus grupos.</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Plus size={18} />Nueva evaluación</button>}</div><AssessmentTable items={items} student={!isTeacher} /></section> }

function AssessmentTable({ items, student }) { if (!items.length) return <EmptyState text="Todavía no hay evaluaciones registradas." />; return <div className="table-wrap"><table><thead><tr><th>Evaluación</th><th>Grupo</th><th>Entrega</th>{!student && <th>Entregas</th>}<th>{student ? 'Estado' : 'Promedio'}</th><th /></tr></thead><tbody>{items.map(a => <tr key={a.id}><td><div className="title-cell"><div className="mini-icon"><ClipboardCheck size={17} /></div><strong>{a.title}</strong></div></td><td>{a.group}</td><td>{a.due}</td>{!student && <td>{a.submissions} / {a.total}</td>}<td>{student ? <span className={`tag ${a.status === 'Activa' ? 'active' : ''}`}>{a.status}</span> : (a.average !== null ? `${a.average}%` : '—')}</td><td><button className="text-btn">{student ? 'Abrir' : 'Resultados'} <ChevronRight size={15} /></button></td></tr>)}</tbody></table></div> }

function Students({ students, groups }) {
  const [query, setQuery] = useState('')
  const [group, setGroup] = useState('Todos')
  const rows = useMemo(() => students.filter(s => (group === 'Todos' || s.group === group) && `${s.name} ${s.email}`.toLowerCase().includes(query.toLowerCase())), [query, group])
  return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Directorio de alumnos</h1><p>Padrón real importado por grupo. El avance aparecerá cuando existan entregas.</p></div></div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar alumno…" /></div><select value={group} onChange={e => setGroup(e.target.value)}><option>Todos</option>{groups.map(item => <option key={item.id}>{item.code}</option>)}</select></div><div className="table-wrap"><table><thead><tr><th>Alumno</th><th>Grupo</th><th>Matrícula</th><th>Cuenta</th><th>Progreso</th><th>Promedio</th></tr></thead><tbody>{rows.map(student => <tr key={student.id}><td><div className="student-cell"><div className="avatar small">{student.name.split(' ').slice(0,2).map(part => part[0]).join('')}</div><div><strong>{student.name}</strong><span>{student.email}</span></div></div></td><td>{student.group}</td><td>{student.enrollment || 'Pendiente'}</td><td>{student.email === 'Cuenta pendiente' ? <span className="pending">Pendiente</span> : 'Registrada'}</td><td>—</td><td>—</td></tr>)}</tbody></table></div></section>
}

function MaterialModal({ groups, onClose, onSave }) {
  const [data, setData] = useState({ title: '', description: '', groupId: groups[0]?.id || '', unit: 'Unidad 1', file: null })
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  async function submit(event) { event.preventDefault(); setBusy(true); setError(''); try { await onSave(data) } catch (err) { setError(err.message || 'No fue posible publicar el material') } finally { setBusy(false) } }
  return <Modal title="Publicar material" onClose={onClose}><form onSubmit={submit}><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre del recurso" /></label><label>Descripción<textarea value={data.description} onChange={e => setData({...data,description:e.target.value})} placeholder="Descripción breve" rows="3" /></label><div className="form-row"><label>Grupo<select required value={data.groupId} onChange={e => setData({...data,groupId:e.target.value})}>{groups.map(group=><option key={group.id} value={group.id}>{group.code}</option>)}</select></label><label>Unidad<input value={data.unit} onChange={e => setData({...data,unit:e.target.value})} /></label></div><label className="upload-zone"><Upload /><strong>{data.file?.name || 'Selecciona un archivo'}</strong><span>PDF, documento o presentación · máximo 20 MB</span><input type="file" accept=".pdf,.docx,.pptx" required onChange={e => setData({...data,file:e.target.files[0]})} /></label>{error && <div className="form-error">{error}</div>}<ModalActions onClose={onClose} label={busy ? 'Publicando…' : 'Publicar'} disabled={busy} /></form></Modal>
}

function AssessmentModal({ groups, onClose, onSave }) {
  const [data, setData] = useState({ title: '', groupId: groups[0]?.id || '', dueAt: '', instructions: '' })
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  async function submit(event) { event.preventDefault(); setBusy(true); setError(''); try { await onSave(data) } catch (err) { setError(err.message || 'No fue posible crear la evaluación') } finally { setBusy(false) } }
  return <Modal title="Nueva evaluación" onClose={onClose}><form onSubmit={submit}><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre de la evaluación" /></label><div className="form-row"><label>Grupo<select required value={data.groupId} onChange={e => setData({...data,groupId:e.target.value})}>{groups.map(group=><option key={group.id} value={group.id}>{group.code}</option>)}</select></label><label>Fecha límite<input type="datetime-local" required value={data.dueAt} onChange={e => setData({...data,dueAt:e.target.value})} /></label></div><label>Instrucciones<textarea value={data.instructions} onChange={e => setData({...data,instructions:e.target.value})} placeholder="Indicaciones para los alumnos" rows="4" /></label>{error && <div className="form-error">{error}</div>}<ModalActions onClose={onClose} label={busy ? 'Creando…' : 'Crear evaluación'} disabled={busy} /></form></Modal>
}

function Modal({ title, onClose, children }) { return <div className="modal-backdrop" onMouseDown={e => e.target === e.currentTarget && onClose()}><div className="modal"><header><div><span className="eyebrow">AULA DIGITAL</span><h2>{title}</h2></div><button className="icon-btn" onClick={onClose}><X /></button></header>{children}</div></div> }
function ModalActions({ onClose, label, disabled }) { return <div className="modal-actions"><button type="button" className="secondary" onClick={onClose}>Cancelar</button><button className="primary" disabled={disabled}>{label}</button></div> }
function EmptyState({ text }) { return <div className="empty-state">{text}</div> }
function Stat({ icon: Icon, value, label, note, color }) { return <div className="stat-card"><div className={`stat-icon ${color}`}><Icon size={21} /></div><div><strong>{value}</strong><span>{label}</span><small>{note}</small></div></div> }
function PanelTitle({ title, action, onClick }) { return <div className="panel-title"><h3>{title}</h3>{action && <button className="text-btn" onClick={onClick}>{action}<ChevronRight size={16} /></button>}</div> }
function Activity({ initials, title, meta, color }) { return <div className="activity"><div className={`activity-avatar ${color}`}>{initials}</div><div><strong>{title}</strong><span>{meta}</span></div></div> }

export default App
