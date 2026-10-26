"""EDOA-20 · R.A. 4.3 · Usar el correo electrónico y la mensajería instantánea con responsabilidad.

Cierra la Unidad 4 con la cuenta cafeteria@escuelita.mx: redactar y enviar, organizar la bandeja, usar el correo
con responsabilidad y la mensajería instantánea. Incluye cuatro simuladores (net_sim.js en modo mail).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-4.3'
CODE_PREFIX = 'EDOA43'
FILE = 'edoa-ra43-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 4.3 · Correo y mensajería'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 4.3 · Correo y mensajería'
HERO_KICK = 'EDOA-20 · R.A. 4.3'
HERO_TITLE = 'Comunícate como profesional'
HERO_TEXT = 'Redacta, envía, organiza y responde correos con responsabilidad, y usa la mensajería instantánea sin riesgos.'
EV_SHORT = 'entrega el historial impreso de envío y recepción de mensajes.'
EV_CARD = 'Historial de mensajes R.A. 4.3'
RA = 'R.A. 4.3'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores de correo y mensajería'], 'c': ['Construye', 'Prácticas con tu correo']}

_DIR = Path(__file__).parent
EXTRA_JS = (_DIR / 'xl3_sim.js').read_text(encoding='utf8') + '\n' + (_DIR / 'net_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".netsim"))nInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".netsim"))return nCheck(d);\n'),
]

c = Course()

ME = 'cafeteria@escuelita.mx'


def msg(n, frm, subj, text, h, box='in', to=ME, cc='', att=None, unread=True, rr=False):
    return {'n': n, 'box': box, 'from': frm, 'to': to, 'cc': cc, 'subj': subj, 'body': text, 'h': h, 'unread': unread, 'att': att or [], 'rr': rr}


INBOX = [
    msg(1, 'direccion@escuelita.mx', 'Horario de diciembre', 'Buen día. A partir del 14 de diciembre la cafetería abre de 7:00 a 13:00. Por favor confirma de recibido.\n\nDirección', 'Lun 08:05', to=f'{ME}, papeleria@escuelita.mx', cc='orientacion@escuelita.mx', rr=True),
    msg(2, 'pedidos@lacteoslaesperanza.mx', 'Lista de precios diciembre', 'Le compartimos la lista de precios de leche, yogur y queso para diciembre.', 'Lun 09:12', att=['Precios_dic.pdf']),
    msg(3, 'ofertas@superpromo.xyz', '¡¡GANASTE UN IPHONE!!', 'Haz clic aquí y paga solo el envío para recibir tu premio.', 'Lun 09:40', att=['premio.exe']),
    msg(4, 'luis.ayudante@escuelita.mx', 'Inventario de vasos', 'Ya conté los vasos: quedan 120 grandes y 80 chicos.', 'Lun 10:02', unread=False),
    msg(5, 'pedidos@lacteoslaesperanza.mx', 'Confirmación de pedido 3381', 'Su pedido llegará el miércoles entre 8 y 9 de la mañana.', 'Lun 11:30'),
    msg(6, 'ofertas@superpromo.xyz', 'Última oportunidad: préstamo sin buró', 'Te prestamos 50 mil pesos hoy mismo, solo envía tu INE.', 'Lun 12:15'),
    msg(7, 'orientacion@escuelita.mx', 'Cadena: reenvía a 10 personas', 'Si no reenvías este mensaje a 10 contactos tendrás mala suerte.', 'Lun 12:50'),
    msg(8, 'alumno.martinez@escuelita.mx', 'Pregunta por el menú', '¿Mañana habrá molletes? Gracias.', 'Lun 13:05', unread=False),
]
CONTACTS = [
    {'n': 'Directora Ruiz', 'st': 'Ocupado', 're': 'Gracias, lo reviso en un momento.'},
    {'n': 'Lácteos La Esperanza', 'st': 'Ausente'},
    {'n': 'Luis (ayudante)', 'st': 'Disponible', 're': '¡Va! Yo me encargo 👍'},
    {'n': 'Número desconocido', 'st': 'Disponible', 're': 'Hola, ganaste un premio 🎁 mándame tu nombre completo y tu CURP.'},
]


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.used, a.sent, a.m, a.rules, a.blocked, a.folders, a.contacts, a.chats, a.ct, a.st, a.S)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pNet({j(ic)},{j(t)},{j(inf)},{{mode:"mail",title:"Correo · cafeteria@escuelita.mx",msgs:{j(INBOX)},contacts:{j(CONTACTS)},tasks:{ts},hint:{j(hint)}{extra}}})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('✉️', 'La bandeja de la cafetería', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Ya configuraste la cuenta; ahora toca <b>usarla bien</b>: escribir correos claros, organizar los que llegan, responder con educación y no caer en engaños. También vas a usar la <b>mensajería instantánea</b> (chat) de forma responsable.'),
    ex('Caso: Cafetería La Escuelita', 'La bandeja de <code>cafeteria@escuelita.mx</code> tiene de todo: la directora pide confirmación del horario, el proveedor de lácteos manda precios, llegan promociones sospechosas y hasta una cadena. Tú vas a poner orden.'),
    r3([('✏️', 'A · Enviar y recibir', 'Redactar, adjuntar, filtrar, bloquear y administrar.'), ('🤝', 'B y C · Responsabilidad y orden', 'Responder, reenviar, acuses, imprimir, carpetas y ordenar.'), ('💬', 'D · Mensajería instantánea', 'Estados, contactos, grupos, voz y video.')])),
    'Un correo bien hecho habla bien de ti y de tu negocio.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia (5%)', 'El <b>historial impreso</b> (o en PDF) de <b>envío y recepción de mensajes</b>: correos que enviaste con CC, CCO y adjuntos, respuestas, reenvíos, acuses, tus carpetas y filtros, y una conversación de mensajería.'),
    bk('Cómo se arma', 'Practica en los cuatro simuladores y luego hazlo con tu cuenta real. Para «imprimir», usa <b>Imprimir › Guardar como PDF</b> en cada mensaje y únelos en un solo archivo, o pega capturas en un documento.'),
    warn('Importante', 'Practica con tus compañeros y tu profesor. No envíes correos de prueba a desconocidos ni respondas al spam.')),
    'Cada simulador es una parte de tu historial.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Enviar, recibir y administrar ─────────────────────────
a0 = c.mark()
c.L('✏️', 'Redactar y enviar un correo', 'Bloque A · Las partes del mensaje', body(
    bk('Para', 'Destinatario principal: a quien va dirigido y de quien esperas respuesta.'),
    bk('CC (con copia)', 'Personas que deben <b>enterarse</b>. Todos ven quién está en CC.'),
    bk('CCO (con copia oculta)', 'Nadie ve a quién más le llegó. Úsalo para enviar a muchas personas sin revelar sus correos (por ejemplo, avisos a todos los padres).'),
    bk('Asunto', 'Corto y claro: <code>Pedido de leche para el miércoles</code>, no <code>hola</code>. Un correo sin asunto parece spam.'),
    bk('Cuerpo y formato', 'Saludo, mensaje breve en párrafos, despedida y firma. Usa <b>negritas</b>, <i>cursivas</i> o listas solo para resaltar lo importante. Nada de escribir TODO EN MAYÚSCULAS (equivale a gritar).'),
    bk('Adjuntos 📎', 'Archivos que viajan con el correo. Menciónalos en el texto («te adjunto el menú») y revisa el tamaño (casi todos los servidores aceptan máximo 20-25 MB).'),
    ex('Ejemplo', 'Para: direccion@escuelita.mx · CC: luis.ayudante@escuelita.mx · Asunto: Menú de la semana · «Buen día, directora. Le adjunto el menú de la semana del 14 al 18 de diciembre. Saludos, Encargado de la cafetería.» · 📎 Menu_semana.pdf')),
    'Para = a quién · CC = quién se entera · CCO = oculto · asunto claro · adjunto mencionado.')
c.A('📮', '¿Para, CC o CCO?', 'Elige dónde va cada dirección.', [
    ['La directora, a quien le pides autorizar el menú', 'Para', 'Es la destinataria principal.'],
    ['El ayudante, que solo debe enterarse del pedido', 'CC', 'Debe saberlo, pero no responder.'],
    ['Cuarenta padres de familia a los que mandas un aviso', 'CCO', 'Así nadie ve los correos de los demás.'],
    ['Tu jefe, al que quieres tener informado sin que el proveedor lo sepa', 'CCO', 'La copia oculta no se ve.'],
    ['El proveedor al que le haces el pedido', 'Para', 'Es quien debe responder.'],
], 'Para = actúa · CC = se entera · CCO = se entera sin que lo vean.', ['Para', 'CC', 'CCO'])
c.L('📥', 'Recibir y administrar el correo', 'Bloque A · Filtros, bloqueo y adjuntos', body(
    bk('Filtros (reglas)', 'Instrucciones automáticas: «si el remitente es <code>pedidos@lacteoslaesperanza.mx</code>, mover a la carpeta Proveedores». Se aplican a lo que llega y a lo que ya está.'),
    bk('Bloquear remitente', 'Todo lo que envíe esa dirección irá directo a Spam. Úsalo con promociones insistentes o personas que te molestan.'),
    bk('Marcar como spam', 'Enseña al filtro antispam a reconocer ese tipo de correo.'),
    bk('Adjuntos recibidos', 'Descarga solo los que esperabas y de remitentes conocidos. Nunca abras <code>.exe</code>, <code>.scr</code> o <code>.js</code> que llegan por correo.'),
    bk('Administrar la cuenta', 'Cambiar la contraseña cada cierto tiempo, activar la verificación en dos pasos, revisar el espacio del buzón y vaciar la Papelera y el Spam.')),
    'Filtra lo conocido, bloquea lo molesto y no abras lo sospechoso.')
sim('✏️', 'Redacta y envía', 'Simulador: CC, CCO, asunto, formato, adjuntos y borradores.', {
    'id': 'm1', 'intro': 'Envía a la directora (<code>direccion@escuelita.mx</code>) el menú de la semana, con copia al ayudante (<code>luis.ayudante@escuelita.mx</code>) y copia oculta a la supervisora (<code>supervision@escuelita.mx</code>).'}, [
    ['Envía un correo a <b>direccion@escuelita.mx</b> con <b>CC</b> al ayudante y un asunto claro.', 'a.sent.some(function(m){return /direccion@escuelita\\.mx/i.test(m.to)&&/luis\\.ayudante/i.test(m.cc||"")&&m.subj!="(sin asunto)"})'],
    ['Que el correo lleve <b>CCO</b> a supervision@escuelita.mx.', 'a.sent.some(function(m){return /supervision@escuelita\\.mx/i.test(m.bcc||"")})'],
    ['Adjunta <b>Menu_semana.pdf</b>.', 'a.sent.some(function(m){return (m.att||[]).indexOf("Menu_semana.pdf")>-1})'],
    ['Usa <b>negrita</b>, cursiva o lista en el texto.', 'a.sent.some(function(m){return m.b||m.i||m.l})'],
    ['Abre la respuesta de la directora y <b>descarga</b> su adjunto.', 'a.used("dl_ok")'],
    ['Guarda otro mensaje como <b>borrador</b>.', 'a.m(function(m){return m.box=="draft"}).length>0']],
    'Usa ✏️ Redactar. El adjunto se elige en la lista 📎 del mensaje.')
sim('📥', 'Pon orden en la bandeja', 'Simulador: carpetas, filtros, bloqueo, spam y ordenar.', {
    'id': 'm2', 'intro': 'La bandeja está revuelta. Crea una carpeta para el proveedor, filtra sus correos, deshazte de las promociones y ordena para encontrar rápido lo pendiente.'}, [
    ['Crea la carpeta <b>Proveedores</b>.', 'a.folders.indexOf("Proveedores")>-1'],
    ['Crea un <b>filtro</b> que mueva lo de <b>pedidos@lacteoslaesperanza.mx</b> a Proveedores.', 'a.rules.some(function(r){return /lacteoslaesperanza/i.test(r.from)&&r.act=="move"&&r.to=="Proveedores"})&&a.m(function(m){return m.box=="Proveedores"}).length>=2'],
    ['<b>Bloquea</b> al remitente ofertas@superpromo.xyz.', 'a.blocked.indexOf("ofertas@superpromo.xyz")>-1'],
    ['Marca la cadena como <b>spam</b> o muévela a la Papelera.', 'a.m(function(m){return m.n==7&&(m.box=="spam"||m.box=="trash"||m.box=="gone")}).length>0'],
    ['Ordena la bandeja por <b>remitente</b> y luego por <b>no leídos primero</b>.', 'a.used("sort_from")&&a.used("sort_unread")'],
    ['Ordena por <b>asunto</b> y revisa la carpeta <b>Spam</b>.', 'a.used("sort_subj")&&a.used("box_spam")']],
    'Los filtros y las carpetas están en la columna izquierda.')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Uso responsable ─────────────────────────
b0 = c.mark()
c.L('🤝', 'Responder, reenviar y eliminar', 'Bloque B · Uso responsable del correo', body(
    bk('Responder', 'Contesta solo al remitente. El asunto empieza con <b>RE:</b>.'),
    bk('Responder a todos', 'Contesta al remitente y a todos los que estaban en Para y CC. Úsalo solo si <b>todos</b> necesitan tu respuesta; si no, llenas buzones ajenos.'),
    bk('Reenviar', 'Manda el mensaje (con sus adjuntos) a otra persona. El asunto empieza con <b>RV:</b> o <b>FW:</b>. Antes de reenviar, borra las direcciones de otros y pregúntate si el autor estaría de acuerdo. <b>No reenvíes cadenas</b> ni rumores.'),
    bk('Eliminar', 'Lo eliminado va a la Papelera; ahí se puede recuperar hasta que la vacías.'),
    bk('Imprimir', 'Imprime solo lo necesario (comprobantes, confirmaciones). La impresión incluye De, Para, Fecha y Asunto, por eso sirve como evidencia. Puedes «imprimir» a PDF para ahorrar papel.'),
    warn('Piensa antes de enviar', 'Un correo no se puede «desenviar». Revisa destinatarios, adjuntos y tono. Si estás enojado, guárdalo como borrador y léelo después.')),
    'Responde a quien corresponde, reenvía con permiso y piensa antes de enviar.')
c.L('🧾', 'Firma, aviso legal y acuses', 'Bloque B · Disclaimer, confirmación de entrega y de lectura', body(
    bk('Firma', 'Texto que se agrega solo al final: nombre, puesto, teléfono. Da formalidad.'),
    bk('Disclaimer (aviso de confidencialidad)', 'Párrafo al final de la firma que dice que el mensaje es solo para su destinatario y qué hacer si llegó por error. Lo usan empresas, escuelas y oficinas de gobierno.'),
    bk('Confirmación de entrega', 'El servidor te avisa que el mensaje <b>llegó</b> al buzón del destinatario.'),
    bk('Confirmación de lectura', 'El destinatario decide si te avisa que lo <b>abrió</b>. Pídela solo en mensajes importantes; muchas personas la consideran invasiva.'),
    ex('En la cafetería', 'La directora pidió confirmación de lectura del nuevo horario: al abrirlo, el encargado elige «Enviar» para que ella sepa que lo leyó.')),
    'Firma = quién eres · disclaimer = confidencial · entrega = llegó · lectura = lo abrieron.')
sim('🤝', 'Usa el correo con responsabilidad', 'Simulador: firma, responder, responder a todos, reenviar, acuses e imprimir.', {
    'id': 'm3', 'intro': 'Atiende los pendientes de la bandeja como lo haría un profesional.'}, [
    ['Activa la <b>firma con disclaimer</b> (✍️ Firma) y envía un mensaje que la lleve.', 'a.sent.some(function(m){return /CONFIDENCIALIDAD/.test(m.body)})'],
    ['Abre «Horario de diciembre» y <b>envía la confirmación de lectura</b> que pidió la directora.', 'a.used("rr_1")'],
    ['<b>Responde a todos</b> ese mensaje confirmando el horario.', 'a.sent.some(function(m){return m.kind=="Responder a todos"&&/papeleria/i.test(m.cc||"")})'],
    ['<b>Reenvía</b> la lista de precios del proveedor (con su adjunto) a luis.ayudante@escuelita.mx.', 'a.sent.some(function(m){return m.fwdOf==2&&(m.att||[]).length>0})'],
    ['Envía un correo pidiendo <b>confirmación de entrega y de lectura</b>.', 'a.sent.some(function(m){return m.rcpt&&m.rr})'],
    ['<b>Imprime</b> la confirmación del pedido 3381.', 'a.S.printed.indexOf(5)>-1'],
    ['<b>Elimina</b> la cadena «reenvía a 10 personas» sin reenviarla.', 'a.m(function(m){return m.n==7&&(m.box=="trash"||m.box=="gone")}).length>0&&!a.sent.some(function(m){return m.fwdOf==7})']],
    'Responder a todos, Reenviar e Imprimir aparecen al abrir un mensaje.')
c.A('🤔', '¿Qué es lo responsable?', 'Elige la acción correcta para cada situación.', [
    ['La directora escribió a 30 personas preguntando quién va a la junta; solo ella necesita tu respuesta', 'Responder', 'Responder a todos llenaría 29 buzones sin necesidad.'],
    ['Te llega «reenvía esto a 10 contactos o tendrás mala suerte»', 'Eliminar', 'Las cadenas no se reenvían.'],
    ['El proveedor manda los precios y el ayudante debe tenerlos', 'Reenviar', 'El reenvío incluye el adjunto.'],
    ['Necesitas comprobante en papel de un pedido confirmado', 'Imprimir', 'La impresión lleva fecha y remitente.'],
    ['El supervisor, la directora y tú deben acordar una fecha', 'Responder a todos', 'Los tres necesitan la respuesta.'],
], 'Antes de dar clic, pregúntate quién necesita el mensaje.', ['Responder', 'Responder a todos', 'Reenviar', 'Eliminar', 'Imprimir'])
b_end = c.mark() - 1

# ───────────────────────── Bloque C · Carpetas y ordenamiento ─────────────────────────
c0 = c.mark()
c.L('🗂️', 'Carpetas y ordenamiento', 'Bloque C · Encuentra cualquier correo en segundos', body(
    bk('Carpetas del sistema', '<b>Recibidos</b>, <b>Enviados</b>, <b>Borradores</b>, <b>Spam</b> y <b>Papelera</b>.'),
    bk('Carpetas propias', 'Crea carpetas por tema (Proveedores, Dirección, Alumnos) y mueve los mensajes o deja que un filtro lo haga.'),
    bk('Ordenar por', '<b>No leídos</b> (lo pendiente arriba) · <b>Remitente</b> (todo lo de una persona junto) · <b>Destinatario</b> (útil en Enviados) · <b>Fecha de recepción o de envío</b> (lo más reciente primero) · <b>Asunto</b> (agrupa conversaciones).'),
    ex('Rutina de 5 minutos', 'Al abrir el correo: ordena por no leídos, atiende lo urgente, mueve lo demás a su carpeta, borra el spam. Bandeja limpia = nada se te olvida.')),
    'Carpetas para guardar, filtros para automatizar, orden para encontrar.')
c.A('🔃', '¿Cómo lo ordenas?', 'Elige el orden que te ayuda en cada caso.', [
    ['Quieres ver primero lo que todavía no has abierto', 'No leídos', 'Lo pendiente queda arriba.'],
    ['Buscas todos los correos del proveedor', 'Remitente', 'Agrupa por quién los envió.'],
    ['En Enviados buscas lo que le mandaste a la directora', 'Destinatario', 'Agrupa por a quién se envió.'],
    ['Quieres juntar todos los mensajes «Pedido 3381»', 'Asunto', 'Agrupa por asunto.'],
    ['Necesitas el correo más reciente', 'Fecha', 'Lo último queda arriba.'],
], 'El orden depende de lo que buscas.', ['No leídos', 'Remitente', 'Destinatario', 'Asunto', 'Fecha'])
c_end = c.mark() - 1

# ───────────────────────── Bloque D · Mensajería instantánea ─────────────────────────
d0 = c.mark()
c.L('💬', 'Mensajería instantánea', 'Bloque D · Chat, estados, contactos, grupos, voz y video', body(
    sp('En palabras sencillas', 'La <b>mensajería instantánea</b> (WhatsApp, Telegram, Teams, Messenger) entrega los mensajes al momento, a diferencia del correo.'),
    bk('Ventana de inicio de sesión', 'Entras con tu número o correo y un código o contraseña. En una computadora compartida, <b>cierra sesión</b> al terminar.'),
    bk('Estados', '<b>Disponible</b> 🟢, <b>Ocupado</b> 🔴 (no molestar), <b>Ausente</b> 🟡 (no estás en la computadora) e <b>Invisible</b> ⚪ (te conectas sin que te vean).'),
    bk('Contactos', '<b>Agregar</b> a quien conoces · <b>eliminar</b> a quien ya no necesitas · <b>bloquear</b> a desconocidos o a quien te molesta (ya no puede escribirte ni llamarte).'),
    bk('Grupos', 'Conversación con varias personas (por ejemplo, «Equipo cafetería»). Mantén el tema del grupo y no lo llenes de cadenas o stickers.'),
    bk('Voz y video', 'Llamadas por internet. Pide permiso antes de una videollamada y cuida lo que se ve detrás de ti.'),
    warn('Uso responsable', 'No compartas tu ubicación, tu CURP, fotos privadas ni códigos de verificación. Si un número desconocido te ofrece premios, <b>bloquéalo</b>. Respeta los horarios: no escribas al proveedor a las 11 de la noche.')),
    'Estado adecuado, contactos conocidos, grupos con tema y nada de datos personales.')
sim('💬', 'Usa la mensajería con responsabilidad', 'Simulador: estado, contactos, grupo, mensajes, voz, video y bloqueo.', {
    'id': 'm4', 'view': 'chat', 'intro': 'Organiza al equipo de la cafetería por mensajería y protege tu cuenta de desconocidos.'}, [
    ['Cambia tu <b>estado</b> a Ocupado o Ausente.', 'a.st!="Disponible"'],
    ['<b>Agrega</b> un contacto nuevo (por ejemplo, «Proveedor de pan»).', 'a.contacts.some(function(c){return !c.g&&["Directora Ruiz","Lácteos La Esperanza","Luis (ayudante)","Número desconocido"].indexOf(c.n)<0})'],
    ['Escríbele a <b>Luis (ayudante)</b> y recibe su respuesta.', '(a.chats["Luis (ayudante)"]||[]).some(function(m){return !m.me})'],
    ['Crea el grupo <b>Equipo cafetería</b> con al menos dos contactos y manda un mensaje.', 'a.contacts.some(function(c){return c.g&&(a.chats[c.n]||[]).some(function(m){return m.me})})'],
    ['Haz una <b>llamada de voz</b> y una <b>videollamada</b>.', '(a.S.calls||[]).some(function(k){return k.k=="v"})&&(a.S.calls||[]).some(function(k){return k.k=="c"})'],
    ['<b>Bloquea</b> al Número desconocido que ofrece premios.', 'a.ct("Número desconocido")&&a.ct("Número desconocido").blk'],
    ['<b>Elimina</b> un contacto que ya no necesitas.', '(a.S.delCt||[]).length>0']],
    'Para el grupo usa 👥 Grupo debajo de los contactos.')
c.W('✍️', 'Tus reglas de comunicación', 'Escribe el reglamento de comunicación de la cafetería.',
    'Escribe cinco reglas para que el equipo de la cafetería use bien el <b>correo</b> y la <b>mensajería</b>. Incluye cuándo usar <b>CC o CCO</b>, cuándo <b>responder a todos</b>, qué hacer con las <b>cadenas o el spam</b> y una regla de <b>seguridad</b> en el chat.',
    [['Tiene al menos 40 palabras', 'palabras:40'],
     ['Menciona CC o CCO', '\\b(cc|cco|copia\\w*)\\b'],
     ['Menciona responder a todos', 'responder a todos|responde a todos'],
     ['Menciona cadenas o spam', '\\b(cadena\\w*|spam)\\b'],
     ['Incluye una regla de seguridad en el chat', '\\b(bloque\\w*|desconocid\\w*|datos|contraseñ\\w*|codigo\\w*|código\\w*)\\b']],
    'Una regla por línea, empezando con un verbo.', 'Ejemplo: 1. Usa CCO cuando…')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('CC', 'Con copia: personas que se enteran y todos las ven.'),
    bk('CCO', 'Con copia oculta: nadie ve a quién más le llegó.'),
    bk('Adjunto', 'Archivo que viaja con el correo.'),
    bk('Filtro (regla)', 'Acción automática sobre los correos que cumplen una condición.'),
    bk('Spam', 'Correo masivo no deseado.'),
    bk('Reenviar', 'Enviar a otra persona un correo recibido, con sus adjuntos.'),
    bk('Disclaimer', 'Aviso de confidencialidad al final del correo.'),
    bk('Confirmación de entrega', 'Aviso de que el correo llegó al buzón.'),
    bk('Confirmación de lectura', 'Aviso de que el destinatario abrió el correo.'),
    bk('Mensajería instantánea', 'Mensajes, llamadas y videollamadas al momento por internet.'),
    bk('Estado', 'Disponible, Ocupado, Ausente o Invisible.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311. El R.A. 4.3 dura 8 h, vale 5% y la A.E. es el viernes 8-ene. Pide que cada alumno tenga a la mano la cuenta que configuró en el R.A. 4.2.', 'sp'),
    bk('Viernes 18-dic · Bloque A (laboratorio)', 'Después de entregar el 4.2: redactar con CC, CCO y adjuntos (simulador 1) y recibir y administrar (simulador 2). Intercambien correos entre compañeros.'),
    bk('Miércoles 6-ene · Bloque B', 'Responder, reenviar, firma con disclaimer, acuses e imprimir (simulador 3) y <b>Práctica 1</b>.'),
    bk('Viernes 8-ene · Bloques C, D y evaluación (laboratorio)', 'Carpetas y ordenamiento, mensajería instantánea (simulador 4), <b>Práctica 2</b> y entrega del historial impreso.'),
    bk('Sin computadora', 'Gmail y Outlook en el celular permiten CC, CCO, adjuntos, etiquetas o carpetas e imprimir a PDF. WhatsApp o Telegram sirven para la parte de mensajería.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '✉️', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '✏️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🤝', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🗂️', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '💬', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"✉️",t:"Empieza aquí",d:"Qué vas a hacer con el correo y la mensajería, y qué vas a entregar.",time:"10 min",obj:["Reconocer el uso profesional del correo","Conocer la evidencia del R.A."],sum:["Correo claro y ordenado.","Mensajería responsable.","Evidencia: historial impreso de envío y recepción (5%)."],q:"¿Qué es lo más molesto que te ha llegado por correo o chat?"},
a:{k:"Bloque A",l:"A",ic:"✏️",t:"Enviar, recibir y administrar",d:"Formato, destinatarios, CC, CCO, adjuntos y asunto; filtros, bloqueo y adjuntos recibidos; administración de la cuenta.",time:"3 h",obj:["Redactar un correo con CC, CCO, asunto y adjunto","Crear filtros y bloquear remitentes","Descargar adjuntos con seguridad"],sum:["Para actúa, CC se entera, CCO oculto.","Asunto claro y adjunto mencionado.","Filtros automatizan; bloquear manda a Spam.","No abras ejecutables recibidos."],q:"¿Cuándo usarías CCO en tu vida diaria?"},
b:{k:"Bloque B",l:"B",ic:"🤝",t:"Uso responsable",d:"Reenvío, disclaimer, respuesta, eliminación, impresión y confirmaciones de entrega y lectura.",time:"2 h",obj:["Elegir entre responder y responder a todos","Reenviar con responsabilidad","Usar firma, disclaimer y acuses","Imprimir y eliminar mensajes"],sum:["RE: responde · RV: reenvía.","Responder a todos solo si todos lo necesitan.","Disclaimer = aviso de confidencialidad.","Entrega = llegó · lectura = lo abrieron."],q:"¿Te ha pasado que alguien respondió a todos sin necesidad?",rev:[["CCO sirve para…",["Ocultar a los demás destinatarios","Pedir confirmación","Adjuntar archivos"],0,"Nadie ve a quién más le llegó."],["Un filtro puede…",["Mover correos a una carpeta","Cifrar la cuenta","Cambiar el servidor"],0,"Actúa solo sobre los mensajes que cumplen la condición."]]},
c:{k:"Bloque C",l:"C",ic:"🗂️",t:"Carpetas y ordenamiento",d:"Manejo de carpetas y ordenamiento por no leídos, remitente, destinatario, fechas y asunto.",time:"1 h",obj:["Crear y usar carpetas","Ordenar la bandeja según lo que buscas"],sum:["Carpetas del sistema y propias.","No leídos, remitente, destinatario, fecha y asunto."],q:"¿Qué carpetas crearías para tu correo escolar?",rev:[["Para que el destinatario te avise que abrió el correo pides…",["Confirmación de lectura","Confirmación de entrega","CCO"],0,"Es la de lectura."],["Las cadenas de «reenvía a 10» se…",["Eliminan","Reenvían","Imprimen"],0,"No se reenvían."]]},
d:{k:"Bloque D",l:"D",ic:"💬",t:"Mensajería instantánea",d:"Inicio de sesión, estados, contactos (agregar, eliminar, bloquear), mensajes, grupos, voz, video y uso responsable.",time:"2 h",obj:["Usar estados y administrar contactos","Crear grupos y hacer llamadas","Protegerte de desconocidos"],sum:["Disponible, Ocupado, Ausente, Invisible.","Agregar, eliminar y bloquear contactos.","Grupos con tema; voz y video con permiso.","Nunca compartas códigos ni datos personales."],q:"¿Qué regla pondrías en el grupo de tu salón?",rev:[["Para ver primero lo pendiente ordenas por…",["No leídos","Asunto","Destinatario"],0,"Lo no leído queda arriba."],["Para guardar los correos de un proveedor creas…",["Una carpeta","Una firma","Un acuse"],0,"Y un filtro que los mueva."]]}
'''

ILL = r'''
ILL["Redactar y enviar un correo"]=function(){return SV(340,140,R_(10,6,320,128,"w",8)+T_(20,26,"Para: direccion@escuelita.mx","t","start")+T_(20,46,"CC: luis.ayudante@escuelita.mx","t","start")+T_(20,66,"CCO: supervision@escuelita.mx","t","start")+T_(20,86,"Asunto: Menú de la semana","t","start")+T_(20,112,"📎 Menu_semana.pdf","tm","start"),"Partes de un correo")};
ILL["Recibir y administrar el correo"]=function(){return flow([["📨","Llega"],["⚙️","Filtro"],["🗂️","Carpeta"],["⛔","Bloqueados|a Spam"]],"Cómo se acomoda lo que llega")};
ILL["Firma, aviso legal y acuses"]=function(){return grid3([["✍️","Firma"],["⚖️","Disclaimer"],["📬","Acuse de|entrega"],["👁️","Acuse de|lectura"]],"Lo que acompaña a un correo formal")};
ILL["Mensajería instantánea"]=function(){return grid3([["🟢","Disponible"],["🔴","Ocupado"],["🟡","Ausente"],["⚪","Invisible"],["👥","Grupos"],["⛔","Bloquear"]],"Estados y herramientas del chat")};
'''

EXH = r'''
EXH.redactar=function(){return exw(mw('Mensaje nuevo','<div class="mm"><span>Para · CC · CCO '+mk(1)+'</span><span>Asunto: Menú de la semana</span><span>📎 Adjuntar archivo '+mk(2)+'</span></div>'),['Escribe los destinatarios en su campo.','El clip agrega el archivo.'])};
EXH.regla=function(){return exw(mw('Reglas › Nueva regla','<div class="mfld">Si el remitente es pedidos@lacteoslaesperanza.mx '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Mover a la carpeta Proveedores '+mk(2)+'</div>'),['Condición.','Acción.'])};
EXH.acuses=function(){return exw(mw('Opciones › Seguimiento','<div class="mm"><span>☑ Solicitar confirmación de entrega '+mk(1)+'</span><span>☑ Solicitar confirmación de lectura '+mk(2)+'</span></div>'),['Avisa que llegó.','Avisa que lo abrieron.'])};
EXH.imprimir=function(){return exw(mw('Imprimir','<div class="mfld">Destino: Guardar como PDF '+mk(1)+'</div>'),['Ahorra papel y sirve como evidencia.'])};
EXH.cel_chat=function(){return exw(mp('WhatsApp o Telegram','<div class="mbox">Nuevo grupo › elige contactos › nombre '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Contacto › Bloquear '+mk(2)+'</div>'),['Crea el grupo del equipo.','Bloquea a desconocidos.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Intercambio de correos con tu equipo',
     'prog': 'Bloques A, B y C · Enviar, responder y organizar',
     'min': 60, 'lug': 'Viernes 18-dic y miércoles 6-ene, en laboratorio o en casa',
     'modes': {
         'pc': {'mat': ['Tu cuenta de correo en la computadora', 'Dos compañeros y tu profesor como destinatarios'],
                'steps': [
                    'Antes de empezar, termina los simuladores 1, 2 y 3.',
                    ['Envía a un compañero un correo con CC a otro y CCO a tu profesor, asunto claro, formato y un adjunto.', 'redactar'],
                    'Pide confirmación de entrega y de lectura en ese correo.',
                    'Responde a un correo de tu compañero, responde a todos en otro y reenvía uno con adjunto.',
                    'Activa una firma con tu nombre, grupo y un disclaimer.',
                    ['Crea una carpeta «EDOA» y un filtro que mueva ahí los correos de tus compañeros.', 'regla'],
                    ['Imprime a PDF cada mensaje enviado y recibido.', 'imprimir']]},
         'cel': {'mat': ['Gmail u Outlook en el celular', 'Dos compañeros y tu profesor como destinatarios'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 1, 2 y 3.',
                     'Envía un correo con Para, CC y CCO, asunto claro y un adjunto (toca la flecha junto a «Para» para ver CC y CCO).',
                     'Responde, responde a todos y reenvía mensajes de tus compañeros.',
                     'Crea una etiqueta o carpeta «EDOA» y mueve ahí sus correos.',
                     'En cada mensaje usa ⋮ › Imprimir › Guardar como PDF.']}},
     'entrega': ['Correos enviados y recibidos impresos a PDF.'],
     'rub': [['Correo con CC, CCO, asunto, formato y adjunto', 30], ['Responder, responder a todos y reenviar', 25], ['Firma, disclaimer y acuses', 20], ['Carpeta y filtro', 15], ['Impresiones', 10]]},
    {'id': 'pr2', 'n': 2, 't': 'Historial de envío y recepción',
     'prog': 'Bloques C y D · Orden, mensajería y evidencia',
     'min': 50, 'lug': 'Viernes 8-ene en laboratorio',
     'modes': {
         'pc': {'mat': ['Tus PDF de la práctica 1', 'Una app de mensajería (WhatsApp Web, Telegram o Teams)'],
                'steps': [
                    'Antes de empezar, termina el simulador 4.',
                    'Ordena tu bandeja por remitente, por asunto y por no leídos; toma captura de cada orden.',
                    ['En la mensajería crea un grupo con tu equipo, cambia tu estado, manda un mensaje y haz una llamada de prueba.', 'cel_chat'],
                    'Toma captura de la conversación del grupo (sin datos personales).',
                    'Une en un solo PDF: tus correos impresos, las capturas de ordenamiento y de mensajería.',
                    'Agrega una portada y una hoja final con tus cinco reglas de comunicación.']},
         'cel': {'mat': ['Tu celular con correo y WhatsApp o Telegram'],
                 'steps': [
                     'Antes de empezar, termina el simulador 4.',
                     'Toma capturas de tu bandeja, tu carpeta EDOA y tus correos enviados.',
                     'Crea un grupo con tu equipo, cambia tu estado y manda un mensaje; toma captura.',
                     'Pega todo en Documentos de Google o Word móvil con portada y tus cinco reglas, y descárgalo como PDF.']}},
     'entrega': ['Historial (PDF) de envío y recepción de mensajes con portada y reglas de comunicación.'],
     'rub': [['Correos enviados y recibidos', 35], ['Carpetas y ordenamiento', 20], ['Mensajería instantánea', 25], ['Reglas de comunicación y presentación', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 4',
    'ra': 'R.A. 4.3', 'title': 'Historial de envío y recepción de mensajes',
    'data': [
        ('Resultado de aprendizaje', 'Utiliza el correo electrónico y la mensajería instantánea de manera responsable, enviando, recibiendo y organizando mensajes.'),
        ('Actividad de evaluación', '4.3.1 Envía y recibe mensajes de correo electrónico y de mensajería instantánea, aplicando las opciones de formato, destinatarios, adjuntos, organización y uso responsable.'),
        ('Evidencia', 'Historial impreso de envío y recepción de mensajes'),
        ('Ponderación', '5% (según el programa)'),
        ('Entrega', 'Viernes 8 de enero: PDF en la plataforma'),
    ],
    'situation': 'El equipo de la Cafetería La Escuelita se comunica por correo y por chat. Demuestra que sabes hacerlo como profesional con el historial de tus mensajes.',
    'hint': 'Imprime a PDF cada mensaje en cuanto lo envíes o lo recibas; al final solo tendrás que unirlos.',
    'steps': [
        ('Enviar y recibir (A)', [
            'Un correo con Para, CC, CCO, asunto claro, formato y adjunto, con acuses de entrega y lectura.',
            'Correos recibidos de tus compañeros y un adjunto descargado.']),
        ('Uso responsable y orden (B y C)', [
            'Una respuesta, una respuesta a todos y un reenvío, con tu firma y disclaimer.',
            'Captura de tu carpeta con filtro y de la bandeja ordenada por remitente, asunto y no leídos.']),
        ('Mensajería instantánea (D)', [
            'Capturas de un grupo con tu equipo, tu estado y una llamada, sin datos personales.',
            'Cinco reglas de comunicación responsable.']),
    ],
    'rubric': [
        ('Correo con destinatarios, formato y adjunto', 20), ('Responder, responder a todos y reenviar', 20), ('Firma, disclaimer y acuses', 15),
        ('Carpetas, filtros y ordenamiento', 15), ('Mensajería instantánea', 15), ('Reglas y presentación del historial', 15),
    ],
    'deliver': ['Un solo archivo PDF (o Word) con el historial.', 'Nombre del archivo: Apellido_Nombre_EDOA43.', 'Súbelo en la actividad R.A. 4.3 de la plataforma.'],
}
