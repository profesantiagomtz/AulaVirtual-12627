// «¿Voy bien?»: puntos que el alumno puede comprobar solo en cada práctica de MTCS.
// Cada práctica corresponde a las del material (pr1, pr2, pr3). Las comprobaciones usan los
// datos asignados (v) de src/lib/mtcs-assignment.js, así cada alumno revisa SU resultado esperado.
//
// Tipos: choice (opción correcta), number (valor numérico), text (formato), output/code (texto pegado
// con varios puntos a revisar), hash (texto + hash SHA-256) y cvss (calificación + gravedad).
// Las pistas orientan sin dar la respuesta.

const lines = text => text.split(/\r?\n/)
const has = (text, pattern) => pattern.test(text)
const count = (text, pattern) => (text.match(pattern) || []).length
const noTraceback = { label: 'El programa termina sin mensajes de error', test: text => !/Traceback \(most recent call last\)|^\w*Error:/m.test(text), hint: 'Tu salida muestra un error. Lee la última línea del mensaje: dice el tipo de error y la línea. Corrígelo y vuelve a ejecutar.' }

// Números que aparecen en una salida de Python: 218340105584896, 218,340,105,584,896, 60.0, 4.75e+17…
export function numbersIn(text) {
  return [...text.matchAll(/\d[\d,_]*(?:\.\d+)?(?:e[+-]?\d+)?/gi)].map(match => match[0].replace(/[,_]/g, ''))
}
const near = (raw, expected, rel = 1e-6) => {
  const value = Number(raw)
  return Number.isFinite(value) && Math.abs(value - expected) <= Math.max(1e-9, Math.abs(expected) * rel)
}
const showsNumber = (text, accept) => numbersIn(text).some(accept)
const sameLine = (text, word, number) => lines(text).some(line => line.toLowerCase().includes(word.toLowerCase()) && numbersIn(line).some(raw => near(raw, number, 0)))

// R.A. 3.1: combinaciones = caracteres ** longitud; segundos = combinaciones / intentos.
function passwordMath({ charset, length, attempts }) {
  const combos = BigInt(charset) ** BigInt(length)
  const secondsExact = combos / BigInt(attempts)
  const seconds = Number(combos) / attempts
  const hours = [Math.floor(seconds / 3600), Number(secondsExact / 3600n), seconds / 3600]
  const minutes = [Math.floor((seconds % 3600) / 60), Number((secondsExact % 3600n) / 60n)]
  return { combos, seconds, secondsExact: Number(secondsExact), hours, minutes }
}

const phases = ['Preparación', 'Detección y análisis', 'Contención, erradicación y recuperación', 'Lecciones aprendidas']

export const practiceChecks = {
  'MTCS-RA-2.2': [
    {
      id: 'pr1', title: 'Práctica 1 · Comprueba la integridad con hash',
      checks: [
        { id: 'hash', type: 'hash', label: 'Escribe el texto de tu archivo (o del laboratorio) y pega el hash SHA-256 que obtuviste.' },
        { id: 'avalancha', type: 'choice', label: 'Cambiaste una sola letra y volviste a calcular. ¿Qué pasó con el hash?', options: ['Cambió casi por completo', 'Cambió solo un carácter', 'Quedó igual'], answer: 0, hint: 'Con una sola letra distinta el hash cambia casi entero. Si quedó igual, seguramente no guardaste el archivo antes de calcular.' },
        { id: 'regreso', type: 'choice', label: 'Regresaste el texto original y calculaste otra vez. ¿Cómo quedó el hash?', options: ['Igual al primero', 'Distinto al primero'], answer: 0, hint: 'Debe volver a ser idéntico. Si no, el texto no es exactamente el mismo: mayúsculas, espacios y acentos cuentan.' },
        { id: 'certutil', type: 'choice', label: 'Solo en computadora: ¿Get-FileHash y certutil dieron el mismo hash?', options: ['Sí, solo cambian mayúsculas y minúsculas', 'No, son diferentes'], answer: 0, hint: 'Los dos calculan SHA-256 del mismo archivo, así que deben coincidir. Revisa que en certutil pusiste SHA256 al final y el mismo nombre de archivo.' },
      ],
    },
    {
      id: 'pr2', title: 'Práctica 2 · Plan de disponibilidad y respuesta a incidentes',
      checks: [
        { id: 'h99', type: 'number', label: 'Horas al año que podría estar caído el servicio con 99 % de disponibilidad', unit: 'h', accept: n => Math.abs(n - 87.6) <= 0.05, hint: () => 'Un año tiene 365 × 24 = 8,760 horas. Con 99 % funciona y el 1 % no: multiplica 8,760 × 0.01.' },
        { id: 'h999', type: 'number', label: 'Horas al año con 99.9 % de disponibilidad', unit: 'h', accept: n => Math.abs(n - 8.76) <= 0.01, hint: () => 'Ahora solo falta el 0.1 %: multiplica 8,760 × 0.001.' },
        { id: 'rpo', type: 'number', label: 'Si tu organización respalda una vez cada noche, ¿cuál es su RPO?', unit: 'h', accept: n => n === 24, hint: () => 'El RPO es la información que podrías perder: todo lo que se hizo desde el último respaldo. ¿Cada cuántas horas respaldas?' },
        { id: 'rto', type: 'number', label: v => `Tu organización acepta máximo ${v.maxHours} h sin servicio. ¿Qué RTO propusiste?`, unit: 'h', accept: (n, v) => n > 0 && n <= v.maxHours, hint: v => `El RTO es el tiempo para que el servicio vuelva. No puede pasar de lo que acepta tu organización (${v.maxHours} h).` },
        { id: 'fase1', type: 'choice', label: '¿Cuál es la primera fase de la respuesta a incidentes?', options: phases, answer: 0, hint: 'Antes de que pase algo ya debe existir un plan, respaldos y responsables.' },
        { id: 'fase3', type: 'choice', label: '¿Qué fase sigue después de «Detección y análisis»?', options: phases, answer: 2, hint: 'Una vez que sabes qué pasó, primero detienes el daño y luego recuperas el servicio.' },
      ],
    },
    {
      id: 'pr3', title: 'Práctica 3 · Revisa la defensa de un equipo y busca vulnerabilidades',
      checks: [
        { id: 'cve', type: 'text', label: 'Escribe el CVE que encontraste en nvd.nist.gov', placeholder: 'CVE-2024-11477', test: text => /^CVE-(19|20)\d{2}-\d{4,7}$/i.test(text.trim()), hint: 'El formato es CVE-año-número, por ejemplo CVE-2024-11477. Cópialo tal cual de la página.' },
        { id: 'cvss', type: 'cvss', label: 'Calificación CVSS y gravedad que anotaste' },
        { id: 'cuenta', type: 'choice', label: 'Trabajar con una cuenta estándar (sin privilegios) protege al…', options: ['Host (el equipo)', 'Servidor', 'Red'], answer: 0, hint: 'La cuenta con la que usas tu computadora es una medida del propio equipo.' },
        { id: 'red', type: 'choice', label: 'Separar el wifi de clientes de la red interna es una medida de…', options: ['Red', 'Host', 'Seguridad física'], answer: 0, hint: 'Separar redes (segmentar con VLAN) protege la red, no un equipo ni el edificio.' },
        { id: 'etica', type: 'choice', label: 'Antes de revisar con Nmap la red de una organización necesitas…', options: ['Autorización por escrito', 'Que nadie se dé cuenta', 'Solo saber usar la herramienta'], answer: 0, hint: 'Sin permiso por escrito, revisar redes ajenas puede ser un delito.' },
      ],
    },
  ],

  'MTCS-RA-3.1': [
    {
      id: 'pr1', title: 'Práctica 1 · Tu primer programa en un archivo .py',
      checks: [
        { id: 'codigo', type: 'code', label: 'Pega el código de tu ciber_lab.py', items: () => [
          { label: 'Tiene al menos dos comentarios', test: text => lines(text).filter(line => line.trim().startsWith('#')).length >= 2, hint: 'Agrega dos comentarios: renglones que empiezan con #.' },
          { label: 'Tiene al menos cuatro print', test: text => count(text, /\bprint\s*\(/g) >= 4, hint: 'Necesitas tres print normales y uno con sep.' },
          { label: 'Uno de los print usa sep', test: text => has(text, /\bsep\s*=/), hint: 'Agrega un print con sep, por ejemplo: print("Usuario", "Clave", sep=" | ")' },
          { label: 'Paréntesis completos', test: text => count(text, /\(/g) === count(text, /\)/g), hint: text => `Revisa los paréntesis: hay ${count(text, /\(/g)} que abren y ${count(text, /\)/g)} que cierran.` },
        ] },
        { id: 'salida', type: 'output', label: 'Pega la salida (lo que aparece al ejecutarlo)', items: () => [
          { label: 'Muestra al menos cuatro renglones', test: text => lines(text).filter(line => line.trim()).length >= 4, hint: 'Cada print escribe un renglón; deberías ver al menos cuatro.' },
          noTraceback,
        ] },
        { id: 'extension', type: 'choice', label: 'Tu archivo fuente termina en…', options: ['.py', '.exe', '.txt'], answer: 0, hint: 'Los programas de Python se guardan como texto con la terminación del lenguaje.' },
        { id: 'interprete', type: 'choice', label: 'Python es un lenguaje…', options: ['Interpretado', 'Compilado'], answer: 0, hint: 'El intérprete lee y ejecuta tu archivo cada vez; no generas un .exe.' },
      ],
    },
    {
      id: 'pr2', title: 'Práctica 2 · Variables, tipos y operadores',
      checks: [
        { id: 'salida', type: 'output', label: 'Pega la salida de tu programa (con los datos de tu escenario)', items: v => {
          const math = passwordMath(v)
          return [
            { label: 'Muestra los cuatro tipos con type()', test: text => ['str', 'int', 'float', 'bool'].every(type => text.includes(`'${type}'`)), hint: text => `Falta mostrar: ${['str', 'int', 'float', 'bool'].filter(type => !text.includes(`'${type}'`)).join(', ')}. Usa print(type(variable)).` },
            { label: 'Combinaciones posibles', test: text => showsNumber(text, raw => raw === math.combos.toString() || near(raw, Number(math.combos), 1e-9)), hint: `Calcula caracteres ** longitud con tus datos: ${v.charset} ** ${v.length}. Usa ** (potencia), no * ni ^.` },
            { label: 'Segundos para probarlas todas', test: text => showsNumber(text, raw => near(raw, math.seconds) || near(raw, math.secondsExact, 0)), hint: `Divide las combinaciones entre los intentos por segundo (${v.attempts.toLocaleString('es-MX')}).` },
            { label: 'Horas', test: text => showsNumber(text, raw => math.hours.some(hours => near(raw, hours, 1e-9))), hint: 'Obtén las horas enteras con segundos // 3600.' },
            { label: 'Minutos que sobran', test: text => showsNumber(text, raw => math.minutes.some(minutes => near(raw, minutes, 0))), hint: 'Los minutos que sobran son segundos % 3600 // 60.' },
            { label: '¿Es segura? (12 o más caracteres)', test: text => text.includes(v.length >= 12 ? 'True' : 'False'), hint: `Compara tu longitud (${v.length}) con 12 usando >=. Python responde True o False.` },
            noTraceback,
          ]
        } },
        { id: 'codigo', type: 'code', label: 'Pega tu código', items: () => [
          { label: 'Usa ** para la potencia', test: text => has(text, /\*\*/), hint: 'La potencia en Python es **, por ejemplo 62 ** 8.' },
          { label: 'Usa // y % para horas y minutos', test: text => has(text, /\/\//) && has(text, /%/), hint: '// da la división entera y % el sobrante.' },
          { label: 'Una condición con and u or', test: text => has(text, /\b(and|or)\b/), hint: 'Agrega una variable lógica que use and u or, por ejemplo: segura = longitud >= 12 and caracteres >= 62' },
          { label: 'Resultados con f-strings', test: text => has(text, /\bf["']/), hint: 'Muestra tus resultados así: print(f"Combinaciones: {combinaciones}")' },
        ] },
      ],
    },
    {
      id: 'pr3', title: 'Práctica 3 · Programa con entradas y corrección de errores',
      checks: [
        { id: 'codigo', type: 'code', label: 'Pega tu programa final', items: () => [
          { label: 'Pide datos con input()', test: text => has(text, /\binput\s*\(/), hint: 'Usa input() para pedir el usuario y la longitud.' },
          { label: 'Convierte la longitud con int()', test: text => has(text, /\bint\s*\(\s*input\s*\(/) || has(text, /\bint\s*\(/), hint: 'input() siempre entrega texto. Conviértelo: longitud = int(input("Longitud: "))' },
          { label: 'Muestra un resumen con f-string', test: text => has(text, /\bf["']/), hint: 'Usa print(f"...{variable}...") para el resumen.' },
          { label: 'Tiene una variable lógica con >=', test: text => has(text, />=/), hint: 'Agrega por ejemplo: segura = longitud >= 12' },
        ] },
        { id: 'sintaxis', type: 'choice', label: 'Olvidaste cerrar un paréntesis. ¿Qué error aparece?', options: ['SyntaxError', 'ValueError', 'Ningún error'], answer: 0, hint: 'Si la escritura está mal, Python ni siquiera arranca: es un error de sintaxis.' },
        { id: 'ejecucion', type: 'choice', label: 'Escribiste «doce» donde el programa hace int(input()). ¿Qué error aparece?', options: ['ValueError (error de ejecución)', 'SyntaxError', 'Ninguno, el programa sigue'], answer: 0, hint: 'El código está bien escrito, pero ese dato no se puede convertir a número: falla al ejecutarse.' },
        { id: 'logica', type: 'choice', label: 'El programa no marca error pero da un resultado incorrecto. Es un error…', options: ['De lógica', 'De sintaxis', 'De ejecución'], answer: 0, hint: 'Si no aparece mensaje, Python hizo lo que escribiste… pero no lo que querías.' },
      ],
    },
  ],

  'MTCS-RA-3.2': [
    {
      id: 'pr1', title: 'Práctica 1 · Control de acceso con decisiones y ciclos',
      checks: [
        { id: 'codigo', type: 'code', label: 'Pega el código de tu acceso.py', items: () => [
          { label: 'Usa while para repetir', test: text => has(text, /\bwhile\b/), hint: 'Pide usuario y clave dentro de un while para repetir hasta 3 veces.' },
          { label: 'Usa if, elif y else', test: text => has(text, /\bif\b/) && has(text, /\belif\b/) && has(text, /\belse\b/), hint: 'Necesitas las tres: if para el primer caso, elif para otro y else para el resto.' },
          { label: 'Usa break al acertar', test: text => has(text, /\bbreak\b/), hint: 'Cuando la clave es correcta, sal del ciclo con break.' },
          { label: 'Usa and u or', test: text => has(text, /\b(and|or)\b/), hint: 'Por ejemplo: if usuario == "ana" and clave == "...":' },
          { label: 'Usa for con range y continue', test: text => has(text, /\bfor\b[^\n]*\brange\s*\(/) && has(text, /\bcontinue\b/), hint: 'Lista los equipos con for i in range(...) y salta el de mantenimiento con continue.' },
          { label: 'El while puede terminar', test: text => !has(text, /while\s+True\s*:/) || has(text, /\bbreak\b/), hint: 'Un while True sin break nunca termina. Cuenta los intentos o usa break.' },
        ] },
        { id: 'salida', type: 'output', label: 'Pega la salida de tus tres pruebas', items: () => [
          { label: 'Prueba con la clave correcta', test: text => has(text, /concedid|bienvenid|acceso correcto|acceso permitido/i), hint: 'Ejecuta una prueba escribiendo bien el usuario y la clave.' },
          { label: 'Prueba con 3 errores: «Cuenta bloqueada»', test: text => has(text, /bloquead/i), hint: 'Escribe mal la clave tres veces seguidas: debe aparecer «Cuenta bloqueada».' },
          { label: 'Prueba con invitado: «Acceso solo a Internet»', test: text => has(text, /internet/i), hint: 'Entra como invitado o visita: debe aparecer «Acceso solo a Internet».' },
          noTraceback,
        ] },
        { id: 'orden', type: 'choice', label: '¿Qué revisa primero tu if?', options: ['Si la cuenta ya está bloqueada', 'Si la clave es correcta'], answer: 0, hint: 'El orden importa: si la cuenta está bloqueada, no debe entrar aunque escriba bien la clave.' },
      ],
    },
    {
      id: 'pr2', title: 'Práctica 2 · Analizador de registros con listas y funciones',
      checks: [
        { id: 'salida', type: 'output', label: 'Prueba tu analizador con los registros e intentos fallidos de tu escenario y pega la salida', items: v => {
          const unique = [...new Set(v.log)].sort()
          const top = unique.map(user => [user, v.log.filter(item => item === user).length]).sort((a, b) => b[1] - a[1])[0]
          const suspicious = v.fails.filter(value => value >= v.threshold)
          return [
            { label: `Veces que aparece «${top[0]}»`, test: text => sameLine(text, top[0], top[1]), hint: `Llama a tu función contar(registros, "${top[0]}") y muestra el resultado en el mismo renglón que el nombre.` },
            { label: 'Usuarios únicos en orden alfabético', test: text => { const low = text.toLowerCase(); let from = 0; return unique.every(user => { const at = low.indexOf(user, from); if (at < 0) return false; from = at + user.length; return true }) }, hint: 'Agrega a otra lista solo los que no están (not in) y después ordénala con sorted().' },
            { label: 'Mayor número de intentos fallidos', test: text => sameLine(text, 'mayor', Math.max(...v.fails)) || sameLine(text, 'máx', Math.max(...v.fails)), hint: 'Tu función mayor() recorre la lista y guarda el número más grande (sin usar max()). Muéstralo en un renglón que diga «mayor».' },
            { label: `Equipos sospechosos (desde ${v.threshold} fallos)`, test: text => text.includes(`[${suspicious.join(', ')}]`) || sameLine(text, 'sospech', suspicious.length), hint: `Cuenta o lista los equipos con ${v.threshold} fallos o más: usa >=, no >.` },
            noTraceback,
          ]
        } },
        { id: 'codigo', type: 'code', label: 'Pega tu código', items: () => [
          { label: 'Cuatro funciones con def', test: text => count(text, /^\s*def\s+\w+\s*\(/gm) >= 4, hint: 'Crea contar, unicos, mayor y sospechosos con def.' },
          { label: 'Las funciones regresan su resultado con return', test: text => count(text, /\breturn\b/g) >= 4, hint: 'Cada función debe terminar con return y el resultado, no solo con print.' },
          { label: 'mayor() sin usar max()', test: text => !has(text, /\bmax\s*\(/), hint: 'Haz tu propio algoritmo: empieza con el primer número y compáralo con cada uno.' },
          { label: 'Ordena con sorted()', test: text => has(text, /\bsorted\s*\(|\.sort\s*\(/), hint: 'Ordena los usuarios únicos con sorted(lista).' },
          { label: 'Permisos con bits: | y &', test: text => has(text, /[^|]\|[^|]/) && has(text, /[^&]&[^&]/), hint: 'Junta permisos con | y revisa uno con &, por ejemplo: permisos = LEER | ESCRIBIR' },
        ] },
      ],
    },
    {
      id: 'pr3', title: 'Práctica 3 · Programa a prueba de errores',
      checks: [
        { id: 'codigo', type: 'code', label: 'Pega tu programa final', items: () => [
          { label: 'try y except en las entradas', test: text => has(text, /\btry\s*:/) && has(text, /\bexcept\b/), hint: 'Pon el int(input()) dentro de try y atrapa el error con except ValueError.' },
          { label: 'Vuelve a pedir el dato si es inválido', test: text => has(text, /\bwhile\b/) && has(text, /\btry\s*:/), hint: 'Mete el try dentro de un while para repetir la pregunta hasta que el dato sea válido.' },
          { label: 'Una función con raise', test: text => has(text, /\braise\s+\w+/), hint: 'Por ejemplo: if intentos < 0: raise ValueError("Los intentos no pueden ser negativos")' },
          { label: 'Bloque finally', test: text => has(text, /\bfinally\s*:/), hint: 'Agrega finally: print("Fin del registro")' },
        ] },
        { id: 'finally', type: 'choice', label: '¿Cuándo se ejecuta el bloque finally?', options: ['Siempre, haya error o no', 'Solo si hubo error', 'Solo si no hubo error'], answer: 0, hint: 'else corre si no hubo error; finally corre en todos los casos.' },
        { id: 'cero', type: 'choice', label: 'Dividir entre cero provoca…', options: ['ZeroDivisionError', 'ValueError', 'SyntaxError'], answer: 0, hint: 'Es un error de ejecución con nombre propio: división entre cero.' },
      ],
    },
  ],
}

const severities = [['Baja', 0.1, 3.9], ['Media', 4, 6.9], ['Alta', 7, 8.9], ['Crítica', 9, 10]]
export const cvssLevels = severities.map(([name]) => name)

function normalize(value) { return String(value ?? '').trim() }
function readNumber(value) { const parsed = Number(normalize(value).replace(',', '.')); return normalize(value) && Number.isFinite(parsed) ? parsed : null }

// Variantes con que Windows o el celular pudieron guardar el texto: con o sin salto de línea final
// y en UTF-8, ANSI (Set-Content de PowerShell 5) o UTF-16 (redirección con >).
function encodings(text) {
  const utf8 = new TextEncoder().encode(text)
  const ansi = Uint8Array.from([...text].map(char => char.charCodeAt(0) < 256 ? char.charCodeAt(0) : 63))
  const utf16 = new Uint8Array(2 + text.length * 2)
  utf16.set([0xff, 0xfe])
  for (let index = 0; index < text.length; index += 1) { const code = text.charCodeAt(index); utf16[2 + index * 2] = code & 255; utf16[3 + index * 2] = code >> 8 }
  return [utf8, Uint8Array.from([0xef, 0xbb, 0xbf, ...utf8]), ansi, utf16]
}
async function sha256(bytes) {
  const digest = await crypto.subtle.digest('SHA-256', bytes)
  return Array.from(new Uint8Array(digest)).map(byte => byte.toString(16).padStart(2, '0')).join('')
}

// Revisa un punto. Regresa null si está sin contestar, o { ok, hint, items } con el detalle.
export async function evaluateCheck(check, answer, v) {
  if (check.type === 'choice') {
    if (answer === undefined || answer === '') return null
    return { ok: Number(answer) === check.answer, hint: check.hint }
  }
  if (check.type === 'number') {
    const value = readNumber(answer)
    if (value === null) return normalize(answer) ? { ok: false, hint: 'Escribe solo el número, sin letras.' } : null
    return { ok: check.accept(value, v), hint: check.hint(v) }
  }
  if (check.type === 'text') {
    if (!normalize(answer)) return null
    return { ok: check.test(normalize(answer)), hint: check.hint }
  }
  if (check.type === 'output' || check.type === 'code') {
    const text = normalize(answer)
    if (!text) return null
    const items = check.items(v).map(item => {
      const ok = item.test(text)
      return { label: item.label, ok, hint: typeof item.hint === 'function' ? item.hint(text) : item.hint }
    })
    return { ok: items.every(item => item.ok), items }
  }
  if (check.type === 'cvss') {
    const score = readNumber(answer?.score)
    if (score === null && !answer?.level) return null
    if (score === null || score < 0 || score > 10) return { ok: false, hint: 'La calificación CVSS es un número de 0 a 10, por ejemplo 7.8.' }
    const level = severities.find(([, low, high]) => score >= low && score <= high + 0.05)?.[0]
    if (!answer?.level) return { ok: false, hint: 'Elige también la gravedad que anotaste.' }
    return { ok: level === answer.level, hint: 'Revisa la gravedad: en CVSS 0.1–3.9 es Baja, 4.0–6.9 Media, 7.0–8.9 Alta y 9.0–10 Crítica.' }
  }
  if (check.type === 'hash') {
    const text = String(answer?.text || '').replace(/[\r\n\s]+$/, '')
    const typed = normalize(answer?.hash).replace(/\s+/g, '').toLowerCase()
    if (!text && !typed) return null
    if (!/^[0-9a-f]{64}$/.test(typed)) return { ok: false, hint: `Un hash SHA-256 tiene 64 caracteres (números y letras de la A a la F). El que pegaste tiene ${typed.length}. Cópialo completo.` }
    if (!text) return { ok: false, hint: 'Escribe también el texto exacto que tiene tu archivo.' }
    if (!crypto?.subtle) return { ok: true, hint: '' }
    const candidates = [text, `${text}\r\n`, `${text}\n`].flatMap(encodings)
    const hashes = await Promise.all(candidates.map(sha256))
    return { ok: hashes.includes(typed), hint: 'El hash no corresponde a ese texto. Revisa que el texto sea idéntico (mayúsculas, espacios, acentos y puntos) y que calculaste SHA-256, no MD5 ni SHA-1.' }
  }
  return null
}
