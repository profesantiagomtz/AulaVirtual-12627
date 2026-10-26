"""EDOA-20 · R.A. 2.1 · Formato de presentaciones electrónicas (PowerPoint).

Caso de las lecciones: Feria de Carreras del plantel (el grupo presenta la carrera de Informática
a alumnos de secundaria). Incluye dos presentaciones simuladas (ppt_sim.js) para practicar sin computadora.
La actividad de evaluación es la entrega de la presentación (.pptx o PDF) en la plataforma.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-2.1'
CODE_PREFIX = 'EDOA21'
FILE = 'edoa-ra21-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 2.1 · Formato de presentaciones'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 2.1 · Formato de presentaciones electrónicas'
HERO_KICK = 'EDOA-20 · R.A. 2.1'
HERO_TITLE = 'Presentaciones claras, ordenadas y con buen diseño'
HERO_TEXT = 'Conoce PowerPoint por dentro, configura tus diapositivas, dales formato y usa plantillas, con el caso de la Feria de Carreras del plantel.'
EV_SHORT = 'da formato a tu presentación y entrégala.'
EV_CARD = 'Presentación R.A. 2.1'
RA = 'R.A. 2.1'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simulador de presentaciones'], 'c': ['Construye', 'Prácticas en PowerPoint']}

EXTRA_JS = (Path(__file__).parent / 'ppt_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".pptsim"))pptInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".pptsim"))return pptCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.n, a.s(i), a.some, a.every, a.used, a.theme, a.size, a.or, a.master, a.view)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pPpt({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


LINES3 = 'String(s.b).split("\\n").filter(function(l){return l.trim()}).length>=3'

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🎤', '¿Para qué sirve una presentación?', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Una <b>presentación electrónica</b> (PowerPoint, Presentaciones de Google, Impress o Canva) es un conjunto de <b>diapositivas</b> que acompañan lo que dices cuando expones. No sustituye al expositor: <b>te apoya</b> para que el público entienda y recuerde.'),
    ex('Caso de las lecciones: Feria de Carreras', 'El viernes vienen alumnos de secundaria al plantel. El grupo 311 tiene 5 minutos para presentarles la carrera de <b>Informática</b>. Vamos a preparar una presentación que se vea profesional y que se entienda desde el fondo del salón.'),
    r3([('🧭', 'Conocer', 'Las barras, las vistas y la ayuda.'), ('📐', 'Configurar', 'Tamaño, orientación, fondo y notas.'), ('🎨', 'Dar formato', 'Fuentes, párrafos, temas y plantillas.')]),
    bk('Al final', 'Entregas una <b>presentación con formato</b> (.pptx o PDF) con diseño de diapositiva, estilos y plantilla. Vale <b>10%</b>. Las animaciones y los videos vienen en el R.A. 2.2.')),
    'La presentación apoya al expositor; no lo reemplaza.')
c.A('🧩', '¿Qué programa conviene?', 'Elige el programa más adecuado para cada tarea del grupo.', [
    ['Exponer la carrera de Informática frente a 40 alumnos de secundaria', 'Presentaciones', 'Para exponer frente a un público se usan diapositivas.'],
    ['Llevar la lista de los alumnos que visitaron el stand y su secundaria', 'Hoja de cálculo', 'Una lista con datos en filas y columnas va en Excel.'],
    ['Redactar el oficio para pedir permiso de usar el auditorio', 'Procesador de texto', 'Un oficio es texto corrido: Word.'],
    ['Mostrar en una pantalla las fotos del laboratorio mientras explicas', 'Presentaciones', 'Las diapositivas combinan imágenes y pocas palabras.'],
    ['Calcular cuánto cuesta imprimir 200 trípticos', 'Hoja de cálculo', 'Hacer cuentas es trabajo de Excel.'],
], 'Exponer → presentaciones · Texto → Word · Datos y cuentas → Excel.', ['Presentaciones', 'Procesador de texto', 'Hoja de cálculo'])
c.L('✅', 'Una buena diapositiva', 'Las reglas que vas a usar en todo el R.A.', body(
    bk('Una idea por diapositiva', 'Cada diapositiva responde una sola pregunta: ¿qué es la carrera?, ¿qué aprendes?, ¿dónde trabajas?'),
    bk('Regla 6 × 6', 'Máximo <b>6 renglones</b> y unas <b>6 palabras</b> por renglón. Lo demás lo dices tú (y lo escribes en las <b>notas</b>).'),
    bk('Letra grande', 'Títulos de <b>32 a 44 puntos</b> y texto de <b>24 a 28 puntos</b>. Si no se lee desde el fondo del salón, es muy chica.'),
    bk('Contraste', 'Letra oscura sobre fondo claro o letra clara sobre fondo oscuro. Nunca amarillo sobre blanco.'),
    warn('Error común', 'Copiar y pegar párrafos completos de internet en la diapositiva y leerlos. El público lee más rápido de lo que hablas y se aburre.')),
    'Una idea · pocas palabras · letra grande · buen contraste.')
c.A('🔍', '¿Bien o mal?', 'Revisa estas diapositivas de otros equipos.', [
    ['Una diapositiva con 14 renglones de texto en letra de 14 puntos', 'Mal', 'Rompe la regla 6 × 6 y no se lee de lejos.'],
    ['Título «¿Qué aprendes?» y 4 puntos cortos: redes, programación, soporte, diseño web', 'Bien', 'Una idea, pocos renglones y palabras clave.'],
    ['Letra amarilla clara sobre fondo blanco', 'Mal', 'Casi no hay contraste: no se distingue.'],
    ['Letra blanca de 28 puntos sobre fondo azul marino', 'Bien', 'Fondo oscuro con letra clara y tamaño adecuado.'],
    ['Cinco tipos de letra distintos en la misma diapositiva', 'Mal', 'Se ve desordenado: usa una o dos fuentes.'],
], 'Recuerda: una idea, 6 × 6, letra grande y contraste.', ['Bien', 'Mal'])
s0_end = c.mark() - 1

# ───────────────────────── A · Entorno de trabajo ─────────────────────────
a0 = c.mark()
c.L('🪟', 'Las partes de la ventana', 'Bloque A · Barras y herramientas', body(
    bk('Barra de título', 'Arriba: el nombre del archivo, por ejemplo <b>FeriaCarreras.pptx</b>.'),
    bk('Barra de herramientas de acceso rápido', 'Guardar, Deshacer, Rehacer y <b>Presentar desde el principio</b>. Puedes agregar los botones que más uses.'),
    bk('Cinta de opciones', 'Las herramientas ordenadas en <b>fichas</b>: Archivo, Inicio, Insertar, Diseño, Transiciones, Animaciones, Presentación con diapositivas, Revisar y Vista.'),
    bk('Panel de miniaturas', 'A la izquierda: todas tus diapositivas en pequeño. Ahí las seleccionas, las mueves arrastrando y las duplicas.'),
    bk('Panel de la diapositiva', 'Al centro: la diapositiva en la que trabajas, con sus <b>marcadores de posición</b> («Haz clic para agregar título»).'),
    bk('Panel de notas y barra de estado', 'Abajo: las notas del orador, el número de diapositiva, los botones de vistas y el zoom.')),
    'Izquierda = miniaturas · Centro = diapositiva · Abajo = notas y vistas.')
c.L('🎀', 'Las fichas de la cinta', 'Bloque A · Dónde está cada herramienta', body(
    bk('Inicio', '<b>Nueva diapositiva</b>, <b>Diseño</b> de la diapositiva, fuente, tamaño, color, viñetas, alineación e interlineado.'),
    bk('Insertar', 'Tablas, imágenes, formas, cuadros de texto, vínculos, video y audio (los usarás en el R.A. 2.2).'),
    bk('Diseño', '<b>Temas</b>, variantes de color, <b>Tamaño de diapositiva</b> y <b>Formato del fondo</b>.'),
    bk('Transiciones y Animaciones', 'Los efectos entre diapositivas y de cada objeto (R.A. 2.2).'),
    bk('Presentación con diapositivas', 'Iniciar la presentación (F5), ensayar intervalos y configurar la exposición.'),
    bk('Vista', 'Normal, Esquema, Clasificador, Página de notas, Vista de lectura y <b>Patrón de diapositivas</b>.'),
    ana('Piensa en…', 'La mochila de la escuela: cada bolsa guarda cosas parecidas. Si buscas el fondo, vas a la bolsa «Diseño».')),
    'Texto → Inicio · Fondo y tema → Diseño · Vistas → Vista.')
c.L('👁️', 'Las vistas de la presentación', 'Bloque A · Ver tu trabajo de distintas formas', body(
    bk('Normal', 'La de siempre: miniaturas, diapositiva y notas. Aquí escribes y das formato.'),
    bk('Esquema', 'Muestra solo los <b>títulos y el texto</b> de todas las diapositivas, como un índice. Sirve para revisar que la historia tenga orden.'),
    bk('Clasificador de diapositivas', 'Todas las diapositivas en cuadrícula. Ideal para <b>ordenarlas arrastrando</b> y ver si el diseño es parejo.'),
    bk('Página de notas', 'Cada diapositiva con sus notas debajo, como se imprimen para el expositor.'),
    bk('Vista de lectura y Presentación', 'Vista de lectura: la presentación en la ventana. Presentación (F5): pantalla completa, como la verá el público.'),
    ex('En la Feria', 'Juan revisa en <b>Esquema</b> que el orden sea: ¿Qué es? → ¿Qué aprendes? → ¿Dónde trabajas? → Contacto. Luego, en el <b>Clasificador</b>, mueve «Contacto» al final.')),
    'Escribir → Normal · Revisar orden → Esquema · Acomodar → Clasificador.')
c.L('❓', 'La ayuda de PowerPoint', 'Bloque A · Cuando no sabes dónde está algo', body(
    bk('Cuadro «Buscar»', 'Arriba de la ventana (o «¿Qué desea hacer?» en versiones anteriores): escribe lo que quieres hacer, por ejemplo «cambiar fondo», y PowerPoint te lleva a la herramienta.'),
    bk('Tecla F1', 'Abre el panel de <b>Ayuda</b> con artículos y videos cortos de Microsoft.'),
    bk('Información en pantalla', 'Deja el puntero quieto sobre un botón: aparece su nombre y para qué sirve.'),
    ana('Piensa en…', 'Preguntarle al bibliotecario dónde está un libro en lugar de recorrer todos los estantes.')),
    'Buscar o F1 antes de rendirte.')
c.A('🪟', '¿Qué parte de la ventana es?', 'Lee la descripción y elige el nombre correcto.', [
    ['Muestra todas las diapositivas en pequeño a la izquierda', 'Panel de miniaturas', 'Ahí seleccionas, mueves y duplicas diapositivas.'],
    ['Dice «Haz clic para agregar título»', 'Marcador de posición', 'Es el espacio listo para escribir el título.'],
    ['Tiene las fichas Inicio, Insertar y Diseño', 'Cinta de opciones', 'Ahí están todas las herramientas.'],
    ['Debajo de la diapositiva, para escribir lo que dirás', 'Panel de notas', 'Las notas del orador no las ve el público.'],
    ['Muestra «Diapositiva 3 de 8» y el zoom', 'Barra de estado', 'Está hasta abajo de la ventana.'],
], 'Recuerda la ilustración de la ventana.', ['Panel de miniaturas', 'Marcador de posición', 'Cinta de opciones', 'Panel de notas', 'Barra de estado'])
c.A('👁️', '¿Qué vista usas?', 'Elige la vista que conviene en cada situación.', [
    ['Quieres revisar solo los títulos de las 10 diapositivas para ver si llevan orden', 'Esquema', 'Esquema muestra el texto de todas como un índice.'],
    ['Necesitas mover la diapositiva 7 al lugar 2 arrastrando', 'Clasificador de diapositivas', 'Ves todas en cuadrícula y las arrastras.'],
    ['Vas a imprimir tus apuntes con lo que dirás en cada diapositiva', 'Página de notas', 'Muestra cada diapositiva con sus notas.'],
    ['Estás escribiendo el texto de la diapositiva 4', 'Normal', 'La vista de trabajo de siempre.'],
    ['Vas a exponer frente al público en pantalla completa', 'Presentación', 'F5 inicia la presentación.'],
], 'Pregúntate: ¿escribo, reviso, acomodo, imprimo o expongo?', ['Normal', 'Esquema', 'Clasificador de diapositivas', 'Página de notas', 'Presentación'])
c.A('🎀', '¿En qué ficha lo buscas?', 'El equipo necesita estas herramientas. ¿Dónde están?', [
    ['Agregar una diapositiva nueva', 'Inicio', 'Inicio › Nueva diapositiva.'],
    ['Aplicar un tema con colores y fuentes ya combinados', 'Diseño', 'Diseño › Temas.'],
    ['Cambiar a la vista Esquema', 'Vista', 'Vista › Esquema.'],
    ['Poner viñetas al texto', 'Inicio', 'El grupo Párrafo de Inicio tiene las viñetas.'],
    ['Cambiar el tamaño de las diapositivas a 4:3', 'Diseño', 'Diseño › Tamaño de diapositiva.'],
], 'Texto y diapositivas → Inicio · Tema, tamaño y fondo → Diseño · Vistas → Vista.', ['Inicio', 'Diseño', 'Vista'])
sim('🧭', 'Recorre PowerPoint', 'Presentación simulada: usa las fichas y las vistas como en PowerPoint.',
    {'id': 'ent', 'tabs': ['arc', 'ini', 'vis'],
     'slides': [{'lay': 'tit', 't': 'Informática en CONALEP', 'b': 'Feria de Carreras'},
                {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes\nProgramación\nSoporte técnico'},
                {'lay': 'tc', 't': 'Contacto', 'b': 'Pregunta en servicios escolares'},
                {'lay': 'tc', 't': '¿Dónde trabajas?', 'b': 'Empresas\nEscuelas\nTu propio negocio'}],
     'intro': 'Esta es la presentación del equipo para la Feria de Carreras, pero le faltan cosas y está desordenada. Usa las fichas de arriba: <b>Inicio</b>, <b>Vista</b> y <b>Archivo</b>. Da clic en una miniatura de la izquierda para cambiar de diapositiva.'},
    [['En la ficha <b>Vista</b>, abre la vista <b>Esquema</b> y lee el orden de los títulos.', 'a.used["view:esq"]'],
     ['Abre el <b>Clasificador de diapositivas</b>. «Contacto» debe ir al final: selecciónala y usa <b>Inicio › ▼ Bajar</b> hasta dejarla al último.', 'a.used["view:cla"]&&/contacto/i.test(a.s(a.n-1).t)'],
     ['Regresa a la vista <b>Normal</b> y en <b>Inicio › Nueva diapositiva</b> agrega una «Título y objetos» con el título <b>¿Qué es Informática?</b> y al menos 3 renglones.', 'a.some(function(s){return /qu[eé] es/i.test(s.t)&&s.lay=="tc"&&' + LINES3 + '})'],
     ['Escribe en las <b>notas del orador</b> de la primera diapositiva lo que dirás para saludar (al menos 15 letras).', 'a.s(0).n.trim().length>=15'],
     ['Revisa tus notas en la vista <b>Página de notas</b>.', 'a.used["view:not"]'],
     ['Abre la <b>Ayuda</b> desde la ficha Archivo.', '!!a.used.help'],
     ['Presenta desde el principio (<b>Archivo › ▶ Desde el principio</b>) y avanza hasta el final.', '!!a.used.showEnd']],
    'El orden de las diapositivas se ve mejor en Esquema y Clasificador. Las notas solo las ves tú.')
a_end = c.mark() - 1

# ───────────────────────── B · Diseño de diapositiva ─────────────────────────
b0 = c.mark()
c.L('📐', 'Tamaño y orientación', 'Bloque B · Diseño de la diapositiva', body(
    bk('Tamaño', '<b>Diseño › Tamaño de diapositiva</b>: <b>Panorámica (16:9)</b>, la de las pantallas y proyectores actuales, o <b>Estándar (4:3)</b>, para proyectores viejos.'),
    bk('Personalizado', 'En «Tamaño de diapositiva personalizado» eliges Carta, A4 o medidas propias, por ejemplo para imprimir un cartel.'),
    bk('Orientación', '<b>Horizontal</b> para proyectar (casi siempre). <b>Vertical</b> para carteles, infografías o historias de redes sociales.'),
    warn('Ojo', 'Si cambias el tamaño cuando ya tienes contenido, PowerPoint pregunta <b>Maximizar</b> o <b>Ajustar</b>. «Ajustar» evita que se corte el contenido.'),
    ana('Piensa en…', 'La tele de tu casa es 16:9; las teles viejas y «cuadradas» eran 4:3.')),
    'Proyector o pantalla → 16:9 horizontal · Cartel → vertical.')
c.L('📏', 'Márgenes y resolución', 'Bloque B · Que nada se corte y se vea nítido', body(
    bk('Márgenes en PowerPoint', 'Las diapositivas no tienen márgenes como Word, pero cada <b>cuadro de texto</b> tiene <b>márgenes internos</b>: clic derecho › Formato de forma › Cuadro de texto › Izquierdo, Derecho, Superior, Inferior.'),
    bk('Zona segura', 'Deja un espacio libre de unos 1.5 cm en las orillas: algunos proyectores recortan los bordes.'),
    bk('Resolución', 'Es la cantidad de puntos (píxeles) de la imagen. Al <b>exportar</b> como video o imagen eliges <b>HD 720p</b> o <b>Full HD 1080p</b>: a más resolución, más nítido y más pesado el archivo.'),
    ex('En la Feria', 'El proyector del auditorio es Full HD (1920 × 1080). Diapositivas en 16:9 y video exportado en 1080p se verán nítidos.')),
    'Deja aire en las orillas · Exporta con la resolución del proyector.')
c.L('🖼️', 'El fondo de la diapositiva', 'Bloque B · Formato del fondo', body(
    bk('Dónde', '<b>Diseño › Formato del fondo</b> (o clic derecho sobre la diapositiva).'),
    bk('Tipos de relleno', '<b>Sólido</b> (un color), <b>Degradado</b> (dos o más colores), <b>Imagen o textura</b> y <b>Trama</b>.'),
    bk('Aplicar a todas', 'Por defecto el fondo cambia solo en la diapositiva actual. El botón <b>Aplicar a todo</b> lo pone en todas: así la presentación se ve pareja.'),
    bk('Transparencia', 'Si usas una foto de fondo, súbele la transparencia para que el texto se lea.'),
    warn('Error común', 'Una foto muy colorida de fondo con texto encima: no se lee nada.')),
    'Mismo fondo en todas · el texto siempre se debe leer.')
c.L('📝', 'Las notas del orador', 'Bloque B · Lo que dirás, sin ponerlo en la diapositiva', body(
    sp('En palabras sencillas', 'Las <b>notas</b> son tu acordeón: escribes ahí lo que vas a decir de cada diapositiva. El público no las ve.'),
    bk('Dónde', 'Debajo de la diapositiva, en el panel «Haz clic para agregar notas». Si no aparece: <b>Vista › Notas</b>.'),
    bk('Vista Moralizador', 'Al presentar con dos pantallas, tú ves tus notas y la siguiente diapositiva; el público solo ve la diapositiva actual.'),
    ex('En la Feria', 'Diapositiva «¿Dónde trabajas?», notas: «Contar que mi primo trabaja en soporte en el hospital y que hay bolsa de trabajo en el plantel».')),
    'Diapositiva = palabras clave · Notas = lo que explicas.')
c.A('📐', '¿Qué configuración conviene?', 'Elige la mejor opción para cada caso.', [
    ['Vas a proyectar en una pantalla moderna del auditorio', 'Panorámica 16:9', 'Es el formato de las pantallas actuales.'],
    ['Vas a imprimir un cartel para pegar en la entrada', 'Orientación vertical', 'Los carteles suelen ser verticales.'],
    ['El texto queda pegado a la orilla del cuadro', 'Márgenes internos del cuadro', 'Formato de forma › Cuadro de texto.'],
    ['Quieres que todas las diapositivas tengan el mismo fondo azul', 'Aplicar a todo', 'Así no cambias una por una.'],
    ['Quieres recordar un dato que dirás, sin que el público lo vea', 'Notas del orador', 'Las notas solo las ve el expositor.'],
    ['Vas a convertir la presentación en video para el proyector Full HD', 'Resolución 1080p', 'Coincide con la pantalla Full HD.'],
], 'Piensa en dónde se va a ver la presentación.',
    ['Panorámica 16:9', 'Orientación vertical', 'Márgenes internos del cuadro', 'Aplicar a todo', 'Notas del orador', 'Resolución 1080p'])
c.Z('🖼️', 'Completa: diseño de la diapositiva', 'Elige la palabra correcta.',
    '<p>El tamaño y el fondo se cambian en la ficha {0}.</p>'
    '<p>Las pantallas y proyectores actuales usan el tamaño {1}.</p>'
    '<p>Para que el fondo quede igual en todas las diapositivas uso {2}.</p>'
    '<p>Lo que voy a decir lo escribo en {3}.</p>'
    '<p>Un video exportado en 1080p tiene más {4} que uno en 720p.</p>',
    [['Diseño', ['Diseño', 'Inicio', 'Vista']],
     ['16:9', ['16:9', '4:3', 'Carta']],
     ['Aplicar a todo', ['Aplicar a todo', 'Duplicar', 'Restablecer']],
     ['las notas del orador', ['las notas del orador', 'el título', 'el pie de página']],
     ['resolución', ['resolución', 'margen', 'transición']]],
    'Recuerda las lecciones del bloque B.')
sim('📐', 'Configura las diapositivas de la Feria', 'Presentación simulada: tamaño, orientación, fondo y notas.',
    {'id': 'dis', 'tabs': ['arc', 'ini', 'dis', 'vis'], 'size': '4:3',
     'slides': [{'lay': 'tit', 't': 'Informática en CONALEP', 'b': 'Feria de Carreras 2026'},
                {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes\nProgramación\nSoporte técnico'},
                {'lay': 'tc', 't': '¿Dónde trabajas?', 'b': 'Empresas\nEscuelas\nTu propio negocio'}],
     'intro': 'Alguien hizo la presentación en tamaño 4:3, pero el auditorio tiene una pantalla panorámica. Arréglala con la ficha <b>Diseño</b>.'},
    [['Cambia el tamaño de diapositiva a <b>Panorámica 16:9</b>.', 'a.size=="16:9"'],
     ['Deja la orientación <b>Horizontal</b> (es para proyectar).', 'a.or=="h"&&a.size=="16:9"'],
     ['En <b>Formato del fondo</b>, elige un color claro para la diapositiva 1 y usa <b>Aplicar fondo a todas</b>.', 'a.every(function(s){return s.bg&&s.bg==a.s(0).bg})&&a.s(0).bg!="#1e293b"'],
     ['Escribe notas del orador (al menos 15 letras) en <b>todas</b> las diapositivas.', 'a.every(function(s){return s.n.trim().length>=15})'],
     ['En <b>Archivo › Exportar video</b>, elige la resolución <b>Full HD (1080p)</b> del proyector del auditorio.', 'a.used.res=="1080"']],
    'El fondo se aplica a una diapositiva; el botón «Aplicar fondo a todas» lo copia a las demás.')
b_end = c.mark() - 1

# ───────────────────────── C · Formato de diapositiva ─────────────────────────
c0 = c.mark()
c.L('🧱', 'Diseños de diapositiva', 'Bloque C · Elegir el acomodo correcto', body(
    sp('En palabras sencillas', 'El <b>diseño</b> (Inicio › Diseño) es el acomodo de los marcadores de posición. No es lo mismo que el tema: el diseño dice <b>dónde</b> va cada cosa.'),
    bk('Diapositiva de título', 'La portada: título grande y subtítulo.'),
    bk('Título y objetos', 'Título arriba y un espacio para viñetas, tabla o imagen. La más usada.'),
    bk('Encabezado de sección', 'Separa partes de la presentación: «Parte 2 · Campo laboral».'),
    bk('Dos objetos', 'Dos columnas: por ejemplo texto a la izquierda y foto a la derecha.'),
    bk('Solo el título y En blanco', 'Para poner una imagen grande o acomodar los objetos libremente.')),
    'Portada → Título · Contenido → Título y objetos · Cambiar de parte → Sección.')
c.L('🔠', 'Estilos de fuente', 'Bloque C · Que el texto se lea y se vea profesional', body(
    bk('Dónde', '<b>Inicio › Fuente</b>: tipo de letra, tamaño, negrita, cursiva, subrayado, sombra, color y espaciado entre caracteres.'),
    bk('Cuántas', 'Máximo <b>dos fuentes</b>: una para títulos y otra para el texto. Las fuentes <b>sin remates</b> (Calibri, Arial, Verdana, Segoe UI) se leen mejor en pantalla.'),
    bk('Tamaños', 'Títulos de 32 a 44 pt, texto de 24 a 28 pt, nunca menos de 18 pt.'),
    bk('Reemplazar fuentes', '<b>Inicio › Reemplazar › Reemplazar fuentes</b> cambia una fuente por otra en <b>toda</b> la presentación de un jalón.'),
    ex('En la Feria', 'Títulos en Segoe UI 40 pt negrita; texto en Segoe UI 26 pt.')),
    'Dos fuentes como máximo y tamaño legible desde el fondo.')
c.L('➕', 'Agregar fuentes', 'Bloque C · Instalar una fuente nueva', body(
    bk('Descargar', 'Busca fuentes gratuitas y legales, por ejemplo en <b>fonts.google.com</b>. Descarga el archivo <b>.ttf</b> u <b>.otf</b>.'),
    bk('Instalar en Windows', 'Abre el archivo y da clic en <b>Instalar</b> (o clic derecho › Instalar). Cierra y abre PowerPoint: ya aparece en la lista.'),
    bk('Incrustar', 'Si vas a abrir la presentación en otra computadora: <b>Archivo › Opciones › Guardar › Incrustar fuentes en el archivo</b>. Si no, PowerPoint la cambia por otra.'),
    warn('Ojo', 'En la escuela a veces no hay permiso para instalar. Si no puedes, usa las fuentes que ya tiene la computadora.')),
    'Descarga → Instalar → reiniciar PowerPoint → incrustar al guardar.')
c.L('¶', 'Párrafo: viñetas, alineación e interlineado', 'Bloque C · Acomodar el texto', body(
    bk('Viñetas y numeración', '<b>Inicio › Párrafo</b>: viñetas (•) para listas sin orden; numeración (1, 2, 3) para pasos.'),
    bk('Niveles de lista', 'Con <b>Tab</b> bajas un nivel (subpunto) y con <b>Mayús + Tab</b> lo subes.'),
    bk('Alineación', 'Izquierda para listas; centrado para títulos y frases cortas. Evita el justificado en diapositivas.'),
    bk('Interlineado', 'Espacio entre renglones: <b>1.0</b>, <b>1.5</b> o <b>2.0</b>. Con 1.0 a 1.2 la lista se ve compacta; con 1.5 respira más.'),
    ex('En la Feria', 'Lista de «¿Qué aprendes?» con viñetas, alineada a la izquierda e interlineado 1.5.')),
    'Viñetas para listas · izquierda para leer · 1.5 para respirar.')
c.L('✂️', 'Edición del texto', 'Bloque C · Corregir rápido', body(
    bk('Copiar formato', 'La <b>brocha</b> (Inicio › Copiar formato) copia el formato de un texto y lo pega en otro.'),
    bk('Buscar y reemplazar', '<b>Inicio › Edición › Reemplazar</b> (Ctrl + L en algunas versiones, Ctrl + H en otras) cambia una palabra en todas las diapositivas.'),
    bk('Seleccionar', '<b>Inicio › Seleccionar › Panel de selección</b> muestra todos los objetos de la diapositiva para elegir el que está escondido debajo de otro.'),
    bk('Ortografía', '<b>Revisar › Ortografía</b> (F7). Una falta de ortografía en grande se ve en todo el auditorio.')),
    'Brocha para el formato · Reemplazar para las palabras · F7 antes de exponer.')
c.A('🧱', '¿Qué diseño de diapositiva?', 'Elige el diseño para cada diapositiva de la Feria.', [
    ['La portada con «Informática en CONALEP» y el nombre del equipo', 'Diapositiva de título', 'Es la portada.'],
    ['«¿Qué aprendes?» con cuatro viñetas', 'Título y objetos', 'Título arriba y la lista abajo.'],
    ['Separar la parte «Campo laboral» del resto', 'Encabezado de sección', 'Marca el inicio de una nueva parte.'],
    ['Texto de un egresado a la izquierda y su foto a la derecha', 'Dos objetos', 'Dos columnas lado a lado.'],
    ['Una foto del laboratorio que ocupe toda la diapositiva', 'En blanco', 'Sin marcadores que estorben.'],
], 'El diseño dice dónde va cada cosa.', ['Diapositiva de título', 'Título y objetos', 'Encabezado de sección', 'Dos objetos', 'En blanco'])
c.A('🧰', '¿Qué herramienta lo resuelve?', 'El equipo tiene estos problemas. Elige la herramienta.', [
    ['Escribieron «Informatica» sin acento en 9 diapositivas', 'Reemplazar', 'Cambia la palabra en todas de una vez.'],
    ['Quieren que el título de la diapositiva 3 tenga el mismo formato que el de la 2', 'Copiar formato', 'La brocha copia el formato.'],
    ['Usaron Times New Roman y quieren Segoe UI en toda la presentación', 'Reemplazar fuentes', 'Cambia la fuente en todas las diapositivas.'],
    ['La lista de pasos debe ir 1, 2, 3', 'Numeración', 'Los pasos llevan número.'],
    ['Los renglones de la lista se ven amontonados', 'Interlineado 1.5', 'Da más espacio entre renglones.'],
], 'Lee el problema y piensa qué cambia: palabra, formato, fuente o párrafo.',
    ['Reemplazar', 'Copiar formato', 'Reemplazar fuentes', 'Numeración', 'Interlineado 1.5'])
c.T('🔢', 'Tamaños de letra', 'Escribe solo el número.', [
    ['¿Cuántas fuentes como máximo conviene usar en una presentación?', '2', 'Una para títulos y otra para el texto.', 'Títulos y texto.', 'm'],
    ['Según la regla 6 × 6, ¿cuántos renglones como máximo lleva una diapositiva?', '6', 'Máximo 6 renglones de unas 6 palabras.', 'Es el primer 6.', 'm'],
    ['¿Cuál es el tamaño mínimo de letra (en puntos) que deberías usar?', '18', 'Menos de 18 pt no se lee desde lejos.', 'Entre 14 y 20.', 'm'],
], 'Repasa las lecciones «Una buena diapositiva» y «Estilos de fuente».')
d_sim = sim('🎨', 'Da formato a las diapositivas', 'Presentación simulada: diseños, fuente y párrafo.',
    {'id': 'fmt', 'tabs': ['ini', 'dis', 'vis'],
     'slides': [{'lay': 'tc', 't': 'Informática en CONALEP', 'b': 'Feria de Carreras'},
                {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes de computadoras\nProgramación\nSoporte técnico\nDiseño web'},
                {'lay': 'tc', 't': '¿Dónde trabajas?', 'b': 'Empresas\nEscuelas\nTu propio negocio'}],
     'intro': 'Todas las diapositivas tienen el mismo diseño y el formato de fábrica. Dales el diseño y el formato que les toca con la ficha <b>Inicio</b>.'},
    [['Cambia la diapositiva 1 al diseño <b>Diapositiva de título</b>.', 'a.s(0).lay=="tit"'],
     ['Agrega después de la portada un <b>Encabezado de sección</b> que diga <b>Conoce la carrera</b>.', 'a.n>=4&&a.s(1).lay=="sec"&&/conoce/i.test(a.s(1).t)'],
     ['En «¿Qué aprendes?» usa la fuente <b>Segoe UI</b> o <b>Verdana</b> y tamaño <b>24</b> o más.', 'a.some(function(s){return /aprendes/i.test(s.t)&&/Segoe|Verdana/.test(s.ff)&&s.sz>=24})'],
     ['En la misma diapositiva deja las <b>viñetas</b> activas, alinea a la <b>izquierda</b> y pon <b>interlineado 1.5</b>.', 'a.some(function(s){return /aprendes/i.test(s.t)&&s.vi&&s.al=="l"&&s.ls==1.5})'],
     ['En «¿Dónde trabajas?» cambia el diseño a <b>Dos objetos</b>.', 'a.some(function(s){return /d[oó]nde/i.test(s.t)&&s.lay=="dos"})'],
     ['Revisa en la vista <b>Clasificador</b> que el orden sea portada, sección y contenido.', 'a.used["view:cla"]']],
    'El diseño (Inicio › Diseño) cambia el acomodo; la fuente y el párrafo, el aspecto del texto.')
c_end = c.mark() - 1

# ───────────────────────── D · Plantillas ─────────────────────────
d0 = c.mark()
c.L('🗂️', 'Temas y plantillas predeterminadas', 'Bloque D · Uso de plantillas', body(
    sp('En palabras sencillas', 'Un <b>tema</b> es un paquete de <b>colores, fuentes y efectos</b> que se aplica a todas las diapositivas de un clic. Una <b>plantilla</b> es un archivo (.potx) con tema, diseños y a veces contenido de ejemplo, listo para empezar.'),
    bk('Temas', '<b>Diseño › Temas</b>: pasa el puntero para ver la vista previa y da clic para aplicarlo. Con <b>Variantes</b> cambias la combinación de colores.'),
    bk('Plantillas predeterminadas', '<b>Archivo › Nuevo</b>: PowerPoint ofrece plantillas para informes escolares, álbumes, currículos y más (también Presentaciones de Google y Canva tienen las suyas).'),
    bk('Diseñador', 'En Microsoft 365, <b>Diseño › Diseñador</b> propone acomodos automáticos cuando insertas imágenes.'),
    ana('Piensa en…', 'El uniforme de la escuela: todos van iguales y se ve ordenado, sin que cada quien escoja su ropa diario.')),
    'Tema = colores + fuentes · Plantilla = archivo listo para empezar.')
c.L('🧩', 'Plantillas personalizadas y patrón', 'Bloque D · Tu propia plantilla', body(
    bk('Patrón de diapositivas', '<b>Vista › Patrón de diapositivas</b>: lo que cambies ahí (logotipo, pie de página, fuentes, colores) aparece en <b>todas</b> las diapositivas. Cierra con «Cerrar vista Patrón».'),
    bk('Guardar como plantilla', '<b>Archivo › Guardar como › Plantilla de PowerPoint (.potx)</b>. La próxima vez la eliges en Archivo › Nuevo › Personal.'),
    bk('¿Para qué?', 'Para que todos los equipos del grupo usen el mismo diseño, o para tener tu propia plantilla de tareas.'),
    ex('En la Feria', 'El grupo 311 crea la plantilla <b>Feria311.potx</b>: tema Océano, logotipo del plantel y el pie «CONALEP · Informática · Grupo 311». Cada equipo la usa para su parte.'),
    warn('Ojo', 'No pongas el logotipo diapositiva por diapositiva: ponlo una sola vez en el patrón.')),
    'Patrón = lo que se repite en todas · .potx = plantilla reutilizable.')
c.A('🗂️', '¿Tema, patrón o plantilla?', 'Elige qué conviene usar.', [
    ['Cambiar de un clic los colores y las fuentes de toda la presentación', 'Tema', 'El tema combina colores, fuentes y efectos.'],
    ['Poner el logotipo del plantel en todas las diapositivas', 'Patrón de diapositivas', 'Lo que va en el patrón se repite en todas.'],
    ['Que los otros equipos empiecen con el mismo diseño que tú', 'Plantilla .potx', 'Guardas tu diseño como plantilla.'],
    ['Empezar un álbum de fotos con un diseño ya hecho', 'Plantilla predeterminada', 'Archivo › Nuevo trae plantillas listas.'],
    ['Agregar el pie «Grupo 311» en todas las diapositivas', 'Patrón de diapositivas', 'También el pie de página se pone en el patrón.'],
], 'Tema = aspecto · Patrón = lo que se repite · Plantilla = archivo para empezar.',
    ['Tema', 'Patrón de diapositivas', 'Plantilla .potx', 'Plantilla predeterminada'])
c.O('🔢', 'Ordena: crear tu propia plantilla', 'Pon en orden los pasos.', [
    ['Aplica un tema en Diseño › Temas', 'Primero el aspecto general.'],
    ['Abre Vista › Patrón de diapositivas', 'Ahí se edita lo que se repite.'],
    ['Agrega el logotipo y el pie de página en el patrón', 'Aparecerán en todas las diapositivas.'],
    ['Cierra la vista Patrón', 'Regresas a la vista Normal.'],
    ['Guarda como Plantilla de PowerPoint (.potx)', 'Queda lista para reutilizar.'],
], 'Tema → patrón → logotipo y pie → cerrar → guardar .potx.')
c.W('✍️', 'Justifica tu diseño', 'Escribe por qué elegiste el tema de tu presentación.',
    'Explica en 2 o 3 oraciones qué <b>tema</b> o <b>colores</b> elegiste para la Feria de Carreras y por qué ayudan a que se lea bien desde el fondo del auditorio.',
    [['Tiene al menos 15 palabras', 'palabras:15'],
     ['Menciona el tema, los colores o el fondo', '\\b(tema|color\\w*|fondo|claro|oscuro|azul|blanco|negro|verde)\\b'],
     ['Habla de que se lea o se vea bien (contraste, legible, tamaño…)', '\\b(contraste|lee|leer|legible|vea|ver|distingu\\w+|tamano|grande)\\b'],
     ['Da una razón (porque, para que, ya que…)', '\\b(porque|para que|ya que|asi|por eso|debido)\\b']],
    'Piensa en la regla del contraste.', 'Elegí el tema… porque…')
sim('🧩', 'Crea la plantilla del grupo', 'Presentación simulada: tema, patrón y plantilla.',
    {'id': 'pla', 'tabs': ['arc', 'ini', 'dis', 'vis'],
     'slides': [{'lay': 'tit', 't': 'Informática en CONALEP', 'b': 'Equipo 1 · Feria de Carreras'},
                {'lay': 'tc', 't': '¿Qué aprendes?', 'b': 'Redes\nProgramación\nSoporte técnico'},
                {'lay': 'tc', 't': '¿Dónde trabajas?', 'b': 'Empresas\nEscuelas\nTu propio negocio'}],
     'intro': 'Ahora vas a dejar lista la plantilla que usarán todos los equipos del grupo 311.'},
    [['Aplica un tema en <b>Diseño › Temas</b> (que no sea Blanco).', 'a.theme!=""'],
     ['Abre <b>Vista › Patrón de diapositivas</b>.', 'a.used["view:pat"]'],
     ['En el patrón escribe el pie <b>CONALEP · Informática · Grupo 311</b>.', '/311/.test(a.master.ft)&&/inform/i.test(a.master.ft)'],
     ['Activa el <b>logotipo</b> de la escuela en el patrón.', 'a.master.logo'],
     ['Regresa a <b>Normal</b> y comprueba que el pie aparece en todas las diapositivas.', 'a.view=="nor"&&!!a.master.ft'],
     ['Guarda la plantilla (<b>Archivo › Guardar como plantilla .potx</b>).', '!!a.used.potx']],
    'Lo que pongas en el patrón aparece en todas las diapositivas.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Diapositiva', 'Cada «hoja» de la presentación.'),
    bk('Marcador de posición', 'Cuadro punteado listo para escribir título, texto o insertar un objeto.'),
    bk('Diseño de diapositiva', 'Acomodo de los marcadores: título, título y objetos, dos objetos…'),
    bk('Tema', 'Paquete de colores, fuentes y efectos para toda la presentación.'),
    bk('Patrón de diapositivas', 'Diapositiva «madre»: lo que tiene se repite en todas.'),
    bk('Plantilla (.potx)', 'Archivo con diseño listo para empezar presentaciones nuevas.'),
    bk('Notas del orador', 'Texto de apoyo para quien expone; el público no lo ve.'),
    bk('Esquema / Clasificador', 'Vistas para revisar el texto o acomodar las diapositivas.'),
    bk('16:9 y 4:3', 'Tamaños de diapositiva: panorámica y estándar.'),
    bk('Resolución', 'Cantidad de píxeles al exportar: 720p o 1080p.'),
    bk('Interlineado', 'Espacio entre renglones.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Plan de recuperación sugerido', body(
    bk('Situación', 'El R.A. 2.1 estaba programado del 6 al 13 de octubre. Este material permite recuperarlo rápido: los alumnos pueden avanzar en casa o en el celular, y los tres simuladores funcionan sin computadora.', 'sp'),
    bk('Sesión 1 · Bloques A y B (2 h)', 'Partes de la ventana, fichas, vistas y ayuda; tamaño, orientación, fondo, notas y resolución. Simuladores «Recorre PowerPoint» y «Configura las diapositivas». <b>Práctica 1</b>.'),
    bk('Sesión 2 · Bloque C (2 h)', 'Diseños de diapositiva, fuentes, agregar fuentes, párrafo y edición. Simulador «Da formato a las diapositivas». <b>Práctica 2</b>.'),
    bk('Sesión 3 · Bloque D y evaluación (2 h)', 'Temas, plantillas predeterminadas, patrón y plantilla .potx. Simulador «Crea la plantilla del grupo». <b>Práctica 3</b> y entrega de la A.E. 2.1.'),
    bk('Sugerencia', 'Si el tiempo apremia, deje los bloques A y B como tarea con el material y use la clase para las prácticas 2 y 3. La presentación de la A.E. 2.1 se reutiliza en el R.A. 2.2 para agregar objetos y animaciones.'),
    bk('Nota', 'La actividad de evaluación se desbloquea al completar este material. En este R.A. todavía no se piden animaciones ni transiciones.', 'sp')),
    'Ajuste las sesiones a su calendario.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🎤', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🪟', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '📐', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🔠', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '🗂️', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🎤",t:"Empieza aquí",d:"Para qué sirve una presentación y cómo es una buena diapositiva.",time:"20 min",obj:["Distinguir cuándo usar una presentación","Reconocer una buena diapositiva"],sum:["La presentación apoya al expositor; no lo reemplaza.","Una idea · regla 6 × 6 · letra grande · buen contraste."],q:"¿Cuál es la peor presentación que te ha tocado ver y qué le faltaba?"},
a:{k:"Bloque A",l:"A",ic:"🪟",t:"Reconocimiento del entorno de trabajo",d:"Barras, herramientas, diapositivas, vistas y ayuda.",time:"80 min",obj:["Nombrar las partes de la ventana de PowerPoint","Ubicar cada herramienta en su ficha","Usar las vistas Normal, Esquema, Clasificador y Notas","Pedir ayuda con Buscar o F1"],sum:["Izquierda = miniaturas · Centro = diapositiva · Abajo = notas.","Texto → Inicio · Tema y fondo → Diseño · Vistas → Vista.","Esquema revisa el texto; Clasificador acomoda las diapositivas."],q:"¿Qué vista usarías para revisar que tu exposición lleve un orden lógico?"},
b:{k:"Bloque B",l:"B",ic:"📐",t:"Diseño de diapositiva",d:"Tamaño, orientación, márgenes, fondo, notas y resolución.",time:"60 min",obj:["Elegir tamaño y orientación según dónde se verá","Aplicar un fondo a todas las diapositivas","Escribir notas del orador","Elegir la resolución al exportar"],sum:["Proyector → 16:9 horizontal · Cartel → vertical.","«Aplicar a todo» deja el mismo fondo en todas.","Notas = lo que dices; el público no las ve."],q:"¿Por qué conviene escribir notas del orador en lugar de llenar la diapositiva de texto?",rev:[["Para revisar solo los títulos de todas las diapositivas uso la vista…",["Esquema","Clasificador","Lectura"],0,"Esquema muestra el texto como índice."],["La ayuda de PowerPoint se abre con la tecla…",["F1","F5","F7"],0,"F5 presenta y F7 revisa ortografía."]]},
c:{k:"Bloque C",l:"C",ic:"🔠",t:"Formato de diapositiva",d:"Diseños, estilos de fuente, agregar fuentes, párrafo y edición.",time:"100 min",obj:["Elegir el diseño adecuado para cada diapositiva","Aplicar fuente, tamaño y color legibles","Instalar e incrustar fuentes","Usar viñetas, alineación e interlineado"],sum:["Portada → Título · Contenido → Título y objetos · Parte nueva → Sección.","Máximo dos fuentes; títulos 32–44 pt, texto 24–28 pt.","Brocha para el formato, Reemplazar para palabras y fuentes."],q:"¿Qué pasa si llevas tu presentación con una fuente descargada a otra computadora?",rev:[["Para que todas las diapositivas tengan el mismo fondo uso…",["Aplicar a todo","Duplicar","Nueva diapositiva"],0,"Está en Formato del fondo."],["Las pantallas modernas usan el tamaño…",["16:9","4:3","Carta"],0,"Panorámica."]]},
d:{k:"Bloque D",l:"D",ic:"🗂️",t:"Uso de plantillas",d:"Temas, plantillas predeterminadas, patrón y plantillas personalizadas.",time:"80 min",obj:["Aplicar un tema y sus variantes","Empezar desde una plantilla predeterminada","Editar el patrón de diapositivas","Guardar una plantilla personalizada .potx"],sum:["Tema = colores + fuentes + efectos.","Patrón = lo que se repite en todas.","Archivo › Guardar como › .potx = plantilla reutilizable."],q:"¿Para qué le serviría al grupo tener una plantilla común?",rev:[["El diseño «Encabezado de sección» sirve para…",["Separar partes de la presentación","Poner la portada","Insertar un video"],0,"Marca el inicio de una nueva parte."],["Cambiar una fuente en toda la presentación de un jalón:",["Reemplazar fuentes","Copiar formato","Interlineado"],0,"Inicio › Reemplazar › Reemplazar fuentes."]]}
'''

ILL = r'''
ILL["Las partes de la ventana"]=function(){var o=R_(10,6,320,20,"r",4)+T_(170,20,"Barra de título · FeriaCarreras.pptx","tw")+R_(10,30,320,22,"g",4)+T_(170,45,"Acceso rápido · Cinta de opciones (fichas)","tw");for(var i=0;i<4;i++)o+=R_(14,58+i*20,50,16,i==1?"b":"s",2);o+=T_(39,148,"miniaturas","tm")+R_(72,58,256,76,"s",4)+T_(200,90,"Haz clic para agregar título","t")+T_(200,112,"(diapositiva)","tm")+R_(72,138,256,16,"a",3)+T_(200,150,"Notas del orador","td")+R_(10,158,320,14,"s",3)+T_(170,169,"Diapositiva 2 de 4 · vistas · zoom","tm");return SV(340,178,o,"Partes de la ventana de PowerPoint")};
ILL["Las vistas de la presentación"]=function(){return grid3([["✏️","Normal|escribir"],["📑","Esquema|revisar texto"],["▦","Clasificador|ordenar"],["📝","Página de|notas"],["📖","Vista de|lectura"],["▶","Presentación|F5"]],"Vistas de PowerPoint")};
ILL["Tamaño y orientación"]=function(){return SV(340,130,R_(20,20,160,90,"b",4)+T_(100,70,"16:9 panorámica","tw")+R_(200,25,100,75,"s",4)+T_(250,67,"4:3","t")+T_(100,124,"pantallas actuales","tm")+T_(250,124,"proyector viejo","tm"),"Tamaños de diapositiva")};
ILL["El fondo de la diapositiva"]=function(){var o='';[["s","Sólido"],["b","Degradado"],["g","Imagen"]].forEach(function(x,i){o+=R_(16+i*108,14,96,60,x[0],4)+T_(64+i*108,48,x[1],x[0]=="s"?"t":"tw")});o+=R_(60,90,220,26,"a",6)+T_(170,108,"Aplicar a todo","td");return SV(340,126,o,"Formato del fondo")};
ILL["Diseños de diapositiva"]=function(){var o='',L=[["Título","tit"],["Título y objetos","tc"],["Sección","sec"],["Dos objetos","dos"]];L.forEach(function(x,i){var X=12+i*82;o+=R_(X,14,74,48,"s",3);if(x[1]=="tit"||x[1]=="sec"){o+=R_(X+8,28,58,8,"b",1)+R_(X+18,40,38,5,"g",1)}else{o+=R_(X+6,18,62,7,"b",1);if(x[1]=="tc")o+=R_(X+6,30,62,26,"g",1);else o+=R_(X+6,30,29,26,"g",1)+R_(X+39,30,29,26,"g",1)}o+=T_(X+37,78,x[0],"tm")});return SV(340,88,o,"Diseños de diapositiva")};
ILL["Temas y plantillas predeterminadas"]=function(){return grid3([["⬜","Blanco"],["🌊","Océano"],["🌲","Bosque"],["🌅","Atardecer"],["📁","Archivo ›|Nuevo"],["✨","Diseñador"]],"Temas y plantillas")};
ILL["Plantillas personalizadas y patrón"]=function(){var o=R_(20,10,120,74,"b",4)+T_(80,40,"Patrón","tw")+T_(80,58,"logo · pie","tw");for(var i=0;i<3;i++)o+=R_(190,8+i*28,110,24,"s",3)+T_(245,24+i*28,"Diapositiva "+(i+1)+" · logo · pie","tm");o+=T_(165,50,"→","t")+T_(170,108,"Lo que va en el patrón se repite en todas","tm");return SV(340,116,o,"Patrón de diapositivas")};
'''

EXH = r'''
function pw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><div style="background:#fff;color:#111;padding:8px;font:13px system-ui;overflow-x:auto">'+b+'</div></div>'}
EXH.ventana=function(){return exw(pw_('PowerPoint · FeriaCarreras.pptx','<div style="background:#c43e1c;color:#fff;padding:4px 8px;border-radius:4px">💾 ↶ ▶ '+mk(1)+' &nbsp; Archivo · Inicio · Insertar · Diseño · Vista '+mk(2)+'</div><div style="display:flex;gap:8px;margin-top:6px"><div style="width:60px;border:1px solid #ccc;padding:3px;font-size:10px">1 ▭<br>2 ▭<br>3 ▭ '+mk(3)+'</div><div style="flex:1;border:1px solid #ccc;padding:14px;text-align:center">Informática en CONALEP '+mk(4)+'</div></div><div style="border:1px solid #ccc;margin-top:4px;padding:3px 6px;color:#666">Haz clic para agregar notas '+mk(5)+'</div>'),['Barra de acceso rápido.','Cinta de opciones.','Panel de miniaturas.','Diapositiva con sus marcadores.','Panel de notas.'])};
EXH.vistas=function(){return exw(pw_('Vista','Normal · <b>Esquema</b> '+mk(1)+' · <b>Clasificador de diapositivas</b> '+mk(2)+' · Página de notas · Vista de lectura'),['Revisa el orden de los títulos.','Acomoda arrastrando.'])};
EXH.tamano=function(){return exw(pw_('Diseño › Tamaño de diapositiva','<b>Panorámica (16:9)</b> '+mk(1)+'<br>Estándar (4:3)<br>Tamaño de diapositiva personalizado… '+mk(2)),['Para el proyector o la pantalla.','Para carteles: elige Carta y orientación vertical.'])};
EXH.fondo=function(){return exw(pw_('Formato del fondo','○ Relleno sólido &nbsp; ● Relleno degradado '+mk(1)+'<br>Color: Azul claro<br>Transparencia: 0%<br><span style="border:1px solid #999;padding:2px 10px;display:inline-block;margin-top:6px">Aplicar a todo</span> '+mk(2)),['El tipo de relleno.','Para que todas queden iguales.'])};
EXH.notas=function(){return exw(pw_('Panel de notas','Diapositiva 3 · ¿Dónde trabajas?<div style="border:1px solid #ccc;margin-top:6px;padding:6px">Contar que hay bolsa de trabajo en el plantel y que muchos egresados ponen su propio negocio de reparación. '+mk(1)+'</div>'),['Lo que vas a decir. El público no lo ve.'])};
EXH.diseno=function(){return exw(pw_('Inicio › Diseño','▭ Diapositiva de título '+mk(1)+' · ▭ Título y objetos '+mk(2)+' · ▭ Encabezado de sección '+mk(3)+' · ▭ Dos objetos'),['Para la portada.','Para el contenido con viñetas.','Para separar partes.'])};
EXH.fuente=function(){return exw(pw_('Inicio › Fuente y Párrafo','Segoe UI ▾ &nbsp; 26 ▾ '+mk(1)+' &nbsp; <b>N</b> <i>K</i> <u>S</u> &nbsp;|&nbsp; • Viñetas '+mk(2)+' &nbsp; ⇤ ↔ ⇥ &nbsp; Interlineado 1.5 ▾ '+mk(3)),['Fuente y tamaño legibles.','Viñetas para la lista.','Más espacio entre renglones.'])};
EXH.instalar=function(){return exw(pw_('Descargas › Montserrat-Regular.ttf','Aa Bb Cc 123<br><span style="border:1px solid #999;padding:2px 10px;display:inline-block;margin-top:6px">Instalar</span> '+mk(1)+'<br><small>Archivo › Opciones › Guardar › ☑ Incrustar fuentes en el archivo</small> '+mk(2)),['Instala y reinicia PowerPoint.','Para que se vea igual en otra computadora.'])};
EXH.patron=function(){return exw(pw_('Vista › Patrón de diapositivas','<div style="border:2px solid #c43e1c;padding:8px;position:relative;height:70px">🏫 '+mk(1)+'<div style="position:absolute;bottom:4px;left:0;right:0;text-align:center;font-size:11px">CONALEP · Informática · Grupo 311 '+mk(2)+'</div></div><span style="border:1px solid #999;padding:2px 10px;display:inline-block;margin-top:6px">Cerrar vista Patrón</span>'),['El logotipo, una sola vez.','El pie que se repite en todas.'])};
EXH.potx=function(){return exw(pw_('Archivo › Guardar como','Nombre: <b>Feria311</b><br>Tipo: <b>Plantilla de PowerPoint (*.potx)</b> '+mk(1)),['Así queda como plantilla reutilizable.'])};
EXH.cel=function(){return exw(mp('PowerPoint o Presentaciones · celular','<div class="mbox">＋ Nueva diapositiva · toca una diapositiva › Diseño '+mk(1)+'</div><div class="mbox" style="margin-top:6px">✏️ Selecciona el texto › A (formato): fuente, tamaño, viñetas '+mk(2)+'</div><div class="mbox" style="margin-top:6px">⋮ › Tema · Cambiar fondo · Notas del orador '+mk(3)+'</div>'),['Agrega y cambia el diseño de las diapositivas.','Formato del texto.','Tema, fondo y notas.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Conoce PowerPoint y prepara tus diapositivas',
     'prog': 'Bloques A y B · Entorno de trabajo y diseño de diapositiva',
     'min': 50, 'lug': 'En clase, laboratorio o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con PowerPoint (o Presentaciones de Google)', 'Documento o carpeta para tus capturas'],
                'steps': [
                    ['Abre PowerPoint, toma una captura de la ventana y señala sus partes: acceso rápido, cinta, miniaturas, diapositiva y notas.', 'ventana'],
                    'Crea el archivo <b>Apellido_Nombre_EDOA21.pptx</b> con 5 diapositivas sobre la carrera de Informática (portada, ¿qué es?, ¿qué aprendes?, ¿dónde trabajas?, contacto).',
                    ['En <b>Diseño › Tamaño de diapositiva</b> deja Panorámica 16:9 y orientación horizontal.', 'tamano'],
                    ['Aplica un fondo claro con <b>Formato del fondo</b> y da clic en <b>Aplicar a todo</b>.', 'fondo'],
                    ['Escribe notas del orador en cada diapositiva y revisa el orden en las vistas Esquema y Clasificador.', 'vistas']]},
         'cel': {'mat': ['Celular con PowerPoint o Presentaciones de Google', 'Galería o notas para tus capturas'],
                 'steps': [
                     ['Abre la app, toma una captura y anota dónde están las diapositivas, el botón de nueva diapositiva y las notas.', 'cel'],
                     'Crea la presentación <b>Apellido_Nombre_EDOA21</b> con 5 diapositivas sobre la carrera de Informática.',
                     'En ⋮ › Configuración de página (o Diseño › Tamaño) deja Panorámica 16:9.',
                     ['Cambia el fondo de las diapositivas a un color claro, igual en todas.', 'fondo'],
                     ['Escribe notas del orador en cada diapositiva (⋮ › Notas del orador).', 'notas']]}},
     'entrega': ['Tu presentación con 5 diapositivas, fondo y notas; la sigues usando en las prácticas 2 y 3.'],
     'rub': [['Partes de la ventana identificadas', 20], ['Cinco diapositivas con orden lógico', 25], ['Tamaño y fondo iguales en todas', 25], ['Notas del orador en cada diapositiva', 30]]},
    {'id': 'pr2', 'n': 2, 't': 'Da formato a tus diapositivas',
     'prog': 'Bloque C · Formato de diapositiva',
     'min': 60, 'lug': 'En clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu presentación de la práctica 1', 'Computadora con PowerPoint'],
                'steps': [
                    'Antes de empezar, termina el simulador «Da formato a las diapositivas» de este material.',
                    ['Asigna el diseño correcto a cada diapositiva: portada, un encabezado de sección y diapositivas de título y objetos.', 'diseno'],
                    ['Elige máximo dos fuentes; títulos de 32 a 44 pt y texto de 24 a 28 pt.', 'fuente'],
                    'Usa viñetas o numeración, alineación a la izquierda e interlineado 1.5 en las listas. Cumple la regla 6 × 6.',
                    ['(Opcional) Instala una fuente gratuita y activa Incrustar fuentes al guardar.', 'instalar'],
                    'Revisa la ortografía con F7 y usa Reemplazar para corregir una palabra en todas las diapositivas.']},
         'cel': {'mat': ['Tu presentación de la práctica 1', 'Celular con PowerPoint o Presentaciones de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Da formato a las diapositivas» de este material.',
                     ['Cambia el diseño de cada diapositiva (toca la diapositiva › Diseño): portada, sección y contenido.', 'cel'],
                     'Selecciona el texto y usa el botón de formato: máximo dos fuentes y tamaños legibles.',
                     'Aplica viñetas, alineación a la izquierda e interlineado en las listas. Cumple la regla 6 × 6.',
                     'Revisa la ortografía de cada diapositiva.']}},
     'entrega': ['Tu presentación con formato: es la base de tu actividad de evaluación.'],
     'rub': [['Diseño adecuado en cada diapositiva', 25], ['Fuentes y tamaños legibles', 25], ['Viñetas, alineación e interlineado', 25], ['Regla 6 × 6 y sin faltas de ortografía', 25]]},
    {'id': 'pr3', 'n': 3, 't': 'Aplica un tema y crea tu plantilla',
     'prog': 'Bloque D · Uso de plantillas',
     'min': 50, 'lug': 'En clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu presentación de las prácticas 1 y 2', 'Computadora con PowerPoint'],
                'steps': [
                    'Antes de empezar, termina el simulador «Crea la plantilla del grupo» de este material.',
                    'Aplica un tema en <b>Diseño › Temas</b> y elige una variante con buen contraste.',
                    ['En <b>Vista › Patrón de diapositivas</b> agrega el logotipo del plantel y el pie «CONALEP · Informática · Grupo 311».', 'patron'],
                    ['Cierra el patrón y guarda una copia como <b>Plantilla de PowerPoint (.potx)</b>.', 'potx'],
                    'Abre Archivo › Nuevo, elige una plantilla predeterminada y toma una captura de las que ofrece.']},
         'cel': {'mat': ['Tu presentación de las prácticas 1 y 2', 'Celular con PowerPoint o Presentaciones de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Crea la plantilla del grupo» de este material.',
                     ['Aplica un tema (⋮ › Cambiar tema, o Diseño › Temas).', 'cel'],
                     'Agrega en cada diapositiva un pie pequeño «CONALEP · Informática · Grupo 311» (en celular no hay patrón: cópialo en todas).',
                     'Abre la galería de plantillas de la app y toma una captura de las que ofrece.',
                     'Escribe en tus notas para qué sirve el patrón de diapositivas.']}},
     'entrega': ['Tu presentación con tema y patrón, y la plantilla .potx (o la captura en celular).'],
     'rub': [['Tema aplicado con buen contraste', 30], ['Logotipo y pie en el patrón', 30], ['Plantilla .potx guardada', 25], ['Captura de plantillas predeterminadas', 15]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 2',
    'ra': 'R.A. 2.1', 'title': 'Presentación electrónica con formato',
    'data': [
        ('Resultado de aprendizaje', 'Aplica formato al documento usando opciones disponibles y de estilo y/o plantillas del presentador gráfico, acorde al diseño requerido del usuario.'),
        ('Actividad de evaluación', '2.1.1 Da formato a una presentación electrónica que cumpla con: diseño de la diapositiva, estilos y plantillas.'),
        ('Evidencia', 'Documento digital (presentación .pptx o PDF)'),
        ('Ponderación', '10% (según el programa)'),
        ('Entrega', 'En la plataforma, en la fecha que indique tu docente'),
    ],
    'situation': 'Vienen alumnos de secundaria a la <b>Feria de Carreras</b> del plantel. Elabora la presentación de 5 minutos que les explique la carrera de <b>Informática</b> (o el tema que te asigne tu docente), con un diseño profesional y fácil de leer desde el fondo del auditorio.',
    'hint': 'Ya hiciste casi todo en las prácticas: revisa esta lista con tu presentación abierta y marca cada punto.',
    'steps': [
        ('Contenido y vistas', [
            'Archivo <b>Apellido_Nombre_EDOA21.pptx</b> con al menos 6 diapositivas: portada, un encabezado de sección y al menos 4 de contenido.',
            'Orden lógico revisado en las vistas Esquema y Clasificador.',
            'Notas del orador en cada diapositiva de contenido.']),
        ('Diseño de la diapositiva', [
            'Tamaño Panorámica 16:9, orientación horizontal.',
            'El mismo fondo (o el del tema) en todas las diapositivas.']),
        ('Estilos', [
            'Diseño de diapositiva adecuado en cada una (título, sección, título y objetos, dos objetos).',
            'Máximo dos fuentes; títulos de 32 a 44 pt y texto de 24 a 28 pt; buen contraste.',
            'Listas con viñetas o numeración, alineación e interlineado adecuados; regla 6 × 6.',
            'Sin faltas de ortografía.']),
        ('Plantillas', [
            'Un tema aplicado (o una plantilla predeterminada).',
            'Patrón de diapositivas con logotipo y pie «CONALEP · Informática · Grupo 311».']),
        ('Entrega', [
            'Revisa la presentación completa con F5.',
            'Sube tu archivo .pptx (o su PDF) en la actividad R.A. 2.1 de la plataforma.']),
    ],
    'rubric': [
        ('Seis diapositivas con orden lógico y notas', 15), ('Tamaño, orientación y fondo uniformes', 15),
        ('Diseño de diapositiva adecuado', 15), ('Fuentes, tamaños y contraste legibles', 20),
        ('Párrafos: viñetas, alineación, interlineado y 6 × 6', 15), ('Tema y patrón con logotipo y pie', 15), ('Ortografía', 5),
    ],
    'deliver': ['Un archivo .pptx (o PDF) de máximo 20 MB.', 'Nombre del archivo: Apellido_Nombre_EDOA21.', 'Súbelo en la actividad R.A. 2.1 de la plataforma.'],
}
