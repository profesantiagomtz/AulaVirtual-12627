"""MTCS-20 · R.A. 3.2 · Estructuras de flujo de control y funciones (Python).

Continúa el caso del Ciber Lab escolar (R.A. 3.1): ahora el programa decide quién entra, cuenta intentos,
recorre listas de registros, usa bits para permisos, se organiza en funciones y maneja excepciones.
Usa el laboratorio de Python (py_sim.js) en modo completo (cfg.full): if, while, for, def, try.
La actividad de evaluación vive en la plataforma (MtcsActivity, con escenario asignado y PDF).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, html, j

CODE = 'MTCS-RA-3.2'
CODE_PREFIX = 'MTCS32'
FILE = 'mtcs-ra32-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 3.2 · Flujo de control y funciones'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 3.2 · Flujo de control y funciones'
HERO_KICK = 'MTCS-20 · R.A. 3.2'
HERO_TITLE = 'Programas que deciden, repiten y se organizan'
HERO_TEXT = 'Haz que tu programa tome decisiones, repita tareas, trabaje con listas, use funciones y no se caiga ante un error.'
EV_SHORT = 'elabora tu reporte de flujo de control con el escenario asignado.'
EV_CARD = 'Reporte R.A. 3.2'
RA = 'R.A. 3.2'
GROUP = '511'

TABS = {'d': ['Diagnostica', 'Laboratorio de Python'], 'c': ['Construye', 'Prácticas de programación']}

EXTRA_JS = (Path(__file__).parent / 'py_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".pysim"))pyInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".pysim"))return pyCheck(d);\n'),
]

c = Course()


def lab(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.out, a.ok, a.t, a.v, a.r, a.uses, a.printed, a.comments, a.lines, a.src,
    a.fn(nombre), a.used, a.run([entradas]) → {out, err, used}, a.ev("expresión") → repr o "ERR:Tipo")]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pPy({j(ic)},{j(t)},{j(inf)},{{full:true,tasks:{ts},hint:{j(hint)}{extra}}})')


def code(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return html('<pre style="background:#0d1117;color:#e6edf3;padding:10px 12px;border-radius:10px;font:13px/1.5 Consolas,monospace;overflow-x:auto;white-space:pre;margin:10px 0">' + s + '</pre>')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🔀', 'El Ciber Lab ahora decide', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'En el R.A. 3.1 tus programas ejecutaban las instrucciones <b>una tras otra</b>. Ahora vas a controlar el <b>flujo</b>: que el programa <b>decida</b> (if), <b>repita</b> (for, while), guarde muchos datos en <b>listas</b>, se divida en <b>funciones</b> y <b>no se caiga</b> cuando algo sale mal (try).'),
    ex('Caso: Ciber Lab escolar', 'El control de acceso del laboratorio debe: dejar entrar solo con la clave correcta, bloquear la cuenta después de 3 intentos, revisar la lista de registros del día para encontrar sospechosos y avisar si alguien escribe letras donde van números. Todo eso es flujo de control.'),
    r3([('🔀', 'A · Procesamiento', 'Condiciones, ciclos, operadores lógicos y de bits, listas y algoritmos.'), ('🧩', 'B · Funciones', 'Parámetros, retorno, valores y excepciones.'), ('📄', 'Reporte (15%)', 'Programas con tu escenario asignado.')])),
    'Decidir, repetir, organizar y prevenir errores.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencia (15%)', 'Un <b>reporte en PDF</b> que demuestre el uso de estructuras de flujo de control y funciones con el <b>escenario asignado</b> en la actividad de la plataforma: tu código en Python, capturas de la salida y tus explicaciones.'),
    bk('Cómo usar este material', 'Cada tema tiene un <b>laboratorio de Python</b> que corre aquí, sin instalar nada. Los retos se marcan solos y algunos prueban tu programa con <b>otros datos</b> para comprobar que de verdad funciona.'),
    warn('La sangría importa', 'En Python, lo que va <b>dentro</b> de un if, for, while, def o try se escribe con <b>4 espacios</b> al inicio. En el laboratorio, Enter después de «:» agrega la sangría sola y Tab inserta 4 espacios.')),
    'Siete laboratorios, tres prácticas y un reporte.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Procesamiento ─────────────────────────
a0 = c.mark()
c.L('🔀', 'Sentencias condicionales y toma de decisiones', 'Bloque A · if, elif y else', body(
    sp('En palabras sencillas', 'Una <b>condición</b> es una pregunta de sí o no (True o False). Con <b>if</b> el programa ejecuta un bloque solo si la respuesta es True.'),
    code('clave = input("Clave: ")\nif clave == "Ciber2026":\n    print("Acceso concedido")\nelse:\n    print("Acceso denegado")'),
    bk('elif', 'Para más de dos caminos: <code>if</code> → <code>elif</code> → <code>elif</code> → <code>else</code>. Python revisa en orden y ejecuta <b>solo el primero</b> que sea True.'),
    bk('Reglas de escritura', 'La línea termina con <b>dos puntos</b> (:). El bloque va con <b>4 espacios</b>. Para comparar se usa <b>==</b>, no =.'),
    ex('Orden de las decisiones', 'Primero se revisa si la cuenta está bloqueada; después, si la clave es correcta. Si lo hicieras al revés, alguien con la cuenta bloqueada podría entrar.')),
    'if pregunta, elif pregunta otra cosa, else atrapa todo lo demás.')
c.L('🔣', 'Operadores lógicos', 'Bloque A · and, or y not', body(
    bk('and', 'True solo si <b>las dos</b> condiciones son True: <code>usuario == "ana" and clave == "Ciber2026"</code>.'),
    bk('or', 'True si <b>al menos una</b> es True: <code>usuario == "invitado" or usuario == "visita"</code>.'),
    bk('not', 'Invierte: <code>not bloqueado</code> es True cuando bloqueado es False.'),
    ex('Tabla de verdad', '<table class="mtb"><tr><th>A</th><th>B</th><th>A and B</th><th>A or B</th></tr><tr><td>True</td><td>True</td><td>True</td><td>True</td></tr><tr><td>True</td><td>False</td><td>False</td><td>True</td></tr><tr><td>False</td><td>True</td><td>False</td><td>True</td></tr><tr><td>False</td><td>False</td><td>False</td><td>False</td></tr></table>')),
    'and = ambas · or = alguna · not = lo contrario.')
c.T('🔣', '¿True o False?', 'Con usuario = "ana", clave = "1234" e intentos = 2, escribe True o False.', [
    ['usuario == "ana" and clave == "Ciber2026"', ['False'], 'La clave no coincide; con and basta una falsa.', 'and necesita las dos.'],
    ['usuario == "ana" or clave == "Ciber2026"', ['True'], 'El usuario sí coincide; con or basta una.', 'or necesita al menos una.'],
    ['not intentos >= 3', ['True'], 'intentos >= 3 es False; not lo vuelve True.', 'Primero la comparación, luego not.'],
    ['intentos > 0 and intentos < 3', ['True'], '2 está entre 0 y 3.', 'Revisa las dos partes.'],
    ['len(clave) >= 12 or clave.isdigit() == False', ['False'], 'La clave mide 4 y sí son dígitos: las dos son False.', 'Evalúa cada lado.'],
], 'Resuelve cada lado y luego combina.', 'u')
lab('🧪', 'Decide quién entra', 'Laboratorio de Python: if, elif, else, and y or.',
    {'id': 'q1', 'code': '# Control de acceso del Ciber Lab\nusuario = input("Usuario: ")\nclave = input("Clave: ")\nintentos = int(input("Intentos fallidos: "))\n', 'inputs': 'ana\nCiber2026\n1',
     'intro': 'El programa ya lee tres datos. Completa las decisiones. Algunos retos prueban tu programa con <b>otras entradas</b> además de las del cuadro.'},
    [['Con <b>if/else</b> muestra <b>Acceso concedido</b> si la clave es <b>Ciber2026</b> y <b>Acceso denegado</b> si no.', 'a.ok&&a.uses(/\\bif\\b/)&&a.uses(/\\belse\\s*:/)&&a.run(["ana","Ciber2026","0"]).out.indexOf("Acceso concedido")>-1&&a.run(["ana","1234","0"]).out.indexOf("Acceso denegado")>-1'],
     ['Agrega un <b>elif</b> (o revisa primero) para que con <b>3 o más</b> intentos muestre <b>Cuenta bloqueada</b>, aunque la clave sea correcta.', 'a.uses(/\\belif\\b/)&&a.run(["ana","Ciber2026","3"]).out.indexOf("Cuenta bloqueada")>-1&&a.run(["ana","Ciber2026","3"]).out.indexOf("concedido")<0&&a.run(["ana","Ciber2026","2"]).out.indexOf("Acceso concedido")>-1'],
     ['Con <b>and</b>: solo entra el usuario <b>ana</b> con su clave (luis con Ciber2026 debe ser denegado).', 'a.uses(/\\band\\b/)&&a.run(["luis","Ciber2026","0"]).out.indexOf("Acceso denegado")>-1&&a.run(["ana","Ciber2026","0"]).out.indexOf("Acceso concedido")>-1'],
     ['Con <b>or</b>: si el usuario es <b>invitado</b> o <b>visita</b>, muestra <b>Acceso solo a Internet</b>.', 'a.uses(/\\bor\\b/)&&a.run(["invitado","x","0"]).out.indexOf("Acceso solo a Internet")>-1&&a.run(["visita","x","0"]).out.indexOf("Acceso solo a Internet")>-1']],
    'Pon primero la condición de bloqueo, luego la de invitado y al final la clave. Cada bloque lleva 4 espacios.')
c.L('🔁', 'Bucles e iteraciones', 'Bloque A · while y for', body(
    sp('En palabras sencillas', 'Un <b>bucle</b> repite un bloque. Cada repetición es una <b>iteración</b>.'),
    bk('while', 'Repite <b>mientras</b> la condición sea True. Úsalo cuando no sabes cuántas veces: «pide la clave mientras sea incorrecta y queden intentos».'),
    code('intentos = 0\nwhile intentos < 3:\n    clave = input("Clave: ")\n    if clave == "Ciber2026":\n        print("Acceso concedido")\n        break\n    intentos += 1'),
    bk('for', 'Recorre una <b>secuencia</b> elemento por elemento: una lista, un texto o <code>range()</code>. Úsalo cuando sabes cuántas veces.'),
    code('for i in range(1, 6):\n    print(f"PC-{i:02d}")'),
    bk('range', '<code>range(5)</code> → 0,1,2,3,4 · <code>range(1, 6)</code> → 1 a 5 · <code>range(0, 10, 2)</code> → 0,2,4,6,8.'),
    bk('break y continue', '<code>break</code> sale del bucle de inmediato. <code>continue</code> salta al siguiente ciclo sin terminar el actual.'),
    warn('Ciclo infinito', 'Si la condición del while nunca se vuelve False, el programa no termina. Asegúrate de que algo cambie dentro del ciclo (intentos += 1).')),
    'while = mientras · for = para cada · break = salir · continue = saltar.')
c.O('🔢', 'Ordena el bucle de intentos', 'Ordena las líneas para pedir la clave hasta 3 veces y salir al acertar.', [
    ['intentos = 0', 'Primero se prepara el contador.'],
    ['while intentos < 3:', 'Se repite mientras queden intentos.'],
    ['    clave = input("Clave: ")', 'Dentro del ciclo se pide la clave.'],
    ['    if clave == "Ciber2026":', 'Se revisa si es correcta.'],
    ['        break', 'Si acierta, sale del ciclo.'],
    ['    intentos += 1', 'Si no, se cuenta el intento.'],
], 'Preparar, repetir, pedir, revisar, salir o contar.')
lab('🧪', 'Repite con control', 'Laboratorio de Python: while, for, range, break y continue.',
    {'id': 'q2', 'code': '# Hasta 3 intentos para entrar\nintentos = 0\n', 'inputs': 'hola\nCiber2026',
     'intro': 'Escribe un <b>while</b> que pida la clave hasta 3 veces. Las entradas ya traen un error y luego la clave correcta.'},
    [['Con <b>while</b> pide la clave hasta 3 veces y usa <b>break</b> al acertar: con «hola, Ciber2026» debe mostrar <b>Acceso concedido</b> y pedir solo 2 veces.', 'a.uses(/\\bwhile\\b/)&&a.uses(/\\bbreak\\b/)&&(function(r){return r.out.indexOf("Acceso concedido")>-1&&r.used==2})(a.run(["hola","Ciber2026","x"]))'],
     ['Si falla 3 veces, al final muestra <b>Cuenta bloqueada</b>.', '(function(r){return r.out.indexOf("Cuenta bloqueada")>-1&&r.used==3})(a.run(["a","b","c","d"]))&&a.run(["Ciber2026"]).out.indexOf("bloqueada")<0'],
     ['Con <b>for</b> y <b>range</b> muestra los equipos <b>PC-01</b> a <b>PC-05</b> (pista: f"PC-{i:02d}").', 'a.ok&&a.uses(/\\bfor\\b[^\\n]*\\brange\\s*\\(/)&&a.printed("PC-01")&&a.printed("PC-05")&&!a.printed("PC-06")'],
     ['El <b>PC-03</b> está en mantenimiento: sáltalo con <b>continue</b>.', 'a.ok&&a.uses(/\\bcontinue\\b/)&&!a.printed("PC-03")&&a.printed("PC-04")']],
    'Dentro del while: pide la clave, revisa con if, usa break si acierta y suma 1 a intentos. Después del while, revisa si intentos llegó a 3.')
c.L('🧮', 'Operaciones bit a bit', 'Bloque A · &, |, ^, ~, << y >>', body(
    sp('En palabras sencillas', 'Los números se guardan en binario (unos y ceros). Los operadores bit a bit trabajan <b>bit por bit</b>. En seguridad se usan para <b>permisos</b>, máscaras de red y cifrados sencillos.'),
    bk('Permisos como bits', 'Leer = 4 (<code>100</code>), Escribir = 2 (<code>010</code>), Ejecutar = 1 (<code>001</code>). Leer y escribir = <code>110</code> = 6. Así funcionan los permisos de Linux (chmod 640).'),
    bk('Operadores', '<code>a | b</code> OR: junta permisos · <code>a &amp; b</code> AND: revisa si tiene uno · <code>a ^ b</code> XOR: cambia (prende o apaga) · <code>~a</code> invierte · <code>a &lt;&lt; n</code> recorre a la izquierda (multiplica por 2ⁿ) · <code>a &gt;&gt; n</code> a la derecha (divide).'),
    code('LEER, ESCRIBIR, EJECUTAR = 4, 2, 1\npermisos = LEER | ESCRIBIR      # 6\nprint((permisos & ESCRIBIR) != 0)  # True: sí puede escribir\nprint(bin(permisos))             # 0b110'),
    ex('Máscara de red', '192 AND 255 = 192 · 37 AND 0 = 0: la máscara 255.255.255.0 «deja pasar» la parte de red con AND.')),
    '| junta · & revisa · ^ cambia · << y >> recorren.')
c.T('🧮', 'Calcula con bits', 'Escribe el resultado en decimal.', [
    ['4 | 1', '5', '100 | 001 = 101 = 5.', 'Junta los bits encendidos.', 'n'],
    ['6 & 2', '2', '110 & 010 = 010 = 2.', 'Solo quedan los bits que están en los dos.', 'n'],
    ['7 ^ 2', '5', '111 ^ 010 = 101 = 5.', 'XOR apaga el bit que coincide.', 'n'],
    ['1 << 3', '8', '1 recorrido 3 lugares = 1000 = 8.', 'Multiplica por 2 tres veces.', 'n'],
    ['20 >> 2', '5', '20 ÷ 4 = 5.', 'Divide entre 2 dos veces.', 'n'],
], 'Pasa a binario, opera bit por bit y regresa a decimal.', 'n')
lab('🧪', 'Permisos con bits', 'Laboratorio de Python: operadores bit a bit para permisos.',
    {'id': 'q3', 'code': '# Permisos de un archivo del Ciber Lab\nLEER = 4\nESCRIBIR = 2\nEJECUTAR = 1\n',
     'intro': 'Cada permiso es un bit. Combínalos y revísalos con los operadores bit a bit.'},
    [['Crea <b>permisos</b> con LEER y ESCRIBIR usando <b>|</b> (debe valer 6).', 'a.v("permisos")==6&&a.uses(/\\|/)'],
     ['Crea <b>puede_escribir</b> revisando con <b>&amp;</b> si permisos tiene ESCRIBIR (debe ser True).', 'a.t("puede_escribir")=="bool"&&a.v("puede_escribir")===true&&a.uses(/&/)'],
     ['Crea <b>solo_lectura</b> quitando ESCRIBIR con <b>^</b> o con <b>&amp; ~</b> (debe valer 4).', 'a.v("solo_lectura")==4&&a.uses(/\\^|&\\s*~/)'],
     ['Muestra <b>permisos</b> en binario con <b>bin()</b> o con f"{permisos:03b}".', 'a.ok&&(a.printed("0b110")||a.printed("110"))&&a.uses(/bin\\s*\\(|:0?3?b\\}/)'],
     ['Crea <b>ADMIN</b> recorriendo un 1 tres lugares con <b>&lt;&lt;</b> (debe valer 8).', 'a.v("ADMIN")==8&&a.uses(/<</)']],
    'Juntar: a | b. Revisar: (a & b) != 0. Quitar: a ^ b. Binario: bin(a).')
c.L('📋', 'Listas', 'Bloque A · Guardar muchos datos en una sola variable', body(
    bk('Crear y leer', '<code>registros = ["ana", "luis", "sofia"]</code> · <code>registros[0]</code> es el primero · <code>registros[-1]</code> el último · <code>len(registros)</code> cuántos hay.'),
    bk('Operaciones con listas', '<code>append(x)</code> agrega al final · <code>insert(i, x)</code> en una posición · <code>remove(x)</code> quita · <code>pop()</code> saca el último · <code>count(x)</code> cuenta · <code>index(x)</code> dice dónde está · <code>x in lista</code> pregunta si está.'),
    bk('Ordenamiento', '<code>lista.sort()</code> ordena la misma lista · <code>sorted(lista)</code> crea una nueva ordenada · <code>reverse=True</code> de mayor a menor.'),
    bk('Recorrer', '<code>for usuario in registros:</code> visita cada elemento. Con <code>enumerate</code> tienes también la posición.'),
    code('registros = ["ana", "luis", "ana"]\nfor i, u in enumerate(registros):\n    print(i, u)\nprint(registros.count("ana"))   # 2')),
    'Lista = varios datos en orden; se recorre con for.')
c.L('🧠', 'Algoritmos con listas y aplicaciones avanzadas', 'Bloque A · Pensar el paso a paso', body(
    sp('En palabras sencillas', 'Un <b>algoritmo</b> es la receta: pasos ordenados y finitos. Muchos se construyen con un bucle que recorre una lista.'),
    bk('Buscar el mayor (sin max)', 'Supón que el primero es el mayor; recorre los demás y, si alguno es más grande, actualiza. Así funcionan max() y muchas búsquedas.'),
    code('intentos = [3, 7, 1, 9, 4]\nmayor = intentos[0]\nfor x in intentos:\n    if x > mayor:\n        mayor = x\nprint(mayor)   # 9'),
    bk('Quitar repetidos', 'Recorre la lista y agrega a una nueva solo lo que <b>no esté</b> todavía: <code>if u not in unicos: unicos.append(u)</code>.'),
    bk('Comprensión de listas', 'Forma corta de crear una lista filtrando: <code>sospechosos = [x for x in intentos if x &gt;= 5]</code>.'),
    ex('Aplicación en ciberseguridad', 'Con estos algoritmos un analista revisa miles de registros: cuenta accesos por usuario, encuentra quién tuvo más fallos y lista los sospechosos para revisarlos.')),
    'Recorrer + comparar + acumular = la base de casi todo algoritmo.')
lab('🧪', 'Analiza los registros', 'Laboratorio de Python: listas, ordenamiento y algoritmos.',
    {'id': 'q4', 'code': '# Registros de entrada del día\nregistros = ["ana", "luis", "ana", "sofia", "pedro", "ana", "luis"]\nintentos = [3, 7, 1, 9, 4]\n',
     'intro': 'Trabaja con las dos listas. Mira la tabla de variables para comprobar tus resultados.'},
    [['Crea <b>veces_ana</b> con cuántas veces aparece "ana" (debe ser 3) y muestra cuántos registros hay con <b>len()</b>.', 'a.v("veces_ana")==3&&a.uses(/len\\s*\\(\\s*registros/)&&a.ok'],
     ['Crea la lista <b>unicos</b> sin repetidos con un <b>for</b>, <b>not in</b> y <b>append</b>.', 'a.r("unicos")=="[\'ana\', \'luis\', \'sofia\', \'pedro\']"&&a.uses(/not\\s+in/)&&a.uses(/append/)'],
     ['Crea <b>ordenados</b> con los usuarios únicos en orden alfabético.', 'a.r("ordenados")=="[\'ana\', \'luis\', \'pedro\', \'sofia\']"'],
     ['Encuentra el <b>mayor</b> número de intentos con un algoritmo propio (sin usar max()).', 'a.v("mayor")==9&&a.uses(/\\bfor\\b/)&&!a.uses(/max\\s*\\(/)'],
     ['Crea <b>sospechosos</b> con los intentos de 5 o más usando una <b>comprensión de listas</b>.', 'a.r("sospechosos")=="[7, 9]"&&a.uses(/\\[[^\\]]*\\bfor\\b[^\\]]*\\bif\\b/)']],
    'count() cuenta, sorted() ordena, y para el mayor: mayor = intentos[0] y luego un for con if.')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Funciones ─────────────────────────
b0 = c.mark()
c.L('🧩', 'Funciones de programación', 'Bloque B · Comunicación, resultados y expresión de retorno', body(
    sp('En palabras sencillas', 'Una <b>función</b> es un bloque con nombre que hace una tarea. Se escribe una vez y se usa muchas veces. Ya usaste funciones de Python: print(), len(), int().'),
    code('def es_segura(clave):\n    return len(clave) >= 12\n\nprint(es_segura("hola"))           # False\nprint(es_segura("CiberLab2026!"))  # True'),
    bk('Comunicación', 'La función recibe datos por sus <b>parámetros</b> (en el def) y tú le mandas <b>argumentos</b> al llamarla. Devuelve su <b>resultado</b> con <b>return</b>.'),
    bk('Expresión de retorno', '<code>return expresión</code> termina la función y entrega el valor. Si no hay return, la función devuelve <b>None</b>.'),
    bk('print o return', '<code>print</code> solo muestra en pantalla; <code>return</code> entrega el valor para que el resto del programa lo use (guardarlo, compararlo, sumarlo).'),
    ana('Piensa en una máquina de jugos', 'Le metes fruta (argumentos), hace su proceso (cuerpo de la función) y te devuelve jugo (return).')),
    'def nombre(parámetros): … return resultado.')
c.L('⚙️', 'Valores, mecanismos y múltiples parámetros', 'Bloque B · Cómo viajan los datos', body(
    bk('Múltiples parámetros', '<code>def tiempo(combinaciones, intentos_por_segundo):</code> recibe dos datos, separados por comas, en ese orden.'),
    bk('Valores por omisión', '<code>def tiempo(combinaciones, intentos_por_segundo=1000000000):</code> si no mandas el segundo, usa ese valor.'),
    bk('Argumentos por nombre', '<code>tiempo(5000, intentos_por_segundo=10)</code>: más claro y no importa el orden.'),
    bk('Variables locales', 'Lo que se crea dentro de la función solo existe ahí (alcance local). Para sacar un dato, usa return.'),
    bk('Funciones que llaman funciones', 'Una función puede usar a otra: <code>evaluar(clave)</code> puede llamar a <code>es_segura(clave)</code>. Así se arma un programa grande con piezas pequeñas.'),
    code('def tiempo(combinaciones, intentos_por_segundo=1000000000):\n    return combinaciones / intentos_por_segundo\n\nprint(tiempo(62 ** 8))          # usa el valor por omisión\nprint(tiempo(62 ** 8, 1000))    # manda los dos')),
    'Parámetros en orden, por nombre o por omisión; el resultado sale con return.')
c.A('🧩', '¿Qué parte de la función es?', 'Observa def tiempo(combinaciones, intentos=1000): return combinaciones / intentos y la llamada tiempo(5000). Elige qué es cada elemento.', [
    ['tiempo', 'Nombre', 'Es el nombre con el que se llama la función.'],
    ['combinaciones', 'Parámetro', 'Es la variable que recibe el dato dentro del def.'],
    ['5000', 'Argumento', 'Es el valor que se manda al llamar.'],
    ['intentos=1000', 'Valor por omisión', 'Se usa si no mandas ese dato.'],
    ['return combinaciones / intentos', 'Retorno', 'Entrega el resultado al que llamó.'],
], 'El def define; la llamada manda; return regresa.', ['Nombre', 'Parámetro', 'Argumento', 'Valor por omisión', 'Retorno'])
lab('🧪', 'Crea tus funciones', 'Laboratorio de Python: def, parámetros, return y funciones que se comunican.',
    {'id': 'q5', 'code': '# Funciones de seguridad del Ciber Lab\n',
     'intro': 'Los retos llaman a tus funciones con varios datos para comprobar que regresan el resultado correcto.'},
    [['Crea <b>es_segura(clave)</b> que regrese <b>True</b> si la clave tiene 12 caracteres o más y False si no.', 'a.fn("es_segura")&&a.ev("es_segura(\\"abc\\")")=="False"&&a.ev("es_segura(\\"CiberLab2026!\\")")=="True"&&a.uses(/\\breturn\\b/)'],
     ['Crea <b>tiempo(combinaciones, intentos_por_segundo=1000000000)</b> que regrese los segundos (combinaciones ÷ intentos).', 'a.fn("tiempo")&&a.ev("tiempo(2000000000)")=="2.0"&&a.ev("tiempo(100, 10)")=="10.0"'],
     ['Crea <b>resumen(usuario, intentos)</b> que <b>regrese</b> (no imprima) un texto con los dos datos, y muéstralo con print.', 'a.fn("resumen")&&/ana/.test(a.ev("resumen(\\"ana\\", 3)"))&&/3/.test(a.ev("resumen(\\"ana\\", 3)"))&&a.uses(/print\\s*\\(\\s*resumen\\s*\\(/)'],
     ['Crea <b>evaluar(clave)</b> que <b>use es_segura</b> y regrese "Fuerte" o "Débil".', 'a.fn("evaluar")&&a.ev("evaluar(\\"abc\\")")=="\'Débil\'"&&a.ev("evaluar(\\"CiberLab2026!\\")")=="\'Fuerte\'"&&/def\\s+evaluar[\\s\\S]*es_segura\\s*\\(/.test(a.src)']],
    'def es_segura(clave):  →  return len(clave) >= 12. En evaluar: if es_segura(clave): return "Fuerte".')
c.L('🧯', 'Excepciones y errores en el código', 'Bloque B · Que el programa no se caiga', body(
    sp('En palabras sencillas', 'Una <b>excepción</b> es un error que ocurre mientras el programa corre (ValueError, ZeroDivisionError, IndexError…). Si nadie la atrapa, el programa se detiene.'),
    code('try:\n    edad = int(input("Edad: "))\nexcept ValueError:\n    print("Escribe la edad con números")\nelse:\n    print("Gracias")\nfinally:\n    print("Fin del registro")'),
    bk('try / except', 'En <b>try</b> va lo que puede fallar; en <b>except Tipo</b> lo que hay que hacer si falla. <code>except ValueError as e</code> guarda el mensaje en e.'),
    bk('else y finally', '<b>else</b> se ejecuta si no hubo error; <b>finally</b> siempre, haya o no error (cerrar archivos, registrar).'),
    bk('raise', 'Tú también puedes lanzar una excepción cuando un dato no tiene sentido: <code>raise ValueError("La edad no puede ser negativa")</code>.'),
    bk('Errores en el código', '<b>De sintaxis</b>: el programa no arranca (falta «:», sangría incorrecta, = en lugar de ==). <b>De ejecución</b>: excepciones. <b>De lógica</b>: corre pero da un resultado equivocado (un if en el orden incorrecto, un ciclo que no termina).'),
    warn('Validar entradas', 'Nunca confíes en lo que escribe el usuario: valídalo. Muchos ataques empiezan con una entrada inesperada.')),
    'try intenta, except atrapa, else si salió bien, finally siempre, raise avisa.')
c.A('🐞', '¿Qué tipo de error es?', 'Clasifica cada error.', [
    ['if edad >= 18 (sin dos puntos)', 'Sintaxis', 'Falta el «:»; Python no puede leer la línea.'],
    ['int("quince")', 'Ejecución', 'Es un ValueError que ocurre al correr.'],
    ['El programa deja entrar a una cuenta bloqueada porque revisa la clave primero', 'Lógica', 'Corre sin errores pero decide mal.'],
    ['while intentos < 3: sin intentos += 1 adentro', 'Lógica', 'Es un ciclo que nunca termina.'],
    ['lista[10] en una lista de 5 elementos', 'Ejecución', 'IndexError al correr.'],
    ['Un print con 2 espacios dentro de un if que tiene otros con 4', 'Sintaxis', 'IndentationError: la sangría no coincide.'],
], 'Sintaxis = no arranca · Ejecución = se detiene · Lógica = resultado equivocado.', ['Sintaxis', 'Ejecución', 'Lógica'])
lab('🧪', 'Atrapa las excepciones', 'Laboratorio de Python: try, except, else, finally y raise.',
    {'id': 'q6', 'code': '# Registro de edad del Ciber Lab\nedad = int(input("Edad: "))\nprint("Edad registrada:", edad)\n', 'inputs': 'quince',
     'intro': 'Ejecuta primero: el programa se cae con ValueError porque el usuario escribió letras. Hazlo a prueba de errores.'},
    [['Atrapa el <b>ValueError</b> con <b>try/except</b> y muestra <b>Escribe la edad con números</b>.', 'a.ok&&a.uses(/\\btry\\s*:/)&&a.uses(/except\\s+ValueError/)&&a.printed("Escribe la edad con números")'],
     ['Pide la edad en un <b>while</b> hasta que sea válida: con «x, y, 15» debe pedirla 3 veces y registrar 15.', '(function(r){return !r.err&&r.used==3&&r.out.indexOf("15")>-1})(a.run(["x","y","15","20"]))&&a.uses(/\\bwhile\\b/)'],
     ['Crea <b>validar_edad(e)</b> que lance <b>ValueError</b> con <b>raise</b> si la edad es negativa y regrese la edad si no.', 'a.fn("validar_edad")&&a.ev("validar_edad(-1)")=="ERR:ValueError"&&a.ev("validar_edad(16)")=="16"&&a.uses(/\\braise\\s+ValueError/)'],
     ['Agrega un bloque <b>finally</b> que muestre <b>Fin del registro</b>.', 'a.ok&&a.uses(/\\bfinally\\s*:/)&&a.printed("Fin del registro")']],
    'while True: → try: edad = int(input(...)) → break → except ValueError: print(...). El break solo se alcanza si int() funcionó.')
lab('🧪', 'Depura el control de acceso', 'Laboratorio de Python: corrige errores de sintaxis, de ejecución y de lógica.',
    {'id': 'q7', 'code': '# Programa con errores: corrígelos uno por uno\nclaves = ["1234", "Ciber2026", "abc"]\nfor c in claves\n    if len(c) >= 8:\n        print(c, "segura")\n    else:\n        print(c, "débil")\n   print("Revisada:", c)\nintentos = 0\nwhile intentos < 3:\n    print("Intento", intentos)\nprint("Total:", len(clave))\n',
     'intro': 'Ejecuta, lee el mensaje (tipo de error, línea y pista), corrige y vuelve a ejecutar hasta que funcione.'},
    [['Corrige el error de sintaxis del <b>for</b> (le falta algo al final).', 'a.uses(/for\\s+c\\s+in\\s+claves\\s*:/)'],
     ['Corrige la <b>sangría</b> de <b>print("Revisada:", c)</b>: debe quedar dentro del for, con 4 espacios.', '/\\n    print\\("Revisada:", c\\)/.test(a.src)&&(!a.err||a.err.kind!="IndentationError")'],
     ['Corrige el <b>ciclo infinito</b>: el while debe terminar después de 3 vueltas.', 'a.uses(/intentos\\s*\\+=\\s*1|intentos\\s*=\\s*intentos\\s*\\+\\s*1/)&&(!a.err||a.err.kind!="RuntimeError")&&a.printed("Intento 2")&&!a.printed("Intento 3")'],
     ['Corrige el <b>NameError</b> de la última línea (la lista se llama claves) para que muestre <b>Total: 3</b>.', 'a.ok&&a.printed("Total: 3")'],
     ['Agrega comentarios (#) que digan qué tipo de error era cada uno: al menos dos, además del que ya trae.', 'a.comments>=3']],
    'Sintaxis: «:» al final del for. Sangría: 4 espacios en print("Revisada:", c). Lógica: intentos += 1 dentro del while. NameError: claves.')
c.W('✍️', 'Explica tu programa', 'Describe el flujo de control de un programa tuyo.',
    'Explica con tus palabras el programa de control de acceso que hiciste: qué <b>condiciones</b> revisa y en qué orden, qué <b>bucle</b> usaste y por qué, qué <b>función</b> creaste (parámetros y return) y qué <b>excepción</b> atrapas.',
    [['Tiene al menos 50 palabras', 'palabras:50'],
     ['Menciona una condición (if, elif, else)', '\\b(if|elif|else|condici\\w*)\\b'],
     ['Menciona un bucle (for, while)', '\\b(for|while|bucle\\w*|ciclo\\w*)\\b'],
     ['Menciona una función, parámetro o return', '\\b(funci\\w*|def|par[aá]metro\\w*|return)\\b'],
     ['Menciona una excepción (try, except, ValueError)', '\\b(try|except|excepci\\w*|valueerror|raise)\\b']],
    'Condiciones → bucle → función → excepción.', 'Ejemplo: Mi programa primero revisa si la cuenta está bloqueada con un if…')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Flujo de control', 'Orden en que se ejecutan las instrucciones.'),
    bk('Condición', 'Expresión que da True o False.'),
    bk('if / elif / else', 'Sentencias condicionales para elegir un camino.'),
    bk('Bucle', 'Bloque que se repite: while o for.'),
    bk('Iteración', 'Cada repetición de un bucle.'),
    bk('break / continue', 'Salir del bucle / saltar a la siguiente iteración.'),
    bk('Operador bit a bit', 'Opera sobre cada bit: &, |, ^, ~, <<, >>.'),
    bk('Lista', 'Colección ordenada de datos entre corchetes.'),
    bk('Algoritmo', 'Pasos ordenados y finitos para resolver un problema.'),
    bk('Función', 'Bloque con nombre que hace una tarea (def).'),
    bk('Parámetro / argumento', 'Variable que recibe el dato / valor que se envía.'),
    bk('return', 'Entrega el resultado de la función.'),
    bk('Excepción', 'Error que ocurre al ejecutar y se puede atrapar con try/except.'),
    bk('Sangría', 'Espacios al inicio de la línea que indican qué está dentro de un bloque.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 511. El R.A. 3.2 dura 15 h y vale 15%. La A.E. es el viernes 8-ene. Los laboratorios corren en el navegador; para las prácticas sirven Thonny, IDLE, Pydroid 3 o un compilador en línea.', 'sp'),
    bk('Lunes 7-dic · Bloque A (3 sesiones)', 'Condiciones y operadores lógicos (laboratorio 1); bucles, range, break y continue (laboratorio 2).'),
    bk('Viernes 11-dic · Bloque A (2 sesiones)', 'Operaciones bit a bit (laboratorio 3) y listas (laboratorio 4). <b>Práctica 1</b>.'),
    bk('Lunes 14-dic · Bloques A y B (3 sesiones)', 'Cierre de algoritmos con listas; funciones, parámetros y return (laboratorio 5). <b>Práctica 2</b>.'),
    bk('Viernes 18-dic · Bloque B (2 sesiones)', 'Excepciones y errores (laboratorios 6 y 7). <b>Práctica 3</b>.'),
    bk('Viernes 8-ene · Evaluación', 'Repaso y entrega del reporte con el escenario asignado en la plataforma.'),
    bk('Sugerencia', 'Pide que lean el mensaje de error en voz alta antes de corregir: tipo, línea y pista. Es la habilidad que más tiempo ahorra.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🔀', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🔁', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🧩', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🔀",t:"Empieza aquí",d:"Qué es el flujo de control y qué vas a entregar.",time:"15 min",obj:["Reconocer para qué sirven decisiones, ciclos y funciones","Conocer el caso y la evidencia"],sum:["El flujo de control decide qué se ejecuta y cuántas veces.","Entregas un reporte con tu escenario asignado (15%)."],q:"¿Qué decisión repetitiva tomas cada día que podría hacer un programa?"},
a:{k:"Bloque A",l:"A",ic:"🔁",t:"Procesamiento",d:"Condicionales, decisiones, bucles, iteraciones, operadores lógicos y bit a bit, listas, ordenamiento y algoritmos.",time:"9 h",obj:["Tomar decisiones con if, elif y else","Repetir con while y for","Combinar condiciones con and, or y not","Usar operadores bit a bit","Trabajar, ordenar y recorrer listas con algoritmos propios"],sum:["if/elif/else con «:» y sangría.","while = mientras · for = para cada.","and, or, not · &, |, ^, <<, >>.","append, count, sort, sorted, comprensiones."],q:"¿Qué lista de datos de tu escuela analizarías con un programa?"},
b:{k:"Bloque B",l:"B",ic:"🧩",t:"Funciones de programación",d:"Comunicación de funciones, resultados, retorno, valores, mecanismos, múltiples parámetros, excepciones y errores.",time:"6 h",obj:["Crear funciones con parámetros y return","Usar valores por omisión y argumentos por nombre","Atrapar y lanzar excepciones","Distinguir errores de sintaxis, ejecución y lógica"],sum:["def nombre(parámetros): … return valor.","Parámetros en orden, por nombre o por omisión.","try/except/else/finally y raise.","Sintaxis, ejecución y lógica."],q:"¿Qué tarea de seguridad convertirías en una función reutilizable?",rev:[["Para repetir mientras una condición sea True se usa…",["while","if","def"],0,"while repite mientras la condición se cumpla."],["6 & 2 da…",["2","6","8"],0,"110 & 010 = 010."]]}
'''

ILL = r'''
ILL["Sentencias condicionales y toma de decisiones"]=function(){return flow([["❓","¿Bloqueada?"],["⛔","Cuenta|bloqueada"],["❓","¿Clave|correcta?"],["✅","Acceso"],["❌","Denegado"]],"Decisiones en orden")};
ILL["Bucles e iteraciones"]=function(){return flow([["🔢","intentos = 0"],["❓","¿< 3?"],["⌨️","Pedir|clave"],["➕","intentos += 1"],["🔁","Repetir"]],"Así gira un while")};
ILL["Operaciones bit a bit"]=function(){return grid3([["👁️","Leer|100 = 4"],["✏️","Escribir|010 = 2"],["▶️","Ejecutar|001 = 1"],["🧩","Leer | Escribir|110 = 6"]],"Permisos como bits")};
ILL["Funciones de programación"]=function(){return flow([["📥","Argumentos"],["🧩","def|función"],["📤","return"],["🖥️","Resultado"]],"Una función recibe y regresa")};
ILL["Excepciones y errores en el código"]=function(){return flow([["🧪","try"],["💥","¿Error?"],["🧯","except"],["✅","else"],["🏁","finally"]],"Manejo de excepciones")};
'''

EXH = r'''
EXH.thonny=function(){return exw(mw('Thonny','<div class="mfld" style="font-family:monospace;white-space:pre">for i in range(1, 6):\n    print(f"PC-{i:02d}") '+mk(1)+'</div><div class="mfld" style="margin-top:6px">▶ Run · Debug (paso a paso) '+mk(2)+'</div>'),['La sangría marca el bloque del for.','Debug ejecuta línea por línea y muestra las variables.'])};
EXH.salida=function(){return exw(mw('Shell','<div class="mfld" style="font-family:monospace;white-space:pre">Clave: hola\nClave: Ciber2026\nAcceso concedido '+mk(1)+'</div>'),['Prueba con varias entradas: correcta, incorrecta y vacía.'])};
EXH.cel=function(){return exw(mp('Pydroid 3 · Android','<div class="mbox" style="background:#0d1117;color:#e6edf3;font-family:monospace;white-space:pre">def es_segura(clave):\n    return len(clave) >= 12 '+mk(1)+'</div><div class="mbox" style="margin-top:6px">▶ Botón amarillo para ejecutar '+mk(2)+'</div>'),['Usa la tecla Tab o 4 espacios para la sangría.','La salida aparece en la terminal.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Control de acceso con decisiones y ciclos',
     'prog': 'Bloque A · Condicionales, bucles y operadores lógicos',
     'min': 80, 'lug': 'Viernes 11-dic en clase o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con Python y Thonny, IDLE o Visual Studio Code'],
                'steps': [
                    'Antes de empezar, termina los laboratorios 1 y 2.',
                    ['Crea <b>acceso.py</b>: pide usuario y clave hasta 3 veces con un while; usa if/elif/else, and y break.', 'thonny'],
                    'Si falla 3 veces, muestra «Cuenta bloqueada»; si el usuario es invitado o visita, «Acceso solo a Internet».',
                    'Agrega un for con range que liste los equipos del laboratorio y salte con continue el que esté en mantenimiento.',
                    ['Pruébalo con tres casos (correcto, incorrecto 3 veces, invitado) y toma captura de cada salida.', 'salida']]},
         'cel': {'mat': ['Celular con Pydroid 3 o un compilador en línea (programiz.com, onlinegdb.com)'],
                 'steps': [
                     'Antes de empezar, termina los laboratorios 1 y 2.',
                     ['Escribe el programa de acceso con while, if/elif/else, and y break.', 'cel'],
                     'Agrega el caso de cuenta bloqueada y el de invitado.',
                     'Agrega el for con range y continue.',
                     'Pruébalo con tres casos y toma captura de cada salida.']}},
     'entrega': ['acceso.py y las capturas de tres pruebas.'],
     'rub': [['Condiciones en el orden correcto', 30], ['while con límite y break', 25], ['for con range y continue', 20], ['Pruebas con tres casos', 25]]},
    {'id': 'pr2', 'n': 2, 't': 'Analizador de registros con listas y funciones',
     'prog': 'Bloques A y B · Listas, algoritmos, bits y funciones',
     'min': 80, 'lug': 'Lunes 14-dic en clase o en casa',
     'modes': {
         'pc': {'mat': ['Python y tu editor'],
                'steps': [
                    'Antes de empezar, termina los laboratorios 3, 4 y 5.',
                    'Crea una lista con al menos 10 registros de usuarios (con repetidos) y otra con sus intentos fallidos.',
                    'Haz funciones: contar(lista, usuario), unicos(lista), mayor(numeros) sin max() y sospechosos(numeros, limite=5).',
                    'Ordena los usuarios únicos y muestra un reporte con f-strings llamando a tus funciones.',
                    'Agrega un apartado de permisos con bits: combina con |, revisa con & y muestra en binario.']},
         'cel': {'mat': ['Pydroid 3 o un compilador en línea'],
                 'steps': [
                     'Antes de empezar, termina los laboratorios 3, 4 y 5.',
                     'Crea las dos listas de registros e intentos.',
                     'Escribe las cuatro funciones y llámalas para armar el reporte.',
                     'Agrega el apartado de permisos con bits y toma captura del código y la salida.']}},
     'entrega': ['analizador.py y la captura del reporte que genera.'],
     'rub': [['Listas y operaciones', 20], ['Algoritmos propios (únicos, mayor)', 25], ['Funciones con parámetros y return', 35], ['Permisos con bits', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Programa a prueba de errores',
     'prog': 'Bloque B · Excepciones y errores',
     'min': 60, 'lug': 'Viernes 18-dic en clase o en casa',
     'modes': {
         'pc': {'mat': ['Tus programas de las prácticas 1 y 2'],
                'steps': [
                    'Antes de empezar, termina los laboratorios 6 y 7.',
                    'En tu programa de acceso, valida con try/except cada número que pidas con input() y vuelve a pedirlo si es inválido.',
                    'Crea una función que lance ValueError con raise cuando un dato no tenga sentido (edad negativa, intentos menores que 0).',
                    'Agrega finally para registrar «Fin del registro».',
                    'Provoca un error de sintaxis, uno de ejecución y uno de lógica; toma captura, explícalos y corrígelos.']},
         'cel': {'mat': ['Tus programas de las prácticas 1 y 2 en Pydroid 3 o en línea'],
                 'steps': [
                     'Antes de empezar, termina los laboratorios 6 y 7.',
                     'Agrega try/except a cada input() numérico y repite la pregunta si es inválido.',
                     'Crea una función con raise para datos sin sentido y agrega finally.',
                     'Provoca y corrige los tres tipos de error, con captura de cada uno.']}},
     'entrega': ['El programa final y las capturas de los tres errores corregidos; es la base de tu reporte.'],
     'rub': [['try/except en las entradas', 30], ['Función con raise', 25], ['finally', 15], ['Tres tipos de error explicados', 30]]},
]

EVALUATION = {
    'course': 'MTCS-20 · Manejo de tecnologías de ciberseguridad · Unidad 3',
    'ra': 'R.A. 3.2', 'title': 'Reporte de estructuras de flujo de control y funciones',
    'data': [
        ('Resultado de aprendizaje', 'Utiliza estructuras de flujo de control empleando el lenguaje e instrucciones de programación requeridas a fin de agrupar instrucciones de manera controlada.'),
        ('Actividad de evaluación', '3.2.1 Demuestra el uso de estructuras de flujo de control evidenciando el procesamiento y las funciones de programación requeridas.'),
        ('Evidencia', 'Reporte (PDF)'),
        ('Ponderación', '15% (según el programa)'),
        ('Entrega', 'Viernes 8 de enero, en la actividad R.A. 3.2 de la plataforma'),
    ],
    'situation': 'En la actividad de evaluación de la plataforma tienes asignado un <b>sistema de control de acceso</b> con su lista de usuarios, la clave correcta, el límite de intentos y los registros del día. Escribe programas en Python que lo controlen y analicen, y elabora un reporte con el código, la salida y tus explicaciones.',
    'hint': 'Prueba cada programa con varios casos (correcto, incorrecto, límite) y pon la captura de cada prueba en el reporte.',
    'steps': [
        ('Procesamiento (Bloque A)', [
            'Programa de acceso con if/elif/else y operadores lógicos, en el orden correcto, con los datos asignados.',
            'Bucle while con límite de intentos y break; for con range o sobre una lista.',
            'Análisis de la lista de registros asignada: contar, quitar repetidos, ordenar y encontrar el mayor con un algoritmo propio.',
            'Permisos con operadores bit a bit.']),
        ('Funciones (Bloque B)', [
            'Al menos tres funciones con parámetros (una con valor por omisión) y return, y una que llame a otra.',
            'Validación con try/except y una función que use raise.']),
        ('Errores y cierre', [
            'Un error de sintaxis, uno de ejecución y uno de lógica: captura, explicación y corrección.',
            'Conclusión: qué estructura te pareció más útil para la ciberseguridad y por qué.']),
        ('Entrega', ['Llena las secciones de la actividad en la plataforma y adjunta tu reporte en PDF con el código y las capturas.']),
    ],
    'rubric': [('Condicionales y operadores lógicos', 15), ('Bucles e iteraciones', 15), ('Listas, ordenamiento y algoritmos', 15), ('Operaciones bit a bit', 10), ('Funciones con parámetros y retorno', 20), ('Excepciones y errores corregidos', 15), ('Redacción y presentación del reporte', 10)],
    'deliver': ['Un archivo PDF con tu reporte, tu código y las capturas de la salida.', 'Se entrega en la actividad R.A. 3.2 de la plataforma, junto con las secciones escritas.'],
}
