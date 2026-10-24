"""EDOA-20 · R.A. 1.2 · Inserción y formato de objetos (Word).

Caso de las lecciones: Club de Fotografía del plantel (horarios, galería y reporte de actividades).
La actividad de evaluación es la entrega del documento (.docx o PDF) en la plataforma.
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-1.2'
CODE_PREFIX = 'EDOA12'
FILE = 'edoa-ra12-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 1.2 · Inserción y formato de objetos'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 1.2 · Inserción y formato de objetos'
HERO_KICK = 'EDOA-20 · R.A. 1.2'
HERO_TITLE = 'Tablas, imágenes y referencias que hacen claro un documento'
HERO_TEXT = 'Aprende a insertar tablas, imágenes y objetos de referencia en Word y a darles formato, con el caso del Club de Fotografía.'
EV_SHORT = 'elabora tu documento con tablas, imágenes y referencias.'
EV_CARD = 'Documento R.A. 1.2'
RA = 'R.A. 1.2'
GROUP = '311'
TABS = {'d': ['Diagnostica', 'Constructor de tablas y ajuste de texto'], 'c': ['Construye', 'Prácticas en Word']}

EXTRA_JS = r'''
function pTabla(){K++;return '<article class="lesson"><header><span class="kick">🧱 Herramienta</span><h1>Constructor de tablas</h1><p class="sub">Elige filas, columnas y opciones de estilo, como en Insertar &gt; Tabla de Word. Cumple los tres retos.</p></header><style>.tbx .ctl{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.tbx label{font-weight:700;font-size:14px;display:block}.tbx select{width:100%;padding:10px;border:2px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:16px inherit}.tbx .ck{display:flex;flex-wrap:wrap;gap:8px 16px;margin:12px 0}.tbx .ck label{font-weight:500;display:flex;gap:6px;align-items:center}.tbx .pv{overflow-x:auto;margin:10px 0;padding:10px;background:var(--bg);border-radius:12px}.tbx table{border-collapse:collapse;min-width:260px;width:100%;background:#fff;color:#111}.tbx td,.tbx th{padding:6px 10px;font-size:14px}.tbx .bd td,.tbx .bd th{border:1px solid #888}.tbx .hd th{background:#2b579a;color:#fff}.tbx .bn tr:nth-child(even) td{background:#e8eef8}.tbx .ct td,.tbx .ct th{text-align:center}.tbx ul{list-style:none;padding:0;margin:8px 0}.tbx li{padding:5px 0}</style><div class="tbx"><div class="ctl"><label>Columnas<select class="tc"></select></label><label>Filas<select class="tr"></select></label></div><div class="ck"><label><input type="checkbox" class="oh"> Fila de encabezado</label><label><input type="checkbox" class="ob"> Filas con bandas</label><label><input type="checkbox" class="od"> Bordes</label><label><input type="checkbox" class="oc"> Centrar el contenido</label></div><div class="pv"></div><ul class="rt"></ul></div><p class="take"><b>En Word:</b> Insertar &gt; Tabla. Después, en <b>Diseño de tabla</b> activas encabezado y bandas, y en <b>Presentación</b> alineas el contenido.</p></article>'}
function tabInit(d){var w=d.querySelector(".tbx");if(!w)return;function g(c){return w.querySelector("."+c)}
 var tc=g("tc"),tr=g("tr"),got=[0,0,0];for(var i=1;i<=7;i++){tc.innerHTML+='<option>'+i+'</option>'}for(i=1;i<=8;i++){tr.innerHTML+='<option>'+i+'</option>'}tc.value=3;tr.value=3;
 var RT=["Tabla de 4 columnas y 5 filas con fila de encabezado","Tabla con bandas y bordes","Contenido centrado"];
 function run(x){var c=+tc.value,r=+tr.value,h=g("oh").checked,b=g("ob").checked,bd=g("od").checked,ce=g("oc").checked,s='<table class="'+(bd?"bd ":"")+(h?"hd ":"")+(b?"bn ":"")+(ce?"ct":"")+'">';
  for(var i=0;i<r;i++){s+='<tr>';for(var j=0;j<c;j++){s+=(i==0&&h?'<th>':'<td>')+(i==0&&h?'Col '+(j+1):'Dato')+(i==0&&h?'</th>':'</td>')}s+='</tr>'}g("pv").innerHTML=s+'</table>';
  if(x){if(c==4&&r==5&&h)got[0]=1;if(b&&bd&&h)got[1]=1;if(ce&&h&&bd)got[2]=1}
  g("rt").innerHTML=RT.map(function(t,k){return '<li>'+(got[k]?'✅':'⬜')+' '+t+'</li>'}).join('');
  if(got[0]&&got[1]&&got[2]){var t="t:Constructor de tablas";if(!ST[t]){ST[t]=1;sv()}}}
 [tc,tr,g("oh"),g("ob"),g("od"),g("oc")].forEach(function(e){e.onchange=function(){run(1)}});run(0)}
function pAjuste(){K++;return '<article class="lesson"><header><span class="kick">🖼️ Herramienta</span><h1>Ajuste de texto</h1><p class="sub">Cambia el ajuste y la posición de la imagen y mira cómo se acomoda el texto. Cumple los tres retos.</p></header><style>.ajx .pgx{position:relative;background:#fff;color:#111;border:1px solid var(--line);border-radius:6px;padding:16px;font:14px/1.6 Georgia,serif;min-height:230px;overflow:hidden}.ajx .im{width:84px;height:64px;background:#9ec1f0;border:2px solid #2b579a;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:28px}.ajx .pgx p{position:relative;z-index:1;margin:0}.ajx .bt{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.ajx .bt button{padding:8px 11px;border:2px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:600 13px inherit;cursor:pointer}.ajx .bt button.on{border-color:var(--pri);background:var(--exb)}.ajx ul{list-style:none;padding:0;margin:8px 0}.ajx li{padding:4px 0}</style><div class="ajx"><div class="bt wr"></div><div class="bt po"></div><div class="pgx"><div class="im">📷</div><p>El Club de Fotografía se reúne los martes y jueves en el laboratorio de cómputo. Los alumnos aprenden encuadre, luz natural y edición básica, y cada mes presentan una galería con sus mejores fotografías. Para participar solo necesitas tu credencial y una cámara o un celular; el club presta tripiés y luces para las prácticas. Al final del semestre se imprime un reporte con las fotos más votadas. Cada alumno elige una foto, escribe quién la tomó y explica por qué le gusta; después el grupo vota y el club exhibe las ganadoras en el pasillo del laboratorio durante una semana completa.</p></div><ul class="rt"></ul></div><p class="take"><b>En Word:</b> selecciona la imagen &gt; <b>Formato de imagen</b> &gt; Ajustar texto. «En línea con el texto» trata la imagen como una letra más.</p></article>'}
function ajuInit(d){var w=d.querySelector(".ajx");if(!w)return;function g(c){return w.querySelector("."+c)}
 var WR=[["inl","En línea con el texto"],["sq","Cuadrado"],["tb","Arriba y abajo"],["bh","Detrás del texto"],["fr","Delante del texto"]],PO=[["l","Izquierda"],["c","Centro"],["r","Derecha"]],mode="inl",pos="l",got=[0,0,0],im=g("im");
 var RT=["Que el texto rodee la imagen por la derecha (Cuadrado y Derecha)","Imagen detrás del texto, como marca de agua","Imagen sola en su renglón (Arriba y abajo)"];
 g("wr").innerHTML=WR.map(function(x){return '<button data-w="'+x[0]+'">'+x[1]+'</button>'}).join("");g("po").innerHTML=PO.map(function(x){return '<button data-p="'+x[0]+'">'+x[1]+'</button>'}).join("");
 function run(x){var s="margin:0;";if(mode=="inl")s+="display:inline-block;vertical-align:middle;margin-right:8px;";if(mode=="sq")s+="float:"+(pos=="r"?"right":"left")+";margin:0 "+(pos=="r"?"0 6px 12px":"12px 6px 0")+";";if(mode=="tb")s+="display:block;margin:6px "+(pos=="r"?"0 6px auto":pos=="c"?"auto 6px":"auto 6px 0")+";";
  if(mode=="bh"||mode=="fr"){s+="position:absolute;top:70px;"+(pos=="r"?"right:30px":pos=="c"?"left:calc(50% - 42px)":"left:30px")+";width:140px;height:110px;z-index:"+(mode=="bh"?0:2)+";"+(mode=="bh"?"opacity:.35;":"opacity:1;")}
  im.setAttribute("style",s);w.querySelectorAll("[data-w]").forEach(function(b){b.className=b.dataset.w==mode?"on":""});w.querySelectorAll("[data-p]").forEach(function(b){b.className=b.dataset.p==pos?"on":""});
  if(x){if(mode=="sq"&&pos=="r")got[0]=1;if(mode=="bh")got[1]=1;if(mode=="tb")got[2]=1}
  g("rt").innerHTML=RT.map(function(t,k){return '<li>'+(got[k]?'✅':'⬜')+' '+t+'</li>'}).join("");
  if(got[0]&&got[1]&&got[2]){var t="t:Ajuste de texto";if(!ST[t]){ST[t]=1;sv()}}}
 w.querySelectorAll("[data-w]").forEach(function(b){b.onclick=function(){mode=b.dataset.w;run(1)}});w.querySelectorAll("[data-p]").forEach(function(b){b.onclick=function(){pos=b.dataset.p;run(1)}});run(0)}
'''
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n tabInit(d);ajuInit(d);\n'),
]

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('📷', 'Un documento que se entiende de un vistazo', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Un documento de Word no es solo texto. Con <b>tablas</b>, <b>imágenes</b> y <b>objetos de referencia</b> (índice, notas, vínculos) la información se encuentra rápido y se lee mejor.'),
    ex('Caso de las lecciones: Club de Fotografía del plantel', 'El club necesita un reporte con su horario de sesiones (una tabla), fotos de la galería con el texto acomodado alrededor, un índice y notas que citen de dónde salió cada dato.'),
    bk('Qué vas a hacer', '<b>1. Aprende</b> los conceptos con ejemplos. <b>2. Diagnostica</b> con un constructor de tablas y un simulador de ajuste de texto. <b>3. Construye</b> tres prácticas en Word que te preparan para tu documento final.'),
    bk('Al final', 'Entregas un <b>documento digital</b> (DOCX o PDF) con tablas, imágenes, referencias y objetos bien formateados.')),
    'Tablas ordenan, imágenes ilustran y las referencias ayudan a encontrar y a confiar.')
c.A('🔎', '¿Qué objeto necesitas?', 'Relaciona cada necesidad del club con el objeto de Word.', [
    ['Mostrar el horario de las sesiones por día y hora', 'Tabla', 'Organiza datos en filas y columnas.'],
    ['Ilustrar el reporte con una foto de la galería', 'Imagen', 'Se inserta desde el equipo o una fuente autorizada.'],
    ['Ir de una sección larga a otra con un clic', 'Hipervínculo', 'Conecta con una página, archivo o sección.'],
    ['Aclarar de dónde salió un dato sin interrumpir el texto', 'Nota al pie', 'Agrega la explicación al final de la página.'],
], 'Datos → tabla · Ilustrar → imagen · Saltar → hipervínculo · Aclarar → nota al pie.', ['Tabla', 'Imagen', 'Hipervínculo', 'Nota al pie'])
s0_end = c.mark() - 1

# ───────────────────────── A · Tablas ─────────────────────────
a0 = c.mark()
c.L('🧱', 'Tablas', 'Bloque A · Organizar datos', body(
    sp('En palabras sencillas', 'Una <b>tabla</b> organiza información en <b>filas</b> (horizontales) y <b>columnas</b> (verticales). Cada cruce es una <b>celda</b>.'),
    bk('Cómo se inserta', 'Insertar &gt; Tabla: eliges con el cursor cuántas columnas y filas. También puedes dibujarla o convertir texto en tabla.'),
    bk('Pestañas nuevas', 'Al seleccionar la tabla aparecen <b>Diseño de tabla</b> (estilos, encabezado, bandas, bordes) y <b>Presentación</b> (insertar o eliminar filas, combinar celdas, alinear).'),
    ana('Piensa en…', 'Un horario escolar impreso: los días son columnas, las horas son filas y cada cuadro dice qué materia toca.'),
    ex('En el club', 'Horario de sesiones: 4 columnas (Día, Hora, Lugar, Tema) y 5 filas. La primera fila es el <b>encabezado</b> y se pone en negritas con relleno de color.'),
    warn('Recuerda', 'Una tabla con encabezado claro, bordes suaves y contenido alineado se lee mejor que una con muchos colores.')),
    'Tabla = filas + columnas · Diseño de tabla = aspecto · Presentación = estructura.')
c.A('🧱', '¿En qué pestaña está?', 'Elige dónde encuentras cada opción de la tabla.', [
    ['Activar fila de encabezado y filas con bandas', 'Diseño de tabla', 'Son opciones de estilo de tabla.'],
    ['Insertar una fila arriba o eliminar una columna', 'Presentación', 'Cambia la estructura de la tabla.'],
    ['Cambiar los bordes y el relleno', 'Diseño de tabla', 'Controla el aspecto.'],
    ['Combinar dos celdas en una', 'Presentación', 'Es un cambio de estructura.'],
    ['Alinear el texto al centro de la celda', 'Presentación', 'La alineación está en Presentación.'],
], 'Aspecto → Diseño de tabla · Estructura y alineación → Presentación.', ['Diseño de tabla', 'Presentación'])
c.O('🧱', 'Ordena: crea la tabla del horario', 'Arma la tabla del club paso a paso.', [
    ['Ubica el cursor donde irá la tabla', 'Primero decides el lugar.'],
    ['Insertar > Tabla y elige 4 columnas por 5 filas', 'Se crea la estructura.'],
    ['Escribe los encabezados en la primera fila', 'Día, Hora, Lugar y Tema.'],
    ['Captura los datos de cada sesión', 'Llenas el resto de las celdas.'],
    ['Aplica el estilo en Diseño de tabla y alinea en Presentación', 'El formato va al final.'],
], 'Lugar · insertar · encabezados · datos · formato.')
c.raw('pTabla()')
a_end = c.mark() - 1

# ───────────────────────── B · Imágenes y otros objetos ─────────────────────────
b0 = c.mark()
c.L('🖼️', 'Imágenes y ajuste de texto', 'Bloque B · Ilustrar el documento', body(
    sp('En palabras sencillas', 'Una imagen se inserta desde <b>Insertar &gt; Imágenes</b>, ya sea del equipo, de internet o de un banco de imágenes autorizado.'),
    bk('Tamaño', 'Arrastra una <b>esquina</b> para cambiar el tamaño sin deformar; si arrastras un costado, la imagen se estira.'),
    bk('Ajuste de texto', '<b>En línea</b>: la imagen es como una letra. <b>Cuadrado</b>: el texto la rodea. <b>Arriba y abajo</b>: el texto queda solo arriba y abajo. <b>Detrás</b> o <b>delante</b> del texto: la imagen flota libre.'),
    ex('En el club', 'La foto de portada va con ajuste <b>Cuadrado</b> a la derecha para que el texto la rodee. El logo del club va <b>Detrás del texto</b> como marca de agua.'),
    warn('Derechos de autor', 'Usa fotos propias o con licencia que permita su uso, y escribe la fuente.')),
    'Esquina para escalar · Ajuste de texto para acomodar.')
c.raw('pAjuste()')
c.A('🖼️', '¿Qué ajuste de texto usarías?', 'Elige el ajuste más adecuado.', [
    ['Quieres que el texto rodee la foto de la galería', 'Cuadrado', 'El texto se acomoda alrededor de la imagen.'],
    ['La imagen es un ícono pequeño dentro de un renglón', 'En línea con el texto', 'Se comporta como un carácter más.'],
    ['El logo del club debe verse tenue detrás de todo el texto', 'Detrás del texto', 'La imagen flota debajo del texto.'],
    ['Una imagen grande debe ir sola entre dos párrafos', 'Arriba y abajo', 'No deja texto a los lados.'],
], 'Rodear → cuadrado · Como letra → en línea · Marca de agua → detrás · Sola → arriba y abajo.', ['Cuadrado', 'En línea con el texto', 'Detrás del texto', 'Arriba y abajo'])
c.L('📎', 'Otros objetos', 'Bloque B · Hojas, gráficas, video y sonido', body(
    sp('En palabras sencillas', 'Word puede integrar <b>hojas de cálculo</b>, gráficos, documentos y presentaciones, y también <b>vincular</b> videos o sonidos cuando el formato lo permite.'),
    bk('Insertar o vincular', '<b>Insertar</b> guarda una copia dentro del documento: no cambia si el original cambia. <b>Vincular</b> mantiene una conexión: se actualiza, pero si mueves el archivo original se pierde.'),
    ex('En el club', 'Una gráfica de Excel con las fotos más votadas se inserta para mostrar números. El video del taller se vincula, porque pesa mucho.'),
    bk('Cuándo elegir', 'Copia fija → insertar. Datos que cambian → vincular.')),
    'Insertar = copia dentro · Vincular = conexión al original.')
c.A('📎', '¿Insertar o vincular?', 'Decide qué conviene en cada caso.', [
    ['Una tabla de calificaciones que se va a actualizar cada semana', 'Vincular', 'Se actualiza desde el archivo original.'],
    ['Una gráfica final que no va a cambiar', 'Insertar', 'Una copia dentro del documento es suficiente.'],
    ['Un video pesado que no quieres meter al archivo', 'Vincular', 'Evita que el documento crezca mucho.'],
    ['Quieres enviar el documento por correo sin archivos aparte', 'Insertar', 'Todo viaja dentro del mismo archivo.'],
], 'Cambia → vincular · Fijo o portátil → insertar.', ['Insertar', 'Vincular'])
b_end = c.mark() - 1

# ───────────────────────── C · Referencias y formato ─────────────────────────
c0 = c.mark()
c.L('🔗', 'Objetos de referencia', 'Bloque C · Índice, notas, vínculos y citas', body(
    sp('En palabras sencillas', 'Son objetos que ayudan a <b>encontrar</b> información y a <b>respaldar</b> de dónde sale.'),
    bk('Hipervínculo', 'Conecta con una página web, un archivo o una sección del mismo documento (Insertar &gt; Vínculo).'),
    bk('Índice automático', 'Primero aplicas <b>Título 1, Título 2…</b> a los encabezados y después insertas la tabla de contenido (Referencias &gt; Tabla de contenido). Se actualiza con un clic.'),
    bk('Nota al pie', 'Agrega una aclaración al final de la página sin interrumpir el texto (Referencias &gt; Insertar nota al pie).'),
    bk('Cita y bibliografía', 'Identifican la fuente: autor, título, año y sitio.'),
    warn('Importante', 'El índice automático <b>solo</b> reconoce los estilos de título; si pones el título solo en negritas, no aparece.')),
    'Estilos de título → índice automático · Nota al pie aclara · Cita respalda.')
c.O('🔗', 'Ordena: genera el índice', 'Pon el índice del reporte del club.', [
    ['Escribe todos los encabezados del reporte', 'Primero va el contenido.'],
    ['Aplica Título 1 y Título 2 a los encabezados', 'Sin estilos no hay índice.'],
    ['Ubica el cursor al inicio del documento', 'Ahí irá el índice.'],
    ['Referencias > Tabla de contenido', 'Se genera el índice.'],
    ['Actualiza la tabla si cambias algún título', 'Así siempre está al día.'],
], 'Contenido · estilos · lugar · insertar · actualizar.')
c.A('🔗', '¿Cuál objeto es?', 'Relaciona cada necesidad con el objeto de referencia.', [
    ['Saltar de la portada a la sección de la galería con un clic', 'Hipervínculo', 'Conecta con otra parte del documento.'],
    ['Mostrar la lista de secciones con su página al inicio', 'Tabla de contenido', 'Se genera con los estilos de título.'],
    ['Aclarar al pie de la hoja de dónde viene un dato', 'Nota al pie', 'No interrumpe el texto.'],
    ['Indicar el autor y el año de un texto que usaste', 'Cita', 'Identifica la fuente.'],
], 'Saltar → hipervínculo · Lista de secciones → tabla de contenido · Aclarar → nota · Fuente → cita.', ['Hipervínculo', 'Tabla de contenido', 'Nota al pie', 'Cita'])
c.L('🎨', 'Formato de objetos', 'Bloque C · Que todo se vea ordenado', body(
    sp('En palabras sencillas', 'Cada objeto tiene un formato propio. Las opciones principales son estas.'),
    bk('Tamaño', 'Alto y ancho. Mantén la proporción para no deformar.'),
    bk('Posición', 'Dónde queda el objeto dentro de la página.'),
    bk('Ajuste de texto', 'Cómo se relaciona el objeto con los párrafos.'),
    bk('Fondo, borde y efectos', 'Deben apoyar la lectura, no distraer: un borde fino y una sombra suave basta.'),
    bk('Alinear', 'Con varios objetos, usa <b>Alinear</b> y <b>Distribuir</b> en lugar de moverlos a ojo.'),
    ex('En el club', 'Tres fotos pequeñas: mismo tamaño, alineadas por la parte superior y distribuidas con el mismo espacio entre ellas.')),
    'Tamaño, posición, ajuste y estilo: pocos efectos y bien alineados.')
c.Z('📌', 'Completa las ideas clave', 'Elige la palabra correcta en cada frase.',
    '<p>Una tabla organiza datos en filas y {0}.</p>'
    '<p>Las opciones de encabezado y bandas están en {1}.</p>'
    '<p>Para escalar una imagen sin deformarla arrastras una {2}.</p>'
    '<p>El índice automático necesita estilos de {3}.</p>',
    [['columnas', ['columnas', 'páginas', 'notas']],
     ['Diseño de tabla', ['Diseño de tabla', 'Presentación', 'Referencias']],
     ['esquina', ['esquina', 'costado', 'nota']],
     ['título', ['título', 'color', 'sombra']]])
c.W('✍️', 'Planea tu reporte', 'Aplica lo aprendido.',
    'Describe cómo armarías el reporte del Club de Fotografía: qué <b>tabla</b> pondrías, dónde irían las <b>imágenes</b> y con qué ajuste, y qué <b>objetos de referencia</b> usarías.',
    [['Tiene al menos 35 palabras', 'palabras:35'],
     ['Menciona una tabla', '\\b(tabla\\w*|fila\\w*|columna\\w*)\\b'],
     ['Menciona una imagen y su ajuste', '\\b(imagen\\w*|foto\\w*|ajuste|cuadrado)\\b'],
     ['Menciona índice, nota, vínculo o cita', '\\b(indice|nota\\w*|vinculo\\w*|hipervinculo\\w*|cita\\w*|referencia\\w*|bibliograf\\w+)\\b']],
    'Tres o cuatro oraciones.', 'Ejemplo: Pondría una tabla con el horario, una foto con ajuste cuadrado y un índice…')
c_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Tabla', 'Objeto con filas y columnas para ordenar datos.'),
    bk('Celda', 'Cruce de una fila y una columna.'),
    bk('Encabezado', 'Primera fila de la tabla con el nombre de cada columna.'),
    bk('Ajuste de texto', 'Cómo se acomoda el texto alrededor de un objeto.'),
    bk('Hipervínculo', 'Enlace que lleva a otra página, archivo o sección.'),
    bk('Estilo de título', 'Formato predefinido (Título 1, 2…) que permite generar el índice.'),
    bk('Tabla de contenido', 'Índice automático del documento.'),
    bk('Nota al pie', 'Aclaración al final de la página.'),
    bk('Cita', 'Referencia a la fuente de una idea o dato.'),
    bk('Vincular', 'Conectar un objeto con su archivo original.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas', body(
    bk('Antes de empezar', 'Grupo 311. Cada práctica tiene versión para celular. Las herramientas de <b>Diagnostica</b> no envían datos y funcionan en celular.', 'sp'),
    bk('Bloque A · tablas', 'Una sesión: tablas y estilos. <b>Práctica 1</b> en clase.'),
    bk('Bloque B · imágenes y otros objetos', 'Una sesión: imágenes, ajuste de texto y objetos incrustados. <b>Práctica 2</b>.'),
    bk('Bloque C · referencias y formato', 'Una sesión: índice, notas, vínculos y formato. <b>Práctica 3</b>.'),
    bk('Evaluación', 'Los alumnos entregan en la plataforma un documento digital (DOCX o PDF) con tabla, imágenes, referencias y objetos bien formateados.')),
    'Ajusta las sesiones a tu cronograma.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '📷', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🧱', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🖼️', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🔗', 'a': c0, 'b': c_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"📷",t:"Empieza aquí",d:"Los objetos de un documento con el caso del Club de Fotografía.",time:"15 min",obj:["Reconocer qué objeto resuelve cada necesidad","Conocer el caso y la evidencia final"],sum:["Datos → tabla · Ilustrar → imagen · Saltar → vínculo · Aclarar → nota.","Entregas un documento con tablas, imágenes y referencias."],q:"¿Qué documento tuyo se vería mejor con una tabla o una imagen?"},
a:{k:"Bloque A",l:"A",ic:"🧱",t:"Tablas",d:"Insertar, estilo y estructura de tablas.",time:"60 min",obj:["Insertar una tabla del tamaño correcto","Distinguir Diseño de tabla y Presentación","Dar formato legible a una tabla"],sum:["Tabla = filas + columnas.","Aspecto en Diseño de tabla; estructura en Presentación.","Encabezado claro y pocos colores."],q:"¿Qué tabla usas en tu vida diaria y cómo la mejorarías?"},
b:{k:"Bloque B",l:"B",ic:"🖼️",t:"Imágenes y otros objetos",d:"Imágenes, ajuste de texto, hojas, gráficas, video y sonido.",time:"70 min",obj:["Escalar una imagen sin deformarla","Elegir el ajuste de texto adecuado","Decidir entre insertar y vincular"],sum:["Esquina para escalar.","Cuadrado rodea; en línea es como letra; detrás es marca de agua.","Insertar = copia · Vincular = conexión."],q:"¿Qué imagen de tu escuela usarías en un reporte y de dónde la tomarías?"},
c:{k:"Bloque C",l:"C",ic:"🔗",t:"Referencias y formato",d:"Hipervínculos, índice, notas al pie, citas y formato de objetos.",time:"70 min",obj:["Generar un índice automático","Insertar notas y vínculos","Alinear y dar formato a varios objetos"],sum:["Sin estilos de título no hay índice.","La nota aclara sin interrumpir.","Alinear y distribuir en vez de mover a ojo."],q:"¿Cuándo te sirve más un índice: en un documento de 2 páginas o de 20?"},
'''

ILL = r'''
ILL["Tablas"]=function(){return grid3([["🏷️","Encabezado"],["▦","Filas"],["▥","Columnas"]],"Partes de una tabla")};
ILL["Imágenes y ajuste de texto"]=function(){return flow([["📷","Insertar"],["↔️","Escalar|esquina"],["📝","Ajustar texto"]],"De la foto al documento")};
ILL["Objetos de referencia"]=function(){return grid3([["🔗","Vínculo"],["📑","Índice"],["¹","Nota al pie"]],"Objetos de referencia")};
'''

EXH = r'''
EXH.horario=function(){return exw('<table class="mtb"><tr><th>Día</th><th>Hora</th><th>Lugar</th><th>Tema</th></tr><tr><td>Martes</td><td>15:00</td><td>Lab. de cómputo</td><td>Encuadre</td></tr><tr><td>Jueves</td><td>15:00</td><td>Lab. de cómputo</td><td>Luz natural</td></tr><tr><td>Martes</td><td>15:00</td><td>Patio</td><td>Retrato</td></tr><tr><td>Jueves</td><td>15:00</td><td>Lab. de cómputo</td><td>Edición</td></tr></table>',['Ejemplo de tabla del club. Haz la tuya con 4 columnas y 5 filas.','El encabezado va en negritas y con relleno de color.'])};
EXH.constructor=function(){return exw('<div class="mbox">🧱 <b>Constructor de tablas</b> (pestaña Diagnostica)<br>✅ Tabla de 4 columnas y 5 filas con encabezado<br>✅ Con bandas y bordes<br>✅ Contenido centrado</div>',['Úsalo para probar el estilo antes de hacerlo en Word.'])};
EXH.ajuste=function(){return exw('<div class="mbox"><b>Imagen con ajuste Cuadrado a la derecha</b><br>Formato de imagen &gt; Ajustar texto &gt; Cuadrado<br><small>Tamaño: mismo ancho para todas las fotos · Borde fino gris</small></div>',['Arrastra una esquina para escalar.','Revisa que el texto no quede pegado a la imagen.'])};
EXH.fuente=function(){return exw('<table class="mtb"><tr><th>Dato</th><th>Ejemplo</th></tr><tr><td>Autor</td><td>Tu nombre</td></tr><tr><td>Título</td><td>Fotografía del club</td></tr><tr><td>Año</td><td>2026</td></tr><tr><td>Fuente</td><td>Archivo propio</td></tr></table>',['Usa fotos propias o con licencia.','Escribe la fuente en una nota al pie.'])};
EXH.indice=function(){return exw('<div class="mbox"><b>Contenido</b><br>1. Club de Fotografía ........ 1<br>&nbsp;&nbsp;1.1 Horario ........ 1<br>&nbsp;&nbsp;1.2 Galería ........ 2<br>2. Reglas del club ........ 3</div>',['Aplica Título 1 y Título 2 antes de insertar el índice.','Referencias &gt; Tabla de contenido.'])};
EXH.notaviculo=function(){return exw('<div class="mbox">Las sesiones son los martes y jueves<sup>1</sup>. Consulta el <u style="color:#2b579a">reglamento del club</u>.<hr style="margin:8px 0"><small><sup>1</sup> Fuente: coordinación del club, 2026.</small></div>',['La nota al pie va en la misma página que el dato.','El hipervínculo puede llevar a una sección del documento.'])};
EXH.alinear=function(){return exw('<div class="mbox"><b>Tres fotos alineadas</b><br>Selecciona las tres &gt; Formato de imagen &gt; Alinear &gt; Alinear arriba y Distribuir horizontalmente.</div>',['Todas del mismo tamaño.','Mismo espacio entre ellas.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Horario del club en una tabla',
     'prog': 'Bloque A · Tablas',
     'min': 40, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word', 'Este material (Constructor de tablas)'],
                'steps': [
                    ['Prueba tu estilo en el Constructor de tablas de la pestaña Diagnostica y cumple los tres retos.', 'constructor'],
                    ['Abre Word e inserta una tabla de 4 columnas y 5 filas con el horario del club.', 'horario'],
                    'Activa la fila de encabezado y las filas con bandas en Diseño de tabla.',
                    'Agrega bordes y centra el contenido desde Presentación.',
                    'Agrega una fila nueva con otra sesión y combina dos celdas para un título.']},
         'cel': {'mat': ['App de Word o Documentos de Google', 'Este material (Constructor de tablas)'],
                 'steps': [
                     ['Prueba tu estilo en el Constructor de tablas de la pestaña Diagnostica y cumple los tres retos.', 'constructor'],
                     ['En la app inserta una tabla de 4 columnas y 5 filas con el horario del club.', 'horario'],
                     'Activa la fila de encabezado y las filas con bandas.',
                     'Agrega bordes y centra el contenido.',
                     'Agrega una fila nueva con otra sesión.']}},
     'entrega': ['Tu documento con la tabla del horario formateada (captura o archivo).'],
     'rub': [['Tabla con el tamaño correcto', 25], ['Encabezado y estilo', 30], ['Contenido alineado', 25], ['Fila nueva y celdas combinadas', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Fotos con ajuste de texto',
     'prog': 'Bloque B · Imágenes y objetos',
     'min': 45, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word', 'Dos o tres fotos propias o con licencia', 'Este material (Ajuste de texto)'],
                'steps': [
                    ['Practica los tres retos del simulador de Ajuste de texto en la pestaña Diagnostica.', 'ajuste'],
                    ['Escribe dos párrafos sobre el club e inserta una foto con ajuste Cuadrado a la derecha.', 'ajuste'],
                    'Escala la foto desde una esquina para que no se deforme.',
                    ['Inserta otras dos fotos, deja el mismo tamaño y alínealas con Alinear y Distribuir.', 'alinear'],
                    ['Anota la fuente de cada imagen en una nota al pie.', 'fuente']]},
         'cel': {'mat': ['App de Word o Documentos de Google', 'Dos o tres fotos del celular', 'Este material (Ajuste de texto)'],
                 'steps': [
                     ['Practica los tres retos del simulador de Ajuste de texto en la pestaña Diagnostica.', 'ajuste'],
                     ['Escribe dos párrafos e inserta una foto con ajuste que rodee el texto.', 'ajuste'],
                     'Escala la foto desde una esquina para que no se deforme.',
                     ['Inserta otras dos fotos con el mismo tamaño y alinéalas.', 'alinear'],
                     ['Anota la fuente de cada imagen.', 'fuente']]}},
     'entrega': ['Documento con texto acomodado alrededor de una foto y tres fotos alineadas, con su fuente.'],
     'rub': [['Ajuste de texto adecuado', 30], ['Fotos sin deformar', 20], ['Alineación y mismo tamaño', 30], ['Fuentes citadas', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Reporte con índice, nota al pie y vínculo',
     'prog': 'Bloque C · Referencias y formato',
     'min': 50, 'lug': 'Aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Word', 'Tu documento de las prácticas anteriores'],
                'steps': [
                    'Escribe al menos tres secciones: Horario, Galería y Reglas del club.',
                    ['Aplica Título 1 y Título 2 a los encabezados e inserta la tabla de contenido al inicio.', 'indice'],
                    ['Agrega una nota al pie y un hipervínculo a una sección del documento.', 'notaviculo'],
                    'Actualiza la tabla de contenido y revisa que los números de página sean correctos.',
                    'Guarda el documento como DOCX y como PDF.']},
         'cel': {'mat': ['App de Word o Documentos de Google', 'Tu documento de las prácticas anteriores'],
                 'steps': [
                     'Escribe al menos tres secciones: Horario, Galería y Reglas del club.',
                     ['Aplica estilos de título e inserta la tabla de contenido al inicio.', 'indice'],
                     ['Agrega una nota al pie y un hipervínculo.', 'notaviculo'],
                     'Actualiza la tabla de contenido.',
                     'Guarda el documento como PDF.']}},
     'entrega': ['Documento con índice automático, nota al pie e hipervínculo (DOCX o PDF).'],
     'rub': [['Estilos de título y tabla de contenido', 35], ['Nota al pie', 20], ['Hipervínculo', 20], ['Documento completo y ordenado', 25]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Documentos digitales avanzados · Unidad 1',
    'ra': 'R.A. 1.2', 'title': 'Documento con tablas, imágenes y referencias',
    'data': [
        ('Resultado de aprendizaje', 'Integra objetos como tablas, imágenes y referencias en un documento digital con la finalidad de mejorar su presentación.'),
        ('Actividad de evaluación', 'Elabora un documento digital con tablas, imágenes, referencias y objetos correctamente formateados.'),
        ('Evidencia', 'Documento digital (DOCX o PDF)'),
        ('Entrega', 'En la actividad R.A. 1.2 de la plataforma. Si aún no entregas, consulta con tu docente.'),
    ],
    'situation': 'Prepara un documento sobre un club o actividad de tu plantel que incluya los objetos que aprendiste en este R.A.',
    'hint': 'Prueba primero el estilo en la pestaña Diagnostica y revisa tu documento contra la rúbrica antes de entregar.',
    'steps': [
        ('Contenido', ['Escribe al menos tres secciones con título.']),
        ('Tabla', ['Inserta una tabla con encabezado, bordes y contenido alineado.']),
        ('Imágenes', ['Inserta al menos dos imágenes con ajuste de texto adecuado y la fuente de cada una.']),
        ('Referencias', ['Inserta índice automático, nota al pie e hipervínculo.']),
        ('Entrega', ['Revisa y guarda el documento como DOCX o PDF y súbelo en la plataforma.']),
    ],
    'rubric': [('Contenido y organización', 15), ('Tabla bien formateada', 25), ('Imágenes con ajuste y fuente', 25), ('Índice, nota al pie y vínculo', 25), ('Presentación general', 10)],
    'deliver': ['Un archivo DOCX o PDF con tu documento.', 'Se entrega en la actividad R.A. 1.2 de la plataforma.'],
}
