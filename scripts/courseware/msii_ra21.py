"""MSII-05 · R.A. 2.1 · Opera el sistema operativo monousuario.

Caso del módulo: el Cibercafé Nova del R.A. 1.2 (el alumno es su técnico).
Incluye tres consolas simuladas (CMD y PowerShell) definidas en shell_sim.js.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MSII-RA-2.1'
CODE_PREFIX = 'MSII21'
FILE = 'msii-ra21-material.html'
TITLE_TAG = 'MSII-05 · R.A. 2.1 · Opera el sistema operativo'
BRAND = 'MSII-05 · Sistemas operativos'
BRAND_SUB = 'R.A. 2.1 · Opera el sistema operativo monousuario'
HERO_KICK = 'MSII-05 · R.A. 2.1'
HERO_TITLE = 'Opera el sistema operativo con comandos'
HERO_TEXT = 'Eres el técnico del Cibercafé Nova: organiza carpetas, configura el sistema y automatiza con CMD y PowerShell, sin miedo a equivocarte.'
EV_SHORT = 'haz tu sesión práctica y tu listado de comandos.'
EV_CARD = 'Sesión práctica'
RA = 'R.A. 2.1'
GROUP = '310'

TABS = {'d': ['Diagnostica', 'Comandos y simulador'], 'c': ['Construye', 'Prácticas con CMD y PowerShell']}

EXTRA_JS = (Path(__file__).parent / 'shell_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".cmdsim"))cmdInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".cmdsim"))return cmdCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cid, mode, intro, tasks, hint, setup=None):
    """tasks: [texto, expresión JS con la api a (a.has, a.isDir, a.fileText, a.used, a.env, a.cwd)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    cfg = f'{{id:{j(cid)},mode:{j(mode)},intro:{j(intro)},hint:{j(hint)},setup:{j(setup or [])},tasks:{ts}}}'
    return c.raw(f'pCmd({j(ic)},{j(t)},{j(inf)},{cfg})')


U = r'C:\\Users\\Alumno\\'  # dentro de expresiones JS

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏠', 'Tú eres el técnico del Cibercafé Nova', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Operar el sistema operativo es <b>saber darle órdenes</b>: organizar carpetas y archivos, consultar cómo está el equipo y configurarlo, con ventanas y también con <b>comandos</b>.'),
    ex('Caso para todo el módulo: Cibercafé Nova', 'El Nova tiene 10 computadoras para clientes. Cada día hay que organizar carpetas, borrar lo que dejan los clientes, respaldar en la USB y revisar el equipo. Con el ratón son muchos clics en cada PC; con comandos, unos segundos.'),
    bk('Sin miedo', 'Vas a practicar en <b>consolas simuladas</b> dentro de este material: si te equivocas, no pasa nada; reinicias y lo intentas otra vez.')),
    'Las ventanas son cómodas; los comandos son rápidos y se pueden repetir.')
c.L('🗺️', 'Tu ruta en este R.A.', 'Cuatro bloques y una evidencia', body(
    bk('A · El sistema operativo', 'Qué es y qué funciones cumple.'),
    bk('B · MS-DOS y Windows', 'Unidades, carpetas, archivos, rutas y comandos; la interfaz gráfica y sus administradores.'),
    bk('C · Configuración', 'Información del sistema y variables de entorno.'),
    bk('D · PowerShell', 'La consola moderna de Windows.'),
    bk('Al final entregas', 'El <b>reporte de una sesión práctica</b> y el <b>listado de los comandos</b> que usaste (25%). Cada práctica te deja capturas y comandos para ese reporte.', 'sp')),
    'Anota cada comando que aprendas: tu listado se arma solo.')
c.A('🖱️', '¿Ventanas o comandos?', 'Decide si cada acción se hace en la interfaz gráfica o en la línea de comandos.', [
    ['Dar doble clic en una carpeta para abrirla', 'Interfaz gráfica', 'Usas el ratón sobre ventanas e íconos.'],
    ['Escribir CD Documentos', 'Línea de comandos', 'Es una orden escrita en la consola.'],
    ['Arrastrar un archivo a la papelera', 'Interfaz gráfica', 'Se hace con el ratón.'],
    ['Escribir DEL foto.jpg', 'Línea de comandos', 'Es el comando para borrar un archivo.'],
    ['Escribir Get-Process en PowerShell', 'Línea de comandos', 'PowerShell también es una consola de comandos.'],
    ['Abrir el menú Inicio y elegir un programa', 'Interfaz gráfica', 'El menú Inicio es parte de la interfaz gráfica.'],
], 'Ratón y ventanas = gráfica · Escribir órdenes = comandos.', ['Interfaz gráfica', 'Línea de comandos'])
s0_end = c.mark() - 1

# ───────────────────────── Bloque A ─────────────────────────
a0 = c.mark()
c.L('🧠', '¿Qué es un sistema operativo?', 'Bloque A · El programa más importante del equipo', body(
    sp('En palabras sencillas', 'El sistema operativo (SO) es el <b>programa principal que administra la computadora</b> y hace de intermediario entre ti, tus programas y el hardware.'),
    ana('Piensa en un restaurante', 'Tú (usuario) pides al mesero (sistema operativo); el mesero lleva el pedido a la cocina (hardware) y te trae el platillo. Tú no entras a la cocina.'),
    bk('Ejemplos', 'Windows, Linux, macOS, Android. <b>MS-DOS</b> fue el sistema de Microsoft antes de Windows: todo se hacía con comandos, y de ahí viene el Símbolo del sistema.')),
    'Sin sistema operativo, la computadora no sabe qué hacer.')
c.L('🧰', 'Las funciones del sistema operativo', 'Bloque A · Qué servicios te da', body(
    bk('⚙️ Procesos', 'Reparte el procesador entre los programas abiertos.'),
    bk('🧮 Memoria', 'Decide qué programa usa qué parte de la RAM.'),
    bk('📁 Archivos', 'Guarda, organiza y encuentra tus archivos en carpetas.'),
    bk('🖨️ Dispositivos', 'Se comunica con impresora, teclado o USB usando controladores.'),
    bk('🔐 Seguridad', 'Pide usuario y contraseña, y controla los permisos.'),
    bk('🖥️ Interfaz', 'Te deja darle órdenes con ventanas o con comandos.'),
    ex('En el Nova', 'Un cliente abre Chrome (proceso), guarda su tarea (archivos), la imprime (dispositivos) e inició sesión con la cuenta Cliente (seguridad).')),
    'Procesos, memoria, archivos, dispositivos, seguridad e interfaz.')
c.L('👤', 'Monousuario, multiusuario y multitarea', 'Bloque A · Formas de dar el servicio', body(
    bk('Monousuario', 'Lo usa <b>una persona a la vez</b>. Ejemplo: MS-DOS o la PC del cibercafé con un cliente sentado.'),
    bk('Multiusuario', 'Lo usan <b>varias personas al mismo tiempo</b>, por ejemplo un servidor Linux. Lo verás en el R.A. 2.2.'),
    bk('Monotarea y multitarea', 'MS-DOS corría <b>un programa a la vez</b> (monotarea). Windows corre muchos al mismo tiempo (multitarea).'),
    ana('Piensa en…', 'Una bicicleta (una persona) contra un camión (muchas personas). Y un cocinero que hace un platillo a la vez contra uno que cuida varias ollas.')),
    'Este R.A. trata del sistema monousuario: MS-DOS y Windows.')
c.A('🧰', '¿Qué función del SO trabaja?', 'Elige la función del sistema operativo en cada situación.', [
    ['Windows reparte el procesador entre Chrome y Word', 'Procesos', 'Administrar los programas en ejecución es la gestión de procesos.'],
    ['Guardas tu tarea en la carpeta Documentos', 'Archivos', 'Organizar archivos y carpetas es la gestión de archivos.'],
    ['La impresora recibe tu documento', 'Dispositivos', 'El SO se comunica con la impresora mediante su controlador.'],
    ['Te pide contraseña al iniciar sesión', 'Seguridad', 'Controlar quién entra es una función de seguridad.'],
    ['Al abrir muchos programas se llena la RAM', 'Memoria', 'El SO decide cómo se reparte la memoria.'],
    ['Das doble clic en un ícono', 'Interfaz', 'La interfaz es la forma en que le das órdenes al SO.'],
], 'Pregúntate qué está administrando el sistema en ese momento.', ['Procesos', 'Memoria', 'Archivos', 'Dispositivos', 'Seguridad', 'Interfaz'])
c.A('👥', '¿Cómo es cada sistema?', 'Clasifica cada caso.', [
    ['MS-DOS: una persona y un programa a la vez', 'Monousuario y monotarea', 'Un usuario y un solo programa al mismo tiempo.'],
    ['Windows en una PC del Nova: un cliente con varios programas abiertos', 'Monousuario y multitarea', 'Una persona, pero muchos programas a la vez.'],
    ['Un servidor Linux con 30 usuarios conectados', 'Multiusuario y multitarea', 'Muchas personas y muchos programas a la vez.'],
    ['Tu celular: tú solo, con varias apps abiertas', 'Monousuario y multitarea', 'Lo usa una persona, con varias apps a la vez.'],
    ['El servidor de la escuela al que entran muchos alumnos a la vez', 'Multiusuario y multitarea', 'Varios usuarios al mismo tiempo.'],
], 'Primero cuenta personas; luego cuenta programas.', ['Monousuario y monotarea', 'Monousuario y multitarea', 'Multiusuario y multitarea'])
c.O('🖨️', 'Ordena: ¿qué pasa cuando imprimes?', 'Pon en orden lo que ocurre desde tu clic hasta la hoja impresa.', [
    ['Das clic en Imprimir', 'Todo empieza con la orden del usuario.'],
    ['Word le pide al sistema operativo que imprima', 'El programa no habla directo con la impresora: se lo pide al SO.'],
    ['El SO pone el documento en la cola de impresión', 'El SO organiza los trabajos en turno.'],
    ['El controlador traduce el documento para la impresora', 'El controlador sabe hablar el idioma de esa impresora.'],
    ['La impresora imprime la hoja', 'El hardware hace el trabajo final.'],
], 'Usuario → programa → sistema operativo → controlador → hardware.')
a_end = c.mark() - 1

# ───────────────────────── Bloque B ─────────────────────────
b0 = c.mark()
c.L('🗄️', 'Unidades, carpetas y archivos', 'Bloque B · Cómo se organiza la información', body(
    bk('💽 Unidad', 'Donde se guarda la información. Se nombra con una letra: <b>C:</b> el disco, <b>D:</b> o <b>E:</b> una USB.'),
    bk('📁 Directorio (carpeta)', 'Un cajón que agrupa archivos y otras carpetas.'),
    bk('📄 Fichero (archivo)', 'El documento en sí. Tiene nombre y <b>extensión</b>, que dice su tipo: .txt texto, .docx Word, .jpg imagen, .exe programa.'),
    ana('Piensa en un archivero', 'El mueble es la unidad, los cajones son carpetas y las hojas son archivos.'),
    ex('En el Nova', 'La tarea de un cliente está en <b>C:\\Users\\Alumno\\Documentos\\tarea.docx</b>: unidad C:, carpetas Users, Alumno y Documentos, y el archivo tarea.docx.')),
    'Unidad › carpetas › archivo.extensión')
c.L('🧭', 'Rutas absolutas y relativas', 'Bloque B · La dirección de cada archivo', body(
    sp('En palabras sencillas', 'Una ruta es la <b>dirección</b> de un archivo o carpeta. Las carpetas se separan con <b>\\</b>.'),
    bk('Absoluta', 'Completa, desde la unidad: <b>C:\\Users\\Alumno\\Descargas</b>. Funciona desde cualquier lugar.'),
    bk('Relativa', 'Desde donde estás parado: <b>Descargas</b> o <b>..\\Descargas</b>. Es más corta, pero depende de dónde estés.'),
    bk('Dos atajos', '<b>.</b> significa «aquí» y <b>..</b> significa «la carpeta de arriba».'),
    ana('Piensa en…', 'Dar tu dirección completa con calle, colonia y código postal (absoluta) o decir «dos casas a la derecha» (relativa).')),
    'Absoluta empieza con la unidad; relativa empieza desde donde estás.')
c.A('🧭', '¿Absoluta o relativa?', 'Clasifica cada ruta.', [
    ['C:\\Users\\Alumno\\Descargas', 'Absoluta', 'Empieza con la unidad C:.'],
    ['Documentos\\Nova', 'Relativa', 'Depende de dónde estés parado.'],
    ['..\\Descargas', 'Relativa', '«..» significa la carpeta de arriba: depende de dónde estés.'],
    ['D:\\Respaldo', 'Absoluta', 'Empieza con la unidad D:.'],
    ['Nova\\Precios\\lista.txt', 'Relativa', 'No dice la unidad: parte de la carpeta actual.'],
    ['C:\\Windows\\System32', 'Absoluta', 'Ruta completa desde la unidad.'],
], 'Si empieza con una letra y dos puntos (C:, D:), es absoluta.', ['Absoluta', 'Relativa'])
c.Z('🧩', 'Completa la ruta', 'Estás en <b>C:\\Users\\Alumno\\Documentos</b>. Elige la ruta correcta en cada caso.',
    '<p>Para entrar a la carpeta Nova que está aquí: CD {0}</p>'
    '<p>Para subir a C:\\Users\\Alumno: CD {1}</p>'
    '<p>Para ir a Descargas, que está al lado de Documentos: CD {2}</p>'
    '<p>La ruta absoluta de Documentos es {3}</p>'
    '<p>Para ir a la raíz de la USB escribes primero {4}</p>',
    [['Nova', ['Nova', '..\\Nova', 'C:\\Nova']],
     ['..', ['..', '.', '\\']],
     ['..\\Descargas', ['..\\Descargas', 'Descargas', '\\Descargas']],
     ['C:\\Users\\Alumno\\Documentos', ['C:\\Users\\Alumno\\Documentos', 'Alumno\\Documentos', '..\\Documentos']],
     ['D:', ['D:', 'CD D', 'USB']]],
    'Dibuja el árbol en tu cuaderno: Alumno tiene dentro a Documentos y a Descargas.')
c.L('⌨️', 'Abrir el Símbolo del sistema', 'Bloque B · La consola heredera de MS-DOS', body(
    bk('Cómo abrirlo', 'Presiona <b>Win + R</b>, escribe <b>cmd</b> y Enter. O busca «Símbolo del sistema» en Inicio.'),
    bk('El indicador', '<b>C:\\Users\\Alumno&gt;</b> te dice <b>dónde estás</b>. Ahí escribes y das Enter.'),
    bk('Reglas', 'Comando + espacio + lo que necesita. Mayúsculas o minúsculas da igual. Si un nombre tiene espacios, va entre comillas: CD "Mis tareas".'),
    bk('Trucos', '<b>Tab</b> completa nombres, <b>flecha ↑</b> repite el comando anterior, <b>HELP</b> lista los comandos.'),
    ex('Truco del técnico', 'En la barra de direcciones del Explorador escribe <b>cmd</b> y Enter: se abre la consola en esa carpeta.')),
    'Lee siempre el indicador: te dice en qué carpeta estás.')
c.L('🚶', 'Moverte por las carpetas: DIR, CD y TREE', 'Bloque B · Gestión de unidades y directorios', body(
    bk('DIR', 'Muestra lo que hay en la carpeta. <b>&lt;DIR&gt;</b> marca las carpetas.'),
    bk('CD carpeta', 'Entra a una carpeta. <b>CD ..</b> sube un nivel; <b>CD \\</b> va a la raíz de la unidad.'),
    bk('TREE', 'Dibuja el árbol de carpetas. Con <b>/F</b> también muestra los archivos.'),
    bk('D:', 'Escribir solo la letra y dos puntos te cambia de unidad (por ejemplo, a la USB).'),
    px('Ejemplo paso a paso', ['<b>DIR</b> → ves Escritorio, Documentos y Descargas.', '<b>CD Documentos</b> → el indicador cambia a C:\\Users\\Alumno\\Documentos&gt;', '<b>CD ..</b> → regresas a C:\\Users\\Alumno&gt;', '<b>D:</b> → ahora estás en la USB: D:\\&gt;', '<b>C:</b> → regresas al disco.'])),
    'DIR para ver, CD para moverte, TREE para el mapa.')
c.L('🛠️', 'Crear, copiar, mover y borrar', 'Bloque B · Gestión de archivos y carpetas', body(
    bk('MD nombre', 'Crea una carpeta. <b>RD nombre</b> la borra si está vacía (<b>RD /S</b> la borra con todo).'),
    bk('ECHO texto &gt; archivo.txt', 'Crea un archivo de texto con ese contenido. <b>TYPE archivo.txt</b> lo muestra.'),
    bk('COPY origen destino', 'Copia un archivo. <b>MOVE</b> lo mueve (no deja copia).'),
    bk('REN viejo nuevo', 'Cambia el nombre. El nombre nuevo va sin ruta.'),
    bk('DEL archivo', 'Borra un archivo. Con <b>*.txt</b> borra todos los .txt.'),
    warn('Cuidado', 'DEL y RD <b>no mandan a la papelera</b>: lo borrado ya no se recupera. Revisa con DIR antes de borrar.')),
    'Antes de borrar, mira con DIR.')
c.A('🧰', '¿Qué comando uso?', 'Elige el comando para cada tarea del técnico.', [
    ['Ver qué hay en la carpeta', 'DIR', 'DIR lista el contenido de la carpeta.'],
    ['Entrar a la carpeta Nova', 'CD', 'CD cambia de carpeta.'],
    ['Crear la carpeta Clientes', 'MD', 'MD (o MKDIR) crea carpetas.'],
    ['Copiar lista.txt a la USB', 'COPY', 'COPY copia sin borrar el original.'],
    ['Cambiar el nombre de notas.txt', 'REN', 'REN renombra.'],
    ['Borrar foto1.jpg', 'DEL', 'DEL borra archivos.'],
    ['Ver el contenido de un .txt', 'TYPE', 'TYPE muestra el texto del archivo.'],
    ['Ver el árbol de carpetas', 'TREE', 'TREE dibuja la estructura.'],
], 'Ver = DIR · Moverse = CD · Crear carpeta = MD · Copiar = COPY · Renombrar = REN · Borrar = DEL.',
    ['DIR', 'CD', 'MD', 'COPY', 'REN', 'DEL', 'TYPE', 'TREE'])
c.Z('✍️', 'Completa los comandos', 'Elige lo que falta en cada comando.',
    '<p>Para subir a la carpeta anterior: {0}</p>'
    '<p>Para copiar a la USB: COPY lista.txt {1}</p>'
    '<p>Para renombrar: REN notas.txt {2}</p>'
    '<p>Para crear un archivo con texto: ECHO Turno matutino {3} turnos.txt</p>'
    '<p>Para borrar todos los archivos .tmp: DEL {4}</p>',
    [['CD ..', ['CD ..', 'CD /', 'UP']],
     ['D:\\', ['D:\\', 'USB', 'D.txt']],
     ['pendientes.txt', ['pendientes.txt', 'D:\\pendientes.txt', '/pendientes']],
     ['>', ['>', '<', '|']],
     ['*.tmp', ['*.tmp', 'todo.tmp', '.tmp*']]],
    'Recuerda: «..» sube, «>» manda el texto a un archivo y «*» significa «cualquier nombre».')
sim('🖥️', 'Simulador: organiza las carpetas del Nova', 'Bloque B · Practica DIR, CD, MD y TREE sin riesgo', 'b1', 'cmd',
    'Escribe los comandos en la consola negra y presiona Enter. Los retos se marcan solos.',
    [['Entra a tu carpeta <b>Documentos</b>', 'a.cwd()=="c:\\\\users\\\\alumno\\\\documentos"||a.isDir("' + U + 'Documentos\\\\Nova")'],
     ['Crea la carpeta <b>Nova</b> dentro de Documentos', f'a.isDir("{U}Documentos\\\\Nova")'],
     ['Dentro de Nova crea las carpetas <b>Clientes</b> y <b>Precios</b>', f'a.isDir("{U}Documentos\\\\Nova\\\\Clientes")&&a.isDir("{U}Documentos\\\\Nova\\\\Precios")'],
     ['Sube un nivel con <b>CD ..</b>', 'a.used("cd ..")'],
     ['Dibuja el árbol de Nova con <b>TREE</b>', 'a.used("tree:c:\\\\users\\\\alumno\\\\documentos\\\\nova")']],
    'Si te pierdes, escribe DIR para ver dónde estás. Para el árbol puedes escribir TREE desde Nova o TREE Nova desde Documentos.')
sim('📦', 'Simulador: archivos y unidades', 'Bloque B · Practica COPY, ECHO, REN, DEL y el cambio de unidad', 'b2', 'cmd',
    'Ya existe Documentos\\Nova con Clientes y Precios. En Descargas hay archivos que dejó un cliente.',
    [['Copia <b>lista_precios.txt</b> de Descargas a <b>Nova\\Precios</b>', f'a.has("{U}Documentos\\\\Nova\\\\Precios\\\\lista_precios.txt")'],
     ['Crea <b>Nova\\Clientes\\turnos.txt</b> con el texto «Turno matutino»', f'a.fileText("{U}Documentos\\\\Nova\\\\Clientes\\\\turnos.txt").indexOf("turno matutino")>-1'],
     ['En Descargas, renombra <b>notas.txt</b> como <b>pendientes.txt</b>', f'a.has("{U}Descargas\\\\pendientes.txt")&&!a.has("{U}Descargas\\\\notas.txt")'],
     ['Borra <b>foto1.jpg</b> de Descargas', f'!a.has("{U}Descargas\\\\foto1.jpg")'],
     ['Cámbiate a la unidad <b>D:</b> (la USB)', 'a.used("unidad:d:")'],
     ['Respalda <b>lista_precios.txt</b> en <b>D:\\Respaldo</b>', 'a.has("D:\\\\Respaldo\\\\lista_precios.txt")']],
    'Puedes usar rutas absolutas (C:\\Users\\Alumno\\Descargas\\lista_precios.txt) o relativas (..\\Descargas). Para el respaldo: COPY C:\\Users\\Alumno\\Descargas\\lista_precios.txt D:\\Respaldo',
    setup=['C:\\Users\\Alumno\\Documentos\\Nova\\Clientes\\', 'C:\\Users\\Alumno\\Documentos\\Nova\\Precios\\'])
c.L('🪟', 'La interfaz gráfica de Windows', 'Bloque B · Características, arquitectura y elementos', body(
    bk('Elementos', '<b>Escritorio</b>, <b>barra de tareas</b>, <b>menú Inicio</b>, <b>ventanas</b>, <b>íconos</b> y el <b>área de notificación</b> (reloj, red, volumen).'),
    bk('Características', 'Gráfica (todo con ratón o toque), multitarea, con usuarios y permisos, y compatible con muchísimo hardware gracias a los controladores.'),
    bk('Arquitectura, en capas', '<b>Núcleo (kernel)</b>: administra procesador y memoria. <b>Controladores</b>: hablan con el hardware. <b>Servicios</b>: trabajan en segundo plano (impresión, actualizaciones). <b>Interfaz</b>: el escritorio y las ventanas que ves.'),
    ana('Piensa en un edificio', 'Los cimientos son el núcleo, las tuberías y cables son controladores y servicios, y los departamentos decorados son la interfaz.')),
    'Lo que ves (interfaz) está montado sobre lo que no ves (núcleo, controladores y servicios).')
c.L('🗂️', 'Administrador de archivos y de programas', 'Bloque B · Las dos herramientas del técnico', body(
    bk('Explorador de archivos (Win + E)', 'Es el <b>administrador de archivos</b>: panel de navegación, barra de direcciones (da clic en ella y verás la ruta absoluta) y vistas. Activa <b>Vista › Mostrar › Extensiones de nombre de archivo</b> para ver .txt, .exe…'),
    bk('Administrador de tareas (Ctrl + Shift + Esc)', 'Es el <b>administrador de programas</b>: pestañas Procesos, Rendimiento y Aplicaciones de inicio. Con <b>Finalizar tarea</b> cierras un programa congelado.'),
    bk('Programas instalados', '<b>Configuración › Aplicaciones</b>: ver y desinstalar programas.'),
    ex('En el Nova', 'Un cliente dice que el navegador «se trabó». Abres el Administrador de tareas, eliges el programa y das Finalizar tarea.')),
    'Explorador = archivos · Administrador de tareas = programas en ejecución.')
c.A('🔁', 'Comando y ventana: ¿qué equivale?', 'Relaciona cada comando con lo que harías con el ratón.', [
    ['DIR', 'Abrir la carpeta y ver su contenido', 'Ambos muestran lo que hay en la carpeta.'],
    ['MD', 'Clic derecho › Nuevo › Carpeta', 'Ambos crean una carpeta.'],
    ['REN', 'Clic derecho › Cambiar nombre', 'Ambos renombran.'],
    ['COPY', 'Ctrl + C y Ctrl + V', 'Ambos copian.'],
    ['CD', 'Doble clic para entrar a una carpeta', 'Ambos te cambian de carpeta.'],
    ['DEL', 'Seleccionar y presionar Supr', 'Ambos borran, pero DEL no usa la papelera.'],
], 'Piensa qué harías con el ratón para lograr lo mismo.')
c.A('🧑‍🔧', '¿Explorador o Administrador de tareas?', 'Elige la herramienta para cada problema.', [
    ['Un programa se congeló', 'Administrador de tareas', 'Ahí se finaliza el proceso.'],
    ['Buscar dónde quedó una descarga', 'Explorador de archivos', 'Es la herramienta para navegar por carpetas.'],
    ['Ver cuánta RAM se está usando', 'Administrador de tareas', 'La pestaña Rendimiento muestra la memoria.'],
    ['Mostrar las extensiones de los archivos', 'Explorador de archivos', 'Se activa en el menú Vista del Explorador.'],
    ['Quitar un programa que arranca solo al encender', 'Administrador de tareas', 'Pestaña Aplicaciones de inicio.'],
    ['Copiar la ruta absoluta de una carpeta', 'Explorador de archivos', 'Clic en la barra de direcciones y se copia la ruta.'],
], 'Archivos y carpetas → Explorador · Programas y rendimiento → Administrador de tareas.', ['Explorador de archivos', 'Administrador de tareas'])
b_end = c.mark() - 1

# ───────────────────────── Bloque C ─────────────────────────
c0 = c.mark()
c.L('⚙️', 'Configurar el sistema operativo', 'Bloque C · Dónde se ajusta Windows', body(
    bk('Configuración (Win + I)', 'Sistema (pantalla, sonido, almacenamiento, información), Personalización, Aplicaciones, Cuentas, Hora e idioma y Windows Update. El <b>Panel de control</b> clásico sigue existiendo para opciones avanzadas.'),
    bk('Consultar con comandos', '<b>VER</b> (versión de Windows), <b>HOSTNAME</b> (nombre del equipo), <b>WHOAMI</b> (usuario actual) y <b>SYSTEMINFO</b> (procesador, RAM, sistema y más).'),
    ex('En el Nova', 'Para saber cuánta RAM tiene cada una de las 10 PCs, el técnico escribe SYSTEMINFO en cada una: es más rápido que abrir varias ventanas.')),
    'Antes de configurar, consulta cómo está el equipo.')
c.L('🏷️', 'Variables de entorno', 'Bloque C · Datos con nombre que todos los programas consultan', body(
    sp('En palabras sencillas', 'Una variable de entorno es un <b>nombre que guarda un dato</b> del sistema: USERNAME (tu usuario), COMPUTERNAME (nombre del equipo), USERPROFILE (tu carpeta personal), TEMP (temporales) y PATH.'),
    ana('Piensa en tus contactos', 'Guardas «Mamá» en vez de memorizar el número. Los programas preguntan por %USERNAME% en vez de saber tu nombre.'),
    bk('En CMD', '<b>ECHO %USERNAME%</b> muestra una variable. <b>SET</b> las lista todas. <b>SET CIBER=Nova</b> crea una solo para esa ventana. <b>SETX CIBER Nova</b> la guarda para tu usuario (aparece en ventanas nuevas).'),
    bk('Con ventanas', 'Busca en Inicio «Editar las variables de entorno de esta cuenta».')),
    'En CMD las variables se escriben entre signos de porcentaje: %NOMBRE%.')
c.L('🛣️', 'PATH: dónde busca Windows los programas', 'Bloque C · La variable más importante', body(
    sp('En palabras sencillas', 'PATH es una <b>lista de carpetas</b>, separadas por punto y coma (;), donde Windows busca un programa cuando escribes su nombre.'),
    ana('Piensa en…', 'Cuando gritas «¡Mamá!» te contesta porque está en casa. Si está en otra casa, no te escucha. PATH le dice a Windows en qué «casas» buscar.'),
    ex('Ejemplo', 'Si la carpeta de 7-Zip está en PATH, puedes escribir <b>7z</b> desde cualquier carpeta. Si no, Windows responde «no se reconoce como un comando».'),
    warn('Cuidado', 'Nunca borres el PATH: muchos programas dejarían de abrir. Para verlo: ECHO %PATH%.')),
    '«No se reconoce como un comando» a veces significa que no está en PATH.')
c.A('🏷️', '¿Qué variable es?', 'Elige la variable que guarda cada dato.', [
    ['El nombre del usuario que inició sesión', 'USERNAME', 'USERNAME guarda el usuario actual.'],
    ['El nombre del equipo, como NOVA-PC01', 'COMPUTERNAME', 'COMPUTERNAME es el nombre de la computadora.'],
    ['Las carpetas donde Windows busca programas', 'PATH', 'PATH es la lista de carpetas de búsqueda.'],
    ['La carpeta de archivos temporales', 'TEMP', 'TEMP indica dónde van los temporales.'],
    ['La carpeta personal del usuario', 'USERPROFILE', 'USERPROFILE es C:\\Users\\tu_usuario.'],
], 'Lee el nombre en inglés: USER = usuario, COMPUTER = computadora, TEMP = temporal.', ['USERNAME', 'COMPUTERNAME', 'PATH', 'TEMP', 'USERPROFILE'])
c.A('⚖️', '¿SET o SETX?', 'Decide qué comando usar.', [
    ['Crear una variable solo para esta ventana', 'SET', 'SET dura mientras la ventana esté abierta.'],
    ['Guardar una variable para siempre en tu usuario', 'SETX', 'SETX la guarda de forma permanente.'],
    ['Ver la lista de todas las variables', 'SET', 'SET sin nada más lista todas.'],
    ['Que la variable exista al abrir otra ventana', 'SETX', 'Solo SETX la conserva en ventanas nuevas.'],
    ['Mostrar las variables que empiezan con P', 'SET', 'SET P lista las que empiezan con P.'],
], 'SET = temporal y para consultar · SETX = permanente.', ['SET', 'SETX'])
sim('🧪', 'Simulador: consulta y configura el equipo', 'Bloque C · Practica VER, HOSTNAME, SET y las variables', 'c1', 'cmd',
    'Eres el técnico del Nova revisando la PC 01.',
    [['Muestra la versión de Windows', 'a.used("ver")'],
     ['Muestra el nombre del equipo', 'a.used("hostname")||a.used("%computername%")'],
     ['Muestra tu usuario con <b>ECHO %USERNAME%</b>', 'a.used("%username%")'],
     ['Lista todas las variables con <b>SET</b>', 'a.used("set:lista")'],
     ['Crea la variable <b>CIBER</b> con el valor <b>Nova</b>', 'a.env("CIBER").toLowerCase()=="nova"'],
     ['Muestra el valor de CIBER con ECHO', 'a.used("%ciber%")'],
     ['Muestra el contenido de <b>PATH</b>', 'a.used("%path%")||a.used("set")&&a.used("%path%")']],
    'Para crear la variable: SET CIBER=Nova (sin espacios alrededor del =). Para mostrarla: ECHO %CIBER%.')
c.T('🧠', '¿Qué escribes?', 'Escribe el comando completo. Las mayúsculas no importan.', [
    ['Para ver el nombre del equipo', ['HOSTNAME', 'ECHO %COMPUTERNAME%'], 'HOSTNAME (o ECHO %COMPUTERNAME%).', 'Host = anfitrión, el equipo.'],
    ['Para ver tu nombre de usuario con una variable', ['ECHO %USERNAME%'], 'ECHO %USERNAME%.', 'ECHO y la variable entre %.'],
    ['Para ver procesador, RAM y versión de Windows', ['SYSTEMINFO'], 'SYSTEMINFO muestra la información del sistema.', 'System + info.'],
    ['Para listar todas las variables de entorno', ['SET'], 'SET sin nada más.', 'Tres letras.'],
    ['Para ver la versión de Windows', ['VER'], 'VER (de «versión»).', 'Tres letras.'],
], 'Si no te acuerdas, repasa la lección «Configurar el sistema operativo».', 'u')
c_end = c.mark() - 1

# ───────────────────────── Bloque D ─────────────────────────
d0 = c.mark()
c.L('💙', '¿Qué es PowerShell?', 'Bloque D · La consola moderna de Windows', body(
    sp('En palabras sencillas', 'PowerShell es la <b>consola moderna de Windows</b>. Sus comandos se llaman <b>cmdlets</b> y siempre son <b>Verbo-Sustantivo</b> en inglés: Get-ChildItem, Set-Location, New-Item.'),
    ana('Piensa en…', 'CMD es una calculadora básica; PowerShell es una calculadora científica: hace lo mismo y mucho más.'),
    bk('Cómo abrirlo', 'Clic derecho en Inicio › <b>Terminal</b> (o busca «Windows PowerShell»). El indicador empieza con <b>PS</b>: PS C:\\Users\\Alumno&gt;'),
    bk('Buena noticia', 'Acepta los nombres que ya conoces: <b>dir</b>, <b>cd</b>, <b>md</b>, <b>copy</b> funcionan como alias.')),
    'Verbo-Sustantivo: dices qué quieres hacer y con qué.')
c.L('🔁', 'De CMD a PowerShell', 'Bloque D · Los mismos trabajos, con cmdlets', body(
    bk('DIR', '<b>Get-ChildItem</b> (alias: dir, ls)'),
    bk('CD', '<b>Set-Location</b> (alias: cd)'),
    bk('MD', '<b>New-Item -ItemType Directory</b> (alias: md, mkdir)'),
    bk('ECHO texto &gt; archivo / TYPE', '<b>Set-Content</b> archivo "texto" / <b>Get-Content</b> archivo'),
    bk('COPY / MOVE / REN / DEL', '<b>Copy-Item</b> / <b>Move-Item</b> / <b>Rename-Item</b> / <b>Remove-Item</b>'),
    bk('ECHO %USERNAME%', '<b>$env:USERNAME</b>'),
    bk('HELP', '<b>Get-Help</b> comando y <b>Get-Command</b>')),
    'Si sabes CMD, ya sabes la mitad de PowerShell.')
c.L('🔗', 'Los verbos y la tubería |', 'Bloque D · Encadenar comandos', body(
    bk('Verbos más usados', '<b>Get</b> obtener · <b>Set</b> cambiar · <b>New</b> crear · <b>Remove</b> borrar.'),
    sp('La tubería |', 'Pasa el resultado de un comando al siguiente. Se escribe con la tecla <b>|</b> (junto al 1 o con AltGr).'),
    ana('Piensa en…', 'Una línea de producción: uno saca las piezas, otro las ordena y otro elige las mejores.'),
    ex('Los 3 programas que más procesador usan', '<b>Get-Process | Sort-Object CPU -Descending | Select-Object -First 3</b>: obtiene los procesos, los ordena de mayor a menor CPU y muestra los primeros 3.'),
    ex('Solo los servicios activos', '<b>Get-Service | Where-Object Status -eq Running</b>')),
    'Obtener | ordenar | elegir.')
c.A('🔤', '¿Qué verbo va?', 'Elige el verbo del cmdlet para cada tarea.', [
    ['Obtener la lista de procesos (Process)', 'Get', 'Get obtiene información.'],
    ['Crear una carpeta (Item)', 'New', 'New crea algo nuevo.'],
    ['Borrar un archivo (Item)', 'Remove', 'Remove elimina.'],
    ['Cambiar de carpeta (Location)', 'Set', 'Set cambia un valor; aquí, la ubicación.'],
    ['Ver el contenido de un archivo (Content)', 'Get', 'Get-Content obtiene el contenido.'],
], 'Obtener = Get · Cambiar = Set · Crear = New · Borrar = Remove.', ['Get', 'Set', 'New', 'Remove'])
c.A('🔁', 'Traduce de CMD a PowerShell', 'Elige el cmdlet que hace lo mismo.', [
    ['En CMD: DIR', 'Get-ChildItem', 'Obtiene los «hijos» (contenido) de una carpeta.'],
    ['En CMD: CD', 'Set-Location', 'Cambia la ubicación.'],
    ['En CMD: TYPE', 'Get-Content', 'Obtiene el contenido de un archivo.'],
    ['En CMD: COPY', 'Copy-Item', 'Copia un elemento.'],
    ['En CMD: DEL', 'Remove-Item', 'Elimina un elemento.'],
    ['En CMD: ECHO %USERNAME%', '$env:USERNAME', 'En PowerShell las variables de entorno se leen con $env:.'],
], 'Piensa qué hace el comando de CMD y búscalo como Verbo-Sustantivo.')
c.O('🔗', 'Arma la tubería', 'Ordena las partes para obtener 5 servicios activos ordenados por nombre.', [
    ['Get-Service', 'Primero se obtienen todos los servicios.'],
    ['| Where-Object Status -eq Running', 'Luego se dejan solo los que están activos.'],
    ['| Sort-Object Name', 'Después se ordenan por nombre.'],
    ['| Select-Object -First 5', 'Al final se eligen los primeros 5.'],
], 'Primero obtienes, luego filtras, ordenas y eliges.')
sim('💙', 'Simulador: PowerShell en el Nova', 'Bloque D · Practica cmdlets y la tubería', 'd1', 'ps',
    'Consola azul = PowerShell. Puedes usar los cmdlets completos o sus alias.',
    [['Muestra dónde estás con <b>Get-Location</b>', 'a.used("get-location")'],
     ['Lista el contenido de Descargas con <b>Get-ChildItem</b>', 'a.used("get-childitem")'],
     ['Crea la carpeta <b>Reportes</b> en Documentos con <b>New-Item</b>', f'a.isDir("{U}Documentos\\\\Reportes")&&a.used("new-item")'],
     ['Crea <b>Reportes\\reporte.txt</b> con el texto «Equipo NOVA-PC01» usando <b>Set-Content</b>', f'a.fileText("{U}Documentos\\\\Reportes\\\\reporte.txt").indexOf("nova-pc01")>-1'],
     ['Muestra los <b>3 procesos</b> que más CPU usan', 'a.used("sort-object")&&a.used("select-object")'],
     ['Muestra solo los <b>servicios activos</b>', 'a.used("get-service")&&a.used("where-object")'],
     ['Muestra el nombre del equipo con <b>$env:COMPUTERNAME</b>', 'a.used("$env:computername")']],
    'New-Item -Path Documentos\\Reportes -ItemType Directory · Set-Content Documentos\\Reportes\\reporte.txt "Equipo NOVA-PC01" · Get-Process | Sort-Object CPU -Descending | Select-Object -First 3')
c.W('🗣️', 'Explica un comando', 'Demuestra que entiendes la tubería.',
    'Explica con tus palabras qué hace: <b>Get-Process | Sort-Object CPU -Descending | Select-Object -First 3</b>',
    [['Tiene al menos 12 palabras', 'palabras:12'],
     ['Habla de procesos o programas', '(proceso|procesos|programa|programas|aplicacion)'],
     ['Dice que los ordena', '(ordena|orden|acomoda|mayor a menor|de mayor)'],
     ['Menciona el procesador o CPU', '(cpu|procesador)'],
     ['Dice cuántos muestra', '(3|tres|primeros)']],
    'Explica cada parte: obtener, ordenar y elegir.', 'Ejemplo: Obtiene los programas en ejecución…')
c.W('📋', 'Escribe una fila de tu listado', 'Practica el formato de tu evidencia.',
    'Escribe una fila de tu <b>listado de comandos</b>: el comando, para qué sirve y el ejemplo exacto que escribiste. Ejemplo: «COPY · copia un archivo · COPY lista.txt D:\\Respaldo».',
    [['Incluye un comando de CMD o PowerShell', '(dir|cd|md|mkdir|rd|copy|move|ren|del|type|echo|tree|set|setx|ver|hostname|systeminfo|get-|set-|new-item|remove-item|copy-item|move-item|rename-item)'],
     ['Dice para qué sirve', '(sirve|para|copia|crea|borra|muestra|lista|cambia|mueve|renombra|entra|ordena)'],
     ['Trae un ejemplo con una ruta o un nombre de archivo', '(\\\\|\\.txt|\\.docx|\\.jpg|[a-z]:|documentos|descargas|nova)'],
     ['Tiene al menos 6 palabras', 'palabras:6']],
    'Comando · para qué sirve · ejemplo.', 'Ejemplo: MD · crea una carpeta · MD Nova\\Clientes')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario (1 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Sistema operativo', 'Programa principal que administra la computadora.'),
    bk('Monousuario', 'Sistema que usa una persona a la vez.'),
    bk('Unidad', 'Lugar de almacenamiento con letra: C:, D:.'),
    bk('Directorio', 'Carpeta.'),
    bk('Fichero', 'Archivo; tiene nombre y extensión.'),
    bk('Ruta absoluta', 'Dirección completa desde la unidad.'),
    bk('Ruta relativa', 'Dirección desde la carpeta actual.'),
    bk('Indicador (prompt)', 'Texto como C:\\Users\\Alumno&gt; que dice dónde estás.'),
    bk('Comando', 'Orden escrita para el sistema.')))
c.L('📖', 'Glosario (2 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Variable de entorno', 'Nombre que guarda un dato del sistema, como USERNAME.'),
    bk('PATH', 'Lista de carpetas donde Windows busca programas.'),
    bk('Núcleo (kernel)', 'Parte central del SO que administra procesador y memoria.'),
    bk('Proceso', 'Programa en ejecución.'),
    bk('Servicio', 'Programa que trabaja en segundo plano.'),
    bk('PowerShell', 'Consola moderna de Windows.'),
    bk('Cmdlet', 'Comando de PowerShell con forma Verbo-Sustantivo.'),
    bk('Alias', 'Nombre corto de un comando (dir = Get-ChildItem).'),
    bk('Tubería |', 'Pasa el resultado de un comando al siguiente.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Laboratorio de este grupo: <b>lunes 10:40-12:20</b> (2 h). Viernes son 3 h de aula. Los simuladores funcionan en celular, así que todas las prácticas tienen versión sin laboratorio.', 'sp'),
    bk('Bloques A y B · 5 al 23-oct', 'Ya impartidos: úsalos de repaso. Los dos simuladores del Bloque B son un buen diagnóstico de 15 minutos en celular.'),
    bk('Lunes 26-oct (laboratorio)', '<b>Práctica 1</b> (CMD real: estructura del Nova). Si sobra tiempo, empieza el Bloque C.'),
    bk('Bloque C · 23-oct al 2-nov', 'Viernes 30-oct: lecciones de configuración, variables y simulador C. <b>Lunes 2-nov (laboratorio): Práctica 2</b> (SYSTEMINFO, SET, SETX, PATH).'),
    bk('Bloque D · 2 al 13-nov', 'Viernes 6-nov: PowerShell, simulador D y actividades. <b>Lunes 9-nov (laboratorio): Práctica 3</b> (PowerShell real).'),
    bk('Evaluación · viernes 13-nov', 'Sesión práctica final y entrega del reporte con el listado de comandos (25%). La evaluación se desbloquea al terminar actividades y prácticas.'),
    bk('Si el laboratorio restringe CMD o PowerShell', 'Algunas escuelas bloquean la consola. En ese caso los alumnos usan los simuladores del material y capturan sus retos resueltos.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🏠', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🧠', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🗄️', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '⚙️', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '💙', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🏠",t:"Empieza aquí",d:"Tu papel como técnico del Cibercafé Nova.",time:"20 min",obj:["Explicar qué significa operar el sistema operativo","Distinguir la interfaz gráfica de la línea de comandos","Conocer la evidencia que vas a entregar"],sum:["Operar el SO es darle órdenes: con ventanas o con comandos.","Los comandos son rápidos y se pueden repetir.","Entregas un reporte de sesión práctica y tu listado de comandos."],q:"¿Qué tarea repetitiva haces en la computadora que te gustaría hacer más rápido?"},
a:{k:"Bloque A",l:"A",ic:"🧠",t:"El sistema operativo",d:"Concepto, funciones y formas de dar servicio.",time:"60 min",obj:["Definir qué es un sistema operativo","Reconocer sus seis funciones","Distinguir monousuario de multiusuario y monotarea de multitarea"],sum:["El SO es el intermediario entre el usuario, los programas y el hardware.","Funciones: procesos, memoria, archivos, dispositivos, seguridad e interfaz.","MS-DOS: monousuario y monotarea · Windows: monousuario y multitarea."],q:"¿Qué sistema operativo usas en tu celular y cuál en la computadora?"},
b:{k:"Bloque B",l:"B",ic:"🗄️",t:"MS-DOS y Windows",d:"Unidades, rutas, comandos y la interfaz gráfica.",time:"180 min",obj:["Escribir rutas absolutas y relativas","Gestionar unidades, carpetas y archivos con comandos","Usar el Explorador y el Administrador de tareas"],sum:["Unidad › carpetas › archivo.extensión.","Absoluta empieza con la unidad; relativa desde donde estás (.. sube).","DIR, CD, MD, RD, COPY, MOVE, REN, DEL, TYPE, TREE y D: para cambiar de unidad."],q:"Escribe la ruta absoluta de una carpeta de tu computadora o tu USB.",rev:[["El sistema operativo es…",["El intermediario entre usuario, programas y hardware","Un antivirus","Un tipo de procesador"],0,"Administra la computadora y sirve de intermediario."],["Windows en una PC con un solo usuario es…",["Monousuario y multitarea","Multiusuario y monotarea","Monousuario y monotarea"],0,"Una persona a la vez, con muchos programas abiertos."]]},
c:{k:"Bloque C",l:"C",ic:"⚙️",t:"Configuración del sistema",d:"Información del sistema y variables de entorno.",time:"120 min",obj:["Consultar la información del equipo con comandos","Leer y crear variables de entorno","Explicar para qué sirve PATH"],sum:["VER, HOSTNAME, WHOAMI y SYSTEMINFO consultan el equipo.","ECHO %VARIABLE% muestra; SET crea temporal; SETX guarda permanente.","PATH es la lista de carpetas donde Windows busca programas."],q:"¿Qué variable usarías para que un programa sepa quién inició sesión?",rev:[["CD .. sirve para…",["Subir a la carpeta de arriba","Borrar la carpeta","Ir a la USB"],0,"«..» es la carpeta de arriba."],["Para borrar un archivo en CMD se usa…",["DEL","RD","REN"],0,"DEL borra archivos; RD borra carpetas."]]},
d:{k:"Bloque D",l:"D",ic:"💙",t:"PowerShell",d:"Cmdlets, alias y la tubería.",time:"150 min",obj:["Usar cmdlets Verbo-Sustantivo","Traducir comandos de CMD a PowerShell","Encadenar comandos con la tubería"],sum:["Get obtiene, Set cambia, New crea, Remove borra.","DIR = Get-ChildItem · CD = Set-Location · TYPE = Get-Content.","Tubería: Get-Process | Sort-Object CPU -Descending | Select-Object -First 3."],q:"¿Qué tarea del cibercafé automatizarías con PowerShell?",rev:[["ECHO %USERNAME% muestra…",["El usuario que inició sesión","El nombre del equipo","La versión de Windows"],0,"USERNAME guarda el usuario actual."],["SETX sirve para…",["Guardar una variable de forma permanente","Ver la versión","Borrar el PATH"],0,"SET es temporal; SETX la guarda."]]}
'''

ILL = r'''
ILL["Tú eres el técnico del Cibercafé Nova"]=function(){return flow([["🗂️","Organizar|carpetas"],["🧹","Limpiar|archivos"],["💾","Respaldar|en USB"],["🔍","Revisar|el equipo"]],"Tareas diarias del técnico")};
ILL["Tu ruta en este R.A."]=function(){return flow([["🧠","A · SO"],["🗄️","B · MS-DOS|y Windows"],["⚙️","C · Confi-|guración"],["💙","D · Power-|Shell"]],"Cuatro bloques")};
ILL["¿Qué es un sistema operativo?"]=function(){var l=[["Usuario","s","t"],["Programas","s","t"],["Sistema operativo","b","tw"],["Hardware","a","td"]],o='';l.forEach(function(x,i){var w=320-i*30,X=(340-w)/2;o+=R_(X,6+i*34,w,28,x[1],6)+T_(170,25+i*34,x[0],x[2])});return SV(340,146,o,"El sistema operativo entre los programas y el hardware")};
ILL["Las funciones del sistema operativo"]=function(){return grid3([["⚙️","Procesos"],["🧮","Memoria"],["📁","Archivos"],["🖨️","Dispositivos"],["🔐","Seguridad"],["🖥️","Interfaz"]],"Seis funciones del sistema operativo")};
ILL["Unidades, carpetas y archivos"]=function(){var t=[["💽 C:",0],["📁 Users",1],["📁 Alumno",2],["📁 Documentos",3],["📄 tarea.docx",4]],o='';t.forEach(function(x,i){var X=20+x[1]*34,y=10+i*28;o+=T_(X,y+14,x[0],i==4?"t":"t","start");if(i)o+='<path d="M'+(X-22)+','+(y-6)+' V'+(y+10)+' H'+(X-6)+'" style="fill:none;stroke:var(--line);stroke-width:2"/>'});o+=T_(330,166,"C:\\Users\\Alumno\\Documentos\\tarea.docx","tm","end");return SV(340,172,o,"Árbol de una ruta")};
ILL["Rutas absolutas y relativas"]=function(){return SV(340,130,R_(10,10,320,44,"b")+T_(170,30,"Absoluta: C:\\Users\\Alumno\\Descargas","tw")+T_(170,46,"desde la unidad, funciona en cualquier lugar","tw")+R_(10,70,320,44,"s")+T_(170,90,"Relativa (estando en Documentos): ..\\Descargas")+T_(170,106,"desde donde estás","tm"),"Ruta absoluta y relativa")};
ILL["Abrir el Símbolo del sistema"]=function(){return SV(340,110,R_(10,6,320,98,"s",8)+'<rect x="10" y="6" width="320" height="98" rx="8" style="fill:#0c0c0c"/>'+'<text x="22" y="34" style="fill:#e8e8e8;font:12px Consolas,monospace">Microsoft Windows [Versión 10.0]</text><text x="22" y="62" style="fill:#e8e8e8;font:12px Consolas,monospace">C:\\Users\\Alumno&gt;<tspan style="fill:#ffd166">cd Documentos</tspan></text><text x="22" y="88" style="fill:#e8e8e8;font:12px Consolas,monospace">C:\\Users\\Alumno\\Documentos&gt;_</text>',"Ventana del Símbolo del sistema")};
ILL["Crear, copiar, mover y borrar"]=function(){return grid3([["📁","MD|crear carpeta"],["📄","ECHO &gt;|crear archivo"],["📋","COPY|copiar"],["🚚","MOVE|mover"],["🏷️","REN|renombrar"],["🗑️","DEL|borrar"]],"Comandos de gestión")};
ILL["La interfaz gráfica de Windows"]=function(){var l=[["Interfaz (escritorio y ventanas)","a","td"],["Servicios","s","t"],["Controladores","s","t"],["Núcleo (kernel)","b","tw"]],o='';l.forEach(function(x,i){o+=R_(40,6+i*32,260,26,x[1],6)+T_(170,23+i*32,x[0],x[2])});return SV(340,138,o,"Capas de Windows")};
ILL["Variables de entorno"]=function(){var v=[["USERNAME","Alumno"],["COMPUTERNAME","NOVA-PC01"],["USERPROFILE","C:\\Users\\Alumno"],["TEMP","…\\AppData\\Local\\Temp"]],o=R_(10,4,320,24,"b",6)+T_(90,21,"Variable","tw")+T_(250,21,"Valor","tw");v.forEach(function(x,i){var y=32+i*28;o+=R_(10,y,320,24,"s",4)+T_(90,y+16,"%"+x[0]+"%")+T_(250,y+16,x[1])});return SV(340,148,o,"Variables de entorno y sus valores")};
ILL["PATH: dónde busca Windows los programas"]=function(){return flow([["⌨️","Escribes|7z"],["🔎","Windows|revisa PATH"],["📁","Carpeta|encontrada"],["▶️","Se abre|el programa"]],"Cómo usa Windows el PATH")};
ILL["Los verbos y la tubería |"]=function(){return flow([["📥","Get-Process|obtiene"],["↕️","Sort-Object|ordena"],["✂️","Select-Object|elige 3"],["📋","Resultado"]],"La tubería pasa resultados de un comando al siguiente")};
'''

EXH = r'''
function cw_(t,b,ps){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:'+(ps?'#012456':'#0c0c0c')+';color:#eee;padding:10px;font:12.5px/1.45 Consolas,monospace;white-space:pre-wrap;overflow-x:auto">'+b+'</pre></div>'}
EXH.cmd_abrir=function(){return exw(mw('Ejecutar','<div style="display:grid;gap:8px"><div>Escriba el nombre del programa…</div><div class="mfld">cmd '+mk(1)+'</div><div><span class="mbtn">Aceptar</span> '+mk(2)+'</div></div>'),['Presiona Win + R y escribe cmd.','Enter o Aceptar: se abre la consola negra.'])};
EXH.cmd_dir=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;dir\n Directorio de C:\\Users\\Alumno\n23/10/2026  10:40    &lt;DIR&gt;          Descargas\n23/10/2026  10:40    &lt;DIR&gt;          Documentos\n23/10/2026  10:40    &lt;DIR&gt;          Escritorio\n\nC:\\Users\\Alumno&gt;cd Documentos\n\nC:\\Users\\Alumno\\Documentos&gt;'),['DIR muestra las carpetas.','Después de CD, el indicador cambia.'])};
EXH.cmd_md=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documentos&gt;md Nova\nC:\\Users\\Alumno\\Documentos&gt;cd Nova\nC:\\Users\\Alumno\\Documentos\\Nova&gt;md Clientes\nC:\\Users\\Alumno\\Documentos\\Nova&gt;md Precios\nC:\\Users\\Alumno\\Documentos\\Nova&gt;md Respaldos'),['Si no ves mensaje, el comando funcionó.','Comprueba con DIR.'])};
EXH.cmd_echo=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documentos\\Nova&gt;echo Turno matutino &gt; Clientes\\turnos.txt\nC:\\Users\\Alumno\\Documentos\\Nova&gt;type Clientes\\turnos.txt\nTurno matutino'),['ECHO texto &gt; archivo crea el archivo.','TYPE muestra su contenido.'])};
EXH.cmd_copy=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documentos\\Nova&gt;echo Lista de precios &gt; ..\\..\\Descargas\\precios.txt\nC:\\Users\\Alumno\\Documentos\\Nova&gt;copy ..\\..\\Descargas\\precios.txt Precios\n        1 archivo(s) copiado(s).'),['..\\.. sube dos niveles: de Nova a Alumno.','Escribe en tu reporte qué ruta es relativa y cuál absoluta.'])};
EXH.cmd_ren=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documentos\\Nova&gt;ren Precios\\precios.txt lista_2026.txt\nC:\\Users\\Alumno\\Documentos\\Nova&gt;echo borrar &gt; temporal.txt\nC:\\Users\\Alumno\\Documentos\\Nova&gt;del temporal.txt'),['REN: el nuevo nombre va sin ruta.','DEL no usa la papelera.'])};
EXH.cmd_tree=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno\\Documentos\\Nova&gt;tree /f\nC:\\USERS\\ALUMNO\\DOCUMENTOS\\NOVA\n├───Clientes\n│       turnos.txt\n├───Precios\n│       lista_2026.txt\n└───Respaldos'),['TREE /F muestra carpetas y archivos.','Esta captura es el resumen de tu práctica.'])};
EXH.explorador=function(){return exw(mw('Explorador de archivos','<div class="mfld" style="margin-bottom:8px">C:\\Users\\Alumno\\Documentos\\Nova '+mk(1)+'</div><div class="mm"><span>📁 Clientes</span><span>📁 Precios</span><span>📁 Respaldos</span></div>'),['Da clic en la barra de direcciones: es la ruta absoluta. Lo que creaste con comandos aparece en ventanas.'])};
EXH.listado=function(){return exw('<table class="mtb"><tr><th>#</th><th>Comando</th><th>Para qué sirve</th><th>Ejemplo que escribí</th></tr><tr><td>1</td><td>MD</td><td>Crea una carpeta</td><td>md Nova</td></tr><tr><td>2</td><td>CD</td><td>Entra a una carpeta</td><td>cd Nova</td></tr><tr><td>3</td><td>COPY</td><td>Copia un archivo</td><td>copy ..\\..\\Descargas\\precios.txt Precios</td></tr></table>',['Una fila por cada comando, en el orden en que los usaste.'])};
EXH.sim_cel=function(){return exw(cw_('Simulador del material','C:\\Users\\Alumno&gt;cd Documentos\nC:\\Users\\Alumno\\Documentos&gt;md Nova\n…\n✅ Retos completados'),['Abre la sección B del material y resuelve el simulador.','Toma captura de los retos en verde.'])};
EXH.files_cel=function(){return exw(mp('Files › Almacenamiento interno','<div class="mbox">📁 Nova '+mk(1)+'</div><div class="mbox" style="margin-top:6px;margin-left:16px">📁 Clientes</div><div class="mbox" style="margin-top:6px;margin-left:16px">📁 Precios</div>'),['En Files de Google o Mis archivos: Almacenamiento interno › ⋮ › Nueva carpeta.'])};
EXH.ruta_cel=function(){return exw(mp('Detalles del archivo','<div class="mbox">Nombre: <b>foto_cliente.jpg</b><br>Ruta: <b>/storage/emulated/0/Nova/Clientes</b> '+mk(1)+'</div>'),['Mantén presionado el archivo › ⓘ Detalles.','En Android las carpetas se separan con / en lugar de \\.'])};
EXH.cmd_info=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;ver\nMicrosoft Windows [Versión 10.0.22631]\n\nC:\\Users\\Alumno&gt;hostname\nLAB3-PC07\n\nC:\\Users\\Alumno&gt;whoami\nlab3-pc07\\alumno'),['Anota los tres resultados de tu equipo.'])};
EXH.cmd_sysinfo=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;systeminfo\nNombre de host:            LAB3-PC07\nNombre del sistema operativo: Microsoft Windows 11 Pro\nProcesador(es):            Intel Core i5\nMemoria física total:      8,192 MB\nMemoria física disponible: 3,950 MB'),['Tarda unos segundos. Anota sistema, procesador y memoria.'])};
EXH.cmd_env=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;echo %USERNAME%\nAlumno\nC:\\Users\\Alumno&gt;echo %COMPUTERNAME%\nLAB3-PC07\nC:\\Users\\Alumno&gt;echo %USERPROFILE%\nC:\\Users\\Alumno'),['Las variables van entre signos %.'])};
EXH.cmd_set=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;set p\nPath=C:\\Windows\\system32;C:\\Windows;…\nPATHEXT=.COM;.EXE;.BAT;…\nPROCESSOR_ARCHITECTURE=AMD64'),['SET sola lista todas; SET P solo las que empiezan con P.'])};
EXH.cmd_settemp=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;set CIBER=Nova\nC:\\Users\\Alumno&gt;echo %CIBER%\nNova\n\n(en una ventana nueva)\nC:\\Users\\Alumno&gt;echo %CIBER%\n%CIBER%'),['En la ventana nueva ya no existe: SET es temporal.','Explica esto en tu reporte.'])};
EXH.cmd_setx=function(){return exw(cw_('Símbolo del sistema','C:\\Users\\Alumno&gt;setx CIBER Nova\nCORRECTO: se guardó el valor especificado.\n\n(en una ventana nueva)\nC:\\Users\\Alumno&gt;echo %CIBER%\nNova'),['SETX la guarda para tu usuario: aparece en ventanas nuevas.'])};
EXH.env_gui=function(){return exw(mw('Variables de entorno','<p style="margin:0 0 4px"><small>Variables de usuario para Alumno</small></p><table class="mtb"><tr><th>Variable</th><th>Valor</th></tr><tr><td><b>CIBER</b> '+mk(1)+'</td><td>Nova</td></tr><tr><td>TEMP</td><td>%USERPROFILE%\\AppData\\Local\\Temp</td></tr></table>'),['Busca en Inicio «Editar las variables de entorno de esta cuenta».','Ahí aparece la variable que creaste con SETX.'])};
EXH.cel_info=function(){return exw(mp('Acerca del teléfono','<div class="mbox">Nombre del dispositivo<br><b>Galaxy de Alumno</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Versión de Android<br><b>14</b> '+mk(2)+'</div>'),['El nombre del dispositivo es como COMPUTERNAME.','La versión es como VER.'])};
EXH.ps_abrir=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno&gt; Get-Location\n\nPath\n----\nC:\\Users\\Alumno',true),['Clic derecho en Inicio › Terminal.','El indicador empieza con PS.'])};
EXH.ps_gci=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno&gt; Get-ChildItem Documentos\n\n    Directorio: C:\\Users\\Alumno\\Documentos\n\nMode     LastWriteTime   Length Name\n----     -------------   ------ ----\nd-----   26/10/2026 11:02        Nova',true),['Es el equivalente de DIR.'])};
EXH.ps_new=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno&gt; New-Item -Path Documentos\\Nova\\Reportes -ItemType Directory\n\n    Directorio: C:\\Users\\Alumno\\Documentos\\Nova\n\nd-----   09/11/2026 10:51        Reportes',true),['-ItemType Directory crea carpeta; File crea archivo.'])};
EXH.ps_content=function(){return exw(cw_('Windows PowerShell','PS C:\\Users\\Alumno&gt; Set-Content Documentos\\Nova\\Reportes\\reporte.txt "Equipo $env:COMPUTERNAME"\nPS C:\\Users\\Alumno&gt; Get-Content Documentos\\Nova\\Reportes\\reporte.txt\nEquipo LAB3-PC07',true),['Set-Content escribe; Get-Content lee.','$env:COMPUTERNAME se cambia por el nombre real del equipo.'])};
EXH.ps_proc=function(){return exw(cw_('Windows PowerShell','PS C:\\&gt; Get-Process | Sort-Object CPU -Descending | Select-Object -First 5\n\nHandles  WS(MB)   CPU(s)     Id ProcessName\n-------  ------   ------     -- -----------\n    720     312   152.31   4120 chrome\n    410     280    88.02   6720 Teams\n    …',true),['Anota qué programas usan más procesador en tu equipo.'])};
EXH.ps_srv=function(){return exw(cw_('Windows PowerShell','PS C:\\&gt; Get-Service | Where-Object Status -eq Running\n\nStatus   Name        DisplayName\n------   ----        -----------\nRunning  Spooler     Cola de impresión\nRunning  WinDefend   Servicio antivirus de Microsoft Defender',true),['Explica qué hace un servicio de la lista.'])};
EXH.ps_tabla=function(){return exw('<table class="mtb"><tr><th>Tarea</th><th>CMD</th><th>PowerShell</th></tr><tr><td>Ver carpeta</td><td>dir</td><td>Get-ChildItem</td></tr><tr><td>Crear carpeta</td><td>md Reportes</td><td>New-Item Reportes -ItemType Directory</td></tr><tr><td>Ver usuario</td><td>echo %USERNAME%</td><td>$env:USERNAME</td></tr></table>',['Al menos 5 filas.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Organiza las carpetas del Nova con CMD',
     'prog': 'Bloque B · Gestión de unidades, directorios y ficheros con rutas absolutas y relativas',
     'min': 100, 'lug': 'Laboratorio, lunes 26-oct (2 h) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Símbolo del sistema', 'Word o Documentos de Google para el reporte', 'Recortes (Win + Shift + S)'],
                'steps': [
                    ['Abre el Símbolo del sistema con Win + R › cmd. Toma captura.', 'cmd_abrir'],
                    ['Escribe DIR y luego CD Documentos. Toma captura.', 'cmd_dir'],
                    ['Crea la estructura: MD Nova, CD Nova, MD Clientes, MD Precios y MD Respaldos.', 'cmd_md'],
                    ['Crea Clientes\\turnos.txt con ECHO y míralo con TYPE.', 'cmd_echo'],
                    ['Crea un archivo en Descargas y cópialo a Precios usando una ruta relativa (..\\..\\Descargas).', 'cmd_copy'],
                    ['Renombra un archivo con REN y borra uno de prueba con DEL.', 'cmd_ren'],
                    ['Muestra el resultado con TREE /F. Toma captura.', 'cmd_tree'],
                    ['Abre la carpeta Nova en el Explorador y compara con lo que hiciste en la consola.', 'explorador'],
                    ['Escribe tu listado de comandos: comando, para qué sirve y el ejemplo que escribiste.', 'listado']]},
         'cel': {'mat': ['Celular', 'Este material (simuladores del Bloque B)', 'App Files de Google o Mis archivos', 'Documentos de Google o notas para el reporte'],
                 'steps': [
                     ['Resuelve el simulador «Organiza las carpetas del Nova» y captura los retos en verde.', 'sim_cel'],
                     ['Resuelve el simulador «Archivos y unidades» y captura los retos en verde.', 'sim_cel'],
                     ['En tu app de archivos crea la carpeta Nova con Clientes y Precios dentro.', 'files_cel'],
                     'Copia una imagen de prueba (no personal) a Nova › Clientes y cámbiale el nombre.',
                     ['Abre los detalles del archivo y anota su ruta. Compárala con una ruta de Windows.', 'ruta_cel'],
                     ['Escribe tu listado con los comandos que usaste en los simuladores.', 'listado']]}},
     'entrega': ['Capturas en orden con una explicación breve de cada una.', 'Listado de comandos (tabla).'],
     'rub': [['Estructura de carpetas completa', 25], ['Uso correcto de rutas absolutas y relativas', 20], ['Archivos creados, copiados, renombrados y borrados', 25], ['Capturas en orden y explicadas', 15], ['Listado de comandos', 15]]},
    {'id': 'pr2', 'n': 2, 't': 'Consulta y configura el sistema',
     'prog': 'Bloque C · Configuración del sistema operativo y variables de entorno',
     'min': 100, 'lug': 'Laboratorio, lunes 2-nov (2 h) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Símbolo del sistema', 'Tu documento de reporte'],
                'steps': [
                    ['Escribe VER, HOSTNAME y WHOAMI. Toma captura.', 'cmd_info'],
                    ['Escribe SYSTEMINFO y anota sistema, procesador, memoria total y disponible.', 'cmd_sysinfo'],
                    ['Muestra ECHO %USERNAME%, ECHO %COMPUTERNAME% y ECHO %USERPROFILE%.', 'cmd_env'],
                    ['Escribe SET y luego SET P. Explica la diferencia.', 'cmd_set'],
                    ['Crea una variable temporal: SET CIBER=Nova y ECHO %CIBER%. Abre otra ventana y repite el ECHO. Explica qué pasó.', 'cmd_settemp'],
                    ['Crea la permanente: SETX CIBER Nova. Abre una ventana nueva y comprueba con ECHO.', 'cmd_setx'],
                    ['Busca en Inicio «Editar las variables de entorno de esta cuenta» y captura donde aparece CIBER.', 'env_gui'],
                    'Escribe ECHO %PATH% y explica con tus palabras para qué sirve.',
                    ['Agrega los comandos nuevos a tu listado.', 'listado']]},
         'cel': {'mat': ['Celular', 'Este material (simulador del Bloque C)', 'Tu documento de reporte'],
                 'steps': [
                     ['Resuelve el simulador «Consulta y configura el equipo» y captura los retos en verde.', 'sim_cel'],
                     ['En el simulador escribe SET y explica tres variables que veas.', 'cmd_set'],
                     ['Comprueba en el simulador que SET CIBER=Nova crea la variable y ECHO %CIBER% la muestra.', 'cmd_settemp'],
                     ['En tu celular abre Ajustes › Acerca del teléfono y relaciona sus datos con HOSTNAME y VER.', 'cel_info'],
                     'Escribe con tus palabras para qué sirve PATH.',
                     ['Agrega los comandos nuevos a tu listado.', 'listado']]}},
     'entrega': ['Capturas explicadas y respuestas a las preguntas.', 'Listado de comandos actualizado.'],
     'rub': [['Información del sistema consultada', 20], ['Variables mostradas y listadas', 20], ['Diferencia entre SET y SETX comprobada', 25], ['PATH explicado', 15], ['Listado de comandos', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Automatiza con PowerShell',
     'prog': 'Bloque D · PowerShell',
     'min': 100, 'lug': 'Laboratorio, lunes 9-nov (2 h) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Terminal o Windows PowerShell', 'Tu documento de reporte'],
                'steps': [
                    ['Abre PowerShell y escribe Get-Location. Toma captura.', 'ps_abrir'],
                    ['Escribe Get-Help Get-ChildItem y luego Get-ChildItem Documentos.', 'ps_gci'],
                    ['Crea la carpeta Documentos\\Nova\\Reportes con New-Item.', 'ps_new'],
                    ['Crea reporte.txt con Set-Content y léelo con Get-Content.', 'ps_content'],
                    ['Muestra los 5 procesos que más CPU usan con la tubería.', 'ps_proc'],
                    ['Muestra solo los servicios activos.', 'ps_srv'],
                    ['Haz una tabla comparando 5 tareas en CMD y en PowerShell.', 'ps_tabla'],
                    ['Agrega los cmdlets a tu listado de comandos.', 'listado']]},
         'cel': {'mat': ['Celular', 'Este material (simulador del Bloque D)', 'Tu documento de reporte'],
                 'steps': [
                     ['Resuelve el simulador «PowerShell en el Nova» y captura los retos en verde.', 'sim_cel'],
                     ['En el simulador escribe Get-Help Get-Process y Get-Command. Explica qué muestran.', 'ps_gci'],
                     ['Prueba la tubería con Get-Process | Sort-Object CPU -Descending | Select-Object -First 5.', 'ps_proc'],
                     ['Haz una tabla comparando 5 tareas en CMD y en PowerShell.', 'ps_tabla'],
                     ['Agrega los cmdlets a tu listado de comandos.', 'listado']]}},
     'entrega': ['Capturas explicadas y tabla comparativa.', 'Listado de comandos completo.'],
     'rub': [['Navegación con cmdlets', 15], ['Carpeta y archivo creados con New-Item y Set-Content', 25], ['Tubería con procesos y servicios', 25], ['Tabla comparativa CMD y PowerShell', 20], ['Listado de comandos', 15]]},
]

EVALUATION = {
    'course': 'MSII-05 · Manejo de sistemas operativos · Unidad 2',
    'ra': 'R.A. 2.1', 'title': 'Sesión práctica y listado de comandos',
    'data': [
        ('Resultado de aprendizaje', 'Opera el sistema operativo monousuario, considerando los aspectos funcionales del sistema informático.'),
        ('Actividad de evaluación', '2.1.1 Realiza una sesión práctica en un sistema sobre la base de operaciones de usuario, eligiendo los comandos adecuados a utilizar en función de una tarea a resolver, considerando la gestión de directorios con MS-DOS y Windows.'),
        ('Evidencias', 'Reporte de la sesión práctica · Listado de comandos ejecutados con la operación realizada al sistema'),
        ('Ponderación', '25% (según el programa)'),
        ('Entrega', 'Viernes 13 de noviembre'),
    ],
    'situation': 'El Cibercafé Nova abre una sucursal y te pide dejar lista la primera computadora. Resuelve la tarea con comandos: organiza las carpetas de trabajo, respalda archivos en la USB, documenta la configuración del equipo y repite parte del trabajo con PowerShell. Registra todo en tu <b>reporte</b> y tu <b>listado de comandos</b>.',
    'hint': 'Antes de cada comando piensa: ¿dónde estoy?, ¿qué quiero lograr?, ¿ruta absoluta o relativa? Si no tienes laboratorio, usa los simuladores del material.',
    'steps': [
        ('Preparación', [
            'Portada con tu nombre, grupo y fecha; objetivo de la sesión en 2 líneas.',
            'Abre el Símbolo del sistema y captura la información del equipo (VER, HOSTNAME, SYSTEMINFO).']),
        ('Gestión de directorios y archivos (CMD)', [
            'Crea en Documentos la estructura <b>Sucursal › Clientes, Precios, Respaldos</b> y muéstrala con TREE.',
            'Crea 2 archivos con ECHO, cópialos y renómbralos usando al menos una <b>ruta absoluta</b> y una <b>relativa</b>.',
            'Mueve un archivo a Respaldos y borra uno de prueba.',
            'Respalda la carpeta Precios en la USB (unidad D: o E:) y comprueba con DIR.']),
        ('Configuración', [
            'Muestra 3 variables de entorno y crea la variable SUCURSAL con SETX; compruébala en una ventana nueva.']),
        ('PowerShell', [
            'Repite con cmdlets: lista la carpeta Sucursal, crea Reportes con New-Item y un archivo con Set-Content.',
            'Muestra los 5 procesos con más CPU y los servicios activos.']),
        ('Reporte y listado', [
            'Reporte: capturas en orden, cada una con qué hiciste y qué resultado obtuviste.',
            'Listado de comandos en tabla: comando, para qué sirve y el ejemplo exacto que ejecutaste.',
            'Conclusión: ¿cuándo conviene usar comandos y cuándo ventanas?']),
    ],
    'rubric': [
        ('Información del equipo', 10), ('Estructura de carpetas y TREE', 15),
        ('Archivos con rutas absolutas y relativas', 20), ('Respaldo en la USB', 10),
        ('Variables de entorno', 10), ('PowerShell: cmdlets y tubería', 15),
        ('Reporte con capturas explicadas', 10), ('Listado de comandos completo', 10),
    ],
    'deliver': ['Un solo archivo PDF o Word con el reporte y el listado.', 'Nombre del archivo: Apellido_Nombre_Sesion_MSII21.', 'Súbelo en la actividad R.A. 2.1 de la plataforma.'],
}
