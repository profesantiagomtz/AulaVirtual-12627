import { useCallback, useEffect, useMemo, useState } from 'react'

// Escenas de temporada para los temas «Acción de Gracias» y «Navidad».
// Todo es decorativo: aria-hidden, pointer-events:none (en seasonal.css) y se apaga con prefers-reduced-motion.

const reducedMotion = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

// Hojas o copos que caen despacio por la pantalla, detrás de la barra superior.
export function SeasonalFall({ theme }) {
  const items = useMemo(() => {
    const glyphs = theme === 'navidad' ? ['❄', '❅', '❆', '✦'] : ['🍂', '🍁', '🍂', '🌾']
    return Array.from({ length: 14 }, (_, index) => ({
      glyph: glyphs[index % glyphs.length],
      left: `${(index * 7.3 + (index % 3) * 2.1) % 100}%`,
      delay: `${-(index * 1.9) % 17}s`,
      duration: `${13 + (index % 5) * 2.4}s`,
      size: `${0.85 + (index % 4) * 0.22}rem`,
    }))
  }, [theme])
  if (theme !== 'navidad' && theme !== 'gracias') return null
  return <div className={`seasonal-fall seasonal-fall-${theme}`} aria-hidden="true">{items.map((item, index) => <span key={index} style={{ left: item.left, animationDelay: item.delay, animationDuration: item.duration, fontSize: item.size }}>{item.glyph}</span>)}</div>
}

// Santa en su trineo cruza la parte de arriba de izquierda a derecha, saluda y dice «¡Ho ho ho!».
// Cada pasada se monta y se desmonta: entre pasadas no hay nada animándose.
const FIRST_PASS_MS = 2500
const PASS_EVERY_MS = 45000

export function SantaFlyby() {
  const [pass, setPass] = useState(0)
  const [flying, setFlying] = useState(false)

  useEffect(() => {
    if (reducedMotion()) return undefined
    let timer
    const launch = () => {
      if (!document.hidden) { setPass(value => value + 1); setFlying(true) }
      timer = window.setTimeout(launch, PASS_EVERY_MS)
    }
    timer = window.setTimeout(launch, FIRST_PASS_MS)
    return () => window.clearTimeout(timer)
  }, [])

  const done = useCallback(() => setFlying(false), [])
  if (!flying) return null
  return <SantaPass key={pass} onDone={done} />
}

function SantaPass({ onDone }) {
  const geometry = useMemo(() => {
    const width = window.innerWidth
    const small = width < 760
    const rig = small ? 190 : 270
    const from = -rig - 20
    const to = width + 30
    const seconds = Math.min(13, Math.max(7, width / 110))
    // El trineo (de donde sale la nieve) va en el primer tercio del dibujo.
    const sleighX = rig * 0.22
    const count = Math.min(38, Math.round(width / 30))
    const flakes = Array.from({ length: count }, (_, index) => {
      const x = (index + 0.5) * (width / count) + ((index * 37) % 13) - 6
      const at = seconds * (x - sleighX - from) / (to - from)
      return { x, at, drift: ((index * 53) % 30) - 15, big: index % 4 === 0 }
    })
    return { rig, from, to, seconds, flakes, top: small ? 28 : 34 }
  }, [])

  useEffect(() => {
    const timer = window.setTimeout(onDone, (geometry.seconds + 3) * 1000)
    return () => window.clearTimeout(timer)
  }, [geometry, onDone])

  const flight = { '--from': `${geometry.from}px`, '--to': `${geometry.to}px`, '--rig': `${geometry.rig}px`, top: geometry.top, animationDuration: `${geometry.seconds}s` }
  return <div className="santa-layer" aria-hidden="true">
    <div className="santa-trail" style={{ top: geometry.top + geometry.rig * 0.28 }}>
      {geometry.flakes.map((flake, index) => <i key={index} className={flake.big ? 'big' : ''} style={{ left: flake.x, animationDelay: `${flake.at.toFixed(2)}s`, '--drift': `${flake.drift}px` }} />)}
    </div>
    <div className="santa-flight" style={flight}>
      <div className="santa-rig">
        <span className="santa-bubble">¡Ho ho ho!</span>
        <SantaSleighArt />
      </div>
    </div>
  </div>
}

function Reindeer({ x, nose }) {
  return <g transform={`translate(${x} 0)`}>
    <g className="reindeer-legs back" stroke="#5b3a24" strokeWidth="4" strokeLinecap="round">
      <line x1="6" y1="62" x2="0" y2="80" />
      <line x1="38" y1="62" x2="44" y2="80" />
    </g>
    <ellipse cx="22" cy="56" rx="24" ry="11" fill="#9a6a45" />
    <ellipse cx="20" cy="60" rx="14" ry="5" fill="#c99a70" opacity=".7" />
    <path d="M2 52 q-7 -2 -8 4 q5 1 8 0z" fill="#f4e6d4" />
    <g className="reindeer-legs front" stroke="#6d4529" strokeWidth="4" strokeLinecap="round">
      <line x1="12" y1="63" x2="16" y2="81" />
      <line x1="34" y1="63" x2="28" y2="81" />
    </g>
    <path d="M38 52 q6 -12 10 -18" stroke="#9a6a45" strokeWidth="9" strokeLinecap="round" fill="none" />
    <ellipse cx="54" cy="31" rx="10" ry="7.5" fill="#a87650" />
    <path d="M47 25 l-4 -8 M49 24 l-1 -12 M43 17 l-6 -3 M48 15 l4 -5" stroke="#6b4a2e" strokeWidth="2.6" strokeLinecap="round" fill="none" />
    <path d="M45 27 l-7 -3 l4 6z" fill="#8a5a3a" />
    <circle cx="55" cy="28" r="1.8" fill="#24160d" />
    {nose
      ? <><circle className="rudolph-glow" cx="64" cy="33" r="7" fill="#ff5a4f" opacity=".35" /><circle cx="64" cy="33" r="4" fill="#e3302b" /></>
      : <circle cx="63.5" cy="33" r="3" fill="#3b261a" />}
    <path d="M42 41 q6 4 12 0" stroke="#c3262f" strokeWidth="3" fill="none" />
    <circle cx="48" cy="44" r="2.4" fill="#f2c14e" />
  </g>
}

function SantaSleighArt() {
  return <svg className="santa-art" viewBox="0 0 300 100" role="presentation" focusable="false">
    {/* riendas */}
    <path d="M98 40 Q150 52 182 41 Q210 34 238 41" stroke="#7a2a1c" strokeWidth="1.8" fill="none" />
    <Reindeer x={170} />
    <Reindeer x={228} nose />
    {/* costal de regalos */}
    <path d="M18 54 q-6 -26 14 -34 q20 4 16 34z" fill="#7b5a3a" />
    <path d="M24 26 q8 -6 18 -2" stroke="#5c3f26" strokeWidth="3" fill="none" />
    <rect x="30" y="16" width="12" height="11" rx="2" fill="#1f6b45" /><rect x="35" y="16" width="2.5" height="11" fill="#f2c14e" />
    <rect x="17" y="20" width="10" height="9" rx="2" fill="#c3262f" /><rect x="21" y="20" width="2.2" height="9" fill="#fff6dc" />
    {/* Santa */}
    <ellipse cx="72" cy="47" rx="19" ry="16" fill="#c3262f" />
    <rect x="57" y="48" width="30" height="5" fill="#24160d" /><rect x="69" y="47" width="7" height="7" rx="1" fill="#f2c14e" />
    <circle cx="74" cy="25" r="11" fill="#f6c9a8" />
    <path d="M62 27 q12 22 24 0 q-2 6 -12 6 q-10 0 -12 -6z" fill="#fff" />
    <path d="M65 29 q9 5 18 0 q0 18 -9 20 q-9 -2 -9 -20z" fill="#fff" />
    <path d="M67 27 q7 -3 14 0" stroke="#fff" strokeWidth="3.5" strokeLinecap="round" fill="none" />
    <circle cx="70" cy="22" r="1.5" fill="#24160d" /><circle cx="78" cy="22" r="1.5" fill="#24160d" />
    <circle cx="74" cy="25.5" r="2.4" fill="#e9967a" />
    <path d="M62 17 q10 -18 26 -8 q-2 3 -3 7z" fill="#c3262f" />
    <path d="M86 9 q8 -2 9 6" stroke="#c3262f" strokeWidth="6" strokeLinecap="round" fill="none" />
    <circle cx="96" cy="17" r="4" fill="#fff" />
    <rect x="61" y="15" width="27" height="6" rx="3" fill="#fff" />
    {/* brazo que saluda */}
    <g className="santa-wave">
      <path d="M84 42 q10 -8 12 -22" stroke="#c3262f" strokeWidth="7" strokeLinecap="round" fill="none" />
      <circle cx="96" cy="18" r="4.4" fill="#fff" />
      <circle cx="96.5" cy="14" r="4.6" fill="#1f6b45" />
    </g>
    {/* trineo */}
    <path d="M14 52 h104 q14 0 18 -14 q4 -6 10 -3 q-2 26 -26 33 h-92 q-16 0 -16 -16z" fill="#b8202a" />
    <path d="M14 52 h104 q14 0 18 -14" stroke="#f2c14e" strokeWidth="3" fill="none" />
    <path d="M30 60 q20 6 40 0 q20 -6 40 0" stroke="#f2c14e" strokeWidth="2" fill="none" opacity=".8" />
    <path d="M18 70 v12 M100 70 v12" stroke="#a87c1f" strokeWidth="3" />
    <path d="M4 84 h126 q16 0 18 -12 q1 -6 -5 -6" stroke="#d9a422" strokeWidth="4" strokeLinecap="round" fill="none" />
  </svg>
}
