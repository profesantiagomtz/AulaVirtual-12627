"""MTCS-20 · R.A. 2.2 · Principios y tecnologías de integridad y disponibilidad.

Caso de las lecciones: Clínica dental Sonríe (expedientes, citas y cobros).
La actividad de evaluación vive en la plataforma (MtcsActivity, con organización asignada y PDF).

Versión «anti dudas» (nov-2026): repaso de lo que se necesita de R.A. anteriores, ejemplos
resueltos paso a paso con el porqué de cada paso, pistas en todas las actividades y prácticas
explicadas paso por paso. Las actividades conservan su título para que el avance guardado se
reubique solo (ver MIGRA y mig22 en EXTRA_JS).
"""
import re

from cw import Course, Js, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MTCS-RA-2.2'
CODE_PREFIX = 'MTCS22'
FILE = 'mtcs-ra22-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 2.2 · Integridad, disponibilidad y defensa'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 2.2 · Integridad, disponibilidad y defensa'
HERO_KICK = 'MTCS-20 · R.A. 2.2'
HERO_TITLE = 'Que la información sea confiable y esté siempre disponible'
HERO_TEXT = 'Paso a paso y sin prisas: aprende a comprobar que los datos no cambiaron, a mantener los servicios funcionando y a defender equipos, servidores y redes.'
EV_SHORT = 'elabora tu reporte con la organización asignada.'
EV_CARD = 'Reporte R.A. 2.2'
RA = 'R.A. 2.2'
GROUP = '511'

TABS = {'d': ['Diagnostica', 'Laboratorio de hash y calculadora'], 'c': ['Construye', 'Prácticas explicadas paso a paso']}


def why(t):
    """Explicación del porqué de un paso (se muestra debajo del paso)."""
    return f'<span class="why">🤔 <b>¿Por qué?</b> {t}</span>'


def ojo(t):
    """Error común o qué hacer si algo no sale."""
    return f'<span class="why ojo">⚠️ <b>Si algo no sale:</b> {t}</span>'


def paso(hacer, porque):
    return f'<b>{hacer}</b>{why(porque)}'


# Avance guardado de la versión anterior: índice de página → título. Al abrir el material,
# mig22 mueve cada actividad terminada a su nuevo lugar (se buscan por título).
OLD_TITLES = [
    '¿Se puede confiar en la información?', '¿Qué pilar se afecta?', 'Hash: la huella digital de los datos',
    'Laboratorio de hash', '¿Qué pasa con la huella?', 'La técnica salting', 'Ordena: guardar una contraseña',
    'HMAC: hash con clave secreta', 'Firmas digitales y certificados', 'Integridad en bases de datos',
    '¿Qué control de integridad usas?', 'Completa las reglas de la base de datos', 'Disponibilidad y alta disponibilidad',
    'Los «nueves» de la disponibilidad', 'Calcula el tiempo fuera de servicio', 'Defensa en profundidad',
    'Respuesta a incidentes', 'Recuperación tras un desastre: RPO y RTO', 'Ordena la respuesta a un ransomware',
    '¿RPO o RTO?', '¿Qué mecanismo usarías?', 'Protección del host', 'Protección del servidor', 'Protección de la red',
    'Seguridad física', '¿Qué capa protege?', '¿Buena o mala práctica?', 'Defiende la clínica en 4 capas',
    'Vulnerabilidades: CVE y CVSS', 'Clasifica la gravedad', 'Ética y principios rectores', '¿Es ético?',
    'Herramientas de ciberseguridad', '¿Qué herramienta usas?', 'Glosario (1 de 2)', 'Glosario (2 de 2)',
    'Guía para el docente',
]

EXTRA_JS_BASE = r'''
(function(){var s=document.createElement("style");s.textContent=".why{display:block;margin-top:5px;padding:6px 9px;border-radius:9px;background:color-mix(in srgb,var(--pri) 8%,transparent);font-weight:400;font-size:14.5px;line-height:1.45}.why.ojo{background:color-mix(in srgb,#e0a800 14%,transparent)}.why b{font-weight:700}.dl3{display:grid;gap:6px;margin:8px 0}.dl3 div{border:1.5px solid var(--line);border-radius:10px;padding:7px 10px;background:var(--card)}.dl3 .dh{display:block;font-weight:700;margin-bottom:2px}.dl3 i{display:block;margin-top:2px}.displab .dx{font-size:18px;padding:8px 10px;width:100%;max-width:220px;display:block;margin-top:4px}.dres{font-size:20px;font-weight:700}@media print{.why{background:none;padding:0 0 0 4px;font-size:inherit}}";document.head.appendChild(s)})();
function pHash(){K++;return '<article class="lesson"><header><span class="kick">🧪 Herramienta</span><h1>Laboratorio de hash</h1><p class="sub">Aquí puedes ver con tus propios ojos cómo funciona un hash. No se califica: es para experimentar.</p></header><div class="co co-def"><div class="co-l">Cómo usarlo (3 pasos)</div><p><b>1.</b> Mira la huella que sale abajo para el texto que ya está escrito.<br><b>2.</b> Cambia una sola letra (por ejemplo «Ana» por «Ena») y observa cuántos caracteres de la huella cambian.<br><b>3.</b> Activa la casilla de la sal y vuelve a escribir: aunque el texto sea el mismo, la huella cambia porque se le agregó un valor al azar.</p></div><div class="hashlab czf"><label>Texto (puede ser una contraseña de prueba o un dato del expediente)<textarea class="hx" rows="2">Ana López · alergia a la penicilina</textarea></label><label style="display:flex;gap:8px;align-items:center;font-weight:500"><input type="checkbox" class="hs"> Agregar sal (un valor aleatorio antes del texto)</label><div class="co co-def"><div class="co-l">Huella SHA-256 (siempre 64 caracteres)</div><p class="ho" style="font-family:Consolas,monospace;word-break:break-all;margin:0"></p></div><p class="hn" style="font-size:14.5px;color:var(--mut)"></p></div><p class="take"><b>¿Qué debes notar?</b> Mismo texto = misma huella. Una letra distinta = huella casi completamente distinta. Por eso el hash sirve para descubrir si alguien cambió algo.</p></article>'}
function hashInit(d){var x=d.querySelector(".hx"),s=d.querySelector(".hs"),o=d.querySelector(".ho"),n=d.querySelector(".hn"),prev=null,salt="";
 function hex(b){return [].map.call(new Uint8Array(b),function(v){return ("0"+v.toString(16)).slice(-2)}).join("")}
 function go(){if(!(window.crypto&&crypto.subtle)){o.textContent="Tu navegador no permite calcular el hash aquí.";return}
  if(s.checked&&!salt){var r=new Uint8Array(4);crypto.getRandomValues(r);salt=hex(r.buffer)}if(!s.checked)salt="";
  crypto.subtle.digest("SHA-256",new TextEncoder().encode(salt+x.value)).then(function(b){var h=hex(b),c=0;if(prev)for(var i=0;i<64;i++)if(prev[i]!=h[i])c++;o.textContent=h;n.innerHTML=(salt?"Sal: <b>"+salt+"</b> · se calcula SHA-256(sal + texto). ":"")+(prev&&prev!=h?"Cambiaron <b>"+c+" de 64</b> caracteres de la huella.":"");prev=h})}
 x.oninput=go;s.onchange=function(){salt="";go()};go()}
function pDisp(){K++;return '<article class="lesson"><header><span class="kick">🧪 Herramienta</span><h1>Calculadora de disponibilidad</h1><p class="sub">Escribe un porcentaje y mira, paso por paso, cuánto tiempo puede estar caído un servicio en un año. Úsala para revisar tus cuentas, no para saltártelas.</p></header><div class="displab czf"><label>Disponibilidad prometida (%)<input class="ti dx" inputmode="decimal" value="99.9" autocomplete="off"></label><div class="dl3 dsteps"></div></div><p class="take"><b>Truco:</b> siempre son los mismos 4 pasos. Si los entiendes aquí, los puedes hacer en tu cuaderno con cualquier número.</p></article>'}
function dispInit(d){var x=d.querySelector(".dx"),o=d.querySelector(".dsteps");
 function f(v,k){return Number(v.toFixed(k==null?4:k)).toLocaleString("es-MX",{maximumFractionDigits:k==null?4:k})}
 function go(){var p=parseFloat(String(x.value).replace(",","."));if(!(p>=0&&p<=100)){o.innerHTML='<div>Escribe un número entre 0 y 100, por ejemplo 99.9 (sin el signo %).</div>';return}
  var no=100-p,dec=no/100,h=8760*dec,m=h*60;
  o.innerHTML='<div><span class="dh">Paso 1 · Horas de un año</span>365 días × 24 horas = <b>8,760 h</b><i>Es todo el tiempo que el servicio debería funcionar.</i></div>'+
  '<div><span class="dh">Paso 2 · ¿Qué parte NO funciona?</span>100 % − '+f(p)+' % = <b>'+f(no)+' %</b><i>Lo que falta para llegar a 100 % es el tiempo caído.</i></div>'+
  '<div><span class="dh">Paso 3 · Pasa el porcentaje a decimal</span>'+f(no)+' ÷ 100 = <b>'+f(dec,6)+'</b><i>«Por ciento» significa «de cada 100», por eso se divide entre 100.</i></div>'+
  '<div><span class="dh">Paso 4 · Multiplica</span>8,760 × '+f(dec,6)+' = <span class="dres">'+f(h,2)+' horas al año</span><i>Eso es lo máximo que puede estar caído.</i></div>'+
  '<div><span class="dh">Extra · En minutos o días</span>'+f(h,2)+' h × 60 = <b>'+f(m,1)+' minutos</b>'+(h>=24?' · '+f(h,2)+' h ÷ 24 = <b>'+f(h/24,2)+' días</b>':'')+'<i>Para minutos se multiplica por 60; para días se divide entre 24.</i></div>'}
 x.oninput=go;go()}
'''

ANIM_JS = r'''
(function(){var s=document.createElement("style");s.textContent=[
".an{position:relative;border:1.5px solid var(--line);border-radius:14px;background:var(--card);padding:12px 12px 10px;margin:12px 0;overflow:hidden;font-size:14px}",
".an .anh{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12.5px;font-weight:700;color:var(--pri);margin-bottom:8px}",
".an .anp{border:1px solid var(--line);background:var(--card);border-radius:8px;font:inherit;font-size:12px;padding:3px 9px;cursor:pointer;color:inherit}",
".an.pz *{animation-play-state:paused!important}",
".an .sw{display:grid}.an .sw>*{grid-area:1/1}",
".an .pa{animation:anA 8s infinite}.an .pb{opacity:0;animation:anB 8s infinite}",
".an .cap{margin-top:8px;font-weight:600;text-align:center;min-height:2.6em;display:grid;align-items:center}",
".an .bx{border:1.5px solid var(--line);border-radius:10px;padding:6px 8px;background:color-mix(in srgb,var(--pri) 5%,transparent);text-align:center}",
".an .mono{font-family:Consolas,monospace;word-break:break-all;font-size:12.5px}",
".an .row{display:grid;grid-template-columns:1fr auto 1fr;gap:6px;align-items:center}",
".an .ar{position:relative;width:46px;height:30px;display:grid;place-items:center;font-size:22px}",
".an .spin{display:inline-block;animation:anSpin 2s linear infinite}",
".an .dot{position:absolute;top:50%;width:9px;height:9px;margin-top:-4px;border-radius:50%;background:var(--pri);animation:anFlow 4s infinite}",
".an mark{background:#ffe14d;color:#111;border-radius:3px;padding:0 1px}",
".an .ok{color:#1d8a4a}.an .bad{color:#c8323a}",
".an .chip{display:inline-block;background:#ffe14d;color:#111;border-radius:6px;padding:0 5px;font-family:Consolas,monospace;opacity:0;animation:anDrop 8s infinite}",
".an .trk{position:relative;height:58px;margin:4px 0}",
".an .trk .end{position:absolute;top:8px;font-size:26px;text-align:center;width:54px;line-height:1.1}.an .trk .end small{display:block;font-size:11px;font-weight:600}",
".an .mv{position:absolute;top:12px;font-size:24px;opacity:0}",
".an .mvA{animation:anMvA 8s infinite}.an .mvB{animation:anMvB 8s infinite}",
".an .dv{position:absolute;left:46%;top:-2px;font-size:22px;opacity:0;animation:anDv 8s infinite}",
".an .okA{opacity:0;animation:anOkA 8s infinite}.an .okB{opacity:0;animation:anOkB 8s infinite}",
".an .cols{display:grid;grid-template-columns:1fr 1fr;gap:10px}",
".an .col{border:1.5px dashed var(--line);border-radius:10px;padding:8px;text-align:center}",
".an .disk{display:inline-block;margin:3px;padding:4px 7px;border-radius:8px;border:1.5px solid var(--line);background:var(--card)}",
".an .d1{animation:anFail 8s infinite}",
".an .svc{font-weight:700;margin-bottom:6px}",
".an .ph{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}",
".an .ph>div{border:1.5px solid var(--line);border-radius:9px;padding:6px 4px;text-align:center;font-size:12.5px;line-height:1.25;animation:anHl 8s infinite}",
".an .ph>div:nth-child(2),.an .caps>span:nth-child(2){animation-delay:2s}.an .ph>div:nth-child(3),.an .caps>span:nth-child(3){animation-delay:4s}.an .ph>div:nth-child(4),.an .caps>span:nth-child(4){animation-delay:6s}",
".an .caps>span{opacity:0;animation:anCap 8s infinite}.an .caps>span:first-child{opacity:1}",
".an .tl{position:relative;height:92px;margin:4px 6px}",
".an .tl .ln{position:absolute;left:0;right:0;top:40px;height:3px;background:var(--line)}",
".an .tl .ic{position:absolute;top:22px;font-size:20px;transform:translateX(-50%)}",
".an .tl .lb{position:absolute;font-size:11.5px;font-weight:700;transform:translateX(-50%);white-space:nowrap}",
".an .tl .rpo{position:absolute;top:36px;height:11px;left:40%;width:30%;background:#c8323a;opacity:.75;transform-origin:right;transform:scaleX(0);animation:anRpo 10s infinite;border-radius:3px}",
".an .tl .rto{position:absolute;top:36px;height:11px;left:70%;width:26%;background:#1d8a4a;opacity:.8;transform-origin:left;transform:scaleX(0);animation:anRto 10s infinite;border-radius:3px}",
".an .tl .t1{opacity:0;animation:anT1 10s infinite}.an .tl .t2{opacity:0;animation:anT2 10s infinite}.an .tl .boom{opacity:0;animation:anBoom 10s infinite}",
".an .lay{position:relative;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;padding-top:30px}",
".an .lay>div{border:1.5px solid var(--line);border-radius:9px;padding:6px 2px;text-align:center;font-size:11.5px;line-height:1.2;position:relative}",
".an .lay .st{position:absolute;top:-22px;left:50%;transform:translateX(-50%);font-size:16px;opacity:0;color:#c8323a}",
".an .lay .s1{animation:anS1 8s infinite}.an .lay .s2{animation:anS2 8s infinite}.an .lay .s3{animation:anS3 8s infinite}",
".an .lay .l3{animation:anL3 8s infinite}",
".an .atk{position:absolute;top:0;left:0;font-size:22px;animation:anAtk 8s infinite}",
"@keyframes anA{0%,45%{opacity:1}50%,95%{opacity:0}100%{opacity:1}}",
"@keyframes anB{0%,45%{opacity:0}50%,95%{opacity:1}100%{opacity:0}}",
"@keyframes anSpin{to{transform:rotate(360deg)}}",
"@keyframes anFlow{0%{left:0;opacity:0}8%{opacity:1}40%{left:calc(100% - 9px);opacity:1}48%,100%{left:calc(100% - 9px);opacity:0}}",
"@keyframes anDrop{0%,45%{opacity:0;transform:translateY(-14px)}55%,95%{opacity:1;transform:none}100%{opacity:0}}",
"@keyframes anMvA{0%{left:56px;opacity:1}38%{left:calc(100% - 92px);opacity:1}44%,100%{left:calc(100% - 92px);opacity:0}}",
"@keyframes anMvB{0%,50%{left:56px;opacity:0}52%{left:56px;opacity:1}88%{left:calc(100% - 92px);opacity:1}94%,100%{left:calc(100% - 92px);opacity:0}}",
"@keyframes anDv{0%,56%{opacity:0}60%,92%{opacity:1}96%,100%{opacity:0}}",
"@keyframes anOkA{0%,37%{opacity:0}40%,47%{opacity:1}50%,100%{opacity:0}}",
"@keyframes anOkB{0%,87%{opacity:0}90%,97%{opacity:1}100%{opacity:0}}",
"@keyframes anFail{0%,45%{background:var(--card);opacity:1}55%,95%{background:#f6c9cc;opacity:.55}100%{background:var(--card);opacity:1}}",
"@keyframes anHl{0%,24%{background:var(--pri);color:var(--on);border-color:var(--pri)}25%,100%{background:none;color:inherit}}",
"@keyframes anCap{0%,24%{opacity:1}25%,100%{opacity:0}}",
"@keyframes anRpo{0%,18%{transform:scaleX(0)}40%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}",
"@keyframes anRto{0%,48%{transform:scaleX(0)}78%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}",
"@keyframes anBoom{0%,12%{opacity:0;transform:translateX(-50%) scale(.4)}18%,92%{opacity:1;transform:translateX(-50%) scale(1)}100%{opacity:0}}",
"@keyframes anT1{0%,30%{opacity:0}40%,92%{opacity:1}100%{opacity:0}}",
"@keyframes anT2{0%,66%{opacity:0}78%,92%{opacity:1}100%{opacity:0}}",
"@keyframes anAtk{0%{left:0;opacity:1}18%{left:2%}38%{left:22%}58%,92%{left:31%;opacity:1}100%{left:31%;opacity:0}}",
"@keyframes anS1{0%,16%{opacity:0}20%,92%{opacity:1}100%{opacity:0}}",
"@keyframes anS2{0%,36%{opacity:0}40%,92%{opacity:1}100%{opacity:0}}",
"@keyframes anS3{0%,56%{opacity:0}60%,92%{opacity:1}100%{opacity:0}}",
"@keyframes anL3{0%,56%{background:none}60%,92%{background:color-mix(in srgb,#1d8a4a 18%,transparent);border-color:#1d8a4a}100%{background:none}}",
"@media (prefers-reduced-motion:reduce){.an *{animation:none!important}}",
"@media print{.an{display:none}}"].join("");document.head.appendChild(s)})();
function AN(k){var t={
 hash:['Animación · el hash como huella','<div class="row"><div class="bx sw"><span class="pa">Ana López · alergia a la penicilin<b>a</b></span><span class="pb">Ana López · alergia a la penicilin<mark>A</mark></span></div><div class="ar"><span class="dot"></span><span class="spin">⚙️</span></div><div class="bx mono sw"><span class="pa">5c1e9a0f…7b2d</span><span class="pb bad">d83b72c4…19ae</span></div></div><div class="cap sw"><span class="pa">Mismo texto → <span class="ok">siempre la misma huella</span></span><span class="pb">Cambió UNA letra → <span class="bad">huella totalmente distinta</span></span></div>'],
 sal:['Animación · qué hace la sal','<div style="display:grid;gap:8px"><div class="row"><div class="bx">👩 Recepción<br><b>123456</b> <span class="chip">a7f2</span></div><div class="ar"><span class="dot"></span><span class="spin">⚙️</span></div><div class="bx mono sw"><span class="pa bad">8d969e…c92</span><span class="pb ok">3c9e1b…a40</span></div></div><div class="row"><div class="bx">👨‍⚕️ Dentista<br><b>123456</b> <span class="chip">91bd</span></div><div class="ar"><span class="dot"></span><span class="spin">⚙️</span></div><div class="bx mono sw"><span class="pa bad">8d969e…c92</span><span class="pb ok">e04a77…5d1</span></div></div></div><div class="cap sw"><span class="pa">Sin sal: misma contraseña → <span class="bad">mismo hash</span> (el atacante lo reconoce)</span><span class="pb">Con sal (amarillo): <span class="ok">cada uno tiene un hash distinto</span></span></div>'],
 hmac:['Animación · HMAC en el camino','<div class="trk"><div class="end" style="left:0">🧪<small>Laboratorio</small></div><div class="end" style="right:0">🏥<small>Clínica</small></div><span class="mv mvA">✉️🔏</span><span class="mv mvB">✉️✏️</span><span class="dv">😈</span><span class="mv okA" style="right:58px;top:8px">✅</span><span class="mv okB" style="right:58px;top:8px">❌</span></div><div class="cap sw"><span class="pa">Llega igual → el HMAC coincide → <span class="ok">se acepta</span></span><span class="pb">Alguien lo cambió en el camino → el HMAC ya no coincide → <span class="bad">se rechaza</span></span></div>'],
 raid:['Animación · punto único de falla vs. redundancia','<div class="cols"><div class="col"><div class="svc sw"><span class="pa ok">🟢 Agenda funciona</span><span class="pb bad">🔴 Agenda caída</span></div>Un solo disco<br><span class="disk d1">💽 Disco</span></div><div class="col"><div class="svc ok">🟢 Agenda funciona</div>RAID 1 (espejo)<br><span class="disk d1">💽 Disco 1</span><span class="disk">💽 Disco 2</span></div></div><div class="cap sw"><span class="pa">Los dos funcionan… mientras no falle nada</span><span class="pb">Falla un disco: sin repuesto <span class="bad">todo se cae</span>; con RAID 1 <span class="ok">sigue funcionando</span></span></div>'],
 inc:['Animación · las 4 fases, una tras otra','<div class="ph"><div>📋<br>Preparación</div><div>🔎<br>Detección y análisis</div><div>🧯<br>Contener y recuperar</div><div>📚<br>Lecciones aprendidas</div></div><div class="cap sw caps"><span>Antes: respaldos, plan y responsables listos</span><span>Se dan cuenta: archivos raros, ¿qué equipos están afectados?</span><span>Desconectan equipos, eliminan el virus y restauran respaldos</span><span>Revisan cómo entró y capacitan al personal</span></div>'],
 rpo:['Animación · RPO y RTO en la línea del tiempo','<div class="tl"><div class="ln"></div><span class="ic" style="left:10%">💾</span><span class="lb" style="left:10%;top:2px">respaldo</span><span class="ic" style="left:40%">💾</span><span class="lb" style="left:40%;top:2px">último respaldo</span><span class="rpo"></span><span class="ic boom" style="left:70%">💥</span><span class="lb boom" style="left:70%;top:2px">desastre</span><span class="rto"></span><span class="ic t2" style="left:96%">✅</span><span class="lb t1 bad" style="left:55%;top:58px">RPO: datos perdidos</span><span class="lb t2 ok" style="left:83%;top:58px">RTO: tiempo para volver</span></div><div class="cap">Rojo: lo que se pierde (desde el último respaldo hacia atrás) · Verde: lo que tardas en volver a funcionar</div>'],
 capas:['Animación · defensa en profundidad','<div class="lay"><span class="atk">🦹</span><div>👥<br>Capacitación<span class="st s1">✖</span></div><div>🧱<br>Firewall<span class="st s2">✖</span></div><div class="l3">🛡️<br>Antivirus<span class="st s3">🛑</span></div><div>🔐<br>Cifrado</div><div>🗄️<br>Datos</div></div><div class="cap">Un correo falso engaña al empleado (✖) y pasa el firewall (✖), pero el antivirus lo detiene (🛑). Si también fallara, los datos siguen cifrados.</div>']
}[k];return '<div class="an exn"><div class="anh"><span>▶ '+t[0]+'</span><button class="anp" type="button" onclick="var a=this.closest(\'.an\');a.classList.toggle(\'pz\');this.textContent=a.classList.contains(\'pz\')?\'▶ Seguir\':\'⏸ Pausar\'">⏸ Pausar</button></div>'+t[1]+'</div>'}
'''


def an(k):
    return Js(f'AN({j(k)})')


ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".hashlab"))hashInit(d);\n if(d.querySelector(".displab"))dispInit(d);\n'),
    ('catch(e){ST={}}\n', 'catch(e){ST={}}\nST=mig22(ST);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏥', '¿Se puede confiar en la información?', 'De qué trata este R.A. y cómo usar este material', body(
    sp('En palabras sencillas', 'En el R.A. 2.1 viste cómo mantener la información <b>en secreto</b>. Ahora vas a aprender tres cosas nuevas:<br>1) cómo comprobar que <b>nadie cambió</b> la información (integridad),<br>2) cómo lograr que un servicio <b>siga funcionando</b> aunque algo falle (disponibilidad) y<br>3) cómo <b>defender</b> las computadoras, los servidores y la red.'),
    ex('Caso de las lecciones: Clínica dental Sonríe', 'Una clínica pequeña con expedientes de pacientes, una agenda de citas en internet y una caja para cobrar. Si alguien cambia la alergia de un paciente, es peligroso. Si la agenda no abre, pierden pacientes. Vamos a protegerla paso a paso.'),
    bk('Cómo estudiar con este material', '<b>1.</b> Lee la lección con calma (un tema por pantalla).<br><b>2.</b> Cuando veas «Ejemplo resuelto», presiona <b>Siguiente paso</b> y lee el <b>¿por qué?</b> de cada paso.<br><b>3.</b> Haz la actividad. Si fallas, lee la explicación y la <b>pista</b>, y vuelve a intentarlo: equivocarse aquí no baja tu calificación.'),
    bk('¿Se te olvidó algo de antes?', 'No pasa nada. Las siguientes pantallas son un <b>repaso</b> de lo que necesitas de los R.A. anteriores.'),
    bk('Al final', 'Elaboras un <b>reporte</b> con la organización que te asigna la plataforma en la actividad de evaluación. Las 3 prácticas te dejan casi todo listo.')),
    'Integridad = que no cambie · Disponibilidad = que funcione cuando se necesita · Defensa = varias capas de protección.')
c.L('🔺', 'Repaso 1: los tres pilares de la seguridad', 'Lo viste en el R.A. 2.1 · Lo vas a usar en todo este R.A.', body(
    sp('En palabras sencillas', 'Proteger la información significa cuidar <b>tres cosas</b> al mismo tiempo. Se les llama los tres pilares (o la tríada CID).'),
    r3([['🤫', 'Confidencialidad', 'Que solo la vea quien debe. Ejemplo: tus calificaciones solo las ves tú y tu profe.'],
        ['✅', 'Integridad', 'Que nadie la cambie sin permiso. Ejemplo: nadie puede subirse la calificación.'],
        ['⏱️', 'Disponibilidad', 'Que funcione cuando la necesitas. Ejemplo: la plataforma abre el día del examen.']]),
    bk('Truco para no confundirlos', 'Hazte tres preguntas: ¿la <b>vio</b> alguien que no debía? → confidencialidad. ¿La <b>cambiaron</b>? → integridad. ¿<b>No funciona</b> o no se puede usar? → disponibilidad.'),
    ana('Piensa en tu celular', 'Si alguien lee tus chats: confidencialidad. Si alguien manda mensajes como si fueras tú: integridad. Si se te descarga la batería: disponibilidad.')),
    '¿La vieron? → confidencialidad · ¿La cambiaron? → integridad · ¿No funciona? → disponibilidad.')
c.A('🔺', '¿Qué pilar se afecta?', 'Elige el pilar que se daña en cada situación de la clínica. Usa el truco de las tres preguntas.', [
    ['Alguien cambia la alergia de un paciente en su expediente', 'Integridad', 'El dato fue <b>cambiado</b> sin permiso: se dañó la integridad. Nadie lo vio de más ni se cayó el sistema.'],
    ['La agenda en línea no abre en todo el día', 'Disponibilidad', 'El servicio <b>no funciona</b> cuando se necesita: es disponibilidad.'],
    ['Un empleado publica radiografías de un paciente', 'Confidencialidad', 'Información privada la <b>vio</b> gente que no debía: confidencialidad.'],
    ['Un virus modifica los montos de los cobros', 'Integridad', 'Los montos <b>cambiaron</b>: integridad. Que sea un virus no importa, lo que importa es qué le pasó al dato.'],
    ['Se va la luz y el servidor no enciende', 'Disponibilidad', 'El sistema <b>no se puede usar</b>: disponibilidad.'],
], '¿La vieron? → Confidencialidad · ¿La cambiaron? → Integridad · ¿No funciona? → Disponibilidad.', ['Confidencialidad', 'Integridad', 'Disponibilidad'])
c.L('🖧', 'Repaso 2: equipos, servidores y redes', 'Lo viste en el R.A. 1.2 · Palabras que aparecen en los bloques B y C', body(
    bk('Host (equipo)', 'Cualquier aparato conectado a la red: una PC, una laptop, un celular, una impresora. «Host» solo es la palabra técnica para «equipo».'),
    bk('Servidor', 'Una computadora que <b>da un servicio a muchos</b>: guarda la agenda de citas, la página web o los archivos de todos. Si el servidor se apaga, todos se quedan sin el servicio.'),
    bk('Red', 'Los cables, el wifi, el módem y el router que <b>unen</b> a los equipos entre sí y con internet.'),
    bk('Internet y proveedor', 'El proveedor (Telmex, Totalplay, Izzi…) es la empresa que te da la salida a internet. Si su servicio falla, toda la red se queda sin internet.'),
    ana('Piensa en una escuela', 'Cada alumno es un <b>host</b>; la dirección que reparte avisos a todos es el <b>servidor</b>; los pasillos que conectan los salones son la <b>red</b>.'),
    ex('En la clínica', 'Hosts: la PC de recepción y la laptop del dentista. Servidor: la computadora donde vive la agenda. Red: el módem, el router y el wifi.')),
    'Host = un equipo · Servidor = el equipo que atiende a todos · Red = lo que los conecta.')
c.L('🔐', 'Repaso 3: cifrar y las claves', 'Lo viste en el R.A. 2.1 · Lo necesitas para el bloque A', body(
    sp('Cifrar', 'Convertir un mensaje en algo que no se entiende, usando una <b>clave</b>. Quien tiene la clave puede <b>regresarlo</b> a su forma original (descifrar). Cifrar sirve para guardar <b>secretos</b>.'),
    bk('Clave simétrica', 'Una sola clave para cerrar y abrir, como un candado con llave que copias para tu amigo.'),
    bk('Clave pública y clave privada', 'Un par de claves que van juntas. La <b>pública</b> se le da a todo el mundo; la <b>privada</b> solo la tiene su dueño y nunca se comparte. Lo que hace una, solo lo comprueba o lo deshace la otra.'),
    ana('Piensa en un buzón', 'Cualquiera puede meter cartas por la ranura (clave pública), pero solo el dueño tiene la llave para abrirlo (clave privada).'),
    warn('Lo nuevo de este R.A.', 'En la siguiente sección verás el <b>hash</b>. Se parece al cifrado, pero <b>no tiene regreso</b>: no se usa para guardar secretos, sino para descubrir si algo cambió.')),
    'Cifrar = esconder y poder regresar · Clave pública = para todos · Clave privada = solo para su dueño.')
c.L('➗', 'Repaso 4: porcentajes sin miedo', 'Matemáticas que vas a usar en el bloque B', body(
    sp('En palabras sencillas', '«Por ciento» quiere decir «<b>de cada 100</b>». 25 % es 25 de cada 100. Para hacer cuentas, el porcentaje se pasa a decimal <b>dividiendo entre 100</b>.'),
    bk('Pasar a decimal', '50 % → 50 ÷ 100 = <b>0.5</b> · 1 % → 1 ÷ 100 = <b>0.01</b> · 0.1 % → 0.1 ÷ 100 = <b>0.001</b>. Truco: dividir entre 100 es recorrer el punto decimal <b>dos lugares a la izquierda</b>.'),
    px('Ejemplo resuelto: ¿cuánto es el 1 % de 8,760?', [
        paso('Escribe el porcentaje como decimal: 1 % = 0.01', 'Las calculadoras y las cuentas no usan el signo %; por eso lo convertimos en número dividiendo entre 100.'),
        paso('Multiplica la cantidad por el decimal: 8,760 × 0.01', '«El 1 % DE 8,760» se traduce como «0.01 POR 8,760». En matemáticas, «de» casi siempre significa multiplicar.'),
        paso('Resultado: 87.6', 'Revisa si tiene sentido: el 1 % es una parte muy pequeña, así que el resultado debe ser mucho menor que 8,760. ✔'),
    ]),
    bk('¿Qué porcentaje es?', 'Si de 100 horas funcionó 96: 96 ÷ 100 = 0.96 → × 100 = <b>96 %</b>. Se divide la parte entre el total y se multiplica por 100.')),
    'Porcentaje → decimal: ÷ 100 · «El X % de» = multiplicar por ese decimal.')
c.T('➗', 'Practica los porcentajes', 'Escribe solo el número (usa punto decimal). Si fallas, abre la pista: te dice el primer paso.', [
    ['Escribe 1 % como decimal', '0.01', '1 ÷ 100 = 0.01 (el punto se recorre dos lugares a la izquierda).', 'Divide 1 entre 100.', 'm', 0.0001],
    ['Escribe 0.1 % como decimal', '0.001', '0.1 ÷ 100 = 0.001.', 'Divide 0.1 entre 100: recorre el punto dos lugares a la izquierda.', 'm', 0.00001],
    ['Si algo funciona el 99 % del tiempo, ¿qué porcentaje NO funciona?', '1', '100 − 99 = 1 %. Lo que falta para llegar a 100 es lo que no funciona.', 'Resta a 100 el porcentaje que sí funciona.', 'm', 0.001],
    ['¿Cuánto es el 10 % de 200?', '20', '10 % = 0.1 → 200 × 0.1 = 20.', 'Pasa 10 % a decimal y multiplica por 200.', 'm', 0.01],
    ['¿Cuántas horas tiene un año? (365 días de 24 horas)', '8760', '365 × 24 = 8,760 horas. Este número lo vas a usar mucho.', 'Multiplica los días por las horas de cada día.', 'm', 0.5],
], 'Porcentaje a decimal: divide entre 100. «El X % de» algo: multiplica.', 'm')
s0_end = c.mark() - 1

# ───────────────────────── A · Integridad ─────────────────────────
a0 = c.mark()
c.L('🧬', 'Hash: la huella digital de los datos', 'Bloque A · Controles de integridad', body(
    sp('En palabras sencillas', 'Un <b>hash</b> es una fórmula matemática que convierte cualquier dato (una palabra, un archivo, una película) en un <b>código corto de tamaño fijo</b>. A ese código le decimos su <b>huella</b>. Con SHA-256 la huella siempre mide 64 caracteres.'),
    an('hash'),
    bk('Regla 1 · Siempre igual', 'El mismo dato <b>siempre</b> da la misma huella. <i>Por eso podemos comparar.</i>'),
    bk('Regla 2 · Cambia todo', 'Si cambia <b>una sola letra</b>, la huella cambia casi completa. <i>Por eso se nota cualquier cambio, por pequeño que sea.</i>'),
    bk('Regla 3 · Sin regreso', 'Con la huella <b>no</b> se puede reconstruir el dato original. <i>Por eso es distinto de cifrar: el cifrado sí tiene regreso con la clave.</i>'),
    ana('Piensa en tu huella dactilar', 'Te identifica, pero con tu huella nadie puede dibujar tu cara. O en un licuado: no puedes volver a sacar el plátano entero.'),
    warn('Algoritmos viejos', 'MD5 y SHA-1 ya no son seguros (se les encontraron fallas). Hoy se usa SHA-256 o superior.')),
    'Mismo dato → misma huella · Una letra distinta → huella totalmente distinta · No tiene regreso.')
c.L('🔎', 'Ejemplo resuelto: descubrir si alguien cambió un expediente', 'Bloque A · El hash en acción', body(
    sp('La situación', 'La clínica quiere saber si alguien modifica a escondidas el expediente de Ana. Mira cómo lo resuelve con un hash.'),
    px('Paso a paso', [
        paso('El lunes calculan la huella del expediente y la anotan en un lugar seguro.', 'Necesitamos una huella «original» para comparar después. Si no la guardamos, no hay contra qué comparar.'),
        paso('El viernes vuelven a calcular la huella del mismo expediente.', 'Por la regla 1, si el expediente sigue igual, la huella tiene que salir exactamente igual.'),
        paso('Comparan las dos huellas carácter por carácter (o solo las primeras 8 letras).', 'Por la regla 2, si alguien cambió aunque sea una coma, la huella sería casi totalmente distinta; con ver el inicio basta para notarlo.'),
        paso('Si son iguales: el expediente no cambió. Si son distintas: alguien lo modificó y hay que revisar.', 'El hash no dice QUÉ cambió, solo SI cambió. Para saber qué cambió se revisan los respaldos y las bitácoras (las verás más adelante).'),
    ]),
    bk('¿Dónde más se usa?', 'Al descargar programas: la página publica la huella del archivo; tú calculas la del archivo descargado y, si coinciden, sabes que nadie lo alteró en el camino.')),
    'El hash responde «¿cambió o no cambió?». Para eso hay que guardar la huella original.')
c.raw('pHash()')
c.A('🧬', '¿Qué pasa con la huella?', 'Usa lo que viste en el laboratorio de hash y las tres reglas.', [
    ['Calculo el hash de «Hola» dos veces', 'Sale la misma huella', 'Regla 1: el mismo dato siempre produce la misma huella.'],
    ['Cambio «Hola» por «hola»', 'Sale una huella totalmente distinta', 'Regla 2: una mayúscula ya es un carácter distinto, y basta uno para que cambie todo.'],
    ['Tengo solo la huella y quiero el texto original', 'No se puede obtener', 'Regla 3: el hash es de un solo sentido, no tiene regreso.'],
    ['Hago el hash de un archivo de 2 GB con SHA-256', 'Sale una huella de 64 caracteres', 'El tamaño de la huella es fijo: no importa si el dato es chico o enorme.'],
], 'Repasa las 3 reglas: siempre igual · una letra cambia todo · sin regreso. Y la huella SHA-256 siempre mide 64.', ['Sale la misma huella', 'Sale una huella totalmente distinta', 'No se puede obtener', 'Sale una huella de 64 caracteres'])
c.L('🔑', '¿Cómo se guardan las contraseñas?', 'Bloque A · Antes de ver la técnica salting', body(
    sp('El problema', 'Cuando creas una cuenta, la página tiene que guardar algo para reconocerte después. Si guardara tu contraseña <b>tal cual</b> y alguien robara la base de datos, tendría las contraseñas de todos.'),
    bk('La solución: guardar la huella', 'La página guarda el <b>hash</b> de tu contraseña, no la contraseña. Cuando inicias sesión, calcula el hash de lo que escribiste y lo compara con el guardado. <i>Si coinciden, escribiste bien. Y como el hash no tiene regreso, el ladrón no puede ver tu contraseña.</i>'),
    ex('Por eso…', 'Una página seria <b>nunca</b> te puede enviar tu contraseña por correo si la olvidas: ella tampoco la conoce. Solo te deja crear una nueva.'),
    warn('Pero queda un hueco', 'Si dos personas usan «123456», sus hashes salen <b>iguales</b> (regla 1). Los atacantes tienen listas gigantes con los hashes de las contraseñas más comunes. Para tapar ese hueco existe la <b>sal</b>.')),
    'Se guarda el hash de la contraseña, nunca la contraseña.')
c.L('🧂', 'La técnica salting', 'Bloque A · Guardar contraseñas de forma segura', body(
    sp('En palabras sencillas', 'La <b>sal</b> es un valor al azar, <b>distinto para cada usuario</b>, que se pega a la contraseña <b>antes</b> de calcular el hash.'),
    an('sal'),
    px('Ejemplo resuelto: dos personas con la misma contraseña', [
        paso('La recepcionista y el dentista eligen la contraseña «123456».', 'Pasa en la vida real: mucha gente usa contraseñas iguales sin saberlo.'),
        paso('El sistema le da a cada uno una sal distinta: «a7f2» a la recepcionista y «91bd» al dentista.', 'La sal se genera al azar para que nunca se repita entre usuarios.'),
        paso('Calcula el hash de «a7f2123456» y el de «91bd123456».', 'Como lo que entra al hash ya es distinto, por la regla 2 las huellas salen totalmente distintas.'),
        paso('Guarda la sal y el hash de cada uno. La contraseña se olvida.', 'La sal no es secreta: se necesita para repetir el cálculo al iniciar sesión. Lo que nunca se guarda es la contraseña.'),
        paso('Resultado: el atacante ve dos hashes diferentes y sus listas de hashes comunes ya no le sirven.', 'Esas listas se hicieron sin sal; con la sal, el atacante tendría que empezar de cero para cada usuario.'),
    ]),
    ana('Piensa en…', 'Dos personas piden el mismo platillo, pero el cocinero le pone a cada uno un ingrediente secreto distinto: ya no saben igual.'),
    bk('En la vida real', 'Se usan algoritmos lentos a propósito, como <b>bcrypt</b> o <b>Argon2</b>, que ya incluyen la sal y hacen más difícil adivinar.')),
    'Contraseña + sal → hash. Se guardan la sal y el hash; la contraseña no.')
c.O('🧂', 'Ordena: guardar una contraseña', 'Pon en orden lo que hace el sistema cuando creas tu contraseña. Piensa: ¿qué se necesita primero para poder hacer lo siguiente?', [
    ['El usuario escribe su contraseña nueva', 'Sin contraseña no hay nada que proteger: todo empieza aquí.'],
    ['El sistema genera una sal aleatoria para ese usuario', 'La sal tiene que existir antes de calcular el hash, porque se pega a la contraseña.'],
    ['Junta la sal con la contraseña y calcula el hash', 'El hash se calcula sobre sal + contraseña.'],
    ['Guarda la sal y el hash; la contraseña se descarta', 'Solo se guarda lo necesario para comparar después. La contraseña nunca se guarda.'],
    ['Al iniciar sesión repite el cálculo y compara los hashes', 'Esto pasa después, cada vez que entras. Si los hashes coinciden, la contraseña es correcta.'],
], 'Orden: escribir → generar sal → calcular hash → guardar → comparar al entrar.')
c.L('🔏', 'HMAC: hash con clave secreta', 'Bloque A · Comprobar quién lo envió', body(
    sp('El problema', 'Un hash solo dice si algo cambió. Pero un tramposo podría cambiar el mensaje <b>y</b> calcular la huella nueva. ¿Cómo sabe la clínica que el mensaje sí viene del laboratorio?'),
    sp('La solución: HMAC', '<b>HMAC</b> es un hash que se calcula usando también una <b>clave secreta</b> que solo conocen el emisor y el receptor. Sin la clave, nadie puede fabricar un HMAC correcto.'),
    an('hmac'),
    px('Ejemplo resuelto: el laboratorio manda resultados', [
        paso('El laboratorio y la clínica acuerdan una clave secreta, en persona.', 'La clave no debe viajar por internet; si alguien la roba, podría fabricar mensajes falsos.'),
        paso('El laboratorio calcula el HMAC del resultado usando la clave y lo envía junto con el resultado.', 'El HMAC funciona como un sello que solo puede hacer quien tiene la clave.'),
        paso('La clínica recibe el mensaje y calcula el HMAC con su copia de la clave.', 'Si el mensaje no cambió y lo mandó el laboratorio, el HMAC calculado debe ser idéntico al recibido.'),
        paso('Si coinciden, lo acepta. Si no, lo rechaza.', 'Un HMAC distinto significa que el mensaje fue alterado o que lo mandó alguien que no conoce la clave.'),
    ]),
    ana('Piensa en…', 'Un sobre sellado con lacre y tu sello personal: si alguien lo abre, se nota, y solo tú tienes ese sello.')),
    'Hash = ¿cambió? · HMAC = ¿cambió? + ¿lo mandó quien tiene la clave?')
c.L('✍️', 'Firmas digitales y certificados', 'Bloque A · Identidad en internet', body(
    sp('Firma digital', 'Se hace con la <b>clave privada</b> del que firma (solo él la tiene) y cualquiera la comprueba con su <b>clave pública</b>. Como solo el dueño tiene la privada, nadie más pudo firmar.'),
    bk('Qué asegura', '<b>Integridad</b> (no cambió) + <b>autenticidad</b> (sí es de quien dice) + <b>no repudio</b> (el que firmó no puede decir «yo no fui»).'),
    bk('Diferencia con HMAC', 'En HMAC los dos comparten la misma clave, así que cualquiera de los dos pudo hacerlo. En la firma digital solo el dueño tiene la clave privada: por eso hay no repudio.'),
    sp('Certificado digital', 'Un documento que emite una <b>autoridad certificadora</b> (una empresa en la que todos confían) y que dice: «esta clave pública es de esta persona o de esta página». Es lo que hay detrás del <b>candado 🔒</b> de las páginas HTTPS.'),
    ana('Piensa en…', 'La firma es tu firma en papel; el certificado es tu INE: una autoridad confiable garantiza que esa firma es tuya.'),
    ex('En México', 'La <b>e.firma</b> del SAT es una firma digital con certificado, y las facturas electrónicas (CFDI) van firmadas digitalmente.')),
    'Clave privada para firmar, clave pública para comprobar · El certificado dice de quién es la clave pública.')
c.L('🗂️', '¿Qué es una base de datos?', 'Bloque A · Antes de hablar de su integridad', body(
    sp('En palabras sencillas', 'Una <b>base de datos</b> es un conjunto de <b>tablas</b> donde un sistema guarda su información en orden. Se parece mucho a una hoja de Excel.'),
    bk('Tabla', 'Un tema: «Pacientes», «Citas», «Pagos».'),
    bk('Registro (fila)', 'Un elemento de la tabla: un paciente, una cita.'),
    bk('Campo (columna)', 'Un dato de cada registro: nombre, teléfono, fecha.'),
    ex('En la clínica', 'Tabla Pacientes: <b>Expediente 101</b> · Ana López · 4421234567. Tabla Citas: Cita 55 · <b>Expediente 101</b> · 20-nov 10:00. El número de expediente une las dos tablas.')),
    'Base de datos = tablas · Tabla = filas (registros) y columnas (campos).')
c.L('🗃️', 'Integridad en bases de datos', 'Bloque A · Reglas para que los datos guardados sean correctos', body(
    bk('Llave primaria', 'Un número que <b>no se puede repetir</b>, como el número de expediente. <i>¿Por qué? Para que nunca haya dos pacientes confundidos con el mismo número.</i>'),
    bk('Llave foránea', 'Un campo que <b>apunta</b> a otra tabla, como el expediente dentro de cada cita. <i>¿Por qué? Para que no se pueda agendar una cita a un paciente que no existe.</i>'),
    bk('Validaciones', 'Reglas como «el teléfono lleva 10 dígitos» o «la fecha de nacimiento no puede ser del futuro». <i>¿Por qué? Para que no entren datos imposibles por error.</i>'),
    bk('Transacciones', '<b>Todo o nada</b>: al cobrar se guarda el pago y se marca la cita como pagada; si una de las dos falla, no se guarda ninguna. <i>¿Por qué? Para que no quede un pago sin cita o una cita pagada sin pago.</i>'),
    bk('Respaldos y bitácoras', 'El respaldo es una copia para regresar a como estaba; la bitácora es un registro de quién cambió qué y cuándo.')),
    'Una base de datos también se protege con reglas, no solo con contraseñas.')
c.A('🧰', '¿Qué control de integridad usas?', 'Elige la herramienta para cada necesidad. Primero pregúntate: ¿es una contraseña, un mensaje, una firma, una página o un dato guardado?', [
    ['Guardar las contraseñas de los empleados', 'Hash con sal', 'Las contraseñas se guardan como hash con sal, nunca tal cual.'],
    ['Que el laboratorio pruebe que el resultado no cambió y que lo envió él', 'HMAC', 'Es un mensaje entre dos que comparten una clave secreta: HMAC.'],
    ['Que el dentista firme recetas electrónicas sin poder negarlo después', 'Firma digital', '«Sin poder negarlo» = no repudio, y eso solo lo da la firma digital con la clave privada.'],
    ['Que los pacientes comprueben que la página de citas es la verdadera', 'Certificado digital', 'El certificado (el candado HTTPS) identifica a la página.'],
    ['Que no existan dos expedientes con el mismo número', 'Llave primaria', 'La llave primaria es la regla de «no se repite».'],
], 'Contraseñas → hash con sal · Mensaje con clave compartida → HMAC · Firmar sin negarlo → firma digital · Identidad de una página → certificado · Número que no se repite → llave primaria.',
    ['Hash con sal', 'HMAC', 'Firma digital', 'Certificado digital', 'Llave primaria'])
c.Z('🗃️', 'Completa las reglas de la base de datos', 'Elige la palabra correcta para cada regla de la clínica. Si dudas, regresa a la lección anterior.',
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
    'No se repite → llave primaria · Apunta a otra tabla → llave foránea · Todo o nada → transacción · Regla de formato → validación.')
a_end = c.mark() - 1

# ───────────────────────── B · Estándar ─────────────────────────
b0 = c.mark()
c.L('🛞', 'Disponibilidad y alta disponibilidad', 'Bloque B · Que el servicio no se detenga', body(
    sp('En palabras sencillas', '<b>Disponibilidad</b> es que el servicio funcione cuando se necesita. <b>Alta disponibilidad</b> es prepararlo para que <b>siga funcionando aunque algo se descomponga</b>.'),
    an('raid'),
    bk('Punto único de falla', 'Una pieza que, si falla, <b>detiene todo</b> porque no tiene repuesto: un solo disco, un solo servidor, un solo proveedor de internet. <i>Para encontrarlo pregúntate: «si esto se descompone, ¿se cae el servicio?». Si la respuesta es sí y solo hay uno, es un punto único de falla.</i>'),
    bk('Redundancia = tener repuesto', 'Poner dos (o más) de lo importante, para que si uno falla el otro siga.'),
    r3([['💽', 'RAID 1', 'Dos discos con la misma información (espejo). Si uno muere, el otro sigue.'],
        ['🔋', 'UPS (no-break)', 'Una batería que da luz unos minutos cuando se va la electricidad.'],
        ['🌐', 'Dos proveedores', 'Si se cae el internet de uno, se usa el del otro.']]),
    bk('Para servicios grandes', '<b>Clúster</b>: varios servidores que trabajan como uno; si uno falla, otro toma su lugar. <b>Balanceo de carga</b>: reparte las visitas entre varios servidores para que ninguno se sature.'),
    ana('Piensa en…', 'La llanta de refacción del coche: no evita que se ponche, pero te deja seguir.')),
    'Encuentra lo que es único y, si falla, detiene todo; luego ponle repuesto.')
c.L('9️⃣', 'Los «nueves» de la disponibilidad', 'Bloque B · Cómo se mide', body(
    sp('En palabras sencillas', 'La disponibilidad se mide en <b>porcentaje del tiempo que el servicio funciona</b>. Las empresas prometen «tres nueves» (99.9 %), «cuatro nueves» (99.99 %), etc. Lo que importa es cuánto tiempo puede estar <b>caído</b>.'),
    px('Ejemplo resuelto: ¿cuántas horas al año puede fallar un servicio de 99.9 %?', [
        paso('Paso 1 · Calcula las horas de un año: 365 × 24 = 8,760 h.', 'Es el tiempo total que el servicio debería funcionar. Siempre se parte de aquí.'),
        paso('Paso 2 · Calcula la parte que NO funciona: 100 − 99.9 = 0.1 %.', 'El 99.9 % es lo que SÍ funciona; nos preguntan por lo que falla, que es lo que falta para llegar a 100.'),
        paso('Paso 3 · Pasa ese porcentaje a decimal: 0.1 ÷ 100 = 0.001.', 'Para hacer la cuenta, el porcentaje se convierte a decimal dividiendo entre 100 (Repaso 4).'),
        paso('Paso 4 · Multiplica: 8,760 × 0.001 = 8.76 horas al año.', '«El 0.1 % de 8,760» significa multiplicar. Ese es el tiempo máximo caído.'),
        paso('Extra · Si te lo piden en minutos: 8.76 × 60 = 525.6 minutos.', 'Cada hora tiene 60 minutos, por eso se multiplica por 60. Si te lo piden en días, divide las horas entre 24.'),
    ]),
    bk('La tabla ya calculada', '99 % → 87.6 h (unos 3.65 días) · 99.9 % → 8.76 h · 99.99 % → 52.6 min · 99.999 % → unos 5 min al año.'),
    warn('Error común', 'Multiplicar 8,760 × 99.9. ¡Eso da el tiempo que SÍ funciona (y además sin pasar a decimal)! Primero resta a 100 y luego divide entre 100.')),
    'Horas del año (8,760) × (100 − disponibilidad) ÷ 100 = horas caídas.')
c.raw('pDisp()')
c.T('🧮', 'Calcula el tiempo fuera de servicio', 'Escribe solo el número. Haz los 4 pasos en tu cuaderno; puedes revisar con la calculadora de disponibilidad.', [
    ['Un servicio tiene 99 % de disponibilidad. ¿Cuántas horas puede estar caído al año?', '87.6', 'Paso 2: 100 − 99 = 1 %. Paso 3: 1 ÷ 100 = 0.01. Paso 4: 8,760 × 0.01 = 87.6 horas.', 'Lo que no funciona es 1 %. ¿Cuánto es el 1 % de 8,760?', 'm', 0.05],
    ['Con 99.9 %, ¿cuántas horas al año?', '8.76', '100 − 99.9 = 0.1 % → 0.001 → 8,760 × 0.001 = 8.76 horas.', 'Lo que no funciona es 0.1 %, que en decimal es 0.001.', 'm', 0.01],
    ['La agenda estuvo caída 4 horas de las 100 que debía funcionar esta semana. ¿Qué porcentaje estuvo disponible?', '96', 'Funcionó 100 − 4 = 96 horas. 96 ÷ 100 = 0.96 → × 100 = 96 %.', 'Primero resta las horas caídas a las 100; luego divide entre el total y multiplica por 100.', 'm', 0.05],
    ['Con 99.99 %, ¿cuántos minutos al año? (redondea a un decimal)', '52.6', '100 − 99.99 = 0.01 % → 0.0001 → 8,760 × 0.0001 = 0.876 h → 0.876 × 60 = 52.56 ≈ 52.6 minutos.', 'Saca primero las horas igual que antes y al final multiplica por 60.', 'm', 0.1],
], 'Los 4 pasos: 8,760 h → 100 − % → ÷ 100 → multiplica. Para minutos, × 60.', 'm')
c.L('🏰', 'Defensa en profundidad', 'Bloque B · Varias capas de protección', body(
    sp('En palabras sencillas', 'Poner <b>varias capas de protección</b>, una detrás de otra, para que si una falla las demás sigan protegiendo. <i>¿Por qué? Porque ninguna protección es perfecta: el antivirus no detecta todo y la gente se equivoca.</i>'),
    bk('Las capas (de afuera hacia adentro)', 'Reglas y capacitación → seguridad física → red → equipo (host) → aplicación → datos.'),
    an('capas'),
    ana('Piensa en un castillo', 'Foso, muralla, guardias, puerta y caja fuerte. Un ladrón tendría que vencerlas todas.'),
    ex('En la clínica', 'Un empleado abre un correo falso (falla la capacitación) → el antivirus lo bloquea (capa host) → y si no lo bloquea, los expedientes están cifrados y respaldados (capa datos).')),
    'Nunca confíes en una sola protección.')
c.L('🚨', 'Respuesta a incidentes', 'Bloque B · Qué hacer cuando algo pasa', body(
    sp('En palabras sencillas', 'Un <b>incidente</b> es algo que daña la seguridad: un virus, un robo de datos, un servidor caído. Para no improvisar, la respuesta sigue <b>4 fases en orden</b>.'),
    bk('Dos palabras que vas a ver', '<b>Malware</b>: cualquier programa dañino (virus, gusano, troyano…). <b>Ransomware</b>: un malware que <b>cifra tus archivos</b> para que no puedas abrirlos y te <b>pide dinero (rescate)</b> para devolverlos. <i>Por eso los respaldos son tan importantes: con ellos no necesitas pagar.</i>'),
    an('inc'),
    bk('1. Preparación (antes)', 'Tener un plan, saber quién hace qué, tener respaldos. <i>¿Por qué va primero? Porque en plena emergencia ya no da tiempo de hacer respaldos ni planes.</i>'),
    bk('2. Detección y análisis', 'Darse cuenta de que algo pasa y entender qué fue y qué tan grave es. <i>¿Por qué antes de actuar? Porque no puedes arreglar algo que no entiendes.</i>'),
    bk('3. Contención, erradicación y recuperación', 'Aislar el problema para que no se extienda, eliminar la causa y volver a funcionar. <i>¿Por qué en ese orden? Primero se detiene el daño (como cerrar la llave de agua en una fuga) y luego se repara.</i>'),
    bk('4. Lecciones aprendidas (después)', 'Revisar qué falló y mejorar. <i>¿Por qué? Para que no vuelva a pasar lo mismo.</i>'),
    ana('Piensa en un simulacro de sismo', 'Te preparas antes, actúas con orden durante y revisas qué mejorar después.')),
    'Preparar → detectar → contener y recuperar → aprender.')
c.L('🌪️', 'Recuperación tras un desastre: RPO y RTO', 'Bloque B · Volver a funcionar', body(
    sp('En palabras sencillas', 'Después de un desastre (incendio, inundación, un virus que cifra todo), hay dos preguntas. Cada una tiene su nombre:'),
    an('rpo'),
    bk('RPO · ¿Cuánta información puedo perder?', 'Mira <b>hacia atrás</b>: todo lo que se hizo desde el último respaldo se pierde. Por eso el RPO depende de <b>cada cuánto respaldas</b>.'),
    bk('RTO · ¿En cuánto tiempo debo volver a funcionar?', 'Mira <b>hacia adelante</b>: es el tiempo máximo que el servicio puede estar caído antes de que sea un problema grave.'),
    px('Ejemplo resuelto: la clínica respalda todas las noches', [
        paso('La clínica respalda cada noche a las 23:00.', 'El respaldo es el «punto de guardado» al que podemos regresar.'),
        paso('El jueves a las 18:00 un virus cifra todo.', 'Lo último que quedó guardado es el respaldo del miércoles a las 23:00.'),
        paso('Se pierde lo del jueves de 0:00 a 18:00 (más el rato del miércoles después de las 23:00): unas 19 horas.', 'Todo lo que se capturó después del último respaldo no está en ninguna copia.'),
        paso('En el peor caso (falla justo antes del respaldo) se pierde casi un día: RPO = 24 horas.', 'El RPO es igual al tiempo entre respaldos: si respaldas cada 24 h, puedes perder hasta 24 h.'),
        paso('La dueña dice: «la agenda tiene que volver en máximo 2 horas». Entonces RTO = 2 horas.', 'El RTO no se calcula: lo decide la organización según cuánto aguanta sin el servicio.'),
    ]),
    bk('Regla 3-2-1 de respaldos', '<b>3</b> copias, en <b>2</b> tipos de soporte distintos (disco y nube, por ejemplo) y <b>1</b> fuera del lugar. <i>¿Por qué fuera? Porque un incendio quemaría también las copias que estén en el mismo edificio.</i>'),
    ana('Piensa en un videojuego', 'El RPO es cada cuánto guardas la partida (lo que pierdes si se apaga); el RTO es cuánto tardas en volver a jugar.')),
    'RPO = datos perdidos (hacia atrás, depende del respaldo) · RTO = tiempo para volver (hacia adelante).')
c.O('🚨', 'Ordena la respuesta a un ransomware', 'La clínica descubre que sus archivos están cifrados por un virus que pide rescate. Ordena lo que deben hacer, de lo primero a lo último.', [
    ['Tener respaldos y un plan antes de que pase', 'Preparación: va primero porque sin respaldos no hay de dónde recuperar.'],
    ['Detectar los archivos cifrados y analizar qué equipos están afectados', 'Detección y análisis: entender qué pasó antes de actuar.'],
    ['Desconectar de la red los equipos infectados', 'Contención: se aísla para que el virus no pase a más equipos.'],
    ['Eliminar el malware y restaurar los respaldos', 'Erradicación y recuperación: ya contenido, se limpia y se vuelve a funcionar.'],
    ['Revisar cómo entró y capacitar al personal', 'Lecciones aprendidas: al final, para que no se repita.'],
], 'Antes (preparar) → darse cuenta → detener el daño → limpiar y recuperar → aprender.')
c.A('⏱️', '¿RPO o RTO?', 'Decide de qué meta habla cada frase. Pregúntate: ¿habla de DATOS perdidos o de TIEMPO sin servicio?', [
    ['Respaldamos cada 4 horas, así que perderíamos máximo 4 horas de datos', 'RPO', 'Habla de cuántos <b>datos</b> se pierden: RPO.'],
    ['La agenda debe volver a funcionar en menos de 1 hora', 'RTO', 'Habla del <b>tiempo</b> para que el servicio regrese: RTO.'],
    ['No podemos perder más de un día de cobros', 'RPO', '«Perder cobros» = perder <b>datos</b>: RPO.'],
    ['El sistema de cobro puede estar caído máximo medio día', 'RTO', '«Estar caído» = <b>tiempo</b> sin servicio: RTO.'],
], '¿Datos perdidos? → RPO · ¿Tiempo sin servicio? → RTO.', ['RPO', 'RTO'])
c.A('🛞', '¿Qué mecanismo usarías?', 'Elige la solución de alta disponibilidad para cada riesgo. Piensa: ¿qué pieza falla y cuál sería su repuesto?', [
    ['Que falle un disco del servidor', 'RAID (discos en espejo)', 'Falla un disco → el repuesto es otro disco con la misma información (RAID 1).'],
    ['Que se vaya la luz', 'UPS (no-break) o planta de luz', 'Falla la energía → el repuesto es una batería (UPS) o una planta.'],
    ['Que se caiga el internet', 'Segundo proveedor de internet', 'Falla el internet → el repuesto es otro proveedor.'],
    ['Que un solo servidor no aguante tantas visitas', 'Balanceo de carga', 'El problema es el exceso de visitas → se reparten entre varios servidores.'],
    ['Que se incendie la clínica', 'Respaldo fuera del lugar (nube)', 'Se pierde todo el edificio → la única copia que sobrevive es la que está fuera.'],
], 'Disco → RAID · Luz → UPS · Internet → segundo proveedor · Muchas visitas → balanceo · Incendio → copia fuera.')
b_end = c.mark() - 1

# ───────────────────────── C · Defensa de sistemas ─────────────────────────
c0 = c.mark()
c.L('🧭', '¿Host, servidor, red o física? Cómo distinguirlos', 'Bloque C · Antes de empezar', body(
    sp('En palabras sencillas', 'En este bloque vas a clasificar medidas de protección en <b>4 capas</b>. Para no confundirte, fíjate <b>qué cosa protege</b> la medida.'),
    bk('💻 Host', '¿Protege a <b>un solo equipo</b> que usa una persona? (su PC, su laptop, su celular).'),
    bk('🗄️ Servidor', '¿Protege a la computadora que <b>atiende a todos</b>? (la de la agenda, la de los archivos).'),
    bk('🌐 Red', '¿Protege <b>la conexión</b> entre equipos o con internet? (wifi, firewall, router).'),
    bk('🔐 Física', '¿Es algo que se puede <b>tocar</b>: puertas, llaves, cámaras, energía, discos?'),
    warn('Caso con truco', 'Un no-break se conecta al servidor, pero protege la <b>energía</b>, que es algo físico: va en «física». Fíjate en <b>qué protege</b>, no en dónde se conecta.')),
    'Un equipo → host · El que atiende a todos → servidor · La conexión → red · Lo que se toca → física.')
c.L('💻', 'Protección del host', 'Bloque C · Cada computadora', body(
    sp('En palabras sencillas', 'Un <b>host</b> es cualquier equipo que usa una persona. Cada uno debe poder protegerse solo.'),
    bk('Actualizaciones al día', 'A las actualizaciones de seguridad también se les llama <b>parches</b>. <i>¿Por qué?</i> Tapan fallas que los atacantes ya conocen. <i>Regla práctica: si el último parche tiene más de 3 meses, el equipo está atrasado.</i>'),
    bk('Antivirus activo', '<i>¿Por qué?</i> Detecta y bloquea programas dañinos antes de que actúen.'),
    bk('Firewall del equipo', '<i>¿Por qué?</i> Bloquea conexiones que nadie pidió.'),
    bk('Cuenta estándar (sin permisos de administrador) para trabajar', '<i>¿Por qué?</i> Si entra un virus, no tiene permiso de instalar ni de cambiar todo el equipo.'),
    bk('Bloqueo de pantalla y disco cifrado (BitLocker)', '<i>¿Por qué?</i> Si te alejas o te roban la laptop, nadie puede ver tus archivos.'),
    ex('En la clínica', 'La PC de recepción usa cuenta estándar, se bloquea sola a los 5 minutos y tiene el disco cifrado.')),
    'Cada equipo: actualizado, con antivirus, firewall, cuenta estándar, bloqueo y disco cifrado.')
c.L('🗄️', 'Protección del servidor', 'Bloque C · El equipo que da servicio a todos', body(
    bk('Menos es más', 'Apagar los servicios y cerrar los puertos que no se usan. <i>¿Por qué? Cada servicio encendido es una puerta por la que podrían entrar.</i>'),
    bk('Escritorio remoto: solo por VPN', 'El <b>escritorio remoto</b> permite manejar el servidor desde otra computadora, como si estuvieras sentado frente a él. Es útil, pero <b>no se deja abierto a todo internet</b>: se entra primero por una <b>VPN</b> (la verás en «Protección de la red»). <i>¿Por qué? Si queda abierto, cualquier persona del mundo puede intentar adivinar la contraseña.</i>'),
    bk('Mínimo privilegio', 'Solo quien lo necesita tiene cuenta de administrador, con contraseña fuerte y doble factor. <i>¿Por qué? Menos llaves maestras = menos riesgo de que una se pierda.</i>'),
    bk('Bitácoras y monitoreo', 'Registrar quién entra y qué cambia, y revisarlo. <i>¿Por qué? Así se detecta a tiempo algo raro.</i>'),
    bk('Respaldos y parches', 'Respaldar diario y aplicar actualizaciones en un horario planeado. <i>¿Por qué planeado? Para no apagar el servicio cuando más se usa.</i>'),
    ana('Piensa en…', 'La bodega de una tienda: pocas puertas, pocas llaves, cámara y registro de quién entra.')),
    'Un servidor seguro tiene pocas puertas abiertas y alguien vigilándolas.')
c.L('🌐', 'Protección de la red', 'Bloque C · Lo que une a todos', body(
    bk('Firewall', 'Un «portero» que revisa lo que entra y sale de internet y bloquea lo que no está permitido.'),
    bk('Segmentación (VLAN)', 'Dividir la red en partes separadas: el wifi de pacientes en una, las computadoras de la clínica en otra. <i>¿Por qué? Si un paciente trae un celular infectado, no llega a los expedientes.</i>'),
    bk('IDS / IPS', 'Vigilantes de la red: el IDS <b>avisa</b> si ve tráfico sospechoso; el IPS además lo <b>bloquea</b>.'),
    bk('VPN', 'Un «túnel» cifrado para conectarse a la red de la clínica desde fuera, sin que nadie vea lo que pasa por él.'),
    bk('Wifi seguro', 'Usar <b>WPA2</b> o <b>WPA3</b> con contraseña fuerte. <i>¿Por qué? Una red abierta deja entrar a cualquiera que esté cerca.</i>')),
    'Separar la red evita que un problema en un lado llegue a todo.')
c.L('🔐', 'Seguridad física', 'Bloque C · Lo que se puede tocar', body(
    bk('Control de acceso', 'El cuarto del servidor con llave o tarjeta; solo entra personal autorizado.'),
    bk('Vigilancia', 'Cámaras y libreta o registro de visitas.'),
    bk('Energía y ambiente', 'No-break, regulador, ventilación y extintor para equipo eléctrico.'),
    bk('Equipos y medios', 'Candados para laptops; destruir los discos viejos antes de tirarlos (borrar no basta: los archivos se pueden recuperar).'),
    warn('Recuerda', 'De nada sirve el mejor firewall si alguien puede entrar y llevarse el servidor.')),
    'La seguridad empieza por la puerta.')
c.A('🧱', '¿Qué capa protege?', 'Clasifica cada medida. Usa el truco: ¿protege a un equipo, al que atiende a todos, la conexión o algo que se toca?', [
    ['Cifrar el disco de la laptop del dentista', 'Host', 'Protege a un solo equipo que usa una persona: host.'],
    ['Desactivar en el servidor los servicios que no se usan', 'Servidor', 'Se hace en la computadora que atiende a todos: servidor.'],
    ['Separar el wifi de pacientes de la red interna', 'Red', 'Cambia cómo se conectan los equipos: red (segmentación).'],
    ['Poner llave al cuarto del servidor', 'Física', 'Una llave y una puerta se pueden tocar: física.'],
    ['Instalar un IDS que avise de tráfico raro', 'Red', 'Vigila lo que viaja por la conexión: red.'],
    ['Usar cuenta estándar en la PC de recepción', 'Host', 'Es una configuración de ese equipo: host.'],
    ['Instalar un no-break para el servidor', 'Física', 'Protege la energía, que es algo físico (el caso con truco).'],
], 'Un equipo → Host · El que atiende a todos → Servidor · La conexión → Red · Lo que se toca o la energía → Física.', ['Host', 'Servidor', 'Red', 'Física'])
c.A('⚖️', '¿Buena o mala práctica?', 'Decide si cada práctica de la clínica es buena o mala. Pregúntate: ¿abre una puerta o la cierra?', [
    ['Dejar abierto el escritorio remoto del servidor a todo internet', 'Mala práctica', 'Abre una puerta a cualquier persona del mundo. Lo correcto es entrar por VPN.'],
    ['Usar WPA3 con contraseña fuerte en la red interna', 'Buena práctica', 'Cierra la puerta: cifra el wifi y no deja entrar a desconocidos.'],
    ['Que todos usen la cuenta de administrador para ir más rápido', 'Mala práctica', 'Da llave maestra a todos; si entra un virus, puede hacer de todo.'],
    ['Tirar a la basura un disco viejo con expedientes sin borrarlo', 'Mala práctica', 'Cualquiera que lo encuentre podría recuperar los datos.'],
    ['Revisar cada semana las bitácoras del servidor', 'Buena práctica', 'Permite ver a tiempo si alguien entró sin permiso.'],
], '¿Abre una puerta? → mala práctica · ¿La cierra? → buena práctica.', ['Buena práctica', 'Mala práctica'])
c.L('📝', 'Ejemplo resuelto: cómo escribir una medida por capa', 'Bloque C · Antes de redactar', body(
    sp('La fórmula', 'Para cada capa escribe una oración así: <b>Capa: qué medida pones + para qué sirve</b>. El «para qué» demuestra que entiendes, no solo que memorizaste.'),
    px('Paso a paso con la clínica', [
        paso('Host: «Las PCs de recepción tienen antivirus y disco cifrado para que, si las roban, no se vean los expedientes».', 'Nombra el equipo, la medida y el para qué.'),
        paso('Servidor: «En el servidor de la agenda solo dejamos encendido el servicio de citas, para tener menos puertas abiertas».', 'Usa la palabra «servidor» y explica el beneficio.'),
        paso('Red: «Separamos el wifi de pacientes de la red interna con una VLAN, para que un celular infectado no llegue a los expedientes».', 'Menciona algo de la red (wifi, firewall, VLAN, VPN).'),
        paso('Física: «El cuarto del servidor tiene llave y un no-break, para que nadie se lo lleve y no se apague si se va la luz».', 'Menciona algo que se pueda tocar.'),
    ]),
    warn('No copies el ejemplo', 'En la siguiente actividad usa tus propias medidas (puedes elegir otras de las lecciones). Se revisa que menciones las 4 capas.')),
    'Capa + medida + para qué sirve.')
c.W('✍️', 'Defiende la clínica en 4 capas', 'Aplica la fórmula de la lección anterior: capa + medida + para qué sirve.',
    'Escribe una medida para cada capa de la clínica: <b>host</b>, <b>servidor</b>, <b>red</b> y <b>física</b>. Una oración por capa.',
    [['Tiene al menos 25 palabras', 'palabras:25'],
     ['Una medida para el host (equipo, PC, laptop, antivirus, cifrado…)', '\\b(host|pc|computadora\\w*|laptop\\w*|equipos?|antivirus|bitlocker|cifr\\w+)\\b'],
     ['Una medida para el servidor', '\\bservidor\\w*\\b'],
     ['Una medida para la red (firewall, VLAN, wifi, IDS, VPN…)', '\\b(red|redes|firewall|vlan|wifi|ids|ips|vpn|wpa\\w*)\\b'],
     ['Una medida física (llave, cámara, no-break, acceso…)', '\\b(llave\\w*|camara\\w*|no-?break|ups|acceso fisico|cuarto\\w*|candado\\w*|tarjeta\\w*|fisic\\w+)\\b']],
    'Empieza cada oración con el nombre de la capa: «Host: …», «Servidor: …», «Red: …», «Física: …».', 'Host: las PCs tienen … para que … Servidor: … Red: … Física: …')
c_end = c.mark() - 1

# ───────────────────────── D · Dominio de la ciberseguridad ─────────────────────────
d0 = c.mark()
c.L('🐞', 'Vulnerabilidades: CVE y CVSS', 'Bloque D · Dominio de vulnerabilidades', body(
    sp('En palabras sencillas', 'Una <b>vulnerabilidad</b> es una falla de un programa o equipo que un atacante puede aprovechar (lo viste en el R.A. 2.1). Cuando una falla se hace pública, recibe un número de identificación llamado <b>CVE</b>, por ejemplo CVE-2024-11477.'),
    bk('Cómo se lee un CVE', '<b>CVE</b> - <b>2024</b> (año en que se registró) - <b>11477</b> (número consecutivo). Es como la matrícula de la falla.'),
    bk('CVSS · qué tan grave es', 'Una calificación de 0 a 10: <b>Baja</b> 0.1–3.9 · <b>Media</b> 4.0–6.9 · <b>Alta</b> 7.0–8.9 · <b>Crítica</b> 9.0–10. Entre más alto, más urgente arreglarla.'),
    bk('Dónde se consultan', '<b>nvd.nist.gov</b> (base de datos del gobierno de EUA, en inglés) y <b>cve.org</b>.'),
    ana('Piensa en…', 'Los «llamados a revisión» de los coches: el fabricante publica la falla, su número y qué tan peligrosa es, para que la arregles.'),
    bk('¿En cuánto tiempo se corrige?', 'Una guía sencilla que usan muchas empresas: <b>Crítica</b> → hoy mismo (máximo 2 días) · <b>Alta</b> → esta semana · <b>Media</b> → este mes · <b>Baja</b> → en el siguiente mantenimiento programado. <i>¿Por qué? Entre más grave, más fácil y dañino es que la aprovechen.</i>'),
    bk('¿Cómo se corrige?', 'Casi siempre <b>actualizando</b> el programa. En la descripción de la falla (en inglés) busca «<b>before</b> 24.07» o «<b>prior to</b> 24.07»: significa que la falla está en las versiones <b>anteriores</b> a la 24.07, así que la solución es actualizar a esa versión o a una más nueva.'),
    ex('En la clínica', 'El sistema de citas tiene una CVE con CVSS 9.8: es crítica y se actualiza hoy mismo. Una de 3.1 (baja) se programa para el siguiente mantenimiento.')),
    'CVE = el nombre de la falla · CVSS = qué tan grave es · Primero se corrigen las críticas y altas.')
c.A('🐞', 'Clasifica la gravedad', 'Según su calificación CVSS, ¿qué tan grave es cada vulnerabilidad? Busca en qué rango cae el número.', [
    ['CVE con CVSS 9.8', 'Crítica', '9.8 está entre 9.0 y 10: crítica.'],
    ['CVE con CVSS 5.3', 'Media', '5.3 está entre 4.0 y 6.9: media.'],
    ['CVE con CVSS 7.5', 'Alta', '7.5 está entre 7.0 y 8.9: alta.'],
    ['CVE con CVSS 2.1', 'Baja', '2.1 está entre 0.1 y 3.9: baja.'],
    ['CVE con CVSS 10.0', 'Crítica', '10 es la calificación máxima: crítica.'],
], 'Menos de 4 → Baja · de 4 a 6.9 → Media · de 7 a 8.9 → Alta · 9 o más → Crítica.', ['Baja', 'Media', 'Alta', 'Crítica'])
c.L('🧭', 'Ética y principios rectores', 'Bloque D · Saber mucho exige responsabilidad', body(
    sp('En palabras sencillas', 'Lo que aprendes de ciberseguridad sirve para proteger o para dañar. La <b>ética</b> es lo que marca la diferencia entre un especialista y un delincuente.'),
    bk('1. Permiso por escrito', 'Solo se revisa un sistema con autorización firmada de su dueño. <i>¿Por qué? Sin permiso es un delito: el Código Penal Federal castiga el acceso ilícito a sistemas (artículos 211 bis 1 al 211 bis 7).</i>'),
    bk('2. Cuidar la privacidad', 'Los datos personales que veas mientras trabajas no se comentan ni se publican.'),
    bk('3. No causar daño', 'Probar sin apagar servicios ni borrar información.'),
    bk('4. Avisar de forma responsable', 'Si encuentras una falla, se la reportas al dueño y le das tiempo de corregirla antes de contarla.'),
    ex('Hacker ético y prueba de penetración', 'Una empresa contrata a una especialista para atacar su propia red y encontrar fallas antes que los delincuentes. A ese ataque autorizado se le llama <b>prueba de penetración</b> (o «pentest»). Antes firma un contrato que dice qué puede y qué no puede hacer.')),
    'Mismo conocimiento, distinta intención: el permiso lo cambia todo.')
c.A('🧭', '¿Es ético?', 'Decide si cada acción es ética o no. Usa las 3 preguntas: ¿tengo permiso?, ¿cuido la privacidad?, ¿causo daño?', [
    ['Escanear la red de la escuela por curiosidad, sin pedir permiso', 'No es ético', 'Falla la pregunta 1: no hay permiso por escrito, aunque sea «por curiosidad».'],
    ['Reportar al dueño una falla que encontraste en su página', 'Es ético', 'Es avisar de forma responsable: ayuda a corregirla.'],
    ['Publicar en redes los datos de pacientes que viste en una auditoría', 'No es ético', 'Falla la pregunta 2: viola la privacidad.'],
    ['Hacer una prueba de penetración con contrato firmado', 'Es ético', 'Tiene permiso por escrito y reglas claras.'],
    ['Usar la contraseña de un compañero que dejó su sesión abierta', 'No es ético', 'Es usar una cuenta ajena sin permiso, aunque esté abierta.'],
], '¿Tengo permiso? ¿Cuido la privacidad? ¿Causo daño? Si alguna falla → no es ético.', ['Es ético', 'No es ético'])
c.L('🛠️', 'Herramientas de ciberseguridad', 'Bloque D · Lo que usa un profesional', body(
    sp('Para recordar', 'Asocia cada herramienta con <b>una sola palabra</b>: la que dice qué revisa.'),
    bk('Nmap → puertos', 'Descubre qué equipos hay en una red y qué «puertas» (puertos) tienen abiertas.'),
    bk('Wireshark → tráfico', 'Captura y muestra lo que viaja por la red.'),
    bk('Escáner de vulnerabilidades → fallas', 'Como OpenVAS: revisa los equipos buscando fallas conocidas (CVE).'),
    bk('Gestor de contraseñas → contraseñas', 'Como Bitwarden: guarda contraseñas largas y distintas, cifradas.'),
    bk('VirusTotal → archivos y enlaces', 'Revisa un archivo o un enlace con muchos antivirus a la vez.'),
    warn('Recuerda', 'Usar Nmap o Wireshark en una red ajena sin permiso es un delito.')),
    'Puertos → Nmap · Tráfico → Wireshark · Fallas → escáner · Contraseñas → gestor · Archivo sospechoso → VirusTotal.')
c.A('🛠️', '¿Qué herramienta usas?', 'Elige la herramienta para cada tarea autorizada. Busca la palabra clave: puertos, tráfico, archivo, fallas o contraseñas.', [
    ['Saber qué puertos tiene abiertos el servidor de la clínica', 'Nmap', 'Palabra clave «puertos» → Nmap.'],
    ['Ver qué tráfico sale de la PC de recepción', 'Wireshark', 'Palabra clave «tráfico» → Wireshark.'],
    ['Revisar un archivo adjunto sospechoso', 'VirusTotal', 'Palabra clave «archivo» → VirusTotal lo revisa con decenas de antivirus.'],
    ['Buscar fallas conocidas (CVE) en todos los equipos', 'Escáner de vulnerabilidades', 'Palabra clave «fallas» → escáner de vulnerabilidades.'],
    ['Guardar contraseñas distintas para cada sistema', 'Gestor de contraseñas', 'Palabra clave «contraseñas» → gestor de contraseñas.'],
], 'Puertos → Nmap · Tráfico → Wireshark · Archivo → VirusTotal · Fallas → escáner · Contraseñas → gestor.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario (1 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Integridad', 'Que la información no se cambie sin permiso.'),
    bk('Hash', 'Fórmula que convierte un dato en una huella de tamaño fijo y sin regreso.'),
    bk('SHA-256', 'Algoritmo de hash seguro; su huella mide 64 caracteres.'),
    bk('Sal (salting)', 'Valor al azar que se pega a la contraseña antes de calcular el hash.'),
    bk('HMAC', 'Hash que se calcula con una clave secreta compartida.'),
    bk('Firma digital', 'Se hace con la clave privada y se comprueba con la pública.'),
    bk('Certificado', 'Documento de una autoridad que dice de quién es una clave pública (el candado HTTPS).'),
    bk('No repudio', 'Que quien firmó no pueda negar que lo hizo.'),
    bk('Llave primaria', 'Número que identifica un registro y no se repite.'),
    bk('Llave foránea', 'Campo que apunta a un registro de otra tabla.'),
    bk('Transacción', 'Operación de «todo o nada» en una base de datos.')))
c.L('📖', 'Glosario (2 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Disponibilidad', 'Que el servicio funcione cuando se necesita.'),
    bk('Alta disponibilidad', 'Preparar el servicio para que siga aunque algo falle.'),
    bk('Punto único de falla', 'Pieza sin repuesto que, si falla, detiene todo.'),
    bk('Redundancia', 'Tener repuesto de lo importante.'),
    bk('RAID 1', 'Dos discos con la misma información (espejo).'),
    bk('UPS (no-break)', 'Batería que da electricidad cuando se va la luz.'),
    bk('Defensa en profundidad', 'Varias capas de protección, una detrás de otra.'),
    bk('RPO', 'Cuánta información se puede perder (depende de cada cuánto respaldas).'),
    bk('RTO', 'En cuánto tiempo debe volver el servicio.'),
    bk('CVE', 'Número de identificación de una vulnerabilidad pública.'),
    bk('CVSS', 'Calificación de gravedad de 0 a 10.'),
    bk('Ransomware', 'Malware que cifra tus archivos y pide un rescate para devolverlos.'),
    bk('Parche', 'Actualización que tapa una falla de seguridad.'),
    bk('VLAN', 'Red separada dentro de la misma red física.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Laboratorio del grupo 511: <b>lunes 17:20-18:10</b> y <b>viernes 18:10-19:50</b>. Cada práctica tiene versión para celular.', 'sp'),
    bk('Versión «anti dudas»', 'Empieza aquí incluye 4 repasos (pilares, equipos y redes, cifrado y claves, porcentajes) para quien aún batalla con R.A. anteriores. Los temas difíciles tienen ejemplo resuelto con el porqué de cada paso, todas las actividades tienen pista y las prácticas explican qué hacer, por qué y qué hacer si algo no sale. En Diagnostica hay una calculadora de disponibilidad que muestra los 4 pasos.', 'sp'),
    bk('Bloque A · 23 y 26-oct', 'Viernes 23: repasos, hash, laboratorio de hash, contraseñas y salting en clase. <b>Lunes 26 (primera hora, laboratorio): Práctica 1</b> (la versión de celular usa la sal, por eso salting va antes); después HMAC, firmas e integridad en bases de datos.'),
    bk('Bloque B · 26-oct y 2-nov', 'Lunes 26 (últimas horas): disponibilidad y los nueves (resolver juntos el ejemplo en el pizarrón). Viernes 30 es CTEC. Lunes 2-nov: defensa en profundidad, incidentes y RPO/RTO; <b>Práctica 2</b> como tarea o en celular.'),
    bk('Bloque C · 2 y 6-nov', '<b>Viernes 6 (laboratorio): Práctica 3</b> y lecciones de defensa de sistemas.'),
    bk('Bloque D y evaluación · lunes 9-nov', 'Vulnerabilidades, ética y herramientas; los alumnos terminan y entregan el reporte en la actividad de la plataforma (organización asignada a cada uno). La actividad se desbloquea al completar este material.'),
    bk('Nota', 'Las herramientas como Nmap y Wireshark solo se usan en una red de práctica autorizada por ti.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp


def _title(page):
    if page.startswith('pHash('):
        return 'Laboratorio de hash'
    if page.startswith('pDisp('):
        return 'Calculadora de disponibilidad'
    return json_title(page)


def json_title(page):
    import json
    m = re.match(r'p\w\("(?:[^"\\]|\\.)*",("(?:[^"\\]|\\.)*")', page)
    return json.loads(m.group(1))


NEW_TITLES = [_title(p) for p in c.pages]
MIGRA = {old: NEW_TITLES.index(t) for old, t in enumerate(OLD_TITLES) if t in NEW_TITLES and NEW_TITLES.index(t) != old}
assert len(set(NEW_TITLES)) == len(NEW_TITLES), 'Títulos repetidos'
# El avance de la versión anterior se reubica una sola vez (marca ST.v22).
EXTRA_JS = EXTRA_JS_BASE + ANIM_JS + (
    'function mig22(S){if(!S||S.v22>=2)return S||{};var M=' + j({str(k): v for k, v in MIGRA.items()}) + ',N={};'
    'Object.keys(S).forEach(function(k){if(!/^\\d+$/.test(k))N[k]=S[k]});'
    'Object.keys(S).forEach(function(k){if(/^\\d+$/.test(k)){var n=M[k]!=null?M[k]:+k;N[n]=S[k]}});'
    '["att","bst"].forEach(function(f){if(S[f]&&typeof S[f]=="object"){var o={};Object.keys(S[f]).forEach(function(k){o[M[k]!=null?M[k]:k]=S[f][k]});N[f]=o}});'
    'delete N.pos;N.v22=2;return N}'
)

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
s0:{k:"Introducción",l:"0",ic:"🏥",t:"Empieza aquí",d:"De qué trata el R.A. y repaso de lo que necesitas de los R.A. anteriores.",time:"50 min",obj:["Distinguir integridad, disponibilidad y confidencialidad","Recordar qué es un host, un servidor y una red","Recordar qué es cifrar y qué son las claves pública y privada","Pasar porcentajes a decimales"],sum:["¿La vieron? → confidencialidad · ¿La cambiaron? → integridad · ¿No funciona? → disponibilidad.","Host = un equipo · Servidor = el que atiende a todos · Red = lo que los conecta.","Porcentaje a decimal: divide entre 100."],q:"¿Qué servicio que usas a diario sería un problema si se cayera un día entero?"},
a:{k:"Bloque A",l:"A",ic:"🧬",t:"Controles de integridad",d:"Hash, contraseñas con sal, HMAC, firmas, certificados y bases de datos.",time:"120 min",obj:["Explicar las 3 reglas del hash","Explicar por qué las contraseñas se guardan con hash y sal","Elegir entre hash, HMAC, firma digital y certificado"],sum:["El hash es una huella sin regreso: mismo dato → misma huella; una letra distinta → huella distinta.","La sal hace que contraseñas iguales tengan hashes distintos.","HMAC = hash + clave compartida · Firma = clave privada (no repudio) · Certificado = de quién es la clave pública."],q:"¿Por qué una página nunca debería poder enviarte tu contraseña por correo si la olvidas?"},
b:{k:"Bloque B",l:"B",ic:"🛞",t:"Estándar de ciberseguridad",d:"Alta disponibilidad, defensa en profundidad, incidentes y recuperación.",time:"150 min",obj:["Encontrar puntos únicos de falla y proponer su repuesto","Calcular el tiempo fuera de servicio con 4 pasos","Ordenar las fases de respuesta a incidentes y distinguir RPO de RTO"],sum:["Redundancia: RAID, UPS, dos proveedores, clúster y balanceo.","8,760 h × (100 − %) ÷ 100 = horas caídas al año.","RPO = datos perdidos (cada cuánto respaldas) · RTO = tiempo para volver."],q:"¿Cada cuánto respaldas tus fotos? ¿Cuál sería tu RPO?",rev:[["Si cambias una letra del texto, su hash…",["Cambia casi por completo","Cambia una letra","No cambia"],0,"Regla 2: un cambio mínimo cambia toda la huella."],["La sal sirve para…",["Que contraseñas iguales tengan hashes distintos","Cifrar el disco","Acelerar el inicio de sesión"],0,"Así las listas de hashes comunes ya no le sirven al atacante."]]},
c:{k:"Bloque C",l:"C",ic:"🧱",t:"Defensa de sistemas y dispositivos",d:"Host, servidor, red y seguridad física.",time:"100 min",obj:["Clasificar medidas en host, servidor, red y física","Proponer una medida por capa explicando para qué sirve"],sum:["Host: actualizaciones, antivirus, cuenta estándar, bloqueo y cifrado.","Servidor: pocos servicios, mínimo privilegio, bitácoras y respaldos.","Red: firewall, VLAN, IDS/IPS, VPN y WPA2/WPA3 · Física: puertas, cámaras, energía y discos."],q:"¿Qué capa de protección es la más débil en tu casa?",rev:[["«No podemos perder más de 4 horas de datos» es un…",["RPO","RTO","CVE"],0,"Habla de datos perdidos."],["Un no-break evita…",["Que se apague el equipo si se va la luz","Los virus","Las contraseñas débiles"],0,"Es el repuesto de la energía."]]},
d:{k:"Bloque D",l:"D",ic:"🧭",t:"Dominio de la ciberseguridad",d:"Vulnerabilidades, ética y herramientas.",time:"60 min",obj:["Leer un CVE y clasificar su CVSS","Aplicar las 3 preguntas de la ética","Relacionar cada herramienta con su palabra clave"],sum:["CVE = nombre de la falla · CVSS = qué tan grave (0 a 10).","Sin permiso por escrito no se prueba nada.","Puertos → Nmap · Tráfico → Wireshark · Fallas → escáner · Contraseñas → gestor · Archivo → VirusTotal."],q:"¿Qué harías si encuentras una falla en la página de tu escuela?",rev:[["Separar el wifi de pacientes de la red interna es…",["Segmentación de red","Seguridad física","Un hash"],0,"Protege la conexión: capa red (VLAN)."],["El servidor debe tener…",["Solo los servicios necesarios","Todos los puertos abiertos","Una sola contraseña para todos"],0,"Menos servicios, menos puertas."]]}
'''

ILL = r'''
ILL["Hash: la huella digital de los datos"]=function(){return flow([["📄","Expediente"],["⚙️","SHA-256"],["🧬","9f86d0…|(64 car.)"]],"Un dato entra y sale su huella")};
ILL["La técnica salting"]=function(){return SV(340,130,R_(10,8,320,50,"s")+T_(20,28,"123456 + sal «a7f2» → hash 3c9e…","t","start")+T_(20,46,"123456 + sal «91bd» → hash e04a…","t","start")+R_(10,70,320,50,"b")+T_(170,92,"Misma contraseña, hashes distintos","tw")+T_(170,108,"Las listas de hashes comunes no sirven","tw"),"Salting")};
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
EXH.ps_abrir=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno&gt; cd Documents\nPS C:\\Users\\Alumno\\Documents&gt;',true),['Tecla Windows → escribe PowerShell → Enter.','Fíjate que la ruta ya termina en \\Documents: ahí quedará tu archivo.'])};
EXH.calc_pasos=function(){return exw('<div class="mbox" style="line-height:1.8"><b>Mi servicio: agenda en línea · 99.9 %</b><br>Paso 1: 365 × 24 = 8,760 h<br>Paso 2: 100 − 99.9 = 0.1 %<br>Paso 3: 0.1 ÷ 100 = 0.001<br>Paso 4: 8,760 × 0.001 = <b>8.76 h al año</b> '+mk(1)+'</div>',['Escribe los 4 pasos, no solo el resultado: así se ve que entendiste.'])};
EXH.nvd_buscar=function(){return exw(mw('nvd.nist.gov/vuln/search','<div style="line-height:1.8">Search Type: <b>Basic</b> · Results Type: <b>Overview</b><br>Keyword Search: <span style="border:1px solid #999;padding:1px 8px">7-Zip</span> '+mk(1)+' <b>[Search]</b><br>CVE-2024-11477 · ... <b>V3.1: 7.8 HIGH</b> '+mk(2)+'</div>'),['Escribe el nombre del programa en Keyword Search y presiona Search.','Abre un resultado: ahí vienen su CVE, su calificación (HIGH = alta) y en la descripción «before X» (la solución: actualizar a la versión X).'])};
'''


CMD = '<code style="font-family:Consolas,monospace;background:color-mix(in srgb,var(--pri) 10%,transparent);padding:1px 5px;border-radius:5px">{}</code>'


def cmd(t):
    return CMD.format(t)


def st(hacer, porque, falla=None, exh=None):
    """Paso de práctica: qué hacer + por qué (+ qué hacer si no sale) (+ ejemplo)."""
    t = f'{hacer}{why(porque)}' + (ojo(falla) if falla else '')
    return [t, exh] if exh else t


P1_FINAL = st('Escribe 4 renglones para tu organización completando estas frases: <b>1)</b> «El archivo más importante que protegería es…» <b>2)</b> «Calcularía su huella original cuando…» <b>3)</b> «Guardaría esa huella en…» <b>4)</b> «Si la huella ya no coincide, haría…»',
              'Es exactamente lo que vas a necesitar en la sección «Integridad» de tu reporte. Las frases te guían para que no se te olvide ninguna parte. Si no sabes qué escribir, regresa al «Ejemplo resuelto: descubrir si alguien cambió un expediente»: tiene las 4 partes.',
              'Tu organización está en la actividad de evaluación R.A. 2.2 de la plataforma, en el recuadro «Datos asignados».')
P2_STEPS = [
    st('Escribe en tu documento <b>3 servicios</b> de tu organización asignada (por ejemplo: cobro, página web, archivos de clientes).',
       'Primero hay que saber QUÉ se quiere mantener funcionando; sin eso no se puede proteger nada.',
       'Los datos de tu organización están en la actividad de evaluación R.A. 2.2 de la plataforma (número de usuarios, equipos, incidente y tiempo máximo sin servicio).'),
    st('Para cada servicio hazte la pregunta: <b>«si esta pieza se descompone, ¿se cae el servicio y no hay otra igual?»</b> Anota esa pieza como su punto único de falla.',
       'Un punto único de falla es justamente eso: algo sin repuesto que detiene todo. La pregunta te ayuda a encontrarlo sin adivinar.',
       'Piensa en: el disco, la luz, el internet, el servidor o una sola persona que sabe usar el sistema.', 'tabla_disp'),
    st('En la misma tabla escribe el <b>repuesto (redundancia)</b> de cada punto de falla: RAID, UPS, segundo proveedor, otro servidor…',
       'Eliminar un punto único de falla = ponerle repuesto. Usa la actividad «¿Qué mecanismo usarías?» como guía.',
       'Si tu punto de falla es una persona (solo ella sabe usar el sistema), su repuesto es capacitar a otra persona.'),
    st('Calcula cuántas horas al año podría estar caído su servicio principal con <b>99 %</b> y con <b>99.9 %</b>. Escribe los <b>4 pasos</b>, no solo el resultado.',
       'Escribir los pasos demuestra que entiendes de dónde sale el número; además, si te equivocas, tu profe puede ver en qué paso fue.',
       'Si te sale un número enorme (como 8,672), multiplicaste por 99 en lugar de por lo que NO funciona. Revisa con la calculadora de disponibilidad en Diagnostica: 99 % → 87.6 h y 99.9 % → 8.76 h.', 'calc_pasos'),
    st('Elige <b>cada cuánto respaldarías</b> 2 servicios y escribe su <b>RPO</b>: es igual al tiempo entre respaldos (respaldo diario → RPO 24 h; cada hora → RPO 1 h).',
       'Lo que se perdería en el peor caso es todo lo hecho desde el último respaldo; por eso el RPO sale de la frecuencia del respaldo.'),
    st('Escribe el <b>RTO</b> de esos 2 servicios: un tiempo <b>igual o menor</b> al tiempo máximo sin servicio que acepta tu organización.',
       'El RTO no se calcula, se decide: es la promesa de en cuánto tiempo vuelves. Si fuera mayor de lo que tu organización aguanta, el plan no serviría.', None, 'rpo_rto'),
    st('Escribe <b>una oración por cada una de las 4 fases</b> de respuesta para el incidente de tu organización: Preparación, Detección y análisis, Contención-erradicación-recuperación, Lecciones aprendidas.',
       'Una oración por fase te obliga a pensar qué se hace en cada momento y en el orden correcto: antes, darse cuenta, detener y reparar, aprender.',
       'Si no sabes qué escribir en una fase, regresa a la lección «Respuesta a incidentes»: cada fase tiene su ejemplo.', 'incidente'),
    st('Explica en 3 renglones cómo aplicarías la <b>defensa en profundidad</b>: menciona al menos 3 capas, una detrás de otra (por ejemplo: capacitación → antivirus → respaldos).',
       'La idea es demostrar que no confías en una sola protección: si una falla, la siguiente detiene el problema.'),
]
P3_FINAL = [
    st('Propón <b>una medida de servidor, una de red y una física</b> para tu organización, con la fórmula «capa + medida + para qué sirve».',
       'Con la revisión del host ya tienes la primera capa; con estas tres completas las 4 capas que pide el reporte.'),
    st('Escribe <b>3 principios éticos</b> que seguirías si te contrataran para revisar esa organización (por ejemplo: «Solo revisaría con permiso por escrito porque…»).',
       'Agregar el «porque» demuestra que sabes la razón de cada principio, no solo su nombre.'),
]

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Comprueba la integridad con hash',
     'prog': 'Bloque A · Algoritmos de hash e integridad de archivos',
     'min': 50, 'lug': 'Laboratorio, lunes 26-oct (primera hora) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'PowerShell y Símbolo del sistema (ya vienen en Windows)', 'Un documento de Word o de Google para pegar tus capturas',
                        'Objetivo: comprobar con tus propios ojos las 3 reglas del hash'],
                'steps': [
                    st(f'Abre <b>PowerShell</b>: presiona la tecla Windows, escribe PowerShell y da Enter. Luego escribe {cmd("cd Documents")} y presiona Enter.',
                       'Los comandos trabajan con los archivos de la carpeta en la que estás parado. Así tu archivo quedará en Documentos y lo encontrarás fácil.',
                       'Si dice que no encuentra la ruta, prueba con ' + cmd('cd Documentos') + '.', 'ps_abrir'),
                    st(f'Crea el archivo escribiendo: {cmd("Set-Content expediente.txt &quot;Ana Lopez - alergia a la penicilina&quot;")} y Enter.',
                       'Necesitamos un archivo para sacarle su huella. Lo escribimos sin acentos para que todos los programas lean exactamente las mismas letras.'),
                    st(f'Calcula su huella con {cmd("Get-FileHash expediente.txt")}. Toma captura y copia en tu tabla los <b>primeros 8 caracteres</b> del hash.',
                       'Esta es la huella «original». Get-FileHash usa SHA-256 sin que se lo pidas. Con 8 caracteres basta para comparar, porque si algo cambia, cambia casi todo.',
                       'Si sale «no se encuentra el archivo», revisa que estés en Documents (paso 1) y que el nombre esté bien escrito. Si el hash sale cortado con «…», usa ' + cmd('Get-FileHash expediente.txt | Format-List') + ': lo muestra completo en un renglón.', 'hash_ps'),
                    st(f'Abre el <b>Símbolo del sistema</b> (tecla Windows → escribe cmd → Enter), escribe {cmd("cd Documents")} y luego {cmd("certutil -hashfile expediente.txt SHA256")}. Compara con el hash del paso 3.',
                       'Son dos programas distintos, pero SHA-256 es un estándar: el mismo archivo debe dar la misma huella sin importar qué programa la calcule (regla 1).',
                       'certutil la muestra en minúsculas y PowerShell en MAYÚSCULAS: son la misma huella. Si no pusiste SHA256 al final, certutil usa otro algoritmo y sale distinta.', 'certutil'),
                    st(f'Cambia <b>una sola letra</b>: {cmd("Set-Content expediente.txt &quot;Ana Lopez - alergia a la penicilinA&quot;")} y vuelve a usar {cmd("Get-FileHash expediente.txt")}. Anótalo en tu tabla.',
                       'Así compruebas la regla 2: con un cambio mínimo, la huella cambia casi completa. Es la prueba de que el hash detecta cualquier alteración.',
                       'Si el hash salió igual, el cambio no se guardó: vuelve a escribir el comando Set-Content con la A mayúscula al final.', 'hash_cambio'),
                    st('Regresa el texto original (el comando del paso 2) y calcula la huella otra vez. Anota si coincide con la del paso 3.',
                       'Si vuelve a coincidir, demuestras que la huella depende SOLO del contenido. Así es como se verifica que un archivo no fue modificado.',
                       'Si no coincide, revisa letra por letra: un espacio de más, un acento o una mayúscula ya cuentan como cambio.'),
                    st('Busca en internet una página de descarga que publique el <b>SHA-256</b> de su archivo (por ejemplo, la de VLC muestra «SHA-256 checksum»). Toma captura y explica en 2 renglones para qué sirve.',
                       'Comparar el hash publicado con el de tu archivo descargado te asegura que bajaste el original y no una copia modificada con virus.', None, 'descarga_hash'),
                    P1_FINAL]},
         'cel': {'mat': ['Celular', 'Este material: pestaña Diagnostica → Laboratorio de hash', 'Documentos de Google o notas para tu reporte',
                         'Objetivo: comprobar con tus propios ojos las 3 reglas del hash'],
                 'steps': [
                     st('Abre <b>Diagnostica → Laboratorio de hash</b>. Deja el texto que trae y toma captura de su huella.',
                        'Esta es la huella «original» con la que vas a comparar todo lo demás.', None, 'hash_cel'),
                     st('Cambia <b>una sola letra</b> (por ejemplo «Ana» por «Ena») y toma captura de cuántos caracteres de la huella cambiaron.',
                        'Así compruebas la regla 2: con un cambio mínimo, la huella cambia casi completa.', 'Si no ves el aviso de cuántos cambiaron, escribe y borra una letra otra vez: se calcula al escribir.', 'hash_cel'),
                     st('Regresa la letra original y comprueba que la huella vuelve a ser la de tu primera captura.',
                        'Regla 1: el mismo texto siempre da la misma huella. Así se verifica que algo no cambió.'),
                     st('Activa la casilla <b>Agregar sal</b>, escribe una contraseña de prueba (no la tuya), quita y vuelve a activar la sal. Explica por qué cambia la huella aunque la contraseña sea la misma.',
                        'Cada vez que se activa, la sal es un valor al azar distinto que se pega antes del texto; lo que entra al hash es diferente y por eso sale otra huella. Es justo lo que protege a dos usuarios con la misma contraseña.', None, 'hash_cel'),
                     st('Busca en internet una página de descarga que publique el <b>SHA-256</b> de su archivo (por ejemplo, la de VLC muestra «SHA-256 checksum»). Toma captura y explica en 2 renglones para qué sirve.',
                        'Comparar el hash publicado con el del archivo descargado te asegura que bajaste el original y no una copia modificada con virus.', None, 'descarga_hash'),
                     P1_FINAL]}},
     'entrega': ['Capturas y tabla de pruebas dentro de tu reporte.', 'Revisa tus resultados con el botón «¿Voy bien?» (arriba del material) antes de entregar.'],
     'rub': [['Hash calculado correctamente', 25], ['Prueba con una letra cambiada', 25], ['Explicación de la descarga verificada', 20], ['Aplicación a la organización', 30]]},
    {'id': 'pr2', 'n': 2, 't': 'Plan de disponibilidad y respuesta a incidentes',
     'prog': 'Bloque B · Alta disponibilidad, respuesta a incidentes y recuperación',
     'min': 100, 'lug': 'Aula, casa o celular (semana del 26-oct al 2-nov)',
     'modes': {
         'pc': {'mat': ['Word o Documentos de Google', 'Tu organización asignada en la actividad de evaluación de la plataforma', 'La calculadora de disponibilidad (pestaña Diagnostica) para revisar tus cuentas'],
                'steps': P2_STEPS},
         'cel': {'mat': ['Documentos de Google o notas', 'Tu organización asignada en la actividad de evaluación de la plataforma', 'La calculadora de disponibilidad (pestaña Diagnostica) para revisar tus cuentas'],
                 'steps': P2_STEPS}},
     'entrega': ['Tablas y respuestas dentro de tu reporte.', 'Revisa tus números con el botón «¿Voy bien?» (arriba del material) antes de entregar.'],
     'rub': [['Puntos de falla y redundancia', 25], ['Cálculo de disponibilidad', 15], ['RPO y RTO bien definidos', 25], ['Fases del incidente', 25], ['Defensa en profundidad', 10]]},
    {'id': 'pr3', 'n': 3, 't': 'Revisa la defensa de un equipo y busca vulnerabilidades',
     'prog': 'Bloques C y D · Protección del host y dominio de vulnerabilidades',
     'min': 100, 'lug': 'Laboratorio, viernes 6-nov o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Navegador', 'Documento para tu reporte'],
                'steps': [
                    st('Abre <b>Seguridad de Windows</b> (tecla Windows → escribe «Seguridad de Windows» → Enter). Toma captura y anota el estado de cada sección: ✅ verde = bien, ⚠️ amarillo = hay algo pendiente.',
                       'Es la forma más rápida de ver si el equipo (host) tiene antivirus, firewall y protección de cuentas activos.',
                       'Si una sección tiene ⚠️, da clic en ella: Windows te dice qué falta. Anótalo, no tienes que arreglarlo en la escuela.', 'seg_win'),
                    st('Haz una tabla con <b>6 medidas del host</b> y cómo comprobaste cada una: <b>1)</b> Actualizaciones: Configuración → Windows Update. <b>2)</b> Antivirus y <b>3)</b> Firewall: Seguridad de Windows. <b>4)</b> Tipo de cuenta: Configuración → Cuentas → Tu información (dice «Administrador» o «Estándar»). <b>5)</b> Bloqueo automático: Configuración → Personalización → Pantalla de bloqueo. <b>6)</b> Cifrado: busca «BitLocker».',
                       'Cada medida tapa una forma distinta de atacar al equipo (lección «Protección del host»). La evidencia demuestra que sí la revisaste y no la inventaste.',
                       'En Windows Home no existe BitLocker: anota «No disponible en esta versión». Que algo NO se cumpla también es un resultado válido: escribe ❌ y qué propones.', 'checklist_host'),
                    st('Entra a <b>nvd.nist.gov/vuln/search</b> → en <b>Keyword Search</b> escribe el nombre de un programa que uses (7-Zip, Chrome, Zoom…) → <b>Search</b> → abre un resultado. Anota su <b>CVE</b>, su calificación <b>CVSS</b> (Base Score) y la <b>solución</b> (busca «before» o «prior to» en la descripción, como viste en la lección «Vulnerabilidades: CVE y CVSS»).',
                       'Así practicas lo que hace un especialista: encontrar fallas públicas de los programas que usa su organización y decidir cuáles corregir primero según su gravedad.',
                       'La página está en inglés: da clic derecho → «Traducir al español». HIGH = alta, CRITICAL = crítica, MEDIUM = media, LOW = baja. Si aparecen dos calificaciones, anota la primera y di de qué versión es (por ejemplo «CVSS 3.1»). Si dice «N/A» o «not yet provided», abre otro resultado.', 'nvd_buscar'),
                    st('Escribe la gravedad de tu CVE con la escala (Baja · Media · Alta · Crítica) y explica <b>en cuánto tiempo</b> la corregirías.',
                       'La calificación sirve para decidir qué se arregla primero. Usa la guía de la lección: Crítica → hoy (máximo 2 días) · Alta → esta semana · Media → este mes · Baja → siguiente mantenimiento.', None, 'cve'),
                    ] + P3_FINAL},
         'cel': {'mat': ['Celular', 'Navegador', 'Documento o notas para tu reporte'],
                 'steps': [
                     st('Abre <b>Ajustes</b> en tu celular y revisa: bloqueo de pantalla, protección contra apps dañinas (Play Protect o equivalente) y fecha del parche de seguridad (Ajustes → Acerca del teléfono). Haz tu lista con ✅ o ❌: el parche lleva ✅ si tiene <b>3 meses o menos</b> (regla de la lección «Protección del host»).',
                        'Tu celular también es un host. Revisarlo te enseña las mismas medidas que se revisan en una computadora.',
                        'Cada marca de celular acomoda distinto los menús: usa la lupa de Ajustes y busca «bloqueo», «Play Protect» o «parche».', 'cel_checklist'),
                     st('Entra a <b>nvd.nist.gov/vuln/search</b> → en <b>Keyword Search</b> escribe «Android» o el nombre de una app que uses → <b>Search</b> → abre un resultado. Anota su <b>CVE</b>, su <b>CVSS</b> (Base Score) y la <b>solución</b> (busca «before» o «prior to» en la descripción, como viste en la lección «Vulnerabilidades: CVE y CVSS»).',
                        'Así practicas lo que hace un especialista: encontrar fallas públicas y decidir cuáles corregir primero según su gravedad.',
                        'La página está en inglés: usa la opción «Traducir» de tu navegador. HIGH = alta, CRITICAL = crítica, MEDIUM = media, LOW = baja. Si dice «N/A» o «not yet provided», abre otro resultado.', 'nvd_buscar'),
                     st('Escribe la gravedad de tu CVE con la escala (Baja · Media · Alta · Crítica) y explica <b>en cuánto tiempo</b> la corregirías.',
                        'La calificación sirve para decidir qué se arregla primero. Usa la guía de la lección: Crítica → hoy (máximo 2 días) · Alta → esta semana · Media → este mes · Baja → siguiente mantenimiento.', None, 'cve'),
                     ] + P3_FINAL}},
     'entrega': ['Capturas, lista de cotejo y ficha del CVE dentro de tu reporte.', 'Revisa tu CVE con el botón «¿Voy bien?» (arriba del material) antes de entregar.'],
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
    'situation': 'En la actividad de evaluación de la plataforma tienes asignada una organización, con su número de usuarios, equipos, un incidente reciente y el tiempo máximo sin servicio que acepta. Elabora un reporte que proponga cómo proteger su integridad, mantener su disponibilidad y defender sus sistemas. No empiezas de cero: tus tres prácticas ya tienen casi todo.',
    'hint': 'Responde siempre para TU organización: cada sección debe mencionar sus datos (servicios, incidente y tiempo sin servicio). Usa la fórmula «qué haría + para qué sirve».',
    'steps': [
        ('Contexto', ['Describe la organización asignada, la información que maneja y los servicios que no pueden detenerse (lo tienes del paso 1 de la Práctica 2).']),
        ('Integridad (Bloque A)', ['Explica cómo usarías hash con sal, HMAC o firma digital y certificados, y cómo cuidarías la integridad de su base de datos (usa tus 4 renglones de la Práctica 1).']),
        ('Estándar (Bloque B)', ['Propón redundancia para sus puntos únicos de falla y calcula su disponibilidad con los 4 pasos (Práctica 2).', 'Define respaldos, RPO y RTO; el RTO no puede ser mayor que el tiempo máximo sin servicio.', 'Describe las 4 fases de respuesta para su incidente reciente, una oración por fase.']),
        ('Defensa de sistemas (Bloque C)', ['Medidas para host, servidor, red y seguridad física, cada una con su «para qué sirve» (Práctica 3).']),
        ('Dominio (Bloque D)', ['Una vulnerabilidad real (CVE y CVSS) que afectaría a la organización y cómo la corregirías.', 'Principios éticos y herramientas que usarías con autorización.']),
        ('Entrega', ['Llena las secciones de la actividad en la plataforma y adjunta tu reporte en PDF.']),
    ],
    'rubric': [('Contexto de la organización', 10), ('Controles de integridad', 20), ('Disponibilidad, RPO/RTO y respuesta al incidente', 25), ('Defensa de sistemas en 4 capas', 20), ('Vulnerabilidad, ética y herramientas', 15), ('Redacción y presentación', 10)],
    'deliver': ['Un archivo PDF con tu reporte.', 'Se entrega en la actividad R.A. 2.2 de la plataforma, junto con las secciones escritas.'],
}
