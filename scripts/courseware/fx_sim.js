// Hoja de cálculo simulada con fórmulas y funciones: nada sale de este navegador.
var FC={},FS={},FCOLS="ABCDEFGHIJ",FERR={d0:"#¡DIV/0!",v:"#¡VALOR!",n:"#¿NOMBRE?",r:"#¡REF!",na:"#N/D",c:"#CIRC"};
function fE(c){return {e:c}}
function fIsE(v){return v&&typeof v=="object"&&v.e!==undefined}
function fIsA(v){return v&&typeof v=="object"&&v.a!==undefined}
function fNew(id){var c=FC[id],sh=c.sheets.map(function(s){var cells={},nf={};Object.keys(s.data||{}).forEach(function(k){var x=s.data[k];cells[k]=typeof x=="object"?String(x.v):String(x);if(typeof x=="object"&&x.nf)nf[k]=x.nf});return {n:s.n,cells:cells,nf:nf,cw:s.cw||{}}});return {sheets:sh,cur:0,sel:"A1",anc:"A1",names:JSON.parse(JSON.stringify(c.names||{})),used:{},show:false}}
function fGet(id){if(!FS[id]){var s=null;try{s=JSON.parse(localStorage.getItem(KEY+"-fx-"+id)||"null")}catch(e){}FS[id]=s&&s.sheets&&s.sheets.length==FC[id].sheets.length?s:fNew(id)}return FS[id]}
function fSave(id){try{localStorage.setItem(KEY+"-fx-"+id,JSON.stringify(FS[id]))}catch(e){}}
function fParse(s){var m=/^\$?([A-J])\$?([0-9]{1,2})$/.exec(String(s).trim().toUpperCase());return m?{c:FCOLS.indexOf(m[1]),r:+m[2]}:null}
function fRange(s){var p=String(s||"").toUpperCase().replace(/\s/g,"").replace(/\$/g,"").split(":");if(p.length>2)return null;var a=fParse(p[0]),b=fParse(p[1]||p[0]);if(!a||!b)return null;return {c1:Math.min(a.c,b.c),c2:Math.max(a.c,b.c),r1:Math.min(a.r,b.r),r2:Math.max(a.r,b.r)}}
function fRstr(g){var a=FCOLS[g.c1]+g.r1,b=FCOLS[g.c2]+g.r2;return a==b?a:a+":"+b}
function fNoAcc(s){return String(s).normalize("NFD").replace(/[̀-ͯ]/g,"")}
function fSerial(y,m,d){return Math.round((Date.UTC(y,m-1,d)-Date.UTC(1899,11,30))/864e5)}
function fDate(n){var d=new Date(Date.UTC(1899,11,30)+Math.floor(n)*864e5);return {y:d.getUTCFullYear(),m:d.getUTCMonth()+1,d:d.getUTCDate()}}
function fRaw(raw){raw=String(raw);if(raw==="")return "";var t=raw.trim();if(/^-?\d+(\.\d+)?$/.test(t))return +t;if(/^-?\d+(\.\d+)?%$/.test(t))return +t.slice(0,-1)/100;var m=/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(t);if(m)return fSerial(+m[3],+m[2],+m[1]);if(/^verdadero$/i.test(t))return true;if(/^falso$/i.test(t))return false;return raw}
// ---------- Analizador de fórmulas ----------
function fTok(src){var out=[],i=0,m,re=[["str",/^"([^"]|"")*"/],["num",/^\d+(\.\d+)?/],["ref",/^(?:(?:'[^']+'|[A-Za-zÁ-úñÑ_][A-Za-z0-9Á-úñÑ_]*)!)?\$?[A-J]\$?\d{1,2}(?::\$?[A-J]\$?\d{1,2})?(?![A-Za-z0-9_.(])/i],["id",/^[A-Za-zÁ-úñÑ_][A-Za-z0-9Á-úñÑ_.]*/],["op",/^(<>|<=|>=|[-+*\/^&=<>%(),;{}:])/]];
 while(i<src.length){if(/\s/.test(src[i])){i++;continue}var s=src.slice(i),ok=false;for(var k=0;k<re.length;k++){m=re[k][1].exec(s);if(m){out.push({t:re[k][0],v:m[0]});i+=m[0].length;ok=true;break}}if(!ok)throw fE(FERR.n)}return out}
function fEval(S,id,sheet,src,cache,stack){var T=fTok(src),p=0,cfg=FC[id];
 function peek(){return T[p]}function eat(v){if(T[p]&&T[p].t=="op"&&T[p].v==v){p++;return true}return false}
 function num(v){if(fIsE(v))throw v;if(fIsA(v))v=v.a[0][0];if(fIsE(v))throw v;if(v===""||v===null||v===undefined)return 0;if(typeof v=="boolean")return v?1:0;if(typeof v=="number")return v;var r=fRaw(v);if(typeof r=="number")return r;throw fE(FERR.v)}
 function txt(v){if(fIsE(v))throw v;if(fIsA(v))v=v.a[0][0];if(fIsE(v))throw v;if(typeof v=="boolean")return v?"VERDADERO":"FALSO";if(typeof v=="number")return String(Math.round(v*1e10)/1e10);return v===undefined||v===null?"":String(v)}
 function map2(a,b,f){if(fIsA(a)||fIsA(b)){var A=fIsA(a)?a.a:null,B=fIsA(b)?b.a:null,R=A?A.length:B.length,C=A?A[0].length:B[0].length,o=[];for(var r=0;r<R;r++){o[r]=[];for(var c=0;c<C;c++){var x=A?A[r][c]:a,y=B?B[r][c]:b;try{o[r][c]=f(x,y)}catch(e){if(fIsE(e))o[r][c]=e;else throw e}}}return {a:o}}return f(a,b)}
 function cmp(x,y,op){if(fIsE(x))throw x;if(fIsE(y))throw y;var a=x===""?(typeof y=="string"?"":0):x,b=y===""?(typeof x=="string"?"":0):y;if(typeof a=="string"&&typeof b!="string"){var r=fRaw(a);if(typeof r=="number")a=r}if(typeof b=="string"&&typeof a!="string"){var r2=fRaw(b);if(typeof r2=="number")b=r2}if(typeof a=="string")a=fNoAcc(a).toLowerCase();if(typeof b=="string")b=fNoAcc(b).toLowerCase();if(typeof a!=typeof b){a=typeof a=="string"?2:typeof a=="boolean"?3:1;b=typeof b=="string"?2:typeof b=="boolean"?3:1}return op=="="?a==b:op=="<>"?a!=b:op=="<"?a<b:op==">"?a>b:op=="<="?a<=b:a>=b}
 function sheetIdx(n){n=n.replace(/^'|'$/g,"");for(var i=0;i<S.sheets.length;i++)if(S.sheets[i].n.toLowerCase()==n.toLowerCase())return i;throw fE(FERR.r)}
 function cell(si,k){return fCell(S,id,si,k,cache,stack)}
 function refVal(tok){var q=tok.v,si=sheet,ix=q.indexOf("!");if(ix>-1){si=sheetIdx(q.slice(0,ix));q=q.slice(ix+1)}var g=fRange(q);if(!g)throw fE(FERR.r);if(g.c2>=FC[id].sheets[si].cols||g.r2>FC[id].sheets[si].rows)throw fE(FERR.r);if(g.c1==g.c2&&g.r1==g.r2&&q.indexOf(":")<0){return cell(si,FCOLS[g.c1]+g.r1)}var o=[];for(var r=g.r1;r<=g.r2;r++){var row=[];for(var c=g.c1;c<=g.c2;c++)row.push(cell(si,FCOLS[c]+r));o.push(row)}return {a:o}}
 function nameVal(n){var k=Object.keys(S.names).filter(function(x){return x.toLowerCase()==n.toLowerCase()})[0];if(!k)throw fE(FERR.n);var t=S.names[k],si=sheet,ix=t.indexOf("!");if(ix>-1){si=sheetIdx(t.slice(0,ix));t=t.slice(ix+1)}return refVal({v:S.sheets[si].n.indexOf(" ")>-1?"'"+S.sheets[si].n+"'!"+t:S.sheets[si].n+"!"+t})}
 function flat(args){var o=[];args.forEach(function(a){if(fIsA(a))a.a.forEach(function(r){r.forEach(function(v){o.push({v:v,ref:true})})});else o.push({v:a,ref:false})});return o}
 function nums(args,strict){var o=[];flat(args).forEach(function(x){var v=x.v;if(fIsE(v))throw v;if(typeof v=="number")o.push(v);else if(!x.ref&&strict!==false){if(typeof v=="boolean")o.push(v?1:0);else if(typeof v=="string"&&v!==""){var r=fRaw(v);if(typeof r!="number")throw fE(FERR.v);o.push(r)}}});return o}
 function crit(c){var m=/^(<>|<=|>=|=|<|>)?(.*)$/.exec(txt(c)),op=m[1]||"=",val=m[2],n=fRaw(val);return function(x){if(x===""||x===undefined)return false;if(fIsE(x))return false;if(typeof n=="number"&&typeof x=="number")return op=="="?x==n:op=="<>"?x!=n:op=="<"?x<n:op==">"?x>n:op=="<="?x<=n:x>=n;if(typeof x=="number"&&typeof n!="number")return op=="<>";var a=fNoAcc(String(x)).toLowerCase(),b=fNoAcc(String(val)).toLowerCase();if(b.indexOf("*")>-1){var rx=new RegExp("^"+b.replace(/[.+?^${}()|[\]\\]/g,"\\$&").replace(/\*/g,".*")+"$");return op=="<>"?!rx.test(a):rx.test(a)}return op=="<>"?a!=b:a==b}}
 var FN={SUMA:function(a){return nums(a).reduce(function(s,x){return s+x},0)},
  PRODUCTO:function(a){var n=nums(a);return n.length?n.reduce(function(s,x){return s*x},1):0},
  PROMEDIO:function(a){var n=nums(a);if(!n.length)throw fE(FERR.d0);return n.reduce(function(s,x){return s+x},0)/n.length},
  MAX:function(a){var n=nums(a);return n.length?Math.max.apply(0,n):0},MIN:function(a){var n=nums(a);return n.length?Math.min.apply(0,n):0},
  CONTAR:function(a){return flat(a).filter(function(x){return typeof x.v=="number"}).length},
  CONTARA:function(a){return flat(a).filter(function(x){return x.v!==""&&x.v!==undefined}).length},
  "CONTAR.SI":function(a){var f=crit(a[1]);return flat([a[0]]).filter(function(x){return f(x.v)}).length},
  "SUMAR.SI":function(a){var f=crit(a[1]),r=flat([a[0]]),s=a[2]?flat([a[2]]):r,t=0;r.forEach(function(x,i){if(f(x.v)&&typeof s[i].v=="number")t+=s[i].v});return t},
  MEDIANA:function(a){var n=nums(a).sort(function(x,y){return x-y});if(!n.length)throw fE(FERR.na);var m=n.length>>1;return n.length%2?n[m]:(n[m-1]+n[m])/2},
  MODA:function(a){var n=nums(a),c={},b=null,bc=1;n.forEach(function(x){c[x]=(c[x]||0)+1});n.forEach(function(x){if(c[x]>bc){bc=c[x];b=x}});if(b===null)throw fE(FERR.na);return b},
  REDONDEAR:function(a){var n=num(a[0]),d=num(a[1]),f=Math.pow(10,d);return Math.round(Math.abs(n)*f+1e-9)/f*(n<0?-1:1)},
  ENTERO:function(a){return Math.floor(num(a[0]))},ABS:function(a){return Math.abs(num(a[0]))},
  RESIDUO:function(a){var d=num(a[1]);if(d==0)throw fE(FERR.d0);var n=num(a[0]);return n-d*Math.floor(n/d)},
  POTENCIA:function(a){return Math.pow(num(a[0]),num(a[1]))},RAIZ:function(a){var n=num(a[0]);if(n<0)throw fE("#¡NUM!");return Math.sqrt(n)},
  HOY:function(){var d=new Date();return fSerial(d.getFullYear(),d.getMonth()+1,d.getDate())},
  AHORA:function(){var d=new Date();return fSerial(d.getFullYear(),d.getMonth()+1,d.getDate())+(d.getHours()*60+d.getMinutes())/1440},
  ANO:function(a){return fDate(num(a[0])).y},MES:function(a){return fDate(num(a[0])).m},DIA:function(a){return fDate(num(a[0])).d},
  DIAS:function(a){return Math.floor(num(a[0]))-Math.floor(num(a[1]))},
  FECHA:function(a){return fSerial(num(a[0]),num(a[1]),num(a[2]))},
  IZQUIERDA:function(a){return txt(a[0]).slice(0,a[1]===undefined?1:num(a[1]))},
  DERECHA:function(a){var s=txt(a[0]),n=a[1]===undefined?1:num(a[1]);return n?s.slice(-n):""},
  EXTRAE:function(a){var i=num(a[1]);if(i<1)throw fE(FERR.v);return txt(a[0]).substr(i-1,num(a[2]))},
  LARGO:function(a){return txt(a[0]).length},MAYUSC:function(a){return txt(a[0]).toUpperCase()},MINUSC:function(a){return txt(a[0]).toLowerCase()},
  NOMPROPIO:function(a){return txt(a[0]).toLowerCase().replace(/(^|[^A-Za-zÁ-úñÑ])([A-Za-zÁ-úñÑ])/g,function(m,x,y){return x+y.toUpperCase()})},
  CONCATENAR:function(a){return flat(a).map(function(x){return txt(x.v)}).join("")},
  Y:function(a){var f=flat(a);if(!f.length)throw fE(FERR.v);return f.every(function(x){if(fIsE(x.v))throw x.v;return !!(x.v===true||typeof x.v=="number"&&x.v!=0)})},
  O:function(a){var f=flat(a);if(!f.length)throw fE(FERR.v);return f.some(function(x){if(fIsE(x.v))throw x.v;return !!(x.v===true||typeof x.v=="number"&&x.v!=0)})},
  NO:function(a){var v=a[0];if(fIsE(v))throw v;return !(v===true||typeof v=="number"&&v!=0)},
  BUSCARV:function(a){var v=a[0],t=a[1],c=num(a[2]),ex=a[3]===false||a[3]===0;if(!fIsA(t))throw fE(FERR.v);if(c<1||c>t.a[0].length)throw fE(FERR.r);var best=-1;for(var r=0;r<t.a.length;r++){var x=t.a[r][0];if(ex){if(cmp(x,v,"="))return t.a[r][c-1]}else{if(x===""||fIsE(x))continue;var le=typeof x==typeof v?cmp(x,v,"<="):false;if(le)best=r;else break}}if(best>-1)return t.a[best][c-1];throw fE(FERR.na)},
  COINCIDIR:function(a){var v=a[0],r=flat([a[1]]);for(var i=0;i<r.length;i++)if(cmp(r[i].v,v,"="))return i+1;throw fE(FERR.na)},
  INDICE:function(a){var t=a[0];if(!fIsA(t))return t;var r=num(a[1]),c=a[2]===undefined?1:num(a[2]);if(t.a.length==1&&a[2]===undefined){c=r;r=1}if(r<1||c<1||r>t.a.length||c>t.a[0].length)throw fE(FERR.r);return t.a[r-1][c-1]}};
 FN["MODA.UNO"]=FN.MODA;FN["CONCAT"]=FN.CONCATENAR;
 function call(name,start){var nm=fNoAcc(name).toUpperCase().replace(/Ñ/g,"N");
  if(nm=="SI"||nm=="SI.ERROR"){var args=parseArgs(true);if(nm=="SI"){var c=args[0]();if(fIsE(c))throw c;if(fIsA(c))c=c.a[0][0];var t=(c===true||(typeof c=="number"&&c!=0));if(typeof c=="string")throw fE(FERR.v);if(t)return args.length>1?args[1]():true;return args.length>2?args[2]():false}var v;try{v=args[0]();if(fIsE(v))throw v}catch(e){if(fIsE(e))return args[1]();throw e}return v}
  if(!FN[nm])throw fE(FERR.n);var vals=parseArgs(false);return FN[nm](vals)}
 function parseArgs(lazy){var out=[];if(eat(")"))return out;do{if(peek()&&(peek().v==","||peek().v==")")){out.push(lazy?function(){return ""}:"");continue}var st=p;if(lazy){skipExpr();(function(a,b){out.push(function(){var save=p;p=a;try{return expr()}finally{p=save}})})(st,p)}else out.push(expr())}while(eat(",")||eat(";"));if(!eat(")"))throw fE(FERR.n);return out}
 function skipExpr(){var d=0;while(p<T.length){var t=T[p];if(t.t=="op"){if(t.v=="(")d++;else if(t.v==")"){if(d==0)return;d--}else if((t.v==","||t.v==";")&&d==0)return}p++}}
 function prim(){var t=T[p];if(!t)throw fE(FERR.n);
  if(t.t=="num"){p++;return +t.v}
  if(t.t=="str"){p++;return t.v.slice(1,-1).replace(/""/g,'"')}
  if(t.t=="ref"){p++;return refVal(t)}
  if(t.t=="op"&&t.v=="("){p++;var v=expr();if(!eat(")"))throw fE(FERR.n);return v}
  if(t.t=="op"&&t.v=="{"){p++;var rows=[[]];while(true){var x=expr();rows[rows.length-1].push(x);if(eat(","))continue;if(eat(";")){rows.push([]);continue}break}if(!eat("}"))throw fE(FERR.n);return {a:rows}}
  if(t.t=="id"){p++;var u=fNoAcc(t.v).toUpperCase();if(u=="VERDADERO"||u=="TRUE")return true;if(u=="FALSO"||u=="FALSE")return false;if(T[p]&&T[p].t=="op"&&T[p].v=="("){p++;return call(t.v)}return nameVal(t.v)}
  throw fE(FERR.n)}
 function post(){var v=prim();while(eat("%")){var q=v;v=map2(q,0,function(x){return num(x)/100})}return v}
 function unary(){if(eat("-")){var v=unary();return map2(v,0,function(x){return -num(x)})}if(eat("+"))return unary();return post()}
 function pw(){var v=unary();while(eat("^")){var r=unary();v=map2(v,r,function(x,y){return Math.pow(num(x),num(y))})}return v}
 function mul(){var v=pw();while(true){if(eat("*")){var r=pw();v=map2(v,r,function(x,y){return num(x)*num(y)})}else if(eat("/")){var r2=pw();v=map2(v,r2,function(x,y){var d=num(y);if(d==0)throw fE(FERR.d0);return num(x)/d})}else return v}}
 function add(){var v=mul();while(true){if(eat("+")){var r=mul();v=map2(v,r,function(x,y){return num(x)+num(y)})}else if(eat("-")){var r2=mul();v=map2(v,r2,function(x,y){return num(x)-num(y)})}else return v}}
 function cat(){var v=add();while(eat("&")){var r=add();v=map2(v,r,function(x,y){return txt(x)+txt(y)})}return v}
 function expr(){var v=cat();while(peek()&&peek().t=="op"&&/^(=|<>|<=|>=|<|>)$/.test(peek().v)){var op=T[p++].v,r=cat();v=map2(v,r,function(x,y){return cmp(x,y,op)})}return v}
 var res=expr();if(p<T.length)throw fE(FERR.n);return res}
function fCell(S,id,si,k,cache,stack){var key=si+"!"+k;if(key in cache)return cache[key];var raw=S.sheets[si].cells[k];if(raw===undefined||raw==="")return cache[key]="";
 if(String(raw).charAt(0)!="="){return cache[key]=fRaw(raw)}
 if(stack[key])throw fE(FERR.c);stack[key]=1;var v;try{v=fEval(S,id,si,String(raw).slice(1),cache,stack);if(fIsA(v))v=v.a[0][0]}catch(e){if(fIsE(e))v=e;else throw e}delete stack[key];return cache[key]=v}
function fShow(S,si,k,v){if(fIsE(v))return v.e;var nf=S.sheets[si].nf[k]||"";if(typeof v=="boolean")return v?"VERDADERO":"FALSO";if(typeof v=="number"){if(nf=="mon")return "$"+v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});if(nf=="num")return v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});if(nf=="por")return Math.round(v*10000)/100+"%";if(nf=="fec"){var d=fDate(v);return ("0"+d.d).slice(-2)+"/"+("0"+d.m).slice(-2)+"/"+d.y}var r=Math.round(v*1e9)/1e9;return String(r)}return String(v)}
function fShift(f,dc,dr){return String(f).split(/("[^"]*")/).map(function(part,i){if(i%2)return part;return part.replace(/(^|[^A-Za-z0-9_.$])(\$?)([A-J])(\$?)(\d{1,2})(?![A-Za-z0-9_(.])/g,function(m,pre,ac,col,ar,row){var c=FCOLS.indexOf(col),r=+row;if(!ac)c+=dc;if(!ar)r+=dr;if(c<0||c>9||r<1)return pre+"#REF!";return pre+ac+FCOLS[c]+ar+r})}).join("")}
function fApi(S,id){var cache={};function si(n){if(n===undefined)return 0;for(var i=0;i<S.sheets.length;i++)if(S.sheets[i].n.toLowerCase()==String(n).toLowerCase())return i;return -1}
 function val(k,n){var i=si(n);if(i<0)return {e:FERR.r};try{return fCell(S,id,i,k,cache,{})}catch(e){return e}}
 return {v:function(k,n){var x=val(k,n);return fIsE(x)?x.e:x},d:function(k,n){var i=si(n);return i<0?"":fShow(S,i,k,val(k,n))},isf:function(k,n){var i=si(n);return i>=0&&String(S.sheets[i].cells[k]||"").charAt(0)=="="},
  f:function(k,n){var i=si(n);return i<0?"":String(S.sheets[i].cells[k]||"").toLowerCase().replace(/\s/g,"")},raw:function(k,n){var i=si(n);return i<0?"":String(S.sheets[i].cells[k]||"")},
  eq:function(k,x,n){var v=val(k,n);return typeof v=="number"&&Math.abs(v-x)<0.005},nf:function(k,n){var i=si(n);return i<0?"":(S.sheets[i].nf[k]||"")},
  nm:function(n){var k=Object.keys(S.names).filter(function(x){return x.toLowerCase()==String(n).toLowerCase()})[0];return k?S.names[k].replace(/\$/g,"").toUpperCase():""},
  nms:S.names,sheets:S.sheets.map(function(s){return s.n}),used:S.used,sel:S.sel}}
function fTasks(id){var S=fGet(id),a=fApi(S,id);return FC[id].tasks.map(function(t){var ok=false;try{ok=!!t[1](a)}catch(e){}return {text:t[0],ok:ok}})}
function fGrid(S,id){var cfg=FC[id].sheets[S.cur],sh=S.sheets[S.cur],g=fRange(S.sel),cache={},h='<table class="fg" style="width:'+(34+cfg.cols*0+function(){var t=0;for(var c=0;c<cfg.cols;c++)t+=sh.cw[FCOLS[c]]||cfg.dw||84;return t}())+'px"><colgroup><col style="width:34px">';
 for(var c=0;c<cfg.cols;c++)h+='<col style="width:'+(sh.cw[FCOLS[c]]||cfg.dw||84)+'px">';h+='</colgroup><tr class="fhr"><th></th>';
 for(c=0;c<cfg.cols;c++)h+='<th class="'+(c>=g.c1&&c<=g.c2?"on":"")+'">'+FCOLS[c]+'</th>';h+='</tr>';
 for(var r=1;r<=cfg.rows;r++){h+='<tr><th class="'+(r>=g.r1&&r<=g.r2?"on":"")+'">'+r+'</th>';
  for(c=0;c<cfg.cols;c++){var k=FCOLS[c]+r,raw=sh.cells[k],v,txt;try{v=fCell(S,id,S.cur,k,cache,{})}catch(e){v=fIsE(e)?e:fE(FERR.v)}
   txt=S.show&&raw&&String(raw).charAt(0)=="="?raw:fShow(S,S.cur,k,v);var al=typeof v=="number"||typeof v=="boolean"?"r":fIsE(v)?"c":"l";
   var hd=cfg.hdrows&&cfg.hdrows.indexOf(r)>-1;
   h+='<td data-r="'+k+'" class="'+(c>=g.c1&&c<=g.c2&&r>=g.r1&&r<=g.r2?"s ":"")+(k==FCOLS[g.c1]+g.r1?"a ":"")+(fIsE(v)?"er ":"")+(hd?"hd ":"")+(raw&&String(raw).charAt(0)=="="?"fo":"")+'" style="text-align:'+({l:"left",r:"right",c:"center"})[al]+'">'+String(txt).replace(/&/g,"&amp;").replace(/</g,"&lt;")+'</td>'}
  h+='</tr>'}return h+'</table>'}
function pFx(ic,t,inf,cfg){K++;FC[cfg.id]=cfg;return '<article class="lesson"><header><span class="kick">'+ic+' Simulador</span><h1>'+t+'</h1><p class="sub">'+inf+'</p></header><style>'
 +'.fxsim .fts{list-style:none;padding:0;margin:0 0 12px;display:grid;gap:6px}.fxsim .fts li{border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14.5px}.fxsim .fts li.y{border-color:var(--ok);background:var(--ok-soft)}'
 +'.fxsim code{font:600 13px Consolas,monospace;background:var(--pri-soft);padding:1px 5px;border-radius:5px}'
 +'.fbook{border:1.5px solid #c8ccd2;border-radius:12px;overflow:hidden;background:#fff;color:#1f2937}.fhead{display:flex;gap:6px;align-items:center;flex-wrap:wrap;background:#217346;padding:6px 8px;color:#e7f3ec;font:600 12.5px system-ui}.fhead select,.fhead button{width:auto;margin:0;font:13px system-ui;border:1px solid #cbd5e1;background:#fff;color:#111827;border-radius:6px;padding:4px 8px;min-height:30px;cursor:pointer}.fhead input{width:110px;margin:0;font:13px system-ui;border:1px solid #cbd5e1;background:#fff;color:#111827;border-radius:6px;padding:4px 8px;min-height:30px}'
 +'.fbar{display:flex;gap:6px;align-items:center;padding:6px 8px;border-bottom:1px solid #d1d5db;background:#fff}.fnb{width:84px;margin:0;font:600 13px Consolas,monospace;border:1px solid #cbd5e1;border-radius:6px;padding:5px 6px;color:#111827;background:#fff}.ffxl{font:italic 700 14px serif;color:#217346}.ffx{flex:1;min-width:0;margin:0;font:14px Consolas,monospace;color:#111827;border:1.5px solid #cbd5e1;border-radius:6px;padding:5px 8px;background:#fff}.ffx:focus{border-color:#059669;outline:0;box-shadow:0 0 0 3px rgba(5,150,105,.18)}.fok{width:auto;margin:0;border:1px solid #059669;background:#ecfdf5;color:#065f46;border-radius:6px;padding:4px 10px;font:700 13px system-ui;cursor:pointer;min-height:30px}'
 +'.fwrap{overflow:auto;max-height:340px;background:#fff}.fg{border-collapse:collapse;table-layout:fixed;color:#111827;user-select:none}.fg th{background:#f3f4f6;color:#4b5563;font:12px system-ui;border:1px solid #d1d5db;padding:2px 4px;text-align:center;position:sticky;top:0}.fg th.on{background:#d1fae5;color:#065f46;font-weight:700}.fg tr th:first-child{position:sticky;left:0}'
 +'.fg td{border:1px solid #e5e7eb;padding:3px 6px;height:24px;white-space:nowrap;overflow:hidden;text-overflow:clip;cursor:cell;font:13.5px Calibri,Carlito,Arial,sans-serif}.fg td.hd{font-weight:700;background:#dbeafe;text-align:center!important}.fg td.s{box-shadow:inset 0 0 0 999px rgba(16,185,129,.16)}.fg td.a{outline:2px solid #059669;outline-offset:-2px}.fg td.er{color:#b91c1c;font-weight:700}.fg td.fo{color:#14532d}'
 +'.fsh{display:flex;gap:6px;align-items:center;flex-wrap:wrap;padding:6px 8px;background:#f3f4f6;border-top:1px solid #d1d5db}.fsh button{font:600 13px system-ui;background:#fff;border:1px solid #cbd5e1;border-radius:0 0 6px 6px;padding:5px 14px;color:#14532d;cursor:pointer;width:auto;margin:0}.fsh button.on{background:#d1fae5;border-bottom:3px solid #059669}'
 +'.ftools{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.fmsg{min-height:22px;margin:6px 0 0;font-size:13.5px;color:var(--mut)}'
 +'</style><div class="fxsim" data-id="'+cfg.id+'">'+(cfg.intro?'<p>'+cfg.intro+'</p>':'')+'<h3 style="margin:8px 0">Retos</h3><ol class="fts"></ol>'
 +'<div class="fbook"><div class="fhead"><span>Excel</span><select class="fnf" aria-label="Formato de número"><option value="">General</option><option value="num">Número</option><option value="mon">Moneda</option><option value="por">Porcentaje</option><option value="fec">Fecha corta</option></select><button type="button" class="fdn" title="Copia la fórmula de la primera celda hacia las de abajo">⬇ Rellenar abajo</button><button type="button" class="frt" title="Copia la fórmula de la primera celda hacia la derecha">➡ Rellenar derecha</button><button type="button" class="fsw">Ver fórmulas</button>'+(cfg.names!==false?'<input class="fnn" placeholder="Nombre" aria-label="Nombre para el rango" maxlength="20"><button type="button" class="fdf" title="Ponle nombre al rango seleccionado">Definir nombre</button>':'')+'</div>'
 +'<div class="fbar"><input class="fnb" aria-label="Cuadro de nombres" title="Cuadro de nombres: escribe una celda, un rango o un nombre y pulsa Enter"><span class="ffxl">fx</span><input class="ffx" aria-label="Barra de fórmulas" autocomplete="off" spellcheck="false" placeholder="Selecciona una celda y escribe aquí; termina con Enter"><button type="button" class="fok" aria-label="Aceptar">✓</button></div><div class="fwrap"></div><div class="fsh"></div></div>'
 +'<p class="fmsg" role="status"></p><div class="ftools"><button type="button" class="btn ghost sm fext">➕ Seleccionar rango (en celular)</button><button type="button" class="btn ghost sm frst">↺ Reiniciar</button></div></div>'
 +(cfg.hint?'<p class="take"><b>Pista:</b> '+cfg.hint+'</p>':'')+'<div class="chk"><button class="btn c">Revisar retos</button></div><div class="res" role="status"></div></article>'}
function fxPaint(d,keepInput){var b=d.querySelector(".fxsim"),id=b.dataset.id,S=fGet(id),g=fRange(S.sel),k0=FCOLS[g.c1]+g.r1,sh=S.sheets[S.cur];
 var nb=b.querySelector(".fnb");if(document.activeElement!==nb)nb.value=S.sel;
 var fx=b.querySelector(".ffx");if(!keepInput)fx.value=sh.cells[k0]===undefined?"":String(sh.cells[k0]);
 b.querySelector(".fnf").value=sh.nf[k0]||"";
 b.querySelector(".fwrap").innerHTML=fGrid(S,id);
 b.querySelector(".fsw").className="fsw";b.querySelector(".fsw").textContent=S.show?"Ver resultados":"Ver fórmulas";
 b.querySelector(".fsh").innerHTML=S.sheets.map(function(s,i){return '<button type="button" data-i="'+i+'" class="'+(i==S.cur?"on":"")+'">'+s.n.replace(/</g,"&lt;")+'</button>'}).join("");
 b.querySelector(".fext").className="btn ghost sm fext"+(S.ext?" on":"");
 var ts=fTasks(id);b.querySelector(".fts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("");return ts}
function fMsg(d,t){d.querySelector(".fmsg").textContent=t||""}
function fSet(d,k,raw){var b=d.querySelector(".fxsim"),id=b.dataset.id,S=fGet(id),sh=S.sheets[S.cur],g=FC[id].sheets[S.cur];var x=fParse(k);if(!x||x.c>=g.cols||x.r>g.rows)return;raw=String(raw).trim();if(raw==="")delete sh.cells[k];else sh.cells[k]=raw;S.used[raw.charAt(0)=="="?"f":"v"]=1;
 if(/\$[A-J]|[A-J]\$/i.test(raw))S.used.abs=1;fSave(id)}
function fxInit(d){var b=d.querySelector(".fxsim"),id=b.dataset.id,S=fGet(id),drag=false,fx=b.querySelector(".ffx"),cfg=FC[id];S.ext=false;
 function selTo(k,ext){if(ext){var a=fParse(S.anc),z=fParse(k);S.sel=fRstr({c1:Math.min(a.c,z.c),c2:Math.max(a.c,z.c),r1:Math.min(a.r,z.r),r2:Math.max(a.r,z.r)})}else{S.anc=k;S.sel=k}fSave(id)}
 function commit(){var g=fRange(S.sel),k=FCOLS[g.c1]+g.r1;fSet(d,k,fx.value);var nr=Math.min(cfg.sheets[S.cur].rows,g.r1+1);S.sel=FCOLS[g.c1]+nr;S.anc=S.sel;fSave(id);fMsg(d,"");fxPaint(d)}
 fx.onkeydown=function(e){if(e.key=="Enter"){e.preventDefault();commit()}else if(e.key=="Escape"){fxPaint(d)}};
 b.querySelector(".fok").onclick=commit;
 var w=b.querySelector(".fwrap");
 w.onpointerdown=function(e){var td=e.target.closest("td[data-r]");if(!td)return;var v=fx.value;
  if(document.activeElement===fx&&v.charAt(0)=="="&&/[=+\-*\/^(,;&<>:]$/.test(v)){e.preventDefault();var ins=td.dataset.r;fx.value=v+ins;fx.focus();S.used.pt=1;return}
  var ext=e.shiftKey||S.ext;selTo(td.dataset.r,ext);S.ext=false;drag=e.pointerType=="mouse"&&!ext;fxPaint(d)};
 w.onpointermove=function(e){if(!drag)return;var el=document.elementFromPoint(e.clientX,e.clientY),td=el&&el.closest&&el.closest("td[data-r]");if(td&&w.contains(td)){var a=fParse(S.anc),z=fParse(td.dataset.r),s=fRstr({c1:Math.min(a.c,z.c),c2:Math.max(a.c,z.c),r1:Math.min(a.r,z.r),r2:Math.max(a.r,z.r)});if(s!=S.sel){S.sel=s;fxPaint(d)}}};
 w.ondblclick=function(){fx.focus()};
 document.addEventListener("pointerup",function(){if(drag){drag=false;fSave(id)}});
 var nb=b.querySelector(".fnb");nb.onkeydown=function(e){if(e.key!="Enter")return;e.preventDefault();var t=nb.value.trim(),g=fRange(t),shc=cfg.sheets[S.cur];
  if(!g){var nk=Object.keys(S.names).filter(function(x){return x.toLowerCase()==t.toLowerCase()})[0];if(nk){var q=S.names[nk],ix=q.indexOf("!");if(ix>-1)q=q.slice(ix+1);g=fRange(q);S.used.nbn=1}}
  if(!g||g.c2>=shc.cols||g.r2>shc.rows||g.r1<1){nb.style.borderColor="#dc2626";nb.value=S.sel;return}nb.style.borderColor="";S.sel=fRstr(g);S.anc=FCOLS[g.c1]+g.r1;S.used.nb=1;fSave(id);nb.blur();fxPaint(d)};
 b.querySelector(".fnf").onchange=function(e){var g=fRange(S.sel),sh=S.sheets[S.cur];for(var r=g.r1;r<=g.r2;r++)for(var c=g.c1;c<=g.c2;c++){var k=FCOLS[c]+r;if(e.target.value)sh.nf[k]=e.target.value;else delete sh.nf[k]}S.used.nf=1;fSave(id);fxPaint(d,true)};
 function fill(dir){var g=fRange(S.sel),sh=S.sheets[S.cur];if(dir=="d"&&g.r1==g.r2||dir=="r"&&g.c1==g.c2){fMsg(d,"Selecciona primero el rango: la primera celda tiene la fórmula y las demás se llenan.");return}
  for(var r=g.r1;r<=g.r2;r++)for(var c=g.c1;c<=g.c2;c++){if(dir=="d"&&r==g.r1||dir=="r"&&c==g.c1)continue;var sk=dir=="d"?FCOLS[c]+g.r1:FCOLS[g.c1]+r,src=sh.cells[sk];if(src===undefined){delete sh.cells[FCOLS[c]+r];continue}sh.cells[FCOLS[c]+r]=String(src).charAt(0)=="="?fShift(src,c-FCOLS.indexOf(sk[0]),r-(+sk.slice(1))):src;if(sh.nf[sk])sh.nf[FCOLS[c]+r]=sh.nf[sk]}
  S.used.fill=1;fSave(id);fMsg(d,"Fórmula copiada. Haz clic en una celda de abajo y mira en la barra de fórmulas cómo cambiaron las referencias.");fxPaint(d)}
 b.querySelector(".fdn").onclick=function(){fill("d")};b.querySelector(".frt").onclick=function(){fill("r")};
 b.querySelector(".fsw").onclick=function(){S.show=!S.show;S.used.show=1;fSave(id);fxPaint(d,true)};
 var df=b.querySelector(".fdf");if(df)df.onclick=function(){var n=b.querySelector(".fnn").value.trim();if(!/^[A-Za-zÁ-úñÑ_][A-Za-z0-9Á-úñÑ_.]*$/.test(n)||fRange(n)||/^[A-J]\d+$/i.test(n)){fMsg(d,"El nombre debe empezar con letra, sin espacios ni parecerse a una celda (como A1).");return}
  var sh=S.sheets[S.cur],q=S.sel.indexOf(":")>-1?S.sel:S.sel+":"+S.sel;S.names[n]=(sh.n.indexOf(" ")>-1?"'"+sh.n+"'":sh.n)+"!"+q;S.used.def=1;fSave(id);fMsg(d,"Nombre «"+n+"» definido para "+S.sel+". Úsalo en una fórmula, por ejemplo =SUMA("+n+").");b.querySelector(".fnn").value="";fxPaint(d,true)};
 b.querySelector(".fsh").onclick=function(e){var t=e.target.closest("button[data-i]");if(!t)return;S.cur=+t.dataset.i;S.sel="A1";S.anc="A1";S.used.sheet=1;fSave(id);fxPaint(d)};
 b.querySelector(".fext").onclick=function(){S.ext=!S.ext;fSave(id);fxPaint(d,true)};
 b.querySelector(".frst").onclick=function(){if(!confirm("¿Reiniciar el simulador? Se borra lo que escribiste."))return;FS[id]=fNew(id);fSave(id);fxInit(d)};
 fxPaint(d)}
function fxCheck(d){var ts=fxPaint(d,true),ok=ts.filter(function(x){return x.ok}).length,n=ts.length,f=ts.filter(function(x){return !x.ok})[0];return {ok:ok,total:n,msg:ok==n?"¡Todos los retos resueltos! Haz lo mismo en Excel con tu propio libro: es tu práctica.":ok+" de "+n+" retos. Sigue con: «"+f.text.replace(/<[^>]*>/g,"")+"»"}}
