// Orden alfabético de alumnos: apellido paterno, apellido materno y nombre(s).
// En la base el nombre está en un solo campo y los alumnos lo escriben «Nombre(s) Paterno Materno»,
// así que se toman las dos últimas palabras como apellidos. Las partículas (de, la, del…) se
// pegan a la palabra siguiente para respetar apellidos compuestos: «De la Cruz», «De los Santos».

const particles = new Set(['de', 'del', 'la', 'las', 'los', 'y', 'san', 'santa', 'van', 'von', 'mac', 'mc'])
const collator = new Intl.Collator('es', { sensitivity: 'base', ignorePunctuation: true, numeric: true })

function units(name = '') {
  const words = String(name).trim().split(/\s+/).filter(Boolean)
  const result = []
  let pending = []
  words.forEach(word => {
    if (particles.has(word.toLocaleLowerCase('es-MX'))) { pending.push(word); return }
    result.push([...pending, word].join(' '))
    pending = []
  })
  if (pending.length) result.length ? result[result.length - 1] += ` ${pending.join(' ')}` : result.push(pending.join(' '))
  return result
}

export function nameParts(name = '') {
  const parts = units(name)
  if (parts.length <= 1) return { paterno: parts[0] || '', materno: '', nombres: '' }
  if (parts.length === 2) return { paterno: parts[1], materno: '', nombres: parts[0] }
  return { paterno: parts.at(-2), materno: parts.at(-1), nombres: parts.slice(0, -2).join(' ') }
}

export function compareNames(a = '', b = '') {
  const x = nameParts(a)
  const y = nameParts(b)
  return collator.compare(x.paterno, y.paterno) || collator.compare(x.materno, y.materno) || collator.compare(x.nombres, y.nombres) || collator.compare(String(a), String(b))
}

// Compara objetos con propiedad name (alumno); los que no tienen alumno van al final.
export function compareStudents(a, b) {
  if (!a?.name || !b?.name) return Number(!a?.name) - Number(!b?.name)
  return compareNames(a.name, b.name) || String(a.id || a.email || '').localeCompare(String(b.id || b.email || ''))
}

// «Nombre(s) Paterno Materno» → «Paterno Materno Nombre(s)», como en una lista de asistencia.
export function surnameFirst(name = '') {
  const { paterno, materno, nombres } = nameParts(name)
  return [paterno, materno, nombres].filter(Boolean).join(' ')
}
