"""EDOA-20 · R.A. 3.2 · Cálculos y funciones en la hoja de cálculo.

Continúa el caso de la Cafetería La Escuelita (R.A. 3.1): ahora la hoja ya no solo se ve bien, también calcula.
Incluye cuatro simuladores con fórmulas reales (fx_sim.js) para practicar sin computadora.
La actividad de evaluación es la entrega del libro de trabajo (.xlsx o PDF) en la plataforma.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'EDOA-RA-3.2'
CODE_PREFIX = 'EDOA32'
FILE = 'edoa-ra32-material.html'
TITLE_TAG = 'EDOA-20 · R.A. 3.2 · Cálculos y funciones'
BRAND = 'EDOA-20 · Documentos digitales avanzados'
BRAND_SUB = 'R.A. 3.2 · Cálculos y funciones'
HERO_KICK = 'EDOA-20 · R.A. 3.2'
HERO_TITLE = 'Que Excel haga las cuentas por ti'
HERO_TEXT = 'Aprende a escribir fórmulas, copiarlas sin equivocarte y usar funciones para sumar, promediar, decidir y buscar datos.'
EV_SHORT = 'entrega tu libro con fórmulas y funciones.'
EV_CARD = 'Libro de trabajo R.A. 3.2'
RA = 'R.A. 3.2'
GROUP = '311'

TABS = {'d': ['Diagnostica', 'Simuladores con fórmulas'], 'c': ['Construye', 'Prácticas en la hoja de cálculo']}

EXTRA_JS = (Path(__file__).parent / 'fx_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".fxsim"))fxInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".fxsim"))return fxCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.v, a.d, a.f, a.isf, a.eq, a.nf, a.nm, a.used, a.sheets)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pFx({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


def tbl(rows, start=1, cols='ABCDEFGHIJ'):
    out = {}
    for r, row in enumerate(rows, start):
        for col, v in zip(cols, row):
            if v is None:
                continue
            out[f'{col}{r}'] = v
    return out


# ───────────────────────── Datos de los simuladores ─────────────────────────
INV = tbl([
    ['Producto', 'Cantidad', 'Precio', 'Total', 'Con descuento'],
    ['Torta de jamón', 20, 35],
    ['Agua natural 600 ml', 48, 12],
    ['Jugo de naranja', 24, 18],
    ['Galletas de avena', 30, 10],
    ['Sincronizada', 15, 30],
    ['Fruta picada', 18, 25],
    [None],
    ['Descuento', {'v': 0.1, 'nf': 'por'}],
    ['Total sin descuento'],
    ['Meta del día', 3000],
    ['¿Se alcanzó la meta?'],
])
INV['D1'] = 'Total'

NOM1 = tbl([
    ['Producto', 'Cantidad', 'Precio'],
    ['Torta de jamón', 20, 35],
    ['Agua natural 600 ml', 48, 12],
    ['Jugo de naranja', 24, 18],
    ['Galletas de avena', 30, 10],
    ['Sincronizada', 15, 30],
    ['Fruta picada', 18, 25],
    [None],
    ['Valor del inventario'],
])
NOM2 = tbl([
    ['Concepto', 'Importe'],
    ['Valor del inventario'],
    ['IVA 16%'],
    ['Total con IVA'],
])

FEC0 = 46314
VENTAS = [
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
VD = tbl([['Fecha', 'Producto', 'Cantidad', 'Precio', 'Total', 'Vendió', 'Forma de pago']])
for r, row in enumerate(VENTAS, 2):
    for col, v in zip('ABCDEFG', row):
        VD[f'{col}{r}'] = {'v': v, 'nf': 'fec'} if col == 'A' else v
for r, (lab) in enumerate(['Total vendido', 'Promedio por venta', 'Venta más alta', 'Venta más baja', 'Número de ventas',
                            'Ventas de Lupita', 'Total de Carlos', 'Meta: $4,500'], 2):
    VD[f'I{r}'] = lab
VD['I1'] = 'Resumen'

CAT = tbl([
    ['Clave', 'Producto', 'Precio', 'Nombre limpio', 'Clave del pedido', 'A01'],
    ['T01', 'torta de jamón', 35, None, 'Producto'],
    ['A01', 'AGUA NATURAL 600 ML', 12, None, 'Precio'],
    ['J01', 'jugo de naranja', 18, None, 'Cantidad', 5],
    ['G01', 'GALLETAS DE AVENA', 10, None, 'Total'],
    ['S01', 'sincronizada', 30, None, 'Descuento'],
    ['F01', 'Fruta Picada', 25, None, 'A pagar'],
    [None, None, None, None, 'Ticket'],
    [None, None, None, None, 'Fecha del pedido'],
    [None, None, None, None, 'Entrega (3 días)'],
])

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🧮', '¿Para qué calcular en Excel?', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'En el R.A. 3.1 dejaste la hoja <b>bonita</b>. Ahora vas a lograr que <b>calcule sola</b>: escribes una <b>fórmula</b> una vez y Excel hace la cuenta, la copia a las demás filas y la <b>actualiza</b> si cambia un dato.'),
    ex('Caso: Cafetería La Escuelita', 'Doña Lupita calculaba los totales con calculadora y a veces se equivocaba. Con fórmulas, si el precio de la torta sube a $38, <b>todos los totales cambian solos</b>.'),
    r3([('➕', 'Fórmulas básicas', 'Operadores, prioridad y referencias.'), ('🧩', 'Funciones', 'SUMA, PROMEDIO, SI, BUSCARV…'), ('🧾', 'Tu libro', 'Entregas un libro que calcula.')]),
    bk('Al final', 'Entregas un <b>libro de trabajo con fórmulas y funciones</b>, digital e impreso. Vale <b>10%</b>.')),
    'Escribes la fórmula una vez; Excel la repite y la actualiza.')
c.A('🧮', '¿Dato o fórmula?', 'Para cada celda, decide si es un dato que se escribe o una fórmula que calcula.', [
    ['El precio de la torta: 35', 'Dato', 'Es un valor que tú capturas.'],
    ['El total de la torta: cantidad por precio', 'Fórmula', 'Se calcula con otras celdas.'],
    ['El nombre del proveedor', 'Dato', 'Es texto que tú escribes.'],
    ['El total del día sumando todas las ventas', 'Fórmula', 'Se calcula con las ventas.'],
    ['El porcentaje de descuento acordado: 10%', 'Dato', 'Es un valor que decides tú.'],
], 'Si sale de operar otras celdas, es fórmula.', ['Dato', 'Fórmula'])
s0_end = c.mark() - 1

# ───────────────────────── A · Fórmulas básicas ─────────────────────────
a0 = c.mark()
c.L('✍️', 'Una fórmula empieza con =', 'Bloque A · Fórmulas básicas', body(
    sp('En palabras sencillas', 'Una <b>fórmula</b> es una instrucción para que Excel calcule. Siempre empieza con el signo <b>=</b>. Sin ese signo, Excel cree que escribiste texto.'),
    bk('Cómo se escribe', 'Selecciona la celda, escribe <b>=B2*C2</b> y pulsa <b>Enter</b>. En la celda ves el <b>resultado</b>; en la barra de fórmulas ves la <b>fórmula</b>.'),
    bk('Señala en vez de teclear', 'Después del = puedes hacer <b>clic en las celdas</b> en lugar de escribir sus nombres. Así no te equivocas de referencia.'),
    ex('En la cafetería', 'En D2 está el total de la torta: <b>=B2*C2</b> (20 tortas × $35 = $700). Si cambias la cantidad en B2, el total cambia solo.'),
    warn('Ojo', 'Si escribes <b>B2*C2</b> sin el =, Excel no calcula: solo muestra el texto.')),
    'Sin = no hay fórmula · Resultado en la celda · Fórmula en la barra.')
c.L('➕', 'Operadores matemáticos', 'Bloque A · Los símbolos de las cuentas', body(
    bk('Suma, resta, multiplicación', '<b>+</b> suma · <b>−</b> resta · <b>*</b> multiplica (el asterisco, no la x).'),
    bk('División y potencia', '<b>/</b> divide · <b>^</b> eleva a una potencia: <b>=3^2</b> da 9.'),
    bk('Porcentaje', '<b>%</b> divide entre 100: <b>=200*10%</b> da 20. También puedes escribir <b>=200*0.1</b>.'),
    ana('Piensa en…', 'La calculadora del celular: los símbolos son casi los mismos. Solo cambia que por (×) es <b>*</b> y entre (÷) es <b>/</b>.'),
    ex('En la cafetería', 'Descuento de 10% a una compra de $450: <b>=450-450*10%</b> da $405.')),
    'Por = * · Entre = / · Potencia = ^ · Porcentaje = %')
c.A('➕', '¿Qué operador uso?', 'Elige el símbolo que necesitas para cada cuenta.', [
    ['Multiplicar la cantidad por el precio', '*', 'En Excel se multiplica con asterisco.'],
    ['Dividir el total entre el número de ventas', '/', 'La división es la diagonal.'],
    ['Calcular el 5% de un precio', '%', 'El porcentaje divide entre 100.'],
    ['Elevar 4 al cuadrado', '^', 'La potencia usa el acento circunflejo.'],
    ['Restar el descuento al total', '-', 'La resta es el guion.'],
], 'Piensa en cómo escribirías la cuenta en una calculadora.', ['+', '-', '*', '/', '^', '%'])
c.L('⚖️', 'Operadores de comparación', 'Bloque A · Preguntas que responde Excel', body(
    sp('En palabras sencillas', 'Comparan dos valores y responden <b>VERDADERO</b> o <b>FALSO</b>. Sirven para tomar decisiones.'),
    bk('Los seis operadores', '<b>=</b> igual · <b>&lt;&gt;</b> diferente · <b>&gt;</b> mayor que · <b>&lt;</b> menor que · <b>&gt;=</b> mayor o igual · <b>&lt;=</b> menor o igual.'),
    ex('En la cafetería', 'Si el total del día está en B10 y la meta en B11, <b>=B10&gt;=B11</b> responde VERDADERO si se llegó a la meta y FALSO si no.'),
    warn('Ojo', 'En Excel «diferente» se escribe <b>&lt;&gt;</b> (menor y mayor juntos), no ≠.')),
    'Comparar = VERDADERO o FALSO.')
c.T('⚖️', '¿VERDADERO o FALSO?', 'Escribe VERDADERO o FALSO como lo mostraría Excel.', [
    ['=5>3', 'VERDADERO', '5 sí es mayor que 3.', 'Compara 5 con 3.'],
    ['=10<=8', 'FALSO', '10 no es menor ni igual a 8.', 'Pregunta: ¿10 es menor o igual que 8?'],
    ['=4<>4', 'FALSO', '<> significa diferente y 4 es igual a 4.', '<> es «diferente».'],
    ['=12>=12', 'VERDADERO', 'Son iguales, y «mayor o igual» incluye la igualdad.', 'El igual cuenta.'],
    ['Si B2 vale 20, ¿cuánto da =B2>10?', 'VERDADERO', '20 es mayor que 10.', 'Sustituye B2 por 20.'],
], 'Responde como lo haría Excel: VERDADERO o FALSO.', 'u')
c.L('🔢', 'Prioridad de las operaciones', 'Bloque A · ¿Qué cuenta se hace primero?', body(
    sp('En palabras sencillas', 'Excel no resuelve de izquierda a derecha sin pensar: sigue el mismo orden que en matemáticas.'),
    bk('El orden', '<b>1.</b> Paréntesis ( ) · <b>2.</b> Potencias ^ · <b>3.</b> Multiplicar * y dividir / · <b>4.</b> Sumar + y restar −. Si hay empate, de izquierda a derecha.'),
    ex('Compruébalo', '<b>=2+3*4</b> da <b>14</b> (primero 3×4=12). Con paréntesis, <b>=(2+3)*4</b> da <b>20</b>.'),
    ex('En la cafetería', 'Total con descuento: <b>=B2*C2*(1-10%)</b>. Sin los paréntesis, 1-10% no se calcularía primero y el total saldría mal.'),
    warn('Regla práctica', 'Si dudas, usa paréntesis: nunca estorban.')),
    'Paréntesis → potencias → × ÷ → + −.')
c.T('🔢', '¿Qué resultado da?', 'Escribe el resultado numérico que mostraría Excel.', [
    ['=2+3*4', '14', 'Primero 3×4=12 y luego 2+12.', 'Primero se multiplica.'],
    ['=(2+3)*4', '20', 'El paréntesis se resuelve primero: 5×4.', 'Resuelve el paréntesis.'],
    ['=10-4/2', '8', 'Primero 4/2=2 y luego 10-2.', 'Primero se divide.'],
    ['=2^3+1', '9', 'Primero 2^3=8 y luego 8+1.', 'La potencia va antes de la suma.'],
    ['=100-100*10%', '90', 'Primero 100×10%=10 y luego 100-10.', 'Primero el porcentaje y la multiplicación.'],
    ['=(8+4)/(1+2)', '4', '12 entre 3.', 'Resuelve los dos paréntesis primero.'],
], 'Aplica el orden: paréntesis, potencias, × ÷, + −.', 'm')
c.L('📌', 'Referencias relativas', 'Bloque A · Copiar fórmulas sin reescribirlas', body(
    sp('En palabras sencillas', 'Una <b>referencia</b> es el nombre de una celda dentro de una fórmula (B2). Por defecto es <b>relativa</b>: al copiar la fórmula, la referencia <b>se mueve</b> igual que la fórmula.'),
    bk('Cómo se copia', 'Selecciona la celda con la fórmula y arrastra el <b>controlador de relleno</b> (el cuadrito de la esquina) hacia abajo, o usa <b>Ctrl + J</b> con el rango seleccionado.'),
    ex('En la cafetería', 'En D2: <b>=B2*C2</b>. Al copiarla una fila abajo queda <b>=B3*C3</b>; en la siguiente, <b>=B4*C4</b>. Cada producto usa sus propios datos.'),
    ana('Piensa en…', 'Una indicación «da vuelta a la derecha»: depende de dónde estés parado. La referencia relativa también depende de dónde está la fórmula.')),
    'Relativa = se mueve al copiar.')
c.L('🔒', 'Referencias absolutas y mixtas', 'Bloque A · Cuando una celda no debe moverse', body(
    sp('En palabras sencillas', 'Si todas las filas deben usar <b>la misma celda</b> (por ejemplo el descuento), pon el signo <b>$</b> antes de la letra y del número: <b>$B$9</b>. Así <b>no cambia</b> al copiar.'),
    bk('Absoluta', '<b>$B$9</b> bloquea la columna y la fila.'),
    bk('Mixta', '<b>$B9</b> bloquea solo la columna; <b>B$9</b> bloquea solo la fila.'),
    bk('Atajo', 'Con el cursor en la referencia, pulsa <b>F4</b> para pasar por B9 → $B$9 → B$9 → $B9. (En celular escribe el $ a mano.)'),
    ex('En la cafetería', 'El descuento está en B9. Total con descuento: <b>=D2-D2*$B$9</b>. Al copiar abajo, D2 se mueve (D3, D4…) pero <b>$B$9 se queda fijo</b>.'),
    warn('Si se te olvida el $', 'Sin $, la referencia baja a B10, B11… y el descuento sale en cero o mal. Es el error más común.')),
    'Absoluta ($B$9) = no se mueve · Relativa (B9) = se mueve.')
c.A('🔒', '¿En qué se convierte al copiar?', 'La fórmula está en la fila 2 y la copias a la fila 3. ¿Cómo queda?', [
    ['=B2*C2', '=B3*C3', 'Las dos referencias son relativas y bajan una fila.'],
    ['=D2-D2*$B$9', '=D3-D3*$B$9', 'D2 baja, pero $B$9 no se mueve.'],
    ['=B2*C$1', '=B3*C$1', 'B2 baja; en C$1 la fila 1 está bloqueada.'],
    ['=$B2*10%', '=$B3*10%', 'La columna B está fija y la fila baja.'],
    ['=B2/$B$8', '=B3/$B$8', 'El divisor está bloqueado en B8.'],
], 'Lo que tiene $ no se mueve.', ['=B3*C3', '=D3-D3*$B$9', '=B3*C$1', '=$B3*10%', '=B3/$B$8', '=C3*D3'])
c.O('📋', 'Ordena: calcular y copiar una fórmula', 'Pon en orden los pasos para llenar la columna de totales.', [
    ['Haz clic en la celda D2', 'Ahí va el primer total.'],
    ['Escribe =B2*C2', 'La fórmula del primer producto.'],
    ['Pulsa Enter y revisa el resultado', 'Comprueba que $700 sea correcto.'],
    ['Selecciona D2 y arrastra el controlador de relleno hasta D7', 'Se copia a todos los productos.'],
    ['Haz clic en D5 y mira la barra de fórmulas', 'Debe decir =B5*C5.'],
], 'Una fórmula, revisarla y copiarla.')
sim('🧮', 'Calcula totales y descuentos', 'Hoja de cálculo simulada con fórmulas reales: escribe en la barra y pulsa Enter.',
    {'id': 'f1', 'sheets': [{'n': 'Inventario', 'cols': 5, 'rows': 12, 'data': INV, 'hdrows': [1], 'dw': 110,
                             'cw': {'A': 170, 'B': 92, 'C': 80, 'D': 92, 'E': 112}}],
     'intro': 'Selecciona una celda (clic), escribe la fórmula en la <b>barra de fórmulas</b> y pulsa <b>Enter</b>. También puedes escribir <b>=</b> y hacer clic en las celdas. Para copiar, selecciona el rango (la primera celda con la fórmula) y usa <b>Rellenar abajo</b>.'},
    [['En <b>D2</b> escribe la fórmula del total de la torta: cantidad × precio.', 'a.isf("D2")&&a.eq("D2",700)&&/b2/.test(a.f("D2"))&&/c2/.test(a.f("D2"))'],
     ['Copia la fórmula hasta <b>D7</b> (selecciona D2:D7 y usa Rellenar abajo).', 'a.isf("D7")&&a.eq("D7",450)&&/^=b7\\*c7$/.test(a.f("D7"))'],
     ['En <b>E2</b> calcula el total con descuento usando <b>$B$9</b>: total menos descuento.', 'a.isf("E2")&&a.eq("E2",630)&&/\\$b\\$9/.test(a.f("E2"))&&/d2/.test(a.f("E2"))'],
     ['Copia la fórmula de E2 hasta <b>E7</b>. Revisa que $B$9 no se mueva.', 'a.isf("E7")&&a.eq("E7",405)&&/\\$b\\$9/.test(a.f("E7"))&&/d7/.test(a.f("E7"))'],
     ['Da formato <b>Moneda</b> a <b>D2:E7</b> (selecciona el rango y elige Moneda).', '["D2","D3","D4","D5","D6","D7","E2","E3","E4","E5","E6","E7"].every(function(k){return a.nf(k)=="mon"})'],
     ['En <b>B10</b> suma los seis totales con el operador + (D2+D3+…).', 'a.isf("B10")&&a.eq("B10",2908)&&/d2/.test(a.f("B10"))&&/d7/.test(a.f("B10"))&&a.f("B10").indexOf("+")>-1'],
     ['En <b>B12</b> compara si el total (B10) alcanzó la meta (B11): usa un operador de comparación.', 'a.isf("B12")&&a.v("B12")===false&&/b10/.test(a.f("B12"))&&/b11/.test(a.f("B12"))']],
    'Escribe el = al inicio. Para el descuento: =D2-D2*$B$9. Para la meta: =B10>=B11.')
c.L('🏷️', 'Nombres de celdas y rangos', 'Bloque A · Fórmulas que se leen solas', body(
    sp('En palabras sencillas', 'Puedes ponerle un <b>nombre</b> a una celda o a un rango y usarlo en las fórmulas. Es más fácil leer <b>=Cantidad*Precio</b> que <b>=B2:B7*C2:C7</b>.'),
    bk('Cómo ponerlo', 'Selecciona el rango, escribe el nombre en el <b>cuadro de nombres</b> (a la izquierda de la barra de fórmulas) y pulsa Enter. También: <b>Fórmulas › Asignar nombre</b>.'),
    bk('Reglas', 'Empieza con letra, <b>sin espacios</b> (usa guion bajo: Precio_torta) y no puede parecerse a una celda (como A1).'),
    bk('Usarlo', 'Escribe el nombre dentro de la fórmula: <b>=SUMA(Cantidad)</b>. Si eliges el nombre en el cuadro de nombres, Excel te lleva a ese rango.'),
    ex('En la cafetería', 'Al rango C2:C7 le pones <b>Precio</b>; al B2:B7, <b>Cantidad</b>. El valor del inventario queda: <b>=SUMA(Cantidad*Precio)</b>.')),
    'Un nombre claro hace la fórmula más fácil de entender.')
c.L('🧱', 'Fórmulas matriciales', 'Bloque A · Operar listas completas', body(
    sp('En palabras sencillas', 'Una fórmula <b>matricial</b> hace la misma cuenta con <b>todos</b> los datos de un rango a la vez y entrega un solo resultado.'),
    ex('En la cafetería', 'En vez de calcular cada total y luego sumarlos, usa <b>=SUMA(B2:B7*C2:C7)</b>: multiplica cada cantidad por su precio y suma todo. Da <b>$2,908</b> en un solo paso.'),
    bk('Cómo se escribe', 'En Excel 365 y en Hojas de cálculo de Google, solo Enter. En versiones anteriores de Excel, se confirma con <b>Ctrl + Shift + Enter</b> y la fórmula aparece entre llaves { }.'),
    warn('Ojo', 'Los dos rangos deben tener el <b>mismo tamaño</b> (6 filas con 6 filas).')),
    'Rango × rango, todo a la vez.')
c.L('📑', 'Fórmulas con varias hojas', 'Bloque A · Usar datos de otra pestaña', body(
    sp('En palabras sencillas', 'Una fórmula puede tomar una celda de <b>otra hoja</b>. Se escribe el nombre de la hoja, un signo <b>!</b> y la celda: <b>=Inventario!B9</b>.'),
    bk('Si el nombre tiene espacios', 'Va entre comillas simples: <b>=\'Ventas del día\'!E2</b>.'),
    bk('Cómo hacerlo fácil', 'Escribe el =, haz clic en la etiqueta de la otra hoja y luego clic en la celda: Excel escribe la referencia por ti.'),
    ex('En la cafetería', 'En la hoja <b>Resumen</b> hay un cuadro con el valor del inventario: <b>=Inventario!B9</b>. Si cambia el inventario, el resumen se actualiza solo.')),
    'Hoja!Celda: así se llega a otra pestaña.')
c.A('🔧', '¿Qué herramienta de fórmulas conviene?', 'Elige la mejor opción para cada situación de la cafetería.', [
    ['El descuento está en una sola celda y todas las filas deben usarla', 'Referencia absoluta ($B$9)', 'Una celda fija para todas las filas.'],
    ['Quieres leer =SUMA(Precio) en lugar de =SUMA(C2:C7)', 'Nombre de rango', 'El nombre hace la fórmula más clara.'],
    ['Multiplicar toda la columna de cantidades por la de precios y sumar en un paso', 'Fórmula matricial', 'Opera rangos completos a la vez.'],
    ['El resumen debe mostrar un dato que está en la hoja Inventario', 'Referencia a otra hoja', 'Se usa Hoja!Celda.'],
    ['Cada total debe usar la cantidad y el precio de su propia fila', 'Referencia relativa', 'Se mueve al copiar.'],
], 'Piensa: ¿debe moverse, tener nombre, operar listas o venir de otra hoja?',
    ['Referencia absoluta ($B$9)', 'Nombre de rango', 'Fórmula matricial', 'Referencia a otra hoja', 'Referencia relativa'])
c.Z('✍️', 'Completa: fórmulas básicas', 'Elige la palabra correcta.',
    '<p>Toda fórmula empieza con el signo {0}.</p>'
    '<p>La multiplicación se escribe con {1}.</p>'
    '<p>Para que una referencia no se mueva al copiar, se escribe con {2}.</p>'
    '<p>Una comparación responde {3}.</p>'
    '<p>Para llegar a otra hoja se usa el signo {4}.</p>',
    [['=', ['=', '+', '@']], ['*', ['*', 'x', '^']], ['$', ['$', '#', '&']],
     ['VERDADERO o FALSO', ['VERDADERO o FALSO', 'un número', 'un texto']], ['!', ['!', '?', ':']]],
    'Repasa las lecciones del Bloque A.')
sim('🏷️', 'Nombres, matrices y varias hojas', 'Hoja de cálculo simulada con dos hojas: nombra rangos y relaciona las hojas.',
    {'id': 'f2', 'sheets': [{'n': 'Inventario', 'cols': 3, 'rows': 9, 'data': NOM1, 'hdrows': [1], 'dw': 110, 'cw': {'A': 170}},
                            {'n': 'Resumen', 'cols': 2, 'rows': 4, 'data': NOM2, 'hdrows': [1], 'dw': 120, 'cw': {'A': 170}}],
     'intro': 'Abajo hay dos hojas: <b>Inventario</b> y <b>Resumen</b>. Para dar nombre a un rango, selecciónalo y usa <b>Definir nombre</b> (arriba) o escribe el nombre y pulsa el botón.'},
    [['En <b>Inventario</b>, selecciona <b>B2:B7</b> y dale el nombre <b>Cantidad</b>.', '/!b2:b7$/i.test(a.nm("Cantidad"))'],
     ['Selecciona <b>C2:C7</b> y dale el nombre <b>Precio</b>.', '/!c2:c7$/i.test(a.nm("Precio"))'],
     ['En <b>B9</b> calcula el valor del inventario con una fórmula matricial: <b>=SUMA(Cantidad*Precio)</b>.', 'a.isf("B9")&&a.eq("B9",2908)&&/cantidad/.test(a.f("B9"))&&/precio/.test(a.f("B9"))'],
     ['Escribe <b>Precio</b> en el cuadro de nombres y pulsa Enter: Excel selecciona el rango.', '!!a.used.nbn'],
     ['En la hoja <b>Resumen</b>, celda <b>B2</b>: trae el valor del inventario con <b>=Inventario!B9</b>.', 'a.isf("B2","Resumen")&&a.eq("B2",2908,"Resumen")&&/^=inventario!b9$/.test(a.f("B2","Resumen"))'],
     ['En <b>Resumen!B3</b> calcula el IVA: el valor del inventario (B2) por 16%.', 'a.isf("B3","Resumen")&&a.eq("B3",465.28,"Resumen")&&/b2/.test(a.f("B3","Resumen"))'],
     ['En <b>Resumen!B4</b> suma el valor y el IVA (B2 + B3).', 'a.isf("B4","Resumen")&&a.eq("B4",3373.28,"Resumen")&&/b2/.test(a.f("B4","Resumen"))&&/b3/.test(a.f("B4","Resumen"))']],
    'Selecciona el rango antes de pulsar «Definir nombre». Para otra hoja, cambia con la etiqueta de abajo.')
a_end = c.mark() - 1

# ───────────────────────── B · Funciones ─────────────────────────
b0 = c.mark()
c.L('🧩', '¿Qué es una función?', 'Bloque B · Fórmulas ya hechas', body(
    sp('En palabras sencillas', 'Una <b>función</b> es una fórmula que Excel ya trae lista para una tarea: sumar, promediar, buscar… Solo le dices con qué datos trabajar.'),
    bk('Cómo se escribe', '<b>=NOMBRE(argumentos)</b>. Los <b>argumentos</b> van entre paréntesis y separados por comas. Ejemplo: <b>=SUMA(B2:B7)</b>.'),
    bk('Cómo encontrarlas', 'El botón <b>fx</b> junto a la barra de fórmulas abre el <b>asistente</b> con todas, agrupadas por categoría. La <b>Autosuma (Σ)</b> de Inicio inserta SUMA en un clic.'),
    bk('Las categorías', 'Matemáticas · Fecha y hora · Estadística · Texto · Búsqueda · Lógica.'),
    ana('Piensa en…', 'Una licuadora: tú pones la fruta (argumentos) y ella sabe cómo licuar (función).'),
    warn('Ojo', 'Todo paréntesis que abres debe cerrarse. Excel colorea los pares para ayudarte.')),
    '=FUNCIÓN(argumentos) · fx abre el asistente.')
c.L('🧮', 'Funciones matemáticas', 'Bloque B · Cuentas más rápidas', body(
    bk('SUMA', '<b>=SUMA(E2:E15)</b> suma todo el rango. También: <b>=SUMA(B2;B5;B9)</b> para celdas sueltas.'),
    bk('PRODUCTO', '<b>=PRODUCTO(B2:C2)</b> multiplica todo el rango.'),
    bk('REDONDEAR', '<b>=REDONDEAR(10/3;2)</b> da <b>3.33</b>: número y cuántos decimales.'),
    bk('ENTERO y RESIDUO', '<b>=ENTERO(7.8)</b> da 7 (quita decimales hacia abajo). <b>=RESIDUO(17;5)</b> da 2 (lo que sobra al dividir).'),
    bk('SUMAR.SI', '<b>=SUMAR.SI(F2:F15;"Carlos";E2:E15)</b> suma los totales <b>solo de Carlos</b>: rango a revisar, condición y rango a sumar.'),
    ex('En la cafetería', 'Total vendido: <b>=SUMA(E2:E15)</b> ($4,571). Lo que vendió Carlos: <b>=SUMAR.SI(F2:F15,"Carlos",E2:E15)</b> ($2,268).')),
    'SUMA suma · SUMAR.SI suma con condición · REDONDEAR da decimales.')
c.L('📅', 'Funciones de fecha y hora', 'Bloque B · Excel y el calendario', body(
    sp('Cómo funciona', 'Excel guarda cada fecha como un <b>número de días</b>; por eso se puede sumar y restar fechas.'),
    bk('HOY y AHORA', '<b>=HOY()</b> muestra la fecha de hoy y se actualiza sola. <b>=AHORA()</b> agrega la hora. Llevan paréntesis vacíos.'),
    bk('AÑO, MES, DIA', '<b>=AÑO(F2)</b>, <b>=MES(F2)</b> y <b>=DIA(F2)</b> sacan una parte de la fecha.'),
    bk('FECHA y DIAS', '<b>=FECHA(2026;11;20)</b> arma una fecha. <b>=DIAS(F2;F1)</b> cuenta los días entre dos fechas.'),
    ex('En la cafetería', 'Entrega del pedido en tres días: <b>=HOY()+3</b>. Días que faltan para la entrega: <b>=DIAS(F10;HOY())</b>.'),
    warn('Si ves un número raro', 'Aplica formato <b>Fecha corta</b> a la celda: es el mismo número, pero con otra presentación (como en el R.A. 3.1).')),
    'HOY() cambia sola · Las fechas se pueden sumar y restar.')
c.L('📊', 'Funciones estadísticas', 'Bloque B · Entender un conjunto de datos', body(
    bk('PROMEDIO', '<b>=PROMEDIO(E2:E15)</b>: suma entre cuántos datos hay ($326.50 por venta).'),
    bk('MAX y MIN', '<b>=MAX(E2:E15)</b> el más grande ($630); <b>=MIN(E2:E15)</b> el más pequeño ($200).'),
    bk('CONTAR', '<b>=CONTAR(E2:E15)</b> cuenta cuántas celdas tienen <b>números</b>. <b>=CONTARA</b> cuenta las que tienen cualquier cosa.'),
    bk('CONTAR.SI', '<b>=CONTAR.SI(F2:F15;"Lupita")</b> cuenta cuántas veces aparece «Lupita».'),
    bk('MEDIANA y MODA', '<b>MEDIANA</b> es el valor de en medio (con los datos ordenados); <b>MODA</b> es el que más se repite.'),
    ana('Piensa en…', 'Tus calificaciones: promedio es tu calificación final, MAX tu mejor examen y MIN el peor.')),
    'Promedio, máximo, mínimo y cuántos hay.')
c.A('🧰', '¿Qué función uso?', 'Elige la función que resuelve cada pregunta de la cafetería.', [
    ['¿Cuánto se vendió en total en la semana?', 'SUMA', 'Suma todo el rango.'],
    ['¿Cuánto vendió Carlos solamente?', 'SUMAR.SI', 'Suma solo las ventas que cumplen la condición.'],
    ['¿Cuál fue la venta más alta?', 'MAX', 'Busca el valor mayor.'],
    ['¿Cuánto se vendió en promedio por venta?', 'PROMEDIO', 'Es el total entre el número de ventas.'],
    ['¿Cuántas ventas hizo Lupita?', 'CONTAR.SI', 'Cuenta las celdas que cumplen la condición.'],
    ['¿Cuál fue la venta más baja?', 'MIN', 'Busca el valor menor.'],
    ['¿Qué fecha es hoy, siempre actualizada?', 'HOY', 'Se actualiza cada vez que abres el libro.'],
], 'Fíjate en la palabra clave: total, promedio, más alta, cuántas…', ['SUMA', 'SUMAR.SI', 'MAX', 'MIN', 'PROMEDIO', 'CONTAR.SI', 'HOY'])
c.T('⌨️', 'Escribe la fórmula', 'Escribe la fórmula completa. No importan las mayúsculas ni los espacios.', [
    ['Sumar las celdas de B2 a B7', '=SUMA(B2:B7)', 'Función SUMA con el rango B2:B7.', 'Empieza con = y usa dos puntos.'],
    ['El promedio de C2 a C9', '=PROMEDIO(C2:C9)', 'PROMEDIO con el rango C2:C9.', 'Promedio = PROMEDIO.'],
    ['El valor más alto de E2 a E15', '=MAX(E2:E15)', 'MAX con el rango.', 'MAX de máximo.'],
    ['Cuántas celdas con número hay de D2 a D20', '=CONTAR(D2:D20)', 'CONTAR cuenta números.', 'Contar = CONTAR.'],
    ['Hoy', '=HOY()', 'HOY lleva paréntesis vacíos.', 'No lleva argumentos.'],
], 'Se escribe =NOMBRE(rango).', 'c')
c.L('🔤', 'Funciones de texto', 'Bloque B · Arreglar y unir palabras', body(
    bk('MAYUSC, MINUSC, NOMPROPIO', '<b>=MAYUSC("torta")</b> da TORTA · <b>=MINUSC(…)</b> da minúsculas · <b>=NOMPROPIO("agua natural")</b> da <b>Agua Natural</b>.'),
    bk('IZQUIERDA y DERECHA', '<b>=IZQUIERDA(A2;3)</b> toma los 3 primeros caracteres; <b>=DERECHA(A2;2)</b> los 2 últimos.'),
    bk('EXTRAE y LARGO', '<b>=EXTRAE(A2;2;3)</b> toma 3 caracteres desde la posición 2. <b>=LARGO(A2)</b> cuenta cuántos caracteres tiene.'),
    bk('Unir textos', 'El signo <b>&amp;</b> une: <b>=A2&amp;" "&amp;B2</b>. También <b>CONCATENAR</b>. El texto escrito va entre <b>comillas</b>.'),
    ex('En la cafetería', 'La lista del proveedor viene con mayúsculas y minúsculas mezcladas. <b>=NOMPROPIO(B2)</b> la deja pareja.')),
    'Texto entre comillas · & une · NOMPROPIO acomoda.')
c.L('🔎', 'Funciones de búsqueda', 'Bloque B · Encontrar un dato en una tabla', body(
    sp('En palabras sencillas', '<b>BUSCARV</b> busca un valor en la <b>primera columna</b> de una tabla y te trae un dato de la misma fila. Es como buscar un nombre en el directorio y leer su teléfono.'),
    bk('Cómo se escribe', '<b>=BUSCARV(qué busco; dónde; qué columna; FALSO)</b>'),
    bk('Los 4 argumentos', '<b>1.</b> El valor a buscar (A01). <b>2.</b> La tabla, con la clave en la <b>primera columna</b> (A2:C7). <b>3.</b> El <b>número de columna</b> que quieres traer. <b>4.</b> <b>FALSO</b> para coincidencia exacta.'),
    ex('En la cafetería', 'El catálogo tiene Clave, Producto y Precio. <b>=BUSCARV("A01";A2:C7;3;FALSO)</b> da el precio $12 del agua natural.'),
    bk('Otras', '<b>COINCIDIR</b> dice en qué posición está un valor; <b>INDICE</b> trae el valor de una posición. Juntas hacen búsquedas más flexibles.'),
    warn('Ojo', 'Si la clave no existe, Excel muestra <b>#N/D</b>. No es un error tuyo: ese dato no está en la tabla.')),
    'BUSCARV: busca en la primera columna y trae otra columna de esa fila.')
c.L('🤔', 'Funciones lógicas', 'Bloque B · Que Excel decida', body(
    sp('En palabras sencillas', 'La función <b>SI</b> hace una pregunta y da una respuesta si es verdadera y otra si es falsa.'),
    bk('SI', '<b>=SI(pregunta; si es verdadero; si es falso)</b>. Ejemplo: <b>=SI(B4&gt;=5;10%;0)</b>: si compran 5 o más, descuento de 10%; si no, cero.'),
    bk('Y y O', '<b>=Y(B4&gt;=5;C4&gt;20)</b> es verdadero solo si se cumplen <b>las dos</b>. <b>=O(…)</b> lo es si se cumple <b>al menos una</b>. <b>=NO(…)</b> invierte el resultado.'),
    bk('SI.ERROR', '<b>=SI.ERROR(A1/B1;"Revisa los datos")</b> muestra un mensaje en vez de un error como #¡DIV/0!.'),
    ex('En la cafetería', '<b>=SI(J2&gt;=4500;"Meta lograda";"Falta vender")</b> escribe el mensaje según las ventas de la semana.'),
    warn('Ojo', 'Los textos van entre comillas; los números y las referencias, no.')),
    'SI decide · Y exige todo · O acepta una.')
c.A('🤔', '¿Qué resultado da?', 'Con B4 = 6, ¿qué muestra la celda?', [
    ['=SI(B4>=5;"Con descuento";"Sin descuento")', 'Con descuento', '6 es mayor o igual que 5.'],
    ['=SI(B4<3;"Poco";"Mucho")', 'Mucho', '6 no es menor que 3.'],
    ['=Y(B4>5;B4<10)', 'VERDADERO', '6 está entre 5 y 10: se cumplen las dos.'],
    ['=O(B4=1;B4=2)', 'FALSO', 'B4 no es 1 ni 2.'],
    ['=NO(B4>10)', 'VERDADERO', 'B4>10 es falso y NO lo invierte.'],
    ['=SI(B4=6;"Seis";"Otro")', 'Seis', 'B4 es igual a 6.'],
], 'Sustituye B4 por 6 y responde la pregunta.', ['Con descuento', 'Sin descuento', 'Poco', 'Mucho', 'VERDADERO', 'FALSO', 'Seis'])
c.O('🪄', 'Ordena: insertar una función con el asistente', 'Pon en orden los pasos para usar PROMEDIO desde el botón fx.', [
    ['Selecciona la celda donde irá el resultado', 'Primero decide dónde se verá.'],
    ['Haz clic en el botón fx de la barra de fórmulas', 'Abre el asistente de funciones.'],
    ['Elige la categoría Estadística y la función PROMEDIO', 'Ahí está PROMEDIO.'],
    ['Selecciona el rango de datos y da Aceptar', 'Son los argumentos.'],
    ['Revisa en la barra de fórmulas que diga =PROMEDIO(…)', 'Siempre comprueba el resultado.'],
], 'fx → categoría → función → argumentos → revisar.')
c.Z('🧩', 'Completa: funciones', 'Elige la palabra o función correcta.',
    '<p>Para sumar un rango uso {0}.</p>'
    '<p>Para tomar una decisión uso {1}.</p>'
    '<p>Para traer un precio de un catálogo uso {2}.</p>'
    '<p>Para que una fecha se actualice sola uso {3}.</p>'
    '<p>Para dejar «agua natural» como «Agua Natural» uso {4}.</p>'
    '<p>Los textos dentro de una fórmula van entre {5}.</p>',
    [['SUMA', ['SUMA', 'CONTAR', 'MAX']], ['SI', ['SI', 'HOY', 'LARGO']], ['BUSCARV', ['BUSCARV', 'PROMEDIO', 'ENTERO']],
     ['HOY', ['HOY', 'FECHA', 'DIA']], ['NOMPROPIO', ['NOMPROPIO', 'MAYUSC', 'EXTRAE']], ['comillas', ['comillas', 'paréntesis', 'llaves']]],
    'Repasa las lecciones del Bloque B.')
sim('📊', 'Resume las ventas de la semana', 'Hoja de cálculo simulada: usa funciones matemáticas, estadísticas y lógicas.',
    {'id': 'f3', 'sheets': [{'n': 'Ventas', 'cols': 10, 'rows': 15, 'data': VD, 'hdrows': [1], 'dw': 78,
                             'cw': {'A': 86, 'B': 150, 'C': 74, 'D': 64, 'E': 70, 'F': 70, 'G': 104, 'H': 20, 'I': 150, 'J': 110}}],
     'names': False,
     'intro': 'Las ventas de la cafetería están en <b>A1:G15</b>. Escribe en la columna <b>J</b> las funciones que responden cada pregunta de la columna I. Tip: después del = escribe el nombre de la función y arrastra para señalar el rango.'},
    [['<b>J2</b> · Total vendido: suma de <b>E2:E15</b>.', 'a.isf("J2")&&a.eq("J2",4571)&&/suma\\(/.test(a.f("J2"))'],
     ['<b>J3</b> · Promedio por venta.', 'a.isf("J3")&&a.eq("J3",326.5)&&/promedio\\(/.test(a.f("J3"))'],
     ['<b>J4</b> · Venta más alta.', 'a.isf("J4")&&a.eq("J4",630)&&/max\\(/.test(a.f("J4"))'],
     ['<b>J5</b> · Venta más baja.', 'a.isf("J5")&&a.eq("J5",200)&&/min\\(/.test(a.f("J5"))'],
     ['<b>J6</b> · Cuántas ventas hay (cuenta los totales).', 'a.isf("J6")&&a.eq("J6",14)&&/contar\\(/.test(a.f("J6"))'],
     ['<b>J7</b> · Cuántas ventas hizo Lupita, con <b>CONTAR.SI</b>.', 'a.isf("J7")&&a.eq("J7",8)&&/contar\\.si\\(/.test(a.f("J7"))'],
     ['<b>J8</b> · Total de Carlos, con <b>SUMAR.SI</b>.', 'a.isf("J8")&&a.eq("J8",2268)&&/sumar\\.si\\(/.test(a.f("J8"))'],
     ['<b>J9</b> · Con <b>SI</b>, escribe «Meta lograda» si el total (J2) llega a $4,500 y «Falta vender» si no.', 'a.isf("J9")&&String(a.v("J9")).toLowerCase()=="meta lograda"&&/si\\(/.test(a.f("J9"))&&/j2/.test(a.f("J9"))'],
     ['Da formato <b>Moneda</b> a <b>J2:J5</b> y <b>J8</b>.', '["J2","J3","J4","J5","J8"].every(function(k){return a.nf(k)=="mon"})']],
    'Ejemplo: =SUMA(E2:E15). Para J7: =CONTAR.SI(F2:F15,"Lupita"). Para J8: =SUMAR.SI(F2:F15,"Carlos",E2:E15).')
sim('🔎', 'Haz un pedido: texto, fechas y búsqueda', 'Hoja de cálculo simulada: limpia textos, busca en un catálogo y toma decisiones.',
    {'id': 'f4', 'sheets': [{'n': 'Catálogo', 'cols': 6, 'rows': 10, 'data': CAT, 'hdrows': [1], 'dw': 100,
                             'cw': {'A': 56, 'B': 170, 'C': 62, 'D': 170, 'E': 130, 'F': 170}}],
     'names': False,
     'intro': 'Doña Lupita recibe un pedido. En <b>F1</b> está la clave del producto y en <b>F4</b> la cantidad. Completa la columna <b>F</b> con fórmulas. Cambia la clave en F1 (por ejemplo a <b>S01</b>) para ver que todo se actualiza solo.'},
    [['<b>D2</b> · Pon el nombre de B2 con mayúscula inicial en cada palabra (NOMPROPIO) y cópialo hasta <b>D7</b>.', 'a.isf("D2")&&/nompropio\\(/.test(a.f("D7"))&&a.v("D7")=="Fruta Picada"&&a.v("D3")=="Agua Natural 600 Ml"'],
     ['<b>F2</b> · Busca el producto de la clave de F1 con <b>BUSCARV</b> (columna 2).', 'a.isf("F2")&&/buscarv\\(/.test(a.f("F2"))&&String(a.v("F2")).toLowerCase()=="agua natural 600 ml"&&/f1/.test(a.f("F2"))'],
     ['<b>F3</b> · Trae el precio con <b>BUSCARV</b> (columna 3).', 'a.isf("F3")&&/buscarv\\(/.test(a.f("F3"))&&a.eq("F3",12)'],
     ['<b>F5</b> · Total: cantidad (F4) por precio (F3).', 'a.isf("F5")&&a.eq("F5",60)&&/f3/.test(a.f("F5"))&&/f4/.test(a.f("F5"))'],
     ['<b>F6</b> · Con <b>SI</b>: descuento de 10% si la cantidad es 5 o más; si no, 0.', 'a.isf("F6")&&/si\\(/.test(a.f("F6"))&&a.eq("F6",0.1)&&/f4/.test(a.f("F6"))'],
     ['<b>F7</b> · A pagar: el total menos el descuento.', 'a.isf("F7")&&a.eq("F7",54)&&/f5/.test(a.f("F7"))&&/f6/.test(a.f("F7"))'],
     ['<b>F8</b> · Ticket de texto: producto con NOMPROPIO, « x », cantidad, « = » y lo que se paga. Ej.: <i>Agua Natural 600 Ml x 5 = 54</i>.', 'a.isf("F8")&&a.v("F8")=="Agua Natural 600 Ml x 5 = 54"&&/nompropio\\(/.test(a.f("F8"))'],
     ['<b>F9</b> · Fecha del pedido con <b>HOY()</b> (formato Fecha corta) y en <b>F10</b> la entrega tres días después.', 'a.isf("F9")&&/hoy\\(\\)/.test(a.f("F9"))&&a.nf("F9")=="fec"&&a.isf("F10")&&a.v("F10")==a.v("F9")+3&&/f9|hoy/.test(a.f("F10"))']],
    'Ejemplos: =NOMPROPIO(B2) · =BUSCARV(F1,A2:C7,2,FALSO) · =SI(F4>=5,10%,0) · =NOMPROPIO(F2)&" x "&F4&" = "&F7')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Fórmula', 'Instrucción que empieza con = y hace un cálculo.'),
    bk('Operador', 'Símbolo de una operación: + − * / ^ % o de comparación.'),
    bk('Referencia', 'Nombre de una celda dentro de una fórmula (B2).'),
    bk('Relativa / absoluta / mixta', 'B2 se mueve · $B$2 no se mueve · B$2 o $B2 se mueve a medias.'),
    bk('Rango con nombre', 'Un rango al que le pones un nombre (Precio).'),
    bk('Fórmula matricial', 'Opera rangos completos en una sola fórmula.'),
    bk('Función', 'Fórmula ya hecha: SUMA, PROMEDIO, SI, BUSCARV…'),
    bk('Argumento', 'Dato que le das a una función, entre paréntesis.'),
    bk('Controlador de relleno', 'Cuadrito de la esquina que copia fórmulas al arrastrar.'),
    bk('VERDADERO / FALSO', 'Los dos resultados de una comparación.'),
    bk('#N/D · #¡DIV/0! · #¿NOMBRE?', 'Errores: no se encontró el dato · división entre cero · nombre mal escrito.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 311: martes 17:20-19:50, miércoles 18:10-19:50 y laboratorio el viernes 15:20-18:10. La A.E. 3.2 es el 20-nov y vale 10%. Los simuladores funcionan sin computadora y las prácticas tienen versión para celular.', 'sp'),
    bk('Bloque A (fórmulas) · 4, 6 y 10-nov', 'Miércoles 4: fórmula, operadores y prioridad. Viernes 6 (laboratorio): referencias, simulador «Calcula totales y descuentos» y <b>Práctica 1</b>. Martes 10: nombres, matrices, varias hojas y el segundo simulador.'),
    bk('Bloque B (funciones) · 11, 13 y 17-nov', 'Miércoles 11: funciones matemáticas y estadísticas. Viernes 13 (laboratorio): fecha y hora, texto y <b>Práctica 2</b>. Martes 17: búsqueda y lógica, simulador final y <b>Práctica 3</b>.'),
    bk('Evaluación · 18 y 20-nov', 'Miércoles 18: repaso y revisión del libro con la lista de cotejo. Viernes 20: A.E. 3.2, libro digital en la plataforma y versión impresa.'),
    bk('Nota', 'La actividad de evaluación se desbloquea al completar este material. Si hay corte o evaluación del 9 al 11 de noviembre, mueve el Bloque A una sesión y ajusta las fechas.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🧮', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '✍️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🧩', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🧮",t:"Empieza aquí",d:"Para qué calcular en Excel y qué vas a entregar.",time:"15 min",obj:["Distinguir un dato de una fórmula","Conocer el caso y la evidencia final"],sum:["Escribes la fórmula una vez; Excel la repite y la actualiza.","Entregas un libro con fórmulas y funciones."],q:"¿Qué cuentas haces a mano en tu casa o tu escuela que Excel podría hacer por ti?"},
a:{k:"Bloque A",l:"A",ic:"✍️",t:"Manejo de fórmulas básicas",d:"Operadores, prioridad, referencias, nombres, matrices y varias hojas.",time:"150 min",obj:["Escribir fórmulas con operadores matemáticos y de comparación","Copiar fórmulas con referencias relativas, absolutas y mixtas","Usar nombres de rango, fórmulas matriciales y datos de otra hoja"],sum:["Toda fórmula empieza con =.","Relativa se mueve; $B$9 no se mueve.","Hoja!Celda llega a otra pestaña."],q:"¿Qué le pasaría a tus totales si se te olvida el $ en el descuento y copias la fórmula hacia abajo?",rev:[["¿Qué da =2+3*4?",["14","20","24"],0,"Primero se multiplica 3×4."],["Para que una celda no se mueva al copiar se usa…",["$","&","!"],0,"Con $ se bloquea la referencia."]]},
b:{k:"Bloque B",l:"B",ic:"🧩",t:"Operaciones con funciones",d:"Matemáticas, fecha y hora, estadística, texto, búsqueda y lógica.",time:"200 min",obj:["Insertar funciones con el asistente y escribirlas a mano","Elegir la función adecuada en cada categoría","Combinar funciones para decidir y buscar datos"],sum:["=NOMBRE(argumentos).","SUMA, PROMEDIO, MAX, MIN y CONTAR.SI resumen datos.","SI decide y BUSCARV encuentra datos."],q:"¿Qué dato de tu casa o escuela podrías buscar con BUSCARV en una tabla?",rev:[["Para contar cuántas veces aparece «Lupita» uso…",["CONTAR.SI","SUMA","MAX"],0,"CONTAR.SI cuenta las que cumplen la condición."],["BUSCARV busca el valor en…",["La primera columna de la tabla","La última fila","Otra hoja siempre"],0,"La clave debe estar en la primera columna."]]}
'''

ILL = r'''
ILL["Operadores matemáticos"]=function(){return grid3([["➕","Suma|+"],["➖","Resta|−"],["✖️","Multiplica|*"],["➗","Divide|/"],["⬆️","Potencia|^"],["％","Porcentaje|%"]],"Operadores de Excel")};
ILL["Prioridad de las operaciones"]=function(){return grid3([["1️⃣","Paréntesis|( )"],["2️⃣","Potencias|^"],["3️⃣","× y ÷|* /"],["4️⃣","+ y −|+ -"]],"Orden de las operaciones")};
ILL["Referencias absolutas y mixtas"]=function(){return grid3([["↕️","Relativa|B9"],["🔒","Absoluta|$B$9"],["📌","Mixta|$B9 o B$9"]],"Tipos de referencia")};
ILL["¿Qué es una función?"]=function(){return grid3([["🧮","Matemáticas"],["📅","Fecha y hora"],["📊","Estadística"],["🔤","Texto"],["🔎","Búsqueda"],["🤔","Lógica"]],"Categorías de funciones")};
'''

EXH = r'''
function xw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><div style="background:#fff;color:#111;padding:8px;font:13px system-ui;overflow-x:auto">'+b+'</div></div>'}
function xt_(rows,hd){return '<table style="border-collapse:collapse;font:12.5px system-ui">'+rows.map(function(r,i){return '<tr>'+r.map(function(c){return '<td style="border:1px solid '+(hd?'#111':'#e5e7eb')+';padding:3px 8px;'+(i==0&&hd?'background:#1e3a8a;color:#fff;font-weight:700;text-align:center':'')+'">'+c+'</td>'}).join("")+'</tr>'}).join("")+'</table>'}
EXH.formula=function(){return exw(xw_('Excel · Inventario','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">D2</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =B2*C2</span>'+mk(1)+'</div>'+xt_([["Producto","Cantidad","Precio","Total"],["Torta de jamón","20","$35.00","$700.00 "+mk(2)],["Agua natural","48","$12.00","$576.00"]],true)),['La fórmula siempre empieza con = y aparece en la barra de fórmulas.','El resultado se ve en la celda.'])};
EXH.absoluta=function(){return exw(xw_('Referencia absoluta','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">E3</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =D3-D3*$B$9</span>'+mk(1)+'</div>'+xt_([["Producto","Total","Con descuento"],["Torta","$700.00","$630.00"],["Agua","$576.00","$518.40 "+mk(2)],["Descuento","10% "+mk(3),""]])),['$B$9 no cambia al copiar.','El resultado de la fila copiada.','La celda del descuento, fija para todos.'])};
EXH.nombres=function(){return exw(xw_('Cuadro de nombres','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">Precio</span>'+mk(1)+'<span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =SUMA(Cantidad*Precio)</span>'+mk(2)+'</div>'+xt_([["Cantidad","Precio"],["20","$35.00"],["48","$12.00"]])),['El nombre del rango en el cuadro de nombres.','La fórmula que usa los nombres.'])};
EXH.otrahoja=function(){return exw(xw_('Resumen · fórmula con otra hoja','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">B2</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =Inventario!B9</span>'+mk(1)+'</div><div style="background:#f3f4f6;padding:3px 8px">Inventario | Resumen '+mk(2)+'</div>'),['Nombre de la hoja, signo ! y la celda.','Las etiquetas de las hojas.'])};
EXH.asistente=function(){return exw(xw_('Insertar función','<b>Categoría:</b> Estadística '+mk(1)+'<br><b>Función:</b> PROMEDIO '+mk(2)+'<br><b>Número1:</b> E2:E15 '+mk(3)+'<br><span style="float:right;border:1px solid #999;padding:2px 10px">Aceptar</span>'),['La categoría de la función.','El nombre de la función.','El rango, es decir, el argumento.'])};
EXH.funciones=function(){return exw(xw_('Hoja «Ventas»','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">J2</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =SUMA(E2:E15)</span>'+mk(1)+'</div>'+xt_([["Resumen",""],["Total vendido","$4,571.00 "+mk(2)],["Promedio","$326.50"],["Venta más alta","$630.00"]])),['Función con su rango.','El resultado.'])};
EXH.buscarv=function(){return exw(xw_('Catálogo','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">F3</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =BUSCARV(F1;A2:C7;3;FALSO)</span>'+mk(1)+'</div>'+xt_([["Clave","Producto","Precio"],["T01","Torta de jamón","$35.00"],["A01","Agua natural","$12.00 "+mk(2)]],true)),['Qué busco, dónde, qué columna y búsqueda exacta.','El dato que trae de la fila de la clave.'])};
EXH.si=function(){return exw(xw_('Función SI','<div style="display:flex;gap:6px;margin-bottom:6px"><span style="border:1px solid #ccc;padding:2px 8px">F6</span><span style="border:1px solid #ccc;padding:2px 8px;flex:1"><i>fx</i> =SI(F4&gt;=5;10%;0)</span>'+mk(1)+'</div>'+xt_([["Cantidad","5"],["Descuento","10% "+mk(2)]])),['Pregunta, si es verdadero y si es falso.','El resultado cambia con la cantidad.'])};
EXH.cel=function(){return exw(mp('Hojas de cálculo · celular','<div class="mbox">✏️ Toca la celda › escribe <b>=</b> y la fórmula '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Botón <b>fx</b> › elige la función por categoría '+mk(2)+'</div><div class="mbox" style="margin-top:6px">Mantén presionada una celda › Copiar y Pegar para repetir la fórmula '+mk(3)+'</div>'),['La fórmula siempre empieza con =.','El botón fx abre las funciones.','Al pegar, las referencias relativas se ajustan solas.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Tu libro que calcula: fórmulas básicas',
     'prog': 'Bloque A · Manejo de fórmulas básicas',
     'min': 60, 'lug': 'Viernes 6-nov en laboratorio, o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con Excel', 'Tu libro del R.A. 3.1 (o uno nuevo)'],
                'steps': [
                    'Antes de empezar, termina los simuladores «Calcula totales y descuentos» y «Nombres, matrices y varias hojas».',
                    ['Abre tu libro (o crea uno) y arma la hoja <b>Inventario</b> con al menos 8 productos: producto, cantidad y precio. Escribe en D2 el total (<b>=B2*C2</b>) y cópialo a todas las filas.', 'formula'],
                    ['Pon una celda de descuento (o IVA) y calcula una columna «Con descuento» con referencia absoluta <b>$</b>. Copia la fórmula y comprueba la barra de fórmulas en dos filas.', 'absoluta'],
                    ['Ponle nombre a los rangos de cantidad y precio y calcula el valor del inventario con una fórmula matricial.', 'nombres'],
                    ['Crea una hoja <b>Resumen</b> que traiga el valor del inventario con una fórmula como <b>=Inventario!B9</b> y que calcule el IVA y el total.', 'otrahoja'],
                    'Agrega una celda con una comparación (por ejemplo, ¿alcanzó la meta?) y toma captura de la vista «Mostrar fórmulas» (Fórmulas › Mostrar fórmulas).']},
         'cel': {'mat': ['Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina los simuladores «Calcula totales y descuentos» y «Nombres, matrices y varias hojas».',
                     ['Crea la hoja <b>Inventario</b> con al menos 8 productos (producto, cantidad y precio). Toca D2, escribe <b>=B2*C2</b> y cópiala a las demás filas (mantén presionada la celda › Copiar, y pega en D3:D9).', 'cel'],
                     ['Agrega una celda de descuento y calcula «Con descuento» con referencia absoluta (escribe el $ a mano).', 'absoluta'],
                     ['Crea una hoja <b>Resumen</b> con una fórmula que traiga el valor total de la hoja Inventario (<b>=Inventario!B9</b>).', 'otrahoja'],
                     'Agrega una comparación (¿alcanzó la meta?) y toma captura de tu hoja.']}},
     'entrega': ['El libro con las hojas Inventario y Resumen funcionando; lo sigues usando en las prácticas 2 y 3.'],
     'rub': [['Totales con fórmula copiada a todas las filas', 25], ['Referencia absoluta bien usada', 25], ['Nombres y fórmula matricial', 20], ['Hoja Resumen con datos de otra hoja', 20], ['Comparación', 10]]},
    {'id': 'pr2', 'n': 2, 't': 'Resume tus datos con funciones',
     'prog': 'Bloque B · Funciones matemáticas, estadísticas, fecha y hora',
     'min': 60, 'lug': 'Viernes 13-nov en laboratorio, o en casa',
     'modes': {
         'pc': {'mat': ['Tu libro de la práctica 1', 'Computadora con Excel'],
                'steps': [
                    'Antes de empezar, termina el simulador «Resume las ventas de la semana».',
                    ['Crea la hoja <b>Ventas</b> con al menos 12 registros (fecha, producto, cantidad, precio, total, quién vendió y forma de pago). Calcula el total de cada registro con una fórmula.', 'funciones'],
                    ['En una zona de resumen usa <b>SUMA, PROMEDIO, MAX, MIN y CONTAR</b>. Revisa con el asistente <b>fx</b> al menos una de ellas.', 'asistente'],
                    'Usa <b>CONTAR.SI</b> y <b>SUMAR.SI</b> para responder: ¿cuántas ventas hizo una persona y cuánto vendió?',
                    'Agrega la fecha de hoy con <b>HOY()</b> y una fecha de entrega con <b>HOY()+7</b>, ambas con formato de fecha.',
                    'Redondea el promedio a dos decimales con REDONDEAR y da formato Moneda al resumen.']},
         'cel': {'mat': ['Tu libro de la práctica 1', 'Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Resume las ventas de la semana».',
                     ['Crea la hoja <b>Ventas</b> con al menos 12 registros y una fórmula de total por registro.', 'cel'],
                     ['Usa el botón <b>fx</b> para insertar SUMA, PROMEDIO, MAX y MIN en una zona de resumen.', 'cel'],
                     'Usa CONTAR.SI y SUMAR.SI para responder cuántas ventas y cuánto vendió una persona.',
                     'Agrega HOY() y HOY()+7 con formato de fecha, y redondea el promedio a dos decimales.']}},
     'entrega': ['La hoja Ventas con su resumen; es parte de tu libro final.'],
     'rub': [['Total por registro con fórmula', 20], ['SUMA, PROMEDIO, MAX, MIN y CONTAR', 30], ['CONTAR.SI y SUMAR.SI', 25], ['Fechas con HOY y formato', 15], ['Resumen con formato', 10]]},
    {'id': 'pr3', 'n': 3, 't': 'Decisiones, textos y búsquedas',
     'prog': 'Bloque B · Funciones de texto, búsqueda y lógicas',
     'min': 70, 'lug': 'Martes 17-nov en clase, o en casa',
     'modes': {
         'pc': {'mat': ['Tu libro de las prácticas 1 y 2', 'Computadora con Excel'],
                'steps': [
                    'Antes de empezar, termina el simulador «Haz un pedido: texto, fechas y búsqueda».',
                    ['Crea la hoja <b>Catálogo</b> con al menos 8 productos (clave, producto en mayúsculas y minúsculas mezcladas, precio). Pon una columna con <b>NOMPROPIO</b> para dejar los nombres parejos.', 'buscarv'],
                    ['Arma un pedido: una celda para la clave y otra para la cantidad. Con <b>BUSCARV</b> trae el producto y el precio, y calcula el total.', 'buscarv'],
                    ['Con <b>SI</b> aplica un descuento cuando la cantidad pase de cierto número, y con <b>SI.ERROR</b> muestra «Clave no encontrada» si la clave no existe.', 'si'],
                    'Arma un ticket de texto uniendo producto, cantidad y total con el signo &amp;.',
                    'Revisa tu libro completo: cambia un dato y comprueba que todo se actualice. Guarda y revisa la lista de cotejo de la evaluación.']},
         'cel': {'mat': ['Tu libro de las prácticas 1 y 2', 'Celular con Excel o Hojas de cálculo de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Haz un pedido: texto, fechas y búsqueda».',
                     ['Crea la hoja <b>Catálogo</b> con al menos 8 productos (clave, producto y precio).', 'cel'],
                     ['Arma un pedido con clave y cantidad, y trae el producto y el precio con <b>BUSCARV</b>.', 'buscarv'],
                     ['Usa <b>SI</b> para dar descuento si la cantidad pasa de cierto número.', 'si'],
                     'Une producto, cantidad y total en un ticket de texto con &amp; y revisa que todo cambie al modificar un dato.']}},
     'entrega': ['El libro terminado con hojas Inventario, Resumen, Ventas y Catálogo: es la base de tu actividad de evaluación.'],
     'rub': [['NOMPROPIO y datos limpios', 15], ['BUSCARV con producto y precio', 30], ['SI y SI.ERROR', 25], ['Ticket de texto', 10], ['El libro se actualiza solo', 20]]},
]

EVALUATION = {
    'course': 'EDOA-20 · Elaboración de documentos digitales avanzados · Unidad 3',
    'ra': 'R.A. 3.2', 'title': 'Libro de trabajo con fórmulas y funciones',
    'data': [
        ('Resultado de aprendizaje', 'Realiza cálculos y aplica funciones para simplificar operaciones de uso cotidiano para una mayor interpretación de la información.'),
        ('Actividad de evaluación', '3.2.1 Elabora una hoja de cálculo con fórmulas básicas (operadores y referencias) y funciones de varias categorías.'),
        ('Evidencia', 'Libro de trabajo digital e impreso'),
        ('Ponderación', '10% (según el programa)'),
        ('Entrega', 'Viernes 20 de noviembre: archivo en la plataforma y versión impresa en clase'),
    ],
    'situation': 'Un negocio o grupo de tu comunidad (la cafetería, la tienda de tu colonia, los gastos de tu grupo o el inventario de tu casa) necesita que sus cuentas se hagan solas. Entrega el <b>libro de trabajo</b> de tus tres prácticas con fórmulas y funciones, <b>sin datos calculados a mano</b>.',
    'hint': 'Cambia un dato cualquiera: si todo lo calculado se actualiza solo, vas bien. Revisa esta lista con tu libro abierto.',
    'steps': [
        ('Fórmulas básicas', [
            'Fórmulas con operadores matemáticos (+, −, *, /, ^, %) y al menos una comparación.',
            'Una fórmula copiada con referencia <b>relativa</b> y otra con referencia <b>absoluta o mixta</b> ($).',
            'Al menos un rango con nombre y una fórmula que use datos de otra hoja.']),
        ('Funciones', [
            'Matemáticas: SUMA y alguna más (REDONDEAR, SUMAR.SI, PRODUCTO…).',
            'Estadísticas: PROMEDIO, MAX, MIN y CONTAR o CONTAR.SI.',
            'Fecha y hora: HOY o AHORA y alguna función de fecha.',
            'Texto: al menos una (NOMPROPIO, MAYUSC, IZQUIERDA, & …).',
            'Búsqueda: BUSCARV (o COINCIDIR e INDICE) bien aplicada.',
            'Lógicas: SI y, si puedes, Y, O o SI.ERROR.']),
        ('Presentación', [
            'Formato claro: título, encabezados, moneda/porcentaje/fecha y bordes (lo aprendido en el R.A. 3.1).',
            'Una hoja con las fórmulas visibles (Fórmulas › Mostrar fórmulas) para la versión impresa.']),
        ('Entrega', [
            'Cambia un dato y comprueba que los resultados se actualizan.',
            'Sube tu archivo .xlsx (o su PDF) en la actividad R.A. 3.2 de la plataforma y entrega la versión impresa en clase.']),
    ],
    'rubric': [
        ('Fórmulas básicas con operadores', 15), ('Referencias relativas, absolutas y mixtas', 15),
        ('Nombres, matriz y varias hojas', 10), ('Funciones matemáticas y estadísticas', 20),
        ('Funciones de fecha, texto y búsqueda', 15), ('Funciones lógicas', 15), ('Presentación y versión impresa', 10),
    ],
    'deliver': ['Un archivo .xlsx (o PDF) con todas tus hojas.', 'Nombre del archivo: Apellido_Nombre_EDOA32.', 'Súbelo en la actividad R.A. 3.2 de la plataforma y entrega la impresión en clase.'],
}
