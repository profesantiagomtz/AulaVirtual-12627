import { useState } from 'react'
import { AlertTriangle, Check, Copy, Sparkles } from 'lucide-react'
import { isSupabaseReady, supabase } from '../lib/supabase'

// Revisión con IA: la función revisar-entrega propone calificación y retroalimentación.
// Solo sugiere; el docente pasa la calificación al campo y la guarda como siempre.

const demoReview = {
  calificacion: 46,
  nivel: 'Bueno',
  resumen: 'Cumple casi todo lo pedido; la ficha técnica está completa, pero dos medidas de seguridad son muy generales.',
  criterios: [
    { criterio: 'Matrices de riesgo', puntos: 18, maximo: 24, comentario: 'Identifica bien los riesgos; las medidas del riesgo 3 no son concretas.' },
    { criterio: 'Ficha técnica del equipo', puntos: 12, maximo: 12, comentario: 'Todos los datos completos y coherentes.' },
    { criterio: 'Cuestionarios', puntos: 16, maximo: 24, comentario: 'Faltan dos preguntas para administradores.' },
  ],
  fortalezas: ['Ficha técnica completa', 'Riesgos bien redactados'],
  mejoras: ['Medidas más concretas', 'Completar el cuestionario de administradores'],
  retroalimentacion: '¡Buen trabajo! Tu ficha técnica está completa y tus riesgos se entienden. Para subir tu calificación, escribe medidas concretas (qué harías, con qué herramienta) y termina las 5 preguntas para administradores.',
  alertas: [],
}

async function errorMessage(error) {
  try { return (await error.context?.json())?.error || error.message } catch { return error.message }
}

export default function AiReview({ submission, onUseScore }) {
  const [review, setReview] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  async function run() {
    setBusy(true); setError(''); setCopied(false)
    try {
      if (!isSupabaseReady) { await new Promise(resolve => setTimeout(resolve, 600)); setReview(demoReview); return }
      const { data, error: invokeError } = await supabase.functions.invoke('revisar-entrega', { body: { submission_id: submission.id } })
      if (invokeError) throw new Error(await errorMessage(invokeError))
      if (data?.error) throw new Error(data.error)
      setReview(data.review)
    } catch (runError) { setError(runError.message || 'No fue posible revisar con IA.') }
    finally { setBusy(false) }
  }

  async function copy() {
    try { await navigator.clipboard.writeText(review.retroalimentacion); setCopied(true) } catch { setError('No se pudo copiar; selecciona el texto a mano.') }
  }

  if (!review) return <div className="ai-review ai-review-idle">
    <button className="secondary ai-review-run" disabled={busy} onClick={run}><Sparkles size={16} /> {busy ? 'Revisando con IA…' : 'Revisar con IA'}</button>
    <small>Propone calificación y retroalimentación. Usted decide.</small>
    {error && <p className="ai-review-error">{error}</p>}
  </div>

  return <div className="ai-review">
    <header><span><Sparkles size={15} /> Sugerencia de la IA</span><b className={`ai-level ai-level-${review.nivel.split(' ')[0].toLowerCase()}`}>{review.nivel}</b><strong>{review.calificacion}/60</strong></header>
    <p className="ai-review-summary">{review.resumen}</p>
    {review.alertas?.length > 0 && <ul className="ai-review-alerts">{review.alertas.map(alert => <li key={alert}><AlertTriangle size={14} /> {alert}</li>)}</ul>}
    {review.criterios?.length > 0 && <table className="ai-review-criteria"><tbody>{review.criterios.map(item => <tr key={item.criterio}><th>{item.criterio}<small>{item.comentario}</small></th><td>{item.puntos}/{item.maximo}</td></tr>)}</tbody></table>}
    <div className="ai-review-feedback"><span>Retroalimentación para el alumno</span><p>{review.retroalimentacion}</p></div>
    <div className="ai-review-actions">
      <button className="primary" onClick={() => onUseScore(review.calificacion)}><Check size={16} /> Usar {review.calificacion} puntos</button>
      <button className="secondary" onClick={copy}><Copy size={16} /> {copied ? 'Copiada' : 'Copiar retroalimentación'}</button>
      <button className="text-btn" disabled={busy} onClick={run}>{busy ? 'Revisando…' : 'Volver a revisar'}</button>
    </div>
    {error && <p className="ai-review-error">{error}</p>}
    <small className="ai-review-note">Es una propuesta. Revise la entrega antes de guardar la calificación.</small>
  </div>
}
