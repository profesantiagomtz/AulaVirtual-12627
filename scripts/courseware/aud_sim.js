// Consola de auditoría simulada de la red de la Papelería Don Beto: escaneo y recopilación de información,
// comparación contra la línea base del plan de seguridad, métricas, nuevos requerimientos, acciones correctivas,
// actualizaciones, planes de contingencia con escalamiento e informe de balance. Nada sale del navegador.
var AUC={},AUS={};
function auE(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
// Línea base: las políticas del plan de seguridad que se definió en el R.A. 2.1.
var AUPOL=[["av","Antivirus activo y con firmas de los últimos 7 días"],["fw","Firewall activo"],["upd","Sin actualizaciones críticas pendientes"],["pw","Sin contraseñas de fábrica"],["rem","Sin servicios remotos inseguros abiertos (RDP, Telnet)"],["wifi","Wi-Fi con WPA2/WPA3 y WPS apagado"],["auth","Solo equipos autorizados en la red"],["bk","Respaldo diario correcto"]];
function auDevs(){return [
 {id:"CAJA-01",t:"PC de cobro · Windows 11",ip:"192.168.1.10",mac:"3C:52:82:1A:0F:10",auth:1,pc:1,av:1,avd:0,fw:1,upd:1,crit:1,ports:[],pw:0,bk:"22 de 30 respaldos correctos este mes",bkOk:0},
 {id:"PC-OFICINA",t:"PC de oficina · Windows 10",ip:"192.168.1.11",mac:"3C:52:82:1A:0F:11",auth:1,pc:1,av:0,avd:41,fw:1,upd:5,crit:2,ports:[3389],pw:0,bk:"No aplica (sin datos de ventas)",bkOk:1},
 {id:"IMPRESORA",t:"Multifuncional HP",ip:"192.168.1.20",mac:"A0:D3:C1:22:41:9E",auth:1,pc:0,ports:[23,80],pw:1,upd:0,crit:0},
 {id:"ROUTER",t:"Módem-router del proveedor",ip:"192.168.1.254",mac:"F4:6B:EF:00:12:34",auth:1,pc:0,ports:[80],pw:1,fwv:"2022.03",upd:1,crit:1,wifi:"WPA2-AES",wps:1},
 {id:"¿DESCONOCIDO?",t:"Fabricante desconocido",ip:"192.168.1.57",mac:"DA:A1:19:7C:55:02",auth:0,pc:0,ports:[]}]}
function auNew(id){var c=AUC[id]||{},s={used:{},devs:auDevs(),scan:false,info:{},cmp:{},met:{},reqs:[],cont:{},act:[],rep:[],tab:(c.tabs||["scan"])[0],cur:null,t:0,bkCfg:false};(c.setup||[]).forEach(function(f){f(s)});return s}
function auGet(id){if(!AUS[id]){var s=null;try{s=JSON.parse(localStorage.getItem(KEY+"-au-"+id)||"null")}catch(e){}AUS[id]=s&&s.devs?s:auNew(id)}return AUS[id]}
function auSave(id){try{localStorage.setItem(KEY+"-au-"+id,JSON.stringify(AUS[id]))}catch(e){}}
function auDev(S,id){return S.devs.filter(function(d){return d.id==id})[0]}
// ¿El equipo cumple la política p? null = no aplica.
function auPol(d,p){if(!d.auth&&p!="auth")return null;
 if(p=="av")return d.pc?!!(d.av&&d.avd<=7):null;if(p=="fw")return d.pc?!!d.fw:null;if(p=="upd")return d.upd==null?null:!d.crit;
 if(p=="pw")return d.pw==null?null:!d.pw;if(p=="rem")return !(d.ports||[]).some(function(x){return x==3389||x==23});
 if(p=="wifi")return d.wifi?(/WPA2|WPA3/.test(d.wifi)&&!d.wps):null;if(p=="auth")return !!d.auth;if(p=="bk")return d.bk?!!d.bkOk:null;return null}
function auComp(S,id){var d=auDev(S,id),r=AUPOL.map(function(p){return auPol(d,p[0])}).filter(function(x){return x!==null});return r.length?Math.round(100*r.filter(Boolean).length/r.length):100}
function auTotal(S){var y=0,n=0;S.devs.forEach(function(d){AUPOL.forEach(function(p){var v=auPol(d,p[0]);if(v!==null){n++;if(v)y++}})});return n?Math.round(100*y/n):100}
// Métricas: valor real calculado del estado actual de la red.
var AUMET=[["avpc","PCs con antivirus activo y al día (%)","100",function(S){var p=S.devs.filter(function(d){return d.pc});return Math.round(100*p.filter(function(d){return d.av&&d.avd<=7}).length/p.length)}],
 ["crit","Actualizaciones críticas pendientes (total)","0",function(S){return S.devs.reduce(function(a,d){return a+(d.auth?d.crit||0:0)},0)}],
 ["pw","Dispositivos con contraseña de fábrica","0",function(S){return S.devs.filter(function(d){return d.pw}).length}],
 ["unk","Dispositivos no autorizados conectados","0",function(S){return S.devs.filter(function(d){return !d.auth}).length}],
 ["bk","Respaldos correctos de la caja en el mes (de 30)","30",function(S){return S.devs[0].bkOk?30:22}]];
// Hallazgos que pueden convertirse en nuevos requerimientos.
var AUFIND=[["f_av","PC-OFICINA sin antivirus desde hace 41 días","Reactivar el antivirus y bloquear su desactivación con contraseña de administrador","Alta"],
 ["f_rdp","PC-OFICINA con escritorio remoto (RDP 3389) abierto","Cerrar RDP y usar una herramienta de soporte remoto con autorización","Alta"],
 ["f_pw","Impresora y router con usuario y contraseña de fábrica","Cambiar las contraseñas de fábrica por contraseñas robustas","Alta"],
 ["f_tel","Impresora con Telnet (23) habilitado","Deshabilitar Telnet y administrar la impresora solo por HTTPS","Media"],
 ["f_unk","Dispositivo desconocido conectado al Wi-Fi","Bloquear el dispositivo, cambiar la clave del Wi-Fi y filtrar por lista de equipos autorizados","Alta"],
 ["f_wps","Router con WPS encendido y firmware de 2022","Apagar WPS y actualizar el firmware del router","Media"],
 ["f_bk","8 respaldos fallidos de la caja este mes","Revisar el disco de respaldo, programar una copia en la nube y verificarla cada semana","Alta"]];
var AUMEAS=AUFIND.map(function(f){return f[2]}).concat(["Desinstalar el antivirus para que la PC sea más rápida","Apagar el router por las noches y no hacer nada más","Comprar otra impresora"]);
var AUACT={"CAJA-01":[["upd","🔄 Instalar actualizaciones"],["bkfix","💾 Reparar y verificar el respaldo"]],"PC-OFICINA":[["av","🛡️ Activar y actualizar antivirus"],["upd","🔄 Instalar actualizaciones"],["rdp","🔒 Cerrar escritorio remoto (3389)"]],
 "IMPRESORA":[["pw","🔑 Cambiar contraseña de fábrica"],["tel","🔒 Deshabilitar Telnet (23)"]],"ROUTER":[["pw","🔑 Cambiar contraseña de fábrica"],["bkcfg","💾 Respaldar configuración"],["fwup","⬆️ Actualizar firmware"],["wps","📶 Apagar WPS"]],"¿DESCONOCIDO?":[["block","⛔ Bloquear dispositivo y cambiar clave Wi-Fi"]]};
function auPwOk(p){return p.length>=10&&/[A-Z]/.test(p)&&/[a-z]/.test(p)&&/\d/.test(p)&&/[^A-Za-z0-9]/.test(p)}
function auDo(S,id,k){var d=auDev(S,id),m="";S.t++;
 if(k=="upd"){d.upd=0;d.crit=0;m="Actualizaciones instaladas en "+id+"."}
 if(k=="bkfix"){d.bkOk=1;d.bk="Respaldo reparado: copia local y en la nube verificadas";m="Respaldo de la caja reparado y verificado."}
 if(k=="av"){d.av=1;d.avd=0;m="Antivirus activado y con firmas de hoy."}
 if(k=="rdp"){d.ports=d.ports.filter(function(x){return x!=3389});m="Puerto 3389 cerrado."}
 if(k=="tel"){d.ports=d.ports.filter(function(x){return x!=23});m="Telnet deshabilitado."}
 if(k=="pw"){var p=prompt("Nueva contraseña para "+id+" (mínimo 10 caracteres con mayúsculas, minúsculas, números y símbolo):")||"";if(!auPwOk(p)){S.msg="✖ Contraseña débil: no se aplicó.";return}d.pw=0;m="Contraseña de fábrica cambiada en "+id+"."}
 if(k=="bkcfg"){S.bkCfg=true;m="Configuración del router respaldada en router_config_"+(S.t)+".bin."}
 if(k=="fwup"){if(!S.bkCfg){S.used.fw_nobk=1;if(!confirm("No has respaldado la configuración del router. Si la actualización falla perderás la configuración. ¿Continuar de todos modos?"))return}d.fwv="2026.10";d.upd=0;d.crit=0;S.used.fw_ok=1;m="Firmware actualizado a 2026.10"+(S.bkCfg?" (con respaldo previo).":" sin respaldo previo.")}
 if(k=="wps"){d.wps=0;m="WPS apagado."}
 if(k=="block"){S.devs=S.devs.filter(function(x){return x.auth});S.cur=null;m="Dispositivo bloqueado y clave del Wi-Fi cambiada."}
 S.used["do_"+k]=1;S.act.push({h:S.t,d:id,k:k,m:m});S.msg="✔ "+m}
function auView(S,c){var tabs=c.tabs||["scan"],h='<div class="autabs">'+tabs.map(function(t){return '<button data-tab="'+t+'" class="'+(S.tab==t?"on":"")+'">'+{scan:"📡 Escaneo",cmp:"⚖️ Comparar",met:"📏 Métricas",req:"📝 Requerimientos",fix:"🛠️ Acciones",cont:"🚨 Contingencia",rep:"📄 Informe"}[t]+'</button>'}).join("")+'</div><div class="aubody">';
 var T=S.tab;
 if(T=="scan"){h+='<div class="aubar"><button data-a="scan" class="btn sm">📡 Escanear la red 192.168.1.0/24</button></div>';
  if(!S.scan)h+='<p class="xm">Aún no has escaneado. El escaneo recopila los equipos conectados, sus puertos abiertos y su estado.</p>';
  else{h+='<table class="autb"><tr><th>Equipo</th><th>IP</th><th>MAC</th><th>Puertos</th><th></th></tr>'+S.devs.map(function(d){return '<tr class="'+(d.auth?"":"bad")+'"><td><b>'+auE(d.id)+'</b><br><small>'+auE(d.t)+'</small></td><td data-l="IP">'+d.ip+'</td><td data-l="MAC"><small>'+d.mac+'</small></td><td data-l="Puertos">'+((d.ports||[]).join(", ")||"—")+'</td><td><button data-a="info" data-v="'+auE(d.id)+'">🔎 Detalle</button></td></tr>'}).join("")+'</table>';
   var d=S.cur&&auDev(S,S.cur);if(d)h+='<div class="aucard"><b>'+auE(d.id)+'</b> · '+auE(d.t)+'<ul>'+(d.auth?'':'<li>⚠️ No está en el inventario de equipos autorizados.</li>')+(d.pc?'<li>Antivirus: '+(d.av?"activo":"<b>desactivado</b>")+' · firmas de hace '+d.avd+' días</li><li>Firewall: '+(d.fw?"activo":"<b>apagado</b>")+'</li>':'')+(d.upd!=null?'<li>Actualizaciones pendientes: '+d.upd+(d.crit?' (<b>'+d.crit+' críticas</b>)':'')+'</li>':'')+(d.fwv?'<li>Firmware: '+d.fwv+'</li>':'')+(d.pw!=null?'<li>Acceso de administración: '+(d.pw?"<b>admin / admin (de fábrica)</b>":"contraseña propia")+'</li>':'')+(d.wifi?'<li>Wi-Fi: '+d.wifi+' · WPS '+(d.wps?"<b>encendido</b>":"apagado")+'</li>':'')+((d.ports||[]).length?'<li>Puertos abiertos: '+d.ports.map(function(p){return p+" ("+({23:"Telnet, sin cifrar",80:"HTTP",3389:"Escritorio remoto"}[p]||"")+")"}).join(", ")+'</li>':'')+(d.bk?'<li>Respaldo: '+auE(d.bk)+'</li>':'')+'</ul></div>'}}
 if(T=="cmp"){h+='<p class="xm">Elige un equipo y compáralo con la <b>línea base</b> del plan de seguridad.</p><div class="aubar">'+S.devs.map(function(d){return '<button data-a="cmp" data-v="'+auE(d.id)+'" class="'+(S.cur==d.id?"on":"")+'">'+auE(d.id)+(S.cmp[d.id]?" · "+auComp(S,d.id)+"%":"")+'</button>'}).join("")+'</div>';
  var e=S.cur&&S.cmp[S.cur]&&auDev(S,S.cur);if(e)h+='<table class="autb"><tr><th>Política del plan</th><th>Resultado</th></tr>'+AUPOL.map(function(p){var v=auPol(e,p[0]);return '<tr><td>'+p[1]+'</td><td>'+(v===null?'<span class="xm">No aplica</span>':v?'<span class="aug">✔ Cumple</span>':'<span class="aur">✖ No cumple</span>')+'</td></tr>'}).join("")+'<tr><th>Cumplimiento</th><th>'+auComp(S,e.id)+'%</th></tr></table>'}
 if(T=="met"){h+='<p class="xm">Calcula cada métrica con lo que encontraste en el escaneo y compárala con la meta.</p><table class="autb"><tr><th>Métrica</th><th>Meta</th><th>Obtenido</th><th>¿Cumple?</th></tr>'+AUMET.map(function(m){var v=S.met[m[0]]||{};return '<tr><td>'+m[1]+'</td><td data-l="Meta">'+m[2]+'</td><td data-l="Obtenido"><input data-m="'+m[0]+'" value="'+auE(v.v||"")+'" inputmode="numeric" size="4"></td><td data-l="¿Cumple?"><select data-mc="'+m[0]+'"><option value="">—</option><option'+(v.c=="Sí"?" selected":"")+'>Sí</option><option'+(v.c=="No"?" selected":"")+'>No</option></select></td></tr>'}).join("")+'</table><div class="aubar"><button data-a="metchk" class="btn sm">Comprobar métricas</button></div>'}
 if(T=="req"){h+='<div class="aucard"><b>Nuevo requerimiento de seguridad</b><label>Hallazgo <select data-r="f"><option value="">Elige…</option>'+AUFIND.map(function(f){return '<option value="'+f[0]+'">'+f[1]+'</option>'}).join("")+'</select></label><label>Medida para solucionarlo <select data-r="m"><option value="">Elige…</option>'+AUMEAS.map(function(x,i){return '<option value="'+i+'">'+x+'</option>'}).join("")+'</select></label><label>Prioridad <select data-r="p"><option>Alta</option><option>Media</option><option>Baja</option></select></label><button data-a="addreq" class="btn sm">Registrar requerimiento</button></div>'+
  (S.reqs.length?'<table class="autb"><tr><th>#</th><th>Hallazgo</th><th>Medida</th><th>Prioridad</th></tr>'+S.reqs.map(function(r,i){var f=AUFIND.filter(function(x){return x[0]==r.f})[0];return '<tr><td>R'+(i+1)+'</td><td>'+f[1]+'</td><td>'+AUMEAS[r.m]+'</td><td>'+r.p+'</td></tr>'}).join("")+'</table>':'')}
 if(T=="fix"){h+='<p class="xm">Aplica las acciones correctivas y las actualizaciones. Después vuelve a <b>Comparar</b> para medir el cumplimiento.</p>'+S.devs.map(function(d){return '<div class="aucard"><b>'+auE(d.id)+'</b> <small>'+auComp(S,d.id)+'% de cumplimiento</small><div class="aubar">'+(AUACT[d.id]||[]).map(function(a){return '<button data-a="do" data-d="'+auE(d.id)+'" data-v="'+a[0]+'">'+a[1]+'</button>'}).join("")+'</div></div>'}).join("")+(S.act.length?'<b>Bitácora de cambios</b><ol class="aulog">'+S.act.map(function(x){return '<li>'+auE(x.m)+'</li>'}).join("")+'</ol>':'')}
 if(T=="cont"){h+=(c.scen||[]).map(function(sc){var r=S.cont[sc.id]||{};return '<div class="aucard"><b>🚨 '+sc.t+'</b><p style="margin:4px 0">'+sc.d+'</p>'+[["a","Primera acción",sc.a],["s","Alternativa de solución",sc.s],["e","Escalar a",sc.e]].map(function(q){return '<label>'+q[1]+' <select data-cs="'+sc.id+'.'+q[0]+'"><option value="">Elige…</option>'+q[2].map(function(o,i){return '<option value="'+i+'"'+(r[q[0]]==String(i)?" selected":"")+'>'+o+'</option>'}).join("")+'</select></label>'}).join("")+'<button data-a="cont" data-v="'+sc.id+'" class="btn sm">Activar plan</button>'+(r.res?'<p class="'+(r.ok?"aug":"aur")+'">'+r.res+'</p>':'')+'</div>'}).join("")}
 if(T=="rep"){h+='<div class="aubar"><button data-a="rep" class="btn sm">📄 Generar informe de balance</button></div>'+(S.rep.length?S.rep.map(function(r,i){return '<div class="aucard"><b>Informe '+(i+1)+' · Papelería Don Beto</b><br>Cumplimiento general del plan: <b>'+r.tot+'%</b><br>'+r.det+'<br>Requerimientos registrados: '+r.req+' · Acciones aplicadas: '+r.act+'</div>'}).join(""):'<p class="xm">El informe resume el cumplimiento de cada equipo contra el plan de seguridad.</p>')}
 return h+'<p class="xmsg" role="status">'+(S.msg||"")+'</p></div>'}
function auApi(S){return {S:S,used:function(k){return !!S.used[k]},scan:S.scan,info:function(id){return !!S.info[id]},cmp:function(id){return !!S.cmp[id]},comp:function(id){return auComp(S,id)},total:function(){return auTotal(S)},
 dev:function(id){return auDev(S,id)},metOk:function(k){return !!(S.met[k]&&S.met[k].ok)},reqs:S.reqs,reqOk:function(){var u={};S.reqs.forEach(function(r){var f=AUFIND.filter(function(x){return x[0]==r.f})[0];if(f&&AUMEAS[r.m]==f[2]&&r.p==f[3])u[r.f]=1});return Object.keys(u).length},
 cont:function(k){return !!(S.cont[k]&&S.cont[k].ok)},act:S.act,rep:S.rep}}
function auTasks(id){var S=auGet(id),a=auApi(S);return (AUC[id].tasks||[]).map(function(t){var ok=false;try{ok=!!t[1](a)}catch(e){}return {text:t[0],ok:ok}})}
function auPaint(d){var b=d.querySelector(".ausim"),id=b.dataset.id,S=auGet(id);b.querySelector(".aubody0").innerHTML=auView(S,AUC[id]);S.msg="";
 var ts=auTasks(id);b.querySelector(".auts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("");return ts}
var AUCSS='.ausim .auts{list-style:none;padding:0;margin:0 0 12px;display:grid;gap:6px}.ausim .auts li{border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14.5px}.ausim .auts li.y{border-color:var(--ok);background:var(--ok-soft)}'+
 '.auwin{border:1.5px solid #c8ccd2;border-radius:12px;overflow:hidden;background:#fff;color:#1f2937;font:13px system-ui}.auwin button,.auwin select,.auwin input{font:13px system-ui;color:#111827}.autit{background:#0f3d3a;color:#fff;padding:6px 10px;font-weight:700;font-size:12.5px}'+
 '.autabs{display:flex;gap:2px;background:#e5e7eb;padding:4px 6px 0;overflow-x:auto}.autabs button{border:0;background:#d1d5db;border-radius:8px 8px 0 0;padding:6px 10px;cursor:pointer;white-space:nowrap}.autabs button.on{background:#fff;font-weight:700}'+
 '.aubody{padding:10px;display:grid;gap:8px;min-height:240px;align-content:start}.aubar{display:flex;gap:6px;flex-wrap:wrap}.aubar button:not(.btn),.autb button{border:1px solid #cbd5e1;background:#fff;border-radius:8px;padding:5px 9px;cursor:pointer}.aubar button.on{background:#dbeafe;border-color:#60a5fa}'+
 '.autb{border-collapse:collapse;width:100%}.autb th,.autb td{border:1px solid #e5e7eb;padding:5px 7px;text-align:left;vertical-align:top}.autb th{background:#f3f4f6}.autb tr.bad td{background:#fdecee}.autb input{width:64px;border:1px solid #cbd5e1;border-radius:6px;padding:3px 6px}.autb select{border:1px solid #cbd5e1;border-radius:6px;padding:3px}'+
 '.aucard{border:1px solid #cbd5e1;border-radius:10px;padding:8px 10px;display:grid;gap:6px;background:#f9fafb}.aucard ul{margin:4px 0;padding-left:18px}.aucard label{display:grid;gap:2px;font-size:12.5px}.aucard select{border:1px solid #cbd5e1;border-radius:6px;padding:5px;background:#fff;max-width:100%}.aulog{margin:0;padding-left:20px}'+
 '.aug{color:#1e8e4e;font-weight:700}.aur{color:#C62F3A;font-weight:700}.ausim .xm{color:#6b7280;margin:0}.ausim .xmsg{color:#1e3a8a;font-weight:600;margin:0;min-height:1em}'+
 '@media(max-width:640px){.autb tr{display:grid;border:1px solid #e5e7eb;border-radius:8px;margin-bottom:6px;padding:4px}.autb th,.autb td{border:0;padding:2px 4px}.autb tr:first-child{display:none}.autb{border:0}.autb td[data-l]::before{content:attr(data-l) ": ";font-weight:600;color:#4b5563}}';
function pAu(ic,t,inf,cfg){K++;AUC[cfg.id]=cfg;return '<article class="lesson"><header><span class="kick">'+ic+' Simulador</span><h1>'+t+'</h1><p class="sub">'+inf+'</p></header><style>'+AUCSS+'</style><div class="ausim" data-id="'+cfg.id+'">'+(cfg.intro?'<p>'+cfg.intro+'</p>':'')+'<h3 style="margin:8px 0">Retos</h3><ol class="auts"></ol><div class="auwin"><div class="autit">Consola de auditoría · Red de la Papelería Don Beto</div><div class="aubody0"></div></div><div class="aubar" style="margin-top:8px"><button type="button" class="btn ghost sm aurst">↺ Reiniciar</button></div></div>'+(cfg.hint?'<p class="take"><b>Pista:</b> '+cfg.hint+'</p>':'')+'<div class="chk"><button class="btn c">Revisar retos</button></div><div class="res" role="status"></div></article>'}
function auInit(d){var b=d.querySelector(".ausim"),id=b.dataset.id;auPaint(d);
 function done(){auSave(id);auPaint(d)}
 b.addEventListener("click",function(e){var S=auGet(id),t=e.target,tb=t.closest("[data-tab]"),x=t.closest("[data-a]");
  if(tb){S.tab=tb.dataset.tab;S.used["tab_"+S.tab]=1;done();return}if(!x)return;var a=x.dataset.a,v=x.dataset.v;
  if(a=="scan"){S.scan=true;S.used.scan=1;S.msg="✔ 5 dispositivos encontrados. Uno no está en el inventario."}
  if(a=="info"){S.cur=v;S.info[v]=1}
  if(a=="cmp"){S.cur=v;S.cmp[v]=1;S.used.cmp=1}
  if(a=="metchk"){var bad=0;AUMET.forEach(function(m){var r=S.met[m[0]]||{},real=m[3](S),ok=String(r.v).trim()==String(real)&&r.c==(String(real)==m[2]?"Sí":"No");r.ok=ok;S.met[m[0]]=r;if(!ok)bad++});S.used.metchk=1;S.msg=bad?"✖ "+bad+" métrica(s) con error. Revisa el escaneo y la comparación.":"✔ Todas las métricas son correctas."}
  if(a=="addreq"){var R=function(k){return b.querySelector('[data-r="'+k+'"]').value};if(!R("f")||R("m")===""){S.msg="Elige el hallazgo y la medida.";done();return}if(S.reqs.some(function(q){return q.f==R("f")})){S.reqs=S.reqs.filter(function(q){return q.f!=R("f")})}S.reqs.push({f:R("f"),m:+R("m"),p:R("p")});var f=AUFIND.filter(function(z){return z[0]==R("f")})[0];S.msg=AUMEAS[+R("m")]==f[2]?(R("p")==f[3]?"✔ Requerimiento registrado.":"⚠ Registrado, pero revisa la prioridad: ¿qué tan grave es el riesgo?"):"✖ Esa medida no resuelve el hallazgo. Elige otra."}
  if(a=="do")auDo(S,x.dataset.d,v);
  if(a=="cont"){var sc=(AUC[id].scen||[]).filter(function(z){return z.id==v})[0],r=S.cont[v]=S.cont[v]||{};if(r.a==null||r.s==null||r.e==null||r.a===""||r.s===""||r.e===""){S.msg="Completa las tres decisiones del plan.";done();return}
   var er=[];if(+r.a!=sc.ok[0])er.push("primera acción");if(+r.s!=sc.ok[1])er.push("alternativa");if(+r.e!=sc.ok[2])er.push("escalamiento");r.ok=!er.length;r.res=r.ok?"✔ "+sc.win:"✖ Revisa: "+er.join(", ")+".";S.used.cont=1}
  if(a=="rep"){S.rep.push({tot:auTotal(S),det:S.devs.map(function(d){return auE(d.id)+": "+auComp(S,d.id)+"%"}).join(" · "),req:S.reqs.length,act:S.act.length});S.used.rep=1}
  done()});
 b.addEventListener("change",function(e){var S=auGet(id),t=e.target;
  if(t.dataset.m){S.met[t.dataset.m]=S.met[t.dataset.m]||{};S.met[t.dataset.m].v=t.value;auSave(id);return}
  if(t.dataset.mc){S.met[t.dataset.mc]=S.met[t.dataset.mc]||{};S.met[t.dataset.mc].c=t.value;auSave(id);return}
  if(t.dataset.cs){var p=t.dataset.cs.split(".");S.cont[p[0]]=S.cont[p[0]]||{};S.cont[p[0]][p[1]]=t.value;auSave(id);return}});
 b.querySelector(".aurst").onclick=function(){if(!confirm("¿Reiniciar el simulador? Se borra todo lo que hiciste aquí."))return;AUS[id]=auNew(id);done()}}
function auCheck(d){var ts=auPaint(d),ok=ts.filter(function(x){return x.ok}).length,n=ts.length,f=ts.filter(function(x){return !x.ok})[0];return {ok:ok,total:n,msg:ok==n?"¡Todos los retos resueltos! Lleva estos resultados a tu portafolio.":ok+" de "+n+" retos. Sigue con: «"+f.text.replace(/<[^>]*>/g,"")+"»"}}
