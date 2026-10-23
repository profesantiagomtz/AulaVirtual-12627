// Hoja de cálculo simulada para practicar formato y diseño de página: nada sale de este navegador.
var XC={},XS={},XCOLS="ABCDEFGHIJ";
var XFILL={"":"Sin relleno","#dbeafe":"Azul claro","#dcfce7":"Verde claro","#fef9c3":"Amarillo","#e5e7eb":"Gris","#1e3a8a":"Azul oscuro"};
var XFC={"":"Automático","#1e3a8a":"Azul","#b91c1c":"Rojo","#15803d":"Verde","#ffffff":"Blanco"};
var XFF=["Calibri","Arial","Verdana","Times New Roman"];
var XSTY={"Título":{b:true,sz:18,fc:"#1e3a8a"},"Encabezado":{b:true,fill:"#1e3a8a",fc:"#ffffff",al:"c"},"Bueno":{fill:"#dcfce7",fc:"#15803d"},"Neutral":{fill:"#fef9c3",fc:""},"Malo":{fill:"#fee2e2",fc:"#b91c1c"},"Normal":{b:false,it:false,sz:11,fc:"",fill:"",al:"",ff:"Calibri"}};
var XPAGE={carta:[816,1056],oficio:[816,1344]},XMAR={normal:67,estrechos:24,anchos:96};
function xRef(c,r){return XCOLS[c]+r}
function xParse(s){var m=/^([A-J])([0-9]{1,2})$/.exec(String(s).trim().toUpperCase());return m?{c:XCOLS.indexOf(m[1]),r:+m[2]}:null}
function xRange(s){var p=String(s||"").toUpperCase().replace(/\s/g,"").split(":");if(p.length>2)return null;var a=xParse(p[0]),b=xParse(p[1]||p[0]);if(!a||!b)return null;return {c1:Math.min(a.c,b.c),c2:Math.max(a.c,b.c),r1:Math.min(a.r,b.r),r2:Math.max(a.r,b.r)}}
function xRstr(g){var a=xRef(g.c1,g.r1),b=xRef(g.c2,g.r2);return a==b?a:a+":"+b}
function xEach(g,f){for(var r=g.r1;r<=g.r2;r++)for(var c=g.c1;c<=g.c2;c++)f(xRef(c,r),c,r)}
function xNew(id){var c=XC[id];return {cells:JSON.parse(JSON.stringify(c.data)),mg:(c.mg||[]).slice(),cw:JSON.parse(JSON.stringify(c.cw||{})),sel:"A1",anc:"A1",pg:{or:"v",mar:"normal",sz:"carta",fit:false,hd:"",ft:"",bg:""},sh:{n:"Hoja1",col:""},vw:{grid:true,frz:false,zm:100},tab:"ini",prev:false,ext:false,used:{}}}
function xGet(id){if(!XS[id]){var s=null;try{s=JSON.parse(localStorage.getItem(KEY+"-xl-"+id)||"null")}catch(e){}XS[id]=s&&s.cells?s:xNew(id)}return XS[id]}
function xSave(id){try{localStorage.setItem(KEY+"-xl-"+id,JSON.stringify(XS[id]))}catch(e){}}
function xFmt(x){if(!x||x.v===undefined||x.v==="")return "";var v=x.v;if(typeof v!="number")return String(v);
 if(x.nf=="mon")return "$"+v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
 if(x.nf=="num")return v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
 if(x.nf=="por")return Math.round(v*1000)/10+"%";
 if(x.nf=="fec"){var d=new Date(Date.UTC(1899,11,30)+v*864e5);return ("0"+d.getUTCDate()).slice(-2)+"/"+("0"+(d.getUTCMonth()+1)).slice(-2)+"/"+d.getUTCFullYear()}
 return String(v)}
var XCTX=null;
function xFont(x){x=x||{};return (x.it?"italic ":"")+(x.b?"bold ":"")+((x.sz||11)*1.25)+"px "+(x.ff||"Calibri")+", Carlito, Arial, sans-serif"}
function xTextW(x){if(!XCTX)XCTX=document.createElement("canvas").getContext("2d");XCTX.font=xFont(x);return Math.ceil(XCTX.measureText(xFmt(x)).width)+14}
function xMerged(S){var cov={},span={};S.mg.forEach(function(m){var g=xRange(m),k=xRef(g.c1,g.r1);span[k]=[g.c2-g.c1+1,g.r2-g.r1+1,g];xEach(g,function(rf){if(rf!=k)cov[rf]=k})});return {cov:cov,span:span}}
function xNeed(S,id,col){var M=xMerged(S),c=XCOLS.indexOf(col),n=0;for(var r=1;r<=XC[id].rows;r++){var k=xRef(c,r),x=S.cells[k];if(!x||M.cov[k]||(M.span[k]&&M.span[k][0]>1)||x.wrap)continue;n=Math.max(n,xTextW(x))}return n}
function xW(S,col){return S.cw[col]||72}
function xTableW(S,id){var t=0;for(var c=0;c<XC[id].cols;c++)t+=xW(S,XCOLS[c]);return t}
function xUsable(S){var p=XPAGE[S.pg.sz]||XPAGE.carta,w=S.pg.or=="h"?p[1]:p[0];return w-2*(XMAR[S.pg.mar]||67)}
function xFits(S,id){return S.pg.fit||xTableW(S,id)<=xUsable(S)}
function xHF(t){var d=new Date();return String(t||"").replace(/&\[p[aá]gina\]/ig,"1").replace(/&\[fecha\]/ig,d.toLocaleDateString("es-MX")).replace(/</g,"&lt;")}
function xCellStyle(x){x=x||{};var s="font:"+xFont(x)+";";if(x.fc)s+="color:"+x.fc+";";if(x.fill)s+="background:"+x.fill+";";var al=x.al||(typeof x.v=="number"?"r":"l");s+="text-align:"+({l:"left",c:"center",r:"right"})[al]+";";if(x.wrap)s+="white-space:normal;";return s}
function xGrid(S,id,print){var tw,cfg=XC[id],M=xMerged(S),g=xRange(S.sel),tw=(print?0:34)+xTableW(S,id),h='<table class="xg'+(print||!S.vw.grid?' nogrid':'')+'" style="width:'+tw+'px"><colgroup>'+(print?'':'<col style="width:34px">');
 for(var c=0;c<cfg.cols;c++)h+='<col style="width:'+xW(S,XCOLS[c])+'px">';h+='</colgroup>';
 if(!print){h+='<tr class="xhr"><th class="x0"></th>';for(c=0;c<cfg.cols;c++)h+='<th class="'+(c>=g.c1&&c<=g.c2?"on":"")+'">'+XCOLS[c]+'</th>';h+='</tr>'}
 for(var r=1;r<=cfg.rows;r++){h+='<tr class="'+(!print&&S.vw.frz&&r==1?"xfz":"")+'">'+(print?'':'<th class="'+(r>=g.r1&&r<=g.r2?"on":"")+'">'+r+'</th>');
  for(c=0;c<cfg.cols;c++){var k=xRef(c,r);if(M.cov[k])continue;var x=S.cells[k]||{},sp=M.span[k],cl=(x.bd?"bd ":"")+(!print&&c>=g.c1&&c<=g.c2&&r>=g.r1&&r<=g.r2?"s ":"")+(!print&&k==xRef(g.c1,g.r1)?"a":"");
   h+='<td data-r="'+k+'" class="'+cl+'"'+(sp?' colspan="'+sp[0]+'" rowspan="'+sp[1]+'"':'')+' style="'+xCellStyle(x)+'">'+xFmt(x).replace(/</g,"&lt;")+'</td>'}
  h+='</tr>'}
 return h+'</table>'}
function xPreview(S,id){var p=XPAGE[S.pg.sz]||XPAGE.carta,pw=S.pg.or=="h"?p[1]:p[0],ph=S.pg.or=="h"?p[0]:p[1],m=XMAR[S.pg.mar]||67,W=260,k=W/pw,tw=xTableW(S,id),u=pw-2*m,fit=xFits(S,id),z=S.pg.fit&&tw>u?u/tw:1;
 var h='<div class="xpage" style="width:'+W+'px;height:'+Math.round(ph*k)+'px"><div class="xhd" style="top:'+Math.round(m*k*0.35)+'px">'+xHF(S.pg.hd)+'</div><div class="xpa" style="left:'+Math.round(m*k)+'px;top:'+Math.round(m*k)+'px;width:'+Math.round(u*k)+'px;height:'+Math.round((ph-2*m)*k)+'px"><div style="transform:scale('+(k*z)+');transform-origin:0 0;width:'+tw+'px">'+xGrid(S,id,true)+'</div></div>'+(fit?'':'<div class="xcut" style="left:'+Math.round((m+u)*k)+'px"></div>')+'<div class="xft" style="bottom:'+Math.round(m*k*0.35)+'px">'+xHF(S.pg.ft)+'</div></div>';
 var info={v:"Vertical",h:"Horizontal"}[S.pg.or]+' · Márgenes '+S.pg.mar+' · '+(S.pg.sz=="oficio"?"Oficio":"Carta")+(S.pg.fit?' · Ajustada a 1 página':'');
 var msg=fit?'✅ La tabla cabe a lo ancho en una sola hoja.':'⚠️ La tabla mide '+tw+' px y el espacio útil es de '+u+' px: la última columna se imprimiría en otra hoja. Prueba orientación horizontal, márgenes estrechos o «Ajustar a 1 página».';
 return '<div class="xprev">'+h+'<div class="xpi"><b>Vista preliminar</b><p>'+info+'</p><p>'+msg+'</p>'+(S.pg.bg?'<p>ℹ️ El fondo de la hoja se ve en pantalla, pero <b>no se imprime</b>.</p>':'')+(S.vw.grid?'<p>ℹ️ Las líneas de cuadrícula no se imprimen: si quieres líneas en papel, usa <b>Bordes</b>.</p>':'')+'<button type="button" class="btn ghost sm xcl">Cerrar vista preliminar</button></div></div>'}
function xApi(S,id){return {c:function(k){return S.cells[k]||{}},all:function(rg,f){var ok=true;xEach(xRange(rg),function(k){if(!f(S.cells[k]||{}))ok=false});return ok},mg:function(rg){return S.mg.indexOf(rg)>-1},
 w:function(col){return xW(S,col)},fitcols:function(cols){return cols.split("").every(function(col){return xW(S,col)>=xNeed(S,id,col)-1})},pg:S.pg,sh:S.sh,vw:S.vw,used:S.used,fits:function(){return xFits(S,id)}}}
function xTasks(id){var S=xGet(id),a=xApi(S,id);return XC[id].tasks.map(function(t){var ok=false;try{ok=!!t[1](a)}catch(e){}return {text:t[0],ok:ok}})}
function xOpt(o,v){return Object.keys(o).map(function(k){return '<option value="'+k+'"'+(k===v?' selected':'')+'>'+o[k]+'</option>'}).join("")}
function xArr(a,v){return a.map(function(k){return '<option'+(String(k)===String(v)?' selected':'')+'>'+k+'</option>'}).join("")}
function xRibbon(S){var c=S.cells[S.sel.split(":")[0]]||{},t=S.tab,o='';
 if(t=="ini")o='<div class="xgp"><small>Fuente</small><select data-x="ff" aria-label="Fuente">'+xArr(XFF,c.ff||"Calibri")+'</select><select data-x="sz" aria-label="Tamaño">'+xArr([10,11,12,14,16,18,20],c.sz||11)+'</select><button type="button" data-x="b" class="'+(c.b?"on":"")+'" title="Negrita"><b>N</b></button><button type="button" data-x="it" class="'+(c.it?"on":"")+'" title="Cursiva"><i>K</i></button><select data-x="fc" aria-label="Color de fuente">'+xOpt(XFC,c.fc||"")+'</select><select data-x="fill" aria-label="Color de relleno">'+xOpt(XFILL,c.fill||"")+'</select><select data-x="bd" aria-label="Bordes"><option value="">Bordes…</option><option value="1">Todos los bordes</option><option value="0">Sin borde</option></select></div>'
  +'<div class="xgp"><small>Alineación</small><button type="button" data-x="al" data-v="l" class="'+(c.al=="l"?"on":"")+'" title="Alinear a la izquierda">⇤</button><button type="button" data-x="al" data-v="c" class="'+(c.al=="c"?"on":"")+'" title="Centrar">↔</button><button type="button" data-x="al" data-v="r" class="'+(c.al=="r"?"on":"")+'" title="Alinear a la derecha">⇥</button><button type="button" data-x="wrap" class="'+(c.wrap?"on":"")+'">Ajustar texto</button><button type="button" data-x="merge">Combinar y centrar</button></div>'
  +'<div class="xgp"><small>Número</small><select data-x="nf" aria-label="Formato de número">'+xOpt({gen:"General",num:"Número",mon:"Moneda",por:"Porcentaje",fec:"Fecha corta"},c.nf||"gen")+'</select></div>'
  +'<div class="xgp"><small>Estilos y celdas</small><select data-x="sty" aria-label="Estilos de celda"><option value="">Estilos de celda…</option>'+Object.keys(XSTY).map(function(k){return '<option>'+k+'</option>'}).join("")+'</select><button type="button" data-x="fit">Autoajustar ancho de columna</button></div>';
 if(t=="ins")o='<div class="xgp xwide"><small>Encabezado y pie de página</small><label>Encabezado <input data-x="hd" value="'+String(S.pg.hd).replace(/"/g,"&quot;")+'" placeholder="Texto del encabezado"></label><label>Pie de página <input data-x="ft" value="'+String(S.pg.ft).replace(/"/g,"&quot;")+'" placeholder="Texto del pie de página"></label><button type="button" data-x="pgn"># Número de página</button><button type="button" data-x="date">📅 Fecha</button></div>';
 if(t=="pag")o='<div class="xgp"><small>Configurar página</small><select data-x="mar" aria-label="Márgenes">'+xOpt({normal:"Márgenes: Normales",estrechos:"Márgenes: Estrechos",anchos:"Márgenes: Anchos"},S.pg.mar)+'</select><select data-x="or" aria-label="Orientación">'+xOpt({v:"Orientación: Vertical",h:"Orientación: Horizontal"},S.pg.or)+'</select><select data-x="psz" aria-label="Tamaño">'+xOpt({carta:"Tamaño: Carta",oficio:"Tamaño: Oficio"},S.pg.sz)+'</select><select data-x="bg" aria-label="Fondo">'+xOpt({"":"Fondo: ninguno",cuadros:"Fondo: imagen de cuadritos"},S.pg.bg)+'</select></div><div class="xgp"><small>Ajustar área de impresión</small><label class="xck"><input type="checkbox" data-x="pfit"'+(S.pg.fit?" checked":"")+'> Ajustar a 1 página</label></div>';
 if(t=="vis")o='<div class="xgp"><small>Mostrar</small><label class="xck"><input type="checkbox" data-x="grid"'+(S.vw.grid?" checked":"")+'> Líneas de cuadrícula</label></div><div class="xgp"><small>Ventana</small><button type="button" data-x="frz" class="'+(S.vw.frz?"on":"")+'">Inmovilizar fila superior</button><select data-x="zm" aria-label="Zoom">'+xOpt({75:"Zoom 75%",100:"Zoom 100%",125:"Zoom 125%"},String(S.vw.zm))+'</select></div>';
 return o}
function xPaint(d){var b=d.querySelector(".xlsim"),id=b.dataset.id,S=xGet(id),g=xRange(S.sel),k0=xRef(g.c1,g.r1),c0=S.cells[k0]||{};
 b.querySelectorAll(".xtabs button").forEach(function(x){x.className=x.dataset.t==S.tab?"on":""});
 b.querySelector(".xrb").innerHTML=xRibbon(S);
 var nb=b.querySelector(".xnb");if(document.activeElement!==nb)nb.value=S.sel;
 b.querySelector(".xfx").textContent=c0.v===undefined?"":String(c0.v);
 var w=b.querySelector(".xwrap");w.className="xwrap"+(S.pg.bg?" xbg":"");w.innerHTML='<div style="zoom:'+S.vw.zm/100+'">'+xGrid(S,id,false)+'</div>';
 b.querySelector(".xext").className="btn ghost sm xext"+(S.ext?" on":"");
 b.querySelector(".xsh").innerHTML='<button type="button" class="xst" style="'+(S.sh.col?"border-bottom:4px solid "+S.sh.col:"")+'">'+S.sh.n.replace(/</g,"&lt;")+'</button><span class="xsm'+(S.shm?"":" hid")+'"><input class="xsn" value="'+S.sh.n.replace(/"/g,"&quot;")+'" maxlength="31" aria-label="Nombre de la hoja"><select class="xsc" aria-label="Color de etiqueta">'+xOpt({"":"Sin color","#2563eb":"Azul","#16a34a":"Verde","#dc2626":"Rojo","#f59e0b":"Naranja"},S.sh.col)+'</select></span>';
 var pv=b.querySelector(".xpv");pv.innerHTML=S.prev?xPreview(S,id):"";
 var ts=xTasks(id);b.querySelector(".xts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("");return ts}
function xDo(d,act,val,el){var b=d.querySelector(".xlsim"),id=b.dataset.id,S=xGet(id),g=xRange(S.sel),U=S.used;U[act]=1;
 function each(f){xEach(g,function(k){var x=S.cells[k]||(S.cells[k]={});f(x,k)})}
 function allp(p){var ok=true;xEach(g,function(k){if(!(S.cells[k]||{})[p])ok=false});return ok}
 if(act=="b"||act=="it"||act=="wrap"){var on=!allp(act);each(function(x){x[act]=on})}
 else if(act=="sz")each(function(x){x.sz=+val});
 else if(act=="ff"||act=="fc"||act=="fill"||act=="nf"||act=="al")each(function(x){x[act]=val});
 else if(act=="bd"){if(val!=="")each(function(x){x.bd=val=="1"})}
 else if(act=="sty"){if(val&&XSTY[val])each(function(x){for(var p in XSTY[val])x[p]=XSTY[val][p]});U["sty:"+val]=1}
 else if(act=="merge"){var rs=xRstr(g),had=S.mg.indexOf(rs)>-1;S.mg=S.mg.filter(function(m){var h=xRange(m);return h.c2<g.c1||h.c1>g.c2||h.r2<g.r1||h.r1>g.r2});if(!had&&rs.indexOf(":")>-1){S.mg.push(rs);var x=S.cells[xRef(g.c1,g.r1)]||(S.cells[xRef(g.c1,g.r1)]={});x.al="c"}}
 else if(act=="fit"){for(var c=g.c1;c<=g.c2;c++){var col=XCOLS[c];S.cw[col]=Math.max(40,xNeed(S,id,col)||72)}}
 else if(act=="hd"||act=="ft")S.pg[act]=val;
 else if(act=="pgn"){S.pg.ft=(S.pg.ft?S.pg.ft+" · ":"")+"Página &[Página]"}
 else if(act=="date"){S.pg.ft=(S.pg.ft?S.pg.ft+" · ":"")+"&[Fecha]"}
 else if(act=="mar"||act=="or"||act=="bg")S.pg[act]=val;
 else if(act=="psz")S.pg.sz=val;
 else if(act=="pfit")S.pg.fit=!!el.checked;
 else if(act=="grid")S.vw.grid=!!el.checked;
 else if(act=="frz")S.vw.frz=!S.vw.frz;
 else if(act=="zm")S.vw.zm=+val;
 xSave(id);xPaint(d)}
function xSelect(d,k,extend){var b=d.querySelector(".xlsim"),S=xGet(b.dataset.id),M=xMerged(S),sp=M.span[k];
 if(extend){var a=xParse(S.anc),z=xParse(k);S.sel=xRstr({c1:Math.min(a.c,z.c),c2:Math.max(a.c,z.c),r1:Math.min(a.r,z.r),r2:Math.max(a.r,z.r)})}
 else{S.anc=k;S.sel=sp&&(sp[0]>1||sp[1]>1)?xRstr(sp[2]):k}xSave(b.dataset.id);xPaint(d)}
function pXls(ic,t,inf,cfg){K++;XC[cfg.id]=cfg;return '<article class="lesson"><header><span class="kick">'+ic+' Simulador</span><h1>'+t+'</h1><p class="sub">'+inf+'</p></header><style>'
 +'.xlsim .xts{list-style:none;padding:0;margin:0 0 12px;display:grid;gap:6px}.xlsim .xts li{border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14.5px}.xlsim .xts li.y{border-color:var(--ok);background:var(--ok-soft)}'
 +'.xbook{border:1.5px solid #c8ccd2;border-radius:12px;overflow:hidden;background:#fff;color:#1f2937}.xtabs{display:flex;gap:2px;background:#217346;padding:6px 6px 0;overflow-x:auto}.xtabs button{border:0;background:transparent;color:#e7f3ec;font:600 13px system-ui;padding:7px 11px;border-radius:7px 7px 0 0;cursor:pointer;white-space:nowrap}.xtabs button.on{background:#f3f4f6;color:#14532d}'
 +'.xrb{background:#f3f4f6;display:flex;flex-wrap:wrap;gap:6px;padding:8px;border-bottom:1px solid #d1d5db}.xgp{display:flex;flex-wrap:wrap;gap:4px;align-items:center;border:1px solid #e5e7eb;background:#fff;border-radius:8px;padding:5px 6px}.xgp small{width:100%;font:600 10.5px system-ui;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}.xgp.xwide{flex:1 1 100%}.xgp.xwide label{display:flex;flex-direction:column;font:12px system-ui;flex:1 1 180px}.xgp.xwide input{width:100%}'
 +'.xrb button,.xrb select,.xrb input{width:auto;max-width:100%;margin:0;font:13px system-ui;border:1px solid #cbd5e1;background:#fff;color:#111827;border-radius:6px;padding:5px 8px;min-height:32px}.xrb button{cursor:pointer}.xrb button.on{background:#d1fae5;border-color:#059669}.xck{display:flex;gap:6px;align-items:center;font:13px system-ui}.xck input{min-height:auto}'
 +'.xbar{display:flex;gap:6px;align-items:center;padding:6px 8px;border-bottom:1px solid #d1d5db;background:#fff}.xnb{width:78px;font:600 13px Consolas,monospace;border:1px solid #cbd5e1;border-radius:6px;padding:5px 6px;color:#111827;background:#fff}.xfxl{font:italic 600 13px serif;color:#6b7280}.xfx{flex:1;font:13px Consolas,monospace;color:#111827;border:1px solid #e5e7eb;border-radius:6px;padding:6px 8px;min-height:30px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}'
 +'.xwrap{overflow:auto;max-height:320px;background:#fff}.xwrap.xbg{background:repeating-linear-gradient(45deg,#f0fdf4 0 10px,#fff 10px 20px)}.xg{border-collapse:collapse;table-layout:fixed;color:#111827;user-select:none}.xg th{background:#f3f4f6;color:#4b5563;font:12px system-ui;border:1px solid #d1d5db;padding:2px 4px;text-align:center}.xg th.on{background:#d1fae5;color:#065f46;font-weight:700}.xhr th{position:sticky;top:0;z-index:2}'
 +'.xg td{border:1px solid #e5e7eb;padding:3px 6px;height:24px;white-space:nowrap;overflow:hidden;cursor:cell;background-clip:padding-box}.xg.nogrid td{border-color:transparent}.xg td.bd{border:1px solid #111827}.xg td.s{box-shadow:inset 0 0 0 999px rgba(16,185,129,.16)}.xg td.a{outline:2px solid #059669;outline-offset:-2px}.xfz td,.xfz th{position:sticky;top:27px;z-index:1;border-bottom:2px solid #059669}.xfz td{background-color:#fff}'
 +'.xsh{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:6px 8px;background:#f3f4f6;border-top:1px solid #d1d5db}.xst{font:600 13px system-ui;background:#fff;border:1px solid #cbd5e1;border-radius:0 0 6px 6px;padding:5px 14px;color:#14532d;cursor:pointer}.xsm{display:flex;gap:6px}.xsm.hid{display:none}.xsm input,.xsm select{font:13px system-ui;border:1px solid #cbd5e1;border-radius:6px;padding:4px 6px;background:#fff;color:#111827}'
 +'.xprev{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-start;margin-top:12px;padding:12px;border:1.5px dashed var(--line);border-radius:12px}.xpage{position:relative;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.25);overflow:hidden;flex:none}.xpa{position:absolute;overflow:hidden;outline:1px dashed #cbd5e1}.xhd,.xft{position:absolute;left:0;right:0;text-align:center;font:9px system-ui;color:#374151}.xcut{position:absolute;top:0;bottom:0;border-left:2px dashed #dc2626}.xpi{flex:1 1 200px;font-size:14.5px}.xpi p{margin:6px 0}'
 +'.xtools{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.xtools .on{background:var(--pri-soft)}'
 +'</style><div class="xlsim" data-id="'+cfg.id+'">'+(cfg.intro?'<p>'+cfg.intro+'</p>':'')+'<h3 style="margin:8px 0">Retos</h3><ol class="xts"></ol>'
 +'<div class="xbook"><div class="xtabs"><button type="button" data-t="arc">Archivo</button><button type="button" data-t="ini">Inicio</button><button type="button" data-t="ins">Insertar</button><button type="button" data-t="pag">Disposición de página</button><button type="button" data-t="vis">Vista</button></div><div class="xrb"></div>'
 +'<div class="xbar"><input class="xnb" aria-label="Cuadro de nombres" title="Cuadro de nombres: escribe una celda o un rango y pulsa Enter"><span class="xfxl">fx</span><div class="xfx" title="Barra de fórmulas: muestra el valor real de la celda"></div></div><div class="xwrap"></div><div class="xsh"></div></div>'
 +'<div class="xtools"><button type="button" class="btn ghost sm xext">➕ Seleccionar rango (en celular)</button><button type="button" class="btn ghost sm xrst">↺ Reiniciar</button></div><div class="xpv"></div></div>'
 +(cfg.hint?'<p class="take"><b>Pista:</b> '+cfg.hint+'</p>':'')+'<div class="chk"><button class="btn c">Revisar retos</button></div><div class="res" role="status"></div></article>'}
function xlsInit(d){var b=d.querySelector(".xlsim"),id=b.dataset.id,S=xGet(id),drag=false;S.shm=false;
 b.querySelector(".xtabs").onclick=function(e){var t=e.target.closest("button");if(!t)return;if(t.dataset.t=="arc"){S.prev=!S.prev;S.used.prev=1}else S.tab=t.dataset.t;xSave(id);xPaint(d)};
 var rb=b.querySelector(".xrb");
 rb.onclick=function(e){var t=e.target.closest("button[data-x]");if(t)xDo(d,t.dataset.x,t.dataset.v,t)};
 rb.onchange=function(e){var t=e.target;if(t.dataset.x&&t.dataset.x!="hd"&&t.dataset.x!="ft")xDo(d,t.dataset.x,t.value,t)};
 rb.oninput=function(e){var t=e.target;if(t.dataset.x=="hd"||t.dataset.x=="ft"){S.pg[t.dataset.x]=t.value;S.used[t.dataset.x]=1;xSave(id);var pv=b.querySelector(".xpv");if(S.prev)pv.innerHTML=xPreview(S,id);var ts=xTasks(id);b.querySelector(".xts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("")}};
 var nb=b.querySelector(".xnb");nb.onkeydown=function(e){if(e.key!="Enter")return;e.preventDefault();var g=xRange(nb.value);if(!g||g.c2>=XC[id].cols||g.r2>XC[id].rows||g.r1<1){nb.value=S.sel;nb.style.borderColor="#dc2626";return}nb.style.borderColor="";S.sel=xRstr(g);S.anc=xRef(g.c1,g.r1);S.used.nb=1;xSave(id);nb.blur();xPaint(d)};
 var w=b.querySelector(".xwrap");
 w.onpointerdown=function(e){var td=e.target.closest("td[data-r]");if(!td)return;var ext=e.shiftKey||S.ext;xSelect(d,td.dataset.r,ext);if(S.ext){S.ext=false;xSave(id);xPaint(d)}drag=e.pointerType=="mouse"&&!ext};
 w.onpointermove=function(e){if(!drag)return;var el=document.elementFromPoint(e.clientX,e.clientY),td=el&&el.closest&&el.closest("td[data-r]");if(td&&w.contains(td)){var a=xParse(S.anc),z=xParse(td.dataset.r),s=xRstr({c1:Math.min(a.c,z.c),c2:Math.max(a.c,z.c),r1:Math.min(a.r,z.r),r2:Math.max(a.r,z.r)});if(s!=S.sel){S.sel=s;xPaint(d)}}};
 document.addEventListener("pointerup",function(){if(drag){drag=false;xSave(id)}});
 b.querySelector(".xext").onclick=function(){S.ext=!S.ext;xSave(id);xPaint(d)};
 var sh=b.querySelector(".xsh");sh.onclick=function(e){if(e.target.closest(".xst")){S.shm=!S.shm;xPaint(d)}};
 sh.onchange=function(e){if(e.target.classList.contains("xsn")){var v=e.target.value.trim();if(v)S.sh.n=v}if(e.target.classList.contains("xsc"))S.sh.col=e.target.value;xSave(id);xPaint(d)};
 b.querySelector(".xpv").onclick=function(e){if(e.target.closest(".xcl")){S.prev=false;xSave(id);xPaint(d)}};
 b.querySelector(".xrst").onclick=function(){if(!confirm("¿Reiniciar el simulador? Se borra el formato que aplicaste."))return;XS[id]=xNew(id);xSave(id);xlsInit(d)};
 xPaint(d)}
function xlsCheck(d){var ts=xPaint(d),ok=ts.filter(function(x){return x.ok}).length,n=ts.length,f=ts.filter(function(x){return !x.ok})[0];return {ok:ok,total:n,msg:ok==n?"¡Todos los retos resueltos! Haz lo mismo en Excel con tu propio libro: es tu práctica.":ok+" de "+n+" retos. Sigue con: «"+f.text.replace(/<[^>]*>/g,"")+"»"}}
