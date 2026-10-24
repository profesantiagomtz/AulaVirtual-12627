/*TABS3*/
var TABL=/*TABL*/{a:["Aprende","Teoría, esquemas y ejercicios"],d:["Diagnostica","Herramientas y simulador"],c:["Construye","Prácticas guiadas"]},CURTAB="",SECI=null;
function isTool(i){return /class="kick">[^<]*(Simulador|Herramienta)/.test(P[i])||/<h1>Simulador:/.test(P[i])}
function toolPages(){var r=[];ORDER.forEach(function(id){var S=SC(id);for(var i=S.a;i<=S.b;i++)if(isTool(i))r.push({i:i,s:id})});return r}
function firstOpen(){var n=null;ORDER.forEach(function(id){var c=cnt(SC(id));if(n===null&&c[0]<c[1])n=id});return n===null?ORDER[0]:n}
function tabbar(){var el=document.getElementById("tabs");
 if(!el){el=document.createElement("nav");el.id="tabs";el.className="tabs3";el.setAttribute("aria-label","Secciones del material");document.querySelector("#app > header.top").insertAdjacentElement("afterend",el)}
 el.innerHTML=[["a","📖","1. "],["d","🧪","2. "],["c","🛠","3. "]].map(function(t){return '<button data-t="'+t[0]+'" class="'+(CURTAB==t[0]?"on":"")+'"'+(CURTAB==t[0]?' aria-current="page"':"")+'><span class="ti3">'+t[1]+'</span><span><b>'+t[2]+TABL[t[0]][0]+'</b><small>'+TABL[t[0]][1]+'</small></span></button>'}).join("");
 el.querySelectorAll("button").forEach(function(b){b.onclick=function(){var k=b.dataset.t;k=="a"?sec(firstOpen()):k=="d"?diag():pracs()}})}
function diag(){CURTAB="d";mode(true);side("diag");var T=toolPages(),h='<nav class="crumb"><button id="bc">Inicio</button><span>›</span><span>'+TABL.d[0]+'</span></nav><article class="lesson"><header><span class="kick">🧪 '+TABL.d[0]+'</span><h1>'+TABL.d[1]+'</h1><p class="sub">Practica con las herramientas y comprueba lo que sabes antes de construir.</p></header></article>';
 if(T.length){h+='<h2 class="dgh">Herramientas y simuladores</h2>';T.forEach(function(t){var k=((P[t.i].match(/class="kick">([^<]*)/)||[])[1]||"").replace(/^\S+\s/,"");h+='<button class="prow" data-s="'+t.s+'" data-i="'+t.i+'"><b>'+(ST[t.i]?"✅ ":"🧪 ")+titleOf(t.i)+'</b><span class="d">'+k+' · '+CH[t.s].k+': '+CH[t.s].t+'</span></button>'})}
 h+='<h2 class="dgh">Comprueba lo que sabes</h2>';
 ORDER.forEach(function(id){var S=SC(id),al=acts(S),c=cnt(S);if(!al.length)return;var f=al.filter(function(i){return !ST[i]})[0];h+='<button class="prow" data-s="'+id+'" data-i="'+(f===undefined?al[0]:f)+'"><b>'+(c[0]>=c[1]?"✅ ":"")+CH[id].t+'</b><span class="d">'+CH[id].k+' · '+c[0]+' de '+c[1]+' actividades</span></button>'});
 MAIN.innerHTML=h;MAIN.querySelectorAll("[data-s]").forEach(function(b){b.onclick=function(){sec(b.dataset.s,+b.dataset.i)}});document.getElementById("bc").onclick=home;window.scrollTo(0,0)}
var _mode=mode,_sec=sec,_pracs=pracs,_prac=prac,_side=side,_go2=go2,_home=home;
mode=function(r){_mode(r);tabbar()};
sec=function(id,p){CURTAB=ORDER.indexOf(id)>-1?"a":"";SECI=p==null?null:p;_sec(id);SECI=null;tabbar()};
pracs=function(){CURTAB="c";_pracs();tabbar()};
prac=function(id){CURTAB="c";_prac(id);tabbar()};
home=function(){CURTAB="";_home()};
go2=function(g){if(g=="diag")return diag();if(g=="ev"||g=="home")CURTAB="";_go2(g)};
side=function(act){_side(act);SIDE.querySelectorAll(".sh").forEach(function(x){if(x.textContent=="Contenido")x.textContent="1 · "+TABL.a[0]});
 var pr=SIDE.querySelector('[data-g="pr"]');if(!pr)return;var d=document.createElement("div");
 d.innerHTML='<div class="sh">2 · '+TABL.d[0]+'</div><button class="sl'+(act=="diag"?" on":"")+'" data-g="diag"><span class="dot">🧪</span><span><b>'+TABL.d[1]+'</b></span></button><div class="sh">3 · '+TABL.c[0]+'</div>';
 while(d.firstChild){var n=d.firstChild;pr.parentNode.insertBefore(n,pr);if(n.dataset&&n.dataset.g)n.onclick=function(){closeD();go2("diag")}}};
