"""EDOA-20 · R.A. 4.2 · Configurar un cliente de correo electrónico.

Caso de la Cafetería La Escuelita: el encargado quiere leer el correo de la cafetería en la computadora
de la caja y en su celular. Incluye dos simuladores de configuración de cuentas (net_sim.js en modo cfg).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-4.2'
CODE_PREFIX = 'EDOA42'
FILE = 'edoa-ra42-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 4.2 · Configurar el correo'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 4.2 · Cliente de correo'
HERO_KICK = 'EDOA-20 · R.A. 4.2'
HERO_TITLE = 'Tu correo, bien configurado'
HERO_TEXT = 'Entiende cómo viaja un correo entre servidores y configura una cuenta con IMAP, POP3 y SMTP de forma segura.'
EV_SHORT = 'entrega tu documento ilustrado de la configuración del cliente de correo.'
EV_CARD = 'Documento ilustrado R.A. 4.2'
RA = 'R.A. 4.2'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores de configuración'], 'c': ['Construye', 'Prácticas con tu correo']}

_DIR = Path(__file__).parent
EXTRA_JS = (_DIR / 'xl3_sim.js').read_text(encoding='utf8') + '\n' + (_DIR / 'net_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".netsim"))nInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".netsim"))return nCheck(d);\n'),
]

c = Course()

ACCOUNTS = [{'mail': 'cafeteria@escuelita.mx', 'pw': 'Cafe2026!'}, {'mail': 'ventas@escuelita.mx', 'pw': 'Ventas#311'}]


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.used, a.acc, a.S)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pNet({j(ic)},{j(t)},{j(inf)},{{mode:"cfg",title:"Correo · Configuración de cuentas",accounts:{j(ACCOUNTS)},tasks:{ts},hint:{j(hint)}{extra}}})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('📧', 'El correo de la cafetería', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Un <b>cliente de correo</b> es el programa o la app con que lees y envías correos (Outlook, Thunderbird, la app Correo del celular o Gmail en el navegador). Para que funcione hay que decirle <b>a qué servidores conectarse</b>.'),
    ex('Caso: Cafetería La Escuelita', 'La escuela le dio a la cafetería la cuenta <code>cafeteria@escuelita.mx</code>. El encargado quiere leerla en la computadora de la caja y en su celular, sin que se pierdan mensajes y sin que nadie pueda espiar su contraseña.'),
    r3([('🖥️', 'A · Servidores y clientes', 'Quién guarda, quién envía y quién lee el correo.'), ('📨', 'A · Protocolos', 'SMTP para enviar; POP3 e IMAP para recibir.'), ('⚙️', 'B · Configuración', 'Entrada, salida, puertos y seguridad.')])),
    'Servidor guarda · cliente muestra · protocolos conectan.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia (5%)', 'Un <b>documento ilustrado</b> (Word o PDF) que describa, paso a paso y con capturas, la <b>configuración de un cliente de correo</b>: servidor de entrada (IMAP o POP3), servidor de salida (SMTP), puertos y seguridad.'),
    bk('Cómo se arma', 'Practica en los dos simuladores y luego configura una cuenta real en Outlook, Thunderbird o la app Correo de tu celular. Toma capturas de cada pantalla.'),
    warn('Importante', 'En tus capturas <b>tapa tu contraseña</b>. Nunca la escribas en el documento.')),
    'Simula, configura de verdad y documenta.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Servidores, clientes y protocolos ─────────────────────────
a0 = c.mark()
c.L('🖥️', 'Servidores y clientes de correo', 'Bloque A · Quién hace qué', body(
    sp('En palabras sencillas', 'El <b>servidor de correo</b> es una computadora que siempre está encendida y funciona como oficina de correos: recibe, guarda y entrega mensajes. El <b>cliente</b> es lo que usas tú para verlos.'),
    bk('Servidor de entrada', 'Guarda tu buzón. Tu cliente se conecta a él para <b>bajar o ver</b> los mensajes (IMAP o POP3). Ejemplo: <code>imap.escuelita.mx</code>.'),
    bk('Servidor de salida', 'Recibe lo que envías y lo lleva al servidor del destinatario (SMTP). Ejemplo: <code>smtp.escuelita.mx</code>.'),
    bk('Cliente de software', 'Programa instalado: <b>Outlook</b>, <b>Thunderbird</b>, la app <b>Correo</b> de Windows, del iPhone o de Android. Hay que configurarlo con los servidores.'),
    bk('Cliente web (webmail)', 'Lo abres en el navegador: <b>Gmail</b>, <b>Outlook.com</b>. El proveedor ya lo configuró; tú solo inicias sesión. Funciona sobre un <b>servidor HTTP</b> (mejor dicho HTTPS, con candado).'),
    ana('Piensa en la oficina de correos', 'Servidor = la oficina con tu apartado postal. Cliente = tú yendo por tus cartas. SMTP = el cartero que lleva tus cartas. IMAP/POP3 = la forma de recoger las tuyas.')),
    'Webmail: solo inicias sesión. Programa o app: lo configuras tú.')
c.L('📨', 'SMTP, POP3 e IMAP', 'Bloque A · Los protocolos del correo', body(
    bk('SMTP · enviar', '<i>Simple Mail Transfer Protocol</i>. Lleva el correo de tu cliente a tu servidor y de tu servidor al del destinatario. Puertos seguros: <b>587</b> (STARTTLS) o <b>465</b> (SSL/TLS).'),
    bk('POP3 · descargar', '<i>Post Office Protocol</i>. <b>Baja</b> los mensajes a un solo equipo y, normalmente, los <b>borra del servidor</b>. Si lo usas en dos equipos, activa «Dejar una copia en el servidor». Puerto seguro: <b>995</b>.'),
    bk('IMAP · sincronizar', '<i>Internet Message Access Protocol</i>. Los mensajes <b>se quedan en el servidor</b> y todos tus equipos ven lo mismo: si lees un correo en el celular, aparece leído en la computadora. Puerto seguro: <b>993</b>.'),
    ex('¿Cuál conviene?', 'El encargado usa la computadora de la caja <b>y</b> su celular → <b>IMAP</b>. Una computadora vieja, con poco internet y un solo usuario → POP3 puede servir.'),
    warn('Puertos sin cifrar', '143 (IMAP), 110 (POP3) y 25 (SMTP) mandan tu contraseña <b>sin cifrar</b>. Úsalos solo si el proveedor no ofrece otra opción.')),
    'SMTP envía · POP3 baja y borra · IMAP sincroniza.')
c.A('📨', '¿Qué protocolo es?', 'Elige el protocolo que corresponde a cada descripción.', [
    ['Envía tu mensaje al servidor del destinatario', 'SMTP', 'SMTP es el protocolo de salida.'],
    ['Baja los mensajes a un equipo y suele borrarlos del servidor', 'POP3', 'POP3 descarga al equipo.'],
    ['Lees un correo en el celular y aparece leído también en la computadora', 'IMAP', 'IMAP sincroniza todo con el servidor.'],
    ['Usa normalmente el puerto 993', 'IMAP', 'IMAP seguro usa 993.'],
    ['Usa el puerto 587 con STARTTLS', 'SMTP', 'Es el puerto de envío recomendado.'],
    ['Usa el puerto 995', 'POP3', 'POP3 seguro usa 995.'],
], 'Salida = SMTP · entrada = POP3 o IMAP.', ['SMTP', 'POP3', 'IMAP'])
c.O('✉️', 'El viaje de un correo', 'Ordena lo que pasa desde que el encargado envía un correo hasta que la directora lo lee.', [
    ['El encargado escribe el mensaje en su cliente y da Enviar', 'Todo empieza en el cliente.'],
    ['El cliente lo entrega por SMTP a smtp.escuelita.mx', 'SMTP es la salida.'],
    ['El servidor de la escuela lo pasa al servidor de correo de la directora', 'Los servidores también hablan SMTP entre ellos.'],
    ['El mensaje queda guardado en el buzón de la directora', 'El servidor de entrada lo guarda.'],
    ['El cliente de la directora lo descarga o sincroniza por IMAP o POP3', 'Al final se recibe.'],
], 'Cliente → SMTP → servidores → buzón → IMAP/POP3 → cliente.')
c.T('🔢', 'Puertos que debes conocer', 'Escribe solo el número del puerto.', [
    ['IMAP con SSL/TLS', '993', 'IMAP seguro usa 993.', 'Empieza con 99…', 'n'],
    ['POP3 con SSL/TLS', '995', 'POP3 seguro usa 995.', 'Dos más que IMAP seguro.', 'n'],
    ['SMTP con STARTTLS (el recomendado para enviar)', '587', 'SMTP de envío usa 587.', 'Termina en 87.', 'n'],
    ['SMTP con SSL/TLS', '465', 'La otra opción segura de SMTP.', 'Está entre 400 y 500.', 'n'],
    ['HTTPS (webmail con candado)', '443', 'El webmail seguro usa HTTPS, puerto 443.', 'El puerto de HTTPS.', 'n'],
], 'Seguro: 993, 995, 587/465 y 443.', 'n')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Configuración ─────────────────────────
b0 = c.mark()
c.L('⚙️', 'Configurar la cuenta paso a paso', 'Bloque B · Entrada, salida y seguridad', body(
    sp('En palabras sencillas', 'Muchos clientes se configuran solos con tu correo y contraseña. Cuando no, eliges <b>configuración manual</b> y escribes los datos que da tu proveedor.'),
    px('Configuración manual', [
        'Abre el cliente › <b>Agregar cuenta</b> › Configuración manual (o avanzada).',
        'Escribe tu <b>nombre</b> (el que verán los demás), tu <b>correo</b> y tu <b>contraseña</b>.',
        '<b>Servidor de entrada</b>: elige IMAP o POP3, escribe el servidor, el puerto y la seguridad SSL/TLS.',
        '<b>Autenticación segura</b>: «Contraseña normal» solo sobre conexión cifrada, o «Contraseña cifrada» si el servidor la admite.',
        '<b>Servidor de salida (SMTP)</b>: servidor, puerto 587 con STARTTLS (o 465 con SSL/TLS) y «el servidor requiere autenticación».',
        'Toca <b>Probar conexión</b>; si todo está bien, <b>Hecho</b>.']),
    bk('Datos de La Escuelita', 'Entrada IMAP: <code>imap.escuelita.mx</code> · 993 · SSL/TLS. Entrada POP3: <code>pop.escuelita.mx</code> · 995 · SSL/TLS. Salida: <code>smtp.escuelita.mx</code> · 587 · STARTTLS (o 465 · SSL/TLS).'),
    warn('Si falla', 'Lee el error: «no responde en el puerto» = puerto equivocado · «pide seguridad SSL/TLS» = cambia la seguridad · «autenticación fallida» = contraseña incorrecta · «no se pudo conectar» = nombre del servidor mal escrito.')),
    'Nombre, correo y contraseña → entrada → salida → probar.')
c.Z('📝', 'Completa la ficha de configuración', 'Elige el dato correcto para configurar la cuenta de la cafetería con IMAP.',
    '<p>Protocolo de entrada: {0}</p><p>Servidor de entrada: {1}</p><p>Puerto de entrada: {2} con seguridad {3}</p><p>Servidor de salida: {4}, puerto {5} con STARTTLS</p>',
    [['IMAP', ['IMAP', 'POP3', 'SMTP']],
     ['imap.escuelita.mx', ['imap.escuelita.mx', 'smtp.escuelita.mx', 'www.escuelita.mx']],
     ['993', ['993', '143', '25']],
     ['SSL/TLS', ['SSL/TLS', 'Ninguna']],
     ['smtp.escuelita.mx', ['smtp.escuelita.mx', 'imap.escuelita.mx', 'pop.escuelita.mx']],
     ['587', ['587', '110', '80']]],
    'Entrada IMAP 993 SSL/TLS · salida SMTP 587 STARTTLS.')
sim('⚙️', 'Configura la cuenta con IMAP', 'Simulador: cuenta de la cafetería en la computadora y el celular.', {
    'id': 'c1', 'intro': 'Configura la cuenta <code>cafeteria@escuelita.mx</code> (contraseña de práctica: <code>Cafe2026!</code>) para que se vea igual en la computadora de la caja y en el celular del encargado.'}, [
    ['Toca <b>Agregar cuenta de correo</b> y escribe nombre, correo y contraseña.', 'a.used("newacc")'],
    ['Usa <b>Probar conexión</b> y lee los errores que salgan.', 'a.S.tests>=1'],
    ['Logra una <b>conexión correcta</b> con IMAP.', 'a.used("ok_imap")'],
    ['Guarda la cuenta (Hecho) con IMAP <b>993 SSL/TLS</b> y SMTP <b>587 STARTTLS</b>.', 'a.acc.some(function(x){return x.mail=="cafeteria@escuelita.mx"&&x.inP=="imap"&&x.inPort=="993"&&x.inSec=="SSL/TLS"&&x.outPort=="587"&&x.outSec=="STARTTLS"})']],
    'Los datos de los servidores están en la lección «Configurar la cuenta paso a paso».')
c.L('📥', 'POP3: cuándo y cómo', 'Bloque B · Descargar sin perder mensajes', body(
    bk('Cuándo usar POP3', 'Cuando solo un equipo lee el correo, cuando el buzón del servidor es pequeño o cuando quieres guardar los mensajes en tu equipo para leerlos sin internet.'),
    bk('Dejar copia en el servidor', 'Si activas esta opción, POP3 baja los mensajes pero <b>no los borra</b> del servidor, y así también los puedes ver desde el celular o el webmail.'),
    bk('Respaldos', 'Con POP3 los mensajes viven en tu computadora: si se descompone, se pierden. Respalda el archivo de datos del cliente (por ejemplo, el .pst de Outlook).'),
    ex('Caso', 'La cuenta <code>ventas@escuelita.mx</code> se lee en una computadora vieja de la bodega, pero la directora a veces revisa el webmail. Se configura con POP3 y <b>copia en el servidor</b>.')),
    'POP3 + dejar copia = no pierdes mensajes en el servidor.')
sim('📥', 'Configura una cuenta con POP3', 'Simulador: cuenta de ventas con copia en el servidor y SMTP 465.', {
    'id': 'c2', 'intro': 'Configura la cuenta <code>ventas@escuelita.mx</code> (contraseña de práctica: <code>Ventas#311</code>) en la computadora de la bodega.'}, [
    ['Agrega la cuenta y elige <b>POP3</b> como protocolo de entrada.', 'a.S.form&&a.S.form.inP=="pop"||a.acc.some(function(x){return x.inP=="pop"})'],
    ['Activa <b>Dejar una copia de los mensajes en el servidor</b>.', 'a.S.form&&a.S.form.keep||a.acc.some(function(x){return x.keep})'],
    ['Logra una <b>conexión correcta</b> con POP3.', 'a.used("ok_pop")'],
    ['Guarda la cuenta con POP3 <b>995 SSL/TLS</b> y SMTP <b>465 SSL/TLS</b>.', 'a.acc.some(function(x){return x.mail=="ventas@escuelita.mx"&&x.inP=="pop"&&x.inPort=="995"&&x.inSec=="SSL/TLS"&&x.keep&&x.outPort=="465"&&x.outSec=="SSL/TLS"})']],
    'Al cambiar a POP3 el servidor cambia: pop.escuelita.mx.')
c.A('🧰', '¿Qué está mal configurado?', 'Lee el error del cliente y elige qué hay que corregir.', [
    ['«El servidor de entrada no responde en el puerto 143»', 'Puerto', 'IMAP seguro usa 993.'],
    ['«Autenticación fallida: la contraseña no es correcta»', 'Contraseña', 'Revisa mayúsculas y símbolos.'],
    ['«No se pudo conectar al servidor imap.escuelita.com»', 'Servidor', 'El dominio correcto es escuelita.mx.'],
    ['«Con el puerto 465 el servidor SMTP pide SSL/TLS»', 'Seguridad', 'El puerto 465 va con SSL/TLS, no STARTTLS.'],
], 'El mensaje de error dice qué parte revisar.', ['Puerto', 'Contraseña', 'Servidor', 'Seguridad'])
c.W('✍️', 'Explica tu configuración', 'Describe cómo configuraste tu cliente de correo.',
    'Escribe cómo configurarías el correo de la cafetería en un celular. Menciona el <b>protocolo de entrada</b> que elegiste y por qué, el <b>servidor y puerto</b> de entrada y de salida, y la <b>seguridad</b> usada.',
    [['Tiene al menos 35 palabras', 'palabras:35'],
     ['Menciona IMAP o POP3', '\\b(imap|pop3?)\\b'],
     ['Menciona SMTP', '\\bsmtp\\b'],
     ['Menciona un puerto', '\\b(993|995|587|465)\\b'],
     ['Menciona la seguridad (SSL, TLS o STARTTLS)', '\\b(ssl|tls|starttls|cifrad\\w*)\\b']],
    'Entrada · salida · puertos · seguridad.', 'Ejemplo: Elegí IMAP porque…')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Servidor de correo', 'Equipo que recibe, guarda y entrega los mensajes.'),
    bk('Cliente de correo', 'Programa, app o página con que lees y envías correo.'),
    bk('Webmail', 'Cliente de correo que se usa en el navegador (HTTPS).'),
    bk('SMTP', 'Protocolo para enviar correo (587 o 465).'),
    bk('POP3', 'Protocolo que descarga los mensajes a un equipo (995).'),
    bk('IMAP', 'Protocolo que sincroniza los mensajes con el servidor (993).'),
    bk('Puerto', 'Número de la «puerta» por donde entra un servicio en el servidor.'),
    bk('SSL/TLS', 'Cifrado de la conexión desde el inicio.'),
    bk('STARTTLS', 'Empieza la conexión normal y luego la cifra.'),
    bk('Autenticación', 'Comprobar con usuario y contraseña que la cuenta es tuya.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311. El R.A. 4.2 dura 5 h, vale 5% y la A.E. es el viernes 18-dic. Si los alumnos no tienen cuenta propia, pueden usar una cuenta personal de Gmail u Outlook configurada en la app Correo.', 'sp'),
    bk('Martes 15-dic · Bloque A', 'Después de entregar el 4.1: servidores y clientes, SMTP, POP3 e IMAP, y puertos.'),
    bk('Miércoles 16-dic · Bloques A y B', 'Configuración manual con los dos simuladores y <b>Práctica 1</b> (configurar una cuenta real).'),
    bk('Viernes 18-dic · Evaluación (laboratorio)', 'Entrega del documento ilustrado (<b>Práctica 2</b>). El mismo día arranca el R.A. 4.3.'),
    bk('Gmail y Outlook', 'Gmail y Outlook.com ya no aceptan la contraseña normal en clientes externos: piden iniciar sesión con OAuth2 o una contraseña de aplicación. Explícalo como «autenticación segura».', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '📧', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '📨', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '⚙️', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"📧",t:"Empieza aquí",d:"Qué es un cliente de correo y qué vas a entregar.",time:"10 min",obj:["Distinguir cliente y servidor de correo","Conocer la evidencia del R.A."],sum:["Cliente = donde lees tu correo.","Servidor = donde se guarda.","Evidencia: documento ilustrado de la configuración (5%)."],q:"¿En cuántos dispositivos revisas tu correo?"},
a:{k:"Bloque A",l:"A",ic:"📨",t:"Servidores, clientes y protocolos",d:"Servidores, clientes web y de software, SMTP, POP3 e IMAP.",time:"2 h",obj:["Explicar la función del servidor y del cliente","Distinguir SMTP, POP3 e IMAP","Reconocer los puertos seguros"],sum:["Webmail ya está configurado; la app no.","SMTP envía (587/465).","POP3 descarga (995); IMAP sincroniza (993)."],q:"¿Qué protocolo usarías si revisas tu correo en el celular y en la computadora?"},
b:{k:"Bloque B",l:"B",ic:"⚙️",t:"Configuración del cliente",d:"Entrada POP3 o IMAP con autenticación segura, salida SMTP y servidores HTTP.",time:"3 h",obj:["Configurar una cuenta con IMAP","Configurar una cuenta con POP3 dejando copia","Interpretar los errores de conexión"],sum:["Nombre, correo, contraseña.","Entrada: servidor, puerto y SSL/TLS.","Salida SMTP con autenticación.","Probar conexión antes de guardar."],q:"¿Qué dato revisarías primero si el correo no se envía?",rev:[["Para enviar correo se usa…",["SMTP","IMAP","POP3"],0,"SMTP es la salida."],["IMAP seguro usa el puerto…",["993","25","80"],0,"993 con SSL/TLS."]]}
'''

ILL = r'''
ILL["Servidores y clientes de correo"]=function(){return flow([["💻","Cliente|encargado"],["📤","SMTP|salida"],["🏤","Servidor|escuelita.mx"],["📥","IMAP/POP3|entrada"],["📱","Cliente|directora"]],"Cliente, servidores y protocolos")};
ILL["SMTP, POP3 e IMAP"]=function(){return grid3([["📤","SMTP|587 · 465"],["⬇️","POP3|995"],["🔄","IMAP|993"]],"Protocolos y puertos seguros")};
ILL["Configurar la cuenta paso a paso"]=function(){return flow([["👤","Nombre|y correo"],["📥","Entrada"],["📤","Salida"],["🔌","Probar"],["✅","Hecho"]],"Configuración manual")};
'''

EXH = r'''
EXH.agregar=function(){return exw(mw('Outlook › Archivo › Agregar cuenta','<div class="mfld">cafeteria@escuelita.mx '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Opciones avanzadas › ☑ Configurar mi cuenta manualmente '+mk(2)+'</div>'),['Escribe tu correo.','Elige configuración manual.'])};
EXH.entrada=function(){return exw(mw('Configuración de la cuenta IMAP','<div class="mm"><span>Correo entrante: imap.escuelita.mx · Puerto 993 '+mk(1)+'</span><span>Cifrado: SSL/TLS '+mk(2)+'</span></div>'),['Servidor y puerto de entrada.','Siempre cifrado.'])};
EXH.salida=function(){return exw(mw('Correo saliente','<div class="mm"><span>Servidor: smtp.escuelita.mx · Puerto 587 '+mk(1)+'</span><span>Cifrado: STARTTLS · ☑ Requiere autenticación '+mk(2)+'</span></div>'),['Servidor y puerto de salida.','El servidor pide tu usuario y contraseña.'])};
EXH.cel_cuenta=function(){return exw(mp('Correo en el celular','<div class="mbox">Configuración › Cuentas › Agregar › Otra › IMAP '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Servidor entrante y saliente, puertos y seguridad '+mk(2)+'</div>'),['Elige configuración manual o «Otra».','Escribe los mismos datos que en la computadora.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Configura una cuenta real',
     'prog': 'Bloques A y B · Protocolos y configuración',
     'min': 50, 'lug': 'Miércoles 16-dic en clase, o en casa (computadora o celular)',
     'modes': {
         'pc': {'mat': ['Computadora con Outlook, Thunderbird o la app Correo', 'Tu cuenta de correo'],
                'steps': [
                    'Antes de empezar, termina los simuladores 1 y 2.',
                    'Busca en la ayuda de tu proveedor (Gmail, Outlook, institucional) los servidores IMAP, POP3 y SMTP con sus puertos.',
                    ['Abre el cliente › Agregar cuenta › configuración manual.', 'agregar'],
                    ['Configura la entrada con IMAP, puerto seguro y SSL/TLS.', 'entrada'],
                    ['Configura la salida SMTP con su puerto, cifrado y autenticación.', 'salida'],
                    'Prueba enviándote un correo a ti mismo y toma captura de cada pantalla (tapa tu contraseña).']},
         'cel': {'mat': ['Celular con la app Correo, Outlook o Gmail', 'Tu cuenta de correo'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 1 y 2.',
                     'Busca los servidores IMAP y SMTP de tu proveedor.',
                     ['En la app agrega una cuenta con configuración manual («Otra»).', 'cel_cuenta'],
                     'Escribe servidor, puerto y seguridad de entrada y salida.',
                     'Envíate un correo de prueba y toma captura de cada pantalla (tapa tu contraseña).']}},
     'entrega': ['Capturas de cada pantalla de la configuración y del correo de prueba.'],
     'rub': [['Datos del proveedor investigados', 20], ['Entrada configurada con seguridad', 30], ['Salida SMTP configurada', 30], ['Prueba de envío', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Documento ilustrado de la configuración',
     'prog': 'Bloques A y B · Evidencia',
     'min': 60, 'lug': 'Viernes 18-dic en laboratorio o en casa',
     'modes': {
         'pc': {'mat': ['Word o Documentos de Google', 'Tus capturas de la práctica 1'],
                'steps': [
                    'Portada con tu nombre, grupo y el cliente que configuraste.',
                    'Explica con tus palabras qué es un servidor de correo, un cliente y la diferencia entre webmail y programa.',
                    'Tabla con SMTP, POP3 e IMAP: para qué sirve cada uno y su puerto seguro.',
                    'Paso a paso de tu configuración, una captura por paso con su explicación (tapa la contraseña).',
                    'Explica por qué elegiste IMAP o POP3 y qué seguridad usaste.',
                    'Cierra con tres errores comunes y cómo se corrigen.']},
         'cel': {'mat': ['Documentos de Google o Word móvil', 'Tus capturas de la práctica 1'],
                 'steps': [
                     'Portada con tu nombre, grupo y la app que configuraste.',
                     'Explica servidor, cliente, webmail y los tres protocolos con sus puertos.',
                     'Pega tus capturas en orden y explica cada paso.',
                     'Explica tu elección de protocolo y de seguridad, y tres errores comunes.']}},
     'entrega': ['Documento ilustrado (Word o PDF) con la configuración del cliente de correo.'],
     'rub': [['Conceptos de servidor, cliente y webmail', 20], ['Tabla de protocolos y puertos', 20], ['Paso a paso ilustrado', 40], ['Justificación y errores comunes', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 4',
    'ra': 'R.A. 4.2', 'title': 'Documento ilustrado de la configuración de un cliente de correo',
    'data': [
        ('Resultado de aprendizaje', 'Configura cuentas de correo electrónico en clientes de software o web, considerando los protocolos de entrada y salida y la autenticación segura.'),
        ('Actividad de evaluación', '4.2.1 Elabora un documento ilustrado que describa la configuración de un cliente de correo electrónico.'),
        ('Evidencia', 'Documento ilustrado de la configuración del cliente de correo'),
        ('Ponderación', '5% (según el programa)'),
        ('Entrega', 'Viernes 18 de diciembre: archivo en la plataforma'),
    ],
    'situation': 'El encargado de la Cafetería La Escuelita necesita un manual para configurar el correo en cualquier equipo nuevo. Elabora ese manual con tu propia configuración.',
    'hint': 'Tapa tu contraseña en todas las capturas: un manual nunca debe mostrarla.',
    'steps': [
        ('Conceptos (A)', [
            'Servidor, cliente de software y cliente web explicados con tus palabras.',
            'Tabla de SMTP, POP3 e IMAP con su función y puerto seguro.']),
        ('Configuración (B)', [
            'Paso a paso con capturas: cuenta, entrada (IMAP o POP3), salida (SMTP), puertos y seguridad.',
            'Prueba de envío y recepción.',
            'Por qué elegiste ese protocolo y tres errores comunes con su solución.']),
    ],
    'rubric': [
        ('Conceptos de servidor y cliente', 15), ('Protocolos y puertos', 20), ('Configuración de entrada', 20),
        ('Configuración de salida', 20), ('Prueba y justificación', 15), ('Presentación y capturas', 10),
    ],
    'deliver': ['Un archivo Word (.docx) o PDF.', 'Nombre del archivo: Apellido_Nombre_EDOA42.', 'Súbelo en la actividad R.A. 4.2 de la plataforma.'],
}
