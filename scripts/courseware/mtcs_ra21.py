"""MTCS-20 · R.A. 2.1 · Fundamentos de la ciberseguridad.

Caso de las lecciones: Gimnasio Fuerza Joven (socios, pagos, torniquete con huella y redes sociales).
La actividad de evaluación vive en la plataforma (MtcsActivity: presentación electrónica con un caso asignado).
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MTCS-RA-2.1'
CODE_PREFIX = 'MTCS21'
FILE = 'mtcs-ra21-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 2.1 · Fundamentos de ciberseguridad'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 2.1 · Fundamentos de ciberseguridad'
HERO_KICK = 'MTCS-20 · R.A. 2.1'
HERO_TITLE = 'Entiende cómo se protege la información y cómo la atacan'
HERO_TEXT = 'Aprende qué es la ciberseguridad, sus principios, las amenazas más comunes y las formas de protegerte, con el caso de un gimnasio.'
EV_SHORT = 'prepara tu presentación con el caso asignado.'
EV_CARD = 'Presentación R.A. 2.1'
RA = 'R.A. 2.1'
GROUP = '511'
TABS = {'d': ['Diagnostica', 'Detecta phishing y mide contraseñas'], 'c': ['Construye', 'Prácticas y presentación']}

EXTRA_JS = r'''
var PHF=[["from","El remitente usa un dominio raro: <b>bancoazteka-seguro.com</b>, no el del banco.","Dominio falso"],["subj","El asunto mete <b>miedo y prisa</b> («URGENTE», «24 horas»).","Urgencia y amenaza"],["hi","Saluda con «Estimado cliente» en vez de tu nombre: es un mensaje masivo.","Saludo genérico"],["link","El enlace apunta a <b>bancoazteka-verifica.com</b>, no a la página oficial.","Enlace falso"],["pin","Ningún banco te pide tu <b>NIP</b> ni tu tarjeta por correo.","Pide datos secretos"],["att","Un archivo <b>.exe</b> adjunto es un programa: puede instalar malware.","Adjunto peligroso"]];
function pPhish(){K++;var f={from:"Soporte Banco Azteka &lt;soporte@bancoazteka-seguro.com&gt;",subj:"URGENTE: tu cuenta será bloqueada en 24 horas"};
return '<article class="lesson"><header><span class="kick">🎣 Herramienta</span><h1>Detective de phishing</h1><p class="sub">Toca las partes del correo que te parezcan sospechosas. Hay 6 señales de alerta y 2 partes normales.</p></header><style>.phx .mail{border:1.5px solid var(--line);border-radius:12px;overflow:hidden;background:var(--card)}.phx .mh{padding:10px 12px;background:var(--bg);border-bottom:1px solid var(--line);font-size:14px;line-height:1.6}.phx .mb{padding:12px;font-size:15px;line-height:1.7}.phx .hs{cursor:pointer;border-radius:6px;padding:1px 3px;border-bottom:2px dashed var(--mut);background:transparent;text-align:left;font:inherit;color:inherit;border-top:0;border-left:0;border-right:0}.phx .hs.on{background:var(--exb);border-bottom-color:var(--amb)}.phx .hs.ok{background:var(--ok-soft);border-bottom:2px solid var(--ok)}.phx .hs.no{background:var(--bad-soft);border-bottom:2px solid var(--bad)}.phx .res2{margin-top:12px}.phx .res2 li{margin:4px 0}</style><div class="phx"><div class="mail"><div class="mh"><div>De: <button class="hs" data-k="from">'+f.from+'</button></div><div>Asunto: <button class="hs" data-k="subj">'+f.subj+'</button></div></div><div class="mb"><button class="hs" data-k="logo" data-d="1">🏦 Banco Azteka</button><p><button class="hs" data-k="hi">Estimado cliente:</button></p><p>Detectamos actividad sospechosa en tu cuenta. <button class="hs" data-k="link">Haz clic aquí para verificar tu cuenta</button> y evita el bloqueo.</p><p><button class="hs" data-k="pin">Para confirmar tu identidad responde con tu número de tarjeta y tu NIP.</button></p><p>Adjunto: <button class="hs" data-k="att">formulario_verificacion.exe</button></p><p><button class="hs" data-k="foot" data-d="1">Aviso de privacidad · Banco Azteka, S.A.</button></p></div></div><p style="margin:12px 0"><button class="btn" data-ph="go">Revisar mis señales</button> <button class="btn ghost" data-ph="reset">Empezar de nuevo</button></p><div class="res2" role="status"></div></div><p class="take"><b>Úsala para:</b> practicar antes de abrir un correo o mensaje que te pida algo con prisa.</p></article>'}
function phInit(d){var w=d.querySelector(".phx");if(!w)return;var hs=[].slice.call(w.querySelectorAll(".hs")),out=w.querySelector(".res2");
 hs.forEach(function(b){b.onclick=function(){if(b.classList.contains("ok")||b.classList.contains("no"))return;b.classList.toggle("on")}});
 w.querySelector("[data-ph=reset]").onclick=function(){hs.forEach(function(b){b.className="hs"});out.innerHTML=""};
 w.querySelector("[data-ph=go]").onclick=function(){var found=0,wrong=[],h="";PHF.forEach(function(r){var b=w.querySelector('[data-k="'+r[0]+'"]'),on=b.classList.contains("on")||b.classList.contains("ok");b.className="hs"+(on?" ok":"");if(on)found++;else h+='<li>⚠️ <b>Te faltó:</b> '+r[1]+'</li>'});
  hs.forEach(function(b){if(b.dataset.d&&b.classList.contains("on")){b.className="hs no";wrong.push(b.textContent)}});
  wrong.forEach(function(t){h+='<li>❌ «'+t+'» es normal en un correo real; no es una señal de alerta.</li>'});
  var all=found==6&&!wrong.length;if(all){var t="t:Detective de phishing";if(!ST[t]){ST[t]=1;sv()}h='<li>✅ <b>¡Las encontraste todas!</b> Cuando veas dos o más de estas señales, no abras nada y avisa.</li>'+h}
  out.innerHTML='<p><b>'+found+' de 6 señales encontradas</b></p><ul>'+h+'</ul>'}}
var PWC=["123456","12345678","123456789","password","contrasena","qwerty","abc123","111111","admin","iloveyou","futbol","mexico","mexico123","football","0000","1234"];
function pPass(){K++;return '<article class="lesson"><header><span class="kick">🔑 Herramienta</span><h1>Medidor de contraseñas</h1><p class="sub">Escribe contraseñas de PRUEBA y mira cuánto tardaría un atacante en adivinarlas.</p></header><style>.pwx .pm{height:12px;border-radius:6px;background:var(--line);overflow:hidden;margin:10px 0}.pwx .pm i{display:block;height:100%;width:0;transition:width .25s,background .25s}.pwx .st3{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:10px 0}.pwx .st3 div{background:var(--bg);border-radius:10px;padding:8px 10px;font-size:14px}.pwx .st3 b{display:block;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}.pwx input[type=text]{width:100%;padding:12px;border:2px solid var(--line);border-radius:10px;font:17px Consolas,monospace;background:var(--card);color:var(--ink)}.pwx .tips li{margin:3px 0}</style><div class="pwx czf"><label>Contraseña de prueba<input type="text" class="pwi" autocomplete="off" spellcheck="false" placeholder="Escribe aquí una contraseña de prueba"></label><div class="pm"><i></i></div><p class="pl" style="font-weight:700;margin:4px 0">Escribe algo para empezar.</p><div class="st3"><div><b>Longitud</b><span class="p1">—</span></div><div><b>Tipos de caracteres</b><span class="p2">—</span></div><div><b>Tiempo para adivinarla*</b><span class="p3">—</span></div><div><b>Pruebas fuertes</b><span class="p4">0</span></div></div><ul class="tips"></ul><p style="font-size:13px;color:var(--mut)">*Estimado con 10,000 millones de intentos por segundo, como un equipo potente que prueba combinaciones. Todo ocurre en tu navegador: no se envía ni se guarda nada. <b>No escribas tus contraseñas reales.</b></p></div><p class="take"><b>Prueba:</b> «hola123», «Futbol2026», una frase de 4 palabras sin relación y una de 5 palabras con un número. ¿Cuál tarda más?</p></article>'}
function pwTime(s){if(s<1)return "al instante";var u=[["segundos",60],["minutos",60],["horas",24],["días",365],["años",1000],["miles de años",1000],["millones de años",1e9]],v=s,i=0;for(;i<u.length-1&&v>=u[i][1];i++)v/=u[i][1];return v>=1e9?"más que la edad del universo":(v<10?v.toFixed(1):Math.round(v).toLocaleString("es-MX"))+" "+u[i][0]}
var PWW="contrasena clave secreto password admin hola amor te amo princesa angel dios familia mexico tamaulipas victoria conalep escuela alumno maestro profe futbol america chivas pumas tigres rayados cruz azul barcelona madrid messi ronaldo juan pedro luis carlos jose maria ana sofia daniel diego miguel gabriel fernando alejandro mariana valeria camila lucia paola laura sara perro gato casa luna sol estrella cielo mar playa flor rosa azul rojo verde negro blanco amigo amiga mejor vida feliz bonito bonita tigre leon lobo oso dragon batman superman goku naruto minecraft fortnite roblox youtube tiktok instagram facebook whatsapp celular telefono internet computadora teclado mouse juego juegos musica rock pizza taco tacos burrito helado pastel dulce chocolate cafe leche pan agua fuego tierra viento universo mundo planeta ciudad pueblo calle escuelita club equipo campeon ganador fuerte rapido grande chico nuevo viejo siempre nunca todo nada quiero amo odio mama papa hermano hermana novio novia gordo flaco loco loca bueno buena malo mala dame vamos vive vida corazon cielo noche dia tarde manana semana lunes martes jueves viernes sabado domingo enero marzo abril mayo junio julio agosto octubre noviembre diciembre qwerty asdf zxcv abc abcd uno dos tres cuatro cinco seis siete ocho nueve diez cero gimnasio socio pago huella torniquete iloveyou love football soccer dragon monkey shadow master hello welcome login letmein sunshine princess".split(" ");
var PWK={};PWW.forEach(function(w){PWK[w]=1});
function pwEst(p){var m={"4":"a","3":"e","1":"i","0":"o","5":"s","7":"t","@":"a","$":"s","!":"i"},q=p.toLowerCase().replace(/[áàä]/g,"a").replace(/[éèë]/g,"e").replace(/[íìï]/g,"i").replace(/[óòö]/g,"o").replace(/[úùü]/g,"u").replace(/ñ/g,"n"),L=q.length,
 best=[0],from=[],i,j,caps=(p.match(/[A-Z]/g)||[]).length,fc=caps==1&&/^[A-Z]/.test(p),pool=(/[a-zñáéíóú]/.test(p)?26:0)+(caps&&!fc?26:0)+(/[0-9]/.test(p)?10:0)+(/[^A-Za-z0-9ñáéíóúÁÉÍÓÚÑ]/.test(p)?33:0),pc=Math.log(pool||26)/Math.LN2;for(i=1;i<=L;i++){best[i]=best[i-1]+pc;from[i]=[i-1,""];for(j=Math.max(0,i-12);j<=i-3;j++){var seg=q.substring(j,i),dl=seg.replace(/[43105@$!7]/g,function(x){return m[x]}),w=PWK[seg]?seg:PWK[dl]?dl:null;if(w){var lt=(w!==seg?1:0),c2=best[j]+13+lt;if(c2<best[i]){best[i]=c2;from[i]=[j,w]}}}
  if(i>=4){var yr=q.substring(i-4,i);if(/^(19|20)\d\d$/.test(yr)&&best[i-4]+7<best[i]){best[i]=best[i-4]+7;from[i]=[i-4,"#"]}}}
 var words=[];i=L;while(i>0){var f=from[i];if(f[1]&&f[1]!="#")words.push(f[1]);i=f[0]}
 var bits=best[L];if(fc)bits+=1
 if(/(.)\1{2,}/.test(q))bits-=6;if(/(012|123|234|345|456|567|678|789|abc|bcd|cde|def)/.test(q))bits-=5;if(bits<4)bits=4;
 return {bits:bits,words:words}}
function pwInit(d){var w=d.querySelector(".pwx");if(!w)return;var x=w.querySelector(".pwi"),bar=w.querySelector(".pm i"),lab=w.querySelector(".pl"),tips=w.querySelector(".tips"),seen={},strong=0;
 x.oninput=function(){var p=x.value;if(!p){bar.style.width="0";lab.textContent="Escribe algo para empezar.";tips.innerHTML="";w.querySelector(".p1").textContent="—";w.querySelector(".p2").textContent="—";w.querySelector(".p3").textContent="—";return}
  var lo=/[a-z]/.test(p),up=/[A-Z]/.test(p),di=/[0-9]/.test(p),sy=/[^A-Za-z0-9]/.test(p),pe=pwEst(p),bits=pe.bits,common=PWC.indexOf(p.toLowerCase())>-1;
  if(common)bits=Math.min(bits,8);var secs=Math.pow(2,bits)/2/1e10,lvl=bits<30?0:bits<42?1:bits<56?2:3,names=["Muy débil","Débil","Aceptable","Fuerte"],cols=["var(--bad)","var(--amb)","var(--pri)","var(--ok)"];
  bar.style.width=[15,40,70,100][lvl]+"%";bar.style.background=cols[lvl];lab.textContent=names[lvl]+(common?" · está en las listas de contraseñas más comunes":"");
  w.querySelector(".p1").textContent=p.length+" caracteres";w.querySelector(".p2").textContent=[lo&&"minúsculas",up&&"MAYÚSCULAS",di&&"números",sy&&"símbolos"].filter(Boolean).join(", ")||"—";w.querySelector(".p3").textContent=pwTime(secs);
  var t=[];if(p.length<12)t.push("Hazla más larga: <b>la longitud pesa más que los símbolos raros</b>. Apunta a 12 o más caracteres.");if(!up&&!lo)t.push("Mezcla letras con números.");if(pe.words.length)t.push("Contiene la palabra «"+pe.words[pe.words.length-1]+"»: los atacantes prueban primero palabras de diccionario, aunque cambies letras por números o uses mayúsculas.");if(common)t.push("Nunca uses contraseñas comunes ni tu nombre, tu fecha de nacimiento o tu equipo favorito.");if(lvl>=2&&p.length>=12)t.push("Una frase larga de varias palabras sin relación es fácil de recordar y difícil de adivinar.");if(lvl==3)t.push("✅ Es fuerte. Aun así, usa una distinta para cada cuenta y activa la verificación en dos pasos.");
  tips.innerHTML=t.map(function(s){return "<li>"+s+"</li>"}).join("");
  if(lvl==3&&!seen[p]){seen[p]=1;strong++;w.querySelector(".p4").textContent=strong;if(strong>=1){var k="t:Medidor de contraseñas";if(!ST[k]){ST[k]=1;sv()}}}}}
'''
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n phInit(d);pwInit(d);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('💪', 'Tu información también vale oro', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'La <b>ciberseguridad</b> es el conjunto de formas de proteger la información, los equipos y los servicios digitales de quien quiera robarlos, cambiarlos o dejarlos sin funcionar. Tú ya la usas: el bloqueo de tu celular, la contraseña de tu cuenta, no abrir un enlace raro.'),
    ex('Caso de las lecciones: Gimnasio Fuerza Joven', 'Guarda nombres, teléfonos y pagos de 400 socios, usa un torniquete con huella digital, ofrece wifi y publica promociones en redes sociales. Un día alguien roba la lista de socios y empiezan los mensajes falsos de «cobro». Vamos a entender qué pasó y cómo evitarlo.'),
    bk('Qué vas a hacer', '<b>1. Aprende</b> los conceptos con ejemplos. <b>2. Diagnostica</b> con dos herramientas: un detective de phishing y un medidor de contraseñas. <b>3. Construye</b> tres prácticas que te preparan para tu presentación.'),
    bk('Al final', 'Entregas una <b>presentación electrónica</b> (20 %) sobre el caso que te asigna la plataforma en la actividad de evaluación.')),
    'Proteger lo digital es cuidar a las personas que están detrás.')
c.A('🔎', '¿Amenaza, vulnerabilidad o riesgo?', 'Clasifica cada frase del caso del gimnasio.', [
    ['La lista de socios está en una hoja de cálculo sin contraseña', 'Vulnerabilidad', 'Es una debilidad que alguien podría aprovechar.'],
    ['Un desconocido intenta entrar a la computadora de recepción', 'Amenaza', 'Es quien o lo que puede causar el daño.'],
    ['Que se filtren los datos de 400 socios y los usen para fraudes', 'Riesgo', 'Es el daño posible cuando la amenaza aprovecha la vulnerabilidad.'],
    ['La recepcionista pega su contraseña en el monitor', 'Vulnerabilidad', 'Es una debilidad en la forma de trabajar.'],
    ['Un virus que llega por un correo falso', 'Amenaza', 'Puede dañar los equipos.'],
], 'Amenaza = lo que puede dañar · Vulnerabilidad = la debilidad · Riesgo = la posibilidad del daño.', ['Amenaza', 'Vulnerabilidad', 'Riesgo'])
s0_end = c.mark() - 1

# ───────────────────────── A · Ciberseguridad ─────────────────────────
a0 = c.mark()
c.L('🛡️', '¿Qué es la ciberseguridad?', 'Bloque A · Concepto', body(
    sp('En palabras sencillas', 'Es proteger <b>información, dispositivos, servicios y redes</b> contra daños accidentales o intencionales. No se logra con una sola herramienta: combina tres cosas.'),
    r3([('👥', 'Personas', 'Saben qué hacer y qué evitar'), ('📋', 'Procesos', 'Reglas y pasos claros'), ('💻', 'Tecnología', 'Antivirus, firewall, cifrado')]),
    ana('Piensa en…', 'Tu casa: de nada sirve una puerta blindada (tecnología) si todos dejan la llave en la maceta (personas) y nadie sabe qué hacer si suena la alarma (procesos).'),
    ex('En el gimnasio', 'Tecnología: antivirus y contraseña en la computadora. Procesos: quién puede ver los pagos. Personas: que los empleados reconozcan un correo falso.')),
    'Personas + procesos + tecnología: si falla una, se debilitan las demás.')
c.L('🕵️', 'Delincuencia cibernética', 'Bloque A · Quién ataca y por qué', body(
    sp('En palabras sencillas', 'Un <b>delito cibernético</b> es cualquier delito que se comete usando computadoras o redes, o que las tiene como objetivo: fraude, robo de datos, extorsión, suplantación de identidad.'),
    bk('¿Qué buscan?', '<b>Dinero</b> (fraudes, ransomware), <b>datos</b> (para venderlos o suplantarte), <b>causar daño</b> o llamar la atención.'),
    bk('¿Quiénes atacan?', 'Aficionados que prueban herramientas · delincuentes organizados que lo hacen como negocio · «hacktivistas» que atacan por una causa · personas dentro de la organización · y, a gran escala, grupos apoyados por gobiernos.'),
    ex('Dato cercano', 'En México la <b>Policía Cibernética</b> y la Guardia Nacional reciben reportes de fraudes y suplantación de identidad. Reportar ayuda a que otros no caigan.'),
    warn('Recuerda', 'Nadie está «demasiado chico» para ser blanco: los delincuentes atacan en masa y esperan que alguien caiga.')),
    'Casi siempre buscan dinero o datos que se pueden convertir en dinero.')
c.L('🚪', 'Amenazas internas y externas', 'Bloque A · De dónde viene el problema', body(
    sp('Amenaza externa', 'Viene de <b>fuera</b> de la organización: un atacante en internet, un virus, un robo.'),
    sp('Amenaza interna', 'Viene de alguien con <b>acceso legítimo</b> o cercano: un empleado, un alumno, un proveedor. Puede ser <b>intencional</b> (venganza, dinero) o <b>accidental</b> (se equivoca o cae en un engaño).'),
    ana('Piensa en…', 'Un robo a tu casa: el externo rompe la ventana; el interno es alguien que ya tiene llave, a propósito o porque la perdió.'),
    ex('En el gimnasio', 'Un instructor se lleva la lista de socios al irse a otro gimnasio (interna, intencional). Otro empleado envía por error el archivo de pagos a un grupo de WhatsApp (interna, accidental). Un atacante entra por el wifi (externa).'),
    bk('Dato importante', 'Muchos incidentes empiezan por un error humano. Por eso la capacitación es una medida de seguridad.')),
    'Interna = con acceso legítimo · Externa = desde fuera · Ambas pueden ser accidentales o a propósito.')
c.A('🚪', '¿Interna o externa?', 'Clasifica cada amenaza del gimnasio.', [
    ['Una hacker en otro país prueba contraseñas en la página de socios', 'Externa', 'Viene de fuera y no tiene acceso legítimo.'],
    ['Un empleado despedido se queda con su cuenta de administrador activa y borra archivos', 'Interna', 'Tenía acceso legítimo y lo usó mal.'],
    ['Una recepcionista abre sin querer un archivo infectado', 'Interna', 'Es una amenaza interna accidental.'],
    ['Un virus que se propaga por internet y llega al correo del gimnasio', 'Externa', 'Se origina fuera de la organización.'],
    ['Un instructor presta su contraseña a un amigo', 'Interna', 'Alguien con acceso legítimo lo comparte.'],
], 'Pregúntate: ¿quién empezó el problema tiene acceso legítimo?', ['Interna', 'Externa'])
c.L('🕳️', 'Vulnerabilidades', 'Bloque A · Las debilidades', body(
    sp('En palabras sencillas', 'Una <b>vulnerabilidad</b> es una debilidad que una amenaza puede aprovechar. Sola no hace daño; el daño llega cuando alguien la usa.'),
    bk('Humanas', 'Contraseñas débiles, caer en engaños, no avisar de algo raro.'),
    bk('Técnicas', 'Programas sin actualizar, fallas del software, equipos sin antivirus.'),
    bk('De configuración', 'Dejar la contraseña de fábrica del módem, permisos de más, wifi abierto.'),
    bk('Físicas', 'Cuarto de equipos sin llave, laptops sin candado, USB desconocidos conectados.'),
    ex('La fórmula', '<b>Riesgo = amenaza que aprovecha una vulnerabilidad → impacto</b>. Si quitas la vulnerabilidad (por ejemplo, actualizas el programa), el riesgo baja aunque la amenaza siga existiendo.')),
    'No puedes controlar a todos los atacantes, pero sí cerrar tus vulnerabilidades.')
c.A('🕳️', '¿Qué tipo de vulnerabilidad es?', 'Clasifica cada debilidad del gimnasio.', [
    ['El módem usa la contraseña que traía de fábrica', 'De configuración', 'Está mal configurado y es fácil de adivinar.'],
    ['La computadora de recepción no se actualiza desde hace un año', 'Técnica', 'El software tiene fallas conocidas sin corregir.'],
    ['El cuarto donde está el servidor se queda abierto', 'Física', 'Cualquiera puede acercarse al equipo.'],
    ['Un empleado hace clic en cualquier enlace que le llega', 'Humana', 'Depende de las decisiones de una persona.'],
    ['Una contraseña igual para todas las cuentas', 'Humana', 'Es un mal hábito de las personas.'],
], 'Persona → humana · Software → técnica · Ajustes → configuración · Lugar → física.', ['Humana', 'Técnica', 'De configuración', 'Física'])
c.L('🧑‍💻', 'Especialistas y certificaciones', 'Bloque A · Trabajar en ciberseguridad', body(
    sp('En palabras sencillas', 'Hay muchos puestos. Algunos ejemplos: <b>analista de seguridad</b> (vigila alertas), <b>pentester</b> (ataca con permiso para encontrar fallas), <b>analista forense</b> (investiga qué pasó), <b>administrador de seguridad</b> y <b>oficial de seguridad de la información</b>.'),
    bk('Certificaciones comunes', '<b>Cisco</b> (CCNA, CyberOps) · <b>CompTIA</b> (Security+) · <b>ISC2</b> (SSCP, CISSP) · <b>EC-Council</b> (CEH). Una certificación comprueba que dominas ciertos conocimientos.'),
    ex('Para empezar', 'Cisco Networking Academy tiene cursos gratuitos de ciberseguridad (en el CONALEP los usan). Aprender redes y sistemas operativos es la base de casi todo.'),
    bk('Lo que más se pide', 'Curiosidad, ética, ganas de aprender y buena comunicación: explicar un riesgo en palabras claras es parte del trabajo.')),
    'Una carrera en ciberseguridad empieza con redes, sistemas y mucha práctica.')
c.O('🧭', 'Ordena la cadena del riesgo', 'Pon en orden cómo se llega a un daño.', [
    ['Existe una vulnerabilidad: la lista de socios no tiene contraseña', 'Primero está la debilidad.'],
    ['Aparece una amenaza: alguien con malas intenciones la encuentra', 'La amenaza detecta la debilidad.'],
    ['La amenaza aprovecha la vulnerabilidad y accede a los datos', 'Se produce el incidente.'],
    ['Se genera el impacto: fraudes con los datos de los socios', 'Es el daño que sufre la organización.'],
], 'Vulnerabilidad → amenaza → aprovechamiento → impacto.')
c.Z('📌', 'Completa las ideas clave', 'Elige la palabra correcta en cada frase.',
    '<p>La ciberseguridad combina personas, {0} y tecnología.</p>'
    '<p>Una {1} es una debilidad que puede ser aprovechada.</p>'
    '<p>Un empleado con acceso legítimo que se equivoca es una amenaza {2}.</p>'
    '<p>El {3} es la posibilidad de daño cuando una amenaza aprovecha una vulnerabilidad.</p>',
    [['procesos', ['procesos', 'virus', 'contraseñas']],
     ['vulnerabilidad', ['vulnerabilidad', 'amenaza', 'certificación']],
     ['interna', ['interna', 'externa', 'física']],
     ['riesgo', ['riesgo', 'hash', 'firewall']]],
    'Persona + proceso + tecnología · Debilidad = vulnerabilidad.')
a_end = c.mark() - 1

# ───────────────────────── B · Principios de seguridad ─────────────────────────
b0 = c.mark()
c.L('🔒', 'Confidencialidad y control de acceso', 'Bloque B · Que solo vea quien debe', body(
    sp('Confidencialidad', 'Que la información sea vista <b>solo por quien está autorizado</b>.'),
    sp('Control de acceso', 'Las reglas que deciden <b>quién puede entrar, ver o cambiar qué</b>.'),
    ana('Piensa en…', 'Tu mochila: solo tú decides a quién le enseñas lo que hay adentro.'),
    ex('En el gimnasio', 'La recepcionista ve nombres y teléfonos; solo la administradora ve los pagos con tarjeta. Si un instructor viera los pagos, se rompería la confidencialidad.'),
    bk('Cómo se logra', 'Cuentas personales, permisos, contraseñas, cifrado y ocultamiento de datos.')),
    'Confidencialidad = secreto; control de acceso = las llaves.')
c.L('✅', 'Integridad', 'Bloque B · Que no se cambie sin permiso', body(
    sp('En palabras sencillas', 'Que la información sea <b>exacta y no se altere sin autorización</b>, ni por error ni a propósito.'),
    ex('En el gimnasio', 'Si alguien cambia la fecha de vencimiento de una membresía para no pagar, se rompió la integridad. Si por una falla el nombre de un socio queda mal escrito en toda la base, también.'),
    bk('Cómo se protege', 'Permisos de solo lectura, registros de cambios (bitácoras), respaldos y comprobaciones como el hash que viste en R.A. 2.2.')),
    'Integridad = que los datos sigan siendo correctos.')
c.L('⏱️', 'Disponibilidad', 'Bloque B · Que funcione cuando se necesita', body(
    sp('En palabras sencillas', 'Que la información y los servicios estén <b>accesibles cuando se necesitan</b>.'),
    ex('En el gimnasio', 'Si el torniquete deja de funcionar a las 6 de la mañana, nadie entra: se afectó la disponibilidad. Puede pasar por una falla de luz, un ataque que satura el sistema o un virus.'),
    bk('Cómo se protege', 'Respaldos, equipo de repuesto, no-break y planes de recuperación (en el R.A. 2.2 verás RPO y RTO).')),
    'Disponibilidad = que sirva a tiempo.')
c.A('🔺', '¿Qué principio se afecta?', 'Elige el principio que se daña en cada situación del gimnasio.', [
    ['Un cliente lee la lista de pagos sin permiso', 'Confidencialidad', 'Alguien no autorizado vio información privada.'],
    ['Alguien modifica el monto de una mensualidad pagada', 'Integridad', 'El dato fue cambiado sin autorización.'],
    ['El sistema de cobro no abre durante todo el día', 'Disponibilidad', 'El servicio no funciona cuando se necesita.'],
    ['Se publican por error los teléfonos de los socios en redes', 'Confidencialidad', 'Información privada llegó a quien no debía.'],
    ['Un virus borra registros de asistencia', 'Integridad', 'Los datos dejaron de ser correctos (también afecta disponibilidad).'],
    ['Un ataque satura la página de inscripción y nadie puede entrar', 'Disponibilidad', 'El servicio se vuelve inaccesible.'],
], 'Secreto → confidencialidad · Sin cambios → integridad · A tiempo → disponibilidad.', ['Confidencialidad', 'Integridad', 'Disponibilidad'])
c.L('💾', 'Estado de los datos', 'Bloque B · Dónde están los datos', body(
    sp('En palabras sencillas', 'Los datos se protegen distinto según <b>dónde están</b>.'),
    r3([('🗄️', 'En reposo', 'Guardados en un disco o la nube'), ('📡', 'En tránsito', 'Viajan por una red'), ('⚙️', 'En proceso', 'Se usan en memoria')]),
    bk('En reposo', 'Se protegen con cifrado del disco, permisos y respaldos.'),
    bk('En tránsito', 'Se protegen con conexiones cifradas: HTTPS, VPN, wifi con WPA2 o WPA3.'),
    bk('En proceso', 'Se protegen con programas actualizados, cuentas sin privilegios y bloqueo de pantalla.'),
    ex('En el gimnasio', 'La base de socios guardada en la computadora está <b>en reposo</b>. Cuando la recepcionista la envía por correo está <b>en tránsito</b>. Cuando la abre para cobrar está <b>en proceso</b>.')),
    'Reposo = guardados · Tránsito = viajando · Proceso = en uso.')
c.A('💾', '¿En qué estado están los datos?', 'Clasifica cada caso.', [
    ['Los pagos guardados en el disco duro del servidor', 'En reposo', 'Están almacenados.'],
    ['La foto de un socio que se envía por WhatsApp', 'En tránsito', 'Viaja por la red.'],
    ['La hoja de socios abierta en pantalla mientras se edita', 'En proceso', 'Se está usando en memoria.'],
    ['El respaldo en una memoria USB guardada en un cajón', 'En reposo', 'Está almacenado fuera de uso.'],
    ['El pago con tarjeta que viaja de la terminal al banco', 'En tránsito', 'Va de un punto a otro.'],
], 'Guardado = reposo · Moviéndose = tránsito · Usándose = proceso.', ['En reposo', 'En tránsito', 'En proceso'])
c.L('🧰', 'Contramedidas', 'Bloque B · Qué hacer para protegerse', body(
    sp('En palabras sencillas', 'Una <b>contramedida</b> (o control) es cualquier cosa que reduce un riesgo. Se agrupan por <b>cuándo actúan</b>.'),
    bk('Preventivas', 'Evitan que pase: contraseñas fuertes, permisos, capacitación, actualizaciones.'),
    bk('Detectivas', 'Avisan cuando ya está pasando: alertas, cámaras, bitácoras.'),
    bk('Correctivas', 'Reparan y recuperan: restaurar un respaldo, eliminar el virus, cambiar contraseñas.'),
    ana('Piensa en…', 'Preventiva: cerrar con llave. Detectiva: la alarma. Correctiva: llamar al seguro y reparar la cerradura.')),
    'Prevenir · detectar · corregir.')
c.A('🧰', '¿Preventivo, detectivo o correctivo?', 'Clasifica cada control del gimnasio.', [
    ['Exigir contraseñas de 12 caracteres', 'Preventivo', 'Evita que adivinen la contraseña.'],
    ['Una alerta cuando alguien intenta entrar 10 veces con contraseña incorrecta', 'Detectivo', 'Avisa que algo está pasando.'],
    ['Restaurar el respaldo después de un virus', 'Correctivo', 'Recupera lo perdido.'],
    ['Capacitar al personal sobre correos falsos', 'Preventivo', 'Reduce el riesgo antes de que pase.'],
    ['Revisar las cámaras para saber quién entró al cuarto de equipos', 'Detectivo', 'Ayuda a descubrir lo ocurrido.'],
    ['Cambiar todas las contraseñas tras un robo de datos', 'Correctivo', 'Reduce las consecuencias del incidente.'],
], 'Antes → preventivo · Durante → detectivo · Después → correctivo.', ['Preventivo', 'Detectivo', 'Correctivo'])
c.L('📐', 'Modelos y marco de trabajo', 'Bloque B · Formas de organizar la seguridad', body(
    sp('Tríada CIA', 'El modelo base: <b>C</b>onfidencialidad, <b>I</b>ntegridad y <b>D</b>isponibilidad (en inglés, CIA). Casi todo lo demás se explica con estos tres principios.'),
    sp('Marco de trabajo (NIST CSF)', 'Un <b>marco</b> es una guía ordenada para organizar la seguridad. El del NIST (EE. UU.) se usa en todo el mundo y tiene seis funciones: <b>Gobernar, Identificar, Proteger, Detectar, Responder y Recuperar</b>.'),
    bk('Cómo se leen', 'Gobernar: definir reglas y responsables · Identificar: saber qué tienes y qué riesgos hay · Proteger: aplicar controles · Detectar: darte cuenta a tiempo · Responder: actuar ante el incidente · Recuperar: volver a la normalidad.'),
    ex('En el gimnasio', 'Identificar: lista de equipos y datos. Proteger: contraseñas y cifrado. Detectar: alertas. Responder: apagar la computadora infectada. Recuperar: restaurar el respaldo.'),
    bk('Otros marcos', 'ISO/IEC 27001 (certificación de seguridad de la información) y los controles CIS. Se usan cuando una organización necesita demostrar que se protege bien.')),
    'Un marco sirve para no improvisar la seguridad.')
c.A('📐', '¿Qué función del marco es?', 'Relaciona cada acción con la función del marco NIST.', [
    ['Hacer la lista de computadoras y datos del gimnasio', 'Identificar', 'Saber qué se debe proteger.'],
    ['Instalar antivirus y activar el cifrado del disco', 'Proteger', 'Aplicar controles.'],
    ['Revisar las alertas del sistema cada mañana', 'Detectar', 'Darse cuenta a tiempo de lo que ocurre.'],
    ['Desconectar de la red el equipo infectado', 'Responder', 'Actuar durante el incidente.'],
    ['Restaurar los datos desde el respaldo', 'Recuperar', 'Volver a la operación normal.'],
    ['Definir quién es responsable de la seguridad', 'Gobernar', 'Establecer reglas y responsables.'],
], 'Gobernar · Identificar · Proteger · Detectar · Responder · Recuperar.', ['Gobernar', 'Identificar', 'Proteger', 'Detectar', 'Responder', 'Recuperar'])
c.W('✍️', 'Explica los tres principios', 'Aplica lo aprendido.',
    'Con el gimnasio como ejemplo, explica con tus palabras <b>confidencialidad</b>, <b>integridad</b> y <b>disponibilidad</b>, con un ejemplo de cada una.',
    [['Tiene al menos 30 palabras', 'palabras:30'],
     ['Explica la confidencialidad', '(confidencialidad|secreto|privad|autorizad|solo.*(ver|acceso))'],
     ['Explica la integridad', '(integridad|alter|modific|cambi|correct|exact)'],
     ['Explica la disponibilidad', '(disponibilidad|disponible|funcion|acces|cuando se necesita)'],
     ['Incluye al menos un ejemplo', '(ejemplo|por ejemplo|como cuando|si alguien|si un)']],
    'Una o dos oraciones por principio.', 'Ejemplo: Confidencialidad: solo la administradora ve los pagos. Integridad: …')
b_end = c.mark() - 1

# ───────────────────────── C · Amenazas, vulnerabilidades y ataques ─────────────────────────
c0 = c.mark()
c.L('🦠', 'Malware: el software dañino', 'Bloque C · Tipos de malware', body(
    sp('En palabras sencillas', '<b>Malware</b> es cualquier programa hecho para dañar, espiar o aprovecharse de un equipo.'),
    bk('Virus', 'Se pega a un archivo o programa y se copia cuando lo abres.'),
    bk('Gusano', 'Se copia solo por la red, sin que nadie abra nada.'),
    bk('Troyano', 'Parece un programa útil (un juego, un «crack») pero esconde algo malo.'),
    bk('Ransomware', '<b>Cifra tus archivos</b> y pide dinero (rescate) para devolverlos.'),
    bk('Spyware y keylogger', 'Espían lo que haces; el keylogger guarda lo que tecleas, como tus contraseñas.'),
    bk('Adware', 'Llena de anuncios o instala cosas sin que lo pidas.'),
    bk('Rootkit', 'Se esconde muy hondo en el sistema para que no lo vean ni los antivirus.'),
    warn('Ojo', 'Pagar el rescate no garantiza recuperar los archivos. Lo mejor es tener respaldos.')),
    'Cada malware tiene un objetivo: copiarse, engañar, espiar o secuestrar.')
c.A('🦠', '¿Qué tipo de malware es?', 'Clasifica cada caso del gimnasio.', [
    ['Una pantalla dice que tus archivos están cifrados y pide un pago', 'Ransomware', 'Cifra los archivos y exige rescate.'],
    ['Un programa «para descargar música gratis» que además roba contraseñas', 'Troyano', 'Parece útil pero esconde algo dañino.'],
    ['Un programa que guarda todo lo que escribe la recepcionista', 'Keylogger', 'Registra las teclas, incluso contraseñas.'],
    ['Aparecen anuncios por todas partes y cambió la página de inicio', 'Adware', 'Muestra anuncios sin permiso.'],
    ['Se copia solo por todas las computadoras de la red', 'Gusano', 'Se propaga por la red sin intervención.'],
], 'Rescate → ransomware · Parece útil → troyano · Teclas → keylogger · Anuncios → adware · Se copia solo → gusano.', ['Ransomware', 'Troyano', 'Keylogger', 'Adware', 'Gusano'])
c.L('📜', 'Código malicioso', 'Bloque C · Más allá de los virus', body(
    sp('En palabras sencillas', 'Además de programas completos, el daño puede venir de pequeños pedazos de código que se esconden en otras cosas.'),
    bk('Macros', 'Instrucciones dentro de un documento de Office. Si abres un archivo y te piden «habilitar contenido», cuidado.'),
    bk('Scripts', 'Pequeños programas en páginas web o archivos que se ejecutan solos.'),
    bk('Puertas traseras', 'Una entrada secreta que deja un atacante para volver cuando quiera.'),
    bk('Bombas lógicas', 'Código dormido que se activa con una fecha o un evento, por ejemplo cuando se borra a un usuario.'),
    ex('En el gimnasio', 'Llega un correo con una hoja de «Rutinas.xlsm» que pide habilitar macros. Al hacerlo, un código descarga un programa dañino. La regla: <b>nunca habilites contenido de un archivo que no esperabas</b>.')),
    'Un documento también puede esconder código dañino.')
c.L('🎭', 'Trucos: la ingeniería social', 'Bloque C · Engañar a las personas', body(
    sp('En palabras sencillas', 'La <b>ingeniería social</b> engaña a las personas (no a las máquinas) para que entreguen datos o hagan algo peligroso. Es el truco más usado porque <b>es más fácil engañar a alguien que romper un sistema</b>.'),
    bk('Phishing', 'Correo o mensaje falso que imita a una empresa para que des datos o hagas clic.'),
    bk('Smishing y vishing', 'Lo mismo pero por <b>SMS</b> (smishing) o por <b>llamada</b> (vishing).'),
    bk('Pretexting', 'Inventan una historia: «soy de soporte técnico y necesito tu contraseña».'),
    bk('Baiting', 'Dejan un «cebo»: una USB tirada en el estacionamiento con la etiqueta «Nóminas».'),
    bk('Tailgating', 'Se cuelan detrás de ti por una puerta con acceso controlado.'),
    ana('Señales de alerta', '<b>Urgencia</b> · <b>miedo o premio</b> · <b>pide datos secretos</b> · <b>enlaces o remitentes raros</b> · <b>faltas o tono extraño</b>.')),
    'Si algo te mete prisa o miedo, para y verifica por otro medio.')
c.raw('pPhish()')
c.A('🎭', '¿Qué truco es?', 'Clasifica cada situación.', [
    ['Te llega un SMS: «Tu paquete está retenido, paga aquí 20 pesos»', 'Smishing', 'Phishing por mensaje de texto.'],
    ['Alguien llama diciendo ser del banco y te pide el código que te llegó', 'Vishing', 'Engaño por llamada telefónica.'],
    ['Encuentras una USB en el pasillo con la etiqueta «Fotos de la fiesta» y la conectas', 'Baiting', 'Es un cebo para que la conectes.'],
    ['Un desconocido con una caja entra pegado a ti a la zona de acceso controlado', 'Tailgating', 'Se cuela detrás de una persona autorizada.'],
    ['Un correo idéntico al de tu banco con un enlace falso', 'Phishing', 'Imita a una empresa para robar datos.'],
], 'Mensaje de texto → smishing · Llamada → vishing · USB cebo → baiting · Se cuela → tailgating · Correo falso → phishing.', ['Phishing', 'Smishing', 'Vishing', 'Baiting', 'Tailgating'])
c.L('⚔️', 'Ciberataques', 'Bloque C · Ataques frecuentes', body(
    sp('En palabras sencillas', 'Un <b>ciberataque</b> es un intento deliberado de dañar, robar o dejar sin servicio un sistema o una red.'),
    bk('Denegación de servicio (DoS / DDoS)', 'Se manda tanto tráfico que el servicio se satura y nadie lo puede usar. <b>DDoS</b> = desde muchos equipos a la vez. Afecta la disponibilidad.'),
    bk('Hombre en el medio', 'El atacante se coloca entre tú y el sitio para leer o cambiar lo que se envía, por ejemplo en un wifi público falso.'),
    bk('Ataques a contraseñas', '<b>Fuerza bruta</b>: prueba todas las combinaciones. <b>Diccionario</b>: prueba palabras y contraseñas comunes.'),
    bk('Inyección SQL', 'Escribir instrucciones en un formulario para que la base de datos entregue o cambie información que no debería.'),
    bk('Día cero (zero-day)', 'Ataque que usa una falla que todavía nadie había corregido.'),
    warn('Wifi público', 'Evita entrar a tu banco o escribir contraseñas en una red abierta de un lugar público.')),
    'Cada ataque apunta a uno de los tres principios: secreto, exactitud o servicio.')
c.A('⚔️', '¿Qué ataque es?', 'Relaciona cada situación con el ataque.', [
    ['Un millón de peticiones falsas tumban la página de inscripción del gimnasio', 'Denegación de servicio', 'Satura el servicio para que nadie lo use.'],
    ['Un atacante prueba la lista de las 1,000 contraseñas más comunes', 'Ataque de diccionario', 'Prueba palabras y contraseñas comunes.'],
    ['Un wifi gratis falso en la plaza lee lo que envías', 'Hombre en el medio', 'El atacante se interpone en la comunicación.'],
    ['Escribe una instrucción rara en el formulario de acceso y la base de datos responde con todos los socios', 'Inyección SQL', 'Engaña a la base de datos con instrucciones.'],
    ['Prueba todas las combinaciones posibles de 4 dígitos de un NIP', 'Fuerza bruta', 'Prueba todas las combinaciones.'],
], 'Saturar → DoS · Palabras comunes → diccionario · Interponerse → hombre en el medio · Formulario → SQL · Todas las combinaciones → fuerza bruta.', ['Denegación de servicio', 'Ataque de diccionario', 'Hombre en el medio', 'Inyección SQL', 'Fuerza bruta'])
c.O('🚨', 'Ordena: qué hacer si caes en phishing', 'Hiciste clic en un enlace falso del «banco» y escribiste tu contraseña. Ordena las acciones.', [
    ['Cambia de inmediato la contraseña desde la página oficial', 'Lo primero es cerrar la puerta que abriste.'],
    ['Si usabas esa contraseña en otros sitios, cámbiala también', 'La gente reutiliza contraseñas y los atacantes las prueban en todas partes.'],
    ['Activa la verificación en dos pasos', 'Aunque tengan la contraseña, no podrán entrar sin el segundo factor.'],
    ['Revisa los movimientos de tu cuenta y avisa al banco si hay algo raro', 'Hay que detectar si ya hubo daño.'],
    ['Reporta el correo falso y cuéntale a tu familia o a tu profe', 'Avisar evita que otros caigan.'],
], 'Cerrar · extender · reforzar · revisar · avisar.')
c_end = c.mark() - 1

# ───────────────────────── D · Protección y seguridad ─────────────────────────
d0 = c.mark()
c.L('🔐', 'Criptografía y encriptación', 'Bloque D · Esconder el mensaje', body(
    sp('En palabras sencillas', 'La <b>criptografía</b> es la ciencia de proteger información con matemáticas. <b>Encriptar (cifrar)</b> es convertir un mensaje legible en uno ilegible con una <b>clave</b>; <b>descifrar</b> es regresarlo a su forma original.'),
    bk('Simétrica', 'Usa <b>la misma clave</b> para cifrar y descifrar. Es rápida (por ejemplo AES). Problema: ¿cómo le mandas la clave sin que la intercepten?'),
    bk('Asimétrica', 'Usa <b>dos claves</b>: la pública cifra y la privada descifra (RSA). Resuelve el problema de compartir la clave.'),
    ana('Piensa en…', 'Simétrica: un candado con una sola llave que copias para tu amigo. Asimétrica: un buzón: cualquiera mete cartas (clave pública), pero solo tú tienes la llave para abrirlo (clave privada).'),
    ex('En tu vida', 'El candado del navegador (HTTPS) usa las dos: la asimétrica para ponerse de acuerdo y la simétrica para viajar rápido. WhatsApp cifra tus mensajes de extremo a extremo.'),
    warn('Recuerda', 'Cifrar protege la confidencialidad, pero si pierdes la clave pierdes los datos.')),
    'Misma clave = simétrica · Clave pública y privada = asimétrica.')
c.A('🔐', '¿Simétrica o asimétrica?', 'Clasifica cada situación.', [
    ['Una sola clave que comparten quien cifra y quien descifra', 'Simétrica', 'La misma clave hace las dos tareas.'],
    ['Cualquiera puede cifrar con tu clave pública, solo tú descifras con la privada', 'Asimétrica', 'Usa un par de claves distintas.'],
    ['AES para cifrar rápido el disco del gimnasio', 'Simétrica', 'AES es un algoritmo simétrico.'],
    ['RSA para intercambiar claves por internet', 'Asimétrica', 'RSA usa clave pública y privada.'],
], 'Una clave → simétrica · Dos claves → asimétrica.', ['Simétrica', 'Asimétrica'])
c.L('🪪', 'Autenticación, autorización y control de acceso', 'Bloque D · Quién eres y qué puedes hacer', body(
    sp('Autenticación', 'Comprobar <b>quién eres</b>.'),
    sp('Autorización', 'Decidir <b>qué puedes hacer</b> una vez que ya te identificaron.'),
    bk('Factores de autenticación', '<b>Algo que sabes</b> (contraseña, NIP) · <b>algo que tienes</b> (celular, tarjeta, llave) · <b>algo que eres</b> (huella, rostro). Usar <b>dos o más</b> es la <b>verificación en dos pasos</b> o autenticación multifactor (MFA).'),
    bk('Mínimo privilegio', 'Dar solo los permisos necesarios para el trabajo, ni uno más.'),
    bk('Las tres A', '<b>Autenticar</b> (¿quién eres?) → <b>Autorizar</b> (¿qué puedes hacer?) → <b>Auditar</b> (registrar lo que hiciste).'),
    ex('En el gimnasio', 'Socio: entra al torniquete con su huella (algo que eres). Recepcionista: usuario y contraseña, más un código al celular (algo que sabes y algo que tienes). Solo la administradora puede ver los pagos (autorización).')),
    'Autenticar = identidad · Autorizar = permisos · Auditar = registro.')
c.A('🪪', '¿Autenticación o autorización?', 'Decide qué es cada acción.', [
    ['Escribir usuario y contraseña para entrar al sistema', 'Autenticación', 'Comprueba quién eres.'],
    ['El sistema te deja ver tus pagos pero no los de otros socios', 'Autorización', 'Define lo que tienes permitido hacer.'],
    ['Poner tu huella en el torniquete', 'Autenticación', 'Comprueba quién eres con algo que eres.'],
    ['Solo la administradora puede cambiar precios', 'Autorización', 'Es un permiso.'],
    ['Recibir un código en el celular para confirmar tu ingreso', 'Autenticación', 'Es un segundo factor para comprobar tu identidad.'],
], 'Identidad → autenticación · Permisos → autorización.', ['Autenticación', 'Autorización'])
c.pw = c.raw('pPass()')
c.A('🔑', '¿Qué factor es?', 'Clasifica cada forma de comprobar tu identidad.', [
    ['Contraseña', 'Algo que sabes', 'Está en tu memoria.'],
    ['Código que llega a tu celular', 'Algo que tienes', 'Depende de un objeto que posees.'],
    ['Huella digital', 'Algo que eres', 'Es una característica tuya.'],
    ['NIP de la tarjeta', 'Algo que sabes', 'Lo memorizas.'],
    ['Tarjeta de acceso del gimnasio', 'Algo que tienes', 'Es un objeto.'],
    ['Reconocimiento facial', 'Algo que eres', 'Usa una característica de tu cara.'],
], 'Memoria → sabes · Objeto → tienes · Cuerpo → eres.', ['Algo que sabes', 'Algo que tienes', 'Algo que eres'])
c.L('🧱', 'Controles de seguridad', 'Bloque D · De qué tipo son', body(
    sp('En palabras sencillas', 'Además de preventivos, detectivos y correctivos (cuándo actúan), los controles se clasifican por <b>qué son</b>.'),
    bk('Administrativos', 'Reglas, políticas y capacitación: política de contraseñas, reglamento de uso del equipo.'),
    bk('Técnicos (lógicos)', 'Tecnología: antivirus, firewall, cifrado, doble factor.'),
    bk('Físicos', 'Lo que se toca: llaves, cámaras, cerraduras, torniquete.'),
    ex('En el gimnasio', 'Política que obliga a cambiar contraseñas cada 3 meses (administrativo). Antivirus (técnico). Cuarto de equipos con llave (físico).'),
    bk('Defensa en profundidad', 'Combinar de los tres tipos, para que si uno falla, otro proteja.')),
    'Administrativo = reglas · Técnico = tecnología · Físico = lo que se toca.')
c.A('🧱', '¿Qué tipo de control es?', 'Clasifica cada control.', [
    ['Una política que prohíbe compartir contraseñas', 'Administrativo', 'Es una regla.'],
    ['Instalar un firewall', 'Técnico', 'Es tecnología.'],
    ['Cámara en el pasillo de equipos', 'Físico', 'Es un elemento físico.'],
    ['Capacitación anual sobre phishing', 'Administrativo', 'Es formación del personal.'],
    ['Activar el cifrado del disco', 'Técnico', 'Se configura en el equipo.'],
    ['Candado en la laptop del gimnasio', 'Físico', 'Es un objeto físico.'],
], 'Regla → administrativo · Tecnología → técnico · Se toca → físico.', ['Administrativo', 'Técnico', 'Físico'])
c.L('🫥', 'Ocultamiento de datos', 'Bloque D · Esconder sin cifrar', body(
    sp('En palabras sencillas', 'No siempre se cifra: a veces se <b>esconde</b> o se <b>disfraza</b> la información.'),
    bk('Esteganografía', 'Esconder un mensaje <b>dentro de otro archivo</b>, por ejemplo en los píxeles de una foto. Nadie sospecha que hay algo ahí.'),
    bk('Enmascaramiento', 'Mostrar solo una parte: **** **** **** 4821 en un ticket. El dato real sigue guardado.'),
    bk('Ofuscación', 'Hacer difícil de entender el código o los datos, aunque se puedan ver.'),
    bk('Anonimización', 'Quitar los datos que identifican a la persona para poder usar la información (por ejemplo, estadísticas del gimnasio sin nombres).'),
    ana('Diferencia clave', '<b>Cifrar</b> es poner el mensaje en una caja fuerte: se ve que hay algo, pero no se puede abrir. <b>Esteganografía</b> es esconder la caja: nadie sabe que existe.')),
    'Cifrar = no se puede leer · Esteganografía = no se sabe que existe.')
c.A('🫥', '¿Cifrado, esteganografía o enmascaramiento?', 'Clasifica cada técnica.', [
    ['Esconder un mensaje en los píxeles de una fotografía', 'Esteganografía', 'El mensaje va oculto dentro de otro archivo.'],
    ['Mostrar solo los últimos 4 dígitos de la tarjeta en el ticket', 'Enmascaramiento', 'Se muestra una parte y se oculta el resto.'],
    ['Convertir un archivo en texto ilegible con una clave', 'Cifrado', 'Hace ilegible el contenido sin la clave.'],
    ['Cambiar los nombres de los socios por números en un reporte', 'Anonimización', 'Quita lo que identifica a la persona.'],
], 'Esconder dentro → esteganografía · Mostrar parte → enmascaramiento · Ilegible → cifrado.', ['Cifrado', 'Esteganografía', 'Enmascaramiento', 'Anonimización'])
c.W('✍️', 'Protege el gimnasio', 'Aplica lo aprendido.',
    'Propón <b>cuatro medidas</b> para proteger al gimnasio: una de <b>autenticación</b>, una de <b>autorización</b>, una de <b>cifrado</b> y una <b>física</b>.',
    [['Tiene al menos 30 palabras', 'palabras:30'],
     ['Una medida de autenticación (contraseña, huella, doble factor…)', '(autentic|contrase|huella|doble factor|dos pasos|codigo|mfa)'],
     ['Una medida de autorización (permisos, roles, mínimo privilegio…)', '(autoriz|permiso|rol|privilegio|solo la|solo el)'],
     ['Una medida de cifrado', '(cifr|encript|cripto|https|vpn)'],
     ['Una medida física (llave, cámara, candado, torniquete…)', '(llave|camara|candado|torniquete|cuarto|cerradura|fisic)']],
    'Una oración por medida.', 'Ejemplo: Autenticación: doble factor para los empleados. Autorización: …')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario (1 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Ciberseguridad', 'Proteger información, equipos, servicios y redes.'),
    bk('Amenaza', 'Lo que puede causar daño.'),
    bk('Vulnerabilidad', 'Debilidad que una amenaza puede aprovechar.'),
    bk('Riesgo', 'Posibilidad de daño cuando una amenaza aprovecha una vulnerabilidad.'),
    bk('Confidencialidad', 'Que solo vea la información quien está autorizado.'),
    bk('Integridad', 'Que la información no cambie sin permiso.'),
    bk('Disponibilidad', 'Que funcione cuando se necesita.'),
    bk('Contramedida', 'Control que reduce un riesgo.'),
    bk('Marco de trabajo', 'Guía ordenada para organizar la seguridad (NIST CSF, ISO 27001).')))
c.L('📖', 'Glosario (2 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Malware', 'Software hecho para dañar o espiar.'),
    bk('Ransomware', 'Malware que cifra tus archivos y pide rescate.'),
    bk('Phishing', 'Mensaje falso que imita a una empresa para robar datos.'),
    bk('Ingeniería social', 'Engañar a las personas para obtener datos o acceso.'),
    bk('DDoS', 'Saturar un servicio desde muchos equipos para dejarlo sin funcionar.'),
    bk('Cifrado', 'Hacer ilegible un mensaje con una clave.'),
    bk('MFA', 'Verificación con dos o más factores (sabes, tienes, eres).'),
    bk('Mínimo privilegio', 'Dar solo los permisos necesarios.'),
    bk('Esteganografía', 'Esconder un mensaje dentro de otro archivo.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Grupo 511: <b>lunes 17:20-18:10</b> y <b>viernes 18:10-19:50</b>. Cada práctica tiene versión para celular. Las herramientas de la pestaña <b>Diagnostica</b> funcionan en celular y no envían datos a ningún servidor.', 'sp'),
    bk('Bloque A · concepto y vulnerabilidades', 'Una sesión: concepto, delincuencia cibernética, amenazas internas y externas, vulnerabilidades, especialistas y certificaciones. <b>Práctica 1</b> en clase o como tarea.'),
    bk('Bloque B · principios', 'Una sesión: confidencialidad, integridad, disponibilidad, estado de los datos, contramedidas y marco NIST.'),
    bk('Bloque C · amenazas y ataques', 'Una sesión: malware, código malicioso, ingeniería social y ciberataques. Usa el <b>Detective de phishing</b> en pantalla grande y deja que el grupo decida.'),
    bk('Bloque D · protección', 'Una sesión: cifrado, autenticación y autorización, controles y ocultamiento. <b>Práctica 2</b> con el medidor de contraseñas (nunca con contraseñas reales).'),
    bk('Evaluación', 'Actividad con fecha en tu cronograma: <b>viernes 23-oct</b>. Los alumnos preparan una <b>presentación electrónica</b> (PPTX o PDF) con el caso asignado en la plataforma; la <b>Práctica 3</b> los lleva paso a paso. El material sirve de repaso y para quienes aún no entregan.')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '💪', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🛡️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🔺', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🦠', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '🔐', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"💪",t:"Empieza aquí",d:"Amenaza, vulnerabilidad y riesgo con el caso de un gimnasio.",time:"20 min",obj:["Distinguir amenaza, vulnerabilidad y riesgo","Conocer el caso y la evidencia final"],sum:["Amenaza = lo que daña · Vulnerabilidad = la debilidad · Riesgo = posibilidad de daño.","Entregas una presentación con el caso asignado."],q:"¿Qué dato tuyo sería más grave que se filtrara: tu teléfono, tu foto o tu contraseña?"},
a:{k:"Bloque A",l:"A",ic:"🛡️",t:"Ciberseguridad",d:"Concepto, delincuencia, amenazas internas y externas, vulnerabilidades y carreras.",time:"90 min",obj:["Explicar qué es la ciberseguridad","Clasificar amenazas internas y externas","Reconocer los tipos de vulnerabilidades"],sum:["Ciberseguridad = personas + procesos + tecnología.","Muchos incidentes empiezan por un error humano.","Se pueden cerrar las vulnerabilidades aunque no se controle a los atacantes."],q:"¿Qué vulnerabilidad humana crees que es la más común entre tus compañeros?"},
b:{k:"Bloque B",l:"B",ic:"🔺",t:"Principios de seguridad",d:"Confidencialidad, integridad, disponibilidad, estado de los datos, contramedidas y marco NIST.",time:"100 min",obj:["Explicar la tríada CIA con ejemplos","Distinguir el estado de los datos","Clasificar contramedidas y funciones del marco"],sum:["CIA: secreto, exactitud y servicio.","Datos en reposo, en tránsito y en proceso.","Prevenir, detectar y corregir; NIST CSF tiene seis funciones."],q:"Piensa en tu cuenta de redes sociales: ¿qué principio te preocupa más proteger?",rev:[["Que alguien lea la lista de pagos sin permiso afecta…",["La confidencialidad","La disponibilidad","Ninguno"],0,"Alguien no autorizado vio información privada."],["Una amenaza interna accidental es…",["Un empleado que se equivoca","Un virus de internet","Un robo"],0,"Tiene acceso legítimo y se equivoca."]]},
c:{k:"Bloque C",l:"C",ic:"🦠",t:"Amenazas, vulnerabilidades y ataques",d:"Malware, código malicioso, ingeniería social y ciberataques.",time:"100 min",obj:["Identificar tipos de malware","Reconocer señales de phishing","Relacionar cada ciberataque con su descripción"],sum:["Malware: virus, gusano, troyano, ransomware, spyware.","La ingeniería social engaña a las personas; busca urgencia y miedo.","DDoS satura; el diccionario prueba contraseñas comunes."],q:"¿Qué mensaje falso has recibido tú o alguien de tu familia?",rev:[["Un programa que cifra tus archivos y pide dinero es…",["Ransomware","Adware","Un gusano"],0,"Secuestra los archivos."],["Un control que restaura un respaldo es…",["Correctivo","Preventivo","Detectivo"],0,"Recupera lo perdido."]]},
d:{k:"Bloque D",l:"D",ic:"🔐",t:"Protección y seguridad",d:"Criptografía, autenticación, autorización, controles y ocultamiento de datos.",time:"100 min",obj:["Distinguir cifrado simétrico y asimétrico","Explicar los factores de autenticación","Clasificar controles y técnicas de ocultamiento"],sum:["Simétrica = una clave · Asimétrica = pública y privada.","Autenticar = quién eres · Autorizar = qué puedes hacer.","Controles administrativos, técnicos y físicos; cifrar no es lo mismo que esteganografía."],q:"¿Qué cuenta tuya activarías hoy con verificación en dos pasos?",rev:[["Una huella digital es…",["Algo que eres","Algo que sabes","Algo que tienes"],0,"Es una característica del cuerpo."],["Esconder un mensaje dentro de una foto es…",["Esteganografía","Cifrado","Un hash"],0,"Se oculta la existencia del mensaje."]]}
'''

ILL = r'''
ILL["¿Qué es la ciberseguridad?"]=function(){return flow([["👥","Personas"],["📋","Procesos"],["💻","Tecnología"]],"Las tres partes de la ciberseguridad")};
ILL["Vulnerabilidades"]=function(){return flow([["🕳️","Vulnerabilidad"],["👿","Amenaza|la aprovecha"],["💥","Impacto"]],"De la vulnerabilidad al impacto")};
ILL["Estado de los datos"]=function(){return flow([["🗄️","En reposo"],["📡","En tránsito"],["⚙️","En proceso"]],"Estados de los datos")};
ILL["Modelos y marco de trabajo"]=function(){return grid3([["🏛️","Gobernar"],["🔍","Identificar"],["🛡️","Proteger"],["🔔","Detectar"],["🚒","Responder"],["♻️","Recuperar"]],"Funciones del marco NIST")};
ILL["Criptografía y encriptación"]=function(){return flow([["📄","Mensaje"],["🔑","Cifrar|con clave"],["🔒","Ilegible"],["🗝️","Descifrar|con clave"]],"Cifrar y descifrar")};
ILL["Autenticación, autorización y control de acceso"]=function(){return flow([["🪪","Autenticar|¿quién eres?"],["✅","Autorizar|¿qué puedes?"],["📝","Auditar|¿qué hiciste?"]],"Las tres A")};
'''

EXH = r'''
function cw_(t,b,ps){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:'+(ps?'#012456':'#0c0c0c')+';color:#eee;padding:10px;font:12.5px/1.45 Consolas,monospace;white-space:pre-wrap;overflow-x:auto">'+b+'</pre></div>'}
EXH.noticia=function(){return exw('<table class="mtb"><tr><th>Dato</th><th>Ejemplo</th></tr><tr><td>Noticia</td><td>«Filtran datos de clientes de una cadena de tiendas»</td></tr><tr><td>Fuente y fecha</td><td>Periódico, 12-oct-2026</td></tr><tr><td>Amenaza</td><td>Atacante externo</td></tr><tr><td>Vulnerabilidad</td><td>Base de datos sin cifrar y sin doble factor</td></tr><tr><td>Impacto</td><td>Datos de 20 mil clientes expuestos</td></tr></table>',['Elige una noticia real y reciente de ciberseguridad.','Anota la fuente y la fecha.'])};
EXH.cia_tabla=function(){return exw('<table class="mtb"><tr><th>Principio</th><th>¿Se afectó?</th><th>Por qué</th></tr><tr><td>Confidencialidad</td><td>Sí</td><td>Los datos quedaron expuestos</td></tr><tr><td>Integridad</td><td>No</td><td>No se reportó que cambiaran</td></tr><tr><td>Disponibilidad</td><td>No</td><td>El servicio siguió funcionando</td></tr></table>',['Explica con tus palabras por qué se afectó cada principio.'])};
EXH.controles=function(){return exw('<table class="mtb"><tr><th>Control</th><th>Tipo (cuándo actúa)</th><th>Tipo (qué es)</th></tr><tr><td>Doble factor</td><td>Preventivo</td><td>Técnico</td></tr><tr><td>Capacitación</td><td>Preventivo</td><td>Administrativo</td></tr><tr><td>Alertas de acceso</td><td>Detectivo</td><td>Técnico</td></tr><tr><td>Restaurar respaldo</td><td>Correctivo</td><td>Técnico</td></tr></table>',['Propón al menos 4 controles y clasifica cada uno de las dos formas.'])};
EXH.medidor=function(){return exw('<div class="mbox">🔑 <b>Medidor de contraseñas</b> (pestaña Diagnostica)<br>«hola123» → <b>Muy débil</b> · se adivina al instante<br>«Mi gato come 5 galletas» → <b>Fuerte</b> · millones de años</div>',['Prueba solo contraseñas de ejemplo, nunca las reales.','Toma captura de dos pruebas: una débil y una fuerte.'])};
EXH.hibp=function(){return exw(mw('haveibeenpwned.com','<div style="line-height:1.8">Correo: <b>tucorreo@ejemplo.com</b> '+mk(1)+'<br>🔴 <b>¡Se encontró en 2 filtraciones!</b> '+mk(2)+'<br>Ejemplo: Canva (2019), Dropbox (2012)<br><small>Si sale en una filtración, cambia esa contraseña y activa el doble factor.</small></div>'),['Escribe solo TU correo personal.','Si sale limpio, también es un buen resultado.'])};
EXH.dospasos=function(){return exw(mp('Seguridad de la cuenta','<div class="mbox">🔐 Verificación en dos pasos: <b>Activada</b> ✅</div><div class="mbox" style="margin-top:6px">📱 Segundo paso: app de autenticación</div>'),['Activa la verificación en dos pasos en una de tus cuentas.','Toma captura donde se vea «Activada». No captures códigos.'])};
EXH.esqueleto=function(){return exw('<table class="mtb"><tr><th>Diapositiva</th><th>Contenido</th></tr><tr><td>1</td><td>Portada: título, tu nombre, grupo y fecha</td></tr><tr><td>2</td><td>¿Qué es la ciberseguridad?</td></tr><tr><td>3</td><td>Confidencialidad, integridad y disponibilidad con ejemplos</td></tr><tr><td>4</td><td>El caso asignado y qué hay que proteger</td></tr><tr><td>5</td><td>Amenazas internas y externas, y vulnerabilidades</td></tr><tr><td>6</td><td>Malware, engaño o ataque posible</td></tr><tr><td>7</td><td>Protección: autenticación, permisos, cifrado</td></tr><tr><td>8</td><td>Conclusión y 3 recomendaciones</td></tr></table>',['Copia este esqueleto en tu programa de presentaciones.'])};
EXH.diseno=function(){return exw('<div class="mbox"><b>✅ Buena diapositiva</b><br>Título corto · 3 a 5 ideas cortas · una imagen o esquema · letra grande (24 pt o más)</div><div class="mbox" style="margin-top:6px"><b>❌ Mala diapositiva</b><br>Un párrafo largo · letra pequeña · colores que no se leen · demasiadas imágenes</div>',['Una idea principal por diapositiva.','Si no se lee desde el fondo del salón, la letra es muy chica.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Analiza una noticia de ciberseguridad',
     'prog': 'Bloques A y B · Amenaza, vulnerabilidad, riesgo y principios',
     'min': 45, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con internet', 'Documento o presentación para tu evidencia'],
                'steps': [
                    ['Busca una noticia reciente de un ciberataque o filtración de datos (en un periódico o en un sitio de noticias de tecnología). Anota el título, la fuente y la fecha.', 'noticia'],
                    'Identifica la amenaza, si fue interna o externa, y su tipo (por ejemplo ransomware, phishing o malware).',
                    'Identifica la vulnerabilidad que se aprovechó: humana, técnica, de configuración o física.',
                    ['Completa una tabla con confidencialidad, integridad y disponibilidad: cuál se afectó y por qué.', 'cia_tabla'],
                    ['Propón 4 controles que hubieran evitado o reducido el daño y clasifícalos.', 'controles']]},
         'cel': {'mat': ['Celular con internet', 'Notas o Documentos de Google'],
                 'steps': [
                     ['Busca una noticia reciente de un ciberataque o filtración de datos. Anota el título, la fuente y la fecha.', 'noticia'],
                     'Identifica la amenaza, si fue interna o externa, y su tipo.',
                     'Identifica la vulnerabilidad que se aprovechó: humana, técnica, de configuración o física.',
                     ['Completa una tabla con confidencialidad, integridad y disponibilidad: cuál se afectó y por qué.', 'cia_tabla'],
                     ['Propón 4 controles que hubieran evitado o reducido el daño y clasifícalos.', 'controles']]}},
     'entrega': ['Tabla con la noticia, amenaza, vulnerabilidad, principios afectados y controles. Sirve como borrador de las diapositivas 4 a 7.'],
     'rub': [['Noticia real con fuente y fecha', 15], ['Amenaza y vulnerabilidad bien identificadas', 30], ['Principios afectados explicados', 25], ['Controles bien clasificados', 30]]},
    {'id': 'pr2', 'n': 2, 't': 'Revisa tu seguridad personal',
     'prog': 'Bloques C y D · Contraseñas, filtraciones y doble factor',
     'min': 40, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con internet', 'Este material (Medidor de contraseñas)', 'Documento para tus capturas'],
                'steps': [
                    ['En la pestaña Diagnostica abre el Medidor de contraseñas y prueba 4 contraseñas DE EJEMPLO: una débil, una común, una media y una fuerte. Captura el resultado.', 'medidor'],
                    ['Revisa en haveibeenpwned.com si tu correo personal aparece en alguna filtración. Anota el resultado.', 'hibp'],
                    ['Activa la verificación en dos pasos en una de tus cuentas y captura la pantalla donde dice «Activada».', 'dospasos'],
                    'Escribe 3 renglones: qué aprendiste y qué vas a cambiar en tus contraseñas.']},
         'cel': {'mat': ['Celular con internet', 'Este material (Medidor de contraseñas)', 'Notas para tus capturas'],
                 'steps': [
                     ['Abre el Medidor de contraseñas (pestaña Diagnostica) y prueba 4 contraseñas DE EJEMPLO: una débil, una común, una media y una fuerte. Captura el resultado.', 'medidor'],
                     ['Revisa en haveibeenpwned.com si tu correo personal aparece en alguna filtración. Anota el resultado.', 'hibp'],
                     ['Activa la verificación en dos pasos en una de tus cuentas y captura la pantalla donde dice «Activada».', 'dospasos'],
                     'Escribe 3 renglones: qué aprendiste y qué vas a cambiar en tus contraseñas.']}},
     'entrega': ['Capturas del medidor, del resultado de filtraciones y de la verificación en dos pasos, sin mostrar contraseñas ni códigos.'],
     'rub': [['Pruebas del medidor con análisis', 30], ['Revisión de filtraciones', 20], ['Verificación en dos pasos activada', 30], ['Reflexión personal', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Arma el esqueleto de tu presentación',
     'prog': 'Todos los bloques · Preparación de la actividad de evaluación',
     'min': 60, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['PowerPoint o Presentaciones de Google', 'Tu caso asignado en la actividad de evaluación de la plataforma'],
                'steps': [
                    ['Crea una presentación nueva con 8 diapositivas siguiendo este esqueleto.', 'esqueleto'],
                    'Escribe en la diapositiva 4 el caso que te asignó la plataforma y los recursos que hay que proteger.',
                    'En las diapositivas 5 a 7 anota amenazas, vulnerabilidades, el posible malware, engaño o ataque y tus controles.',
                    ['Revisa el diseño: una idea por diapositiva, letra grande y una imagen o esquema.', 'diseno'],
                    'Escribe la conclusión con 3 recomendaciones concretas en la diapositiva 8.']},
         'cel': {'mat': ['App de Presentaciones de Google, PowerPoint o Canva', 'Tu caso asignado en la actividad de evaluación de la plataforma'],
                 'steps': [
                     ['Crea una presentación nueva con 8 diapositivas siguiendo este esqueleto.', 'esqueleto'],
                     'Escribe en la diapositiva 4 el caso que te asignó la plataforma y los recursos que hay que proteger.',
                     'En las diapositivas 5 a 7 anota amenazas, vulnerabilidades, el posible malware, engaño o ataque y tus controles.',
                     ['Revisa el diseño: una idea por diapositiva, letra grande y una imagen o esquema.', 'diseno'],
                     'Escribe la conclusión con 3 recomendaciones concretas en la diapositiva 8.']}},
     'entrega': ['Tu presentación en borrador (PPTX o PDF). La versión final la subes en la actividad de evaluación.'],
     'rub': [['Estructura de 8 diapositivas', 25], ['Caso y recursos identificados', 20], ['Amenazas, vulnerabilidades y controles', 35], ['Diseño y conclusión', 20]]},
]

EVALUATION = {
    'course': 'MTCS-20 · Manejo de tecnologías de ciberseguridad · Unidad 2',
    'ra': 'R.A. 2.1', 'title': 'Presentación de fundamentos de ciberseguridad',
    'data': [
        ('Resultado de aprendizaje', 'Identifica fundamentos de la ciberseguridad de acuerdo con los principios y tecnologías de confidencialidad con la finalidad de contextualizar su aplicación en la red.'),
        ('Actividad de evaluación', '2.1.1 Describe a través de una presentación electrónica los fundamentos de la ciberseguridad considerando principios de seguridad, amenazas y ataques, y protección y seguridad.'),
        ('Evidencia', 'Presentación electrónica (PPTX o PDF)'),
        ('Ponderación', '20% (según el programa)'),
        ('Entrega', 'Fecha de tu cronograma: viernes 23 de octubre. Si aún no entregas, consulta con tu docente. Se entrega en la actividad R.A. 2.1 de la plataforma.'),
    ],
    'situation': 'En la actividad de evaluación de la plataforma tienes asignado un caso con una situación de seguridad. Prepara una presentación de 8 diapositivas que explique los fundamentos de la ciberseguridad y los aplique a ese caso.',
    'hint': 'Cada diapositiva debe mencionar los datos de TU caso. Una idea por diapositiva y letra que se lea desde el fondo del salón.',
    'steps': [
        ('Portada y concepto', ['Diapositiva 1: título de tu presentación y tus datos.', 'Diapositiva 2: explica qué es la ciberseguridad con tus propias palabras.']),
        ('Principios (Bloque B)', ['Diapositiva 3: explica confidencialidad, integridad y disponibilidad con ejemplos.']),
        ('El caso (Bloques A y B)', ['Diapositiva 4: resume el caso asignado e identifica los recursos que necesitan protección.', 'Diapositiva 5: identifica amenazas internas, externas y vulnerabilidades presentes.']),
        ('Ataques (Bloque C)', ['Diapositiva 6: explica qué malware, engaño o ataque podría aprovechar esas debilidades.']),
        ('Protección (Bloque D)', ['Diapositiva 7: propón autenticación, permisos, cifrado u otros controles adecuados.']),
        ('Cierre y entrega', ['Diapositiva 8: conclusión y tres recomendaciones concretas.', 'Guarda tu presentación como PPTX o PDF y súbela en la actividad de la plataforma, junto con las respuestas escritas.']),
    ],
    'rubric': [('Portada y datos', 10), ('Concepto de ciberseguridad', 10), ('Principios con ejemplos', 20), ('Caso y recursos a proteger', 10), ('Amenazas y vulnerabilidades', 15), ('Malware, engaño o ataque', 10), ('Protección propuesta', 15), ('Conclusión y recomendaciones', 10)],
    'deliver': ['Un archivo PPTX o PDF con tu presentación de 8 diapositivas.', 'Se entrega en la actividad R.A. 2.1 de la plataforma, junto con las secciones escritas.'],
}
