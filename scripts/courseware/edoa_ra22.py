"""EDOA-20 · R.A. 2.2 · Objetos, animaciones y transiciones en presentaciones (PowerPoint).

Caso de las lecciones: Feria de Carreras del plantel (continúa la presentación del R.A. 2.1).
Incluye tres presentaciones simuladas (ppt_sim.js) para practicar sin computadora.
La actividad de evaluación es la entrega de la presentación (.pptx o PDF) en la plataforma.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-2.2'
CODE_PREFIX = 'EDOA22'
FILE = 'edoa-ra22-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 2.2 · Objetos y animación en presentaciones'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 2.2 · Objetos, animaciones y transiciones'
HERO_KICK = 'EDOA-20 · R.A. 2.2'
HERO_TITLE = 'Tablas, imágenes, video y movimiento con propósito'
HERO_TEXT = 'Inserta objetos en tus diapositivas, dales formato y anímalos con medida, para que la presentación de la Feria de Carreras atrape al público sin distraerlo.'
EV_SHORT = 'inserta objetos y anima tu presentación.'
EV_CARD = 'Presentación R.A. 2.2'
RA = 'R.A. 2.2'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simulador de presentaciones'], 'c': ['Construye', 'Prácticas en PowerPoint']}

EXTRA_JS = (Path(__file__).parent / 'ppt_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".pptsim"))pptInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".pptsim"))return pptCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.n, a.s(i), a.objs(k), a.obj(f), a.anims(), a.some, a.every, a.used)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pPpt({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


FERIA = [{'lay': 'tit', 't': 'Informática en CONALEP', 'b': 'Feria de Carreras · Grupo 311'},
         {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes\nProgramación\nSoporte técnico'},
         {'lay': 'dos', 't': '¿Dónde trabajas?', 'b': 'Empresas\nEscuelas\nTu propio negocio'},
         {'lay': 'tc', 't': 'Contacto', 'b': 'Servicios escolares\nRedes sociales del plantel'}]

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🎬', 'Objetos y movimiento con propósito', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'En el R.A. 2.1 le diste formato a tu presentación. Ahora le agregas <b>objetos</b> (tablas, imágenes, vínculos, video y audio) y <b>movimiento</b> (animaciones y transiciones) para que el público entienda mejor y no se aburra.'),
    ex('Caso de las lecciones: Feria de Carreras', 'La presentación del grupo 311 ya tiene buen diseño. Le falta una tabla con el plan de estudios, fotos del laboratorio, el video del plantel y que las ideas aparezcan una por una mientras el expositor habla.'),
    r3([('➕', 'Insertar', 'Texto, tablas, imágenes, vínculos y multimedia.'), ('📐', 'Dar formato', 'Tamaño, fondo y posición de cada objeto.'), ('✨', 'Animar', 'Animaciones de objetos y transiciones entre diapositivas.')]),
    bk('Al final', 'Entregas una <b>presentación</b> (.pptx o PDF) con tablas, imágenes, objetos de referencia y otros objetos con formato, incluyendo animación. Vale <b>10%</b>.')),
    'Cada objeto y cada efecto debe ayudar a explicar, no solo adornar.')
c.A('🎯', '¿Ayuda o distrae?', 'Decide si cada idea ayuda a la presentación de la Feria.', [
    ['Una foto del laboratorio de cómputo en la diapositiva «¿Qué aprendes?»', 'Ayuda', 'La imagen muestra de verdad dónde aprenden.'],
    ['Que cada letra del título gire y rebote durante 5 segundos', 'Distrae', 'El público espera y pierde el hilo.'],
    ['Que los cuatro puntos de la lista aparezcan uno por uno mientras los explicas', 'Ayuda', 'El público atiende solo lo que estás diciendo.'],
    ['Música a todo volumen que suena durante toda la exposición', 'Distrae', 'Compite con tu voz.'],
    ['Una tabla con las materias de cada semestre', 'Ayuda', 'Ordena mucha información en poco espacio.'],
    ['Una transición distinta y ruidosa en cada diapositiva', 'Distrae', 'Mejor una transición suave y la misma en todas.'],
], 'Pregúntate: ¿esto explica algo o solo se mueve?', ['Ayuda', 'Distrae'])
s0_end = c.mark() - 1

# ───────────────────────── A · Insertar objetos ─────────────────────────
a0 = c.mark()
c.L('🔤', 'Cuadros de texto y tablas', 'Bloque A · Inserta objetos', body(
    bk('Cuadro de texto', '<b>Insertar › Cuadro de texto</b>: dibuja un rectángulo y escribe. Sirve para notas cortas fuera de los marcadores, por ejemplo «¡Inscripciones abiertas!».'),
    bk('Tabla', '<b>Insertar › Tabla</b>: eliges filas y columnas en la cuadrícula. Después, la ficha <b>Diseño de tabla</b> da estilo (fila de encabezado, filas con bandas) y <b>Disposición</b> agrega filas, combina celdas y alinea.'),
    bk('Cuándo usar tabla', 'Cuando comparas datos: materias por semestre, horarios, costos. Máximo unas <b>5 filas y 4 columnas</b> para que se lea.'),
    ex('En la Feria', 'Tabla de 3 columnas (Semestre, Materias, Práctica) y 4 filas: encabezado y tres semestres.'),
    warn('Error común', 'Pegar una tabla de Excel con 30 filas en letra de 10 puntos. Nadie la lee: resume o divide.')),
    'Texto suelto → cuadro de texto · Comparar datos → tabla pequeña.')
c.L('🖼️', 'Imágenes', 'Bloque A · Inserta objetos', body(
    bk('Insertar', '<b>Insertar › Imágenes</b>: desde <b>este dispositivo</b> (tus fotos), <b>imágenes de stock</b> o <b>imágenes en línea</b>.'),
    bk('Calidad', 'Usa fotos nítidas y del tamaño adecuado. Una imagen pixelada estirada a toda la diapositiva se ve mal.'),
    bk('Derechos de autor', 'Usa tus propias fotos, imágenes de stock de PowerPoint o bancos gratuitos (Pexels, Unsplash, Pixabay). Si no es tuya, <b>escribe la fuente</b>.'),
    bk('Texto alternativo', 'Clic derecho › <b>Ver texto alternativo</b>: describe la imagen para personas que usan lector de pantalla.'),
    ex('En la Feria', 'Foto del laboratorio tomada por el equipo, con el texto alternativo «Alumnos del grupo 311 armando una computadora en el laboratorio».')),
    'Imagen nítida, con permiso y con texto alternativo.')
c.L('🔗', 'Hipervínculos', 'Bloque A · Inserta objetos de referencia', body(
    sp('En palabras sencillas', 'Un <b>hipervínculo</b> convierte un texto o una imagen en un «botón» que abre una página web, otra diapositiva, un archivo o un correo.'),
    bk('Cómo', 'Selecciona el texto › <b>Insertar › Vínculo</b> (Ctrl + Alt + K o Ctrl + K) › escribe la dirección (URL). El vínculo solo funciona en modo <b>Presentación</b> o con Ctrl + clic.'),
    bk('Lugar de este documento', 'En la ventana de vínculo eliges «Lugar de este documento» para saltar a otra diapositiva: útil para un menú o un botón «Volver al inicio».'),
    bk('Texto claro', 'Escribe «Página de CONALEP Tamaulipas», no pegues la dirección larga.'),
    ex('En la Feria', 'En «Contacto», el texto «Facebook del plantel» lleva a la página oficial; en la portada, un menú con vínculos a cada sección.')),
    'Texto claro + dirección correcta · se prueba en modo Presentación.')
c.L('🎞️', 'Video, audio y otros archivos', 'Bloque A · Otros objetos', body(
    bk('Video', '<b>Insertar › Video</b>: desde este dispositivo (se guarda dentro del archivo) o <b>video en línea</b> (YouTube; necesita internet al presentar).'),
    bk('Audio', '<b>Insertar › Audio</b>: un archivo de música de <b>ambientación</b> o <b>Grabar audio</b> para tu <b>narración</b>. En Reproducción eliges «Iniciar automáticamente», «Reproducir en todas las diapositivas» y el volumen.'),
    bk('Otros archivos (objetos)', '<b>Insertar › Objeto</b>: un <b>documento de Word</b>, una <b>hoja de cálculo</b> o <b>otra presentación</b>. Puedes incrustarlo (va dentro) o vincularlo (se actualiza si cambia el original). También se pueden mostrar como ícono.'),
    warn('Peso del archivo', 'Un video dentro de la presentación la hace muy pesada. La plataforma acepta hasta <b>20 MB</b>: usa un video corto, comprímelo (Archivo › Información › Comprimir medios) o insértalo en línea.'),
    ex('En la Feria', 'Video de 40 segundos del plantel, audio de fondo suave en la portada y la hoja de cálculo con el horario incrustada como ícono.')),
    'Video corto · audio que no tape tu voz · objetos como ícono si son grandes.')
c.A('➕', '¿Qué objeto insertas?', 'Elige el objeto adecuado para cada necesidad de la Feria.', [
    ['Mostrar las materias de 1.º, 2.º y 3.er semestre en columnas', 'Tabla', 'Comparar datos ordenados.'],
    ['Que al dar clic en «Facebook del plantel» se abra la página', 'Hipervínculo', 'Un vínculo abre la página web.'],
    ['Mostrar cómo es el laboratorio de cómputo', 'Imagen', 'Una foto lo muestra mejor que palabras.'],
    ['Explicar con tu voz grabada la diapositiva de la portada', 'Audio', 'Grabar audio sirve para la narración.'],
    ['Poner el horario que ya tienes en Excel', 'Hoja de cálculo', 'Insertar › Objeto › Hoja de cálculo.'],
    ['Un recorrido de 40 segundos por el plantel', 'Video', 'El movimiento se muestra con video.'],
    ['Escribir «¡Inscripciones abiertas!» en una esquina', 'Cuadro de texto', 'Texto corto fuera de los marcadores.'],
], 'Piensa qué quieres mostrar: datos, lugar, voz, movimiento o un archivo.',
    ['Tabla', 'Hipervínculo', 'Imagen', 'Audio', 'Hoja de cálculo', 'Video', 'Cuadro de texto'])
c.A('⚖️', '¿Cierto o falso?', 'Lee cada afirmación sobre objetos.', [
    ['Un hipervínculo funciona con un clic normal mientras editas en la vista Normal', 'Falso', 'En vista Normal se usa Ctrl + clic; funciona con clic en modo Presentación.'],
    ['Un video en línea necesita internet al momento de presentar', 'Cierto', 'Se reproduce desde la página web.'],
    ['Puedes usar cualquier imagen de internet sin dar crédito', 'Falso', 'Respeta los derechos de autor y escribe la fuente.'],
    ['Un objeto vinculado se actualiza si cambias el archivo original', 'Cierto', 'Vincular mantiene la conexión con el original.'],
    ['El texto alternativo describe la imagen para personas con discapacidad visual', 'Cierto', 'Lo leen los lectores de pantalla.'],
], 'Repasa las lecciones del bloque A.', ['Cierto', 'Falso'])
sim('➕', 'Inserta objetos en la presentación', 'Presentación simulada: usa la ficha Insertar como en PowerPoint.',
    {'id': 'ins', 'tabs': ['arc', 'ini', 'ins', 'for'], 'theme': 'oc', 'slides': FERIA,
     'intro': 'La presentación ya tiene formato, pero solo tiene texto. Elige una diapositiva en las miniaturas y usa la ficha <b>Insertar</b>. Al insertar, el objeto queda seleccionado y abajo puedes escribir su descripción.'},
    [['En «¿Qué aprendes?» inserta una <b>Tabla</b> de <b>4 filas y 3 columnas</b> (cámbialo abajo, en el editor).', 'a.some(function(s){return /aprendes/i.test(s.t)&&s.objs.some(function(x){return x.k=="tbl"&&x.r==4&&x.c==3})})'],
     ['En «¿Dónde trabajas?» inserta una <b>Imagen</b> y descríbela (al menos 10 letras): es su texto alternativo.', 'a.some(function(s){return /d[oó]nde/i.test(s.t)&&s.objs.some(function(x){return x.k=="img"&&x.lb.trim().length>=10&&x.lb!="Imagen"})})'],
     ['En «Contacto» inserta un <b>Hipervínculo</b> con un texto claro y una dirección que empiece con <b>https://</b>.', 'a.some(function(s){return /contacto/i.test(s.t)&&s.objs.some(function(x){return x.k=="lnk"&&/^https:\\/\\/\\S+\\.\\S+/.test(x.url)&&!/^https?:/.test(x.lb)})})'],
     ['Inserta un <b>Video</b> en cualquier diapositiva.', 'a.objs("vid")>=1'],
     ['En la portada inserta un <b>Audio</b> de ambientación.', 'a.s(0).objs.some(function(x){return x.k=="aud"})'],
     ['Inserta un objeto <b>Hoja de cálculo</b> (Insertar › Objeto).', 'a.objs("xls")>=1'],
     ['Agrega un <b>Cuadro de texto</b> que diga <b>¡Inscripciones abiertas!</b>', 'a.obj(function(x){return x.k=="txt"&&/inscripciones/i.test(x.lb)})']],
    'Primero elige la diapositiva en las miniaturas y después inserta.')
a_end = c.mark() - 1

# ───────────────────────── B · Formato de objeto ─────────────────────────
b0 = c.mark()
c.L('📏', 'Tamaño de los objetos', 'Bloque B · Formato de objeto', body(
    bk('Con el ratón', 'Arrastra los <b>controladores</b> (los circulitos de las esquinas). Usa las <b>esquinas</b> para no deformar la imagen.'),
    bk('Exacto', 'Ficha <b>Formato de imagen</b> (o Formato de forma) › grupo <b>Tamaño</b>: alto y ancho en centímetros, con «Bloquear relación de aspecto».'),
    bk('Recortar', '<b>Formato de imagen › Recortar</b> quita lo que sobra de una foto, o la recorta en forma de círculo.'),
    warn('Error común', 'Estirar una foto desde el borde de en medio: las personas salen «aplastadas» o «alargadas».')),
    'Esquinas para escalar · Recortar para quitar lo que sobra.')
c.L('🎨', 'Fondo (relleno) de los objetos', 'Bloque B · Formato de objeto', body(
    bk('Relleno de forma', '<b>Formato de forma › Relleno de forma</b>: color sólido, degradado, imagen o textura detrás del cuadro de texto o de la forma.'),
    bk('Contorno y efectos', 'Color y grosor del borde; sombra, reflejo o bordes suaves con moderación.'),
    bk('Estilos rápidos', 'Formato de forma › <b>Estilos de forma</b> o Formato de imagen › <b>Estilos de imagen</b>: marcos y sombras listos en un clic.'),
    bk('Transparencia', 'Un relleno claro y semitransparente detrás del texto ayuda a que se lea encima de una foto.'),
    ex('En la Feria', 'El cuadro «¡Inscripciones abiertas!» con relleno amarillo y contorno naranja: resalta sin tapar nada.')),
    'Relleno para resaltar · contorno discreto · estilos con moderación.')
c.L('🧭', 'Posición y alineación', 'Bloque B · Formato de objeto', body(
    bk('Arrastrar', 'Mueve el objeto y sigue las <b>guías inteligentes</b> (líneas rojas punteadas) que aparecen al alinearlo con otros.'),
    bk('Alinear', '<b>Formato › Organizar › Alinear</b>: izquierda, centro, derecha, arriba, en medio, abajo y <b>Distribuir</b> para dejar el mismo espacio entre varios objetos.'),
    bk('Orden', '<b>Traer adelante</b> / <b>Enviar atrás</b>: qué objeto queda encima del otro.'),
    bk('Agrupar', 'Selecciona varios objetos (Mayús + clic) › <b>Agrupar</b>: se mueven juntos.'),
    ana('Piensa en…', 'Acomodar fotos en el corcho del salón: alineadas y con el mismo espacio se ve ordenado; amontonadas, no.')),
    'Alinear y distribuir · traer adelante o atrás · agrupar.')
c.A('📐', '¿Qué herramienta de formato?', 'El equipo tiene estos problemas con sus objetos.', [
    ['La foto del laboratorio tiene un bote de basura en la orilla', 'Recortar', 'Quita lo que sobra de la imagen.'],
    ['Tres íconos quedaron con espacios distintos entre ellos', 'Distribuir horizontalmente', 'Deja el mismo espacio entre ellos.'],
    ['El cuadro de texto quedó detrás de la foto y no se ve', 'Traer adelante', 'Lo pone encima de la foto.'],
    ['Al agrandar la foto, la gente salió alargada', 'Bloquear relación de aspecto', 'Mantiene la proporción de la imagen.'],
    ['El texto encima de una foto no se lee', 'Relleno semitransparente', 'Un fondo claro detrás del texto mejora el contraste.'],
    ['El logotipo y su texto se separan al moverlos', 'Agrupar', 'Agrupados se mueven juntos.'],
], 'Piensa: ¿es tamaño, relleno, posición u orden?',
    ['Recortar', 'Distribuir horizontalmente', 'Traer adelante', 'Bloquear relación de aspecto', 'Relleno semitransparente', 'Agrupar'])
c.O('🔢', 'Ordena: insertar y acomodar una imagen', 'Pon en orden los pasos.', [
    ['Selecciona la diapositiva', 'Primero dónde va.'],
    ['Insertar › Imágenes › Este dispositivo', 'Elige tu foto.'],
    ['Recorta lo que sobra', 'Formato de imagen › Recortar.'],
    ['Ajusta el tamaño desde una esquina', 'Sin deformarla.'],
    ['Alinea con Organizar › Alinear', 'Que quede ordenada.'],
    ['Escribe el texto alternativo', 'Para que sea accesible.'],
], 'Insertar → recortar → tamaño → alinear → texto alternativo.')
a_fmt = sim('📐', 'Da formato a los objetos', 'Presentación simulada: tamaño, relleno y posición.',
    {'id': 'fmt', 'tabs': ['ini', 'ins', 'for'], 'theme': 'oc',
     'slides': [FERIA[0],
                {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes\nProgramación\nSoporte técnico', 'objs': [{'k': 'img', 'lb': 'Foto del laboratorio', 'sz': 's', 'pos': 'c'}]},
                {'lay': 'tc', 't': 'Contacto', 'b': 'Servicios escolares', 'objs': [{'k': 'txt', 'lb': '¡Inscripciones abiertas!', 'sz': 'l', 'pos': 'c'}]}],
     'intro': 'Los objetos ya están insertados, pero mal acomodados. Da clic sobre un objeto de la diapositiva: se selecciona y se abre la ficha <b>Formato</b>.'},
    [['En «¿Qué aprendes?», haz la foto del laboratorio <b>Grande</b> y colócala a la <b>Derecha</b>.', 'a.s(1).objs.some(function(x){return x.k=="img"&&x.sz=="l"&&x.pos=="d"})'],
     ['En «Contacto», deja el cuadro «¡Inscripciones abiertas!» en tamaño <b>Pequeño</b>, <b>Abajo</b> y con relleno <b>Amarillo</b>.', 'a.obj(function(x){return x.k=="txt"&&x.sz=="s"&&x.pos=="ab"&&x.fill=="#fef9c3"})'],
     ['En la portada, inserta una imagen del logotipo, hazla <b>Pequeña</b> y ponla <b>Arriba</b>.', 'a.s(0).objs.some(function(x){return x.k=="img"&&x.sz=="s"&&x.pos=="ar"})']],
    'Selecciona el objeto con un clic; la ficha Formato cambia solo el objeto seleccionado.')
b_end = c.mark() - 1

# ───────────────────────── C · Animación ─────────────────────────
c0 = c.mark()
c.L('✨', 'Tipos de animación', 'Bloque C · Animación predeterminada', body(
    sp('En palabras sencillas', 'Una <b>animación</b> es el movimiento de un <b>objeto</b> dentro de la diapositiva: un texto que aparece, una imagen que crece o una flecha que se va.'),
    bk('🟢 Entrada', 'Cómo <b>aparece</b> el objeto: Aparecer, Desvanecer, Entrar volando, Zoom, Barrido.'),
    bk('🟡 Énfasis', 'Llama la atención sobre algo que <b>ya está</b>: Pulso, Girar, Cambio de color.'),
    bk('🔴 Salida', 'Cómo <b>se va</b>: Desaparecer, Salir volando.'),
    bk('Trayectorias', 'El objeto se mueve siguiendo una línea o curva que tú dibujas.'),
    bk('Dónde', 'Selecciona el objeto › ficha <b>Animaciones</b> › elige el efecto. Con <b>Opciones de efectos</b> cambias la dirección (desde la izquierda, por letra, por párrafo…).')),
    'Entrada = aparece · Énfasis = resalta · Salida = se va.')
c.L('⏱️', 'Inicio, duración y panel de animación', 'Bloque C · Animación personalizada', body(
    bk('Inicio', '<b>Al hacer clic</b> (espera tu clic), <b>Con la anterior</b> (al mismo tiempo que la animación previa) o <b>Después de la anterior</b> (cuando termina la previa).'),
    bk('Duración y retraso', 'Duración: cuánto tarda el efecto (0.5 a 1 s es suficiente). Retraso: cuánto espera antes de empezar.'),
    bk('Panel de animación', '<b>Animaciones › Panel de animación</b>: la lista en orden de todas las animaciones de la diapositiva. Ahí las reordenas, las pruebas y ves sus tiempos.'),
    bk('Copiar animación', 'El botón <b>Copiar animación</b> (brocha) pasa el mismo efecto a otro objeto.'),
    ex('En la Feria', 'Cada punto de «¿Qué aprendes?»: Entrada · Desvanecer · Al hacer clic · 0.5 s. Así aparecen uno por uno mientras el expositor habla.')),
    'Al hacer clic = tú controlas · Con la anterior = juntas · Después de = en cadena.')
c.L('🧠', 'Animar con criterio', 'Bloque C · Menos es más', body(
    bk('Para qué sí', 'Mostrar las ideas <b>una por una</b>, revelar un resultado, señalar una parte de una imagen o mostrar los pasos de un proceso.'),
    bk('Para qué no', 'Para «que se vea bonito»: tres efectos distintos en una diapositiva, animaciones largas o con sonido en cada punto.'),
    bk('Regla práctica', 'Uno o dos efectos de entrada para toda la presentación, rápidos (0.5 s), y un énfasis solo para el dato más importante.'),
    warn('Ojo', 'Si tu presentación se va a ver en PDF, las animaciones no funcionan: el contenido tiene que entenderse sin ellas.')),
    'Pocos efectos, rápidos y con un propósito.')
c.A('✨', '¿Qué tipo de animación?', 'Elige el tipo de animación que necesita cada caso.', [
    ['Que cada punto de la lista aparezca cuando lo vas a explicar', 'Entrada', 'El objeto aparece en la diapositiva.'],
    ['Que el dato «95% consigue trabajo» lata para llamar la atención', 'Énfasis', 'Resalta algo que ya está visible.'],
    ['Que una flecha desaparezca después de señalar algo', 'Salida', 'El objeto se va de la diapositiva.'],
    ['Que un dibujo de cable recorra el camino de la PC al router', 'Trayectoria', 'El objeto sigue una línea dibujada.'],
], 'Aparece → entrada · resalta → énfasis · se va → salida · recorre → trayectoria.', ['Entrada', 'Énfasis', 'Salida', 'Trayectoria'])
c.A('⏱️', '¿Qué opción de inicio?', 'Elige cómo debe iniciar cada animación.', [
    ['Quieres controlar cuándo aparece cada punto mientras hablas', 'Al hacer clic', 'Espera tu clic.'],
    ['La foto y su pie deben aparecer al mismo tiempo', 'Con la anterior', 'Las dos animaciones corren juntas.'],
    ['El título aparece y, en cuanto termina, aparece el subtítulo solo', 'Después de la anterior', 'Empieza cuando termina la previa.'],
], 'Tu clic · al mismo tiempo · en cadena.', ['Al hacer clic', 'Con la anterior', 'Después de la anterior'])
c.Z('⏱️', 'Completa: animaciones', 'Elige la palabra correcta.',
    '<p>Las animaciones se aplican a {0} y las transiciones a {1}.</p>'
    '<p>Para ver todas las animaciones en orden uso el {2}.</p>'
    '<p>Una duración recomendable para un efecto de entrada es de {3}.</p>'
    '<p>Si la presentación se entrega en PDF, las animaciones {4}.</p>',
    [['los objetos', ['los objetos', 'las diapositivas completas', 'el patrón']],
     ['las diapositivas completas', ['las diapositivas completas', 'los objetos', 'las tablas']],
     ['panel de animación', ['panel de animación', 'panel de notas', 'clasificador']],
     ['0.5 segundos', ['0.5 segundos', '5 segundos', '30 segundos']],
     ['no funcionan', ['no funcionan', 'se duplican', 'se vuelven video']]],
    'Recuerda: objeto → animación; diapositiva → transición.')
sim('✨', 'Anima la diapositiva «¿Qué aprendes?»', 'Presentación simulada: animaciones de objetos.',
    {'id': 'ani', 'tabs': ['arc', 'ani'], 'theme': 'oc',
     'slides': [FERIA[0],
                {'lay': 'bla', 'objs': [{'k': 'txt', 'lb': '¿Qué aprendes?', 'sz': 'l', 'pos': 'ar'}, {'k': 'txt', 'lb': 'Redes', 'sz': 's', 'pos': 'i'}, {'k': 'txt', 'lb': 'Programación', 'sz': 's', 'pos': 'c'}, {'k': 'txt', 'lb': 'Soporte técnico', 'sz': 's', 'pos': 'd'}, {'k': 'txt', 'lb': '¡Empleo seguro!', 'fill': '#fef9c3', 'sz': 's', 'pos': 'ab'}]}],
     'intro': 'Selecciona la diapositiva 2. Da clic sobre cada objeto y usa la ficha <b>Animaciones</b>. Con <b>▶ Vista previa</b> ves cómo queda; en la vista previa da clic para avanzar.'},
    [['Da a «Redes», «Programación» y «Soporte técnico» una animación de <b>Entrada</b> que inicie <b>Al hacer clic</b>.', 'a.s(1).objs.slice(1,4).every(function(x){return ["ap","de","vu","zo","ba"].indexOf(x.an.fx)>-1&&x.an.st=="clic"})'],
     ['Usa el <b>mismo efecto</b> de entrada en los tres puntos (que se vea parejo).', 'a.s(1).objs.slice(1,4).every(function(x,i,o){return x.an.fx&&x.an.fx==o[0].an.fx})'],
     ['Ponles una duración de <b>0.5 s</b>.', 'a.s(1).objs.slice(1,4).every(function(x){return x.an.fx&&x.an.dur==0.5})'],
     ['Al cuadro «¡Empleo seguro!» dale un <b>Énfasis</b> (Pulso o Girar) que inicie <b>Después de la anterior</b>.', '(function(x){return (x.an.fx=="pu"||x.an.fx=="gi")&&x.an.st=="des"})(a.s(1).objs[4])'],
     ['Deja el título «¿Qué aprendes?» <b>sin animación</b>: ya está ahí cuando llega la diapositiva.', 'a.s(1).objs[0].an.fx==""&&a.anims()>=4'],
     ['Revisa el resultado con <b>▶ Vista previa</b>.', '!!a.used.aprev']],
    'Revisa el Panel de animación: debe decir 🖱️ en los tres puntos y ⏱️ en el énfasis.')
c_end = c.mark() - 1

# ───────────────────────── D · Transiciones ─────────────────────────
d0 = c.mark()
c.L('🔀', 'Transiciones', 'Bloque D · Pasar de una diapositiva a otra', body(
    sp('En palabras sencillas', 'Una <b>transición</b> es el efecto al <b>cambiar de diapositiva</b>: la nueva se desvanece, empuja a la anterior o la cubre.'),
    bk('Dónde', 'Selecciona la diapositiva › ficha <b>Transiciones</b> › elige el efecto. <b>Opciones de efectos</b> cambia la dirección (desde la derecha, desde abajo…).'),
    bk('Sutiles y llamativas', 'Sutiles: Desvanecer, Empujar, Barrido, Cubrir. Llamativas: Cortina, Remolino, Origami. <b>Transformación</b> (Morph) mueve suavemente los objetos que se repiten entre dos diapositivas.'),
    bk('Aplicar a todas', 'Elige la transición y da clic en <b>Aplicar a todo</b>: la presentación se ve pareja.'),
    ex('En la Feria', 'Transición «Desvanecer» de 1 s en todas, y «Transformación» solo entre la portada y la primera diapositiva.')),
    'Una transición sutil, la misma en todas.')
c.L('⏲️', 'Intervalos: sonido, duración y avance', 'Bloque D · Grupo Intervalos', body(
    bk('Sonido', 'Un efecto al cambiar (aplauso, cámara…). Úsalo casi nunca: en una exposición distrae.'),
    bk('Duración', 'Cuánto tarda la transición: 0.5 a 1.5 s.'),
    bk('Avanzar a la diapositiva', '<b>Al hacer clic con el mouse</b>: tú decides cuándo. <b>Después de</b>: avanza sola tras los segundos indicados.'),
    bk('Presentación automática', 'Si desmarcas «Al hacer clic» y pones «Después de: 00:05» en todas, la presentación corre sola: ideal para una pantalla en el stand de la Feria. Con <b>Presentación con diapositivas › Ensayar intervalos</b> PowerPoint mide los tiempos mientras practicas.'),
    ex('En la Feria', 'Versión para la pantalla del stand: todas con «Después de: 5 s», sin clic, y en Configurar presentación «Repetir hasta presionar Esc».')),
    'Exposición → al hacer clic · Pantalla del stand → después de N segundos.')
c.A('🔀', '¿Animación o transición?', 'Decide qué herramienta usas.', [
    ['Que la diapositiva 3 entre empujando a la 2', 'Transición', 'Es el efecto entre diapositivas.'],
    ['Que la foto del laboratorio aparezca con zoom', 'Animación', 'Es el efecto de un objeto.'],
    ['Que todas las diapositivas cambien con Desvanecer', 'Transición', 'Transición aplicada a todas.'],
    ['Que un punto de la lista salga volando', 'Animación', 'Animación de salida de un objeto.'],
    ['Que la presentación avance sola cada 5 segundos', 'Transición', 'Grupo Intervalos de la ficha Transiciones.'],
], 'Objeto → animación · diapositiva completa → transición.', ['Animación', 'Transición'])
c.A('⏲️', '¿Qué configuración de intervalos?', 'Elige la configuración para cada caso.', [
    ['Vas a exponer y quieres avanzar cuando termines de hablar', 'Al hacer clic', 'Tú controlas el avance.'],
    ['La presentación se repetirá sola en la pantalla del stand', 'Después de: 5 s', 'Avanza sola.'],
    ['Quieres que el cambio sea rápido y suave', 'Duración 1 s', 'Ni muy lento ni brusco.'],
    ['Quieres saber cuánto tardas en cada diapositiva al practicar', 'Ensayar intervalos', 'Mide los tiempos mientras ensayas.'],
], 'Exponer → clic · stand → automático.', ['Al hacer clic', 'Después de: 5 s', 'Duración 1 s', 'Ensayar intervalos'])
sim('🔀', 'Prepara la versión del stand', 'Presentación simulada: transiciones e intervalos.',
    {'id': 'tra', 'tabs': ['arc', 'tra'], 'theme': 'oc', 'slides': FERIA,
     'intro': 'El grupo quiere dejar la presentación corriendo sola en la pantalla del stand. Usa la ficha <b>Transiciones</b>.'},
    [['En la diapositiva 1 elige la transición <b>Desvanecer</b> con duración de <b>1 s</b>.', 'a.s(0).tr.fx=="de"&&a.s(0).tr.dur==1'],
     ['Que <b>no</b> tenga sonido (para no tapar la música del stand).', 'a.s(0).tr.fx&&a.s(0).tr.snd==""'],
     ['Desmarca <b>Al hacer clic</b> y elige <b>Después de: 5 s</b>.', '!a.s(0).tr.clic&&a.s(0).tr.aft==5'],
     ['Usa <b>Aplicar a todas</b> para que todas tengan lo mismo.', 'a.every(function(s){return s.tr.fx=="de"&&!s.tr.clic&&s.tr.aft==5})'],
     ['Presenta desde el principio (<b>Archivo › ▶ Desde el principio</b>) y deja que avance sola hasta el final.', '!!a.used.showEnd']],
    'La configuración se hace en una diapositiva y «Aplicar a todas» la copia a las demás.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Objeto', 'Cualquier elemento de la diapositiva: cuadro de texto, tabla, imagen, video, audio, forma.'),
    bk('Hipervínculo', 'Texto o imagen que abre una página, una diapositiva, un archivo o un correo.'),
    bk('Incrustar / vincular', 'Incrustar guarda el archivo dentro; vincular lo conecta con el original.'),
    bk('Texto alternativo', 'Descripción de una imagen para lectores de pantalla.'),
    bk('Controladores', 'Circulitos para cambiar el tamaño de un objeto.'),
    bk('Animación', 'Efecto de un objeto: entrada, énfasis, salida o trayectoria.'),
    bk('Panel de animación', 'Lista en orden de las animaciones de la diapositiva.'),
    bk('Transición', 'Efecto al pasar de una diapositiva a otra.'),
    bk('Intervalos', 'Sonido, duración y forma de avanzar de una transición.'),
    bk('Transformación (Morph)', 'Transición que mueve suavemente los objetos repetidos entre dos diapositivas.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Plan de recuperación sugerido', body(
    bk('Situación', 'El R.A. 2.2 estaba programado del 13 al 23 de octubre. Este material permite recuperarlo rápido: los alumnos pueden avanzar en casa o en el celular, y los cuatro simuladores funcionan sin computadora.', 'sp'),
    bk('Sesión 1 · Bloques A y B (2 h)', 'Cuadros de texto, tablas, imágenes, vínculos, video, audio y objetos; tamaño, relleno y posición. Simuladores «Inserta objetos» y «Da formato a los objetos». <b>Práctica 1</b>.'),
    bk('Sesión 2 · Bloque C (2 h)', 'Tipos de animación, inicio, duración y panel de animación. Simulador «Anima la diapositiva». <b>Práctica 2</b>.'),
    bk('Sesión 3 · Bloque D y evaluación (2 h)', 'Transiciones, intervalos y presentación automática. Simulador «Prepara la versión del stand». <b>Práctica 3</b> y entrega de la A.E. 2.2.'),
    bk('Sugerencia', 'Los alumnos continúan la presentación de la A.E. 2.1: así no empiezan de cero. Pida videos cortos o en línea para no pasar de 20 MB.'),
    bk('Nota', 'La actividad de evaluación se desbloquea al completar este material.', 'sp')),
    'Ajuste las sesiones a su calendario.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🎬', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '➕', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '📐', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '✨', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '🔀', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🎬",t:"Empieza aquí",d:"Objetos y movimiento que ayudan a explicar.",time:"15 min",obj:["Distinguir un objeto o efecto útil de uno que distrae","Conocer la evidencia final"],sum:["Cada objeto y cada efecto debe ayudar a explicar.","Entregas una presentación con objetos con formato y animación."],q:"¿Qué efecto de una presentación te ha distraído más y por qué?"},
a:{k:"Bloque A",l:"A",ic:"➕",t:"Inserta objetos",d:"Cuadros de texto, tablas, imágenes, hipervínculos, video, audio y otros archivos.",time:"100 min",obj:["Insertar cuadros de texto y tablas","Insertar imágenes con permiso y texto alternativo","Crear hipervínculos a páginas y diapositivas","Insertar video, audio y otros archivos sin pasar de 20 MB"],sum:["Comparar datos → tabla pequeña.","Imagen nítida, con permiso y con texto alternativo.","Vínculo con texto claro; se prueba en modo Presentación.","Video corto o en línea; audio que no tape tu voz."],q:"¿Qué objeto le agregarías a una presentación sobre tu comunidad y por qué?"},
b:{k:"Bloque B",l:"B",ic:"📐",t:"Formato de objeto",d:"Tamaño, fondo (relleno) y posición.",time:"70 min",obj:["Cambiar el tamaño sin deformar","Aplicar relleno, contorno y estilos","Alinear, distribuir, ordenar y agrupar objetos"],sum:["Esquinas para escalar · Recortar para quitar lo que sobra.","Relleno para resaltar; contorno discreto.","Alinear, distribuir, traer adelante y agrupar."],q:"¿Por qué una diapositiva con objetos alineados se ve más profesional?",rev:[["Para que un texto abra una página web uso…",["Hipervínculo","Cuadro de texto","Tabla"],0,"Insertar › Vínculo."],["Un video en línea necesita…",["Internet al presentar","Una tabla","Un tema"],0,"Se reproduce desde la página."]]},
c:{k:"Bloque C",l:"C",ic:"✨",t:"Animación",d:"Animaciones predeterminadas y personalizadas.",time:"90 min",obj:["Distinguir entrada, énfasis, salida y trayectoria","Configurar inicio, duración y orden","Usar el panel de animación","Animar con criterio"],sum:["Entrada = aparece · Énfasis = resalta · Salida = se va.","Al hacer clic · Con la anterior · Después de la anterior.","Pocos efectos, rápidos y con propósito."],q:"¿En qué diapositiva de tu presentación sí conviene una animación?",rev:[["Para que la foto no salga deformada al agrandarla…",["Arrastra desde una esquina","Arrastra desde un lado","Usa una transición"],0,"Las esquinas mantienen la proporción."],["Para dejar el mismo espacio entre tres íconos uso…",["Distribuir","Agrupar","Recortar"],0,"Organizar › Alinear › Distribuir."]]},
d:{k:"Bloque D",l:"D",ic:"🔀",t:"Transiciones",d:"Opciones de efectos, intervalos (sonido, duración) y avance.",time:"70 min",obj:["Aplicar una transición y sus opciones de efectos","Configurar sonido y duración","Elegir cómo avanzar: clic o automático"],sum:["Una transición sutil, la misma en todas.","Exposición → al hacer clic · Stand → después de N segundos.","Ensayar intervalos mide tus tiempos."],q:"¿Cuándo conviene que una presentación avance sola?",rev:[["Una animación se aplica a…",["Un objeto","Toda la diapositiva","El patrón"],0,"La transición es para la diapositiva."],["Para que los puntos aparezcan uno por uno mientras hablas, el inicio es…",["Al hacer clic","Con la anterior","Después de la anterior"],0,"Así tú controlas el ritmo."]]}
'''

ILL = r'''
ILL["Cuadros de texto y tablas"]=function(){var o=R_(10,10,150,100,"s",4)+T_(85,30,"¿Qué aprendes?","t");for(var r=0;r<4;r++)for(var k=0;k<3;k++)o+=R_(20+k*44,40+r*16,44,16,r==0?"r":"s",0);o+=R_(180,30,150,40,"a",6)+T_(255,55,"¡Inscripciones abiertas!","td")+T_(255,90,"cuadro de texto","tm")+T_(85,124,"tabla 4 × 3","tm");return SV(340,132,o,"Tabla y cuadro de texto")};
ILL["Video, audio y otros archivos"]=function(){return grid3([["🎬","Video|del dispositivo o en línea"],["🔊","Audio|ambientación o narración"],["📄","Documento|de Word"],["📊","Hoja de|cálculo"],["📽️","Otra|presentación"],["⚖️","Máx.|20 MB"]],"Otros objetos")};
ILL["Posición y alineación"]=function(){var o='';for(var i=0;i<3;i++)o+=R_(30+i*100,30,70,50,"b",6)+T_(65+i*100,60,"Ícono "+(i+1),"tw");o+=T_(170,100,"Distribuir: el mismo espacio entre ellos","tm");return SV(340,112,o,"Alinear y distribuir")};
ILL["Tipos de animación"]=function(){return grid3([["🟢","Entrada|aparece"],["🟡","Énfasis|resalta"],["🔴","Salida|se va"],["〰️","Trayectoria|recorre"],["⚙️","Opciones|de efectos"],["⏱️","0.5 s|rápido"]],"Tipos de animación")};
ILL["Inicio, duración y panel de animación"]=function(){var L=[["🖱️ 1 · Redes · Desvanecer","s"],["🖱️ 2 · Programación · Desvanecer","s"],["🖱️ 3 · Soporte · Desvanecer","s"],["⏱️ · ¡Empleo seguro! · Pulso","a"]],o=T_(170,16,"Panel de animación","t");L.forEach(function(x,i){o+=R_(40,24+i*24,260,20,x[1],4)+T_(170,38+i*24,x[0],x[1]=="a"?"td":"t")});return SV(340,124,o,"Panel de animación")};
ILL["Transiciones"]=function(){return SV(340,100,R_(20,20,120,68,"s",4)+T_(80,58,"Diapositiva 1","t")+T_(170,58,"→ Desvanecer →","tm")+R_(200,20,120,68,"b",4)+T_(260,58,"Diapositiva 2","tw"),"La transición ocurre entre diapositivas")};
'''

EXH = r'''
function pw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><div style="background:#fff;color:#111;padding:8px;font:13px system-ui;overflow-x:auto">'+b+'</div></div>'}
EXH.insertar=function(){return exw(pw_('Insertar','▦ Tabla '+mk(1)+' · 🖼️ Imágenes '+mk(2)+' · 🔤 Cuadro de texto · 🔗 Vínculo '+mk(3)+' · 🎬 Video · 🔊 Audio '+mk(4)+' · 📄 Objeto'),['Elige filas y columnas.','Desde este dispositivo o de stock.','Selecciona antes el texto.','Ambientación o grabar narración.'])};
EXH.tabla=function(){return exw(pw_('Diseño de tabla','<table style="border-collapse:collapse;font-size:12px"><tr style="background:#c43e1c;color:#fff"><td style="padding:3px 8px">Semestre</td><td style="padding:3px 8px">Materias</td><td style="padding:3px 8px">Práctica</td></tr><tr><td style="padding:3px 8px">1.º</td><td>Matemáticas, Inglés</td><td>Armar una PC</td></tr><tr style="background:#fde8e1"><td style="padding:3px 8px">3.º</td><td>Sistemas operativos</td><td>Instalar Windows</td></tr></table> '+mk(1)),['Fila de encabezado y filas con bandas.'])};
EXH.vinculo=function(){return exw(pw_('Insertar hipervínculo','Texto: <b>Facebook del plantel</b> '+mk(1)+'<br>Dirección: <u>https://www.facebook.com/…</u> '+mk(2)+'<br><small>Vincular a: Archivo o página web · Lugar de este documento '+mk(3)+'</small>'),['Texto claro.','La dirección completa con https://','Para saltar a otra diapositiva.'])};
EXH.formato=function(){return exw(pw_('Formato de imagen','Recortar '+mk(1)+' · Alto 8 cm · Ancho 12 cm 🔒 '+mk(2)+' · Estilos de imagen · Organizar › Alinear › Distribuir '+mk(3)),['Quita lo que sobra.','Relación de aspecto bloqueada.','Alinea y deja el mismo espacio.'])};
EXH.animar=function(){return exw(pw_('Animaciones','Desvanecer ▾ '+mk(1)+' · Opciones de efectos · Inicio: Al hacer clic '+mk(2)+' · Duración: 00.50 '+mk(3)+' · Panel de animación '+mk(4)),['Efecto de entrada.','Tú controlas cuándo aparece.','Rápido: medio segundo.','Revisa el orden.'])};
EXH.transicion=function(){return exw(pw_('Transiciones','Desvanecer ▾ '+mk(1)+' · Sonido: [Sin sonido] '+mk(2)+' · Duración: 01.00 · ☑ Al hacer clic con el mouse '+mk(3)+' · ☐ Después de: 00:05 · Aplicar a todo '+mk(4)),['Una transición sutil.','Sin sonido en una exposición.','Para exponer, avance con clic.','Para que todas queden iguales.'])};
EXH.cel=function(){return exw(mp('PowerPoint o Presentaciones · celular','<div class="mbox">＋ Insertar: imagen, tabla, forma, cuadro de texto, vínculo '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Toca el objeto › Animaciones (o ⋮ › Animar) '+mk(2)+'</div><div class="mbox" style="margin-top:6px">Toca la diapositiva › Transiciones '+mk(3)+'</div>'),['Insertar objetos.','Animaciones del objeto.','Transición de la diapositiva.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Inserta objetos y dales formato',
     'prog': 'Bloques A y B · Inserta objetos y formato de objeto',
     'min': 60, 'lug': 'En clase, laboratorio o en casa',
     'modes': {
         'pc': {'mat': ['Tu presentación de la A.E. 2.1', 'Computadora con PowerPoint', 'Fotos propias o de stock'],
                'steps': [
                    'Guarda una copia de tu presentación del R.A. 2.1 como <b>Apellido_Nombre_EDOA22.pptx</b>.',
                    ['Inserta una tabla (máximo 5 × 4) con diseño de tabla y encabezado.', 'tabla'],
                    ['Inserta al menos dos imágenes y escribe su texto alternativo.', 'insertar'],
                    ['Agrega un hipervínculo a una página web y otro a una diapositiva (Lugar de este documento).', 'vinculo'],
                    'Inserta un video corto o en línea, un audio de ambientación o narración, y un objeto (documento, hoja de cálculo u otra presentación) como ícono.',
                    ['Da formato: tamaño sin deformar, recorte, relleno de forma y alineación o distribución.', 'formato']]},
         'cel': {'mat': ['Tu presentación de la A.E. 2.1', 'Celular con PowerPoint o Presentaciones de Google'],
                 'steps': [
                     'Haz una copia de tu presentación del R.A. 2.1 con el nombre <b>Apellido_Nombre_EDOA22</b>.',
                     ['Con ＋ Insertar agrega una tabla, dos imágenes con su texto alternativo y un cuadro de texto.', 'cel'],
                     'Selecciona un texto y agrega un vínculo a una página web.',
                     'Inserta un video de YouTube o de tu galería (corto) y, si la app lo permite, un audio.',
                     'Ajusta el tamaño de cada objeto desde las esquinas y acomódalos alineados.']}},
     'entrega': ['Tu presentación con objetos; la sigues usando en las prácticas 2 y 3.'],
     'rub': [['Tabla con formato', 20], ['Imágenes con texto alternativo', 20], ['Hipervínculos que funcionan', 20], ['Video, audio u otro objeto', 20], ['Objetos con buen tamaño y alineados', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Anima con propósito',
     'prog': 'Bloque C · Animación',
     'min': 50, 'lug': 'En clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu presentación de la práctica 1', 'Computadora con PowerPoint'],
                'steps': [
                    'Antes de empezar, termina el simulador «Anima la diapositiva «¿Qué aprendes?»» de este material.',
                    ['Anima la lista de una diapositiva para que aparezca punto por punto (Entrada, Al hacer clic, 0.5 s).', 'animar'],
                    'Agrega un efecto de énfasis al dato más importante de tu presentación.',
                    'Usa al menos una vez «Con la anterior» o «Después de la anterior» (por ejemplo, una imagen con su pie).',
                    'Revisa el orden en el Panel de animación y prueba con F5. Máximo dos tipos de entrada en toda la presentación.']},
         'cel': {'mat': ['Tu presentación de la práctica 1', 'Celular con PowerPoint o Presentaciones de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador de animaciones de este material.',
                     ['Toca la lista › Animaciones › elige una entrada para que aparezca punto por punto.', 'cel'],
                     'Agrega un énfasis al dato más importante.',
                     'Revisa el orden de las animaciones y pruébalas con ▶.',
                     'Escribe en tus notas por qué animaste esos objetos.']}},
     'entrega': ['Tu presentación con animaciones revisadas.'],
     'rub': [['Lista animada punto por punto', 35], ['Énfasis en el dato importante', 20], ['Uso de Con la anterior o Después de la anterior', 20], ['Efectos rápidos y parejos', 25]]},
    {'id': 'pr3', 'n': 3, 't': 'Transiciones y versión para el stand',
     'prog': 'Bloque D · Transiciones',
     'min': 40, 'lug': 'En clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu presentación de las prácticas 1 y 2', 'Computadora con PowerPoint'],
                'steps': [
                    'Antes de empezar, termina el simulador «Prepara la versión del stand» de este material.',
                    ['Aplica una transición sutil de 1 s, sin sonido, a todas las diapositivas.', 'transicion'],
                    'Presenta con F5 y ensaya: usa Presentación con diapositivas › Ensayar intervalos.',
                    'Guarda una copia <b>Apellido_Nombre_EDOA22_stand.pptx</b> que avance sola cada 5 s y se repita hasta presionar Esc.']},
         'cel': {'mat': ['Tu presentación de las prácticas 1 y 2', 'Celular con PowerPoint o Presentaciones de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Prepara la versión del stand» de este material.',
                     ['Toca cada diapositiva › Transiciones › elige la misma transición sutil para todas.', 'cel'],
                     'Presenta con ▶ y comprueba que todo se vea y se entienda.',
                     'Escribe en tus notas cuánto tardas en cada diapositiva.']}},
     'entrega': ['La presentación terminada: es tu actividad de evaluación.'],
     'rub': [['Transición sutil y pareja', 35], ['Sin sonidos que distraigan', 15], ['Intervalos ensayados', 25], ['Versión automática para el stand', 25]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 2',
    'ra': 'R.A. 2.2', 'title': 'Presentación con objetos y animación',
    'data': [
        ('Resultado de aprendizaje', 'Inserta y da animación a un objeto en una presentación electrónica de acuerdo con las características de operación del presentador gráfico y con los requerimientos de diseño.'),
        ('Actividad de evaluación', '2.2.1 Elabora una presentación electrónica que contenga tablas, imágenes, objetos de referencia y otros objetos, los cuales deberán cumplir con las características de formato establecidas, incluyendo animación.'),
        ('Evidencia', 'Presentación en formato digital (.pptx; PDF solo si tu docente lo autoriza, porque pierde las animaciones)'),
        ('Ponderación', '10% (según el programa)'),
        ('Entrega', 'En la plataforma, en la fecha que indique tu docente'),
    ],
    'situation': 'Termina la presentación de la <b>Feria de Carreras</b> (o el tema que te asigne tu docente): agrégale tablas, imágenes, vínculos y multimedia con formato, y anímala para que el público siga la explicación sin distraerse.',
    'hint': 'Parte de tu presentación del R.A. 2.1 y de tus tres prácticas: revisa esta lista con el archivo abierto.',
    'steps': [
        ('Objetos', [
            'Archivo <b>Apellido_Nombre_EDOA22.pptx</b> con al menos 6 diapositivas.',
            'Al menos una tabla con diseño de tabla.',
            'Al menos dos imágenes nítidas, con permiso de uso y texto alternativo.',
            'Al menos un hipervínculo a una página web y uno a otra diapositiva.',
            'Al menos un video o audio y un objeto (documento, hoja de cálculo u otra presentación).']),
        ('Formato de objeto', [
            'Objetos con tamaño adecuado y sin deformar.',
            'Relleno o estilo en al menos un cuadro o forma.',
            'Objetos alineados o distribuidos.']),
        ('Animación y transiciones', [
            'Al menos una lista animada punto por punto (Al hacer clic).',
            'Un efecto de énfasis y uso de «Con la anterior» o «Después de la anterior».',
            'Una transición sutil y pareja en todas las diapositivas, con duración y avance configurados.']),
        ('Entrega', [
            'Prueba todo con F5: vínculos, video, audio, animaciones y transiciones.',
            'Revisa que el archivo pese máximo 20 MB y súbelo en la actividad R.A. 2.2 de la plataforma.']),
    ],
    'rubric': [
        ('Tabla con formato', 10), ('Imágenes con formato y texto alternativo', 15), ('Hipervínculos que funcionan', 10),
        ('Video, audio u otro objeto', 15), ('Formato de objeto: tamaño, relleno y posición', 15),
        ('Animaciones con propósito', 20), ('Transiciones e intervalos', 15),
    ],
    'deliver': ['Un archivo .pptx de máximo 20 MB.', 'Nombre del archivo: Apellido_Nombre_EDOA22.', 'Súbelo en la actividad R.A. 2.2 de la plataforma.'],
}
