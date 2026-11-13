import { useCallback, useEffect, useMemo, useState } from 'react'
import { Ico } from './AulaIcon.jsx'

// Escenas de temporada para los temas «Acción de Gracias» y «Navidad».
// Todo es decorativo: aria-hidden, pointer-events:none (en seasonal.css) y se apaga con prefers-reduced-motion.

const reducedMotion = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

// Hojas o copos que caen despacio por la pantalla, detrás de la barra superior.
export function SeasonalFall({ theme }) {
  const items = useMemo(() => {
    const glyphs = theme === 'navidad' ? ['snowflake', 'snowflake2', 'snowflake3', 'snowflake2'] : ['leaf', 'maple', 'leaf', 'wheat']
    return Array.from({ length: 14 }, (_, index) => ({
      glyph: glyphs[index % glyphs.length],
      left: `${(index * 7.3 + (index % 3) * 2.1) % 100}%`,
      delay: `${-(index * 1.9) % 17}s`,
      duration: `${13 + (index % 5) * 2.4}s`,
      size: `${0.85 + (index % 4) * 0.22}rem`,
    }))
  }, [theme])
  if (theme !== 'navidad' && theme !== 'gracias') return null
  return <div className={`seasonal-fall seasonal-fall-${theme}`} aria-hidden="true">{items.map((item, index) => <span key={index} style={{ left: item.left, animationDelay: item.delay, animationDuration: item.duration, fontSize: item.size }}><Ico name={item.glyph} /></span>)}</div>
}

// Santa en su trineo cruza la parte de arriba de izquierda a derecha, saluda y dice «¡Ho ho ho!».
// Cada pasada se monta y se desmonta: entre pasadas no hay nada animándose.
const FIRST_PASS_MS = 2500
const PASS_EVERY_MS = 45000

export function SantaFlyby() {
  return <Flyby Pass={SantaPass} />
}

// Acción de Gracias: un pavito cruza corriendo sobre la barra de arriba, dice «¡Glu glu!» y suelta hojas de otoño.
export function TurkeyRun() {
  return <Flyby Pass={TurkeyPass} />
}

function Flyby({ Pass }) {
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
  return <Pass key={pass} onDone={done} />
}

function TurkeyPass({ onDone }) {
  const geometry = useMemo(() => {
    const width = window.innerWidth
    const small = width < 760
    // Alto del dibujo; la familia mide 1.8 veces eso de ancho y el pavito 1 vez.
    const h = small ? 50 : 64
    const rig = h * 2.95
    const from = -rig - 20
    const to = width + 30
    const seconds = Math.min(12, Math.max(6.5, width / 120))
    const count = Math.min(16, Math.round(width / 80))
    const glyphs = ['leaf', 'maple', 'leaf', 'wheat']
    const leaves = Array.from({ length: count }, (_, index) => {
      const x = (index + 0.5) * (width / count) + ((index * 37) % 21) - 10
      const at = seconds * (x - h * 2.1 - from) / (to - from)
      return { x, at, glyph: glyphs[index % glyphs.length], drift: ((index * 53) % 40) - 20, spin: index % 2 ? 220 : -200 }
    })
    // Que las patas pisen la raya de la barra superior (78 px en PC, 68 px en celular).
    const top = (small ? 68 : 78) - h * 0.8
    return { h, rig, from, to, seconds, leaves, top }
  }, [])

  useEffect(() => {
    const timer = window.setTimeout(onDone, (geometry.seconds + 3.5) * 1000)
    return () => window.clearTimeout(timer)
  }, [geometry, onDone])

  const run = { '--from': `${geometry.from}px`, '--to': `${geometry.to}px`, '--rig': `${geometry.rig}px`, top: geometry.top, animationDuration: `${geometry.seconds}s` }
  return <div className="santa-layer turkey-layer" aria-hidden="true">
    <div className="turkey-leaves" style={{ top: geometry.top + geometry.h * 0.7 }}>
      {geometry.leaves.map((leaf, index) => <i key={index} style={{ left: leaf.x, animationDelay: `${leaf.at.toFixed(2)}s`, '--drift': `${leaf.drift}px`, '--spin': `${leaf.spin}deg` }}><Ico name={leaf.glyph} /></i>)}
    </div>
    <div className="santa-flight" style={run}>
      <div className="turkey-rig" style={{ height: geometry.h }}>
        <div className="family-chase"><span className="santa-bubble family-bubble">¡Ven acá, pavito!</span><FamilyArt /></div>
        <div className="turkey-runner"><span className="santa-bubble turkey-bubble">¡Glu glu glu!</span><TurkeyArt /></div>
      </div>
    </div>
  </div>
}

// Una persona corriendo hacia la derecha con los brazos estirados. x = posición; s = tamaño.
function Runner({ x, s = 1, shirt, pants, hair, skin = '#e8b48c', hat, braid, delay = 0 }) {
  return <g transform={`translate(${x} ${96 - 92 * s}) scale(${s})`}>
    <g className="runner-bob" style={{ animationDelay: `${delay}s` }}>
      <g stroke={pants} strokeWidth="7" strokeLinecap="round" fill="none">
        <path className="runner-leg a" d="M22 60 l-6 16 l-6 12" style={{ animationDelay: `${delay}s` }} />
        <path className="runner-leg b" d="M26 60 l6 15 l-2 14" style={{ animationDelay: `${delay}s` }} />
      </g>
      <path className="runner-arm b" d="M22 38 l-10 10 l-6 -2" stroke={shirt} strokeWidth="6" strokeLinecap="round" fill="none" />
      <rect x="12" y="30" width="22" height="34" rx="9" fill={shirt} transform="rotate(12 23 47)" />
      <path className="runner-arm a" d="M30 38 l14 4 l8 -4" stroke={shirt} strokeWidth="6" strokeLinecap="round" fill="none" />
      <circle cx="52" cy="38" r="3.4" fill={skin} />
      <circle cx="30" cy="18" r="11" fill={skin} />
      <path d="M19 16 q2 -12 13 -10 q9 1 9 8 q-8 -4 -14 0 q-4 3 -8 2z" fill={hair} />
      {braid && <path d="M20 18 q-8 6 -6 16" stroke={hair} strokeWidth="5" strokeLinecap="round" fill="none" />}
      {hat && <><rect x="20" y="-6" width="20" height="14" fill="#2b2420" transform="rotate(8 30 2)" /><rect x="15" y="6" width="31" height="4" rx="2" fill="#2b2420" transform="rotate(8 30 8)" /><rect x="26" y="1" width="7" height="5" fill="none" stroke="#e8a531" strokeWidth="1.6" transform="rotate(8 30 4)" /></>}
      <circle cx="35" cy="17" r="1.6" fill="#24160d" />
      <path d="M34 23 q3 2 5 0" stroke="#7a2a1c" strokeWidth="1.8" strokeLinecap="round" fill="none" />
    </g>
  </g>
}

function FamilyArt() {
  return <svg className="santa-art family-art" viewBox="0 0 180 100" role="presentation" focusable="false">
    <Runner x={2} s={0.98} shirt="#5f7f3a" pants="#3a2618" hair="#3b2416" hat delay={-0.1} />
    <Runner x={62} s={0.92} shirt="#b23a2b" pants="#5a2e17" hair="#6b3519" braid delay={-0.2} />
    <Runner x={120} s={0.66} shirt="#e8a531" pants="#2c4a6b" hair="#24160d" delay={0} />
  </svg>
}

function TurkeyArt() {
  const feathers = ['#b23a2b', '#e8a531', '#8a4a22', '#c9772f', '#5f7f3a', '#e8a531', '#b23a2b']
  return <svg className="santa-art turkey-art" viewBox="0 0 100 100" role="presentation" focusable="false">
    {/* cola en abanico */}
    <g className="turkey-tail">
      {feathers.map((color, index) => <ellipse key={index} cx="34" cy="22" rx="9" ry="24" fill={color} transform={`rotate(${-75 + index * 25} 38 56)`} />)}
      {feathers.map((_, index) => <circle key={`o${index}`} cx="34" cy="6" r="3" fill="#fff4dc" opacity=".75" transform={`rotate(${-75 + index * 25} 38 56)`} />)}
    </g>
    {/* patas */}
    <g stroke="#d9862b" strokeWidth="3.4" strokeLinecap="round" fill="none">
      <path className="turkey-leg a" d="M42 74 l-3 16 l-5 2 M39 90 l3 3" />
      <path className="turkey-leg b" d="M54 74 l3 16 l5 2 M57 90 l-2 3" />
    </g>
    {/* cuerpo */}
    <ellipse cx="48" cy="60" rx="21" ry="18" fill="#7a4524" />
    <path d="M34 56 q10 12 26 6 q-6 12 -18 10 q-10 -3 -8 -16z" fill="#5c3018" />
    <ellipse cx="45" cy="58" rx="9" ry="7" fill="#9a5a30" />
    {/* cuello y cabeza */}
    <path d="M62 54 q8 -10 6 -24" stroke="#8a4f2a" strokeWidth="9" strokeLinecap="round" fill="none" />
    <circle cx="69" cy="28" r="9" fill="#c98b5b" />
    <circle cx="71" cy="25" r="2" fill="#24160d" /><circle cx="71.6" cy="24.4" r=".7" fill="#fff" />
    <path d="M77 27 l8 3 l-8 3z" fill="#f2b233" />
    <path className="turkey-wattle" d="M76 32 q4 8 -1 12 q-4 -4 -2 -11z" fill="#d9302b" />
    <path d="M66 20 q2 -6 6 -4" stroke="#d9302b" strokeWidth="2.5" strokeLinecap="round" fill="none" />
  </svg>
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
    // Regalitos que salen del costal (a la izquierda del trineo) y caen girando.
    const sackX = rig * 0.1
    const giftCount = small ? 4 : 7
    const colors = [['#c3262f', '#f2c14e'], ['#1f6b45', '#f8e7b0'], ['#f2c14e', '#c3262f'], ['#2c6fb7', '#fff'], ['#8a2a3a', '#f2c14e'], ['#fff', '#c3262f'], ['#3c9d7a', '#fff']]
    const gifts = Array.from({ length: giftCount }, (_, index) => {
      const x = width * (0.1 + 0.8 * (index + 0.5) / giftCount) + ((index * 41) % 30) - 15
      const at = seconds * (x - sackX - from) / (to - from)
      const [box, ribbon] = colors[index % colors.length]
      return { x, at, box, ribbon, dx: 40 + ((index * 29) % 50), spin: index % 2 ? 300 : -260, size: (small ? 22 : 28) + (index % 3) * 4 }
    })
    return { rig, from, to, seconds, flakes, gifts, top: small ? 28 : 34 }
  }, [])

  useEffect(() => {
    const timer = window.setTimeout(onDone, (geometry.seconds + 4) * 1000)
    return () => window.clearTimeout(timer)
  }, [geometry, onDone])

  const flight = { '--from': `${geometry.from}px`, '--to': `${geometry.to}px`, '--rig': `${geometry.rig}px`, top: geometry.top, animationDuration: `${geometry.seconds}s` }
  return <><div className="santa-gifts" aria-hidden="true" style={{ '--gift-top': `${geometry.top + geometry.rig * 0.12}px` }}>
    {geometry.gifts.map((gift, index) => <span key={index} className="santa-gift" style={{ left: gift.x, animationDelay: `${gift.at.toFixed(2)}s`, '--dx': `${gift.dx}px` }}>
      <i style={{ animationDelay: `${gift.at.toFixed(2)}s`, '--spin': `${gift.spin}deg`, '--box': gift.box, '--ribbon': gift.ribbon, width: gift.size, height: gift.size * 0.85 }} />
    </span>)}
  </div>
  <div className="santa-layer" aria-hidden="true">
    <div className="santa-trail" style={{ top: geometry.top + geometry.rig * 0.28 }}>
      {geometry.flakes.map((flake, index) => <i key={index} className={flake.big ? 'big' : ''} style={{ left: flake.x, animationDelay: `${flake.at.toFixed(2)}s`, '--drift': `${flake.drift}px` }} />)}
    </div>
    <div className="santa-flight" style={flight}>
      <div className="santa-rig">
        <span className="santa-bubble">¡Ho ho ho!</span>
        <SantaSleighArt />
      </div>
    </div>
  </div></>
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

// Navidad: fondo con un pino adornado y regalos al pie, discreto y por debajo del contenido.
// Las lucecitas parpadean despacio; se congelan con el interruptor de animaciones o reduced-motion.
export function XmasBackdrop() {
  const lights = [[200, 92, '#ffd166'], [176, 128, '#ff6b6b'], [226, 140, '#7fd1ff'], [158, 178, '#ffd166'], [244, 186, '#ff6b6b'], [196, 196, '#7fd1ff'],
    [140, 236, '#ff6b6b'], [262, 240, '#ffd166'], [208, 254, '#ff6b6b'], [122, 292, '#7fd1ff'], [174, 300, '#ffd166'], [236, 304, '#7fd1ff'], [282, 296, '#ff6b6b']]
  const ink = '#173d2a'
  return <div className="xmas-backdrop" aria-hidden="true">
    <svg viewBox="0 0 400 440" role="presentation" focusable="false">
      {/* suelo nevado */}
      <ellipse cx="200" cy="418" rx="196" ry="22" fill="#eef4f8" />
      <ellipse cx="200" cy="414" rx="150" ry="13" fill="#fff" />
      {/* tronco */}
      <rect x="184" y="338" width="32" height="44" rx="4" fill="#7a4a2a" stroke={ink} strokeWidth="3" />
      {/* tres pisos del pino, de abajo hacia arriba */}
      <path d="M200 196 L330 344 Q200 362 70 344 Z" fill="#1f7a46" stroke={ink} strokeWidth="4" strokeLinejoin="round" />
      <path d="M200 124 L296 254 Q200 270 104 254 Z" fill="#2a8f55" stroke={ink} strokeWidth="4" strokeLinejoin="round" />
      <path d="M200 58 L262 166 Q200 180 138 166 Z" fill="#35a463" stroke={ink} strokeWidth="4" strokeLinejoin="round" />
      {/* nieve en las puntas */}
      <path d="M86 340 q18 -10 34 2 q16 -10 30 2M250 342 q16 -12 32 0 q14 -10 32 -2M118 252 q16 -10 30 1M252 252 q14 -10 30 0M148 165 q14 -9 26 1M226 166 q13 -9 26 -1" fill="none" stroke="#fff" strokeWidth="6" strokeLinecap="round" opacity=".9" />
      {/* guirnaldas */}
      <path d="M150 152 Q200 172 250 146M120 236 Q200 266 282 230M92 322 Q200 356 312 316" fill="none" stroke="#f2c94c" strokeWidth="4" strokeDasharray="2 9" strokeLinecap="round" />
      {/* esferas y foquitos */}
      {lights.map(([x, y, c], i) => <circle key={i} className="xmas-light" cx={x} cy={y} r={i % 3 ? 7 : 9} fill={c} stroke={ink} strokeWidth="2.5" style={{ animationDelay: `${(i * 0.37) % 2.4}s` }} />)}
      {/* estrella */}
      <g className="xmas-star"><path d="M200 18 l10 22 24 2 -18 16 6 24 -22 -13 -22 13 6 -24 -18 -16 24 -2z" fill="#ffd166" stroke={ink} strokeWidth="3.5" strokeLinejoin="round" /></g>
      {/* regalos al pie */}
      <g stroke={ink} strokeWidth="3.5" strokeLinejoin="round">
        <rect x="74" y="360" width="78" height="56" rx="5" fill="#d93c3c" />
        <rect x="70" y="350" width="86" height="16" rx="4" fill="#e85a5a" />
        <path d="M113 350v66" stroke="#ffd166" strokeWidth="9" />
        <path d="M113 350c-8-18-32-22-30-8 2 10 20 8 30 8zM113 350c8-18 32-22 30-8-2 10-20 8-30 8z" fill="#ffd166" />
        <rect x="222" y="372" width="64" height="44" rx="5" fill="#3b6fd8" />
        <rect x="218" y="364" width="72" height="13" rx="4" fill="#5a8ae8" />
        <path d="M254 364v52" stroke="#fff" strokeWidth="8" />
        <path d="M254 364c-6-14-24-16-22-6 2 8 15 6 22 6zM254 364c6-14 24-16 22-6-2 8-15 6-22 6z" fill="#fff" />
        <rect x="160" y="384" width="56" height="32" rx="4" fill="#2f9e5b" />
        <path d="M188 384v32M160 400h56" stroke="#ffd166" strokeWidth="6" />
        <rect x="296" y="392" width="40" height="24" rx="4" fill="#c86bd6" />
        <path d="M316 392v24" stroke="#ffd166" strokeWidth="5" />
      </g>
    </svg>
  </div>
}
