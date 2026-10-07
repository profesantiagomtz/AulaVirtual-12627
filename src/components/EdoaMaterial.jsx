import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, CheckCircle2, ChevronLeft, ChevronRight, Monitor, ShieldCheck } from 'lucide-react'
import { supabase } from '../lib/supabase'

const cards = [
  { icon: '🖥️', title: 'Conoce la interfaz de Word', intro: 'Antes de editar, ubica las zonas principales de Word 2019.', notes: [['Barra de título', 'Muestra el nombre del documento.'], ['Acceso rápido', 'Contiene Guardar, Deshacer y Rehacer.'], ['Pestañas', 'Agrupan los comandos por tipo de trabajo.'], ['Cinta de opciones', 'Muestra los botones de la pestaña activa.'], ['Regla', 'Ayuda a controlar márgenes y sangrías.'], ['Área de trabajo', 'Es la hoja donde escribes.'], ['Barra de estado', 'Muestra página, palabras y zoom.']], question: '¿En qué parte aparecen los botones de la pestaña activa?', options: ['Cinta de opciones', 'Barra de estado', 'Regla'], answer: 'Cinta de opciones' },
  { icon: '📐', title: 'Diseño de página', intro: 'Configura la hoja antes de comenzar a escribir.', notes: [['Márgenes', 'Espacio en blanco alrededor del texto. Ruta: Disposición › Márgenes.'], ['Orientación', 'Cambia la hoja entre vertical y horizontal.'], ['Tamaño', 'Selecciona Carta, A4 u Oficio.'], ['Encabezado y pie', 'Texto que se repite arriba o abajo. Ruta: Insertar.'], ['Color de página', 'Cambia el fondo desde la pestaña Diseño.']], question: '¿Qué opción cambia la hoja entre vertical y horizontal?', options: ['Orientación', 'Márgenes', 'Interlineado'], answer: 'Orientación' },
  { icon: '🔤', title: 'Formato de texto y párrafo', intro: 'La pestaña Inicio contiene los grupos Fuente y Párrafo.', notes: [['Fuente', 'Negrita, cursiva, subrayado, tamaño y color.'], ['Alineación izquierda', 'Los renglones comienzan en el margen izquierdo.'], ['Centrada', 'El texto queda equilibrado respecto al centro.'], ['Derecha', 'Los renglones terminan en el margen derecho.'], ['Justificada', 'El texto se alinea en ambos márgenes.'], ['Interlineado y sangría', 'Controlan el espacio entre renglones y la entrada del párrafo.']], question: '¿Qué alineación deja rectos ambos márgenes?', options: ['Justificada', 'Centrada', 'Derecha'], answer: 'Justificada' },
  { icon: '🖱️', title: 'Iconos y atajos esenciales', intro: 'Reconocer los botones y atajos te permite trabajar con mayor rapidez.', notes: [['Ctrl+C', 'Copia el contenido seleccionado.'], ['Ctrl+X', 'Corta: quita el contenido y lo guarda temporalmente.'], ['Ctrl+V', 'Pega lo copiado o cortado.'], ['Ctrl+Z', 'Deshace el último cambio.'], ['Ctrl+G', 'Guarda el documento.'], ['Ctrl+E', 'Selecciona todo el documento.']], question: '¿Qué diferencia principal existe entre copiar y cortar?', options: ['Cortar quita el original', 'Copiar elimina el original', 'No existe diferencia'], answer: 'Cortar quita el original' },
  { icon: '💾', title: 'Plantillas, respaldo y tipos de archivo', intro: 'El tipo de archivo determina cómo podrás reutilizar o compartir el documento.', notes: [['.docx', 'Documento actual y editable de Word.'], ['.dotx', 'Plantilla reutilizable.'], ['.pdf', 'Formato para compartir sin facilitar la edición.'], ['.doc', 'Documento de versiones antiguas de Word.'], ['.txt', 'Texto sin formato.'], ['Respaldo', 'Guarda una copia adicional antes de hacer cambios importantes.']], question: '¿Qué extensión corresponde a una plantilla reutilizable?', options: ['.dotx', '.docx', '.txt'], answer: '.dotx' },
  { icon: '📊', title: 'Insertar tablas e imágenes', intro: 'Los objetos permiten organizar información y comunicar ideas visualmente.', notes: [['Tabla', 'Organiza datos en filas y columnas.'], ['Imagen', 'Puede insertarse desde el equipo o desde una fuente en línea.'], ['Diseño de tabla', 'Permite aplicar estilos, bordes, combinar celdas y agregar filas.'], ['Formato de imagen', 'Permite recortar, aplicar estilos y cambiar el ajuste del texto.']], question: '¿Qué objeto organiza datos en filas y columnas?', options: ['Tabla', 'Imagen', 'Nota al pie'], answer: 'Tabla' },
  { icon: '📚', title: 'Objetos de referencia', intro: 'Word ayuda a documentar las fuentes y organizar trabajos extensos.', notes: [['Hipervínculo', 'Ctrl+K enlaza una palabra con una web, archivo o correo.'], ['Tabla de contenido', 'Se genera utilizando títulos con estilo.'], ['Nota al pie', 'Amplía una idea en la parte inferior de la página.'], ['Cita y bibliografía', 'Registra las fuentes y genera la lista de referencias.'], ['Objeto', 'Permite insertar documentos, hojas de cálculo o presentaciones.']], question: '¿En qué pestaña se inserta una nota al pie?', options: ['Referencias', 'Inicio', 'Disposición'], answer: 'Referencias' },
  { icon: '🎯', title: 'Formato y ajuste de objetos', intro: 'Selecciona el objeto para mostrar sus herramientas de formato.', notes: [['Tamaño', 'Arrastra desde una esquina para conservar la proporción.'], ['Relleno y contorno', 'Cambian el fondo y borde de una forma.'], ['En línea', 'El objeto se comporta como una letra dentro del texto.'], ['Cuadrado', 'El texto rodea el objeto.'], ['Detrás o delante', 'Coloca el objeto por debajo o encima del texto.']], question: '¿Desde dónde debes redimensionar una imagen para no deformarla?', options: ['Desde una esquina', 'Desde un lado', 'Desde el centro'], answer: 'Desde una esquina' },
  { icon: '📄', title: 'Formato APA del documento', intro: 'Estos ajustes corresponden a APA 7.ª edición.', notes: [['Márgenes', '2.54 cm en cada lado.'], ['Fuente', 'Times New Roman 12 o Calibri 11.'], ['Interlineado', 'Doble en el documento.'], ['Sangría', 'Primera línea de cada párrafo a 1.27 cm.'], ['Número de página', 'En la parte superior derecha.']], question: '¿Cuál es el margen indicado por APA?', options: ['2.54 cm', '1 cm', '5 cm'], answer: '2.54 cm' },
  { icon: '🔎', title: 'Cita y referencia', intro: 'Una fuente se reconoce dentro del texto y también en la lista final.', notes: [['Cita parentética', '(Cuartero, 2016).'], ['Cita narrativa', 'Cuartero (2016).'], ['Dos autores', '(Alfie & Veloso, 2011).'], ['Tres o más', '(Gómez et al., 2020).'], ['Referencia de libro', 'Autor. (Año). Título. Editorial.'], ['Lista final', 'Orden alfabético y sangría francesa.']], question: '¿Cuál cita corresponde a tres o más autores?', options: ['(Gómez et al., 2020)', '(Gómez, 2020)', 'Gómez y todos (2020)'], answer: '(Gómez et al., 2020)' },
  { icon: '🛠️', title: 'Práctica guiada en Word', intro: 'Aplica lo aprendido en un documento nuevo.', notes: [['1. Configura la página', 'Carta, orientación vertical y márgenes de 2.54 cm.'], ['2. Escribe un título', 'Aplica estilo Título 1.'], ['3. Agrega contenido', 'Escribe dos párrafos y usa alineación justificada.'], ['4. Inserta objetos', 'Crea una tabla 3×3 y agrega una imagen con ajuste cuadrado.'], ['5. Registra fuentes', 'Agrega tres fuentes, inserta sus citas y genera la bibliografía.'], ['6. Guarda', 'Conserva una copia .docx y exporta otra en PDF.']], question: '¿Qué debes hacer antes de generar automáticamente la tabla de contenido?', options: ['Aplicar estilos de título', 'Cambiar el color de página', 'Insertar una imagen'], answer: 'Aplicar estilos de título' },
]

export default function EdoaMaterial({ session, onBack, onProgressUpdate }) {
  const code = 'EDOA-WORD-U1'
  const [page, setPage] = useState(0)
  const [completed, setCompleted] = useState([])
  const [answer, setAnswer] = useState('')
  const [message, setMessage] = useState('')
  const current = cards[page]
  const percent = Math.round(completed.length / cards.length * 100)
  const done = completed.includes(page)

  useEffect(() => {
    if (session.preview) return
    supabase.from('learning_progress').select('completed_steps').eq('material_code', code).maybeSingle().then(({ data }) => setCompleted(data?.completed_steps || []))
  }, [session.preview])

  useEffect(() => { setAnswer(''); setMessage('') }, [page])

  async function completeCard() {
    if (answer !== current.answer) { setMessage('Todavía no es correcto. Revisa la ficha y vuelve a intentarlo.'); return }
    const next = [...new Set([...completed, page])].sort((a, b) => a - b)
    setCompleted(next); setMessage('¡Correcto! Ficha completada.')
    const progress = { material_code: code, completed_steps: next, completed_at: next.length === cards.length ? new Date().toISOString() : null }
    onProgressUpdate?.(progress)
    if (!session.preview) await supabase.from('learning_progress').upsert({ student_id: session.id, ...progress }, { onConflict: 'student_id,material_code' })
  }

  const status = useMemo(() => cards.map((_, index) => completed.includes(index)), [completed])
  return <section className="panel page-panel edoa-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="edoa-hero"><div><span className="eyebrow">EDOA · WORD 2019 · UNIDAD 1</span><h1>Diseño y formato del documento</h1><p>Aprende, practica y aplica cada herramienta paso a paso.</p></div><div className="edoa-progress"><strong>{percent}%</strong><span>COMPLETADO</span></div></div>
    <div className="edoa-step-strip">{status.map((isDone, index) => <button className={index === page ? 'active' : isDone ? 'done' : ''} key={cards[index].title} onClick={() => setPage(index)} aria-label={`Ficha ${index + 1}`}>{isDone ? <CheckCircle2 size={14} /> : index + 1}</button>)}</div>
    <article className="edoa-card">
      <header><div className="edoa-card-icon">{current.icon}</div><div><small>FICHA {page + 1} DE {cards.length}</small><h2>{current.title}</h2></div></header>
      <p className="edoa-intro">{current.intro}</p>
      <div className="edoa-notes">{current.notes.map(([title, text]) => <div key={title}><strong>{title}</strong><p>{text}</p></div>)}</div>
      <section className="edoa-check"><span>COMPRUEBA LO APRENDIDO</span><h3>{current.question}</h3><div>{current.options.map(option => <label key={option}><input type="radio" name={`edoa-${page}`} checked={answer === option} disabled={done} onChange={() => setAnswer(option)} />{option}</label>)}</div><button className="primary" disabled={done || !answer} onClick={completeCard}>{done ? 'Ficha completada' : 'Revisar respuesta'}</button>{message && <p className={message.startsWith('¡') ? 'correct-feedback' : 'wrong-feedback'}>{message}</p>}</section>
    </article>
    <div className="edoa-nav"><button className="secondary" disabled={page === 0} onClick={() => setPage(page - 1)}><ChevronLeft size={17} />Anterior</button><span>{page + 1} / {cards.length}</span><button className="secondary" disabled={page === cards.length - 1} onClick={() => setPage(page + 1)}>Siguiente<ChevronRight size={17} /></button></div>
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}><ShieldCheck size={24} /><div><strong>{percent === 100 ? 'Unidad completada' : 'Continúa con las fichas'}</strong><p>{percent === 100 ? 'Terminaste el recorrido de Word 2019.' : `Te faltan ${cards.length - completed.length} fichas por completar.`}</p></div></div>
  </section>
}
