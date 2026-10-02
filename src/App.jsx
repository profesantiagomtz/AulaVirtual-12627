import { useMemo, useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import {
  Bell, BookOpen, CheckCircle2, ChevronRight, ClipboardCheck, FileText, GraduationCap,
  LayoutDashboard, LogOut, Menu, Plus, Search, Settings, TrendingUp, Upload, Users, X
} from 'lucide-react'
import { assessments, groups, materials, students } from './data/demo'
import { isSupabaseReady, supabase } from './lib/supabase'

const navItems = [
  { id: 'inicio', label: 'Resumen', icon: LayoutDashboard },
  { id: 'materiales', label: 'Materiales', icon: BookOpen },
  { id: 'evaluaciones', label: 'Evaluaciones', icon: ClipboardCheck },
  { id: 'alumnos', label: 'Alumnos', icon: Users },
]

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
        const role = data.user?.user_metadata?.role || mode
        const session = { email: data.user.email, role, name: data.user.user_metadata?.full_name || 'Usuario' }
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
  const isTeacher = session.role === 'teacher'
  const [view, setView] = useState('inicio')
  const [mobileMenu, setMobileMenu] = useState(false)
  const [modal, setModal] = useState(null)
  const [toast, setToast] = useState('')
  const [materialList, setMaterialList] = useState(materials)
  const [assessmentList, setAssessmentList] = useState(assessments)

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
        <div className="profile-mini"><div className="avatar">{session.name.slice(0, 2).toUpperCase()}</div><div><strong>{session.name}</strong><small>{isTeacher ? 'Docente' : `Grupo ${session.group}`}</small></div><button className="logout" onClick={onLogout} title="Cerrar sesión"><LogOut size={18} /></button></div>
      </div>
    </aside>
    <div className="main-area">
      <header className="topbar">
        <button className="icon-btn menu-btn" onClick={() => setMobileMenu(true)}><Menu /></button>
        <div><span className="breadcrumb">Aula digital</span><h2>{pageTitle}</h2></div>
        <div className="top-actions"><button className="icon-btn"><Bell size={20} /><span className="notification-dot" /></button>{isTeacher && <button className="primary" onClick={() => setModal(view === 'evaluaciones' ? 'assessment' : 'material')}><Plus size={18} /> {view === 'evaluaciones' ? 'Nueva evaluación' : 'Publicar material'}</button>}</div>
      </header>
      <main className="content">
        {view === 'inicio' && (isTeacher ? <TeacherHome setView={setView} /> : <StudentHome session={session} />)}
        {view === 'materiales' && <Materials items={materialList} isTeacher={isTeacher} onAdd={() => setModal('material')} />}
        {view === 'evaluaciones' && <Assessments items={assessmentList} isTeacher={isTeacher} onAdd={() => setModal('assessment')} />}
        {view === 'alumnos' && isTeacher && <Students />}
      </main>
    </div>
    {mobileMenu && <div className="overlay mobile" onClick={() => setMobileMenu(false)} />}
    {modal === 'material' && <MaterialModal onClose={() => setModal(null)} onSave={(item) => { setMaterialList([{ id: Date.now(), ...item, date: 'Hoy' }, ...materialList]); saved('Material publicado correctamente') }} />}
    {modal === 'assessment' && <AssessmentModal onClose={() => setModal(null)} onSave={(item) => { setAssessmentList([{ id: Date.now(), ...item, submissions: 0, total: groups.find(g => g.id === item.group)?.students || 0, average: 0, status: 'Activa' }, ...assessmentList]); saved('Evaluación creada correctamente') }} />}
    {toast && <div className="toast"><CheckCircle2 size={19} />{toast}</div>}
  </div>
}

function TeacherHome({ setView }) {
  return <>
    <section className="welcome-row"><div><span className="eyebrow">JUEVES, 1 DE OCTUBRE</span><h1>Buenos días, profesor.</h1><p>Esto es lo que sucede hoy con tus grupos.</p></div><div className="term-card"><span>Periodo actual</span><strong>Agosto 2026 – Enero 2027</strong></div></section>
    <section className="stat-grid">
      <Stat icon={Users} value="95" label="Alumnos activos" note="4 grupos" color="blue" />
      <Stat icon={BookOpen} value="12" label="Materiales publicados" note="+3 este mes" color="gold" />
      <Stat icon={ClipboardCheck} value="2" label="Evaluaciones activas" note="35 pendientes" color="purple" />
      <Stat icon={TrendingUp} value="84%" label="Promedio general" note="+4% vs. mes anterior" color="green" />
    </section>
    <section className="two-cols">
      <div className="panel"><PanelTitle title="Actividad reciente" action="Ver alumnos" onClick={() => setView('alumnos')} />
        <div className="activity-list">
          <Activity initials="A1" title="Un alumno entregó el diagnóstico de pensamiento matemático" meta="Grupo 111 · Hace 18 min" color="navy" />
          <Activity initials="A2" title="Un alumno obtuvo 68 en la actividad R.A. 1.1" meta="Grupo 310 · Hace 1 h" color="amber" />
          <Activity initials="A3" title="Un alumno consultó el material de documentos digitales" meta="Grupo 311 · Hace 2 h" color="teal" />
          <Activity initials="A4" title="Un alumno inició la actividad de redes" meta="Grupo 511 · Hace 3 h" color="purple" />
        </div>
      </div>
      <div className="panel"><PanelTitle title="Avance por grupo" />
        <div className="group-progress">{groups.map((g, i) => { const progress = [86, 72, 81, 91][i]; return <div className="progress-row" key={g.id}><div><strong>Grupo {g.name}</strong><span>{g.students} alumnos · {g.semester}º semestre</span></div><div className="progress-meta"><b>{progress}%</b><div className="bar"><i style={{ width: `${progress}%` }} /></div></div></div> })}</div>
      </div>
    </section>
    <section className="panel"><PanelTitle title="Evaluaciones activas" action="Ver todas" onClick={() => setView('evaluaciones')} /><AssessmentTable items={assessments.filter(a => a.status === 'Activa')} /></section>
  </>
}

function StudentHome({ session }) {
  return <>
    <section className="welcome-row"><div><span className="eyebrow">GRUPO {session.group} · {session.semester}º SEMESTRE</span><h1>Hola, {session.name}.</h1><p>Continúa con tus actividades y revisa lo nuevo de tu clase.</p></div><div className="student-score"><span>Tu promedio</span><strong>91</strong><small>Excelente avance</small></div></section>
    <section className="stat-grid student-stats"><Stat icon={BookOpen} value="8" label="Materiales revisados" note="2 nuevos" color="blue" /><Stat icon={ClipboardCheck} value="1" label="Actividad pendiente" note="Entrega 4 de octubre" color="gold" /><Stat icon={TrendingUp} value="92%" label="Progreso del curso" note="Vas al corriente" color="green" /></section>
    <section className="two-cols"><div className="panel"><PanelTitle title="Próxima entrega" /><div className="next-task"><div className="date-box"><b>04</b><span>OCT</span></div><div><span className="tag active">ACTIVA</span><h3>Diagnóstico de pensamiento matemático</h3><p>10 preguntas · 20 minutos</p><button className="primary">Comenzar evaluación</button></div></div></div><div className="panel"><PanelTitle title="Material nuevo" /><div className="featured-material"><div className="file-icon"><FileText /></div><div><h3>Pensamiento aritmético</h3><p>PDF · Unidad 1</p><button className="text-btn">Abrir material <ChevronRight size={16} /></button></div></div></div></section>
  </>
}

function Materials({ items, isTeacher, onAdd }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(m => m.title.toLowerCase().includes(query.toLowerCase()))
  return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Material didáctico</h1><p>Recursos organizados por grupo y unidad.</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Upload size={18} />Publicar material</button>}</div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar material…" /></div><select><option>Todos los grupos</option>{groups.map(g => <option key={g.id}>Grupo {g.id}</option>)}</select></div><div className="card-grid">{filtered.map(m => <article className="material-card" key={m.id}><div className="material-icon"><FileText /></div><span className="tag">{m.unit}</span><h3>{m.title}</h3><p>{m.type} · Grupo {m.group}</p><footer><span>Publicado {m.date}</span><button className="text-btn">Abrir <ChevronRight size={15} /></button></footer></article>)}</div></section>
}

function Assessments({ items, isTeacher, onAdd }) { return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Evaluaciones</h1><p>Actividades y resultados de tus grupos.</p></div>{isTeacher && <button className="primary" onClick={onAdd}><Plus size={18} />Nueva evaluación</button>}</div><AssessmentTable items={items} student={!isTeacher} /></section> }

function AssessmentTable({ items, student }) { return <div className="table-wrap"><table><thead><tr><th>Evaluación</th><th>Grupo</th><th>Entrega</th>{!student && <th>Entregas</th>}<th>{student ? 'Estado' : 'Promedio'}</th><th /></tr></thead><tbody>{items.map(a => <tr key={a.id}><td><div className="title-cell"><div className="mini-icon"><ClipboardCheck size={17} /></div><strong>{a.title}</strong></div></td><td>{a.group}</td><td>{a.due}</td>{!student && <td>{a.submissions} / {a.total}</td>}<td>{student ? <span className={`tag ${a.status === 'Activa' ? 'active' : ''}`}>{a.status}</span> : (a.average ? `${a.average}%` : '—')}</td><td><button className="text-btn">{student ? 'Abrir' : 'Resultados'} <ChevronRight size={15} /></button></td></tr>)}</tbody></table></div> }

function Students() {
  const [query, setQuery] = useState('')
  const [group, setGroup] = useState('Todos')
  const rows = useMemo(() => students.filter(s => (group === 'Todos' || s.group === group) && `${s.name} ${s.email}`.toLowerCase().includes(query.toLowerCase())), [query, group])
  return <section className="panel page-panel"><div className="list-toolbar"><div><h1>Seguimiento de alumnos</h1><p>Consulta el avance, resultados y actividades pendientes.</p></div><button className="secondary">Descargar reporte</button></div><div className="filters"><div className="search"><Search size={18} /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar alumno…" /></div><select value={group} onChange={e => setGroup(e.target.value)}><option>Todos</option>{groups.map(g => <option key={g.id}>{g.id}</option>)}</select></div><div className="table-wrap"><table><thead><tr><th>Alumno</th><th>Grupo</th><th>Progreso</th><th>Promedio</th><th>Pendientes</th><th /></tr></thead><tbody>{rows.map(s => <tr key={s.id}><td><div className="student-cell"><div className="avatar small">{s.name.split(' ').slice(0,2).map(x => x[0]).join('')}</div><div><strong>{s.name}</strong><span>{s.email}</span></div></div></td><td>{s.group}</td><td><div className="inline-progress"><div className="bar"><i style={{ width: `${s.progress}%` }} /></div><span>{s.progress}%</span></div></td><td><b className={s.average < 70 ? 'low-score' : ''}>{s.average}</b></td><td>{s.pending ? <span className="pending">{s.pending}</span> : '—'}</td><td><button className="text-btn">Ver perfil <ChevronRight size={15} /></button></td></tr>)}</tbody></table></div></section>
}

function MaterialModal({ onClose, onSave }) { const [data, setData] = useState({ title: '', type: 'PDF', group: '111', unit: 'Unidad 1' }); return <Modal title="Publicar material" onClose={onClose}><form onSubmit={e => { e.preventDefault(); onSave(data) }}><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre del recurso" /></label><div className="form-row"><label>Tipo<select value={data.type} onChange={e => setData({...data,type:e.target.value})}><option>PDF</option><option>Presentación</option><option>Video</option><option>Enlace</option></select></label><label>Grupo<select value={data.group} onChange={e => setData({...data,group:e.target.value})}>{groups.map(g=><option key={g.id}>{g.id}</option>)}</select></label></div><label>Unidad<input value={data.unit} onChange={e => setData({...data,unit:e.target.value})} /></label><div className="upload-zone"><Upload /><strong>Selecciona un archivo</strong><span>PDF, documento o presentación · máximo 20 MB</span></div><ModalActions onClose={onClose} label="Publicar" /></form></Modal> }

function AssessmentModal({ onClose, onSave }) { const [data, setData] = useState({ title: '', group: '111', due: '08 oct' }); return <Modal title="Nueva evaluación" onClose={onClose}><form onSubmit={e => { e.preventDefault(); onSave(data) }}><label>Título<input required value={data.title} onChange={e => setData({...data,title:e.target.value})} placeholder="Nombre de la evaluación" /></label><div className="form-row"><label>Grupo<select value={data.group} onChange={e => setData({...data,group:e.target.value})}>{groups.map(g=><option key={g.id}>{g.id}</option>)}</select></label><label>Fecha límite<input type="date" required onChange={e => setData({...data,due: new Date(`${e.target.value}T12:00`).toLocaleDateString('es-MX',{day:'2-digit',month:'short'})})} /></label></div><label>Instrucciones<textarea placeholder="Indicaciones para los alumnos" rows="4" /></label><ModalActions onClose={onClose} label="Crear evaluación" /></form></Modal> }

function Modal({ title, onClose, children }) { return <div className="modal-backdrop" onMouseDown={e => e.target === e.currentTarget && onClose()}><div className="modal"><header><div><span className="eyebrow">AULA DIGITAL</span><h2>{title}</h2></div><button className="icon-btn" onClick={onClose}><X /></button></header>{children}</div></div> }
function ModalActions({ onClose, label }) { return <div className="modal-actions"><button type="button" className="secondary" onClick={onClose}>Cancelar</button><button className="primary">{label}</button></div> }
function Stat({ icon: Icon, value, label, note, color }) { return <div className="stat-card"><div className={`stat-icon ${color}`}><Icon size={21} /></div><div><strong>{value}</strong><span>{label}</span><small>{note}</small></div></div> }
function PanelTitle({ title, action, onClick }) { return <div className="panel-title"><h3>{title}</h3>{action && <button className="text-btn" onClick={onClick}>{action}<ChevronRight size={16} /></button>}</div> }
function Activity({ initials, title, meta, color }) { return <div className="activity"><div className={`activity-avatar ${color}`}>{initials}</div><div><strong>{title}</strong><span>{meta}</span></div></div> }

export default App
