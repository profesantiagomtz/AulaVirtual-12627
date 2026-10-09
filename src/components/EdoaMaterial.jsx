import { useEffect, useMemo, useState } from 'react'
import JSZip from 'jszip'
import { ArrowLeft, BookOpen, CheckCircle2, ChevronLeft, ChevronRight, Download, FileText, LockKeyhole, ShieldCheck, Upload } from 'lucide-react'
import { supabase } from '../lib/supabase'

const cards = [
  { icon: '🖥️', title: 'Conoce la interfaz de Word', intro: 'Antes de editar, ubica las zonas principales de Word 2019.', notes: [['Barra de título', 'Muestra el nombre del documento.'], ['Acceso rápido', 'Contiene Guardar, Deshacer y Rehacer.'], ['Pestañas', 'Agrupan los comandos por tipo de trabajo.'], ['Cinta de opciones', 'Muestra los botones de la pestaña activa.'], ['Regla', 'Ayuda a controlar márgenes y sangrías.'], ['Área de trabajo', 'Es la hoja donde escribes.'], ['Barra de estado', 'Muestra página, palabras y zoom.']], question: '¿En qué parte aparecen los botones de la pestaña activa?', options: ['Cinta de opciones', 'Barra de estado', 'Regla'], answer: 'Cinta de opciones' },
  { icon: '📐', title: 'Diseño de página', intro: 'Configura la hoja antes de comenzar a escribir.', notes: [['Márgenes', 'Espacio en blanco alrededor del texto. Ruta: Disposición › Márgenes.'], ['Orientación', 'Cambia la hoja entre vertical y horizontal.'], ['Tamaño', 'Selecciona Carta, A4 u Oficio.'], ['Encabezado y pie', 'Texto que se repite arriba o abajo. Ruta: Insertar.'], ['Color de página', 'Cambia el fondo desde la pestaña Diseño.']], question: '¿Qué opción cambia la hoja entre vertical y horizontal?', options: ['Orientación', 'Márgenes', 'Interlineado'], answer: 'Orientación' },
  { icon: '🔤', title: 'Formato de texto y párrafo', intro: 'La pestaña Inicio contiene los grupos Fuente y Párrafo.', notes: [['Fuente', 'Negrita, cursiva, subrayado, tamaño y color.'], ['Alineación izquierda', 'Los renglones comienzan en el margen izquierdo.'], ['Centrada', 'El texto queda equilibrado respecto al centro.'], ['Derecha', 'Los renglones terminan en el margen derecho.'], ['Justificada', 'El texto se alinea en ambos márgenes.'], ['Interlineado y sangría', 'Controlan el espacio entre renglones y la entrada del párrafo.']], question: '¿Qué alineación deja rectos ambos márgenes?', options: ['Justificada', 'Centrada', 'Derecha'], answer: 'Justificada' },
  { icon: '🖱️', title: 'Iconos y atajos esenciales', intro: 'Reconocer los botones y atajos te permite trabajar con mayor rapidez.', notes: [['Ctrl+C', 'Copia el contenido seleccionado.'], ['Ctrl+X', 'Corta: quita el contenido y lo guarda temporalmente.'], ['Ctrl+V', 'Pega lo copiado o cortado.'], ['Ctrl+Z', 'Deshace el último cambio.'], ['Ctrl+G', 'Guarda el documento.'], ['Ctrl+E', 'Selecciona todo el documento.']], question: '¿Qué diferencia principal existe entre copiar y cortar?', options: ['Cortar quita el original', 'Copiar elimina el original', 'No existe diferencia'], answer: 'Cortar quita el original' },
  { icon: '💾', title: 'Plantillas, respaldo y tipos de archivo', intro: 'El tipo de archivo determina cómo podrás reutilizar o compartir el documento.', notes: [['.docx', 'Documento actual y editable de Word.'], ['.dotx', 'Plantilla reutilizable.'], ['.pdf', 'Formato para compartir sin facilitar la edición.'], ['.doc', 'Documento de versiones antiguas de Word.'], ['.txt', 'Texto sin formato.'], ['Respaldo', 'Guarda una copia adicional antes de hacer cambios importantes.']], question: '¿Qué extensión corresponde a una plantilla reutilizable?', options: ['.dotx', '.docx', '.txt'], answer: '.dotx' },
  { icon: '📄', title: 'Formato APA del documento', intro: 'Estos ajustes corresponden a APA 7.ª edición.', notes: [['Márgenes', '2.54 cm en cada lado.'], ['Fuente', 'Times New Roman 12 o Calibri 11.'], ['Interlineado', 'Doble en el documento.'], ['Sangría', 'Primera línea de cada párrafo a 1.27 cm.'], ['Número de página', 'En la parte superior derecha.']], question: '¿Cuál es el margen indicado por APA?', options: ['2.54 cm', '1 cm', '5 cm'], answer: '2.54 cm' },
  { icon: '🔎', title: 'Cita y referencia', intro: 'Una fuente se reconoce dentro del texto y también en la lista final.', notes: [['Cita parentética', '(Cuartero, 2016).'], ['Cita narrativa', 'Cuartero (2016).'], ['Dos autores', '(Alfie & Veloso, 2011).'], ['Tres o más', '(Gómez et al., 2020).'], ['Referencia de libro', 'Autor. (Año). Título. Editorial.'], ['Lista final', 'Orden alfabético y sangría francesa.']], question: '¿Cuál cita corresponde a tres o más autores?', options: ['(Gómez et al., 2020)', '(Gómez, 2020)', 'Gómez y todos (2020)'], answer: '(Gómez et al., 2020)' },
  { icon: '🛠️', title: 'Antes de comenzar las prácticas', intro: 'Repasa el orden correcto para preparar un documento del R.A. 1.1.', notes: [['1. Configura la página', 'Define tamaño, orientación y márgenes antes de capturar el contenido.'], ['2. Escribe y organiza', 'Captura el texto y separa las ideas en párrafos.'], ['3. Aplica formato', 'Utiliza fuente, estilos, alineación, interlineado y sangría según las instrucciones.'], ['4. Revisa', 'Corrige ortografía y confirma que el documento sea fácil de leer.'], ['5. Guarda y respalda', 'Conserva el archivo .docx y crea una copia de seguridad.']], question: '¿Qué conviene hacer antes de empezar a capturar el contenido?', options: ['Configurar la página', 'Imprimir el documento', 'Cerrar Word'], answer: 'Configurar la página' },
]

const practices = [
  { code: 'practice-1', title: 'Práctica 1  Reconocimiento de la interfaz', file: 'EDOA_RA11_Practica_1_Interfaz.docx', description: 'Identifica dónde se encuentra y para qué sirve cada elemento de Word.', rule: 'interfaz' },
  { code: 'practice-2', title: 'Práctica 2  Diseño de página', file: 'EDOA_RA11_Practica_2_Diseno_pagina.docx', description: 'Configura tamaño, orientación, márgenes, encabezado y pie de página.', rule: 'pagina' },
  { code: 'practice-3', title: 'Práctica 3  Texto y párrafo', file: 'EDOA_RA11_Practica_3_Texto_parrafo.docx', description: 'Aplica fuente, estilos, color, alineación, interlineado y sangría.', rule: 'formato' },
  { code: 'practice-4', title: 'Práctica 4  Edición y listas', file: 'EDOA_RA11_Practica_4_Edicion_listas.docx', description: 'Ordena información, crea listas y utiliza Buscar y reemplazar.', rule: 'listas' },
  { code: 'practice-5', title: 'Práctica 5  Integradora del R.A. 1.1', file: 'EDOA_RA11_Practica_5_Integradora.docx', description: 'Entrega un documento completo con diseño, formato, estilos y respaldo.', rule: 'integradora' },
]

const archivedCardIndexes = [0]
const archivedPracticeCodes = ['practice-1']

const interfaceParts = [
  ['Barra de título', 'Nombre del documento'], ['Acceso rápido', 'Guardar, deshacer y rehacer'],
  ['Pestañas', 'Agrupan los comandos'], ['Cinta de opciones', 'Botones de la pestaña activa'],
  ['Regla', 'Márgenes y sangrías'], ['Área de trabajo', 'La hoja donde escribes'],
  ['Barra de estado', 'Página, palabras y zoom'],
]

function NumberBadge({ children }) { return <span className="word-number">{children}</span> }

function WordInterfaceGraphic() {
  return <div className="word-interface-visual" role="img" aria-label="Ventana de Word 2019 con siete partes numeradas">
    <div className="word-title"><NumberBadge>1</NumberBadge><span><NumberBadge>2</NumberBadge> 💾 ↶ ↷ &nbsp; Documento1 - Word</span><span>— ▢ ✕</span></div>
    <div className="word-tabs"><NumberBadge>3</NumberBadge><b>Inicio</b><span>Insertar</span><span>Diseño</span><span>Disposición</span><span>Revisar</span></div>
    <div className="word-ribbon"><NumberBadge>4</NumberBadge><span>📋<small>Portapapeles</small></span><span><b>N</b> <i>K</i> <u>S</u><small>Fuente</small></span><span>☰<small>Párrafo</small></span></div>
    <div className="word-ruler"><NumberBadge>5</NumberBadge><span>1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10</span></div>
    <div className="word-canvas"><NumberBadge>6</NumberBadge><div><strong>Aquí escribes tu texto</strong><i></i><i></i><i></i></div></div>
    <div className="word-status"><NumberBadge>7</NumberBadge><span>Página 1 de 1 · 0 palabras</span><span>− &nbsp; 100% &nbsp; +</span></div>
  </div>
}

function AlignmentLines({ type }) {
  const widths = type === 'Justificada' ? [100, 100, 100, 100] : [100, 72, 88, 58]
  return <div className={`alignment-lines ${type.toLowerCase()}`}>{widths.map((width, index) => <i style={{ width: `${width}%` }} key={index} />)}</div>
}

function TopicVisual({ page }) {
  if (page === 0) return <div className="edoa-visual"><WordInterfaceGraphic /><div className="word-legend">{interfaceParts.map(([name, description], index) => <div key={name}><NumberBadge>{index + 1}</NumberBadge><span><b>{name}</b><small>{description}</small></span></div>)}</div><p className="visual-tip">💡 Las pestañas agrupan los comandos y la cinta muestra sus botones.</p></div>
  if (page === 1) return <div className="edoa-visual visual-grid three"><div><span className="paper vertical"><i /></span><b>Márgenes</b><small>Espacio alrededor</small></div><div><span className="paper-pair"><i /><i /></span><b>Orientación</b><small>Vertical u horizontal</small></div><div><span className="paper-pair sizes"><i /><i /></span><b>Tamaño</b><small>Carta, A4 u Oficio</small></div></div>
  if (page === 2) return <div className="edoa-visual visual-grid four">{['Izquierda', 'Centrada', 'Derecha', 'Justificada'].map(type => <div key={type}><AlignmentLines type={type} /><b>{type}</b></div>)}</div>
  if (page === 3) return <div className="edoa-visual shortcut-visual">{[['Ctrl+C', 'Copiar'], ['Ctrl+X', 'Cortar'], ['Ctrl+V', 'Pegar'], ['Ctrl+Z', 'Deshacer'], ['Ctrl+G', 'Guardar'], ['Ctrl+E', 'Seleccionar todo']].map(([key, action]) => <div key={key}><kbd>{key}</kbd><span>{action}</span></div>)}</div>
  if (page === 4) return <div className="edoa-visual visual-grid file-types">{[['.docx', 'Documento'], ['.dotx', 'Plantilla'], ['.pdf', 'Compartir'], ['.doc', 'Word antiguo'], ['.txt', 'Texto simple']].map(([extension, use]) => <div key={extension}><strong>{extension}</strong><small>{use}</small></div>)}</div>
  if (page === 5) return <div className="edoa-visual apa-visual"><div className="apa-page"><span>2.54 cm</span><div><b>Título del trabajo</b><i /><i /><i /><i /></div></div><div className="apa-labels"><span>↔ Márgenes 2.54 cm</span><span>🔤 Fuente legible</span><span>☰ Interlineado doble</span><span>↳ Sangría 1.27 cm</span></div></div>
  if (page === 6) return <div className="edoa-visual reference-visual"><p><span className="author">Cuartero, J.</span> <span className="year">(2016).</span> <span className="title"><i>Word 2016 manual práctico paso a paso.</i></span> <span className="publisher">Alfaomega.</span></p><div><span className="author">Autor</span><span className="year">Año</span><span className="title">Título</span><span className="publisher">Editorial</span></div></div>
  return <div className="edoa-visual workflow-visual">{['Configura', 'Escribe', 'Da formato', 'Revisa', 'Guarda'].map((step, index) => <div key={step}><NumberBadge>{index + 1}</NumberBadge><b>{step}</b>{index < 4 && <span>→</span>}</div>)}</div>
}

async function analyzePractice(file, practice) {
  if (!file.name.toLowerCase().endsWith('.docx')) throw new Error('Selecciona el archivo DOCX que trabajaste en Word.')
  const zip = await JSZip.loadAsync(file)
  const documentXml = await zip.file('word/document.xml')?.async('text')
  if (!documentXml) throw new Error('El archivo no parece ser un documento válido de Word.')
  const headerFiles = Object.keys(zip.files).filter(name => /^word\/header\d+\.xml$/.test(name))
  const footerFiles = Object.keys(zip.files).filter(name => /^word\/footer\d+\.xml$/.test(name))
  const plain = documentXml.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ')
  const placeholderCount = (plain.match(/Escribe aquí/gi) || []).length
  const checks = []
  if (practice.rule === 'interfaz') checks.push({ label: 'Completó las 18 explicaciones de la interfaz', ok: placeholderCount === 0 })
  if (practice.rule === 'pagina') {
    checks.push({ label: 'Agregó encabezado', ok: headerFiles.length > 0 }, { label: 'Agregó pie de página', ok: footerFiles.length > 0 }, { label: 'Configuró márgenes cercanos a 2.54 cm', ok: /w:top="1(?:3|4|5)\d{2}"/.test(documentXml) && /w:left="1(?:3|4|5)\d{2}"/.test(documentXml) }, { label: 'Escribió la evidencia solicitada', ok: placeholderCount === 0 })
  }
  if (practice.rule === 'formato') checks.push({ label: 'Aplicó negrita', ok: /<w:b\/?/.test(documentXml) }, { label: 'Aplicó cursiva', ok: /<w:i\/?/.test(documentXml) }, { label: 'Utilizó alineación centrada', ok: /w:val="center"/.test(documentXml) }, { label: 'Utilizó texto justificado', ok: /w:val="both"/.test(documentXml) }, { label: 'Aplicó sangría o interlineado', ok: /w:firstLine=|w:line=/.test(documentXml) })
  if (practice.rule === 'listas') {
    const numberingXml = await zip.file('word/numbering.xml')?.async('text') || ''
    checks.push({ label: 'Creó listas reales de Word', ok: numberingXml.length > 0 && (documentXml.match(/<w:numPr>/g) || []).length >= 2 }, { label: 'Realizó la edición solicitada', ok: (plain.match(/\barchivo\b/gi) || []).length <= 2 })
  }
  if (practice.rule === 'integradora') checks.push({ label: 'Agregó encabezado', ok: headerFiles.length > 0 }, { label: 'Aplicó estilos de título', ok: /w:val="(?:Title|Heading1|Heading2|T.tulo|T.tulo1|T.tulo2)"/i.test(documentXml) }, { label: 'Aplicó texto justificado', ok: /w:val="both"/.test(documentXml) }, { label: 'Completó la conclusión', ok: placeholderCount === 0 })
  return { checks, passed: checks.length > 0 && checks.every(check => check.ok) }
}

export default function EdoaMaterial({ session, onBack, onProgressUpdate }) {
  const code = 'EDOA-WORD-U1'
  const activeCardIndexes = cards.map((_, index) => index).filter(index => !archivedCardIndexes.includes(index))
  const activePractices = practices.filter(practice => !archivedPracticeCodes.includes(practice.code))
  const [page, setPage] = useState(activeCardIndexes[0])
  const [completed, setCompleted] = useState([])
  const [answer, setAnswer] = useState('')
  const [message, setMessage] = useState('')
  const [practiceReviews, setPracticeReviews] = useState({})
  const [busy, setBusy] = useState('')
  const [view, setView] = useState('learn')
  const current = cards[page]
  const completedActiveSteps = completed.filter(step => step !== 'card-0' && !archivedPracticeCodes.includes(step))
  const totalSteps = activeCardIndexes.length + activePractices.length
  const percent = Math.round(completedActiveSteps.length / totalSteps * 100)
  const done = completed.includes(`card-${page}`)

  useEffect(() => {
    if (session.preview) return
    supabase.from('learning_progress').select('completed_steps').eq('material_code', code).maybeSingle().then(({ data }) => {
      const stored = data?.completed_steps || []
      setCompleted(stored.map(step => Number.isInteger(step) ? `card-${step}` : step))
    })
  }, [session.preview])

  useEffect(() => { setAnswer(''); setMessage('') }, [page])

  async function saveProgress(next) {
    const activeCompletedCount = next.filter(step => step !== 'card-0' && !archivedPracticeCodes.includes(step)).length
    const progress = { material_code: code, completed_steps: next, completed_at: activeCompletedCount >= totalSteps ? new Date().toISOString() : null }
    setCompleted(next); onProgressUpdate?.(progress)
    if (!session.preview) await supabase.from('learning_progress').upsert({ student_id: session.id, ...progress }, { onConflict: 'student_id,material_code' })
  }

  async function completeCard() {
    if (answer !== current.answer) { setMessage('Todavía no es correcto. Revisa la ficha y vuelve a intentarlo.'); return }
    const next = [...new Set([...completed, `card-${page}`])]
    setMessage('¡Correcto! Ficha completada.'); await saveProgress(next)
  }

  async function submitPractice(practice, file) {
    if (!file) return
    setBusy(practice.code); setMessage('')
    try {
      const review = await analyzePractice(file, practice)
      setPracticeReviews(currentReviews => ({ ...currentReviews, [practice.code]: review }))
      if (!review.passed) throw new Error('El documento todavía no cumple todos los puntos. Corrígelo en Word y vuelve a subirlo.')
      if (!session.preview) {
        const path = `${session.id}/edoa/${practice.code}/${file.name}`
        const { error: uploadError } = await supabase.storage.from('submissions').upload(path, file, { upsert: true, contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
        if (uploadError) throw uploadError
        const { error } = await supabase.from('edoa_practice_submissions').upsert({ student_id: session.id, practice_code: practice.code, file_path: path, original_filename: file.name, analysis: review, submitted_at: new Date().toISOString() }, { onConflict: 'student_id,practice_code' })
        if (error) throw error
      }
      await saveProgress([...new Set([...completed, practice.code])])
      setMessage('¡Práctica revisada y entregada correctamente!')
    } catch (error) { setMessage(error.message || 'No fue posible revisar la práctica.') }
    finally { setBusy('') }
  }

  const status = useMemo(() => cards.map((_, index) => completed.includes(`card-${index}`)), [completed])
  const activeStatus = activeCardIndexes.map(index => status[index])
  const completedLessons = activeStatus.filter(Boolean).length
  const completedPractices = activePractices.filter(practice => completed.includes(practice.code)).length
  const pagePosition = activeCardIndexes.indexOf(page)
  return <section className="panel page-panel edoa-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="edoa-hero"><div><span className="eyebrow">EDOA · UNIDAD 1 · R.A. 1.1</span><h1>Diseño y formato de documentos</h1><p>Domina Word 2019 con explicaciones visuales y prácticas guiadas.</p><div className="edoa-hero-meta"><span><BookOpen size={15} /> {completedLessons} de {activeCardIndexes.length} temas</span><span><FileText size={15} /> {completedPractices} de {activePractices.length} prácticas</span></div></div><div className="edoa-progress"><strong>{percent}%</strong><span>AVANCE GENERAL</span><i><b style={{ width: `${percent}%` }} /></i></div></div>
    <div className="edoa-archived-section"><LockKeyhole size={18} /><div><strong>A) Identificación de los elementos del procesador de textos</strong><span>Contenido concluido y cerrado por el docente.</span></div><b>FINALIZADO</b></div>
    <nav className="edoa-view-tabs" aria-label="Secciones del material"><button className={view === 'learn' ? 'active' : ''} onClick={() => setView('learn')}><BookOpen size={18} /><span><b>1. Aprende</b><small>Teoría y ejemplos visuales</small></span></button><button className={view === 'practice' ? 'active' : ''} onClick={() => setView('practice')}><FileText size={18} /><span><b>2. Practica</b><small>Documentos para trabajar en Word</small></span></button></nav>
    {view === 'learn' && <div className="edoa-learning-layout"><aside className="edoa-topic-nav"><div><span>CONTENIDO DISPONIBLE</span><strong>{completedLessons}/{activeCardIndexes.length} temas completados</strong></div>{activeCardIndexes.map((cardIndex, position) => { const card = cards[cardIndex]; return <button className={cardIndex === page ? 'active' : status[cardIndex] ? 'done' : ''} key={card.title} onClick={() => setPage(cardIndex)}><span>{status[cardIndex] ? <CheckCircle2 size={17} /> : position + 1}</span><div><small>TEMA {position + 1}</small><b>{card.title}</b></div></button> })}</aside><main className="edoa-lesson">
    <article className="edoa-card">
      <header><div className="edoa-card-icon">{current.icon}</div><div><small>FICHA {pagePosition + 1} DE {activeCardIndexes.length}</small><h2>{current.title}</h2></div></header>
      <p className="edoa-intro">{current.intro}</p>
      <TopicVisual page={page} />
      <div className="edoa-notes">{current.notes.map(([title, text]) => <div key={title}><strong>{title}</strong><p>{text}</p></div>)}</div>
      <section className="edoa-check"><span>COMPRUEBA LO APRENDIDO</span><h3>{current.question}</h3><div>{current.options.map(option => <label key={option}><input type="radio" name={`edoa-${page}`} checked={answer === option} disabled={done} onChange={() => setAnswer(option)} />{option}</label>)}</div><button className="primary" disabled={done || !answer} onClick={completeCard}>{done ? 'Ficha completada' : 'Revisar respuesta'}</button>{message && <p className={message.startsWith('¡') ? 'correct-feedback' : 'wrong-feedback'}>{message}</p>}</section>
    </article>
    <div className="edoa-nav"><button className="secondary" disabled={pagePosition === 0} onClick={() => setPage(activeCardIndexes[pagePosition - 1])}><ChevronLeft size={17} />Anterior</button><span>{pagePosition + 1} / {activeCardIndexes.length}</span><button className="secondary" disabled={pagePosition === activeCardIndexes.length - 1} onClick={() => setPage(activeCardIndexes[pagePosition + 1])}>Siguiente<ChevronRight size={17} /></button></div>
    </main></div>}
    {view === 'practice' && <section className="edoa-practices"><div className="edoa-practice-heading"><div><span className="eyebrow">R.A. 1.1 · PRÁCTICAS GUIADAS</span><h2>Aplica lo aprendido en Word</h2><p>Trabaja en orden: descarga el documento, completa las instrucciones y sube el mismo archivo.</p></div><div><strong>{completedPractices}/{activePractices.length}</strong><span>ENTREGADAS</span></div></div>{activePractices.map((practice, index) => { const requiredCards = index === activePractices.length - 1 ? activeCardIndexes.length : Math.min(activeCardIndexes.length, index * 2 + 3); const available = session.preview || activeStatus.slice(0, requiredCards).every(Boolean); const delivered = completed.includes(practice.code); const review = practiceReviews[practice.code]; return <article className={delivered ? 'practice-complete' : !available ? 'practice-locked' : ''} key={practice.code}><header><span>{delivered ? <CheckCircle2 size={18} /> : !available ? <LockKeyhole size={16} /> : index + 1}</span><div><small>{delivered ? 'COMPLETADA' : available ? 'DISPONIBLE' : `SE DESBLOQUEA AL TERMINAR ${requiredCards} TEMAS`}</small><h3>{practice.title.replace(/^Práctica \d+\s+/, `Práctica ${index + 1} · `)}</h3><p>{practice.description}</p></div></header><div className="edoa-practice-actions"><a className={`secondary ${!available ? 'disabled' : ''}`} href={available ? `${import.meta.env.BASE_URL}materials/edoa/${practice.file}` : undefined} download><Download size={16} />Descargar DOCX</a><label className={!available || delivered ? 'disabled' : ''}><Upload size={16} /><span>{delivered ? 'Documento entregado' : busy === practice.code ? 'Revisando…' : 'Subir documento terminado'}</span><input type="file" accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document" disabled={!available || delivered || busy === practice.code} onChange={event => submitPractice(practice, event.target.files?.[0])} /></label></div>{!available && <small>Continúa en la sección Aprende para desbloquear esta práctica.</small>}{review && <div className="edoa-review">{review.checks.map(check => <span className={check.ok ? 'ok' : 'bad'} key={check.label}>{check.ok ? '✓' : '×'} {check.label}</span>)}</div>}</article> })}</section>}
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}><ShieldCheck size={24} /><div><strong>{percent === 100 ? 'Actividad de evaluación 1.1 desbloqueada' : 'Actividad de evaluación 1.1 bloqueada'}</strong><p>{percent === 100 ? 'Terminaste las fichas y todas las prácticas disponibles del R.A. 1.1.' : `Completa los ${totalSteps - completedActiveSteps.length} pasos pendientes.`}</p></div></div>
  </section>
}
