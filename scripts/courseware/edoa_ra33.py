"""EDOA-20 · R.A. 3.3 · Gráficas y macros en la hoja de cálculo.

Continúa el caso de la Cafetería La Escuelita (R.A. 3.1 y 3.2): ahora sus datos se ven en gráficas
y las tareas repetitivas se hacen solas con macros.
Incluye seis simuladores (xl3_sim.js): tres de gráficas y tres de macros.
La actividad de evaluación es la entrega del libro de trabajo (.xlsm, .xlsx o PDF) en la plataforma.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-3.3'
CODE_PREFIX = 'EDOA33'
FILE = 'edoa-ra33-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 3.3 · Gráficas y macros'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 3.3 · Gráficas y macros'
HERO_KICK = 'EDOA-20 · R.A. 3.3'
HERO_TITLE = 'Datos que se entienden y tareas que se hacen solas'
HERO_TEXT = 'Convierte las ventas de la cafetería en gráficas claras y graba macros para que Excel repita por ti el trabajo aburrido.'
EV_SHORT = 'entrega tu libro con gráficas y macros.'
EV_CARD = 'Libro de trabajo R.A. 3.3'
RA = 'R.A. 3.3'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores de gráficas y macros'], 'c': ['Construye', 'Prácticas en la hoja de cálculo']}

EXTRA_JS = (Path(__file__).parent / 'xl3_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".xlsim"))xInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".xlsim"))return xCheck(d);\n'),
]

c = Course()


def sheet(name, rows, fmt=None):
    """rows: lista de filas desde A1; fmt: {celda: {b, f, nf}}."""
    cells = {}
    for r, row in enumerate(rows, 1):
        for k, v in enumerate(row):
            if v is not None and v != '':
                cells['ABCDEFGH'[k] + str(r)] = {'v': v}
    for k, f in (fmt or {}).items():
        cells.setdefault(k, {'v': ''}).update(f)
    return {'n': name, 'c': cells}


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.ch, a.v, a.cell, a.used, a.m, a.mac, a.runs, a.fmt, a.blocked, a.rec)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pXl({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


VENTAS = [['Mes', 'Tortas', 'Jugos', 'Snacks'], ['Ago', 120, 80, 95], ['Sep', 150, 90, 110], ['Oct', 140, 100, 105],
          ['Nov', 165, 85, 120], ['Dic', 90, 60, 70]]
PART = [['Producto', 'Ventas'], ['Tortas', 665], ['Jugos', 415], ['Snacks', 500], ['Café', 260]]
VENTAS_ERR = [r[:] for r in VENTAS]
VENTAS_ERR[4][2] = 850
HDR = {'A1': {'b': 1}, 'B1': {'b': 1}, 'C1': {'b': 1}, 'D1': {'b': 1}}
PED = [['Producto', 'Cantidad', 'Precio', 'Total'], ['Torta de jamón', 12, 35, 420], ['Jugo de naranja', 20, 18, 360],
       ['Sincronizada', 15, 25, 375], ['Café', 30, 15, 450], ['Galletas', 25, 10, 250]]
PED2 = [['Producto', 'Cantidad', 'Precio', 'Total'], ['Torta de pollo', 10, 38, 380], ['Agua fresca', 24, 15, 360],
        ['Molletes', 14, 30, 420], ['Café', 28, 15, 420], ['Fruta picada', 18, 20, 360]]
COBRO = [['Cliente', 'Grupo', 'Pedido', 'Monto', 'Estado'], ['Ana', '311', 'Torta', 35], ['Luis', '312', 'Jugo', 18],
         ['Sofía', '311', 'Café', 15], ['Diego', '313', 'Molletes', 30], ['Valeria', '312', 'Fruta', 20], ['Iván', '311', 'Torta', 35]]
MAC3 = {
    'ResaltarTotal': {'steps': [{'t': 'sel', 'a': 'D2:D6'}, {'t': 'bold'}, {'t': 'fill', 'v': '#FFE699'}, {'t': 'nf', 'v': '$#,##0.00'}],
                      'rel': False, 'sc': 't', 'desc': 'Resalta la columna Total', 'wh': 'Este libro'},
    'MacroVieja': {'steps': [{'t': 'sel', 'a': 'A1'}, {'t': 'clr'}], 'rel': False, 'sc': '', 'desc': 'Prueba que ya no se usa', 'wh': 'Este libro'},
}

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('📊', 'Una imagen vale más que mil celdas', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Una <b>gráfica</b> convierte una tabla de números en un dibujo que se entiende de un vistazo. Una <b>macro</b> es una grabación de pasos que Excel repite por ti con un clic.'),
    ex('Caso: Cafetería La Escuelita', 'La cafetería ya tiene su libro con ventas, inventario y fórmulas (R.A. 3.1 y 3.2). Ahora la directora quiere ver <b>qué producto se vende más</b> y <b>cómo cambian las ventas cada mes</b>, y el encargado está cansado de dar el mismo formato a cada hoja nueva.'),
    r3([('📊', 'A · Gráficas', 'Tipos, datos, elementos, diseño y edición.'), ('⏺️', 'B · Macros', 'Grabar, referencias, editar, ejecutar y eliminar.'), ('📁', 'Evidencia (10%)', 'Libro de trabajo digital e impreso.')])),
    'Gráficas para entender; macros para no repetir.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia', 'Un <b>libro de trabajo</b> con gráficas bien hechas y al menos dos macros funcionando, en digital (archivo .xlsm) e impreso.'),
    bk('Cómo se arma', 'Los simuladores te dejan practicar sin miedo. Las prácticas las haces en Excel (computadora) o en la app de tu celular; las macros se graban en computadora.'),
    bk('Sin computadora en casa', 'Las gráficas salen en Excel o Hojas de cálculo de Google del celular. Las macros las practicas en el simulador y las grabas en el laboratorio.', 'sp')),
    'Cada práctica es una hoja de tu libro final.')
c.A('🤔', '¿Gráfica o macro?', 'Decide qué herramienta resuelve cada necesidad de la cafetería.', [
    ['Ver de un vistazo qué producto se vende más', 'Gráfica', 'Una gráfica compara cantidades con barras o rebanadas.'],
    ['Dar el mismo formato a la hoja de cada semana', 'Macro', 'Una tarea que se repite igual es perfecta para una macro.'],
    ['Mostrar a la directora cómo subieron las ventas de agosto a noviembre', 'Gráfica', 'Una gráfica de líneas muestra la tendencia.'],
    ['Marcar como «Pagado» cada pedido con un solo atajo', 'Macro', 'La macro repite escribir y colorear en la celda que elijas.'],
    ['Comparar las ventas de tortas, jugos y snacks por mes', 'Gráfica', 'Columnas agrupadas comparan varias series.'],
], 'Gráfica = entender datos. Macro = repetir pasos.', ['Gráfica', 'Macro'])
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Gráficas ─────────────────────────
a0 = c.mark()
c.L('📊', 'Tipos de gráficos', 'Bloque A · Cada pregunta tiene su gráfica', body(
    sp('En palabras sencillas', 'El tipo de gráfica depende de la <b>pregunta</b> que quieres responder.'),
    bk('📊 Columnas / 📶 Barras', '<b>Comparar</b> cantidades entre categorías: ventas por producto, por mes. Las barras (horizontales) sirven cuando los nombres son largos.'),
    bk('📈 Líneas', 'Ver una <b>tendencia en el tiempo</b>: ¿suben o bajan las ventas mes con mes?'),
    bk('🥧 Circular (pastel)', 'Ver las <b>partes de un total</b>: qué porcentaje de las ventas es de cada producto. Solo usa <b>una serie</b> y pocas categorías (máximo 6).'),
    bk('⛰️ Área', 'Como la de líneas, pero resalta el volumen acumulado.'),
    bk('✳️ Dispersión (XY)', 'Ver si dos números se relacionan: temperatura del día contra jugos vendidos.'),
    warn('Error común', 'Usar una circular para ver meses: el pastel no muestra tendencias.')),
    'Comparar → columnas · Tiempo → líneas · Partes del total → circular.')
c.A('🎯', 'Elige la gráfica', 'Escoge el tipo de gráfica para cada pregunta.', [
    ['¿Cómo cambiaron las ventas de agosto a diciembre?', 'Líneas', 'Es una tendencia en el tiempo.'],
    ['¿Qué porcentaje de las ventas es de café?', 'Circular', 'Es una parte de un total.'],
    ['¿Qué producto vendió más en octubre?', 'Columnas', 'Comparas cantidades entre categorías.'],
    ['¿Los días más calurosos se venden más jugos?', 'Dispersión', 'Relación entre dos números.'],
    ['Comparar 10 platillos con nombres largos', 'Barras', 'Las barras horizontales dejan espacio a los nombres.'],
], 'Primero piensa en la pregunta; después en el dibujo.', ['Columnas', 'Barras', 'Líneas', 'Circular', 'Dispersión'])
c.L('🖱️', 'Seleccionar los datos', 'Bloque A · Lo que eliges es lo que se dibuja', body(
    sp('En palabras sencillas', 'Antes de insertar la gráfica, <b>selecciona la tabla con sus títulos</b>: la primera fila (nombres de las series) y la primera columna (categorías).'),
    px('Pasos en Excel', [
        'Selecciona desde la celda del título (A1) hasta el último dato (por ejemplo, D6).',
        'Ve a <b>Insertar › Gráficos</b> y elige el tipo (o usa <b>Gráficos recomendados</b>).',
        'Si te equivocaste de rango: clic en la gráfica › <b>Diseño de gráfico › Seleccionar datos</b>.']),
    bk('Celdas separadas', 'Para graficar columnas que no están juntas (por ejemplo, Mes y Snacks), selecciona la primera y mantén <b>Ctrl</b> mientras seleccionas la otra.'),
    warn('Cuidado', 'No selecciones la fila de totales junto con los meses: la gráfica mostraría el total como si fuera un mes más y aplastaría lo demás.')),
    'Selecciona títulos + datos, sin totales.')
c.L('🧩', 'Elementos de una gráfica', 'Bloque A · Las partes que la hacen entendible', body(
    bk('Título', 'Dice de qué trata: «Ventas por mes · 2026».'),
    bk('Ejes', 'El horizontal muestra las categorías (meses) y el vertical los valores (piezas vendidas). Cada eje puede llevar su <b>título</b>.'),
    bk('Series de datos', 'Cada grupo de valores con su color: Tortas, Jugos, Snacks.'),
    bk('Leyenda', 'La explicación de los colores. Se puede poner a la derecha, arriba, abajo o quitar.'),
    bk('Etiquetas de datos', 'El número escrito sobre cada barra o rebanada.'),
    bk('Dónde se agregan', 'Clic en la gráfica › <b>Diseño de gráfico › Agregar elemento de gráfico</b>, o el botón <b>+</b> junto a la gráfica.')),
    'Título + ejes con nombre + leyenda = gráfica que se lee sola.')
c.Z('🧩', 'Nombra las partes', 'Completa la descripción de la gráfica de la cafetería.',
    '<p>El texto «Ventas por mes» arriba de la gráfica es el {0}.</p>'
    '<p>Los meses Ago, Sep, Oct… aparecen en el eje {1}.</p>'
    '<p>Tortas, Jugos y Snacks son las {2} de datos.</p>'
    '<p>El cuadro que dice qué color es cada producto es la {3}.</p>'
    '<p>El número 165 encima de una barra es una {4}.</p>',
    [['título', ['título', 'eje', 'pie']], ['horizontal', ['horizontal', 'vertical', 'de profundidad']],
     ['series', ['series', 'celdas', 'hojas']], ['leyenda', ['leyenda', 'tabla', 'macro']],
     ['etiqueta de datos', ['etiqueta de datos', 'fórmula', 'leyenda']]],
    'Repasa la lección «Elementos de una gráfica».')
sim('📊', 'Tu primera gráfica de columnas', 'Simulador: selecciona datos, inserta y agrega elementos.', {
    'id': 'g1', 'mode': 'chart', 'rows': 8, 'file': 'Cafeteria_LaEscuelita.xlsx', 'sheets': [sheet('Ventas', VENTAS, HDR)],
    'intro': 'La directora quiere comparar las ventas de cada producto por mes. Para seleccionar un rango toca la <b>primera celda</b> (A1) y luego la <b>última</b> (D6).'}, [
    ['Selecciona <b>A1:D6</b> e inserta una gráfica de <b>columnas agrupadas</b>.', 'a.ch&&a.ch.type=="col"&&a.ch.rng=="A1:D6"'],
    ['En <b>Formato</b>, escribe el título «Ventas por mes».', 'a.ch&&a.ch.title&&/ventas/i.test(a.ch.tt||"")'],
    ['Agrega títulos de ejes: «Mes» y «Piezas vendidas».', 'a.ch&&a.ch.axt&&/mes/i.test(a.ch.xt||"")&&/pieza/i.test(a.ch.yt||"")'],
    ['Pon la <b>leyenda abajo</b>.', 'a.ch&&a.ch.leg=="bottom"'],
    ['Activa las <b>etiquetas de datos</b>.', 'a.ch&&a.ch.lbl']],
    'Después de insertar se activan las fichas Diseño de gráfico y Formato.')
c.L('🎨', 'Diseño del gráfico', 'Bloque A · Que se vea claro y profesional', body(
    bk('Estilos y colores', '<b>Diseño de gráfico › Cambiar colores</b> y <b>Estilos de diseño</b> cambian todo de una vez. Usa colores que se distingan entre sí.'),
    bk('Diseño rápido', 'Combinaciones listas de título, leyenda y etiquetas.'),
    bk('Cambiar tipo', 'Si elegiste mal, <b>Cambiar tipo de gráfico</b> sin volver a empezar.'),
    bk('Reglas de oro', 'Un mensaje por gráfica · sin efectos 3D que deforman · etiquetas solo si ayudan · colores con buen contraste.'),
    ex('Circular de la cafetería', 'Título «¿Qué se vende más?», etiquetas con <b>porcentaje</b> y la leyenda a la derecha: en dos segundos se ve que las tortas son casi un tercio de las ventas.')),
    'Menos adornos, más claridad.')
sim('🥧', 'Gráfica circular de participación', 'Simulador: una serie, porcentajes y colores.', {
    'id': 'g2', 'mode': 'chart', 'rows': 7, 'file': 'Cafeteria_LaEscuelita.xlsx',
    'sheets': [sheet('Ventas', VENTAS, HDR), sheet('Participación', PART, {'A1': {'b': 1}, 'B1': {'b': 1}})],
    'intro': 'Ahora la directora pregunta qué parte de las ventas es de cada producto. Cambia a la hoja <b>Participación</b> (abajo).'}, [
    ['En la hoja Participación, selecciona <b>A1:B5</b> e inserta una gráfica <b>circular</b>.', 'a.ch&&a.ch.type=="pie"&&a.ch.rng=="A1:B5"&&a.ch.src==1'],
    ['Ponle el título «¿Qué se vende más?».', 'a.ch&&a.ch.title&&/vende/i.test(a.ch.tt||"")'],
    ['Activa las etiquetas para ver los <b>porcentajes</b>.', 'a.ch&&a.ch.lbl'],
    ['Cambia la combinación de <b>colores</b>.', 'a.ch&&a.ch.pal>0']],
    'La circular usa una sola serie: la columna Ventas.')
c.L('✏️', 'Editar un gráfico', 'Bloque A · Corregir sin empezar de cero', body(
    bk('Los datos mandan', 'Si cambias un número en la tabla, la gráfica <b>se actualiza sola</b>. Por eso un error de captura se ve enseguida (una barra gigante).'),
    bk('Seleccionar datos', 'Agrega o quita meses y series: <b>Diseño de gráfico › Seleccionar datos</b>.'),
    bk('Cambiar entre filas y columnas', 'Intercambia qué se agrupa: por mes o por producto.'),
    bk('Mover gráfico', 'A una <b>hoja nueva</b> para imprimirla grande, o como objeto junto a la tabla.'),
    bk('Eliminar', 'Clic en el borde de la gráfica y tecla <b>Supr</b>.')),
    'Edita los datos o el rango; la gráfica te sigue.')
sim('✏️', 'Corrige y mejora la gráfica', 'Simulador: cambia el tipo, corrige datos, cambia el rango y muévela.', {
    'id': 'g3', 'mode': 'chart', 'rows': 8, 'file': 'Cafeteria_LaEscuelita.xlsx', 'sheets': [sheet('Ventas', VENTAS_ERR, HDR)],
    'ch': {'type': 'col', 'rng': 'A1:D6', 'src': 0, 'title': True, 'tt': 'Ventas por mes', 'leg': 'right', 'pal': 0, 'place': 'obj'},
    'intro': 'El encargado hizo esta gráfica, pero algo se ve raro. Corrígela.'}, [
    ['Una barra es gigante: corrige el error de captura (los jugos de noviembre fueron <b>85</b>).', 'a.v("C5",0)==85'],
    ['Cambia el tipo a <b>líneas</b> para ver la tendencia.', 'a.ch&&a.ch.type=="line"'],
    ['Diciembre fue de vacaciones: con <b>Seleccionar datos</b> deja solo de agosto a noviembre (<b>A1:D5</b>).', 'a.ch&&a.ch.rng=="A1:D5"'],
    ['Prueba <b>Cambiar entre filas y columnas</b> (y regrésalo si no te gusta).', 'a.used("swap")'],
    ['Mueve la gráfica a una <b>hoja nueva</b> para imprimirla.', 'a.ch&&a.ch.place=="hoja"']],
    'Para corregir un dato toca la celda, escribe el número en la barra de arriba y presiona Enter.')
c.T('🧮', 'Lee la gráfica', 'Usa la tabla de ventas de la cafetería (Ago 120/80/95 · Sep 150/90/110 · Oct 140/100/105 · Nov 165/85/120 · Dic 90/60/70). Escribe solo el número.', [
    ['¿Cuántas tortas se vendieron en total de agosto a diciembre?', '665', '120+150+140+165+90 = 665.', 'Suma la serie Tortas.', 'n'],
    ['¿Cuántas piezas más de tortas que de jugos se vendieron en noviembre?', '80', '165 − 85 = 80.', 'Resta los dos valores de noviembre.', 'n'],
    ['Si en total se vendieron 1840 piezas y 665 fueron tortas, ¿qué porcentaje es (redondeado)?', '36', '665 ÷ 1840 × 100 ≈ 36 %.', 'Parte ÷ total × 100.', 'n'],
    ['¿En cuántos meses los snacks vendieron más que los jugos?', '5', 'En los 5 meses: 95>80, 110>90, 105>100, 120>85, 70>60.', 'Compara mes por mes.', 'n'],
], 'La gráfica y la tabla dicen lo mismo: una con dibujos y otra con números.', 'n')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Macros ─────────────────────────
b0 = c.mark()
c.L('⏺️', '¿Qué es una macro?', 'Bloque B · Una grabadora de pasos', body(
    sp('En palabras sencillas', 'Una macro es una <b>serie de pasos grabados</b> que Excel repite cuando tú quieras, con un botón o un atajo de teclado. Por dentro se guarda como código <b>VBA</b> (Visual Basic para Aplicaciones).'),
    ana('Piensa en una grabadora de voz', 'Grabas una vez («negrita, relleno amarillo, bordes») y después le das play cuantas veces quieras.'),
    bk('Prepara Excel', 'Activa la ficha <b>Programador</b>: Archivo › Opciones › Personalizar cinta de opciones › marca <b>Programador</b>. (También puedes usar <b>Vista › Macros</b>.)'),
    bk('Guárdala bien', 'Un libro con macros se guarda como <b>.xlsm</b> (habilitado para macros). Si lo guardas como .xlsx, las macros <b>se pierden</b>.'),
    warn('Seguridad', 'Las macros pueden traer virus. Excel las deshabilita en archivos descargados y muestra una barra amarilla: <b>habilita solo las de archivos que tú hiciste o de alguien de confianza</b>.')),
    'Graba una vez, repite siempre. Guárdalo como .xlsm.')
c.L('🎙️', 'Grabar una macro', 'Bloque B · Paso a paso', body(
    px('Cómo se graba', [
        'Selecciona la celda donde quieres empezar.',
        '<b>Programador › Grabar macro</b>.',
        'Escribe el <b>nombre</b> (sin espacios, empieza con letra: <i>FormatoEncabezado</i>), un <b>atajo</b> (Ctrl + Mayús + letra), dónde guardarla (<b>Este libro</b>) y una <b>descripción</b>.',
        'Clic en <b>Aceptar</b>: desde ahora todo lo que hagas se graba.',
        'Haz los pasos con calma (los errores también se graban).',
        '<b>Programador › Detener grabación</b>.']),
    bk('Para ejecutarla', 'El atajo que elegiste, o <b>Programador › Macros › Ejecutar</b>.'),
    ex('En la cafetería', 'Cada semana se crea una hoja de pedidos nueva. La macro <b>FormatoEncabezado</b> pone negrita, relleno y bordes al encabezado y formato de moneda a los precios: 4 clics se vuelven 1 atajo.')),
    'Nombre sin espacios · atajo con Mayús · detener al terminar.')
c.O('🔢', 'Ordena la grabación', 'Pon en orden lo que haces para grabar una macro.', [
    ['Seleccionar la celda de inicio', 'La macro empieza desde donde estás.'],
    ['Programador › Grabar macro', 'Se abre el cuadro para configurarla.'],
    ['Escribir nombre, atajo y descripción y dar Aceptar', 'Desde aquí todo se graba.'],
    ['Hacer los pasos de formato', 'Cada acción queda registrada.'],
    ['Detener grabación', 'Si no la detienes, sigue grabando todo.'],
    ['Probarla en otra hoja', 'Así compruebas que funciona.'],
], 'Configurar → grabar → detener → probar.')
sim('⏺️', 'Graba tu primera macro', 'Simulador: graba, detén y ejecuta en otra hoja.', {
    'id': 'm1', 'mode': 'macro', 'rows': 7, 'file': 'Pedidos_semanales.xlsx',
    'sheets': [sheet('Semana1', PED), sheet('Semana2', PED2)],
    'intro': 'Graba en la hoja <b>Semana1</b> una macro que dé formato a la tabla y después úsala en <b>Semana2</b>. Para seleccionar un rango toca la primera celda y luego la última.'}, [
    ['Graba una macro llamada <b>FormatoEncabezado</b> con un atajo de una letra.', 'a.m("FormatoEncabezado")&&a.m("FormatoEncabezado").sc'],
    ['Dentro de la grabación: selecciona <b>A1:D1</b> y aplica <b>negrita</b>, un <b>relleno</b> y <b>bordes</b>.', 'a.m("FormatoEncabezado")&&["bold","fill","bd"].every(function(t){return a.m("FormatoEncabezado").steps.some(function(s){return s.t==t})})'],
    ['También dentro de la grabación: selecciona <b>C2:D6</b> y dale formato de <b>moneda</b>. Luego detén la grabación.', 'a.m("FormatoEncabezado")&&a.m("FormatoEncabezado").steps.some(function(s){return s.t=="nf"&&s.v=="$#,##0.00"})&&!a.rec'],
    ['Ve a la hoja <b>Semana2</b> y ejecuta la macro: debe quedar igual que Semana1.', 'a.cell("A1",1).b&&a.cell("D1",1).f&&a.cell("A1",1).bd&&a.cell("D6",1).nf=="$#,##0.00"'],
    ['Abre <b>Macros › Modificar</b> y mira el código que se grabó.', 'a.used("edit")']],
    'Si te equivocas mientras grabas, termina, elimina la macro y vuelve a grabarla.')
c.L('📍', 'Referencias absolutas y relativas en macros', 'Bloque B · ¿Siempre en la misma celda o desde donde estés?', body(
    sp('En palabras sencillas', 'Por defecto la macro graba <b>referencias absolutas</b>: si grabaste en A1:D1, siempre trabajará en A1:D1. Con <b>Usar referencias relativas</b> activado, graba los movimientos <b>a partir de la celda activa</b>: «una a la derecha», «una abajo».'),
    bk('Absoluta', 'Ideal para dar formato a un encabezado que siempre está en el mismo lugar. Código: <code>Range("A1:D1").Select</code>.'),
    bk('Relativa', 'Ideal para repetir algo en la fila que tú elijas: marcar un pedido como pagado. Código: <code>ActiveCell.Offset(1, 0).Range("A1").Select</code> = una celda abajo de donde estás.'),
    ana('Piensa en indicaciones', 'Absoluta: «ve a la calle Morelos 15». Relativa: «camina una cuadra a la derecha desde donde estás».'),
    warn('Actívala antes', 'El botón <b>Usar referencias relativas</b> se activa <b>antes</b> de empezar a grabar.')),
    'Absoluta = mismo lugar siempre. Relativa = desde la celda activa.')
c.A('📍', '¿Absoluta o relativa?', 'Elige el tipo de referencia que conviene para cada macro.', [
    ['Poner el título del reporte siempre en A1', 'Absoluta', 'Siempre va en la misma celda.'],
    ['Escribir «Pagado» en la fila del cliente que seleccione', 'Relativa', 'Depende de dónde estés.'],
    ['Dar formato al encabezado A1:E1 de cada hoja nueva', 'Absoluta', 'El encabezado siempre está en el mismo lugar.'],
    ['Copiar la fecha de hoy en la celda activa y bajar a la siguiente', 'Relativa', 'Se mueve a partir de la celda activa.'],
    ['Resaltar la fila completa del pedido que elijas', 'Relativa', 'Cambia según la fila seleccionada.'],
], 'Pregunta: ¿siempre en el mismo lugar, o donde yo esté?', ['Absoluta', 'Relativa'])
sim('📍', 'Macro con referencias relativas', 'Simulador: graba una macro que funcione en cualquier fila.', {
    'id': 'm2', 'mode': 'macro', 'rows': 8, 'file': 'Cobros_cafeteria.xlsx', 'sel': 'E2',
    'sheets': [sheet('Cobros', COBRO, {'A1': {'b': 1}, 'B1': {'b': 1}, 'C1': {'b': 1}, 'D1': {'b': 1}, 'E1': {'b': 1}})],
    'intro': 'Cada vez que un cliente paga, el encargado escribe «Pagado» en la columna Estado, la pinta de verde y baja a la siguiente fila. Haz que una macro lo haga.'}, [
    ['Activa <b>Usar referencias relativas</b>, deja seleccionada <b>E2</b> y empieza a grabar <b>MarcarPagado</b>.', 'a.m("MarcarPagado")&&a.m("MarcarPagado").rel||(a.rec&&a.S.rec.rel&&/marcarpagado/i.test(a.S.rec.n))'],
    ['Escribe <b>Pagado</b> en E2 (barra de arriba y Enter), ponle relleno <b>verde</b>, toca <b>E3</b> y detén la grabación.', 'a.m("MarcarPagado")&&a.m("MarcarPagado").rel&&a.m("MarcarPagado").steps.some(function(s){return s.t=="val"&&/pagado/i.test(s.v)})&&a.m("MarcarPagado").steps.some(function(s){return s.t=="fill"&&s.v=="#C6EFCE"})&&a.m("MarcarPagado").steps.some(function(s){return s.t=="sel"&&s.rel&&s.dr==1&&s.dc==0})'],
    ['Ejecuta la macro desde otras celdas de la columna E (al menos <b>2 veces</b>).', 'a.runs.filter(function(r){return /marcarpagado/i.test(r.n)}).length>=2'],
    ['Al final deben quedar al menos <b>3 pedidos</b> en «Pagado» y en verde.', '["E2","E3","E4","E5","E6","E7"].filter(function(k){var x=a.cell(k,0);return /pagado/i.test(x.v||"")&&x.f=="#C6EFCE"}).length>=3']],
    'Si la macro escribe siempre en E2, la grabaste absoluta: elimínala, activa referencias relativas y vuelve a grabar.')
c.L('🧑‍💻', 'Editar, ejecutar y eliminar macros', 'Bloque B · Administrar tus macros', body(
    bk('Ejecutar', '<b>Programador › Macros</b> › elige la macro › <b>Ejecutar</b>. O con su atajo, o asignándola a un botón (Insertar › Formas › clic derecho › Asignar macro).'),
    bk('Modificar', '<b>Macros › Modificar</b> abre el editor de Visual Basic (<b>Alt + F11</b>). Ahí puedes cambiar un color, una celda o un texto sin volver a grabar.'),
    ex('Leer el código', '<code>Selection.Interior.Color = RGB(255, 230, 153)</code> es el relleno amarillo. Los tres números son rojo, verde y azul (de 0 a 255). Cambiarlos cambia el color.'),
    bk('Eliminar', '<b>Macros</b> › elige › <b>Eliminar</b>. Borra las de prueba para no confundirte.'),
    bk('Guardar y abrir', 'Guarda como <b>.xlsm</b>. Al abrirlo de nuevo, Excel muestra «Las macros se han deshabilitado»: toca <b>Habilitar contenido</b> solo si confías en el archivo.')),
    'Modificar = cambiar el código. Eliminar = quitar la que no sirve. .xlsm = conservar macros.')
c.Z('🧑‍💻', 'Lee el código de la macro', 'Completa la explicación del código.',
    '<pre style="background:#f3f4f6;padding:10px;border-radius:8px;font:12.5px/1.5 Consolas,monospace;white-space:pre-wrap">Sub ResaltarTotal()\n    Range("D2:D6").Select\n    Selection.Font.Bold = True\n    Selection.Interior.Color = RGB(255, 230, 153)\nEnd Sub</pre>'
    '<p>La macro se llama {0}.</p><p>Trabaja siempre en el rango {1}, porque la referencia es {2}.</p>'
    '<p>La línea Font.Bold pone el texto en {3}.</p><p>Para cambiar el relleno a azul se modifican los números de {4}.</p>',
    [['ResaltarTotal', ['ResaltarTotal', 'Sub', 'Selection']], ['D2:D6', ['D2:D6', 'A1', 'toda la hoja']],
     ['absoluta', ['absoluta', 'relativa', 'circular']], ['negrita', ['negrita', 'cursiva', 'rojo']],
     ['RGB', ['RGB', 'Range', 'End Sub']]],
    'Lee cada línea como una instrucción en inglés: Select = selecciona, Bold = negrita.')
sim('🧑‍💻', 'Edita, guarda y habilita macros', 'Simulador: editor de VBA, eliminar, guardar como .xlsm y seguridad.', {
    'id': 'm3', 'mode': 'macro', 'rows': 7, 'file': 'Pedidos_semanales.xlsx', 'sheets': [sheet('Semana1', PED, HDR)], 'mac': MAC3,
    'intro': 'El encargado dejó dos macros. Ajusta una, borra la que no sirve y guarda el libro para que no se pierdan.'}, [
    ['Abre <b>Macros › Modificar</b> en ResaltarTotal y cambia el relleno a azul: <b>RGB(189, 215, 238)</b>. Guarda el código.', 'a.m("ResaltarTotal")&&a.m("ResaltarTotal").steps.some(function(s){return s.t=="fill"&&s.v=="#BDD7EE"})'],
    ['Ejecuta <b>ResaltarTotal</b> y comprueba que la columna Total quedó azul.', 'a.cell("D2",0).f=="#BDD7EE"&&a.cell("D6",0).f=="#BDD7EE"'],
    ['Elimina la macro <b>MacroVieja</b>.', '!a.m("MacroVieja")&&a.used("mdel")'],
    ['Guarda el libro como <b>habilitado para macros (.xlsm)</b>.', 'a.fmt=="xlsm"&&a.m("ResaltarTotal")'],
    ['Ciérralo y vuelve a abrirlo; lee el aviso y <b>habilita el contenido</b>.', 'a.used("reopen")&&a.used("enable")&&!a.blocked']],
    'En el editor solo cambia los tres números de RGB; si borras una comilla o un paréntesis, el editor te avisa del error.')
c.W('✍️', 'Explica tu macro', 'Escribe para qué sirve una macro que grabarías.',
    'Describe una macro que le ahorraría trabajo a la cafetería (o a ti en la escuela). Di <b>qué pasos graba</b>, si usarías referencias <b>absolutas o relativas</b> y <b>por qué</b>.',
    [['Tiene al menos 25 palabras', 'palabras:25'],
     ['Menciona pasos (formato, negrita, relleno, escribir, copiar…)', '\\b(formato|negrita|relleno|color|escrib\\w*|copi\\w*|bordes?|moneda)\\b'],
     ['Dice si es absoluta o relativa', '\\b(absolut\\w*|relativ\\w*)\\b'],
     ['Explica por qué', '\\b(porque|ya que|para que|asi)\\b']],
    'Pasos + tipo de referencia + razón.', 'Ejemplo: Grabaría una macro que…')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Serie de datos', 'Grupo de valores que se dibujan con el mismo color.'),
    bk('Categoría', 'Cada elemento del eje horizontal (meses, productos).'),
    bk('Eje', 'Línea de referencia: horizontal (categorías) y vertical (valores).'),
    bk('Leyenda', 'Explica qué color es cada serie.'),
    bk('Etiqueta de datos', 'Número escrito sobre la barra, punto o rebanada.'),
    bk('Macro', 'Pasos grabados que Excel repite automáticamente.'),
    bk('VBA', 'Visual Basic para Aplicaciones: el lenguaje en que se guardan las macros.'),
    bk('Referencia absoluta', 'La macro trabaja siempre en las mismas celdas.'),
    bk('Referencia relativa', 'La macro se mueve a partir de la celda activa.'),
    bk('.xlsm', 'Libro de Excel habilitado para macros.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311: martes 17:20-19:50, miércoles 18:10-19:50 y laboratorio el viernes 15:20-18:10. La A.E. 3.3 es el miércoles 2-dic y vale 10%. El viernes 27-nov hay evaluación del segundo corte, así que el bloque de macros se apoya en los simuladores y en una sesión de laboratorio si la consigues.', 'sp'),
    bk('Bloque A (gráficas) · 24 y 25-nov', 'Martes 24: tipos de gráficos, selección de datos y elementos; simuladores «Tu primera gráfica de columnas» y «Gráfica circular»; <b>Práctica 1</b> (se puede hacer en el celular). Miércoles 25: diseño y edición, simulador «Corrige y mejora la gráfica» y arranque del bloque B.'),
    bk('Bloque B (macros) · 25-nov y 1-dic', 'Miércoles 25: qué es una macro, cómo se graba, primer simulador. Martes 1: referencias absolutas y relativas, editar, ejecutar y eliminar; simuladores 2 y 3 y <b>Práctica 2</b> en computadora.'),
    bk('Evaluación · miércoles 2-dic', 'Entrega del libro .xlsm en la plataforma y versión impresa (gráficas y una captura del código de cada macro). El mismo día arranca el R.A. 3.4.'),
    bk('Si no hay computadoras', 'Las gráficas se hacen en Excel o Hojas de cálculo de Google del celular. Las macros se graban en el simulador: pide la captura del código y de la ejecución en otra hoja.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '📊', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '📈', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '⏺️', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"📊",t:"Empieza aquí",d:"Para qué sirven las gráficas y las macros.",time:"20 min",obj:["Distinguir cuándo usar una gráfica y cuándo una macro","Conocer la evidencia del R.A."],sum:["Gráfica = entender datos de un vistazo.","Macro = repetir pasos con un clic.","Evidencia: libro de trabajo digital e impreso (10%)."],q:"¿Qué tarea repites igual cada semana en la computadora o en el celular?"},
a:{k:"Bloque A",l:"A",ic:"📈",t:"Manejo de datos mediante gráficas",d:"Tipos de gráficos, selección de datos, elementos, diseño y edición.",time:"5 h",obj:["Elegir el tipo de gráfico según la pregunta","Seleccionar los datos correctos","Agregar título, ejes, leyenda y etiquetas","Cambiar el diseño y editar el gráfico"],sum:["Comparar → columnas · Tiempo → líneas · Partes del total → circular.","Selecciona títulos y datos, sin totales.","Título + ejes con nombre + leyenda.","Seleccionar datos, cambiar tipo, filas/columnas y mover."],q:"¿Qué gráfica usarías para mostrar tus calificaciones del semestre?"},
b:{k:"Bloque B",l:"B",ic:"⏺️",t:"Macros para automatizar tareas",d:"Grabar, referencias absolutas y relativas, editar, ejecutar y eliminar.",time:"5 h",obj:["Grabar una macro con nombre y atajo","Distinguir referencias absolutas y relativas","Leer y modificar el código VBA","Ejecutar, eliminar y guardar como .xlsm"],sum:["Grabar → hacer los pasos → detener → probar.","Absoluta = mismas celdas; relativa = desde la celda activa.","Modificar abre el editor de VBA (Alt + F11).",".xlsm conserva las macros; habilita solo archivos de confianza."],q:"¿Qué riesgo hay en abrir un archivo con macros que te mandó un desconocido?",rev:[["Para ver una tendencia mes con mes conviene una gráfica de…",["Líneas","Circular","Dispersión"],0,"Las líneas muestran cambios en el tiempo."],["Si cambias un número en la tabla, la gráfica…",["Se actualiza sola","Se borra","No cambia"],0,"La gráfica está ligada a los datos."]]}
'''

ILL = r'''
ILL["Una imagen vale más que mil celdas"]=function(){return flow([["🔢","Tabla"],["📊","Gráfica"],["💡","Decisión"]],"De los datos a la decisión")};
ILL["Tipos de gráficos"]=function(){return grid3([["📊","Columnas|comparar"],["📈","Líneas|tiempo"],["🥧","Circular|partes"],["📶","Barras|nombres largos"],["⛰️","Área|volumen"],["✳️","Dispersión|relación"]],"Tipos de gráfico y para qué sirven")};
ILL["Elementos de una gráfica"]=function(){var o=T_(170,16,"Título del gráfico","t")+'<line x1="50" y1="26" x2="50" y2="112" stroke="#888"/><line x1="50" y1="112" x2="250" y2="112" stroke="#888"/>';[[60,60,"b"],[80,40,"a"],[120,70,"b"],[140,52,"a"],[180,40,"b"],[200,30,"a"]].forEach(function(b){o+=R_(b[0],b[1],16,112-b[1],b[2],1)});o+=T_(150,128,"Eje horizontal (categorías)","tm")+T_(24,70,"Eje","tm")+R_(262,40,70,40,"s",4)+T_(297,56,"Leyenda","t")+T_(297,72,"■ Tortas ■ Jugos","tm");return SV(340,134,o,"Partes de una gráfica")};
ILL["¿Qué es una macro?"]=function(){return flow([["⏺️","Grabar"],["🖱️","Pasos"],["⏹️","Detener"],["▶️","Ejecutar|mil veces"]],"Cómo funciona una macro")};
ILL["Referencias absolutas y relativas en macros"]=function(){return SV(340,110,R_(10,14,150,80,"b",8)+T_(85,40,"Absoluta","tw")+T_(85,62,"Range(\"A1\")","tw")+T_(85,82,"siempre A1","tw")+R_(180,14,150,80,"g",8)+T_(255,40,"Relativa","tw")+T_(255,62,"Offset(1, 0)","tw")+T_(255,82,"una abajo de donde estés","tw"),"Absoluta contra relativa")};
'''

EXH = r'''
EXH.insertar=function(){return exw(mw('Insertar › Gráficos','<div class="mm"><span>Gráficos recomendados</span><span class="hl">📊 Columna agrupada '+mk(1)+'</span><span>📈 Línea</span><span>🥧 Circular</span></div>'),['Selecciona A1:D6 antes de abrir el menú.'])};
EXH.elementos=function(){return exw(mw('Diseño de gráfico › Agregar elemento de gráfico','<div class="mm"><span>Títulos de ejes ▸ '+mk(1)+'</span><span>Título del gráfico ▸</span><span>Etiquetas de datos ▸ '+mk(2)+'</span><span class="hl">Leyenda ▸ Abajo '+mk(3)+'</span></div>'),['Nombre de cada eje.','Números sobre las barras.','Posición de la leyenda.'])};
EXH.circular=function(){return exw(mw('Gráfico circular','<div style="text-align:center;font-size:44px">🥧</div><div class="mbox">Etiquetas de datos › Más opciones › ☑ Porcentaje '+mk(1)+'</div>'),['Muestra el porcentaje de cada rebanada.'])};
EXH.cel_graf=function(){return exw(mp('Excel / Hojas de cálculo','<div class="mbox">Selecciona A1:D6 › ⋮ › Insertar › Gráfico '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Editar › Tipo · Título · Leyenda '+mk(2)+'</div>'),['En Hojas de cálculo de Google: + › Gráfico.','Toca la gráfica y luego el lápiz para editarla.'])};
EXH.programador=function(){return exw(mw('Archivo › Opciones › Personalizar cinta de opciones','<div class="mbox">☑ Programador '+mk(1)+'</div>'),['Activa la ficha Programador para grabar macros.'])};
EXH.grabar=function(){return exw(mw('Grabar macro','<div class="mfld">Nombre: FormatoEncabezado '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Ctrl + Mayús + F '+mk(2)+'</div><div class="mfld" style="margin-top:6px">Guardar en: Este libro '+mk(3)+'</div>'),['Sin espacios.','Atajo.','Para que viaje con el archivo.'])};
EXH.relativa=function(){return exw(mw('Programador','<div class="mm"><span>⏺ Grabar macro</span><span class="hl">☑ Usar referencias relativas '+mk(1)+'</span><span>▶ Macros</span></div>'),['Actívala antes de grabar.'])};
EXH.vba=function(){return exw('<pre style="margin:0;background:#1e1e1e;color:#d4d4d4;padding:10px;border-radius:8px;font:12.5px/1.45 Consolas,monospace;white-space:pre-wrap">Sub FormatoEncabezado()\n    Range("A1:D1").Select '+mk(1)+'\n    Selection.Font.Bold = True\n    Selection.Interior.Color = RGB(255, 230, 153) '+mk(2)+'\nEnd Sub</pre>',['Rango absoluto.','Color: cambia los tres números y guarda.'])};
EXH.xlsm=function(){return exw(mw('Guardar como','<div class="mfld">Pedidos_semanales.xlsm</div><div class="mfld" style="margin-top:6px">Tipo: Libro de Excel habilitado para macros (*.xlsm) '+mk(1)+'</div>'),['Si eliges .xlsx, las macros se pierden.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Gráficas de la cafetería',
     'prog': 'Bloque A · Manejo de datos mediante gráficas',
     'min': 60, 'lug': 'Martes 24-nov en clase, o en casa (computadora o celular)',
     'modes': {
         'pc': {'mat': ['Computadora con Excel', 'Tu libro de los R.A. 3.1 y 3.2 (o uno nuevo)'],
                'steps': [
                    'Antes de empezar, termina los simuladores de gráficas.',
                    'Crea la hoja <b>Ventas</b> con la tabla Mes / Tortas / Jugos / Snacks de agosto a diciembre (usa los datos del material o los tuyos).',
                    ['Inserta una gráfica de <b>columnas agrupadas</b> con A1:D6.', 'insertar'],
                    ['Agrega título, títulos de ejes, leyenda abajo y etiquetas de datos.', 'elementos'],
                    ['Crea la hoja <b>Participación</b> con el total por producto e inserta una <b>circular</b> con porcentajes.', 'circular'],
                    'Haz una gráfica de <b>líneas</b> con la tendencia de agosto a noviembre y muévela a una hoja nueva.',
                    'Escribe debajo de cada gráfica una conclusión de una línea (por ejemplo: «Las tortas son el producto más vendido»).']},
         'cel': {'mat': ['Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina los simuladores de gráficas.',
                     'Crea la hoja Ventas con la tabla Mes / Tortas / Jugos / Snacks.',
                     ['Selecciona A1:D6 e inserta una gráfica de columnas. Ponle título y leyenda.', 'cel_graf'],
                     'Crea la tabla de participación e inserta una circular con porcentajes.',
                     'Cambia la primera gráfica a líneas, toma capturas y escribe una conclusión por gráfica.']}},
     'entrega': ['Hojas Ventas y Participación con tres gráficas y sus conclusiones.'],
     'rub': [['Columnas con todos sus elementos', 30], ['Circular con porcentajes', 25], ['Líneas en hoja nueva', 20], ['Conclusiones', 15], ['Diseño claro', 10]]},
    {'id': 'pr2', 'n': 2, 't': 'Macros que trabajan por ti',
     'prog': 'Bloque B · Macros para automatizar tareas',
     'min': 60, 'lug': 'Martes 1-dic en laboratorio o en casa (computadora con Excel)',
     'modes': {
         'pc': {'mat': ['Computadora con Excel para Windows o Mac'],
                'steps': [
                    'Antes de empezar, termina los tres simuladores de macros.',
                    ['Activa la ficha <b>Programador</b>.', 'programador'],
                    'Crea dos hojas de pedidos (Semana1 y Semana2) con Producto, Cantidad, Precio y Total, sin formato.',
                    ['En Semana1 graba <b>FormatoEncabezado</b> (absoluta): negrita, relleno y bordes en A1:D1 y moneda en C2:D6.', 'grabar'],
                    'Ejecútala en Semana2 y toma captura del antes y el después.',
                    ['Activa <b>Usar referencias relativas</b> y graba <b>MarcarPagado</b> en una columna Estado. Ejecútala en tres filas distintas.', 'relativa'],
                    ['Abre <b>Macros › Modificar</b>, cambia un color en el código y vuelve a ejecutarla. Toma captura del código.', 'vba'],
                    ['Guarda como <b>.xlsm</b>, ciérralo, ábrelo y habilita el contenido.', 'xlsm']]},
         'cel': {'mat': ['Celular (Excel móvil no graba macros)', 'Los simuladores de este material'],
                 'steps': [
                     'Resuelve los tres simuladores de macros y toma captura de cada uno con todos los retos en verde.',
                     'En el simulador «Graba tu primera macro», abre Modificar y toma captura del código.',
                     'Escribe en tu libro la explicación de cada línea del código.',
                     'Cuando tengas computadora (laboratorio o casa), graba FormatoEncabezado en Excel y guárdalo como .xlsm.']}},
     'entrega': ['Libro .xlsm con dos macros funcionando y capturas del código.'],
     'rub': [['Macro absoluta grabada y probada en otra hoja', 30], ['Macro relativa usada en varias filas', 30], ['Código modificado', 20], ['Guardado como .xlsm', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 3',
    'ra': 'R.A. 3.3', 'title': 'Libro de trabajo con gráficas y macros',
    'data': [
        ('Resultado de aprendizaje', 'Genera gráficas en las hojas de cálculo basadas en series de datos y automatiza tareas repetitivas con la creación y ejecución de procedimientos automatizados.'),
        ('Actividad de evaluación', '3.3.1 Realiza una hoja de cálculo en la que se grafiquen datos y se automaticen procesos mediante el uso de macros.'),
        ('Evidencia', 'Libro de trabajo digital e impreso'),
        ('Ponderación', '10% (según el programa)'),
        ('Entrega', 'Miércoles 2 de diciembre: archivo en la plataforma y versión impresa en clase'),
    ],
    'situation': 'La Cafetería La Escuelita necesita un libro que muestre sus ventas en gráficas claras y que dé formato a sus hojas de pedidos con macros. Entrega tu libro de trabajo con las gráficas y las macros de tus prácticas.',
    'hint': 'Si trabajaste en el celular, entrega el libro con las gráficas y agrega las capturas de los simuladores de macros con su código explicado.',
    'steps': [
        ('Gráficas (Bloque A)', [
            'Hoja Ventas con una gráfica de columnas con título, ejes, leyenda y etiquetas.',
            'Hoja Participación con una circular con porcentajes.',
            'Una gráfica de líneas con la tendencia, en hoja nueva, y una conclusión por gráfica.']),
        ('Macros (Bloque B)', [
            'Macro absoluta FormatoEncabezado probada en otra hoja.',
            'Macro relativa MarcarPagado usada en varias filas.',
            'Captura del código de una macro modificada, con la explicación de cada línea.']),
        ('Entrega', [
            'Archivo .xlsm (o .xlsx con las capturas de las macros si no tuviste computadora).',
            'Impresión de las gráficas y del código.']),
    ],
    'rubric': [
        ('Gráfica de columnas completa', 20), ('Gráfica circular con porcentajes', 15), ('Gráfica de líneas y conclusiones', 15),
        ('Macro absoluta funcionando', 20), ('Macro relativa funcionando', 15), ('Código modificado y explicado', 10), ('Presentación', 5),
    ],
    'deliver': ['Un archivo .xlsm (o .xlsx/PDF con capturas).', 'Nombre del archivo: Apellido_Nombre_EDOA33.', 'Súbelo en la actividad R.A. 3.3 de la plataforma y entrega la impresión en clase.'],
}
