"""MTCS-20 · R.A. 1.2 · Direccionamiento y enrutamiento IPv4.

Caso de las lecciones: Taller Mecánico Rápido (oficina y taller en una misma red).
La actividad de evaluación vive en la plataforma (MtcsActivity: reporte PDF con datos de red asignados).
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MTCS-RA-1.2'
CODE_PREFIX = 'MTCS12'
FILE = 'mtcs-ra12-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 1.2 · Direccionamiento y enrutamiento IPv4'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 1.2 · Direccionamiento y enrutamiento IPv4'
HERO_KICK = 'MTCS-20 · R.A. 1.2'
HERO_TITLE = 'Entiende cómo se identifican y se comunican los equipos de una red'
HERO_TEXT = 'Aprende direcciones IPv4, máscaras, subredes, puerta de enlace, IPv6 y DHCP con el caso de un taller mecánico.'
EV_SHORT = 'elabora tu reporte de direccionamiento y enrutamiento.'
EV_CARD = 'Reporte R.A. 1.2'
RA = 'R.A. 1.2'
GROUP = '511'
TABS = {'d': ['Diagnostica', 'Calcula subredes y revisa gateways'], 'c': ['Construye', 'Prácticas y reporte']}

EXTRA_JS = r'''

function ip2n(s){var m=String(s).trim().match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);if(!m)return null;var n=0;for(var i=1;i<5;i++){var o=+m[i];if(o>255)return null;n=n*256+o}return n}
function n2ip(n){n=n>>>0;return [n>>>24,(n>>>16)&255,(n>>>8)&255,n&255].join(".")}
function pmask(p){return p<=0?0:((0xFFFFFFFF<<(32-p))>>>0)}
function bin32(n,p){var s="";for(var i=0;i<32;i++){var b=(n>>>(31-i))&1;s+=(i<p?"<b>"+b+"</b>":b)+(i%8==7&&i<31?".":"")}return s}
function pSub(){K++;return '<article class="lesson"><header><span class="kick">🧮 Herramienta</span><h1>Calculadora de subredes</h1><p class="sub">Escribe una dirección IP y el prefijo. Verás la red, los hosts válidos y el broadcast.</p></header><style>.sbx input[type=text]{padding:11px;border:2px solid var(--line);border-radius:10px;font:17px Consolas,monospace;background:var(--card);color:var(--ink);width:100%}.sbx .row2{display:grid;grid-template-columns:2fr 1fr;gap:10px}.sbx label{font-weight:700;font-size:14px}.sbx .st3{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:10px 0}.sbx .st3 div{background:var(--bg);border-radius:10px;padding:8px 10px;font-size:15px;font-family:Consolas,monospace}.sbx .st3 b{display:block;font:700 11.5px system-ui;letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}.sbx .bn{font:13.5px/1.9 Consolas,monospace;background:var(--bg);border-radius:10px;padding:8px 10px;overflow-x:auto;white-space:nowrap}.sbx .bn b{color:var(--pri)}.sbx hr{border:0;border-top:1px solid var(--line);margin:14px 0}</style><div class="sbx"><div class="row2"><label>Dirección IP<input type="text" class="sip" value="192.168.10.25" inputmode="decimal" autocomplete="off"></label><label>Prefijo (/)<input type="text" class="spf" value="24" inputmode="numeric" autocomplete="off"></label></div><p class="sms" style="min-height:22px;margin:8px 0;color:var(--bad);font-weight:700"></p><div class="st3"><div><b>Máscara</b><span class="r1">—</span></div><div><b>Hosts utilizables</b><span class="r2">—</span></div><div><b>Dirección de red</b><span class="r3">—</span></div><div><b>Broadcast</b><span class="r4">—</span></div><div><b>Primer host</b><span class="r5">—</span></div><div><b>Último host</b><span class="r6">—</span></div></div><p style="margin:6px 0 4px;font-size:13px;color:var(--mut)">En negritas, los bits de la red; los demás son del host.</p><div class="bn r7"></div><hr><label>¿Cuántos hosts necesitas en la subred?<input type="text" class="sn" placeholder="Por ejemplo 28" inputmode="numeric" autocomplete="off"></label><p class="snr" style="margin:8px 0;font-weight:700"></p></div><p class="take"><b>Úsala para:</b> comprobar tus cálculos a mano antes de llenar la tabla de tu reporte.</p></article>'}
function subInit(d){var w=d.querySelector(".sbx");if(!w)return;var a=w.querySelector(".sip"),b=w.querySelector(".spf"),n=w.querySelector(".sn"),ms=w.querySelector(".sms"),seen={};
 function q(c){return w.querySelector("."+c)}
 function calc(x){var ip=ip2n(a.value),p=parseInt(b.value,10);["r1","r2","r3","r4","r5","r6"].forEach(function(c){q(c).textContent="—"});q("r7").innerHTML="";
  if(!a.value.trim()){ms.textContent="";return}
  if(ip===null){ms.textContent="La dirección debe tener 4 números del 0 al 255 separados por puntos.";return}
  if(!(p>=1&&p<=32)||String(p)!=b.value.trim()){ms.textContent="El prefijo debe ser un número del 1 al 32.";return}
  ms.textContent="";var m=pmask(p),net=(ip&m)>>>0,bc=(net|(~m>>>0))>>>0,h=p>=31?0:Math.pow(2,32-p)-2;
  q("r1").textContent=n2ip(m);q("r2").textContent=h.toLocaleString("es-MX");q("r3").textContent=n2ip(net);q("r4").textContent=n2ip(bc);q("r5").textContent=h?n2ip(net+1):"no aplica";q("r6").textContent=h?n2ip(bc-1):"no aplica";
  q("r7").innerHTML="IP&nbsp;&nbsp;&nbsp;"+bin32(ip,p)+"<br>Másc "+bin32(m,p);
  var key=n2ip(net)+"/"+p;if(x&&!seen[key]){seen[key]=1;if(Object.keys(seen).length>=3){var t="t:Calculadora de subredes";if(!ST[t]){ST[t]=1;sv()}}}}
 function need(){var v=parseInt(n.value,10),o=w.querySelector(".snr");if(!n.value.trim()){o.textContent="";return}if(!(v>=1&&v<=16000000)){o.textContent="Escribe un número de hosts mayor que cero.";return}
  var p=30;while(p>1&&Math.pow(2,32-p)-2<v)p--;o.textContent="Necesitas al menos /"+p+" (máscara "+n2ip(pmask(p))+"): caben "+(Math.pow(2,32-p)-2).toLocaleString("es-MX")+" hosts."}
 a.oninput=function(){calc(1)};b.oninput=a.oninput;n.oninput=need;calc(0)}
function pSame(){K++;return '<article class="lesson"><header><span class="kick">🔀 Herramienta</span><h1>¿Misma red o necesita gateway?</h1><p class="sub">Escribe dos equipos y el prefijo. Verás si se hablan directo o si el paquete debe pasar por el router.</p></header><style>.smx input[type=text]{padding:11px;border:2px solid var(--line);border-radius:10px;font:17px Consolas,monospace;background:var(--card);color:var(--ink);width:100%}.smx .g3{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}.smx label{font-weight:700;font-size:14px}.smx .vd{margin-top:12px;padding:12px;border-radius:12px;background:var(--bg);line-height:1.6}.smx .vd.ok{background:var(--ok-soft)}.smx .vd.bd{background:var(--bad-soft)}.smx .tr{font-size:13px;color:var(--mut);margin-top:6px}</style><div class="smx"><div class="g3"><label>Equipo A<input type="text" class="ia" value="192.168.10.20" inputmode="decimal" autocomplete="off"></label><label>Equipo B<input type="text" class="ib" value="192.168.10.70" inputmode="decimal" autocomplete="off"></label><label>Prefijo (/)<input type="text" class="ip" value="26" inputmode="numeric" autocomplete="off"></label><label>Gateway de A<input type="text" class="ig" value="192.168.10.1" inputmode="decimal" autocomplete="off"></label></div><div class="vd" role="status">Escribe los datos para ver el resultado.</div><p class="tr"></p></div><p class="take"><b>Úsala para:</b> responder «¿por qué no navega?» antes de tocar la configuración.</p></article>'}
function sameInit(d){var w=d.querySelector(".smx");if(!w)return;function g(c){return w.querySelector("."+c)}var seen={},o=g("vd");
 function run(x){var A=ip2n(g("ia").value),B=ip2n(g("ib").value),p=parseInt(g("ip").value,10),G=g("ig").value.trim()?ip2n(g("ig").value):-1;
  if(A===null||B===null||!(p>=1&&p<=30)){o.className="vd";o.textContent="Revisa que las dos direcciones sean válidas y que el prefijo sea del 1 al 30.";g("tr").textContent="";return}
  var m=pmask(p),nA=(A&m)>>>0,nB=(B&m)>>>0,same=nA==nB,h="";g("tr").textContent="Red de A: "+n2ip(nA)+"/"+p+" · Red de B: "+n2ip(nB)+"/"+p;
  if(same){h="✅ <b>Están en la misma red.</b> Se comunican directo, a través del switch; no necesitan al router."}else{h="🔀 <b>Están en redes distintas.</b> A entrega el paquete a su <b>puerta de enlace</b> y el router decide el camino hacia B."}
  var gwOk=true;if(G===null){h+="<br>⚠️ La dirección del gateway no es válida."}else if(G>=0){var bc=(nA|(~m>>>0))>>>0;if((G&m)>>>0!=nA){gwOk=false;h+="<br>❌ <b>El gateway "+n2ip(G)+" no está en la red de A.</b> A no puede alcanzarlo: no podrá salir de su red."}else if(G==nA||G==bc){gwOk=false;h+="<br>❌ El gateway no puede ser la dirección de red ni el broadcast."}else{h+="<br>✅ El gateway está en la red de A: es alcanzable."}}
  o.className="vd "+(gwOk?"ok":"bd");o.innerHTML=h;var k=(same?"s":"d")+(gwOk?"1":"0");if(x&&!seen[k]){seen[k]=1;if(seen.s1&&seen.d1){var t="t:¿Misma red o necesita gateway?";if(!ST[t]){ST[t]=1;sv()}}}}
 ["ia","ib","ip","ig"].forEach(function(c){g(c).oninput=function(){run(1)}});run(0)}
'''
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n subInit(d);sameInit(d);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🔧', 'Cada equipo necesita una dirección', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Para que dos computadoras se hablen, cada una necesita una <b>dirección IP</b>, como tu casa necesita una dirección para que llegue el correo. Una <b>máscara</b> dice qué parte de la dirección es la calle (la red) y cuál es el número de casa (el equipo).'),
    ex('Caso de las lecciones: Taller Mecánico Rápido', 'Tiene una oficina con 4 computadoras y una impresora, y un taller con una pantalla de diagnóstico y 3 tabletas. Todo cuelga de un solo switch y un solo router. Los de la oficina empiezan a ver la red lenta y el dueño quiere separar las dos áreas.'),
    bk('Qué vas a hacer', '<b>1. Aprende</b> los conceptos con ejemplos. <b>2. Diagnostica</b> con una calculadora de subredes y un revisor de gateway. <b>3. Construye</b> tres prácticas que te preparan para tu reporte.'),
    bk('Al final', 'Entregas un <b>reporte en PDF</b> con los datos de red que te asigna la plataforma en la actividad de evaluación.')),
    'Una dirección identifica al equipo; la máscara dice a qué red pertenece.')
c.A('🔎', '¿Qué es cada dato?', 'Relaciona cada dato de red del taller con su función.', [
    ['192.168.10.25', 'Dirección IP', 'Identifica al equipo.'],
    ['255.255.255.0', 'Máscara', 'Separa la parte de red de la parte de host.'],
    ['192.168.10.1', 'Puerta de enlace', 'Es el router al que se envía lo que sale de la red.'],
    ['8.8.8.8', 'Servidor DNS', 'Traduce nombres de páginas a direcciones.'],
], 'IP = quién eres · Máscara = en qué red estás · Gateway = por dónde sales · DNS = traduce nombres.', ['Dirección IP', 'Máscara', 'Puerta de enlace', 'Servidor DNS'])
s0_end = c.mark() - 1

# ───────────────────────── A · Acceso e IP ─────────────────────────
a0 = c.mark()
c.L('🔌', 'Capa de acceso', 'Bloque A · Conectarse a la red local', body(
    sp('En palabras sencillas', 'La <b>capa de acceso</b> es la parte que conecta un dispositivo al medio local (cable o wifi) y entrega los datos <b>dentro de la misma red</b>.'),
    bk('Dirección física (MAC)', 'Cada tarjeta de red trae una dirección única de 48 bits de fábrica. El switch la usa para saber por qué puerto mandar los datos.'),
    bk('Dispositivos', 'El <b>switch</b> conecta equipos por cable en la misma red; el <b>punto de acceso</b> hace lo mismo por wifi.'),
    ana('Piensa en…', 'Un edificio: la MAC es el nombre pegado en cada puerta y el switch es el conserje que lleva el paquete al departamento correcto del mismo edificio.'),
    ex('En el taller', 'La computadora de recepción manda un archivo a la impresora de la oficina. El switch lo entrega por el puerto correcto; todavía no necesita salir a otra red.')),
    'MAC = identidad local · Switch = entrega dentro de la misma red.')
c.L('🔢', 'Propósito de IP y máscara', 'Bloque A · Las direcciones IPv4', body(
    sp('En palabras sencillas', 'Una dirección <b>IPv4</b> tiene 32 bits, separados en 4 grupos de 8 llamados <b>octetos</b>: por ejemplo <b>192.168.10.25</b>. Cada octeto va de 0 a 255.'),
    bk('La máscara', 'Marca con unos los bits de <b>red</b> y con ceros los bits de <b>host</b>. <b>255.255.255.0</b> equivale a <b>/24</b>: los primeros 24 bits son la red.'),
    ex('En 192.168.10.25/24', '<b>Red:</b> 192.168.10.0 · <b>Host:</b> el 25 · <b>Primer host:</b> .1 · <b>Último:</b> .254 · <b>Broadcast:</b> .255 · <b>Hosts utilizables:</b> 254.'),
    bk('Direcciones reservadas', 'La primera de la red (todos los bits de host en 0) es la <b>dirección de red</b>; la última (todos en 1) es el <b>broadcast</b>. Ninguna se le asigna a un equipo.'),
    warn('Recuerda', 'Utilizables = 2<sup>bits de host</sup> − 2. Con /24 hay 8 bits de host: 256 − 2 = 254.')),
    'La máscara separa red y host · Hosts utilizables = 2^bits de host − 2.')
c.A('🔢', 'Red y host en /24', 'Para cada dirección /24 del taller, ¿cuál es la dirección de red?', [
    ['192.168.10.25/24', '192.168.10.0', 'Los tres primeros octetos son la red; el host se pone en 0.'],
    ['192.168.40.130/24', '192.168.40.0', 'Con /24 siempre termina en .0.'],
    ['10.0.5.99/24', '10.0.5.0', 'Conserva 10.0.5 y cambia el último octeto a 0.'],
    ['172.16.8.200/24', '172.16.8.0', 'La red es 172.16.8.0.'],
], 'Con /24 la red conserva 3 octetos y el último es 0 · el broadcast termina en 255.', ['192.168.10.0', '192.168.40.0', '10.0.5.0', '172.16.8.0'])
c.Z('📌', 'Completa las ideas clave', 'Elige la palabra correcta en cada frase.',
    '<p>Una dirección IPv4 tiene {0} bits.</p>'
    '<p>La {1} separa la parte de red de la parte de host.</p>'
    '<p>La última dirección de una red se llama {2}.</p>'
    '<p>Con /24 hay {3} hosts utilizables.</p>',
    [['32', ['32', '48', '128']],
     ['máscara', ['máscara', 'MAC', 'DNS']],
     ['broadcast', ['broadcast', 'gateway', 'unicast']],
     ['254', ['254', '256', '255']]])
a_end = c.mark() - 1

# ───────────────────────── B · Comunicación y subredes ─────────────────────────
b0 = c.mark()
c.L('📣', 'Unicast, broadcast y multicast', 'Bloque B · A quién le hablas', body(
    sp('En palabras sencillas', 'Hay tres formas de enviar datos según cuántos receptores tengan.'),
    r3([('🎯', 'Unicast', 'A un solo destino'), ('📢', 'Broadcast', 'A todos en la red'), ('👥', 'Multicast', 'A un grupo suscrito')]),
    ana('Piensa en…', 'Unicast: una llamada telefónica. Broadcast: un altavoz en toda la plaza. Multicast: un chat de grupo al que solo entran los suscritos.'),
    ex('En el taller', 'Imprimir en una sola impresora es unicast. «¿Quién tiene la 192.168.10.5?» lo oyen todos: broadcast. Una transmisión de video para algunas pantallas suscritas es multicast.'),
    warn('Dato importante', 'Demasiado broadcast hace la red lenta. Por eso se dividen las redes grandes en subredes.')),
    'Unicast = uno · Broadcast = todos · Multicast = un grupo.')
c.A('📣', '¿Unicast, broadcast o multicast?', 'Clasifica cada envío.', [
    ['Mandar una foto de una tableta a la impresora', 'Unicast', 'Un origen y un solo destino.'],
    ['Un equipo pregunta a toda la red quién tiene cierta dirección', 'Broadcast', 'Se envía a todos los equipos de la red local.'],
    ['Una pantalla transmite una capacitación solo a los equipos suscritos', 'Multicast', 'Va a un grupo específico.'],
    ['Abrir una página web desde tu equipo', 'Unicast', 'Es una comunicación entre dos extremos.'],
    ['Un aviso a todos los equipos de la red local', 'Broadcast', 'Todos lo reciben.'],
], 'Uno → unicast · Todos → broadcast · Grupo → multicast.', ['Unicast', 'Broadcast', 'Multicast'])
c.L('✂️', 'Segmentación en subredes', 'Bloque B · Dividir una red', body(
    sp('En palabras sencillas', '<b>Segmentar</b> es dividir una red grande en redes más pequeñas llamadas <b>subredes</b>. Se logra «pidiendo prestados» bits de host y agregándolos a la parte de red: el prefijo crece.'),
    bk('Para qué sirve', 'Reduce el broadcast, ordena los equipos por área y permite poner reglas de seguridad entre ellas.'),
    bk('Prefijos comunes', '<b>/24</b>: 254 hosts · <b>/25</b>: 126 · <b>/26</b>: 62 · <b>/27</b>: 30 · <b>/28</b>: 14 · <b>/29</b>: 6 · <b>/30</b>: 2.'),
    ex('En el taller: 192.168.10.0/24 para 50 y 20 equipos', 'Oficina (50) necesita /26 (62 hosts): red <b>192.168.10.0</b>, hosts .1 a .62, broadcast .63. Taller (20) cabe en /27 (30 hosts): red <b>192.168.10.64</b>, hosts .65 a .94, broadcast .95.'),
    warn('Cuidado', 'La segunda subred empieza justo después del broadcast de la primera, y ninguna dirección puede repetirse. Comprueba tus cálculos en la pestaña <b>Diagnostica</b>.')),
    'Subredes: elige el prefijo que alcance, calcula red, rango y broadcast, y la siguiente empieza después.')
c.raw('pSub()')
c.A('✂️', '¿Cuántos hosts caben?', 'Relaciona cada prefijo con sus hosts utilizables.', [
    ['/24', '254', '8 bits de host: 256 − 2.'],
    ['/26', '62', '6 bits de host: 64 − 2.'],
    ['/27', '30', '5 bits de host: 32 − 2.'],
    ['/28', '14', '4 bits de host: 16 − 2.'],
    ['/30', '2', '2 bits de host: 4 − 2.'],
], 'Cada bit de host que quitas parte los hosts a la mitad.', ['254', '62', '30', '14', '2'])
c.A('🧮', '¿Qué prefijo necesita?', 'Elige el prefijo más pequeño que alcance para cada área.', [
    ['Oficina con 50 equipos', '/26', '62 hosts alcanzan; /27 solo tiene 30.'],
    ['Taller con 20 equipos', '/27', '30 hosts alcanzan; /28 solo tiene 14.'],
    ['Sala de juntas con 10 equipos', '/28', '14 hosts alcanzan.'],
    ['Enlace entre dos routers', '/30', 'Solo se necesitan 2 hosts.'],
    ['Área con 120 equipos', '/25', '126 hosts alcanzan; /26 se queda corto.'],
], 'Elige el prefijo cuyo total de hosts sea igual o mayor a los que necesitas.', ['/25', '/26', '/27', '/28', '/30'])
c.W('✍️', 'Explica una subred', 'Aplica lo aprendido.',
    'Con la oficina del taller (192.168.10.0/26) explica cuál es su <b>dirección de red</b>, su <b>rango de hosts</b> y su <b>broadcast</b>, y por qué el broadcast no se le puede asignar a un equipo.',
    [['Tiene al menos 30 palabras', 'palabras:30'],
     ['Menciona la dirección de red', '(192\\.168\\.10\\.0|direcci.n de red)'],
     ['Menciona el rango o el primer y último host', '(\\.1|\\.62|primer|último|ultimo|rango)'],
     ['Menciona el broadcast', '(192\\.168\\.10\\.63|broadcast)'],
     ['Explica por qué no se asigna', '(reservad|todos|no se (puede|asigna)|no.*(equipo|host))']],
    'Una o dos oraciones por dato.', 'Ejemplo: La red es 192.168.10.0, los hosts van de .1 a .62 y el broadcast es .63…')
b_end = c.mark() - 1

# ───────────────────────── C · Enrutamiento, IPv6 y DHCP ─────────────────────────
c0 = c.mark()
c.L('🚪', 'Puerta de enlace y enrutamiento', 'Bloque C · Salir de tu red', body(
    sp('En palabras sencillas', 'Si el destino está en <b>otra red</b>, el equipo no lo busca directo: entrega el paquete a su <b>puerta de enlace</b> (gateway), que es la interfaz del router en su misma red. El router consulta su <b>tabla de enrutamiento</b> para decidir el siguiente camino.'),
    bk('¿Cómo sabe el equipo si es otra red?', 'Compara su red con la del destino usando la máscara. Si las redes son distintas, usa el gateway.'),
    bk('Reglas del gateway', 'Debe estar en <b>la misma red</b> que el equipo y no puede ser la dirección de red ni el broadcast. Si está mal escrito, el equipo no sale de su red.'),
    ana('Piensa en…', 'Tu colonia: si el destino está en tu calle, caminas. Si está en otra colonia, llegas a la avenida principal (gateway) y ahí te dicen qué camino tomar.'),
    ex('En el taller', 'La oficina (192.168.10.0/26) manda un archivo al taller (192.168.10.64/27). Son redes distintas: el equipo lo manda al gateway 192.168.10.1 y el router lo entrega al taller.')),
    'Misma red → directo · Otra red → gateway → router.')
c.O('🛤️', 'Ordena: el recorrido de un paquete', 'Un equipo de la oficina manda un archivo al servidor del taller, en otra subred. Ordena los pasos.', [
    ['El equipo compara su red con la del destino y ve que es otra', 'Lo primero es saber si el destino es local.'],
    ['Entrega el paquete a su puerta de enlace', 'No puede llegar directo a otra red.'],
    ['El router revisa su tabla de enrutamiento', 'Decide por cuál interfaz sale.'],
    ['El router lo envía a la subred del taller', 'Elige el siguiente camino.'],
    ['El switch del taller lo entrega al servidor', 'La entrega final es local, dentro de la subred.'],
], 'Comparar · gateway · tabla · salida · entrega local.')
c.raw('pSame()')
c.A('🚪', '¿Directo o por gateway?', 'Con /24 en cada equipo, ¿cómo se comunican?', [
    ['192.168.10.20 → 192.168.10.30', 'Directo', 'Ambos están en 192.168.10.0/24.'],
    ['192.168.10.20 → 192.168.20.30', 'Por gateway', 'Una es red 10 y la otra red 20.'],
    ['10.0.5.8 → 10.0.5.200', 'Directo', 'Los dos pertenecen a 10.0.5.0/24.'],
    ['172.16.1.5 → 172.16.2.5', 'Por gateway', 'Los terceros octetos son distintos con /24.'],
], 'Misma red → directo · Distinta red → por gateway.', ['Directo', 'Por gateway'])
c.L('🌐', 'IPv6 y DHCP', 'Bloque C · Más direcciones y configuración automática', body(
    sp('IPv6', 'Usa <b>128 bits</b> escritos en hexadecimal, separados por dos puntos: <b>2001:db8:10::25</b>. Existe porque IPv4 ya casi no tiene direcciones libres.'),
    bk('Diferencias con IPv4', 'IPv4: 32 bits, decimal, 4 octetos. IPv6: 128 bits, hexadecimal, 8 grupos. IPv6 da un espacio de direcciones enorme y no depende de NAT para conectar muchos equipos.'),
    sp('DHCP', 'Es el servicio que <b>asigna automáticamente</b> dirección IP, máscara, puerta de enlace y DNS a los equipos que se conectan.'),
    ex('En el taller', 'Las tabletas del taller reciben su configuración por DHCP al conectarse. La impresora y el servidor usan una dirección fija para que siempre se encuentren.'),
    bk('Cuándo usar cada una', '<b>Dinámica (DHCP)</b> para equipos que entran y salen. <b>Estática</b> para servidores, impresoras y routers.')),
    'IPv6: 128 bits · DHCP: configura automáticamente · Estática: para servidores y routers.')
c.A('🌐', '¿IPv4, IPv6 o DHCP?', 'Elige a qué corresponde cada frase.', [
    ['Usa 32 bits escritos en cuatro octetos', 'IPv4', 'Ese es el formato de IPv4.'],
    ['Usa 128 bits escritos en hexadecimal', 'IPv6', 'Tiene espacio de direcciones mucho mayor.'],
    ['Asigna IP, máscara, gateway y DNS de forma automática', 'DHCP', 'Es el servicio de configuración automática.'],
    ['2001:db8:10::25', 'IPv6', 'Se escribe con dos puntos y hexadecimal.'],
    ['192.168.200.14', 'IPv4', 'Cuatro octetos separados por puntos.'],
], 'Octetos decimales → IPv4 · Hexadecimal con dos puntos → IPv6 · Automático → DHCP.', ['IPv4', 'IPv6', 'DHCP'])
c.W('✍️', 'Explica por qué un equipo no navega', 'Aplica lo aprendido.',
    'Un equipo del taller tiene IP 192.168.10.25/24 y gateway <b>192.168.20.1</b>. Se comunica con la impresora pero no abre páginas. Explica el problema y cómo lo corregirías.',
    [['Tiene al menos 30 palabras', 'palabras:30'],
     ['Identifica que el gateway no está en su red', '(gateway|puerta de enlace)'],
     ['Menciona la red o el rango correcto', '(192\\.168\\.10|misma red|otra red|distint)'],
     ['Propone una corrección', '(cambi|corregi|configur|poner|usar|192\\.168\\.10\\.1)']],
    'Tres o cuatro oraciones.', 'Ejemplo: El gateway 192.168.20.1 está en otra red…')
c_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Dirección IP', 'Número que identifica a un equipo en una red.'),
    bk('Máscara de subred', 'Marca qué bits son de red y cuáles de host.'),
    bk('Prefijo', 'Cantidad de bits de red; se escribe con /.'),
    bk('Dirección de red', 'Primera dirección de la red; identifica la red.'),
    bk('Broadcast', 'Última dirección de la red; llega a todos.'),
    bk('Host', 'Equipo con dirección en la red.'),
    bk('Subred', 'Red más pequeña dentro de una red mayor.'),
    bk('Puerta de enlace', 'Router al que se envía lo que sale de la red.'),
    bk('Tabla de enrutamiento', 'Lista que usa el router para elegir el camino.'),
    bk('DHCP', 'Servicio que asigna la configuración de red automáticamente.'),
    bk('IPv6', 'Versión de IP con direcciones de 128 bits.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Grupo 511: <b>lunes 17:20-18:10</b> y <b>viernes 18:10-19:50</b>. Cada práctica tiene versión para celular. Las herramientas de <b>Diagnostica</b> funcionan en celular y no envían datos a ningún servidor.', 'sp'),
    bk('Bloque A · acceso e IP', 'Una sesión: capa de acceso, IPv4, máscara y reservadas. Pide a los alumnos escribir la dirección de red a mano y comprobarla con la calculadora.'),
    bk('Bloque B · subredes', 'Una o dos sesiones: tipos de comunicación y segmentación. <b>Práctica 1</b> en clase.'),
    bk('Bloque C · enrutamiento', 'Una sesión: gateway, recorrido del paquete, IPv6 y DHCP. <b>Práctica 2</b> y <b>3</b>.'),
    bk('Evaluación', 'Actividad en la plataforma: un <b>reporte en PDF</b> con datos de red asignados a cada alumno (valor 60 puntos).')),
    'Ajusta las sesiones a tu cronograma.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🔧', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🔢', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '✂️', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🚪', 'a': c0, 'b': c_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🔧",t:"Empieza aquí",d:"Dirección, máscara y gateway con el caso de un taller mecánico.",time:"20 min",obj:["Reconocer los datos de red de un equipo","Conocer el caso y la evidencia final"],sum:["IP = quién eres · Máscara = en qué red · Gateway = por dónde sales.","Entregas un reporte con los datos de red que te asigne la plataforma."],q:"¿Qué pasaría si dos equipos de una red tuvieran la misma dirección IP?"},
a:{k:"Bloque A",l:"A",ic:"🔢",t:"Acceso e IP",d:"Capa de acceso, direcciones IPv4 y máscara.",time:"90 min",obj:["Explicar la función de la capa de acceso","Separar red y host con la máscara","Calcular hosts utilizables"],sum:["La MAC identifica a la tarjeta en la red local.","IPv4 tiene 32 bits en 4 octetos.","Hosts utilizables = 2^bits de host − 2."],q:"¿Por qué la primera y la última dirección de una red no se asignan a equipos?"},
b:{k:"Bloque B",l:"B",ic:"✂️",t:"Comunicación y subredes",d:"Unicast, broadcast, multicast y segmentación.",time:"110 min",obj:["Distinguir unicast, broadcast y multicast","Elegir el prefijo que alcance","Calcular red, rango y broadcast de una subred"],sum:["Más broadcast hace más lenta la red.","Cada bit de host que quitas parte los hosts a la mitad.","La segunda subred empieza después del broadcast de la primera."],q:"¿Por qué conviene separar la oficina del taller en subredes distintas?"},
c:{k:"Bloque C",l:"C",ic:"🚪",t:"Enrutamiento, IPv6 y DHCP",d:"Puerta de enlace, tabla de enrutamiento, IPv6 y configuración automática.",time:"90 min",obj:["Decidir si un envío es directo o por gateway","Explicar el recorrido de un paquete","Comparar IPv4 con IPv6 y explicar DHCP"],sum:["Otra red → gateway → router.","El gateway debe estar en la misma red que el equipo.","IPv6 usa 128 bits; DHCP asigna la configuración."],q:"¿Qué equipos de tu escuela deberían tener dirección fija y cuáles dinámica?"},
'''

ILL = r'''
ILL["Propósito de IP y máscara"]=function(){return flow([["🌐","Red|192.168.10"],["💻","Host|.25"],["🎭","Máscara|/24"]],"Dirección = red + host")};
ILL["Segmentación en subredes"]=function(){return flow([["🏢","Red grande|/24"],["✂️","Dividir|más prefijo"],["🏬","Subredes|/26 y /27"]],"De una red a varias subredes")};
ILL["Puerta de enlace y enrutamiento"]=function(){return flow([["💻","Equipo"],["🚪","Gateway"],["🧭","Router|tabla"],["🏠","Otra red"]],"Cómo sale un paquete")};
'''

EXH = r'''
function cw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:#0c0c0c;color:#eee;padding:10px;font:12.5px/1.45 Consolas,monospace;white-space:pre-wrap;overflow-x:auto">'+b+'</pre></div>'}
EXH.tabla_sub=function(){return exw('<table class="mtb"><tr><th></th><th>Subred A</th><th>Subred B</th></tr><tr><td>Hosts pedidos</td><td>50</td><td>20</td></tr><tr><td>Prefijo y máscara</td><td>/26 · 255.255.255.192</td><td>/27 · 255.255.255.224</td></tr><tr><td>Dirección de red</td><td>192.168.10.0</td><td>192.168.10.64</td></tr><tr><td>Primer host</td><td>192.168.10.1</td><td>192.168.10.65</td></tr><tr><td>Último host</td><td>192.168.10.62</td><td>192.168.10.94</td></tr><tr><td>Broadcast</td><td>192.168.10.63</td><td>192.168.10.95</td></tr></table>',['Ejemplo con otros números: usa los datos de tu práctica.','Comprueba cada fila con la Calculadora de subredes.'])};
EXH.asignacion=function(){return exw('<table class="mtb"><tr><th>Dispositivo</th><th>IP</th><th>Máscara</th><th>Gateway</th></tr><tr><td>Router (interfaz A)</td><td>192.168.10.1</td><td>255.255.255.192</td><td>—</td></tr><tr><td>Servidor</td><td>192.168.10.2</td><td>255.255.255.192</td><td>192.168.10.1</td></tr><tr><td>PC 1</td><td>192.168.10.10</td><td>255.255.255.192</td><td>192.168.10.1</td></tr><tr><td>PC 2</td><td>192.168.10.11</td><td>255.255.255.192</td><td>192.168.10.1</td></tr></table>',['Ninguna dirección se repite.','No uses la dirección de red ni el broadcast.'])};
EXH.revisor=function(){return exw('<div class="mbox">🔀 <b>¿Misma red o necesita gateway?</b> (pestaña Diagnostica)<br>A: 192.168.10.20 · B: 192.168.10.70 · /26<br>🔀 <b>Están en redes distintas.</b> A entrega el paquete a su puerta de enlace.<br>✅ El gateway está en la red de A.</div>',['Prueba un caso que se comunique directo y otro que no.','Toma captura de los dos resultados.'])};
EXH.ipconfig=function(){return exw(cw_('Símbolo del sistema','C:\\\\&gt; ipconfig\n\nAdaptador de Ethernet:\n   Dirección IPv4. . . : 192.168.10.25\n   Máscara . . . . . . : 255.255.255.0\n   Puerta de enlace . .: 192.168.20.1'),['El gateway 192.168.20.1 no está en la red 192.168.10.0/24: ese es el error.','Anota en qué línea está el problema.'])};
EXH.pingseq=function(){return exw(cw_('Símbolo del sistema','C:\\\\&gt; ping 127.0.0.1      → responde (tarjeta de red OK)\nC:\\\\&gt; ping 192.168.10.25   → responde (IP propia OK)\nC:\\\\&gt; ping 192.168.10.1    → responde (gateway alcanzable)\nC:\\\\&gt; ping 8.8.8.8         → responde (hay salida)\nC:\\\\&gt; ping www.ejemplo.com  → falla (problema de DNS)'),['Los pings van de lo más cercano a lo más lejano.','El primero que falla indica dónde está el problema.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Divide la red del taller en dos subredes',
     'prog': 'Bloque B · Segmentación',
     'min': 45, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con Word o Excel', 'Este material (Calculadora de subredes)'],
                'steps': [
                    'Parte de la red 192.168.30.0/24 del taller. La oficina necesita 40 equipos y el taller 12.',
                    'Elige el prefijo más pequeño que alcance para cada subred y anótalo con su máscara.',
                    ['Calcula a mano red, primer host, último host y broadcast de cada subred y llénalos en una tabla.', 'tabla_sub'],
                    ['Comprueba tus resultados en la pestaña Diagnostica con la Calculadora de subredes y corrige si hace falta.', 'revisor'],
                    'Escribe una frase: por qué la segunda subred empieza donde empieza.']},
         'cel': {'mat': ['Celular', 'Este material (Calculadora de subredes)', 'Notas o Documentos de Google'],
                 'steps': [
                     'Parte de la red 192.168.30.0/24 del taller. La oficina necesita 40 equipos y el taller 12.',
                     'Elige el prefijo más pequeño que alcance para cada subred y anótalo con su máscara.',
                     ['Calcula a mano red, primer host, último host y broadcast de cada subred y anótalos.', 'tabla_sub'],
                     ['Comprueba tus resultados en la pestaña Diagnostica con la Calculadora de subredes y corrige si hace falta.', 'revisor'],
                     'Escribe una frase: por qué la segunda subred empieza donde empieza.']}},
     'entrega': ['Tabla con prefijo, máscara, red, primer host, último host y broadcast de las dos subredes, ya comprobada con la calculadora.'],
     'rub': [['Prefijos correctos', 25], ['Direcciones de red y broadcast correctas', 35], ['Rangos de hosts sin traslape', 25], ['Explicación', 15]]},
    {'id': 'pr2', 'n': 2, 't': 'Asigna direcciones y gateway',
     'prog': 'Bloques A y C · IP, máscara y puerta de enlace',
     'min': 40, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con Word o Excel', 'Tus subredes de la práctica 1'],
                'steps': [
                    ['Para cada subred, arma una tabla con router, servidor y dos equipos: IP, máscara y gateway.', 'asignacion'],
                    'Revisa que ninguna dirección se repita y que no uses la de red ni el broadcast.',
                    ['Usa el revisor de la pestaña Diagnostica con un equipo de cada subred para confirmar que el gateway está en su red.', 'revisor'],
                    'Escribe 3 renglones explicando la función de cada gateway.']},
         'cel': {'mat': ['Celular', 'Tus subredes de la práctica 1', 'Notas'],
                 'steps': [
                     ['Para cada subred, anota router, servidor y dos equipos: IP, máscara y gateway.', 'asignacion'],
                     'Revisa que ninguna dirección se repita y que no uses la de red ni el broadcast.',
                     ['Usa el revisor de la pestaña Diagnostica con un equipo de cada subred para confirmar que el gateway está en su red.', 'revisor'],
                     'Escribe 3 renglones explicando la función de cada gateway.']}},
     'entrega': ['Tabla de asignación de direcciones de las dos subredes y la explicación de cada gateway.'],
     'rub': [['Direcciones sin repetir ni reservadas', 35], ['Máscaras correctas', 20], ['Gateway en la red correcta', 30], ['Explicación', 15]]},
    {'id': 'pr3', 'n': 3, 't': 'Diagnostica un equipo que no navega',
     'prog': 'Bloque C · Diagnóstico ordenado',
     'min': 45, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con Word', 'Este material (¿Misma red o necesita gateway?)'],
                'steps': [
                    ['Lee el resultado de ipconfig de un equipo del taller: IP 192.168.10.25/24 y gateway 192.168.20.1.', 'ipconfig'],
                    ['Escribe el orden en que probarías con ping para encontrar la falla.', 'pingseq'],
                    ['Comprueba en la pestaña Diagnostica si el gateway es alcanzable desde la red del equipo.', 'revisor'],
                    'Propón la corrección y cómo verificarías que ya navega.']},
         'cel': {'mat': ['Celular', 'Este material (¿Misma red o necesita gateway?)', 'Notas'],
                 'steps': [
                     ['Lee el resultado de ipconfig de un equipo del taller: IP 192.168.10.25/24 y gateway 192.168.20.1.', 'ipconfig'],
                     ['Escribe el orden en que probarías con ping para encontrar la falla.', 'pingseq'],
                     ['Comprueba en la pestaña Diagnostica si el gateway es alcanzable desde la red del equipo.', 'revisor'],
                     'Propón la corrección y cómo verificarías que ya navega.']}},
     'entrega': ['Diagnóstico escrito: causa, orden de pruebas, corrección y forma de verificar.'],
     'rub': [['Identifica la causa', 30], ['Orden lógico de pruebas', 30], ['Corrección adecuada', 25], ['Verificación', 15]]},
]

EVALUATION = {
    'course': 'MTCS-20 · Manejo de tecnologías de ciberseguridad · Unidad 1',
    'ra': 'R.A. 1.2', 'title': 'Reporte de direccionamiento y enrutamiento',
    'data': [
        ('Resultado de aprendizaje', 'Configura el direccionamiento y enrutamiento IPv4 de una red con la finalidad de segmentarla y comunicarla.'),
        ('Actividad de evaluación', 'Reporte en PDF con el direccionamiento y enrutamiento de los datos de red que te asigna la plataforma.'),
        ('Evidencia', 'Reporte en PDF'),
        ('Valor', '60 puntos'),
        ('Entrega', 'En la actividad R.A. 1.2 de la plataforma. Si aún no entregas, consulta con tu docente.'),
    ],
    'situation': 'En la actividad de evaluación de la plataforma tienes asignados una red base, la cantidad de hosts de dos subredes y un equipo con falla. Prepara un reporte en PDF con tus cálculos y explicaciones.',
    'hint': 'Escribe tus cálculos a mano o en una tabla y compruébalos en la Calculadora de subredes antes de entregar.',
    'steps': [
        ('Análisis de la red', ['Explica qué información dan la dirección de red y la máscara asignadas.']),
        ('Subredes A y B', ['Calcula prefijo, máscara, red, primer host, último host y broadcast de cada una.']),
        ('Asignación y gateway', ['Asigna direcciones a router, servidor y dos equipos por subred.', 'Indica la puerta de enlace de cada subred y su función.']),
        ('Recorrido y diagnóstico', ['Explica el recorrido de un paquete de una subred a la otra.', 'Diagnostica el equipo con falla y propón una solución.']),
        ('IPv6 y entrega', ['Explica dos razones para adoptar IPv6 y una diferencia con IPv4.', 'Guarda el reporte como PDF y súbelo en la actividad de la plataforma.']),
    ],
    'rubric': [('Análisis de la red', 10), ('Subredes A y B', 30), ('Asignación de direcciones', 15), ('Gateway y recorrido', 20), ('Diagnóstico', 15), ('IPv6', 10)],
    'deliver': ['Un archivo PDF con tu reporte.', 'Se entrega en la actividad R.A. 1.2 de la plataforma.'],
}
