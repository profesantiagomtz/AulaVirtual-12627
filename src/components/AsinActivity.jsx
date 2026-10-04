import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, CheckCircle2, ChevronLeft, ChevronRight, Save, Send } from 'lucide-react'
import { supabase } from '../lib/supabase'

const probabilityRows = [
  { label: 'Alta', value: 3 },
  { label: 'Media', value: 2 },
  { label: 'Baja', value: 1 },
]
const impactColumns = [
  { label: 'Mínima', value: 1 },
  { label: 'Moderada', value: 2 },
  { label: 'Mayor', value: 3 },
]

const blankRisk = () => ({ risk: '', description: '', probability: null, impact: null, actionNeeded: '', measures: '' })
const blankQuestion = () => ({ text: '', type: 'Sí / No' })
const initialAnswers = {
  risks: [blankRisk(), blankRisk(), blankRisk()],
  equipment: { brandModel: '', operatingSystem: '', processor: '', ram: '', storage: '', antivirus: '', network: '', observations: '' },
  questionnaires: {
    users: Array.from({ length: 5 }, blankQuestion),
    administrators: Array.from({ length: 5 }, blankQuestion),
  },
}

function riskLevel(probability, impact) {
  const score = Number(probability) * Number(impact)
  if (!score) return null
  return { score, label: score <= 3 ? 'Bajo' : score <= 6 ? 'Medio' : 'Alto', tone: score <= 3 ? 'low' : score <= 6 ? 'medium' : 'high' }
}

function normalizeAnswers(saved) {
  if (!saved || typeof saved !== 'object') return initialAnswers
  return {
    risks: Array.from({ length: 3 }, (_, index) => ({ ...blankRisk(), ...(saved.risks?.[index] || {}) })),
    equipment: { ...initialAnswers.equipment, ...(saved.equipment || {}) },
    questionnaires: {
      users: Array.from({ length: 5 }, (_, index) => ({ ...blankQuestion(), ...(saved.questionnaires?.users?.[index] || {}) })),
      administrators: Array.from({ length: 5 }, (_, index) => ({ ...blankQuestion(), ...(saved.questionnaires?.administrators?.[index] || {}) })),
    },
  }
}

function stageComplete(stage, answers) {
  if (stage === 1) return answers.risks.every(item => item.risk.trim() && item.description.trim() && item.probability && item.impact && item.actionNeeded && item.measures.trim())
  if (stage === 2) return Object.values(answers.equipment).every(value => value.trim())
  return [...answers.questionnaires.users, ...answers.questionnaires.administrators].every(item => item.text.trim() && item.type)
}

export default function AsinActivity({ assessment, onBack }) {
  const [assignment, setAssignment] = useState(null)
  const [answers, setAnswers] = useState(initialAnswers)
  const [stage, setStage] = useState(1)
  const [status, setStatus] = useState('loading')
  const [submitted, setSubmitted] = useState(false)
  const [message, setMessage] = useState('')

  const completed = useMemo(() => [1, 2, 3].map(number => stageComplete(number, answers)), [answers])

  useEffect(() => {
    let active = true
    async function loadActivity() {
      try {
        const { data: assignmentData, error: assignmentError } = await supabase.rpc('get_or_create_asin_assignment', { p_assessment_id: assessment.id })
        if (assignmentError) throw assignmentError
        const currentAssignment = Array.isArray(assignmentData) ? assignmentData[0] : assignmentData
        const { data: submission, error: submissionError } = await supabase
          .from('submissions')
          .select('answers, submitted_at')
          .eq('assessment_id', assessment.id)
          .maybeSingle()
        if (submissionError) throw submissionError
        if (active) {
          setAssignment(currentAssignment)
          setAnswers(normalizeAnswers(submission?.answers))
          setSubmitted(Boolean(submission?.submitted_at))
          setStatus('ready')
        }
      } catch (error) {
        if (active) { setMessage(error.message || 'No fue posible abrir la actividad'); setStatus('error') }
      }
    }
    loadActivity()
    return () => { active = false }
  }, [assessment.id])

  async function save(submit = false) {
    if (submit && !completed.every(Boolean)) {
      setMessage('Completa todos los campos de las tres etapas antes de entregar.')
      setStatus('error')
      return
    }
    try {
      setStatus('saving'); setMessage('')
      const { data, error } = await supabase.rpc('save_asin_progress', {
        p_assessment_id: assessment.id,
        p_answers: answers,
        p_submit: submit,
      })
      if (error) throw error
      const result = Array.isArray(data) ? data[0] : data
      setSubmitted(Boolean(result?.submitted_at) || submit)
      setMessage(submit ? 'Actividad entregada correctamente.' : 'Avance guardado.')
      setStatus(submit ? 'submitted' : 'ready')
    } catch (error) {
      setMessage(error.message || 'No fue posible guardar tu avance')
      setStatus('error')
    }
  }

  function updateRisk(index, patch) {
    setAnswers(current => ({ ...current, risks: current.risks.map((item, itemIndex) => itemIndex === index ? { ...item, ...patch } : item) }))
  }

  function updateEquipment(field, value) {
    setAnswers(current => ({ ...current, equipment: { ...current.equipment, [field]: value } }))
  }

  function updateQuestion(audience, index, patch) {
    setAnswers(current => ({
      ...current,
      questionnaires: {
        ...current.questionnaires,
        [audience]: current.questionnaires[audience].map((item, itemIndex) => itemIndex === index ? { ...item, ...patch } : item),
      },
    }))
  }

  if (status === 'loading') return <section className="panel page-panel activity-workspace"><div className="loading-state">Preparando la actividad…</div></section>

  return <section className="panel page-panel activity-workspace asin-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">ASIN · R.A. 1.1</span><h1>{assessment.title}</h1><p>Completa las tres etapas directamente en la plataforma. Puedes guardar y continuar después.</p></div>{assignment && <div className="equipment-chip"><span>Equipo asignado</span><strong>{assignment.variant.equipment}</strong></div>}</div>

    <nav className="stage-nav" aria-label="Etapas de la actividad">
      {[['1', 'Matrices de riesgo'], ['2', 'Ficha técnica'], ['3', 'Cuestionarios']].map(([number, label]) => <button key={number} className={`${stage === Number(number) ? 'active' : ''} ${completed[Number(number) - 1] ? 'complete' : ''}`} onClick={() => setStage(Number(number))}><span>{completed[Number(number) - 1] ? <CheckCircle2 size={17} /> : number}</span><b>{label}</b></button>)}
    </nav>

    <fieldset disabled={submitted || status === 'saving'} className="asin-form">
      {stage === 1 && <RiskStage risks={answers.risks} updateRisk={updateRisk} />}
      {stage === 2 && <EquipmentStage equipment={answers.equipment} updateEquipment={updateEquipment} assignedEquipment={assignment?.variant?.equipment} />}
      {stage === 3 && <QuestionnaireStage questionnaires={answers.questionnaires} updateQuestion={updateQuestion} />}
    </fieldset>

    {message && <div className={status === 'error' ? 'form-error asin-message' : 'submission-success asin-message'}>{message}</div>}
    <footer className="activity-footer">
      <button className="secondary" onClick={() => setStage(value => Math.max(1, value - 1))} disabled={stage === 1}><ChevronLeft size={17} /> Anterior</button>
      <div className="activity-footer-actions">
        {!submitted && <button className="secondary" onClick={() => save(false)} disabled={status === 'saving'}><Save size={17} /> {status === 'saving' ? 'Guardando…' : 'Guardar avance'}</button>}
        {stage < 3 ? <button className="primary" onClick={() => setStage(value => Math.min(3, value + 1))}>Siguiente <ChevronRight size={17} /></button> : <button className="primary" onClick={() => save(true)} disabled={submitted || status === 'saving'}><Send size={17} /> {submitted ? 'Actividad entregada' : 'Entregar actividad'}</button>}
      </div>
    </footer>
  </section>
}

function RiskStage({ risks, updateRisk }) {
  return <div className="asin-stage"><div className="stage-heading"><span>Etapa 1 de 3</span><h2>Tres matrices de riesgo</h2><p>Identifica tres riesgos diferentes del laboratorio. Para cada uno, selecciona una sola combinación de probabilidad e impacto.</p></div><div className="risk-list">{risks.map((risk, index) => <RiskCard key={index} index={index} risk={risk} update={patch => updateRisk(index, patch)} />)}</div></div>
}

function RiskCard({ index, risk, update }) {
  const level = riskLevel(risk.probability, risk.impact)
  return <article className="risk-card"><header><div><span>Riesgo {index + 1}</span><h3>{risk.risk || 'Pendiente'}</h3></div>{level && <div className={`risk-result ${level.tone}`}><small>Nivel {level.label}</small><strong>{level.score}</strong></div>}</header><label className="risk-name-field">Nombre del riesgo detectado<input value={risk.risk} onChange={event => update({ risk: event.target.value })} required /></label><label>Descripción del riesgo<textarea rows="3" value={risk.description} onChange={event => update({ description: event.target.value })} required /></label><table className="risk-matrix-table" aria-label={`Matriz del riesgo ${index + 1}`}><thead><tr><th className="matrix-blank" colSpan="2" /><th className="consequence-head" colSpan="3">Consecuencia (Impacto)</th></tr><tr><th className="matrix-blank" colSpan="2" />{impactColumns.map(impact => <th className="impact-label" key={impact.value}>{impact.label}</th>)}</tr><tr><th className="probability-head" colSpan="2">Probabilidad</th>{impactColumns.map(impact => <th className="axis-score" key={impact.value}>{impact.value}</th>)}</tr></thead><tbody>{probabilityRows.map(probability => <tr key={probability.value}><th className="probability-label">{probability.label}</th><th className="axis-score">{probability.value}</th>{impactColumns.map(impact => { const selected = risk.probability === probability.value && risk.impact === impact.value; return <td key={impact.value}><button type="button" className={selected ? 'selected' : ''} onClick={() => update({ probability: probability.value, impact: impact.value })} aria-pressed={selected} aria-label={`${probability.label}, impacto ${impact.label}`}>{selected ? '✓' : ''}</button></td> })}</tr>)}</tbody></table><div className="form-row"><label>¿Se deben tomar medidas para prevenirlo?<select value={risk.actionNeeded} onChange={event => update({ actionNeeded: event.target.value })} required><option value="">Selecciona una respuesta</option><option>Sí</option><option>No</option></select></label><label>Medidas preventivas<textarea rows="3" value={risk.measures} onChange={event => update({ measures: event.target.value })} required /></label></div></article>
}

function EquipmentStage({ equipment, updateEquipment, assignedEquipment }) {
  const fields = [
    ['brandModel', 'Marca y modelo'],
    ['operatingSystem', 'Sistema operativo y versión'],
    ['processor', 'Procesador'],
    ['ram', 'Memoria RAM'],
    ['storage', 'Almacenamiento'],
    ['antivirus', 'Antivirus y estado'],
    ['network', 'Conectividad'],
  ]
  return <div className="asin-stage"><div className="stage-heading"><span>Etapa 2 de 3</span><h2>Ficha técnica del equipo</h2><p>Completa la ficha técnica del {assignedEquipment || 'equipo asignado'}.</p></div><div className="equipment-form">{fields.map(([field, label]) => <label key={field}>{label}<input value={equipment[field]} onChange={event => updateEquipment(field, event.target.value)} required /></label>)}<label className="full-field">Observaciones<textarea rows="4" value={equipment.observations} onChange={event => updateEquipment('observations', event.target.value)} required /></label></div></div>
}

function QuestionnaireStage({ questionnaires, updateQuestion }) {
  return <div className="asin-stage"><div className="stage-heading"><span>Etapa 3 de 3</span><h2>Cuestionarios para identificar riesgos</h2><p>Redacta cinco preguntas para usuarios y cinco para administradores.</p></div><div className="questionnaire-grid"><Questionnaire title="Cuestionario para usuarios" items={questionnaires.users} onChange={(index, patch) => updateQuestion('users', index, patch)} /><Questionnaire title="Cuestionario para administradores" items={questionnaires.administrators} onChange={(index, patch) => updateQuestion('administrators', index, patch)} /></div></div>
}

function Questionnaire({ title, items, onChange }) {
  return <section className="questionnaire"><header><h3>{title}</h3></header>{items.map((item, index) => <div className="question-row" key={index}><span>{index + 1}</span><label>Pregunta<input value={item.text} onChange={event => onChange(index, { text: event.target.value })} required /></label><label>Tipo de respuesta<select value={item.type} onChange={event => onChange(index, { type: event.target.value })}><option>Sí / No</option><option>Opción múltiple</option><option>Respuesta abierta</option><option>Escala de frecuencia</option></select></label></div>)}</section>
}
