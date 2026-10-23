"""MTCS-20 · R.A. 2.2 · Principios y tecnologías de integridad y disponibilidad.

Caso de las lecciones: Clínica dental Sonríe (expedientes, citas y cobros).
La actividad de evaluación vive en la plataforma (MtcsActivity, con organización asignada y PDF).
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MTCS-RA-2.2'
CODE_PREFIX = 'MTCS22'
FILE = 'mtcs-ra22-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 2.2 · Integridad, disponibilidad y defensa'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 2.2 · Integridad, disponibilidad y defensa'
HERO_KICK = 'MTCS-20 · R.A. 2.2'
HERO_TITLE = 'Que la información sea confiable y esté siempre disponible'
HERO_TEXT = 'Aprende a comprobar que los datos no cambiaron, a mantener los servicios funcionando y a defender equipos, servidores y redes.'
EV_SHORT = 'elabora tu reporte con la organización asignada.'
EV_CARD = 'Reporte R.A. 2.2'
RA = 'R.A. 2.2'
GROUP = '511'

EXTRA_JS = r'''
function pHash(){K++;return '<article class="lesson"><header><span class="kick">🧪 Herramienta</span><h1>Laboratorio de hash</h1><p class="sub">Escribe, cambia una sola letra y mira qué le pasa a la huella.</p></header><div class="hashlab czf"><label>Texto (puede ser una contraseña de prueba o un dato del expediente)<textarea class="hx" rows="2">Ana López · alergia a la penicilina</textarea></label><label style="display:flex;gap:8px;align-items:center;font-weight:500"><input type="checkbox" class="hs"> Agregar sal (un valor aleatorio antes del texto)</label><div class="co co-def"><div class="co-l">Huella SHA-256 (64 caracteres)</div><p class="ho" style="font-family:Consolas,monospace;word-break:break-all;margin:0"></p></div><p class="hn" style="font-size:14.5px;color:var(--mut)"></p></div><p class="take"><b>Prueba:</b> cambia «Ana» por «Ena». Después activa la sal y escribe dos veces lo mismo. No cuenta como actividad.</p></article>'}
function hashInit(d){var x=d.querySelector(".hx"),s=d.querySelector(".hs"),o=d.querySelector(".ho"),n=d.querySelector(".hn"),prev=null,salt="";
 function hex(b){return [].map.call(new Uint8Array(b),function(v){return ("0"+v.toString(16)).slice(-2)}).join("")}
 function go(){if(!(window.crypto&&crypto.subtle)){o.textContent="Tu navegador no permite calcular el hash aquí.";return}
  if(s.checked&&!salt){var r=new Uint8Array(4);crypto.getRandomValues(r);salt=hex(r.buffer)}if(!s.checked)salt="";
  crypto.subtle.digest("SHA-256",new TextEncoder().encode(salt+x.value)).then(function(b){var h=hex(b),c=0;if(prev)for(var i=0;i<64;i++)if(prev[i]!=h[i])c++;o.textContent=h;n.innerHTML=(salt?"Sal: <b>"+salt+"</b> · se calcula SHA-256(sal + texto). ":"")+(prev&&prev!=h?"Cambiaron <b>"+c+" de 64</b> caracteres de la huella.":"");prev=h})}
 x.oninput=go;s.onchange=function(){salt="";go()};go()}
'''
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".hashlab"))hashInit(d);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏥', '¿Se puede confiar en la información?', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'En el R.A. 2.1 viste cómo mantener la información en secreto (confidencialidad). Ahora vas a ver cómo comprobar que <b>nadie la alteró</b> (integridad), cómo lograr que <b>siempre esté disponible</b> y cómo <b>defender</b> los equipos.'),
    ex('Caso de las lecciones: Clínica dental Sonríe', 'Tiene expedientes de pacientes, una agenda de citas en línea y un sistema de cobro. Si alguien cambia una alergia en un expediente, es peligroso. Si la agenda se cae, pierden pacientes. Vamos a protegerla paso a paso.'),
    bk('Al final', 'Elaboras un <b>reporte</b> (15%) con la organización que te asigna la plataforma en la actividad de evaluación.')),
    'Integridad = que no cambie · Disponibilidad = que funcione cuando se necesita.')
c.A('🔺', '¿Qué pilar se afecta?', 'Elige el pilar de la seguridad que se daña en cada situación de la clínica.', [
    ['Alguien cambia la alergia de un paciente en su expediente', 'Integridad', 'El dato fue alterado: se perdió la integridad.'],
    ['La agenda en línea no abre en todo el día', 'Disponibilidad', 'El servicio no funciona cuando se necesita.'],
    ['Un empleado publica radiografías de un paciente', 'Confidencialidad', 'Información privada llegó a quien no debía.'],
    ['Un virus modifica los montos de los cobros', 'Integridad', 'Los datos cambiaron sin autorización.'],
    ['Se va la luz y el servidor no enciende', 'Disponibilidad', 'El sistema deja de estar disponible.'],
], 'Secreto = confidencialidad · Sin cambios = integridad · Que funcione = disponibilidad.', ['Confidencialidad', 'Integridad', 'Disponibilidad'])
s0_end = c.mark() - 1

# ───────────────────────── A · Integridad ─────────────────────────
a0 = c.mark()
c.L('🧬', 'Hash: la huella digital de los datos', 'Bloque A · Controles de integridad', body(
    sp('En palabras sencillas', 'Un <b>hash</b> es un algoritmo que convierte cualquier dato en un <b>resumen de tamaño fijo</b> (su «huella»). SHA-256 siempre da 64 caracteres, sea una palabra o una película.'),
    bk('Tres propiedades', '1) El mismo dato siempre da la misma huella. 2) Si cambia <b>una sola letra</b>, la huella cambia por completo. 3) No se puede regresar de la huella al dato original.'),
    ana('Piensa en…', 'Tu huella dactilar: te identifica, pero con la huella no se puede reconstruir tu cara. O un licuado: no puedes volver a sacar el plátano entero.'),
    ex('En la clínica', 'Se guarda la huella de cada expediente. Si mañana la huella ya no coincide, alguien lo modificó.'),
    warn('Algoritmos viejos', 'MD5 y SHA-1 ya no son seguros. Hoy se usa SHA-256 o superior.')),
    'Misma entrada → misma huella; un cambio mínimo → huella totalmente distinta.')
c.raw('pHash()')
c.A('🧬', '¿Qué pasa con la huella?', 'Usa lo que viste en el laboratorio de hash.', [
    ['Calculo el hash de «Hola» dos veces', 'Sale la misma huella', 'El mismo dato siempre produce la misma huella.'],
    ['Cambio «Hola» por «hola»', 'Sale una huella totalmente distinta', 'Basta un carácter distinto (aunque sea mayúscula) para que cambie todo.'],
    ['Tengo solo la huella y quiero el texto original', 'No se puede obtener', 'El hash es de un solo sentido.'],
    ['Hago el hash de un archivo de 2 GB con SHA-256', 'Sale una huella de 64 caracteres', 'El tamaño de la huella es fijo, sin importar el tamaño del archivo.'],
], 'Recuerda las tres propiedades del hash.', ['Sale la misma huella', 'Sale una huella totalmente distinta', 'No se puede obtener', 'Sale una huella de 64 caracteres'])
c.L('🧂', 'La técnica salting', 'Bloque A · Guardar contraseñas de forma segura', body(
    sp('En palabras sencillas', 'Las contraseñas nunca se guardan tal cual: se guarda su hash. La <b>sal</b> es un valor aleatorio, distinto para cada usuario, que se agrega a la contraseña <b>antes</b> de calcular el hash.'),
    bk('¿Por qué?', 'Sin sal, dos personas con la contraseña «123456» tendrían el mismo hash, y un atacante podría usar <b>tablas precalculadas</b> (tablas arcoíris) con millones de hashes de contraseñas comunes.'),
    ana('Piensa en…', 'Dos personas piden el mismo platillo, pero el cocinero le pone a cada uno un ingrediente secreto distinto: ya no saben igual.'),
    ex('En la clínica', 'La recepcionista y el dentista usan la misma contraseña por coincidencia. Gracias a la sal, en la base de datos sus hashes son diferentes.'),
    bk('Para contraseñas', 'Se usan algoritmos lentos a propósito, como <b>bcrypt</b> o <b>Argon2</b>, que ya incluyen la sal.')),
    'Contraseña + sal → hash. La sal se guarda junto al hash; la contraseña no.')
c.O('🧂', 'Ordena: guardar una contraseña', 'Pon en orden lo que hace el sistema cuando creas tu contraseña.', [
    ['El usuario escribe su contraseña nueva', 'Todo empieza con la contraseña en texto claro.'],
    ['El sistema genera una sal aleatoria para ese usuario', 'Cada usuario recibe una sal diferente.'],
    ['Junta la sal con la contraseña y calcula el hash', 'El hash se calcula sobre sal + contraseña.'],
    ['Guarda la sal y el hash; la contraseña se descarta', 'Nunca se guarda la contraseña original.'],
    ['Al iniciar sesión repite el cálculo y compara los hashes', 'Si coinciden, la contraseña es correcta.'],
], 'La contraseña original nunca se guarda.')
c.L('🔏', 'HMAC: hash con clave secreta', 'Bloque A · Comprobar quién lo envió', body(
    sp('En palabras sencillas', '<b>HMAC</b> combina un hash con una <b>clave secreta</b> que solo conocen el emisor y el receptor. Comprueba que el mensaje no cambió <b>y</b> que lo envió alguien que conoce la clave.'),
    ana('Piensa en…', 'Un sobre sellado con lacre y tu sello personal: si alguien lo abre, se nota, y solo tú tienes ese sello.'),
    ex('En la clínica', 'El laboratorio envía resultados a la clínica con un HMAC. Si alguien intercepta el mensaje y cambia un valor, el HMAC ya no coincide y la clínica lo rechaza.')),
    'Hash solo = ¿cambió? · HMAC = ¿cambió y quién lo envió?')
c.L('✍️', 'Firmas digitales y certificados', 'Bloque A · Identidad en internet', body(
    sp('Firma digital', 'Se crea con la <b>clave privada</b> del emisor y cualquiera la verifica con su <b>clave pública</b>. Asegura integridad, autenticidad y <b>no repudio</b> (el emisor no puede negar que firmó).'),
    sp('Certificado digital', 'Documento emitido por una <b>autoridad certificadora</b> que dice «esta clave pública pertenece a esta persona o a este sitio». Es lo que usa HTTPS.'),
    ana('Piensa en…', 'La firma es tu firma autógrafa; el certificado es tu INE: una autoridad confiable garantiza que esa firma es tuya.'),
    ex('En México', 'La <b>e.firma</b> del SAT es una firma digital con certificado. Las facturas electrónicas (CFDI) van firmadas digitalmente.')),
    'Privada para firmar, pública para verificar.')
c.L('🗃️', 'Integridad en bases de datos', 'Bloque A · Que los datos guardados sean correctos', body(
    bk('Llave primaria', 'Un identificador único: no puede haber dos pacientes con el mismo número de expediente.'),
    bk('Llave foránea', 'Relaciona tablas: no se puede registrar una cita de un paciente que no existe.'),
    bk('Validaciones y restricciones', 'Reglas como «la fecha de nacimiento no puede ser del futuro» o «el teléfono lleva 10 dígitos».'),
    bk('Transacciones', 'Todo o nada: al cobrar, se registra el pago y se marca la cita como pagada, o no se hace ninguna de las dos.'),
    bk('Respaldos y bitácoras', 'Permiten regresar a un estado correcto y saber quién cambió qué.')),
    'La base de datos también se protege con reglas, no solo con contraseñas.')
c.A('🧰', '¿Qué control de integridad usas?', 'Elige la herramienta para cada necesidad.', [
    ['Guardar las contraseñas de los empleados', 'Hash con sal', 'Se guarda el hash con sal, nunca la contraseña.'],
    ['Que el laboratorio pruebe que el resultado no cambió y que lo envió él', 'HMAC', 'Hash + clave secreta compartida.'],
    ['Que el dentista firme recetas electrónicas sin poder negarlo después', 'Firma digital', 'Da no repudio con la clave privada.'],
    ['Que los pacientes comprueben que la página de citas es la verdadera', 'Certificado digital', 'El certificado HTTPS identifica al sitio.'],
    ['Que no existan dos expedientes con el mismo número', 'Llave primaria', 'La llave primaria es única.'],
], 'Contraseñas → sal · Mensaje con clave → HMAC · Firmar → firma · Identidad del sitio → certificado · Datos únicos → llave primaria.',
    ['Hash con sal', 'HMAC', 'Firma digital', 'Certificado digital', 'Llave primaria'])
c.Z('🗃️', 'Completa las reglas de la base de datos', 'Elige la palabra correcta para cada regla de la clínica.',
    '<p>El número de expediente es la {0}: no se repite.</p>'
    '<p>La tabla Citas usa una {1} para que cada cita pertenezca a un paciente que sí existe.</p>'
    '<p>Al cobrar, el pago y el estado de la cita se guardan en una {2}: se hace todo o nada.</p>'
    '<p>La regla «el teléfono lleva 10 dígitos» es una {3}.</p>'
    '<p>Las contraseñas se guardan como {4}.</p>',
    [['llave primaria', ['llave primaria', 'llave foránea', 'contraseña']],
     ['llave foránea', ['llave foránea', 'llave primaria', 'sal']],
     ['transacción', ['transacción', 'firma', 'bitácora']],
     ['validación', ['validación', 'transacción', 'llave foránea']],
     ['hash con sal', ['hash con sal', 'texto claro', 'llave primaria']]],
    'Única → primaria · Relación → foránea · Todo o nada → transacción.')
a_end = c.mark() - 1

# ───────────────────────── B · Estándar ─────────────────────────
b0 = c.mark()
c.L('🛞', 'Disponibilidad y alta disponibilidad', 'Bloque B · Que el servicio no se detenga', body(
    sp('En palabras sencillas', '<b>Disponibilidad</b> es que el servicio funcione cuando se necesita. <b>Alta disponibilidad</b> es diseñarlo para que siga funcionando aunque algo falle.'),
    bk('Punto único de falla', 'Una pieza que, si falla, detiene todo: un solo disco, un solo servidor, un solo proveedor de internet.'),
    bk('Redundancia', 'Tener repuesto: discos en <b>RAID</b>, dos fuentes de poder, <b>UPS</b> (no-break), dos proveedores de internet, servidores en <b>clúster</b> y <b>balanceo de carga</b>.'),
    ana('Piensa en…', 'La llanta de refacción del coche: no evita ponchar, pero te deja seguir.'),
    ex('En la clínica', 'El servidor de la agenda tiene dos discos en espejo (RAID 1) y un no-break. Si un disco falla o se va la luz, la agenda sigue.')),
    'Encuentra el punto único de falla y ponle repuesto.')
c.L('9️⃣', 'Los «nueves» de la disponibilidad', 'Bloque B · Cómo se mide', body(
    bk('99 %', 'Hasta 3.65 días fuera de servicio al año.'),
    bk('99.9 % (tres nueves)', 'Unas 8.76 horas al año.'),
    bk('99.99 % (cuatro nueves)', 'Unos 52.6 minutos al año.'),
    bk('99.999 % (cinco nueves)', 'Poco más de 5 minutos al año.'),
    ex('Cómo se calcula', 'Un año tiene 8,760 horas. Con 99.9 %, el tiempo fuera es el 0.1 %: 8,760 × 0.001 = <b>8.76 horas</b>.')),
    'Cada nueve extra cuesta más dinero y reduce el tiempo caído 10 veces.')
c.T('🧮', 'Calcula el tiempo fuera de servicio', 'Escribe solo el número. Un año = 8,760 horas.', [
    ['Un servicio tiene 99 % de disponibilidad. ¿Cuántas horas puede estar caído al año?', '87.6', '8,760 × 0.01 = 87.6 horas.', 'El 1 % de 8,760.', 'm', 0.05],
    ['Con 99.9 %, ¿cuántas horas al año?', '8.76', '8,760 × 0.001 = 8.76 horas.', 'El 0.1 % de 8,760.', 'm', 0.01],
    ['La agenda estuvo caída 4 horas de las 100 que debía funcionar esta semana. ¿Qué porcentaje estuvo disponible?', '96', '(96 ÷ 100) × 100 = 96 %.', 'Resta las horas caídas y divide entre el total.', 'm', 0.05],
    ['Con 99.99 %, ¿cuántos minutos al año? (redondea a un decimal)', '52.6', '8,760 × 0.0001 = 0.876 h × 60 = 52.56 ≈ 52.6 minutos.', 'Calcula las horas y multiplica por 60.', 'm', 0.1],
], 'Tiempo fuera = total × (100 − disponibilidad) ÷ 100.', 'm')
c.L('🏰', 'Defensa en profundidad', 'Bloque B · Varias capas de protección', body(
    sp('En palabras sencillas', 'Poner <b>varias capas de protección</b>, para que si una falla, las demás sigan protegiendo.'),
    bk('Las capas', 'Políticas y capacitación → seguridad física → red → equipo (host) → aplicación → datos.'),
    ana('Piensa en un castillo', 'Foso, muralla, guardias, puerta y caja fuerte. Un ladrón tendría que vencerlas todas.'),
    ex('En la clínica', 'Aunque un empleado abra un correo falso (falla la capacitación), el antivirus lo bloquea; y si no, los expedientes están cifrados y respaldados.')),
    'Nunca confíes en una sola protección.')
c.L('🚨', 'Respuesta a incidentes', 'Bloque B · Qué hacer cuando algo pasa', body(
    sp('En palabras sencillas', 'Un incidente es un evento que daña la seguridad: un virus, un robo de datos, un servidor caído. La respuesta sigue fases para no improvisar.'),
    bk('1. Preparación', 'Antes de que pase: plan, responsables, respaldos y herramientas.'),
    bk('2. Detección y análisis', 'Darse cuenta y entender qué pasó y qué tan grave es.'),
    bk('3. Contención, erradicación y recuperación', 'Aislar el problema, eliminar la causa y volver a funcionar.'),
    bk('4. Lecciones aprendidas', 'Revisar qué falló y mejorar para que no se repita.'),
    ana('Piensa en un simulacro de sismo', 'Te preparas antes, actúas con orden durante y revisas qué mejorar después.')),
    'Preparar · detectar · contener y recuperar · aprender.')
c.L('🌪️', 'Recuperación tras un desastre: RPO y RTO', 'Bloque B · Volver a funcionar', body(
    sp('En palabras sencillas', 'El plan de recuperación dice cómo volver a funcionar después de un desastre: incendio, inundación, ransomware.'),
    bk('RPO · ¿cuánta información puedo perder?', 'Si respaldas cada noche, en el peor caso pierdes un día de datos: RPO = 24 horas.'),
    bk('RTO · ¿en cuánto tiempo debo volver?', 'El tiempo máximo para que el servicio regrese. Si la clínica dice «la agenda debe volver en 2 horas», RTO = 2 h.'),
    bk('Regla 3-2-1', '3 copias, en 2 tipos de soporte, 1 fuera del lugar (por ejemplo, en la nube).'),
    ana('Piensa en…', 'Guardar la partida del videojuego: el RPO es cada cuánto guardas; el RTO es cuánto tardas en volver a jugar.')),
    'RPO mira hacia atrás (datos perdidos); RTO mira hacia adelante (tiempo para volver).')
c.O('🚨', 'Ordena la respuesta a un ransomware', 'La clínica descubre que sus archivos están cifrados. Ordena lo que deben hacer.', [
    ['Tener respaldos y un plan antes de que pase', 'Preparación: sin respaldos no hay recuperación.'],
    ['Detectar los archivos cifrados y analizar qué equipos están afectados', 'Detección y análisis.'],
    ['Desconectar de la red los equipos infectados', 'Contención: evita que se extienda.'],
    ['Eliminar el malware y restaurar los respaldos', 'Erradicación y recuperación.'],
    ['Revisar cómo entró y capacitar al personal', 'Lecciones aprendidas.'],
], 'Antes, durante y después.')
c.A('⏱️', '¿RPO o RTO?', 'Decide de qué meta habla cada frase.', [
    ['Respaldamos cada 4 horas, así que perderíamos máximo 4 horas de datos', 'RPO', 'Habla de cuánta información se puede perder.'],
    ['La agenda debe volver a funcionar en menos de 1 hora', 'RTO', 'Habla del tiempo para recuperar el servicio.'],
    ['No podemos perder más de un día de cobros', 'RPO', 'Pérdida de datos: RPO.'],
    ['El sistema de cobro puede estar caído máximo medio día', 'RTO', 'Tiempo fuera de servicio: RTO.'],
], 'Datos perdidos = RPO · Tiempo para volver = RTO.', ['RPO', 'RTO'])
c.A('🛞', '¿Qué mecanismo usarías?', 'Elige la solución de alta disponibilidad para cada riesgo.', [
    ['Que falle un disco del servidor', 'RAID (discos en espejo)', 'El otro disco tiene la misma información.'],
    ['Que se vaya la luz', 'UPS (no-break) o planta de luz', 'Da energía mientras regresa la electricidad.'],
    ['Que se caiga el internet', 'Segundo proveedor de internet', 'Un enlace de respaldo evita depender de uno.'],
    ['Que un solo servidor no aguante tantas visitas', 'Balanceo de carga', 'Reparte las visitas entre varios servidores.'],
    ['Que se incendie la clínica', 'Respaldo fuera del lugar (nube)', 'La copia externa sobrevive al desastre.'],
], 'Relaciona cada riesgo con su repuesto.')
b_end = c.mark() - 1

# ───────────────────────── C · Defensa de sistemas ─────────────────────────
c0 = c.mark()
c.L('💻', 'Protección del host', 'Bloque C · Cada computadora', body(
    sp('En palabras sencillas', 'Un <b>host</b> es cualquier equipo conectado: la PC de recepción, la laptop del dentista, el celular.'),
    bk('Medidas', 'Actualizaciones al día · antivirus o EDR · firewall local · cuenta estándar para trabajar · bloqueo de pantalla · cifrado del disco (BitLocker).'),
    ex('En la clínica', 'La PC de recepción usa cuenta estándar, se bloquea sola a los 5 minutos y tiene el disco cifrado.')),
    'Ya lo conoces de ASIN y del R.A. 2.1: cada equipo se protege a sí mismo.')
c.L('🗄️', 'Protección del servidor', 'Bloque C · El equipo que da servicio a todos', body(
    bk('Menos es más', 'Desactivar servicios y puertos que no se usan: cada servicio abierto es una puerta.'),
    bk('Mínimo privilegio', 'Cuentas de administrador solo para quien las necesita, con contraseñas fuertes y doble factor.'),
    bk('Bitácoras y monitoreo', 'Registrar accesos y cambios, y revisarlos.'),
    bk('Respaldos y parches', 'Respaldar a diario y aplicar actualizaciones en una ventana de mantenimiento.'),
    ana('Piensa en…', 'La bodega de una tienda: pocas puertas, pocas llaves, cámara y registro de quién entra.')),
    'Un servidor seguro tiene pocas puertas abiertas y alguien vigilándolas.')
c.L('🌐', 'Protección de la red', 'Bloque C · Lo que une a todos', body(
    bk('Firewall perimetral', 'Filtra lo que entra y sale de internet.'),
    bk('Segmentación (VLAN)', 'Separa la red: pacientes en el wifi de invitados, equipos médicos en otra red, administración en otra.'),
    bk('IDS / IPS', 'Detectan (y el IPS bloquea) tráfico sospechoso.'),
    bk('VPN', 'Túnel cifrado para conectarse desde fuera.'),
    bk('Wifi seguro', '<b>WPA2</b> o <b>WPA3</b> con contraseña fuerte; nunca una red abierta para los equipos internos.')),
    'Separar la red evita que un problema en un lado llegue a todo.')
c.L('🔐', 'Seguridad física', 'Bloque C · Lo que se puede tocar', body(
    bk('Control de acceso', 'El cuarto del servidor bajo llave o con tarjeta; solo entra personal autorizado.'),
    bk('Vigilancia', 'Cámaras y registro de visitas.'),
    bk('Energía y ambiente', 'UPS, regulador, ventilación y extintor adecuado para equipo eléctrico.'),
    bk('Equipos y medios', 'Candados para laptops, destruir discos viejos antes de tirarlos.'),
    warn('Recuerda', 'De nada sirve el mejor firewall si alguien puede entrar y llevarse el servidor.')),
    'La seguridad empieza por la puerta.')
c.A('🧱', '¿Qué capa protege?', 'Clasifica cada medida.', [
    ['Cifrar el disco de la laptop del dentista', 'Host', 'Protege a ese equipo.'],
    ['Desactivar en el servidor los servicios que no se usan', 'Servidor', 'Reduce las puertas del servidor.'],
    ['Separar el wifi de pacientes de la red interna', 'Red', 'Es segmentación de la red.'],
    ['Poner llave al cuarto del servidor', 'Física', 'Controla el acceso físico.'],
    ['Instalar un IDS que avise de tráfico raro', 'Red', 'Vigila el tráfico de la red.'],
    ['Usar cuenta estándar en la PC de recepción', 'Host', 'Es una medida del equipo.'],
    ['Instalar un no-break para el servidor', 'Física', 'Protege la energía del equipo.'],
], 'Un equipo → host · El que da servicio → servidor · Conexiones → red · Lo que se toca → física.', ['Host', 'Servidor', 'Red', 'Física'])
c.A('⚖️', '¿Buena o mala práctica?', 'Decide si cada práctica de la clínica es buena o mala.', [
    ['Dejar abierto el escritorio remoto del servidor a todo internet', 'Mala práctica', 'Es una puerta abierta a cualquier atacante; se usa VPN.'],
    ['Usar WPA3 con contraseña fuerte en la red interna', 'Buena práctica', 'Cifra el wifi y dificulta el acceso.'],
    ['Que todos usen la cuenta de administrador para ir más rápido', 'Mala práctica', 'Viola el mínimo privilegio.'],
    ['Tirar a la basura un disco viejo con expedientes sin borrarlo', 'Mala práctica', 'Cualquiera podría recuperar los datos.'],
    ['Revisar cada semana las bitácoras del servidor', 'Buena práctica', 'Permite detectar accesos extraños.'],
], 'Pregúntate: ¿abre una puerta o la cierra?', ['Buena práctica', 'Mala práctica'])
c.W('✍️', 'Defiende la clínica en 4 capas', 'Aplica lo aprendido.',
    'Escribe una medida para cada capa de la clínica: <b>host</b>, <b>servidor</b>, <b>red</b> y <b>física</b>.',
    [['Tiene al menos 25 palabras', 'palabras:25'],
     ['Una medida para el host (equipo, PC, laptop, antivirus, cifrado…)', '(host|pc|computadora|laptop|equipo|antivirus|bitlocker|cifra)'],
     ['Una medida para el servidor', '(servidor)'],
     ['Una medida para la red (firewall, VLAN, wifi, IDS, VPN…)', '(red|firewall|vlan|wifi|ids|ips|vpn|wpa)'],
     ['Una medida física (llave, cámara, no-break, acceso…)', '(llave|camara|no-break|nobreak|ups|acceso fisico|cuarto|candado|tarjeta|fisica)']],
    'Una oración por capa.', 'Ejemplo: Host: las PCs tienen antivirus y disco cifrado. Servidor: …')
c_end = c.mark() - 1

# ───────────────────────── D · Dominio de la ciberseguridad ─────────────────────────
d0 = c.mark()
c.L('🐞', 'Vulnerabilidades: CVE y CVSS', 'Bloque D · Dominio de vulnerabilidades', body(
    sp('En palabras sencillas', 'Una <b>vulnerabilidad</b> es una falla en un programa o equipo que un atacante puede aprovechar. Las que se hacen públicas reciben un identificador <b>CVE</b>, por ejemplo CVE-2024-12345.'),
    bk('CVSS', 'Calificación de 0 a 10 para saber qué tan grave es: <b>Baja</b> 0.1–3.9 · <b>Media</b> 4.0–6.9 · <b>Alta</b> 7.0–8.9 · <b>Crítica</b> 9.0–10.'),
    bk('Dónde consultarlas', '<b>cve.org</b> y la base del NIST (<b>nvd.nist.gov</b>).'),
    ana('Piensa en…', 'Los avisos de «llamado a revisión» de los coches: el fabricante publica la falla, su número y qué tan peligrosa es, para que la arregles.'),
    ex('En la clínica', 'El sistema de citas tiene una CVE con CVSS 9.8: es crítica y se actualiza hoy mismo. Una de 3.1 se programa para el siguiente mantenimiento.')),
    'Primero se corrigen las críticas y altas.')
c.A('🐞', 'Clasifica la gravedad', 'Según su calificación CVSS, ¿qué tan grave es cada vulnerabilidad?', [
    ['CVE con CVSS 9.8', 'Crítica', '9.0 a 10 es crítica.'],
    ['CVE con CVSS 5.3', 'Media', '4.0 a 6.9 es media.'],
    ['CVE con CVSS 7.5', 'Alta', '7.0 a 8.9 es alta.'],
    ['CVE con CVSS 2.1', 'Baja', '0.1 a 3.9 es baja.'],
    ['CVE con CVSS 10.0', 'Crítica', 'Es la calificación máxima.'],
], 'Baja < 4 · Media < 7 · Alta < 9 · Crítica 9 o más.', ['Baja', 'Media', 'Alta', 'Crítica'])
c.L('🧭', 'Ética y principios rectores', 'Bloque D · Saber mucho exige responsabilidad', body(
    sp('En palabras sencillas', 'Quien sabe de ciberseguridad puede proteger o dañar. La ética marca la diferencia.'),
    bk('Autorización por escrito', 'Solo se revisa o prueba un sistema con permiso firmado del dueño. Sin permiso es un delito: el Código Penal Federal castiga el acceso ilícito a sistemas (artículos 211 bis 1 al 211 bis 7).'),
    bk('Privacidad', 'Proteger los datos personales que veas durante tu trabajo.'),
    bk('No causar daño', 'Probar sin afectar el servicio ni la información.'),
    bk('Divulgación responsable', 'Reportar las fallas al dueño y darle tiempo de corregirlas antes de hacerlas públicas.'),
    ex('Hacker ético', 'Una empresa contrata a una especialista para atacar su propia red y encontrar fallas antes que los delincuentes. Firma un contrato con lo que puede y no puede hacer.')),
    'Mismo conocimiento, distinta intención: el permiso lo cambia todo.')
c.A('🧭', '¿Es ético?', 'Decide si cada acción es ética o no.', [
    ['Escanear la red de la escuela por curiosidad, sin pedir permiso', 'No es ético', 'Sin autorización por escrito es acceso no autorizado.'],
    ['Reportar al dueño una falla que encontraste en su página', 'Es ético', 'Es divulgación responsable.'],
    ['Publicar en redes los datos de pacientes que viste en una auditoría', 'No es ético', 'Viola la privacidad.'],
    ['Hacer una prueba de penetración con contrato firmado', 'Es ético', 'Tiene autorización y reglas claras.'],
    ['Usar la contraseña de un compañero que dejó su sesión abierta', 'No es ético', 'Es usar una cuenta ajena sin permiso.'],
], 'Pregúntate: ¿tengo permiso?, ¿protejo la privacidad?, ¿causo daño?', ['Es ético', 'No es ético'])
c.L('🛠️', 'Herramientas de ciberseguridad', 'Bloque D · Lo que usa un profesional', body(
    bk('Nmap', 'Descubre qué equipos hay en una red y qué puertos tienen abiertos.'),
    bk('Wireshark', 'Captura y analiza el tráfico de la red.'),
    bk('Escáneres de vulnerabilidades', 'Como OpenVAS: buscan fallas conocidas (CVE) en los equipos.'),
    bk('Gestores de contraseñas', 'Como Bitwarden: guardan contraseñas largas y únicas, cifradas.'),
    bk('VirusTotal', 'Analiza un archivo o enlace con muchos antivirus a la vez.'),
    warn('Recuerda', 'Usar Nmap o Wireshark en una red ajena sin permiso es un delito.')),
    'Una herramienta es tan ética como quien la usa.')
c.A('🛠️', '¿Qué herramienta usas?', 'Elige la herramienta para cada tarea autorizada.', [
    ['Saber qué puertos tiene abiertos el servidor de la clínica', 'Nmap', 'Nmap descubre equipos y puertos.'],
    ['Ver qué tráfico sale de la PC de recepción', 'Wireshark', 'Wireshark captura el tráfico.'],
    ['Revisar un archivo adjunto sospechoso', 'VirusTotal', 'Lo analiza con decenas de antivirus.'],
    ['Buscar fallas conocidas (CVE) en todos los equipos', 'Escáner de vulnerabilidades', 'Compara los equipos con bases de CVE.'],
    ['Guardar contraseñas distintas para cada sistema', 'Gestor de contraseñas', 'Las guarda cifradas.'],
], 'Puertos → Nmap · Tráfico → Wireshark · Archivo → VirusTotal · Fallas → escáner · Contraseñas → gestor.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario (1 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Integridad', 'Que la información no se altere sin autorización.'),
    bk('Hash', 'Resumen de tamaño fijo, de un solo sentido, que funciona como huella de los datos.'),
    bk('SHA-256', 'Algoritmo de hash seguro de 64 caracteres hexadecimales.'),
    bk('Sal (salting)', 'Valor aleatorio que se agrega a la contraseña antes del hash.'),
    bk('HMAC', 'Hash con clave secreta compartida.'),
    bk('Firma digital', 'Se crea con la clave privada y se verifica con la pública.'),
    bk('Certificado', 'Documento de una autoridad que asocia una clave pública con su dueño.'),
    bk('No repudio', 'Que el emisor no pueda negar que envió o firmó algo.'),
    bk('Llave primaria', 'Identificador único de un registro.')))
c.L('📖', 'Glosario (2 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Alta disponibilidad', 'Diseño para que el servicio siga aunque algo falle.'),
    bk('Punto único de falla', 'Pieza que, si falla, detiene todo.'),
    bk('RAID', 'Varios discos trabajando juntos para tener redundancia.'),
    bk('Defensa en profundidad', 'Varias capas de protección.'),
    bk('RPO', 'Cuánta información se puede perder.'),
    bk('RTO', 'En cuánto tiempo debe volver el servicio.'),
    bk('CVE', 'Identificador público de una vulnerabilidad.'),
    bk('CVSS', 'Calificación de gravedad de 0 a 10.'),
    bk('VLAN', 'Red virtual para separar partes de la red.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Laboratorio del grupo 511: <b>lunes 17:20-18:10</b> y <b>viernes 18:10-19:50</b>. Cada práctica tiene versión para celular.', 'sp'),
    bk('Bloque A · 23 y 26-oct', 'Viernes 23: hash y laboratorio de hash en clase. <b>Lunes 26 (primera hora, laboratorio): Práctica 1</b>; después salting, HMAC, firmas e integridad en bases de datos.'),
    bk('Bloque B · 26-oct y 2-nov', 'Lunes 26 (últimas horas): disponibilidad y los nueves. Viernes 30 es CTEC. Lunes 2-nov: defensa en profundidad, incidentes y RPO/RTO; <b>Práctica 2</b> como tarea o en celular.'),
    bk('Bloque C · 2 y 6-nov', '<b>Viernes 6 (laboratorio): Práctica 3</b> y lecciones de defensa de sistemas.'),
    bk('Bloque D y evaluación · lunes 9-nov', 'Vulnerabilidades, ética y herramientas; los alumnos terminan y entregan el reporte en la actividad de la plataforma (organización asignada a cada uno). La actividad se desbloquea al completar este material.'),
    bk('Nota', 'Las herramientas como Nmap y Wireshark solo se usan en una red de práctica autorizada por ti.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🏥', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🧬', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🛞', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🧱', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '🧭', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🏥",t:"Empieza aquí",d:"Integridad, disponibilidad y defensa con el caso de una clínica.",time:"20 min",obj:["Distinguir integridad, disponibilidad y confidencialidad","Conocer el caso y la evidencia final"],sum:["Integridad = sin cambios · Disponibilidad = que funcione.","Entregas un reporte con la organización asignada."],q:"¿Qué servicio que usas a diario sería un problema si se cayera un día entero?"},
a:{k:"Bloque A",l:"A",ic:"🧬",t:"Controles de integridad",d:"Hash, salting, HMAC, firmas, certificados y bases de datos.",time:"120 min",obj:["Explicar las propiedades del hash","Describir por qué se usa sal en las contraseñas","Elegir entre hash, HMAC, firma digital y certificado"],sum:["El hash es una huella de un solo sentido; MD5 y SHA-1 ya no son seguros.","La sal hace que contraseñas iguales tengan hashes distintos.","HMAC = hash + clave · Firma = clave privada · Certificado = identidad avalada."],q:"¿Por qué una página nunca debería poder enviarte tu contraseña por correo si la olvidas?"},
b:{k:"Bloque B",l:"B",ic:"🛞",t:"Estándar de ciberseguridad",d:"Alta disponibilidad, defensa en profundidad, incidentes y recuperación.",time:"150 min",obj:["Identificar puntos únicos de falla y su redundancia","Calcular el tiempo fuera de servicio","Ordenar las fases de respuesta a incidentes y distinguir RPO de RTO"],sum:["Redundancia: RAID, UPS, dos enlaces, clúster y balanceo.","99.9 % ≈ 8.76 h al año fuera de servicio.","RPO = datos perdidos · RTO = tiempo para volver."],q:"¿Cada cuánto respaldas tus fotos? ¿Cuál sería tu RPO?",rev:[["Si cambias una letra del texto, su hash…",["Cambia por completo","Cambia una letra","No cambia"],0,"Un cambio mínimo cambia toda la huella."],["La sal sirve para…",["Que contraseñas iguales tengan hashes distintos","Cifrar el disco","Acelerar el inicio de sesión"],0,"Evita las tablas precalculadas."]]},
c:{k:"Bloque C",l:"C",ic:"🧱",t:"Defensa de sistemas y dispositivos",d:"Host, servidor, red y seguridad física.",time:"100 min",obj:["Proponer medidas para host, servidor y red","Reconocer la importancia de la seguridad física"],sum:["Host: parches, antivirus, cuenta estándar y cifrado.","Servidor: pocos servicios, mínimo privilegio, bitácoras y respaldos.","Red: firewall, VLAN, IDS/IPS, VPN y WPA2/WPA3 · Física: acceso, energía y medios."],q:"¿Qué capa de protección es la más débil en tu casa?",rev:[["«No podemos perder más de 4 horas de datos» es un…",["RPO","RTO","CVE"],0,"Habla de datos perdidos."],["Un no-break evita…",["Que se apague el equipo si se va la luz","Los virus","Las contraseñas débiles"],0,"Es redundancia de energía."]]},
d:{k:"Bloque D",l:"D",ic:"🧭",t:"Dominio de la ciberseguridad",d:"Vulnerabilidades, ética y herramientas.",time:"60 min",obj:["Interpretar un CVE y su CVSS","Aplicar principios éticos","Relacionar herramientas con su uso"],sum:["CVE identifica la falla; CVSS dice qué tan grave es.","Sin autorización por escrito no se prueba nada.","Nmap, Wireshark, escáneres, gestores de contraseñas y VirusTotal."],q:"¿Qué harías si encuentras una falla en la página de tu escuela?",rev:[["Separar el wifi de pacientes de la red interna es…",["Segmentación de red","Seguridad física","Un hash"],0,"Se hace con VLAN o redes separadas."],["El servidor debe tener…",["Solo los servicios necesarios","Todos los puertos abiertos","Una sola contraseña para todos"],0,"Menos servicios, menos puertas."]]}
'''

ILL = r'''
ILL["Hash: la huella digital de los datos"]=function(){return flow([["📄","Expediente"],["⚙️","SHA-256"],["🧬","9f86d0…|(64 car.)"]],"Un dato entra y sale su huella")};
ILL["La técnica salting"]=function(){return SV(340,130,R_(10,8,320,50,"s")+T_(20,28,"123456 + sal «a7f2» → hash 3c9e…","t","start")+T_(20,46,"123456 + sal «91bd» → hash e04a…","t","start")+R_(10,70,320,50,"b")+T_(170,92,"Misma contraseña, hashes distintos","tw")+T_(170,108,"Las tablas precalculadas no sirven","tw"),"Salting")};
ILL["HMAC: hash con clave secreta"]=function(){return flow([["🧪","Laboratorio"],["🔑","Mensaje +|clave secreta"],["🔏","HMAC"],["🏥","Clínica|verifica"]],"HMAC entre el laboratorio y la clínica")};
ILL["Firmas digitales y certificados"]=function(){return SV(340,130,R_(10,10,150,110,"b")+E_(85,50,"🔐",28)+T_(85,80,"Clave privada","tw")+T_(85,98,"firma","tw")+R_(180,10,150,110,"s")+E_(255,50,"🔓",28)+T_(255,80,"Clave pública")+T_(255,98,"verifica","tm"),"Clave privada firma, pública verifica")};
ILL["Disponibilidad y alta disponibilidad"]=function(){return SV(340,130,T_(85,16,"Sin redundancia","t")+R_(30,26,110,40,"r")+T_(85,50,"1 disco","tw")+E_(85,98,"💥",24)+T_(255,16,"Con redundancia","t")+R_(200,26,110,40,"g")+T_(255,50,"Disco 1","tw")+R_(200,74,110,40,"g")+T_(255,98,"Disco 2 (espejo)","tw"),"Punto único de falla y redundancia")};
ILL["Los «nueves» de la disponibilidad"]=function(){var r=[["99 %","3.65 días",100],["99.9 %","8.76 h",62],["99.99 %","52.6 min",30],["99.999 %","5.3 min",10]],o='';r.forEach(function(x,i){var y=8+i*32;o+=T_(70,y+18,x[0],"t","end")+R_(80,y+4,2*x[2],20,i==3?"g":"b",4)+T_(90+2*x[2],y+18,x[1],"t","start")});return SV(340,136,o,"Tiempo fuera de servicio por año")};
ILL["Defensa en profundidad"]=function(){var l=["Políticas","Física","Red","Host","Aplicación","Datos"],o='';l.forEach(function(x,i){var r=76-i*12;o+=C_(170,80,r,i==5?"b":"s")});o+=T_(170,85,"Datos","tw");l.slice(0,5).forEach(function(x,i){o+=T_(170,14+i*12,x,"tm")});return SV(340,160,o,"Capas de protección")};
ILL["Respuesta a incidentes"]=function(){return flow([["📋","Preparación"],["🔎","Detección|y análisis"],["🧯","Contener y|recuperar"],["📚","Lecciones|aprendidas"]],"Fases de la respuesta a incidentes")};
ILL["Recuperación tras un desastre: RPO y RTO"]=function(){return SV(340,110,'<line x1="20" y1="60" x2="320" y2="60" class="kb"/>'+R_(30,40,120,40,"a",6)+T_(90,57,"RPO:|datos perdidos","td")+E_(170,68,"💥",24)+R_(190,40,120,40,"b",6)+T_(250,57,"RTO:|tiempo caído","tw")+T_(90,100,"último respaldo → desastre","tm")+T_(250,100,"desastre → servicio de vuelta","tm"),"RPO y RTO en una línea de tiempo")};
ILL["Protección de la red"]=function(){return grid3([["🧱","Firewall"],["🔀","VLAN"],["🚨","IDS / IPS"],["🚇","VPN"],["📶","WPA2 /|WPA3"]],"Medidas de red")};
ILL["Vulnerabilidades: CVE y CVSS"]=function(){var s=[["Baja","0.1–3.9","g"],["Media","4–6.9","a"],["Alta","7–8.9","r"],["Crítica","9–10","b"]],o='';s.forEach(function(x,i){var X=10+i*82;o+=R_(X,20,76,60,x[2],6)+T_(X+38,46,x[0],x[2]=="a"?"td":"tw")+T_(X+38,64,x[1],x[2]=="a"?"td":"tw")});return SV(340,96,o,"Escala CVSS")};
'''

EXH = r'''
function cw_(t,b,ps){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:'+(ps?'#012456':'#0c0c0c')+';color:#eee;padding:10px;font:12.5px/1.45 Consolas,monospace;white-space:pre-wrap;overflow-x:auto">'+b+'</pre></div>'}
EXH.hash_ps=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno\\Documents&gt; Set-Content expediente.txt "Ana Lopez - alergia a la penicilina"\nPS C:\\Users\\Alumno\\Documents&gt; Get-FileHash expediente.txt\n\nAlgorithm  Hash                                                    Path\n---------  ----                                                    ----\nSHA256     5C1E9A…(64 caracteres)…7B2D                            C:\\…\\expediente.txt',true),['Get-FileHash calcula SHA-256 por defecto.','Copia el hash completo en tu tabla.'])};
EXH.hash_cambio=function(){return exw('<table class="mtb"><tr><th>Prueba</th><th>Contenido</th><th>Hash (primeros 8)</th><th>¿Igual al original?</th></tr><tr><td>Original</td><td>Ana Lopez - alergia a la penicilina</td><td>5C1E9A0F</td><td>—</td></tr><tr><td>Cambio 1 letra</td><td>Ana Lopez - alergia a la penicilinA</td><td>D83B72C4</td><td>No</td></tr><tr><td>Igual al original</td><td>Ana Lopez - alergia a la penicilina</td><td>5C1E9A0F</td><td>Sí</td></tr></table>',['Cambia una sola letra, guarda y vuelve a calcular.','Regresa el texto original y comprueba que el hash vuelve a coincidir.'])};
EXH.certutil=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documents&gt;certutil -hashfile expediente.txt SHA256\nHash SHA256 de expediente.txt:\n5c1e9a…7b2d\nCertUtil: -hashfile comando completado correctamente.'),['Es otra forma de calcular el hash, desde CMD.'])};
EXH.hash_cel=function(){return exw('<div class="mbox">🧪 <b>Laboratorio de hash</b> (Bloque A de este material)<br>Texto: Ana López · alergia a la penicilina<br>Huella: 2b7f…<br>Cambiaron <b>61 de 64</b> caracteres al cambiar una letra.</div>',['Usa el laboratorio de hash de este material.','Toma captura del texto original y del texto con una letra cambiada.'])};
EXH.descarga_hash=function(){return exw(mw('Página de descarga (ejemplo)','<div style="line-height:1.8">Archivo: <b>programa-setup.exe</b><br>SHA-256: <b>e3b0c442…b855</b> '+mk(1)+'</div>'),['Muchos sitios publican el hash de sus descargas.','Si el hash de tu archivo coincide, no fue alterado en el camino.'])};
EXH.tabla_disp=function(){return exw('<table class="mtb"><tr><th>Servicio</th><th>Punto único de falla</th><th>Redundancia propuesta</th></tr><tr><td>Agenda en línea</td><td>Un solo disco</td><td>RAID 1 (espejo)</td></tr><tr><td>Cobro</td><td>Un solo proveedor de internet</td><td>Segundo proveedor o datos móviles</td></tr><tr><td>Servidor</td><td>Energía eléctrica</td><td>UPS (no-break)</td></tr></table>',['Mínimo 3 servicios de tu organización.'])};
EXH.rpo_rto=function(){return exw('<table class="mtb"><tr><th>Servicio</th><th>Respaldo</th><th>RPO</th><th>RTO</th></tr><tr><td>Expedientes</td><td>Diario 23:00, en la nube</td><td>24 h</td><td>4 h</td></tr><tr><td>Agenda</td><td>Cada hora</td><td>1 h</td><td>1 h</td></tr></table>',['RPO sale de cada cuánto respaldas.','RTO es lo que la organización acepta estar sin servicio.'])};
EXH.incidente=function(){return exw('<table class="mtb"><tr><th>Fase</th><th>¿Qué haría la clínica ante un ransomware?</th></tr><tr><td>Preparación</td><td>Respaldos 3-2-1 y lista de responsables</td></tr><tr><td>Detección y análisis</td><td>Archivos con extensión rara; revisar qué equipos</td></tr><tr><td>Contención, erradicación y recuperación</td><td>Desconectar equipos, limpiar y restaurar</td></tr><tr><td>Lecciones aprendidas</td><td>Capacitar contra correos falsos</td></tr></table>',['Usa el incidente de tu organización asignada.'])};
EXH.seg_win=function(){return exw(mw('Seguridad de Windows','<div class="mm"><span>🛡️ Protección antivirus y contra amenazas ✅</span><span>🔥 Firewall y protección de red ✅</span><span>🔑 Protección de cuentas ✅</span><span>💻 Seguridad del dispositivo ⚠️ '+mk(1)+'</span></div>'),['Revisa cada sección y anota su estado.','Si una tiene advertencia, explica qué significa.'])};
EXH.checklist_host=function(){return exw('<table class="mtb"><tr><th>Medida del host</th><th>¿Cumple?</th><th>Evidencia</th></tr><tr><td>Actualizaciones al día</td><td>✅</td><td>Captura de Windows Update</td></tr><tr><td>Antivirus activo</td><td>✅</td><td>Captura de Seguridad de Windows</td></tr><tr><td>Cuenta estándar</td><td>❌</td><td>Uso cuenta de administrador</td></tr><tr><td>Bloqueo automático</td><td>✅</td><td>5 minutos</td></tr></table>',['Mínimo 6 medidas, con su evidencia.'])};
EXH.cve=function(){return exw(mw('nvd.nist.gov (ejemplo)','<div style="line-height:1.8"><b>CVE-2024-11477</b> '+mk(1)+'<br>Producto: 7-Zip<br>CVSS 3.x: <b>7.8 ALTA</b> '+mk(2)+'<br>Solución: actualizar a la versión 24.07 o posterior '+mk(3)+'</div>'),['Identificador CVE.','Calificación y gravedad.','Qué hay que hacer.'])};
EXH.cel_checklist=function(){return exw(mp('Ajustes › Seguridad','<div class="mbox">🔒 Bloqueo de pantalla: PIN ✅</div><div class="mbox" style="margin-top:6px">🛡️ Play Protect: sin apps dañinas ✅</div><div class="mbox" style="margin-top:6px">🔄 Parche de seguridad: 1 sep 2026 ⚠️</div>'),['Haz la lista de medidas de tu celular como host.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Comprueba la integridad con hash',
     'prog': 'Bloque A · Algoritmos de hash e integridad de archivos',
     'min': 50, 'lug': 'Laboratorio, lunes 26-oct (primera hora) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'PowerShell o Símbolo del sistema', 'Documento para tu reporte'],
                'steps': [
                    ['Crea expediente.txt con un texto y calcula su hash con Get-FileHash. Toma captura.', 'hash_ps'],
                    ['Calcula el mismo hash con certutil desde CMD y comprueba que es igual.', 'certutil'],
                    ['Cambia una sola letra, guarda y vuelve a calcular. Regresa el texto original y calcula otra vez.', 'hash_cambio'],
                    ['Busca una página de descarga que publique el hash de su archivo y explica para qué sirve.', 'descarga_hash'],
                    'Escribe en 4 renglones cómo usarías el hash para proteger los expedientes de tu organización.']},
         'cel': {'mat': ['Celular', 'Este material (laboratorio de hash)', 'Documento o notas para tu reporte'],
                 'steps': [
                     ['En el laboratorio de hash escribe un dato y toma captura de su huella.', 'hash_cel'],
                     ['Cambia una letra y captura cuántos caracteres de la huella cambiaron.', 'hash_cel'],
                     ['Activa la sal, escribe dos veces la misma contraseña de prueba y explica por qué cambia la huella.', 'hash_cel'],
                     ['Busca una página de descarga que publique el hash de su archivo y explica para qué sirve.', 'descarga_hash'],
                     'Escribe en 4 renglones cómo usarías el hash para proteger los expedientes de tu organización.']}},
     'entrega': ['Capturas y tabla de pruebas dentro de tu reporte.'],
     'rub': [['Hash calculado correctamente', 25], ['Prueba con una letra cambiada', 25], ['Explicación de la descarga verificada', 20], ['Aplicación a la organización', 30]]},
    {'id': 'pr2', 'n': 2, 't': 'Plan de disponibilidad y respuesta a incidentes',
     'prog': 'Bloque B · Alta disponibilidad, respuesta a incidentes y recuperación',
     'min': 100, 'lug': 'Aula, casa o celular (semana del 26-oct al 2-nov)',
     'modes': {
         'pc': {'mat': ['Word o Documentos de Google', 'Tu organización asignada en la actividad de la plataforma'],
                'steps': [
                    ['Haz la tabla de puntos únicos de falla de tu organización y su redundancia.', 'tabla_disp'],
                    'Calcula cuántas horas al año podría estar caído su servicio principal con 99 % y con 99.9 %.',
                    ['Define respaldos, RPO y RTO de 2 servicios.', 'rpo_rto'],
                    ['Describe las 4 fases de respuesta para el incidente de tu organización.', 'incidente'],
                    'Explica en 3 renglones cómo aplicarías la defensa en profundidad.']},
         'cel': {'mat': ['Documentos de Google o notas', 'Tu organización asignada en la actividad de la plataforma'],
                 'steps': [
                     ['Haz la tabla de puntos únicos de falla de tu organización y su redundancia.', 'tabla_disp'],
                     'Calcula cuántas horas al año podría estar caído su servicio principal con 99 % y con 99.9 %.',
                     ['Define respaldos, RPO y RTO de 2 servicios.', 'rpo_rto'],
                     ['Describe las 4 fases de respuesta para el incidente de tu organización.', 'incidente'],
                     'Explica en 3 renglones cómo aplicarías la defensa en profundidad.']}},
     'entrega': ['Tablas y respuestas dentro de tu reporte.'],
     'rub': [['Puntos de falla y redundancia', 25], ['Cálculo de disponibilidad', 15], ['RPO y RTO bien definidos', 25], ['Fases del incidente', 25], ['Defensa en profundidad', 10]]},
    {'id': 'pr3', 'n': 3, 't': 'Revisa la defensa de un equipo y busca vulnerabilidades',
     'prog': 'Bloques C y D · Protección del host y dominio de vulnerabilidades',
     'min': 100, 'lug': 'Laboratorio, viernes 6-nov o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Navegador', 'Documento para tu reporte'],
                'steps': [
                    ['Abre Seguridad de Windows y captura el estado de cada sección.', 'seg_win'],
                    ['Haz la lista de cotejo de protección del host con 6 medidas y su evidencia.', 'checklist_host'],
                    ['En nvd.nist.gov busca una vulnerabilidad de un programa que uses (por ejemplo 7-Zip o tu navegador). Anota su CVE, CVSS y solución.', 'cve'],
                    'Propón una medida de servidor, una de red y una física para tu organización.',
                    'Escribe 3 principios éticos que seguirías si te contrataran para revisar esa organización.']},
         'cel': {'mat': ['Celular', 'Navegador', 'Documento o notas para tu reporte'],
                 'steps': [
                     ['Revisa en Ajustes la seguridad de tu celular y haz su lista de cotejo.', 'cel_checklist'],
                     ['En nvd.nist.gov busca una vulnerabilidad de Android o de una app que uses. Anota su CVE, CVSS y solución.', 'cve'],
                     'Propón una medida de servidor, una de red y una física para tu organización.',
                     'Escribe 3 principios éticos que seguirías si te contrataran para revisar esa organización.']}},
     'entrega': ['Capturas, lista de cotejo y ficha del CVE dentro de tu reporte.'],
     'rub': [['Revisión del host con evidencia', 30], ['CVE con CVSS y solución', 25], ['Medidas de servidor, red y física', 25], ['Principios éticos', 20]]},
]

EVALUATION = {
    'course': 'MTCS-20 · Manejo de tecnologías de ciberseguridad · Unidad 2',
    'ra': 'R.A. 2.2', 'title': 'Reporte de principios y tecnologías',
    'data': [
        ('Resultado de aprendizaje', 'Utiliza principios y tecnologías de confidencialidad empleando los protocolos tecnológicos aplicados en la seguridad cibernética.'),
        ('Actividad de evaluación', '2.2.1 Elabora un reporte demostrando el uso de principios y tecnologías de confidencialidad aplicados en la ciberseguridad, evidenciando estándar, defensa de sistemas y dominio de ciberseguridad.'),
        ('Evidencia', 'Reporte (PDF)'),
        ('Ponderación', '15% (según el programa)'),
        ('Entrega', 'Lunes 9 de noviembre, en la actividad R.A. 2.2 de la plataforma'),
    ],
    'situation': 'En la actividad de evaluación de la plataforma tienes asignada una organización, con su número de usuarios, equipos, un incidente reciente y el tiempo máximo sin servicio que acepta. Elabora un reporte que proponga cómo proteger su integridad, mantener su disponibilidad y defender sus sistemas. Tus tres prácticas son la base.',
    'hint': 'Responde siempre para TU organización: cada sección debe mencionar sus datos (servicios, incidente y tiempo sin servicio).',
    'steps': [
        ('Contexto', ['Describe la organización asignada, la información que maneja y los servicios que no pueden detenerse.']),
        ('Integridad (Bloque A)', ['Explica cómo usarías hash con sal, HMAC o firma digital y certificados, y cómo cuidarías la integridad de su base de datos.']),
        ('Estándar (Bloque B)', ['Propón redundancia para sus puntos únicos de falla y calcula su disponibilidad.', 'Define respaldos, RPO y RTO de acuerdo con el tiempo máximo sin servicio.', 'Describe las 4 fases de respuesta para su incidente reciente.']),
        ('Defensa de sistemas (Bloque C)', ['Medidas para host, servidor, red y seguridad física.']),
        ('Dominio (Bloque D)', ['Una vulnerabilidad real (CVE y CVSS) que afectaría a la organización y cómo la corregirías.', 'Principios éticos y herramientas que usarías con autorización.']),
        ('Entrega', ['Llena las secciones de la actividad en la plataforma y adjunta tu reporte en PDF.']),
    ],
    'rubric': [('Contexto de la organización', 10), ('Controles de integridad', 20), ('Disponibilidad, RPO/RTO y respuesta al incidente', 25), ('Defensa de sistemas en 4 capas', 20), ('Vulnerabilidad, ética y herramientas', 15), ('Redacción y presentación', 10)],
    'deliver': ['Un archivo PDF con tu reporte.', 'Se entrega en la actividad R.A. 2.2 de la plataforma, junto con las secciones escritas.'],
}
