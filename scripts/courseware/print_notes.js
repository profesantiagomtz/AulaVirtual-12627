(function(){var m=/-ra(\d)(\d)-avance/.exec(typeof KEY=="string"?KEY:"");if(!m||+m[1]<2||typeof sec!="function")return;
/* Apuntes imprimibles: arma una hoja carta con las lecciones de «Aprende» (sin actividades ni simuladores) en dos columnas. */
function txt(s){return document.createElement("i").appendChild(document.createTextNode(s||"")).parentNode.innerHTML}
function brand(){var b=document.querySelector(".brand b"),s=document.querySelector(".brand span"),mo=(b?b.textContent:"").split("·"),ra=(s?s.textContent:"").split("·");
 return {mod:(mo[0]||"").trim(),modName:(mo.slice(1).join("·")||"").trim(),ra:(ra[0]||"").trim(),raName:(ra.slice(1).join("·")||"").trim()}}
function clean(h){var d=document.createElement("div");d.innerHTML=h;
 d.querySelectorAll("button,input,select,textarea,script,.pxb,.exn,[data-px],[data-pxall]").forEach(function(x){x.remove()});
 d.querySelectorAll("[hidden]").forEach(function(x){x.removeAttribute("hidden")});d.querySelectorAll("details").forEach(function(x){x.open=true});
 d.querySelectorAll("[style]").forEach(function(x){if(!x.closest("svg"))x.style.removeProperty("max-height")});
 var a=d.querySelector(".lesson"),hd=a&&a.querySelector("header");if(hd&&hd.nextElementSibling){var g=document.createElement("div");g.className="hd";a.insertBefore(g,hd);g.appendChild(hd);g.appendChild(g.nextElementSibling)}
 var t=d.querySelector(".take");if(t){t.className="tip";t.innerHTML='<span class="ti">💡</span><span>'+t.innerHTML+'</span>'}
 return d}
function illCss(){var o=[];[].forEach.call(document.styleSheets,function(s){try{[].forEach.call(s.cssRules,function(r){if(r.selectorText&&/^\.ill /.test(r.selectorText)&&!/svg/.test(r.selectorText))o.push(r.cssText)})}catch(e){}});return o.join("\n")}
function lessonIdx(S){var r=[];for(var i=S.a;i<=S.b;i++)if(/class="kick">[^<]*Lección/.test(P[i]))r.push(i);return r}
var CSS=':root{--pri:#1b3fa0;--pri-soft:#e9effb;--ok:#1e8e4e;--ok-soft:#e6f4ec;--amb:#f2a900;--ex:#7a5a00;--ex-bg:#fff5d6;--bad:#c62f3a;--bad-soft:#fdeaec;--ink:#14213d;--mut:#4a5870;--line:#c9d2e3;--card:#fff;--bg:#f4f6fa;--on:#fff}'+
'*{box-sizing:border-box}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}body{margin:0;background:#dfe4ec;color:var(--ink);font:8.6pt/1.3 "Segoe UI",Roboto,Arial,sans-serif}'+
'.bar{position:sticky;top:0;z-index:5;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 14px;background:var(--pri);color:#fff;font-size:13px}.bar button{border:0;border-radius:10px;padding:10px 16px;font:700 14px system-ui;background:#fff;color:var(--pri)}.bar span{flex:1;min-width:200px;opacity:.9}'+
'.sheet{width:216mm;max-width:100%;margin:14px auto;background:#fff;padding:9mm 9mm 12mm;box-shadow:0 2px 12px rgba(0,0,0,.18)}'+
'.band{display:flex;align-items:center;gap:8px;background:var(--pri);color:#fff;border-radius:6px;padding:4px 10px;font-weight:700;font-size:8.5pt}.band b{letter-spacing:.04em}.band .grow{flex:1}'+
'.cover{display:grid;grid-template-columns:1fr auto;gap:2px 14px;align-items:end;border-bottom:2px solid var(--pri);padding:5px 0 5px;margin-bottom:6px}.cover h1{margin:0;font-size:16pt;line-height:1.1;color:var(--ink)}.cover p{margin:0;color:var(--mut)}.who{font-size:8pt;color:var(--mut);text-align:right;white-space:nowrap}.who i{display:inline-block;border-bottom:1px solid var(--mut);width:42mm;margin-left:3px}.who i.s{width:14mm}'+
'.flow{column-count:2;column-gap:5mm;column-fill:balance}'+
'.blk{column-span:all;display:flex;gap:6px;align-items:center;background:var(--pri-soft);border-left:4px solid var(--pri);border-radius:3px 6px 6px 3px;padding:3px 8px;margin:6px 0 4px;font-weight:700;color:var(--pri);font-size:9pt;break-after:avoid}.blk small{font-weight:600;color:var(--mut)}'+
'.lesson{border:1px solid var(--line);border-radius:7px;padding:5px 7px 6px;margin:0 0 4mm;break-inside:auto}'+
'.hd{break-inside:avoid}.lesson header{break-after:avoid;margin-bottom:3px}.kick{display:inline-block;font-size:7pt;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#fff;background:var(--ok);border-radius:4px;padding:0 5px}.lesson h1{font-size:10.6pt;line-height:1.15;margin:2px 0 1px;color:var(--pri)}.sub{margin:0;color:var(--mut);font-size:8pt}'+
'.lesson p{margin:3px 0}.lesson ul,.lesson ol{margin:3px 0;padding-left:14px}.lesson li{margin:1px 0}h2,h3{font-size:9pt;margin:5px 0 2px;break-after:avoid}'+
'.it{display:grid;grid-template-columns:30% 1fr;gap:0 6px;padding:2px 5px;border:1px solid var(--line);margin-top:-1px;break-inside:avoid}.it b{color:var(--pri)}.lesson>.it:first-of-type,header+.it,.ill+.it{border-radius:5px 5px 0 0;margin-top:4px}'+
'.co{border-left:3px solid var(--pri);background:var(--pri-soft);border-radius:3px 6px 6px 3px;padding:3px 6px;margin:4px 0;break-inside:avoid}.co p{margin:1px 0 0}.co-l{font-size:6.8pt;letter-spacing:.06em;text-transform:uppercase;font-weight:800;color:var(--pri)}.co-ex{border-color:var(--amb);background:var(--ex-bg)}.co-ex .co-l{color:var(--ex)}.co-ana{border-color:var(--mut);background:var(--bg)}.co-ana .co-l{color:var(--mut)}.co-warn{border-color:var(--bad);background:var(--bad-soft)}.co-warn .co-l{color:var(--bad)}'+
'.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin:4px 0;break-inside:avoid}.tile{border:1px solid var(--line);border-radius:5px;padding:3px;text-align:center}.tile>div{font-size:13px!important;line-height:1}.tile b{display:block;font-size:8pt}.tile span{display:block;font-size:7.4pt;color:var(--mut);line-height:1.2}'+
'.pasos{border:1px solid var(--line);border-radius:6px;padding:3px 6px;margin:4px 0}.pxt{font-weight:700;color:var(--pri)}.px{display:flex;gap:5px;align-items:flex-start;padding:2px 0;border-top:1px dashed var(--line);break-inside:avoid}.pxn{flex:none;width:14px;height:14px;border-radius:50%;background:var(--ok);color:#fff;display:grid;place-items:center;font-size:7pt;font-weight:800}'+
'.ill{border:1px solid var(--line);border-radius:6px;padding:3px;margin:4px 0;background:var(--bg);break-inside:avoid}.ill svg{display:block;width:100%;height:auto;max-height:30mm;margin:0 auto}'+
'.tip{display:flex;gap:5px;align-items:flex-start;background:var(--ok-soft);border:1px solid color-mix(in srgb,var(--ok) 35%,#fff);border-radius:6px;padding:3px 6px;margin:5px 0 0;break-inside:avoid}.tip .ti{font-size:10pt;line-height:1}'+
'code{font:7.8pt Consolas,monospace;background:var(--bg);border-radius:3px;padding:0 2px}pre{font:7.4pt/1.25 Consolas,monospace;background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:3px 5px;white-space:pre-wrap;margin:3px 0;break-inside:avoid}'+
'table{width:100%;border-collapse:collapse;font-size:7.6pt;margin:3px 0;break-inside:avoid}th,td{border:1px solid var(--line);padding:1px 4px;text-align:left;vertical-align:top}th{background:var(--pri-soft)}'+
'.exw,.mw,.mph{max-width:100%;overflow:hidden;font-size:7.5pt;break-inside:avoid;margin:3px 0}.mw{border:1px solid var(--line);border-radius:5px}.mt{background:var(--bg);padding:1px 5px;font-size:7pt}.mt i{display:none}.mbd{padding:3px}.mcap{font-size:7.5pt;margin:2px 0}'+
'.sum{border:1.5px solid var(--ok);border-radius:7px;padding:0 7px 5px;margin:0 0 4mm;break-inside:avoid}.sum h4{display:inline-block;margin:0 0 3px -7px;background:var(--ok);color:#fff;border-radius:6px 0 6px 0;padding:1px 8px;font-size:8.5pt}.sum ul{margin:0;padding-left:13px}.sum .q{margin-top:3px;font-weight:600}.sum .ln{border-bottom:1px solid var(--line);height:5.5mm}'+
'.foot{display:flex;align-items:center;gap:8px;margin-top:4mm;color:var(--mut);font-size:7pt}.foot i{flex:1;border-top:1px solid var(--line)}.foot b{color:var(--pri);font-size:9pt;letter-spacing:.05em}'+
'@page{size:letter portrait;margin:8mm 8mm 9mm}@media print{body{background:#fff}.bar{display:none}.sheet{width:auto;margin:0;padding:0;box-shadow:none}}'+
'@media (max-width:600px){.sheet{padding:4mm;margin:6px auto}.flow{column-count:1}.cover{grid-template-columns:1fr}.who{text-align:left;white-space:normal}.who i{width:30mm}}';
function build(){var B=brand(),h='',n=0;
 ORDER.forEach(function(id){var S=SC(id),C=CH[id],L=lessonIdx(S);if(!L.length)return;
  h+='<div class="blk">'+(C?txt(C.k)+' · '+C.t:S.t)+(C&&C.time?' <small>· '+C.time+'</small>':'')+'</div>';
  L.forEach(function(i){n++;var d=clean(P[i]),k=d.querySelector(".kick");if(k)k.textContent="Lección "+n;h+=d.innerHTML});
  if(C&&C.sum&&C.sum.length)h+='<section class="sum"><h4>✔ Practica y repasa</h4><ul>'+C.sum.map(function(x){return '<li>'+x+'</li>'}).join("")+'</ul>'+(C.q?'<p class="q">✍ '+C.q+'</p><div class="ln"></div><div class="ln"></div>':'')+'</section>'});
 var mod=B.mod+(B.modName?': '+B.modName:'');
 return '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Apuntes '+txt(B.mod+' '+B.ra)+'</title><style>'+CSS+'\n'+illCss()+'</style></head><body>'+
  '<div class="bar"><button onclick="print()">🖨️ Imprimir o guardar PDF</button><span>En celular: toca el botón y elige «Guardar como PDF». Sale en hoja carta, lista para pegar en tu cuaderno.</span></div>'+
  '<div class="sheet"><div class="band"><b>MÓDULO:</b><span class="grow">'+txt(mod)+'</span><span>'+txt(B.ra)+'</span></div>'+
  '<div class="cover"><div><h1>'+txt(B.raName)+'</h1><p>Apuntes · '+txt(B.ra+(B.raName?' · '+B.raName:''))+'</p></div><div class="who">Nombre <i></i> Grupo <i class="s"></i></div></div>'+
  '<div class="flow">'+h+'</div><div class="foot"><i></i><span>Plantel 12627 · '+txt(B.mod+' · '+B.ra)+'</span><b>AulaVirtual</b></div></div></body></html>'}
function open(){var html=build(),w=null;try{w=window.open("","_blank")}catch(e){}
 if(w){w.document.open();w.document.write(html);w.document.close();return}
 var u=URL.createObjectURL(new Blob([html],{type:"text/html"}));location.href=u}
window.apuntes=open;
var st=document.createElement("style");st.textContent='.crumb .apx{margin-left:auto;border:1.5px solid var(--pri);background:var(--card);color:var(--pri);border-radius:999px;padding:5px 12px;font-weight:700;font-size:13px}.crumb .apx:hover{background:var(--pri-soft)}@media (max-width:560px){.crumb .apx{padding:4px 10px;font-size:12px}}';document.head.appendChild(st);
var _sec=sec;sec=function(id,p){_sec(id,p);if(ORDER.indexOf(id)<0)return;var c=document.querySelector("#main .crumb");if(!c||c.querySelector(".apx"))return;
 var b=document.createElement("button");b.className="apx";b.type="button";b.title="Descarga los apuntes de «Aprende» para imprimir y pegar en tu cuaderno";b.textContent="🖨️ Descargar apuntes";b.onclick=open;c.appendChild(b)}})();
