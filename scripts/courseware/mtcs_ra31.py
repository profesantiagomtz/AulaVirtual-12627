"""MTCS-20 · R.A. 3.1 · Fundamentos y lenguajes de programación (Python).

Caso de las lecciones: Ciber Lab escolar (control de accesos al laboratorio de cómputo).
Incluye un laboratorio de Python (py_sim.js) con instrucciones secuenciales: variables, literales,
operadores, entrada y salida, y errores de sintaxis y de ejecución. Las condiciones y los ciclos
se estudian en el R.A. 3.2.
La actividad de evaluación vive en la plataforma (MtcsActivity, con escenario asignado y PDF).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MTCS-RA-3.1'
CODE_PREFIX = 'MTCS31'
FILE = 'mtcs-ra31-material.html'
TITLE_TAG = 'MTCS-20 · R.A. 3.1 · Fundamentos de programación'
BRAND = 'MTCS-20 · Tecnologías de ciberseguridad'
BRAND_SUB = 'R.A. 3.1 · Fundamentos de programación'
HERO_KICK = 'MTCS-20 · R.A. 3.1'
HERO_TITLE = 'Aprende a darle instrucciones a la computadora'
HERO_TEXT = 'Escribe tus primeros programas en Python: variables, datos, operadores y cómo encontrar y corregir tus errores.'
EV_SHORT = 'elabora tu reporte con el escenario asignado.'
EV_CARD = 'Reporte R.A. 3.1'
RA = 'R.A. 3.1'
GROUP = '511'

TABS = {'d': ['Diagnostica', 'Laboratorio de Python'], 'c': ['Construye', 'Prácticas de programación']}

EXTRA_JS = (Path(__file__).parent / 'py_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".pysim"))pyInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".pysim"))return pyCheck(d);\n'),
]

c = Course()


def lab(ic, t, inf, cfg, tasks, hint):
    """tasks: [texto, expresión JS con la api a (a.out, a.ok, a.t, a.v, a.r, a.uses, a.printed, a.comments, a.lines, a.src)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    extra = ''.join(f',{k}:{j(v)}' for k, v in cfg.items())
    return c.raw(f'pPy({j(ic)},{j(t)},{j(inf)},{{tasks:{ts},hint:{j(hint)}{extra}}})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('💻', '¿Para qué programar en ciberseguridad?', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Programar es <b>escribir instrucciones</b> para que la computadora haga una tarea sola. En ciberseguridad se usa para <b>automatizar</b>: revisar miles de registros de acceso, avisar de intentos sospechosos o comprobar contraseñas, en segundos y sin cansarse.'),
    ex('Caso: Ciber Lab escolar', 'El laboratorio de cómputo anota quién entra, a qué hora y cuántas veces se equivocó con su contraseña. Contarlo a mano tarda horas. Un <b>programa de 10 líneas</b> lo hace al instante. Vas a aprender a escribirlo.'),
    r3([('🧠', 'Entender', 'Qué es un programa y un lenguaje.'), ('⌨️', 'Escribir', 'Variables, datos y operadores.'), ('🐞', 'Corregir', 'Errores de sintaxis y de lógica.')]),
    bk('Lenguaje del curso', 'Usaremos <b>Python</b>, uno de los lenguajes más usados en ciberseguridad y el más fácil de leer. Todo se practica <b>aquí mismo</b> en el Laboratorio de Python, sin instalar nada.'),
    bk('Al final', 'Entregas un <b>reporte</b> (20%) con el escenario que te asigna la plataforma en la actividad de evaluación.')),
    'Programar = darle instrucciones claras a la computadora.')
c.A('💻', '¿Esto se puede programar?', 'Decide si la tarea la puede hacer un programa (siguiendo instrucciones claras) o necesita criterio humano.', [
    ['Contar cuántas veces falló la contraseña cada alumno', 'Programa', 'Es contar y sumar: instrucciones claras.'],
    ['Decidir si un alumno merece una segunda oportunidad', 'Criterio humano', 'Requiere juicio y contexto.'],
    ['Calcular cuántas contraseñas posibles hay con 8 caracteres', 'Programa', 'Es una operación matemática.'],
    ['Convencer a un profesor de usar contraseñas más largas', 'Criterio humano', 'Es persuadir a una persona.'],
    ['Mostrar el mensaje «Acceso denegado» cuando algo no coincide', 'Programa', 'Es una instrucción que se repite igual cada vez.'],
], 'Si se puede describir en pasos exactos, se puede programar.', ['Programa', 'Criterio humano'])
s0_end = c.mark() - 1

# ───────────────────────── A · Programación informática ─────────────────────────
a0 = c.mark()
c.L('🧩', 'Conceptos universales de programación', 'Bloque A · Lo que sirve en cualquier lenguaje', body(
    bk('Programa', 'Conjunto de <b>instrucciones</b> que la computadora ejecuta para resolver una tarea.'),
    bk('Algoritmo', 'Los <b>pasos ordenados</b> para resolver un problema, antes de escribir código. Es como una receta de cocina.'),
    bk('Entrada, proceso y salida', 'Todo programa recibe <b>datos</b> (entrada), los <b>transforma</b> (proceso) y muestra un <b>resultado</b> (salida).'),
    bk('Datos', 'Lo que el programa guarda y usa: números, textos, verdadero o falso…'),
    ana('Piensa en…', 'Una licuadora: pones fruta (entrada), la licúa (proceso) y sale el licuado (salida). Si cambias la fruta, cambia el licuado, pero el proceso es el mismo.'),
    ex('En el Ciber Lab', 'Entrada: el usuario escribe su contraseña. Proceso: el programa la compara con la guardada. Salida: «Acceso concedido» o «Acceso denegado».')),
    'Entrada → Proceso → Salida.')
c.A('🧩', '¿Entrada, proceso o salida?', 'Clasifica cada paso de un programa del Ciber Lab.', [
    ['El usuario escribe su contraseña', 'Entrada', 'Es un dato que llega al programa.'],
    ['El programa compara la contraseña con la guardada', 'Proceso', 'Es una transformación o comparación de datos.'],
    ['Se muestra «Acceso concedido»', 'Salida', 'Es un resultado que ve el usuario.'],
    ['Se lee la lista de usuarios registrados', 'Entrada', 'Son datos que llegan al programa.'],
    ['Se calcula el total de intentos fallidos', 'Proceso', 'Es una operación con los datos.'],
    ['Se imprime el reporte del día', 'Salida', 'Es un resultado que se entrega.'],
], 'Datos que llegan = entrada · Lo que se hace con ellos = proceso · Lo que sale = salida.', ['Entrada', 'Proceso', 'Salida'])
c.L('📋', 'Instrucciones y algoritmos', 'Bloque A · El orden importa', body(
    sp('En palabras sencillas', 'Una <b>instrucción</b> es una orden que la computadora entiende, por ejemplo «muestra este mensaje». El programa las ejecuta <b>una tras otra, en orden</b>, de arriba hacia abajo.'),
    bk('Secuencia', 'Si cambias el orden, cambia el resultado. No puedes usar un dato antes de crearlo.'),
    bk('Precisión', 'La computadora no adivina: hace exactamente lo que le escribes, ni más ni menos.'),
    ex('En el Ciber Lab', 'Primero se pide el usuario, luego la contraseña, después se compara. Si compararas antes de pedir los datos, el programa fallaría.'),
    warn('Ojo', 'Un algoritmo es la idea; el programa es esa idea escrita en un lenguaje.')),
    'Instrucción tras instrucción, en orden.')
c.O('🔐', 'Ordena el algoritmo de entrada al laboratorio', 'Pon los pasos en el orden en que el programa debe hacerlos.', [
    ['Mostrar el mensaje de bienvenida y pedir el usuario', 'Primero se saluda y se pide el dato.'],
    ['Leer la contraseña que escribe la persona', 'Después se recibe el segundo dato.'],
    ['Comparar los datos con los guardados', 'Solo se puede comparar cuando ya se tienen.'],
    ['Mostrar el resultado: acceso concedido o denegado', 'La salida depende de la comparación.'],
    ['Registrar el intento en el historial', 'Al final queda registro para revisar.'],
], 'Primero los datos, luego el proceso y al final la salida.')
c.L('🗣️', 'Lenguajes de programación', 'Bloque A · Cómo le hablamos a la computadora', body(
    sp('En palabras sencillas', 'La computadora solo entiende <b>ceros y unos</b> (lenguaje máquina). Los <b>lenguajes de alto nivel</b>, como Python, se parecen más al lenguaje humano y se traducen a ceros y unos.'),
    bk('Bajo nivel', 'Cerca de la máquina: lenguaje máquina y ensamblador. Muy rápidos, pero difíciles de escribir.'),
    bk('Alto nivel', 'Cerca de las personas: Python, JavaScript, Java, C#… Más fáciles de leer y escribir.'),
    bk('Interpretado o compilado', '<b>Interpretado</b>: un intérprete traduce y ejecuta el programa línea por línea (Python, JavaScript). <b>Compilado</b>: un compilador traduce todo antes y genera un archivo ejecutable (C, C++).'),
    ex('En ciberseguridad', 'Python sirve para automatizar tareas y analizar datos; C aparece en sistemas y malware; JavaScript, en páginas web; Bash y PowerShell, para administrar sistemas.')),
    'Alto nivel = fácil de leer · Interpretado = se traduce al ejecutar.')
c.A('🗣️', '¿Compilado o interpretado?', 'Elige cómo se ejecuta normalmente cada lenguaje.', [
    ['Python', 'Interpretado', 'El intérprete de Python ejecuta el código línea por línea.'],
    ['C', 'Compilado', 'Un compilador genera el ejecutable antes.'],
    ['JavaScript', 'Interpretado', 'El navegador lo interpreta al abrir la página.'],
    ['C++', 'Compilado', 'Se compila a un ejecutable.'],
], 'Interpretado = se traduce al ejecutar · Compilado = se traduce antes.', ['Interpretado', 'Compilado'])
c.L('📄', 'El archivo fuente', 'Bloque A · Dónde vive tu programa', body(
    sp('En palabras sencillas', 'El <b>archivo fuente</b> es un archivo de <b>texto</b> donde escribes las instrucciones. En Python termina en <b>.py</b>, por ejemplo <b>ciberlab.py</b>.'),
    bk('Cómo se crea', 'Con un editor de texto o un IDE: escribes, guardas con extensión .py y ejecutas.'),
    bk('Cómo se ejecuta', 'En la terminal: <b>python ciberlab.py</b>. O con el botón ▶ de tu editor.'),
    bk('Fuente vs ejecutable', 'El código fuente lo lee y modifica una persona. El <b>ejecutable</b> (.exe) ya está traducido y lo ejecuta la computadora.'),
    warn('Buenas costumbres', 'Nombre sin espacios ni acentos (ciber_lab.py), guárdalo en una carpeta que encuentres fácil y nunca pongas contraseñas reales dentro del código.')),
    'Archivo fuente = texto con tus instrucciones (.py).')
c.A('📄', '¿Archivo fuente o ejecutable?', 'Clasifica cada archivo.', [
    ['saludo.py escrito en el Bloc de notas', 'Archivo fuente', 'Es texto con instrucciones que una persona escribió.'],
    ['setup.exe que instalas con doble clic', 'Programa ejecutable', 'Ya está traducido para la computadora.'],
    ['El archivo que el programador abre para corregir una línea', 'Archivo fuente', 'Es lo que una persona puede leer y modificar.'],
    ['El archivo que el usuario final ejecuta sin ver el código', 'Programa ejecutable', 'El usuario no necesita ver el código.'],
], 'Lo que escribe la persona es fuente; lo ya traducido es ejecutable.', ['Archivo fuente', 'Programa ejecutable'])
c.L('🔤', 'Elementos del lenguaje', 'Bloque A · Las piezas de un programa en Python', body(
    bk('Palabras reservadas', 'Palabras con significado especial (if, for, while, def, class, True, False…). <b>No se pueden usar como nombres</b>.'),
    bk('Identificadores', 'Los nombres que tú eliges: de variables, funciones… Ejemplo: <b>intentos</b>, <b>usuario</b>.'),
    bk('Comentarios', 'Empiezan con <b>#</b>. Python los ignora; sirven para explicar el código a las personas.'),
    bk('Instrucciones y líneas', 'Normalmente una instrucción por línea. Los paréntesis y las comillas se abren y se <b>cierran</b>.'),
    bk('Indentación', 'Los espacios al inicio de una línea tienen significado en Python. Por ahora, todas las líneas empiezan en la primera columna.'),
    ex('Ejemplo', '<code># Cuenta los intentos</code> es un comentario. <code>intentos = 3</code> usa el identificador «intentos». <code>print("Hola")</code> usa la función print.')),
    'Reservadas, identificadores, comentarios e indentación.')
c.Z('🔤', 'Completa: elementos del lenguaje', 'Elige la palabra correcta.',
    '<p>Un comentario empieza con el símbolo {0}.</p>'
    '<p>Las palabras como if o while se llaman palabras {1}.</p>'
    '<p>El nombre que tú le pones a una variable es un {2}.</p>'
    '<p>Un archivo fuente de Python termina en {3}.</p>'
    '<p>Un programa se ejecuta instrucción por instrucción, en {4}.</p>',
    [['#', ['#', '//', '!']], ['reservadas', ['reservadas', 'opcionales', 'ocultas']], ['identificador', ['identificador', 'comentario', 'operador']],
     ['.py', ['.py', '.exe', '.doc']], ['orden', ['orden', 'desorden', 'paralelo']]],
    'Repasa «Elementos del lenguaje».')
c.L('🚀', 'Programación moderna', 'Bloque A · Cómo se programa hoy', body(
    bk('Lenguajes de alto nivel y bibliotecas', 'Nadie empieza de cero: se usan <b>bibliotecas</b> (código ya hecho por otras personas) para calcular, dibujar, conectarse a Internet o analizar datos.'),
    bk('IDE', 'Un <b>entorno de desarrollo</b> (como Thonny o Visual Studio Code) junta el editor con colores, la ayuda y el botón de ejecutar.'),
    bk('Repositorios y control de versiones', '<b>Git</b> guarda cada versión de tu código y <b>GitHub</b> permite compartirlo y trabajar en equipo.'),
    bk('APIs', 'Una <b>API</b> es la «ventanilla» para que tu programa use un servicio de otro (el clima, un mapa, un sistema de pagos).'),
    bk('Asistentes de IA', 'Pueden sugerir código y explicar errores, pero <b>tú debes entender, probar y revisar</b> lo que sugieren. Pueden equivocarse o escribir código inseguro.'),
    bk('Paradigmas', 'Hay distintas formas de organizar un programa: por pasos (procedural), por objetos (POO) o con funciones (funcional). Por ahora usaremos la más sencilla: instrucciones en secuencia.')),
    'Bibliotecas, IDE, Git, APIs y asistentes de IA: hay que entender lo que usas.')
c.A('🚀', '¿Qué herramienta moderna es?', 'Relaciona cada necesidad con la herramienta.', [
    ['Editor con colores, ayuda y botón de ejecutar en un solo programa', 'IDE', 'Un IDE junta todo en un entorno.'],
    ['Guardar cada versión de mi código y compartirlo con mi equipo', 'Git y repositorio', 'Git controla las versiones.'],
    ['Usar funciones ya hechas por otras personas', 'Biblioteca', 'Una biblioteca es código reutilizable.'],
    ['Conectar mi programa con el servicio de clima de otra empresa', 'API', 'La API es la ventanilla de un servicio.'],
    ['Pedir una sugerencia de código y revisarla antes de usarla', 'Asistente de IA', 'Ayuda, pero hay que verificar.'],
], 'Piensa para qué sirve cada una.', ['IDE', 'Git y repositorio', 'Biblioteca', 'API', 'Asistente de IA'])
lab('🧪', 'Tu primer programa', 'Laboratorio de Python: escribe y ejecuta instrucciones. Todo corre aquí, sin instalar nada.',
    {'id': 'p1', 'code': '# Mi primer programa en el Ciber Lab\nprint("Hola, mundo")\n',
     'intro': 'Escribe en el cuadro negro y pulsa <b>▶ Ejecutar</b> (o Ctrl + Enter). La <b>salida</b> aparece abajo. Cada reto se marca solo cuando tu programa lo cumple.'},
    [['Muestra el mensaje <b>Bienvenido al Ciber Lab</b> con <b>print</b>.', 'a.ok&&a.printed("Bienvenido al Ciber Lab")&&a.uses(/print\\s*\\(/)'],
     ['Agrega al menos <b>dos comentarios</b> (líneas que empiezan con #) que expliquen tu programa.', 'a.comments>=2'],
     ['Con <b>tres print</b> distintos muestra tu nombre, tu grupo y el nombre del lenguaje (Python), cada dato en su línea.', 'a.ok&&(a.src.match(/print\\s*\\(/g)||[]).length>=3&&a.lines.length>=4&&a.printed("Python")'],
     ['Haz que <b>un solo print</b> muestre tres datos separados por « | » usando <b>sep</b>. Ejemplo: print("PC-01", "Ana", "Lab", sep=" | ").', 'a.ok&&a.uses(/sep\\s*=\\s*["\']\\s*\\|\\s*["\']/)&&a.printed(" | ")'],
     ['Con <b>end</b> logra que dos print salgan en la misma línea. Ejemplo: print("Acceso ", end="") y luego print("concedido").', 'a.ok&&a.uses(/end\\s*=\\s*["\']/)&&a.lines.some(function(l){return l.indexOf("Acceso")>-1&&l.indexOf("concedido")>-1})']],
    'print("texto") muestra un mensaje. El texto va entre comillas. Los comentarios empiezan con #.')
a_end = c.mark() - 1

# ───────────────────────── B · Codificación ─────────────────────────
b0 = c.mark()
c.L('✍️', 'Sintaxis: las reglas de escritura', 'Bloque B · Escribir de forma que Python entienda', body(
    sp('En palabras sencillas', 'La <b>sintaxis</b> son las reglas de escritura del lenguaje, como la ortografía en español. Si no las respetas, Python <b>ni siquiera empieza</b> a ejecutar el programa.'),
    bk('Reglas básicas', 'Cierra las comillas y los paréntesis que abres · usa <b>print</b> con paréntesis · escribe los nombres exactamente igual (mayúsculas y minúsculas importan) · no uses palabras reservadas como nombres.'),
    bk('Error de sintaxis', 'Python muestra <b>SyntaxError</b> y la línea donde se confundió. Ejemplo: <code>print("Hola"</code> (falta cerrar el paréntesis).'),
    ex('Cómo leer un error', 'Lee <b>el final</b> del mensaje (qué pasó) y el número de línea (dónde). Casi siempre la solución está en esa línea o en la anterior.'),
    warn('Ojo', 'No copies código de un chat o documento sin revisar: las comillas “curvas” no son comillas de programación (" y \' sí).')),
    'Sintaxis = reglas de escritura. Si falla, el programa no arranca.')
c.L('🧭', 'Semántica: lo que significa el programa', 'Bloque B · Que haga lo que quieres', body(
    sp('En palabras sencillas', 'La <b>semántica</b> es el <b>significado</b>: qué hace realmente el programa. Un programa puede estar bien escrito y aun así hacer algo equivocado.'),
    bk('Error de ejecución', 'El programa arranca, pero se detiene en una línea con un error (por ejemplo, usar una variable que no existe o dividir entre cero). Las líneas anteriores sí se ejecutaron.'),
    bk('Error de lógica', 'El programa corre completo sin errores, pero el resultado es incorrecto: sumaste en vez de restar, dividiste entre 3 cuando eran 4 datos…'),
    ex('Comparación', 'Sintaxis: «Comi la tacos» está mal escrito. Semántica: «Voy a comer una piedra» está bien escrito pero no tiene sentido.'),
    bk('Cómo prevenirlos', 'Prueba tu programa con datos que ya conoces la respuesta, por ejemplo 2 + 2.')),
    'Sintaxis = cómo se escribe · Semántica = qué significa y qué hace.')
c.A('🐞', '¿Qué tipo de error es?', 'Elige el tipo de error de cada situación.', [
    ['print("Hola"  (falta cerrar el paréntesis)', 'Error de sintaxis', 'Python no entiende cómo está escrito y no ejecuta nada.'],
    ['print(nombre) sin haber creado la variable nombre', 'Error de ejecución', 'Arranca y falla en esa línea: NameError.'],
    ['Calcular el promedio de 4 datos dividiendo entre 3', 'Error de lógica', 'Corre sin error, pero el resultado está mal.'],
    ['total = 5 +  (la suma quedó incompleta)', 'Error de sintaxis', 'La instrucción está incompleta.'],
    ['print(10 / 0)', 'Error de ejecución', 'No se puede dividir entre cero: ZeroDivisionError.'],
    ['Un programa que suma el descuento en lugar de restarlo y muestra un total mayor', 'Error de lógica', 'Corre bien, pero hace algo equivocado.'],
], 'Sintaxis: ni arranca · Ejecución: se detiene · Lógica: termina pero mal.', ['Error de sintaxis', 'Error de ejecución', 'Error de lógica'])
c.L('📦', 'Variables', 'Bloque B · Cajas con nombre para guardar datos', body(
    sp('En palabras sencillas', 'Una <b>variable</b> es un espacio en la memoria con <b>nombre</b> donde guardas un dato. Se crea con el signo <b>=</b>: <code>intentos = 3</code>.'),
    bk('Leer el = al revés', 'No significa «igual a» como en matemáticas. Significa: «<b>guarda</b> el valor de la derecha en la variable de la izquierda».'),
    bk('Reglas del nombre', 'Empieza con letra o guion bajo · sin espacios (usa guion bajo: <b>intentos_fallidos</b>) · sin símbolos como $ o @ · no puede ser palabra reservada · <b>Edad</b> y <b>edad</b> son variables distintas.'),
    bk('Cambiar el valor', 'Puedes reasignar: <code>intentos = intentos + 1</code> o la forma corta <code>intentos += 1</code>.'),
    bk('Intercambiar', '<code>a, b = b, a</code> intercambia dos variables en una sola línea.'),
    ana('Piensa en…', 'Una caja con etiqueta: la etiqueta es el nombre y lo de adentro es el valor. Puedes sacar lo de adentro y poner otra cosa.'),
    warn('Ojo', 'Los nombres claros ayudan: <b>intentos_fallidos</b> se entiende; <b>x1</b> no.')),
    'nombre = valor · Guarda; no es una igualdad.')
c.A('📦', '¿Es un nombre de variable válido?', 'Decide si Python aceptaría cada nombre.', [
    ['intentos', 'Válido', 'Solo letras: correcto.'],
    ['2intentos', 'No válido', 'No puede empezar con número.'],
    ['intentos fallidos', 'No válido', 'Lleva un espacio; se usa guion bajo.'],
    ['intentos_fallidos', 'Válido', 'El guion bajo sí se permite.'],
    ['class', 'No válido', 'Es una palabra reservada.'],
    ['total$', 'No válido', 'El símbolo $ no se permite.'],
    ['_clave', 'Válido', 'Puede empezar con guion bajo.'],
], 'Letras, números y guion bajo; sin espacios, sin empezar con número.', ['Válido', 'No válido'])
c.L('🔢', 'Literales y tipos de datos', 'Bloque B · Los datos tienen tipo', body(
    sp('En palabras sencillas', 'Un <b>literal</b> es un valor escrito directamente en el código. Cada dato tiene un <b>tipo</b>, que decide qué se puede hacer con él.'),
    bk('int · entero', '<code>15</code>, <code>-7</code>, <code>0</code>: números sin punto decimal.'),
    bk('float · decimal', '<code>3.14</code>, <code>0.75</code>, <code>2.0</code>: números con punto decimal (siempre punto, nunca coma).'),
    bk('str · texto', '<code>"Ana"</code>, <code>\'PC-07\'</code>: entre comillas. <b>«15» entre comillas es texto, no número.</b>'),
    bk('bool · lógico', 'Solo dos valores: <code>True</code> y <code>False</code> (con mayúscula inicial).'),
    bk('Ver y cambiar el tipo', '<code>type(x)</code> dice el tipo. <code>int("15")</code>, <code>float("2.5")</code> y <code>str(15)</code> convierten de uno a otro.'),
    ex('En el Ciber Lab', '<code>equipo = "PC-07"</code> (str) · <code>intentos = 3</code> (int) · <code>tasa = 0.75</code> (float) · <code>bloqueado = False</code> (bool).')),
    'int, float, str y bool · Comillas = texto.')
c.A('🔢', '¿Qué tipo de dato es?', 'Elige el tipo de cada literal.', [
    ['15', 'int', 'Número entero, sin punto.'],
    ['3.14', 'float', 'Tiene punto decimal.'],
    ['"15"', 'str', 'Está entre comillas: es texto.'],
    ['True', 'bool', 'Valor lógico.'],
    ['"True"', 'str', 'Entre comillas es texto, no un valor lógico.'],
    ['-7', 'int', 'Entero negativo.'],
    ['2.0', 'float', 'Tiene punto decimal, aunque sea 2.'],
    ["'hola'", 'str', 'Las comillas simples también hacen texto.'],
], 'Comillas = texto · Punto decimal = float · True/False = bool.', ['int', 'float', 'str', 'bool'])
lab('🧪', 'Variables y tipos de datos', 'Laboratorio de Python: crea variables de distintos tipos y revisa la tabla de memoria.',
    {'id': 'p2', 'code': '# Datos de un equipo del Ciber Lab\nequipo = "PC-07"\n',
     'intro': 'Fíjate en la tabla <b>Variables en memoria</b>: muestra el valor y el <b>tipo</b> de cada una después de ejecutar.'},
    [['Crea la variable <b>equipo</b> con texto (ya viene en el programa).', 'a.t("equipo")=="str"'],
     ['Crea la variable <b>intentos_fallidos</b> con el número entero <b>3</b>.', 'a.t("intentos_fallidos")=="int"&&a.v("intentos_fallidos")==3||a.t("intentos_fallidos")=="int"&&a.uses(/intentos_fallidos\\s*\\+=\\s*1/)'],
     ['Crea la variable <b>tasa</b> con el decimal <b>0.75</b>.', 'a.t("tasa")=="float"&&a.v("tasa")==0.75'],
     ['Crea la variable <b>bloqueado</b> con un valor lógico.', 'a.t("bloqueado")=="bool"'],
     ['Súbele <b>1</b> a <b>intentos_fallidos</b> con <b>+=</b> (debe quedar en 4).', 'a.v("intentos_fallidos")==4&&a.uses(/intentos_fallidos\\s*\\+=\\s*1|intentos_fallidos\\s*=\\s*intentos_fallidos\\s*\\+\\s*1/)'],
     ['Con una <b>f-string</b> muestra: <i>El equipo PC-07 tiene 4 intentos fallidos</i> (usa tus variables).', 'a.ok&&a.uses(/f["\']/)&&a.printed("El equipo PC-07 tiene 4 intentos fallidos")&&a.uses(/\\{\\s*equipo\\s*\\}/)'],
     ['Muestra con <b>type()</b> el tipo de la variable <b>tasa</b>.', 'a.ok&&a.uses(/type\\s*\\(\\s*tasa\\s*\\)/)&&a.printed("<class \'float\'>")']],
    'Una variable se crea así: nombre = valor. Texto entre comillas; decimales con punto; True o False con mayúscula. f-string: print(f"Hola {nombre}").')
c.L('➕', 'Operadores aritméticos', 'Bloque B · Hacer cuentas', body(
    bk('Los siete', '<b>+</b> suma · <b>-</b> resta · <b>*</b> multiplica · <b>/</b> divide (siempre da decimal) · <b>//</b> división entera · <b>%</b> residuo · <b>**</b> potencia.'),
    bk('División entera y residuo', '<code>10 // 4</code> da <b>2</b> (cuántas veces cabe) y <code>10 % 4</code> da <b>2</b> (lo que sobra).'),
    bk('Prioridad', 'Igual que en matemáticas y en Excel: paréntesis, potencias, × ÷ // %, y al final + −. Si dudas, usa paréntesis.'),
    bk('Con textos', '<code>"Hola " + "mundo"</code> los une y <code>"ab" * 3</code> los repite. Pero <b>no puedes sumar texto con número</b>: <code>"Edad: " + 15</code> da error.'),
    ex('En ciberseguridad', 'Contraseñas posibles con 62 caracteres y longitud 8: <code>62 ** 8</code> = 218,340,105,584,896. Tiempo a mil millones de intentos por segundo: <code>62 ** 8 / 1000000000</code> ≈ 218,340 segundos (unos 2.5 días).')),
    '+ − * / // % ** · Prioridad: paréntesis, potencia, × ÷, + −.')
c.T('➕', '¿Qué resultado da?', 'Escribe el número que mostraría print en cada línea.', [
    ['print(2 + 3 * 4)', '14', 'Primero se multiplica 3×4=12 y luego 2+12.', 'Primero se multiplica.'],
    ['print(10 // 4)', '2', 'El 4 cabe 2 veces en 10.', '// es división entera.'],
    ['print(10 % 4)', '2', 'Sobran 2 al dividir 10 entre 4.', '% es el residuo.'],
    ['print(2 ** 5)', '32', '2 elevado a la 5: 2×2×2×2×2.', '** es potencia.'],
    ['print(10 / 4)', '2.5', 'La división normal da decimal.', '/ da decimal.'],
    ['print(17 % 5)', '2', '17 = 3×5 + 2: sobran 2.', 'Cuántos sobran.'],
    ['print((2 + 3) * 4)', '20', 'El paréntesis se resuelve primero.', 'Paréntesis primero.'],
    ['print(len("seguridad"))', '9', 'len cuenta los caracteres: s-e-g-u-r-i-d-a-d.', 'Cuenta las letras.'],
], 'Aplica la prioridad: paréntesis, potencias, × ÷ // %, + −.', 'm')
c.L('⚖️', 'Operadores de comparación y lógicos', 'Bloque B · Preguntas con respuesta True o False', body(
    bk('Comparación', '<b>==</b> igual · <b>!=</b> diferente · <b>&gt;</b> mayor · <b>&lt;</b> menor · <b>&gt;=</b> mayor o igual · <b>&lt;=</b> menor o igual. Dan <code>True</code> o <code>False</code>.'),
    warn('El error más común', '<b>=</b> guarda un valor; <b>==</b> compara. <code>edad = 15</code> guarda; <code>edad == 15</code> pregunta si vale 15.'),
    bk('Lógicos', '<b>and</b>: verdadero solo si las <b>dos</b> son verdaderas · <b>or</b>: verdadero si <b>al menos una</b> lo es · <b>not</b>: invierte el resultado.'),
    ex('En el Ciber Lab', '<code>es_segura = longitud &gt;= 12</code> guarda True o False. <code>acceso = usuario_valido and not bloqueado</code> es True solo si el usuario es válido y no está bloqueado.'),
    ana('Piensa en…', 'Para entrar a un concierto: tienes boleto <b>y</b> eres mayor de edad. Si falta una de las dos, no pasas (and). En cambio, para el descuento basta ser estudiante <b>o</b> adulto mayor (or).')),
    '== compara · = guarda · and exige todo · or acepta una.')
c.A('⚖️', '¿True o False?', 'Decide qué valor daría cada expresión.', [
    ['5 > 3', 'True', '5 sí es mayor que 3.'],
    ['"a" == "A"', 'False', 'Mayúsculas y minúsculas son distintas.'],
    ['10 != 10', 'False', '10 es igual a 10, así que «diferente» es falso.'],
    ['3 >= 3', 'True', 'Son iguales y «mayor o igual» incluye la igualdad.'],
    ['True and False', 'False', 'Con and se necesitan las dos verdaderas.'],
    ['False or True', 'True', 'Con or basta una verdadera.'],
    ['not True', 'False', 'not invierte el valor.'],
    ['len("abc") == 3', 'True', 'La palabra tiene 3 caracteres.'],
], 'Resuelve primero lo de adentro; and exige las dos; or acepta una.', ['True', 'False'])
c.L('💬', 'Entrada y salida de datos', 'Bloque B · Hablar con el usuario', body(
    bk('Salida con print', '<code>print("Hola", nombre)</code> muestra varios datos separados por espacio. Con <b>sep</b> cambias el separador y con <b>end</b> lo que va al final.'),
    bk('f-strings', 'Una cadena que empieza con <b>f</b> y lleva variables entre llaves: <code>print(f"Equipo {equipo}: {intentos} intentos")</code>. Con <code>{valor:.2f}</code> muestras 2 decimales.'),
    bk('Entrada con input', '<code>nombre = input("¿Cómo te llamas? ")</code> pide un dato al usuario.'),
    warn('Lo que más confunde', '<b>input() siempre entrega texto</b>, aunque el usuario escriba 15. Para operar con números conviértelo: <code>edad = int(input("Edad: "))</code>.'),
    ex('En el Ciber Lab', 'El usuario teclea la longitud de su contraseña. Con <code>longitud = int(input("Longitud: "))</code> ya puedes calcular <code>62 ** longitud</code>.')),
    'input() da texto · int() o float() lo convierten.')
lab('🧪', 'Entrada, conversión y salida', 'Laboratorio de Python: el programa le pide datos al usuario. Las respuestas se escriben en «Entradas del teclado».',
    {'id': 'p3', 'code': 'nombre = input("¿Cómo te llamas? ")\nedad = input("¿Cuántos años tienes? ")\n', 'inputs': 'Ana\n15',
     'intro': 'En el cuadro de <b>Entradas del teclado</b> ya hay dos respuestas (una por línea): Ana y 15. El programa las lee en ese orden.'},
    [['Convierte <b>edad</b> a número entero con <b>int()</b> (en la tabla debe decir int).', 'a.ok&&a.t("edad")=="int"&&a.uses(/int\\s*\\(/)'],
     ['Crea <b>edad_en_5</b> con la edad más 5 (debe valer 20).', 'a.t("edad_en_5")=="int"&&a.v("edad_en_5")==a.v("edad")+5&&a.uses(/edad\\s*\\+\\s*5/)'],
     ['Muestra con una <b>f-string</b>: <i>Ana, dentro de 5 años tendrás 20 años</i> (usa tus variables, no escribas Ana ni 20 a mano).', 'a.ok&&a.uses(/f["\']/)&&a.printed(a.v("nombre")+", dentro de 5 años tendrás "+(a.v("edad")+5)+" años")&&a.uses(/\\{\\s*nombre\\s*\\}/)'],
     ['Cambia las <b>Entradas del teclado</b> a otra persona (otro nombre y otra edad) y comprueba que el resultado cambia solo.', 'a.ok&&a.v("nombre")!="Ana"&&a.t("edad")=="int"&&a.printed(a.v("nombre")+", dentro de 5 años tendrás "+(a.v("edad")+5)+" años")']],
    'input() devuelve texto: edad = int(input(...)) o edad = int(edad). Una f-string: print(f"{nombre}, ...").')
lab('🧪', 'Operadores y seguridad', 'Laboratorio de Python: calcula cuánto tardaría un atacante en adivinar una contraseña.',
    {'id': 'p4', 'code': '# Contraseñas posibles y tiempo para adivinarlas\ncaracteres = 62      # mayúsculas, minúsculas y dígitos\nlongitud = 8\nintentos_por_segundo = 1000000000\nusuario_valido = True\nbloqueado = False\n',
     'intro': 'Con los operadores calcularás cuántas contraseñas son posibles y cuánto tardaría un atacante en probarlas todas. Revisa los tipos en la tabla: <b>/</b> siempre da decimal (float).'},
    [['Crea <b>combinaciones</b> con la potencia <b>caracteres ** longitud</b>.', 'a.t("combinaciones")=="int"&&a.v("combinaciones")==218340105584896&&a.uses(/\\*\\*/)'],
     ['Crea <b>segundos</b> dividiendo las combinaciones entre los intentos por segundo.', 'a.t("segundos")=="float"&&Math.abs(a.v("segundos")-218340.105584896)<0.001'],
     ['Crea <b>horas</b> con la división entera <b>//</b> de los segundos entre 3600.', 'Math.abs(a.v("horas")-60)<0.001&&a.uses(/\\/\\/\\s*3600/)'],
     ['Crea <b>minutos</b> con el residuo <b>%</b>: los minutos que sobran después de las horas, <b>(segundos % 3600) // 60</b>.', 'Math.abs(a.v("minutos")-39)<0.001&&a.uses(/%/)'],
     ['Crea <b>es_segura</b> con una comparación: <b>True</b> si <b>longitud &gt;= 12</b>. Con 8 debe dar False.', 'a.t("es_segura")=="bool"&&a.v("es_segura")===false&&a.uses(/>=|>/)'],
     ['Crea <b>acceso</b> con <b>and</b> y <b>not</b>: usuario_valido and not bloqueado (debe dar True).', 'a.t("acceso")=="bool"&&a.v("acceso")===true&&a.uses(/\\band\\b/)&&a.uses(/\\bnot\\b/)'],
     ['Muestra con una f-string el tiempo: <i>Tardaría 60 horas y 39 minutos</i>. Usa horas y minutos con <b>int()</b>.', 'a.ok&&a.uses(/f["\']/)&&a.printed("Tardaría 60 horas y 39 minutos")&&a.uses(/int\\s*\\(/)']],
    'Potencia: **. División entera: //. Residuo: %. Comparar: >=. Unir condiciones: and, not. Para quitar el .0 usa int(horas).')
c.L('🛠️', 'Herramientas de programación', 'Bloque B · Con qué se programa y se corrigen errores', body(
    bk('Editor o IDE', 'Donde escribes: <b>IDLE</b> y <b>Thonny</b> (fáciles para empezar), <b>Visual Studio Code</b> (el más usado). Resaltan colores y avisan errores.'),
    bk('Intérprete', 'El programa <b>Python</b> que traduce y ejecuta tu archivo .py.'),
    bk('Terminal', 'Desde ella ejecutas <code>python ciber_lab.py</code>. En Windows: Símbolo del sistema o PowerShell.'),
    bk('Depurador', 'Permite ir <b>línea por línea</b> viendo cómo cambian las variables. También sirve imprimir valores con print para investigar.'),
    bk('Ayuda y documentación', '<code>help(print)</code> o <b>docs.python.org</b> explican cada función. Leer el mensaje de error completo ya resuelve la mitad.'),
    bk('Sin computadora', 'En el celular puedes usar apps como <b>Pydroid 3</b> (Android) o compiladores en línea en el navegador.'),
    warn('Seguridad', 'No ejecutes código que no entiendes ni lo pegues de fuentes desconocidas: puede borrar o robar información.')),
    'Editor, intérprete, terminal, depurador y documentación.')
c.A('🛠️', '¿Qué herramienta uso?', 'Elige la herramienta para cada necesidad.', [
    ['Escribir mi programa con colores y ayuda', 'Editor o IDE', 'Ahí se escribe y se resalta el código.'],
    ['Traducir y ejecutar mi archivo .py', 'Intérprete', 'Python ejecuta el programa.'],
    ['Escribir el comando python ciber_lab.py', 'Terminal', 'Los comandos se escriben en la terminal.'],
    ['Ir línea por línea para ver por qué falla', 'Depurador', 'Permite seguir el programa paso a paso.'],
    ['Leer cómo funciona la función print', 'Documentación', 'La ayuda explica cada función.'],
], 'Escribir · ejecutar · comandos · corregir · consultar.', ['Editor o IDE', 'Intérprete', 'Terminal', 'Depurador', 'Documentación'])
lab('🧪', 'Depura el programa', 'Laboratorio de Python: este programa tiene errores. Corrígelos uno por uno, leyendo el mensaje.',
    {'id': 'p5', 'code': '# Programa con errores: corrígelos uno por uno\nusuario = "ana\nintentos = 3\nprint("Usuario:", usuario)\nprint("Intentos restantes: " + intentos)\ntotal = intentos * 2\nprint("Total:", totl)\n',
     'intro': 'Pulsa ▶ Ejecutar y lee el mensaje: dice el <b>tipo de error</b>, la <b>línea</b> y una pista. Corrige, vuelve a ejecutar y repite hasta que no quede ninguno.'},
    [['Corrige el <b>error de sintaxis</b> de la línea 2 (falta cerrar las comillas).', 'a.uses(/usuario\\s*=\\s*["\']ana["\']/)&&(a.ok||(a.err&&a.err.kind!="SyntaxError"))'],
     ['Corrige el <b>error de ejecución</b> de la línea 5 (no se puede sumar texto con un número). Usa <b>str()</b> o una f-string.', 'a.uses(/str\\s*\\(\\s*intentos\\s*\\)|f["\'][^"\']*\\{\\s*intentos\\s*\\}/)&&(a.ok||(a.err&&a.err.kind=="NameError"))'],
     ['Corrige el <b>NameError</b>: la variable se llama <b>total</b>, no «totl».', 'a.ok&&a.uses(/\\btotal\\b/)&&!a.uses(/totl/)'],
     ['El programa debe mostrar <i>Usuario: ana</i>, <i>Intentos restantes: 3</i> y <i>Total: 6</i>.', 'a.ok&&a.printed("Usuario: ana")&&a.printed("Intentos restantes: 3")&&a.printed("Total: 6")'],
     ['Agrega un comentario que explique qué error corregiste.', 'a.comments>=2']],
    'Lee primero el final del mensaje y la línea. Sintaxis: comillas. Ejecución: str(intentos). NameError: escribe bien el nombre.')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Programa', 'Conjunto de instrucciones que ejecuta la computadora.'),
    bk('Algoritmo', 'Pasos ordenados para resolver un problema.'),
    bk('Archivo fuente', 'Archivo de texto con el código (.py).'),
    bk('Intérprete / compilador', 'Traducen el programa a lenguaje máquina: uno al ejecutar, el otro antes.'),
    bk('Sintaxis', 'Reglas de escritura de un lenguaje.'),
    bk('Semántica', 'Significado: lo que el programa hace.'),
    bk('Variable', 'Espacio con nombre que guarda un dato.'),
    bk('Literal', 'Valor escrito directamente en el código (15, "Ana", True).'),
    bk('Tipo de dato', 'int, float, str o bool.'),
    bk('Operador', 'Símbolo que opera datos: + − * / // % ** == != and or not.'),
    bk('f-string', 'Texto con f al inicio y variables entre llaves.'),
    bk('IDE', 'Entorno que junta editor, ayuda y ejecución.'),
    bk('Depurar', 'Buscar y corregir errores.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 511: lunes y viernes por la tarde. Este R.A. vale 20% y su A.E. es el 4-dic. El Laboratorio de Python corre en el navegador (computadora o celular), sin instalar nada. Las prácticas piden además un editor real.', 'sp'),
    bk('Bloque A · 13 y 20-nov', 'Viernes 13: qué es programar, entrada-proceso-salida, algoritmo y orden de instrucciones. Viernes 20: lenguajes, archivo fuente, elementos del lenguaje, programación moderna, laboratorio «Tu primer programa» y <b>Práctica 1</b>. (El lunes 16 es día inhábil.)'),
    bk('Bloque B · 23, 27 y 30-nov', 'Lunes 23: sintaxis, semántica y variables (laboratorio de variables). Viernes 27: tipos de datos y operadores (laboratorio «Operadores y seguridad»). Lunes 30: entrada y salida, herramientas, «Depura el programa» y <b>Prácticas 2 y 3</b>.'),
    bk('Evaluación · 4-dic', 'Viernes 4: A.E. 3.1, reporte en PDF con el escenario asignado en la plataforma.'),
    bk('Nota', 'La actividad de evaluación se desbloquea al completar este material. Las condiciones y los ciclos (if, for, while) se estudian en el R.A. 3.2; el laboratorio avisa cuando alguien los intenta usar.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '💻', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🧩', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '✍️', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"💻",t:"Empieza aquí",d:"Para qué programar en ciberseguridad y qué vas a entregar.",time:"15 min",obj:["Reconocer qué tareas puede hacer un programa","Conocer el caso y la evidencia final"],sum:["Programar = darle instrucciones claras a la computadora.","Entregas un reporte con el escenario asignado."],q:"¿Qué tarea repetitiva de tu escuela o tu casa te gustaría que hiciera un programa por ti?"},
a:{k:"Bloque A",l:"A",ic:"🧩",t:"Programación informática",d:"Conceptos, instrucciones, lenguajes, archivo fuente y programación moderna.",time:"150 min",obj:["Explicar qué es un programa, un algoritmo y un lenguaje","Distinguir archivo fuente y programa ejecutable","Reconocer los elementos de un programa en Python"],sum:["Entrada → proceso → salida.","Las instrucciones se ejecutan en orden.","Fuente (.py) es texto; ejecutable ya está traducido."],q:"¿Por qué un asistente de IA no te quita la necesidad de entender el código?",rev:[["Un archivo fuente de Python termina en…",[".py",".exe",".doc"],0,"Los programas de Python se guardan como .py."],["Un lenguaje interpretado se traduce…",["Al ejecutarse","Antes, a un .exe","Nunca"],0,"El intérprete lo traduce línea por línea."]]},
b:{k:"Bloque B",l:"B",ic:"✍️",t:"Codificación",d:"Sintaxis, semántica, variables, literales, operadores y herramientas.",time:"240 min",obj:["Escribir instrucciones con sintaxis correcta","Crear variables de distintos tipos y usar operadores","Leer errores y corregirlos"],sum:["Sintaxis = cómo se escribe; semántica = qué significa.","Variables: nombre = valor.","input() da texto: conviértelo con int() o float()."],q:"¿Por qué conviene probar tu programa con datos de los que ya conoces la respuesta?",rev:[["x = 5 guarda; x == 5…",["Compara","Guarda otra vez","Suma"],0,"== compara y da True o False."],["input() siempre entrega…",["Texto","Un entero","Un decimal"],0,"Aunque escribas 15, es texto."]]}
'''

ILL = r'''
ILL["Conceptos universales de programación"]=function(){return grid3([["⌨️","Entrada|datos"],["⚙️","Proceso|instrucciones"],["🖥️","Salida|resultado"]],"Entrada, proceso y salida")};
ILL["Literales y tipos de datos"]=function(){return grid3([["🔢","int|15"],["🔟","float|3.14"],["🔤","str|\"Ana\""],["✅","bool|True / False"]],"Tipos de datos en Python")};
ILL["Operadores aritméticos"]=function(){return grid3([["➕","Suma|+"],["➖","Resta|-"],["✖️","Multiplica|*"],["➗","Divide|/"],["🧮","Entera|//"],["♻️","Residuo|%"],["⬆️","Potencia|**"]],"Operadores de Python")};
'''

EXH = r'''
function pw_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><div style="background:#0d1117;color:#e6edf3;padding:10px;font:13px Consolas,monospace;overflow-x:auto;white-space:pre">'+b+'</div></div>'}
EXH.editor=function(){return exw(pw_('ciber_lab.py · Thonny','# Mi primer programa '+mk(1)+'\nnombre = "Ana" '+mk(2)+'\nprint("Hola,", nombre) '+mk(3)+'\n\n▶ Ejecutar '+mk(4)),['Un comentario: Python lo ignora.','Una variable con un literal de texto.','Una instrucción: muestra un mensaje.','El botón para ejecutar el archivo.'])};
EXH.terminal=function(){return exw(pw_('Símbolo del sistema','C:\\Users\\Alumno\\Documents> python ciber_lab.py '+mk(1)+'\nHola, Ana '+mk(2)+'\n\nC:\\Users\\Alumno\\Documents> '),['Comando que ejecuta el archivo fuente.','La salida del programa.'])};
EXH.errores=function(){return exw(pw_('Un error en la terminal','Traceback (most recent call last):\n  File "ciber_lab.py", line 4 '+mk(1)+'\n    print("Total: " + total)\nTypeError: can only concatenate str '+mk(2)+'\n(not "int") to str'),['La línea donde falló.','El tipo de error y qué pasó.'])};
EXH.online=function(){return exw(pw_('Compilador de Python en línea','1  # Programa del Ciber Lab '+mk(1)+'\n2  longitud = 8\n3  print(62 ** longitud) '+mk(2)+'\n\n[ Run ] '+mk(3)+'\n218340105584896 '+mk(4)),['El código se escribe en el editor.','Una operación con potencia.','El botón para ejecutar.','La salida del programa.'])};
EXH.salida=function(){return exw(pw_('Salida de tu programa','Usuario: ana\nIntentos fallidos: 4 '+mk(1)+'\nContraseña segura: False '+mk(2)+'\nTardaría 60 horas y 39 minutos '+mk(3)),['Un dato guardado en una variable.','El resultado de una comparación.','Una f-string con cálculos.'])};
EXH.cel=function(){return exw(mp('Pydroid 3 · Android','<div class="mbox" style="background:#0d1117;color:#e6edf3;font-family:monospace">nombre = "Ana"\nprint("Hola,", nombre) '+mk(1)+'</div><div class="mbox" style="margin-top:6px">▶ Botón amarillo para ejecutar '+mk(2)+'</div><div class="mbox" style="margin-top:6px">Guarda con el nombre ciber_lab.py '+mk(3)+'</div>'),['El código en el editor.','El botón de ejecutar.','El archivo se guarda con extensión .py.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Tu primer programa en un archivo .py',
     'prog': 'Bloque A · Programación informática',
     'min': 60, 'lug': 'Viernes 20-nov en clase o en casa',
     'modes': {
         'pc': {'mat': ['Computadora con Python y un editor (Thonny, IDLE o Visual Studio Code)', 'Python se descarga gratis de python.org'],
                'steps': [
                    'Antes de empezar, termina el laboratorio «Tu primer programa» de este material.',
                    ['Instala Python y un editor (o abre uno que ya tengas). Crea el archivo <b>ciber_lab.py</b> y escribe: dos comentarios, tres print y un print con sep.', 'editor'],
                    ['Ejecútalo con el botón ▶ y luego desde la terminal con <b>python ciber_lab.py</b>. Toma captura de la salida.', 'terminal'],
                    'Marca en una captura o en tu cuaderno: un comentario, una instrucción, una palabra reservada y un identificador de tu programa.',
                    'Escribe en tus palabras: qué es el archivo fuente, qué lenguaje usaste y si es interpretado o compilado.']},
         'cel': {'mat': ['Celular con Pydroid 3 (Android) o con el navegador para un compilador de Python en línea', 'Ejemplos de sitios: programiz.com/python-programming/online-compiler o onlinegdb.com'],
                 'steps': [
                     'Antes de empezar, termina el laboratorio «Tu primer programa» de este material.',
                     ['Abre Pydroid 3 (o un compilador en línea), escribe dos comentarios, tres print y un print con sep. Guarda como <b>ciber_lab.py</b> si la app lo permite.', 'cel'],
                     ['Ejecuta el programa y toma captura del código y de la salida.', 'online'],
                     'Marca en la captura un comentario, una instrucción, una palabra reservada y un identificador.',
                     'Escribe en tus palabras: qué es el archivo fuente y si Python es interpretado o compilado.']}},
     'entrega': ['El archivo ciber_lab.py (o su captura) con la salida del programa; lo mejoras en las prácticas 2 y 3.'],
     'rub': [['Archivo con comentarios y print', 30], ['Ejecución con captura de la salida', 25], ['Identificación de elementos del lenguaje', 25], ['Explicación de fuente e intérprete', 20]]},
    {'id': 'pr2', 'n': 2, 't': 'Variables, tipos y operadores',
     'prog': 'Bloque B · Variables, literales y operadores',
     'min': 70, 'lug': 'Viernes 27-nov en clase o en casa',
     'modes': {
         'pc': {'mat': ['Tu archivo de la práctica 1', 'Python y tu editor'],
                'steps': [
                    'Antes de empezar, termina los laboratorios «Variables y tipos de datos» y «Operadores y seguridad».',
                    ['Crea variables de los cuatro tipos (str, int, float, bool) con datos de tu escenario. Muestra el tipo de cada una con <b>type()</b>.', 'salida'],
                    ['Calcula con los datos de tu escenario: combinaciones posibles (<b>**</b>), segundos, horas (<b>//</b>) y minutos (<b>%</b>) para adivinar una contraseña.', 'salida'],
                    ['Crea al menos dos variables lógicas con comparaciones (<b>&gt;=</b>, <b>==</b>) y una con <b>and</b> o <b>or</b>.', 'salida'],
                    'Muestra todos los resultados con f-strings y toma captura del código y de la salida.']},
         'cel': {'mat': ['Tu archivo de la práctica 1', 'Pydroid 3 o un compilador en línea'],
                 'steps': [
                     'Antes de empezar, termina los laboratorios «Variables y tipos de datos» y «Operadores y seguridad».',
                     ['Crea variables de los cuatro tipos con datos de tu escenario y muestra su tipo con type().', 'cel'],
                     ['Calcula combinaciones, segundos, horas y minutos con tus datos asignados.', 'online'],
                     'Agrega variables lógicas con comparaciones y con and o or.',
                     'Muestra todo con f-strings y toma captura del código y de la salida.']}},
     'entrega': ['El programa con variables, operadores y comparaciones, y la captura de su salida.'],
     'rub': [['Variables de los cuatro tipos con type()', 25], ['Cálculos con los operadores correctos', 30], ['Comparaciones y operadores lógicos', 25], ['Salida clara con f-strings', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Programa con entradas y corrección de errores',
     'prog': 'Bloque B · Entrada y salida, errores y herramientas',
     'min': 70, 'lug': 'Lunes 30-nov en clase, o antes en casa',
     'modes': {
         'pc': {'mat': ['Tus programas de las prácticas 1 y 2', 'Python y tu editor'],
                'steps': [
                    'Antes de empezar, termina los laboratorios «Entrada, conversión y salida» y «Depura el programa».',
                    ['Haz un programa que pida con <b>input()</b> el usuario y la longitud de su contraseña, convierta con <b>int()</b> y calcule cuántas combinaciones hay.', 'salida'],
                    'El programa debe mostrar con una f-string un resumen y una variable lógica: ¿la contraseña es segura (por ejemplo, 12 o más caracteres)?',
                    ['Provoca a propósito un error de sintaxis y uno de ejecución. Toma captura de cada mensaje, explica qué significan y corrígelos.', 'errores'],
                    'Escribe en tus palabras qué herramientas usaste (editor, intérprete, terminal) y qué otra tarea de seguridad te gustaría automatizar.']},
         'cel': {'mat': ['Tus programas de las prácticas 1 y 2', 'Pydroid 3 o un compilador en línea'],
                 'steps': [
                     'Antes de empezar, termina los laboratorios «Entrada, conversión y salida» y «Depura el programa».',
                     ['Haz un programa con input() para el usuario y la longitud de la contraseña, convierte con int() y calcula las combinaciones.', 'online'],
                     'Muestra un resumen con f-string y una variable lógica: ¿la contraseña es segura?',
                     ['Provoca un error de sintaxis y uno de ejecución, toma captura, explica y corrige.', 'errores'],
                     'Escribe qué herramientas usaste y qué otra tarea de seguridad te gustaría automatizar.']}},
     'entrega': ['El programa final, las capturas de los errores y tu explicación; es la base de tu reporte de evaluación.'],
     'rub': [['input con conversión correcta', 25], ['Resumen con f-string y variable lógica', 25], ['Dos errores explicados y corregidos', 30], ['Herramientas y reflexión', 20]]},
]

EVALUATION = {
    'course': 'MTCS-20 · Manejo de tecnologías de ciberseguridad · Unidad 3',
    'ra': 'R.A. 3.1', 'title': 'Reporte de fundamentos y lenguajes de programación',
    'data': [
        ('Resultado de aprendizaje', 'Utiliza fundamentos y lenguajes de programación informática de acuerdo con las operaciones requeridas a fin de optimizar funciones y acciones predefinidas.'),
        ('Actividad de evaluación', '3.1.1 Elabora un reporte demostrando el uso de fundamentos y lenguajes de programación empleando las operaciones predefinidas.'),
        ('Evidencia', 'Reporte (PDF)'),
        ('Ponderación', '20% (según el programa)'),
        ('Entrega', 'Viernes 4 de diciembre, en la actividad R.A. 3.1 de la plataforma'),
    ],
    'situation': 'En la actividad de evaluación de la plataforma tienes asignado el <b>sistema de control de acceso</b> de un lugar, con su número de usuarios, la longitud de contraseña, el conjunto de caracteres permitido y los intentos por segundo de un atacante. Escribe programas en Python que lo analicen y elabora un reporte con el código, la salida y tus explicaciones.',
    'hint': 'Usa SIEMPRE los datos de TU escenario en el código: cada programa del reporte debe mostrar esos números en la salida.',
    'steps': [
        ('Contexto y conceptos (Bloque A)', [
            'Describe el sistema asignado y para qué sirve programar en su seguridad.',
            'Explica con tus palabras: programa, algoritmo, entrada-proceso-salida y archivo fuente.',
            'Indica el lenguaje (Python), si es interpretado o compilado, y las herramientas que usaste.']),
        ('Programas (Bloque B)', [
            'Programa 1: variables de los tipos str, int, float y bool con los datos asignados, mostrando el tipo de cada una con type().',
            'Programa 2: cálculo de combinaciones posibles, segundos, horas y minutos para adivinar la contraseña, con los operadores **, /, // y %.',
            'Programa 3: variables lógicas con comparaciones y con and, or o not (por ejemplo, ¿la contraseña es segura?), usando input() con conversión.']),
        ('Errores y cierre', [
            'Un error de sintaxis y uno de ejecución o de lógica que cometiste: captura, explicación y corrección.',
            'Conclusión: qué otra tarea de seguridad te gustaría automatizar con programación.']),
        ('Entrega', ['Llena las secciones de la actividad en la plataforma y adjunta tu reporte en PDF con el código y las capturas de la salida.']),
    ],
    'rubric': [('Contexto y conceptos', 15), ('Lenguaje, archivo fuente y herramientas', 10), ('Variables y tipos de datos', 20), ('Operadores y cálculos con los datos asignados', 25), ('Errores explicados y corregidos', 15), ('Redacción y presentación del reporte', 15)],
    'deliver': ['Un archivo PDF con tu reporte, tu código y las capturas de la salida.', 'Se entrega en la actividad R.A. 3.1 de la plataforma, junto con las secciones escritas.'],
}
