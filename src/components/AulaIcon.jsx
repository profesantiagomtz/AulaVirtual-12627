import data from '../lib/aula-icons.json'

// Dibujos propios de AulaVirtual (scripts/icons/aula_icons.py). En esta plataforma no se usan emojis como imágenes.
export function iconMarkup(name) {
  const icon = data.icons[name] || data.icons[data.emoji[name]]
  if (!icon) return ''
  return icon.art
    ? `<svg class="aico aart" viewBox="0 0 48 48" aria-hidden="true" focusable="false">${icon.b}</svg>`
    : `<svg class="aico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${icon.b}</svg>`
}

export function Ico({ name, className = '' }) {
  return <span className={`aico-wrap ${className}`} aria-hidden="true" dangerouslySetInnerHTML={{ __html: iconMarkup(name) }} />
}
