"""EDOA-20 · R.A. 1.3 · Correspondencia y revisión colaborativa (Word).

Caso de las lecciones: Torneo de ajedrez del plantel (constancias para cada participante y revisión del aviso en equipo).
La actividad de evaluación es la entrega de los documentos (.docx o PDF) en la plataforma.
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-1.3'
CODE_PREFIX = 'EDOA13'
FILE = 'edoa-ra13-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 1.3 · Correspondencia y revisión colaborativa'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 1.3 · Correspondencia y revisión colaborativa'
HERO_KICK = 'EDOA-20 · R.A. 1.3'
HERO_TITLE = 'Un documento para muchos y un equipo que lo revisa'
HERO_TEXT = 'Aprende a generar documentos para varias personas con combinación de correspondencia y a revisar un archivo en equipo con control de cambios.'
EV_SHORT = 'elabora tus documentos combinados y la revisión con cambios.'
EV_CARD = 'Documentos R.A. 1.3'
RA = 'R.A. 1.3'
GROUP = '311'
TABS = {'d': ['Diagnostica', 'Simulador de combinación y control de cambios'], 'c': ['Construye', 'Prácticas en Word']}

EXTRA_JS = r'''
var MGR=[["Ana Torres","3-A","2601"],["Luis Pérez","3-A","2602"],["Marta Ruiz","","2603"],["Jorge Díaz","3-B","2604"]];
function pMerge(){K++;return '<article class="lesson"><header><span class="kick">✉️ Herramienta</span><h1>Simulador de combinación</h1><p class="sub">Revisa la constancia con cada destinatario, corrige el dato que falta y finaliza la combinación.</p></header><style>.mgx .doc{background:#fff;color:#111;border:1px solid var(--line);border-radius:6px;padding:16px;font:15px/1.7 Georgia,serif}.mgx .fd{background:#d6e4f7;border-radius:4px;padding:0 4px;color:#1f3f7a;font-weight:700}.mgx .fd.em{background:#f9d6d6;color:#9b1c1c}.mgx .bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:10px 0}.mgx button.bn{padding:9px 13px;border:2px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:600 14px inherit;cursor:pointer}.mgx button.bn.on{border-color:var(--pri);background:var(--exb)}.mgx button.bn:disabled{opacity:.45}.mgx table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0}.mgx td,.mgx th{border:1px solid var(--line);padding:5px 8px;text-align:left}.mgx input{width:100%;padding:5px;border:2px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);font:14px inherit}.mgx .ms{font-weight:700;margin:8px 0;min-height:22px}</style><div class="mgx"><p style="margin:4px 0;font-weight:700">Lista de destinatarios (cada columna es un campo)</p><div class="tb"></div><div class="bar"><button class="bn" data-m="f">Ver campos</button><button class="bn" data-m="p">Vista previa de resultados</button><button class="bn" data-m="prev" disabled>‹</button><span class="rn"></span><button class="bn" data-m="next" disabled>›</button></div><div class="doc"></div><div class="bar"><button class="bn" data-m="fin">Finalizar y combinar</button></div><p class="ms" role="status"></p></div><p class="take"><b>En Word:</b> Correspondencia &gt; Iniciar combinación &gt; Seleccionar destinatarios &gt; Insertar campo combinado &gt; Vista previa &gt; Finalizar y combinar.</p></article>'}
function mrgInit(d){var w=d.querySelector(".mgx");if(!w)return;function g(c){return w.querySelector("."+c)}function q(s){return w.querySelector(s)}
 var rows=MGR.map(function(r){return r.slice()}),prev=false,i=0,seen={0:1};
 function tb(){g("tb").innerHTML='<table><tr><th>Nombre</th><th>Grupo</th><th>Matrícula</th></tr>'+rows.map(function(r,k){return '<tr><td>'+r[0]+'</td><td><input data-r="'+k+'" value="'+r[1]+'" placeholder="(vacío)"></td><td>'+r[2]+'</td></tr>'}).join("")+'</table>';w.querySelectorAll("[data-r]").forEach(function(e){e.oninput=function(){rows[+e.dataset.r][1]=e.value.trim();draw()}})}
 function f(n,v){return prev?(v?'<b>'+v+'</b>':'<span class="fd em">¡campo vacío!</span>'):'<span class="fd">«'+n+'»</span>'}
 function draw(){var r=rows[i];g("doc").innerHTML='<p style="text-align:center"><b>CONSTANCIA</b></p><p>Se hace constar que '+f("Nombre",r[0])+', del grupo '+f("Grupo",r[1])+', con matrícula '+f("Matrícula",r[2])+', participó en el torneo de ajedrez del plantel.</p><p style="text-align:right">Cd. Victoria, Tamaulipas</p>';
  g("rn").textContent=prev?"Registro "+(i+1)+" de "+rows.length:"";q("[data-m=prev]").disabled=!prev||i==0;q("[data-m=next]").disabled=!prev||i==rows.length-1;q("[data-m=f]").className="bn"+(prev?"":" on");q("[data-m=p]").className="bn"+(prev?" on":"")}
 w.querySelectorAll("[data-m]").forEach(function(b){b.onclick=function(){var m=b.dataset.m;if(m=="f")prev=false;if(m=="p"){prev=true;seen[i]=1}if(m=="prev"&&i>0){i--;seen[i]=1}if(m=="next"&&i<rows.length-1){i++;seen[i]=1}
  if(m=="fin"){var empt=rows.filter(function(r){return !r[1]}).length,all=Object.keys(seen).length==rows.length,ms=g("ms");if(!prev||!all){ms.textContent="⚠️ Antes de finalizar, revisa la vista previa de todos los registros.";return}if(empt){ms.textContent="❌ Hay "+empt+" registro(s) con campos vacíos. Corrige la lista y vuelve a revisar.";return}ms.textContent="✅ Se crearon "+rows.length+" constancias, una por destinatario.";var t="t:Simulador de combinación";if(!ST[t]){ST[t]=1;sv()}return}
  g("ms").textContent="";draw()}});tb();draw()}
var TKC=[{o:"18 de noviembre",n:"20 de noviembre",w:"Coordinación",ok:"a",no:"Fecha confirmada por la dirección."},{o:"gimnasio",n:"auditorio",w:"Coordinación",ok:"a",no:"El gimnasio estará en uso ese día."},{o:"cuatro",n:"diez",w:"Alumno",ok:"r",no:"Comentario de la dirección: el reglamento permite máximo 4 por grupo."},{o:"",n:"No se permiten celulares durante las partidas.",w:"Profesor",ok:"a",no:"Evita distracciones."}];
function pTrack(){K++;return '<article class="lesson"><header><span class="kick">📝 Herramienta</span><h1>Control de cambios</h1><p class="sub">Tres personas hicieron cambios al aviso del torneo. Acepta o rechaza cada uno y deja la versión correcta.</p></header><style>.tkx .doc{background:#fff;color:#111;border:1px solid var(--line);border-radius:6px;padding:16px;font:15px/1.8 Georgia,serif}.tkx del{color:#b91c1c;text-decoration:line-through}.tkx ins{color:#166534;text-decoration:underline;background:#dcf5e3}.tkx .cl{margin:10px 0;display:grid;gap:8px}.tkx .it{border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--card);font-size:14px}.tkx .it .bt{margin-top:6px;display:flex;gap:6px}.tkx button{padding:7px 12px;border:2px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);font:600 13px inherit;cursor:pointer}.tkx button.on{border-color:var(--pri);background:var(--exb)}.tkx .ms{font-weight:700;margin:8px 0;min-height:22px}</style><div class="tkx"><div class="doc"></div><div class="cl"></div><p class="ms" role="status"></p><button class="rs">Reiniciar</button></div><p class="take"><b>En Word:</b> Revisar &gt; Control de cambios registra lo que cambia cada persona. Con Aceptar o Rechazar decides la versión final.</p></article>'}
function trkInit(d){var w=d.querySelector(".tkx");if(!w)return;function g(c){return w.querySelector("."+c)}var st=[];
 function draw(){var s="El torneo interno de ajedrez se realizará el "+chg(0)+", en el "+chg(1)+" del plantel. Cada grupo inscribirá a "+chg(2)+" participantes. "+chg(3);g("doc").innerHTML=s;
  g("cl").innerHTML=TKC.map(function(c,k){return '<div class="it"><b>'+c.w+'</b>: '+(c.o?'cambió «'+c.o+'» por «'+c.n+'»':'agregó «'+c.n+'»')+'<br><small>'+c.no+'</small><div class="bt"><button data-a="'+k+'" class="'+(st[k]=="a"?"on":"")+'">✔ Aceptar</button><button data-r="'+k+'" class="'+(st[k]=="r"?"on":"")+'">✖ Rechazar</button></div></div>'}).join("");
  w.querySelectorAll("[data-a]").forEach(function(b){b.onclick=function(){st[+b.dataset.a]="a";draw();fin()}});w.querySelectorAll("[data-r]").forEach(function(b){b.onclick=function(){st[+b.dataset.r]="r";draw();fin()}})}
 function chg(k){var c=TKC[k],s=st[k];if(s=="a")return c.n;if(s=="r")return c.o;return (c.o?"<del>"+c.o+"</del> ":"")+"<ins>"+c.n+"</ins>"}
 function fin(){var ms=g("ms");if(TKC.some(function(c,k){return !st[k]})){ms.textContent="";return}var bad=TKC.filter(function(c,k){return st[k]!=c.ok});if(bad.length){ms.textContent="❌ Revisa de nuevo: hay un cambio que no debía aceptarse (o uno que sí). Lee los comentarios.";return}ms.textContent="✅ Versión final correcta: aceptaste los cambios válidos y rechazaste el que contradecía el reglamento.";var t="t:Control de cambios";if(!ST[t]){ST[t]=1;sv()}}
 g("rs").onclick=function(){st=[];g("ms").textContent="";draw()};draw()}
'''
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n mrgInit(d);trkInit(d);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('♟️', 'El mismo documento para muchas personas', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Si necesitas 40 constancias que solo cambian en el nombre, no las escribes una por una: usas la <b>combinación de correspondencia</b>. Y cuando varias personas editan un archivo, el <b>control de cambios</b> muestra qué cambió cada una.'),
    ex('Caso de las lecciones: Torneo de ajedrez del plantel', 'Hay que entregar una constancia a cada participante (con su nombre, grupo y matrícula) y revisar entre varias personas el aviso del torneo antes de publicarlo.'),
    bk('Qué vas a hacer', '<b>1. Aprende</b> los conceptos con ejemplos. <b>2. Diagnostica</b> con un simulador de combinación y uno de control de cambios. <b>3. Construye</b> tres prácticas en Word.'),
    bk('Al final', 'Entregas tus <b>documentos combinados</b> y un documento <b>revisado con control de cambios</b> (DOCX o PDF).')),
    'Combinar para muchos destinatarios · Revisar para trabajar en equipo.')
c.A('🔎', '¿Qué herramienta uso?', 'Elige la herramienta de Word para cada situación.', [
    ['Generar 40 constancias que cambian solo en el nombre', 'Combinar correspondencia', 'Un documento principal y una lista de destinatarios.'],
    ['Ver qué cambió cada compañero en el aviso', 'Control de cambios', 'Registra inserciones y eliminaciones por persona.'],
    ['Dejar una observación sin modificar el texto', 'Comentario', 'Explica sin cambiar el documento.'],
    ['Evitar que otros editen el archivo final', 'Restringir edición', 'Protege contra cambios no autorizados.'],
], 'Muchos documentos → combinar · Quién cambió → control de cambios · Observación → comentario · Proteger → restringir.', ['Combinar correspondencia', 'Control de cambios', 'Comentario', 'Restringir edición'])
s0_end = c.mark() - 1

# ───────────────────────── A · Combinación de correspondencia ─────────────────────────
a0 = c.mark()
c.L('✉️', 'Combinación de correspondencia', 'Bloque A · Un documento, muchos destinatarios', body(
    sp('En palabras sencillas', 'Combina un <b>documento principal</b> (la plantilla) con una <b>lista de destinatarios</b>. Lo fijo se queda igual y los <b>campos</b> cambian para cada persona.'),
    bk('Para qué sirve', 'Cartas, constancias, etiquetas, sobres y gafetes.'),
    ana('Piensa en…', 'Una invitación de boda: el texto es igual para todos, pero cada tarjeta lleva un nombre distinto.'),
    ex('En el torneo', 'La constancia dice «Se hace constar que «Nombre», del grupo «Grupo», con matrícula «Matrícula»…». Word genera una constancia por cada fila de la lista.'),
    bk('Los dos elementos', '<b>Documento principal</b> + <b>lista de destinatarios</b> (puede ser una tabla de Word, una hoja de Excel o una lista nueva).')),
    'Documento principal + lista = un documento por destinatario.')
c.L('📋', 'Destinatarios y campos', 'Bloque A · La lista y los campos', body(
    sp('En palabras sencillas', 'La lista es una tabla: cada <b>columna</b> es un <b>campo</b> (Nombre, Grupo, Matrícula) y cada <b>fila</b> es un destinatario.'),
    bk('Lista nueva o existente', 'Correspondencia &gt; Seleccionar destinatarios &gt; Escribir una lista nueva, o usar una lista existente de Excel.'),
    bk('Insertar campos', 'Coloca el cursor donde irá el dato y elige <b>Insertar campo combinado</b>. Aparece entre «».'),
    warn('Cuidado', 'Si falta un dato en la lista, el documento sale con un hueco. Revísala antes de combinar.'),
    ex('En el torneo', 'La lista tiene Ana (3-A), Luis (3-A), Marta (sin grupo) y Jorge (3-B). A Marta le falta el grupo: hay que corregirlo.')),
    'Columna = campo · Fila = destinatario · Datos completos antes de combinar.')
c.O('✉️', 'Ordena: haz la combinación', 'Genera las constancias del torneo paso a paso.', [
    ['Escribe la constancia con el texto fijo', 'Es el documento principal.'],
    ['Correspondencia > Iniciar combinación > Cartas', 'Indicas el tipo de documento.'],
    ['Seleccionar destinatarios y elegir la lista', 'Conectas la lista con el documento.'],
    ['Insertar campos combinados donde van los datos', 'Nombre, Grupo y Matrícula.'],
    ['Vista previa de resultados y recorrer los registros', 'Revisas cada constancia.'],
    ['Finalizar y combinar', 'Se generan los documentos individuales.'],
], 'Texto · iniciar · destinatarios · campos · vista previa · finalizar.')
c.raw('pMerge()')
c.L('👁️', 'Vista previa, formato e impresión', 'Bloque A · Revisa antes de finalizar', body(
    sp('En palabras sencillas', '<b>Vista previa de resultados</b> te deja ver cada registro con sus datos reales antes de generar los documentos.'),
    bk('Qué revisar', 'Que no haya campos vacíos, que los nombres largos no desborden y que el formato (fuente, tamaño) sea el mismo en todos.'),
    bk('Finalizar y combinar', '<b>Editar documentos individuales</b> crea un archivo con todas las constancias; <b>Imprimir documentos</b> las manda a la impresora; también puedes enviarlas por correo.'),
    ex('En el torneo', 'Antes de imprimir las 40 constancias, recorre todos los registros y detecta el que no tiene grupo.')),
    'Vista previa de todos los registros antes de finalizar.')
c.A('👁️', '¿Qué revisas en la vista previa?', 'Marca qué acción corresponde.', [
    ['Un registro sale con un hueco donde iba el grupo', 'Corregir la lista', 'El dato falta en la fuente, no en el documento.'],
    ['El nombre más largo se sale de la línea', 'Ajustar el formato', 'Es un problema de formato del documento principal.'],
    ['Todas las constancias se ven bien', 'Finalizar y combinar', 'Ya puedes generar o imprimir.'],
    ['Quieres una sola copia en papel de cada una', 'Imprimir documentos', 'Finalizar y combinar permite imprimir directo.'],
], 'Dato faltante → corregir la lista · Formato → ajustar el documento · Todo bien → finalizar.', ['Corregir la lista', 'Ajustar el formato', 'Finalizar y combinar', 'Imprimir documentos'])
a_end = c.mark() - 1

# ───────────────────────── B · Revisión ─────────────────────────
b0 = c.mark()
c.L('✅', 'Ortografía y revisión', 'Bloque B · Revisar un documento', body(
    sp('En palabras sencillas', 'Antes de entregar un documento conviene revisarlo con las herramientas de la ficha <b>Revisar</b>.'),
    bk('Ortografía y gramática', 'Word subraya posibles errores. <b>Tú decides</b> si aceptas la sugerencia: los nombres propios pueden ser correctos aunque aparezcan subrayados.'),
    bk('Sinónimos', 'Ayudan a evitar repetir la misma palabra.'),
    bk('Comentarios', 'Permiten dejar observaciones sin modificar el texto.'),
    ex('En el torneo', 'Word marca «Kasparov» como error: es un nombre propio y no se cambia. En cambio, «reglamenot» sí se corrige.'),
    warn('Recuerda', 'No aceptes todas las sugerencias sin leerlas.')),
    'Revisar es leer y decidir, no aceptar todo.')
c.L('🔍', 'Control de cambios', 'Bloque B · Quién cambió qué', body(
    sp('En palabras sencillas', '<b>Control de cambios</b> registra las inserciones, eliminaciones y cambios de formato, y muestra quién los hizo.'),
    bk('Cómo se usa', 'Revisar &gt; Control de cambios (actívalo antes de compartir). Cada persona edita; sus cambios aparecen de color.'),
    bk('Aceptar o rechazar', '<b>Aceptar</b> deja el cambio en el texto final. <b>Rechazar</b> regresa al texto original.'),
    ex('En el torneo', 'Alguien cambió la fecha, otra persona el lugar y un alumno propuso 10 participantes por grupo, pero el reglamento dice 4: ese cambio se rechaza.'),
    warn('Importante', 'Aceptar todo de una vez es arriesgado: revisa uno por uno.')),
    'Aceptar = pasa al texto final · Rechazar = vuelve al original.')
c.raw('pTrack()')
c.A('🔍', '¿Aceptar o rechazar?', 'Decide qué hacer con cada cambio propuesto.', [
    ['Corrige una falta de ortografía real en el aviso', 'Aceptar', 'Mejora el documento.'],
    ['Cambia la fecha del torneo por una que no está confirmada', 'Rechazar', 'Contradice la información oficial.'],
    ['Agrega una regla que ya aprobó la dirección', 'Aceptar', 'Es información correcta.'],
    ['Borra un párrafo que contiene el reglamento', 'Rechazar', 'Se pierde información necesaria.'],
], 'Mejora o dato confirmado → aceptar · Contradice o borra algo necesario → rechazar.', ['Aceptar', 'Rechazar'])
c.L('🛡️', 'Comparar y proteger', 'Bloque B · Versiones y permisos', body(
    sp('Comparar', 'Revisar &gt; Comparar muestra las <b>diferencias entre dos versiones</b> del documento, aunque nadie haya activado el control de cambios.'),
    sp('Restringir edición', 'Revisar &gt; Restringir edición protege el archivo: permite solo lectura, solo comentarios o solo cambios con control. También puedes agregar una <b>contraseña</b>.'),
    ex('En el torneo', 'El aviso final se protege como «solo lectura» para que nadie cambie la fecha por accidente.'),
    warn('Contraseña', 'Si la olvidas, no hay forma sencilla de recuperarla: anótala en un lugar seguro.')),
    'Comparar encuentra diferencias · Restringir protege el archivo final.')
c.Z('📌', 'Completa las ideas clave', 'Elige la palabra correcta en cada frase.',
    '<p>La combinación necesita un documento principal y una lista de {0}.</p>'
    '<p>Cada columna de la lista es un {1}.</p>'
    '<p>Antes de finalizar se revisa la vista {2}.</p>'
    '<p>{3} cambios muestra quién modificó el documento.</p>',
    [['destinatarios', ['destinatarios', 'imágenes', 'tablas']],
     ['campo', ['campo', 'estilo', 'índice']],
     ['previa', ['previa', 'lateral', 'final']],
     ['Control de', ['Control de', 'Índice de', 'Formato de']]])
c.W('✍️', 'Explica el proceso', 'Aplica lo aprendido.',
    'Explica cómo generarías las constancias del torneo con <b>combinación de correspondencia</b> y cómo revisarías el aviso con tu equipo usando <b>control de cambios</b>.',
    [['Tiene al menos 40 palabras', 'palabras:40'],
     ['Menciona la lista de destinatarios y los campos', '(lista|destinatario|campo)'],
     ['Menciona la vista previa', '(vista previa|revisar.*registro|previa)'],
     ['Menciona control de cambios y aceptar o rechazar', '(control de cambios|aceptar|rechazar)']],
    'Cuatro o cinco oraciones.', 'Ejemplo: Primero escribiría la constancia y una lista con nombre, grupo y matrícula…')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Combinación de correspondencia', 'Genera un documento por cada destinatario de una lista.'),
    bk('Documento principal', 'Plantilla con el texto fijo y los campos.'),
    bk('Campo combinado', 'Marcador que se sustituye por un dato de la lista.'),
    bk('Lista de destinatarios', 'Tabla de datos: columnas = campos, filas = personas.'),
    bk('Vista previa de resultados', 'Muestra el documento con los datos reales de cada registro.'),
    bk('Control de cambios', 'Registra quién cambió qué en un documento.'),
    bk('Aceptar / Rechazar', 'Decidir si un cambio queda o se descarta.'),
    bk('Comentario', 'Observación que no modifica el texto.'),
    bk('Comparar', 'Mostrar diferencias entre dos versiones.'),
    bk('Restringir edición', 'Proteger el documento contra cambios no autorizados.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas', body(
    bk('Antes de empezar', 'Grupo 311. Cada práctica tiene versión para celular. Las herramientas de <b>Diagnostica</b> no envían datos.', 'sp'),
    bk('Bloque A · combinación', 'Una o dos sesiones. <b>Práctica 1</b> con la lista de alumnos del torneo (usa datos de ejemplo).'),
    bk('Bloque B · revisión', 'Una sesión: ortografía, control de cambios, comparar y proteger. <b>Prácticas 2 y 3</b>.'),
    bk('Evaluación', 'Los alumnos entregan en la plataforma sus documentos combinados y un documento revisado con control de cambios (DOCX o PDF).')),
    'Ajusta las sesiones a tu cronograma.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '♟️', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '✉️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🔍', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"♟️",t:"Empieza aquí",d:"Combinar y revisar con el caso del torneo de ajedrez.",time:"15 min",obj:["Distinguir combinación y control de cambios","Conocer el caso y la evidencia final"],sum:["Muchos documentos → combinación.","Trabajo en equipo → control de cambios."],q:"¿Qué documento has repetido muchas veces cambiando solo un nombre?"},
a:{k:"Bloque A",l:"A",ic:"✉️",t:"Combinación de correspondencia",d:"Documento principal, lista, campos, vista previa y finalización.",time:"90 min",obj:["Preparar la lista de destinatarios","Insertar campos combinados","Revisar y finalizar la combinación"],sum:["Columna = campo · Fila = destinatario.","La vista previa detecta datos faltantes.","Finalizar genera o imprime los documentos."],q:"¿Qué dato de una lista podría faltar y arruinar tus documentos?"},
b:{k:"Bloque B",l:"B",ic:"🔍",t:"Revisión y control de cambios",d:"Ortografía, comentarios, control de cambios, comparar y proteger.",time:"90 min",obj:["Revisar sin aceptar todo a ciegas","Aceptar o rechazar cambios","Proteger el documento final"],sum:["Tú decides cada sugerencia.","Rechaza lo que contradice la información oficial.","Restringir edición protege el archivo final."],q:"¿Qué cambio de un compañero rechazarías aunque estuviera bien escrito?"},
'''

ILL = r'''
ILL["Combinación de correspondencia"]=function(){return flow([["📄","Documento|principal"],["📋","Lista|destinatarios"],["📑","Un documento|por persona"]],"Cómo funciona la combinación")};
ILL["Control de cambios"]=function(){return flow([["✏️","Alguien edita"],["🎨","Se marca el cambio"],["✔️","Aceptar o rechazar"]],"Ciclo de revisión")};
'''

EXH = r'''
EXH.lista=function(){return exw('<table class="mtb"><tr><th>Nombre</th><th>Grupo</th><th>Matrícula</th></tr><tr><td>Ana Torres</td><td>3-A</td><td>2601</td></tr><tr><td>Luis Pérez</td><td>3-A</td><td>2602</td></tr><tr><td>Marta Ruiz</td><td>3-B</td><td>2603</td></tr><tr><td>Jorge Díaz</td><td>3-B</td><td>2604</td></tr></table>',['Usa datos de ejemplo o de compañeros que lo autoricen.','Una columna por campo y sin celdas vacías.'])};
EXH.constancia=function(){return exw('<div class="mbox" style="text-align:center"><b>CONSTANCIA</b><br>Se hace constar que <b>«Nombre»</b>, del grupo <b>«Grupo»</b>, con matrícula <b>«Matrícula»</b>, participó en el torneo.</div>',['Los campos se insertan con Insertar campo combinado.'])};
EXH.simulador=function(){return exw('<div class="mbox">✉️ <b>Simulador de combinación</b> (pestaña Diagnostica)<br>✅ Se crearon 4 constancias, una por destinatario.</div>',['Úsalo para practicar antes de hacerlo en Word.'])};
EXH.texto=function(){return exw('<div class="mbox">El torneo se realisará el 20 de noviembre en el auditorio del plantel. Cada grupo inscribira a 4 participantes. Los alumnos deben traer su credensial.</div>',['Texto de ejemplo con errores de ortografía.','Corrige los que sean errores y deja los que sean correctos.'])};
EXH.cambios=function(){return exw('<div class="mbox">El torneo se realizará el <del style="color:#b91c1c">18</del> <ins style="color:#166534">20</ins> de noviembre.<br><small>Revisar &gt; Aceptar o Rechazar</small></div>',['Activa Control de cambios antes de editar.','Haz al menos tres cambios diferentes.'])};
EXH.proteger=function(){return exw('<div class="mbox">Revisar &gt; Restringir edición<br>☑ Permitir solo este tipo de edición: <b>Sin cambios (solo lectura)</b><br>🔒 Sí, aplicar protección</div>',['Usa una contraseña que puedas recordar.','Prueba abrir el documento y editar: no debe dejarte.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Constancias con combinación de correspondencia',
     'prog': 'Bloque A · Combinación',
     'min': 50, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word', 'Este material (Simulador de combinación)'],
                'steps': [
                    ['Practica en el Simulador de combinación de la pestaña Diagnostica y corrige el dato vacío.', 'simulador'],
                    ['Crea la lista de destinatarios (4 personas) en una tabla de Word o una hoja de Excel.', 'lista'],
                    ['Escribe la constancia e inserta los campos combinados.', 'constancia'],
                    'Revisa la Vista previa de resultados de todos los registros.',
                    'Finalizar y combinar > Editar documentos individuales, y guarda el resultado como PDF.']},
         'cel': {'mat': ['Celular', 'Este material (Simulador de combinación)', 'Notas o Documentos de Google'],
                 'steps': [
                     ['Practica en el Simulador de combinación de la pestaña Diagnostica y corrige el dato vacío.', 'simulador'],
                     ['Escribe la lista de 4 destinatarios con nombre, grupo y matrícula.', 'lista'],
                     ['Escribe la constancia y marca dónde irían los campos.', 'constancia'],
                     'Describe qué revisarías en la vista previa.',
                     'Si tienes acceso a Word, haz la combinación y guarda un PDF.']}},
     'entrega': ['Constancias generadas (PDF) o, desde celular, la lista, la plantilla y la descripción del proceso.'],
     'rub': [['Lista completa y bien organizada', 25], ['Campos insertados correctamente', 30], ['Vista previa revisada', 20], ['Documentos finales', 25]]},
    {'id': 'pr2', 'n': 2, 't': 'Revisa un aviso con ortografía y comentarios',
     'prog': 'Bloque B · Ortografía y revisión',
     'min': 35, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word'],
                'steps': [
                    ['Copia el texto de ejemplo a Word y ejecuta Revisar > Ortografía y gramática.', 'texto'],
                    'Corrige solo los errores reales y deja los nombres propios correctos.',
                    'Usa el diccionario de sinónimos para evitar una palabra repetida.',
                    'Agrega dos comentarios con observaciones para el autor.']},
         'cel': {'mat': ['App de Word o Documentos de Google'],
                 'steps': [
                     ['Copia el texto de ejemplo y revisa la ortografía.', 'texto'],
                     'Corrige solo los errores reales.',
                     'Cambia una palabra repetida por un sinónimo.',
                     'Agrega dos comentarios con observaciones.']}},
     'entrega': ['Texto corregido con dos comentarios (captura o archivo).'],
     'rub': [['Errores reales corregidos', 35], ['Nombres propios respetados', 20], ['Sinónimo bien usado', 20], ['Comentarios útiles', 25]]},
    {'id': 'pr3', 'n': 3, 't': 'Control de cambios, comparar y proteger',
     'prog': 'Bloque B · Revisión en equipo',
     'min': 45, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word', 'Este material (Control de cambios)'],
                'steps': [
                    ['Resuelve el simulador de Control de cambios en la pestaña Diagnostica.', 'cambios'],
                    ['Activa Control de cambios en Word y haz tres cambios al aviso.', 'cambios'],
                    'Pásalo a un compañero para que acepte o rechace cada cambio.',
                    'Guarda una copia, edítala y usa Comparar para ver las diferencias.',
                    ['Protege el documento final con Restringir edición.', 'proteger']]},
         'cel': {'mat': ['App de Word o Documentos de Google', 'Este material (Control de cambios)'],
                 'steps': [
                     ['Resuelve el simulador de Control de cambios en la pestaña Diagnostica.', 'cambios'],
                     ['Activa el modo de sugerencias o control de cambios y haz tres cambios.', 'cambios'],
                     'Pásalo a un compañero para que acepte o rechace.',
                     'Compara la versión original con la final y anota las diferencias.',
                     ['Comparte el documento solo con permiso de lectura.', 'proteger']]}},
     'entrega': ['Documento con cambios revisados y protección aplicada (captura o archivo).'],
     'rub': [['Cambios registrados', 25], ['Aceptar y rechazar con criterio', 30], ['Comparación de versiones', 20], ['Protección', 25]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Documentos digitales avanzados · Unidad 1',
    'ra': 'R.A. 1.3', 'title': 'Documentos combinados y revisión con control de cambios',
    'data': [
        ('Resultado de aprendizaje', 'Genera documentos mediante combinación de correspondencia y revisa documentos de manera colaborativa.'),
        ('Actividad de evaluación', 'Elabora documentos mediante combinación de correspondencia y demuestra el uso de revisión y control de cambios.'),
        ('Evidencia', 'Documentos combinados y documento revisado (DOCX o PDF)'),
        ('Entrega', 'En la actividad R.A. 1.3 de la plataforma. Si aún no entregas, consulta con tu docente.'),
    ],
    'situation': 'Prepara documentos para un evento de tu plantel con combinación de correspondencia y un aviso revisado en equipo.',
    'hint': 'Practica primero en la pestaña Diagnostica y revisa tu entrega con la rúbrica.',
    'steps': [
        ('Lista y plantilla', ['Crea la lista de destinatarios y el documento principal.']),
        ('Combinación', ['Inserta campos, revisa la vista previa y finaliza la combinación.']),
        ('Revisión', ['Activa el control de cambios, haz cambios y acepta o rechaza con criterio.']),
        ('Protección', ['Compara versiones y protege el documento final.']),
        ('Entrega', ['Guarda como DOCX o PDF y súbelos en la plataforma.']),
    ],
    'rubric': [('Lista y documento principal', 20), ('Campos y vista previa', 25), ('Documentos combinados', 15), ('Control de cambios', 25), ('Comparar y proteger', 15)],
    'deliver': ['Archivos DOCX o PDF con los documentos combinados y el documento revisado.', 'Se entregan en la actividad R.A. 1.3 de la plataforma.'],
}
