"""EDOA-20 · R.A. 4.1 · Navegar y buscar información en internet de forma segura.

Abre la Unidad 4 con el caso de la Cafetería La Escuelita: el encargado necesita investigar becas,
proveedores y trámites en internet sin caer en fraudes. Incluye cuatro simuladores de navegador
(net_sim.js, que usa los estilos de xl3_sim.js).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-4.1'
CODE_PREFIX = 'EDOA41'
FILE = 'edoa-ra41-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 4.1 · Internet seguro'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 4.1 · Navegar y buscar seguro'
HERO_KICK = 'EDOA-20 · R.A. 4.1'
HERO_TITLE = 'Internet sin sustos'
HERO_TEXT = 'Entiende cómo funciona internet, configura tu navegador, descarga sin virus, detecta el phishing y encuentra información confiable en segundos.'
EV_SHORT = 'entrega tu trabajo documental de búsqueda de información.'
EV_CARD = 'Trabajo documental R.A. 4.1'
RA = 'R.A. 4.1'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores de navegador'], 'c': ['Construye', 'Prácticas en tu navegador']}

_DIR = Path(__file__).parent
EXTRA_JS = (_DIR / 'xl3_sim.js').read_text(encoding='utf8') + '\n' + (_DIR / 'net_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".netsim"))nInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".netsim"))return nCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.used, a.visited, a.tabs, a.favs, a.priv, a.dl, a.q, a.forms)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pNet({j(ic)},{j(t)},{j(inf)},{{mode:"web",title:"Navegador",tasks:{ts},hint:{j(hint)}{extra}}})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🌐', 'El encargado investiga en internet', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Internet es una red enorme de computadoras conectadas. El <b>navegador</b> es el programa con el que entras a sus páginas, y el <b>buscador</b> te ayuda a encontrarlas. Navegar <b>seguro</b> es hacerlo sin entregar tus datos ni llenarte de virus.'),
    ex('Caso: Cafetería La Escuelita', 'El encargado debe buscar la convocatoria de becas para los alumnos que ayudan en la cafetería, bajar un programa para comprimir archivos y revisar el banco. En el camino le llegan enlaces de «concursos», descargas «FULL» y un correo que dice que su cuenta será bloqueada. Tú le vas a enseñar a distinguir lo confiable de lo peligroso.'),
    r3([('🛡️', 'A · Seguridad', 'Antispyware, antispam, firewall y anti-phishing.'), ('🌐', 'B y C · Internet y navegador', 'IP, dominios, protocolos y partes del navegador.'), ('🔎', 'D, E y F · Navegar, buscar y cuidarte', 'Descargas, buscadores, fraudes y ética.')])),
    'Primero entiende cómo funciona; luego navega, busca y protégete.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia (5%)', 'Un <b>trabajo documental</b> (Word o PDF) con los <b>resultados de una búsqueda de información</b>: qué buscaste, con qué operadores, qué fuentes elegiste y por qué son confiables, más las medidas de seguridad que aplicaste en tu navegador.'),
    bk('Cómo se arma', 'Practica en los cuatro simuladores y luego haz lo mismo en tu navegador real (Chrome, Edge, Firefox o el de tu celular). Toma capturas de pantalla para tu documento.'),
    warn('Importante', 'En las prácticas <b>nunca</b> escribas contraseñas reales ni datos de tarjetas en sitios desconocidos. Los sitios falsos de este material solo existen dentro del simulador.')),
    'Cada simulador es una sección de tu trabajo documental.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Herramientas de seguridad ─────────────────────────
a0 = c.mark()
c.L('🛡️', 'Las herramientas que te cuidan', 'Bloque A · Antispyware, antispam, firewall y anti-phishing', body(
    sp('En palabras sencillas', 'Cada amenaza tiene su guardia. Ninguna herramienta hace todo: se combinan.'),
    bk('Antispyware', 'Detecta y elimina <b>spyware</b>: programas que espían lo que haces (páginas, teclas, contraseñas) y lo mandan a otra persona. Hoy viene dentro del antivirus (por ejemplo, Seguridad de Windows).'),
    bk('Antispam', 'Filtra el <b>correo basura</b> (spam): publicidad masiva, cadenas y correos fraudulentos. Los manda a la carpeta Spam antes de que los abras.'),
    bk('Firewall (cortafuegos)', 'Vigila la <b>puerta de red</b> de tu equipo: deja pasar las conexiones permitidas y bloquea las que no autorizaste. Protege contra <b>intrusos</b> que intentan entrar desde internet.'),
    bk('Anti-phishing', 'Avisa cuando un sitio <b>se hace pasar por otro</b> (tu banco, tu escuela) para robar tus datos. En el navegador se llama <b>Navegación segura</b> y muestra una pantalla roja.'),
    ana('Piensa en la cafetería', 'Firewall = la puerta con guardia. Antispyware = revisar que nadie haya escondido una cámara. Antispam = el filtro del buzón. Anti-phishing = el guardia que reconoce a los impostores.')),
    'Espías → antispyware · Basura → antispam · Intrusos → firewall · Impostores → anti-phishing.')
c.A('🛡️', '¿Qué herramienta lo detiene?', 'Elige la herramienta que protege en cada situación.', [
    ['Un programa gratis anota todo lo que escribes y lo manda a un desconocido', 'Antispyware', 'Eso es spyware: un programa espía.'],
    ['Te llegan 40 correos al día de «gana dinero desde casa»', 'Antispam', 'Es correo masivo no deseado.'],
    ['Alguien en internet intenta conectarse a tu computadora sin permiso', 'Firewall', 'El firewall bloquea conexiones no autorizadas.'],
    ['Abres un enlace que imita la página de tu banco', 'Anti-phishing', 'La navegación segura avisa de sitios engañosos.'],
    ['Un programa desconocido quiere recibir conexiones de la red', 'Firewall', 'El firewall pregunta si permites esa conexión.'],
], 'Pregúntate: ¿espía, basura, intruso o impostor?', ['Antispyware', 'Antispam', 'Firewall', 'Anti-phishing'])
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Internet ─────────────────────────
b0 = c.mark()
c.L('🌍', '¿Cómo funciona internet?', 'Bloque B · Red, dirección IP y dominio', body(
    sp('En palabras sencillas', '<b>Internet</b> es la red mundial que une millones de redes. Cada equipo conectado tiene una <b>dirección IP</b>, como un número de teléfono (por ejemplo <code>201.175.40.10</code>).'),
    bk('Dominio', 'Como nadie recuerda números, usamos <b>nombres de dominio</b>: <code>conalep.edu.mx</code>. Se lee de derecha a izquierda: <b>.mx</b> = México, <b>.edu</b> = educación, <b>conalep</b> = la institución. Otros: <code>.gob.mx</code> (gobierno), <code>.com</code> (comercial), <code>.org</code> (organizaciones).'),
    bk('DNS', 'El <b>DNS</b> es la agenda de internet: traduce el dominio a su dirección IP. Si escribes mal el dominio, el DNS no lo encuentra y el navegador dice «No se puede acceder a este sitio».'),
    bk('WWW', 'La <b>World Wide Web</b> es el conjunto de páginas enlazadas que ves con el navegador. Internet es la carretera; la Web es uno de los servicios que viajan por ella (el correo y la mensajería son otros).'),
    ex('Ejemplo', 'Escribes <code>www.conalep.edu.mx</code> → el DNS responde <code>201.175.40.10</code> → tu navegador se conecta a esa IP → el servidor le manda la página.')),
    'Dominio para las personas, IP para las máquinas, DNS para traducir.')
c.L('🔐', 'Protocolos: las reglas para hablar', 'Bloque B · HTTP, HTTPS, FTP y DNS', body(
    sp('En palabras sencillas', 'Un <b>protocolo</b> es un conjunto de reglas para que dos equipos se entiendan. La primera parte de la dirección dice qué protocolo se usa.'),
    bk('HTTP', 'Protocolo de la Web. Manda las páginas <b>sin cifrar</b>: quien esté en tu misma red wifi podría leer lo que escribes. El navegador lo marca como <b>«No seguro»</b>.'),
    bk('HTTPS', 'HTTP + cifrado (TLS). Muestra el <b>candado 🔒</b>. Es obligatorio para escribir contraseñas, datos personales o de pago.'),
    bk('FTP', 'Protocolo para <b>transferir archivos</b> entre tu equipo y un servidor. Se usa con programas como FileZilla. Su versión segura es SFTP.'),
    bk('DNS', 'Protocolo que traduce nombres de dominio a direcciones IP.'),
    warn('Ojo', 'El candado solo dice que la conexión está cifrada, <b>no</b> que el sitio sea honesto. Un sitio falso también puede tener candado: revisa siempre el <b>dominio</b>.')),
    'HTTP = postal abierta · HTTPS = sobre cerrado · FTP = mudanza de archivos · DNS = agenda.')
c.T('🔗', 'Desarma la dirección', 'Observa la dirección <code>https://www.conalep.edu.mx/becas</code> y escribe la respuesta.', [
    ['¿Qué protocolo usa?', ['HTTPS'], 'La dirección empieza con https://.', 'Lo que va antes de ://'],
    ['¿Cuál es el dominio de país?', ['.mx', 'mx'], '.mx indica México.', 'La última parte del dominio.'],
    ['¿Qué tipo de institución indica .edu?', ['Educativa', 'Educación', 'Escuela', 'Educativo'], '.edu es para instituciones educativas.', 'edu viene de…'],
    ['¿Cómo se llama la página o carpeta dentro del sitio?', ['becas', '/becas'], 'Lo que va después de la primera diagonal es la ruta.', 'Lo que va después del dominio.'],
    ['¿Qué servicio traduce www.conalep.edu.mx a 201.175.40.10?', ['DNS'], 'El DNS traduce nombres a IP.', 'La agenda de internet.'],
], 'Protocolo :// dominio / ruta.', 'u')
c.O('🔢', '¿Qué pasa al escribir una dirección?', 'Ordena lo que ocurre desde que escribes la dirección hasta que ves la página.', [
    ['Escribes www.conalep.edu.mx en la barra de direcciones', 'Todo empieza con tu dirección.'],
    ['El DNS busca el dominio y responde con su dirección IP', 'Sin la IP el navegador no sabe a dónde ir.'],
    ['Tu navegador se conecta al servidor de esa IP por HTTPS', 'Ahora sí hay conexión cifrada con el servidor.'],
    ['El servidor envía la página', 'El servidor contesta con el contenido.'],
    ['El navegador la muestra con el candado 🔒', 'Al final ves la página.'],
], 'Nombre → IP → conexión → respuesta → pantalla.')
sim('🌍', 'Recorre el internet simulado', 'Simulador: dominios, IP, DNS y protocolos.', {
    'id': 'w1', 'intro': 'Este navegador está conectado a un internet de práctica. Escribe las direcciones en la barra de arriba y observa lo que pasa.'}, [
    ['Entra a <b>www.sat.gob.mx</b> escribiéndolo en la barra de direcciones.', 'a.visited("www.sat.gob.mx")'],
    ['Toca el <b>candado</b> 🔒 de la barra para ver la IP y el protocolo del sitio.', 'a.used("info")'],
    ['Entra al banco escribiendo directamente su IP: <b>200.33.1.20</b>.', 'a.used("byip")'],
    ['Abre <b>neverssl.com</b> y observa el aviso «No seguro» (HTTP).', 'a.visited("neverssl.com")'],
    ['Intenta abrir <b>ftp://ftp.escuelita.mx</b> y lee por qué el navegador no lo abre.', 'a.used("ftp")'],
    ['Escribe un dominio mal escrito (por ejemplo <b>www.conalep.edu.xm</b>) y lee el error del DNS.', 'a.used("notfound")']],
    'Después de escribir la dirección presiona Enter.')
b_end = c.mark() - 1

# ───────────────────────── Bloque C · El navegador ─────────────────────────
cc0 = c.mark()
c.L('🧭', 'Las partes del navegador', 'Bloque C · Navegadores y sus elementos', body(
    sp('En palabras sencillas', 'Un <b>navegador</b> es el programa para ver páginas web: Chrome, Edge, Firefox, Safari, Opera o el navegador de tu celular. Todos tienen las mismas partes.'),
    bk('Barra de direcciones', 'Donde escribes la dirección (URL) o una búsqueda. A la izquierda está el <b>candado</b> o el aviso «No seguro».'),
    bk('Pestañas', 'Varias páginas abiertas en la misma ventana. ＋ abre una nueva; ✕ la cierra.'),
    bk('Botones de navegación', '← Atrás, → Adelante y ⟳ Recargar.'),
    bk('Favoritos (marcadores)', 'La ☆ guarda la página para volver con un clic.'),
    bk('Historial y descargas', 'En el menú ⋮: el historial guarda las páginas que visitaste; Descargas muestra los archivos que bajaste.'),
    bk('Configuración de privacidad', 'Navegación segura, usar siempre HTTPS, bloquear cookies de terceros y «No rastrear».'),
    bk('Ventana de incógnito', 'No guarda historial ni cookies al cerrarla, pero <b>no te hace invisible</b>: la escuela, tu proveedor de internet y los sitios sí ven lo que haces.')),
    'Barra · pestañas · favoritos · historial · descargas · privacidad.')
c.A('🧭', '¿Qué parte del navegador usas?', 'Elige la parte del navegador para cada necesidad.', [
    ['Volver a la página de becas que viste ayer', 'Historial', 'El historial guarda lo visitado.'],
    ['Tener a la mano el portal del CONALEP todos los días', 'Favoritos', 'Un favorito te lleva con un clic.'],
    ['Comparar dos proveedores al mismo tiempo', 'Pestañas', 'Cada proveedor en su pestaña.'],
    ['Saber si la conexión está cifrada', 'Candado', 'El candado indica HTTPS.'],
    ['Usar la computadora de la biblioteca sin dejar historial', 'Incógnito', 'Al cerrar no queda historial ni cookies.'],
], 'Cada parte resuelve una necesidad distinta.', ['Historial', 'Favoritos', 'Pestañas', 'Candado', 'Incógnito'])
sim('🧭', 'Configura tu navegador', 'Simulador: pestañas, favoritos, historial y privacidad.', {
    'id': 'w2', 'intro': 'Deja el navegador listo para el encargado: con sus páginas a la mano y bien protegido.'}, [
    ['Ten al menos <b>3 pestañas</b> abiertas (usa ＋).', 'a.tabs.length>=3'],
    ['Entra a <b>www.conalep.edu.mx/becas</b> y guárdala en <b>favoritos</b> (☆).', 'a.favs.some(function(f){return f.u=="www.conalep.edu.mx/becas"})'],
    ['Abre el <b>historial</b> desde el menú ⋮.', 'a.used("panel_hist")'],
    ['<b>Borra los datos de navegación</b> desde el historial.', 'a.used("cleared")'],
    ['En <b>Privacidad y seguridad</b> activa navegación segura, HTTPS siempre y bloqueo de cookies de terceros.', 'a.priv.safe&&a.priv.https&&a.priv.cookies'],
    ['Abre una <b>ventana de incógnito</b> y lee qué protege y qué no.', 'a.used("incog")']],
    'El menú ⋮ está a la derecha de la barra de direcciones.')
cc_end = c.mark() - 1

# ───────────────────────── Bloque D · Navegar y descargar ─────────────────────────
d0 = c.mark()
c.L('⬇️', 'Navegar, enviar datos y descargar con seguridad', 'Bloque D · Navegación, envío de información y descargas', body(
    sp('En palabras sencillas', 'Cada vez que llenas un formulario o bajas un archivo, abres una puerta. Revisa antes de abrirla.'),
    px('Antes de enviar información', [
        'Mira el <b>dominio</b> completo en la barra: <code>bancodelahorro.mx</code> ≠ <code>bancodelahorro-verifica.xyz</code>.',
        'Comprueba el <b>candado</b> (HTTPS). En un sitio «No seguro» no escribas contraseñas.',
        'Pregúntate si el sitio <b>necesita</b> ese dato. Ningún banco pide tu NIP por internet.',
        'Escribe la dirección tú mismo en lugar de abrir enlaces de correos o mensajes.']),
    px('Descargas seguras', [
        'Descarga solo del <b>sitio oficial</b> del programa o de la tienda de apps.',
        'Desconfía de «FULL», «crack», «gratis» de programas de paga y de los que piden <b>desactivar el antivirus</b>.',
        'Revisa en <b>Descargas</b> que el archivo se analizó y no tenga extensiones raras (.exe que dice ser PDF).',
        'Si el navegador lo marca como peligroso, <b>elimínalo</b>.']),
    ex('En la cafetería', 'El encargado necesita 7-Zip: lo baja de <code>www.7-zip.org</code>. Un anuncio le ofrece «Office FULL crack» en <code>descargas-gratis-full.xyz</code>: la navegación segura lo bloquea.')),
    'Dominio correcto + candado + sitio oficial = navegación segura.')
c.A('🚦', '¿Seguro o peligroso?', 'Decide si cada acción es segura o peligrosa.', [
    ['Bajar 7-Zip desde www.7-zip.org', 'Segura', 'Es el sitio oficial del programa.'],
    ['Escribir tu contraseña en un formulario de un sitio «No seguro» (HTTP)', 'Peligrosa', 'Sin HTTPS la contraseña viaja sin cifrar.'],
    ['Descargar un programa «FULL crack» que pide desactivar el antivirus', 'Peligrosa', 'Es la forma típica de meter malware.'],
    ['Entrar al banco escribiendo tú la dirección www.bancodelahorro.mx', 'Segura', 'Escribir la dirección evita enlaces falsos.'],
    ['Dar tu NIP en bancodelahorro-verifica.xyz porque «tu cuenta será bloqueada»', 'Peligrosa', 'Es phishing: el dominio no es el del banco y ningún banco pide el NIP.'],
], 'Revisa dominio, candado y si de verdad necesitan ese dato.', ['Segura', 'Peligrosa'])
sim('⬇️', 'Navega y descarga sin caer', 'Simulador: navegación segura, descargas y phishing.', {
    'id': 'w3', 'intro': 'Al encargado le llegaron estos enlaces por mensaje: <code>www.7-zip.org</code> · <code>descargas-gratis-full.xyz</code> · <code>bancodelahorro-verifica.xyz</code>. Revísalos con cuidado.'}, [
    ['Primero activa la <b>navegación segura</b> en ⋮ › Privacidad y seguridad.', 'a.priv.safe'],
    ['Descarga <b>7-Zip</b> desde su sitio oficial.', 'a.dl.some(function(d){return d.src=="www.7-zip.org"&&!d.bad})'],
    ['Abre <b>descargas-gratis-full.xyz</b> y observa cómo se bloquea el malware.', 'a.used("warn_mal")'],
    ['Abre <b>bancodelahorro-verifica.xyz</b> y observa el aviso de sitio engañoso.', 'a.used("warn_phish")'],
    ['Envía el formulario de <b>Contacto</b> del CONALEP (sitio con HTTPS).', 'a.forms.some(function(f){return f.s&&!f.bad&&f.u=="www.conalep.edu.mx/contacto"})'],
    ['Revisa el panel de <b>Descargas</b> para ver si tu archivo se analizó.', 'a.used("panel_dl")']],
    'El formulario de contacto está en www.conalep.edu.mx › Contacto.')
d_end = c.mark() - 1

# ───────────────────────── Bloque E · Buscadores ─────────────────────────
e0 = c.mark()
c.L('🔎', 'Motores de búsqueda', 'Bloque E · Buscadores, opciones y tipos de búsqueda', body(
    sp('En palabras sencillas', 'Un <b>motor de búsqueda</b> (Google, Bing, DuckDuckGo) revisa millones de páginas y te muestra las que coinciden con tus palabras. Mientras mejores palabras uses, mejores resultados.'),
    bk('Búsqueda simple', 'Pocas palabras clave, sin artículos: <code>becas conalep requisitos</code>.'),
    bk('Búsqueda avanzada con operadores', '<code>"beca benito juárez"</code> frase exacta · <code>site:gob.mx</code> solo en sitios de gobierno · <code>filetype:pdf</code> solo documentos PDF · <code>-memes</code> quita una palabra · <code>phishing OR pharming</code> una u otra.'),
    bk('Restringir resultados', 'Las pestañas <b>Imágenes, Videos, Noticias</b> y la opción <b>Herramientas › Último año</b> limitan por tipo y fecha. Muchos buscadores tienen una página de <b>Búsqueda avanzada</b> con estos mismos filtros.'),
    bk('¿Es confiable?', 'Prefiere sitios oficiales (<code>.gob.mx</code>, <code>.edu.mx</code>), con autor y fecha recientes. Compara al menos dos fuentes. Desconfía de lo que pide dinero o datos.'),
    ex('Ejemplo', '<code>becas</code> da cientos de resultados. <code>"beca benito juarez" site:gob.mx filetype:pdf</code> da la convocatoria oficial en PDF.')),
    'Palabras clave + operadores + filtros = la fuente correcta.')
c.A('🔎', '¿Qué operador usas?', 'Elige el operador que necesitas para cada búsqueda.', [
    ['Solo quieres resultados de páginas del gobierno', 'site:', 'site:gob.mx limita al dominio.'],
    ['Buscas exactamente la frase «uso responsable de internet»', 'Comillas', 'Las comillas buscan la frase exacta.'],
    ['Quieres solo documentos PDF', 'filetype:', 'filetype:pdf limita el tipo de archivo.'],
    ['Buscas phishing pero aparecen muchos memes', 'Signo menos', '-memes quita esa palabra de los resultados.'],
    ['Te sirve información de phishing o de pharming', 'OR', 'OR acepta cualquiera de las dos palabras.'],
], 'Comillas = exacto · site: = dónde · filetype: = qué tipo · − = sin · OR = o.', ['Comillas', 'site:', 'filetype:', 'Signo menos', 'OR'])
sim('🔎', 'Busca como experto', 'Simulador: búsqueda simple, avanzada y filtros.', {
    'id': 'w4', 'intro': 'Abre <b>www.buscador.mx</b> (o escribe tus palabras directo en la barra) y encuentra información confiable para el trabajo del encargado.'}, [
    ['Haz una búsqueda simple sobre <b>becas</b>.', 'a.q.some(function(q){return /beca/i.test(q.q)&&q.n>0})'],
    ['Busca una <b>frase exacta</b> entre comillas que dé resultados.', 'a.q.some(function(q){return q.ph>0&&q.n>0})'],
    ['Limita una búsqueda a sitios de gobierno con <b>site:gob.mx</b>.', 'a.q.some(function(q){return q.site&&/gob\\.mx/.test(q.site)&&q.n>0})'],
    ['Encuentra un documento con <b>filetype:pdf</b>.', 'a.q.some(function(q){return q.ft=="pdf"&&q.n>0})'],
    ['Quita resultados con el <b>signo menos</b> (por ejemplo <code>phishing -memes</code>).', 'a.q.some(function(q){return q.neg>0&&q.n>0})'],
    ['Usa <b>OR</b> para buscar una palabra u otra.', 'a.q.some(function(q){return q.or&&q.n>0})'],
    ['Filtra los resultados con <b>Videos</b> o <b>Último año</b>.', 'a.used("tool_video")||a.used("tool_year")']],
    'Los operadores se escriben junto con tus palabras, en la misma caja.')
c.Z('🧐', '¿Qué fuente eliges?', 'Buscaste «becas media superior» y obtuviste estos resultados. Completa las conclusiones.',
    '<div class="exw" style="margin-bottom:12px"><p style="margin:4px 0"><b>1.</b> Becas para el Bienestar · <code>www.gob.mx/becasbenitojuarez</code> · 2026</p><p style="margin:4px 0"><b>2.</b> ¡Beca segura en 5 minutos! Deposita 300 pesos · <code>becas-faciles-ya.xyz</code></p><p style="margin:4px 0"><b>3.</b> ¿Cuántos mexicanos usan internet? · <code>www.xataka.com.mx</code> · 2024</p></div>'
    '<p>La fuente más confiable es la número {0}, porque su dominio es {1}.</p>'
    '<p>El resultado 2 es probablemente un {2}: pide {3}.</p>'
    '<p>El resultado 3 {4} sirve para el tema de becas.</p>',
    [['1', ['1', '2', '3']],
     ['de gobierno (.gob.mx)', ['de gobierno (.gob.mx)', '.xyz', 'comercial (.com)']],
     ['fraude', ['fraude', 'sitio oficial', 'periódico']],
     ['dinero', ['dinero', 'nada', 'tu boleta']],
     ['no', ['no', 'sí']]],
    'Fuente oficial, sin pedir dinero, y que hable del tema.')
e_end = c.mark() - 1

# ───────────────────────── Bloque F · Buenas prácticas ─────────────────────────
f0 = c.mark()
c.L('🦠', 'Riesgos en internet', 'Bloque F · Malware, spam, intrusos, piratería y fraudes', body(
    bk('Malware', 'Programa malicioso: <b>virus</b> (se pega a archivos), <b>gusano</b> (se copia solo por la red), <b>troyano</b> (se disfraza de programa útil), <b>ransomware</b> (secuestra tus archivos y pide rescate) y <b>spyware</b> (espía).'),
    bk('Spam', 'Correo masivo no solicitado. Puede traer enlaces de fraude o adjuntos con malware.'),
    bk('Intrusos', 'Personas que intentan entrar a tu equipo o a tus cuentas: adivinan contraseñas o aprovechan equipos sin actualizar.'),
    bk('Piratería', 'Copiar o descargar software, música o películas <b>sin permiso</b> del autor. Es ilegal y es la vía favorita para colar malware («crack», «keygen»).'),
    bk('Phishing', 'Engaño por <b>correo o mensaje</b> que te lleva a un sitio falso para robar tus datos. Variantes: <b>smishing</b> (SMS) y <b>vishing</b> (llamada).'),
    bk('Pharming', 'El atacante cambia la traducción del DNS: escribes bien la dirección, pero llegas a un sitio falso. Por eso revisa el candado y el certificado.'),
    bk('Fraude y robo de información', 'Ventas falsas, premios inexistentes, suplantación de identidad. Con tu nombre, CURP y fotos alguien puede hacerse pasar por ti.')),
    'Si suena demasiado bueno, urgente o pide datos: es sospechoso.')
c.L('✅', 'Buenas prácticas y ética', 'Bloque F · Úsalo bien', body(
    px('Diez hábitos de seguridad', [
        'Contraseñas largas y distintas en cada cuenta, y verificación en dos pasos.',
        'Sistema, navegador y antivirus siempre actualizados.',
        'Navegación segura y firewall activados.',
        'No abrir enlaces ni adjuntos de desconocidos; escribe tú la dirección.',
        'Descargar solo de sitios oficiales; nada de cracks.',
        'Revisar dominio y candado antes de escribir datos.',
        'Cerrar sesión en equipos compartidos o usar incógnito.',
        'No publicar datos personales (dirección, CURP, horarios).',
        'Respaldar tus archivos importantes.',
        'Si caíste: cambia contraseñas, avisa al banco y reporta (Policía Cibernética 088).']),
    bk('Ética en internet', 'Respeta los derechos de autor (cita tus fuentes y usa contenido con licencia libre), no compartas información de otros sin permiso, no difundas noticias falsas y trata a los demás con respeto.'),
    warn('Recuerda', 'Copiar y pegar un texto de internet en tu tarea sin citarlo es <b>plagio</b>. En tu trabajo documental anota siempre la dirección y la fecha de consulta.')),
    'Protégete, respeta a los demás y cita tus fuentes.')
c.A('🕵️', '¿Qué riesgo es?', 'Identifica el riesgo de cada caso.', [
    ['Un SMS dice que ganaste un premio y pide tus datos en un enlace', 'Phishing', 'Te engaña para que entregues tus datos.'],
    ['Tus archivos aparecen cifrados y piden dinero para recuperarlos', 'Malware', 'Es ransomware, un tipo de malware.'],
    ['Escribes bien la dirección de tu banco pero llegas a una copia falsa', 'Pharming', 'Cambiaron la traducción del DNS.'],
    ['Descargas una película de estreno desde una página sin permiso', 'Piratería', 'Copiar sin permiso del autor es piratería.'],
    ['Alguien prueba cientos de contraseñas para entrar a tu correo', 'Intrusos', 'Es un intento de acceso no autorizado.'],
], 'Piensa en qué buscan: datos, dinero o acceso.', ['Phishing', 'Pharming', 'Malware', 'Piratería', 'Intrusos'])
c.W('✍️', 'Tu informe de búsqueda', 'Describe cómo buscaste y por qué confías en tus fuentes.',
    'Elige un tema (becas, uso de internet en México o cómo evitar el phishing). Escribe qué <b>buscaste</b>, qué <b>operadores</b> usaste, qué <b>fuente</b> elegiste y por qué es <b>confiable</b>, y una medida de <b>seguridad</b> que aplicaste.',
    [['Tiene al menos 40 palabras', 'palabras:40'],
     ['Menciona un operador (comillas, site, filetype, OR o menos)', '(site:|filetype:|comillas|\\bOR\\b|operador\\w*|"[^"]+")'],
     ['Menciona una fuente o dominio (.gob.mx, .edu.mx…)', '(\\.gob|\\.edu|\\.org|\\.mx|oficial|fuente)'],
     ['Explica por qué es confiable', '\\b(confiable\\w*|oficial\\w*|autor\\w*|fecha\\w*|reciente\\w*)\\b'],
     ['Menciona una medida de seguridad', '\\b(https|candado|segur\\w*|antivirus|phishing|dominio)\\b']],
    'Tema → búsqueda → fuente → por qué confías → seguridad.', 'Ejemplo: Busqué "beca benito juarez" site:gob.mx…')
f_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Internet', 'Red mundial que une millones de redes.'),
    bk('WWW', 'Conjunto de páginas enlazadas que ves con el navegador.'),
    bk('Dirección IP', 'Número que identifica a un equipo en la red.'),
    bk('Dominio', 'Nombre fácil de recordar de un sitio (conalep.edu.mx).'),
    bk('DNS', 'Servicio que traduce dominios a direcciones IP.'),
    bk('Protocolo', 'Reglas para que dos equipos se comuniquen (HTTP, HTTPS, FTP, DNS).'),
    bk('URL', 'Dirección completa: protocolo, dominio y ruta.'),
    bk('Navegador', 'Programa para ver páginas web.'),
    bk('Motor de búsqueda', 'Sitio que encuentra páginas con tus palabras clave.'),
    bk('Operador de búsqueda', 'Símbolo o palabra que afina la búsqueda ("", site:, filetype:, -, OR).'),
    bk('Malware', 'Programa malicioso (virus, gusano, troyano, ransomware, spyware).'),
    bk('Phishing / pharming', 'Engaños para llevarte a un sitio falso y robar tus datos.'),
    bk('Firewall', 'Filtro que bloquea conexiones de red no autorizadas.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311: martes 17:20-19:50, miércoles 18:10-19:50 y laboratorio el viernes 15:20-18:10. El R.A. 4.1 dura 7 h, vale 5% y la A.E. es el martes 15-dic.', 'sp'),
    bk('Miércoles 9-dic · Bloque A', 'Después de entregar el 3.4: herramientas de seguridad (antispyware, antispam, firewall, anti-phishing). Pide a los alumnos abrir Seguridad de Windows o la de su celular y ubicar cada herramienta.'),
    bk('Viernes 11-dic · Bloques B, C y D (laboratorio)', 'Internet, IP, DNS y protocolos (simulador 1); partes del navegador y privacidad (simulador 2); navegación y descargas seguras (simulador 3) y <b>Práctica 1</b>.'),
    bk('Martes 15-dic · Bloques E, F y evaluación', 'Buscadores y operadores (simulador 4), riesgos, buenas prácticas y ética. <b>Práctica 2</b> y entrega del trabajo documental. El mismo día arranca el R.A. 4.2.'),
    bk('Sin computadora', 'Todo se puede hacer en el navegador del celular: Chrome y Safari tienen favoritos, historial, incógnito y navegación segura, y los operadores de búsqueda funcionan igual.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🌐', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🛡️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🌍', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🧭', 'a': cc0, 'b': cc_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '⬇️', 'a': d0, 'b': d_end},
    {'id': 'e', 't': 'E', 's': '', 'ic': '🔎', 'a': e0, 'b': e_end},
    {'id': 'f', 't': 'F', 's': '', 'ic': '✅', 'a': f0, 'b': f_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd', 'e', 'f']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🌐",t:"Empieza aquí",d:"De qué trata navegar y buscar seguro, y qué vas a entregar.",time:"10 min",obj:["Reconocer para qué sirven el navegador y el buscador","Conocer la evidencia del R.A."],sum:["Navegador = programa para ver páginas.","Buscador = encuentra páginas con tus palabras.","Evidencia: trabajo documental con resultados de búsqueda (5%)."],q:"¿Qué buscaste en internet la última vez y cómo supiste que era confiable?"},
a:{k:"Bloque A",l:"A",ic:"🛡️",t:"Herramientas de seguridad",d:"Antispyware, antispam, firewall y anti-phishing.",time:"1 h",obj:["Explicar qué protege cada herramienta","Elegir la herramienta adecuada para cada amenaza"],sum:["Antispyware contra espías.","Antispam contra correo basura.","Firewall contra intrusos.","Anti-phishing contra sitios impostores."],q:"¿Cuáles de estas herramientas tiene tu celular?"},
b:{k:"Bloque B",l:"B",ic:"🌍",t:"Internet",d:"Dirección IP, dominio, protocolos HTTP, HTTPS, FTP y DNS, y la WWW.",time:"1.5 h",obj:["Explicar qué es una dirección IP y un dominio","Describir cómo el DNS traduce nombres","Distinguir HTTP, HTTPS y FTP"],sum:["IP = número del equipo · dominio = nombre.","DNS traduce dominio → IP.","HTTPS cifra; HTTP no.","FTP transfiere archivos."],q:"¿Por qué crees que todos los bancos usan HTTPS?",rev:[["El firewall protege contra…",["Intrusos de la red","Correos de publicidad","Faltas de ortografía"],0,"Bloquea conexiones no autorizadas."],["La pantalla roja de «sitio engañoso» es del…",["Anti-phishing","Antispam","Firewall"],0,"La navegación segura detecta sitios falsos."]]},
c:{k:"Bloque C",l:"C",ic:"🧭",t:"El navegador",d:"Navegadores y sus elementos: barra, pestañas, favoritos, historial, descargas y privacidad.",time:"1 h",obj:["Identificar las partes del navegador","Configurar la privacidad y seguridad"],sum:["Barra de direcciones con candado.","Pestañas, favoritos, historial y descargas.","Privacidad: navegación segura, HTTPS y cookies.","Incógnito no te hace invisible."],q:"¿Qué guardarías en favoritos para la escuela?",rev:[["El DNS sirve para…",["Traducir dominios a IP","Cifrar contraseñas","Descargar archivos"],0,"Es la agenda de internet."],["El candado 🔒 indica que…",["La conexión está cifrada","El sitio es honesto","No hay virus"],0,"Solo dice que la conexión es HTTPS."]]},
d:{k:"Bloque D",l:"D",ic:"⬇️",t:"Navegar y descargar",d:"Navegación, envío de información y descarga segura de archivos.",time:"1 h",obj:["Revisar dominio y candado antes de enviar datos","Descargar solo de sitios oficiales"],sum:["Escribe tú la dirección.","Sin HTTPS no escribas contraseñas.","Nada de cracks ni «FULL».","Revisa el panel de Descargas."],q:"¿Qué harías si un sitio te pide desactivar tu antivirus?",rev:[["El historial sirve para…",["Volver a páginas visitadas","Cifrar la conexión","Bloquear virus"],0,"Guarda lo que visitaste."],["La ventana de incógnito…",["No guarda historial al cerrar","Te hace invisible","Bloquea todos los virus"],0,"Los sitios y tu red siguen viéndote."]]},
e:{k:"Bloque E",l:"E",ic:"🔎",t:"Buscadores",d:"Motores de búsqueda, opciones, tipos de búsqueda y restricción de resultados.",time:"1.5 h",obj:["Hacer búsquedas simples y avanzadas","Usar operadores y filtros","Elegir fuentes confiables"],sum:["Palabras clave sin artículos.","\"frase\", site:, filetype:, -, OR.","Filtros por tipo y fecha.","Fuentes oficiales y recientes."],q:"¿Qué operador te ahorraría más tiempo en tus tareas?",rev:[["Un sitio pide tu NIP para «verificar tu cuenta». Es…",["Phishing","Una actualización","Un sitio oficial"],0,"Ningún banco pide el NIP."],["Lo más seguro para bajar un programa es…",["Su sitio oficial","Una página de cracks","Un enlace de un SMS"],0,"El sitio oficial es la fuente confiable."]]},
f:{k:"Bloque F",l:"F",ic:"✅",t:"Buenas prácticas",d:"Malware, spam, intrusos, piratería, phishing, pharming, fraudes, robo de información y ética.",time:"1 h",obj:["Reconocer los riesgos de internet","Aplicar hábitos de seguridad y ética"],sum:["Malware: virus, gusano, troyano, ransomware, spyware.","Phishing por mensaje; pharming por DNS.","La piratería es ilegal y trae malware.","Cita tus fuentes: copiar sin citar es plagio."],q:"¿Qué hábito de seguridad vas a empezar hoy?",rev:[["Para buscar solo en sitios de gobierno usas…",["site:gob.mx","filetype:gob","-gob"],0,"site: limita el dominio."],["Las comillas en una búsqueda sirven para…",["Buscar la frase exacta","Quitar palabras","Buscar PDF"],0,"Buscan exactamente esa frase."]]}
'''

ILL = r'''
ILL["¿Cómo funciona internet?"]=function(){return flow([["💻","Tu equipo"],["📒","DNS|nombre → IP"],["🌐","Internet"],["🖥️","Servidor|201.175.40.10"],["📄","Página"]],"Del dominio a la página")};
ILL["Protocolos: las reglas para hablar"]=function(){return grid3([["📨","HTTP|sin cifrar"],["🔒","HTTPS|cifrado"],["📦","FTP|archivos"],["📒","DNS|nombres"]],"Protocolos de internet")};
ILL["Las herramientas que te cuidan"]=function(){return grid3([["🕵️","Antispyware|espías"],["📭","Antispam|basura"],["🧱","Firewall|intrusos"],["🎣","Anti-phishing|impostores"]],"Una herramienta por amenaza")};
ILL["Las partes del navegador"]=function(){return SV(340,120,R_(4,6,332,26,"s",6)+T_(16,23,"Pestaña 1 | Pestaña 2 | ＋","t","start")+R_(4,38,332,28,"w",14)+T_(16,56,"← 🔒 https://www.conalep.edu.mx      ☆ ⋮","t","start")+R_(4,72,332,44,"w",6)+T_(170,98,"Contenido de la página","tm"),"Pestañas, barra de direcciones, favoritos y menú")};
ILL["Motores de búsqueda"]=function(){return flow([["🔤","Palabras|clave"],["🧩","Operadores"],["🎚️","Filtros"],["✅","Fuente|confiable"]],"Cómo afinar una búsqueda")};
ILL["Riesgos en internet"]=function(){return grid3([["🦠","Malware"],["📭","Spam"],["🥷","Intrusos"],["🏴‍☠️","Piratería"],["🎣","Phishing"],["🪤","Pharming"]],"Riesgos en internet")};
'''

EXH = r'''
EXH.privacidad=function(){return exw(mw('Configuración › Privacidad y seguridad','<div class="mm"><span>☑ Navegación segura '+mk(1)+'</span><span>☑ Usar siempre conexiones seguras (HTTPS) '+mk(2)+'</span><span>☑ Bloquear cookies de terceros</span></div>'),['Activa la protección contra sitios peligrosos.','Te avisa si un sitio no tiene HTTPS.'])};
EXH.candado=function(){return exw(mw('Navegador','<div class="mfld">🔒 https://www.conalep.edu.mx '+mk(1)+'</div><div class="mfld" style="margin-top:6px">⚠️ No seguro | neverssl.com '+mk(2)+'</div>'),['Con candado: conexión cifrada.','Sin candado: no escribas datos.'])};
EXH.buscar=function(){return exw(mw('Buscador','<div class="mfld">"beca benito juarez" site:gob.mx filetype:pdf '+mk(1)+'</div><div class="mm" style="margin-top:6px"><span>Todo</span><span>Videos</span><span class="hl">Herramientas › Último año '+mk(2)+'</span></div>'),['Frase exacta + sitio + tipo de archivo.','Limita por fecha.'])};
EXH.descargas=function(){return exw(mw('Descargas','<div class="mm"><span>📄 7z2408-x64.exe · www.7-zip.org · Analizado '+mk(1)+'</span><span>⛔ Office_FULL_crack.exe · Bloqueado '+mk(2)+'</span></div>'),['Del sitio oficial y analizado.','El navegador bloqueó el archivo peligroso.'])};
EXH.cel_priv=function(){return exw(mp('Chrome en el celular','<div class="mbox">⋮ › Configuración › Privacidad y seguridad › Navegación segura '+mk(1)+'</div><div class="mbox" style="margin-top:6px">⋮ › Nueva pestaña de incógnito '+mk(2)+'</div>'),['Activa la protección.','Navega sin guardar historial.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Mi navegador seguro',
     'prog': 'Bloques A, B, C y D · Seguridad, internet y navegador',
     'min': 60, 'lug': 'Viernes 11-dic en laboratorio, o en casa (computadora o celular)',
     'modes': {
         'pc': {'mat': ['Computadora con Chrome, Edge o Firefox', 'Word o Documentos de Google'],
                'steps': [
                    'Antes de empezar, termina los simuladores 1, 2 y 3.',
                    'Abre Seguridad de Windows y toma captura del estado del antivirus (antispyware) y del firewall.',
                    ['Entra a www.conalep.edu.mx, toca el candado y anota el protocolo y si el certificado es válido.', 'candado'],
                    ['En Configuración › Privacidad y seguridad activa la navegación segura y el uso de HTTPS; toma captura.', 'privacidad'],
                    'Abre tres pestañas con sitios de la escuela y guárdalos en una carpeta de favoritos llamada «Escuela».',
                    'Abre el historial, revisa lo que visitaste hoy y borra los datos de navegación de la última hora.',
                    ['Descarga un programa útil (por ejemplo 7-Zip) desde su sitio oficial y toma captura del panel de descargas.', 'descargas'],
                    'Pega todas las capturas en un documento y explica en una línea qué protege cada configuración.']},
         'cel': {'mat': ['Celular con Chrome, Safari o el navegador que uses'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 1, 2 y 3.',
                     ['En el menú del navegador activa la navegación segura y abre una pestaña de incógnito.', 'cel_priv'],
                     'Entra a www.conalep.edu.mx, toca el candado y toma captura de la información del sitio.',
                     'Guarda tres sitios de la escuela en favoritos y toma captura.',
                     'Revisa el historial y borra los datos de la última hora.',
                     'Pega las capturas en un documento (Documentos de Google o Word móvil) y explica qué protege cada una.']}},
     'entrega': ['Documento con capturas de la configuración de seguridad del navegador y su explicación.'],
     'rub': [['Herramientas de seguridad del equipo', 20], ['Candado y protocolo', 15], ['Privacidad configurada', 25], ['Favoritos e historial', 20], ['Descarga segura y explicación', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Trabajo documental de búsqueda',
     'prog': 'Bloques E y F · Buscadores y buenas prácticas',
     'min': 60, 'lug': 'Martes 15-dic en clase o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con navegador', 'Word o Documentos de Google'],
                'steps': [
                    'Antes de empezar, termina el simulador 4.',
                    'Elige un tema: becas para media superior, uso de internet en México o cómo evitar fraudes en línea.',
                    'Haz una búsqueda simple y anota cuántos resultados aparecen.',
                    ['Repite la búsqueda con al menos tres operadores (comillas, site:, filetype:, − u OR) y con un filtro de fecha o tipo.', 'buscar'],
                    'Elige tres fuentes confiables; para cada una anota título, dirección, autor o institución, fecha y por qué confías en ella.',
                    'Escribe un resumen de media página con tus propias palabras y cita las fuentes al final.',
                    'Agrega un apartado «Navegué seguro» con tres medidas de seguridad que aplicaste.']},
         'cel': {'mat': ['Celular con navegador', 'Documentos de Google o Word móvil'],
                 'steps': [
                     'Antes de empezar, termina el simulador 4.',
                     'Elige uno de los tres temas.',
                     'Busca primero con palabras simples y luego con al menos tres operadores; toma captura de cada búsqueda.',
                     'Elige tres fuentes confiables y anota título, dirección, institución y fecha.',
                     'Escribe el resumen con tus palabras, cita las fuentes y agrega tres medidas de seguridad que aplicaste.']}},
     'entrega': ['Trabajo documental (Word o PDF) con búsquedas, fuentes, resumen y medidas de seguridad.'],
     'rub': [['Búsqueda simple y avanzada con capturas', 30], ['Tres fuentes confiables bien citadas', 25], ['Resumen con palabras propias', 25], ['Medidas de seguridad', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 4',
    'ra': 'R.A. 4.1', 'title': 'Trabajo documental de búsqueda de información en internet',
    'data': [
        ('Resultado de aprendizaje', 'Navega en internet y busca información de manera segura, utilizando las herramientas del navegador y de los motores de búsqueda.'),
        ('Actividad de evaluación', '4.1.1 Realiza un trabajo documental con los resultados de búsqueda de información en internet, aplicando medidas de seguridad.'),
        ('Evidencia', 'Trabajo documental con resultados de búsqueda de información'),
        ('Ponderación', '5% (según el programa)'),
        ('Entrega', 'Martes 15 de diciembre: archivo en la plataforma'),
    ],
    'situation': 'El encargado de la Cafetería La Escuelita necesita información confiable para un aviso a los alumnos. Investiga el tema que elegiste en internet, con búsquedas avanzadas y navegando seguro, y entrégale un trabajo documental.',
    'hint': 'Toma capturas de tus búsquedas mientras las haces: así no tienes que repetirlas al armar el documento.',
    'steps': [
        ('Seguridad del navegador (A a D)', [
            'Capturas de la navegación segura, el uso de HTTPS y el candado de un sitio oficial.',
            'Una descarga segura desde un sitio oficial o la explicación de cómo la harías.']),
        ('Búsqueda de información (E)', [
            'Una búsqueda simple y la misma búsqueda con al menos tres operadores y un filtro.',
            'Tres fuentes confiables con título, dirección, institución, fecha y por qué confías.']),
        ('Resumen y buenas prácticas (F)', [
            'Resumen de media página con tus palabras y las fuentes citadas.',
            'Tres medidas de seguridad y una reflexión sobre el uso ético de la información.']),
    ],
    'rubric': [
        ('Configuración segura del navegador', 20), ('Búsqueda simple y avanzada', 25), ('Fuentes confiables bien citadas', 20),
        ('Resumen con palabras propias', 20), ('Medidas de seguridad y ética', 15),
    ],
    'deliver': ['Un archivo Word (.docx) o PDF.', 'Nombre del archivo: Apellido_Nombre_EDOA41.', 'Súbelo en la actividad R.A. 4.1 de la plataforma.'],
}
