(function(){var m=/-ra(\d)(\d)-avance/.exec(typeof KEY=="string"?KEY:"");if(!m||+m[1]<2||typeof sec!="function")return;
/* Apuntes imprimibles: solo lo que sirve para estudiar (conceptos, pasos, diagramas, avisos e ideas clave) de las lecciones de «Aprende».
   Casos, analogías, actividades, prácticas y simuladores se quedan en la plataforma. */
var KEEP_EX=/^(Ejemplo|Así sí|Atajo|Comparación|La fórmula|Cómo |Leer el código|Truco|¿Cuál conviene|Compruébalo|Porcentaje)/;
function txt(s){return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;")}
function brand(){var b=document.querySelector(".brand b"),s=document.querySelector(".brand span"),mo=(b?b.textContent:"").split("·"),ra=(s?s.textContent:"").split("·");
 return {mod:(mo[0]||"").trim(),modName:mo.slice(1).join("·").trim(),ra:(ra[0]||"").trim(),raName:ra.slice(1).join("·").trim()}}
function lessonIdx(S){var r=[];for(var i=S.a;i<=S.b;i++)if(/class="kick">[^<]*Lección/.test(P[i]))r.push(i);return r}
function topic(h,num,pre){var d=document.createElement("div");d.innerHTML=h;var a=d.querySelector(".lesson");if(!a)return "";
 a.querySelectorAll("button,input,select,textarea,script,.pxb,.exn,.co-ana,.tile>div:first-child").forEach(function(x){x.remove()});
 a.querySelectorAll(".co-ex").forEach(function(x){var l=x.querySelector(".co-l");if(!l||!KEEP_EX.test(l.textContent.trim()))x.remove()});
 a.querySelectorAll("[hidden]").forEach(function(x){x.removeAttribute("hidden")});a.querySelectorAll("details").forEach(function(x){x.open=true});
 var t=(a.querySelector("h1")||{}).innerHTML||"",tk=a.querySelector(".take"),key=tk?tk.innerHTML.replace(/^\s*<b>[^<]*<\/b>\s*/,""):"";
 [].slice.call(a.children).forEach(function(x){if(x.tagName=="HEADER"||x.classList.contains("take"))x.remove()});
 var body=a.innerHTML.trim();if(!body&&!key)return "";
 /* El título viaja pegado al primer elemento para que no quede solo al final de una columna. */
 var k=0;a.querySelectorAll(".it>b:first-child,.pxt,h2,h4").forEach(function(x){k++;x.insertAdjacentHTML("afterbegin",'<span class="sn">'+num+'.'+k+'</span>')});
 var first=a.firstElementChild,rest="";if(first){first.remove();rest=a.innerHTML}
 return '<section class="tp"><div class="hd">'+(pre||"")+'<h3><span class="n">Tema '+num+'</span>'+t+'</h3>'+(first?first.outerHTML:"")+'</div>'+rest+(key?'<p class="key"><b>Idea clave</b>'+key+'</p>':'')+'</section>'}
function illCss(){var o=[];[].forEach.call(document.styleSheets,function(s){try{[].forEach.call(s.cssRules,function(r){if(r.selectorText&&/^\.ill /.test(r.selectorText)&&!/svg/.test(r.selectorText))o.push(r.cssText)})}catch(e){}});return o.join("\n")}
var CSS=':root{--pri:#1b3a8a;--pri-soft:#eef2fa;--ok:#1e7a46;--amb:#b7791f;--bad:#b42332;--ink:#1a1f2b;--mut:#5a6578;--line:#d5dbe6;--card:#fff;--bg:#f6f8fb;--on:#fff}'+
'*{box-sizing:border-box}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}body{margin:0;background:#e3e7ee;color:var(--ink);font:8.6pt/1.34 "Segoe UI",Roboto,Arial,sans-serif}'+
'.bar{position:sticky;top:0;z-index:5;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 14px;background:var(--pri);color:#fff;font-size:13px}.bar button{border:0;border-radius:8px;padding:10px 16px;font:700 14px system-ui;background:#fff;color:var(--pri)}.bar span{flex:1;min-width:200px;opacity:.9}'+
'.sheet{width:216mm;max-width:100%;margin:14px auto;background:#fff;padding:10mm 11mm 12mm;box-shadow:0 2px 12px rgba(0,0,0,.15)}'+
'.top{display:flex;justify-content:space-between;align-items:center;background:var(--pri);color:#fff;font-size:7.4pt;font-weight:700;letter-spacing:.09em;text-transform:uppercase;padding:4px 9px;border-radius:4px 4px 0 0}'+
'.cover{display:flex;align-items:stretch;border:1px solid var(--line);border-top:0}.ra{flex:none;display:flex;flex-direction:column;justify-content:center;align-items:center;background:var(--pri-soft);color:var(--pri);padding:5px 12px;border-right:1px solid var(--line)}.ra small{font-size:6.6pt;font-weight:800;letter-spacing:.1em}.ra b{font-size:19pt;line-height:1;font-weight:800}'+
'.cover h1{flex:1;align-self:center;margin:0;padding:6px 12px;font-size:15.5pt;line-height:1.12;font-weight:750}'+
'.who{display:grid;grid-template-columns:1fr 20mm 46mm;border:1px solid var(--line);border-top:0;margin-bottom:5px}.who div{padding:3px 9px;border-right:1px solid var(--line)}.who div:last-child{border-right:0}.who small{display:block;font-size:6.4pt;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}.who b{display:block;min-height:13px;font-size:9.4pt;font-weight:650}'+
'.idx{display:flex;flex-wrap:wrap;gap:2px 14px;margin:0 0 8px;padding:3px 0 5px;border-bottom:2px solid var(--pri);font-size:7.8pt;color:var(--mut)}.idx b{color:var(--pri);margin-right:3px}.idx>span:first-child{font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:6.6pt;color:var(--ink);align-self:center}'+
'.flow{column-count:2;column-gap:7mm;column-rule:1px solid var(--line)}'+
'.inc{display:flex;align-items:center;gap:7px;margin:2px 0 6px;padding-bottom:3px;border-bottom:2px solid var(--pri);break-after:avoid}.inc .l{flex:none;display:grid;place-items:center;min-width:20px;height:20px;padding:0 4px;border-radius:4px;background:var(--pri);color:#fff;font-weight:800;font-size:9.6pt}.inc .t{font-size:10.2pt;font-weight:750;color:var(--pri);line-height:1.15}.inc small{display:block;font-size:6.4pt;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}'+
'.tp{margin:0 0 9px}.hd{break-inside:avoid}'+
'h3{display:flex;gap:7px;align-items:baseline;font-size:9.8pt;line-height:1.2;margin:0 0 3px;padding:2px 0 2px 7px;border-left:3px solid var(--pri);background:linear-gradient(90deg,var(--pri-soft),transparent);color:var(--ink)}h3 .n{flex:none;font-size:7pt;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--pri)}'+
'.sn{display:inline-block;margin-right:4px;font-size:7pt;font-weight:700;color:var(--mut);font-variant-numeric:tabular-nums}'+
'.tp p{margin:3px 0}.tp ul,.tp ol{margin:3px 0;padding-left:15px}.tp li{margin:1px 0}h2,h4{font-size:9pt;margin:5px 0 2px;break-after:avoid}'+
'.it{display:grid;grid-template-columns:31% 1fr;gap:0 7px;padding:2px 0;border-bottom:1px solid var(--line);break-inside:avoid}.it b{color:var(--pri);font-weight:650}'+
'.co{margin:4px 0;padding:3px 7px;break-inside:avoid;border-left:2.5px solid var(--pri);background:var(--pri-soft)}.co p{margin:1px 0 0}.co-l{font-size:6.8pt;letter-spacing:.07em;text-transform:uppercase;font-weight:800;color:var(--pri)}'+
'.co-def .co-l{font-size:0}.co-def .co-l:after{content:"Definición";font-size:6.8pt}.co-ex{border-color:var(--amb);background:#fdf8ee}.co-ex .co-l{color:var(--amb)}.co-warn{border-color:var(--bad);background:#fcf1f2}.co-warn .co-l{color:var(--bad)}'+
'.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:4px 0;border:1px solid var(--line);break-inside:avoid}.tile{padding:3px 5px;border-right:1px solid var(--line)}.tile:last-child{border-right:0}.tile b{display:block;font-size:8.2pt;color:var(--pri)}.tile span{display:block;font-size:7.8pt;color:var(--mut);line-height:1.25}'+
'.pasos{margin:4px 0}.pxt{font-weight:700;margin-bottom:1px}.px{display:flex;gap:6px;align-items:flex-start;padding:1px 0;break-inside:avoid}.px>div{flex:1}.pxn{flex:none;width:13px;height:13px;margin-top:1px;border-radius:50%;background:var(--pri);color:#fff;display:grid;place-items:center;font-size:6.8pt;font-weight:800}'+
'.ill{margin:4px 0;padding:2px;border:1px solid var(--line);border-radius:4px;break-inside:avoid}.ill svg{display:block;width:100%;height:auto;max-height:30mm;margin:0 auto}'+
'.key{margin:5px 0 0!important;padding:3px 7px;border:1px solid var(--line);border-radius:4px;background:var(--bg);break-inside:avoid}.key b{display:block;font-size:6.8pt;letter-spacing:.07em;text-transform:uppercase;color:var(--ok)}'+
'code{font:8pt Consolas,monospace;background:var(--bg);border-radius:2px;padding:0 2px}pre{font:7.6pt/1.3 Consolas,monospace;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:3px 5px;white-space:pre-wrap;margin:3px 0;break-inside:avoid}'+
'table{width:100%;border-collapse:collapse;font-size:7.8pt;margin:3px 0;break-inside:avoid}th,td{border:1px solid var(--line);padding:1px 4px;text-align:left;vertical-align:top}th{background:var(--pri-soft)}'+
'.exw,.mw,.mph{max-width:100%;overflow:hidden;font-size:7.6pt;break-inside:avoid;margin:3px 0}.mw{border:1px solid var(--line);border-radius:4px}.mt{background:var(--bg);padding:1px 5px;font-size:7pt}.mt i{display:none}.mbd{padding:3px}.mcap{font-size:7.6pt;margin:2px 0}'+
'.foot{display:flex;justify-content:space-between;margin-top:6mm;padding-top:3px;border-top:1px solid var(--line);color:var(--mut);font-size:7pt}.foot b{color:var(--pri);letter-spacing:.05em}.foot em{font-family:"Segoe Script","Brush Script MT",cursive;font-size:8.4pt;color:var(--pri);margin-right:6px}'+
'@page{size:letter portrait;margin:9mm 9mm 10mm}@media print{body{background:#fff}.bar{display:none}.sheet{width:auto;margin:0;padding:0;box-shadow:none}}'+
'@media (max-width:600px){.sheet{padding:5mm;margin:6px auto}.flow{column-count:1}.who{grid-template-columns:1fr 1fr}.who div:first-child{grid-column:1/-1;border-right:0;border-bottom:1px solid var(--line)}}';
/* Nombre y grupo del alumno: primero la sesión de la plataforma (mismo origen), luego lo que escribió en «Mi entrega». */
function alumno(){var s=null;try{s=JSON.parse(localStorage.getItem("aula-session")||"null")}catch(e){}
 var st=s&&s.role=="student"&&(!s.id||SID=="local"||s.id==SID)?s:{};
 return {name:(st.name||ST.nm||"").trim(),group:(st.group&&st.group!="Sin asignar"?st.group:ST.gr||"").trim()}}
function hoy(){try{return new Date().toLocaleDateString("es-MX",{day:"numeric",month:"long",year:"numeric"})}catch(e){return new Date().toISOString().slice(0,10)}}
function build(){var B=brand(),A=alumno(),h='',idx='';
 ORDER.forEach(function(id){var S=SC(id),C=CH[id]||{};if(/Introducci/.test(C.k||""))return;var n=0,part='';
  var L=C.l||"",head='<div class="inc"><span class="l">'+L+')</span><span class="t"><small>Inciso</small>'+(C.t||"")+'</span></div>';
  lessonIdx(S).forEach(function(i){var t=topic(P[i],(C.l||"")+"."+(n+1),n?"":head);if(t){n++;part+=t}});
  if(part)idx+='<span><b>'+L+')</b>'+(C.t||"")+'</span>';h+=part});
 var mod=B.mod+(B.modName?' · '+B.modName:'');
 return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Apuntes '+txt(B.mod+' '+B.ra)+'</title><style>'+CSS+'\n'+illCss()+'</style></head><body>'+
  '<div class="bar"><button onclick="print()">🖨️ Imprimir o guardar PDF</button><span>En celular: toca el botón y elige «Guardar como PDF». Sale en hoja carta, lista para pegar en tu cuaderno.</span></div>'+
  '<div class="sheet"><div class="top"><span>'+txt(mod)+'</span><span>Apuntes</span></div>'+
  '<div class="cover"><div class="ra"><small>R.A.</small><b>'+txt(B.ra.replace(/^R\.A\.\s*/,""))+'</b></div><h1>'+txt(B.raName)+'</h1></div>'+
  '<div class="who"><div><small>Alumno</small><b>'+txt(A.name)+'</b></div><div><small>Grupo</small><b>'+txt(A.group)+'</b></div><div><small>Fecha de descarga</small><b>'+hoy()+'</b></div></div>'+
  '<div class="idx"><span>Contenido</span>'+idx+'</div>'+
  '<div class="flow">'+h+'</div><div class="foot"><span>'+txt(B.mod+' · '+B.ra+' · '+B.raName)+'</span><span><em>Ing. Santiago Martínez González</em><b>AulaVirtual</b></span></div></div></body></html>'}
function open(){var html=build(),w=null;try{w=window.open("","_blank")}catch(e){}
 if(w){w.document.open();w.document.write(html);w.document.close();return}
 location.href=URL.createObjectURL(new Blob([html],{type:"text/html"}))}
window.apuntes=open;
var st=document.createElement("style");st.textContent='.crumb .apx{margin-left:auto;border:1.5px solid var(--pri);background:var(--card);color:var(--pri);border-radius:999px;padding:5px 12px;font-weight:700;font-size:13px}.crumb .apx:hover{background:var(--pri-soft)}@media (max-width:560px){.crumb .apx{padding:4px 10px;font-size:12px}}';document.head.appendChild(st);
var _sec=sec;sec=function(id,p){_sec(id,p);if(ORDER.indexOf(id)<0)return;var c=document.querySelector("#main .crumb");if(!c||c.querySelector(".apx"))return;
 var b=document.createElement("button");b.className="apx";b.type="button";b.title="Descarga los apuntes de «Aprende» para imprimir y pegar en tu cuaderno";b.textContent="🖨️ Descargar apuntes";b.onclick=open;c.appendChild(b)}})();
