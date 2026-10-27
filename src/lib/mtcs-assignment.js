// Datos que la plataforma asigna a cada alumno en las actividades de MTCS.
// Salen siempre iguales para el mismo alumno y actividad: los usan la actividad y «¿Voy bien?».

export function hash(text) {
  let value = 2166136261
  for (let index = 0; index < text.length; index += 1) value = Math.imul(value ^ text.charCodeAt(index), 16777619)
  return value >>> 0
}

export function assignmentFor(studentId, assessmentId, code) {
  const seed = hash(`${studentId}-${assessmentId}-${code}`)
  if (code === 'MTCS-RA-1.1') {
    const places = ['laboratorio escolar', 'biblioteca', 'taller técnico', 'oficina administrativa']
    return {
      title: `Escenario ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Lugar: ${places[seed % places.length]}`, `Equipos cableados: ${12 + (seed % 9)}`, `Dispositivos inalámbricos: ${6 + (seed % 7)}`, `Servicios: archivos, impresión e Internet`, `Condición: dos zonas separadas y acceso para visitantes`],
    }
  }
  if (code === 'MTCS-RA-1.2') {
    const second = 20 + (seed % 170)
    const hostA = 28 + (seed % 17)
    const hostB = 12 + (seed % 9)
    return {
      title: `Datos de red ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Red base: 192.168.${second}.0/24`, `Subred A: ${hostA} hosts`, `Subred B: ${hostB} hosts`, `Equipo con falla: 192.168.${second}.${200 + (seed % 30)}/24`, `Gateway registrado en el equipo: 192.168.${second}.1`],
    }
  }
  if (code === 'MTCS-RA-3.1') {
    const places = ['laboratorio de cómputo', 'biblioteca escolar', 'cooperativa de ahorro', 'tienda en línea', 'consultorio médico', 'gimnasio']
    const sets = [['letras minúsculas', 26], ['letras minúsculas y dígitos', 36], ['letras mayúsculas, minúsculas y dígitos', 62], ['letras, dígitos y símbolos', 94]]
    const chars = sets[(seed >>> 3) % sets.length]
    const length = 6 + ((seed >>> 5) % 7)
    const attempts = [1000, 100000, 1000000000][(seed >>> 7) % 3]
    return {
      values: { length, charset: chars[1], attempts },
      title: `Sistema ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Sistema: control de acceso de un ${places[seed % places.length]}`, `Usuarios registrados: ${20 + (seed % 80)}`, `Longitud de contraseña: ${length} caracteres`, `Caracteres permitidos: ${chars[0]} (${chars[1]})`, `Intentos por segundo de un atacante: ${attempts}`],
    }
  }
  if (code === 'MTCS-RA-3.2') {
    const places = ['laboratorio de cómputo', 'biblioteca escolar', 'cooperativa de ahorro', 'tienda en línea', 'consultorio médico', 'gimnasio']
    const names = ['ana', 'luis', 'sofia', 'pedro', 'carla', 'diego', 'elena', 'marco', 'rosa', 'tomas']
    const users = [0, 1, 2, 3].map((step) => names[(seed + step * 3) % names.length])
    const log = Array.from({ length: 8 }, (_, index) => users[(seed >>> (index + 2)) % users.length])
    const fails = Array.from({ length: 6 }, (_, index) => ((seed >>> (index * 3)) % 10) + 1)
    const key = `Acceso${String(1000 + (seed % 9000))}`
    const maxAttempts = 3 + (seed % 3)
    const threshold = 4 + ((seed >>> 4) % 3)
    return {
      values: { users, key, maxAttempts, log, fails, threshold },
      title: `Escenario ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Sistema: control de acceso de un ${places[seed % places.length]}`, `Usuarios autorizados: ${users.join(', ')} · Clave: ${key}`, `Intentos antes de bloquear la cuenta: ${maxAttempts}`, `Registros del día: ${log.join(', ')}`, `Intentos fallidos por equipo: ${fails.join(', ')} · sospechoso desde ${threshold} fallos`],
    }
  }
  if (code === 'MTCS-RA-2.2') {
    const organizations = ['clínica dental con expedientes electrónicos', 'tienda en línea de refacciones', 'despacho contable con declaraciones de clientes', 'escuela con plataforma de calificaciones', 'cibercafé con servicio de impresión', 'farmacia con sistema de inventario y ventas']
    const incidents = ['se cortó la energía y el servidor no volvió a encender', 'un ransomware cifró la carpeta compartida', 'se detectaron cambios no autorizados en precios o registros', 'el disco del servidor principal falló sin aviso', 'un empleado instaló software sin licencia que desactivó el antivirus']
    const maxHours = [1, 2, 4, 8][seed % 4]
    return {
      values: { maxHours },
      title: `Organización ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Organización: ${organizations[seed % organizations.length]}`, `Usuarios: ${5 + (seed % 26)} · Equipos: ${4 + (seed % 19)} · Servidores: ${1 + (seed % 2)}`, `Incidente reciente: ${incidents[seed % incidents.length]}`, `Tiempo máximo sin servicio aceptado: ${maxHours} h`],
    }
  }
  const cases = [
    'Un usuario abrió un archivo adjunto inesperado y después varios documentos dejaron de abrir.',
    'Una cuenta con permisos administrativos fue compartida y se detectaron cambios fuera del horario laboral.',
    'Un equipo sin actualizaciones se conectó a una red pública y comenzó a enviar tráfico inusual.',
    'Una memoria USB desconocida fue conectada a un equipo que almacena información importante.',
  ]
  return { title: `Caso ${String(seed % 997).padStart(3, '0')}`, lines: [cases[seed % cases.length], 'Analiza únicamente la información disponible y señala también qué datos investigarías.'] }
}
