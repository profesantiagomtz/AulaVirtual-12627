"""MSII-05 · R.A. 2.2 · Opera el sistema operativo multiusuario (Linux).

Caso del módulo: el Cibercafé Nova (R.A. 1.2 y 2.1) abre una sucursal con equipos Linux; el alumno es su administrador.
Incluye cuatro terminales bash simuladas definidas en bash_sim.js.
"""
from pathlib import Path

from cw import Course, sp, ex, ana, bk, warn, r3, px, body, j

CODE = 'MSII-RA-2.2'
CODE_PREFIX = 'MSII22'
FILE = 'msii-ra22-material.html'
TITLE_TAG = 'MSII-05 · R.A. 2.2 · Sistema operativo multiusuario'
BRAND = 'MSII-05 · Sistemas operativos'
BRAND_SUB = 'R.A. 2.2 · Opera el sistema operativo multiusuario'
HERO_KICK = 'MSII-05 · R.A. 2.2'
HERO_TITLE = 'Administra Linux: usuarios, permisos, discos y procesos'
HERO_TEXT = 'La sucursal del Cibercafé Nova usa Linux y tú eres su administrador. Aprende a manejarlo con la terminal, paso a paso y sin miedo a equivocarte.'
EV_SHORT = 'haz tu sesión práctica en Linux y tu listado de comandos.'
EV_CARD = 'Sesión práctica Linux'
RA = 'R.A. 2.2'
GROUP = '310'

TABS = {'d': ['Diagnostica', 'Comandos y terminal simulada'], 'c': ['Construye', 'Prácticas en Linux']}

EXTRA_JS = (Path(__file__).parent / 'bash_sim.js').read_text(encoding='utf8')
ENGINE_PATCHES = [
    ('function initW(d){\n', 'function initW(d){\n if(d.querySelector(".lxsim"))lxInit(d);\n'),
    ('function checkPage(d,att){\n', 'function checkPage(d,att){\n if(d.querySelector(".lxsim"))return lxCheck(d);\n'),
]

c = Course()


def sim(ic, t, inf, cid, intro, tasks, hint, setup=''):
    """tasks: [texto, expresión JS con la api a (a.has, a.isDir, a.text, a.mode, a.owner, a.used, a.user, a.pw,
    a.inGroup, a.group, a.proc, a.cron, a.pkg, a.disk, a.env, a.cwd, a.me, a.hist)]."""
    ts = '[' + ','.join(f'[{j(text)},function(a){{return {cond}}}]' for text, cond in tasks) + ']'
    st = f',setup:[function(s){{{setup}}}]' if setup else ''
    cfg = f'{{id:{j(cid)},intro:{j(intro)},hint:{j(hint)},tasks:{ts}{st}}}'
    return c.raw(f'pLx({j(ic)},{j(t)},{j(inf)},{cfg})')


H = '/home/alumno'

# ───────────────────────── Empieza aquí ─────────────────────────
s0 = c.mark()
c.L('🐧', 'La sucursal del Nova usa Linux', 'De qué trata este R.A.', body(
    sp('En palabras sencillas', 'Un sistema <b>multiusuario</b> deja que <b>varias personas</b> usen la misma computadora (o el mismo servidor), cada una con su cuenta, sus archivos y sus permisos, sin estorbarse. Linux es multiusuario desde su origen.'),
    ex('Caso del R.A.: sucursal del Cibercafé Nova', 'Para ahorrar en licencias, la sucursal instaló <b>Ubuntu Linux</b>. Tú eres el <b>administrador</b>: creas las cuentas de los empleados, cuidas que nadie vea lo que no debe, preparas los discos, instalas programas y vigilas que el equipo no se trabe.'),
    r3([('🗂️', 'A · Linux', 'Archivos, terminal, escritorios, procesos y tareas.'), ('💽', 'B · Discos', 'Particiones, formato, montaje y fstab.'), ('👥', 'C · Administrar', 'Usuarios, permisos, programas, impresoras.'), ('⚙️', 'D · Procesos y memoria', 'Estados, prioridad y memoria.')]),
    bk('Sin miedo', 'Practicas en <b>terminales simuladas</b>: si borras algo o te equivocas, reinicias y listo. Nada toca tu computadora.')),
    'Multiusuario = varias cuentas, cada una con sus archivos y permisos.')
c.L('🗺️', 'Tu ruta y tu evidencia', 'Lo que vas a entregar', body(
    bk('Evidencias (35%)', 'El <b>reporte de una sesión práctica</b> en Linux y el <b>listado de los comandos</b> que usaste con lo que hizo cada uno.'),
    bk('Cómo se arma', 'Cada simulador y cada práctica te dejan comandos y capturas. Con el comando <b>history</b> ves todo lo que escribiste: cópialo a tu listado.'),
    bk('¿Sin Linux en casa?', 'No pasa nada: las prácticas tienen versión en los simuladores, en una máquina virtual del laboratorio o en el celular con la app <b>Termux</b> (Android).', 'sp')),
    'Anota cada comando que aprendas: tu listado se arma solo.')
c.A('👥', '¿Monousuario o multiusuario?', 'Decide qué tipo de uso describe cada caso.', [
    ['Un servidor de la escuela donde 300 alumnos entran con su propia cuenta', 'Multiusuario', 'Muchas cuentas a la vez, cada una con sus permisos.'],
    ['Tu celular, que solo usas tú', 'Monousuario', 'Una sola persona lo usa.'],
    ['La computadora de la sucursal, donde cada empleado tiene su cuenta y su carpeta', 'Multiusuario', 'Varias cuentas separadas en el mismo equipo.'],
    ['Una calculadora científica', 'Monousuario', 'No tiene cuentas de usuario.'],
    ['Un servidor web que atiende a miles de personas al mismo tiempo', 'Multiusuario', 'Reparte sus recursos entre muchos usuarios.'],
], 'Pregúntate: ¿hay varias cuentas con permisos distintos?', ['Multiusuario', 'Monousuario'])
s0_end = c.mark() - 1

# ───────────────────────── A · Operación de Linux ─────────────────────────
a0 = c.mark()
c.L('🐧', '¿Qué es Linux?', 'Bloque A · Introducción al sistema operativo Linux', body(
    bk('Origen', 'En 1991 <b>Linus Torvalds</b> creó el <b>kernel</b> (núcleo) Linux. Junto con las herramientas del proyecto <b>GNU</b> forma un sistema operativo completo: GNU/Linux.'),
    bk('Software libre', 'Se puede usar, estudiar, modificar y compartir. La mayoría de las distribuciones son <b>gratuitas</b>.'),
    bk('Distribuciones', 'Paquetes listos de Linux: <b>Ubuntu</b> y <b>Linux Mint</b> (fáciles para empezar), <b>Debian</b>, <b>Fedora</b>, <b>Arch</b>. Android también usa el kernel Linux.'),
    bk('¿Dónde está?', 'En casi todos los servidores de internet, en supercomputadoras, routers, televisores inteligentes y celulares Android.'),
    ana('Piensa en…', 'El kernel es el motor de un carro; la distribución es el carro completo, con asientos, volante y pintura.')),
    'Kernel = motor · Distribución = carro completo.')
c.L('🌳', 'El sistema de ficheros de Linux', 'Bloque A · Todo cuelga de la raíz /', body(
    sp('En palabras sencillas', 'Linux no tiene unidades C: o D:. Todo está en <b>un solo árbol</b> que empieza en la raíz <b>/</b>. Los discos y memorias se «cuelgan» (montan) en alguna carpeta de ese árbol.'),
    bk('/home', 'Las carpetas personales: <b>/home/alumno</b>, /home/ana… Como «Usuarios» en Windows.'),
    bk('/root', 'La carpeta personal del administrador (root).'),
    bk('/etc', 'Archivos de <b>configuración</b> del sistema (fstab, hostname, passwd).'),
    bk('/bin y /usr/bin', 'Los programas y comandos.'),
    bk('/dev', 'Los <b>dispositivos</b>: /dev/sda es el primer disco; /dev/sdb, una memoria USB.'),
    bk('/mnt y /media', 'Donde se montan discos y memorias.'),
    bk('/var/log y /tmp', 'Registros (bitácoras) del sistema y archivos temporales.'),
    warn('Ojo', 'Linux distingue <b>mayúsculas y minúsculas</b>: Notas.txt y notas.txt son dos archivos distintos. Y las rutas usan <b>/</b>, no \\ como en Windows.')),
    'Un solo árbol desde / · /home personal · /etc configuración · /dev dispositivos.')
c.L('⌨️', 'El intérprete de comandos (shell)', 'Bloque A · La terminal', body(
    bk('Shell', 'Programa que recibe tus órdenes escritas y se las pasa al sistema. En Ubuntu es <b>bash</b>. Se abre con <b>Ctrl + Alt + T</b>.'),
    bk('El indicador', '<code>alumno@lab-pc07:~$</code> = usuario @ equipo : carpeta. <b>~</b> es tu carpeta personal. <b>$</b> usuario normal, <b>#</b> administrador (root).'),
    bk('Forma de un comando', '<code>comando -opciones argumentos</code>. Ejemplo: <code>ls -l Documentos</code>.'),
    bk('Trucos', '<b>Tab</b> completa nombres; <b>↑</b> repite comandos anteriores; <b>Ctrl + C</b> detiene un comando; <b>history</b> muestra lo que escribiste.'),
    bk('Ayuda', '<code>man ls</code> (manual), <code>ls --help</code> (ayuda corta), <code>whatis ls</code> (una línea).')),
    '$ usuario normal · # root · Tab completa · man explica.')
c.L('📜', 'Principales órdenes de Linux', 'Bloque A · Los comandos de todos los días', body(
    bk('Moverse', '<code>pwd</code> dónde estoy · <code>ls</code> qué hay (<code>-l</code> detalle, <code>-a</code> ocultos) · <code>cd carpeta</code> entrar · <code>cd ..</code> subir · <code>cd ~</code> a tu carpeta.'),
    bk('Crear', '<code>mkdir carpeta</code> (<code>-p a/b</code> crea las intermedias) · <code>touch archivo</code> archivo vacío · <code>echo "texto" > archivo</code> escribir · <code>>></code> agregar.'),
    bk('Ver', '<code>cat</code> todo el archivo · <code>head</code> / <code>tail</code> inicio y final · <code>grep texto archivo</code> buscar.'),
    bk('Copiar, mover y borrar', '<code>cp</code> copiar (<code>-r</code> carpetas) · <code>mv</code> mover o renombrar · <code>rm</code> borrar (<code>-r</code> carpetas).'),
    warn('Cuidado', '<code>rm</code> no manda a la papelera: lo borrado <b>no se recupera</b>. Revisa dos veces antes de dar Enter.'),
    ex('Comparación con CMD (R.A. 2.1)', 'DIR → ls · CD → cd · MD → mkdir · COPY → cp · MOVE → mv · DEL → rm · TYPE → cat · CLS → clear.')),
    'pwd · ls · cd · mkdir · touch · cat · cp · mv · rm.')
c.L('🖥️', 'Entornos gráficos', 'Bloque A · X-Windows y escritorios', body(
    bk('X Window (X11) y Wayland', 'El sistema base que dibuja ventanas, recibe el ratón y el teclado. Sobre él trabajan los escritorios.'),
    bk('GNOME', 'El de Ubuntu: moderno, con barra de actividades. Usa más memoria.'),
    bk('KDE Plasma', 'Muy personalizable, parecido a Windows.'),
    bk('MATE y Cinnamon', 'Clásicos y ligeros. Cinnamon es el de Linux Mint; MATE va bien en equipos viejos.'),
    bk('¿Cuál uso?', 'Escribe <code>echo $XDG_CURRENT_DESKTOP</code>. En un servidor normalmente <b>no hay</b> entorno gráfico: todo es terminal.'),
    ana('Piensa en…', 'El mismo celular con diferente launcher: cambia cómo se ve, no lo que puede hacer.')),
    'X11/Wayland dibuja ventanas · GNOME, KDE, MATE y Cinnamon son escritorios.')
c.L('⚙️', 'Procesos de Linux: tipos y estados', 'Bloque A · Programas en ejecución', body(
    sp('En palabras sencillas', 'Un <b>proceso</b> es un programa que se está ejecutando. Cada uno tiene un número único: el <b>PID</b>.'),
    bk('Tipos', '<b>De primer plano</b>: los que usas en la terminal. <b>De segundo plano</b>: terminan en <code>&</code> y te dejan seguir escribiendo. <b>Demonios (daemons)</b>: servicios que corren siempre, como <code>cupsd</code> (impresión) o <code>sshd</code> (acceso remoto).'),
    bk('Estados', '<b>R</b> ejecutándose · <b>S</b> durmiendo (esperando algo) · <b>T</b> detenido (pausado) · <b>Z</b> zombie (ya terminó, pero su padre no lo ha recogido).'),
    bk('Ver procesos', '<code>ps</code> los tuyos · <code>ps aux</code> todos · <code>top</code> los que más consumen · <code>pstree</code> en árbol.'),
    bk('Terminar', '<code>kill PID</code> pide amablemente que termine (TERM). <code>kill -9 PID</code> lo fuerza (KILL). Solo puedes terminar <b>tus</b> procesos, salvo con sudo.')),
    'PID identifica · R S T Z son los estados · kill pide, kill -9 obliga.')
c.L('⏰', 'Tareas programadas con cron', 'Bloque A · Que el sistema trabaje solo', body(
    bk('cron', 'Servicio que ejecuta comandos a la hora que le digas. Cada usuario tiene su lista: su <b>crontab</b>.'),
    bk('Ver y editar', '<code>crontab -l</code> lista tus tareas · <code>crontab -e</code> las edita.'),
    bk('Los 5 campos', '<code>minuto hora día-del-mes mes día-de-la-semana comando</code>. El <b>*</b> significa «todos». Día de la semana: 0 domingo, 1 lunes… 6 sábado.'),
    ex('Ejemplos', '<code>30 7 * * 1-5 /home/alumno/respaldo.sh</code> → de lunes a viernes a las 7:30.<br><code>0 22 * * 0 apt update</code> → domingos a las 22:00.<br><code>*/15 * * * * revisar.sh</code> → cada 15 minutos.'),
    bk('En el simulador', 'Como no hay editor, agrega una tarea así: <code>(crontab -l; echo "30 7 * * 1-5 /home/alumno/respaldo.sh") | crontab -</code>')),
    'minuto hora día mes día-semana comando.')
c.A('🌳', '¿En qué carpeta está?', 'Elige la carpeta de Linux donde se encuentra cada cosa.', [
    ['Los archivos personales de la usuaria ana', '/home', 'Cada usuario tiene /home/su-nombre.'],
    ['El archivo fstab que dice qué discos se montan al arrancar', '/etc', '/etc guarda la configuración.'],
    ['La memoria USB como dispositivo (sdb)', '/dev', 'Los dispositivos están en /dev.'],
    ['Las bitácoras donde se registran errores e intentos de acceso', '/var/log', 'Los registros van en /var/log.'],
    ['El lugar donde sueles montar una memoria USB a mano', '/mnt', '/mnt o /media.'],
    ['La carpeta personal del administrador', '/root', 'root tiene su propia carpeta.'],
], 'Recuerda el árbol: / → home, root, etc, dev, var, mnt.', ['/home', '/etc', '/dev', '/var/log', '/mnt', '/root'])
c.T('⌨️', 'Escribe el comando', 'Escribe el comando de Linux (en minúsculas).', [
    ['Mostrar en qué carpeta estás', 'pwd', 'pwd = print working directory.', 'Tres letras.', 'c'],
    ['Listar con detalle (permisos, dueño, tamaño)', 'ls -l', 'La opción -l da el formato largo.', 'ls y una opción.', 'c'],
    ['Crear la carpeta clientes', 'mkdir clientes', 'mkdir = make directory.', 'Como MD en CMD.', 'c'],
    ['Ver el contenido de notas.txt', 'cat notas.txt', 'cat muestra el archivo completo.', 'Como TYPE en CMD.', 'c'],
    ['Subir a la carpeta de arriba', 'cd ..', 'Dos puntos = carpeta padre.', 'cd y dos puntos.', 'c'],
    ['Ver todos los procesos de todos los usuarios', 'ps aux', 'ps aux muestra todos con su usuario.', 'ps y tres letras.', 'c'],
], 'Repasa «Principales órdenes de Linux».')
c.A('⏱️', '¿Qué estado tiene el proceso?', 'Elige la letra de estado que verías en ps.', [
    ['Un juego que está usando el 70% del procesador ahora mismo', 'R', 'Se está ejecutando.'],
    ['El servicio de impresión esperando a que alguien mande a imprimir', 'S', 'Duerme hasta que haya trabajo.'],
    ['Un programa que pausaste con kill -STOP', 'T', 'Detenido hasta que reciba CONT.'],
    ['Una descarga que ya terminó pero aparece como <defunct>', 'Z', 'Es un zombie.'],
], 'R corre · S espera · T pausado · Z terminó sin ser recogido.', ['R', 'S', 'T', 'Z'])
c.A('⏰', '¿Cuándo se ejecuta?', 'Lee la línea de crontab y elige cuándo corre.', [
    ['30 7 * * 1-5 respaldo.sh', 'Lunes a viernes, 7:30', 'Minuto 30, hora 7, días 1 a 5.'],
    ['0 22 * * 0 actualizar.sh', 'Domingos, 22:00', 'Día de la semana 0 = domingo.'],
    ['*/15 * * * * revisar.sh', 'Cada 15 minutos', '*/15 en el campo de minutos.'],
    ['0 9 1 * * reporte.sh', 'El día 1 de cada mes, 9:00', 'Día del mes = 1.'],
], 'Orden de los campos: minuto, hora, día del mes, mes, día de la semana.',
    ['Lunes a viernes, 7:30', 'Domingos, 22:00', 'Cada 15 minutos', 'El día 1 de cada mes, 9:00'])
sim('🐧', 'Primer día en la terminal de la sucursal', 'Terminal de Linux simulada: archivos, procesos y tareas.', 'ta',
    'Eres el administrador de la sucursal. Abre tu terminal y organiza la carpeta de trabajo. Escribe <b>help</b> si no recuerdas un comando y usa <b>Tab</b> para completar nombres.',
    [['Muestra en qué carpeta estás y lista su contenido con detalle (<b>ls -l</b>).', 'a.used("pwd")&&a.used("ls -l")'],
     ['Crea la estructura <b>sucursal/clientes</b> y <b>sucursal/precios</b> en tu carpeta personal (usa mkdir -p).', 'a.isDir("' + H + '/sucursal/clientes")&&a.isDir("' + H + '/sucursal/precios")'],
     ['Crea <b>sucursal/precios/tarifas.txt</b> con el texto <b>Impresion 2 pesos</b> (usa echo y >).', '/impresi/i.test(a.text("' + H + '/sucursal/precios/tarifas.txt"))'],
     ['Copia <b>Descargas/lista.txt</b> a <b>sucursal/clientes</b>.', 'a.has("' + H + '/sucursal/clientes/lista.txt")'],
     ['Busca con <b>grep</b> la palabra <b>monitor</b> dentro de esa lista.', 'a.used("grep")'],
     ['Revisa los procesos con <b>ps aux</b>: hay uno trabado que usa 70% de CPU. Termínalo (si no obedece, fuerza con -9).', '!a.proc(function(p){return p.c=="juego-trabado"}).length'],
     ['Programa con cron un respaldo de lunes a viernes a las <b>20:00</b> que ejecute <b>/home/alumno/respaldo.sh</b> y compruébalo con <b>crontab -l</b>.', 'a.cron().some(function(l){var f=l.trim().split(/\\s+/);return f[0]=="0"&&f[1]=="20"&&f[4]=="1-5"&&/respaldo/.test(f[5])})&&a.used("crontab -l")'],
     ['Consulta el manual de un comando con <b>man</b>.', 'a.used("man")']],
    'Para cron en el simulador: (crontab -l; echo "0 20 * * 1-5 /home/alumno/respaldo.sh") | crontab -')
a_end = c.mark() - 1

# ───────────────────────── B · Sistema de archivos y discos ─────────────────────────
b0 = c.mark()
c.L('💽', 'Sistemas de archivos que soporta Linux', 'Bloque B · Cómo se guardan los datos', body(
    sp('En palabras sencillas', 'Un <b>sistema de archivos</b> es la forma de organizar los datos dentro de una partición, como el índice y los estantes de una biblioteca.'),
    bk('ext4', 'El de Linux por defecto: confiable y con <b>registro (journaling)</b> para recuperarse de apagones.'),
    bk('xfs y btrfs', 'Para servidores y discos grandes; btrfs permite instantáneas (snapshots).'),
    bk('vfat (FAT32) y exFAT', 'Para memorias USB que se usan en Windows, Mac y Linux. FAT32 no acepta archivos de más de 4 GB.'),
    bk('NTFS', 'El de Windows: Linux lo lee y escribe.'),
    bk('swap', 'Partición de intercambio: memoria extra en el disco cuando se llena la RAM.')),
    'Linux → ext4 · USB para todos → vfat/exFAT · Windows → NTFS.')
c.L('🧩', 'Particiones del disco duro', 'Bloque B · Dividir el disco', body(
    bk('Nombres', 'Discos: <b>/dev/sda</b>, <b>/dev/sdb</b>… (o /dev/nvme0n1 en discos NVMe). Particiones: <b>sda1</b>, <b>sda2</b>…'),
    bk('Tablas', '<b>MBR (dos)</b>: hasta 4 primarias, discos de hasta 2 TB. <b>GPT</b>: la moderna, muchas particiones y discos enormes.'),
    bk('Ver', '<code>lsblk</code> muestra discos, particiones y dónde están montados. <code>sudo fdisk -l</code> da el detalle. <code>blkid</code> muestra el UUID (identificador único) y el tipo.'),
    bk('Crear', '<code>sudo fdisk /dev/sdb</code> o el programa gráfico <b>GParted</b>.'),
    ex('En la sucursal', 'sda1 (238 GB, ext4) es el sistema en <b>/</b>; sda2 (2 GB) es swap; sdb1 es la memoria USB nueva.')),
    'lsblk para ver · fdisk o GParted para dividir.')
c.L('🧽', 'Formatear y asignar el sistema de archivos', 'Bloque B · mkfs', body(
    bk('Formatear', 'Dar formato = crear el sistema de archivos en una partición. <b>Borra todo</b> lo que tenía.'),
    bk('Comandos', '<code>sudo mkfs.ext4 /dev/sdb1</code> (para Linux) · <code>sudo mkfs.vfat /dev/sdb1</code> (para compartir con Windows) · también <code>mkfs -t ext4</code>.'),
    bk('Antes de formatear', '1) Revisa con <code>lsblk</code> que sea la partición correcta. 2) Debe estar <b>desmontada</b>.'),
    warn('¡Peligro!', 'Si te equivocas de letra (sda en lugar de sdb) borras el sistema. Lee dos veces el nombre del dispositivo.')),
    'lsblk → desmontar → mkfs.tipo /dev/partición.')
c.L('🔌', 'Montar y desmontar: mount y umount', 'Bloque B · Colgar el disco en el árbol', body(
    sp('En palabras sencillas', '<b>Montar</b> es conectar una partición a una carpeta del árbol para poder usarla. La carpeta se llama <b>punto de montaje</b>.'),
    bk('Montar', '<code>sudo mkdir /mnt/usb</code> (una vez) y luego <code>sudo mount /dev/sdb1 /mnt/usb</code>. Ahora lo que guardes en /mnt/usb va a la memoria.'),
    bk('Comprobar', '<code>df -h</code> muestra cuánto espacio tiene cada sistema montado; <code>lsblk</code> muestra el punto de montaje.'),
    bk('Desmontar', '<code>sudo umount /mnt/usb</code> antes de sacar la memoria (como «Quitar hardware de forma segura»). Si dice «ocupado», sal de esa carpeta con <code>cd ~</code>.'),
    ana('Piensa en…', 'Enchufar una extensión a la pared: hasta que la conectas, los aparatos no tienen luz.')),
    'mkdir punto → mount dispositivo punto → umount antes de retirar.')
c.L('📄', 'El archivo de configuración fstab', 'Bloque B · Montar al arrancar', body(
    bk('Qué es', '<b>/etc/fstab</b> es la lista de particiones que se montan solas al encender el equipo.'),
    bk('Sus 6 columnas', '<code>dispositivo  punto  tipo  opciones  dump  pass</code><br>Ejemplo: <code>/dev/sdb1 /mnt/usb ext4 defaults 0 2</code>'),
    bk('pass', '0 = no revisar · 1 = la raíz / · 2 = las demás (se revisan con fsck al arrancar).'),
    bk('UUID', 'Es mejor usar <code>UUID=…</code> (lo da blkid) que /dev/sdb1, porque las letras pueden cambiar.'),
    bk('Probar', 'Después de editar: <code>sudo mount -a</code> monta todo lo de fstab. Si marca error, corrígelo antes de reiniciar.'),
    warn('Ojo', 'Un error en fstab puede impedir que el sistema arranque. Haz una copia antes: <code>sudo cp /etc/fstab /etc/fstab.bak</code>.')),
    'fstab = qué se monta al arrancar · prueba con mount -a.')
c.L('🩺', 'Integridad del sistema de ficheros', 'Bloque B · fsck', body(
    bk('Qué revisa', 'Después de un apagón o de sacar una USB sin desmontar, el sistema de archivos puede quedar con errores.'),
    bk('fsck', '<code>sudo fsck /dev/sdb1</code> revisa y repara. La partición debe estar <b>desmontada</b>.'),
    bk('La raíz', 'La partición del sistema (/) no se revisa en uso: Linux la revisa sola al arrancar si hace falta.'),
    bk('Espacio', '<code>df -h</code> avisa cuando un disco se está llenando; arriba del 90% conviene limpiar.')),
    'Desmontar → fsck → montar otra vez.')
c.A('💽', '¿Qué comando usas?', 'Elige el comando para cada tarea con la memoria USB.', [
    ['Ver qué discos y particiones tiene el equipo', 'lsblk', 'Lista discos, particiones y montaje.'],
    ['Darle formato ext4 a la memoria', 'mkfs.ext4', 'Crea el sistema de archivos.'],
    ['Conectar la memoria a /mnt/usb', 'mount', 'Monta la partición en una carpeta.'],
    ['Saber cuánto espacio libre queda en cada disco', 'df -h', 'Muestra tamaño, usado y disponible.'],
    ['Quitar la memoria con seguridad', 'umount', 'Desmonta antes de retirar.'],
    ['Revisar la memoria después de un apagón', 'fsck', 'Revisa y repara el sistema de archivos.'],
], 'Ver → lsblk · formatear → mkfs · conectar → mount · espacio → df · retirar → umount · revisar → fsck.',
    ['lsblk', 'mkfs.ext4', 'mount', 'df -h', 'umount', 'fsck'])
c.O('🔢', 'Ordena: preparar una memoria USB nueva', 'Pon los pasos en orden.', [
    ['Identificar la partición con lsblk', 'Primero confirma que es sdb1 y no sda.'],
    ['Dar formato con sudo mkfs.ext4 /dev/sdb1', 'Crea el sistema de archivos.'],
    ['Crear el punto de montaje con sudo mkdir /mnt/usb', 'La carpeta donde se colgará.'],
    ['Montar con sudo mount /dev/sdb1 /mnt/usb', 'La conecta al árbol.'],
    ['Comprobar con df -h', 'Debe aparecer /mnt/usb.'],
    ['Desmontar con sudo umount /mnt/usb al terminar', 'Antes de retirarla.'],
], 'Identificar → formatear → carpeta → montar → comprobar → desmontar.')
c.Z('📄', 'Completa la línea de fstab', 'Elige cada campo de la línea para montar la USB en /mnt/usb al arrancar.',
    '<p><code>{0}  {1}  {2}  {3}  0  {4}</code></p>',
    [['/dev/sdb1', ['/dev/sdb1', '/mnt/usb', 'ext4']],
     ['/mnt/usb', ['/mnt/usb', '/dev/sdb1', 'defaults']],
     ['ext4', ['ext4', 'swap', '/mnt']],
     ['defaults', ['defaults', 'ext4', '2']],
     ['2', ['2', '1', '0']]],
    'dispositivo · punto de montaje · tipo · opciones · dump · pass (2 para discos que no son la raíz).')
sim('💽', 'Prepara la memoria USB de respaldos', 'Terminal de Linux simulada: discos, formato, montaje y fstab.', 'tb',
    'Llegó una memoria USB nueva para los respaldos de la sucursal. Prepárala para que se monte sola cada vez que enciendas el equipo. Recuerda que estas tareas necesitan <b>sudo</b>.',
    [['Identifica la memoria con <b>lsblk</b> (es la que no está montada).', 'a.used("lsblk")'],
     ['Dale formato <b>ext4</b> a <b>/dev/sdb1</b>.', 'a.disk.fs=="ext4"'],
     ['Crea el punto de montaje <b>/mnt/usb</b> y monta la memoria ahí.', 'a.used("mount:ok")'],
     ['Comprueba el espacio con <b>df -h</b> mientras está montada.', 'a.used("df")&&a.used("mount:ok")'],
     ['Agrega la línea a <b>/etc/fstab</b> (con echo y sudo tee -a) para que se monte al arrancar.', '/^(\\/dev\\/sdb1|UUID=\\S+)\\s+\\/mnt\\/usb\\s+ext4\\s+\\S+\\s+0\\s+2\\s*$/m.test(a.text("/etc/fstab"))'],
     ['Desmonta, revisa la integridad con <b>fsck</b> y vuelve a montar con <b>sudo mount -a</b>.', 'a.used("fsck:ok")&&a.used("mount -a")&&a.disk.mnt=="/mnt/usb"']],
    'Para fstab: echo "/dev/sdb1 /mnt/usb ext4 defaults 0 2" | sudo tee -a /etc/fstab')
b_end = c.mark() - 1

# ───────────────────────── C · Configuración y administración ─────────────────────────
c0 = c.mark()
c.L('💿', 'Instalar Linux y el arranque GRUB', 'Bloque C · Instalación del sistema operativo', body(
    bk('Preparar', 'Descarga la imagen ISO de Ubuntu, grábala en una USB con <b>Rufus</b> o <b>balenaEtcher</b> y arranca la PC desde ella (tecla F12, F9 o Esc según la marca).'),
    bk('Instalar', 'Idioma y teclado (Español-Latinoamérica) → tipo de instalación (borrar disco o junto a Windows) → zona horaria → usuario y contraseña → esperar → reiniciar y quitar la USB.'),
    bk('GRUB', 'Es el <b>administrador de arranque</b>: el menú que aparece al encender y te deja elegir Ubuntu o Windows (arranque dual). Su configuración está en <b>/etc/default/grub</b> (por ejemplo GRUB_TIMEOUT=5 segundos).'),
    bk('Actualizar GRUB', 'Después de cambiar su configuración o instalar otro sistema: <code>sudo update-grub</code>.'),
    ana('Piensa en…', 'GRUB es el recepcionista que te pregunta a qué piso vas antes de subir al elevador.')),
    'ISO en USB → instalar → GRUB elige el sistema al arrancar.')
c.L('📦', 'Instalar aplicaciones', 'Bloque C · Gestor de paquetes apt', body(
    sp('En palabras sencillas', 'En Linux los programas se instalan desde <b>repositorios</b> (tiendas oficiales y seguras) con un <b>gestor de paquetes</b>. En Ubuntu es <b>apt</b>; también está la tienda gráfica «Centro de software».'),
    bk('Actualizar la lista', '<code>sudo apt update</code> descarga la lista de programas disponibles. Hazlo primero.'),
    bk('Instalar y quitar', '<code>sudo apt install tree</code> · <code>sudo apt remove tree</code> · <code>apt search texto</code> para buscar.'),
    bk('Actualizar todo', '<code>sudo apt upgrade</code> instala las actualizaciones de seguridad de todo el sistema.'),
    bk('Otros formatos', 'Paquetes <b>.deb</b> descargados, <b>Snap</b> y <b>Flatpak</b>.'),
    warn('Seguridad', 'No instales programas de páginas desconocidas: usa los repositorios.')),
    'update → install → upgrade, siempre con sudo.')
c.L('🛡️', 'Administrador, sudo y root', 'Bloque C · Configuración y administración', body(
    bk('root', 'El superusuario: puede hacer <b>todo</b>, incluso destruir el sistema. Por eso en Ubuntu no se entra como root.'),
    bk('sudo', 'Antepones <code>sudo</code> para ejecutar <b>un</b> comando como administrador. Te pide <b>tu</b> contraseña y solo funciona si perteneces al grupo <b>sudo</b>.'),
    bk('Configurar el equipo', 'Nombre del equipo (<code>/etc/hostname</code>), red, fecha y hora, idioma: desde «Configuración» (gráfico) o con comandos.'),
    bk('Servicios', '<code>systemctl status cups</code> ve si un servicio corre; <code>sudo systemctl restart cups</code> lo reinicia.'),
    warn('Regla de oro', 'Usa sudo solo cuando haga falta y entiende el comando antes de darle Enter.')),
    'Trabaja como usuario normal y usa sudo solo para administrar.')
c.L('👥', 'Administración de usuarios y grupos', 'Bloque C · Cuentas en un sistema multiusuario', body(
    bk('Crear usuario', '<code>sudo useradd -m ana</code> (<code>-m</code> crea /home/ana) y luego <code>sudo passwd ana</code> para su contraseña. En Ubuntu también existe <code>sudo adduser ana</code>, que pregunta todo.'),
    bk('Grupos', 'Un grupo junta usuarios que comparten permisos. <code>sudo groupadd caja</code> · <code>sudo usermod -aG caja ana</code> (la <b>-a</b> es importante: sin ella se le quitan sus otros grupos).'),
    bk('Consultar', '<code>id ana</code> o <code>groups ana</code>. Los usuarios se guardan en <b>/etc/passwd</b> y los grupos en <b>/etc/group</b>.'),
    bk('Cambiar de usuario', '<code>su - ana</code> entra como ana; <code>exit</code> regresa. <code>whoami</code> dice quién eres.'),
    bk('Borrar', '<code>sudo userdel -r ana</code> (-r borra también su carpeta).'),
    ex('En la sucursal', 'Usuarios: <b>ana</b> y <b>luis</b> (cajeros) en el grupo <b>caja</b>; <b>beto</b> (técnico) en <b>soporte</b>. Cada quien con su contraseña.')),
    'useradd -m + passwd · groupadd · usermod -aG · id.')
c.L('🔐', 'Permisos de archivos y directorios', 'Bloque C · Quién puede hacer qué', body(
    bk('Leer ls -l', '<code>-rwxr-x--- 1 ana caja … ventas.txt</code>: el primer carácter dice si es archivo (-) o carpeta (d); luego tres grupos de <b>rwx</b> para <b>dueño</b>, <b>grupo</b> y <b>otros</b>.'),
    bk('r w x', '<b>r</b> leer (4) · <b>w</b> escribir (2) · <b>x</b> ejecutar o entrar a la carpeta (1).'),
    bk('Números', 'Se suman: rwx = 7, rw- = 6, r-x = 5, r-- = 4. <code>chmod 750 carpeta</code> → dueño todo, grupo leer y entrar, otros nada.'),
    bk('Letras', '<code>chmod u+x script.sh</code> agrega ejecutar al dueño · <code>chmod o-r archivo</code> quita leer a otros · <code>chmod g=rw archivo</code>.'),
    bk('Dueño y grupo', '<code>sudo chown ana:caja ventas.txt</code> cambia dueño y grupo (<code>-R</code> para toda una carpeta).'),
    ex('Carpeta compartida de caja', '<code>sudo mkdir /srv/caja</code> → <code>sudo chown root:caja /srv/caja</code> → <code>sudo chmod 770 /srv/caja</code>. Solo root y el grupo caja entran.')),
    'r=4 w=2 x=1 · dueño-grupo-otros · chmod y chown.')
c.L('🖨️', 'Impresoras, seguridad y ayuda', 'Bloque C · CUPS, mantenimiento y manuales', body(
    bk('CUPS', 'El sistema de impresión de Linux. Se administra desde el navegador en <b>http://localhost:631</b> o en Configuración › Impresoras. Comandos: <code>lpstat -p</code> impresoras · <code>lp archivo</code> imprimir · <code>lpstat -o</code> cola · <code>cancel id</code> cancelar.'),
    bk('Mantenimiento y seguridad', 'Actualiza seguido (<code>sudo apt update && sudo apt upgrade</code>), activa el cortafuegos (<code>sudo ufw enable</code>), usa contraseñas fuertes, no compartas cuentas y revisa las bitácoras (<code>/var/log</code>).'),
    bk('Ayuda del sistema', '<code>man comando</code>, <code>comando --help</code>, <code>whatis</code>, <code>apropos palabra</code> y la documentación en línea de la distribución (help.ubuntu.com).')),
    'CUPS imprime · ufw protege · man ayuda.')
c.L('💬', 'Comunicación entre usuarios y variables de entorno', 'Bloque C · Hablar y configurar la sesión', body(
    bk('¿Quién está?', '<code>who</code> y <code>w</code> muestran los usuarios conectados.'),
    bk('Mensajes', '<code>write ana</code> envía un mensaje a la terminal de ana; <code>wall "Se reinicia el servidor a las 3"</code> avisa a todos. <code>mesg n</code> bloquea mensajes.'),
    bk('Variables de entorno', 'Datos que usan los programas: <code>$HOME</code> (tu carpeta), <code>$USER</code>, <code>$PATH</code> (dónde buscar comandos), <code>$SHELL</code>, <code>$LANG</code>.'),
    bk('Usarlas', '<code>echo $HOME</code> · <code>printenv</code> todas · <code>export SUCURSAL=Centro</code> crea una para esta sesión. Para que sea permanente, se agrega al archivo <b>~/.bashrc</b>.'),
    ex('Comparación con Windows', 'Windows: %USERNAME% y SETX · Linux: $USER y export (+ .bashrc).')),
    'who · write · wall · echo $VAR · export.')
c.L('🧪', 'Emuladores y máquinas virtuales', 'Bloque C · Probar Linux sin borrar Windows', body(
    sp('En palabras sencillas', 'Una <b>máquina virtual</b> es una computadora «de mentiras» dentro de tu computadora. Ahí instalas Linux y practicas sin tocar tu sistema.'),
    bk('VirtualBox', 'Gratuito (Oracle). Creas la VM, le asignas RAM (2–4 GB), disco (25 GB) y montas la ISO de Ubuntu.'),
    bk('VMware Workstation Player', 'Gratuito para uso personal; muy estable.'),
    bk('Vagrant', 'Crea máquinas virtuales con comandos: <code>vagrant init ubuntu/jammy64</code> y <code>vagrant up</code>. Útil para tener la misma VM en todo el laboratorio.'),
    bk('Otras opciones', '<b>WSL</b> (Linux dentro de Windows 10/11) y <b>Termux</b> en Android.'),
    warn('Requisito', 'Activa la <b>virtualización</b> (VT-x o AMD-V) en el BIOS si la VM no arranca.')),
    'VM = computadora dentro de tu computadora: practica sin riesgo.')
c.A('🔐', '¿Qué permisos son?', 'Elige el número que corresponde a cada permiso.', [
    ['rwxr-x--- (dueño todo, grupo leer y entrar, otros nada)', '750', '7 = rwx, 5 = r-x, 0 = ---.'],
    ['rw-r--r-- (dueño lee y escribe, los demás solo leen)', '644', '6 = rw-, 4 = r--.'],
    ['rwxrwx--- (dueño y grupo todo, otros nada)', '770', 'Ideal para una carpeta de equipo.'],
    ['rw------- (solo el dueño lee y escribe)', '600', 'Privado para el dueño.'],
    ['rwxr-xr-x (todos leen y ejecutan; solo el dueño escribe)', '755', 'Típico de programas y carpetas públicas.'],
], 'Suma r=4, w=2, x=1 en cada grupo.', ['750', '644', '770', '600', '755'])
c.A('👥', '¿Qué comando de administración?', 'Elige el comando para cada tarea de la sucursal.', [
    ['Crear la cuenta de luis con su carpeta personal', 'sudo useradd -m luis', 'useradd -m crea /home/luis.'],
    ['Ponerle contraseña a luis', 'sudo passwd luis', 'passwd asigna la contraseña.'],
    ['Crear el grupo caja', 'sudo groupadd caja', 'groupadd crea grupos.'],
    ['Meter a luis al grupo caja sin quitarle sus otros grupos', 'sudo usermod -aG caja luis', 'La -a agrega sin quitar.'],
    ['Que la carpeta /srv/caja sea del grupo caja', 'sudo chown root:caja /srv/caja', 'chown cambia dueño:grupo.'],
    ['Instalar el programa tree', 'sudo apt install tree', 'apt instala desde los repositorios.'],
], 'Usuarios → useradd/passwd · grupos → groupadd/usermod · dueño → chown · programas → apt.',
    ['sudo useradd -m luis', 'sudo passwd luis', 'sudo groupadd caja', 'sudo usermod -aG caja luis', 'sudo chown root:caja /srv/caja', 'sudo apt install tree'])
c.A('🧭', '¿Cierto o falso?', 'Lee cada afirmación sobre administración en Linux.', [
    ['Con sudo escribes la contraseña de root', 'Falso', 'sudo pide TU contraseña, si estás en el grupo sudo.'],
    ['usermod -G caja ana (sin -a) puede quitarle a ana sus otros grupos', 'Cierto', 'Por eso se usa -aG.'],
    ['Un archivo con permisos 600 lo pueden leer los del grupo', 'Falso', '600 = solo el dueño lee y escribe.'],
    ['GRUB es el menú que deja elegir el sistema al encender', 'Cierto', 'Es el administrador de arranque.'],
    ['Antes de apt install conviene hacer apt update', 'Cierto', 'Así tienes la lista de paquetes al día.'],
    ['Una máquina virtual borra el Windows de tu computadora', 'Falso', 'Corre dentro de tu sistema sin tocarlo.'],
], 'Repasa las lecciones del bloque C.', ['Cierto', 'Falso'])
c.W('✍️', 'Explica tu decisión de permisos', 'Redacta como administrador.',
    'La carpeta <b>/srv/caja</b> guarda las ventas del día. Explica en 2 o 3 oraciones qué <b>dueño, grupo y permisos</b> le pondrías y <b>por qué</b>.',
    [['Tiene al menos 15 palabras', 'palabras:15'],
     ['Menciona el grupo (caja) o el dueño', '\\b(grupo|caja|dueno|propietario|root|chown)\\b'],
     ['Menciona permisos (números como 770 o letras rwx)', '\\b([0-7]{3}|rwx|lectura|escritura|leer|escribir|permis\\w*)\\b'],
     ['Explica por qué (para que, porque, así…)', '\\b(porque|para que|asi|ya que|evitar|solo)\\b']],
    'Piensa: ¿quién debe entrar y quién no?', 'Le pondría dueño … y grupo … con permisos … porque …')
sim('👥', 'Da de alta al personal de la sucursal', 'Terminal de Linux simulada: usuarios, grupos y permisos.', 'tc',
    'Llegaron dos cajeros y un técnico. Crea sus cuentas y una carpeta compartida solo para caja. Recuerda: administrar requiere <b>sudo</b>.',
    [['Crea los usuarios <b>ana</b> y <b>luis</b> con su carpeta personal y ponles contraseña.', 'a.user("ana")&&a.user("luis")&&a.pw("ana")&&a.pw("luis")&&a.isDir("/home/ana")&&a.isDir("/home/luis")'],
     ['Crea el grupo <b>caja</b> y agrega a ana y a luis.', 'a.inGroup("ana","caja")&&a.inGroup("luis","caja")'],
     ['Crea la carpeta <b>/srv/caja</b> (con sudo mkdir -p).', 'a.isDir("/srv/caja")'],
     ['Haz que su dueño sea <b>root</b> y su grupo <b>caja</b>.', 'a.owner("/srv/caja")=="root:caja"'],
     ['Ponle permisos <b>770</b>: root y caja todo, los demás nada.', 'a.mode("/srv/caja")=="770"'],
     ['Comprueba con <b>id ana</b> y <b>ls -l /srv</b>.', 'a.used("id")&&a.used("ls -l")'],
     ['Entra como ana (<b>su - ana</b>), escribe en /srv/caja un archivo <b>corte.txt</b> y regresa con <b>exit</b>.', 'a.has("/srv/caja/corte.txt")&&a.me=="alumno"'],
     ['Instala el programa <b>tree</b> (primero sudo apt update) y úsalo.', 'a.pkg("tree")&&a.used("tree")']],
    'Si «su - ana» falla, revisa que tenga contraseña. Si ana no puede escribir, revisa grupo y permisos.')
sim('🖨️', 'Impresora, seguridad y comunicación', 'Terminal de Linux simulada: CUPS, ufw, variables y mensajes.', 'tc2',
    'Antes de abrir la sucursal, revisa la impresora, la seguridad y deja un aviso al personal.',
    [['Revisa que el servicio de impresión esté activo (<b>systemctl status cups</b>) y las impresoras con <b>lpstat -p</b>.', 'a.used("systemctl")&&a.used("lpstat")'],
     ['Imprime <b>notas.txt</b> con <b>lp</b> y revisa la cola con <b>lpstat -o</b>.', 'a.used("lp:ok")&&a.S.used.lpstat'],
     ['Actualiza el sistema: <b>sudo apt update</b> y <b>sudo apt upgrade</b>.', 'a.S.upd&&a.used("apt:upgrade")'],
     ['Activa el cortafuegos con <b>ufw</b> y revisa su estado.', 'a.ufw'],
     ['Crea la variable <b>SUCURSAL</b> con el valor <b>Centro</b> y muéstrala con echo.', 'a.env("SUCURSAL")=="Centro"&&a.used("$SUCURSAL")'],
     ['Avisa a todos con <b>wall</b> que el equipo se reinicia a las 15:00.', 'a.used("wall")']],
    'Variables: export SUCURSAL=Centro y luego echo $SUCURSAL')
c_end = c.mark() - 1

# ───────────────────────── D · Procesos y memoria ─────────────────────────
d0 = c.mark()
c.L('🔄', 'Estados y operaciones de los procesos', 'Bloque D · Ciclo de vida de un proceso', body(
    bk('Ciclo de vida', '<b>Nuevo</b> → <b>Listo</b> (espera su turno de CPU) → <b>Ejecución</b> → <b>Bloqueado/En espera</b> (espera un dato, el disco o la red) → vuelve a Listo → <b>Terminado</b>.'),
    bk('Operaciones', 'Crear (un proceso padre crea un hijo con <i>fork</i>), suspender o pausar (<code>kill -STOP</code>), reanudar (<code>kill -CONT</code>), cambiar prioridad y terminar (<code>kill</code>).'),
    bk('Padre e hijo', 'Cada proceso tiene un padre (<code>pstree</code> lo muestra). Un <b>zombie</b> es un hijo que terminó y su padre no ha leído su resultado; un <b>huérfano</b> es un hijo cuyo padre terminó (lo adopta systemd).'),
    bk('Segundo plano', '<code>comando &</code> · <code>jobs</code> lista · <code>fg %1</code> lo trae al frente · <code>kill %1</code> lo termina.'),
    ana('Piensa en…', 'La fila de las tortillas: esperas (listo), te atienden (ejecución), vas por cambio (bloqueado), regresas a la fila.')),
    'Nuevo → Listo → Ejecución ⇄ Bloqueado → Terminado.')
c.L('🗓️', 'Planificación de procesos', 'Bloque D · ¿A quién le toca la CPU?', body(
    sp('En palabras sencillas', 'Hay cientos de procesos y pocos núcleos. El <b>planificador</b> del sistema decide quién usa la CPU y cuánto tiempo, tan rápido que parece que todo corre a la vez.'),
    bk('FCFS (FIFO)', 'El primero que llega, se atiende primero. Sencillo, pero uno largo hace esperar a todos.'),
    bk('SJF', 'El trabajo más corto primero: reduce la espera promedio.'),
    bk('Round Robin', 'Cada proceso recibe un <b>quantum</b> (porción de tiempo) por turnos. Es justo y es la base de los sistemas multiusuario.'),
    bk('Por prioridad', 'Los importantes primero. En Linux la prioridad se ajusta con el valor <b>nice</b>: de <b>-20</b> (más prioridad) a <b>19</b> (menos). <code>nice -n 10 comando</code> inicia con menos prioridad; <code>renice 10 -p PID</code> cambia uno que ya corre. Bajar el número (subir prioridad) requiere sudo.'),
    ex('En la sucursal', 'El respaldo nocturno corre con <code>nice -n 15</code> para no alentar a los clientes.')),
    'Round Robin reparte turnos · nice: -20 más prioridad, 19 menos.')
c.L('📡', 'Comunicación entre procesos', 'Bloque D · IPC', body(
    bk('Tuberías (pipes)', 'La salida de un proceso es la entrada de otro: <code>ps aux | grep firefox</code>.'),
    bk('Señales', 'Avisos cortos: TERM (termina), KILL (fuerza), STOP (pausa), CONT (continúa), HUP (recarga configuración).'),
    bk('Archivos y sockets', 'Compartir datos en archivos, o conectarse por red local o internet con <b>sockets</b> (así habla el navegador con un servidor).'),
    bk('Memoria compartida y colas de mensajes', 'Zonas de memoria o buzones que usan varios procesos; necesitan <b>sincronización</b> (semáforos) para no pisarse.')),
    'Tubería | · señales · archivos · sockets · memoria compartida.')
c.L('🧠', 'Gestión de la memoria', 'Bloque D · RAM, swap y memoria virtual', body(
    bk('Qué hace', 'El sistema reparte la RAM entre los procesos, protege la memoria de cada uno y recupera la que liberan.'),
    bk('Memoria virtual', 'Cada proceso cree tener toda la memoria para él; el sistema traduce esas direcciones «virtuales» a direcciones reales de la RAM.'),
    bk('Swap', 'Cuando la RAM se llena, lo que no se usa se pasa al disco (swap). Es mucho más lento: si se usa mucho, el equipo «se arrastra».'),
    bk('Ver', '<code>free -h</code> (total, usado, libre, disponible y swap) · <code>top</code> (%MEM de cada proceso) · <code>vmstat</code> · <code>cat /proc/meminfo</code>.'),
    warn('Ojo', 'En Linux «libre» suele verse bajo porque usa RAM sobrante como caché. Fíjate en «disponible».')),
    'free -h: mira «disponible» y el uso de swap.')
c.L('🧱', 'Paginación y segmentación', 'Bloque D · Cómo se divide la memoria', body(
    bk('Paginación', 'La memoria virtual se corta en <b>páginas</b> del mismo tamaño (4 KB) y la RAM en <b>marcos</b> del mismo tamaño. Una <b>tabla de páginas</b> dice en qué marco está cada página. Si una página no está en RAM ocurre un <b>fallo de página</b> y se trae del disco.'),
    bk('Segmentación', 'La memoria del programa se divide en <b>segmentos</b> de tamaño variable según su uso: <b>código</b>, <b>datos</b>, <b>pila</b>. Cada segmento tiene base y límite.'),
    bk('Diferencias', 'Paginación: tamaños iguales, evita huecos externos, invisible para el programador. Segmentación: tamaños distintos, sigue la lógica del programa, puede dejar huecos (fragmentación externa).'),
    bk('Hoy', 'Los sistemas modernos (Linux en x86-64) usan sobre todo <b>paginación</b>.'),
    ana('Piensa en…', 'Paginación: guardar todo en cajas iguales numeradas. Segmentación: un cajón para playeras, otro para pantalones y otro para calcetines, cada uno de su tamaño.')),
    'Páginas iguales en marcos · segmentos por tipo y de tamaño variable.')
c.A('🗓️', '¿Qué algoritmo de planificación?', 'Elige el algoritmo que describe cada caso.', [
    ['Cada proceso tiene 20 milisegundos y luego pasa al final de la fila', 'Round Robin', 'Turnos con quantum fijo.'],
    ['Se atiende en el orden en que llegaron, sin interrumpir', 'FCFS', 'First Come, First Served.'],
    ['Primero el trabajo que tardará menos', 'SJF', 'Shortest Job First.'],
    ['El antivirus se atiende antes que el juego porque es más importante', 'Por prioridad', 'Gana el de mayor prioridad.'],
], 'Turnos → Round Robin · orden de llegada → FCFS · el más corto → SJF · el más importante → prioridad.',
    ['Round Robin', 'FCFS', 'SJF', 'Por prioridad'])
c.A('🧱', '¿Paginación o segmentación?', 'Decide a qué técnica se refiere.', [
    ['Bloques de 4 KB todos del mismo tamaño', 'Paginación', 'Páginas y marcos iguales.'],
    ['Un bloque para el código, otro para los datos y otro para la pila', 'Segmentación', 'Segmentos según su uso.'],
    ['Tabla que dice en qué marco de la RAM está cada página', 'Paginación', 'Es la tabla de páginas.'],
    ['Cada parte tiene base y límite y puede ser de distinto tamaño', 'Segmentación', 'Tamaños variables.'],
    ['La que usa principalmente Linux en las PC actuales', 'Paginación', 'x86-64 trabaja con paginación.'],
], 'Iguales → paginación · por tipo y tamaño variable → segmentación.', ['Paginación', 'Segmentación'])
c.T('🔢', 'Prioridades nice', 'Escribe solo el número.', [
    ['¿Cuál es el valor nice de MAYOR prioridad?', '-20', 'De -20 (más) a 19 (menos).', 'Es negativo.', 'm'],
    ['¿Cuál es el valor nice de MENOR prioridad?', '19', 'El más «amable» con los demás.', 'Positivo, menor que 20.', 'm'],
    ['¿Qué valor nice tiene un proceso normal al iniciar?', '0', 'Por defecto todos empiezan en 0.', 'Ni positivo ni negativo.', 'm'],
], 'Repasa «Planificación de procesos».')
sim('⚙️', 'El equipo de la sucursal está lento', 'Terminal de Linux simulada: procesos, prioridades y memoria.', 'td',
    'Un cliente se queja de que la computadora va lenta. Investiga qué pasa y arréglalo sin reiniciar.',
    [['Revisa la memoria con <b>free -h</b>.', 'a.used("free")'],
     ['Busca con <b>top</b> (o ps aux) el proceso que más CPU consume.', 'a.used("top")||a.used("ps aux")'],
     ['Termina el proceso <b>juego-trabado</b> (si ignora la señal normal, fuerza con -9).', '!a.proc(function(p){return p.c=="juego-trabado"}).length'],
     ['Baja la prioridad de <b>firefox</b> a <b>10</b> con renice.', 'a.proc(function(p){return p.c=="firefox"&&p.n>=10}).length==1'],
     ['Inicia un respaldo en segundo plano con baja prioridad: <b>nice -n 15 sleep 600 &</b>, y revísalo con <b>jobs</b>.', 'a.proc(function(p){return /sleep/.test(p.c)&&p.n>=15}).length>=1&&a.used("jobs")'],
     ['Pausa ese respaldo con <b>kill -STOP</b> y reanúdalo con <b>kill -CONT</b>.', 'a.used("kill:STOP")&&a.used("kill:CONT")'],
     ['Intenta terminar el proceso zombie <b>descarga</b> y lee por qué no se puede.', 'a.used("kill:zombie")'],
     ['Muestra el árbol de procesos con <b>pstree</b>.', 'a.used("pstree")']],
    'PID: el número de la segunda columna en ps aux. Para el trabajo en segundo plano también puedes usar kill -STOP %1.')
d_end = c.mark() - 1

# ───────────────────────── Glosario y guía ─────────────────────────
g0 = c.mark()
c.L('📖', 'Glosario', 'Apoyo · Palabras que vas a usar', body(
    bk('Kernel', 'Núcleo del sistema operativo: maneja CPU, memoria y dispositivos.'),
    bk('Distribución', 'Linux completo y listo para instalar: Ubuntu, Mint, Debian, Fedora.'),
    bk('Shell / bash', 'Intérprete que recibe tus comandos.'),
    bk('root / sudo', 'Superusuario / ejecutar un comando como administrador.'),
    bk('Punto de montaje', 'Carpeta donde se conecta una partición.'),
    bk('fstab', 'Archivo con las particiones que se montan al arrancar.'),
    bk('GRUB', 'Administrador de arranque: menú para elegir el sistema.'),
    bk('Repositorio / apt', 'Tienda oficial de programas / su gestor de paquetes.'),
    bk('Permisos rwx', 'Leer, escribir y ejecutar para dueño, grupo y otros.'),
    bk('PID', 'Número que identifica a un proceso.'),
    bk('Demonio (daemon)', 'Proceso de servicio que corre en segundo plano.'),
    bk('nice', 'Valor de prioridad: -20 (más) a 19 (menos).'),
    bk('Swap', 'Espacio en disco que se usa como memoria extra.'),
    bk('Página / marco', 'Bloques iguales de memoria virtual / de RAM.'),
    bk('Máquina virtual', 'Computadora simulada dentro de otra.')))
g_end = c.mark() - 1
doc0 = c.mark()
c.L('👩‍🏫', 'Guía para el docente', 'Sesiones sugeridas con tu cronograma', body(
    bk('Antes de empezar', 'Laboratorio de este grupo: <b>lunes 10:40-12:20</b>. Si el laboratorio no tiene Linux, use una máquina virtual (VirtualBox con Ubuntu), WSL o los simuladores del material; Termux sirve en celulares Android.', 'sp'),
    bk('Bloque A · 13 al 23-nov', 'Introducción, sistema de ficheros, shell, órdenes, escritorios, procesos y cron. Simulador A. <b>Práctica 1</b> el lunes 23-nov. (16-nov es inhábil).'),
    bk('Bloque B · 23-nov al 4-dic', 'Sistemas de archivos, particiones, formato, mount, fstab y fsck. Simulador B. <b>Práctica 2</b> el lunes 30-nov (usar una USB que se pueda borrar).'),
    bk('Bloque C · 7 al 14-dic', 'Instalación, GRUB, apt, usuarios, grupos, permisos, CUPS, seguridad, ayuda, comunicación, variables y máquinas virtuales. Simuladores C. <b>Práctica 3</b> el lunes 7 o 14-dic.'),
    bk('Bloque D · 14-dic al 8-ene', 'Procesos, planificación, IPC, memoria, paginación y segmentación. Simulador D y <b>Práctica 4</b>.'),
    bk('Evaluación · viernes 8-ene', 'Sesión práctica en Linux con reporte y listado de comandos (35%). Se desbloquea al terminar el material.'),
    bk('Recomendación', 'Ninguna práctica formatea discos reales del equipo: en la práctica 2 se usa una USB o un disco virtual de la VM.', 'sp')),
    'Las fechas vienen de tu cronograma 1-26/27; ajústalas si cambia.')
doc_end = c.mark() - 1

P = c.js_pages()
EXP = c.exp

SEC = [
    {'id': 's0', 't': 'Empieza aquí', 's': '', 'ic': '🐧', 'a': s0, 'b': s0_end},
    {'id': 'a', 't': 'A', 's': '', 'ic': '⌨️', 'a': a0, 'b': a_end},
    {'id': 'b', 't': 'B', 's': '', 'ic': '💽', 'a': b0, 'b': b_end},
    {'id': 'c', 't': 'C', 's': '', 'ic': '👥', 'a': c0, 'b': c_end},
    {'id': 'd', 't': 'D', 's': '', 'ic': '⚙️', 'a': d0, 'b': d_end},
    {'id': 'g', 't': 'Glosario', 's': '', 'ic': '📖', 'a': g0, 'b': g_end},
    {'id': 'doc', 't': 'Guía docente', 's': '', 'ic': '👩‍🏫', 'a': doc0, 'b': doc_end},
]
ORDER = ['s0', 'a', 'b', 'c', 'd']

CH = r'''
s0:{k:"Introducción",l:"0",ic:"🐧",t:"Empieza aquí",d:"Qué es un sistema multiusuario y qué vas a entregar.",time:"20 min",obj:["Distinguir monousuario de multiusuario","Conocer el caso y la evidencia"],sum:["Multiusuario = varias cuentas con sus archivos y permisos.","Entregas un reporte de sesión práctica y tu listado de comandos (35%)."],q:"¿Qué computadoras o servicios que usas a diario son multiusuario?"},
a:{k:"Bloque A",l:"A",ic:"⌨️",t:"Operación del sistema multiusuario sobre Linux",d:"Linux, sistema de ficheros, shell, órdenes, escritorios, procesos y tareas programadas.",time:"6 h",obj:["Explicar qué es Linux y sus distribuciones","Ubicar las carpetas principales del árbol /","Usar las órdenes básicas en la terminal","Reconocer tipos y estados de procesos","Programar tareas con cron"],sum:["Un solo árbol desde / · /home, /etc, /dev, /var/log.","pwd · ls · cd · mkdir · cat · cp · mv · rm.","Estados R S T Z · kill y kill -9.","crontab: minuto hora día mes día-semana comando."],q:"¿Qué tarea de tu casa o tu escuela programarías para que se hiciera sola?"},
b:{k:"Bloque B",l:"B",ic:"💽",t:"Manejo del sistema de archivos, discos y dispositivos",d:"Sistemas de archivos, particiones, formato, mount, umount, fstab e integridad.",time:"7 h",obj:["Comparar ext4, vfat, NTFS y swap","Identificar discos y particiones","Formatear, montar y desmontar","Configurar fstab y revisar con fsck"],sum:["lsblk → mkfs → mkdir → mount → df -h → umount.","fstab: dispositivo punto tipo opciones dump pass.","fsck solo con la partición desmontada."],q:"¿Por qué es peligroso equivocarse de letra al formatear?",rev:[["El archivo de configuración de los discos que se montan al arrancar es…",["/etc/fstab","/home/fstab","/dev/fstab"],0,"La configuración vive en /etc."],["El estado Z de un proceso significa…",["Zombie","Zona","Zoom"],0,"Terminó pero su padre no lo recogió."]]},
c:{k:"Bloque C",l:"C",ic:"👥",t:"Configuración y administración del sistema Linux",d:"Instalación, apt, GRUB, usuarios, permisos, CUPS, seguridad, ayuda, comunicación, máquinas virtuales y variables.",time:"10 h",obj:["Describir la instalación y el arranque con GRUB","Instalar programas con apt","Crear usuarios y grupos","Asignar permisos y dueños","Usar CUPS, ufw, man, write, wall y variables","Crear una máquina virtual"],sum:["sudo para administrar; root puede todo.","useradd -m + passwd · groupadd · usermod -aG.","r=4 w=2 x=1 · chmod · chown.","apt update → install → upgrade."],q:"¿Por qué es mejor que cada empleado tenga su propia cuenta?",rev:[["Para montar la memoria en /mnt/usb se usa…",["mount /dev/sdb1 /mnt/usb","mkfs /mnt/usb","fsck /mnt/usb"],0,"mount dispositivo punto."],["Antes de fsck la partición debe estar…",["Desmontada","Montada","Formateada de nuevo"],0,"Revisarla montada puede dañarla."]]},
d:{k:"Bloque D",l:"D",ic:"⚙️",t:"Gestión de procesos y memoria",d:"Estados, operaciones, planificación, comunicación entre procesos, memoria, paginación y segmentación.",time:"7 h",obj:["Describir el ciclo de vida de un proceso","Comparar algoritmos de planificación","Ajustar prioridades con nice y renice","Explicar memoria virtual, swap, paginación y segmentación"],sum:["Nuevo → Listo → Ejecución ⇄ Bloqueado → Terminado.","Round Robin reparte turnos; nice de -20 a 19.","Paginación: bloques iguales; segmentación: por tipo."],q:"¿Qué harías si un equipo multiusuario se queda sin memoria?",rev:[["chmod 770 deja que…",["Dueño y grupo hagan todo; otros nada","Todos lean","Solo el dueño lea"],0,"7 = rwx, 0 = ---."],["Para agregar a ana al grupo caja sin quitarle otros grupos…",["usermod -aG caja ana","usermod -G caja ana","groupadd caja ana"],0,"La -a agrega."]]}
'''

ILL = r'''
ILL["El sistema de ficheros de Linux"]=function(){var o=R_(145,6,50,22,"b",6)+T_(170,22,"/","tw"),k=["home","etc","dev","var","mnt","root"];k.forEach(function(x,i){var X=14+i*54;o+=R_(X,52,48,20,i==0?"g":"s",4)+T_(X+24,66,x,i==0?"tw":"t")+'<line x1="170" y1="28" x2="'+(X+24)+'" y2="52" stroke="currentColor" stroke-opacity=".35"/>'});o+=R_(8,92,60,18,"s",3)+T_(38,105,"alumno","tm")+R_(8,114,60,18,"s",3)+T_(38,127,"ana","tm")+T_(250,108,"Todo cuelga de la raíz /","tm");return SV(340,138,o,"Árbol de carpetas de Linux")};
ILL["El intérprete de comandos (shell)"]=function(){return SV(340,70,R_(10,10,320,50,"s",6)+T_(170,32,"alumno@lab-pc07:~$ ls -l Documentos","t")+T_(170,50,"usuario @ equipo : carpeta $ comando -opción argumento","tm"),"Partes del indicador y de un comando")};
ILL["Procesos de Linux: tipos y estados"]=function(){return grid3([["▶️","R|ejecutando"],["💤","S|durmiendo"],["⏸️","T|detenido"],["🧟","Z|zombie"],["🔢","PID|identificador"],["🛎️","Demonio|servicio"]],"Estados y conceptos")};
ILL["Particiones del disco duro"]=function(){return SV(340,110,R_(10,14,250,26,"s",4)+R_(10,14,220,26,"b",4)+T_(120,32,"sda1 · ext4 · /","tw")+R_(232,14,28,26,"a",4)+T_(246,32,"swap","td")+T_(300,32,"sda","t")+R_(10,60,250,26,"g",4)+T_(135,78,"sdb1 · USB · /mnt/usb","tw")+T_(300,78,"sdb","t")+T_(170,104,"Discos (sda, sdb) y particiones (sda1, sdb1)","tm"),"Particiones")};
ILL["Montar y desmontar: mount y umount"]=function(){return SV(340,100,R_(10,30,90,40,"g",6)+T_(55,55,"/dev/sdb1","tw")+T_(170,48,"mount →","t")+T_(170,66,"← umount","tm")+R_(230,30,100,40,"b",6)+T_(280,55,"/mnt/usb","tw"),"Montar conecta el dispositivo a una carpeta")};
ILL["Permisos de archivos y directorios"]=function(){var g=[["d","tipo","s"],["rwx","dueño","g"],["r-x","grupo","b"],["---","otros","r"]],o='',x=20;g.forEach(function(q,i){var w=i?90:40;o+=R_(x,16,w,30,q[2],4)+T_(x+w/2,36,q[0],q[2]=="s"?"t":"tw")+T_(x+w/2,64,q[1],"tm");x+=w+4});o+=T_(170,90,"rwx = 4+2+1 = 7 · r-x = 5 · --- = 0  →  750","t");return SV(340,100,o,"Cómo se leen los permisos")};
ILL["Estados y operaciones de los procesos"]=function(){var s=[["Nuevo",20,"s"],["Listo",90,"b"],["Ejecución",170,"g"],["Terminado",260,"s"]],o='';s.forEach(function(q){o+=R_(q[1],20,64,26,q[2],6)+T_(q[1]+32,37,q[0],q[2]=="s"?"t":"tw")});o+=R_(150,76,90,26,"a",6)+T_(195,93,"Bloqueado","td")+T_(170,124,"Listo ⇄ Ejecución ⇄ Bloqueado","tm");return SV(340,132,o,"Ciclo de vida de un proceso")};
ILL["Paginación y segmentación"]=function(){var o=T_(80,14,"Paginación","t")+T_(255,14,"Segmentación","t");for(var i=0;i<6;i++)o+=R_(20+(i%3)*40,22+Math.floor(i/3)*30,36,26,"b",3)+T_(38+(i%3)*40,39+Math.floor(i/3)*30,"P"+i,"tw");o+=R_(200,22,110,20,"g",3)+T_(255,36,"código","tw")+R_(200,46,110,32,"a",3)+T_(255,66,"datos","td")+R_(200,82,110,14,"s",3)+T_(255,93,"pila","tm");return SV(340,104,o,"Bloques iguales contra segmentos por uso")};
'''

EXH = r'''
function lt_(t,b){return '<div class="mw"><div class="mt"><i></i><i></i><i></i><b>'+t+'</b></div><pre style="margin:0;background:#300a24;color:#eeeeec;padding:8px;font:12.5px/1.4 Consolas,monospace;white-space:pre-wrap">'+b+'</pre></div>'}
EXH.term=function(){return exw(lt_('Terminal · Ctrl + Alt + T','<b style="color:#8ae234">alumno@lab-pc07:~$</b> pwd '+mk(1)+'\n/home/alumno\n<b style="color:#8ae234">alumno@lab-pc07:~$</b> mkdir -p sucursal/clientes sucursal/precios '+mk(2)+'\n<b style="color:#8ae234">alumno@lab-pc07:~$</b> ls -l sucursal '+mk(3)+'\ndrwxr-xr-x 2 alumno alumno 4096 clientes\ndrwxr-xr-x 2 alumno alumno 4096 precios'),['Dónde estás.','Crea la estructura.','Comprueba con detalle.'])};
EXH.ps=function(){return exw(lt_('Procesos','<b style="color:#8ae234">$</b> ps aux '+mk(1)+'\nalumno 1588 71.5 9.8 R juego-trabado\n<b style="color:#8ae234">$</b> kill -9 1588 '+mk(2)+'\n<b style="color:#8ae234">$</b> crontab -l '+mk(3)+'\n0 20 * * 1-5 /home/alumno/respaldo.sh'),['Busca el proceso y su PID.','Lo termina a la fuerza.','La tarea programada.'])};
EXH.disco=function(){return exw(lt_('Discos','<b style="color:#8ae234">$</b> lsblk '+mk(1)+'\nsdb      8:16   1   7.5G  0 disk\n└─sdb1   8:17   1   7.5G  0 part\n<b style="color:#8ae234">$</b> sudo mkfs.ext4 /dev/sdb1 '+mk(2)+'\n<b style="color:#8ae234">$</b> sudo mount /dev/sdb1 /mnt/usb '+mk(3)+'\n<b style="color:#8ae234">$</b> df -h '+mk(4)+'\n/dev/sdb1   7.3G   24K  6.9G   1% /mnt/usb'),['Identifica la memoria.','Le da formato.','La monta.','Comprueba el espacio.'])};
EXH.fstab=function(){return exw(lt_('/etc/fstab','UUID=6f1c-a2 /        ext4 errors=remount-ro 0 1\n/dev/sdb1    /mnt/usb ext4 defaults          0 2 '+mk(1)+'\n\n<b style="color:#8ae234">$</b> sudo mount -a '+mk(2)),['La línea nueva.','Prueba que no haya errores.'])};
EXH.usuarios=function(){return exw(lt_('Usuarios y grupos','<b style="color:#8ae234">$</b> sudo useradd -m ana '+mk(1)+'\n<b style="color:#8ae234">$</b> sudo passwd ana\n<b style="color:#8ae234">$</b> sudo groupadd caja '+mk(2)+'\n<b style="color:#8ae234">$</b> sudo usermod -aG caja ana\n<b style="color:#8ae234">$</b> id ana '+mk(3)+'\nuid=1001(ana) gid=1001(ana) grupos=ana,caja'),['Crea la cuenta y su carpeta.','Crea el grupo y la agrega.','Comprueba.'])};
EXH.permisos=function(){return exw(lt_('Carpeta compartida','<b style="color:#8ae234">$</b> sudo mkdir -p /srv/caja\n<b style="color:#8ae234">$</b> sudo chown root:caja /srv/caja '+mk(1)+'\n<b style="color:#8ae234">$</b> sudo chmod 770 /srv/caja '+mk(2)+'\n<b style="color:#8ae234">$</b> ls -l /srv\ndrwxrwx--- 2 root caja 4096 caja '+mk(3)),['Dueño root, grupo caja.','Grupo con todo, otros nada.','Así debe verse.'])};
EXH.apt=function(){return exw(lt_('Paquetes','<b style="color:#8ae234">$</b> sudo apt update '+mk(1)+'\n<b style="color:#8ae234">$</b> sudo apt install tree '+mk(2)+'\n<b style="color:#8ae234">$</b> tree sucursal'),['Actualiza la lista.','Instala el programa.'])};
EXH.vm=function(){return exw(mp('VirtualBox · Nueva máquina','<div class="mbox">Nombre: Ubuntu-Nova · Tipo: Linux '+mk(1)+'</div><div class="mbox" style="margin-top:6px">Memoria: 4096 MB · Disco: 25 GB '+mk(2)+'</div><div class="mbox" style="margin-top:6px">Almacenamiento › ISO de Ubuntu › Iniciar '+mk(3)+'</div>'),['Nombre y tipo.','Recursos de la VM.','Arranca desde la ISO.'])};
EXH.top=function(){return exw(lt_('top y free','<b style="color:#8ae234">$</b> free -h '+mk(1)+'\nMem:   7.6Gi  3.0Gi  1.2Gi … 4.4Gi disponible\n<b style="color:#8ae234">$</b> renice 10 -p 1530 '+mk(2)+'\n<b style="color:#8ae234">$</b> nice -n 15 sleep 600 & '+mk(3)+'\n[1] 2001'),['Mira «disponible».','Menos prioridad a firefox.','Respaldo con baja prioridad.'])};
EXH.termux=function(){return exw(mp('Termux · Android','<div class="mbox">pkg update · pkg install tree '+mk(1)+'</div><div class="mbox" style="margin-top:6px">mkdir, ls -l, chmod, ps, top funcionan igual '+mk(2)+'</div>'),['Termux usa pkg en lugar de apt.','Los comandos básicos son los mismos.'])};
'''

PR = [
    {'id': 'pr1', 'n': 1, 't': 'Opera Linux desde la terminal',
     'prog': 'Bloque A · Operación del sistema multiusuario',
     'min': 100, 'lug': 'Laboratorio (Linux o máquina virtual) o celular con Termux',
     'modes': {
         'pc': {'mat': ['Equipo con Ubuntu o una máquina virtual', 'Documento para tus capturas'],
                'steps': [
                    'Antes de empezar, termina el simulador «Primer día en la terminal de la sucursal».',
                    ['Abre la terminal y crea la estructura <b>sucursal/clientes</b>, <b>sucursal/precios</b> y <b>sucursal/respaldos</b>; compruébala con ls -l.', 'term'],
                    'Crea tres archivos con echo, cópialos, muévelos y renombra uno. Busca una palabra con grep.',
                    ['Revisa los procesos con ps aux y top, identifica un PID y explica su estado.', 'ps'],
                    'Programa con crontab una tarea de respaldo y muéstrala con crontab -l.',
                    'Escribe <b>history</b> y guarda la lista de comandos para tu reporte.']},
         'cel': {'mat': ['Celular Android con Termux (o los simuladores del material)', 'Galería para tus capturas'],
                 'steps': [
                     'Antes de empezar, termina el simulador «Primer día en la terminal de la sucursal».',
                     ['Instala Termux, actualiza con pkg update y abre la terminal.', 'termux'],
                     'Crea la estructura sucursal/clientes, precios y respaldos y compruébala con ls -l.',
                     'Crea archivos con echo, cópialos y muévelos; busca una palabra con grep.',
                     'Ejecuta ps y top, toma capturas y escribe history para guardar tus comandos.']}},
     'entrega': ['Capturas y la lista de comandos (history); la usarás en tu reporte.'],
     'rub': [['Estructura de carpetas correcta', 25], ['Archivos creados, copiados y movidos', 25], ['Procesos identificados con su estado', 25], ['Tarea programada en cron', 25]]},
    {'id': 'pr2', 'n': 2, 't': 'Prepara una memoria USB en Linux',
     'prog': 'Bloque B · Sistema de archivos y discos',
     'min': 80, 'lug': 'Laboratorio con una USB que se pueda borrar, o disco virtual en la VM',
     'modes': {
         'pc': {'mat': ['Equipo o VM con Ubuntu', 'Memoria USB que se pueda borrar (o un disco virtual nuevo en la VM)'],
                'steps': [
                    'Antes de empezar, termina el simulador «Prepara la memoria USB de respaldos».',
                    ['Identifica la memoria con lsblk y sudo fdisk -l. Confirma la letra dos veces.', 'disco'],
                    'Dale formato ext4 (o vfat si la usarás en Windows), crea /mnt/usb y móntala.',
                    'Comprueba con df -h, copia un archivo y desmonta con umount.',
                    ['Agrega la línea a /etc/fstab (haz antes una copia), prueba con sudo mount -a y revisa con fsck estando desmontada.', 'fstab']]},
         'cel': {'mat': ['Los simuladores del material', 'Galería para tus capturas'],
                 'steps': [
                     'Termina el simulador «Prepara la memoria USB de respaldos» completo.',
                     'Captura cada paso: lsblk, mkfs, mount, df -h, fstab, fsck y mount -a.',
                     'Escribe con tus palabras para qué sirve cada comando.',
                     'Explica qué pasaría si formatearas /dev/sda1 en lugar de /dev/sdb1.']}},
     'entrega': ['Capturas de cada comando y la explicación de fstab.'],
     'rub': [['Partición identificada correctamente', 20], ['Formato y montaje', 30], ['fstab correcto y probado', 30], ['fsck con la partición desmontada', 20]]},
    {'id': 'pr3', 'n': 3, 't': 'Administra usuarios, permisos y programas',
     'prog': 'Bloque C · Configuración y administración',
     'min': 100, 'lug': 'Laboratorio (VM con Ubuntu) o simuladores',
     'modes': {
         'pc': {'mat': ['VM con Ubuntu (VirtualBox, VMware o Vagrant)', 'Documento para tus capturas'],
                'steps': [
                    'Antes de empezar, termina los simuladores del bloque C.',
                    ['Si no tienes Linux, crea una VM en VirtualBox con la ISO de Ubuntu.', 'vm'],
                    ['Crea los usuarios ana, luis y beto con contraseña y los grupos caja y soporte.', 'usuarios'],
                    ['Crea /srv/caja con dueño root, grupo caja y permisos 770; comprueba que beto no puede entrar.', 'permisos'],
                    ['Actualiza el sistema e instala un programa con apt.', 'apt'],
                    'Revisa CUPS (lpstat -p), activa ufw, crea una variable con export y envía un aviso con wall.']},
         'cel': {'mat': ['Los simuladores del material', 'Galería para tus capturas'],
                 'steps': [
                     'Termina los simuladores «Da de alta al personal» e «Impresora, seguridad y comunicación».',
                     'Captura id ana, ls -l /srv y la prueba de que ana puede escribir en /srv/caja.',
                     'Explica en tus notas qué significa cada número de chmod 770.',
                     'Describe los pasos para crear una VM en VirtualBox.']}},
     'entrega': ['Capturas de usuarios, grupos, permisos y paquetes.'],
     'rub': [['Usuarios y grupos correctos', 25], ['Carpeta compartida con dueño y permisos', 30], ['Paquetes actualizados e instalados', 20], ['CUPS, ufw, variable y mensaje', 25]]},
    {'id': 'pr4', 'n': 4, 't': 'Diagnostica procesos y memoria',
     'prog': 'Bloque D · Gestión de procesos y memoria',
     'min': 60, 'lug': 'Laboratorio, VM, Termux o simuladores',
     'modes': {
         'pc': {'mat': ['Equipo o VM con Ubuntu', 'Documento para tus capturas'],
                'steps': [
                    'Antes de empezar, termina el simulador «El equipo de la sucursal está lento».',
                    ['Revisa la memoria con free -h y vmstat; anota el total, lo disponible y el uso de swap.', 'top'],
                    'Abre varios programas, identifica en top el que más consume y explica su estado.',
                    'Inicia un proceso con nice -n 15 en segundo plano, pásalo por los estados T y S con kill -STOP / -CONT y termínalo.',
                    'Haz un cuadro comparativo: FCFS, SJF, Round Robin y prioridad; paginación contra segmentación.']},
         'cel': {'mat': ['Termux o los simuladores del material', 'Cuaderno o documento'],
                 'steps': [
                     'Termina el simulador «El equipo de la sucursal está lento».',
                     'En Termux ejecuta top y free (o captura el simulador) y anota lo que ves.',
                     'Dibuja el ciclo de vida de un proceso con sus 5 estados.',
                     'Haz un cuadro comparativo: FCFS, SJF, Round Robin y prioridad; paginación contra segmentación.']}},
     'entrega': ['Capturas y el cuadro comparativo.'],
     'rub': [['Lectura correcta de memoria y swap', 25], ['Procesos y estados explicados', 25], ['Prioridad con nice/renice y señales', 25], ['Cuadro comparativo completo', 25]]},
]

EVALUATION = {
    'course': 'MSII-05 · Manejo de sistemas operativos · Unidad 2',
    'ra': 'R.A. 2.2', 'title': 'Sesión práctica en Linux y listado de comandos',
    'data': [
        ('Resultado de aprendizaje', 'Opera el sistema operativo multiusuario, considerando los aspectos funcionales del sistema informático.'),
        ('Actividad de evaluación', '2.2.1 Realiza una sesión práctica sobre las técnicas de gestión de recursos del sistema operativo multiusuario.'),
        ('Evidencias', 'Reporte de la sesión en práctica · Listado de los comandos utilizados y ejecutados con la operación realizada al sistema'),
        ('Ponderación', '35% (según el programa)'),
        ('Entrega', 'Viernes 8 de enero'),
    ],
    'situation': 'La sucursal del Cibercafé Nova abre con un equipo Linux compartido por tres empleados. Como administrador, déjalo listo: organiza archivos, prepara la memoria de respaldos, crea las cuentas con sus permisos, instala lo necesario y comprueba que los procesos y la memoria estén sanos. Registra todo en tu <b>reporte</b> y tu <b>listado de comandos</b>.',
    'hint': 'Hazlo en Ubuntu (equipo o máquina virtual). Si no es posible, usa los simuladores del material y captura cada reto resuelto. Al final escribe history para armar tu listado.',
    'steps': [
        ('Preparación', [
            'Portada con tu nombre, grupo y fecha; objetivo de la sesión en 2 líneas.',
            'Información del equipo: uname -a, lsblk, free -h y echo $XDG_CURRENT_DESKTOP.']),
        ('Archivos y procesos (A)', [
            'Estructura sucursal con 3 subcarpetas y archivos creados, copiados y movidos.',
            'Procesos con ps aux y top; un proceso terminado con kill y una tarea programada en crontab.']),
        ('Discos (B)', [
            'Memoria USB o disco virtual formateado, montado en /mnt/usb, comprobado con df -h, agregado a fstab y revisado con fsck.']),
        ('Administración (C)', [
            'Usuarios ana, luis y beto con contraseña; grupos caja y soporte.',
            'Carpeta /srv/caja con chown root:caja y chmod 770; prueba de acceso permitido y denegado.',
            'apt update, instalación de un programa, ufw activo y estado de CUPS.']),
        ('Procesos y memoria (D)', [
            'Proceso en segundo plano con nice, cambio de prioridad con renice y pausa/continuación con señales.',
            'Explicación breve de los estados del proceso y de la memoria (RAM, swap, paginación).']),
        ('Reporte y listado', [
            'Reporte: capturas en orden, cada una con qué hiciste y qué resultado obtuviste.',
            'Listado de comandos en tabla: comando, para qué sirve y el ejemplo exacto que ejecutaste.',
            'Conclusión: ¿qué ventajas tiene un sistema multiusuario bien administrado?']),
    ],
    'rubric': [
        ('Información del equipo', 5), ('Archivos, procesos y cron', 15), ('Discos: formato, montaje, fstab y fsck', 15),
        ('Usuarios y grupos', 15), ('Permisos y propietarios', 15), ('Paquetes, seguridad e impresión', 10),
        ('Prioridades y señales', 10), ('Reporte con capturas explicadas', 5), ('Listado de comandos completo', 10),
    ],
    'deliver': ['Un solo archivo PDF o Word con el reporte y el listado.', 'Nombre del archivo: Apellido_Nombre_Sesion_MSII22.', 'Súbelo en la actividad R.A. 2.2 de la plataforma.'],
}
