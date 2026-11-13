(function(){/* Dibujos propios en lugar de emojis (regla de AulaVirtual: no se usan emojis como imágenes).
 Los dibujos salen de scripts/icons/aula_icons.py; embed_patch.py los pega aquí en lugar de ICONS. */
var D=/*ICONS*/{},I=D.icons||{},M=D.emoji||{};
var keys=Object.keys(M).sort(function(a,b){return b.length-a.length});
function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")}
var SRC="(?:"+keys.map(esc).join("|")+")️?|[\u{1F1E6}-\u{1F1FF}\u{1F300}-\u{1FAFF}]️?(?:‍[\u{1F300}-\u{1FAFF}☀-➿]️?)*|[️‍]";
var RE=new RegExp(SRC,"gu");
function has(s){RE.lastIndex=0;var r=RE.test(s);RE.lastIndex=0;return r}
function svg(n){var i=I[n];if(!i)return "";
 return i.art?'<svg class="aico aart" viewBox="0 0 48 48" width="1.3em" height="1.3em" style="vertical-align:-.28em;overflow:visible" aria-hidden="true" focusable="false">'+i.b+'</svg>'
 :'<svg class="aico" viewBox="0 0 24 24" width="1.15em" height="1.15em" style="vertical-align:-.2em;overflow:visible" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+i.b+'</svg>'}
function swap(m){return svg(M[m.replace(/️/g,"")]||M[m])}
function plain(s){return s.replace(RE,"").replace(/^\s+(?=\S)/,"").replace(/ {2,}/g," ")}
function escH(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
/* Para HTML armado como texto (p. ej. los apuntes para imprimir). */
function html(h){var raw=false;return String(h).split(/(<[^>]*>)/).map(function(p){
 if(p.charAt(0)==="<"){var t=/^<(\/?)(script|style|title|textarea|option)\b/i.exec(p);if(t)raw=!t[1];return has(p)?p.replace(RE,""):p}
 if(raw||!has(p))return p;return p.replace(RE,swap)}).join("")}
var SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,OPTION:1,OPTGROUP:1,TITLE:1,NOSCRIPT:1,TEMPLATE:1};
var ATTR=["title","placeholder","aria-label","alt"];
function text(n){var s=n.nodeValue,p=n.parentNode;if(!p||!s||!has(s))return;
 if(SKIP[p.nodeName]||p.namespaceURI==="http://www.w3.org/2000/svg"||p.isContentEditable){if(p.nodeName!=="SCRIPT"&&p.nodeName!=="STYLE")n.nodeValue=plain(s);return}
 var t=document.createElement("template");t.innerHTML=escH(s).replace(RE,swap);p.replaceChild(t.content,n)}
function attrs(el){for(var i=0;i<ATTR.length;i++){var v=el.getAttribute(ATTR[i]);if(v&&has(v))el.setAttribute(ATTR[i],plain(v))}
 if(el.tagName==="INPUT"&&/^(button|submit|reset)$/i.test(el.type)&&has(el.value))el.value=plain(el.value)}
function walk(root){if(!root)return;if(root.nodeType===3){text(root);return}if(root.nodeType!==1&&root.nodeType!==11)return;
 if(root.nodeType===1){if(root.namespaceURI==="http://www.w3.org/2000/svg")return;attrs(root)}
 var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),list=[],n;while((n=w.nextNode()))if(has(n.nodeValue))list.push(n);list.forEach(text);
 if(root.querySelectorAll)[].forEach.call(root.querySelectorAll("[title],[placeholder],[aria-label],[alt],input"),attrs)}
window.aulaIconsHtml=html;window.aulaIconSvg=svg;
["alert","confirm","prompt"].forEach(function(k){var f=window[k];if(typeof f!=="function")return;window[k]=function(m,d){return f.call(window,typeof m==="string"?plain(m):m,d)}});
function start(){walk(document.body);try{document.title=plain(document.title)}catch(e){}
 new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var m=ms[i];
  if(m.type==="characterData")text(m.target);
  else if(m.type==="attributes")attrs(m.target);
  else for(var j=0;j<m.addedNodes.length;j++)walk(m.addedNodes[j])}})
 .observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:ATTR})}
if(document.body)start();else document.addEventListener("DOMContentLoaded",start)})();
