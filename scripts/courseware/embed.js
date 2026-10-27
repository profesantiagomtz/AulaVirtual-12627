(function(){var emb=false;try{emb=window.self!==window.top}catch(e){emb=true}
if(!emb)return;var R=document.documentElement,last=null;R.classList.add("embed");
function paint(el,m){var s=el.style,v=m.vars||{};for(var k in v)if(v[k])s.setProperty(k,v[k]);
 s.setProperty("--pri-soft","color-mix(in srgb,var(--pri) 11%,var(--card))");s.setProperty("--ok-soft","color-mix(in srgb,var(--ok) 13%,var(--card))");s.setProperty("--bad-soft","color-mix(in srgb,var(--bad) 12%,var(--card))");
 s.setProperty("--ex","color-mix(in srgb,var(--amb) 65%,var(--ink))");s.setProperty("--ex-bg","color-mix(in srgb,var(--amb) 15%,var(--card))");s.setProperty("--soft","var(--pri-soft)");s.setProperty("--exb","var(--ex-bg)");
 s.colorScheme=m.dark?"dark":"light";el.setAttribute("data-theme",m.dark?"dark":"light");if(m.skin)el.setAttribute("data-skin",m.skin);else el.removeAttribute("data-skin")}
function frames(){[].forEach.call(document.querySelectorAll("iframe"),function(f){try{if(last&&f.contentDocument&&f.contentDocument.documentElement)paint(f.contentDocument.documentElement,last)}catch(e){}})}
addEventListener("message",function(e){if(e.origin!==location.origin)return;var m=e.data;if(m&&m.type==="aula-theme"){last=m;paint(R,m);frames()}});
document.addEventListener("load",function(e){if(e.target&&e.target.tagName==="IFRAME")frames()},true);
try{parent.postMessage({type:"aula-theme-request"},location.origin)}catch(x){}})();
