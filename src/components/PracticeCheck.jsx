import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { AlertTriangle, CheckCircle2, ListChecks, X } from 'lucide-react'
import { cvssLevels, evaluateCheck, practiceChecks } from '../data/practice-checks'

// «¿Voy bien?»: el alumno revisa por su cuenta si su práctica de MTCS da el resultado esperado.
// No guarda nada en la base de datos ni cuenta para la calificación; las respuestas se recuerdan en el navegador.

export const hasPracticeChecks = code => Boolean(practiceChecks[code])

function readStore(key) { try { return JSON.parse(localStorage.getItem(key)) || {} } catch { return {} } }
function writeStore(key, value) { try { localStorage.setItem(key, JSON.stringify(value)) } catch { /* sin almacenamiento: solo no se recuerda */ } }

export function PracticeCheckButton({ onClick, compact = false }) {
  return <button type="button" className={`voybien-trigger ${compact ? 'compact' : ''}`} onClick={onClick}><ListChecks size={17} /><span>¿Voy bien?<small>Comprueba tu práctica</small></span></button>
}

export default function PracticeCheck({ code, label, assignment, session, onClose }) {
  const practices = practiceChecks[code] || []
  const storeKey = `aula-voybien:${session?.id || session?.email || 'invitado'}:${code}`
  const [answers, setAnswers] = useState(() => readStore(storeKey))
  const [practiceId, setPracticeId] = useState(() => readStore(storeKey)._practice || practices[0]?.id)
  const [results, setResults] = useState({})
  const [checking, setChecking] = useState(false)
  const dialog = useRef(null)
  const values = assignment?.values || {}
  const practice = practices.find(item => item.id === practiceId) || practices[0]

  useEffect(() => { writeStore(storeKey, { ...answers, _practice: practiceId }) }, [storeKey, answers, practiceId])
  useEffect(() => {
    const previous = document.activeElement
    dialog.current?.focus()
    const onKey = event => { if (event.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    document.body.classList.add('voybien-open')
    return () => { window.removeEventListener('keydown', onKey); document.body.classList.remove('voybien-open'); previous?.focus?.() }
  }, [onClose])

  const keyOf = check => `${practice.id}.${check.id}`
  const setAnswer = (check, value) => {
    setAnswers(current => ({ ...current, [keyOf(check)]: value }))
    setResults(current => ({ ...current, [keyOf(check)]: undefined }))
  }

  async function review() {
    setChecking(true)
    const entries = await Promise.all(practice.checks.map(async check => [keyOf(check), await evaluateCheck(check, answers[keyOf(check)], values)]))
    setResults(current => ({ ...current, ...Object.fromEntries(entries), [`${practice.id}._done`]: true }))
    setChecking(false)
  }

  const reviewed = results[`${practice.id}._done`]
  const graded = practice.checks.map(check => results[keyOf(check)]).filter(Boolean)
  const good = graded.filter(result => result.ok).length
  const practiceState = item => {
    if (!results[`${item.id}._done`]) return ''
    const list = item.checks.map(check => results[`${item.id}.${check.id}`]).filter(Boolean)
    return list.length && list.every(result => result.ok) ? 'ok' : list.length ? 'fix' : ''
  }

  // Se dibuja directo en <body> para quedar encima del menú inferior del celular.
  return createPortal(<div className="voybien-backdrop" onMouseDown={event => { if (event.target === event.currentTarget) onClose() }}>
    <aside className="voybien" role="dialog" aria-modal="true" aria-labelledby="voybien-title" tabIndex={-1} ref={dialog}>
      <header className="voybien-head">
        <span className="voybien-icon"><ListChecks size={22} /></span>
        <div><small>{label}</small><h2 id="voybien-title">¿Voy bien?</h2><p>Escribe lo que obtuviste en tu práctica y revisa si es el resultado esperado.</p></div>
        <button type="button" className="icon-btn" onClick={onClose} aria-label="Cerrar"><X size={20} /></button>
      </header>
      {assignment?.lines?.length > 0 && <details className="voybien-data"><summary>Tus datos asignados · {assignment.title}</summary><ul>{assignment.lines.map(line => <li key={line}>{line}</li>)}</ul></details>}
      <nav className="voybien-tabs" aria-label="Prácticas">{practices.map(item => <button type="button" key={item.id} className={`${item.id === practice.id ? 'active' : ''} ${practiceState(item)}`} aria-current={item.id === practice.id ? 'true' : undefined} onClick={() => setPracticeId(item.id)}>{practiceState(item) === 'ok' ? <CheckCircle2 size={15} /> : practiceState(item) === 'fix' ? <AlertTriangle size={15} /> : null}{item.title.split(' · ')[0]}</button>)}</nav>
      <div className="voybien-body">
        <h3>{practice.title.split(' · ')[1]}</h3>
        <ol className="voybien-checks">{practice.checks.map((check, index) => <CheckRow key={keyOf(check)} number={index + 1} check={check} values={values} answer={answers[keyOf(check)]} result={results[keyOf(check)]} onChange={value => setAnswer(check, value)} />)}</ol>
      </div>
      <footer className="voybien-foot">
        <div className={`voybien-summary ${reviewed ? (graded.length && good === graded.length ? 'ok' : graded.length ? 'fix' : '') : ''}`} aria-live="polite">
          {!reviewed ? <span>Contesta lo que ya hiciste; puedes dejar en blanco lo que no.</span>
            : !graded.length ? <span>Aún no escribes nada para revisar.</span>
            : good === graded.length ? <span><CheckCircle2 size={17} /><b>¡Vas muy bien!</b> Todo lo que revisaste es correcto.</span>
            : <span><AlertTriangle size={17} /><b>Vas bien en {good} de {graded.length}.</b> Corrige lo marcado en amarillo y vuelve a revisar.</span>}
        </div>
        <button type="button" className="primary" onClick={review} disabled={checking}><ListChecks size={17} />{checking ? 'Revisando…' : 'Revisar mi práctica'}</button>
      </footer>
      <p className="voybien-note">Esta revisión no cuenta para tu calificación: solo te dice si vas bien antes de entregar.</p>
    </aside>
  </div>, document.body)
}

function CheckRow({ number, check, values, answer, result, onChange }) {
  const label = typeof check.label === 'function' ? check.label(values) : check.label
  const id = `vb-${check.id}-${number}`
  const state = result ? (result.ok ? 'ok' : 'fix') : ''
  let field
  if (check.type === 'choice') field = <div className="voybien-options" role="radiogroup" aria-labelledby={`${id}-label`}>{check.options.map((option, index) => <label key={option} className={Number(answer) === index && answer !== '' && answer !== undefined ? 'picked' : ''}><input type="radio" name={id} checked={answer !== undefined && answer !== '' && Number(answer) === index} onChange={() => onChange(index)} /><span>{option}</span></label>)}</div>
  else if (check.type === 'number') field = <div className="voybien-number"><input id={id} inputMode="decimal" value={answer ?? ''} onChange={event => onChange(event.target.value)} placeholder="0" />{check.unit && <span>{check.unit}</span>}</div>
  else if (check.type === 'text') field = <input id={id} value={answer ?? ''} onChange={event => onChange(event.target.value)} placeholder={check.placeholder} />
  else if (check.type === 'cvss') field = <div className="voybien-pair"><input id={id} inputMode="decimal" value={answer?.score ?? ''} onChange={event => onChange({ ...answer, score: event.target.value })} placeholder="Ej. 7.8" aria-label="Calificación CVSS" /><select value={answer?.level ?? ''} onChange={event => onChange({ ...answer, level: event.target.value })} aria-label="Gravedad"><option value="">Gravedad…</option>{cvssLevels.map(level => <option key={level}>{level}</option>)}</select></div>
  else if (check.type === 'hash') field = <div className="voybien-stack"><input id={id} value={answer?.text ?? ''} onChange={event => onChange({ ...answer, text: event.target.value })} placeholder="Texto exacto de tu archivo" /><input className="mono" value={answer?.hash ?? ''} onChange={event => onChange({ ...answer, hash: event.target.value })} placeholder="Hash SHA-256 (64 caracteres)" aria-label="Hash SHA-256" spellCheck="false" autoCapitalize="off" /></div>
  else field = <textarea id={id} className="mono" rows={check.type === 'code' ? 7 : 5} value={answer ?? ''} onChange={event => onChange(event.target.value)} placeholder={check.type === 'code' ? 'Copia y pega aquí tu código…' : 'Copia y pega aquí lo que salió en la pantalla…'} spellCheck="false" autoCapitalize="off" />

  return <li className={`voybien-check ${state}`}>
    <div className="voybien-q"><b>{state === 'ok' ? <CheckCircle2 size={15} /> : state === 'fix' ? <AlertTriangle size={14} /> : number}</b><label id={`${id}-label`} htmlFor={['choice'].includes(check.type) ? undefined : id}>{label}</label></div>
    {field}
    {result && (result.items
      ? <ul className="voybien-items">{result.items.map(item => <li key={item.label} className={item.ok ? 'ok' : 'fix'}>{item.ok ? <CheckCircle2 size={15} /> : <AlertTriangle size={14} />}<span><b>{item.label}</b>{!item.ok && <small>{item.hint}</small>}</span></li>)}</ul>
      : <p className={`voybien-result ${state}`}>{result.ok ? <><CheckCircle2 size={15} /><b>¡Correcto!</b></> : <><AlertTriangle size={14} /><span><b>Revisa este punto.</b> {result.hint}</span></>}</p>)}
  </li>
}
