from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

OUT = Path('output/pear')
OUT.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor('#073B63')
BLUE = colors.HexColor('#147AA2')
GOLD = colors.HexColor('#F4B740')
PALE = colors.HexColor('#EEF6FA')
INK = colors.HexColor('#102A43')
MUTED = colors.HexColor('#526C7A')
LINE = colors.HexColor('#D5E0E7')
GREEN = colors.HexColor('#0B7A64')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=colors.black, alignment=TA_LEFT, spaceAfter=12))
styles.add(ParagraphStyle(name='Subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=16, textColor=MUTED, spaceAfter=16))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.black, spaceBefore=5, spaceAfter=10, keepWithNext=True))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.black, spaceBefore=10, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontName='Helvetica', fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name='CoverCode', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLUE, spaceAfter=12))
styles.add(ParagraphStyle(name='Step', parent=styles['BodyText'], fontName='Helvetica', fontSize=8.7, leading=11.8, leftIndent=16, firstLineIndent=-16, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name='CenterSmall', parent=styles['Smallx'], alignment=TA_CENTER))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(doc.leftMargin, 1.35*cm, letter[0]-doc.rightMargin, 1.35*cm)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, .92*cm, 'Aula Virtual  |  Pensamiento matemático I')
    canvas.drawRightString(letter[0]-doc.rightMargin, .92*cm, f'Página {doc.page}')
    canvas.restoreState()

def doc(path, title, subtitle, code, story):
    d = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=1.7*cm, rightMargin=1.7*cm, topMargin=1.55*cm, bottomMargin=1.7*cm, title=title, author='Aula Virtual')
    cover = [Spacer(1, .45*cm), Paragraph(code, styles['CoverCode']), Paragraph(title, styles['DocTitle']), Paragraph(subtitle, styles['Subtitle']), Spacer(1, .15*cm)]
    cover.append(Table([[Paragraph('<b>Grupo</b><br/>111', styles['Bodyx']), Paragraph('<b>Periodo</b><br/>Agosto 2026 - Enero 2027', styles['Bodyx']), Paragraph('<b>Asignatura</b><br/>Pensamiento matemático I', styles['Bodyx'])]], colWidths=[3.2*cm, 5.1*cm, 6.7*cm], style=TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.8,LINE),('INNERGRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)])))
    d.build(cover + story, onFirstPage=footer, onLaterPages=footer)

def p(text, style='Bodyx'):
    return Paragraph(text, styles[style])

def bullets(items):
    return [p(f'<b>•</b> {item}', 'Step') for item in items]

def section(title, body):
    return [p(title, 'H1x')] + body

def table(data, widths, header=True, font=8.2):
    t = Table([[p(str(cell), 'Smallx') for cell in row] for row in data], colWidths=widths, repeatRows=1 if header else 0)
    cmds=[('BOX',(0,0),(-1,-1),.7,LINE),('INNERGRID',(0,0),(-1,-1),.45,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]
    if header: cmds += [('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0: cmds.append(('BACKGROUND',(0,r),(-1,r),PALE))
    t.setStyle(TableStyle(cmds))
    return t

def material_11():
    story=[]
    story += section('Qué aprenderás', [p('Utilizarás la lógica matemática para reconocer proposiciones, construir expresiones compuestas y analizar argumentos relacionados con situaciones de tu contexto.')])
    story += bullets(['Distinguir enunciados que son proposiciones.', 'Representar proposiciones con letras y símbolos.', 'Usar negación, conjunción, disyunción, condicional y bicondicional.', 'Construir e interpretar tablas de verdad.', 'Sustentar una decisión mediante un razonamiento lógico.'])
    story += [PageBreak()]
    story += section('1  Proposiciones y valor de verdad', [p('Una <b>proposición</b> es un enunciado declarativo que puede clasificarse como verdadero o falso, pero no ambos al mismo tiempo. Las preguntas, órdenes y expresiones abiertas no son proposiciones hasta que se especifican sus datos.')])
    story.append(table([
        ['Enunciado','¿Es proposición?','Razón'],
        ['El número 12 es par.','Sí','Puede determinarse que es verdadero.'],
        ['¿Terminaste la actividad?','No','Es una pregunta.'],
        ['Respeta el turno de participación.','No','Es una indicación.'],
        ['x + 3 = 10','No, todavía','Depende del valor asignado a x.'],
    ], [6.3*cm,3*cm,5.7*cm]))
    story += [p('Representación', 'H2x'), p('Las proposiciones simples se representan con letras minúsculas: <b>p</b>, <b>q</b>, <b>r</b>. Por ejemplo: p: “La información fue verificada”. Cada letra puede tener valor verdadero (V) o falso (F).')]
    story += [PageBreak()]
    story += section('2  Operadores lógicos', [p('Un operador permite formar una proposición compuesta a partir de una o más proposiciones simples.')])
    story.append(table([
        ['Operador','Símbolo','Lectura','Es verdadero cuando...'],
        ['Negación','¬p','no p','p es falsa.'],
        ['Conjunción','p ∧ q','p y q','ambas proposiciones son verdaderas.'],
        ['Disyunción','p ∨ q','p o q','al menos una proposición es verdadera.'],
        ['Condicional','p → q','si p, entonces q','no ocurre el caso p verdadera y q falsa.'],
        ['Bicondicional','p ↔ q','p si y solo si q','p y q tienen el mismo valor.'],
    ], [3.0*cm,2.1*cm,4.2*cm,5.7*cm]))
    story += [p('Atención', 'H2x'), p('En lógica, la disyunción “o” normalmente es inclusiva: también es verdadera cuando las dos proposiciones son verdaderas. El condicional solamente es falso cuando se cumple la condición, pero no la consecuencia.')]
    story += [PageBreak()]
    story += section('3  Cómo construir una tabla de verdad', [p('Una tabla de verdad muestra todas las combinaciones posibles de valores. Con dos proposiciones hay 2² = 4 filas; con tres proposiciones hay 2³ = 8 filas.')])
    story += bullets(['Identifica las proposiciones simples.', 'Cuenta cuántas combinaciones se necesitan.', 'Escribe las columnas de p, q y r en un orden sistemático.', 'Agrega una columna por cada operación intermedia.', 'Calcula la expresión principal fila por fila.', 'Interpreta qué significa el resultado en la situación analizada.'])
    story.append(table([
        ['p','q','p ∧ q','p ∨ q','p → q','p ↔ q'],
        ['V','V','V','V','V','V'],
        ['V','F','F','V','F','F'],
        ['F','V','F','V','V','F'],
        ['F','F','F','F','V','V'],
    ], [2.5*cm]*6))
    story += [PageBreak()]
    story += section('4  Del resultado a una decisión', [p('La tabla no sustituye el diálogo: ayuda a revisar si una conclusión se desprende de las condiciones planteadas. Después de calcularla, se debe explicar el significado de las filas relevantes con palabras propias y contrastarlo con razones, evidencias y derechos de las personas.')])
    story += [p('Guía de análisis', 'H2x')] + bullets(['¿Qué hechos representan p, q y r?', '¿Qué operador conecta correctamente las ideas?', '¿En qué combinaciones la expresión es verdadera?', '¿Qué conclusión sí está respaldada por la tabla?', '¿Qué información adicional se necesita para tomar una decisión responsable?'])
    story += [p('Practica sin respuestas', 'H2x')] + bullets(['Decide cuáles de cinco enunciados cotidianos son proposiciones.', 'Representa con símbolos: “Si se respeta la privacidad, entonces se protege la dignidad”.', 'Construye la tabla de verdad de (p ∧ q) → r.', 'Explica una fila de la tabla con una oración completa.'])
    doc(OUT/'PEAR_Proposito_1.1_Material_didactico.pdf','Propósito 1.1  Lógica matemática y tablas de verdad','Guía didáctica para reconocer proposiciones, utilizar operadores lógicos y fundamentar decisiones con tablas de verdad.','MATERIAL DIDÁCTICO 1.1',story)

def activity_11():
    story=[]
    story += section('Actividad', [p('Analiza el caso sobre derechos humanos asignado en Aula Virtual. Construye las tablas de verdad solicitadas y utiliza sus resultados para sustentar una postura razonada.')])
    story += section('Instrucciones', bullets(['Copia en tu reporte el tema y las tres proposiciones asignadas.', 'Identifica cada proposición con las letras p, q y r sin modificar su significado.', 'Escribe en lenguaje cotidiano y en símbolos las expresiones: negación, conjunción, disyunción, condicional y bicondicional indicadas.', 'Construye una tabla de verdad completa para cada una de las cuatro expresiones compuestas asignadas.', 'Marca las filas que resulten importantes para analizar el caso.', 'Interpreta cada tabla con un párrafo breve; no escribas únicamente V y F.', 'Redacta una postura final de 150 a 200 palabras y susténtala con al menos dos resultados de tus tablas.', 'Incluye una reflexión de cinco líneas sobre la importancia de escuchar posturas distintas durante un debate.', 'Entrega todo en un solo archivo PDF en Aula Virtual.']))
    story += [p('Estructura del reporte', 'H1x')]
    story.append(table([
        ['Sección','Contenido mínimo'],
        ['1  Caso asignado','Tema y proposiciones p, q y r.'],
        ['2  Expresiones lógicas','Traducción entre lenguaje cotidiano y símbolos.'],
        ['3  Tablas de verdad','Cuatro tablas completas, ordenadas y legibles.'],
        ['4  Interpretación','Explicación breve de cada resultado.'],
        ['5  Postura final','Conclusión de 150 a 200 palabras.'],
        ['6  Reflexión','Escucha, respeto y diálogo durante el debate.'],
    ], [4.2*cm,10.8*cm]))
    story += [p('Datos de entrega', 'H1x')]
    story.append(table([['Elemento','Indicación'],['Producto','Reporte con tablas de verdad en PDF'],['Trabajo','Individual'],['Valor','15%'],['Nombre del archivo','PEAR_111_Apellido_Nombre_1.1.pdf']], [4*cm,11*cm]))
    story += [p('Antes de entregar', 'H1x')] + bullets(['Las tablas contienen todas las combinaciones necesarias.', 'Cada operador fue aplicado correctamente.', 'Las interpretaciones están escritas con palabras propias.', 'La postura utiliza resultados de las tablas.', 'El PDF abre correctamente y tiene el nombre solicitado.'])
    doc(OUT/'PEAR_Actividad_evaluacion_1.1.pdf','Actividad de evaluación 1.1  Lógica y derechos humanos','Instrucciones para analizar proposiciones de un debate mediante tablas de verdad y formular una postura fundamentada.','ACTIVIDAD DE EVALUACIÓN 1.1',story)

def material_12():
    story=[]
    story += section('Qué aprenderás', [p('Comprenderás cómo diferentes civilizaciones resolvieron la necesidad de contar, por qué el cero cambió las matemáticas y cómo el sistema indoarábigo y el ábaco siguen presentes en la vida cotidiana.')])
    story += bullets(['Reconocer sistemas de conteo históricos.', 'Distinguir sistemas aditivos, posicionales y de base.', 'Explicar la función del cero.', 'Representar cantidades y operaciones sencillas con un ábaco.'])
    story += [PageBreak()]
    story += section('1  Contar antes de los números modernos', [p('Contar surgió de necesidades concretas: registrar cosechas, intercambios, animales, impuestos, calendarios y construcciones. Las marcas, fichas y símbolos permitieron conservar información más allá de la memoria.')])
    story.append(table([
        ['Civilización','Rasgos principales','Aporte o uso del cero'],
        ['Mesopotamia','Sistema posicional de base 60; escritura cuneiforme.','Usó marcadores de posición en etapas tardías.'],
        ['Egipto','Sistema decimal aditivo con símbolos para potencias de diez.','No requirió un cero posicional.'],
        ['Pueblos olmeca y maya','Sistema vigesimal; puntos, barras y niveles.','Desarrollaron un símbolo explícito para el cero.'],
        ['India','Sistema decimal posicional.','Consolidó el cero como número y marcador de posición.'],
        ['Mundo árabe','Difundió y desarrolló el sistema procedente de India.','Transmitió su uso hacia Europa.'],
    ], [3.0*cm,7.0*cm,5.0*cm]))
    story += [p('Idea clave', 'H2x'), p('En un sistema posicional, el valor de una cifra depende de su posición. En 507, el 5 representa centenas; el cero conserva la posición de las decenas.')]
    story += [PageBreak()]
    story += section('2  Número, naturales y sistema indoarábigo', [p('<b>Número</b> es la idea que permite expresar cantidad, orden o medida. Los <b>números naturales</b> se usan principalmente para contar: 1, 2, 3, 4… En algunos contextos también se incluye el 0.'), p('El sistema indoarábigo utiliza diez cifras —0 a 9—, base diez y valor posicional. Su eficiencia facilita escribir cantidades grandes y realizar algoritmos de cálculo.')])
    story += [p('Leonardo de Pisa', 'H2x'), p('Leonardo de Pisa, conocido como Fibonacci, difundió en Europa el uso práctico de las cifras indoarábigas mediante su obra <i>Liber Abaci</i>. Este sistema resultó más eficiente para el comercio y el cálculo que la numeración romana.')]
    story.append(table([['Número','Descomposición posicional','Lectura'],['3 406','3×1000 + 4×100 + 0×10 + 6','Tres mil cuatrocientos seis'],['72 018','7×10 000 + 2×1000 + 0×100 + 1×10 + 8','Setenta y dos mil dieciocho']], [2.3*cm,7.7*cm,5*cm]))
    story += [PageBreak()]
    story += section('3  El ábaco', [p('El ábaco es un instrumento de conteo y cálculo. Cada columna representa un valor posicional: unidades, decenas, centenas y millares. Una ficha colocada en una columna vale tantas unidades como indica esa posición.')])
    story.append(table([['Columna','Millares','Centenas','Decenas','Unidades'],['Valor de una ficha','1000','100','10','1'],['Ejemplo para 2 431','2 fichas','4 fichas','3 fichas','1 ficha']], [3*cm,3*cm,3*cm,3*cm,3*cm]))
    story += [p('Para sumar', 'H2x'), p('Representa el primer número, agrega las fichas del segundo y realiza agrupaciones: diez unidades se cambian por una decena; diez decenas por una centena.'), p('Para restar', 'H2x'), p('Retira fichas. Cuando no hay suficientes, cambia una ficha de la columna siguiente por diez fichas de la columna actual.')]
    story += [p('Comprueba tu aprendizaje', 'H2x')] + bullets(['Representa 1 205 y explica la función del cero.', 'Representa 368 y agrega 147 realizando los cambios necesarios.', 'Explica una ventaja del ábaco frente a contar solamente con los dedos.'])
    doc(OUT/'PEAR_Proposito_1.2_Material_didactico.pdf','Propósito 1.2  Historia del conteo y el ábaco','Guía didáctica para estudiar los sistemas de conteo, el cero, los números naturales y el funcionamiento del ábaco.','MATERIAL DIDÁCTICO 1.2',story)

def activity_12():
    story=[]
    story += section('Actividad', [p('Construye un ábaco físico funcional utilizando principalmente materiales reciclables. Entrega el modelo acompañado de una explicación breve y evidencia fotográfica.')])
    story += section('Instrucciones', bullets(['Construye una estructura estable con al menos cuatro columnas: unidades, decenas, centenas y millares.', 'Coloca diez fichas móviles en cada columna. Deben desplazarse con facilidad.', 'Rotula cada posición y usa materiales reciclables de forma visible.', 'Utiliza el ábaco para representar dos cantidades y resolver una suma o una resta.', 'Prepara una explicación de una página con: materiales empleados, funcionamiento, utilidad y procedimiento de la operación.', 'Toma tres fotografías claras: vista completa, detalle de columnas y operación representada.', 'Sube a Aula Virtual un solo archivo PDF con la explicación y las fotografías. Conserva el modelo para presentarlo en clase.']))
    story += [p('Datos de entrega', 'H1x')]
    story.append(table([['Elemento','Indicación'],['Producto','Ábaco físico y evidencia en PDF'],['Trabajo','Individual'],['Valor','5%'],['Nombre del archivo','PEAR_111_Apellido_Nombre_1.2.pdf']], [4*cm,11*cm]))
    story += [p('Antes de entregar', 'H1x')] + bullets(['El ábaco se sostiene, sus fichas se mueven y las columnas están rotuladas.', 'La operación coincide con la cantidad representada y las fotografías permiten comprobarla.', 'La explicación está redactada con palabras propias.', 'El PDF abre correctamente y tiene el nombre solicitado.'])
    doc(OUT/'PEAR_Actividad_evaluacion_1.2.pdf','Actividad de evaluación 1.2  Construcción de un ábaco','Instrucciones directas para elaborar, comprobar y documentar un modelo físico de ábaco.','ACTIVIDAD DE EVALUACIÓN 1.2',story)

def material_13():
    story=[]
    story += section('Qué aprenderás', [p('Clasificarás números, realizarás operaciones con enteros, reconocerás sus propiedades y aplicarás factorización, máximo común divisor y mínimo común múltiplo en decisiones cotidianas.')])
    story += bullets(['Clasificar números reales.', 'Relacionar operaciones directas e inversas.', 'Usar propiedades para simplificar cálculos.', 'Descomponer números en factores primos.', 'Elegir entre MCD y MCM según la situación.'])
    story += [PageBreak()]
    story += section('1  Clasificación de los números reales', [p('Los conjuntos numéricos están relacionados: cada número natural es entero, cada entero es racional y todo racional es real.')])
    story.append(table([['Conjunto','Descripción','Ejemplos'],['Naturales N','Conteo de elementos.','0, 1, 2, 3, 4'],['Enteros Z','Naturales, sus opuestos y cero.','-8, -1, 0, 6'],['Racionales Q','Pueden escribirse como fracción de enteros.','3/4, -2, 0.25'],['Irracionales I','Decimales infinitos no periódicos.','√2, π'],['Reales R','Reúnen racionales e irracionales.','Todos los anteriores']], [3.1*cm,7.4*cm,4.5*cm]))
    story += [p('Para clasificar', 'H2x')] + bullets(['Identifica primero el conjunto más pequeño al que pertenece.', 'Un decimal exacto o periódico es racional.', 'Una raíz no exacta puede ser irracional.'])
    story += [PageBreak()]
    story += section('2  Operaciones e inversas', [p('La suma y la resta son operaciones inversas; la multiplicación y la división también. Una operación inversa permite comprobar o deshacer otra.')])
    story.append(table([['Operación','Inversa','Comprobación'],['27 + 18 = 45','45 - 18 = 27','La resta recupera el dato inicial.'],['12 × 7 = 84','84 ÷ 7 = 12','La división recupera el factor.']], [4*cm,4*cm,7*cm]))
    story += [p('Propiedades', 'H2x')]
    story.append(table([['Propiedad','Forma general','Ejemplo'],['Cerradura','a y b del conjunto ⇒ resultado en el conjunto','-3 + 8 = 5'],['Conmutativa','a + b = b + a; ab = ba','4 + 9 = 9 + 4'],['Asociativa','(a+b)+c = a+(b+c)','(2+3)+7 = 2+(3+7)'],['Distributiva','a(b+c)=ab+ac','6(10+2)=60+12'],['Neutro','a+0=a; a×1=a','25+0=25'],['Inverso','a+(-a)=0; a×1/a=1','9+(-9)=0']], [3*cm,6.2*cm,5.8*cm]))
    story += [PageBreak()]
    story += section('3  Factorización prima', [p('Todo número natural mayor que 1 puede expresarse de manera única como producto de números primos, sin considerar el orden. Esta idea se conoce como teorema fundamental de la aritmética.')])
    story += [p('Ejemplo  84', 'H2x'), p('84 = 2 × 42 = 2 × 2 × 21 = 2² × 3 × 7. Un árbol de factores puede tener distintas ramas, pero termina en los mismos factores primos.'), p('Procedimiento', 'H2x')] + bullets(['Divide entre el menor número primo posible.', 'Continúa con el cociente.', 'Detente cuando el cociente sea 1.', 'Escribe el producto usando exponentes cuando un factor se repita.'])
    story += [p('Practica', 'H2x'), p('Descompón 72, 90 y 126 en factores primos. Después comprueba multiplicando los factores.')]
    story += [PageBreak()]
    story += section('4  Máximo común divisor y mínimo común múltiplo', [p('<b>MCD</b> es el mayor número que divide exactamente a dos o más cantidades. Se usa para formar grupos iguales o dividir sin sobrantes. <b>MCM</b> es el menor múltiplo positivo común. Se usa para sincronizar eventos o calcular cuándo volverán a coincidir.')])
    story.append(table([['Situación','Conviene usar','Razón'],['Repartir 24 jabones y 36 toallas en paquetes iguales sin sobrantes.','MCD','Se busca el mayor tamaño común de agrupación.'],['Una revisión ocurre cada 6 días y otra cada 8 días.','MCM','Se busca cuándo coinciden nuevamente.']], [8*cm,3*cm,4*cm]))
    story += [p('Ejemplo con 24 y 36', 'H2x'), p('24 = 2³ × 3 y 36 = 2² × 3². Para el MCD se toman los factores comunes con menor exponente: 2² × 3 = 12. Para el MCM se toman todos con mayor exponente: 2³ × 3² = 72.')]
    story += [PageBreak()]
    story += section('5  Matemáticas para un presupuesto saludable', [p('Un presupuesto organiza ingresos, gastos y ahorro. Las operaciones permiten obtener totales y saldos; la factorización ayuda a comparar agrupaciones; el MCD sirve para formar paquetes iguales y el MCM para planear compras periódicas.')])
    story.append(table([['Concepto','Cálculo','Interpretación'],['Ingresos totales','Suma de entradas de dinero','Recursos disponibles'],['Egresos totales','Suma de gastos','Dinero utilizado'],['Saldo','Ingresos - egresos','Cantidad disponible o faltante'],['Porcentaje destinado','Gasto ÷ ingreso × 100','Proporción del ingreso']], [4*cm,5*cm,6*cm]))
    story += [p('Ejemplo breve', 'H2x'), p('Una familia dispone de $8 000 y planea $2 400 en alimentación, $600 en higiene, $500 en medicina tradicional y $3 200 en otros gastos. Egresos: $6 700. Saldo: $1 300. La decisión final debe explicar si el presupuesto es equilibrado y qué ajuste sería responsable.')]
    story += [p('Practica sin respuestas', 'H2x')] + bullets(['Clasifica: -12, 7, 2/5, √5 y 0.', 'Descompón 180 y 252 en factores primos.', 'Decide si una situación de agrupación requiere MCD o MCM.', 'Diseña un presupuesto y comprueba cada total con la operación inversa.'])
    doc(OUT/'PEAR_Proposito_1.3_Material_didactico.pdf','Propósito 1.3  Números, operaciones y presupuesto','Guía didáctica para clasificar números y aplicar operaciones, propiedades, factorización, MCD y MCM.','MATERIAL DIDÁCTICO 1.3',story)

def activity_13():
    story=[]
    story += section('Actividad', [p('Elabora un reporte de presupuesto que integre alimentación, higiene y una práctica cultural de salud comunitaria. Deberás justificar las operaciones utilizadas y explicar si el presupuesto es equilibrado.')])
    story += section('Instrucciones', bullets(['Registra el caso asignado en Aula Virtual: ingreso disponible, número de integrantes y periodicidad.', 'Incluye al menos tres prácticas de salud: alimentación, higiene y una práctica cultural o comunitaria.', 'Organiza los gastos en una tabla con concepto, cantidad, precio unitario, frecuencia y subtotal.', 'Calcula ingresos, egresos y saldo. Comprueba al menos un cálculo con su operación inversa.', 'Selecciona tres cantidades del presupuesto y realiza su factorización prima.', 'Plantea una situación real del presupuesto que se resuelva con MCD y otra con MCM. Explica por qué elegiste cada uno.', 'Clasifica cinco números usados en el reporte como naturales, enteros, racionales o reales.', 'Redacta una conclusión: indica si el presupuesto es equilibrado y propone un ajuste responsable.', 'Entrega un solo archivo PDF en Aula Virtual.']))
    story += [p('Estructura del reporte', 'H1x')]
    story.append(table([['Sección','Contenido mínimo'],['1  Datos del caso','Ingreso, integrantes y periodo.'],['2  Presupuesto','Tabla completa, egresos y saldo.'],['3  Operaciones','Procedimientos y comprobaciones.'],['4  Factorización, MCD y MCM','Descomposición y dos aplicaciones justificadas.'],['5  Clasificación','Cinco números y conjunto correspondiente.'],['6  Conclusión','Análisis y propuesta de ajuste.']], [4.2*cm,10.8*cm]))
    story += [p('Datos de entrega', 'H1x')]
    story.append(table([['Elemento','Indicación'],['Producto','Reporte en PDF'],['Trabajo','Individual'],['Valor','10%'],['Nombre del archivo','PEAR_111_Apellido_Nombre_1.3.pdf']], [4*cm,11*cm]))
    story += [p('Antes de entregar', 'H1x')] + bullets(['Todos los subtotales y totales coinciden.', 'Se muestran procedimientos, no solo resultados.', 'El MCD y el MCM responden a situaciones distintas.', 'La conclusión utiliza los resultados del presupuesto.', 'El texto está escrito con palabras propias.', 'El PDF abre correctamente y tiene el nombre solicitado.'])
    doc(OUT/'PEAR_Actividad_evaluacion_1.3.pdf','Actividad de evaluación 1.3  Presupuesto de salud comunitaria','Instrucciones para integrar conteo, operaciones, propiedades, factorización, MCD y MCM en un presupuesto.','ACTIVIDAD DE EVALUACIÓN 1.3',story)

if __name__ == '__main__':
    material_11(); activity_11(); material_12(); activity_12(); material_13(); activity_13()
    for item in sorted(OUT.glob('*.pdf')): print(item)
