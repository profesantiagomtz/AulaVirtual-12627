"""EDOA-20 · R.A. 3.4 · Reportes ejecutivos con tablas dinámicas y protección de la información.

Cierra la Unidad 3 con el caso de la Cafetería La Escuelita: con el registro de ventas por mes, producto y turno
se arman tablas y gráficos dinámicos para la directora, y el libro se protege antes de compartirlo.
Incluye cinco simuladores (pv_sim.js sobre las utilidades de xl3_sim.js).
"""
import random
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-3.4'
CODE_PREFIX = 'EDOA34'
FILE = 'edoa-ra34-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 3.4 · Tablas dinámicas y protección'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 3.4 · Tablas dinámicas y protección'
HERO_KICK = 'EDOA-20 · R.A. 3.4'
HERO_TITLE = 'Del montón de datos al reporte ejecutivo'
HERO_TEXT = 'Resume cientos de ventas en segundos con tablas y gráficos dinámicos, y protege tu libro para que nadie lo descomponga.'
EV_SHORT = 'entrega tu libro con tablas dinámicas y protección.'
EV_CARD = 'Libro de trabajo R.A. 3.4'
RA = 'R.A. 3.4'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores de tablas dinámicas'], 'c': ['Construye', 'Prácticas en la hoja de cálculo']}

_DIR = Path(__file__).parent
EXTRA_JS = (_DIR / 'xl3_sim.js').read_text(encoding='utf8') + '\n' + (_DIR / 'pv_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".pvsim"))pInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".pvsim"))return pCheck(d);\n'),
]

c = Course()


def sheet(name, rows):
    cells = {}
    for r, row in enumerate(rows, 1):
        for k, v in enumerate(row):
            cells['ABCDEFGH'[k] + str(r)] = {'v': v}
            if r == 1:
                cells['ABCDEFGH'[k] + str(r)]['b'] = 1
    return {'n': name, 'c': cells}


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.pv, a.pch, a.prev, a.pr, a.used, a.calc, a.v, a.lock, a.sheet)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pPv({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


random.seed(7)
PRECIO = {'Tortas': 35, 'Jugos': 18, 'Snacks': 12, 'Café': 15}
DATOS = [['Mes', 'Producto', 'Turno', 'Piezas', 'Importe']]
for m in ['Sep', 'Oct', 'Nov']:
    for p, pz in PRECIO.items():
        for t in ['Matutino', 'Vespertino']:
            q = random.randint(20, 70)
            DATOS.append([m, p, t, q, q * pz])
BASE = {'rows': 26, 'file': 'Ventas_LaEscuelita.xlsx', 'sheets': [sheet('Ventas', DATOS)]}


def cfg(**kw):
    d = dict(BASE)
    d.update(kw)
    return d


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('📋', 'La directora quiere un reporte', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Una <b>tabla dinámica</b> resume una lista larga de datos en una tabla corta, y la puedes reacomodar con unos clics. Un <b>reporte ejecutivo</b> es ese resumen bien presentado para quien toma decisiones.'),
    ex('Caso: Cafetería La Escuelita', 'La cafetería anotó cada venta por <b>mes, producto y turno</b>. La directora pregunta: ¿qué producto deja más dinero?, ¿en qué turno se vende más?, ¿cómo vamos por mes? Con fórmulas tardarías; con una tabla dinámica, segundos. Después hay que <b>proteger</b> el libro para que nadie borre fórmulas sin querer.'),
    r3([('📋', 'A · Tablas dinámicas', 'Crear, campos, cálculos, orden, subtotales y filtros.'), ('📊', 'B · Gráficos dinámicos', 'Crear, configurar y vista preliminar.'), ('🔒', 'C · Protección', 'Contraseñas, restricciones de formato, edición y macros.')])),
    'Resumir, mostrar y proteger: eso es un reporte ejecutivo.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia (15%)', 'Un <b>libro de trabajo con tablas dinámicas</b>, al menos un gráfico dinámico y <b>contraseña y restricciones</b> asignadas.'),
    bk('Cómo se arma', 'Practica en los simuladores y luego haz lo mismo en Excel con tus datos. Las tablas dinámicas también existen en Excel del celular (Insertar › Tabla dinámica) y en Hojas de cálculo de Google.'),
    warn('Importante', 'Para que tu profesor pueda revisarlo, la contraseña <b>para abrir</b> el libro que entregas será <b>EDOA34-311</b>. Las contraseñas de la hoja y del libro las eliges tú y las anotas en la hoja «Evidencias».')),
    'Cada simulador es una pieza de tu reporte.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Tablas dinámicas ─────────────────────────
a0 = c.mark()
c.L('🧱', 'Antes de crear: datos bien acomodados', 'Bloque A · La lista de origen', body(
    sp('En palabras sencillas', 'La tabla dinámica necesita una <b>lista ordenada</b>: una fila de encabezados y un registro por fila.'),
    bk('Reglas de la lista', 'Cada columna con <b>encabezado único</b> (Mes, Producto, Turno, Piezas, Importe) · sin filas ni columnas vacías en medio · sin celdas combinadas · cada columna con un solo tipo de dato.'),
    ex('Así sí', '<code>Nov | Café | Vespertino | 56 | 840</code> · una venta por fila.'),
    warn('Así no', 'Un título combinado arriba de la tabla, totales escritos a mano en medio o meses como columnas (Sep, Oct, Nov…) en lugar de una columna «Mes».')),
    'Lista limpia = tabla dinámica sin problemas.')
c.L('📋', 'Crear una tabla dinámica', 'Bloque A · Paso a paso', body(
    px('En Excel', [
        'Toca cualquier celda dentro de la lista.',
        '<b>Insertar › Tabla dinámica</b>. Excel propone el rango completo; elige <b>Nueva hoja de cálculo</b>.',
        'Aparece el panel <b>Campos de tabla dinámica</b> con los encabezados de tu lista.',
        'Lleva cada campo a un área: <b>Filas</b>, <b>Columnas</b>, <b>Valores</b> o <b>Filtros</b>.']),
    bk('Las cuatro áreas', '<b>Filas</b>: lo que quieres listar hacia abajo (productos). <b>Columnas</b>: lo que quieres comparar hacia la derecha (meses). <b>Valores</b>: lo que se suma o cuenta (importe). <b>Filtros</b>: lo que quieres elegir arriba (solo un turno).'),
    ana('Piensa en una pregunta', '«¿Cuánto <b>dinero</b> (Valores) dejó cada <b>producto</b> (Filas) en cada <b>mes</b> (Columnas), solo en el <b>turno vespertino</b> (Filtro)?»')),
    'Pregunta → campos → áreas.')
c.A('🧩', '¿A qué área va?', 'La directora pregunta: «¿cuánto dinero dejó cada producto en cada mes, solo en el turno matutino?». Elige el área de cada campo.', [
    ['Producto', 'Filas', 'Se lista hacia abajo: un renglón por producto.'],
    ['Mes', 'Columnas', 'Se compara hacia la derecha: una columna por mes.'],
    ['Importe', 'Valores', 'Es lo que se suma.'],
    ['Turno', 'Filtros', 'Solo se quiere ver uno de los turnos.'],
], 'Lo que se suma va a Valores; lo que se elige, a Filtros.', ['Filas', 'Columnas', 'Valores', 'Filtros'])
sim('📋', 'Tu primera tabla dinámica', 'Simulador: crea la tabla y responde «¿qué producto deja más dinero?».', cfg(
    id='p1', intro='Esta es la lista de ventas de la cafetería. Toca una celda dentro de la lista y usa <b>Insertar › Tabla dinámica</b>.'), [
    ['Inserta una <b>tabla dinámica</b> (se crea en la hoja Resumen).', 'a.pv'],
    ['Pon <b>Producto</b> en Filas e <b>Importe</b> en Valores (Suma).', 'a.pv&&a.pv.rows[0]=="Producto"&&!a.pv.rows[1]&&a.pv.val=="Importe"&&a.pv.fn=="sum"'],
    ['Dale formato de <b>moneda</b> a los valores.', 'a.pv&&a.pv.nf=="$#,##0.00"'],
    ['Ordénala de <b>mayor a menor</b> para ver qué producto deja más dinero.', 'a.pv&&a.pv.sort=="val"']],
    'Todo se configura en la ficha Análisis de tabla dinámica.')
c.L('🧮', 'Campos y cálculos', 'Bloque A · Sumar, contar, promediar', body(
    bk('Resumir valores por', '<b>Suma</b> (total de dinero), <b>Cuenta</b> (cuántos registros), <b>Promedio</b>, <b>Máx</b> y <b>Mín</b>. En Excel: clic en el campo de Valores › <b>Configuración de campo de valor</b>.'),
    bk('Formato de número', 'En la misma ventana › <b>Formato de número</b> › Moneda. Así el formato se queda aunque la tabla cambie.'),
    bk('Ordenar', 'Clic en la flecha de Etiquetas de fila › <b>Ordenar de A a Z</b>, o clic derecho en un valor › <b>Ordenar de mayor a menor</b>.'),
    bk('Campo calculado', 'En <b>Análisis › Campos, elementos y conjuntos › Campo calculado</b> creas una columna nueva con una fórmula (por ejemplo, Importe × 0.16 para el IVA).'),
    ex('Ejemplo', 'Promedio de Piezas por Turno: el vespertino vende en promedio más piezas que el matutino → conviene reforzar ese turno.')),
    'Suma para dinero, Cuenta para cuántos, Promedio para lo típico.')
c.L('🧾', 'Subtotales, totales y filtros', 'Bloque A · Detalle y resumen a la vez', body(
    bk('Dos niveles de filas', 'Si pones <b>Mes</b> y debajo <b>Producto</b> en Filas, verás cada mes con sus productos adentro.'),
    bk('Subtotales', 'Con dos niveles aparece un <b>subtotal</b> por cada mes. Se activan o quitan en <b>Diseño › Subtotales</b>.'),
    bk('Totales generales', 'La última fila y la última columna. Se controlan en <b>Diseño › Totales generales</b>.'),
    bk('Filtros', 'El campo en <b>Filtros</b> aparece arriba de la tabla con una flecha: eliges un valor (solo «Nov») y toda la tabla se recalcula. También puedes usar <b>Segmentación de datos</b> (botones para filtrar).'),
    warn('Actualizar', 'Si cambias un dato en la lista, la tabla dinámica <b>no cambia sola</b>: clic derecho › <b>Actualizar</b> (o Análisis › Actualizar).')),
    'Subtotal = por grupo · Total general = todo · Filtro = solo lo que eliges · Actualizar al cambiar datos.')
sim('🧾', 'Cruza y filtra la información', 'Simulador: dos niveles, promedio, subtotales, filtro y actualizar.', cfg(
    id='p2', intro='Ahora la directora quiere saber cuántas piezas se venden en promedio por producto y turno, solo en noviembre.'), [
    ['Inserta la tabla dinámica y pon <b>Producto</b> en Filas y <b>Turno</b> como 2.º nivel.', 'a.pv&&a.pv.rows[0]=="Producto"&&a.pv.rows[1]=="Turno"'],
    ['Pon <b>Piezas</b> en Valores y resúmelo por <b>Promedio</b>.', 'a.pv&&a.pv.val=="Piezas"&&a.pv.fn=="avg"'],
    ['Quita los <b>subtotales</b>, observa y vuelve a activarlos.', 'a.pv&&a.used("p_sub")&&a.pv.sub!==false'],
    ['Usa el <b>filtro</b> para ver solo <b>Nov</b>.', 'a.pv&&a.pv.filt=="Mes"&&a.pv.fv=="Nov"'],
    ['En la hoja Ventas corrige <b>D5</b>: fueron <b>16</b> piezas (no 61). Luego <b>actualiza</b> la tabla dinámica.', 'a.v("D5")==16&&a.pv&&a.pv.snap.rows[3].Piezas==16']],
    'Para corregir D5 cambia a la hoja Ventas (abajo), toca la celda y escribe en la barra de arriba.')
c.T('🧮', 'Lee la tabla dinámica', 'Usa la tabla «Suma de Importe por Producto» de la cafetería: Café 3 465 · Jugos 4 338 · Snacks 2 448 · Tortas 8 365. Escribe solo el número.', [
    ['¿Cuál es el total general de importe?', '18616', '3465 + 4338 + 2448 + 8365 = 18 616.', 'Suma las cuatro filas.', 'n'],
    ['¿Cuánto más dejaron las tortas que los jugos?', '4027', '8365 − 4338 = 4027.', 'Resta.', 'n'],
    ['¿Qué porcentaje del total son las tortas (redondeado)?', '45', '8365 ÷ 18616 × 100 ≈ 45 %.', 'Parte ÷ total × 100.', 'n'],
    ['Si la lista tiene 24 registros y pides «Cuenta de Importe», ¿qué número sale en el total general?', '24', 'Cuenta cuántos registros hay, no suma dinero.', 'Cuenta = número de filas.', 'n'],
], 'La tabla dinámica hace estas cuentas por ti; aquí compruebas que las entiendes.', 'n')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Gráficos dinámicos ─────────────────────────
b0 = c.mark()
c.L('📊', 'Gráficos dinámicos', 'Bloque B · La tabla dinámica hecha dibujo', body(
    sp('En palabras sencillas', 'Un <b>gráfico dinámico</b> está conectado a la tabla dinámica: si cambias un filtro o un campo, la gráfica cambia también.'),
    px('Crear y configurar', [
        'Clic dentro de la tabla dinámica.',
        '<b>Análisis de tabla dinámica › Gráfico dinámico</b> (o Insertar › Gráfico dinámico).',
        'Elige el tipo (columnas, barras, líneas o circular).',
        'Configúralo como cualquier gráfica: título, etiquetas, leyenda y colores.']),
    bk('Diferencia con una gráfica normal', 'La gráfica normal depende de un rango fijo; la dinámica obedece a los filtros de la tabla.'),
    bk('Vista preliminar', '<b>Archivo › Imprimir</b> muestra cómo saldrá la hoja: elige <b>orientación horizontal</b> si la tabla es ancha y <b>Ajustar hoja en una página</b> para que no se corte.')),
    'Tabla dinámica + gráfico dinámico + vista preliminar = reporte listo.')
c.A('🖨️', '¿Qué ajuste de impresión usas?', 'Elige el ajuste para cada problema de la vista preliminar.', [
    ['La tabla es muy ancha y la última columna sale en otra hoja', 'Orientación horizontal', 'La hoja acostada da más espacio a lo ancho.'],
    ['El reporte ocupa 2 páginas pero debería caber en 1', 'Ajustar hoja en una página', 'Excel reduce un poco el tamaño para que quepa.'],
    ['Quieres comprobar cómo saldrá antes de gastar papel', 'Vista preliminar', 'Muestra la impresión en pantalla.'],
    ['La gráfica sale cortada a la mitad', 'Ajustar hoja en una página', 'Ajustar evita que se divida en dos hojas.'],
], 'Revisa siempre la vista preliminar antes de imprimir.', ['Vista preliminar', 'Orientación horizontal', 'Ajustar hoja en una página'])
sim('📊', 'Reporte con gráfico dinámico', 'Simulador: gráfico conectado a la tabla y vista preliminar.', cfg(
    id='p3', pv={'rows': ['Producto'], 'col': 'Mes', 'val': 'Importe', 'fn': 'sum', 'filt': 'Turno', 'fv': '(Todas)', 'sort': 'asc', 'nf': '$#,##0.00'},
    intro='La tabla dinámica ya está en la hoja <b>Resumen</b>. Convierte el reporte en algo que la directora entienda de un vistazo.'), [
    ['Inserta un <b>gráfico dinámico</b> de columnas.', 'a.pch&&a.pch.type=="col"'],
    ['Ponle el título «Importe por producto y mes».', 'a.pch&&/importe/i.test(a.pch.tt||"")'],
    ['En la tabla, filtra el turno <b>Vespertino</b> y mira cómo cambia la gráfica.', 'a.pv.fv=="Vespertino"&&a.pch'],
    ['Abre la <b>vista preliminar</b> (Archivo) en orientación <b>horizontal</b> y <b>ajustada a una página</b>.', 'a.prev&&a.prev.or=="h"&&a.prev.fit']],
    'El gráfico dinámico se crea desde Insertar; el filtro está en Análisis de tabla dinámica.')
b_end = c.mark() - 1

# ───────────────────────── Bloque C · Protección ─────────────────────────
c0 = c.mark()
c.L('🔒', 'Proteger la hoja', 'Bloque C · Restricciones de edición y de formato', body(
    sp('En palabras sencillas', 'Proteger una hoja <b>impide cambiar sus celdas</b> (y, si quieres, darles formato), para que nadie borre una fórmula sin querer.'),
    bk('Bloqueadas y desbloqueadas', 'Todas las celdas vienen <b>bloqueadas</b>, pero el bloqueo solo funciona cuando proteges la hoja. Antes de proteger, <b>desbloquea</b> las celdas donde sí se debe capturar: selecciónalas › clic derecho › <b>Formato de celdas › Proteger</b> › quita la marca de <b>Bloqueada</b>.'),
    bk('Proteger', '<b>Revisar › Proteger hoja</b>: escribe una contraseña y marca lo que sí se permite (seleccionar celdas, <b>aplicar formato</b>, insertar filas…).'),
    ex('En la cafetería', 'El encargado solo captura <b>Piezas</b> (columna D). Se desbloquea D2:D25 y se protege la hoja sin permitir formato: puede capturar, pero no borrar los importes ni cambiar colores.'),
    warn('Recuerda', 'La protección de hoja evita errores, pero no es cifrado: para que nadie <b>abra</b> el archivo usa la contraseña de apertura.')),
    'Desbloquea lo que se captura → protege con contraseña.')
sim('🔒', 'Protege la hoja de captura', 'Simulador: desbloquea, protege y prueba las restricciones.', cfg(
    id='p4', intro='El encargado capturará las piezas cada día. Haz que solo pueda cambiar la columna D.'), [
    ['Selecciona <b>D2:D25</b> y desbloquéalas (Revisar › Desbloquear celdas seleccionadas).', '!a.lock("D2")&&!a.lock("D25")&&a.lock("E2")'],
    ['<b>Protege la hoja</b> con contraseña y <b>sin</b> permitir aplicar formato.', 'a.pr.sh&&a.pr.sh.pw&&!a.pr.sh.fmt'],
    ['Intenta cambiar un importe (columna E): debe impedírtelo.', 'a.used("blocked")'],
    ['Cambia unas piezas en la columna D: eso sí debe dejarte.', 'a.used("editunl")'],
    ['Intenta poner <b>negrita</b> a una celda: también debe impedírtelo.', 'a.used("blockfmt")']],
    'Para seleccionar D2:D25 toca D2 y luego D25.')
c.L('🗝️', 'Proteger el libro y cifrarlo', 'Bloque C · Estructura y contraseña de apertura', body(
    bk('Proteger estructura', '<b>Revisar › Proteger libro</b>: nadie puede agregar, borrar, mover ni renombrar hojas.'),
    bk('Cifrar con contraseña', '<b>Archivo › Información › Proteger libro › Cifrar con contraseña</b>: sin la contraseña el archivo <b>no se abre</b>. Si la olvidas, no hay forma de recuperarlo.'),
    bk('Contraseña segura', 'Al menos 8 caracteres con letras, números y un símbolo. Nada de «1234» ni tu nombre.'),
    bk('Ejecución de macros', '<b>Archivo › Opciones › Centro de confianza › Configuración de macros</b>. Lo recomendado: <b>Deshabilitar todas las macros con notificación</b> (ves la barra amarilla y decides).'),
    ana('Piensa en una casa', 'Proteger hoja = cajones con llave. Proteger libro = no se pueden mover los muebles. Cifrar = la puerta de la casa con llave.')),
    'Hoja = celdas · Libro = hojas · Cifrar = abrir · Centro de confianza = macros.')
c.A('🔐', '¿Qué protección necesitas?', 'Elige la protección que resuelve cada problema.', [
    ['Alguien borró la hoja Resumen por error', 'Proteger libro', 'La protección de estructura impide borrar hojas.'],
    ['Que nadie pueda abrir el archivo de sueldos sin permiso', 'Cifrar con contraseña', 'Sin la contraseña de apertura el archivo no se abre.'],
    ['Que el encargado capture piezas pero no cambie las fórmulas', 'Proteger hoja', 'Desbloqueas la captura y proteges la hoja.'],
    ['Que un archivo descargado no ejecute macros sin avisar', 'Configuración de macros', 'El Centro de confianza decide qué pasa con las macros.'],
    ['Que nadie le cambie los colores al reporte', 'Proteger hoja', 'Al proteger la hoja no permites «Aplicar formato a celdas».'],
], 'Pregunta: ¿quiero cuidar celdas, hojas, la apertura del archivo o las macros?', ['Proteger hoja', 'Proteger libro', 'Cifrar con contraseña', 'Configuración de macros'])
sim('🗝️', 'Protege y cifra el libro', 'Simulador: estructura, contraseña de apertura y seguridad de macros.', cfg(
    id='p5', intro='Antes de enviar el reporte a la dirección, protege todo el libro.'), [
    ['<b>Protege el libro</b> (estructura) con contraseña.', 'a.pr.book&&a.pr.book.pw'],
    ['Intenta agregar una hoja nueva: no debe dejarte.', 'a.used("blockbook")'],
    ['<b>Cifra</b> el libro con una contraseña de al menos 8 caracteres.', 'a.pr.open&&a.pr.open.length>=8'],
    ['Ciérralo y ábrelo escribiendo la contraseña.', 'a.used("opened")'],
    ['En el Centro de confianza elige <b>Deshabilitar todas las macros con notificación</b>.', 'a.pr.mac==1&&a.used("trustgo")']],
    'Proteger libro está en Revisar; cifrar y el Centro de confianza están en Archivo.')
c.W('✍️', 'Tu política de protección', 'Explica cómo protegerías tu libro.',
    'Escribe cómo protegerías el libro de ventas de la cafetería antes de compartirlo. Menciona qué celdas <b>desbloqueas</b>, si proteges la <b>hoja</b> y el <b>libro</b>, si lo <b>cifras</b> y cómo sería una <b>contraseña segura</b>.',
    [['Tiene al menos 30 palabras', 'palabras:30'],
     ['Menciona desbloquear celdas', '\\b(desbloque\\w*)\\b'],
     ['Menciona proteger hoja o libro', '\\b(protej\\w*|proteg\\w*)\\b'],
     ['Menciona cifrar o contraseña de apertura', '\\b(cifr\\w*|abrir|apertura)\\b'],
     ['Describe la contraseña (caracteres, números, símbolos)', '\\b(caracteres|numeros|simbolo\\w*|mayuscula\\w*|letras)\\b']],
    'Celdas → hoja → libro → archivo.', 'Ejemplo: Desbloquearía la columna Piezas…')
c_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Tabla dinámica', 'Resumen interactivo de una lista de datos.'),
    bk('Campo', 'Cada columna de la lista (Mes, Producto…).'),
    bk('Filas / Columnas / Valores / Filtros', 'Las cuatro áreas donde acomodas los campos.'),
    bk('Subtotal', 'Total de cada grupo dentro de la tabla.'),
    bk('Total general', 'Total de toda la tabla, al final.'),
    bk('Actualizar', 'Volver a leer la lista cuando cambian los datos.'),
    bk('Gráfico dinámico', 'Gráfica conectada a una tabla dinámica.'),
    bk('Vista preliminar', 'Cómo saldrá la hoja impresa.'),
    bk('Celda bloqueada', 'No se puede cambiar cuando la hoja está protegida.'),
    bk('Cifrar', 'Proteger el archivo con contraseña para abrirlo.'),
    bk('Centro de confianza', 'Opciones de seguridad de Office, incluida la ejecución de macros.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311: martes 17:20-19:50, miércoles 18:10-19:50 y laboratorio el viernes 15:20-18:10. La A.E. 3.4 es el miércoles 9-dic y vale 15%.', 'sp'),
    bk('Bloque A · 2 y 4-dic', 'Miércoles 2 (después de entregar el 3.3): lista de origen y crear la tabla; simulador 1. Viernes 4 (laboratorio): campos, cálculos, subtotales y filtros; simulador 2 y <b>Práctica 1</b>.'),
    bk('Bloques B y C · 4 y 8-dic', 'Viernes 4 (segunda parte): gráfico dinámico y vista preliminar, simulador 3. Martes 8: protección de hoja, libro, cifrado y macros; simuladores 4 y 5 y <b>Práctica 2</b>.'),
    bk('Evaluación · miércoles 9-dic', 'Entrega del libro con tablas y gráficos dinámicos, contraseña y restricciones. La contraseña de apertura acordada es <b>EDOA34-311</b>; las de hoja y libro vienen anotadas en la hoja «Evidencias». El mismo día arranca el R.A. 4.1.'),
    bk('Sin computadora', 'Excel móvil y Hojas de cálculo de Google crean tablas dinámicas. La protección de hoja también existe en Google (Datos › Proteger hojas y rangos); el cifrado se demuestra en el simulador.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '📋', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🧮', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '📊', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🔒', 'a': c0, 'b': c_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"📋",t:"Empieza aquí",d:"Qué es un reporte ejecutivo y qué vas a entregar.",time:"15 min",obj:["Explicar para qué sirve una tabla dinámica","Conocer la evidencia del R.A."],sum:["Tabla dinámica = resumen que se reacomoda.","Reporte ejecutivo = resumen bien presentado para decidir.","Evidencia: libro con tablas dinámicas, contraseña y restricciones (15%)."],q:"¿Qué datos de tu vida diaria te gustaría resumir (gastos, calificaciones, horas de juego)?"},
a:{k:"Bloque A",l:"A",ic:"🧮",t:"Tablas dinámicas",d:"Crear, diseño, formato, campos y cálculos, ordenar, subtotales, totales y filtros.",time:"4 h",obj:["Preparar una lista de origen correcta","Crear una tabla dinámica y acomodar campos","Resumir por suma, cuenta o promedio y dar formato","Usar subtotales, totales, orden y filtros, y actualizar"],sum:["Lista limpia: encabezados únicos, un registro por fila.","Filas, Columnas, Valores y Filtros.","Suma, Cuenta, Promedio, Máx, Mín · formato de número.","Subtotales por grupo · Actualizar al cambiar datos."],q:"¿Qué pregunta le harías a la lista de ventas de la cafetería?"},
b:{k:"Bloque B",l:"B",ic:"📊",t:"Gráficos dinámicos",d:"Crear, configurar y vista preliminar.",time:"2 h",obj:["Crear un gráfico dinámico","Configurarlo y usar sus filtros","Revisar la vista preliminar antes de imprimir"],sum:["El gráfico dinámico obedece a la tabla.","Título, etiquetas y leyenda como cualquier gráfica.","Horizontal y ajustar a una página."],q:"¿Por qué conviene revisar la vista preliminar antes de imprimir?",rev:[["El campo que se suma va en…",["Valores","Filas","Filtros"],0,"Valores es lo que se calcula."],["Si cambias un dato de la lista, la tabla dinámica…",["Se actualiza con «Actualizar»","Cambia sola siempre","Se borra"],0,"Hay que actualizarla."]]},
c:{k:"Bloque C",l:"C",ic:"🔒",t:"Protección de información",d:"Contraseña de hoja y libro, restricciones de formato y edición, y ejecución de macros.",time:"4 h",obj:["Desbloquear celdas de captura y proteger la hoja","Restringir formato y edición","Proteger la estructura y cifrar el libro","Configurar la ejecución de macros"],sum:["Desbloquear → proteger hoja con contraseña.","Sin permitir formato no se cambian colores ni negritas.","Proteger libro = hojas; cifrar = abrir.","Macros: deshabilitar con notificación."],q:"¿Qué información de la escuela protegerías con contraseña?",rev:[["Un gráfico dinámico está conectado a…",["Una tabla dinámica","Una macro","Una hoja protegida"],0,"Obedece a sus filtros."],["Para que la tabla ancha quepa en la hoja impresa se usa…",["Orientación horizontal","Negrita","Cifrar"],0,"La hoja acostada da más espacio."]]}
'''

ILL = r'''
ILL["La directora quiere un reporte"]=function(){return flow([["🧾","24 ventas"],["📋","Tabla|dinámica"],["📊","Gráfico"],["🔒","Proteger"],["👩‍💼","Directora"]],"Del registro al reporte")};
ILL["Crear una tabla dinámica"]=function(){return SV(340,120,R_(10,10,150,100,"s",8)+T_(85,30,"Campos","t")+T_(85,52,"Mes · Producto","tm")+T_(85,70,"Turno · Piezas","tm")+T_(85,88,"Importe","tm")+R_(180,10,72,46,"b",6)+T_(216,38,"Filtros","tw")+R_(258,10,72,46,"b",6)+T_(294,38,"Columnas","tw")+R_(180,64,72,46,"g",6)+T_(216,92,"Filas","tw")+R_(258,64,72,46,"a",6)+T_(294,92,"Valores","td"),"Campos y las cuatro áreas")};
ILL["Subtotales, totales y filtros"]=function(){var r=[["Sep","",1],["  Tortas","2415",0],["  Café","1200",0],["  …","",0],["Total Sep","6087",2],["Total general","18616",3]],o='';r.forEach(function(x,i){var y=8+i*24,c=x[2]==3?"g":x[2]==2?"s":"w";o+=R_(60,y,220,22,c,3)+T_(70,y+15,x[0],x[2]==3?"tw":"t","start")+T_(270,y+15,x[1],x[2]==3?"tw":"t","end")});return SV(340,156,o,"Grupo, subtotal y total general")};
ILL["Proteger la hoja"]=function(){return flow([["🖱️","Selecciona|captura"],["🔓","Desbloquea"],["🔒","Proteger|hoja"],["🔑","Contraseña"],["✅","Prueba"]],"Pasos para proteger la hoja")};
ILL["Proteger el libro y cifrarlo"]=function(){return grid3([["🗄️","Hoja|celdas"],["📕","Libro|hojas"],["🔐","Cifrar|abrir"],["🛡️","Macros|confianza"]],"Niveles de protección")};
'''

EXH = r'''
EXH.lista=function(){return exw('<table class="mtb"><tr><th>Mes</th><th>Producto</th><th>Turno</th><th>Piezas</th><th>Importe</th></tr><tr><td>Sep</td><td>Tortas</td><td>Matutino</td><td>40</td><td>1400</td></tr><tr><td>Sep</td><td>Tortas</td><td>Vespertino</td><td>29</td><td>1015</td></tr><tr><td>…</td><td>…</td><td>…</td><td>…</td><td>…</td></tr></table>',['Un registro por fila, encabezados únicos, sin filas vacías.'])};
EXH.insertar_td=function(){return exw(mw('Insertar › Tabla dinámica','<div class="mfld">Tabla o rango: Ventas!$A$1:$E$25 '+mk(1)+'</div><div class="mfld" style="margin-top:6px">◉ Nueva hoja de cálculo '+mk(2)+'</div>'),['Excel propone el rango; revisa que incluya todo.','Mejor en hoja nueva.'])};
EXH.campos=function(){return exw(mw('Campos de tabla dinámica','<div class="mm"><span>☑ Producto → Filas '+mk(1)+'</span><span>☑ Mes → Columnas</span><span>☑ Importe → Valores (Suma) '+mk(2)+'</span><span>☑ Turno → Filtros</span></div>'),['Arrastra cada campo a su área.','Clic › Configuración de campo de valor para cambiar a Promedio o Cuenta.'])};
EXH.grafico_td=function(){return exw(mw('Análisis de tabla dinámica','<div class="mm"><span class="hl">📊 Gráfico dinámico '+mk(1)+'</span><span>🔄 Actualizar '+mk(2)+'</span></div>'),['Crea el gráfico conectado.','Úsalo cuando cambies datos.'])};
EXH.imprimir=function(){return exw(mw('Archivo › Imprimir','<div class="mfld">Orientación horizontal '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Ajustar hoja en una página '+mk(2)+'</div>'),['Para tablas anchas.','Para que no se corte.'])};
EXH.bloq=function(){return exw(mw('Formato de celdas › Proteger','<div class="mfld">☐ Bloqueada '+mk(1)+'</div><div class="mfld" style="margin-top:6px">☐ Oculta</div>'),['Quita la marca en las celdas de captura antes de proteger.'])};
EXH.prot=function(){return exw(mw('Proteger hoja','<div class="mfld">Contraseña: •••••••• '+mk(1)+'</div><div class="mm" style="margin-top:6px"><span>☑ Seleccionar celdas bloqueadas</span><span>☑ Seleccionar celdas desbloqueadas</span><span>☐ Aplicar formato a celdas '+mk(2)+'</span></div>'),['Contraseña para desproteger.','Sin formato: nadie cambia colores.'])};
EXH.cifrar=function(){return exw(mw('Archivo › Información › Proteger libro','<div class="mm"><span>Proteger hoja actual</span><span>Proteger estructura del libro '+mk(1)+'</span><span class="hl">Cifrar con contraseña '+mk(2)+'</span></div>'),['Nadie mueve hojas.','Nadie abre sin contraseña.'])};
EXH.cel_td=function(){return exw(mp('Excel móvil','<div class="mbox">Selecciona la lista › Insertar › Tabla dinámica '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Toca la tabla › Campos › Filas, Columnas, Valores '+mk(2)+'</div>'),['También en Hojas de cálculo de Google: Insertar › Tabla dinámica.','Acomoda los campos desde el panel.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Reporte ejecutivo con tablas y gráficos dinámicos',
     'prog': 'Bloques A y B · Tablas y gráficos dinámicos',
     'min': 90, 'lug': 'Viernes 4-dic en laboratorio, o en casa (computadora o celular)',
     'modes': {
         'pc': {'mat': ['Computadora con Excel'],
                'steps': [
                    'Antes de empezar, termina los simuladores 1, 2 y 3.',
                    ['Captura la lista de ventas (mes, producto, turno, piezas e importe) con al menos 24 registros, o usa tus propios datos.', 'lista'],
                    ['Inserta una tabla dinámica en hoja nueva.', 'insertar_td'],
                    ['Arma «Importe por producto y mes» con filtro de turno y formato de moneda; ordénala de mayor a menor.', 'campos'],
                    'Arma una segunda tabla dinámica con Producto y Turno en filas, Piezas en Promedio y subtotales.',
                    ['Crea un gráfico dinámico de la primera tabla y prueba el filtro.', 'grafico_td'],
                    ['Revisa la vista preliminar en horizontal y ajustada a una página.', 'imprimir'],
                    'Escribe tres conclusiones para la directora (qué producto deja más, qué turno vende más y cómo van los meses).']},
         'cel': {'mat': ['Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 1, 2 y 3.',
                     'Captura la lista de ventas con al menos 24 registros.',
                     ['Inserta una tabla dinámica y acomoda Producto en filas, Mes en columnas e Importe en valores.', 'cel_td'],
                     'Agrega un filtro por turno y ordena de mayor a menor.',
                     'Inserta un gráfico a partir de la tabla dinámica.',
                     'Toma capturas y escribe tres conclusiones para la directora.']}},
     'entrega': ['Libro con dos tablas dinámicas, un gráfico dinámico y conclusiones.'],
     'rub': [['Lista de origen correcta', 15], ['Tabla dinámica con filtro, formato y orden', 25], ['Segunda tabla con promedio y subtotales', 20], ['Gráfico dinámico', 20], ['Vista preliminar y conclusiones', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Protege tu libro',
     'prog': 'Bloque C · Protección de información',
     'min': 45, 'lug': 'Martes 8-dic en clase o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con Excel', 'Tu libro de la práctica 1'],
                'steps': [
                    'Antes de empezar, termina los simuladores 4 y 5.',
                    ['En la hoja de la lista, desbloquea solo la columna de captura (Piezas).', 'bloq'],
                    ['Protege la hoja con contraseña sin permitir formato; prueba que no deja cambiar un importe.', 'prot'],
                    ['Protege la estructura del libro y cífralo con una contraseña segura.', 'cifrar'],
                    'Revisa en el Centro de confianza que las macros estén deshabilitadas con notificación.',
                    'Toma captura de cada mensaje de protección y guárdalas en una hoja «Evidencias».']},
         'cel': {'mat': ['Hojas de cálculo de Google en el celular o el navegador'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 4 y 5.',
                     'En Hojas de cálculo de Google: Datos › Proteger hojas y rangos › protege la hoja y deja libre solo la columna Piezas.',
                     'Comparte el archivo con permiso de «Lector» a un compañero y comprueba que no puede editar.',
                     'Toma captura de cada paso y explica qué protege cada uno.']}},
     'entrega': ['Libro protegido (hoja, estructura y contraseña de apertura) con su hoja de evidencias.'],
     'rub': [['Celdas de captura desbloqueadas', 25], ['Hoja protegida sin formato', 25], ['Libro protegido y cifrado', 30], ['Evidencias y explicación', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 3',
    'ra': 'R.A. 3.4', 'title': 'Reporte ejecutivo con tablas dinámicas y protección',
    'data': [
        ('Resultado de aprendizaje', 'Diseña reportes ejecutivos como resultado del análisis de datos con el uso de tablas dinámicas y aplica niveles de protección de información en la hoja de cálculo.'),
        ('Actividad de evaluación', '3.4.1 Elabora hoja de cálculo que contenga el uso de tablas dinámicas, aplique restricciones de acceso, de formato y de edición.'),
        ('Evidencia', 'Libro de trabajo con tablas dinámicas aplicando contraseña y restricciones asignadas'),
        ('Ponderación', '15% (según el programa)'),
        ('Entrega', 'Miércoles 9 de diciembre: archivo en la plataforma'),
    ],
    'situation': 'La directora de la cafetería quiere un reporte de ventas que pueda revisar sin miedo a descomponerlo. Entrega tu libro con tablas y gráficos dinámicos y con la protección que practicaste.',
    'hint': 'Cifra el libro con la contraseña de apertura EDOA34-311 para que tu profesor pueda abrirlo, y anota en la hoja «Evidencias» las contraseñas que usaste para proteger la hoja y el libro.',
    'steps': [
        ('Tablas dinámicas (A)', [
            'Lista de origen con al menos 24 registros.',
            'Tabla dinámica con filtro, formato de moneda y orden de mayor a menor.',
            'Segunda tabla con dos niveles de filas, otra función (promedio o cuenta) y subtotales.']),
        ('Gráfico dinámico (B)', [
            'Gráfico dinámico con título y etiquetas, conectado a la primera tabla.',
            'Hoja configurada para imprimir (horizontal y ajustada) y tres conclusiones.']),
        ('Protección (C)', [
            'Celdas de captura desbloqueadas y hoja protegida sin permitir formato.',
            'Estructura del libro protegida y contraseña de apertura EDOA34-311; hoja «Evidencias» con las contraseñas de hoja y libro.']),
    ],
    'rubric': [
        ('Lista de origen', 10), ('Tabla dinámica con filtro, formato y orden', 20), ('Segunda tabla con subtotales', 15),
        ('Gráfico dinámico y vista preliminar', 20), ('Conclusiones', 10), ('Restricciones de edición y formato', 15), ('Libro protegido y cifrado', 10),
    ],
    'deliver': ['Un archivo .xlsx protegido, cifrado con la contraseña de apertura EDOA34-311.', 'Nombre del archivo: Apellido_Nombre_EDOA34.', 'Súbelo en la actividad R.A. 3.4 de la plataforma.'],
}
