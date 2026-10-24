"""EDOA-20 · R.A. 3.1 · Formato del libro y la hoja de cálculo.

Caso de las lecciones: Cafetería La Escuelita (inventario y ventas de la cafetería del plantel).
Incluye dos hojas de cálculo simuladas (xls_sim.js) para practicar sin computadora.
La actividad de evaluación es la entrega del libro (.xlsx o PDF) en la plataforma.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-3.1'
CODE_PREFIX = 'EDOA31'
FILE = 'edoa-ra31-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 3.1 · Formato del libro y la hoja de cálculo'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 3.1 · Formato del libro y la hoja de cálculo'
HERO_KICK = 'EDOA-20 · R.A. 3.1'
HERO_TITLE = 'Una hoja de cálculo clara, ordenada y lista para imprimir'
HERO_TEXT = 'Conoce las partes de Excel, configura la hoja y la página, y da formato a celdas, filas y columnas como lo haría una oficina real.'
EV_SHORT = 'da formato a tu libro de trabajo y entrégalo.'
EV_CARD = 'Libro de trabajo R.A. 3.1'
RA = 'R.A. 3.1'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simulador de hoja de cálculo'], 'c': ['Construye', 'Prácticas en la hoja de cálculo']}

EXTRA_JS = (Path(__file__).parent / 'xls_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".xlsim"))xlsInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".xlsim"))return xlsCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.c, a.all, a.mg, a.fitcols, a.pg, a.sh, a.vw, a.used, a.fits)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pXls({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


def table(rows, start=1, style=None):
    """Convierte filas en celdas {A1:{v:…}}; style(c, r, v) agrega formato."""
    out = {}
    for r, row in enumerate(rows, start):
        for col, v in zip('ABCDEFG', row):
            if v is None:
                continue
            cell = {'v': v}
            if style:
                cell.update(style(col, r, v))
            out[f'{col}{r}'] = cell
    return out


INVENTARIO = table([
    ['Cafetería La Escuelita · Inventario de la semana'],
    ['Producto', 'Cantidad', 'Precio', 'Total', 'Descuento', 'Fecha de compra', 'Proveedor'],
    ['Torta de jamón', 20, 35, 700, 0, 46318, 'Panadería El Trigal'],
    ['Agua natural 600 ml', 48, 12, 576, 0.05, 46316, 'Purificadora Agua Clara'],
    ['Jugo de naranja', 24, 18, 432, 0.1, 46317, 'Frutería Doña Mary'],
    ['Galletas de avena', 30, 10, 300, 0, 46315, 'Dulcería La Huasteca'],
    ['Sincronizada', 15, 30, 450, 0.05, 46318, 'Panadería El Trigal'],
    ['Fruta picada', 18, 25, 450, 0.15, 46319, 'Frutería Doña Mary'],
])

VENTAS_ROWS = [
    ['Fecha', 'Producto', 'Cantidad', 'Precio', 'Total', 'Vendió', 'Forma de pago'],
    [46314, 'Torta de jamón', 12, 35, 420, 'Lupita', 'Efectivo'],
    [46314, 'Agua natural 600 ml', 25, 12, 300, 'Lupita', 'Efectivo'],
    [46314, 'Fruta picada', 9, 25, 225, 'Carlos', 'Transferencia'],
    [46315, 'Sincronizada', 8, 30, 240, 'Carlos', 'Efectivo'],
    [46315, 'Jugo de naranja', 14, 18, 252, 'Lupita', 'Tarjeta'],
    [46315, 'Galletas de avena', 20, 10, 200, 'Lupita', 'Efectivo'],
    [46316, 'Torta de jamón', 15, 35, 525, 'Carlos', 'Transferencia'],
    [46316, 'Agua natural 600 ml', 30, 12, 360, 'Carlos', 'Efectivo'],
    [46317, 'Fruta picada', 11, 25, 275, 'Lupita', 'Tarjeta'],
    [46317, 'Sincronizada', 10, 30, 300, 'Lupita', 'Efectivo'],
    [46318, 'Jugo de naranja', 16, 18, 288, 'Carlos', 'Efectivo'],
    [46318, 'Torta de jamón', 18, 35, 630, 'Carlos', 'Transferencia'],
    [46318, 'Galletas de avena', 22, 10, 220, 'Lupita', 'Efectivo'],
    [46318, 'Agua natural 600 ml', 28, 12, 336, 'Lupita', 'Tarjeta'],
]


def ventas_style(col, r, v):
    if r == 1:
        return {'b': True, 'fill': '#1e3a8a', 'fc': '#ffffff', 'al': 'c', 'bd': True}
    s = {'bd': True}
    if col == 'A':
        s['nf'] = 'fec'
    if col in 'DE':
        s['nf'] = 'mon'
    return s


VENTAS = table(VENTAS_ROWS, style=ventas_style)

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('☕', '¿Para qué sirve una hoja de cálculo?', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Una <b>hoja de cálculo</b> (Excel, Hojas de cálculo de Google o Calc) es una cuadrícula para organizar datos en filas y columnas, hacer cuentas y presentar la información. En Word escribes textos; en Excel <b>ordenas y calculas datos</b>.'),
    ex('Caso de las lecciones: Cafetería La Escuelita', 'Doña Lupita lleva el inventario y las ventas de la cafetería del plantel en una libreta. Le vamos a ayudar a pasarlo a Excel y a dejarlo <b>claro, bonito y listo para imprimir</b>.'),
    r3([('🧭', 'Conocer', 'Las partes de la ventana y del libro.'), ('⚙️', 'Configurar', 'La hoja y la página para imprimir.'), ('🎨', 'Dar formato', 'Celdas, filas, columnas y números.')]),
    bk('Al final', 'Entregas un <b>libro de trabajo con formato</b>, en digital (.xlsx o PDF) e impreso. Vale <b>5%</b>. En este R.A. todavía no usamos fórmulas: eso viene en el 3.2.')),
    'Word = textos · Excel = datos en filas y columnas.')
c.A('🧩', '¿Qué programa conviene?', 'Elige el programa más adecuado para cada tarea de la cafetería.', [
    ['Llevar el inventario con cantidades y precios de cada producto', 'Hoja de cálculo', 'Son datos en filas y columnas, con números.'],
    ['Escribir una carta al director pidiendo más mesas', 'Procesador de texto', 'Una carta es texto corrido: Word.'],
    ['Registrar las ventas de cada día de la semana', 'Hoja de cálculo', 'Una tabla de datos que crece cada día.'],
    ['Presentar el nuevo menú en la junta de padres', 'Presentaciones', 'Para exponer se usan diapositivas.'],
    ['Comparar cuánto se gastó con cada proveedor', 'Hoja de cálculo', 'Comparar números es trabajo de Excel.'],
], 'Datos y números → hoja de cálculo · Texto → Word · Exponer → PowerPoint.', ['Hoja de cálculo', 'Procesador de texto', 'Presentaciones'])
s0_end = c.mark() - 1

# ───────────────────────── A · Elementos del libro ─────────────────────────
a0 = c.mark()
c.L('📗', 'Libro, hoja y celda', 'Bloque A · Elementos del libro de trabajo', body(
    bk('Libro de trabajo', 'Es el <b>archivo</b> de Excel (termina en <b>.xlsx</b>). Un libro puede tener varias hojas.'),
    bk('Hoja', 'Cada pestaña de abajo (Hoja1, Hoja2…). Se forma de <b>columnas</b> con letras (A, B, C…) y <b>filas</b> con números (1, 2, 3…).'),
    bk('Celda', 'El cuadrito donde se cruzan una columna y una fila. Su nombre es la <b>referencia</b>: primero la letra y luego el número, por ejemplo <b>C3</b>.'),
    bk('Rango', 'Un grupo de celdas. Se escribe la primera y la última separadas por dos puntos: <b>A2:G8</b>.'),
    ana('Piensa en…', 'El juego de «Batalla naval»: dices «B-4» y todos saben qué cuadro es. En Excel es igual: B4.'),
    ex('En la cafetería', 'El libro <b>Cafeteria.xlsx</b> tiene una hoja «Inventario» y otra «Ventas». En la celda A3 está «Torta de jamón» y en C3 su precio.')),
    'Libro = archivo · Hoja = pestaña · Celda = columna + fila (C3).')
c.L('🪟', 'Las partes de la ventana', 'Bloque A · Barras y herramientas', body(
    bk('Barra de título', 'Arriba: muestra el nombre del libro.'),
    bk('Barra de herramientas de acceso rápido', 'Botones que siempre están a la mano: Guardar, Deshacer, Rehacer. Se puede personalizar.'),
    bk('Cinta de opciones', 'Todas las herramientas, ordenadas en <b>fichas</b> (Inicio, Insertar, Disposición de página…).'),
    bk('Cuadro de nombres', 'A la izquierda, bajo la cinta: dice en qué celda estás. También sirve para ir a una celda o seleccionar un rango: escribe <b>A2:G8</b> y Enter.'),
    bk('Barra de fórmulas', 'Junto al cuadro de nombres (botón <b>fx</b>): muestra el <b>contenido real</b> de la celda.'),
    bk('Etiquetas de hojas', 'Abajo: las pestañas de cada hoja y el botón <b>+</b> para agregar otra.'),
    bk('Barra de estado', 'Hasta abajo: muestra la suma y el promedio de lo que seleccionas, las vistas y el zoom.')),
    'Cuadro de nombres = dónde estoy · Barra de fórmulas = qué hay realmente.')
c.L('🎀', 'Las fichas de la cinta de opciones', 'Bloque A · Dónde está cada herramienta', body(
    bk('Archivo', 'Guardar, abrir, <b>Imprimir</b> (con vista preliminar) y <b>Opciones</b> de Excel.'),
    bk('Inicio', 'La más usada: fuente, tamaño, color, alineación, bordes, relleno, formato de número, estilos y ancho de columnas.'),
    bk('Insertar', 'Tablas, imágenes, gráficos y el <b>encabezado y pie de página</b>.'),
    bk('Disposición de página', 'Márgenes, orientación, tamaño del papel, fondo y área de impresión.'),
    bk('Fórmulas, Datos y Revisar', 'Cálculos, ordenar y filtrar, ortografía y proteger (los verás en los siguientes R.A.).'),
    bk('Vista', 'Zoom, líneas de cuadrícula e inmovilizar paneles.'),
    ana('Piensa en…', 'Un supermercado: cada pasillo (ficha) agrupa productos parecidos. Si buscas leche, vas a lácteos; si buscas márgenes, vas a Disposición de página.')),
    'Formato → Inicio · Imprimir → Archivo · Página → Disposición de página · Ver → Vista.')
c.A('🪟', '¿Qué parte de la ventana es?', 'Lee la descripción y elige el nombre correcto.', [
    ['Muestra «B4» porque ahí está el cursor', 'Cuadro de nombres', 'Dice en qué celda estás.'],
    ['Muestra 0.16 aunque la celda dice 16%', 'Barra de fórmulas', 'Enseña el contenido real de la celda.'],
    ['Tiene las fichas Inicio, Insertar y Vista', 'Cinta de opciones', 'Ahí están todas las herramientas.'],
    ['Al seleccionar varios números dice «Suma: 2,908»', 'Barra de estado', 'Muestra cálculos rápidos de lo seleccionado.'],
    ['Tiene los botones Guardar y Deshacer siempre visibles', 'Barra de acceso rápido', 'Es la barra de herramientas de acceso rápido.'],
    ['Las pestañas «Inventario» y «Ventas»', 'Etiquetas de hojas', 'Cada pestaña es una hoja del libro.'],
], 'Recuerda la ilustración de la ventana.', ['Cuadro de nombres', 'Barra de fórmulas', 'Cinta de opciones', 'Barra de estado', 'Barra de acceso rápido', 'Etiquetas de hojas'])
c.T('🔤', 'Escribe la referencia', 'Escribe la celda o el rango, sin espacios.', [
    ['La celda de la columna C y la fila 5', 'C5', 'Primero la letra de la columna y luego el número de fila.', 'Letra y luego número.', 'u'],
    ['La celda que está a la derecha de B4', 'C4', 'A la derecha cambia la columna: de B a C.', 'Cambia la letra, no el número.', 'u'],
    ['La celda que está arriba de B4', 'B3', 'Arriba cambia la fila: de 4 a 3.', 'Cambia el número, no la letra.', 'u'],
    ['El rango que va de A1 hasta D10', 'A1:D10', 'Primera celda, dos puntos y última celda.', 'Usa dos puntos.', 'c'],
    ['¿Cuántas celdas tiene el rango A1:B3? (escribe solo el número)', '6', '2 columnas (A y B) × 3 filas = 6 celdas.', 'Columnas × filas.', 'm'],
], 'Columna (letra) + fila (número).')
c.A('🎀', '¿En qué ficha lo buscas?', 'Doña Lupita necesita estas herramientas. ¿Dónde están?', [
    ['Poner en negritas los encabezados', 'Inicio', 'El formato de fuente está en Inicio.'],
    ['Cambiar la hoja a horizontal', 'Disposición de página', 'La orientación está en Disposición de página.'],
    ['Agregar el nombre de la cafetería en el encabezado', 'Insertar', 'Insertar › Encabezado y pie de página.'],
    ['Que los títulos no se muevan al bajar por la lista', 'Vista', 'Vista › Inmovilizar paneles.'],
    ['Ver cómo saldrá la hoja antes de imprimir', 'Archivo', 'Archivo › Imprimir muestra la vista preliminar.'],
], 'Formato → Inicio · Página → Disposición · Encabezado → Insertar · Ver → Vista · Imprimir → Archivo.',
    ['Archivo', 'Inicio', 'Insertar', 'Disposición de página', 'Vista'])
a_end = c.mark() - 1

# ───────────────────────── B · Opciones de la hoja ─────────────────────────
b0 = c.mark()
c.L('👁️', 'El área de trabajo: ficha Vista', 'Bloque B · Opciones de la hoja de cálculo', body(
    bk('Zoom', 'Acerca o aleja la hoja (abajo a la derecha o en Vista › Zoom). No cambia el tamaño de impresión.'),
    bk('Líneas de cuadrícula', 'Las líneas grises que separan las celdas. Se pueden ocultar y <b>no se imprimen</b>.'),
    bk('Encabezados', 'Las letras de columna y los números de fila; también se pueden ocultar.'),
    bk('Inmovilizar paneles', '<b>Vista › Inmovilizar › Inmovilizar fila superior</b>: la fila 1 se queda fija mientras bajas. Muy útil en listas largas.'),
    ex('En la cafetería', 'La lista de ventas tiene 200 renglones. Con la fila superior inmovilizada, Doña Lupita siempre ve «Fecha, Producto, Cantidad…».')),
    'Inmovilizar = que los encabezados no se vayan.')
c.L('🧰', 'Personaliza tu barra de herramientas', 'Bloque B · Excel a tu medida', body(
    bk('Barra de acceso rápido', 'Da clic en la flechita <b>▾</b> al final de la barra y marca los comandos que más usas, por ejemplo <b>Vista previa de impresión e imprimir</b>.'),
    bk('Fuente predeterminada', '<b>Archivo › Opciones › General</b> › «Al crear nuevos libros»: eliges la fuente, el tamaño y cuántas hojas trae un libro nuevo. Se aplica al cerrar y volver a abrir Excel.'),
    bk('Mostrar u ocultar la cinta', 'Doble clic sobre el nombre de una ficha la contrae o la expande; así ganas espacio en pantallas pequeñas.'),
    warn('Ojo', 'Según tu versión, la fuente de fábrica es <b>Calibri</b> o <b>Aptos Narrow</b>, tamaño 11.')),
    'Lo que usas mucho, ponlo a un clic.')
c.L('🗂️', 'Trabaja con las hojas', 'Bloque B · Organizar el libro', body(
    bk('Insertar', 'Botón <b>+</b> junto a las etiquetas.'),
    bk('Cambiar nombre', 'Doble clic en la etiqueta (o clic derecho › Cambiar nombre). Usa nombres claros: «Inventario», no «Hoja1».'),
    bk('Color de etiqueta', 'Clic derecho › Color de pestaña, para distinguir las hojas.'),
    bk('Mover, copiar y eliminar', 'Arrastra la etiqueta para moverla; clic derecho para copiar o eliminar (¡eliminar no se puede deshacer!).'),
    ex('En la cafetería', 'Libro con tres hojas: <b>Inventario</b> (verde), <b>Ventas</b> (azul) y <b>Precios</b> (naranja).')),
    'Una hoja por tema, con nombre y color.')
c.A('⚙️', '¿Qué opción usas?', 'Elige la opción de Excel que resuelve cada situación.', [
    ['Al bajar por la lista ya no se ven los encabezados', 'Inmovilizar fila superior', 'Deja fija la fila 1.'],
    ['Las hojas se llaman Hoja1, Hoja2 y Hoja3 y nadie sabe qué tiene cada una', 'Cambiar nombre de la hoja', 'Un nombre claro dice qué contiene.'],
    ['Quieres que todos los libros nuevos usen Arial 12', 'Archivo › Opciones › General', 'Ahí se define la fuente predeterminada.'],
    ['Imprimes muy seguido y quieres el botón siempre a la mano', 'Personalizar acceso rápido', 'Agrega el comando a la barra de acceso rápido.'],
    ['Las letras se ven muy pequeñas en pantalla, pero se imprimen bien', 'Zoom', 'El zoom cambia la vista, no la impresión.'],
], 'Pregúntate: ¿es de la vista, de la hoja o de Excel?',
    ['Inmovilizar fila superior', 'Cambiar nombre de la hoja', 'Archivo › Opciones › General', 'Personalizar acceso rápido', 'Zoom'])
c.O('🔢', 'Ordena: cambiar la fuente predeterminada', 'Pon en orden los pasos para que los libros nuevos usen Arial 12.', [
    ['Abre la ficha Archivo', 'Las opciones de Excel están en Archivo.'],
    ['Entra a Opciones', 'Abre la ventana Opciones de Excel.'],
    ['En General, busca «Al crear nuevos libros»', 'Ahí está la fuente predeterminada.'],
    ['Elige Arial y tamaño 12 y da Aceptar', 'Guarda el cambio.'],
    ['Cierra y vuelve a abrir Excel', 'El cambio se aplica al reiniciar.'],
], 'Archivo → Opciones → General.')
b_end = c.mark() - 1

# ───────────────────────── C · Diseño de página ─────────────────────────
c0 = c.mark()
c.L('📄', 'Márgenes, orientación y tamaño', 'Bloque C · Diseño de la hoja de cálculo', body(
    bk('Márgenes', 'El espacio en blanco alrededor de la hoja. En <b>Disposición de página › Márgenes</b>: Normales, Anchos o Estrechos. Con estrechos cabe más.'),
    bk('Orientación', '<b>Vertical</b> para listas largas y con pocas columnas; <b>horizontal</b> para tablas anchas, con muchas columnas.'),
    bk('Tamaño', 'El papel: <b>Carta</b> (21.6 × 27.9 cm), el más usado en México, u <b>Oficio</b> (21.6 × 35.6 cm), más largo.'),
    ana('Piensa en…', 'Una foto de grupo: si salen muchos a lo ancho, volteas el celular a horizontal.'),
    ex('En la cafetería', 'La tabla de ventas tiene 7 columnas y no cabe a lo ancho en vertical: se imprime en horizontal con márgenes estrechos.')),
    'Tabla ancha → horizontal · Lista larga → vertical.')
c.L('🔖', 'Encabezado y pie de página', 'Bloque C · Datos que se repiten en cada hoja impresa', body(
    sp('En palabras sencillas', 'El <b>encabezado</b> va arriba y el <b>pie de página</b> abajo, fuera de las celdas, y se repiten en cada hoja impresa.'),
    bk('Cómo', '<b>Insertar › Encabezado y pie de página</b>. Excel cambia a la vista Diseño de página y muestra tres secciones: izquierda, centro y derecha.'),
    bk('Elementos automáticos', '<b>Número de página</b> (&amp;[Página]), número de páginas, fecha, hora, nombre del archivo o de la hoja e imágenes (como un logotipo).'),
    ex('En la cafetería', 'Encabezado: «Cafetería La Escuelita · Ventas de octubre». Pie: «Elaboró: Lupita Hernández · Página 1 de 2».'),
    warn('Recuerda', 'Para volver a la vista de siempre: <b>Vista › Normal</b>.')),
    'Arriba quién y qué; abajo quién lo hizo y la página.')
c.L('🖨️', 'Fondo, área de impresión y vista preliminar', 'Bloque C · Antes de imprimir', body(
    bk('Fondo', '<b>Disposición de página › Fondo</b> pone una imagen detrás de las celdas. Se ve en pantalla, pero <b>no se imprime</b>. Para color impreso usa el relleno de celda.'),
    bk('Vista preliminar', '<b>Archivo › Imprimir</b> (Ctrl + P) muestra cómo saldrá cada hoja. Revisa siempre antes de gastar papel.'),
    bk('Ajustar a una página', 'En la configuración de impresión elige <b>«Ajustar hoja en una página»</b> o «Ajustar todas las columnas en una página» si la tabla se pasa un poco.'),
    bk('Área de impresión', 'Selecciona solo lo que quieres imprimir y usa <b>Disposición de página › Área de impresión › Establecer</b>.'),
    warn('Ojo', 'Las líneas grises de cuadrícula tampoco se imprimen: si quieres líneas en papel, pon <b>bordes</b>.')),
    'Revisa la vista preliminar antes de imprimir.')
c.A('🖨️', '¿Qué configuración conviene?', 'Elige la mejor opción para cada caso.', [
    ['Una tabla con 9 columnas que no cabe a lo ancho', 'Orientación horizontal', 'Lo horizontal da más espacio a lo ancho.'],
    ['A la tabla le sobra solo una columna para caber', 'Ajustar a una página', 'Reduce un poco todo para que quepa.'],
    ['Que cada hoja impresa diga el nombre de la cafetería', 'Encabezado', 'El encabezado se repite en cada página.'],
    ['Que cada hoja diga «Página 1», «Página 2»…', 'Pie de página', 'Se usa el número de página automático.'],
    ['Imprimir solo la tabla de precios y no el resto de la hoja', 'Área de impresión', 'Imprime solo el rango elegido.'],
    ['Saber cuántas hojas saldrán antes de imprimir', 'Vista preliminar', 'Archivo › Imprimir muestra el resultado.'],
], 'Piensa en qué problema resuelve cada herramienta.',
    ['Orientación horizontal', 'Ajustar a una página', 'Encabezado', 'Pie de página', 'Área de impresión', 'Vista preliminar'])
c.Z('📄', 'Completa: preparar la impresión', 'Elige la palabra correcta.',
    '<p>Los márgenes, la orientación y el tamaño están en la ficha {0}.</p>'
    '<p>El fondo de la hoja se ve en pantalla, pero {1}.</p>'
    '<p>Si quieres líneas en la hoja impresa, aplica {2}.</p>'
    '<p>El papel más usado en México es tamaño {3}.</p>'
    '<p>Para ver cómo saldrá la hoja antes de imprimir uso la {4}.</p>',
    [['Disposición de página', ['Disposición de página', 'Inicio', 'Vista']],
     ['no se imprime', ['no se imprime', 'se imprime en color', 'se imprime en gris']],
     ['bordes', ['bordes', 'líneas de cuadrícula', 'zoom']],
     ['Carta', ['Carta', 'Oficio', 'A3']],
     ['vista preliminar', ['vista preliminar', 'barra de estado', 'cinta de opciones']]],
    'Recuerda la lección «Fondo, área de impresión y vista preliminar».')
sim('🖨️', 'Prepara la impresión de las ventas', 'Hoja de cálculo simulada: configura la hoja y la página como en Excel.',
    {'id': 'pag', 'cols': 7, 'rows': len(VENTAS_ROWS), 'data': VENTAS,
     'cw': {'A': 92, 'B': 150, 'C': 78, 'D': 80, 'E': 86, 'F': 100, 'G': 140},
     'intro': 'La tabla de ventas ya tiene formato, pero Doña Lupita necesita imprimirla. Usa las fichas de arriba (como en Excel) y la etiqueta de la hoja de abajo.'},
    [['Cambia el nombre de la hoja a <b>Ventas</b> y ponle color a su etiqueta (clic en la etiqueta «Hoja1»).', 'a.sh.n.trim().toLowerCase()=="ventas"&&!!a.sh.col'],
     ['En la ficha <b>Vista</b>, inmoviliza la fila superior y baja por la lista para comprobarlo.', 'a.vw.frz'],
     ['Abre <b>Archivo</b> para ver la vista preliminar: ¿cabe la tabla a lo ancho?', '!!a.used.prev'],
     ['En <b>Disposición de página</b>, cambia la orientación a <b>Horizontal</b>.', 'a.pg.or=="h"'],
     ['Usa márgenes <b>Estrechos</b>.', 'a.pg.mar=="estrechos"'],
     ['En <b>Insertar</b>, escribe en el encabezado: <b>Cafetería La Escuelita</b>.', '/escuelita/i.test(a.pg.hd)'],
     ['Pon en el pie de página tu nombre y el <b>número de página</b>.', '/&\\[p[aá]gina\\]/i.test(a.pg.ft)&&a.pg.ft.replace(/&\\[[^\\]]*\\]/g,"").replace(/p[aá]gina|·/gi,"").trim().length>=3'],
     ['Revisa otra vez la vista preliminar: la tabla debe caber en una sola hoja.', '!!a.used.prev&&a.fits()']],
    'Las fichas funcionan como en Excel. «Archivo» abre y cierra la vista preliminar.')
c_end = c.mark() - 1

# ───────────────────────── D · Formato de celda, fila y columna ─────────────────────────
d0 = c.mark()
c.L('🔠', 'Fuente, tamaño y color', 'Bloque D · Estilos de la letra', body(
    bk('Dónde', '<b>Inicio › Fuente</b>: tipo de letra, tamaño, negrita (Ctrl + N), cursiva (Ctrl + K), subrayado, color de fuente y color de relleno.'),
    bk('Regla de oro', 'Máximo <b>dos fuentes</b> en un libro, títulos más grandes que los datos y colores que contrasten (letra oscura en fondo claro o letra blanca en fondo oscuro).'),
    bk('Agregar fuentes', 'Descarga una fuente gratuita (por ejemplo de <b>fonts.google.com</b>), abre el archivo <b>.ttf</b> u <b>.otf</b> y da clic en <b>Instalar</b>. Cierra y abre Excel: ya aparece en la lista.'),
    ex('En la cafetería', 'Título en tamaño 16 y negrita; encabezados en negrita con letra blanca sobre azul; datos en tamaño 11.'),
    warn('Ojo', 'Si envías el archivo a otra computadora que no tiene tu fuente instalada, Excel la cambia por otra.')),
    'Pocas fuentes, buen tamaño y buen contraste.')
c.L('↔️', 'Alineación, ajustar texto e interlineado', 'Bloque D · Acomodar el contenido de la celda', body(
    bk('Alineación horizontal', 'Izquierda, centro o derecha. Por costumbre: textos a la izquierda, números a la derecha, encabezados centrados.'),
    bk('Alineación vertical', 'Arriba, en medio o abajo de la celda; se nota cuando la fila es alta.'),
    bk('Ajustar texto', 'Un texto largo se acomoda en varias líneas dentro de la misma celda. Para cortar la línea donde tú quieras: <b>Alt + Enter</b>.'),
    bk('«Interlineado» en Excel', 'Excel no tiene interlineado como Word: el espacio entre líneas se controla con el <b>alto de la fila</b> y la alineación vertical (en Formato de celdas › Alineación › Vertical › <b>Justificar</b> se reparten las líneas en toda la altura).'),
    bk('Combinar y centrar', 'Une varias celdas en una y centra el contenido. Ideal para el <b>título</b> que va sobre toda la tabla.')),
    'Textos a la izquierda, números a la derecha, títulos centrados.')
c.L('📏', 'Ancho de columna y alto de fila', 'Bloque D · Que todo se vea completo', body(
    bk('Ajustar a mano', 'Arrastra el borde entre dos letras de columna (o entre dos números de fila).'),
    bk('Autoajustar', '<b>Doble clic</b> en ese borde, o <b>Inicio › Formato › Autoajustar ancho de columna</b>: la columna toma el ancho del dato más largo.'),
    bk('¿Y los ####?', 'Si una celda muestra <b>#####</b>, el número no cabe: ensancha la columna. El dato no se perdió.'),
    ana('Piensa en…', 'Un cajón donde no cierra la caja: no la tiras, buscas un cajón más ancho.'),
    ex('En la cafetería', 'Al poner formato Moneda, $1,250.00 ya no cabía y salía ####. Con doble clic en el borde de la columna se arregló.')),
    '##### = la columna es angosta, no un error del dato.')
c.L('🎨', 'Bordes, relleno y estilos de celda', 'Bloque D · Que la tabla se lea fácil', body(
    bk('Bordes', '<b>Inicio › Bordes › Todos los bordes</b> dibuja las líneas de la tabla (las que sí se imprimen).'),
    bk('Color de relleno', 'El cubeta de pintura: color de fondo de la celda. Úsalo en encabezados y totales, no en todo.'),
    bk('Estilos de celda', '<b>Inicio › Estilos de celda</b> aplica en un clic un formato completo: Título, Encabezado, Bueno, Neutral, Malo…'),
    bk('Dar formato como tabla', 'Convierte el rango en una tabla con colores alternos y filtros.'),
    ex('En la cafetería', 'Encabezados con estilo «Encabezado», toda la tabla con bordes y los productos con descuento en verde claro.')),
    'Bordes para ordenar, relleno para resaltar.')
c.L('💲', 'Formato de número', 'Bloque D · El mismo dato, otra presentación', body(
    sp('En palabras sencillas', 'El formato de número cambia <b>cómo se ve</b> un valor, pero <b>no cambia el valor</b> con el que Excel hace cuentas. Está en <b>Inicio › Número</b> (o Ctrl + 1).'),
    bk('Moneda', '1250 → <b>$1,250.00</b>'),
    bk('Porcentaje', '0.16 → <b>16%</b> (Excel multiplica por 100 solo para mostrarlo).'),
    bk('Fecha', 'Excel guarda las fechas como un número de días: 46318 → <b>23/10/2026</b>. Si ves un número raro en lugar de una fecha, aplica formato Fecha.'),
    bk('Número', '1250 → <b>1,250.00</b>, con decimales y separador de miles.'),
    ex('Compruébalo', 'Selecciona una celda con 16%: en la barra de fórmulas verás <b>0.16</b>.')),
    'El formato cambia la vista, no el dato.')
c.A('💲', '¿Qué formato de número?', 'Elige el formato para cada columna de la cafetería.', [
    ['El precio de cada producto', 'Moneda', 'Son pesos: $35.00.'],
    ['El descuento de 0.05', 'Porcentaje', '0.05 se ve como 5%.'],
    ['La columna dice 46318 y debería ser el día de compra', 'Fecha', '46318 es el 23/10/2026 guardado como número.'],
    ['El peso de la fruta en kilos con dos decimales: 2.50', 'Número', 'No es dinero ni porcentaje: número con decimales.'],
    ['El total vendido en el día', 'Moneda', 'Es dinero.'],
], 'Dinero → Moneda · Parte de 100 → Porcentaje · Día → Fecha.', ['Moneda', 'Porcentaje', 'Fecha', 'Número'])
c.A('👀', '¿Qué se verá en la celda?', 'El valor real está a la izquierda. ¿Qué muestra la celda con ese formato?', [
    ['0.25 con formato Porcentaje', '25%', 'Se multiplica por 100 para mostrarlo.'],
    ['80 con formato Moneda', '$80.00', 'Agrega el signo de pesos y dos decimales.'],
    ['46316 con formato Fecha corta', '21/10/2026', 'Dos días antes de 46318 (23/10/2026).'],
    ['1.5 con formato Porcentaje', '150%', '1.5 × 100 = 150.'],
    ['Un número que no cabe en la columna', '#####', 'Hay que ensanchar la columna.'],
], 'El formato no cambia el valor, solo cómo se muestra.', ['25%', '$80.00', '21/10/2026', '150%', '#####'])
c.A('🧰', '¿Qué herramienta lo resuelve?', 'Doña Lupita tiene estos problemas. Elige la herramienta.', [
    ['La celda muestra ##### en lugar del total', 'Autoajustar ancho de columna', 'La columna es angosta.'],
    ['«Agua natural 600 ml» se ve cortado y la columna no debe crecer', 'Ajustar texto', 'Pasa el texto a varias líneas.'],
    ['El título debe quedar centrado sobre las 7 columnas', 'Combinar y centrar', 'Une A1:G1 y centra.'],
    ['En papel no se ven las líneas de la tabla', 'Bordes', 'La cuadrícula no se imprime; los bordes sí.'],
    ['Los encabezados no se distinguen de los datos', 'Estilo de celda «Encabezado»', 'Aplica negrita, relleno y centrado de un clic.'],
], 'Lee el problema y piensa qué cambia: ancho, líneas, unión o estilo.',
    ['Autoajustar ancho de columna', 'Ajustar texto', 'Combinar y centrar', 'Bordes', 'Estilo de celda «Encabezado»'])
sim('🎨', 'Da formato al inventario', 'Hoja de cálculo simulada: aplica el formato como en Excel.',
    {'id': 'fmt', 'cols': 7, 'rows': 8, 'data': INVENTARIO,
     'intro': 'Este es el inventario de la cafetería, sin formato. Selecciona celdas con clic y arrastre, o escribe el rango en el <b>cuadro de nombres</b> (por ejemplo <b>A2:G2</b>) y pulsa Enter. Después usa la ficha <b>Inicio</b>.'},
    [['Combina y centra el título en <b>A1:G1</b>.', 'a.mg("A1:G1")'],
     ['Pon el título en <b>negrita</b> y tamaño <b>16</b> o más.', 'a.c("A1").b&&(a.c("A1").sz||11)>=16'],
     ['Encabezados <b>A2:G2</b>: negrita, color de relleno y centrados (o usa el estilo «Encabezado»).', 'a.all("A2:G2",function(x){return x.b&&x.fill&&x.al=="c"})'],
     ['Formato <b>Moneda</b> en Precio y Total (<b>C3:D8</b>).', 'a.all("C3:D8",function(x){return x.nf=="mon"})'],
     ['Formato <b>Porcentaje</b> en Descuento (<b>E3:E8</b>).', 'a.all("E3:E8",function(x){return x.nf=="por"})'],
     ['Formato <b>Fecha corta</b> en <b>F3:F8</b> (hoy se ven números como 46318).', 'a.all("F3:F8",function(x){return x.nf=="fec"})'],
     ['<b>Todos los bordes</b> en la tabla <b>A2:G8</b>.', 'a.all("A2:G8",function(x){return x.bd})'],
     ['Autoajusta el ancho de las columnas <b>A a G</b> para que nada se corte.', 'a.fitcols("ABCDEFG")']],
    'Autoajusta al final: si cambias un formato después, la columna puede volver a quedar angosta.')
c.O('🪜', 'Ordena: dar formato a una tabla', 'Ordena los pasos que conviene seguir para que la tabla quede bien.', [
    ['Escribir y revisar los datos', 'Primero el contenido, después el formato.'],
    ['Combinar y centrar el título', 'El título va sobre toda la tabla.'],
    ['Dar estilo a los encabezados y formato de número a los datos', 'Encabezados y números con su formato.'],
    ['Aplicar bordes a la tabla', 'Las líneas que sí se imprimen.'],
    ['Autoajustar el ancho de las columnas', 'Al final, para que nada se corte.'],
], 'Contenido → título → encabezados y números → bordes → ancho.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Libro de trabajo', 'Archivo de Excel (.xlsx) con una o varias hojas.'),
    bk('Celda / referencia', 'Cruce de columna y fila; se nombra como C3.'),
    bk('Rango', 'Grupo de celdas: A2:G8.'),
    bk('Cinta de opciones', 'Barra con las fichas de herramientas.'),
    bk('Cuadro de nombres', 'Muestra o elige la celda activa.'),
    bk('Barra de fórmulas', 'Muestra el contenido real de la celda.'),
    bk('Inmovilizar paneles', 'Deja fijas filas o columnas al desplazarte.'),
    bk('Orientación', 'Vertical u horizontal.'),
    bk('Encabezado / pie de página', 'Texto que se repite arriba o abajo de cada hoja impresa.'),
    bk('Formato de número', 'Cómo se muestra un valor: moneda, porcentaje, fecha…'),
    bk('Autoajustar', 'Dar a la columna el ancho de su dato más largo.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311: martes 17:20-19:50, miércoles 18:10-19:50 y laboratorio el viernes 15:20-18:10. El viernes 30-oct es CTEC, así que las prácticas tienen versión para celular (Excel o Hojas de cálculo de Google) y los dos simuladores funcionan sin computadora.', 'sp'),
    bk('Bloque A · viernes 23 y martes 27-oct', 'Viernes 23 (laboratorio, después de la A.E. 2.2): partes de la ventana y referencias. Martes 27: fichas de la cinta y <b>Práctica 1</b> (pueden traerla de tarea si no hay equipo).'),
    bk('Bloque B · martes 27-oct', 'Vista, barra de acceso rápido, fuente predeterminada y manejo de hojas.'),
    bk('Bloque C · miércoles 28-oct', 'Márgenes, orientación, tamaño, encabezado y pie, fondo y vista preliminar. Simulador «Prepara la impresión» y <b>Práctica 2</b>.'),
    bk('Bloque D y evaluación · martes 3-nov', 'Formato de celda, fila y columna; simulador «Da formato al inventario» y <b>Práctica 3</b>. Cierre con la A.E. 3.1: libro digital en la plataforma y versión impresa.'),
    bk('Nota', 'La actividad de evaluación se desbloquea al completar este material. En este R.A. no se piden fórmulas; los totales de los ejemplos ya vienen calculados.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '☕', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '📗', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '⚙️', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🖨️', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '🎨', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"☕",t:"Empieza aquí",d:"Para qué sirve una hoja de cálculo y qué vas a entregar.",time:"15 min",obj:["Distinguir cuándo usar una hoja de cálculo","Conocer el caso y la evidencia final"],sum:["Word = textos · Excel = datos en filas y columnas.","Entregas un libro con formato, digital e impreso."],q:"¿Qué datos de tu casa o tu escuela podrías organizar en una hoja de cálculo?"},
a:{k:"Bloque A",l:"A",ic:"📗",t:"Elementos del libro de trabajo",d:"Libro, hoja, celda, barras y fichas.",time:"90 min",obj:["Nombrar las partes de la ventana de Excel","Escribir referencias de celdas y rangos","Ubicar cada herramienta en su ficha"],sum:["Libro = archivo · Hoja = pestaña · Celda = C3 · Rango = A2:G8.","Cuadro de nombres = dónde estoy · Barra de fórmulas = qué hay realmente.","Inicio, Insertar, Disposición de página, Vista y Archivo."],q:"¿En qué se parece la referencia de una celda a jugar Batalla naval?"},
b:{k:"Bloque B",l:"B",ic:"⚙️",t:"Opciones de la hoja de cálculo",d:"Área de trabajo, barra de herramientas y hojas.",time:"60 min",obj:["Usar zoom, cuadrícula e inmovilizar paneles","Personalizar la barra de acceso rápido y la fuente predeterminada","Insertar, renombrar y colorear hojas"],sum:["Inmovilizar fila superior mantiene los encabezados.","Archivo › Opciones › General define la fuente de los libros nuevos.","Una hoja por tema, con nombre y color."],q:"¿Qué botón agregarías a tu barra de acceso rápido y por qué?",rev:[["La celda de la columna D y la fila 7 es…",["D7","7D","D-7"],0,"Primero la letra, luego el número."],["La barra de fórmulas muestra…",["El contenido real de la celda","El nombre del libro","La suma de lo seleccionado"],0,"Por eso ahí ves 0.16 aunque la celda diga 16%."]]},
c:{k:"Bloque C",l:"C",ic:"🖨️",t:"Diseño de la hoja de cálculo",d:"Márgenes, orientación, tamaño, encabezado, pie y fondo.",time:"100 min",obj:["Configurar márgenes, orientación y tamaño","Agregar encabezado y pie de página con elementos automáticos","Revisar la vista preliminar y ajustar a una página"],sum:["Tabla ancha → horizontal y márgenes estrechos.","El encabezado y el pie se repiten en cada hoja impresa.","El fondo y la cuadrícula no se imprimen; los bordes sí."],q:"¿Por qué conviene revisar la vista preliminar antes de imprimir?",rev:[["Para que los encabezados no se muevan al bajar se usa…",["Inmovilizar fila superior","Combinar y centrar","Zoom"],0,"Está en la ficha Vista."],["La fuente predeterminada se cambia en…",["Archivo › Opciones › General","Inicio › Fuente","Vista › Zoom"],0,"Se aplica a los libros nuevos."]]},
d:{k:"Bloque D",l:"D",ic:"🎨",t:"Formato de celda, fila y columna",d:"Fuente, alineación, ancho, bordes, estilos y formato de número.",time:"120 min",obj:["Aplicar fuente, tamaño, color y alineación","Ajustar ancho de columna y combinar celdas","Aplicar formato de número sin cambiar el valor"],sum:["Pocas fuentes, títulos grandes y buen contraste.","##### = columna angosta; doble clic para autoajustar.","Moneda, porcentaje y fecha cambian la vista, no el dato."],q:"¿Qué pasaría si escribes los precios con el signo $ en lugar de usar formato Moneda?",rev:[["Una tabla de 9 columnas se imprime mejor en…",["Horizontal","Vertical","Oficio vertical"],0,"Da más espacio a lo ancho."],["Para tener líneas en la hoja impresa se usan…",["Bordes","Líneas de cuadrícula","Fondo"],0,"La cuadrícula y el fondo no se imprimen."]]}
'''

ILL = r'''
ILL["Libro, hoja y celda"]=function(){var o='',L="ABCDE";for(var i=0;i<5;i++)o+=R_(40+i*56,8,56,20,"s",0)+T_(68+i*56,22,L[i],"tm");for(var r=0;r<4;r++){o+=R_(10,28+r*22,30,22,"s",0)+T_(25,43+r*22,String(r+1),"tm");for(i=0;i<5;i++)o+=R_(40+i*56,28+r*22,56,22,(i==2&&r==2)?"b":(r>=1&&r<=3&&i<=1?"g":"s"),0)}o+=T_(180,87,"C3","tw")+T_(96,134,"Rango A2:B4","tm")+T_(220,134,"Celda C3 = columna C + fila 3","tm");return SV(340,142,o,"Columnas, filas, celda y rango")};
ILL["Las partes de la ventana"]=function(){var b=[["Barra de título · Cafeteria.xlsx","b"],["Barra de acceso rápido · Cinta de opciones (fichas)","g"],["Cuadro de nombres  ·  fx Barra de fórmulas","s"],["Área de celdas","s"],["Etiquetas de hojas  ·  Barra de estado","s"]],y=6,o='';b.forEach(function(x,i){var h=i==3?44:22;o+=R_(10,y,320,h,x[1],4)+T_(170,y+h/2+5,x[0],x[1]=="s"?"t":"tw");y+=h+4});return SV(340,y+4,o,"Partes de la ventana de Excel")};
ILL["Las fichas de la cinta de opciones"]=function(){return grid3([["🏠","Inicio|formato"],["➕","Insertar|encabezado"],["📄","Disposición|de página"],["👁️","Vista|inmovilizar"],["🖨️","Archivo|imprimir"],["⚙️","Opciones|de Excel"]],"Fichas de la cinta")};
ILL["El área de trabajo: ficha Vista"]=function(){return grid3([["🔍","Zoom"],["▦","Líneas de|cuadrícula"],["📌","Inmovilizar|paneles"]],"Opciones de la ficha Vista")};
ILL["Trabaja con las hojas"]=function(){var t=[["Inventario","g"],["Ventas","b"],["Precios","a"]],o=R_(10,10,320,50,"s",4)+T_(170,40,"Área de celdas","tm");t.forEach(function(x,i){o+=R_(14+i*92,64,88,26,x[1],4)+T_(58+i*92,82,x[0],x[1]=="a"?"td":"tw")});o+=R_(292,64,30,26,"s",4)+T_(307,82,"+","t");return SV(340,100,o,"Etiquetas de hojas con nombre y color")};
ILL["Márgenes, orientación y tamaño"]=function(){return SV(340,140,R_(40,10,84,108,"s",4)+R_(50,22,64,84,"b",0)+T_(82,68,"Vertical","tw")+T_(82,134,"listas largas","tm")+R_(170,30,140,84,"s",4)+R_(180,40,120,64,"g",0)+T_(240,76,"Horizontal","tw")+T_(240,134,"tablas anchas","tm"),"Orientación y márgenes")};
ILL["Encabezado y pie de página"]=function(){return SV(340,150,R_(90,6,160,138,"s",4)+R_(100,12,140,18,"b",3)+T_(170,25,"Cafetería La Escuelita","tw")+R_(104,38,132,76,"s",0)+T_(170,80,"Tabla de ventas","tm")+R_(100,120,140,18,"g",3)+T_(170,133,"Lupita · Página 1","tw"),"Encabezado arriba y pie abajo")};
ILL["Formato de número"]=function(){var r=[["0.16","Porcentaje","16%"],["1250","Moneda","$1,250.00"],["46318","Fecha","23/10/2026"]],o=T_(60,16,"Valor real","tm")+T_(170,16,"Formato","tm")+T_(280,16,"Se ve","tm");r.forEach(function(x,i){var y=24+i*34;o+=R_(20,y,80,26,"s",4)+T_(60,y+18,x[0],"t")+T_(170,y+18,x[1]+" →","tm")+R_(230,y,100,26,"g",4)+T_(280,y+18,x[2],"tw")});return SV(340,128,o,"El formato cambia la vista, no el valor")};
ILL["Ancho de columna y alto de fila"]=function(){return SV(340,100,R_(30,30,70,28,"r",0)+T_(65,49,"#####","tw")+T_(65,78,"columna angosta","tm")+T_(150,49,"doble clic →","tm")+R_(200,30,110,28,"g",0)+T_(255,49,"$1,250.00","tw")+T_(255,78,"autoajustada","tm"),"##### se arregla ensanchando la columna")};
ILL["Bordes, relleno y estilos de celda"]=function(){var o='',w=[100,60,70];for(var r=0;r<4;r++){var x=40;for(var i=0;i<3;i++){o+=R_(x,10+r*24,w[i],24,r==0?"b":(r==3?"a":"s"),0);x+=w[i]}}o+=T_(90,27,"Producto","tw")+T_(170,27,"Cant.","tw")+T_(235,27,"Total","tw")+T_(90,99,"Total","td")+T_(235,99,"$2,908.00","td");return SV(340,116,o,"Encabezado con relleno, bordes y fila de total")};
'''

EXH = r'''
function xw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><div style="background:#fff;color:#111;padding:8px;font:13px system-ui;overflow-x:auto">'+b+'</div></div>'}
function xt_(rows,hd){return '<table style="border-collapse:collapse;font:12.5px system-ui">'+rows.map(function(r,i){return '<tr>'+r.map(function(c){return '<td style="border:1px solid '+(hd?'#111':'#e5e7eb')+';padding:3px 8px;'+(i==0&&hd?'background:#1e3a8a;color:#fff;font-weight:700;text-align:center':'')+'">'+c+'</td>'}).join("")+'</tr>'}).join("")+'</table>'}
EXH.ventana=function(){return exw(xw_('Excel · Cafeteria.xlsx','<div style="background:#217346;color:#fff;padding:4px 8px;border-radius:4px">💾 ↶ ↷ '+mk(1)+' &nbsp; Archivo · Inicio · Insertar · Disposición de página · Vista '+mk(2)+'</div><div style="display:flex;gap:6px;margin:6px 0"><span style="border:1px solid #ccc;padding:2px 8px">A3</span>'+mk(3)+'<span style="border:1px solid #ccc;padding:2px 8px;flex:1">fx Torta de jamón</span>'+mk(4)+'</div>'+xt_([["","A","B"],["1","Producto","Cantidad"],["2","Torta de jamón","20"]])+'<div style="margin-top:6px;background:#f3f4f6;padding:3px 8px">Inventario | Ventas | + '+mk(5)+' &nbsp;&nbsp; Suma: 20 '+mk(6)+'</div>'),['Barra de acceso rápido.','Cinta de opciones con sus fichas.','Cuadro de nombres.','Barra de fórmulas.','Etiquetas de hojas.','Barra de estado.'])};
EXH.hojas=function(){return exw(xw_('Etiquetas de hojas','<span style="border-bottom:4px solid #16a34a;padding:3px 10px;background:#f3f4f6">Inventario</span> <span style="border-bottom:4px solid #2563eb;padding:3px 10px;background:#f3f4f6">Ventas</span> <span style="border-bottom:4px solid #f59e0b;padding:3px 10px;background:#f3f4f6">Precios</span> '+mk(1)+' <span style="padding:3px 8px">+</span>'),['Tres hojas con nombre claro y color de pestaña (clic derecho › Color de pestaña).'])};
EXH.opciones=function(){return exw(xw_('Opciones de Excel › General','<b>Al crear nuevos libros</b> '+mk(1)+'<br>Usar esta fuente: <u>Arial</u><br>Tamaño de fuente: <u>12</u><br>Incluir este número de hojas: <u>3</u><br><span style="float:right;border:1px solid #999;padding:2px 10px">Aceptar</span><br>'),['Cambia la fuente, el tamaño y el número de hojas; reinicia Excel.'])};
EXH.acceso=function(){return exw(xw_('Barra de herramientas de acceso rápido','💾 ↶ ↷ 🖨️ '+mk(1)+' ▾ '+mk(2)),['El botón nuevo: Vista previa de impresión e imprimir.','La flechita para personalizar la barra.'])};
EXH.inmov=function(){return exw(xw_('Vista › Inmovilizar','Inmovilizar paneles<br><b>Inmovilizar fila superior</b> '+mk(1)+'<br>Inmovilizar primera columna'),['Baja con la rueda del ratón: la fila 1 se queda fija.'])};
EXH.datos=function(){return exw(xw_('Hoja «Ventas»',xt_([["Fecha","Producto","Cantidad","Precio","Total","Vendió","Forma de pago"],["19/10/2026","Torta de jamón","12","$35.00","$420.00","Lupita","Efectivo"],["19/10/2026","Agua natural 600 ml","25","$12.00","$300.00","Lupita","Efectivo"],["…","…","…","…","…","…","…"]],true)),['Mínimo 12 renglones de datos y 6 columnas.'])};
EXH.pagina=function(){return exw(xw_('Disposición de página','Márgenes: <b>Estrechos</b> '+mk(1)+' · Orientación: <b>Horizontal</b> '+mk(2)+' · Tamaño: <b>Carta</b> '+mk(3)),['Márgenes estrechos.','Horizontal porque la tabla es ancha.','Carta, el papel más común.'])};
EXH.encabezado=function(){return exw(xw_('Vista Diseño de página','<div style="display:flex;justify-content:space-between;border-bottom:1px dashed #999;padding-bottom:4px"><span></span><b>Cafetería La Escuelita · Ventas</b>'+mk(1)+'<span>&amp;[Fecha]</span></div><div style="height:40px;color:#999;text-align:center;padding-top:10px">(tabla)</div><div style="display:flex;justify-content:space-between;border-top:1px dashed #999;padding-top:4px"><span>Elaboró: Ana Pérez · 311</span><span>Página &amp;[Página] de &amp;[Páginas]</span>'+mk(2)+'</div>'),['Encabezado al centro con el nombre del negocio.','Pie con tu nombre, grupo y número de página.'])};
EXH.preliminar=function(){return exw(xw_('Archivo › Imprimir','<div style="display:flex;gap:12px;align-items:flex-start"><div style="width:120px;height:90px;border:1px solid #999;box-shadow:0 1px 4px #0003;padding:6px;font-size:8px">Cafetería La Escuelita<br>▦▦▦▦▦▦▦<br>▦▦▦▦▦▦▦</div><div>Configuración '+mk(1)+'<br>Orientación horizontal<br>Carta<br>Márgenes estrechos<br><b>Ajustar hoja en una página</b> '+mk(2)+'<br>Página 1 de 1 '+mk(3)+'</div></div>'),['Revisa la configuración.','Usa «Ajustar» solo si le falta poco.','Debe salir en una sola página.'])};
EXH.formato=function(){return exw(xw_('Hoja «Inventario» con formato','<div style="text-align:center;font-weight:700;font-size:16px;border:1px solid #111;padding:3px">Cafetería La Escuelita · Inventario de la semana</div>'+xt_([["Producto","Cantidad","Precio","Total","Descuento","Fecha de compra"],["Torta de jamón","20","$35.00","$700.00","0%","23/10/2026"],["Agua natural 600 ml","48","$12.00","$576.00","5%","21/10/2026"]],true)),['Título combinado, encabezados con estilo, moneda, porcentaje, fecha y bordes.'])};
EXH.cel=function(){return exw(mp('Hojas de cálculo · celular','<div class="mbox">✏️ Toca la celda › ícono <b>A</b> (formato) '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Texto: negrita, tamaño, color · Celda: relleno, bordes, combinar '+mk(2)+'</div><div class="mbox" style="margin-top:6px">⋮ › Imprimir o Compartir y exportar › PDF '+mk(3)+'</div>'),['El botón de formato de la app.','Las mismas opciones que en Excel, en dos pestañas.','Para la vista preliminar y el PDF.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Conoce y organiza tu libro de trabajo',
     'prog': 'Bloques A y B · Elementos del libro y opciones de la hoja',
     'min': 50, 'lug': 'Martes 27-oct en clase, laboratorio o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con Excel', 'Documento o carpeta para tus capturas'],
                'steps': [
                    ['Abre Excel, toma una captura de la ventana y señala (con números o flechas) sus 6 partes: acceso rápido, cinta, cuadro de nombres, barra de fórmulas, etiquetas y barra de estado.', 'ventana'],
                    ['Crea el libro <b>Apellido_Nombre_EDOA31.xlsx</b> con tres hojas: Inventario, Ventas y Precios, cada una con color de pestaña.', 'hojas'],
                    ['Agrega a la barra de acceso rápido el botón <b>Vista previa de impresión e imprimir</b>.', 'acceso'],
                    ['En Archivo › Opciones › General cambia la fuente predeterminada y toma captura (después puedes regresarla).', 'opciones'],
                    ['Escribe en la hoja Ventas al menos 12 renglones con 6 columnas (fecha, producto, cantidad, precio, total, forma de pago) e inmoviliza la fila superior.', 'inmov']]},
         'cel': {'mat': ['Celular con Excel o Hojas de cálculo de Google', 'Galería o notas para tus capturas'],
                 'steps': [
                     ['Abre la app, toma una captura y anota qué parte es el cuadro de celda, la barra de fórmulas y las pestañas de hojas.', 'cel'],
                     ['Crea el libro <b>Apellido_Nombre_EDOA31</b> con tres hojas: Inventario, Ventas y Precios, con color de pestaña (mantén presionada la pestaña).', 'hojas'],
                     ['Escribe en la hoja Ventas al menos 12 renglones con 6 columnas (fecha, producto, cantidad, precio, total, forma de pago).', 'datos'],
                     ['Inmoviliza la fila 1 (mantén presionado el número de fila › Inmovilizar) y toma captura.', 'inmov'],
                     'Escribe en tus notas para qué sirve el cuadro de nombres y para qué la barra de fórmulas.']}},
     'entrega': ['Tu libro con las tres hojas y las capturas; lo sigues usando en las prácticas 2 y 3.'],
     'rub': [['Partes de la ventana identificadas', 25], ['Tres hojas con nombre y color', 25], ['Barra de acceso rápido o fuente predeterminada', 20], ['Datos capturados e inmovilizados', 30]]},
    {'id': 'pr2', 'n': 2, 't': 'Prepara tu hoja para imprimir',
     'prog': 'Bloque C · Diseño de la hoja de cálculo',
     'min': 50, 'lug': 'Miércoles 28-oct en clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu libro de la práctica 1', 'Computadora con Excel'],
                'steps': [
                    'Antes de empezar, termina el simulador «Prepara la impresión de las ventas» de este material.',
                    ['En la hoja Ventas elige márgenes, orientación y tamaño adecuados para tu tabla.', 'pagina'],
                    ['Agrega encabezado con el nombre del negocio y pie de página con tu nombre, grupo, fecha y número de página.', 'encabezado'],
                    ['Revisa la vista preliminar (Ctrl + P). Si no cabe, ajusta orientación, márgenes o «Ajustar hoja en una página».', 'preliminar'],
                    'Guarda una captura de la vista preliminar y escribe en una celda por qué elegiste esa orientación.']},
         'cel': {'mat': ['Tu libro de la práctica 1', 'Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Prepara la impresión de las ventas» de este material.',
                     ['Abre ⋮ › Imprimir (o Diseño de página) y elige orientación, tamaño Carta y márgenes.', 'cel'],
                     ['Agrega encabezado y pie de página (en Google: Imprimir › Encabezados y pies de página; en Excel móvil: Diseño de página).', 'encabezado'],
                     ['Revisa la vista previa y ajusta para que la tabla quepa a lo ancho.', 'preliminar'],
                     'Toma captura de la vista previa y escribe por qué elegiste esa orientación.']}},
     'entrega': ['Captura de la vista preliminar y el libro guardado.'],
     'rub': [['Márgenes, orientación y tamaño adecuados', 30], ['Encabezado con datos del negocio', 20], ['Pie con nombre y número de página', 25], ['La tabla cabe en la hoja', 25]]},
    {'id': 'pr3', 'n': 3, 't': 'Da formato profesional a tu inventario',
     'prog': 'Bloque D · Formato en celda, fila y columna',
     'min': 70, 'lug': 'Martes 3-nov en clase, o antes en casa',
     'modes': {
         'pc': {'mat': ['Tu libro de las prácticas 1 y 2', 'Computadora con Excel'],
                'steps': [
                    'Antes de empezar, termina el simulador «Da formato al inventario» de este material.',
                    'En la hoja Inventario escribe al menos 8 productos con: producto, cantidad, precio, total, descuento (0.05, 0.1…) y fecha de compra.',
                    ['Título combinado y centrado, en negrita y tamaño 16; encabezados con estilo de celda o relleno, negrita y centrados.', 'formato'],
                    'Aplica Moneda a precios y totales, Porcentaje a descuentos y Fecha corta a las fechas.',
                    'Aplica todos los bordes, ajusta texto donde haga falta y autoajusta el ancho de las columnas (sin #####).']},
         'cel': {'mat': ['Tu libro de las prácticas 1 y 2', 'Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Da formato al inventario» de este material.',
                     'En la hoja Inventario escribe al menos 8 productos con: producto, cantidad, precio, total, descuento y fecha de compra.',
                     ['Con el botón de formato (A) combina el título, ponlo en negrita y tamaño 16, y da relleno y negrita a los encabezados.', 'cel'],
                     'Aplica formato de número: Moneda, Porcentaje y Fecha (botón 123 o Formato › Número).',
                     'Aplica bordes y ajusta el ancho de las columnas para que nada se corte.']}},
     'entrega': ['El libro terminado: es la base de tu actividad de evaluación.'],
     'rub': [['Título y encabezados con formato', 25], ['Formato de número correcto', 30], ['Bordes y alineación', 20], ['Columnas sin texto cortado ni #####', 25]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 3',
    'ra': 'R.A. 3.1', 'title': 'Libro de trabajo con formato',
    'data': [
        ('Resultado de aprendizaje', 'Aplica formato al libro y hoja de cálculo estableciendo opciones disponibles y de estilo de la aplicación acorde al diseño requerido por el usuario.'),
        ('Actividad de evaluación', '3.1.1 Da formato a una hoja de cálculo que cumpla con: márgenes, orientación, tamaño, fondo, encabezado, pie de página, y formato de celda, fila y columna.'),
        ('Evidencia', 'Libro de trabajo digital e impreso'),
        ('Ponderación', '5% (según el programa)'),
        ('Entrega', 'Martes 3 de noviembre: archivo en la plataforma y versión impresa en clase'),
    ],
    'situation': 'Un negocio o grupo de tu comunidad (la cafetería, la tienda de tu colonia, los gastos de tu grupo o el inventario de tu casa) necesita sus datos en orden. Entrega el <b>libro de trabajo</b> de tus tres prácticas, con al menos dos hojas con formato completo y listo para imprimir.',
    'hint': 'Ya hiciste casi todo en las prácticas: revisa esta lista con tu libro abierto y marca cada punto.',
    'steps': [
        ('Libro y hojas', [
            'Archivo <b>Apellido_Nombre_EDOA31.xlsx</b> con al menos dos hojas con nombre y color de pestaña.',
            'Cada hoja con un mínimo de 8 renglones y 6 columnas de datos, y la fila de encabezados inmovilizada.']),
        ('Formato de celda, fila y columna', [
            'Título combinado y centrado, con fuente y tamaño distintos a los datos.',
            'Encabezados con negrita, relleno y alineación centrada (o un estilo de celda).',
            'Formato de número correcto: moneda, porcentaje o fecha según el dato.',
            'Bordes en la tabla y columnas autoajustadas: sin texto cortado ni #####.']),
        ('Diseño de página', [
            'Márgenes, orientación y tamaño adecuados para que cada tabla quepa a lo ancho.',
            'Encabezado con el nombre del negocio o grupo y pie de página con tu nombre, grupo y número de página.',
            'Un fondo de hoja en una de las hojas (recuerda que no se imprime).']),
        ('Entrega', [
            'Revisa la vista preliminar de cada hoja.',
            'Sube tu archivo .xlsx (o su PDF) en la actividad R.A. 3.1 de la plataforma y entrega la versión impresa en clase.']),
    ],
    'rubric': [
        ('Libro con hojas nombradas, coloreadas e inmovilizadas', 15), ('Título y encabezados con formato', 15),
        ('Formato de número correcto', 20), ('Bordes, alineación y columnas autoajustadas', 15),
        ('Márgenes, orientación y tamaño adecuados', 15), ('Encabezado, pie de página y fondo', 15), ('Versión impresa', 5),
    ],
    'deliver': ['Un archivo .xlsx (o PDF) con todas tus hojas.', 'Nombre del archivo: Apellido_Nombre_EDOA31.', 'Súbelo en la actividad R.A. 3.1 de la plataforma y entrega la impresión en clase.'],
}
