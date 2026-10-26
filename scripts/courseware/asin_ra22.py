"""ASIN-20 · R.A. 2.2 · Da seguimiento a la operación de las herramientas informáticas.

Caso de la unidad: la Papelería Don Beto (R.A. 1.2 y 2.1). Un mes después de instalar y configurar
las herramientas, los alumnos revisan su estado, corrigen y ajustan configuraciones y las respaldan.
Incluye un centro de seguridad simulado definido en sec_sim.js.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'ASIN-RA-2.2'
CODE_PREFIX = 'ASIN22'
FILE = 'asin-ra22-material.html'
TITLE_TAG = 'ASIN-20 · R.A. 2.2 · Da seguimiento a las herramientas de seguridad'
BRAND = 'ASIN-20 · Seguridad informática'
BRAND_SUB = 'R.A. 2.2 · Seguimiento de las herramientas'
HERO_KICK = 'ASIN-20 · R.A. 2.2'
HERO_TITLE = 'Da seguimiento a las herramientas de seguridad'
HERO_TEXT = 'Ya instalaste y configuraste la seguridad de la papelería. Ahora vigila que siga funcionando, corrige lo que falle y respalda la configuración.'
EV_SHORT = 'arma tu portafolio de seguimiento.'
EV_CARD = 'Portafolio de seguimiento'
RA = 'R.A. 2.2'
GROUP = '310'

TABS = {'d': ['Diagnostica', 'Revisa y comprueba tu avance'], 'c': ['Construye', 'Monitorea, ajusta y respalda']}

EXTRA_JS = (Path(__file__).parent / 'sec_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".scsim"))scInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".scsim"))return scCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cid, intro, tasks, hint, setup=''):
    """tasks: [texto, expresión JS con la api a (a.av, a.fw, a.wu, a.bk, a.acc(n), a.rule(f), a.seen, a.used,
    a.rep, a.exp(k), a.restored, a.issues(sec), a.chg(re))]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    st = f',setup:[function(s){{{setup}}}]' if setup else ''
    cfg = f'{{id:{j(cid)},intro:{j(intro)},hint:{j(hint)},tasks:{ts}{st}}}'
    return c.raw(f'pSc({j(ic)},{j(t)},{j(inf)},{cfg})')


# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏪', 'Un mes después en la papelería', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Dar seguimiento es <b>revisar con regularidad que las herramientas de seguridad sigan funcionando</b>, corregir lo que falle, ajustarlas cuando cambian las necesidades y guardar una copia de su configuración.'),
    ana('Piensa en un coche', 'Comprarlo y ponerle seguro no basta: hay que revisar el aceite, las llantas y los frenos cada cierto tiempo. Con el antivirus, el firewall y los respaldos pasa lo mismo.'),
    ex('Caso: Papelería Don Beto', 'Hace un mes dejaste la caja (CAJA-01) bien configurada. Hoy Don Beto dice que «algo raro pasa»: alguien desactivó cosas, hay actualizaciones en pausa y las copias de seguridad fallan. Te toca revisar, reportar y corregir.')),
    'Instalar es el inicio; el seguimiento mantiene la seguridad viva.')
c.L('🗺️', 'Tu ruta y tu portafolio', 'Dos bloques y tres evidencias', body(
    r3([('📊', 'A · Reportes de estado', 'Revisa cómo está cada herramienta y si funciona.'),
        ('🛠️', 'B · Modifica configuraciones', 'Corrige con el manual, atiende nuevos requerimientos y respalda.'),
        ('📁', 'Portafolio (20%)', 'Reporte de estado, reporte de cambios y respaldo digital.')]),
    bk('Al final entregas', 'Un <b>portafolio de evidencias</b> con: 1) el <b>reporte del estado</b> de las aplicaciones, 2) el <b>reporte de modificación</b> de configuraciones y 3) el <b>respaldo digital</b> de las configuraciones.'),
    bk('Cómo usar este material', 'Lee, resuelve las actividades y practica en el <b>centro de seguridad simulado</b>: ahí puedes equivocarte sin riesgo. Las prácticas tienen versión para computadora y para celular.', 'sp')),
    'Cada simulador y cada práctica te deja una pieza del portafolio.')
c.A('🔎', '¿Instalar, monitorear o modificar?', 'Decide qué tipo de tarea es cada acción.', [
    ['Revisar cada viernes si el antivirus tiene definiciones de hoy', 'Monitorear', 'Solo se observa y se anota el estado: es monitoreo.'],
    ['Agregar una regla al firewall para el nuevo programa de ventas', 'Modificar', 'Se cambia la configuración por un requerimiento nuevo.'],
    ['Poner un antivirus en una computadora nueva', 'Instalar', 'Agregar un programa que no estaba es instalar (R.A. 2.1).'],
    ['Ver en el Historial de archivos cuándo fue la última copia', 'Monitorear', 'Es revisar el estado de la herramienta de respaldo.'],
    ['Cambiar las copias de seguridad de «cada mes» a «cada día»', 'Modificar', 'Se ajusta una opción que ya existe.'],
    ['Generar el reporte semanal de seguridad para Don Beto', 'Monitorear', 'El reporte resume lo que se observó.'],
], 'Monitorear = observar y reportar. Modificar = cambiar un ajuste. Instalar = agregar algo nuevo.', ['Instalar', 'Monitorear', 'Modificar'])
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · Reportes del estado ─────────────────────────
a0 = c.mark()
c.L('🚦', 'Estado y funcionamiento', 'Bloque A · Dos preguntas para cada herramienta', body(
    sp('En palabras sencillas', 'Para cada herramienta te haces dos preguntas: <b>¿cuál es su estado?</b> (está encendida, actualizada, sin errores) y <b>¿funciona?</b> (de verdad hace su trabajo: detecta, bloquea, respalda).'),
    bk('Estado', 'Lo que dice la pantalla: «Activado», «Estás al día», «Última copia: hoy».'),
    bk('Funcionamiento', 'Lo que compruebas con una prueba: el antivirus detecta un archivo de prueba, el respaldo se puede abrir, el firewall bloquea lo que debe.'),
    ana('Piensa en una alarma de casa', 'Que el foquito esté verde (estado) no garantiza que suene si alguien entra (funcionamiento). Por eso se prueba de vez en cuando.'),
    bk('El semáforo', '🟢 <b>Correcto</b>: cumple lo que dice el manual. 🟡 <b>Atención</b>: funciona, pero algo se está atrasando. 🔴 <b>Crítico</b>: el equipo está desprotegido; se corrige hoy.')),
    'Estado = lo que se ve. Funcionamiento = lo que se comprueba.')
c.L('🖥️', '¿Dónde reviso el estado?', 'Bloque A · Las pantallas que ya conoces', body(
    bk('🛡️ Seguridad de Windows', 'Inicio › escribe <b>Seguridad de Windows</b>. El panel muestra una palomita verde ✔, un triángulo amarillo ⚠ o una X roja ✖ en cada área: antivirus, firewall, cuentas, navegador y dispositivo.'),
    bk('🔄 Windows Update', '<b>Configuración › Windows Update</b>: si estás al día, si hay pendientes o si está en pausa, y el historial.'),
    bk('💾 Copias de seguridad', '<b>Panel de control › Historial de archivos</b> (o OneDrive): la última copia y si la unidad está conectada.'),
    bk('📒 Visor de eventos', 'Errores y advertencias de cada programa, con fecha y hora (lo viste en el R.A. 2.1).'),
    bk('📱 En el celular', '<b>Play Protect</b> (antivirus), <b>Ajustes › Seguridad y privacidad</b> (estado general), <b>Ajustes › Google › Copia de seguridad</b> (respaldo).')),
    'Un buen técnico revisa siempre las mismas pantallas, en el mismo orden.')
c.A('🚦', 'Pon el semáforo', 'Clasifica el estado de cada herramienta según el manual de Don Beto.', [
    ['Antivirus: protección en tiempo real desactivada', 'Crítico', 'Sin tiempo real, un virus puede entrar sin que nadie lo detenga.'],
    ['Firewall activado en las tres redes', 'Correcto', 'Es justo lo que pide el manual.'],
    ['Última copia de seguridad correcta: hace 3 días (el manual pide diaria)', 'Atención', 'Funciona, pero se está atrasando: hay que revisarlo.'],
    ['Windows Update: en pausa desde hace un mes, con parches de seguridad pendientes', 'Crítico', 'Hay hoyos de seguridad conocidos sin tapar.'],
    ['Definiciones de virus actualizadas hoy', 'Correcto', 'El antivirus reconoce las amenazas recientes.'],
    ['Último examen rápido: hace 10 días (el manual pide cada semana)', 'Atención', 'Falta el examen, pero la protección sigue activa.'],
], 'Rojo = desprotegido hoy. Amarillo = funciona pero se atrasa. Verde = cumple el manual.', ['Correcto', 'Atención', 'Crítico'])
c.L('📏', 'Indicadores: medir con números', 'Bloque A · Cómo saber si funciona', body(
    sp('En palabras sencillas', 'Un indicador (métrica) es un <b>dato que se puede medir</b> y comparar con una meta. Así el reporte no dice «más o menos bien», sino «4 de 5 equipos cumplen».'),
    bk('Indicadores típicos', 'Días desde la última actualización de definiciones · días desde el último examen · actualizaciones de seguridad pendientes · días desde la última copia correcta · inicios de sesión fallidos · amenazas detectadas.'),
    bk('Meta (lo que pide el manual)', 'Definiciones: máximo 1 día. Examen rápido: cada 7 días. Pendientes de seguridad: 0. Copia correcta: cada día.'),
    ex('Porcentaje de cumplimiento', 'De 5 computadoras, 4 tienen el antivirus al día: 4 ÷ 5 × 100 = <b>80 %</b> de cumplimiento.'),
    warn('Ojo', 'Un número sin meta no dice nada. «3 días» es bueno para un examen semanal, pero malo para un respaldo diario.')),
    'Indicador + meta = puedes decir si cumple o no.')
c.T('🧮', 'Calcula los indicadores', 'Escribe solo el número.', [
    ['De 5 computadoras, 4 tienen el firewall activado. ¿Qué porcentaje cumple?', '80', '4 ÷ 5 × 100 = 80 %.', 'Divide los que cumplen entre el total y multiplica por 100.', 'n'],
    ['En noviembre (30 días) el respaldo terminó bien 24 días. ¿Qué porcentaje de copias correctas hubo?', '80', '24 ÷ 30 × 100 = 80 %.', 'Copias correctas entre días del mes, por 100.', 'n'],
    ['Las definiciones se actualizaron el 2 de diciembre y hoy es 9 de diciembre. ¿Cuántos días tienen?', '7', '9 − 2 = 7 días. La meta es 1: está en rojo.', 'Resta las fechas.', 'n'],
    ['Había 6 actualizaciones de seguridad pendientes y se instalaron 4. ¿Cuántas faltan?', '2', '6 − 4 = 2. La meta es 0: todavía no cumple.', 'Resta.', 'n'],
    ['En el Visor de eventos hay 15 inicios de sesión fallidos en 3 noches. ¿Cuántos por noche, en promedio?', '5', '15 ÷ 3 = 5 por noche: alguien intenta adivinar la contraseña.', 'Divide entre el número de noches.', 'n'],
], 'Porcentaje = parte ÷ total × 100.', 'n')
c.L('📄', 'El reporte del estado de las aplicaciones', 'Bloque A · Tu primera evidencia', body(
    sp('En palabras sencillas', 'Es un documento corto que dice <b>cómo está cada herramienta, qué problema tiene y qué se recomienda</b>. Lo lee el dueño, que no es técnico: debe entenderse a la primera.'),
    bk('1. Datos', 'Equipo revisado, fecha, hora y quién revisó.'),
    bk('2. Tabla de estado', 'Una fila por herramienta: estado (semáforo), detalle con el indicador y evidencia (captura).'),
    bk('3. Interpretación', 'Qué significa cada problema y qué riesgo trae. Ejemplo: «sin tiempo real, una USB infectada contagia la caja».'),
    bk('4. Recomendaciones', 'Qué hacer, quién y para cuándo, empezando por lo crítico.'),
    ex('Ejemplo de una fila', '🔴 <b>Copias de seguridad</b> · Última copia correcta hace 18 días; la unidad USB está desconectada · <i>Riesgo:</i> si el disco falla se pierden las ventas del mes · <i>Acción:</i> cambiar a un disco fijo y copia diaria, hoy.')),
    'Estado + indicador + riesgo + acción: así se lee fácil.')
c.O('🔢', 'Ordena cómo se hace un reporte de estado', 'Pon los pasos en el orden correcto.', [
    ['Abrir cada herramienta y anotar su estado', 'Primero se observa.'],
    ['Comparar cada dato con la meta del manual', 'Con la meta sabes si cumple.'],
    ['Asignar el color del semáforo', 'Verde, amarillo o rojo según la comparación.'],
    ['Escribir el riesgo de cada problema', 'Se interpreta qué puede pasar.'],
    ['Proponer acciones empezando por lo crítico', 'Al final se recomienda qué hacer.'],
], 'Observar → comparar → clasificar → interpretar → recomendar.')
sim('📊', 'Revisa el estado de la caja', 'Centro de seguridad simulado: monitorea y genera el reporte.', 'sa',
    'Don Beto te pide revisar la computadora de la caja (CAJA-01). <b>No cambies nada todavía</b>: primero observa y reporta. Recorre cada herramienta desde el menú de la izquierda (en celular, arriba).',
    [['Entra al <b>Antivirus</b> y revisa sus indicadores.', 'a.seen("av")'],
     ['Entra al <b>Firewall</b> y revisa los perfiles y las reglas.', 'a.seen("fw")'],
     ['Entra a <b>Windows Update</b>.', 'a.seen("wu")'],
     ['Entra a <b>Copias de seguridad</b>.', 'a.seen("bk")'],
     ['Entra a <b>Cuentas</b>.', 'a.seen("acc")'],
     ['Haz un <b>examen rápido</b> con el antivirus (comprobar que funciona sí está permitido).', 'a.used("avscan")'],
     ['Vuelve al <b>Panel</b> y genera el <b>reporte de estado</b>.', 'a.rep>=1']],
    'Lee cada aviso en rojo o amarillo: son los problemas que vas a interpretar en la siguiente actividad.')
c.Z('🔎', 'Interpreta el reporte de la caja', 'Completa la interpretación con lo que viste en el simulador.',
    '<p>La herramienta con más problemas críticos es {0}.</p>'
    '<p>La cuenta «Cliente» es administrador; el riesgo es que un cliente pueda {1}.</p>'
    '<p>La regla «Juego_Torrent» abre un {2} que nadie autorizó.</p>'
    '<p>Las copias fallan porque {3}.</p>'
    '<p>Lo primero que se debe corregir son los puntos en color {4}.</p>',
    [['el antivirus', ['el antivirus', 'las cuentas', 'el panel']],
     ['instalar programas y cambiar la configuración', ['instalar programas y cambiar la configuración', 'imprimir', 'navegar más rápido']],
     ['puerto', ['puerto', 'archivo', 'usuario']],
     ['la unidad USB está desconectada', ['la unidad USB está desconectada', 'el disco está lleno de fotos', 'el antivirus las borra']],
     ['rojo', ['rojo', 'amarillo', 'verde']]],
    'Vuelve al simulador y lee el reporte si dudas.')
c.W('✍️', 'Escribe una recomendación', 'Redacta una fila de recomendación para Don Beto.',
    'Escribe una recomendación para el problema de <b>Windows Update en pausa</b>. Di el <b>riesgo</b>, la <b>acción</b> y <b>para cuándo</b>.',
    [['Tiene al menos 20 palabras', 'palabras:20'],
     ['Menciona el riesgo (virus, ataque, falla, hoyo, vulnerable…)', '\\b(riesgo|virus|ataque\\w*|falla\\w*|hoyo\\w*|vulnerab\\w*|desprotegid\\w*|amenaza\\w*)\\b'],
     ['Dice la acción (reanudar, instalar, actualizar)', '\\b(reanud\\w*|instal\\w*|actualiz\\w*|quitar la pausa)\\b'],
     ['Dice cuándo (hoy, de inmediato, esta semana…)', '\\b(hoy|inmediat\\w*|ya|urgente|esta semana|manana|antes de)\\b']],
    'Riesgo + acción + fecha.', 'Ejemplo: Riesgo: la caja tiene hoyos de seguridad conocidos… Acción: …')
a_end = c.mark() - 1

# ───────────────────────── Bloque B · Modifica configuraciones ─────────────────────────
b0 = c.mark()
c.L('📘', 'Modificar con procedimiento', 'Bloque B · El manual manda', body(
    sp('En palabras sencillas', 'Modificar una configuración es <b>cambiar un ajuste de una herramienta</b>. En una empresa no se cambia «a ver qué pasa»: se sigue el <b>procedimiento del manual</b> que hiciste en el R.A. 2.1.'),
    px('Los 6 pasos de un cambio seguro', [
        '<b>Motivo:</b> ¿por qué hay que cambiarlo? (un problema del reporte o un requerimiento nuevo).',
        '<b>Autorización:</b> el responsable (Don Beto) aprueba el cambio.',
        '<b>Respaldo:</b> guarda la configuración actual por si algo sale mal.',
        '<b>Aplicación:</b> haz el cambio siguiendo el manual, paso a paso.',
        '<b>Prueba:</b> comprueba que funciona y que no se descompuso otra cosa.',
        '<b>Registro:</b> anota el cambio en la bitácora (antes, después, quién y cuándo).']),
    warn('Error común', 'Desactivar el antivirus o el firewall «un ratito» para que funcione algo y olvidar volver a activarlo.')),
    'Motivo → autorización → respaldo → cambio → prueba → registro.')
c.L('📝', 'El reporte de modificación (control de cambios)', 'Bloque B · Tu segunda evidencia', body(
    sp('En palabras sencillas', 'Es la <b>lista de cambios hechos</b> con lo necesario para entenderlos y deshacerlos si hace falta.'),
    bk('Columnas', 'Fecha y hora · equipo · herramienta · cambio · valor <b>antes</b> · valor <b>después</b> · motivo · quién autorizó · resultado de la prueba.'),
    ana('Piensa en un expediente médico', 'El doctor anota qué medicina cambió, por qué y cómo reaccionó el paciente. Si algo sale mal, otro doctor sabe qué se hizo.'),
    ex('Ejemplo', '04/12 · 08:20 · CAJA-01 · Firewall · Eliminar regla «Juego_Torrent» · Antes: permitir puerto 6881 · Después: eliminada · Motivo: puerto abierto sin autorización · Autorizó: Don Beto · Prueba: el panel ya no marca el firewall en rojo.')),
    'Si no está registrado, para el negocio el cambio no existe.')
c.A('⚖️', '¿El cambio se hizo bien?', 'Decide si cada forma de modificar sigue el procedimiento.', [
    ['Cambiar la regla del firewall después de que Don Beto la aprobó y anotarlo en la bitácora', 'Bien hecho', 'Tiene autorización y registro.'],
    ['Apagar el antivirus para instalar un programa y olvidar encenderlo', 'Mal hecho', 'Deja el equipo desprotegido y no hubo prueba final.'],
    ['Exportar las reglas del firewall antes de cambiarlas', 'Bien hecho', 'Si algo falla, se puede regresar a como estaba.'],
    ['Cambiar varias cosas a la vez sin anotar el valor anterior', 'Mal hecho', 'Si algo deja de funcionar, no sabrás qué regresar.'],
    ['Probar que la copia de seguridad se abre después de cambiar la unidad', 'Bien hecho', 'Comprobar el funcionamiento es parte del procedimiento.'],
    ['Darle permisos de administrador a la cajera «para que ya no pregunte»', 'Mal hecho', 'Rompe el privilegio mínimo del manual.'],
], 'Bien hecho = sigue el manual, se respalda, se prueba y se registra.', ['Bien hecho', 'Mal hecho'])
sim('🛠️', 'Corrige la caja con el manual', 'Centro de seguridad simulado: aplica los procedimientos del manual.', 'sb',
    'Don Beto autorizó corregir todo lo que salió en rojo y amarillo. Aplica el manual en la caja. Cada cambio se anota solo en la <b>Bitácora de cambios</b>.',
    [['<b>Antivirus:</b> activa el tiempo real y el análisis de USB, actualiza las definiciones y quita la exclusión.', 'a.av.rt&&a.av.usb&&a.av.def==0&&!a.av.exc.length'],
     ['<b>Antivirus:</b> la amenaza en cuarentena es un keylogger: elimínala (no la restaures).', 'a.av.q[0].st=="Eliminada"'],
     ['<b>Firewall:</b> actívalo en la red pública, elimina «Juego_Torrent» y deja el escritorio remoto solo en la red privada.', 'a.fw.pub&&!a.rule(function(r){return /Juego/.test(r.n)}).length&&a.rule(function(r){return r.p=="3389"&&r.pr=="Privada"}).length==1'],
     ['<b>Windows Update:</b> reanuda las actualizaciones e instala al menos las de seguridad.', 'a.wu.pause==0&&!a.wu.pend.some(function(p){return p.c})'],
     ['<b>Windows Update:</b> pon las horas activas de 08:00 a 21:00 (el horario de la papelería).', 'a.wu.h1<="08:00"&&a.wu.h2>="21:00"'],
     ['<b>Copias:</b> usa el disco de respaldo (D:) o OneDrive, copia cada día y haz una copia ahora.', '!/desconectada/.test(a.bk.drv)&&(a.bk.freq=="Cada día"||a.bk.freq=="Cada hora")&&a.bk.last==0&&!a.bk.fail'],
     ['<b>Cuentas:</b> la cuenta «Cliente» debe ser estándar y la de «Pepe» (ya no trabaja) debe estar deshabilitada.', 'a.acc("Cliente").t=="Estándar"&&!a.acc("Pepe").on'],
     ['Genera un <b>nuevo reporte de estado</b> sin puntos críticos y revisa la <b>Bitácora de cambios</b>.', 'a.rep>=1&&a.S.rep[a.S.rep.length-1].is.every(function(x){return x[1]!="r"})&&a.seen("log")']],
    'Usa el Panel para ver qué falta: las bolitas rojas y amarillas del menú te dicen dónde.')
c.L('🆕', 'Nuevos requerimientos', 'Bloque B · Cuando el negocio cambia', body(
    sp('En palabras sencillas', 'Un requerimiento nuevo es una <b>necesidad que antes no existía</b>: llega un empleado, se compra un programa, cambia una ley o aparece un riesgo nuevo. La configuración se ajusta para atenderlo sin abrir puertas de más.'),
    bk('Ejemplos en la papelería', 'Contrató a <b>Sofía</b> en la caja · compró un <b>programa de punto de venta</b> que usa el puerto 8080 en la red local · el contador pide <b>conservar las facturas un año</b> · Don Beto ya <b>no usa el escritorio remoto</b>.'),
    px('Cómo se atiende', [
        '<b>Analiza:</b> ¿qué necesita exactamente? (qué programa, qué puerto, qué persona, qué datos).',
        '<b>Propón</b> la configuración mínima que lo resuelve.',
        '<b>Autoriza, aplica, prueba y registra</b>, como cualquier cambio.']),
    bk('Regla de oro', 'Abre <b>solo</b> lo necesario: un puerto y no todos; la red privada y no todas; cuenta estándar y no administrador.', 'sp'),
    warn('Lo que ya no se usa, se cierra', 'Si el escritorio remoto ya no se ocupa, se elimina o se bloquea su regla. Cada puerta abierta es un riesgo.')),
    'Nuevo requerimiento = cambio mínimo, autorizado y registrado.')
c.A('🧩', 'Requerimiento → configuración', 'Elige la configuración que atiende cada requerimiento.', [
    ['Llegó Sofía, nueva cajera', 'Crear cuenta estándar', 'Una cuenta por persona y sin permisos de administrador.'],
    ['El punto de venta necesita el puerto 8080 en la red de la papelería', 'Regla de firewall en red privada', 'Se abre solo ese puerto y solo en la red local.'],
    ['El contador pide conservar las facturas un año', 'Cambiar la retención de copias', 'Las copias deben guardarse al menos un año.'],
    ['Don Beto ya no usa el escritorio remoto', 'Eliminar o bloquear la regla', 'Lo que no se usa se cierra.'],
    ['Un empleado renunció', 'Deshabilitar la cuenta', 'Se deshabilita el mismo día para que no pueda entrar.'],
], 'Busca la configuración más pequeña que resuelve la necesidad.',
    ['Crear cuenta estándar', 'Regla de firewall en red privada', 'Cambiar la retención de copias', 'Eliminar o bloquear la regla', 'Deshabilitar la cuenta'])
sim('🆕', 'Atiende los nuevos requerimientos', 'Centro de seguridad simulado: ajusta la configuración a lo que el negocio necesita ahora.', 'sc',
    'La caja ya está corregida. Don Beto trae una lista de <b>nuevos requerimientos</b> (ya autorizados). Atiéndelos con el cambio mínimo.',
    [['Crea la cuenta <b>Sofia</b> de tipo <b>estándar</b> para la nueva cajera.', 'a.acc("Sofia")&&a.acc("Sofia").t=="Estándar"&&a.acc("Sofia").on'],
     ['Agrega una regla que <b>permita</b> el puerto <b>8080</b> («Punto de venta») solo en la red <b>privada</b>.', 'a.rule(function(r){return r.p=="8080"&&r.a=="Permitir"&&r.pr=="Privada"}).length==1'],
     ['Don Beto ya no usa el <b>escritorio remoto</b> (3389): elimina su regla.', '!a.rule(function(r){return r.p=="3389"&&r.a=="Permitir"}).length'],
     ['Para no perder ventas, cambia las copias a <b>cada hora</b>.', 'a.bk.freq=="Cada hora"'],
     ['El contador pide conservar las copias <b>1 año</b> o más.', 'a.bk.keep=="1 año"||a.bk.keep=="Para siempre"'],
     ['Comprueba que todo sigue en verde: genera el <b>reporte de estado</b>.', 'a.rep>=1&&a.issues()==0']],
    'Las cuentas se crean en Cuentas › Agregar cuenta; las reglas en Firewall › Nueva regla.',
    'scFix(s)')
c.L('📤', 'Respalda las configuraciones', 'Bloque B · Tu tercera evidencia', body(
    sp('En palabras sencillas', 'Además de respaldar los <b>datos</b> (fotos, facturas), se respalda la <b>configuración</b>: las reglas, ajustes y cuentas que tanto trabajo costó dejar bien. Si el equipo se descompone o se reinstala, se restaura en minutos.'),
    bk('Qué se puede exportar en Windows', '<b>Firewall:</b> wf.msc › Acción › Exportar directiva (archivo .wfw). <b>Antivirus:</b> la lista de sus ajustes con PowerShell (Get-MpPreference). <b>Programas instalados:</b> winget list. <b>Equipo:</b> systeminfo. <b>Sistema completo:</b> un punto de restauración.'),
    bk('Dónde se guarda', '<b>Fuera del equipo</b>: un disco de respaldo, una USB guardada en otro lugar o la nube. Un respaldo en el mismo Escritorio se pierde junto con el equipo.'),
    bk('Regla 3-2-1', '<b>3</b> copias, en <b>2</b> lugares distintos, y <b>1</b> fuera del negocio (por ejemplo, en la nube).'),
    warn('Protégelo', 'Un respaldo de configuración dice cómo está protegida la red: guárdalo comprimido y con contraseña (7-Zip con AES-256).')),
    'Configuración respaldada fuera del equipo = recuperación rápida.')
c.A('💾', '¿Buen lugar para el respaldo?', 'Decide si cada lugar es seguro para guardar el respaldo de configuración.', [
    ['En el Escritorio de la misma computadora', 'Mal lugar', 'Si el equipo falla o se reinstala, el respaldo se pierde con él.'],
    ['En el disco de respaldo (D:) y una copia en OneDrive', 'Buen lugar', 'Cumple la regla 3-2-1: dos lugares y uno fuera.'],
    ['Comprimido con contraseña en una USB que Don Beto guarda en su casa', 'Buen lugar', 'Está fuera del negocio y protegido.'],
    ['Enviado por WhatsApp a un grupo de amigos', 'Mal lugar', 'Información sensible en manos de cualquiera.'],
    ['En la carpeta Descargas de la computadora de renta', 'Mal lugar', 'Los clientes la pueden ver o borrar.'],
], 'Buen lugar = fuera del equipo, protegido y solo para el responsable.', ['Buen lugar', 'Mal lugar'])
sim('📤', 'Respalda y recupera la configuración', 'Centro de seguridad simulado: exporta, simula una falla y restaura.', 'sd',
    'La caja está bien configurada. Antes de que algo pase, <b>respalda su configuración</b> y comprueba que la puedes recuperar.',
    [['En <b>Respaldar configuración</b>, exporta las <b>5 herramientas</b> a un lugar <b>fuera del equipo</b> (disco D: u OneDrive).', '["av","fw","wu","bk","acc"].every(function(k){return a.exp(k)})'],
     ['Simula una <b>falla</b> (reinstalación de Windows) y mira cómo queda el Panel.', 'a.used("crash")'],
     ['<b>Restaura</b> la configuración desde tu respaldo.', 'a.restored'],
     ['Comprueba con el <b>reporte de estado</b> que todo volvió a verde.', 'a.restored&&a.rep>=1&&a.S.rep[a.S.rep.length-1].is.length==0'],
     ['Revisa en la <b>Bitácora de cambios</b> la falla y la restauración.', 'a.restored&&a.seen("log")']],
    'Si guardas los respaldos en el Escritorio, se pierden con la falla: pruébalo y verás.',
    'scFix(s)')
c.O('♻️', 'Ordena la recuperación', 'Ordena lo que haces cuando la caja se reinstala.', [
    ['Conectar el disco de respaldo o entrar a OneDrive', 'Primero se recupera el acceso al respaldo.'],
    ['Importar la configuración del firewall y del antivirus', 'Se restauran los ajustes de protección.'],
    ['Volver a crear las cuentas con su tipo correcto', 'Se aplican las cuentas del respaldo.'],
    ['Generar el reporte de estado', 'Se comprueba que todo quedó en verde.'],
    ['Registrar la recuperación en la bitácora', 'Al final queda anotado.'],
], 'Acceder al respaldo → restaurar → comprobar → registrar.')
c.W('✍️', 'Registra un cambio', 'Escribe una fila de tu reporte de modificación.',
    'Escribe el registro del cambio <b>«Agregar regla para el punto de venta»</b>. Incluye el <b>antes</b>, el <b>después</b>, el <b>motivo</b> y <b>quién autorizó</b>.',
    [['Tiene al menos 20 palabras', 'palabras:20'],
     ['Dice cómo estaba antes', '\\b(antes|no existia|sin regla|anterior)\\b'],
     ['Dice cómo quedó (puerto 8080, permitir, privada)', '\\b(8080|despues|permit\\w*|privada)\\b'],
     ['Dice el motivo', '\\b(motivo|porque|para que|necesita|requerimiento)\\b'],
     ['Dice quién autorizó', '\\b(autoriz\\w*|aprob\\w*|don beto)\\b']],
    'Antes · después · motivo · autorizó.', 'Ejemplo: 03/12 08:30 CAJA-01 Firewall. Antes: no existía regla…')
b_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Seguimiento', 'Revisar con regularidad que una herramienta funcione y corregirla si no.'),
    bk('Estado', 'Cómo se encuentra una herramienta: activada, actualizada, con errores.'),
    bk('Funcionamiento', 'Si de verdad hace su trabajo; se comprueba con una prueba.'),
    bk('Indicador (métrica)', 'Dato medible que se compara con una meta.'),
    bk('Reporte de estado', 'Documento con el estado de cada herramienta, su riesgo y la acción recomendada.'),
    bk('Control de cambios', 'Registro de cada modificación: antes, después, motivo, autorización y prueba.'),
    bk('Requerimiento', 'Necesidad del negocio que la configuración debe atender.'),
    bk('Exclusión', 'Carpeta o archivo que el antivirus no revisa. Peligrosa si no está justificada.'),
    bk('Exportar', 'Guardar la configuración de un programa en un archivo.'),
    bk('Restaurar', 'Volver a aplicar una configuración o datos desde un respaldo.'),
    bk('Regla 3-2-1', 'Tres copias, en dos lugares, una fuera del negocio.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Laboratorio de este grupo: <b>lunes 07:50-08:40</b>. Jueves (2 h) y viernes (1 h) son aula. Los simuladores y las versiones de celular cubren lo que el laboratorio no permita.', 'sp'),
    bk('Bloque A · 20 al 26-nov', 'Viernes 20: estado, funcionamiento y semáforo. <b>Lunes 23 (laboratorio): Práctica 1</b> (reporte de estado). Jueves 26: indicadores, reporte, simulador «Revisa el estado de la caja» e interpretación.'),
    bk('Bloque B · 30-nov al 4-dic', '<b>Lunes 30 (laboratorio): Práctica 2</b> (modificación con control de cambios). Jueves 3: procedimiento, nuevos requerimientos y los simuladores «Corrige la caja» y «Atiende los nuevos requerimientos». Viernes 4: respaldo de configuraciones, simulador de recuperación y <b>Práctica 3</b>.'),
    bk('Evaluación · lunes 7-dic', 'Entrega del portafolio de evidencias (20%): reporte de estado, reporte de modificación y respaldo digital. Se desbloquea al terminar actividades y prácticas.'),
    bk('Si el laboratorio tiene restricciones', 'Si el equipo dice «Algunas opciones las administra tu organización», que lo capturen y lo expliquen: es un ejemplo real de configuración controlada. Los cambios que no se puedan hacer se documentan con el simulador.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🏪', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '📊', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '🛠️', 'a': b0, 'b': b_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🏪",t:"Empieza aquí",d:"Qué es dar seguimiento y qué vas a entregar.",time:"20 min",obj:["Explicar qué es dar seguimiento a una herramienta","Distinguir instalar, monitorear y modificar","Conocer las tres evidencias del portafolio"],sum:["Seguimiento = revisar, corregir, ajustar y respaldar.","Monitorear observa; modificar cambia un ajuste.","Portafolio: reporte de estado, reporte de cambios y respaldo."],q:"¿Qué aparato de tu casa necesita revisión aunque funcione bien?"},
a:{k:"Bloque A",l:"A",ic:"📊",t:"Elabora e interpreta reportes del estado de las aplicaciones",d:"Estado, funcionamiento, indicadores y reporte de estado.",time:"4 h",obj:["Distinguir estado de funcionamiento","Clasificar con el semáforo","Calcular indicadores y compararlos con la meta","Elaborar e interpretar un reporte de estado"],sum:["Estado = lo que se ve; funcionamiento = lo que se prueba.","Verde cumple, amarillo se atrasa, rojo desprotege.","Indicador + meta = cumple o no cumple.","Reporte: datos, tabla, interpretación y recomendaciones."],q:"Si fueras Don Beto, ¿qué querrías leer primero en el reporte?",rev:[["Revisar cada semana el estado del antivirus es…",["Monitorear","Instalar","Modificar"],0,"Solo se observa y se reporta."],["La evidencia de este R.A. es…",["Un portafolio de evidencias","Un examen escrito","Una maqueta"],0,"Reporte de estado, de cambios y respaldo."]]},
b:{k:"Bloque B",l:"B",ic:"🛠️",t:"Modifica configuraciones",d:"Procedimiento del manual, control de cambios, nuevos requerimientos y respaldo de configuraciones.",time:"6 h",obj:["Modificar configuraciones siguiendo el manual","Registrar cambios en un control de cambios","Atender nuevos requerimientos con el cambio mínimo","Respaldar y restaurar configuraciones"],sum:["Motivo → autorización → respaldo → cambio → prueba → registro.","Control de cambios: antes, después, motivo, autorizó, prueba.","Abre solo lo necesario; cierra lo que ya no se usa.","Respaldo fuera del equipo · regla 3-2-1."],q:"¿Qué pasaría si nadie anotara los cambios en la papelería?",rev:[["Un punto en rojo en el reporte significa…",["El equipo está desprotegido","Todo está bien","Es opcional"],0,"Rojo = crítico, se corrige hoy."],["5 de 5 equipos con firewall activo es…",["100 %","50 %","5 %"],0,"5 ÷ 5 × 100."]]}
'''

ILL = r'''
ILL["Un mes después en la papelería"]=function(){return flow([["🔍","Revisar"],["📊","Reportar"],["🛠️","Corregir"],["🆕","Ajustar"],["📤","Respaldar"]],"El ciclo del seguimiento")};
ILL["Estado y funcionamiento"]=function(){return SV(340,110,R_(10,14,100,80,"g",8)+E_(60,46,"🟢",26)+T_(60,80,"Correcto","tw")+R_(120,14,100,80,"a",8)+E_(170,46,"🟡",26)+T_(170,80,"Atención","td")+R_(230,14,100,80,"r",8)+E_(280,46,"🔴",26)+T_(280,80,"Crítico","tw"),"El semáforo del estado")};
ILL["Indicadores: medir con números"]=function(){return flow([["📏","Indicador|7 días"],["🎯","Meta|1 día"],["⚖️","Comparar"],["🔴","No|cumple"]],"Indicador contra meta")};
ILL["El reporte del estado de las aplicaciones"]=function(){var bd=[["Datos","b"],["Tabla de estado","g"],["Interpretación","a"],["Recomendaciones","r"]],o=R_(85,4,170,112,"w",6);bd.forEach(function(b,i){o+=R_(95,12+i*25,150,21,b[1],4)+T_(170,26+i*25,b[0],b[1]=="a"?"td":"tw")});return SV(340,122,o,"Partes del reporte de estado")};
ILL["Modificar con procedimiento"]=function(){return flow([["❓","Motivo"],["✅","Autoriza"],["📤","Respalda"],["🛠️","Cambia"],["🧪","Prueba"],["📝","Registra"]],"Seis pasos de un cambio seguro")};
ILL["El reporte de modificación (control de cambios)"]=function(){var h=["Cambio","Antes","Después","Autorizó"],o='';h.forEach(function(x,i){o+=R_(10+i*80,14,76,24,"b",4)+T_(48+i*80,30,x,"tw")});["Regla 6881","Permitir","Eliminada","Don Beto"].forEach(function(x,i){o+=R_(10+i*80,42,76,24,"s",4)+T_(48+i*80,58,x,"t")});return SV(340,76,o,"Una fila del control de cambios")};
ILL["Nuevos requerimientos"]=function(){return flow([["🆕","Necesidad"],["🔍","Analiza"],["🧩","Cambio|mínimo"],["✅","Autoriza|y prueba"],["📝","Registra"]],"Atender un requerimiento nuevo")};
ILL["Respalda las configuraciones"]=function(){return SV(340,120,E_(50,50,"💻",34)+T_(50,84,"CAJA-01")+A_(80,50,130,30)+A_(80,50,130,90)+R_(134,12,90,36,"g",6)+T_(179,34,"Disco D:","tw")+R_(134,72,90,36,"b",6)+T_(179,94,"OneDrive","tw")+T_(290,40,"3 copias","t")+T_(290,60,"2 lugares","t")+T_(290,80,"1 fuera","t"),"Regla 3-2-1")};
'''

EXH = r'''
function lt_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:#012456;color:#eeeeee;padding:8px;font:12.5px/1.4 Consolas,monospace;white-space:pre-wrap">'+b+'</pre></div>'}
EXH.panel=function(){return exw(mw('Seguridad de Windows','<div class="mbox">🛡️ Protección antivirus · ✔ No se requiere ninguna acción '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🧱 Firewall y protección de red · ✔</div><div class="mbox" style="margin-top:6px">👤 Protección de cuentas · ⚠ Se recomienda una acción '+mk(2)+'</div>'),['Palomita verde = correcto.','Triángulo amarillo = atención: abre y lee qué recomienda.'])};
EXH.av_estado=function(){return exw(mw('Protección antivirus y contra amenazas','<div class="mbox">Último examen: hoy, 08:02 · 0 amenazas '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Actualizaciones de protección · Última: hoy, 06:40 '+mk(2)+'</div>'),['Fecha del último examen.','Fecha de las definiciones: compárala con la meta (1 día).'])};
EXH.wu_estado=function(){return exw(mw('Windows Update','<div class="mbox">✅ Estás al día · Última comprobación: hoy '+mk(1)+'</div><div class="mm" style="margin-top:6px"><span class="hl">Historial de actualizaciones '+mk(2)+'</span></div>'),['Estado actual.','Anota la fecha de la última actualización de seguridad.'])};
EXH.hist_arch=function(){return exw(mw('Historial de archivos','<div class="mbox">El Historial de archivos está <b>activado</b> '+mk(1)+'<br><small>Copia de archivos más reciente: 22/11/2026 19:00</small> '+mk(2)+'</div>'),['¿Está activado?','Fecha de la última copia: compárala con la meta.'])};
EXH.tabla_estado=function(){return exw('<table class="mtb"><tr><th>Herramienta</th><th>Indicador</th><th>Meta</th><th>Estado</th></tr><tr><td>Antivirus</td><td>Definiciones: hoy</td><td>≤ 1 día</td><td>🟢</td></tr><tr><td>Windows Update</td><td>2 pendientes de seguridad</td><td>0</td><td>🔴</td></tr><tr><td>Copias</td><td>Última: hace 3 días</td><td>Diaria</td><td>🟡</td></tr></table>',['Una fila por herramienta.','El color sale de comparar indicador y meta.'])};
EXH.reco=function(){return exw('<div class="mbox">🔴 <b>Windows Update</b>: 2 actualizaciones de seguridad pendientes. <i>Riesgo:</i> fallas conocidas sin tapar. <i>Acción:</i> instalarlas hoy al cerrar la papelería.</div>',['Problema + riesgo + acción + cuándo.'])};
EXH.cel_estado=function(){return exw(mp('Seguridad y privacidad','<div class="mbox">🛡️ Análisis de apps · ✔ '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🔄 Actualización de seguridad · 1 de noviembre de 2026 '+mk(2)+'</div><div class="mbox" style="margin-top:6px">🔒 Bloqueo de pantalla · ✔</div>'),['Play Protect.','Fecha del parche de seguridad.'])};
EXH.cel_backup=function(){return exw(mp('Copia de seguridad','<div class="mbox">Copia de seguridad de Google One · <b>Activada</b> '+mk(1)+'<br><small>Última copia: ayer, 02:13</small> '+mk(2)+'</div>'),['¿Está activada?','¿Cuándo fue la última copia?'])};
EXH.cambio_fmt=function(){return exw('<table class="mtb"><tr><th>Fecha</th><th>Herramienta</th><th>Cambio</th><th>Antes</th><th>Después</th><th>Motivo</th><th>Autorizó</th><th>Prueba</th></tr><tr><td>30/11 08:05</td><td>Pantalla</td><td>Bloqueo automático</td><td>Nunca</td><td>5 min</td><td>Equipo solo en la caja</td><td>Profe</td><td>Se bloqueó a los 5 min ✔</td></tr></table>',['Una fila por cambio.','Toma captura del antes y del después.'])};
EXH.bloqueo_pc=function(){return exw(mw('Configuración › Sistema › Inicio/apagado y batería','<div class="mbox">Apagar la pantalla después de: <b>5 minutos</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Cuentas › Opciones de inicio de sesión › Si has estado ausente, ¿cuándo debe Windows volver a pedirte que inicies sesión? <b>Al reactivarse</b> '+mk(2)+'</div>'),['Tiempo para apagar la pantalla.','Que pida contraseña al volver.'])};
EXH.navegador=function(){return exw(mw('Edge › Configuración › Privacidad, búsqueda y servicios','<div class="mbox">Microsoft Defender SmartScreen · <b>Activado</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Cambiar automáticamente a conexiones más seguras (HTTPS) · <b>Activado</b> '+mk(2)+'</div>'),['Filtro de sitios peligrosos.','Preferir HTTPS.'])};
EXH.cel_cambio=function(){return exw(mp('Pantalla','<div class="mbox">Tiempo de espera de la pantalla · <b>30 segundos</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Encontrar mi dispositivo · <b>Activado</b> '+mk(2)+'</div>'),['Bloqueo rápido.','Para localizar o borrar el celular si se pierde.'])};
EXH.ps_export=function(){return exw(lt_('PowerShell','PS C:\\Users\\Alumno&gt; <b>mkdir Respaldo_Config</b> '+mk(1)+'\nPS&gt; <b>netsh advfirewall firewall show rule name=all &gt; Respaldo_Config\\firewall.txt</b> '+mk(2)+'\nPS&gt; <b>Get-MpPreference &gt; Respaldo_Config\\defender.txt</b> '+mk(3)+'\nPS&gt; <b>winget list &gt; Respaldo_Config\\programas.txt</b>\nPS&gt; <b>systeminfo &gt; Respaldo_Config\\equipo.txt</b> '+mk(4)),['Carpeta del respaldo.','Reglas del firewall.','Ajustes del antivirus.','Datos del equipo.'])};
EXH.zip=function(){return exw(mw('Añadir al archivo (7-Zip)','<div class="mfld">Respaldo_Config_CAJA01_2026-12-04.7z '+mk(1)+'</div><div class="mfld" style="margin-top:6px">Encriptación AES-256 · ••••••••••••• '+mk(2)+'</div>'),['Nombre con equipo y fecha.','Contraseña fuerte.'])};
EXH.cel_export=function(){return exw(mp('Contactos › Exportar','<div class="mbox">Exportar a archivo .vcf '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Guardar en Drive › Respaldo_Config '+mk(2)+'</div>'),['Exporta tus contactos.','Guárdalo fuera del teléfono.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Reporte del estado de las aplicaciones',
     'prog': 'Bloque A · Estado, funcionamiento e indicadores',
     'min': 50, 'lug': '1 sesión de 50 min (laboratorio, lunes 23-nov) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Word o Documentos de Google', 'Recortes (Win + Shift + S)'],
                'steps': [
                    'Antes de empezar, termina el simulador «Revisa el estado de la caja».',
                    ['Abre <b>Seguridad de Windows</b> y captura el panel con el estado de cada área.', 'panel'],
                    ['Abre <b>Protección antivirus</b>: anota la fecha del último examen y de las definiciones. Haz un examen rápido.', 'av_estado'],
                    ['Abre <b>Windows Update</b>: anota si estás al día o cuántas pendientes hay.', 'wu_estado'],
                    ['Revisa el <b>Historial de archivos</b> (u OneDrive): ¿está activo?, ¿cuándo fue la última copia?', 'hist_arch'],
                    'Abre el Visor de eventos y anota cuántos errores hubo hoy en Aplicación y en Sistema.',
                    ['Haz la <b>tabla de estado</b>: herramienta, indicador, meta y color del semáforo.', 'tabla_estado'],
                    ['Escribe una <b>recomendación</b> por cada punto amarillo o rojo.', 'reco']]},
         'cel': {'mat': ['Celular', 'App de notas o Documentos de Google'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Revisa el estado de la caja».',
                     ['Abre <b>Ajustes › Seguridad y privacidad</b> y captura el estado.', 'cel_estado'],
                     'Abre <b>Play Store › Play Protect</b>, toca Analizar y anota el resultado.',
                     ['Revisa <b>Ajustes › Google › Copia de seguridad</b>: ¿está activa y cuándo fue la última?', 'cel_backup'],
                     'Revisa en Play Store cuántas apps tienen actualización pendiente.',
                     ['Haz la <b>tabla de estado</b> de tu celular con indicador, meta y semáforo.', 'tabla_estado'],
                     ['Escribe una <b>recomendación</b> por cada punto amarillo o rojo.', 'reco']]}},
     'entrega': ['Reporte de estado: datos, tabla con capturas, interpretación y recomendaciones.'],
     'rub': [['Datos del equipo, fecha y responsable', 10], ['Capturas de cada herramienta', 25], ['Indicadores comparados con su meta', 25], ['Semáforo correcto', 15], ['Recomendaciones con riesgo y acción', 25]]},
    {'id': 'pr2', 'n': 2, 't': 'Modificación de configuraciones con control de cambios',
     'prog': 'Bloque B · Procedimiento del manual y nuevos requerimientos',
     'min': 50, 'lug': '1 sesión de 50 min (laboratorio, lunes 30-nov) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Tu manual del R.A. 2.1', 'Formato de control de cambios'],
                'steps': [
                    'Antes de empezar, termina los simuladores «Corrige la caja con el manual» y «Atiende los nuevos requerimientos».',
                    ['Copia en tu documento el <b>formato de control de cambios</b>.', 'cambio_fmt'],
                    ['Cambio 1 · Pantalla: que se apague a los 5 minutos y pida contraseña al volver. Captura antes y después.', 'bloqueo_pc'],
                    ['Cambio 2 · Navegador: activa SmartScreen y el cambio automático a HTTPS. Captura antes y después.', 'navegador'],
                    'Cambio 3 · Antivirus: abre la configuración y anota el estado de «Protección en la nube» y «Envío automático de muestras»; actívalas si están apagadas.',
                    'Prueba cada cambio (por ejemplo, espera a que se bloquee la pantalla) y anota el resultado.',
                    'Si algo dice «Lo administra tu organización», captúralo y explica por qué no se pudo cambiar.',
                    'Agrega las capturas de la Bitácora de cambios de los simuladores.']},
         'cel': {'mat': ['Celular', 'Formato de control de cambios en notas o Documentos de Google'],
                 'steps': [
                     'Antes de empezar, termina los simuladores «Corrige la caja con el manual» y «Atiende los nuevos requerimientos».',
                     ['Copia el <b>formato de control de cambios</b>.', 'cambio_fmt'],
                     ['Cambio 1 · Pantalla: tiempo de espera de 30 segundos. Cambio 2 · activa «Encontrar mi dispositivo». Captura antes y después.', 'cel_cambio'],
                     'Cambio 3 · Quita un permiso que una app no necesite (Ajustes › Privacidad › Administrador de permisos).',
                     'Prueba cada cambio y anota el resultado.',
                     'Agrega las capturas de la Bitácora de cambios de los simuladores.']}},
     'entrega': ['Reporte de modificación: tabla de control de cambios con capturas de antes y después.'],
     'rub': [['Formato completo (antes, después, motivo, autorizó, prueba)', 30], ['Tres cambios aplicados con capturas', 30], ['Prueba de cada cambio', 20], ['Bitácora de los simuladores', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Respaldo digital de configuraciones',
     'prog': 'Bloque B · Respalda las configuraciones de las aplicaciones',
     'min': 50, 'lug': 'Aula, casa o celular (viernes 4-dic)',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'PowerShell', '7-Zip', 'USB u OneDrive'],
                'steps': [
                    'Antes de empezar, termina el simulador «Respalda y recupera la configuración».',
                    ['Abre PowerShell (Inicio › escribe PowerShell) y exporta las reglas del firewall, los ajustes del antivirus, los programas instalados y los datos del equipo a la carpeta Respaldo_Config.', 'ps_export'],
                    'Abre cada archivo .txt y comprueba que tiene información.',
                    ['Comprime la carpeta con 7-Zip, AES-256 y contraseña. El nombre lleva equipo y fecha.', 'zip'],
                    'Guárdalo fuera del equipo (USB u OneDrive) y captura dónde quedó.',
                    'Escribe en 3 renglones cómo restaurarías la configuración si el equipo se reinstala.']},
         'cel': {'mat': ['Celular', 'Google Drive'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Respalda y recupera la configuración».',
                     ['Exporta tus contactos a un archivo .vcf y guárdalo en Drive, en la carpeta Respaldo_Config.', 'cel_export'],
                     'Captura tus ajustes de seguridad (bloqueo, Play Protect, Encontrar mi dispositivo) y súbelos a la misma carpeta.',
                     ['Revisa que la copia de seguridad de Google esté activa y haz una copia ahora.', 'cel_backup'],
                     'Escribe en 3 renglones cómo restaurarías todo en un celular nuevo.']}},
     'entrega': ['Respaldo digital (archivo .7z o carpeta en Drive) y capturas de dónde quedó.', 'Procedimiento de restauración en 3 renglones.'],
     'rub': [['Configuraciones exportadas', 35], ['Respaldo protegido (contraseña o cuenta)', 20], ['Guardado fuera del equipo', 20], ['Procedimiento de restauración', 25]]},
]

EVALUATION = {
    'course': 'ASIN-20 · Aplicación de la seguridad informática · Unidad 2',
    'ra': 'R.A. 2.2', 'title': 'Portafolio de seguimiento de las herramientas',
    'data': [
        ('Resultado de aprendizaje', 'Da seguimiento a la operación de las herramientas informáticas de acuerdo con el plan de seguridad determinado.'),
        ('Actividad de evaluación', '2.2.1 Monitorea la operación de las herramientas informáticas a fin de garantizar su funcionamiento y elabora un portafolio de evidencias.'),
        ('Evidencias', 'Reporte del estado de las aplicaciones · Reporte de modificación de configuraciones · Respaldo digital de configuraciones'),
        ('Ponderación', '20% (según el programa)'),
        ('Entrega', 'Lunes 7 de diciembre'),
    ],
    'situation': 'Don Beto quiere saber si la seguridad que instalaste sigue funcionando. Arma un <b>portafolio de evidencias</b> con el estado de las herramientas, los cambios que hiciste para corregirlas o atender nuevas necesidades y el respaldo de su configuración. Usa lo que produjiste en tus tres prácticas y en los simuladores.',
    'hint': 'Ya tienes casi todo: ordénalo en las tres secciones y revisa que cada problema tenga su riesgo y cada cambio su antes y después.',
    'steps': [
        ('Inicio', [
            'Portada: nombre del portafolio, tu nombre completo, grupo y fecha.',
            'Índice con las tres evidencias.']),
        ('1. Reporte del estado de las aplicaciones', [
            'Datos del equipo, fecha y responsable.',
            'Tabla con cada herramienta: indicador, meta, semáforo y captura.',
            'Interpretación del riesgo y recomendaciones, empezando por lo crítico.']),
        ('2. Reporte de modificación de configuraciones', [
            'Tabla de control de cambios: fecha, herramienta, cambio, antes, después, motivo, autorizó y prueba.',
            'Al menos 3 cambios propios con captura de antes y después, y la bitácora de los simuladores.',
            'Un nuevo requerimiento atendido y explicado (por qué fue el cambio mínimo).']),
        ('3. Respaldo digital de configuraciones', [
            'El archivo de respaldo (.7z o carpeta de Drive) o la captura de dónde quedó.',
            'Procedimiento de restauración en pasos.']),
        ('Cierre', [
            'Conclusión: ¿por qué no basta con instalar las herramientas una vez?']),
    ],
    'rubric': [
        ('Portada e índice', 5), ('Reporte de estado con indicadores y semáforo', 25), ('Interpretación y recomendaciones', 15),
        ('Control de cambios completo', 25), ('Nuevo requerimiento atendido', 10), ('Respaldo digital y restauración', 15), ('Conclusión y presentación', 5),
    ],
    'deliver': ['Un solo archivo PDF o Word con las tres evidencias (el respaldo .7z, si lo haces, va como captura de dónde quedó).', 'Nombre del archivo: Apellido_Nombre_Portafolio_ASIN22.', 'Súbelo en la actividad R.A. 2.2 de la plataforma.'],
}
