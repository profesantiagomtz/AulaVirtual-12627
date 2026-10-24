"""ASIN-20 · R.A. 2.1 · Instala y configura herramientas de seguridad.

Caso de toda la unidad: la Papelería Don Beto del R.A. 1.2 (5 computadoras:
1 caja, 1 oficina y 3 de renta para clientes; 3 empleados y el dueño). En el
1.2 los alumnos hicieron su plan; aquí lo ponen en práctica.
"""
from cw import Course, sp, ex, ana, bk, warn, r3, px, html, body

CODE = 'ASIN-RA-2.1'
CODE_PREFIX = 'ASIN21'
FILE = 'asin-ra21-material.html'
TITLE_TAG = 'ASIN-20 · R.A. 2.1 · Instala y configura herramientas de seguridad'
BRAND = 'ASIN-20 · Seguridad informática'
BRAND_SUB = 'R.A. 2.1 · Instala y configura herramientas'
HERO_KICK = 'ASIN-20 · R.A. 2.1'
HERO_TITLE = 'Instala y configura herramientas de seguridad'
HERO_TEXT = 'Pon en marcha el plan de Don Beto: instala, configura y documenta la seguridad de cada computadora y de su red.'
EV_SHORT = 'elabora tu manual de instalación y configuración.'
EV_CARD = 'Manual de instalación'
RA = 'R.A. 2.1'
GROUP = '310'

TABS = {'d': ['Diagnostica', 'Revisa y comprueba tu avance'], 'c': ['Construye', 'Instala y configura en práctica']}

c = Course()

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🏠', 'Del plan a la acción', 'En el R.A. 1.2 hiciste el plan; ahora lo vas a aplicar', body(
    sp('En palabras sencillas', 'Instalar y configurar herramientas de seguridad es <b>poner en las computadoras los programas y ajustes que tu plan prometió</b>: antivirus, cuentas, firewall, respaldos, cifrado.'),
    bk('Piensa en tu celular nuevo', 'Primero <b>instalas</b> tus apps. Después las <b>configuras</b>: pones huella, decides qué permisos les das y activas las actualizaciones. Con las computadoras de una empresa pasa lo mismo.'),
    ex('Caso para toda la unidad: Papelería Don Beto', 'Tiene <b>5 computadoras</b>: 1 en la caja, 1 en la oficina de Don Beto y 3 que se rentan a los clientes para imprimir y hacer tareas. En su plan prometió antivirus, una cuenta por empleado, firewall y respaldos. Ahora toca hacerlo de verdad.')),
    'Un plan que no se aplica es solo papel.')
c.L('🗺️', 'Tu ruta en este R.A.', 'Tres bloques y una evidencia final', body(
    r3([('📘', 'Bloque A', 'El manual: requerimientos, instalación y configuración'),
        ('💻', 'Bloque B', 'Seguridad dentro de cada computadora'),
        ('🌐', 'Bloque C', 'Seguridad de toda la red')]),
    bk('Al final entregas', 'Un <b>manual de instalación y configuración</b> (30% de tu calificación del módulo). Todo lo que practiques aquí se convierte en una parte de ese manual.'),
    bk('Cómo usar este material', 'Lee la lección, resuelve la actividad y revisa la explicación de cada respuesta. Las prácticas tienen versión para el laboratorio y para tu celular.')),
    'Cada práctica que hagas es una página de tu manual.')
c.A('🔎', '¿Instalar o configurar?', 'Decide si cada acción es instalar algo nuevo o configurar lo que ya está.', [
    ['Descargar 7-Zip y ponerlo en la computadora de la oficina', 'Instalar', 'Se agrega un programa que antes no estaba: eso es instalar.'],
    ['Activar las actualizaciones automáticas de Windows', 'Configurar', 'Windows ya estaba; solo se ajusta una opción.'],
    ['Ponerle contraseña a la cuenta de la cajera', 'Configurar', 'La cuenta ya existe; se ajusta su seguridad.'],
    ['Poner un antivirus en una computadora que no tenía', 'Instalar', 'Es un programa nuevo para ese equipo.'],
    ['Bloquear un juego en el firewall', 'Configurar', 'El firewall ya está; se le agrega una regla.'],
    ['Bajar una app nueva desde la tienda oficial del celular', 'Instalar', 'Agregar una app nueva es instalar.'],
], 'Instalar = agregar algo que no estaba. Configurar = ajustar algo que ya está.', ['Instalar', 'Configurar'])
c.A('🧭', '¿En la computadora o en la red?', 'Clasifica dónde se configura cada protección. Así sabrás en qué bloque la verás.', [
    ['El firewall de la computadora de la caja', 'En cada computadora', 'Protege solo a ese equipo: es seguridad local (Bloque B).'],
    ['El router que conecta la papelería a internet', 'En la red', 'Protege la entrada de toda la red (Bloque C).'],
    ['Las cuentas de usuario de Windows', 'En cada computadora', 'Cada equipo tiene sus propias cuentas (Bloque B).'],
    ['La página de pagos con candado (HTTPS)', 'En la red', 'Protege la información mientras viaja por la red (Bloque C).'],
    ['El antivirus', 'En cada computadora', 'Se instala y configura en cada equipo (Bloque B).'],
    ['Una alarma que detecta intrusos en la red', 'En la red', 'Vigila el tráfico de toda la red (Bloque C).'],
], 'Pregúntate: ¿protege a un solo equipo o a todos los que están conectados?', ['En cada computadora', 'En la red'])
s0_end = c.mark() - 1

# ───────────────────────── Bloque A · El manual ─────────────────────────
a0 = c.mark()
c.L('📘', '¿Qué es un manual de instalación?', 'Bloque A · El documento que vas a entregar', body(
    sp('En palabras sencillas', 'Es un documento con <b>los pasos para instalar un programa y dejarlo listo</b>, escrito para que cualquier persona lo pueda repetir sin ayuda.'),
    bk('Piensa en…', 'El instructivo de un mueble para armar: trae la lista de piezas (requerimientos), los pasos con dibujos (procedimiento) y cómo saber que quedó bien.'),
    ex('En la papelería', 'Si el técnico que instaló el antivirus ya no está, con el manual cualquier empleado puede reinstalarlo igual, sin adivinar.')),
    'Un buen manual lo puede seguir alguien que nunca lo ha hecho.')
c.L('📋', 'Requerimientos: ¿lo puedo instalar?', 'Bloque A · Lo que el equipo necesita', body(
    sp('En palabras sencillas', 'Los requerimientos son <b>lo que necesita la computadora para que el programa funcione</b>. Si el equipo no los cumple, el programa no se instala o funciona mal.'),
    bk('Sistema operativo', 'Qué Windows (10 u 11) y de cuántos bits (casi siempre 64 bits).'),
    bk('Procesador y memoria RAM', 'Qué tan rápido y cuánta memoria pide como mínimo (por ejemplo, 4 GB de RAM).'),
    bk('Espacio en disco', 'Cuánto lugar ocupa una vez instalado.'),
    bk('Permisos y licencia', 'Si necesitas una cuenta de administrador y si el programa es gratuito o de pago.'),
    ana('Como una receta', 'Si la receta pide horno y no tienes horno, no hay pastel. Por eso se revisa <b>antes</b> de empezar.')),
    'Revisa los requerimientos antes de instalar, no después.')
c.L('🔍', '¿Dónde veo lo que tiene mi equipo?', 'Bloque A · Para comparar con lo que pide el programa', body(
    bk('En Windows', '<b>Configuración › Sistema › Información</b>. Ahí ves el procesador, la RAM instalada, el tipo de sistema (64 bits) y la edición de Windows.'),
    bk('Espacio libre', 'Abre el <b>Explorador de archivos › Este equipo</b>. Debajo del disco C: dice cuántos GB quedan libres.'),
    bk('En el celular', '<b>Ajustes › Acerca del teléfono</b> (versión de Android y RAM) y <b>Ajustes › Almacenamiento</b> (espacio libre).'),
    ex('Atajo', 'La combinación <b>Win + Pausa</b> abre directo la pantalla de Información (si tu teclado no tiene la tecla Pausa, usa el camino de Configuración).')),
    'Anota los datos de tu equipo: los usarás en tu tabla de requerimientos.')
c.A('✅', '¿Cumple o no cumple?', 'Compara lo que pide el programa con lo que tiene la computadora de la caja.', [
    ['El programa pide 4 GB de RAM y la caja tiene 8 GB', 'Cumple', '8 GB es más que el mínimo de 4 GB.'],
    ['Pide 2 GB libres en disco y la caja tiene 500 MB libres', 'No cumple', '2 GB son 2048 MB; 500 MB no alcanzan. Hay que liberar espacio primero.'],
    ['Pide Windows de 64 bits y la caja tiene Windows 11 de 64 bits', 'Cumple', 'El sistema y los bits coinciden.'],
    ['Pide permisos de administrador y la cajera usa una cuenta estándar', 'Necesita al administrador', 'La cuenta estándar no puede instalar: Don Beto (administrador) debe autorizarlo.'],
    ['Pide internet para activarse y la caja tiene internet', 'Cumple', 'Tiene lo que se necesita para activarlo.'],
], 'Si lo que tiene el equipo es igual o mayor que lo que pide el programa, cumple.', ['Cumple', 'No cumple', 'Necesita al administrador'])
c.L('🪜', 'El procedimiento de instalación', 'Bloque A · Pasos que cualquiera puede seguir', body(
    sp('En palabras sencillas', 'El procedimiento es la <b>lista de pasos en orden</b>. Un buen paso empieza con un verbo, hace una sola cosa y dice qué debe aparecer en pantalla.'),
    ex('Así sí', '«3. Da clic en <b>Install</b>. Aparece una barra de avance y al final el botón <b>Close</b>.»'),
    warn('Así no', '«Le picas a lo que sale y ya.» No dice dónde, ni qué botón, ni qué debe pasar.'),
    px('Ejemplo: instalar 7-Zip (un compresor gratuito que también cifra)', [
        'Entra al sitio oficial <b>7-zip.org</b>. Nunca descargues programas de páginas desconocidas.',
        'Descarga la versión para <b>Windows 64-bit (x64)</b>.',
        'Abre el archivo descargado desde la carpeta <b>Descargas</b>.',
        'Windows pregunta «¿Quieres permitir que esta aplicación haga cambios?». Da clic en <b>Sí</b> (necesitas ser administrador).',
        'Deja la carpeta que propone y da clic en <b>Install</b>. Al terminar, da clic en <b>Close</b>.',
        '<b>Verifica:</b> da clic derecho sobre cualquier archivo; debe aparecer la opción <b>7-Zip</b>.'])),
    'Verbo + una acción + lo que debe aparecer. Y una captura por paso.')
c.O('🔢', 'Ordena la instalación', 'Pon los pasos en el orden correcto, de arriba hacia abajo.', [
    ['Revisar los requerimientos del equipo', 'Primero se comprueba que el equipo puede con el programa.'],
    ['Descargar el instalador del sitio oficial', 'Con el equipo listo, se baja el programa de un lugar confiable.'],
    ['Abrir el instalador y aceptar el permiso de administrador', 'Windows pide autorización antes de instalar.'],
    ['Elegir la carpeta y dar clic en Instalar', 'Ahora sí se copian los archivos del programa.'],
    ['Verificar que el programa funciona', 'Al final se comprueba que quedó bien.'],
], 'Antes de instalar se revisa; después de instalar se verifica.')
c.L('⚙️', 'Configurar: dejarlo listo y seguro', 'Bloque A · Lo que haces después de instalar', body(
    sp('En palabras sencillas', 'Configurar es <b>ajustar las opciones de un programa</b> para que funcione como lo necesitas y de forma segura.'),
    bk('Qué se suele configurar', 'Actualizaciones automáticas, quién puede usar el programa, contraseñas, qué analiza o bloquea, dónde guarda los archivos.'),
    ex('Con 7-Zip', 'Al comprimir una carpeta se configura una <b>contraseña</b> y el método de cifrado <b>AES-256</b>, para que nadie más la pueda abrir.'),
    warn('Ojo', 'La configuración «de fábrica» no siempre es la más segura. Instalar sin configurar es como estrenar celular sin poner bloqueo de pantalla.'),
    bk('Verificación', 'Al final pruebas que todo funciona. Por ejemplo: abres el archivo comprimido y compruebas que te pide la contraseña.')),
    'Instalar + configurar + verificar = herramienta lista.')
c.L('📑', 'Las partes del manual', 'Bloque A · Lo que debe llevar tu evidencia', body(
    bk('1. Portada', 'Nombre del manual, programa, tu nombre, grupo y fecha.'),
    bk('2. Objetivo', 'Para qué sirve el manual, en una o dos líneas.'),
    bk('3. Requerimientos', 'Tabla con lo que pide el programa, lo que tiene el equipo y si cumple.'),
    bk('4. Procedimiento de instalación', 'Pasos numerados, cada uno con su captura.'),
    bk('5. Procedimiento de configuración', 'Los ajustes de seguridad que hiciste, con capturas.'),
    bk('6. Verificación', 'Cómo compruebas que todo funciona.'),
    bk('7. Problemas comunes', 'Qué hacer si aparece un error (por ejemplo, «Acceso denegado»).')),
    'Esta es la estructura de tu evidencia final.')
c.A('📑', '¿En qué parte del manual va?', 'Elige la sección del manual donde va cada texto.', [
    ['Windows 10 u 11 de 64 bits y 5 MB libres en disco', 'Requerimientos', 'Describe lo que necesita el equipo.'],
    ['Da clic en Install y espera a que termine la barra', 'Instalación', 'Es un paso para instalar el programa.'],
    ['Activa la opción Cifrar nombres de archivo', 'Configuración', 'Es un ajuste de seguridad después de instalar.'],
    ['Comprime un archivo de prueba y comprueba que pide contraseña', 'Verificación', 'Sirve para comprobar que todo funciona.'],
    ['Si aparece «Acceso denegado», pide al administrador que instale', 'Problemas comunes', 'Explica qué hacer ante un error.'],
    ['Que la oficina de Don Beto pueda proteger sus archivos con contraseña', 'Objetivo', 'Dice para qué sirve el manual.'],
], 'Requerimientos = qué necesita · Instalación = cómo se pone · Configuración = cómo se ajusta · Verificación = cómo se comprueba.',
    ['Objetivo', 'Requerimientos', 'Instalación', 'Configuración', 'Verificación', 'Problemas comunes'])
c.W('✍️', 'Escribe un paso como profesional', 'Redacta un paso para tu manual.',
    'Escribe el paso para <b>abrir el instalador</b> después de descargarlo. Empieza con un verbo y di qué debe aparecer en pantalla.',
    [['Tiene al menos 8 palabras', 'palabras:8'],
     ['Empieza con un verbo (abre, da clic, busca, ejecuta…)', '^ *(abre|abrir|da|dar|haz|dale|ejecuta|ejecutar|selecciona|busca|entra|ve|localiza|presiona|ubica)'],
     ['Menciona el instalador o el archivo', '(instalador|archivo|descarga|exe|7-zip|7zip|programa)'],
     ['Dice qué aparece o qué pasa', '(aparece|aparecera|se abre|abrira|muestra|mostrara|veras|sale|saldra|pregunta)']],
    'Verbo + dónde + lo que aparece.', 'Ejemplo: Abre la carpeta Descargas y da doble clic en el instalador; aparece una ventana que pide permiso')
c.T('🧮', 'Calcula si alcanza', 'Escribe solo el número. Recuerda: 1 GB = 1024 MB.', [
    ['La caja tiene 3 GB libres. ¿Cuántos MB son?', '3072', '3 × 1024 = 3072 MB.', 'Multiplica los GB por 1024.', 'n'],
    ['Un programa pide 1500 MB y hay 3072 MB libres. ¿Cuántos MB quedan libres después de instalarlo?', '1572', '3072 − 1500 = 1572 MB.', 'Resta lo que ocupa el programa.', 'n'],
    ['El programa pide 4 GB de RAM y la PC tiene 16 GB. ¿Cuántas veces cabe el mínimo en lo que tiene?', '4', '16 ÷ 4 = 4 veces. Cumple de sobra.', 'Divide lo que tiene entre lo que pide.', 'n'],
    ['Un instalador pesa 300 MB. Si lo descargas en cada una de las 5 computadoras, ¿cuántos MB descargas en total?', '1500', '300 × 5 = 1500 MB. En el Bloque B verás cómo un servidor central evita descargar lo mismo varias veces.', 'Multiplica por el número de computadoras.', 'n'],
], 'Lee con calma qué te piden: convertir, restar, dividir o multiplicar.', 'n')
a_end = c.mark() - 1

# ───────────────────────── Bloque B1 · Actualizaciones, cuentas y bitácoras ─────────────────────────
b10 = c.mark()
c.L('🩹', 'Actualizaciones: parches para los hoyos', 'Bloque B · Configuración local', body(
    sp('En palabras sencillas', 'Una actualización es una <b>corrección que publica el fabricante</b> para tapar una falla de seguridad (vulnerabilidad) o mejorar el programa.'),
    bk('Piensa en…', 'Una llanta ponchada: el parche cierra el hoyo antes de que se desinfle. Sin parche, cualquier clavo la vuelve a ponchar.'),
    ex('En la papelería', 'Si la caja no se actualiza, un virus puede entrar por una falla que <b>ya tenía arreglo</b> desde hace meses.'),
    warn('Dato importante', 'Muchos ataques aprovechan fallas que ya tenían parche, pero nadie lo instaló.')),
    'Equipo actualizado = protegido contra lo que ya se conoce.')
c.L('⏰', 'Actualizaciones automáticas sin que estorben', 'Bloque B · Que se instalen solas, a buena hora', body(
    bk('Windows', '<b>Configuración › Windows Update</b>. Déjalas automáticas y ajusta las <b>Horas activas</b>: el horario en que Windows no reiniciará la computadora.'),
    bk('Aplicaciones', 'La <b>Microsoft Store</b> y los navegadores se actualizan solos si no lo desactivas. En el celular, activa la actualización automática en la Play Store.'),
    ex('Don Beto', 'La papelería abre de 8:00 a 21:00. Pone esas horas activas: así la caja se actualiza y reinicia en la noche, no a mitad de una venta.'),
    warn('No hagas esto', 'Pausar las actualizaciones «para siempre» porque tardan. Solo se pausan unos días si hay una razón, y luego se instalan.')),
    'Automáticas sí, pero fuera del horario de trabajo.')
c.L('🏷️', 'Clasificación de actualizaciones', 'Bloque B · No todas son igual de urgentes', body(
    bk('🔴 De seguridad y críticas', 'Tapan fallas que un atacante puede usar. Se instalan <b>cuanto antes</b>.'),
    bk('🛡️ De definiciones', 'Le enseñan al antivirus a reconocer virus nuevos. Llegan a diario y se instalan solas.'),
    bk('🔌 Controladores (drivers)', 'Hacen que el hardware funcione: impresora, video, red.'),
    bk('✨ De características', 'Agregan funciones nuevas o cambian el aspecto. Son grandes; conviene planearlas.'),
    bk('➕ Opcionales', 'No son urgentes; se instalan si se necesitan.')),
    'Primero seguridad, después todo lo demás.')
c.L('🏢', 'Servidores centrales de actualizaciones', 'Bloque B · Cuando hay muchas computadoras', body(
    sp('En palabras sencillas', 'Un servidor central <b>descarga las actualizaciones una sola vez y las reparte</b> a todas las computadoras de la red. El administrador decide cuáles se aprueban. En Windows se llama <b>WSUS</b>.'),
    bk('Piensa en…', 'La tiendita de la colonia: compra al mayoreo y reparte, en vez de que cada vecino vaya hasta la central de abastos.'),
    ex('¿Quién lo usa?', 'Tu escuela, con decenas de computadoras, sí lo necesita. Don Beto, con 5, puede usar las actualizaciones automáticas normales.'),
    bk('Ventajas', 'Ahorra internet, el administrador prueba antes de instalar y sabe qué equipo está atrasado.')),
    'Muchas computadoras = un servidor central que controla las actualizaciones.')
c.A('🏷️', 'Clasifica la actualización', 'Elige el tipo de cada actualización.', [
    ['Corrige una falla que permitía a un virus controlar la computadora', 'De seguridad', 'Tapa un hoyo de seguridad: es de las urgentes.'],
    ['Agrega las huellas de 300 virus nuevos al antivirus', 'De definiciones', 'Las definiciones enseñan al antivirus a reconocer amenazas nuevas.'],
    ['Hace que funcione la impresora nueva de la papelería', 'Controlador', 'Los controladores (drivers) hacen funcionar el hardware.'],
    ['Cambia el menú Inicio y agrega funciones nuevas', 'De características', 'Trae funciones nuevas: es una actualización de características.'],
    ['Un paquete de idioma extra que nadie en la papelería usa', 'Opcional', 'No es necesaria: se instala solo si se necesita.'],
], 'Pregúntate: ¿tapa un hoyo, enseña al antivirus, hace funcionar un aparato, trae funciones o es extra?',
    ['De seguridad', 'De definiciones', 'Controlador', 'De características', 'Opcional'])
c.A('⚖️', '¿Buena o mala decisión?', 'Decide si cada decisión sobre actualizaciones es buena o mala.', [
    ['Pausar las actualizaciones para siempre porque «hacen lenta la computadora»', 'Mala decisión', 'El equipo queda con hoyos de seguridad conocidos.'],
    ['Poner horas activas de 8:00 a 21:00 en la caja', 'Buena decisión', 'Se actualiza fuera del horario de ventas.'],
    ['Instalar primero las actualizaciones de seguridad', 'Buena decisión', 'Son las que tapan fallas que los atacantes ya conocen.'],
    ['Descargar «parches» de una página desconocida', 'Mala decisión', 'Solo se actualiza desde Windows Update o el sitio oficial; lo demás puede traer virus.'],
    ['Usar un servidor central en una escuela con 40 computadoras', 'Buena decisión', 'Se descarga una vez y el administrador controla qué se instala.'],
], 'Una buena decisión mantiene el equipo al día sin interrumpir el trabajo.', ['Buena decisión', 'Mala decisión'])
c.L('👤', 'Cuentas de usuario: cada quien la suya', 'Bloque B · Quién entra y qué puede hacer', body(
    sp('En palabras sencillas', 'Una cuenta es tu <b>llave personal</b> para entrar a la computadora. Hay dos tipos: <b>Administrador</b> (puede instalar y cambiar todo) y <b>Estándar</b> (usa los programas, pero no cambia la configuración).'),
    bk('Piensa en…', 'Las llaves del local: Don Beto tiene la llave de todo; los empleados, solo la de la entrada.'),
    bk('Regla de oro: privilegio mínimo', 'Cada persona recibe <b>solo los permisos que necesita</b> para su trabajo. Ni uno más.'),
    ex('Don Beto', 'Administrador: solo él, con contraseña fuerte. Cajera y empleados: cuenta estándar, una por persona. Las 3 computadoras de renta: una cuenta estándar «Cliente», sin acceso a la oficina.'),
    warn('Errores comunes', 'Compartir la misma cuenta entre todos, usar la cuenta de administrador para trabajar a diario y no poner contraseña.')),
    'Una cuenta por persona y el permiso justo.')
c.L('🔐', 'Cómo se administran las cuentas', 'Bloque B · Dónde se hace en Windows', body(
    bk('Agregar o cambiar cuentas', '<b>Configuración › Cuentas › Otros usuarios</b>. Ahí se agrega una cuenta y se cambia su tipo (administrador o estándar). Necesitas ser administrador.'),
    bk('Inicio de sesión', '<b>Configuración › Cuentas › Opciones de inicio de sesión</b>: contraseña o PIN.'),
    bk('Bloquear al levantarte', 'Presiona <b>Win + L</b>. La sesión queda cerrada con tu contraseña y nadie usa tu cuenta.'),
    ex('Política de cuentas de Don Beto', '1) Cada empleado tiene su cuenta estándar. 2) Contraseña de al menos 10 caracteres. 3) Se bloquea la sesión al dejar la caja. 4) Al salir un empleado, se desactiva su cuenta ese mismo día.')),
    'Win + L antes de levantarte.')
c.A('👥', '¿Qué tipo de cuenta le das?', 'Aplica el privilegio mínimo a cada persona.', [
    ['Don Beto, el dueño que instala programas', 'Administrador', 'Es el responsable de instalar y configurar.'],
    ['La cajera, que solo cobra', 'Estándar', 'Solo usa el programa de cobro; no necesita cambiar nada.'],
    ['Los clientes en las computadoras de renta', 'Estándar', 'Usan programas, pero no deben instalar ni cambiar la configuración.'],
    ['El ayudante que imprime y escanea', 'Estándar', 'Usar la impresora no requiere permisos de administrador.'],
    ['La cuenta con la que se cambia la configuración del firewall', 'Administrador', 'Cambiar el firewall es una tarea de administración.'],
], 'Si no instala ni cambia configuraciones, le basta una cuenta estándar.', ['Administrador', 'Estándar'])
c.L('📒', 'Bitácoras: el diario de la computadora', 'Bloque B · Lo que pasó, con fecha y hora', body(
    sp('En palabras sencillas', 'Una bitácora (registro o <i>log</i>) es la <b>lista de lo que pasa en el equipo</b>, con fecha y hora: quién entró, qué falló, qué se instaló.'),
    bk('Piensa en…', 'La libreta de la caseta de vigilancia donde se anota quién entra y a qué hora.'),
    bk('Dónde se ve', '<b>Win + X › Visor de eventos › Registros de Windows</b>. Tiene tres registros principales: <b>Aplicación</b> (programas), <b>Seguridad</b> (inicios de sesión) y <b>Sistema</b> (Windows y hardware).'),
    bk('Niveles', 'ℹ️ Información (todo normal) · ⚠️ Advertencia (atención) · ❌ Error (algo falló). En Seguridad verás «Auditoría correcta» o «Error de auditoría».'),
    ex('En la papelería', 'Varios «Error de auditoría» de inicio de sesión a las 3 de la mañana: alguien intentó adivinar la contraseña.'),
    warn('Ojo', 'La bitácora solo sirve si alguien la revisa. La política dice quién y cada cuándo.')),
    'Aplicación = programas · Seguridad = quién entra · Sistema = Windows y hardware.')
c.A('📒', '¿Qué registro reviso?', 'Elige en qué registro del Visor de eventos buscarías cada cosa.', [
    ['Quiero saber si alguien intentó entrar con contraseña equivocada', 'Seguridad', 'Los inicios de sesión, correctos o fallidos, quedan en Seguridad.'],
    ['El programa de cobro se cerró solo', 'Aplicación', 'Las fallas de los programas quedan en Aplicación.'],
    ['La computadora se apagó de golpe sin razón', 'Sistema', 'Los apagados y fallas de Windows quedan en Sistema.'],
    ['Falló el controlador de la impresora al encender', 'Sistema', 'El hardware y sus controladores se registran en Sistema.'],
    ['A qué hora inició sesión la cajera', 'Seguridad', 'Los inicios de sesión correctos también están en Seguridad.'],
    ['Excel marcó un error al abrir un archivo', 'Aplicación', 'Excel es un programa: su error va a Aplicación.'],
], 'Programas → Aplicación · Personas que entran → Seguridad · Windows y aparatos → Sistema.', ['Aplicación', 'Seguridad', 'Sistema'])
c.Z('🔎', 'Lee la bitácora de la caja', 'Lee el registro y completa las conclusiones.',
    '<div style="overflow-x:auto;margin-bottom:12px"><table class="mtb" style="font-size:12.5px"><tr><th>Hora</th><th>Nivel</th><th>Registro</th><th>Descripción</th></tr>'
    '<tr><td>08:01</td><td>Auditoría correcta</td><td>Seguridad</td><td>Inicio de sesión: Cajera</td></tr>'
    '<tr><td>03:12</td><td>Error de auditoría</td><td>Seguridad</td><td>Inicio de sesión fallido: Administrador</td></tr>'
    '<tr><td>03:13</td><td>Error de auditoría</td><td>Seguridad</td><td>Inicio de sesión fallido: Administrador</td></tr>'
    '<tr><td>03:13</td><td>Error de auditoría</td><td>Seguridad</td><td>Inicio de sesión fallido: Administrador</td></tr>'
    '<tr><td>10:40</td><td>Advertencia</td><td>Sistema</td><td>Poco espacio en el disco C:</td></tr>'
    '<tr><td>12:05</td><td>Error</td><td>Aplicación</td><td>El programa de cobro dejó de responder</td></tr></table></div>'
    '<p>Hubo {0} intentos fallidos de entrar como Administrador.</p>'
    '<p>Ocurrieron a las {1}, cuando la papelería está cerrada.</p>'
    '<p>Lo más probable es que alguien {2}.</p>'
    '<p>El aviso de poco espacio es de nivel {3}.</p>'
    '<p>La falla del programa de cobro aparece en el registro de {4}.</p>',
    [['3', ['3', '1', '6']],
     ['3 de la mañana', ['3 de la mañana', '8 de la mañana', '12 del día']],
     ['intentó adivinar la contraseña', ['intentó adivinar la contraseña', 'imprimió un documento', 'actualizó Windows']],
     ['Advertencia', ['Advertencia', 'Error', 'Información']],
     ['Aplicación', ['Aplicación', 'Seguridad', 'Sistema']]],
    'Cuenta las filas de «Error de auditoría» y fíjate en la hora.')
b1_end = c.mark() - 1

# ───────────────────────── Bloque B2 · Protección del equipo ─────────────────────────
b20 = c.mark()
c.L('📦', 'Manejo de software: solo lo necesario', 'Bloque B · Qué se instala, de dónde y quién', body(
    sp('En palabras sencillas', 'Manejar el software es <b>decidir qué programas se instalan, de dónde se descargan y quién puede instalarlos</b>.'),
    bk('1. Solo de sitios oficiales', 'La página del fabricante o la tienda oficial (Microsoft Store, Play Store).'),
    bk('2. Con licencia', 'Gratuito o pagado, pero legal. Los programas «crackeados» suelen traer virus.'),
    bk('3. Solo lo necesario', 'Lo que no se usa se desinstala: cada programa extra es una puerta más.'),
    bk('4. Inventario', 'Una lista de qué programas tiene cada computadora.'),
    ana('Piensa en…', 'Las medicinas: se compran en la farmacia, no a un desconocido en la calle, aunque salgan más baratas.'),
    ex('Don Beto', 'En las computadoras de renta nadie instala nada. Si un cliente necesita un programa, lo pide y Don Beto decide.')),
    'Oficial, legal y solo lo necesario.')
c.A('📦', '¿Se permite o no?', 'Aplica la política de software de la papelería.', [
    ['Descargar 7-Zip desde 7-zip.org', 'Se permite', 'Es el sitio oficial y el programa es gratuito y legal.'],
    ['Instalar un Office «crackeado» que pasó un amigo', 'No se permite', 'No tiene licencia y puede traer virus escondidos.'],
    ['Un cliente instala un juego en la computadora de renta', 'No se permite', 'Los clientes usan cuenta estándar y no instalan nada.'],
    ['Desinstalar una barra de herramientas que nadie usa', 'Se permite', 'Quitar lo que no se usa reduce riesgos.'],
    ['Instalar una app de la Play Store revisando sus permisos', 'Se permite', 'Es la tienda oficial y se revisaron los permisos.'],
    ['Abrir un .exe que llegó por WhatsApp de un número desconocido', 'No se permite', 'Un ejecutable de origen desconocido puede ser un virus.'],
], 'Pregunta: ¿es oficial?, ¿es legal?, ¿se necesita?, ¿quién lo instala?', ['Se permite', 'No se permite'])
c.L('🧱', 'Firewall local: el portero de tu computadora', 'Bloque B · Qué conexiones entran y salen', body(
    sp('En palabras sencillas', 'Un firewall es un <b>filtro que decide qué conexiones entran y salen</b> del equipo, según reglas. El firewall <b>local</b> vive en cada computadora: en Windows es el <b>Firewall de Windows Defender</b>.'),
    bk('Piensa en…', 'El portero de un edificio con una lista: si estás en la lista, pasas; si no, no.'),
    bk('Perfiles de red', '<b>Privada</b>: tu casa o la papelería, donde confías. <b>Pública</b>: un café o la escuela, donde se desconfía más. Debe estar activado en todos.'),
    bk('Reglas', 'De <b>entrada</b> (lo que llega al equipo) y de <b>salida</b> (lo que sale). Se pueden permitir o bloquear programas.'),
    bk('Dónde se ve', '<b>Seguridad de Windows › Firewall y protección de red</b>.'),
    warn('Nunca', 'Desactivar el firewall «para que funcione un juego». Si algo necesita pasar, se crea una regla solo para eso.')),
    'Firewall activo en todos los perfiles, y reglas solo para lo necesario.')
c.L('🛡️', 'Política de antivirus', 'Bloque B · Reglas para que el antivirus sí proteja', body(
    sp('En palabras sencillas', 'El antivirus <b>detecta, bloquea y elimina programas maliciosos</b>. La política dice cómo debe usarse para que no sea solo un ícono.'),
    bk('Dónde está', 'En Windows ya viene: <b>Seguridad de Windows › Protección antivirus y contra amenazas</b> (Microsoft Defender).'),
    bk('Reglas típicas', '1) Protección en tiempo real siempre activada. 2) Definiciones actualizadas a diario (automático). 3) Examen rápido cada semana y completo cada mes. 4) Toda memoria USB se analiza antes de abrirla. 5) Nadie lo desactiva.'),
    ana('Cuarentena', 'Cuando encuentra algo sospechoso lo pone en cuarentena: lo aísla para que no contagie, como al enfermo en la enfermería. No se restaura sin revisar.'),
    ex('Don Beto', 'En las computadoras de renta los clientes conectan muchas USB: el análisis automático de USB es obligatorio.')),
    'Tiempo real activo, definiciones al día y USB analizada.')
c.L('🕵️', 'Spyware y antispyware', 'Bloque B · El programa espía', body(
    sp('En palabras sencillas', 'El <b>spyware</b> es un programa espía que se esconde y <b>roba lo que haces</b>: contraseñas, páginas visitadas o lo que tecleas (keylogger). El <b>antispyware</b> lo detecta; en Windows viene dentro de Microsoft Defender.'),
    bk('Señales', 'Anuncios raros, el navegador abre una página de inicio que no elegiste, extensiones que nadie instaló, la computadora lenta sin razón.'),
    bk('Política antispyware', '1) No instalar extensiones desconocidas. 2) Revisar las extensiones del navegador cada mes. 3) Examen completo si hay señales. 4) En el celular, revisar qué apps usan micrófono, cámara y ubicación.'),
    ex('Riesgo en la papelería', 'Un cliente entra a su correo en una computadora de renta con un keylogger: le roban la contraseña. Por eso se cierran las sesiones y se revisan los equipos.')),
    'El spyware no se nota: hay que buscarlo con reglas.')
c.Z('🛡️', 'Arma la política del antivirus', 'Elige la palabra correcta para completar la política de Don Beto.',
    '<p><b>Objetivo:</b> detectar y eliminar {0} antes de que dañen los equipos.</p>'
    '<p><b>Alcance:</b> las {1} computadoras de la papelería.</p>'
    '<p><b>Responsable:</b> {2}.</p>'
    '<p><b>Reglas:</b> la protección en tiempo real estará siempre {3}; las definiciones se actualizan {4}; toda memoria USB se {5} antes de abrirla; lo detectado se manda a {6}.</p>',
    [['programas maliciosos', ['programas maliciosos', 'clientes', 'impresoras']],
     ['5', ['5', '2', '20']],
     ['Don Beto', ['Don Beto', 'cada cliente', 'nadie']],
     ['activada', ['activada', 'apagada', 'en pausa']],
     ['a diario', ['a diario', 'cada año', 'nunca']],
     ['analiza', ['analiza', 'formatea', 'presta']],
     ['cuarentena', ['cuarentena', 'la papelera', 'un correo']]],
    'Recuerda las 4 partes de una política: objetivo, alcance, responsable y reglas.')
c.A('🚨', '¿Qué haces?', 'Elige la acción correcta en cada situación.', [
    ['Un cliente conecta su memoria USB', 'Analizarla con el antivirus antes de abrirla', 'Las USB son una de las formas más comunes de contagio.'],
    ['El antivirus manda un archivo a cuarentena', 'Dejarlo ahí y avisar al responsable', 'No se restaura sin revisar: puede ser peligroso.'],
    ['Aparece una extensión del navegador que nadie instaló', 'Quitarla y hacer un examen completo', 'Puede ser spyware: se elimina y se revisa todo el equipo.'],
    ['El antivirus avisa que sus definiciones están desactualizadas', 'Buscar actualizaciones de protección', 'Sin definiciones nuevas no reconoce las amenazas recientes.'],
    ['Un juego pide desactivar el antivirus para instalarse', 'No instalarlo', 'Un programa legal no necesita apagar tu protección.'],
], 'Piensa qué haría alguien responsable de la seguridad.',
    ['Buscar actualizaciones de protección', 'No instalarlo', 'Analizarla con el antivirus antes de abrirla', 'Quitarla y hacer un examen completo', 'Dejarlo ahí y avisar al responsable'])
c.L('📁', 'Permisos de archivos y carpetas', 'Bloque B · Quién puede ver, cambiar o borrar', body(
    sp('En palabras sencillas', 'Los permisos dicen <b>quién puede ver, cambiar o borrar</b> una carpeta o un archivo.'),
    bk('👁️ Lectura', 'Solo puede abrir y ver.'),
    bk('✏️ Modificar', 'Puede ver, cambiar y borrar.'),
    bk('👑 Control total', 'Todo lo anterior y además cambiar los permisos de otros.'),
    bk('Dónde se ve', 'Clic derecho en la carpeta › <b>Propiedades › Seguridad</b>.'),
    ana('Piensa en…', 'Un cuaderno de la clase: unos solo lo pueden leer, otros pueden escribir en él y el dueño decide quién lo usa.'),
    ex('Carpeta «Precios»', 'Cajera: Lectura. Ayudante que actualiza precios: Modificar. Don Beto: Control total. Clientes: sin acceso.')),
    'Privilegio mínimo también en las carpetas.')
c.A('📁', 'Asigna el permiso justo', 'Elige el permiso mínimo que necesita cada persona.', [
    ['La cajera necesita consultar la lista de precios', 'Lectura', 'Solo necesita ver; no debe cambiar precios.'],
    ['El ayudante actualiza el inventario cada día', 'Modificar', 'Necesita cambiar el archivo, pero no los permisos.'],
    ['Don Beto, dueño de la carpeta', 'Control total', 'Como responsable, decide quién entra.'],
    ['Los clientes, en la carpeta Facturas', 'Sin acceso', 'Las facturas son confidenciales: los clientes no deben verlas.'],
    ['Un empleado que solo debe ver los pedidos', 'Lectura', 'Ver no requiere cambiar nada.'],
], 'Da el permiso más bajo con el que la persona puede hacer su trabajo.', ['Sin acceso', 'Lectura', 'Modificar', 'Control total'])
c.L('🔒', 'Cifrado de archivos y carpetas', 'Bloque B · Que nadie entienda tus datos sin la clave', body(
    sp('En palabras sencillas', 'Cifrar es <b>convertir la información en un código</b> que solo se puede leer con la contraseña o la llave correcta.'),
    bk('Piensa en…', 'Un diario con candado y escrito en clave: aunque te lo roben, no lo entienden.'),
    bk('En Windows', '<b>EFS</b>: clic derecho › Propiedades › Opciones avanzadas › Cifrar contenido (Windows Pro). <b>BitLocker</b>: cifra todo el disco (Windows Pro).'),
    bk('Con 7-Zip', 'Comprime la carpeta con contraseña y método <b>AES-256</b>. Funciona en cualquier Windows.'),
    bk('En el celular', 'Android cifra el teléfono cuando tienes bloqueo de pantalla. La app <b>Files de Google</b> tiene una «Carpeta segura» con PIN.'),
    warn('Cuidado', 'Si olvidas la contraseña no hay forma de recuperar los archivos. Guárdala en un lugar seguro.'),
    ex('Don Beto', 'Su laptop con las facturas usa BitLocker. El respaldo en USB va comprimido con 7-Zip y contraseña.')),
    'Si te roban el equipo, el cifrado protege la información.')
c.A('🧰', '¿Qué herramienta resuelve el problema?', 'Elige la protección local que corresponde a cada problema.', [
    ['Llega un virus en una memoria USB', 'Antivirus', 'El antivirus detecta y elimina programas maliciosos.'],
    ['Alguien desde la red quiere conectarse a la caja', 'Firewall local', 'El firewall decide qué conexiones entran al equipo.'],
    ['Le roban la laptop con las facturas', 'Cifrado', 'Si los archivos están cifrados, el ladrón no los puede leer.'],
    ['La cajera borra por error la carpeta de precios', 'Permisos', 'Con permiso de solo lectura no la hubiera podido borrar.'],
    ['Un programa espía roba las contraseñas', 'Antispyware', 'El antispyware detecta programas espía.'],
    ['Windows tiene una falla que ya tiene parche', 'Actualizaciones', 'La actualización tapa la falla.'],
], 'Relaciona el problema con lo que lo evita.', ['Antivirus', 'Antispyware', 'Firewall local', 'Permisos', 'Cifrado', 'Actualizaciones'])
c.W('✍️', 'Redacta una regla de seguridad', 'Escribe una regla para la computadora de la caja.',
    'Escribe una regla para el <b>antivirus</b>, el <b>firewall</b> o las <b>actualizaciones</b>. Debe decir qué se hace y cada cuándo, para que se pueda comprobar.',
    [['Tiene al menos 8 palabras', 'palabras:8'],
     ['Menciona antivirus, firewall o actualizaciones', '(antivirus|firewall|cortafuegos|actualizacion|actualizaciones|definiciones|parche|parches)'],
     ['Dice cada cuándo o en qué momento (diario, cada semana, siempre, antes de…)', '(diario|diaria|diariamente|cada|semana|semanal|mes|mensual|siempre|nunca|antes de|al iniciar|todos los)'],
     ['Usa un verbo de acción (activar, analizar, instalar, revisar…)', '(activa|activar|analiza|analizar|instala|instalar|revisa|revisar|actualiza|actualizar|bloquea|bloquear|mantener|mantiene|ejecuta|ejecutar|permanecera|estara)']],
    'Qué + cada cuándo. Ejemplo: «Se hará un examen completo con el antivirus cada viernes».',
    'Ejemplo: El antivirus estará siempre activado y se analizará cada USB antes de abrirla')
b2_end = c.mark() - 1

# ───────────────────────── Bloque C · Seguridad en la red ─────────────────────────
c0 = c.mark()
c.L('🏰', 'Firewall perimetral: la reja de toda la red', 'Bloque C · Configuración de red', body(
    sp('En palabras sencillas', 'El firewall perimetral <b>protege toda la red</b> en el punto donde se conecta a internet (el «perímetro»). Puede ser el router o un equipo especial.'),
    bk('Piensa en…', 'La reja del fraccionamiento (perimetral) y la puerta de cada casa (local). Se usan los dos: si uno falla, queda el otro.'),
    bk('Reglas típicas', '1) Bloquear todo lo que entra sin que nadie lo haya pedido. 2) Permitir solo lo necesario: navegar y el sistema de cobro. 3) Separar la red de los clientes de la red de la caja.'),
    ex('Don Beto', 'Activa el firewall del router y crea un <b>wifi de invitados</b> para los clientes: navegan, pero no pueden ver la caja ni la oficina.')),
    'Local cuida un equipo; perimetral cuida a todos.')
c.L('🚨', 'Sistema de detección de intrusos (IDS)', 'Bloque C · La alarma de la red', body(
    sp('En palabras sencillas', 'Un <b>IDS</b> vigila el tráfico de la red y <b>avisa</b> cuando ve algo sospechoso. Un <b>IPS</b> hace lo mismo y además lo <b>bloquea</b>.'),
    bk('Piensa en…', 'La alarma con sensores: no cierra la puerta (eso lo hace el firewall), pero suena y avisa cuando alguien entra.'),
    bk('Cómo detecta', '<b>Por firmas</b>: compara con ataques conocidos, como la ficha de un ladrón buscado. <b>Por anomalías</b>: nota lo que no es normal, como la caja enviando datos a las 3 de la mañana.'),
    bk('Ejemplos', 'Snort y Suricata son IDS gratuitos muy usados. Algunos routers y firewalls ya traen uno.'),
    ex('En la papelería', 'El IDS avisa a Don Beto cuando alguien prueba cientos de contraseñas contra el wifi.')),
    'Firewall = reja · IDS = alarma · IPS = guardia que detiene.')
c.A('🧱', '¿Firewall, IDS o IPS?', 'Elige la herramienta que corresponde a cada descripción.', [
    ['Bloquea las conexiones que no están en sus reglas', 'Firewall', 'El firewall filtra según reglas.'],
    ['Avisa que alguien está revisando qué equipos hay en la red', 'IDS', 'Detecta y avisa, pero no bloquea.'],
    ['Detecta un ataque conocido y lo corta en ese momento', 'IPS', 'El IPS detecta y además bloquea.'],
    ['Funciona como la alarma con sensores', 'IDS', 'Suena, pero no cierra la puerta.'],
    ['Funciona como la reja con lista de quién pasa', 'Firewall', 'Deja pasar solo lo permitido.'],
    ['Es como un guardia que ve al ladrón y lo detiene', 'IPS', 'Ve el ataque y lo frena.'],
], 'Filtra con reglas → firewall · Solo avisa → IDS · Avisa y bloquea → IPS.', ['Firewall', 'IDS', 'IPS'])
c.L('🔐', 'HTTPS: el candado del navegador', 'Bloque C · Protocolos de seguridad', body(
    sp('En palabras sencillas', '<b>HTTPS</b> es HTTP (la forma en que viajan las páginas web) <b>sobre SSL/TLS</b>, una capa que cifra. Lo que escribes viaja en código, y un <b>certificado</b> demuestra que la página es quien dice ser.'),
    bk('Piensa en…', 'Una postal (HTTP): cualquiera que la toque la lee. Una carta en sobre sellado (HTTPS): solo la abre quien la recibe.'),
    bk('Cómo reconocerla', 'La dirección empieza con <b>https://</b> y aparece el ícono del candado o de configuración. Al darle clic dice «La conexión es segura» y puedes ver el certificado: a quién se emitió, quién lo emitió y hasta cuándo es válido.'),
    bk('Nota', 'SSL es el nombre antiguo; hoy se usa TLS, pero mucha gente sigue diciendo SSL.'),
    warn('Cuidado', 'El candado dice que la conexión está cifrada, <b>no que la página sea honesta</b>. Una página falsa también puede tener HTTPS: revisa bien la dirección.')),
    'Sin HTTPS no escribas contraseñas ni datos de tarjetas.')
c.L('🚇', 'IPsec: un túnel seguro entre redes', 'Bloque C · Protocolos de seguridad', body(
    sp('En palabras sencillas', '<b>IPsec</b> protege todos los paquetes que viajan entre dos equipos o dos redes: comprueba de quién vienen (autenticación) y los cifra. Se usa mucho en las <b>VPN</b>.'),
    bk('Piensa en…', 'Un túnel privado bajo la ciudad que une dos sucursales: lo que va dentro nadie lo ve desde la calle.'),
    ex('Don Beto', 'Abre una segunda sucursal. Con una VPN con IPsec, la caja de la sucursal consulta el inventario de la papelería principal sin dejarlo expuesto en internet.'),
    bk('HTTPS o IPsec', 'HTTPS protege <b>una página web</b> en el navegador. IPsec protege <b>toda la comunicación</b> entre dos puntos, sin importar el programa.')),
    'HTTPS = una página · IPsec = todo el camino entre dos redes.')
c.A('🔐', '¿HTTPS o IPsec?', 'Elige el protocolo que protege cada situación.', [
    ['Pagar en una tienda en línea', 'HTTPS', 'Es una página web en el navegador.'],
    ['Unir por internet la red de dos sucursales', 'IPsec', 'Protege toda la comunicación entre las dos redes.'],
    ['Ver el candado en la barra de direcciones', 'HTTPS', 'El candado indica una conexión HTTPS.'],
    ['Una VPN para trabajar desde casa con la red de la empresa', 'IPsec', 'Las VPN suelen usar IPsec para crear el túnel.'],
    ['Iniciar sesión en tu correo desde el navegador', 'HTTPS', 'El inicio de sesión en una página web va por HTTPS.'],
    ['Proteger todo el tráfico entre dos routers', 'IPsec', 'IPsec trabaja a nivel de red, entre dos equipos.'],
], 'Navegador y página → HTTPS · Redes completas o VPN → IPsec.', ['HTTPS', 'IPsec'])
c.A('🕵️', '¿Escribirías aquí tus datos?', 'Decide si es seguro escribir una contraseña o tu tarjeta en cada caso.', [
    ['http://pagos-papeleria.com (sin candado) pide tu tarjeta', 'No: no tiene HTTPS', 'Sin HTTPS los datos viajan sin cifrar.'],
    ['https://www.sat.gob.mx con candado y certificado vigente, escrito por ti', 'Sí: dirección correcta y HTTPS', 'La dirección oficial, escrita por ti, con conexión cifrada.'],
    ['https://sat-gob-mx.info con candado, llegó en un mensaje', 'No: la dirección es falsa', 'Tiene candado, pero no es la dirección oficial: es phishing.'],
    ['El navegador avisa «La conexión no es privada» por certificado vencido', 'No: el certificado no es válido', 'Si el certificado no es válido, no se puede confiar en la conexión.'],
], 'Revisa dos cosas: que tenga HTTPS y que la dirección sea la oficial.',
    ['No: no tiene HTTPS', 'No: la dirección es falsa', 'No: el certificado no es válido', 'Sí: dirección correcta y HTTPS'])
c.L('📂', 'Carpetas compartidas en red: dos candados', 'Bloque C · Permisos por la red', body(
    sp('En palabras sencillas', 'Al compartir una carpeta en la red hay <b>dos tipos de permisos</b>: los de <b>recurso compartido</b> (Lectura, Cambiar o Control total, para quien entra por la red) y los de <b>Seguridad</b> que ya viste (Lectura, Modificar, Control total).'),
    bk('Regla', 'Por la red se aplica <b>el más restrictivo de los dos</b>.'),
    bk('Piensa en…', 'Para entrar a un salón necesitas permiso en la puerta del edificio y en la del salón. Si una de las dos dice «solo mirar», solo miras.'),
    ex('Carpeta «Precios» de Don Beto', 'Compartido: Cambiar para Empleados. Seguridad: Lectura. Por la red, la cajera <b>solo puede leer</b>.'),
    warn('Nunca', 'Compartir con «Todos» y Control total. Comparte solo lo necesario, con usuarios que tengan contraseña, y deja de compartir lo que ya no se usa.')),
    'Dos candados: gana el más estricto.')
c.T('🔑', '¿Qué permiso gana?', 'Escribe el permiso que tiene el usuario cuando entra por la red. Escribe la palabra (por ejemplo: Lectura).', [
    ['Compartido: Control total · Seguridad: Lectura', 'Lectura', 'Gana Lectura porque es el más restrictivo.', 'El más estricto de los dos.'],
    ['Compartido: Lectura · Seguridad: Modificar', 'Lectura', 'El compartido solo deja leer: gana Lectura.', '¿Cuál de los dos deja hacer menos?'],
    ['Compartido: Control total · Seguridad: Control total', ['Control total'], 'Los dos dan Control total.', 'Si son iguales, ese es el resultado.'],
    ['Compartido: Cambiar · Seguridad: Modificar', ['Modificar', 'Cambiar'], 'Los dos permiten ver y cambiar: puede modificar.', 'Cambiar y Modificar significan casi lo mismo.'],
    ['Compartido: Lectura · Seguridad: sin acceso', ['Sin acceso', 'Ninguno', 'Ninguna', 'Nada', 'Denegado'], 'Si un candado no deja pasar, no hay acceso.', 'Si uno de los dos no deja entrar…'],
], 'Siempre gana el permiso que deja hacer menos.', 'u')
c.O('🧅', 'Ordena las capas de protección', 'Ordena de afuera (internet) hacia adentro (los archivos).', [
    ['Firewall perimetral en la entrada de la red', 'Es la primera barrera, entre internet y la red.'],
    ['IDS vigilando el tráfico de la red', 'Dentro de la red, vigila lo que pasó el firewall.'],
    ['Firewall local de cada computadora', 'Protege cada equipo por separado.'],
    ['Antivirus y actualizaciones del equipo', 'Protegen lo que corre dentro de la computadora.'],
    ['Permisos y cifrado de los archivos', 'La última capa protege directamente la información.'],
], 'Es como una cebolla: capa tras capa hasta llegar a la información.')
c.W('✍️', 'Diseña la red segura de Don Beto', 'Explica cómo protegerías la red de la papelería.',
    'Describe en 3 o 4 renglones cómo protegerías la red de Don Beto. Menciona el <b>firewall perimetral</b>, cómo separas a los <b>clientes</b>, si usarías un <b>IDS</b> y dónde usarías <b>HTTPS o IPsec</b>.',
    [['Tiene al menos 25 palabras', 'palabras:25'],
     ['Menciona el firewall', '(firewall|cortafuegos)'],
     ['Separa la red de los clientes (wifi de invitados o red aparte)', '(invitad|separ|aparte|otra red|red de clientes|clientes)'],
     ['Menciona IDS, IPS o detección de intrusos', '(ids|ips|intrus|deteccion|alarma)'],
     ['Menciona HTTPS, IPsec o VPN', '(https|ipsec|vpn|tls|ssl)']],
    'Recorre las capas: entrada de la red, clientes, vigilancia y comunicación.',
    'Ejemplo: Activaría el firewall del router y crearía un wifi de invitados…')
c_end = c.mark() - 1

# ───────────────────────── Glosario y guía docente ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario (1 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Requerimientos', 'Lo que necesita un equipo para que un programa funcione.'),
    bk('Procedimiento', 'Lista de pasos en orden para hacer algo.'),
    bk('Actualización (parche)', 'Corrección del fabricante para tapar fallas o mejorar un programa.'),
    bk('WSUS', 'Servidor central de Windows que reparte las actualizaciones en una red.'),
    bk('Cuenta estándar', 'Cuenta que usa programas pero no cambia la configuración.'),
    bk('Administrador', 'Cuenta que puede instalar y cambiar todo.'),
    bk('Privilegio mínimo', 'Dar a cada quien solo los permisos que necesita.'),
    bk('Bitácora (log)', 'Registro de lo que pasa en el equipo, con fecha y hora.'),
    bk('Visor de eventos', 'Programa de Windows para leer las bitácoras.')))
c.L('📖', 'Glosario (2 de 2)', 'Apoyo · Palabras que vas a usar', body(
    bk('Firewall', 'Filtro que decide qué conexiones entran y salen.'),
    bk('Spyware', 'Programa espía que roba lo que haces.'),
    bk('Cuarentena', 'Lugar donde el antivirus aísla lo sospechoso.'),
    bk('Cifrado', 'Convertir información en código que solo se lee con la clave.'),
    bk('IDS / IPS', 'Sistema que detecta intrusos (IDS) o los detecta y bloquea (IPS).'),
    bk('HTTPS', 'HTTP sobre SSL/TLS: páginas web con conexión cifrada.'),
    bk('Certificado', 'Documento digital que demuestra que una página es quien dice ser.'),
    bk('IPsec', 'Protocolo que autentica y cifra la comunicación entre dos redes o equipos.'),
    bk('VPN', 'Red privada virtual: un túnel seguro a través de internet.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma y tus horas de laboratorio', body(
    bk('Antes de empezar', 'Laboratorio de este grupo: <b>lunes 07:50-08:40</b>. Jueves (2 h) y viernes (1 h) son aula. Cada práctica tiene versión para celular, así que ninguna sesión depende del laboratorio.', 'sp'),
    bk('Bloque A · 15 al 23-oct', 'Si ya lo viste en clase, úsalo como repaso: lecciones y actividades en celular. <b>Lunes 26-oct (laboratorio): Práctica 1</b> (instalar 7-Zip con su tabla de requerimientos). Revisa antes que los alumnos puedan instalar; si no, instálalo tú y que documenten desde la verificación, o que usen la versión celular.'),
    bk('Bloque B · 26-oct al 5-nov', 'Jueves 29-oct: actualizaciones, cuentas y bitácoras. <b>Lunes 2-nov (laboratorio): Práctica 2</b>, puntos 1 a 4. Jueves 5-nov: firewall, antivirus, permisos y cifrado, y Práctica 2 puntos 5 a 9 (en celular o de tarea).'),
    bk('Bloque C · 6 al 13-nov', 'Viernes 6 y jueves 12: lecciones de red y actividades. <b>Lunes 9-nov (laboratorio): Práctica 3</b>. Viernes 13: armar el manual con las capturas de las tres prácticas.'),
    bk('Evaluación · jueves 19-nov', 'Entrega del manual de instalación y configuración (30%). La evaluación se desbloquea al terminar actividades y prácticas. El lunes 16-nov es inhábil.'),
    bk('Si el laboratorio tiene restricciones', 'Si Windows Update, las cuentas o el firewall dicen «Algunas opciones las administra tu organización», pide que lo capturen: es un ejemplo real de servidor central y de políticas aplicadas.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🏠', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '📘', 'a': a0, 'b': a_end},
    {'id': 'b1', 't': 'B1', 's': '', 'ic': '🔄', 'a': b10, 'b': b1_end},
    {'id': 'b2', 't': 'B2', 's': '', 'ic': '🛡️', 'a': b20, 'b': b2_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '🌐', 'a': c0, 'b': c_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b1', 'b2', 'c']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🏠",t:"Empieza aquí",d:"Del plan de seguridad a las herramientas instaladas.",time:"30 min",obj:["Explicar la diferencia entre instalar y configurar","Distinguir la seguridad de cada computadora de la seguridad de la red","Conocer la evidencia que vas a entregar"],sum:["Instalar = agregar un programa · Configurar = ajustarlo.","Bloque B cuida cada computadora; Bloque C cuida la red.","Tu evidencia es un manual de instalación y configuración."],q:"¿Qué programa de tu celular instalaste y luego tuviste que configurar? ¿Qué ajustaste?"},
a:{k:"Bloque A",l:"A",ic:"📘",t:"El manual de instalación",d:"Requerimientos, procedimiento de instalación y de configuración.",time:"90 min",obj:["Revisar si un equipo cumple los requerimientos de un programa","Escribir pasos de instalación claros","Reconocer las partes de un manual"],sum:["Requerimientos = lo que el equipo necesita; se revisan antes.","Un buen paso: verbo + una acción + lo que aparece, con captura.","Manual: portada, objetivo, requerimientos, instalación, configuración, verificación y problemas comunes."],q:"Si le dieras tu manual a alguien que nunca ha instalado nada, ¿podría seguirlo solo?"},
b1:{k:"Bloque B · Parte 1",l:"B1",ic:"🔄",t:"Actualizaciones, cuentas y bitácoras",d:"Mantener el equipo al día y saber quién entra y qué pasa.",time:"100 min",obj:["Configurar actualizaciones automáticas y clasificarlas","Asignar cuentas con el privilegio mínimo","Leer una bitácora en el Visor de eventos"],sum:["Las actualizaciones de seguridad van primero; un servidor central (WSUS) las reparte en redes grandes.","Una cuenta por persona: administrador solo quien instala.","La bitácora registra con fecha y hora: Aplicación, Seguridad y Sistema."],q:"¿Qué tipo de cuenta tienes en la computadora del laboratorio? ¿Por qué crees que la escuela lo decidió así?",rev:[["En un manual, «Windows 11 de 64 bits y 4 GB de RAM» va en…",["Requerimientos","Verificación","Objetivo"],0,"Describe lo que necesita el equipo: requerimientos."],["Un buen paso de instalación empieza con…",["Un verbo","Una disculpa","El nombre del alumno"],0,"Verbo + una acción + lo que debe aparecer."]]},
b2:{k:"Bloque B · Parte 2",l:"B2",ic:"🛡️",t:"Firewall, antivirus, permisos y cifrado",d:"Las protecciones que viven dentro de cada computadora.",time:"120 min",obj:["Aplicar una política de software","Explicar qué hacen el firewall local, el antivirus y el antispyware","Asignar permisos y cifrar archivos"],sum:["Software oficial, legal y solo el necesario.","Firewall activo en todos los perfiles; antivirus con tiempo real y definiciones al día.","Permisos con privilegio mínimo; cifrado para que un robo no exponga los datos."],q:"Si te robaran el celular hoy, ¿qué protege tu información y qué no?",rev:[["Las actualizaciones que tapan fallas que un atacante puede usar son…",["De seguridad","Opcionales","De características"],0,"Las de seguridad se instalan cuanto antes."],["El registro del Visor de eventos donde ves inicios de sesión fallidos es…",["Seguridad","Aplicación","Sistema"],0,"Los inicios de sesión quedan en Seguridad."]]},
c:{k:"Bloque C",l:"C",ic:"🌐",t:"Seguridad en la red",d:"Firewall perimetral, IDS, HTTPS, IPsec y carpetas compartidas.",time:"120 min",obj:["Diferenciar firewall local, perimetral, IDS e IPS","Reconocer cuándo se usa HTTPS y cuándo IPsec","Calcular el permiso efectivo de una carpeta compartida"],sum:["Firewall perimetral = reja de toda la red; IDS = alarma; IPS = guardia que detiene.","HTTPS protege páginas web; IPsec protege todo el camino entre dos redes (VPN).","En carpetas compartidas gana el permiso más restrictivo."],q:"¿Qué páginas usas a diario? ¿Todas tienen HTTPS?",rev:[["El firewall local protege…",["Solo a esa computadora","A toda la red","A internet"],0,"El local vive en cada equipo; el perimetral cuida a todos."],["Si la cajera solo debe ver los precios, su permiso es…",["Lectura","Control total","Modificar"],0,"Privilegio mínimo: solo lectura."]]}
'''

ILL = r'''
ILL["Del plan a la acción"]=function(){return flow([["📜","Plan"],["💿","Instalar"],["⚙️","Configurar"],["✅","Verificar"],["📘","Docu-|mentar"]],"Del plan al manual")};
ILL["Tu ruta en este R.A."]=function(){return grid3([["📘","A · Manual"],["💻","B · Cada|equipo"],["🌐","C · La red"]],"Tres bloques del R.A.")};
ILL["¿Qué es un manual de instalación?"]=function(){return flow([["📋","Requeri-|mientos"],["💿","Instalación"],["⚙️","Configu-|ración"],["✅","Verificación"]],"Partes principales del manual")};
ILL["Requerimientos: ¿lo puedo instalar?"]=function(){var r=[["Windows 64 bits","Windows 11 · 64 bits"],["4 GB de RAM","8 GB"],["2 GB en disco","120 GB libres"]],o=R_(10,4,320,24,"b",6)+T_(90,21,"Pide el programa","tw")+T_(250,21,"Tiene la caja","tw");r.forEach(function(x,i){var y=36+i*34;o+=R_(10,y,320,28,"s",6)+T_(90,y+18,x[0])+T_(250,y+18,x[1])+E_(318,y+20,"✅",14)});return SV(340,140,o,"Tabla de requerimientos que cumple")};
ILL["El procedimiento de instalación"]=function(){var s=["Descargar","Abrir","Permitir","Instalar","Verificar"],o='';s.forEach(function(x,i){var X=8+i*66;o+=C_(X+26,40,18,i==4?"g":"b")+T_(X+26,45,String(i+1),"tw")+T_(X+26,82,x);if(i<4)o+=A_(X+46,40,X+70,40)});return SV(340,100,o,"Cinco pasos de instalación")};
ILL["Las partes del manual"]=function(){var bd=[["Portada","b"],["Objetivo","b"],["Requerimientos","g"],["Instalación","a"],["Configuración","a"],["Verificación","g"],["Problemas comunes","r"]],o=R_(85,4,170,170,"w",6);bd.forEach(function(b,i){o+=R_(95,12+i*23,150,19,b[1],4)+T_(170,25+i*23,b[0],b[1]=="a"?"td":"tw")});return SV(340,180,o,"Las siete partes del manual")};
ILL["Actualizaciones: parches para los hoyos"]=function(){return flow([["🕳️","Falla|descubierta"],["🧑‍💻","Fabricante|crea parche"],["🔄","Se|instala"],["🛡️","Hoyo|cerrado"]],"Ciclo de una actualización")};
ILL["Clasificación de actualizaciones"]=function(){return grid3([["🔴","Seguridad"],["🛡️","Definiciones"],["🔌","Drivers"],["✨","Caracte-|rísticas"],["➕","Opcionales"]],"Tipos de actualización")};
ILL["Servidores centrales de actualizaciones"]=function(){var o=E_(40,58,"☁️",30)+T_(40,84,"Internet","tm")+A_(64,52,112,52)+R_(116,26,80,52,"b")+T_(156,50,"Servidor|central","tw");for(var i=0;i<4;i++){var y=8+i*34;o+=A_(198,52,258,y+14)+E_(280,y+22,"💻",20)}o+=T_(300,150,"PCs de la red","tm","end");return SV(340,156,o,"Un servidor central reparte las actualizaciones")};
ILL["Cuentas de usuario: cada quien la suya"]=function(){return SV(340,130,R_(20,10,140,110,"b")+E_(90,52,"👑",30)+T_(90,82,"Administrador","tw")+T_(90,100,"Instala y cambia todo","tw")+R_(180,10,140,110,"s")+E_(250,52,"👤",30)+T_(250,82,"Estándar")+T_(250,100,"Usa, no cambia","tm"),"Cuenta de administrador y cuenta estándar")};
ILL["Bitácoras: el diario de la computadora"]=function(){var r=[["ℹ️","08:01 Inicio de sesión: Cajera"],["⚠️","10:40 Poco espacio en disco"],["❌","12:05 Cobro dejó de responder"]],o=R_(20,4,300,24,"b",6)+T_(170,21,"Visor de eventos","tw");r.forEach(function(x,i){var y=34+i*30;o+=R_(20,y,300,26,"s",4)+E_(38,y+19,x[0],15)+T_(54,y+17,x[1],"t","start")});return SV(340,128,o,"Ejemplo de bitácora")};
ILL["Manejo de software: solo lo necesario"]=function(){return grid3([["🏪","Sitio|oficial"],["📜","Con|licencia"],["✂️","Solo lo|necesario"],["📋","Inventario"],["👑","Instala el|admin"]],"Reglas para el software")};
ILL["Firewall local: el portero de tu computadora"]=function(){var o=R_(150,10,22,120,"r",3)+E_(290,78,"💻",36)+T_(290,112,"Tu computadora");o+=T_(20,40,"Programa permitido","t","start")+A_(20,50,270,50)+T_(20,100,"Conexión extraña","t","start")+'<line x1="20" y1="110" x2="146" y2="110" class="kb"/>'+E_(160,116,"⛔",18);return SV(340,140,o,"El firewall deja pasar lo permitido y bloquea lo demás")};
ILL["Política de antivirus"]=function(){return flow([["🔍","Analiza"],["🚨","Detecta"],["🧪","Cuarentena"],["🗑️","Elimina"]],"Cómo actúa el antivirus")};
ILL["Permisos de archivos y carpetas"]=function(){var u=["Don Beto","Ayudante","Cajera","Clientes"],p=[["👑","g"],["✏️","a"],["👁️","b"],["⛔","r"]],o=R_(10,4,320,24,"b",6)+T_(90,21,"Carpeta «Precios»","tw")+T_(250,21,"Permiso","tw");u.forEach(function(x,i){var y=34+i*28;o+=R_(10,y,320,24,"s",4)+T_(90,y+16,x)+E_(250,y+18,p[i][0],15)});return SV(340,150,o,"Permisos por persona")};
ILL["Cifrado de archivos y carpetas"]=function(){return flow([["📄","Factura"],["🔑","Cifrar"],["🔣","x9#Qa…"],["🔑","Descifrar"],["📄","Factura"]],"Cifrar y descifrar con la clave")};
ILL["Firewall perimetral: la reja de toda la red"]=function(){var o=E_(30,72,"☁️",30)+T_(30,98,"Internet","tm")+A_(54,66,96,66)+R_(100,30,64,72,"r")+T_(132,62,"Firewall","tw")+T_(132,78,"perimetral","tw")+A_(166,50,214,30)+A_(166,84,214,110)+R_(218,8,112,50,"s")+T_(274,28,"Caja y oficina")+T_(274,44,"💻 💻","t")+R_(218,88,112,50,"s")+T_(274,108,"Wifi invitados")+T_(274,124,"📱 📱","t");return SV(340,146,o,"Firewall perimetral con red separada para clientes")};
ILL["Sistema de detección de intrusos (IDS)"]=function(){return SV(340,120,R_(10,20,96,80,"s")+E_(58,58,"🧱",28)+T_(58,88,"Firewall: filtra")+R_(122,20,96,80,"a")+E_(170,58,"🚨",28)+T_(170,88,"IDS: avisa","td")+R_(234,20,96,80,"b")+E_(282,58,"👮",28)+T_(282,88,"IPS: detiene","tw"),"Firewall, IDS e IPS")};
ILL["HTTPS: el candado del navegador"]=function(){return SV(340,130,R_(10,14,150,100,"s")+E_(85,56,"✉️",34)+T_(85,88,"HTTP: postal")+T_(85,104,"Cualquiera la lee","tm")+R_(180,14,150,100,"b")+E_(255,56,"🔒",34)+T_(255,88,"HTTPS: sobre sellado","tw")+T_(255,104,"Viaja cifrado","tw"),"HTTP contra HTTPS")};
ILL["IPsec: un túnel seguro entre redes"]=function(){return SV(340,120,E_(40,60,"🏪",34)+T_(40,92,"Papelería")+E_(300,60,"🏬",34)+T_(300,92,"Sucursal")+R_(70,40,200,30,"b",15)+T_(170,60,"Túnel IPsec (cifrado)","tw")+T_(170,100,"Internet alrededor: no ve lo de adentro","tm"),"Túnel IPsec entre dos sucursales")};
ILL["Carpetas compartidas en red: dos candados"]=function(){return flow([["👤","Cajera|en la red"],["🚪","Compartido|Cambiar"],["🔐","Seguridad|Lectura"],["👁️","Resultado|Lectura"]],"Gana el permiso más restrictivo")};
'''

EXH = r'''
EXH.nombre_archivo=function(){return exw('<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span style="font-size:30px">📄</span><b style="font-size:17px"><span style="color:#d92d3a">Perez</span>_<span style="color:#2b5fd9">Ana</span>_<span style="color:#1e8e4e">Manual_7Zip</span>.docx</b></div>',['Apellido, nombre y tema, separados con guion bajo.','Evita nombres como «tarea final final».'])};
EXH.acerca_win=function(){return exw(mw('Configuración › Sistema › Información','<div style="line-height:1.9">Procesador: <b>Intel Core i5 · 2.10 GHz</b> '+mk(1)+'<br>RAM instalada: <b>8.00 GB</b> '+mk(2)+'<br>Tipo de sistema: <b>Sistema operativo de 64 bits</b> '+mk(3)+'<br>Edición: <b>Windows 11 Pro</b> '+mk(4)+'</div>'),['Procesador: nombre y velocidad.','RAM: cuánta memoria tiene.','Tipo de sistema: 64 bits.','Edición de Windows: Home, Pro o Education.'])};
EXH.disco_libre=function(){return exw(mw('Este equipo','<div>💽 <b>Disco local (C:)</b> '+mk(1)+'<div class="mbar" style="margin:6px 0"><i style="width:62%"></i></div><small>180 GB disponibles de 476 GB</small></div>'),['Anota los GB disponibles del disco C:.'])};
EXH.req_tabla=function(){return exw('<table class="mtb"><tr><th>Requisito</th><th>Pide el programa</th><th>Tiene mi equipo</th><th>¿Cumple?</th></tr><tr><td>Sistema</td><td>Windows 10 u 11</td><td>Windows 11 Pro</td><td>✅</td></tr><tr><td>Arquitectura</td><td>64 bits (x64)</td><td>64 bits</td><td>✅</td></tr><tr><td>Espacio</td><td>5 MB</td><td>180 GB libres</td><td>✅</td></tr><tr><td>Permisos</td><td>Administrador</td><td>Cuenta estándar</td><td>⚠️ Pedir al profe</td></tr></table>',['Una fila por requisito.','Si algo no cumple, escribe qué harás para resolverlo.'])};
EXH.sitio_7z=function(){return exw(mw('7-zip.org','<p style="margin:0 0 6px"><b>Download 7-Zip</b></p><table class="mtb"><tr><th>Link</th><th>Type</th><th>Windows</th></tr><tr><td><span class="mbtn">Download</span> '+mk(1)+'</td><td>.exe</td><td>64-bit x64</td></tr><tr><td>Download</td><td>.exe</td><td>32-bit x86</td></tr></table>'),['Descarga la fila que dice <b>64-bit x64</b>.','Revisa que la dirección sea 7-zip.org.'])};
EXH.uac=function(){return exw(mw('Control de cuentas de usuario','<p style="margin:0 0 8px">¿Quieres permitir que esta aplicación haga cambios en el dispositivo?</p><p style="margin:0 0 8px"><b>7-Zip</b> · Editor comprobado: Igor Pavlov '+mk(1)+'</p><span class="mbtn">Sí</span> '+mk(2)+' <span class="mbtn" style="background:#888">No</span>'),['Revisa que el editor sea el correcto.','Da clic en Sí. Si te pide contraseña de administrador y no la tienes, pide ayuda a tu profe.'])};
EXH.install_7z=function(){return exw(mw('7-Zip Setup','<div style="display:grid;gap:8px"><div><small>Destination folder:</small><div class="mfld">C:\\Program Files\\7-Zip '+mk(1)+'</div></div><div><span class="mbtn">Install</span> '+mk(2)+'</div><div class="mbox">7-Zip is installed. <span class="mbtn">Close</span> '+mk(3)+'</div></div>'),['Deja la carpeta que propone.','Da clic en Install.','Al terminar, Close. Toma captura de cada pantalla.'])};
EXH.menu_7z=function(){return exw(mw('Clic derecho sobre un archivo','<div class="mm"><span>Abrir</span><span class="hl">7-Zip ▸ '+mk(1)+'</span><span>Añadir al archivo…</span><span>Copiar</span><span>Propiedades</span></div>'),['Si aparece 7-Zip en el menú, la instalación funcionó.','En Windows 11 puede estar en «Mostrar más opciones».'])};
EXH.paso_bien=function(){return exw('<div class="mbox"><b>Paso 3.</b> Da clic en <b>Install</b>. Aparece una barra de avance y al final el botón Close.<br><i>[Captura 3: ventana de instalación con el botón Install marcado]</i></div>',['Número + verbo + lo que aparece.','La captura va debajo del paso, con la parte importante marcada.'])};
EXH.acerca_cel=function(){return exw(mp('Acerca del teléfono','<div class="mbox">Versión de Android<br><b>14</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">RAM<br><b>4 GB</b> '+mk(2)+'</div><div class="mbox" style="margin-top:6px">Almacenamiento<br><b>26 GB libres de 64 GB</b> '+mk(3)+'</div>'),['Ajustes › Acerca del teléfono (o Información del teléfono).','La RAM y el almacenamiento pueden estar en «Especificaciones».'])};
EXH.ficha_app=function(){return exw(mp('Play Store · Files de Google','<b>Files de Google</b><br><small>Google LLC ✔</small> '+mk(1)+'<div class="mbox" style="margin-top:8px">Acerca de esta app ›<br>Requiere Android: <b>8.0 o superior</b> '+mk(2)+'<br>Tamaño de descarga: <b>≈ 20 MB</b> '+mk(3)+'</div>'),['Revisa que el desarrollador sea el oficial (Google LLC).','En «Acerca de esta app» busca la versión de Android requerida.','Anota el tamaño aproximado.'])};
EXH.datos_app=function(){return exw(mp('Seguridad de los datos','<div class="mbox">📁 Archivos y documentos<br><small>Se usan para el funcionamiento de la app</small> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🔒 Los datos se encriptan en tránsito '+mk(2)+'</div>'),['Anota qué datos recopila la app.','Fíjate si dice que los datos viajan cifrados.'])};
EXH.permiso_app=function(){return exw(mp('Permiso','<p style="margin:0 0 8px">¿Permitir que <b>Files</b> acceda a fotos, videos y archivos?</p><div class="mbox">Permitir '+mk(1)+'</div><div class="mbox" style="margin-top:6px">No permitir</div>'),['Acepta solo los permisos que la app necesita para funcionar.','Una app de archivos sí necesita archivos; no necesitaría tu micrófono.'])};
EXH.winupdate=function(){return exw(mw('Configuración › Windows Update','<div class="mbox">✅ <b>Estás al día</b> '+mk(1)+'<br><small>Última comprobación: hoy, 07:55</small></div><div class="mm" style="margin-top:8px"><span>Pausar actualizaciones</span><span class="hl">Historial de actualizaciones '+mk(2)+'</span><span>Opciones avanzadas › Horas activas '+mk(3)+'</span></div>'),['Captura el estado.','Abre el Historial para ver qué se instaló.','En Opciones avanzadas están las Horas activas.'])};
EXH.historial=function(){return exw('<table class="mtb"><tr><th>Actualización (del historial)</th><th>Mi clasificación</th></tr><tr><td>Actualización de seguridad para Windows (KB…)</td><td>De seguridad</td></tr><tr><td>Actualización de inteligencia de seguridad para Microsoft Defender</td><td>De definiciones</td></tr><tr><td>Intel – Display – 31.0…</td><td>Controlador</td></tr></table>',['Copia el nombre de 3 actualizaciones y clasifícalas.','«Inteligencia de seguridad» son las definiciones del antivirus.'])};
EXH.horas_activas=function(){return exw(mw('Horas activas','<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><small>Hora de inicio</small><div class="mfld">8:00 '+mk(1)+'</div></div><div><small>Hora de finalización</small><div class="mfld">21:00 '+mk(2)+'</div></div></div><p style="margin:8px 0 0;font-size:13px;color:#a15c00">⚠️ Algunas opciones las administra tu organización '+mk(3)+'</p>'),['Pon el horario de trabajo (en la papelería, de 8:00 a 21:00).','Fin del horario.','Si aparece este aviso, captúralo: la escuela controla las actualizaciones desde un servidor central.'])};
EXH.cuenta_tipo=function(){return exw(mw('Configuración › Cuentas › Tu información','<div style="display:flex;gap:10px;align-items:center"><span style="font-size:34px">👤</span><div><b>Alumno Lab 03</b><br><small>Cuenta local · <b>Usuario estándar</b></small> '+mk(1)+'</div></div>'),['Debajo de tu nombre dice si eres Administrador o Usuario estándar.'])};
EXH.visor=function(){return exw(mw('Visor de eventos › Registros de Windows › Sistema','<table class="mtb"><tr><th>Nivel</th><th>Fecha y hora</th><th>Origen</th><th>Id.</th></tr><tr><td>ℹ️ Información</td><td>02/11 07:51</td><td>Kernel-General</td><td>12</td></tr><tr><td>⚠️ Advertencia '+mk(1)+'</td><td>02/11 07:52</td><td>DNS Client</td><td>1014</td></tr><tr><td>❌ Error '+mk(2)+'</td><td>01/11 18:03</td><td>Service Control Manager</td><td>7000</td></tr></table>'),['Elige una Advertencia: anota fecha, origen y lo que dice abajo en «General».','Haz lo mismo con un Error.'])};
EXH.firewall=function(){return exw(mw('Seguridad de Windows › Firewall y protección de red','<div class="mbox">🏢 Red de dominio · <b>El firewall está activado</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🏠 Red privada · <b>El firewall está activado</b></div><div class="mbox" style="margin-top:6px">☕ Red pública (activa) · <b>El firewall está activado</b> '+mk(2)+'</div>'),['Revisa que los tres perfiles digan «activado».','Anota cuál dice «(activa)»: es la red que usas ahora.'])};
EXH.antivirus=function(){return exw(mw('Protección antivirus y contra amenazas','<div class="mbox">Amenazas actuales: <b>No hay amenazas actuales</b><br><small>Último examen: hoy (examen rápido) · 312 archivos examinados</small> '+mk(1)+'</div><div style="margin-top:8px"><span class="mbtn">Examen rápido</span> '+mk(2)+'</div><div class="mbox" style="margin-top:8px">Actualizaciones de protección<br><small>Última actualización: hoy, 06:40</small> '+mk(3)+'</div>'),['Resultado del examen.','Botón para iniciar el examen rápido.','Fecha de las últimas definiciones.'])};
EXH.permisos=function(){return exw(mw('Propiedades: Practica_Permisos','<div class="mtabs2"><span>General</span><span>Compartir</span><span class="on">Seguridad '+mk(1)+'</span></div><p style="margin:8px 0 4px"><small>Nombres de grupos o usuarios:</small></p><div class="mm"><span>SYSTEM</span><span class="hl">Alumno Lab 03 '+mk(2)+'</span><span>Administradores</span></div><table class="mtb" style="margin-top:6px"><tr><th>Permisos de Alumno Lab 03</th><th>Permitir</th></tr><tr><td>Control total</td><td>✔</td></tr><tr><td>Modificar</td><td>✔</td></tr><tr><td>Lectura</td><td>✔</td></tr></table>'),['Pestaña Seguridad.','Selecciona cada usuario y anota sus permisos en una tabla.'])};
EXH.cifrado_7z=function(){return exw(mw('Añadir al archivo (7-Zip)','<div style="display:grid;gap:6px"><div><small>Formato de archivo</small><div class="mfld">7z '+mk(1)+'</div></div><div><small>Encriptación · Introduzca la contraseña</small><div class="mfld">••••••••••••</div></div><div><small>Método de encriptación</small><div class="mfld">AES-256 '+mk(2)+'</div></div><div class="mfld">☑ Encriptar nombres de fichero '+mk(3)+'</div></div>'),['Clic derecho en la carpeta › 7-Zip › Añadir al archivo… y elige formato 7z.','Escribe una contraseña de al menos 12 caracteres; el método es AES-256.','Marca la casilla para que tampoco se vean los nombres de los archivos. Luego ábrelo y comprueba que pide la contraseña.'])};
EXH.config_rec=function(){return exw('<table class="mtb"><tr><th>Punto</th><th>Configuración recomendada para la caja</th></tr><tr><td>Actualizaciones</td><td>Automáticas · horas activas 8:00-21:00</td></tr><tr><td>Cuentas</td><td>Cajera con cuenta estándar y contraseña de 10+ caracteres</td></tr><tr><td>Firewall</td><td>Activado en los 3 perfiles</td></tr><tr><td>Antivirus</td><td>Tiempo real activo · examen completo cada mes</td></tr></table>',['Una fila por cada punto de la práctica.'])};
EXH.upd_cel=function(){return exw(mp('Actualización de software','<div class="mbox">Versión de Android: <b>14</b><br>Nivel de parche de seguridad: <b>1 de octubre de 2026</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">✅ Tu sistema está actualizado '+mk(2)+'</div>'),['La fecha del parche de seguridad dice qué tan protegido está.','Si hay una actualización pendiente, anótalo (instálala con carga y wifi).'])};
EXH.play_upd=function(){return exw(mp('Play Store › Administrar apps','<div class="mbox">Actualizaciones disponibles: <b>3</b> <span class="mbtn">Actualizar todo</span> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Ajustes › Preferencias de red › Actualizar apps automáticamente: <b>Con cualquier red</b> o <b>Solo con Wi-Fi</b> '+mk(2)+'</div>'),['Actualiza las apps pendientes.','Activa la actualización automática.'])};
EXH.bloqueo_cel=function(){return exw(mp('Seguridad','<div class="mbox">🔒 Bloqueo de pantalla: <b>PIN</b> '+mk(1)+'</div><div class="mbox" style="margin-top:6px">👆 Huella digital: <b>1 huella</b></div>'),['Solo anota el tipo de bloqueo. Nunca captures ni escribas tu PIN.'])};
EXH.playprotect=function(){return exw(mp('Play Protect','<div class="mbox" style="text-align:center">🛡️<br><b>No se encontraron apps dañinas</b><br><small>Apps analizadas hace 1 minuto</small> '+mk(1)+'</div><div style="margin-top:8px;text-align:center"><span class="mbtn">Analizar</span> '+mk(2)+'</div>'),['Play Protect es el antivirus que trae Android.','Toca Analizar y captura el resultado.'])};
EXH.permisos_cel=function(){return exw(mp('Administrador de permisos','<div class="mbox">📍 Ubicación · 6 de 40 apps '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🎙️ Micrófono · 5 de 40 apps</div><div class="mbox" style="margin-top:6px">📷 Cámara · 7 de 40 apps</div>'),['Entra a Ubicación y Micrófono; revisa qué apps los usan.','Quita el permiso a una app que no lo necesite (por ejemplo, una linterna con micrófono).'])};
EXH.cifrado_cel=function(){return exw(mp('Encriptación y credenciales','<div class="mbox">🔐 Encriptar teléfono<br><b>Encriptado</b> '+mk(1)+'</div>'),['Puede estar en Ajustes › Seguridad › Más ajustes de seguridad. En Android 10 o superior suele venir cifrado si tienes bloqueo de pantalla.'])};
EXH.carpeta_segura=function(){return exw(mp('Files › Colecciones','<div class="mbox">⭐ Destacados</div><div class="mbox" style="margin-top:6px">🔒 <b>Carpeta segura</b> '+mk(1)+'</div><p style="margin:8px 0 2px"><small>En un archivo › ⋮ › Mover a Carpeta segura</small> '+mk(2)+'</p>'),['Abre Carpeta segura y crea un PIN o patrón.','Mueve una foto de prueba (no una personal) y comprueba que pide el PIN.'])};
EXH.panel_priv=function(){return exw(mp('Panel de privacidad','<p style="margin:0 0 6px"><small>Últimas 24 horas</small></p><div class="mbox">📍 Ubicación · usada por Maps, Clima '+mk(1)+'</div><div class="mbox" style="margin-top:6px">🎙️ Micrófono · usado por WhatsApp</div>'),['Ajustes › Seguridad y privacidad › Panel de privacidad.','Es una bitácora: qué app usó cada permiso y cuándo.'])};
EXH.barra_https=function(){return exw('<div style="display:grid;gap:8px"><div class="mfld">🔒 <b>https://</b>www.sat.gob.mx '+mk(1)+'</div><div class="mfld" style="background:#fdecee">⚠️ No seguro | <b>http://</b>neverssl.com '+mk(2)+'</div></div>',['Con HTTPS aparece el candado o el ícono de configuración.','Sin HTTPS el navegador dice «No seguro».'])};
EXH.certificado=function(){return exw(mw('Visor de certificados','<div style="line-height:1.9">Emitido para: <b>www.sat.gob.mx</b> '+mk(1)+'<br>Emitido por: <b>(autoridad certificadora)</b> '+mk(2)+'<br>Válido desde: 03/02/2026 · Válido hasta: <b>03/02/2027</b> '+mk(3)+'</div>'),['¿A quién se emitió? Debe coincidir con la página.','¿Quién lo emitió? Es la autoridad que lo garantiza.','Vigencia: si ya venció, el navegador avisa.'])};
EXH.apps_fw=function(){return exw(mw('Permitir a las aplicaciones comunicarse a través del Firewall','<table class="mtb"><tr><th>Nombre</th><th>Privada</th><th>Pública</th></tr><tr><td>Microsoft Edge '+mk(1)+'</td><td>✔</td><td>✔</td></tr><tr><td>Microsoft Teams</td><td>✔</td><td>✔</td></tr><tr><td>Uso compartido de archivos e impresoras</td><td>✔</td><td></td></tr></table>'),['Seguridad de Windows › Firewall y protección de red › Permitir una aplicación a través del firewall.','Anota 3 apps y en qué perfil están permitidas.'])};
EXH.diagrama_red=function(){var f=(typeof ILL!="undefined"&&ILL["Firewall perimetral: la reja de toda la red"])?ILL["Firewall perimetral: la reja de toda la red"]():"";return exw(f,['Dibuja: internet, el router con firewall, la red de la caja y oficina, y el wifi de invitados.','Agrega dónde pondrías el IDS (después del firewall, vigilando la red).','Puedes hacerlo con formas en Word, en draw.io o a mano.'])};
EXH.tabla_compartidos=function(){return exw('<table class="mtb"><tr><th>Carpeta</th><th>Usuario</th><th>Compartido</th><th>Seguridad</th><th>Resultado por la red</th></tr><tr><td>Precios</td><td>Cajera</td><td>Cambiar</td><td>Lectura</td><td>Lectura</td></tr><tr><td>Facturas</td><td>Clientes</td><td>—</td><td>Sin acceso</td><td>Sin acceso</td></tr><tr><td>Impresiones</td><td>Clientes</td><td>Cambiar</td><td>Modificar</td><td>Modificar</td></tr></table>',['Aplica la regla: gana el más restrictivo.','Haz al menos 3 carpetas y 3 usuarios.'])};
EXH.https_ipsec_ej=function(){return exw('<p style="margin:0;font-size:14.5px">«La tienda en línea de la papelería y el portal del banco deben usar <b>HTTPS</b>. Si Don Beto abre una sucursal, uniría las dos redes con una <b>VPN con IPsec</b> para consultar el inventario.»</p>',['Tres renglones: dónde HTTPS, dónde IPsec y por qué.'])};
EXH.wifi_cel=function(){return exw(mp('Wi-Fi › Red conectada','<div class="mbox">Red: <b>Papeleria_Invitados</b><br>Seguridad: <b>WPA2-Personal</b> '+mk(1)+'</div>'),['Toca la red a la que estás conectado y anota el tipo de seguridad.','WPA2 o WPA3 cifran el wifi; «Abierta» no protege nada.'])};
EXH.notas_cel=function(){return exw(mp('Nueva nota','<b>Manual de instalación</b><br><small>1. Requerimientos</small><br>• Android 8.0 o superior · tengo 14 ✅<br><small>2. Instalación</small><br>• Paso 1: Abre Play Store…'+mk(1)),['Usa títulos y listas. Pega tus capturas debajo de cada paso.','Si prefieres, usa Documentos de Google o Word móvil.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Instala una herramienta revisando sus requerimientos',
     'prog': 'Bloque A · Requerimientos, procedimiento de instalación y verificación',
     'min': 50, 'lug': '1 sesión de 50 min (laboratorio, lunes 26-oct) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Word (o Documentos de Google)', 'Internet', 'Herramienta Recortes (Win + Shift + S) para las capturas'],
                'steps': [
                    ['Crea un documento llamado Apellido_Nombre_Manual_7Zip.', 'nombre_archivo'],
                    ['Abre Configuración › Sistema › Información y anota procesador, RAM, tipo de sistema y edición de Windows. Toma captura.', 'acerca_win'],
                    ['Abre Este equipo y anota el espacio libre del disco C:.', 'disco_libre'],
                    ['Haz la tabla de requerimientos: lo que pide 7-Zip, lo que tiene tu equipo y si cumple.', 'req_tabla'],
                    ['Entra a 7-zip.org y descarga la versión para Windows 64-bit (x64). Toma captura.', 'sitio_7z'],
                    ['Abre el instalador. Revisa que el editor sea Igor Pavlov y da clic en Sí. Toma captura.', 'uac'],
                    ['Da clic en Install y luego en Close. Toma captura de cada pantalla.', 'install_7z'],
                    ['Verifica: clic derecho sobre un archivo, debe aparecer 7-Zip. Toma captura.', 'menu_7z'],
                    ['Debajo de cada captura escribe su paso: número, verbo y lo que aparece.', 'paso_bien'],
                    'Guarda el documento: es el inicio de tu manual.']},
         'cel': {'mat': ['Celular Android (en iPhone usa la App Store y los mismos pasos)', 'App de notas, Documentos de Google o Word móvil', 'Internet'],
                 'steps': [
                     ['Crea una nota o documento llamado Apellido_Nombre_Manual_App.', 'notas_cel'],
                     ['Abre Ajustes › Acerca del teléfono y anota versión de Android, RAM y almacenamiento libre. Toma captura.', 'acerca_cel'],
                     ['En la Play Store busca «Files de Google». En «Acerca de esta app» anota la versión de Android que pide y su tamaño.', 'ficha_app'],
                     ['Haz la tabla de requerimientos: lo que pide la app, lo que tiene tu celular y si cumple.', 'req_tabla'],
                     ['Revisa la sección «Seguridad de los datos» y anota qué datos usa la app.', 'datos_app'],
                     'Instala la app (o actualízala si ya la tienes) y toma captura.',
                     ['Ábrela y acepta solo los permisos que necesita. Toma captura.', 'permiso_app'],
                     ['Debajo de cada captura escribe su paso: número, verbo y lo que aparece.', 'paso_bien'],
                     'Guarda o comparte tu documento (PDF o enlace).']}},
     'entrega': ['Documento con tabla de requerimientos y pasos con capturas (Word, Documentos de Google o PDF).', 'Nombre completo y grupo en la primera hoja.'],
     'rub': [['Datos del equipo completos', 15], ['Tabla de requerimientos con «cumple / no cumple»', 25], ['Pasos de instalación en orden con captura', 30], ['Pasos redactados con verbo y resultado', 20], ['Verificación final', 10]]},
    {'id': 'pr2', 'n': 2, 't': 'Configuración local de seguridad',
     'prog': 'Bloque B · Actualizaciones, cuentas, bitácoras, firewall, antivirus, permisos y cifrado',
     'min': 100, 'lug': '2 sesiones: laboratorio (lunes 2-nov) + aula, casa o celular',
     'modes': {
         'pc': {'mat': ['Computadora con Windows', 'Tu documento del manual', '7-Zip instalado (Práctica 1)'],
                'steps': [
                    ['Parte 1 · Abre Configuración › Windows Update. Captura el estado y abre el Historial de actualizaciones.', 'winupdate'],
                    ['Parte 1 · Copia 3 actualizaciones del historial y clasifícalas (seguridad, definiciones, controlador o características).', 'historial'],
                    ['Parte 1 · Revisa las Horas activas. Si aparece «Algunas opciones las administra tu organización», captúralo y explica por qué.', 'horas_activas'],
                    ['Parte 1 · En Configuración › Cuentas › Tu información anota si tu cuenta es administrador o estándar.', 'cuenta_tipo'],
                    ['Parte 1 · Win + X › Visor de eventos › Registros de Windows › Sistema: anota una Advertencia y un Error (fecha, origen y descripción).', 'visor'],
                    ['Parte 2 · Seguridad de Windows › Firewall y protección de red: captura los 3 perfiles.', 'firewall'],
                    ['Parte 2 · Protección antivirus y contra amenazas: haz un examen rápido y captura el resultado y la fecha de las definiciones.', 'antivirus'],
                    ['Parte 2 · Crea la carpeta Practica_Permisos en Documentos y captura su pestaña Seguridad.', 'permisos'],
                    ['Parte 2 · Comprime la carpeta con 7-Zip, contraseña y AES-256. Comprueba que pide la contraseña al abrir.', 'cifrado_7z'],
                    ['Parte 2 · Escribe en tu manual la configuración recomendada para la caja de Don Beto en cada punto.', 'config_rec']]},
         'cel': {'mat': ['Celular', 'Tu documento del manual', 'App Files de Google (Práctica 1)'],
                 'steps': [
                     ['Parte 1 · Ajustes › Sistema › Actualización de software: captura la versión y la fecha del parche de seguridad.', 'upd_cel'],
                     ['Parte 1 · Play Store › tu perfil › Administrar apps: actualiza las apps y activa la actualización automática.', 'play_upd'],
                     ['Parte 1 · Ajustes › Seguridad: confirma qué bloqueo de pantalla tienes (sin capturar tu PIN).', 'bloqueo_cel'],
                     ['Parte 1 · Ajustes › Seguridad y privacidad › Panel de privacidad: anota qué apps usaron ubicación y micrófono (es una bitácora).', 'panel_priv'],
                     ['Parte 2 · Play Store › tu perfil › Play Protect: toca Analizar y captura el resultado.', 'playprotect'],
                     ['Parte 2 · Ajustes › Privacidad › Administrador de permisos: quita un permiso que una app no necesite.', 'permisos_cel'],
                     ['Parte 2 · Busca en Ajustes si el teléfono está encriptado y captúralo.', 'cifrado_cel'],
                     ['Parte 2 · En Files › Colecciones › Carpeta segura crea un PIN y mueve un archivo de prueba.', 'carpeta_segura'],
                     ['Parte 2 · Escribe en tu manual la configuración recomendada para el celular de la cajera en cada punto.', 'config_rec']]}},
     'entrega': ['Capturas con su explicación, dentro de tu manual.', 'Tabla de configuración recomendada.'],
     'rub': [['Actualizaciones: estado, historial clasificado y horas activas', 20], ['Cuentas y bitácora (advertencia y error explicados)', 20], ['Firewall y antivirus revisados', 20], ['Permisos y cifrado comprobados', 20], ['Configuración recomendada para Don Beto', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Revisión de seguridad en la red',
     'prog': 'Bloque C · HTTPS, firewall, diseño de red y carpetas compartidas',
     'min': 50, 'lug': '1 sesión de 50 min (laboratorio, lunes 9-nov) o en tu celular',
     'modes': {
         'pc': {'mat': ['Computadora con navegador', 'Tu documento del manual', 'Word, draw.io o cuaderno para el diagrama'],
                'steps': [
                    ['Abre www.sat.gob.mx y http://neverssl.com. Captura la barra de direcciones de cada una y explica la diferencia.', 'barra_https'],
                    ['En la página con HTTPS da clic en el candado › La conexión es segura › certificado. Anota a quién se emitió, quién lo emitió y su vigencia.', 'certificado'],
                    ['Seguridad de Windows › Firewall › Permitir una aplicación a través del firewall: anota 3 apps permitidas y en qué perfil.', 'apps_fw'],
                    ['Dibuja el diagrama de red de Don Beto: internet, firewall perimetral, IDS, red de caja y oficina, y wifi de invitados.', 'diagrama_red'],
                    ['Haz la tabla de permisos de 3 carpetas compartidas con el permiso que gana por la red.', 'tabla_compartidos'],
                    ['Escribe en 3 renglones dónde usarías HTTPS y dónde IPsec.', 'https_ipsec_ej']]},
         'cel': {'mat': ['Celular con navegador', 'Tu documento del manual', 'Cuaderno para el diagrama'],
                 'steps': [
                     ['Abre www.sat.gob.mx y http://neverssl.com en el navegador. Captura la barra de cada una y explica la diferencia.', 'barra_https'],
                     ['Toca el ícono junto a la dirección › La conexión es segura. Anota lo que muestre del certificado.', 'certificado'],
                     ['Ajustes › Wi-Fi › toca tu red: anota el tipo de seguridad (WPA2, WPA3 o abierta).', 'wifi_cel'],
                     ['Dibuja en tu cuaderno el diagrama de red de Don Beto y tómale foto.', 'diagrama_red'],
                     ['Haz la tabla de permisos de 3 carpetas compartidas con el permiso que gana por la red.', 'tabla_compartidos'],
                     ['Escribe en 3 renglones dónde usarías HTTPS y dónde IPsec.', 'https_ipsec_ej']]}},
     'entrega': ['Capturas, diagrama y tablas dentro de tu manual.'],
     'rub': [['HTTPS y certificado analizados', 25], ['Firewall o seguridad del wifi revisados', 15], ['Diagrama de red con todas sus partes', 25], ['Tabla de permisos compartidos correcta', 20], ['Uso de HTTPS e IPsec explicado', 15]]},
]

EVALUATION = {
    'course': 'ASIN-20 · Aplicación de la seguridad informática · Unidad 2',
    'ra': 'R.A. 2.1', 'title': 'Manual de instalación y configuración',
    'data': [
        ('Resultado de aprendizaje', 'Instala y configura herramientas informáticas acorde con los estándares y buenas prácticas de seguridad en cómputo.'),
        ('Actividad de evaluación', '2.1.1 Instala y configura herramientas informáticas de manera segura y en apego al manual determinado.'),
        ('Evidencia', 'Manual de instalación y configuración de software'),
        ('Ponderación', '30% (según el programa)'),
        ('Entrega', 'Jueves 19 de noviembre'),
    ],
    'situation': 'Don Beto quiere que cualquiera de sus empleados pueda dejar segura una computadora nueva sin depender de un técnico. Elabora el <b>manual de instalación y configuración</b> de una herramienta (7-Zip en computadora o Files de Google en celular) y de la <b>configuración de seguridad</b> del equipo y de la red. Usa las capturas y tablas de tus tres prácticas.',
    'hint': 'Ya tienes casi todo en tus prácticas: ordénalo en las secciones del manual y revisa que cada paso tenga verbo, resultado y captura.',
    'steps': [
        ('Inicio', [
            'Portada: nombre del manual, herramienta, tu nombre completo, grupo y fecha.',
            'Objetivo del manual en 1 o 2 líneas (para qué sirve y para quién).']),
        ('Requerimientos e instalación', [
            'Tabla de <b>requerimientos</b>: lo que pide la herramienta, lo que tiene el equipo y si cumple.',
            '<b>Procedimiento de instalación</b>: pasos numerados con verbo, resultado y captura.']),
        ('Configuración local (Bloque B)', [
            'Actualizaciones: estado, clasificación de 3 actualizaciones y horas activas (o la política de tu organización).',
            'Cuentas y bitácora: tipo de cuenta y una advertencia o error explicado.',
            'Firewall, antivirus y antispyware: capturas y la regla que propones para cada uno.',
            'Permisos y cifrado: tabla de permisos y comprobación de la carpeta cifrada.']),
        ('Configuración de red (Bloque C)', [
            'Diagrama de red con firewall perimetral, IDS y red de invitados.',
            'HTTPS (certificado revisado) e IPsec: dónde usarías cada uno.',
            'Tabla de permisos de carpetas compartidas con el permiso que gana.']),
        ('Cierre', [
            '<b>Verificación</b>: cómo compruebas que la herramienta y la configuración funcionan.',
            '<b>Problemas comunes</b>: al menos 2 errores posibles y su solución.']),
    ],
    'rubric': [
        ('Portada y objetivo', 5), ('Requerimientos en tabla con «cumple / no cumple»', 15),
        ('Procedimiento de instalación claro, en orden y con capturas', 20),
        ('Configuración local: actualizaciones, cuentas, bitácora, firewall, antivirus, permisos y cifrado', 30),
        ('Configuración de red: diagrama, HTTPS/IPsec y carpetas compartidas', 15),
        ('Verificación y problemas comunes', 10), ('Redacción y presentación', 5),
    ],
    'deliver': ['Un solo archivo PDF o Word con todas las secciones.', 'Nombre del archivo: Apellido_Nombre_Manual_ASIN21.', 'Súbelo en la actividad R.A. 2.1 de la plataforma.'],
}
