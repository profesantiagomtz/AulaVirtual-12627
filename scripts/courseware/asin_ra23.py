"""ASIN-20 · R.A. 2.3 · Controla parámetros de seguridad mediante verificación y actualización.

Cierra la Unidad 2 con la Papelería Don Beto: se audita toda la red (equipos, impresora, router y un intruso),
se compara contra el plan de seguridad, se miden resultados, se definen nuevos requerimientos y se aplican
acciones correctivas, actualizaciones y planes de contingencia. Incluye una consola de auditoría (aud_sim.js).
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'ASIN-RA-2.3'
CODE_PREFIX = 'ASIN23'
FILE = 'asin-ra23-material.html'
TITLE_TAG = 'ASIN-20 · R.A. 2.3 · Controla parámetros de seguridad'
BRAND = 'ASIN-20 · Seguridad informática'
BRAND_SUB = 'R.A. 2.3 · Verificación y actualización'
HERO_KICK = 'ASIN-20 · R.A. 2.3'
HERO_TITLE = 'Audita, mide y mejora la seguridad'
HERO_TEXT = 'Revisa toda la red de la papelería contra su plan de seguridad, mide los resultados, define nuevos requerimientos y prepara planes de contingencia.'
EV_SHORT = 'arma tu portafolio de auditoría con el balance de resultados y los nuevos requerimientos.'
EV_CARD = 'Portafolio de auditoría'
RA = 'R.A. 2.3'
GROUP = '310'

TABS = {'d': ['Diagnostica', 'Consola de auditoría'], 'c': ['Construye', 'Audita una red real']}

EXTRA_JS = (Path(__file__).parent / 'aud_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".ausim"))auInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".ausim"))return auCheck(d);\n'),
]

c = Course()

LVL = ['Nivel 1 · Encargado (Don Beto): resuelve lo básico', 'Nivel 2 · Técnico de soporte (tú): configura y restaura', 'Nivel 3 · Externo: proveedor, banco o autoridad']
SCEN = [
    {'id': 'net', 't': 'Se cayó el internet a las 9:00', 'd': 'El router no da señal y la terminal de cobro con tarjeta no funciona. Hay fila de clientes.',
     'a': ['Revisar las luces del router y reiniciarlo', 'Cambiar todas las contraseñas', 'Formatear la caja'],
     's': ['Compartir los datos del celular de la papelería para la terminal y anotar ventas en la libreta', 'Cerrar la papelería todo el día', 'Cobrar solo en efectivo sin anotar nada'],
     'e': [x + (' (si reiniciar no funcionó)' if i == 2 else '') for i, x in enumerate(LVL)], 'ok': [0, 0, 2],
     'win': 'Plan correcto: lo básico primero, se sigue vendiendo con una alternativa y, si no se resuelve, se reporta al proveedor de internet.'},
    {'id': 'ran', 't': 'Mensaje de rescate en la caja', 'd': 'CAJA-01 muestra «Tus archivos están cifrados, paga 500 dólares». Los archivos de ventas no abren.',
     'a': ['Desconectar la caja de la red (cable y Wi-Fi) de inmediato', 'Pagar el rescate', 'Reiniciar y seguir cobrando'],
     's': ['Restaurar desde el último respaldo verificado y cobrar con la terminal mientras tanto', 'Borrar el mensaje y seguir', 'Esperar a que se arregle solo'],
     'e': LVL, 'ok': [0, 0, 1],
     'win': 'Plan correcto: aislar evita que se infecte la PC de oficina; el técnico restaura el respaldo y revisa cómo entró.'},
    {'id': 'fra', 't': 'Una empleada dio su contraseña por teléfono', 'd': 'Alguien que dijo ser «del banco» le pidió la contraseña de la banca en línea de la papelería y ella se la dio.',
     'a': ['Cambiar de inmediato la contraseña y cerrar las sesiones abiertas', 'No decir nada para no regañarla', 'Apagar la computadora'],
     's': ['Activar la verificación en dos pasos y revisar los movimientos de la cuenta', 'Desinstalar el navegador', 'Comprar otra computadora'],
     'e': LVL, 'ok': [0, 0, 2],
     'win': 'Plan correcto: se corta el acceso y se escala al banco y a la Policía Cibernética (088); después se capacita al personal.'},
]


def sim(ic, t, inf, cid, intro, tabs, tasks, hint, setup='', scen=False):
    """tasks: [texto, expresión JS con la api a (a.used, a.scan, a.info(id), a.cmp(id), a.comp(id), a.total(), a.dev(id),
    a.metOk(k), a.reqs, a.reqOk(), a.cont(k), a.act, a.rep)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    st = f',setup:[function(s){{{setup}}}]' if setup else ''
    sc = f',scen:{j(SCEN)}' if scen else ''
    cfg = f'{{id:{j(cid)},intro:{j(intro)},hint:{j(hint)},tabs:{j(tabs)},tasks:{ts}{st}{sc}}}'
    return c.raw(f'pAu({j(ic)},{j(t)},{j(inf)},{cfg})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏪', 'Auditoría en la papelería', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Controlar los parámetros de seguridad es <b>revisar con evidencia</b> si los equipos y la red cumplen el plan de seguridad, <b>medir</b> qué tan bien vamos, decidir qué <b>nuevos requerimientos</b> hacen falta y <b>corregir</b> lo que falla.'),
    ex('Caso: Papelería Don Beto', 'Ya instalaste (R.A. 2.1) y diste seguimiento (R.A. 2.2) a la seguridad de la caja. Ahora Don Beto agregó una PC de oficina, la impresora está en red y le parece que «alguien más usa el Wi-Fi». Vas a auditar <b>toda la red</b>.'),
    r3([('🔎', 'A · Revisar la configuración', 'Herramientas de auditoría para recopilar y comparar.'), ('📏', 'B · Analizar reportes', 'Métricas, nuevos requerimientos y medidas.'), ('🛠️', 'C · Acciones correctivas', 'Planes de contingencia, escalamiento y actualizaciones.')])),
    'Auditar = revisar con evidencia, medir y mejorar.')
c.L('🗺️', 'Tu ruta y tu portafolio', 'Lo que vas a entregar', body(
    bk('Portafolio de evidencias (15%)', 'Dos informes: 1) el <b>balance de resultados</b> de la configuración de las herramientas de seguridad en equipos y red (qué cumple, qué no y en qué porcentaje) y 2) los <b>nuevos requerimientos y riesgos</b> identificados, con sus medidas.'),
    bk('Cómo se arma', 'Practica con la <b>consola de auditoría</b> (cuatro simuladores) y luego audita una red real: la de tu casa o la del laboratorio, con permiso.'),
    warn('Ética', 'Solo audita equipos y redes <b>propios o con autorización por escrito</b>. Escanear redes ajenas puede ser un delito.')),
    'Cada simulador te da datos para el portafolio.')
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Revisar la configuración ─────────────────────────
a0 = c.mark()
c.L('📡', 'Herramientas para recopilar información', 'Bloque A · Saber qué hay y cómo está', body(
    sp('En palabras sencillas', 'No puedes proteger lo que no sabes que existe. Primero se hace un <b>inventario</b> de equipos y de su estado.'),
    bk('Escáner de red', 'Encuentra los dispositivos conectados con su IP, MAC y puertos abiertos: <b>Advanced IP Scanner</b>, <b>Angry IP Scanner</b>, <b>Nmap</b> (en computadora) o <b>Fing</b> (en el celular).'),
    bk('Información del equipo', '<code>msinfo32</code> y <code>systeminfo</code> en Windows; en PowerShell <code>Get-ComputerInfo</code>. Dicen sistema operativo, versión, actualizaciones instaladas y hardware.'),
    bk('Estado de la seguridad', 'Seguridad de Windows (antivirus, firewall), <code>Get-MpComputerStatus</code> (estado de Defender), Windows Update y el panel del router (dispositivos conectados, firmware, Wi-Fi).'),
    bk('Registros (logs)', 'El <b>Visor de eventos</b> guarda inicios de sesión, errores y cambios: es la memoria de lo que pasó.'),
    ex('Ejemplo', 'El escáner encuentra 5 equipos, pero el inventario de la papelería solo tiene 4: hay un dispositivo desconocido conectado al Wi-Fi.')),
    'Escanear → detallar cada equipo → revisar registros.')
c.L('⚖️', 'Herramientas para comparar configuraciones', 'Bloque A · Línea base contra realidad', body(
    sp('En palabras sencillas', 'La <b>línea base</b> es cómo <i>debería</i> estar cada equipo según el plan de seguridad. Comparar es ver la diferencia con cómo <i>está</i> hoy.'),
    bk('Lista de verificación (checklist)', 'Cada política del plan con una casilla «Cumple / No cumple / No aplica». Es la herramienta más sencilla y la más usada.'),
    bk('Herramientas de comparación', '<b>Microsoft Security Compliance Toolkit</b> (Policy Analyzer) compara las directivas de un equipo con una línea base recomendada. <b>WinMerge</b> compara dos archivos de configuración exportados (por ejemplo, la del router de hoy contra la del mes pasado).'),
    bk('Porcentaje de cumplimiento', 'Políticas que cumplen ÷ políticas que aplican × 100. Ejemplo: 4 de 6 → 67 %.'),
    warn('No aplica no es «no cumple»', 'La impresora no lleva antivirus: esa política <b>no aplica</b> y no cuenta en el porcentaje.')),
    'Línea base + comparación = lista de lo que hay que corregir.')
c.A('🧰', '¿Qué herramienta usas?', 'Elige la herramienta para cada necesidad de la auditoría.', [
    ['Saber qué dispositivos están conectados al Wi-Fi', 'Escáner de red', 'Lista IP, MAC y puertos de cada dispositivo.'],
    ['Ver quién intentó entrar como administrador anoche', 'Visor de eventos', 'Los inicios de sesión quedan registrados.'],
    ['Comparar la configuración del router de hoy con la del mes pasado', 'Comparador de archivos', 'WinMerge marca las diferencias entre dos exportaciones.'],
    ['Conocer la versión de Windows y sus actualizaciones', 'Información del sistema', 'msinfo32 o systeminfo lo muestran.'],
    ['Revisar si cada equipo cumple las políticas del plan', 'Lista de verificación', 'Cumple / No cumple por política.'],
], 'Recopilar primero, comparar después.', ['Escáner de red', 'Visor de eventos', 'Comparador de archivos', 'Información del sistema', 'Lista de verificación'])
sim('📡', 'Escanea y compara la red', 'Consola de auditoría: recopila información y compárala con la línea base.', 'x1',
    'Audita la red 192.168.1.0/24 de la papelería: encuentra qué hay conectado y qué tan bien cumple el plan de seguridad.', ['scan', 'cmp'], [
    ['<b>Escanea</b> la red.', 'a.scan'],
    ['Abre el <b>detalle</b> del dispositivo desconocido.', 'a.info("¿DESCONOCIDO?")'],
    ['Revisa el detalle de la <b>impresora</b> y del <b>router</b>.', 'a.info("IMPRESORA")&&a.info("ROUTER")'],
    ['<b>Compara</b> los cinco dispositivos con la línea base del plan.', '["CAJA-01","PC-OFICINA","IMPRESORA","ROUTER","¿DESCONOCIDO?"].every(function(d){return a.cmp(d)})']],
    'El detalle está en el botón 🔎 de cada fila del escaneo.')
c.T('🧮', 'Calcula el cumplimiento', 'Escribe solo el número (porcentaje redondeado, sin el signo %).', [
    ['Un equipo cumple 6 de 8 políticas que aplican.', '75', '6 ÷ 8 × 100 = 75.', 'Cumple ÷ aplican × 100.', 'n'],
    ['La impresora cumple 2 de 4 políticas que le aplican.', '50', '2 ÷ 4 × 100 = 50.', 'Divide y multiplica por 100.', 'n'],
    ['En toda la red se revisaron 25 políticas y cumplen 15.', '60', '15 ÷ 25 × 100 = 60.', 'Mismo cálculo.', 'n'],
    ['El router tiene 5 políticas: 3 cumplen y 1 no aplica. ¿Cuántas cuentan para el porcentaje?', '4', 'Las que no aplican no cuentan: 5 − 1 = 4.', 'Quita las que no aplican.', 'n'],
], 'No aplica no cuenta en el total.', 'n')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Analizar reportes ─────────────────────────
b0 = c.mark()
c.L('📏', 'Reportes y métricas', 'Bloque B · Comparar lo esperado con lo obtenido', body(
    sp('En palabras sencillas', 'Una <b>métrica</b> es un número que dice qué tan bien va la seguridad. Cada métrica tiene una <b>meta</b> (lo que pide el plan) y un valor <b>obtenido</b> (lo que mediste).'),
    bk('Reportes de operación', 'Las aplicaciones generan reportes: el antivirus (amenazas y análisis), Windows Update (historial), el respaldo (copias correctas y fallidas) y el router (dispositivos conectados).'),
    bk('Métricas típicas', '% de equipos con antivirus al día · actualizaciones críticas pendientes · dispositivos con contraseña de fábrica · dispositivos no autorizados · respaldos correctos en el mes.'),
    bk('Comparar', 'Si el obtenido alcanza la meta → <b>cumple</b>. Si no → es un <b>hallazgo</b>. Un semáforo ayuda: verde cumple, amarillo cerca, rojo lejos.'),
    ex('Ejemplo', 'Meta: 30 respaldos correctos en el mes. Obtenido: 22. No cumple: 8 días sin copia de las ventas.')),
    'Meta vs. obtenido = cumple o hallazgo.')
c.L('📝', 'Nuevos requerimientos de seguridad', 'Bloque B · Del hallazgo a la medida', body(
    bk('Identificar', 'Cada hallazgo es un riesgo: ¿qué podría pasar y qué tan grave sería?'),
    bk('Definir el requerimiento', 'Lo que la papelería necesita ahora: «Ningún dispositivo con contraseña de fábrica», «Solo equipos autorizados en el Wi-Fi».'),
    bk('Establecer la medida', 'La acción concreta que lo resuelve: cambiar contraseñas, filtrar por MAC, reparar el respaldo.'),
    bk('Prioridad', '<b>Alta</b>: puede causar pérdida de dinero o datos pronto (intrusos, sin antivirus, respaldos fallidos). <b>Media</b>: aumenta el riesgo pero no es inmediato (WPS, Telnet en la red interna). <b>Baja</b>: mejora deseable.'),
    bk('Optimizar lo existente', 'A veces no hace falta comprar nada: programar el antivirus, activar el firewall o automatizar la copia en la nube ya mejora mucho.')),
    'Hallazgo → riesgo → requerimiento → medida → prioridad.')
sim('📏', 'Mide y define requerimientos', 'Consola de auditoría: métricas y nuevos requerimientos.', 'x2',
    'Ya escaneaste la red. Calcula las métricas del informe y convierte los hallazgos en requerimientos con su medida y prioridad.', ['scan', 'cmp', 'met', 'req'], [
    ['Calcula correctamente las métricas de <b>antivirus</b> y <b>actualizaciones críticas</b>.', 'a.metOk("avpc")&&a.metOk("crit")'],
    ['Calcula correctamente las de <b>contraseñas de fábrica</b>, <b>no autorizados</b> y <b>respaldos</b>.', 'a.metOk("pw")&&a.metOk("unk")&&a.metOk("bk")'],
    ['Registra el requerimiento del <b>dispositivo desconocido</b> con su medida y prioridad correctas.', 'a.reqs.some(function(r){return r.f=="f_unk"})&&a.reqOk()>=1'],
    ['Registra al menos <b>5 requerimientos</b> correctos (medida y prioridad).', 'a.reqOk()>=5']],
    'Para las métricas usa el detalle de cada equipo: suma las críticas pendientes de todos.', setup='s.scan=true;')
c.A('🚦', '¿Qué prioridad tiene?', 'Elige la prioridad de cada requerimiento.', [
    ['La caja lleva 8 días sin respaldo de las ventas', 'Alta', 'Si falla el disco se pierde el dinero registrado.'],
    ['Un dispositivo desconocido usa el Wi-Fi de la papelería', 'Alta', 'Puede espiar o atacar los equipos.'],
    ['El router tiene WPS encendido', 'Media', 'Facilita entrar al Wi-Fi, pero requiere estar cerca.'],
    ['Poner fondo de pantalla con el logo de la papelería en todas las PCs', 'Baja', 'Es deseable, no reduce riesgos.'],
    ['La PC de oficina no tiene antivirus desde hace 41 días', 'Alta', 'Está expuesta a malware ahora mismo.'],
], 'Alta = daño grave y pronto.', ['Alta', 'Media', 'Baja'])
b_end = c.mark() - 1

# ───────────────────────── Bloque C · Acciones correctivas ─────────────────────────
c0 = c.mark()
c.L('🚨', 'Planes de contingencia', 'Bloque C · Definición, características, alternativas y escalamiento', body(
    sp('En palabras sencillas', 'Un <b>plan de contingencia</b> dice qué hacer cuando algo falla, para que el negocio <b>siga funcionando</b> y se recupere rápido.'),
    bk('Características', 'Está <b>escrito</b> antes del problema · dice <b>quién</b> hace <b>qué</b> · tiene <b>alternativas</b> para seguir trabajando · indica a quién <b>escalar</b> · se <b>prueba</b> y se actualiza.'),
    px('Partes del plan', ['<b>Riesgo</b>: qué puede pasar (se cae internet, ransomware, fraude).', '<b>Primera acción</b>: lo que se hace de inmediato para contener el daño.', '<b>Alternativa de solución</b>: cómo seguir operando mientras se arregla.', '<b>Escalamiento</b>: a quién se avisa si no se resuelve.', '<b>Recuperación y lecciones</b>: volver a la normalidad y evitar que se repita.']),
    bk('Escalamiento de problemas', '<b>Nivel 1</b> · usuario o encargado: lo básico (reiniciar, revisar cables). <b>Nivel 2</b> · técnico de soporte: configuraciones, restaurar respaldos, limpiar malware. <b>Nivel 3</b> · externo: proveedor de internet, fabricante, banco o autoridades (Policía Cibernética 088).'),
    warn('Nunca', 'Pagar un rescate no garantiza recuperar los archivos. La mejor defensa contra el ransomware es un <b>respaldo verificado</b>.')),
    'Contener → seguir operando → escalar → recuperar → aprender.')
c.O('🔢', 'Ordena la respuesta al ransomware', 'Ordena lo que se hace cuando la caja muestra un mensaje de rescate.', [
    ['Desconectar la caja de la red', 'Primero se contiene: que no se propague.'],
    ['Avisar al técnico de soporte (nivel 2)', 'Se escala a quien puede resolverlo.'],
    ['Cobrar con la terminal y anotar en libreta mientras tanto', 'El negocio sigue operando.'],
    ['Restaurar desde el último respaldo verificado', 'Se recupera la información.'],
    ['Cambiar contraseñas, actualizar y documentar qué pasó', 'Se cierra la puerta por donde entró.'],
], 'Contener, escalar, operar, recuperar, aprender.')
c.L('⬆️', 'Actualización de software y de equipo', 'Bloque C · Acciones correctivas', body(
    bk('Software', 'Instala las actualizaciones <b>críticas</b> primero. Actualiza firmas del antivirus a diario. Programa las actualizaciones fuera del horario de venta.'),
    bk('Equipo (firmware)', 'Routers, impresoras y cámaras también tienen sistema propio (<b>firmware</b>). Se actualiza desde su panel web. <b>Antes</b>, respalda la configuración: si la actualización falla, la restauras.'),
    bk('Corregir configuraciones', 'Cambiar contraseñas de fábrica, cerrar puertos innecesarios (RDP 3389, Telnet 23), apagar WPS, bloquear dispositivos desconocidos.'),
    bk('Verificar', 'Después de corregir, <b>vuelve a escanear y comparar</b>: el informe de balance muestra el cumplimiento antes y después.'),
    ex('Bitácora', 'Cada acción se registra: fecha, equipo, qué se cambió y quién. Es la evidencia del control de cambios.')),
    'Respaldar → corregir/actualizar → verificar → registrar.')
sim('🛠️', 'Corrige y actualiza', 'Consola de auditoría: acciones correctivas, firmware e informe de balance.', 'x3',
    'Aplica las medidas de tus requerimientos hasta que toda la red cumpla el plan, y genera el informe de balance.', ['fix', 'cmp', 'rep'], [
    ['Deja la <b>PC-OFICINA</b> al 100 % de cumplimiento.', 'a.comp("PC-OFICINA")==100'],
    ['Deja la <b>impresora</b> al 100 % (contraseña robusta y sin Telnet).', 'a.comp("IMPRESORA")==100'],
    ['Actualiza el <b>firmware del router</b> después de <b>respaldar su configuración</b>.', 'a.used("fw_ok")&&!a.used("fw_nobk")'],
    ['<b>Bloquea</b> el dispositivo desconocido.', '!a.dev("¿DESCONOCIDO?")'],
    ['Logra el <b>100 %</b> de cumplimiento en toda la red.', 'a.total()==100'],
    ['Genera el <b>informe de balance</b> con la red al 100 %.', 'a.rep.some(function(r){return r.tot==100})']],
    'Las contraseñas deben tener 10 caracteres o más con mayúsculas, minúsculas, números y un símbolo.',
    setup='s.scan=true;["CAJA-01","PC-OFICINA","IMPRESORA","ROUTER","¿DESCONOCIDO?"].forEach(function(d){s.cmp[d]=1});')
sim('🚨', 'Activa los planes de contingencia', 'Consola de auditoría: primera acción, alternativa y escalamiento.', 'x4',
    'Tres problemas reales. Para cada uno elige la primera acción, la alternativa para seguir trabajando y a qué nivel escalar.', ['cont'], [
    ['Resuelve «Se cayó el internet».', 'a.cont("net")'],
    ['Resuelve «Mensaje de rescate en la caja».', 'a.cont("ran")'],
    ['Resuelve «Una empleada dio su contraseña por teléfono».', 'a.cont("fra")']],
    'Primero contener, luego seguir operando y escalar a quien puede resolverlo.', scen=True)
c.W('✍️', 'Tu informe de nuevos requerimientos', 'Redacta el segundo informe del portafolio.',
    'Redacta un informe breve para Don Beto con <b>tres hallazgos</b> de la auditoría. Para cada uno escribe el <b>riesgo</b>, el <b>nuevo requerimiento</b>, la <b>medida</b> y su <b>prioridad</b>. Cierra con el <b>porcentaje de cumplimiento</b> antes y después.',
    [['Tiene al menos 60 palabras', 'palabras:60'],
     ['Menciona riesgos', '\\b(riesgo\\w*)\\b'],
     ['Menciona requerimientos o medidas', '\\b(requerimiento\\w*|medida\\w*)\\b'],
     ['Indica prioridades', '\\b(alta|media|baja|prioridad\\w*)\\b'],
     ['Da un porcentaje de cumplimiento', '\\d+\\s*(%|por ciento)']],
    'Hallazgo · riesgo · requerimiento · medida · prioridad.', 'Ejemplo: Hallazgo 1: un dispositivo desconocido…')
c_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Auditoría', 'Revisión con evidencia de si algo cumple lo establecido.'),
    bk('Línea base', 'Configuración esperada según el plan de seguridad.'),
    bk('Escáner de red', 'Herramienta que lista los dispositivos conectados y sus puertos.'),
    bk('Métrica', 'Número que mide un aspecto de la seguridad.'),
    bk('Hallazgo', 'Diferencia encontrada entre lo esperado y lo real.'),
    bk('Requerimiento', 'Lo que se necesita para cumplir o mejorar la seguridad.'),
    bk('Plan de contingencia', 'Qué hacer cuando algo falla para seguir operando.'),
    bk('Escalamiento', 'Pasar un problema al siguiente nivel de atención.'),
    bk('Firmware', 'Software interno de routers, impresoras y otros equipos.'),
    bk('Puerto', 'Número por donde un servicio recibe conexiones (3389 escritorio remoto, 23 Telnet).')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Grupo 310. El R.A. 2.3 dura 12 h, vale 15% y la A.E. es el viernes 8-ene. Si el laboratorio lo permite, deja un dispositivo «intruso» (un celular) conectado a la red de práctica para que lo descubran.', 'sp'),
    bk('10 y 11-dic · Bloque A', 'Herramientas de recopilación y de comparación; simulador 1. En el laboratorio, escaneo con Advanced IP Scanner o Fing y <b>Práctica 1</b>.'),
    bk('14 y 17-dic · Bloque B', 'Reportes, métricas y nuevos requerimientos; simulador 2.'),
    bk('18-dic y 7-ene · Bloque C', 'Planes de contingencia, escalamiento y actualizaciones; simuladores 3 y 4 y <b>Práctica 2</b>.'),
    bk('Viernes 8-ene · Evaluación', 'Entrega del portafolio: informe de balance de resultados e informe de nuevos requerimientos y riesgos.'),
    bk('Ética', 'Recalca que solo se escanean redes propias o con autorización. En casa, pide permiso a quien administra el módem.', 'sp')),
    'Las fechas vienen de tu cronograma; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🏪', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '🔎', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '📏', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🛠️', 'a': c0, 'b': c_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🏪",t:"Empieza aquí",d:"Qué es controlar los parámetros de seguridad y qué vas a entregar.",time:"20 min",obj:["Explicar qué es una auditoría de seguridad","Conocer el portafolio del R.A."],sum:["Auditar = revisar con evidencia.","Medir, definir requerimientos y corregir.","Portafolio: balance de resultados y nuevos requerimientos (15%)."],q:"¿Cuántos dispositivos crees que hay conectados al Wi-Fi de tu casa?"},
a:{k:"Bloque A",l:"A",ic:"🔎",t:"Revisar la configuración",d:"Herramientas de auditoría para recopilar información y para comparar configuraciones.",time:"4 h",obj:["Recopilar información de equipos y red","Comparar contra la línea base","Calcular el porcentaje de cumplimiento"],sum:["Escáner de red, msinfo32, Visor de eventos.","Línea base = cómo debería estar.","Cumple ÷ aplican × 100."],q:"¿Qué dispositivo de tu casa nunca has revisado?"},
b:{k:"Bloque B",l:"B",ic:"📏",t:"Analizar reportes",d:"Reportes de operación, métricas, nuevos requerimientos, medidas y alternativas de optimización.",time:"4 h",obj:["Comparar métricas con resultados","Identificar y definir nuevos requerimientos","Asignar medidas y prioridades"],sum:["Meta vs. obtenido.","Hallazgo → riesgo → requerimiento → medida.","Prioridad alta, media o baja."],q:"¿Qué métrica pondrías para la seguridad de tu celular?",rev:[["La línea base es…",["Cómo debería estar el equipo","El primer equipo de la red","Un tipo de virus"],0,"Es la configuración esperada."],["Un escáner de red muestra…",["IP, MAC y puertos de los dispositivos","Las contraseñas de todos","Las fotos de los equipos"],0,"Hace el inventario de la red."]]},
c:{k:"Bloque C",l:"C",ic:"🛠️",t:"Acciones correctivas",d:"Planes de contingencia (definición, características, alternativas y escalamiento) y actualización de software y equipo.",time:"4 h",obj:["Diseñar respuestas de contingencia","Escalar problemas al nivel correcto","Aplicar correcciones y actualizaciones de forma segura"],sum:["Contener, operar, escalar, recuperar.","Nivel 1, 2 y 3.","Respaldar antes de actualizar firmware.","Verificar y registrar cada cambio."],q:"¿Cuál sería tu plan si mañana no hay internet en la escuela?",rev:[["Si la meta es 0 dispositivos desconocidos y hay 1…",["No cumple: es un hallazgo","Cumple","No aplica"],0,"No alcanza la meta."],["Una medida es…",["La acción concreta que resuelve un hallazgo","Un tipo de cable","Una métrica"],0,"Resuelve el requerimiento."]]}
'''

ILL = r'''
ILL["Auditoría en la papelería"]=function(){return flow([["📡","Recopilar"],["⚖️","Comparar"],["📏","Medir"],["📝","Requerir"],["🛠️","Corregir"]],"Ciclo de la auditoría")};
ILL["Herramientas para comparar configuraciones"]=function(){return SV(340,120,R_(10,10,150,100,"s",8)+T_(85,34,"Línea base","t")+T_(85,58,"Firewall: activo","tm")+T_(85,78,"WPS: apagado","tm")+R_(180,10,150,100,"w",8)+T_(255,34,"Realidad","t")+T_(255,58,"Firewall: activo ✔","tm")+T_(255,78,"WPS: encendido ✖","tm"),"Lo esperado contra lo real")};
ILL["Planes de contingencia"]=function(){return flow([["🧯","Contener"],["🔁","Seguir|operando"],["📞","Escalar"],["💾","Recuperar"],["📚","Aprender"]],"Respuesta ante un incidente")};
ILL["Actualización de software y de equipo"]=function(){return flow([["💾","Respaldar"],["⬆️","Actualizar"],["🔎","Verificar"],["🗒️","Registrar"]],"Cambio seguro")};
'''

EXH = r'''
EXH.escaner=function(){return exw(mw('Advanced IP Scanner','<div class="mfld">192.168.1.1 - 192.168.1.254 · Explorar '+mk(1)+'</div><div class="mm" style="margin-top:6px"><span>192.168.1.10 · CAJA-01</span><span class="hl">192.168.1.57 · Desconocido '+mk(2)+'</span></div>'),['Escribe el rango de tu red y explora.','Marca lo que no esté en tu inventario.'])};
EXH.msinfo=function(){return exw(mw('PowerShell','<div class="mfld">Get-ComputerInfo | Select OsName, OsVersion '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Get-MpComputerStatus | Select AntivirusEnabled, AntivirusSignatureAge '+mk(2)+'</div>'),['Sistema y versión.','Antivirus activo y antigüedad de firmas (días).'])};
EXH.router=function(){return exw(mw('Panel del router · 192.168.1.254','<div class="mm"><span>Dispositivos conectados '+mk(1)+'</span><span>Firmware: 2022.03 · Buscar actualización '+mk(2)+'</span></div>'),['Compara con tu inventario.','Respalda antes de actualizar.'])};
EXH.fing=function(){return exw(mp('Fing (celular)','<div class="mbox">Escanear red › lista de dispositivos '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Toca un dispositivo › puertos abiertos '+mk(2)+'</div>'),['Encuentra todos los equipos del Wi-Fi.','Revisa qué servicios tienen abiertos.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Auditoría de una red real',
     'prog': 'Bloques A y B · Recopilar, comparar y medir',
     'min': 120, 'lug': 'Laboratorio (10 y 11-dic) o tu casa con permiso de quien administra el módem',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Advanced IP Scanner o Angry IP Scanner', 'Acceso al panel del router (con permiso)'],
                'steps': [
                    'Antes de empezar, termina los simuladores 1 y 2.',
                    ['Escanea la red y haz el inventario: nombre, IP, MAC, tipo y si está autorizado.', 'escaner'],
                    ['En cada computadora obtén sistema, versión, antivirus y antigüedad de firmas.', 'msinfo'],
                    ['En el router revisa dispositivos conectados, firmware, tipo de cifrado del Wi-Fi y WPS.', 'router'],
                    'Llena la lista de verificación con las ocho políticas de la línea base (Cumple / No cumple / No aplica).',
                    'Calcula el porcentaje de cumplimiento de cada equipo y de toda la red.',
                    'Calcula las cinco métricas del simulador 2 y marca si cumplen la meta.']},
         'cel': {'mat': ['Celular con la app Fing', 'Acceso al panel del módem desde el navegador (con permiso)'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 1 y 2.',
                     ['Escanea tu red con Fing y haz el inventario de dispositivos.', 'fing'],
                     'Entra al panel del módem (192.168.1.254 o la dirección de su etiqueta) y revisa dispositivos, cifrado y WPS.',
                     'Llena la lista de verificación y calcula el porcentaje de cumplimiento.',
                     'Toma captura de cada paso (tapa contraseñas y direcciones MAC completas).']}},
     'entrega': ['Inventario, lista de verificación, porcentajes y métricas con capturas.'],
     'rub': [['Inventario completo', 20], ['Información de cada equipo', 20], ['Lista de verificación', 25], ['Porcentajes y métricas', 25], ['Ética y cuidado de datos', 10]]},
    {'id': 'pr2', 'n': 2, 't': 'Requerimientos y plan de contingencia',
     'prog': 'Bloques B y C · Requerimientos, contingencia y correcciones',
     'min': 90, 'lug': 'Clase (18-dic y 7-ene) o en casa',
     'modes': {
         'pc': {'mat': ['Tus resultados de la práctica 1', 'Word o Documentos de Google'],
                'steps': [
                    'Antes de empezar, termina los simuladores 3 y 4.',
                    'Escribe una tabla de hallazgos: riesgo, nuevo requerimiento, medida y prioridad.',
                    'Aplica al menos dos medidas que sí puedas hacer (por ejemplo, actualizar Windows o activar el firewall) y regístralas en una bitácora.',
                    'Vuelve a medir el cumplimiento y escribe el balance antes y después.',
                    'Escribe un plan de contingencia para dos riesgos (por ejemplo, sin internet y ransomware) con primera acción, alternativa y escalamiento por niveles.']},
         'cel': {'mat': ['Tus resultados de la práctica 1', 'Documentos de Google o Word móvil'],
                 'steps': [
                     'Antes de empezar, termina los simuladores 3 y 4.',
                     'Haz la tabla de hallazgos con riesgo, requerimiento, medida y prioridad.',
                     'Aplica dos medidas posibles en tu celular o módem y toma captura.',
                     'Escribe el balance antes y después y un plan de contingencia para dos riesgos.']}},
     'entrega': ['Informe de nuevos requerimientos y riesgos, bitácora y plan de contingencia.'],
     'rub': [['Tabla de hallazgos y requerimientos', 30], ['Medidas aplicadas y bitácora', 25], ['Balance antes y después', 20], ['Plan de contingencia con escalamiento', 25]]},
]

EVALUATION = {
    'course': 'ASIN-20 · Aplicación de la seguridad informática · Unidad 2',
    'ra': 'R.A. 2.3', 'title': 'Portafolio de auditoría de la configuración de seguridad',
    'data': [
        ('Resultado de aprendizaje', 'Controla parámetros de seguridad mediante verificación y actualización, acorde con nuevos requerimientos obtenidos.'),
        ('Actividad de evaluación', '2.3.1 Revisa las configuraciones de equipos y redes de comunicación evaluando el cumplimiento de las políticas del plan de seguridad, así como determinar nuevos requerimientos.'),
        ('Evidencia', 'Portafolio de evidencias: informe del balance de resultados e informe de nuevos requerimientos y/o riesgos'),
        ('Ponderación', '15% (según el programa)'),
        ('Entrega', 'Viernes 8 de enero: archivo en la plataforma'),
    ],
    'situation': 'Don Beto quiere saber si su papelería está tan segura como dice el plan y qué falta. Entrega tu portafolio de auditoría de la red que revisaste.',
    'hint': 'Usa la misma lista de ocho políticas en todos los equipos: así el porcentaje de cumplimiento es comparable.',
    'steps': [
        ('Informe 1 · Balance de resultados', [
            'Inventario de equipos y red con las herramientas usadas.',
            'Lista de verificación por equipo contra la línea base y porcentaje de cumplimiento.',
            'Métricas: meta, obtenido y si cumple.']),
        ('Informe 2 · Nuevos requerimientos y riesgos', [
            'Tabla de hallazgos con riesgo, requerimiento, medida y prioridad.',
            'Medidas aplicadas y balance antes y después.',
            'Plan de contingencia para dos riesgos con escalamiento por niveles.']),
    ],
    'rubric': [
        ('Recopilación de información', 15), ('Comparación con la línea base', 20), ('Métricas', 15),
        ('Requerimientos y medidas', 20), ('Acciones correctivas y balance', 15), ('Plan de contingencia', 15),
    ],
    'deliver': ['Un archivo Word (.docx) o PDF con los dos informes.', 'Nombre del archivo: Apellido_Nombre_ASIN23.', 'Súbelo en la actividad R.A. 2.3 de la plataforma.'],
}
