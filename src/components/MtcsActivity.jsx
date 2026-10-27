import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, BookOpen, CheckCircle2, Network, Save, Send, ShieldCheck, Terminal, Upload } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { uploadSubmissionFile } from '../lib/upload'

export const mtcsContent = {
  'MTCS-RA-1.1': {
    label: 'MTCS · R.A. 1.1',
    materialTitle: 'Comunicación y componentes de una red',
    intro: 'Revisa cada bloque antes de resolver la actividad. La información explica los conceptos; las decisiones del diseño las tomarás tú.',
    lessons: [
      ['1. ¿Cómo se comunica una red?', 'Una red conecta dispositivos para intercambiar información. El mensaje se divide en datos que viajan por un medio y siguen reglas llamadas protocolos. El rendimiento depende del ancho de banda, la latencia, el medio y la cantidad de tráfico.'],
      ['2. Componentes y conexiones', 'Los equipos finales generan o reciben datos. Los dispositivos intermediarios conectan y dirigen el tráfico. El medio puede ser cobre, fibra óptica o inalámbrico. Cada elección responde a distancia, velocidad, interferencia, costo y seguridad.'],
      ['3. Clientes, servidores y protocolos', 'Un cliente solicita un servicio y un servidor lo proporciona. Los protocolos permiten que ambos interpreten la información de la misma manera. En una comunicación intervienen varias reglas, no un solo protocolo.'],
      ['4. Redes inalámbricas y móviles', 'Una red inalámbrica facilita la movilidad, pero requiere planear cobertura, interferencias, capacidad y protección del acceso. La comodidad no sustituye una configuración segura.'],
      ['5. Red doméstica y medios', 'Una red doméstica suele integrar módem u ONT, router, punto de acceso, cableado y equipos finales. El medio adecuado se selecciona según el entorno y la necesidad de conexión.'],
      ['6. Modelos de comunicación', 'Los modelos organizan las funciones de red por capas. Esto ayuda a explicar el recorrido de la información y a localizar fallas sin revisar todo al mismo tiempo.'],
    ],
    example: 'Ejemplo: en un aula con computadoras fijas, impresora compartida y dispositivos móviles, el diseño puede combinar cableado para los equipos que requieren estabilidad y conexión inalámbrica para movilidad. La justificación debe explicar por qué cada componente y medio es adecuado.',
    taskTitle: 'Actividad de evaluación: crea el diagrama de una red funcional',
    taskIntro: 'Diseña en Packet Tracer la red del escenario asignado y explica aquí tus decisiones. Valor máximo: 60 puntos.',
    fields: [
      ['networkType', '¿Qué tipo de red implementarías y por qué?'],
      ['devices', 'Lista los dispositivos finales e intermediarios necesarios. Indica la función de cada uno.'],
      ['topology', 'Describe cómo conectarías los equipos. Incluye un diagrama usando texto, flechas o una descripción ordenada.'],
      ['media', 'Selecciona el medio de conexión para cada zona y justifica tus elecciones.'],
      ['protocols', 'Menciona los protocolos o servicios necesarios y explica para qué se usaría cada uno.'],
      ['wireless', 'Explica cómo configurarías la conexión inalámbrica y qué cuidados aplicarías.'],
      ['performance', 'Identifica dos factores que podrían disminuir el rendimiento y propón una solución para cada uno.'],
      ['test', 'Describe cómo comprobarías que la red funciona correctamente.'],
    ],
  },
  'MTCS-RA-1.2': {
    label: 'MTCS · R.A. 1.2',
    materialTitle: 'Direccionamiento y enrutamiento IPv4',
    intro: 'Avanza en orden. Los ejemplos muestran el procedimiento, pero deberás aplicarlo a una red diferente.',
    lessons: [
      ['1. Capa de acceso', 'La capa de acceso permite que un dispositivo se conecte al medio local y entregue tramas dentro de la red. Aquí intervienen las interfaces, direcciones físicas y dispositivos como switches y puntos de acceso.'],
      ['2. Propósito de IP', 'IP permite identificar origen y destino para transportar paquetes entre redes. Una dirección IPv4 tiene 32 bits divididos en cuatro octetos. La máscara separa la parte de red de la parte de host.'],
      ['3. Unicast, broadcast y multicast', 'Unicast comunica un origen con un destino; broadcast envía a todos los equipos de la red local; multicast entrega a un grupo específico de receptores.'],
      ['4. Segmentación', 'Dividir una red en subredes reduce dominios de broadcast, organiza equipos y permite aplicar controles. Cada subred necesita dirección de red, rango válido de hosts y dirección de broadcast.'],
      ['5. Puerta de enlace y enrutamiento', 'Un equipo envía a la puerta de enlace los paquetes cuyo destino está fuera de su red. El router consulta su tabla de enrutamiento para seleccionar el siguiente camino.'],
      ['6. IPv6 y DHCP', 'IPv6 amplía el espacio de direcciones y mejora la escalabilidad. DHCP asigna automáticamente parámetros como dirección IP, máscara, puerta de enlace y DNS.'],
    ],
    example: 'Ejemplo: para 192.168.10.0/24, la dirección de red es 192.168.10.0, los hosts válidos van de 192.168.10.1 a 192.168.10.254 y el broadcast es 192.168.10.255. Al crear subredes, esos límites cambian según la nueva máscara.',
    taskTitle: 'Actividad de evaluación: reporte de direccionamiento y enrutamiento',
    taskIntro: 'Prepara un reporte en PDF con los datos que te asignó la plataforma y explica tus procedimientos. Valor máximo: 60 puntos.',
    fields: [
      ['analysis', 'Explica qué información proporciona la dirección de red y la máscara asignadas.'],
      ['subnetA', 'Calcula para la Subred A: prefijo, máscara, dirección de red, primer host, último host y broadcast.'],
      ['subnetB', 'Calcula para la Subred B: prefijo, máscara, dirección de red, primer host, último host y broadcast.'],
      ['allocation', 'Asigna direcciones a router, servidor y dos equipos de cada subred. No repitas direcciones reservadas.'],
      ['gateway', 'Indica la puerta de enlace de cada subred y explica su función.'],
      ['traffic', 'Explica el recorrido de un paquete entre un equipo de la Subred A y otro de la Subred B.'],
      ['diagnosis', 'Un equipo tiene la dirección indicada en el caso, pero no navega. Propón un diagnóstico ordenado y una solución.'],
      ['ipv6', 'Explica dos razones para adoptar IPv6 y una diferencia respecto a IPv4.'],
    ],
  },
  'MTCS-RA-2.1': {
    label: 'MTCS · R.A. 2.1',
    materialTitle: 'Primeros fundamentos de ciberseguridad',
    intro: 'Este bloque inicia el R.A. 2.1. Lee los conceptos y aplícalos al análisis del caso asignado.',
    lessons: [
      ['1. Ciberseguridad', 'La ciberseguridad protege información, dispositivos, servicios y redes frente a acciones accidentales o intencionales. No depende de una sola herramienta: combina personas, procesos y tecnología.'],
      ['2. Amenaza, vulnerabilidad y riesgo', 'Una amenaza puede causar daño; una vulnerabilidad es una debilidad; el riesgo surge cuando una amenaza puede aprovechar una vulnerabilidad y producir un impacto. No son sinónimos.'],
      ['3. Principios de seguridad', 'La confidencialidad limita el acceso; la integridad evita alteraciones no autorizadas; la disponibilidad mantiene información y servicios accesibles cuando se requieren.'],
      ['4. Amenazas internas y externas', 'Una amenaza interna proviene de alguien con acceso legítimo o cercano a la organización. Una externa se origina fuera de ella. Ambas pueden ser deliberadas o accidentales.'],
      ['5. Controles de seguridad', 'Los controles preventivos buscan evitar incidentes; los detectivos identifican lo ocurrido; los correctivos ayudan a recuperar la operación y reducir las consecuencias.'],
    ],
    example: 'Ejemplo: compartir una contraseña es una vulnerabilidad de operación; el acceso indebido es la amenaza y la exposición o modificación de datos representa el posible impacto. Cambiar contraseñas, limitar permisos y revisar registros son controles distintos.',
    taskTitle: 'Actividad de evaluación: presentación sobre fundamentos de ciberseguridad',
    taskIntro: 'Prepara una presentación electrónica basada en el caso asignado. Puedes entregarla como PPTX o PDF. Valor máximo: 60 puntos.',
    fields: [
      ['cover', 'Diapositiva 1. Escribe el título de tu presentación y los datos que incluirás en la portada.'],
      ['concept', 'Diapositiva 2. Explica qué es la ciberseguridad con tus propias palabras.'],
      ['principles', 'Diapositiva 3. Explica confidencialidad, integridad y disponibilidad mediante ejemplos.'],
      ['case', 'Diapositiva 4. Resume el caso asignado e identifica los recursos que necesitan protección.'],
      ['threats', 'Diapositiva 5. Identifica amenazas internas, externas y vulnerabilidades presentes.'],
      ['attacks', 'Diapositiva 6. Explica qué malware, engaño o ataque podría aprovechar esas debilidades.'],
      ['protection', 'Diapositiva 7. Propón autenticación, permisos, cifrado u otros controles adecuados.'],
      ['closing', 'Diapositiva 8. Escribe una conclusión y tres recomendaciones concretas.'],
    ],
  },
  'MTCS-RA-2.2': {
    label: 'MTCS · R.A. 2.2',
    materialTitle: 'Principios y tecnologías de confidencialidad',
    intro: 'Este R.A. muestra cómo se comprueba que la información no fue alterada, cómo se mantiene disponible y cómo se defienden equipos, servidores y redes. Al final elaborarás un reporte con el caso asignado.',
    lessons: [
      ['1. Hash y técnica salting', 'Un algoritmo de hash, como SHA-256, convierte cualquier dato en un resumen de longitud fija. Si cambia un solo carácter, el resumen cambia por completo, por eso sirve para verificar integridad. Las contraseñas se guardan como hash, nunca en texto claro; la técnica salting agrega un valor aleatorio distinto a cada contraseña antes de calcular el hash, para que dos contraseñas iguales no produzcan el mismo resultado y no puedan atacarse con tablas precalculadas. MD5 y SHA-1 ya no se consideran seguros.'],
      ['2. HMAC, firmas digitales y certificados', 'HMAC combina un hash con una clave secreta compartida: comprueba que el mensaje no cambió y que lo envió alguien que conoce la clave. La firma digital usa la clave privada del emisor y se verifica con su clave pública; aporta integridad, autenticidad y no repudio. Un certificado digital, emitido por una autoridad certificadora, asocia una clave pública con una persona o un sitio; es lo que permite que HTTPS confirme que un sitio es quien dice ser. En las bases de datos, la integridad se protege con validaciones, llaves primarias y foráneas, restricciones y respaldos.'],
      ['3. Disponibilidad y alta disponibilidad', 'La disponibilidad asegura que la información y los servicios funcionen cuando se necesitan. La alta disponibilidad busca eliminar puntos únicos de falla mediante redundancia: discos en RAID, fuentes de energía y enlaces duplicados, servidores en clúster y balanceo de carga. Se mide en porcentaje de tiempo en servicio; por ejemplo, 99.999 % («cinco nueves») equivale a poco más de 5 minutos fuera de servicio al año.'],
      ['4. Defensa en profundidad, incidentes y recuperación', 'La defensa en profundidad coloca varias capas de protección (políticas, seguridad física, red, equipo, aplicación y datos) para que la falla de una no exponga todo. La respuesta a incidentes sigue fases: preparación; detección y análisis; contención, erradicación y recuperación; y actividades posteriores para aprender del incidente. El plan de recuperación tras un desastre define respaldos, sitios alternos y dos metas: RPO, cuánta información se puede perder, y RTO, en cuánto tiempo debe volver el servicio.'],
      ['5. Defensa de sistemas y dispositivos', 'Protección del host: actualizaciones, antivirus o EDR, firewall local, cuentas sin privilegios y cifrado de disco. Protección del servidor: desactivar servicios innecesarios, mínimo privilegio, registros (bitácoras) y respaldos. Protección de la red: firewall, segmentación con VLAN, sistemas de detección o prevención de intrusos (IDS/IPS), VPN y redes inalámbricas con WPA2 o WPA3. Seguridad física: control de acceso a los sitios, cámaras, candados y respaldo de energía (UPS).'],
      ['6. Dominio de la ciberseguridad', 'Las vulnerabilidades públicas se registran con un identificador CVE y se califican con CVSS para priorizar su corrección. El trabajo en ciberseguridad exige ética: actuar solo con autorización por escrito, proteger la privacidad, no causar daño y reportar los hallazgos de forma responsable. Algunas herramientas comunes son Nmap para descubrir equipos y puertos, Wireshark para analizar tráfico, gestores de contraseñas y escáneres de vulnerabilidades; usarlas sin permiso puede ser un delito.'],
    ],
    example: 'Ejemplo: una papelería guarda las contraseñas de sus empleados con hash y salting, firma digitalmente sus facturas electrónicas y usa un certificado HTTPS en su tienda en línea (integridad). Duplica su servicio de Internet y respalda sus ventas cada noche en la nube (disponibilidad y recuperación). Protege la caja con antivirus y una cuenta sin privilegios, separa la red de clientes de la red interna y mantiene el módem bajo llave (defensa en profundidad).',
    taskTitle: 'Actividad de evaluación: reporte de principios y tecnologías de confidencialidad',
    taskIntro: 'Elabora un reporte en PDF sobre la organización que te asignó la plataforma. Usa estas secciones como guía y entrega el archivo al terminar. Valor máximo: 60 puntos.',
    fields: [
      ['context', 'Describe la organización asignada, la información que maneja y los servicios que no pueden detenerse.'],
      ['integrity', 'Controles de integridad: explica cómo usarías hash con salting, HMAC o firmas digitales y certificados en este caso.'],
      ['database', 'Integridad en la base de datos: indica qué validaciones, llaves, restricciones o respaldos aplicarías.'],
      ['availability', 'Disponibilidad: identifica puntos únicos de falla y propón medidas de alta disponibilidad.'],
      ['incident', 'Respuesta a incidentes y recuperación: describe las fases ante el incidente asignado y define el RPO y el RTO.'],
      ['defense', 'Defensa de sistemas: propón medidas para host, servidor, red y seguridad física, organizadas como defensa en profundidad.'],
      ['domain', 'Dominio de ciberseguridad: menciona una vulnerabilidad (con su CVE si la conoces), una herramienta que usarías y los principios éticos que respetarías.'],
      ['conclusion', 'Conclusión: resume las tres medidas más importantes y por qué.'],
    ],
  },
  'MTCS-RA-3.1': {
    label: 'MTCS · R.A. 3.1',
    materialTitle: 'Fundamentos y lenguajes de programación',
    intro: 'Este R.A. enseña a darle instrucciones a la computadora con Python: variables, tipos de datos y operadores. Al final elaborarás un reporte con el escenario asignado.',
    lessons: [
      ['1. Programa, algoritmo y lenguaje', 'Un programa es un conjunto de instrucciones; un algoritmo son los pasos ordenados para resolver un problema. Todo programa recibe datos (entrada), los transforma (proceso) y muestra un resultado (salida). Python es un lenguaje de alto nivel e interpretado.'],
      ['2. Archivo fuente y herramientas', 'El archivo fuente es un archivo de texto (.py) con las instrucciones. Se escribe en un editor o IDE y se ejecuta con el intérprete, por ejemplo con el comando python ciber_lab.py en la terminal.'],
      ['3. Sintaxis y semántica', 'La sintaxis son las reglas de escritura: si falla, el programa no arranca (SyntaxError). La semántica es el significado: un error de ejecución detiene el programa en una línea y un error de lógica da un resultado incorrecto sin mostrar mensaje.'],
      ['4. Variables y literales', 'Una variable es un espacio con nombre que guarda un dato (intentos = 3). Los literales tienen tipo: int (15), float (3.14), str ("Ana") y bool (True o False). input() siempre entrega texto; se convierte con int() o float().'],
      ['5. Operadores', 'Aritméticos: + - * / // % **. De comparación: == != > < >= <=, que dan True o False. Lógicos: and, or y not. Se resuelven con la misma prioridad que en matemáticas; los paréntesis cambian el orden.'],
    ],
    example: 'Ejemplo: con 62 caracteres posibles y contraseñas de 8 caracteres, caracteres ** longitud da 218,340,105,584,896 combinaciones; dividido entre mil millones de intentos por segundo, un atacante tardaría unas 60 horas y 39 minutos. Con longitud >= 12 se obtiene True o False para saber si la contraseña es segura.',
    taskTitle: 'Actividad de evaluación: reporte de fundamentos y lenguajes de programación',
    taskIntro: 'Elabora un reporte en PDF con el sistema asignado por la plataforma. Incluye tu código en Python y capturas de la salida. Valor máximo: 60 puntos.',
    fields: [
      ['context', 'Describe el sistema asignado y para qué sirve programar en su seguridad.'],
      ['concepts', 'Conceptos: explica qué es un programa, un algoritmo, entrada-proceso-salida y la diferencia entre archivo fuente y programa ejecutable.'],
      ['language', 'Lenguaje y herramientas: indica que usaste Python, si es interpretado o compilado y qué editor, intérprete o terminal utilizaste.'],
      ['variables', 'Variables y literales: describe las variables de tu programa con los datos asignados, su tipo (str, int, float, bool) y por qué elegiste esos nombres.'],
      ['operators', 'Operadores: muestra los cálculos con los datos asignados (combinaciones, segundos, horas y minutos) y las comparaciones o condiciones lógicas, con sus resultados.'],
      ['errors', 'Errores: describe un error de sintaxis y uno de ejecución o de lógica que cometiste, qué mensaje apareció y cómo lo corregiste.'],
      ['conclusion', 'Conclusión: explica qué otra tarea de seguridad te gustaría automatizar con programación y qué necesitarías aprender.'],
    ],
  },
  'MTCS-RA-3.2': {
    label: 'MTCS · R.A. 3.2',
    materialTitle: 'Estructuras de flujo de control y funciones',
    intro: 'Este R.A. enseña a controlar el flujo de un programa en Python: decidir, repetir, trabajar con listas, organizar el código en funciones y atrapar errores. Al final elaborarás un reporte con el escenario asignado.',
    lessons: [
      ['1. Condiciones', 'if ejecuta un bloque solo si la condición es True; elif revisa otra condición y else cubre el resto. and exige que se cumplan las dos condiciones y or basta con una. El orden importa: primero se revisa el bloqueo y después la clave.'],
      ['2. Bucles', 'while repite mientras la condición sea True (útil para pedir la clave hasta 3 veces). for recorre una lista o un range(). break sale del ciclo y continue salta a la siguiente iteración. Algo debe cambiar dentro del while para que termine.'],
      ['3. Operadores bit a bit y listas', 'Con | se juntan permisos, con & se revisa uno y con ^ se quita. Una lista guarda muchos datos: append agrega, count cuenta, sorted ordena y for la recorre para buscar el mayor o filtrar sospechosos.'],
      ['4. Funciones', 'def crea una función con parámetros; al llamarla se mandan argumentos y return entrega el resultado. Una función puede llamar a otra y los parámetros pueden tener valor por omisión.'],
      ['5. Excepciones', 'try contiene lo que puede fallar y except atrapa el error (ValueError, ZeroDivisionError). else corre si no hubo error y finally siempre. raise lanza una excepción cuando un dato no tiene sentido.'],
    ],
    example: 'Ejemplo: un while pide la clave hasta 3 veces; si el usuario acierta, break termina el ciclo y se muestra «Acceso concedido»; si falla 3 veces, se muestra «Cuenta bloqueada». La función es_segura(clave) regresa True si la clave tiene 12 caracteres o más, y un try/except evita que el programa se caiga si escriben letras donde van números.',
    taskTitle: 'Actividad de evaluación: reporte de flujo de control y funciones',
    taskIntro: 'Elabora un reporte en PDF con el escenario asignado por la plataforma. Incluye tu código en Python y capturas de la salida de cada programa. Valor máximo: 60 puntos.',
    fields: [
      ['context', 'Describe el escenario asignado y qué debe resolver tu programa.'],
      ['conditions', 'Condiciones: muestra el programa de acceso con if, elif, else y operadores lógicos (and, or) usando los usuarios y la clave asignados; explica el orden de las condiciones.'],
      ['loops', 'Bucles: muestra cómo pides la clave con while hasta el límite de intentos asignado, con break, y un for que recorra los registros del día.'],
      ['lists', 'Listas y algoritmos: con los registros asignados, cuenta los accesos de un usuario, quita repetidos, ordénalos y encuentra el mayor número de fallos sin usar max(). Si usaste operadores bit a bit para permisos, explícalos.'],
      ['functions', 'Funciones: describe al menos dos funciones tuyas, sus parámetros, su return y cómo se comunican entre ellas.'],
      ['exceptions', 'Excepciones y depuración: muestra un try/except que evite que el programa se caiga y describe un error de sintaxis, de ejecución o de lógica que corregiste.'],
      ['conclusion', 'Conclusión: explica qué parte del flujo de control te pareció más útil para la seguridad y por qué.'],
    ],
  },
}

function hash(text) {
  let value = 2166136261
  for (let index = 0; index < text.length; index += 1) value = Math.imul(value ^ text.charCodeAt(index), 16777619)
  return value >>> 0
}

function assignmentFor(studentId, assessmentId, code) {
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
    const chars = sets[(seed >> 3) % sets.length]
    return {
      title: `Sistema ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Sistema: control de acceso de un ${places[seed % places.length]}`, `Usuarios registrados: ${20 + (seed % 80)}`, `Longitud de contraseña: ${6 + ((seed >> 5) % 7)} caracteres`, `Caracteres permitidos: ${chars[0]} (${chars[1]})`, `Intentos por segundo de un atacante: ${[1000, 100000, 1000000000][(seed >> 7) % 3]}`],
    }
  }
  if (code === 'MTCS-RA-3.2') {
    const places = ['laboratorio de cómputo', 'biblioteca escolar', 'cooperativa de ahorro', 'tienda en línea', 'consultorio médico', 'gimnasio']
    const names = ['ana', 'luis', 'sofia', 'pedro', 'carla', 'diego', 'elena', 'marco', 'rosa', 'tomas']
    const users = [0, 1, 2, 3].map((step) => names[(seed + step * 3) % names.length])
    const log = Array.from({ length: 8 }, (_, index) => users[(seed >> (index + 2)) % users.length])
    const fails = Array.from({ length: 6 }, (_, index) => ((seed >> (index * 3)) % 10) + 1)
    return {
      title: `Escenario ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Sistema: control de acceso de un ${places[seed % places.length]}`, `Usuarios autorizados: ${users.join(', ')} · Clave: Acceso${String(1000 + (seed % 9000))}`, `Intentos antes de bloquear la cuenta: ${3 + (seed % 3)}`, `Registros del día: ${log.join(', ')}`, `Intentos fallidos por equipo: ${fails.join(', ')} · sospechoso desde ${4 + ((seed >> 4) % 3)} fallos`],
    }
  }
  if (code === 'MTCS-RA-2.2') {
    const organizations = ['clínica dental con expedientes electrónicos', 'tienda en línea de refacciones', 'despacho contable con declaraciones de clientes', 'escuela con plataforma de calificaciones', 'cibercafé con servicio de impresión', 'farmacia con sistema de inventario y ventas']
    const incidents = ['se cortó la energía y el servidor no volvió a encender', 'un ransomware cifró la carpeta compartida', 'se detectaron cambios no autorizados en precios o registros', 'el disco del servidor principal falló sin aviso', 'un empleado instaló software sin licencia que desactivó el antivirus']
    return {
      title: `Organización ${String(seed % 997).padStart(3, '0')}`,
      lines: [`Organización: ${organizations[seed % organizations.length]}`, `Usuarios: ${5 + (seed % 26)} · Equipos: ${4 + (seed % 19)} · Servidores: ${1 + (seed % 2)}`, `Incidente reciente: ${incidents[seed % incidents.length]}`, `Tiempo máximo sin servicio aceptado: ${[1, 2, 4, 8][seed % 4]} h`],
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

const mtcsDeliverables = {
  'MTCS-RA-1.1': { label: 'Diagrama final de Packet Tracer', accept: '.pkt,application/octet-stream', extensions: ['pkt'], help: 'Archivo .pkt · máximo 20 MB' },
  'MTCS-RA-1.2': { label: 'Reporte final', accept: '.pdf,application/pdf', extensions: ['pdf'], help: 'Archivo PDF · máximo 20 MB' },
  'MTCS-RA-2.2': { label: 'Reporte final', accept: '.pdf,application/pdf', extensions: ['pdf'], help: 'Archivo PDF · máximo 20 MB' },
  'MTCS-RA-3.1': { label: 'Reporte final', accept: '.pdf,application/pdf', extensions: ['pdf'], help: 'Archivo PDF · máximo 20 MB' },
  'MTCS-RA-3.2': { label: 'Reporte final', accept: '.pdf,application/pdf', extensions: ['pdf'], help: 'Archivo PDF · máximo 20 MB' },
  'MTCS-RA-2.1': { label: 'Presentación electrónica', accept: '.pptx,.pdf,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/pdf', extensions: ['pptx', 'pdf'], help: 'Archivo PPTX o PDF · máximo 20 MB' },
}

export default function MtcsActivity({ assessment, session, onBack }) {
  const definition = mtcsContent[assessment.activityCode]
  const assignment = useMemo(() => assignmentFor(session.id, assessment.id, assessment.activityCode), [session.id, assessment.id, assessment.activityCode])
  const [tab, setTab] = useState('material')
  const [answers, setAnswers] = useState({})
  const [packetTracerFiles, setPacketTracerFiles] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [status, setStatus] = useState('loading')
  const [message, setMessage] = useState('')
  const [file, setFile] = useState(null)
  const [storedFile, setStoredFile] = useState({ path: '', name: '' })
  const deliverable = mtcsDeliverables[assessment.activityCode]

  useEffect(() => {
    if (session.preview) { setStatus('ready'); return undefined }
    let active = true
    supabase.from('submissions').select('answers, submitted_at, file_path, original_filename').eq('assessment_id', assessment.id).maybeSingle().then(({ data, error }) => {
      if (!active) return
      if (error) { setMessage(error.message); setStatus('error'); return }
      setAnswers(data?.answers?.responses || {})
      setPacketTracerFiles(data?.answers?.packet_tracer || {})
      setStoredFile({ path: data?.file_path || '', name: data?.original_filename || '' })
      setSubmitted(Boolean(data?.submitted_at))
      setStatus('ready')
    })
    return () => { active = false }
  }, [assessment.id])

  const complete = definition.fields.every(([key]) => String(answers[key] || '').trim().length >= 12)

  async function save(deliver = false) {
    if (session.preview) { setMessage('Esta es una vista previa. Las respuestas no se guardan ni generan entregas.'); setStatus('ready'); return }
    if (deliver && !complete) { setMessage('Completa todas las respuestas antes de entregar. Revisa que estén explicadas, no solo contestadas con una palabra.'); setStatus('error'); return }
    if (deliver && deliverable && !file && !storedFile.path) { setMessage(`Adjunta tu ${deliverable.label.toLowerCase()} antes de entregar.`); setStatus('error'); return }
    setStatus('saving'); setMessage('')
    const { data: authData } = await supabase.auth.getUser()
    let uploaded = storedFile
    if (file) {
      const extension = file.name.split('.').pop().toLowerCase()
      if (!deliverable.extensions.includes(extension)) { setMessage(`El archivo debe ser ${deliverable.extensions.map(item => `.${item}`).join(' o ')}.`); setStatus('error'); return }
      if (file.size > 20 * 1024 * 1024) { setMessage('El archivo supera el límite de 20 MB.'); setStatus('error'); return }
      const path = `${authData.user.id}/${assessment.id}/final/entrega.${extension}`
      try { await uploadSubmissionFile(path, file, extension === 'pkt' ? 'application/octet-stream' : undefined) } catch (uploadError) { setMessage(uploadError.message || 'No fue posible subir el archivo.'); setStatus('error'); return }
      uploaded = { path, name: file.name }
      setStoredFile(uploaded)
    }
    const payload = { assessment_id: assessment.id, student_id: authData.user.id, answers: { activity: assessment.activityCode, assigned_case: assignment, responses: answers, ...(Object.keys(packetTracerFiles).length ? { packet_tracer: packetTracerFiles } : {}) }, file_path: uploaded.path || null, original_filename: uploaded.name || null, submitted_at: deliver ? new Date().toISOString() : null }
    const { error } = await supabase.from('submissions').upsert(payload, { onConflict: 'assessment_id,student_id' })
    if (error) { setMessage(error.message || 'No fue posible guardar.'); setStatus('error'); return }
    setSubmitted(deliver)
    setMessage(deliver ? 'Actividad entregada correctamente.' : 'Avance guardado correctamente.')
    setStatus(deliver ? 'submitted' : 'ready')
  }

  if (!definition) return null
  if (status === 'loading') return <section className="panel page-panel activity-workspace"><div className="loading-state">Preparando MTCS…</div></section>

  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a evaluaciones</button>
    <div className="activity-hero"><div><span className="eyebrow">{definition.label}</span><h1>{definition.materialTitle}</h1><p>{definition.intro}</p></div><div className="mtcs-value"><strong>60</strong><span>PUNTOS MÁX.</span></div></div>
    <nav className="mtcs-tabs"><button className={tab === 'material' ? 'active' : ''} onClick={() => setTab('material')}><BookOpen size={17} /> Material y ejemplo</button><button className={tab === 'activity' ? 'active' : ''} onClick={() => setTab('activity')}><ShieldCheck size={17} /> Actividad</button></nav>

    {tab === 'material' ? <div className="mtcs-material"><div className="lesson-grid">{definition.lessons.map(([title, text]) => <article key={title}><span>{title.split('.')[0]}</span><div><h3>{title.replace(/^\d+\.\s*/, '')}</h3><p>{text}</p></div></article>)}</div><div className="worked-example"><strong>Ejemplo para comprender</strong><p>{definition.example}</p></div><button className="primary mtcs-continue" onClick={() => { setTab('activity'); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>Continuar a la actividad</button></div> : <div className="mtcs-activity">
      <div className="assigned-case"><span className="eyebrow">Datos asignados</span><h2>{assignment.title}</h2><ul>{assignment.lines.map(line => <li key={line}>{line}</li>)}</ul></div>
      <div className="stage-heading"><h2>{definition.taskTitle}</h2><p>{definition.taskIntro}</p></div>
      <fieldset disabled={submitted || status === 'saving'} className="mtcs-form">{definition.fields.map(([key, label], index) => <label key={key}><span><b>{index + 1}</b>{label}</span><textarea rows="4" value={answers[key] || ''} onChange={event => setAnswers(current => ({ ...current, [key]: event.target.value }))} placeholder="Escribe y explica tu respuesta…" /></label>)}</fieldset>
      {deliverable && <label className="mtcs-final-upload"><Upload size={22} /><span><strong>{file?.name || storedFile.name || deliverable.label}</strong><small>{deliverable.help}</small></span><input type="file" accept={deliverable.accept} disabled={submitted || status === 'saving'} onChange={event => setFile(event.target.files?.[0] || null)} /></label>}
      {message && <div className={status === 'error' ? 'form-error asin-message' : 'submission-success asin-message'}>{message}</div>}
      <footer className="activity-footer"><span className="mtcs-progress">{definition.fields.filter(([key]) => String(answers[key] || '').trim().length >= 12).length} de {definition.fields.length} respuestas completas</span><div className="activity-footer-actions">{!submitted && <button className="secondary" onClick={() => save(false)} disabled={status === 'saving'}><Save size={17} /> Guardar avance</button>}<button className="primary" onClick={() => save(true)} disabled={submitted || status === 'saving'}>{submitted ? <CheckCircle2 size={17} /> : <Send size={17} />}{submitted ? 'Actividad entregada' : 'Entregar actividad'}</button></div></footer>
    </div>}
  </section>
}

const ra11Checks = [
  { question: '¿Qué elemento solicita normalmente un servicio en la red?', options: ['Cliente', 'Medio', 'Router'], correct: 'Cliente' },
  { question: '¿Cuál es un dispositivo intermediario?', options: ['Switch', 'Teclado', 'Documento'], correct: 'Switch' },
  { question: '¿Qué permite que dos equipos interpreten la comunicación con las mismas reglas?', options: ['Un protocolo', 'El tamaño del monitor', 'La marca del equipo'], correct: 'Un protocolo' },
  { question: '¿Qué aspecto debe revisarse al planear una red inalámbrica?', options: ['Cobertura e interferencia', 'Color de los cables', 'Fondo de pantalla'], correct: 'Cobertura e interferencia' },
  { question: '¿Qué medio suele ser adecuado para movilidad?', options: ['Inalámbrico', 'Fibra sin equipos', 'Cable desconectado'], correct: 'Inalámbrico' },
  { question: '¿Para qué sirven las capas de un modelo de red?', options: ['Organizar funciones y localizar fallas', 'Aumentar el tamaño de archivos', 'Eliminar protocolos'], correct: 'Organizar funciones y localizar fallas' },
]

const ra11ExtraChecks = [
  [
    { question: '¿Qué necesita todo mensaje para llegar correctamente?', options: ['Origen, destino, medio y reglas', 'Solo electricidad', 'Únicamente Internet'], correct: 'Origen, destino, medio y reglas' },
    { question: '¿Qué situación puede disminuir el rendimiento?', options: ['Demasiado tráfico y alta latencia', 'Nombrar los equipos', 'Usar una carpeta'], correct: 'Demasiado tráfico y alta latencia' },
  ],
  [
    { question: '¿Cuál es un equipo final?', options: ['Computadora', 'Switch', 'Cable UTP'], correct: 'Computadora' },
    { question: '¿Qué elemento transporta físicamente o por ondas la información?', options: ['El medio', 'El usuario', 'La contraseña'], correct: 'El medio' },
  ],
  [
    { question: '¿Qué hace normalmente un servidor?', options: ['Proporciona recursos o servicios', 'Solo solicita servicios', 'Sustituye todo el cableado'], correct: 'Proporciona recursos o servicios' },
    { question: '¿Por qué son necesarios los protocolos?', options: ['Definen reglas comunes de comunicación', 'Cambian el tamaño del monitor', 'Eliminan las direcciones'], correct: 'Definen reglas comunes de comunicación' },
  ],
  [
    { question: '¿Qué puede afectar una señal Wi-Fi?', options: ['Distancia, obstáculos e interferencias', 'El nombre del usuario', 'El formato de un documento'], correct: 'Distancia, obstáculos e interferencias' },
    { question: '¿Qué acción mejora la seguridad inalámbrica?', options: ['Usar cifrado y una clave robusta', 'Compartir la clave públicamente', 'Desactivar toda autenticación'], correct: 'Usar cifrado y una clave robusta' },
  ],
  [
    { question: '¿Qué medio ofrece alta velocidad y resistencia a interferencias?', options: ['Fibra óptica', 'Papel', 'Bluetooth sin adaptador'], correct: 'Fibra óptica' },
    { question: '¿Qué criterio ayuda a elegir un medio?', options: ['Distancia, velocidad, ambiente y costo', 'El color favorito', 'La marca del escritorio'], correct: 'Distancia, velocidad, ambiente y costo' },
  ],
  [
    { question: 'Si falla el cable, ¿qué parte conviene revisar primero?', options: ['Acceso físico al medio', 'Aplicación de correo', 'Diseño del documento'], correct: 'Acceso físico al medio' },
    { question: '¿Qué ventaja ofrece trabajar por capas?', options: ['Diagnosticar una función a la vez', 'Evitar todos los dispositivos', 'No utilizar protocolos'], correct: 'Diagnosticar una función a la vez' },
  ],
]

const ra11Details = [
  ['Emisor: dispositivo que origina la información.', 'Receptor: dispositivo o servicio que debe recibirla.', 'Mensaje: datos que se desean comunicar.', 'Medio: camino por cable, fibra u ondas.', 'Protocolo: reglas que ordenan el intercambio.', 'Ancho de banda es capacidad; latencia es tiempo de respuesta. No significan lo mismo.'],
  ['Equipos finales: computadoras, celulares, impresoras y servidores.', 'Intermediarios: switches, routers y puntos de acceso.', 'El switch conecta equipos dentro de una red local.', 'El router comunica redes diferentes y selecciona rutas.', 'El punto de acceso permite que dispositivos inalámbricos entren a la red.'],
  ['El cliente inicia una solicitud; el servidor procesa y responde.', 'DNS traduce nombres comprensibles a direcciones IP.', 'DHCP entrega parámetros de red automáticamente.', 'HTTP y HTTPS permiten solicitar recursos web.', 'Una comunicación real utiliza varios protocolos de manera coordinada.'],
  ['La cobertura indica hasta dónde llega una señal útil.', 'Paredes, distancia y otros equipos pueden producir pérdida o interferencia.', 'Más usuarios simultáneos significan más capacidad compartida.', 'La autenticación controla quién entra; el cifrado protege la comunicación.', 'La ubicación del punto de acceso influye en cobertura y rendimiento.'],
  ['Cobre: económico y común, pero limitado por distancia e interferencias.', 'Fibra: alta velocidad y largas distancias, con mayor cuidado de instalación.', 'Inalámbrico: movilidad y rapidez de despliegue, pero comparte el aire.', 'La decisión correcta depende del problema, no de escoger siempre el medio más costoso.'],
  ['Las capas separan funciones para comprender y diagnosticar.', 'Las capas inferiores se relacionan con señal, medio y acceso.', 'Las capas intermedias identifican destinos y transportan información.', 'Las capas superiores atienden los servicios que utiliza el usuario.', 'Al diagnosticar se empieza por lo básico y se avanza de manera ordenada.'],
]

const packetTracerPractices = [
  {
    id: 'pt-componentes',
    title: 'Práctica 1 · Construcción de una red local básica',
    related: 'Temas 2 y 3: componentes, conexiones, clientes y servidores',
    goal: 'Construir una red local sencilla, asignar direcciones y comprobar la comunicación entre sus equipos.',
    steps: [
      { title: 'Abre un trabajo nuevo', detail: 'Inicia Packet Tracer. Arriba, haz clic en File y después en New. Si aparece una pregunta para guardar otro trabajo, pide apoyo antes de cerrarlo.', check: 'Debes ver un espacio grande y vacío.' },
      { title: 'Coloca el switch', detail: 'En la parte inferior izquierda, haz clic en Network Devices. Después elige Switches. Busca el modelo 2960, haz clic sobre él y luego haz clic en el centro del espacio blanco.', check: 'Debe aparecer un switch con un nombre parecido a Switch0.' },
      { title: 'Coloca tres computadoras', detail: 'Abajo a la izquierda, haz clic en End Devices. Elige PC y haz clic tres veces en lugares separados del espacio blanco.', check: 'Debes tener PC0, PC1 y PC2.' },
      { title: 'Coloca el servidor', detail: 'Sin salir de End Devices, busca Server. Haz clic en él y colócalo cerca de las computadoras.', check: 'Ahora debes ver cuatro equipos finales y un switch.' },
      { title: 'Elige el cable', detail: 'Abajo, haz clic en Connections, identificado con un rayo. Selecciona Copper Straight-Through; normalmente aparece como una línea negra continua.', check: 'El puntero debe quedar listo para conectar.' },
      { title: 'Conecta la primera computadora', detail: 'Haz clic en PC0 y elige FastEthernet0. Después haz clic en el switch y elige FastEthernet0/1.', check: 'Aparecerá una línea entre PC0 y el switch.' },
      { title: 'Conecta los demás equipos', detail: 'Repite lo anterior: PC1 con FastEthernet0/2, PC2 con FastEthernet0/3 y Server0 con FastEthernet0/4. En cada equipo elige FastEthernet0.', check: 'Espera unos segundos: los puntos de cada cable deben ponerse verdes.' },
      { title: 'Configura la dirección de PC0', detail: 'Haz clic en PC0. Abre la pestaña Desktop y luego IP Configuration. Marca Static. En IPv4 Address escribe el primer host asignado y en Subnet Mask escribe 255.255.255.0. Cierra la ventana con la X.', check: 'La dirección debe quedar completa y sin espacios.' },
      { title: 'Configura PC1, PC2 y Server0', detail: 'Repite Desktop > IP Configuration > Static en cada equipo. Usa un host diferente de los cuatro que te asignó la plataforma. La máscara es 255.255.255.0 en todos.', check: 'Ningún equipo debe tener la misma dirección.' },
      { title: 'Comprueba la configuración', detail: 'Abre PC0 > Desktop > Command Prompt. Escribe ipconfig y presiona Enter.', check: 'La dirección mostrada debe ser la misma que escribiste en PC0.' },
      { title: 'Prueba la comunicación', detail: 'En la misma ventana negra escribe ping, deja un espacio y agrega la dirección de PC1. Presiona Enter. Repite con PC2 y Server0.', check: 'Cada prueba debe mostrar Reply from o Respuesta desde. Si falla la primera vez, repítela una vez.' },
      { title: 'Observa el recorrido', detail: 'Cierra la ventana de PC0. Abajo a la derecha cambia de Realtime a Simulation. En la barra derecha, haz clic en el sobre cerrado Add Simple PDU. Haz clic primero en PC0 y después en Server0. Usa Auto Capture/Play para ver el sobre avanzar.', check: 'La prueba debe terminar correctamente y mostrar una marca verde.' },
      { title: 'Agrega tu identificación', detail: 'Busca Place Note en la barra de herramientas, haz clic en un espacio vacío y escribe exactamente el código que te asignó la plataforma.', check: 'El código debe quedar visible dentro del área de trabajo.' },
      { title: 'Guarda el archivo', detail: 'Arriba haz clic en File > Save As. Elige una carpeta que puedas encontrar y escribe Grupo_Apellido_Practica1. Packet Tracer agregará la terminación .pkt.', check: 'Revisa arriba de la ventana que aparezca el nombre nuevo.' },
    ],
    checks: ['Los cuatro equipos muestran enlace activo.', 'No existen direcciones IP repetidas.', 'Los cuatro destinos responden correctamente.'],
  },
  {
    id: 'pt-inalambrica',
    title: 'Práctica 2 · Red cableada e inalámbrica',
    related: 'Temas 4 y 5: redes inalámbricas, red doméstica y medios',
    goal: 'Integrar dispositivos cableados e inalámbricos y observar cómo cambia el medio de conexión.',
    steps: [
      { title: 'Crea un archivo nuevo', detail: 'Abre Packet Tracer y haz clic en File > New. Trabaja en el espacio blanco.', check: 'El área de trabajo debe estar vacía.' },
      { title: 'Coloca el router inalámbrico', detail: 'Abajo a la izquierda abre Network Devices y después Wireless Devices. Busca Wireless Router o WRT300N, selecciónalo y colócalo en el centro.', check: 'Debe verse un equipo con antenas.' },
      { title: 'Coloca los equipos', detail: 'Abre End Devices. Coloca una PC, una Laptop y un Smartphone. Déjalos separados para distinguir sus conexiones.', check: 'Debes tener cuatro dispositivos en total contando el router.' },
      { title: 'Conecta la computadora por cable', detail: 'Abre Connections con el icono del rayo. Elige Copper Straight-Through. Haz clic en PC0 > FastEthernet0 y después en el router inalámbrico > Ethernet 1.', check: 'La línea debe terminar con puntos verdes después de esperar unos segundos.' },
      { title: 'Abre la configuración del router', detail: 'Haz clic en el router inalámbrico y abre la pestaña GUI. Dentro de la pantalla del router, busca Wireless y luego Basic Wireless Settings.', check: 'Debes encontrar un campo llamado Network Name o SSID.' },
      { title: 'Configura la red local', detail: 'Dentro de GUI abre Setup > Basic Setup. En Local IP Address escribe la dirección de la red asignada terminada en .1. Deja la máscara 255.255.255.0, activa DHCP Server y coloca 100 en Starting IP Address. Haz clic en Save Settings.', check: 'El router debe usar .1 y repartir direcciones a partir de .100.' },
      { title: 'Escribe el nombre de la red', detail: 'En Network Name (SSID) borra el nombre anterior y escribe exactamente el nombre asignado por la plataforma. Guarda con Save Settings.', check: 'El nombre debe coincidir letra por letra.' },
      { title: 'Protege la red', detail: 'En la misma pantalla entra a Wireless > Wireless Security. Elige WPA2 Personal o WPA2-PSK. En Passphrase escribe una clave de al menos ocho caracteres que puedas recordar. Haz clic en Save Settings.', check: 'No compartas la clave con otro equipo de trabajo.' },
      { title: 'Conecta la laptop', detail: 'Haz clic en Laptop0 > Desktop > PC Wireless. Abre la pestaña Connect, pulsa Refresh si hace falta, selecciona el nombre de tu red y haz clic en Connect. Escribe la clave cuando la pida.', check: 'Debe indicar que la laptop está conectada.' },
      { title: 'Conecta el teléfono', detail: 'Haz clic en Smartphone0 > Config > Wireless0. Busca el nombre de tu red, selecciónalo y escribe la misma clave. Si aparece DHCP, déjalo activado.', check: 'El teléfono debe mostrar conexión inalámbrica.' },
      { title: 'Pide direcciones automáticamente', detail: 'En PC0 y Laptop0 abre Desktop > IP Configuration y pulsa DHCP. En el teléfono revisa Config > Wireless0 y confirma que recibió una dirección.', check: 'Los tres equipos deben mostrar direcciones de la red asignada.' },
      { title: 'Comprueba con ipconfig', detail: 'En PC0 abre Desktop > Command Prompt, escribe ipconfig y presiona Enter. Haz lo mismo en Laptop0.', check: 'Las direcciones deben ser diferentes, pero comenzar con los mismos tres números de la red asignada.' },
      { title: 'Prueba con ping', detail: 'Desde PC0 escribe ping, un espacio y la dirección de Laptop0. Presiona Enter.', check: 'Debe aparecer Reply from o Respuesta desde.' },
      { title: 'Mira cómo viaja el mensaje', detail: 'Cambia a Simulation abajo a la derecha. Elige Add Simple PDU, el sobre cerrado. Haz clic en PC0 y luego en Laptop0. Pulsa Auto Capture/Play.', check: 'Observa que el mensaje pasa por el router inalámbrico.' },
      { title: 'Coloca tu código', detail: 'Usa Place Note, haz clic junto al router y escribe el código exacto indicado en tus datos asignados.', check: 'El código debe quedar visible en la topología.' },
      { title: 'Guarda tu práctica', detail: 'Haz clic en File > Save As y nombra el archivo Grupo_Apellido_Practica2.', check: 'Confirma que el archivo termina en .pkt.' },
    ],
    checks: ['El equipo cableado y los inalámbricos pertenecen a la misma red.', 'La red tiene seguridad configurada.', 'La prueba de comunicación es satisfactoria.'],
  },
  {
    id: 'pt-diagnostico',
    title: 'Práctica 3 · Diagnóstico y corrección de conectividad',
    related: 'Tema 6: modelos de comunicación y diagnóstico por capas',
    goal: 'Aplicar un orden de diagnóstico, localizar errores de configuración y comprobar la solución.',
    steps: [
      { title: 'Prepara la red', detail: 'Crea un archivo nuevo. En Network Devices > Switches coloca un 2960. En End Devices coloca cuatro PC.', check: 'Debes ver Switch0 y las computadoras PC0, PC1, PC2 y PC3.' },
      { title: 'Conecta las cuatro computadoras', detail: 'En Connections elige Copper Straight-Through. Conecta FastEthernet0 de cada PC a los puertos FastEthernet0/1, 0/2, 0/3 y 0/4 del switch.', check: 'Espera hasta que todos los puntos de conexión estén verdes.' },
      { title: 'Configura tres equipos correctamente', detail: 'En cada PC abre Desktop > IP Configuration > Static. Usa la red que te asignó la plataforma y coloca hosts .10, .11, .12 y .13 con máscara 255.255.255.0.', check: 'Cada PC debe tener una dirección diferente.' },
      { title: 'Crea el error solicitado', detail: 'Busca en tus datos cuál PC debe iniciar con error. Solo en esa PC cambia el tercer número de su dirección por uno diferente. No cambies la máscara ni desconectes cables.', check: 'El error debe estar únicamente en la PC indicada.' },
      { title: 'Revisa PC0', detail: 'Haz clic en PC0 > Desktop > Command Prompt. Escribe ipconfig y presiona Enter. Anota mentalmente la dirección que muestra.', check: 'Comprueba si coincide con la red asignada.' },
      { title: 'Prueba una PC a la vez', detail: 'Desde PC0 escribe ping seguido de la dirección de PC1. Repite hacia PC2 y PC3.', check: 'Una de las pruebas debe fallar con Request timed out o Tiempo de espera agotado.' },
      { title: 'Localiza la causa', detail: 'Abre la PC que no respondió. En Desktop > Command Prompt escribe ipconfig. Compara el tercer número de su dirección con las demás.', check: 'Debes reconocer que está en una red distinta.' },
      { title: 'Corrige sin mover nada más', detail: 'En esa misma PC entra a Desktop > IP Configuration. Cambia únicamente la dirección para que use la red correcta y conserve su número final.', check: 'No cambies cables, puertos ni direcciones de otros equipos.' },
      { title: 'Comprueba la reparación', detail: 'Regresa a PC0 > Desktop > Command Prompt y repite el ping hacia la PC corregida.', check: 'Ahora debe aparecer Reply from o Respuesta desde.' },
      { title: 'Revisa toda la red', detail: 'Haz ping desde PC0 hacia las otras tres computadoras. Si una falla, compara nuevamente su dirección y máscara.', check: 'Las tres pruebas deben responder.' },
      { title: 'Escribe lo que encontraste', detail: 'Usa Place Note y haz clic en un espacio vacío. Escribe el código asignado, el nombre de la PC con falla, la dirección incorrecta y la dirección corregida.', check: 'La explicación debe quedar visible dentro del archivo.' },
      { title: 'Guarda el resultado', detail: 'Haz clic en File > Save As y usa el nombre Grupo_Apellido_Practica3.', check: 'Confirma que guardaste el archivo .pkt después de hacer la corrección.' },
    ],
    checks: ['El archivo conserva la nota del diagnóstico.', 'Las cuatro computadoras quedan en la misma red.', 'Todos los equipos responden después de la corrección.'],
  },
]

function packetAssignmentsFor(studentId = '') {
  const seed = hash(`packet-tracer-${studentId}`)
  const networkA = 30 + (seed % 50)
  const networkB = 100 + ((seed >>> 4) % 50)
  const station = (seed >>> 8) % 4
  const code = String(1000 + (seed % 9000))
  return {
    'pt-componentes': {
      code: `PT1-${code}`,
      values: [`Red asignada: 192.168.${networkA}.0/24`, `Hosts: .10, .11, .12 y .100`, `Código de identificación: PT1-${code}`],
      note: `Agrega una nota visible en la topología con el código PT1-${code}.`,
    },
    'pt-inalambrica': {
      code: `PT2-${code}`,
      values: [`Nombre de red: AULA-${code}`, `Red local: 192.168.${networkB}.0/24`, `Código de identificación: PT2-${code}`],
      note: `Agrega una nota visible junto al router con el código PT2-${code}.`,
    },
    'pt-diagnostico': {
      code: `PT3-${code}`,
      values: [`Red correcta: 192.168.${networkA + 80}.0/24`, `Equipo que debe iniciar con error: PC${station}`, `Código de identificación: PT3-${code}`],
      note: `La nota final debe incluir el código PT3-${code}, el error encontrado y la corrección.`,
    },
  }
}

export function MtcsMaterialView({ code, session, onBack, onProgressUpdate }) {
  const definition = mtcsContent[code]
  if (!definition) return null
  if (code === 'MTCS-RA-1.1') return <Ra11LearningPath definition={definition} session={session} onBack={onBack} onProgressUpdate={onProgressUpdate} />
  return <GuidedMaterial definition={definition} code={code} session={session} onProgressUpdate={onProgressUpdate} onBack={onBack} />
}

const guidedExamples = {
  'MTCS-RA-1.2': [
    'Una laptop entrega una trama al switch para comunicarse dentro del salón. El switch utiliza las direcciones físicas para enviarla por el puerto correcto; todavía no necesita salir a otra red.',
    'En 192.168.10.25/24, los primeros 24 bits identifican la red. Por eso la red es 192.168.10.0 y el 25 identifica al equipo dentro de ella.',
    'Una impresión enviada a una sola impresora es unicast. Un aviso dirigido a todos los equipos de la red local es broadcast. Una transmisión para un grupo suscrito es multicast.',
    'Si una sola red tiene demasiados equipos, se divide. Cada nueva subred obtiene su propia dirección de red, rango de hosts y broadcast; ninguna dirección puede repetirse.',
    'El equipo 192.168.10.20 quiere comunicarse con 192.168.20.30. Como el destino no pertenece a su red, entrega el paquete a su puerta de enlace para que el router decida la ruta.',
    'Al conectarse, DHCP puede entregar dirección, prefijo, puerta de enlace y DNS. IPv6 ofrece un espacio de direcciones mucho mayor que IPv4 y utiliza una escritura hexadecimal separada por dos puntos.',
  ],
  'MTCS-RA-2.1': [
    'Una escuela protege expedientes, computadoras y servicios. Capacita usuarios, define procedimientos y configura tecnología: las tres partes trabajan juntas.',
    'Una contraseña escrita junto al monitor es una vulnerabilidad. Una persona que intenta usarla es la amenaza. El acceso indebido y la exposición de datos constituyen el riesgo.',
    'Leer calificaciones sin permiso afecta confidencialidad; modificarlas afecta integridad; impedir que el sistema abra durante evaluaciones afecta disponibilidad.',
    'Un empleado que comparte accidentalmente un archivo provoca una amenaza interna. Un atacante que intenta ingresar desde Internet representa una amenaza externa.',
    'Bloquear archivos peligrosos es preventivo; generar una alerta es detectivo; restaurar una copia limpia después del incidente es correctivo.',
  ],
  'MTCS-RA-2.2': [
    'Al descargar una imagen de instalación, el sitio publica su SHA-256. Si el resumen que calculas en tu equipo coincide, el archivo no fue alterado; si difiere en un solo carácter, no lo instales.',
    'El banco firma digitalmente su estado de cuenta: tu lector usa la clave pública del banco para comprobar que nadie lo modificó y que realmente lo emitió el banco.',
    'Una escuela tiene un solo servidor y un solo enlace a Internet. Si cualquiera falla, nadie entra a la plataforma: son puntos únicos de falla. Un segundo enlace y un servidor de respaldo los eliminan.',
    'Si el respaldo se hace cada noche, el RPO es de 24 horas: en el peor caso se pierde un día de trabajo. Si el servicio debe volver en 2 horas, ese es el RTO.',
    'En el laboratorio: equipos con actualizaciones y cuentas de alumno sin privilegios (host), servidor sin servicios innecesarios (servidor), red de alumnos separada de la administrativa (red) y puerta con llave (física).',
    'Un técnico encuentra un puerto abierto con Nmap en la red de su escuela. Solo lo hizo porque tenía autorización por escrito y reporta el hallazgo al responsable, sin aprovecharlo.',
  ],
}

const guidedExercises = {
  'MTCS-RA-1.2': [
    'Explica qué función cumple la capa de acceso cuando dos computadoras del mismo laboratorio se comunican.',
    'Para 192.168.40.18/24, identifica red, parte de host y cantidad máxima de hosts utilizables.',
    'Escribe un ejemplo propio de unicast, broadcast y multicast sin repetir los del ejemplo.',
    'Obtén red, primer host, último host y broadcast de 192.168.50.0/24.',
    'Explica el recorrido de un paquete que sale de una red local hacia otra red e identifica cuándo interviene el router.',
    'Compara una dirección IPv4 con una IPv6 e indica qué parámetros podría entregar DHCP.',
  ],
  'MTCS-RA-2.1': [
    'Selecciona un recurso del laboratorio y escribe cómo lo protegerías mediante personas, procesos y tecnología.',
    'Construye un ejemplo nuevo que identifique claramente amenaza, vulnerabilidad, impacto y riesgo.',
    'Clasifica tres situaciones propias según afecten confidencialidad, integridad o disponibilidad y justifica.',
    'Propón una amenaza interna accidental y una externa intencional para una escuela.',
    'Para un archivo infectado, propón un control preventivo, uno detectivo y uno correctivo.',
  ],
  'MTCS-RA-2.2': [
    'Explica con tus palabras por qué dos usuarios con la misma contraseña no deben tener el mismo hash guardado y qué técnica lo evita.',
    'Indica qué aporta una firma digital que no aporta un hash solo, y para qué sirve el certificado de un sitio HTTPS.',
    'Identifica dos puntos únicos de falla en el laboratorio o en tu casa y propón cómo eliminarlos.',
    'Una tienda respalda cada 6 horas y necesita volver a vender en 1 hora. Escribe su RPO y su RTO y una medida para cumplirlos.',
    'Propón una medida de protección para cada capa: host, servidor, red y seguridad física.',
    'Escribe tres reglas éticas que seguirías antes de usar una herramienta como Nmap o Wireshark.',
  ],
}

function GuidedMaterial({ definition, code, session, onProgressUpdate, onBack }) {
  const examples = guidedExamples[code] || []
  const exercises = guidedExercises[code] || []
  const reviewExercises = code === 'MTCS-RA-1.2' ? [
    'En la red 192.168.50.0/24 identifica dirección de red, primer host, último host y broadcast.',
    'Explica qué cambia cuando el destino está en otra red.',
    'Escribe un orden lógico para revisar un equipo que no puede salir de su red.',
  ] : code === 'MTCS-RA-2.2' ? [
    'Distingue para qué sirven hash con salting, HMAC y firma digital.',
    'Explica la diferencia entre RPO y RTO con un ejemplo.',
    'Propón tres capas de defensa en profundidad para una organización pequeña.',
  ] : [
    'Escribe un ejemplo propio de amenaza, vulnerabilidad y riesgo.',
    'Explica una afectación a confidencialidad, integridad y disponibilidad.',
    'Propón un control preventivo, uno detectivo y uno correctivo.',
  ]
  const [completed, setCompleted] = useState([])
  const [responses, setResponses] = useState({})
  const [reviewChecks, setReviewChecks] = useState([])
  const [message, setMessage] = useState('')
  const [view, setView] = useState('learn')
  const [selectedTopic, setSelectedTopic] = useState(0)
  const totalSteps = definition.lessons.length + 1

  useEffect(() => {
    if (session?.preview) return undefined
    let active = true
    supabase.from('learning_progress').select('completed_steps').eq('material_code', code).maybeSingle().then(({ data }) => {
      if (active) setCompleted(Array.isArray(data?.completed_steps) ? data.completed_steps : [])
    })
    return () => { active = false }
  }, [code, session?.id])

  async function completeStep(step) {
    if (completed.includes(step)) return
    const next = [...completed, step]
    setCompleted(next)
    const progress = { material_code: code, completed_steps: next, completed_at: next.length >= totalSteps ? new Date().toISOString() : null }
    if (session?.preview) { onProgressUpdate?.(progress); return }
    const { error } = await supabase.from('learning_progress').upsert({ student_id: session.id, ...progress, updated_at: new Date().toISOString() }, { onConflict: 'student_id,material_code' })
    if (error) setMessage('No fue posible guardar el avance. Revisa la conexión e inténtalo otra vez.')
    else onProgressUpdate?.(progress)
  }

  function completeTopic(index) {
    if (String(responses[index] || '').trim().length < 20) { setMessage('Explica tu respuesta con al menos una oración completa antes de continuar.'); return }
    setMessage('')
    completeStep(`tema-${index + 1}`)
  }

  const percent = Math.round(completed.length / totalSteps * 100)
  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="mtcs-learning-hero"><div><span>{definition.label} · MATERIAL DIDÁCTICO</span><h1>{definition.materialTitle}</h1><p>{definition.intro}</p><small>{completed.filter(step => step.startsWith('tema-')).length} de {definition.lessons.length} temas completados</small></div><div className="mtcs-progress-ring"><strong>{percent}%</strong><span>AVANCE GENERAL</span><i><b style={{ width: `${percent}%` }} /></i></div></div>
    <nav className="mtcs-section-tabs"><button className={view === 'learn' ? 'active' : ''} onClick={() => setView('learn')}><BookOpen size={18} /><span><b>1. Aprende y aplica</b><small>Teoría, ejemplo y ejercicio</small></span></button><button className={view === 'review' ? 'active' : ''} onClick={() => setView('review')}><ShieldCheck size={18} /><span><b>2. Repaso final</b><small>Comprueba que estás listo</small></span></button></nav>
    {view === 'learn' && <div className="mtcs-learning-layout"><aside className="mtcs-topic-nav"><header><small>CONTENIDO DEL RESULTADO</small><b>{definition.lessons.length} temas</b></header>{definition.lessons.map(([title], index) => { const done = completed.includes(`tema-${index + 1}`); return <button className={selectedTopic === index ? 'active' : done ? 'done' : ''} key={title} onClick={() => setSelectedTopic(index)}><span>{done ? <CheckCircle2 size={16} /> : index + 1}</span><div><small>TEMA {index + 1}</small><b>{title.replace(/^\d+\.\s*/, '')}</b></div></button> })}</aside><main className="guided-topic-list">{definition.lessons.map(([title, text], index) => { if (index !== selectedTopic) return null; const done = completed.includes(`tema-${index + 1}`); return <article className={done ? 'guided-complete' : ''} key={title}><header><span>{done ? <CheckCircle2 size={17} /> : index + 1}</span><div><small>TEMA {index + 1} DE {definition.lessons.length}</small><h2>{title.replace(/^\d+\.\s*/, '')}</h2></div></header><section><small>1 · APRENDE</small><h3>Conceptos clave</h3><p>{text}</p></section><section className="guided-example"><small>2 · OBSERVA</small><h3>Ejemplo práctico</h3><p>{examples[index]}</p></section><section className="guided-exercise"><small>3 · APLICA</small><h3>Ejercicio de refuerzo</h3><p>{exercises[index]}</p><textarea rows="3" disabled={done} value={responses[index] || ''} onChange={event => setResponses(current => ({ ...current, [index]: event.target.value }))} placeholder="Explica con tus propias palabras" /><button className="primary" disabled={done} onClick={() => completeTopic(index)}>{done ? 'Tema completado' : 'Guardar y completar tema'}</button></section><footer><button className="secondary" disabled={selectedTopic === 0} onClick={() => setSelectedTopic(selectedTopic - 1)}>Tema anterior</button><span>{selectedTopic + 1} / {definition.lessons.length}</span><button className="secondary" disabled={selectedTopic === definition.lessons.length - 1} onClick={() => setSelectedTopic(selectedTopic + 1)}>Tema siguiente</button></footer></article> })}</main></div>}
    {view === 'review' && <section className={`mtcs-practice mtcs-review-card ${completed.includes('repaso-final') ? 'guided-complete' : ''}`}><div className="stage-heading"><span>REPASO FINAL</span><h2>Comprueba que puedes hacerlo</h2><p>Realiza estos ejercicios antes de abrir la evaluación.</p></div><div className="review-checks">{reviewExercises.map((item, index) => <label key={item}><input type="checkbox" checked={reviewChecks.includes(index)} disabled={completed.includes('repaso-final')} onChange={() => setReviewChecks(current => current.includes(index) ? current.filter(value => value !== index) : [...current, index])} /><span>{item}</span></label>)}</div><button className="primary" disabled={reviewChecks.length !== reviewExercises.length || completed.includes('repaso-final')} onClick={() => completeStep('repaso-final')}>{completed.includes('repaso-final') ? 'Repaso completado' : 'Terminé los ejercicios de repaso'}</button></section>}
    {message && <div className="form-error">{message}</div>}
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}><ShieldCheck size={24} /><div><strong>{percent === 100 ? 'Actividad de evaluación desbloqueada' : 'Actividad de evaluación bloqueada'}</strong><p>{percent === 100 ? 'Ya puedes ir a Evaluaciones y comenzar la actividad de este R.A.' : `Completa los ${totalSteps - completed.length} pasos pendientes.`}</p></div></div>
  </section>
}

function Ra11LearningPath({ definition, session, onBack, onProgressUpdate }) {
  const [completed, setCompleted] = useState([])
  const [answers, setAnswers] = useState({})
  const [feedback, setFeedback] = useState({})
  const [command, setCommand] = useState('')
  const [terminal, setTerminal] = useState(['Escribe un comando para comenzar el diagnóstico.'])
  const [status, setStatus] = useState('loading')
  const [assessmentId, setAssessmentId] = useState(null)
  const [packetUploads, setPacketUploads] = useState({})
  const [uploadingPractice, setUploadingPractice] = useState('')
  const [practiceMessage, setPracticeMessage] = useState({})
  const [view, setView] = useState('learn')
  const [selectedTopic, setSelectedTopic] = useState(0)
  const packetAssignments = useMemo(() => packetAssignmentsFor(session?.id || session?.email), [session?.id, session?.email])
  const totalSteps = definition.lessons.length + 1 + packetTracerPractices.length

  useEffect(() => {
    if (session?.preview) { setStatus('ready'); return undefined }
    let active = true
    Promise.all([
      supabase.from('learning_progress').select('completed_steps').eq('material_code', 'MTCS-RA-1.1').maybeSingle(),
      supabase.from('assessments').select('id').eq('activity_code', 'MTCS-RA-1.1').maybeSingle(),
    ]).then(([progressResult, assessmentResult]) => {
      if (!active) return
      if (!progressResult.error) setCompleted(Array.isArray(progressResult.data?.completed_steps) ? progressResult.data.completed_steps : [])
      if (!assessmentResult.error && assessmentResult.data?.id) {
        setAssessmentId(assessmentResult.data.id)
        supabase.from('submissions').select('answers').eq('assessment_id', assessmentResult.data.id).maybeSingle().then(({ data }) => {
          if (active) setPacketUploads(data?.answers?.packet_tracer || {})
        })
      }
      setStatus(progressResult.error || assessmentResult.error ? 'error' : 'ready')
    })
    return () => { active = false }
  }, [session?.id])

  async function completeStep(step) {
    if (completed.includes(step)) return
    const next = [...completed, step]
    setCompleted(next)
    if (session?.preview) { onProgressUpdate?.({ material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: next.length >= totalSteps ? new Date().toISOString() : null }); return }
    setStatus('saving')
    const done = next.length >= totalSteps
    const { error } = await supabase.from('learning_progress').upsert({ student_id: session.id, material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: done ? new Date().toISOString() : null, updated_at: new Date().toISOString() }, { onConflict: 'student_id,material_code' })
    setStatus(error ? 'error' : 'ready')
    if (!error) onProgressUpdate?.({ material_code: 'MTCS-RA-1.1', completed_steps: next, completed_at: done ? new Date().toISOString() : null })
  }

  function checkLesson(index) {
    const questions = [ra11Checks[index], ...ra11ExtraChecks[index]]
    const correct = questions.every((item, questionIndex) => answers[`${index}-${questionIndex}`] === item.correct)
    setFeedback(current => ({ ...current, [index]: correct ? '¡Correcto! Tema completado.' : 'Revisa nuevamente los apuntes y vuelve a intentarlo.' }))
    if (correct) completeStep(`tema-${index + 1}`)
  }

  function runCommand(event) {
    event.preventDefault()
    const clean = command.trim().toLowerCase()
    const outputs = {
      ipconfig: 'IPv4: 192.168.10.24  Máscara: 255.255.255.0  Puerta de enlace: 192.168.10.1',
      'ping 192.168.10.1': 'Respuesta desde 192.168.10.1: tiempo=2ms. Conexión local correcta.',
      'ping 8.8.8.8': 'Respuesta desde 8.8.8.8: tiempo=24ms. Hay salida a otra red.',
      'tracert 8.8.8.8': '1  192.168.10.1\n2  10.20.0.1\n3  8.8.8.8  Ruta completada.',
    }
    setTerminal(current => [...current, `> ${command}`, outputs[clean] || 'Comando no reconocido. Prueba: ipconfig, ping 192.168.10.1, ping 8.8.8.8 o tracert 8.8.8.8'])
    setCommand('')
    const history = [...terminal, clean].join(' ').toLowerCase()
    if (history.includes('ipconfig') && history.includes('ping 192.168.10.1') && history.includes('tracert 8.8.8.8')) completeStep('practica-comandos')
  }

  async function uploadPacketPractice(practice, file) {
    if (!file) return
    if (!file.name.toLowerCase().endsWith('.pkt')) { setPracticeMessage(current => ({ ...current, [practice.id]: 'Selecciona el archivo .pkt que guardaste en Packet Tracer.' })); return }
    if (file.size > 20 * 1024 * 1024) { setPracticeMessage(current => ({ ...current, [practice.id]: 'El archivo supera el límite de 20 MB.' })); return }
    if (session?.preview) { setPracticeMessage(current => ({ ...current, [practice.id]: 'En la vista previa no se generan entregas.' })); return }
    if (!assessmentId) { setPracticeMessage(current => ({ ...current, [practice.id]: 'No fue posible identificar la actividad. Actualiza la página e inténtalo nuevamente.' })); return }
    setUploadingPractice(practice.id)
    setPracticeMessage(current => ({ ...current, [practice.id]: '' }))
    try {
      const { data: authData, error: authError } = await supabase.auth.getUser()
      if (authError || !authData.user) throw authError || new Error('La sesión ya no está disponible.')
      const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_')
      const path = `${authData.user.id}/${assessmentId}/packet-tracer/${practice.id}-${safeName}`
      const { bytes } = await uploadSubmissionFile(path, file, 'application/octet-stream')
      const digest = await crypto.subtle.digest('SHA-256', bytes)
      const checksum = Array.from(new Uint8Array(digest)).map(byte => byte.toString(16).padStart(2, '0')).join('')
      const { data: existing, error: readError } = await supabase.from('submissions').select('id, answers, submitted_at').eq('assessment_id', assessmentId).maybeSingle()
      if (readError) throw readError
      if (existing?.submitted_at) throw new Error('La evaluación final ya fue entregada y no admite cambios.')
      const entry = { path, filename: file.name, practice: practice.title, assigned_code: packetAssignments[practice.id].code, assigned_values: packetAssignments[practice.id].values, checksum, size: file.size, uploaded_at: new Date().toISOString() }
      const nextUploads = { ...(existing?.answers?.packet_tracer || packetUploads), [practice.id]: entry }
      const answers = { ...(existing?.answers || {}), packet_tracer: nextUploads }
      const query = existing?.id
        ? supabase.from('submissions').update({ answers }).eq('id', existing.id)
        : supabase.from('submissions').insert({ assessment_id: assessmentId, student_id: authData.user.id, answers })
      const { error: saveError } = await query
      if (saveError) throw saveError
      setPacketUploads(nextUploads)
      await completeStep(practice.id)
      setPracticeMessage(current => ({ ...current, [practice.id]: 'Práctica entregada correctamente. Puedes reemplazarla antes de entregar la evaluación final.' }))
    } catch (error) {
      setPracticeMessage(current => ({ ...current, [practice.id]: error.message || 'No fue posible entregar el archivo.' }))
    } finally { setUploadingPractice('') }
  }

  const percent = Math.round(completed.length / totalSteps * 100)
  return <section className="panel page-panel activity-workspace mtcs-workspace">
    <button className="text-btn back-action" onClick={onBack}><ArrowLeft size={16} /> Volver a materiales</button>
    <div className="mtcs-learning-hero"><div><span>MTCS · R.A. 1.1 · MATERIAL DIDÁCTICO</span><h1>{definition.materialTitle}</h1><p>Aprende, comprueba y practica antes de realizar la evaluación.</p><small>{completed.filter(step => step.startsWith('tema-')).length} de {definition.lessons.length} temas · {completed.filter(step => step.startsWith('pt-')).length} de {packetTracerPractices.length} prácticas Packet Tracer</small></div><div className="mtcs-progress-ring"><strong>{percent}%</strong><span>AVANCE GENERAL</span><i><b style={{ width: `${percent}%` }} /></i></div></div>
    <nav className="mtcs-section-tabs three"><button className={view === 'learn' ? 'active' : ''} onClick={() => setView('learn')}><BookOpen size={18} /><span><b>1. Aprende</b><small>Teoría, esquemas y ejercicios</small></span></button><button className={view === 'commands' ? 'active' : ''} onClick={() => setView('commands')}><Terminal size={18} /><span><b>2. Diagnostica</b><small>Comandos y simulador</small></span></button><button className={view === 'packet' ? 'active' : ''} onClick={() => setView('packet')}><Network size={18} /><span><b>3. Construye</b><small>Prácticas en Packet Tracer</small></span></button></nav>
    {view === 'learn' && <div className="mtcs-learning-layout"><aside className="mtcs-topic-nav"><header><small>CONTENIDO DEL R.A. 1.1</small><b>{definition.lessons.length} temas</b></header>{definition.lessons.map(([title], index) => { const done=completed.includes(`tema-${index+1}`); return <button className={selectedTopic===index?'active':done?'done':''} key={title} onClick={()=>setSelectedTopic(index)}><span>{done?<CheckCircle2 size={16}/>:index+1}</span><div><small>TEMA {index+1}</small><b>{title.replace(/^\d+\.\s*/,'')}</b></div></button> })}</aside><main className="learning-topic-list">{definition.lessons.map(([title,text],index)=>{ if(index!==selectedTopic)return null; const done=completed.includes(`tema-${index+1}`); const questions=[ra11Checks[index],...ra11ExtraChecks[index]]; const answered=questions.every((_,qi)=>answers[`${index}-${qi}`]); return <article className={done?'topic-complete':''} key={title}><header><span>{done?<CheckCircle2 size={18}/>:index+1}</span><div><small>TEMA {index+1} DE {definition.lessons.length}</small><h2>{title.replace(/^\d+\.\s*/,'')}</h2></div></header><div className="topic-notes"><h3>Conceptos clave</h3><p>{text}</p><ul className="concept-list">{ra11Details[index].map(detail=><li key={detail}>{detail}</li>)}</ul><TopicDiagram index={index}/><div className="topic-example"><b>Para visualizarlo:</b> {index===0?'la red funciona como un servicio de mensajería: necesita remitente, destino, camino y reglas.':index===1?'el dispositivo final crea o recibe; el intermediario dirige; el medio transporta.':index===2?'cliente pregunta, servidor responde y el protocolo define cómo conversan.':index===3?'tener señal no basta: debe llegar bien, soportar usuarios y estar protegida.':index===4?'no existe un medio perfecto; se elige el que mejor resuelve la necesidad.':'las capas permiten revisar una parte del problema a la vez.'}</div></div><div className="topic-check"><b>Ejercicios del tema</b>{questions.map((check,qi)=><div className="topic-question" key={check.question}><p>{qi+1}. {check.question}</p><div className="check-options">{check.options.map(option=><label key={option}><input type="radio" name={`check-${index}-${qi}`} checked={answers[`${index}-${qi}`]===option} onChange={()=>setAnswers(current=>({...current,[`${index}-${qi}`]:option}))}/>{option}</label>)}</div></div>)}<button className="primary" onClick={()=>checkLesson(index)} disabled={!answered||done}>{done?'Ejercicios completados':'Comprobar respuestas'}</button>{feedback[index]&&<small className={done?'correct-feedback':'wrong-feedback'}>{feedback[index]}</small>}</div><footer><button className="secondary" disabled={selectedTopic===0} onClick={()=>setSelectedTopic(selectedTopic-1)}>Tema anterior</button><span>{selectedTopic+1} / {definition.lessons.length}</span><button className="secondary" disabled={selectedTopic===definition.lessons.length-1} onClick={()=>setSelectedTopic(selectedTopic+1)}>Tema siguiente</button></footer></article>})}</main></div>}
    {view === 'commands' && <><CommandGuide /><section className={`network-simulator ${completed.includes('practica-comandos') ? 'topic-complete' : ''}`}><div className="stage-heading"><span>PRÁCTICA OBLIGATORIA</span><h2>Simulador de diagnóstico de red</h2><p>Obtén la configuración, comprueba la puerta de enlace y observa la ruta. Debes ejecutar <b>ipconfig</b>, <b>ping 192.168.10.1</b> y <b>tracert 8.8.8.8</b>.</p></div><div className="fake-terminal">{terminal.map((line, index) => <pre key={`${line}-${index}`}>{line}</pre>)}<form onSubmit={runCommand}><span>C:\AulaVirtual&gt;</span><input value={command} onChange={event => setCommand(event.target.value)} placeholder="Escribe un comando" autoComplete="off" /><button>Ejecutar</button></form></div>{completed.includes('practica-comandos') && <div className="submission-success"><CheckCircle2 size={17} /> Práctica completada.</div>}</section></>}
    {view === 'packet' && <PacketTracerPractices completed={completed} uploads={packetUploads} uploading={uploadingPractice} messages={practiceMessage} assignments={packetAssignments} preview={session?.preview} onUpload={uploadPacketPractice} />}
    {status === 'error' && <div className="form-error">No fue posible guardar el avance. Revisa la conexión y vuelve a intentarlo.</div>}
    <div className={`unlock-status ${percent === 100 ? 'unlocked' : ''}`}><ShieldCheck size={24} /><div><strong>{percent === 100 ? 'Actividad de evaluación desbloqueada' : 'Actividad de evaluación bloqueada'}</strong><p>{percent === 100 ? 'Ya puedes ir a Evaluaciones y comenzar la actividad del R.A. 1.1.' : `Completa los ${totalSteps - completed.length} pasos pendientes para desbloquearla.`}</p></div></div>
  </section>
}

function PacketTracerPractices({ completed, uploads, uploading, messages, assignments, preview, onUpload }) {
  return <section className="packet-tracer-section"><div className="stage-heading"><span>PRÁCTICAS EN PACKET TRACER</span><h2>Construye, prueba y entrega tus redes</h2><p>Realiza únicamente estas prácticas en Cisco Packet Tracer. Sigue un paso a la vez y no avances hasta obtener el resultado indicado en <b>“Vas bien si…”</b>.</p></div><div className="packet-first-help"><b>Antes de comenzar</b><span><strong>Parte inferior izquierda:</strong> aquí se encuentran los equipos y los cables.</span><span><strong>Espacio blanco:</strong> aquí vas a construir la red.</span><span><strong>Doble clic o un clic sobre un equipo:</strong> abre su ventana de configuración.</span><span><strong>Realtime / Simulation:</strong> está abajo a la derecha y permite observar el recorrido de los mensajes.</span></div><div className="packet-practice-list">{packetTracerPractices.map((practice, index) => { const delivered = Boolean(uploads[practice.id]) || completed.includes(practice.id); const assignment = assignments[practice.id]; return <article className={delivered ? 'practice-delivered' : ''} key={practice.id}><header><span>{delivered ? <CheckCircle2 size={20} /> : index + 1}</span><div><small>{practice.related}</small><h3>{practice.title}</h3></div></header><div className="packet-practice-body"><div className="practice-goal"><b>Meta</b><p>{practice.goal}</p></div><div className="packet-assignment"><b>Datos asignados para tu práctica</b>{assignment.values.map(value => <span key={value}>{value}</span>)}<p>{assignment.note}</p></div><div className="practice-columns"><div><h4>Hazlo paso a paso</h4><ol className="handheld-steps">{practice.steps.map(step => <li key={step.title}><b>{step.title}</b><p>{step.detail}</p><small><CheckCircle2 size={13} /> Vas bien si: {step.check}</small></li>)}</ol></div><div><h4>Antes de entregar, comprueba</h4><ul>{practice.checks.map(check => <li key={check}>{check}</li>)}<li>{assignment.note}</li></ul><div className="stuck-note"><b>¿Algo no aparece?</b><p>Detente en ese paso. Revisa que elegiste el equipo, puerto o pestaña indicados antes de cambiar otras cosas.</p></div></div></div><label className="packet-upload"><Upload size={20} /><span><strong>{uploads[practice.id]?.filename || 'Selecciona tu archivo de Packet Tracer'}</strong><small>Formato permitido: .pkt · máximo 20 MB</small></span><input type="file" accept=".pkt,application/octet-stream" disabled={uploading === practice.id || preview} onChange={event => onUpload(practice, event.target.files?.[0])} /></label>{uploading === practice.id && <div className="upload-status">Subiendo y vinculando tu práctica…</div>}{messages[practice.id] && <div className={delivered ? 'submission-success' : 'form-error'}>{messages[practice.id]}</div>}{delivered && !messages[practice.id] && <div className="submission-success"><CheckCircle2 size={17} /> Archivo entregado. Puedes reemplazarlo mientras no hayas enviado la evaluación final.</div>}</div></article> })}</div></section>
}

function TopicDiagram({ index }) {
  if (index === 5) return <div className="layer-diagram"><span>Aplicación</span><span>Transporte</span><span>Red</span><span>Acceso y medio</span></div>
  const diagrams = [
    ['Emisor', 'Datos', 'Medio', 'Receptor'],
    ['Computadora', 'Switch', 'Router', 'Internet'],
    ['Cliente', 'Solicitud', 'Servidor', 'Respuesta'],
    ['Dispositivo', 'Punto de acceso', 'Router', 'Internet'],
    ['Necesidad', 'Distancia', 'Ambiente', 'Medio adecuado'],
  ]
  return <div className="flow-diagram" aria-label="Esquema del tema">{diagrams[index].map((item, itemIndex) => <span key={item}>{item}{itemIndex < diagrams[index].length - 1 && <i>→</i>}</span>)}</div>
}

function CommandGuide() {
  const commands = [
    { name: 'ipconfig', purpose: 'Muestra la configuración de red del equipo.', use: 'Úsalo primero para conocer la dirección IP, máscara y puerta de enlace.', example: 'ipconfig' },
    { name: 'ping', purpose: 'Comprueba si otro dispositivo responde y mide el tiempo de comunicación.', use: 'Úsalo para saber si alcanzas la puerta de enlace, otro equipo o un destino de Internet.', example: 'ping 192.168.10.1' },
    { name: 'tracert', purpose: 'Muestra los saltos que sigue la información hasta el destino.', use: 'Úsalo cuando hay conexión parcial y necesitas localizar en qué tramo se interrumpe la ruta.', example: 'tracert 8.8.8.8' },
  ]
  return <section className="command-guide"><div className="stage-heading"><span>ANTES DEL SIMULADOR</span><h2>Herramientas básicas de diagnóstico</h2><p>Los comandos no reparan por sí solos la red: proporcionan información para localizar el problema y decidir qué revisar.</p></div><div className="command-grid">{commands.map(command => <article key={command.name}><code>{command.name}</code><h3>¿Para qué sirve?</h3><p>{command.purpose}</p><h3>¿Cuándo se utiliza?</h3><p>{command.use}</p><div><span>Ejemplo</span><b>C:\&gt; {command.example}</b></div></article>)}</div><div className="diagnostic-order"><b>Orden recomendado</b><span>1. Revisar configuración con <code>ipconfig</code></span><span>2. Probar comunicación local con <code>ping</code></span><span>3. Seguir la ruta con <code>tracert</code></span></div></section>
}

function PracticeExercises({ code }) {
  const exercises = code === 'MTCS-RA-1.1' ? [
    'Clasifica cinco elementos de una red cercana como equipo final, dispositivo intermediario o medio.',
    'Compara cable de cobre, fibra óptica y conexión inalámbrica. Escribe una ventaja y una limitación de cada uno.',
    'Dibuja el recorrido de la información desde una computadora hasta un servicio de Internet e identifica los componentes que intervienen.',
    'Propón dos cambios para mejorar una red con señal inalámbrica débil y conexión inestable.',
  ] : code === 'MTCS-RA-1.2' ? [
    'En la red 192.168.50.0/24 identifica dirección de red, primer host, último host y broadcast.',
    'Explica qué ocurre cuando dos equipos de la misma red se comunican y qué cambia cuando el destino está en otra red.',
    'Determina si 192.168.20.15/24 y 192.168.21.15/24 pertenecen a la misma red. Justifica tu respuesta.',
    'Un equipo tiene dirección IP y máscara correctas, pero no puede salir de su red. Escribe un orden lógico de revisión.',
  ] : code === 'MTCS-RA-2.2' ? [
    'Calcula el SHA-256 de un archivo de texto (por ejemplo, con certutil -hashfile archivo.txt SHA256), cambia una letra y vuelve a calcularlo. Compara ambos resultados.',
    'Abre el candado de un sitio HTTPS en tu navegador y anota quién emitió su certificado y hasta cuándo es válido.',
    'Para un servidor de archivos de la escuela, propón una medida de alta disponibilidad y una de recuperación tras desastre.',
  ] : [
    'Escribe un ejemplo propio de amenaza, vulnerabilidad y riesgo sin utilizar el ejemplo del material.',
    'Clasifica tres situaciones como afectación a confidencialidad, integridad o disponibilidad y explica por qué.',
    'Propón un control preventivo, uno detectivo y uno correctivo para un equipo compartido.',
  ]
  return <section className="mtcs-practice"><div className="stage-heading"><span>PRACTICA ANTES DE EVALUARTE</span><h2>Ejercicios de comprobación</h2><p>Resuélvelos en tu libreta o coméntalos con tu docente. No se entregan en este apartado.</p></div><ol>{exercises.map(item => <li key={item}>{item}</li>)}</ol></section>
}
