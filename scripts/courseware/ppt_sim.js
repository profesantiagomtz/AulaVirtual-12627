// Presentación simulada (como PowerPoint) para practicar diseño, formato, objetos, animaciones y transiciones: nada sale de este navegador.
var PC={},PS={};
var PTHEME={"":{n:"Blanco",bg:"#ffffff",fg:"#111827",ac:"#2563eb",ff:"Calibri"},oc:{n:"Océano",bg:"linear-gradient(135deg,#0c4a6e,#0369a1)",fg:"#ffffff",ac:"#7dd3fc",ff:"Segoe UI"},bo:{n:"Bosque",bg:"#ecfdf5",fg:"#064e3b",ac:"#059669",ff:"Georgia"},at:{n:"Atardecer",bg:"linear-gradient(135deg,#fde68a,#fb923c)",fg:"#431407",ac:"#9a3412",ff:"Verdana"}};
var PLAY={tit:"Diapositiva de título",tc:"Título y objetos",dos:"Dos objetos",sec:"Encabezado de sección",sol:"Solo el título",bla:"En blanco"};
var PFF=["Calibri","Arial","Verdana","Georgia","Segoe UI"];
var PBG={"":"Del tema","#ffffff":"Blanco","#fef9c3":"Amarillo claro","#dbeafe":"Azul claro","#dcfce7":"Verde claro","#1e293b":"Azul noche"};
var PFC={"":"Del tema","#111827":"Negro","#1e3a8a":"Azul","#b91c1c":"Rojo","#15803d":"Verde","#ffffff":"Blanco"};
var POBJ={txt:["🔤","Cuadro de texto"],tbl:["▦","Tabla"],img:["🖼️","Imagen"],lnk:["🔗","Hipervínculo"],vid:["🎬","Video"],aud:["🔊","Audio"],doc:["📄","Documento de Word"],xls:["📊","Hoja de cálculo"],ppt:["📽️","Presentación"]};
var PAN={"":"Ninguna",ap:"Entrada · Aparecer",de:"Entrada · Desvanecer",vu:"Entrada · Entrar volando",zo:"Entrada · Zoom",ba:"Entrada · Barrido",pu:"Énfasis · Pulso",gi:"Énfasis · Girar",ds:"Salida · Desaparecer",sv:"Salida · Salir volando"};
var PTR={"":"Ninguna",de:"Desvanecer",em:"Empujar",ba:"Barrido",cu:"Cubrir",tr:"Transformación"};
var PSND={"":"Sin sonido",apl:"Aplauso",cam:"Cámara",vie:"Viento"};
var PSZ={s:"Pequeño",m:"Mediano",l:"Grande"},PPOS={i:"Izquierda",c:"Centro",d:"Derecha",ar:"Arriba",ab:"Abajo"};
var PFILL={"":"Sin relleno","#dbeafe":"Azul claro","#dcfce7":"Verde claro","#fef9c3":"Amarillo","#fee2e2":"Rosa"};
function pEsc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;")}
function pSlide(o){o=o||{};return {lay:o.lay||"tc",t:o.t||"",b:o.b||"",n:o.n||"",bg:o.bg||"",ff:o.ff||"",sz:o.sz||0,fb:!!o.fb,fc:o.fc||"",al:o.al||"",ls:o.ls||1,vi:o.vi!==false,objs:(o.objs||[]).map(function(x){return pObj(x.k,x)}),tr:o.tr||{fx:"",dur:1,snd:"",clic:true,aft:0}}}
function pObj(k,o){o=o||{};return {k:k,lb:o.lb||POBJ[k][1],url:o.url||"",r:o.r||3,c:o.c||3,sz:o.sz||"m",pos:o.pos||"c",fill:o.fill||"",an:o.an||{fx:"",st:"clic",dur:0.5}}}
function pNew(id){var c=PC[id];return {slides:(c.slides||[{lay:"tit"}]).map(pSlide),cur:0,sel:-1,theme:c.theme||"",size:c.size||"16:9",or:"h",view:"nor",tab:(c.tabs||["ini"])[0],master:{ft:"",logo:false},used:{},show:null}}
function pGet(id){if(!PS[id]){var s=null;try{s=JSON.parse(localStorage.getItem(KEY+"-pp-"+id)||"null")}catch(e){}PS[id]=s&&s.slides?s:pNew(id)}return PS[id]}
function pSave(id){try{var S=PS[id],sh=S.show;S.show=null;localStorage.setItem(KEY+"-pp-"+id,JSON.stringify(S));S.show=sh}catch(e){}}
function pTh(S){return PTHEME[S.theme]||PTHEME[""]}
function pRatio(S){var r=S.size=="4:3"?[4,3]:[16,9];return S.or=="v"?r[1]+"/"+r[0]:r[0]+"/"+r[1]}
function pObjHtml(x,i,S,sel){var w={s:22,m:34,l:48}[x.sz]||34,p={i:"left:4%;top:38%",c:"left:"+(50-w/2)+"%;top:40%",d:"right:4%;top:38%",ar:"left:"+(50-w/2)+"%;top:6%",ab:"left:"+(50-w/2)+"%;bottom:10%"}[x.pos]||"",in_='';
 if(x.k=="tbl"){in_='<table>';for(var r=0;r<Math.min(x.r,5);r++){in_+='<tr>';for(var c=0;c<Math.min(x.c,5);c++)in_+=(r==0?'<th>':'<td>')+(r==0?'Col '+(c+1):'')+(r==0?'</th>':'</td>');in_+='</tr>'}in_+='</table>'}
 else if(x.k=="lnk")in_='<u>'+pEsc(x.lb)+'</u>'+(x.url?'<small>'+pEsc(x.url)+'</small>':'');
 else if(x.k=="txt")in_='<b class="ptx">'+pEsc(x.lb)+'</b>';
 else in_='<span class="pic">'+POBJ[x.k][0]+'</span><small>'+pEsc(x.lb)+'</small>';
 return '<div class="pob'+(sel?' on':'')+(x.an.fx?' anm':'')+'" data-o="'+i+'" style="'+p+';width:'+w+'%;'+(x.fill?'background:'+x.fill+';':'')+'">'+in_+(x.an.fx?'<i class="pbadge">★</i>':'')+'</div>'}
function pRender(S,sl,mini,selObj){var th=pTh(S),bg=sl.bg||th.bg,fg=sl.fc||th.fg,ff=sl.ff||th.ff,sz=sl.sz||0,h='<div class="pstg'+(mini?' mini':'')+'" style="aspect-ratio:'+pRatio(S)+';background:'+bg+';color:'+fg+';font-family:'+ff+',Arial,sans-serif">';
 var tsz=sl.lay=="tit"||sl.lay=="sec"?"2.1em":"1.5em",bs=sz?(sz/18)+"em":"1em",al=sl.al?({l:"left",c:"center",r:"right"})[sl.al]:(sl.lay=="tit"||sl.lay=="sec"?"center":"left");
 if(sl.lay!="bla")h+='<div class="ptt" style="font-size:'+tsz+';text-align:'+al+';color:'+(sl.fc||th.ac)+';'+(sl.lay=="tit"||sl.lay=="sec"?'top:30%':'top:6%')+'">'+(pEsc(sl.t)||(mini?'':'<span class="pph">Haz clic para agregar título</span>'))+'</div>';
 if(sl.lay=="tc"||sl.lay=="dos"||sl.lay=="tit"){var lines=String(sl.b||"").split("\n").filter(function(l){return l.trim()}),bh;
  if(sl.lay=="tit")bh='<div class="psub" style="text-align:'+al+'">'+(lines.map(pEsc).join("<br>")||(mini?'':'<span class="pph">Subtítulo</span>'))+'</div>';
  else bh='<div class="pbd'+(sl.lay=="dos"?' half':'')+'" style="font-size:'+bs+';text-align:'+al+';line-height:'+(1.25*sl.ls)+';'+(sl.fb?'font-weight:700;':'')+'">'+(lines.length?(sl.vi?'<ul>'+lines.map(function(l){return '<li>'+pEsc(l)+'</li>'}).join("")+'</ul>':lines.map(pEsc).join("<br>")):(mini?'':'<span class="pph">Haz clic para agregar texto</span>'))+'</div>';
  h+=bh}
 if(sl.lay=="sec"&&sl.b)h+='<div class="psub" style="top:52%;text-align:center">'+pEsc(sl.b)+'</div>';
 sl.objs.forEach(function(x,i){h+=pObjHtml(x,i,S,!mini&&selObj===i)});
 if(S.master.ft||S.master.logo)h+='<div class="pft">'+(S.master.logo?'<b>🏫</b> ':'')+pEsc(S.master.ft)+'</div>';
 return h+'</div>'}
function pApi(S){return {sl:S.slides,n:S.slides.length,s:function(i){return S.slides[i]||pSlide()},theme:S.theme,size:S.size,or:S.or,view:S.view,master:S.master,used:S.used,
 objs:function(k){var n=0;S.slides.forEach(function(s){s.objs.forEach(function(x){if(!k||x.k==k)n++})});return n},
 every:function(f){return S.slides.every(f)},some:function(f){return S.slides.some(f)},
 anims:function(){var n=0;S.slides.forEach(function(s){s.objs.forEach(function(x){if(x.an.fx)n++})});return n},
 obj:function(f){return S.slides.some(function(s){return s.objs.some(f)})}}}
function pTasks(id){var S=pGet(id),a=pApi(S);return PC[id].tasks.map(function(t){var ok=false;try{ok=!!t[1](a)}catch(e){}return {text:t[0],ok:ok}})}
function pOpt(o,v){return Object.keys(o).map(function(k){return '<option value="'+k+'"'+(String(k)===String(v)?' selected':'')+'>'+o[k]+'</option>'}).join("")}
function pArr(a,v){return a.map(function(k){return '<option'+(String(k)===String(v)?' selected':'')+'>'+k+'</option>'}).join("")}
function pRibbon(S){var sl=S.slides[S.cur],t=S.tab,x=S.sel>-1?sl.objs[S.sel]:null,o='';
 if(t=="arc")o='<div class="xgp"><small>Presentar</small><button type="button" data-p="show">▶ Desde el principio</button></div><div class="xgp"><small>Plantillas</small><button type="button" data-p="potx">💾 Guardar como plantilla (.potx)</button></div><div class="xgp"><small>Exportar video</small><select data-p="res" aria-label="Resolución">'+pOpt({"":"Resolución…","720":"HD (720p)","1080":"Full HD (1080p)"},S.used.res||"")+'</select></div><div class="xgp"><small>Ayuda</small><button type="button" data-p="help">❓ Ayuda (F1)</button></div>';
 if(t=="ini")o='<div class="xgp"><small>Diapositivas</small><select data-p="add" aria-label="Nueva diapositiva"><option value="">➕ Nueva diapositiva…</option>'+pOpt(PLAY,"")+'</select><select data-p="lay" aria-label="Diseño de la diapositiva">'+pOpt(PLAY,sl.lay)+'</select><button type="button" data-p="mvu" title="Subir diapositiva">▲ Subir</button><button type="button" data-p="mvd" title="Bajar diapositiva">▼ Bajar</button><button type="button" data-p="dup">Duplicar</button><button type="button" data-p="del">Eliminar</button></div>'
  +'<div class="xgp"><small>Fuente</small><select data-p="ff" aria-label="Fuente">'+pArr(["(Del tema)"].concat(PFF),sl.ff||"(Del tema)")+'</select><select data-p="sz" aria-label="Tamaño">'+pArr(["(Auto)",14,18,20,24,28,32],sl.sz||"(Auto)")+'</select><button type="button" data-p="fb" class="'+(sl.fb?"on":"")+'"><b>N</b></button><select data-p="fc" aria-label="Color de fuente">'+pOpt(PFC,sl.fc)+'</select></div>'
  +'<div class="xgp"><small>Párrafo</small><button type="button" data-p="al" data-v="l" class="'+(sl.al=="l"?"on":"")+'">⇤</button><button type="button" data-p="al" data-v="c" class="'+(sl.al=="c"?"on":"")+'">↔</button><button type="button" data-p="al" data-v="r" class="'+(sl.al=="r"?"on":"")+'">⇥</button><button type="button" data-p="vi" class="'+(sl.vi?"on":"")+'">• Viñetas</button><select data-p="ls" aria-label="Interlineado">'+pOpt({1:"Interlineado 1.0",1.5:"Interlineado 1.5",2:"Interlineado 2.0"},sl.ls)+'</select></div>';
 if(t=="ins")o='<div class="xgp"><small>Insertar en la diapositiva '+(S.cur+1)+'</small>'+["txt","tbl","img","lnk","vid","aud"].map(function(k){return '<button type="button" data-p="ins" data-v="'+k+'">'+POBJ[k][0]+' '+POBJ[k][1]+'</button>'}).join("")+'</div><div class="xgp"><small>Objeto</small><select data-p="insobj" aria-label="Insertar objeto"><option value="">Otro archivo…</option><option value="doc">Documento de Word</option><option value="xls">Hoja de cálculo</option><option value="ppt">Otra presentación</option></select></div>';
 if(t=="dis")o='<div class="xgp"><small>Temas</small>'+Object.keys(PTHEME).map(function(k){var q=PTHEME[k];return '<button type="button" data-p="th" data-v="'+k+'" class="'+(S.theme===k?"on":"")+'" style="background:'+q.bg+';color:'+q.fg+'">'+q.n+'</button>'}).join("")+'</div><div class="xgp"><small>Personalizar</small><select data-p="size" aria-label="Tamaño de diapositiva">'+pOpt({"16:9":"Tamaño: Panorámica 16:9","4:3":"Tamaño: Estándar 4:3"},S.size)+'</select><select data-p="or" aria-label="Orientación">'+pOpt({h:"Orientación: Horizontal",v:"Orientación: Vertical"},S.or)+'</select><select data-p="bg" aria-label="Formato del fondo">'+pOpt(PBG,sl.bg)+'</select><button type="button" data-p="bgall">Aplicar fondo a todas</button></div>';
 if(t=="for")o=x?'<div class="xgp"><small>'+POBJ[x.k][1]+' seleccionado</small><select data-p="osz" aria-label="Tamaño">'+pOpt(PSZ,x.sz)+'</select><select data-p="opos" aria-label="Posición">'+pOpt(PPOS,x.pos)+'</select><select data-p="ofill" aria-label="Relleno">'+pOpt(PFILL,x.fill)+'</select><button type="button" data-p="odel">Eliminar objeto</button></div>':'<div class="xgp"><small>Formato de forma</small><span class="pmsg">Primero da clic en un objeto de la diapositiva.</span></div>';
 if(t=="ani")o=x?'<div class="xgp"><small>Animación de: '+pEsc(x.lb)+'</small><select data-p="afx" aria-label="Efecto">'+pOpt(PAN,x.an.fx)+'</select><select data-p="ast" aria-label="Inicio">'+pOpt({clic:"Inicio: Al hacer clic",con:"Inicio: Con la anterior",des:"Inicio: Después de la anterior"},x.an.st)+'</select><select data-p="adur" aria-label="Duración">'+pOpt({0.5:"Duración 0.5 s",1:"Duración 1 s",2:"Duración 2 s"},x.an.dur)+'</select><button type="button" data-p="aprev">▶ Vista previa</button></div>':'<div class="xgp"><small>Animaciones</small><span class="pmsg">Primero da clic en un objeto de la diapositiva.</span></div>';
 if(t=="ani"){var pa=sl.objs.map(function(y,i){return y.an.fx?'<li>'+(y.an.st=="clic"?"🖱️":y.an.st=="con"?"⇉":"⏱️")+' '+pEsc(y.lb)+' · '+PAN[y.an.fx]+'</li>':''}).join("");o+='<div class="xgp xwide"><small>Panel de animación</small><ol class="ppa">'+(pa||'<li>Sin animaciones en esta diapositiva.</li>')+'</ol></div>'}
 if(t=="tra")o='<div class="xgp"><small>Transición de la diapositiva '+(S.cur+1)+'</small><select data-p="tfx" aria-label="Efecto de transición">'+pOpt(PTR,sl.tr.fx)+'</select><select data-p="tdur" aria-label="Duración">'+pOpt({0.5:"Duración 0.5 s",1:"Duración 1 s",2:"Duración 2 s"},sl.tr.dur)+'</select><select data-p="tsnd" aria-label="Sonido">'+pOpt(PSND,sl.tr.snd)+'</select><button type="button" data-p="tprev">▶ Vista previa</button></div><div class="xgp"><small>Avanzar a la diapositiva</small><label class="xck"><input type="checkbox" data-p="tclic"'+(sl.tr.clic?" checked":"")+'> Al hacer clic</label><select data-p="taft" aria-label="Después de">'+pOpt({0:"Después de: —",3:"Después de: 3 s",5:"Después de: 5 s",10:"Después de: 10 s"},sl.tr.aft)+'</select><button type="button" data-p="tall">Aplicar a todas</button></div>';
 if(t=="vis")o='<div class="xgp"><small>Vistas de presentación</small>'+[["nor","Normal"],["esq","Esquema"],["cla","Clasificador de diapositivas"],["not","Página de notas"],["lec","Vista de lectura"]].map(function(v){return '<button type="button" data-p="view" data-v="'+v[0]+'" class="'+(S.view==v[0]?"on":"")+'">'+v[1]+'</button>'}).join("")+'</div><div class="xgp"><small>Vistas patrón</small><button type="button" data-p="view" data-v="pat" class="'+(S.view=="pat"?"on":"")+'">Patrón de diapositivas</button></div>';
 return o}
function pEditor(S){var sl=S.slides[S.cur],x=S.sel>-1?sl.objs[S.sel]:null,h='<div class="ped">';
 if(S.view=="pat")return h+'<b>Patrón de diapositivas</b> (lo que pongas aquí aparece en <b>todas</b> las diapositivas)<label>Pie de página del patrón<input data-e="mft" value="'+pEsc(S.master.ft)+'" placeholder="Ej. CONALEP · EDOA · Grupo 311"></label><label class="xck"><input type="checkbox" data-e="mlogo"'+(S.master.logo?" checked":"")+'> Logotipo de la escuela en cada diapositiva</label><button type="button" class="btn ghost sm" data-p="view" data-v="nor">Cerrar vista Patrón</button></div>';
 if(sl.lay!="bla")h+='<label>Título<input data-e="t" value="'+pEsc(sl.t)+'" placeholder="Escribe el título"></label>';
 if(sl.lay!="bla"&&sl.lay!="sol")h+='<label>'+(sl.lay=="tit"||sl.lay=="sec"?"Subtítulo":"Texto (un punto por renglón)")+'<textarea data-e="b" rows="3" placeholder="Escribe aquí">'+pEsc(sl.b)+'</textarea></label>';
 if(x&&(x.k=="txt"||x.k=="lnk"||x.k=="img"||x.k=="vid"||x.k=="aud"))h+='<label>'+(x.k=="lnk"?"Texto del vínculo":x.k=="txt"?"Texto del cuadro":"Descripción del "+POBJ[x.k][1].toLowerCase())+'<input data-e="olb" value="'+pEsc(x.lb)+'"></label>'+(x.k=="lnk"?'<label>Dirección (URL)<input data-e="ourl" value="'+pEsc(x.url)+'" placeholder="https://…"></label>':'');
 if(x&&x.k=="tbl")h+='<label>Tabla<span class="prc"><select data-e="or_" aria-label="Filas">'+pArr([2,3,4,5],x.r)+'</select> filas × <select data-e="oc_" aria-label="Columnas">'+pArr([2,3,4,5],x.c)+'</select> columnas</span></label>';
 h+='<label>Notas del orador'+(S.view=="not"?' (vista Página de notas)':'')+'<textarea data-e="n" rows="2" placeholder="Lo que vas a decir al exponer esta diapositiva">'+pEsc(sl.n)+'</textarea></label>';
 return h+'</div>'}
function pPaint(d){var b=d.querySelector(".pptsim"),id=b.dataset.id,S=pGet(id);if(S.cur>=S.slides.length)S.cur=S.slides.length-1;var sl=S.slides[S.cur];if(S.sel>=sl.objs.length)S.sel=-1;
 b.querySelectorAll(".ptabs button").forEach(function(x){x.className=x.dataset.t==S.tab?"on":""});
 b.querySelector(".xrb").innerHTML=pRibbon(S);
 var th=S.slides.map(function(s,i){return '<button type="button" class="pth'+(i==S.cur?' on':'')+'" data-s="'+i+'"><b>'+(i+1)+'</b>'+pRender(S,s,true)+(s.tr.fx?'<i class="ptr">✦</i>':'')+'</button>'}).join(""),main;
 if(S.view=="esq")main='<div class="pesq">'+S.slides.map(function(s,i){return '<div class="'+(i==S.cur?'on':'')+'" data-s="'+i+'"><b>'+(i+1)+'. '+(pEsc(s.t)||'(sin título)')+'</b>'+String(s.b||"").split("\n").filter(function(l){return l.trim()}).map(function(l){return '<span>• '+pEsc(l)+'</span>'}).join("")+'</div>'}).join("")+'</div>';
 else if(S.view=="cla")main='<div class="pcla">'+th+'</div>';
 else main=pRender(S,sl,false,S.sel)+(S.view=="not"?'<div class="pnot"><b>Notas:</b> '+(pEsc(sl.n)||'<i>(escribe tus notas abajo)</i>')+'</div>':'');
 b.querySelector(".pwk").className="pwk v-"+S.view;
 b.querySelector(".pside").innerHTML=S.view=="cla"||S.view=="lec"?'':th;
 b.querySelector(".pmain").innerHTML=main;
 var ed=b.querySelector(".pedw");if(!ed.contains(document.activeElement))ed.innerHTML=S.view=="lec"||S.view=="cla"||S.view=="esq"?'<p class="pmsg">Vista '+({lec:"de lectura",cla:"Clasificador",esq:"Esquema"})[S.view]+': regresa a <b>Vista › Normal</b> para escribir.</p>':pEditor(S);
 b.querySelector(".pst").textContent="Diapositiva "+(S.cur+1)+" de "+S.slides.length+" · "+PTHEME[S.theme].n+" · "+S.size+(S.or=="v"?" vertical":"");
 pShow(b,S);
 var ts=pTasks(id);b.querySelector(".xts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("");return ts}
function pSteps(sl){var st=[];sl.objs.forEach(function(x,i){if(!x.an.fx)return;if(x.an.st=="clic"||!st.length)st.push([i]);else st[st.length-1].push(i)});return st}
function pShow(b,S){var ov=b.querySelector(".pshow");if(!S.show){ov.hidden=true;ov.innerHTML="";return}
 var q=S.show,sl=S.slides[q.i],steps=pSteps(sl),vis={},html;
 steps.forEach(function(g,k){g.forEach(function(i){var fx=sl.objs[i].an.fx,ent=["ap","de","vu","zo","ba"].indexOf(fx)>-1;vis[i]=k<q.k?(fx=="ds"||fx=="sv"?"gone":"shown"):(ent?"hidden":"");if(k==q.k-1)vis[i]+=" pa-"+fx})});
 html=pRender(S,sl,false,-1);
 ov.hidden=false;ov.innerHTML='<div class="pshw tr-'+(q.k==0?sl.tr.fx:"")+'" style="--d:'+sl.tr.dur+'s">'+html+'</div><div class="pshb"><span>'+(q.i+1)+' / '+S.slides.length+(sl.tr.snd&&q.k==0?' · 🔊 '+PSND[sl.tr.snd]:'')+(steps.length>q.k?' · clic: siguiente animación':'')+'</span><button type="button" class="btn ghost sm pnx">Siguiente ▶</button><button type="button" class="btn ghost sm pxx">Salir</button></div>';
 ov.querySelectorAll(".pob").forEach(function(e){var i=+e.dataset.o,v=vis[i]||"",x=sl.objs[i];e.className+=" "+v;e.style.setProperty("--ad",x.an.dur+"s")});
 if(q.tm)clearTimeout(q.tm);if(sl.tr.aft&&q.k>=steps.length)q.tm=setTimeout(function(){pNext(b,S)},sl.tr.aft*1000)}
function pNext(b,S){var q=S.show;if(!q)return;if(q.tm){clearTimeout(q.tm);q.tm=0}var sl=S.slides[q.i];if(q.k<pSteps(sl).length)q.k++;else if(q.i<S.slides.length-1){q.i++;q.k=0}else{S.show=null;S.used.showEnd=1;pSave(b.dataset.id)}pShow(b,S)}
function pDo(d,act,val,el){var b=d.querySelector(".pptsim"),id=b.dataset.id,S=pGet(id),sl=S.slides[S.cur],x=S.sel>-1?sl.objs[S.sel]:null,U=S.used;U[act]=1;
 if(act=="show"){S.show={i:0,k:0};}
 else if(act=="potx"){U.potx=1;alert("Plantilla guardada (simulación): Mi_plantilla.potx. En PowerPoint: Archivo › Guardar como › Plantilla de PowerPoint (.potx).")}
 else if(act=="res"){U.res=val}
 else if(act=="help"){alert("Ayuda de PowerPoint: escribe lo que quieres hacer en el cuadro «Buscar» (o «¿Qué desea hacer?») de la parte de arriba, o pulsa F1.")}
 else if(act=="add"){if(!val)return;S.slides.splice(S.cur+1,0,pSlide({lay:val}));S.cur++;S.sel=-1;U["lay:"+val]=1}
 else if(act=="lay"){sl.lay=val;U["lay:"+val]=1}
 else if(act=="mvu"||act=="mvd"){var to=S.cur+(act=="mvu"?-1:1);if(to<0||to>=S.slides.length)return;var mv=S.slides.splice(S.cur,1)[0];S.slides.splice(to,0,mv);S.cur=to}
 else if(act=="dup"){S.slides.splice(S.cur+1,0,JSON.parse(JSON.stringify(sl)));S.cur++}
 else if(act=="del"){if(S.slides.length<2)return;if(!confirm("¿Eliminar la diapositiva "+(S.cur+1)+"?"))return;S.slides.splice(S.cur,1);S.cur=Math.max(0,S.cur-1);S.sel=-1}
 else if(act=="ff")sl.ff=val=="(Del tema)"?"":val;
 else if(act=="sz")sl.sz=val=="(Auto)"?0:+val;
 else if(act=="fb")sl.fb=!sl.fb;
 else if(act=="fc")sl.fc=val;
 else if(act=="al")sl.al=sl.al==val?"":val;
 else if(act=="vi")sl.vi=!sl.vi;
 else if(act=="ls")sl.ls=+val;
 else if(act=="ins"||act=="insobj"){if(!val)return;var o=pObj(val);if(val=="lnk")o.lb="Más información";sl.objs.push(o);S.sel=sl.objs.length-1;U["ins:"+val]=1}
 else if(act=="th"){S.theme=val;U["th:"+val]=1}
 else if(act=="size")S.size=val;
 else if(act=="or")S.or=val;
 else if(act=="bg")sl.bg=val;
 else if(act=="bgall"){S.slides.forEach(function(s){s.bg=sl.bg})}
 else if(act=="osz"&&x)x.sz=val;
 else if(act=="opos"&&x)x.pos=val;
 else if(act=="ofill"&&x)x.fill=val;
 else if(act=="odel"&&x){sl.objs.splice(S.sel,1);S.sel=-1}
 else if(act=="afx"&&x){x.an.fx=val;U["an:"+val]=1}
 else if(act=="ast"&&x)x.an.st=val;
 else if(act=="adur"&&x)x.an.dur=+val;
 else if(act=="aprev"){S.show={i:S.cur,k:0}}
 else if(act=="tfx"){sl.tr.fx=val;U["tr:"+val]=1}
 else if(act=="tdur")sl.tr.dur=+val;
 else if(act=="tsnd")sl.tr.snd=val;
 else if(act=="tclic")sl.tr.clic=!!el.checked;
 else if(act=="taft")sl.tr.aft=+val;
 else if(act=="tall"){var tr=JSON.stringify(sl.tr);S.slides.forEach(function(s){s.tr=JSON.parse(tr)})}
 else if(act=="tprev"){S.show={i:S.cur,k:0}}
 else if(act=="view"){S.view=val;U["view:"+val]=1}
 pSave(id);pPaint(d)}
function pPpt(ic,t,inf,cfg){K++;PC[cfg.id]=cfg;var tabs=cfg.tabs||["arc","ini","ins","dis","for","tra","ani","vis"],TN={arc:"Archivo",ini:"Inicio",ins:"Insertar",dis:"Diseño",for:"Formato",tra:"Transiciones",ani:"Animaciones",vis:"Vista"};
 return '<article class="lesson"><header><span class="kick">'+ic+' Simulador</span><h1>'+t+'</h1><p class="sub">'+inf+'</p></header><style>'
 +'.pptsim .xts{list-style:none;padding:0;margin:0 0 12px;display:grid;gap:6px}.pptsim .xts li{border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14.5px}.pptsim .xts li.y{border-color:var(--ok);background:var(--ok-soft)}'
 +'.pbook{position:relative;border:1.5px solid #c8ccd2;border-radius:12px;overflow:hidden;background:#fff;color:#1f2937}.ptabs{display:flex;gap:2px;background:#c43e1c;padding:6px 6px 0;overflow-x:auto}.ptabs button{border:0;background:transparent;color:#fde8e1;font:600 13px system-ui;padding:7px 11px;border-radius:7px 7px 0 0;cursor:pointer;white-space:nowrap}.ptabs button.on{background:#f3f4f6;color:#7c2d12}'
 +'.pptsim .xrb{background:#f3f4f6;display:flex;flex-wrap:wrap;gap:6px;padding:8px;border-bottom:1px solid #d1d5db}.pptsim .xgp{display:flex;flex-wrap:wrap;gap:4px;align-items:center;border:1px solid #e5e7eb;background:#fff;border-radius:8px;padding:5px 6px}.pptsim .xgp small{width:100%;font:600 10.5px system-ui;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}.pptsim .xgp.xwide{flex:1 1 100%}'
 +'.pptsim .xrb button,.pptsim .xrb select,.pptsim .ped input,.pptsim .ped textarea,.pptsim .ped select{width:auto;max-width:100%;margin:0;font:13px system-ui;border:1px solid #cbd5e1;background:#fff;color:#111827;border-radius:6px;padding:5px 8px;min-height:32px}.pptsim .xrb button{cursor:pointer}.pptsim .xrb button.on{outline:2px solid #c43e1c;outline-offset:1px}.pptsim .xck{display:flex;gap:6px;align-items:center;font:13px system-ui}.pptsim .xck input{min-height:auto}.pmsg{font:13px system-ui;color:#6b7280}.ppa{margin:0;padding-left:20px;font:13px system-ui}'
 +'.pwk{display:grid;grid-template-columns:96px 1fr;gap:8px;padding:8px;background:#e5e7eb}.pwk.v-cla,.pwk.v-lec,.pwk.v-esq{grid-template-columns:1fr}.pwk.v-cla .pside,.pwk.v-lec .pside{display:none}.pwk.v-esq .pside{display:none}.pside{display:flex;flex-direction:column;gap:6px;max-height:340px;overflow:auto}.pth{position:relative;display:flex;gap:4px;align-items:flex-start;border:2px solid transparent;border-radius:6px;background:none;padding:2px;cursor:pointer}.pth.on{border-color:#c43e1c}.pth>b{font:600 11px system-ui;color:#374151}.pth .pstg{flex:1}.ptr{position:absolute;right:3px;bottom:2px;font-size:10px;color:#c43e1c;font-style:normal}'
 +'.pstg{position:relative;width:100%;border-radius:4px;box-shadow:0 1px 6px rgba(0,0,0,.25);overflow:hidden;font-size:15px}.pstg.mini{font-size:3.4px;box-shadow:0 0 0 1px #9ca3af}.ptt{position:absolute;left:6%;right:6%;font-weight:700;line-height:1.15}.psub{position:absolute;left:10%;right:10%;top:52%;font-size:1.05em;opacity:.85}.pbd{position:absolute;left:6%;right:6%;top:24%;bottom:10%;overflow:hidden}.pbd.half{right:52%}.pbd ul{margin:0;padding-left:1.2em}.pph{opacity:.45;font-weight:400}.pft{position:absolute;left:0;right:0;bottom:2%;text-align:center;font-size:.6em;opacity:.8}'
 +'.pob{position:absolute;border:1.5px dashed rgba(0,0,0,.35);border-radius:6px;padding:.4em;background:rgba(255,255,255,.75);color:#111827;font-size:.75em;text-align:center;cursor:pointer;min-height:2.6em;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px}.pob.on{outline:3px solid #c43e1c}.pob .pic{font-size:1.8em}.pob small{font-size:.85em}.pob .ptx{font-size:1.25em}.pob table{border-collapse:collapse;width:100%}.pob th{background:#c43e1c;color:#fff;font-weight:600}.pob td,.pob th{border:1px solid #9ca3af;height:1.1em;font-size:.8em}.pbadge{position:absolute;top:-.6em;right:-.6em;background:#f59e0b;color:#fff;border-radius:50%;width:1.4em;height:1.4em;font-style:normal;font-size:.9em;line-height:1.4em}.mini .pob{border-width:.5px;padding:0}.mini .pbadge{display:none}'
 +'.pmain{min-width:0}.pnot{background:#fff;border:1px solid #d1d5db;border-radius:6px;padding:8px;margin-top:8px;font:13px system-ui}.pesq{background:#fff;border-radius:6px;padding:10px;font:14px system-ui;display:grid;gap:8px}.pesq div{cursor:pointer;padding:4px 6px;border-radius:6px}.pesq div.on{background:#fde8e1}.pesq span{display:block;padding-left:18px;color:#374151}.pcla{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px}.pcla .pstg.mini{font-size:4.2px}'
 +'.pedw{padding:8px;border-top:1px solid #d1d5db;background:#fff}.ped{display:grid;gap:6px}.ped label{display:grid;gap:3px;font:600 12.5px system-ui;color:#374151}.ped input,.ped textarea{width:100%!important}.prc{display:flex;gap:6px;align-items:center;font-weight:400}.pst{padding:4px 8px;background:#f3f4f6;border-top:1px solid #d1d5db;font:12px system-ui;color:#4b5563}'
 +'.pshow{position:absolute;inset:0;z-index:5;background:#111;display:flex;flex-direction:column;justify-content:center;padding:10px;gap:8px}.pshow[hidden]{display:none}.pshw{max-width:100%;margin:auto;width:100%}.pshb{display:flex;gap:8px;align-items:center;flex-wrap:wrap;color:#e5e7eb;font:13px system-ui}.pshb span{flex:1}.pshb .btn{color:#fff;border-color:rgba(255,255,255,.6);background:transparent}.pshow .pob{cursor:default;border-style:solid;border-color:transparent}.pshow .pbadge{display:none}.pshow .pob.hidden,.pshow .pob.gone{visibility:hidden}'
 +'.pshow .pa-ap{animation:paAp .01s}.pshow .pa-de{animation:paDe var(--ad) ease}.pshow .pa-vu{animation:paVu var(--ad) ease-out}.pshow .pa-zo{animation:paZo var(--ad) ease-out}.pshow .pa-ba{animation:paBa var(--ad) linear}.pshow .pa-pu{animation:paPu var(--ad) ease 2}.pshow .pa-gi{animation:paGi var(--ad) ease}.pshow .pa-ds{animation:paDs var(--ad) forwards;visibility:visible!important}.pshow .pa-sv{animation:paSv var(--ad) ease-in forwards;visibility:visible!important}'
 +'@keyframes paAp{from{opacity:0}}@keyframes paDe{from{opacity:0}}@keyframes paVu{from{transform:translateY(120%);opacity:0}}@keyframes paZo{from{transform:scale(.1);opacity:0}}@keyframes paBa{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}@keyframes paPu{50%{transform:scale(1.15)}}@keyframes paGi{to{transform:rotate(360deg)}}@keyframes paDs{to{opacity:0}}@keyframes paSv{to{transform:translateY(-150%);opacity:0}}'
 +'.pshw.tr-de{animation:paDe var(--d)}.pshw.tr-em{animation:trEm var(--d) ease-out}.pshw.tr-ba{animation:paBa var(--d) linear}.pshw.tr-cu{animation:trCu var(--d) ease-out}.pshw.tr-tr{animation:paZo var(--d) ease}@keyframes trEm{from{transform:translateY(100%)}}@keyframes trCu{from{transform:translateX(100%)}}'
 +'.ptools{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}@media(max-width:560px){.pwk{grid-template-columns:1fr}.pside{flex-direction:row;max-height:none;overflow-x:auto;order:2}.pth{width:84px;flex:none}.pstg{font-size:11px}}'
 +'</style><div class="pptsim" data-id="'+cfg.id+'">'+(cfg.intro?'<p>'+cfg.intro+'</p>':'')+'<h3 style="margin:8px 0">Retos</h3><ol class="xts"></ol>'
 +'<div class="pbook"><div class="ptabs">'+tabs.map(function(k){return '<button type="button" data-t="'+k+'">'+TN[k]+'</button>'}).join("")+'</div><div class="xrb"></div><div class="pwk"><div class="pside"></div><div class="pmain"></div></div><div class="pedw"></div><div class="pst"></div><div class="pshow" hidden></div></div>'
 +'<div class="ptools"><button type="button" class="btn ghost sm prst">↺ Reiniciar</button></div></div>'
 +(cfg.hint?'<p class="take"><b>Pista:</b> '+cfg.hint+'</p>':'')+'<div class="chk"><button class="btn c">Revisar retos</button></div><div class="res" role="status"></div></article>'}
function pptInit(d){var b=d.querySelector(".pptsim"),id=b.dataset.id,S=pGet(id);S.show=null;
 b.querySelector(".ptabs").onclick=function(e){var t=e.target.closest("button");if(!t)return;S.tab=t.dataset.t;S.used["tab:"+S.tab]=1;pSave(id);pPaint(d)};
 var rb=b.querySelector(".xrb");
 rb.onclick=function(e){var t=e.target.closest("button[data-p]");if(t)pDo(d,t.dataset.p,t.dataset.v,t)};
 rb.onchange=function(e){var t=e.target;if(t.dataset.p&&t.tagName!="BUTTON")pDo(d,t.dataset.p,t.value,t)};
 function pick(e){var s=e.target.closest("[data-s]");if(s){S.cur=+s.dataset.s;S.sel=-1;if(S.view=="cla"&&e.detail>1)S.view="nor";pSave(id);pPaint(d);return true}}
 b.querySelector(".pside").onclick=pick;
 b.querySelector(".pmain").onclick=function(e){if(pick(e))return;var o=e.target.closest(".pob");S.sel=o?+o.dataset.o:-1;if(o&&S.tab!="ani"&&S.tab!="for")S.tab="for";pSave(id);pPaint(d)};
 var ed=b.querySelector(".pedw");
 ed.oninput=function(e){var t=e.target,k=t.dataset.e,sl=S.slides[S.cur],x=S.sel>-1?sl.objs[S.sel]:null;if(!k)return;
  if(k=="t"||k=="b"||k=="n")sl[k]=t.value;else if(k=="olb"&&x)x.lb=t.value;else if(k=="ourl"&&x)x.url=t.value.trim();else if(k=="mft")S.master.ft=t.value;else return;S.used["e:"+k]=1;pSave(id);
  var keep=document.activeElement;pPaint(d);if(keep&&ed.contains(keep))keep.focus()};
 ed.onchange=function(e){var t=e.target,k=t.dataset.e,sl=S.slides[S.cur],x=S.sel>-1?sl.objs[S.sel]:null;
  if(k=="mlogo")S.master.logo=!!t.checked;else if(k=="or_"&&x)x.r=+t.value;else if(k=="oc_"&&x)x.c=+t.value;else return;pSave(id);t.blur();pPaint(d)};
 ed.onclick=function(e){var t=e.target.closest("button[data-p]");if(t){t.blur();pDo(d,t.dataset.p,t.dataset.v,t)}};
 ed.onfocusout=function(){setTimeout(function(){if(!ed.contains(document.activeElement))pPaint(d)},0)};
 b.querySelector(".pshow").onclick=function(e){if(e.target.closest(".pxx")){if(S.show&&S.show.tm)clearTimeout(S.show.tm);S.show=null;pPaint(d);return}pNext(b,S)};
 b.querySelector(".prst").onclick=function(){if(!confirm("¿Reiniciar el simulador? Se borra lo que hiciste en esta presentación."))return;PS[id]=pNew(id);pSave(id);pptInit(d)};
 pPaint(d)}
function pptCheck(d){var ts=pPaint(d),ok=ts.filter(function(x){return x.ok}).length,n=ts.length,f=ts.filter(function(x){return !x.ok})[0];return {ok:ok,total:n,msg:ok==n?"¡Todos los retos resueltos! Ahora hazlo en PowerPoint (o Presentaciones de Google) con tu propio tema: es tu práctica.":ok+" de "+n+" retos. Sigue con: «"+f.text.replace(/<[^>]*>/g,"")+"»"}}
