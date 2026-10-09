import { useEffect, useState } from 'react'
import { ArrowLeft, CheckCircle2, ChevronRight, FileText, Image, Link2, LockKeyhole, Mail, ShieldCheck, Table2 } from 'lucide-react'
import { supabase } from '../lib/supabase'

const paths = {
  'EDOA-RA-1.2': {
    label: 'R.A. 1.2', title: 'Inserción y formato de objetos', description: 'Integra tablas, imágenes y objetos de referencia con un diseño claro y funcional.',
    topics: [
      { icon: Table2, title: 'Tablas', theory: ['Una tabla organiza información en filas y columnas.', 'Desde Insertar > Tabla puedes elegir el número de celdas.', 'Las pestañas Diseño de tabla y Presentación aparecen al seleccionar la tabla.'], example: 'Para un horario: usa columnas para los días y filas para las horas.', question: '¿Qué elemento organiza datos en filas y columnas?', options: ['Tabla', 'Hipervínculo', 'Nota al pie'], answer: 'Tabla' },
      { icon: Image, title: 'Imágenes', theory: ['Inserta imágenes desde el equipo o desde una fuente autorizada.', 'Usa las esquinas para cambiar el tamaño sin deformar.', 'El ajuste de texto controla cómo se acomoda el texto alrededor de la imagen.'], example: 'El ajuste Cuadrado permite que el texto rodee la imagen.', question: '¿Desde dónde conviene redimensionar una imagen para no deformarla?', options: ['Desde una esquina', 'Desde un costado', 'Desde el centro'], answer: 'Desde una esquina' },
      { icon: Link2, title: 'Objetos de referencia', theory: ['Un hipervínculo conecta con una página, archivo o sección.', 'Los estilos de título permiten generar un índice automático.', 'Las notas al pie aclaran información sin interrumpir el texto.', 'Las citas identifican la fuente utilizada.'], example: 'Aplica Título 1 a los encabezados antes de insertar la tabla de contenido.', question: '¿Qué debes aplicar antes de generar un índice automático?', options: ['Estilos de título', 'Color de página', 'Marca de agua'], answer: 'Estilos de título' },
      { icon: FileText, title: 'Otros objetos', theory: ['Word puede integrar hojas de cálculo, documentos y presentaciones.', 'También puede vincular videos o sonidos cuando el formato lo permite.', 'Elige insertar o vincular según necesites una copia o una conexión al archivo original.'], example: 'Una gráfica de Excel puede insertarse para presentar datos numéricos.', question: '¿Qué objeto resulta adecuado para mostrar datos calculados?', options: ['Hoja de cálculo', 'Nota al pie', 'Encabezado'], answer: 'Hoja de cálculo' },
      { icon: Image, title: 'Formato de objetos', theory: ['Tamaño define alto y ancho.', 'Posición ubica el objeto dentro de la página.', 'El ajuste de texto controla la relación entre objeto y párrafos.', 'Fondo, borde y efectos deben apoyar la lectura, no distraer.'], example: 'Usa Alinear para ordenar varios objetos con precisión.', question: '¿Qué opción decide cómo rodea el texto a una imagen?', options: ['Ajuste de texto', 'Ortografía', 'Interlineado'], answer: 'Ajuste de texto' },
    ],
  },
  'EDOA-RA-1.3': {
    label: 'R.A. 1.3', title: 'Correspondencia y revisión colaborativa', description: 'Automatiza documentos para varios destinatarios y controla los cambios realizados en equipo.',
    topics: [
      { icon: Mail, title: 'Combinación de correspondencia', theory: ['Combina un documento principal con una lista de destinatarios.', 'El contenido fijo permanece igual y los campos cambian para cada persona.', 'Se usa en cartas, constancias, etiquetas y sobres.'], example: 'Una constancia puede generar automáticamente el nombre y matrícula de cada alumno.', question: '¿Qué dos elementos necesita una combinación?', options: ['Documento y lista de destinatarios', 'Imagen y tabla', 'Encabezado y pie'], answer: 'Documento y lista de destinatarios' },
      { icon: Table2, title: 'Destinatarios y campos', theory: ['Puedes crear una lista nueva o utilizar una existente.', 'Cada columna de la lista representa un campo: Nombre, Grupo o Matrícula.', 'Los campos se insertan exactamente donde debe aparecer cada dato.'], example: '«Nombre» se sustituye por el nombre correspondiente en cada documento.', question: '¿Qué representa una columna de la lista?', options: ['Un campo', 'Una página', 'Una plantilla'], answer: 'Un campo' },
      { icon: FileText, title: 'Vista previa, formato e impresión', theory: ['Vista previa permite revisar cada registro antes de finalizar.', 'Comprueba que no existan campos vacíos o textos desbordados.', 'Finalizar y combinar crea documentos individuales o los envía a impresión.'], example: 'Recorre los destinatarios uno por uno antes de generar los archivos finales.', question: '¿Qué debes hacer antes de finalizar la combinación?', options: ['Revisar la vista previa', 'Cerrar Word', 'Eliminar la lista'], answer: 'Revisar la vista previa' },
      { icon: CheckCircle2, title: 'Ortografía y revisión', theory: ['El corrector detecta posibles errores, pero tú decides cada cambio.', 'El diccionario de sinónimos ayuda a evitar repeticiones.', 'Los comentarios permiten explicar observaciones sin modificar el texto.'], example: 'No aceptes todas las sugerencias sin leer: algunos nombres propios son correctos.', question: '¿Quién decide si una sugerencia ortográfica se acepta?', options: ['La persona que revisa', 'Word automáticamente', 'La impresora'], answer: 'La persona que revisa' },
      { icon: ShieldCheck, title: 'Control, comparación y protección', theory: ['Control de cambios registra inserciones, eliminaciones y formato.', 'Aceptar o rechazar confirma la versión final.', 'Comparar muestra diferencias entre dos documentos.', 'Restringir edición protege el archivo contra cambios no autorizados.'], example: 'Activa Control de cambios antes de compartir el documento con el equipo.', question: '¿Qué función registra quién modificó el documento?', options: ['Control de cambios', 'Combinar celdas', 'Vista de lectura'], answer: 'Control de cambios' },
    ],
  },
}

export default function EdoaAdvancedMaterial({ code, session, onBack, onProgressUpdate }) {
  const definition = paths[code] || paths['EDOA-RA-1.2']
  const [completed, setCompleted] = useState([])
  const [answers, setAnswers] = useState({})
  const [message, setMessage] = useState({})
  useEffect(() => {
    if (session.preview) return
    supabase.from('learning_progress').select('completed_steps').eq('material_code', code).maybeSingle().then(({ data }) => setCompleted(data?.completed_steps || []))
  }, [code, session.preview])
  async function check(index) {
    const topic = definition.topics[index]
    if (answers[index] !== topic.answer) { setMessage(current => ({ ...current, [index]: 'Revisa la explicación e inténtalo de nuevo.' })); return }
    const next = [...new Set([...completed, `topic-${index}`])]
    const progress = { material_code: code, completed_steps: next, completed_at: next.length >= definition.topics.length ? new Date().toISOString() : null }
    setCompleted(next); setMessage(current => ({ ...current, [index]: '¡Correcto! Tema completado.' })); onProgressUpdate?.(progress)
    if (!session.preview) await supabase.from('learning_progress').upsert({ student_id: session.id, ...progress }, { onConflict: 'student_id,material_code' })
  }
  const doneCount = definition.topics.filter((_, index) => completed.includes(`topic-${index}`)).length
  const percent = Math.round(doneCount / definition.topics.length * 100)
  return <section className="panel page-panel edoa-ra-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <header className="edoa-ra-hero"><div><span>{definition.label} · UNIDAD 1</span><h1>{definition.title}</h1><p>{definition.description}</p></div><div><strong>{percent}%</strong><small>COMPLETADO</small></div></header>
    <div className="edoa-ra-route">{definition.topics.map((topic, index) => <span className={completed.includes(`topic-${index}`) ? 'done' : ''} key={topic.title}>{completed.includes(`topic-${index}`) ? <CheckCircle2 size={16} /> : index + 1}<b>{topic.title}</b></span>)}</div>
    <div className="edoa-ra-topics">{definition.topics.map((topic, index) => { const Icon = topic.icon; const done = completed.includes(`topic-${index}`); return <article className={done ? 'done' : ''} key={topic.title}><header><span><Icon size={20} /></span><div><small>TEMA {index + 1}</small><h2>{topic.title}</h2></div>{done && <CheckCircle2 size={20} />}</header><section><h3>Lo que necesitas aprender</h3><ul>{topic.theory.map(point => <li key={point}>{point}</li>)}</ul><div className="edoa-ra-example"><b>Ejemplo práctico</b><p>{topic.example}</p></div></section><section className="edoa-ra-question"><h3>Comprueba lo aprendido</h3><p>{topic.question}</p><div>{topic.options.map(option => <label key={option}><input type="radio" name={`${code}-${index}`} disabled={done} checked={answers[index] === option} onChange={() => setAnswers(current => ({ ...current, [index]: option }))} />{option}</label>)}</div><button className="primary" disabled={done || !answers[index]} onClick={() => check(index)}>{done ? 'Tema completado' : 'Comprobar respuesta'}</button>{message[index] && <small className={message[index].startsWith('¡') ? 'correct-feedback' : 'wrong-feedback'}>{message[index]}</small>}</section></article> })}</div>
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}>{percent === 100 ? <ShieldCheck size={24} /> : <LockKeyhole size={24} />}<div><strong>{percent === 100 ? `Actividad de evaluación ${definition.label.replace('R.A. ', '')} desbloqueada` : `Actividad de evaluación ${definition.label.replace('R.A. ', '')} bloqueada`}</strong><p>{percent === 100 ? 'Ya puedes ir a Evaluaciones y entregar tu evidencia.' : `Completa los ${definition.topics.length - doneCount} temas pendientes.`}</p></div><ChevronRight size={19} /></div>
  </section>
}
