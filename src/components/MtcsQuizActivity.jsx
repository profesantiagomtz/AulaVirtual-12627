import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, BookOpen, Camera, CheckCircle2, Save, Send, ShieldCheck, X } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { uploadSubmissionFile } from '../lib/upload'
import { AUTO_MAX, TEACHER_MAX, gradeQuiz, quizFor } from '../lib/mtcs-quiz'

// Reduce la foto del cuaderno a JPG (máx. 1600 px) para que suba rápido desde el celular.
async function compressPhoto(file) {
  try {
    const bitmap = await createImageBitmap(file)
    const scale = Math.min(1, 1600 / Math.max(bitmap.width, bitmap.height))
    const canvas = document.createElement('canvas')
    canvas.width = Math.round(bitmap.width * scale)
    canvas.height = Math.round(bitmap.height * scale)
    canvas.getContext('2d').drawImage(bitmap, 0, 0, canvas.width, canvas.height)
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.82))
    if (blob) return new File([blob], 'cuaderno.jpg', { type: 'image/jpeg' })
  } catch { /* si el navegador no puede leerla, se sube tal cual */ }
  return file
}

export default function MtcsQuizActivity({ definition, assessment, session, onBack }) {
  const quiz = useMemo(() => quizFor(assessment.activityCode, session.id, assessment.id), [assessment.activityCode, session.id, assessment.id])
  const [tab, setTab] = useState('activity')
  const [answers, setAnswers] = useState({})
  const [stored, setStored] = useState({ path: '', name: '', quiz: null, legacy: false })
  const [photo, setPhoto] = useState(null)
  const [photoUrl, setPhotoUrl] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [status, setStatus] = useState('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (session.preview) { setStatus('ready'); return undefined }
    let active = true
    supabase.from('submissions').select('answers, submitted_at, file_path, original_filename').eq('assessment_id', assessment.id).maybeSingle().then(({ data, error }) => {
      if (!active) return
      if (error) { setMessage(error.message); setStatus('error'); return }
      const saved = data?.answers || {}
      const isNew = saved.quiz?.version === 2
      setAnswers(isNew ? saved.responses || {} : {})
      setStored({ path: data?.file_path || '', name: data?.original_filename || '', quiz: isNew ? saved.quiz : null, legacy: Boolean(data?.submitted_at && !isNew) })
      setSubmitted(Boolean(data?.submitted_at))
      setStatus('ready')
    })
    return () => { active = false }
  }, [assessment.id])

  useEffect(() => () => { if (photoUrl) URL.revokeObjectURL(photoUrl) }, [photoUrl])

  const answered = quiz.questions.filter(question => String(answers[question.key] || '').trim().length >= (question.type === 'open' ? 15 : 1)).length
  const complete = answered === quiz.questions.length
  const setAnswer = (key, value) => setAnswers(current => ({ ...current, [key]: value }))

  function pickPhoto(file) {
    if (!file) return
    if (!file.type.startsWith('image/')) { setMessage('Sube una foto (JPG o PNG) de tu cuaderno.'); setStatus('error'); return }
    setPhoto(file); setPhotoUrl(URL.createObjectURL(file)); setMessage(''); setStatus('ready')
  }

  async function save(deliver = false) {
    if (session.preview) { setMessage(deliver ? 'Vista previa: así se vería la entrega. No se guarda nada.' : 'Vista previa: las respuestas no se guardan.'); setStatus('ready'); return }
    if (deliver && !complete) { setMessage('Contesta todas las preguntas antes de entregar.'); setStatus('error'); return }
    if (deliver && !photo && !stored.path) { setMessage('Sube la foto de tu cuaderno antes de entregar.'); setStatus('error'); return }
    if (deliver && !window.confirm('Al entregar ya no podrás cambiar tus respuestas. ¿Entregar ahora?')) return
    setStatus('saving'); setMessage('')
    const { data: authData } = await supabase.auth.getUser()
    let uploaded = { path: stored.path, name: stored.name }
    if (photo) {
      const ready = await compressPhoto(photo)
      if (ready.size > 20 * 1024 * 1024) { setMessage('La foto supera 20 MB. Toma otra con menor resolución.'); setStatus('error'); return }
      const extension = ready.type === 'image/png' ? 'png' : ready.type === 'image/webp' ? 'webp' : 'jpg'
      const path = `${authData.user.id}/${assessment.id}/final/cuaderno.${extension}`
      try { await uploadSubmissionFile(path, ready, ready.type || 'image/jpeg') } catch (uploadError) { setMessage(uploadError.message || 'No fue posible subir la foto.'); setStatus('error'); return }
      uploaded = { path, name: photo.name || `cuaderno.${extension}` }
    }
    const graded = gradeQuiz(quiz, answers)
    const payload = { assessment_id: assessment.id, student_id: authData.user.id, answers: { activity: assessment.activityCode, assigned_case: { title: quiz.title, lines: quiz.lines }, responses: answers, quiz: graded }, file_path: uploaded.path || null, original_filename: uploaded.name || null, submitted_at: deliver ? new Date().toISOString() : null }
    const { error } = await supabase.from('submissions').upsert(payload, { onConflict: 'assessment_id,student_id' })
    if (error) { setMessage(error.message || 'No fue posible guardar.'); setStatus('error'); return }
    setStored({ ...uploaded, quiz: graded, legacy: false })
    setPhoto(null)
    setSubmitted(deliver)
    setMessage(deliver ? 'Actividad entregada correctamente.' : 'Avance guardado correctamente.')
    setStatus(deliver ? 'submitted' : 'ready')
  }

  if (status === 'loading') return <section className="panel page-panel activity-workspace"><div className="loading-state">Preparando la actividad…</div></section>

  const result = submitted && stored.quiz
  const marks = Object.fromEntries((stored.quiz?.items || []).map(item => [item.key, item.ok]))
  let number = 0

  return <section className="panel page-panel activity-workspace mtcs-workspace mtcs-quiz">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">{definition.label} · Actividad de evaluación</span><h1>{definition.quizTitle}</h1><p>{definition.quizIntro}</p></div><div className="mtcs-value"><strong>60</strong><span>PUNTOS MÁX.</span></div></div>
    <nav className="mtcs-tabs"><button className={tab === 'material' ? 'active' : ''} onClick={() => setTab('material')}><BookOpen size={17} /> Repaso y ejemplo</button><button className={tab === 'activity' ? 'active' : ''} onClick={() => setTab('activity')}><ShieldCheck size={17} /> Actividad</button></nav>

    {tab === 'material' ? <div className="mtcs-material"><div className="lesson-grid">{definition.lessons.map(([title, text]) => <article key={title}><span>{title.split('.')[0]}</span><div><h3>{title.replace(/^\d+\.\s*/, '')}</h3><p>{text}</p></div></article>)}</div><div className="worked-example"><strong>Ejemplo resuelto</strong><p>{definition.quizExample}</p></div><button className="primary mtcs-continue" onClick={() => { setTab('activity'); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>Ir a la actividad</button></div> : <div className="mtcs-activity">
      {stored.legacy ? <div className="quiz-legacy"><CheckCircle2 size={20} /><div><strong>Ya entregaste esta actividad con el formato anterior.</strong><p>Tu profesor la calificará con lo que enviaste. No necesitas hacer nada más.</p></div></div> : <>
        <ol className="quiz-steps"><li><b>1</b><span>Lee tus datos. Son <strong>solo tuyos</strong>: cada compañero tiene otros.</span></li><li><b>2</b><span>Resuelve en tu <strong>cuaderno</strong> y contesta aquí.</span></li><li><b>3</b><span>Toma una <strong>foto</strong> de tu cuaderno y entrega.</span></li></ol>
        <div className="assigned-case"><span className="eyebrow">Tus datos</span><h2>{quiz.title}</h2><ul>{quiz.lines.map(line => <li key={line}>{line}</li>)}</ul></div>
        {result && <div className="quiz-score"><div><strong>{stored.quiz.auto}<small>/{AUTO_MAX}</small></strong><span>Revisión automática</span></div><p>Tu profesor revisará la foto de tu cuaderno{quiz.questions.some(question => question.type === 'open') ? ' y tu respuesta escrita' : ''} (hasta {TEACHER_MAX} puntos más).</p></div>}
        <fieldset disabled={submitted || status === 'saving'} className="quiz-list">{quiz.questions.map(question => {
          number += 1
          const mark = result && question.type !== 'open' ? marks[question.key] : undefined
          return <div key={question.key} className={`quiz-item ${mark === true ? 'ok' : mark === false ? 'bad' : ''}`}>
            <p><b>{number}</b><span>{question.label}</span>{question.points && <em>{question.points} pts</em>}{mark === true && <CheckCircle2 size={18} />}{mark === false && <X size={18} />}</p>
            {question.type === 'choice' && <div className="quiz-options">{question.options.map(option => <label key={option} className={answers[question.key] === option ? 'selected' : ''}><input type="radio" name={question.key} checked={answers[question.key] === option} onChange={() => setAnswer(question.key, option)} />{option}</label>)}</div>}
            {question.type === 'text' && <input className="quiz-input" inputMode="decimal" autoComplete="off" value={answers[question.key] || ''} placeholder={question.placeholder} onChange={event => setAnswer(question.key, event.target.value)} />}
            {question.type === 'open' && <textarea rows="3" value={answers[question.key] || ''} placeholder={question.placeholder} onChange={event => setAnswer(question.key, event.target.value)} />}
          </div>
        })}</fieldset>
        <div className="quiz-photo"><div className="quiz-photo-text"><Camera size={22} /><div><strong>Foto de tu cuaderno · {TEACHER_MAX} pts</strong><p>{quiz.notebook}</p></div></div>
          {photoUrl ? <img src={photoUrl} alt="Vista previa de la foto del cuaderno" /> : stored.path ? <span className="quiz-photo-ok"><CheckCircle2 size={16} /> Foto recibida: {stored.name}</span> : null}
          {!submitted && <label className="secondary quiz-photo-btn"><Camera size={16} /> {photo || stored.path ? 'Cambiar foto' : 'Tomar o elegir foto'}<input type="file" accept="image/*" disabled={status === 'saving'} onChange={event => pickPhoto(event.target.files?.[0])} /></label>}
        </div>
        {message && <div className={status === 'error' ? 'form-error asin-message' : 'submission-success asin-message'}>{message}</div>}
        <footer className="activity-footer"><span className="mtcs-progress">{answered} de {quiz.questions.length} respuestas · {photo || stored.path ? 'foto lista' : 'falta la foto'}</span><div className="activity-footer-actions">{!submitted && <button className="secondary" onClick={() => save(false)} disabled={status === 'saving'}><Save size={17} /> Guardar avance</button>}<button className="primary" onClick={() => save(true)} disabled={submitted || status === 'saving'}>{submitted ? <CheckCircle2 size={17} /> : <Send size={17} />}{submitted ? 'Actividad entregada' : status === 'saving' ? 'Enviando…' : 'Entregar actividad'}</button></div></footer>
      </>}
    </div>}
  </section>
}
