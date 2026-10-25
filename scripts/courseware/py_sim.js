// Laboratorio de Python (subconjunto sin condiciones ni ciclos, que se ven en el R.A. 3.2): todo corre en este navegador.
var PC={},PS={};
var PYKW="False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" ");
var PYCTL="if elif else for while def class try except finally with import from return break continue pass lambda global nonlocal assert del raise async await yield".split(" ");
function PyErr(kind,msg,line,hint){this.kind=kind;this.msg=msg;this.line=line;this.hint=hint||""}
function pyI(n){return {t:"int",v:BigInt(n)}}function pyF(n){return {t:"float",v:n}}function pyS(s){return {t:"str",v:s}}function pyB(b){return {t:"bool",v:!!b}}
var PYNONE={t:"none",v:null};
function pyTN(x){return x.t=="none"?"NoneType":x.t=="func"?"builtin_function_or_method":x.t}
function pyEs(s){var q=s.indexOf("'")>-1&&s.indexOf('"')<0?'"':"'";return q+s.replace(/\\/g,"\\\\").replace(/\n/g,"\\n").replace(/\t/g,"\\t").replace(new RegExp(q,"g"),"\\"+q)+q}
function pyFl(n){if(n===Infinity)return "inf";if(n===-Infinity)return "-inf";if(isNaN(n))return "nan";var a=Math.abs(n);if(a!=0&&(a>=1e16||a<1e-4)){var e=n.toExponential().replace(/e([+-])(\d)$/,"e$10$2");return e}if(Number.isInteger(n))return n.toFixed(1);return String(n)}
function pyRepr(x){if(x.t=="str")return pyEs(x.v);if(x.t=="list")return "["+x.v.map(pyRepr).join(", ")+"]";if(x.t=="tuple")return "("+x.v.map(pyRepr).join(", ")+(x.v.length==1?",":"")+")";return pyStr(x)}
function pyStr(x){switch(x.t){case "int":return x.v.toString();case "float":return pyFl(x.v);case "str":return x.v;case "bool":return x.v?"True":"False";case "none":return "None";case "meth":return "<built-in method "+x.n+">";case "type":return "<class '"+x.v+"'>";case "func":return "<built-in function "+x.v+">"}return pyRepr(x)}
function pyNum(x){return x.t=="float"?x.v:Number(x.v)}
function pyIsN(x){return x.t=="int"||x.t=="float"||x.t=="bool"}
function pyTruth(x){switch(x.t){case "int":return x.v!==0n;case "float":return x.v!==0;case "str":case "list":case "tuple":return x.v.length>0;case "bool":return x.v;case "none":return false}return true}
function pyEq(a,b){if(pyIsN(a)&&pyIsN(b)){if(a.t=="float"||b.t=="float")return pyNum(a)==pyNum(b);return BigInt(a.t=="bool"?+a.v:a.v)==BigInt(b.t=="bool"?+b.v:b.v)}if(a.t!=b.t)return false;if(a.t=="str")return a.v==b.v;if(a.t=="none")return true;if(a.t=="list"||a.t=="tuple")return a.v.length==b.v.length&&a.v.every(function(x,i){return pyEq(x,b.v[i])});return a===b}
function pyLex(src){var T=[],i=0,ln=1,depth=0,stack=[],atStart=true,n=src.length;
 function err(k,m,l,h){throw new PyErr(k,m,l||ln,h)}
 while(i<n){var ch=src[i],f=false;
  if(atStart&&depth==0){var j=i,sp=0;while(src[j]==" "||src[j]=="\t"){sp++;j++}if(src[j]=="\n"||src[j]=="#"||j>=n){while(j<n&&src[j]!="\n")j++;i=j+1;ln++;continue}if(sp>0)err("IndentationError","unexpected indent",ln,"En Python los espacios al inicio de una línea tienen significado. Aquí no hace falta: empieza todas las instrucciones en la primera columna.");atStart=false;i=j;continue}
  if(ch=="\n"){if(depth==0)T.push({t:"NL",ln:ln});ln++;i++;atStart=depth==0;continue}
  if(ch==" "||ch=="\t"||ch=="\r"){i++;continue}
  if(ch=="#"){while(i<n&&src[i]!="\n")i++;continue}
  var m=/^(?:\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)/.exec(src.slice(i,i+40));
  if(m&&(ch!="."||/\d/.test(src[i+1]||""))){var nx=src[i+m[0].length]||"";if(/[A-Za-z_\u00C0-\u024F]/.test(nx))err("SyntaxError","invalid decimal literal",ln,"Un número no puede llevar letras pegadas. Si es un nombre de variable, no puede empezar con un número.");T.push({t:"NUM",v:m[0],ln:ln});i+=m[0].length;continue}
  var id=/^[A-Za-z_\u00C0-\u024F][A-Za-z0-9_\u00C0-\u024F]*/.exec(src.slice(i,i+80));
  if(id){var q=src[i+id[0].length];if(/^[fF]$/.test(id[0])&&(q=='"'||q=="'")){i+=1;f=true;ch=q;id=null;m=null;}else{T.push({t:"NAME",v:id[0],ln:ln});i+=id[0].length;continue}}
  if(ch=='"'||ch=="'"){var st=ln,s="",k=i+1,raw=[],ok=false,tri=src.substr(i,3)==ch+ch+ch;if(tri)err("SyntaxError","las cadenas de varias líneas no se usan en este laboratorio",ln);
   while(k<n){var c=src[k];if(c=="\n")break;if(c=="\\"){var e=src[k+1];s+=e=="n"?"\n":e=="t"?"\t":e=="\\"?"\\":e=='"'?'"':e=="'"?"'":"\\"+e;k+=2;continue}if(c==ch){ok=true;break}s+=c;k++}
   if(!ok)err("SyntaxError","unterminated string literal (detected at line "+ln+")",st,"Falta cerrar las comillas. Cada texto debe empezar y terminar con el mismo tipo de comillas.");
   T.push({t:"STR",v:s,f:!!f,ln:ln,q:ch});i=k+1;continue}
  var op=/^(\*\*=|\/\/=|\*\*|\/\/|==|!=|<=|>=|\+=|-=|\*=|\/=|%=|[-+*\/%<>=()\[\],.:])/.exec(src.slice(i,i+3));
  if(op){var o=op[0];if(o=="("||o=="[")stack.push({c:o,ln:ln}),depth++;if(o==")"||o=="]"){var top=stack.pop();if(!top||(o==")"&&top.c!="(")||(o=="]"&&top.c!="["))err("SyntaxError","unmatched '"+o+"'",ln,"Sobra o no corresponde este paréntesis o corchete. Cuenta los que abres y los que cierras.");depth--}T.push({t:"OP",v:o,ln:ln});i+=o.length;continue}
  err("SyntaxError",ch=="$"||ch=="?"||ch=="!"||ch=="@"||ch=="&"||ch=="|"||ch=="~"||ch=="^"||ch==";"||ch=="{"||ch=="}"?"invalid syntax":"invalid character '"+ch+"'",ln,"Ese símbolo no se puede usar así en Python. Revisa que no sea un carácter copiado de otro programa (como comillas curvas).")}
 if(stack.length){var o2=stack[stack.length-1];throw new PyErr("SyntaxError","'"+o2.c+"' was never closed",o2.ln,"Abriste un paréntesis o corchete y no lo cerraste.")}
 T.push({t:"NL",ln:ln});T.push({t:"END",ln:ln});return T}
function pyParse(T){var p=0;
 function pk(){return T[p]}function nx(){return T[p++]}
 function isOp(v){return T[p].t=="OP"&&T[p].v==v}function eat(v){if(isOp(v)){p++;return true}return false}
 function bad(msg,ln,hint){throw new PyErr("SyntaxError",msg||"invalid syntax",ln||T[p].ln,hint||"")}
 function tuple(){var a=[expr()];var tup=false;while(isOp(",")){p++;tup=true;if(endTok())break;a.push(expr())}return tup?{k:"tuple",a:a,ln:a[0].ln}:a[0]}
 function endTok(){var t=T[p];return t.t=="NL"||t.t=="END"||(t.t=="OP"&&(t.v=="="||t.v==")"||t.v=="]"||/=$/.test(t.v)&&t.v!="==" &&t.v!="!="&&t.v!="<="&&t.v!=">="))}
 function expr(){return orx()}
 function orx(){var l=andx();while(T[p].t=="NAME"&&T[p].v=="or"){var ln=nx().ln;l={k:"or",a:l,b:andx(),ln:ln}}return l}
 function andx(){var l=notx();while(T[p].t=="NAME"&&T[p].v=="and"){var ln=nx().ln;l={k:"and",a:l,b:notx(),ln:ln}}return l}
 function notx(){if(T[p].t=="NAME"&&T[p].v=="not"){var ln=nx().ln;return {k:"not",a:notx(),ln:ln}}return cmp()}
 function cmp(){var l=add();while(true){var t=T[p],op=null;if(t.t=="OP"&&/^(==|!=|<=|>=|<|>)$/.test(t.v)){op=t.v;p++}else if(t.t=="NAME"&&t.v=="in"){op="in";p++}else if(t.t=="NAME"&&t.v=="not"&&T[p+1].t=="NAME"&&T[p+1].v=="in"){op="not in";p+=2}else return l;l={k:"cmp",op:op,a:l,b:add(),ln:t.ln}}}
 function add(){var l=mul();while(T[p].t=="OP"&&(T[p].v=="+"||T[p].v=="-")){var t=nx();l={k:"bin",op:t.v,a:l,b:mul(),ln:t.ln}}return l}
 function mul(){var l=un();while(T[p].t=="OP"&&/^(\*|\/|\/\/|%)$/.test(T[p].v)){var t=nx();l={k:"bin",op:t.v,a:l,b:un(),ln:t.ln}}return l}
 function un(){if(T[p].t=="OP"&&(T[p].v=="-"||T[p].v=="+")){var t=nx();return {k:"un",op:t.v,a:un(),ln:t.ln}}return pw()}
 function pw(){var b=post();if(isOp("**")){var t=nx();return {k:"bin",op:"**",a:b,b:un(),ln:t.ln}}return b}
 function post(){var a=atom();while(true){var t=T[p];if(isOp("(")){p++;var args=[],kw={};if(!isOp(")")){do{if(isOp(")"))break;if(T[p].t=="NAME"&&T[p+1].t=="OP"&&T[p+1].v=="="){var nm=nx().v;p++;kw[nm]=expr()}else args.push(expr())}while(eat(","))}if(!eat(")"))bad("'(' was never closed",t.ln,"Falta cerrar el paréntesis de la llamada.");a={k:"call",f:a,args:args,kw:kw,ln:t.ln}}
  else if(isOp("[")){p++;var i1=null,i2=null,sl=false;if(!isOp(":"))i1=expr();if(eat(":")){sl=true;if(!isOp("]"))i2=expr()}if(!eat("]"))bad("invalid syntax",t.ln);a={k:sl?"slice":"idx",a:a,i:i1,j:i2,ln:t.ln}}
  else if(isOp(".")){p++;var nm2=nx();if(nm2.t!="NAME")bad("invalid syntax",t.ln);a={k:"attr",a:a,n:nm2.v,ln:t.ln}}else return a}}
 function atom(){var t=nx();
  if(t.t=="NUM")return {k:"num",v:/^\d+$/.test(t.v)?pyI(t.v):pyF(parseFloat(t.v)),ln:t.ln};
  if(t.t=="STR"){var parts=[t];while(T[p].t=="STR"&&!!T[p].f==!!t.f)parts.push(nx());if(t.f)return {k:"fstr",parts:parts.map(function(x){return pyFs(x.v,x.ln)}),ln:t.ln};return {k:"str",v:parts.map(function(x){return x.v}).join(""),ln:t.ln}}
  if(t.t=="NAME"){if(t.v=="True")return {k:"const",v:pyB(true),ln:t.ln};if(t.v=="False")return {k:"const",v:pyB(false),ln:t.ln};if(t.v=="None")return {k:"const",v:PYNONE,ln:t.ln};if(PYKW.indexOf(t.v)>-1)bad("invalid syntax",t.ln,"«"+t.v+"» es una palabra reservada de Python: no se puede usar como nombre.");return {k:"name",n:t.v,ln:t.ln}}
  if(t.t=="OP"&&t.v=="("){if(eat(")"))return {k:"tuple",a:[],ln:t.ln};var e=tuple();if(!eat(")"))bad("'(' was never closed",t.ln,"Falta cerrar el paréntesis.");return e}
  if(t.t=="OP"&&t.v=="["){var el=[];if(!isOp("]")){do{if(isOp("]"))break;el.push(expr())}while(eat(","))}if(!eat("]"))bad("'[' was never closed",t.ln,"Falta cerrar el corchete.");return {k:"list",a:el,ln:t.ln}}
  p--;bad("invalid syntax",t.ln,"Python no entiende esta línea. Revisa comillas, paréntesis, operadores y que cada instrucción esté completa.")}
 function pyFs(s,ln){var out=[],i=0;while(i<s.length){if(s[i]=="{"){if(s[i+1]=="{"){out.push(pyS("{"));i+=2;continue}var d=1,j=i+1;while(j<s.length&&d>0){if(s[j]=="{")d++;else if(s[j]=="}")d--;j++}if(d)throw new PyErr("SyntaxError","f-string: expecting '}'",ln,"Falta cerrar la llave } de la f-string.");var inner=s.slice(i+1,j-1),spec="",c=inner.search(/:(?![^\[(]*[\])])/);if(c>-1){spec=inner.slice(c+1);inner=inner.slice(0,c)}var sub=pyParse(pyLex(inner.trim()+"\n"));out.push({e:sub.body[0].e,spec:spec});i=j}else if(s[i]=="}"){out.push(pyS("}"));i+=s[i+1]=="}"?2:1}else{var k=i;while(k<s.length&&s[k]!="{"&&s[k]!="}")k++;out.push(pyS(s.slice(i,k)));i=k}}return out}
 var body=[];
 while(T[p].t!="END"){if(T[p].t=="NL"){p++;continue}var t0=T[p],st;
  if(t0.t=="NAME"&&PYKW.indexOf(t0.v)>-1&&T[p+1].t=="OP"&&T[p+1].v=="=")bad("invalid syntax",t0.ln,"«"+t0.v+"» es una palabra reservada de Python: no se puede usar como nombre de variable. Elige otro nombre.");
  if(t0.t=="NAME"&&PYCTL.indexOf(t0.v)>-1)throw new PyErr("Aviso","«"+t0.v+"» todavía no se usa en este laboratorio",t0.ln,"Las condiciones (if), los ciclos (for, while), las funciones (def) y los módulos (import) se estudian en el R.A. 3.2. Aquí practicas con instrucciones que se ejecutan una tras otra.");
  if(t0.t=="NAME"&&t0.v=="print"&&T[p+1].t!="OP"&&T[p+1].t!="NL")bad("Missing parentheses in call to 'print'. Did you mean print(...)?",t0.ln,"En Python 3 print es una función: lleva paréntesis, por ejemplo print(\"Hola\").");
  var first=tuple();
  if(T[p].t=="OP"&&(T[p].v=="="||/^(\+|-|\*\*|\*|\/\/|\/|%)=$/.test(T[p].v))){var targets=[first],aug=null;
   if(T[p].v!="="){aug=T[p].v.slice(0,-1);p++;st={k:"aug",op:aug,t:first,e:tuple(),ln:t0.ln}}else{var val;while(eat("=")){val=tuple();if(isOp("=")){targets.push(val)}}
    targets.forEach(function(tg){var items=tg.k=="tuple"?tg.a:[tg];items.forEach(function(x){if(x.k!="name"&&x.k!="idx")bad("cannot assign to "+(x.k=="num"||x.k=="str"||x.k=="const"?"literal":x.k=="call"?"function call":"expression")+" here. Maybe you meant '==' instead of '='?",x.ln,"A la izquierda del = debe ir el nombre de una variable (por ejemplo edad = 15). Si querías comparar, se usa ==.")})});
    st={k:"assign",t:targets,e:val,ln:t0.ln}}}
  else st={k:"expr",e:first,ln:t0.ln};
  if(T[p].t!="NL"&&T[p].t!="END")bad("invalid syntax",T[p].ln,"Después de una instrucción debe terminar la línea. ¿Falta una coma, un operador o unas comillas?");
  body.push(st)}
 return {body:body}}
function pyFmt(x,spec,ln){if(!spec)return pyStr(x);var m=/^([<>^])?(\d+)?(,)?(?:\.(\d+))?([fdsx%])?$/.exec(spec);if(!m)throw new PyErr("ValueError","Invalid format specifier '"+spec+"'",ln,"Ese formato no se reconoce. Ejemplos: :.2f (dos decimales), :, (separador de miles), :>10 (alinear).");
 var al=m[1],w=+m[2]||0,co=m[3],pr=m[4]===undefined?null:+m[4],ty=m[5],s;
 if(ty=="f"||ty=="%"||(pr!==null&&!ty&&pyIsN(x))){if(!pyIsN(x))throw new PyErr("ValueError","Unknown format code 'f' for object of type '"+pyTN(x)+"'",ln,"El formato de decimales solo funciona con números.");var v=pyNum(x)*(ty=="%"?100:1);s=v.toFixed(pr===null?6:pr);if(co)s=s.replace(/\B(?=(\d{3})+(?!\d)(?!.*\.))/g,",").replace(/^(-?\d+)/,function(a){return a.replace(/\B(?=(\d{3})+$)/g,",")});if(ty=="%")s+="%"}
 else if(ty=="d"||co&&x.t=="int"){if(x.t!="int")throw new PyErr("ValueError","Unknown format code 'd' for object of type '"+pyTN(x)+"'",ln,"El formato d solo funciona con enteros.");s=x.v.toString();if(co)s=s.replace(/\B(?=(\d{3})+$)/g,",")}
 else s=pyStr(x);
 if(s.length<w){var pad=w-s.length;al=al||(pyIsN(x)?">":"<");s=al==">"?" ".repeat(pad)+s:al=="<"?s+" ".repeat(pad):" ".repeat(pad>>1)+s+" ".repeat(pad-(pad>>1))}return s}
function pyRun(src,inputs){var out=[],env={},ip=0,lines=src.split("\n"),res={out:"",err:null,vars:{},src:src,ran:true},calls=0;
 var tb=function(e){e.src=(lines[e.line-1]||"").trim();return e};
 try{for(var li=0;li<lines.length;li++){var cm=/^(if|elif|else|for|while|def|class|try|except|finally|with|import|from|lambda|global|nonlocal|assert|del|raise|async|await|yield|return|break|continue|pass)\b(?!\s*=[^=])/.exec(lines[li]);if(cm)throw new PyErr("Aviso","«"+cm[1]+"» todavía no se usa en este laboratorio",li+1,"Las condiciones (if), los ciclos (for, while), las funciones (def) y los módulos (import) se estudian en el R.A. 3.2. Aquí practicas con instrucciones que se ejecutan una tras otra.")}
  var prog=pyParse(pyLex(src.replace(/\r/g,"")+"\n"))}catch(e){if(e instanceof PyErr){res.err=tb(e);return res}throw e}
 function E(kind,msg,ln,hint){return new PyErr(kind,msg,ln,hint)}
 var BI={print:1,input:1,int:1,float:1,str:1,bool:1,len:1,type:1,round:1,abs:1,max:1,min:1,sum:1};
 function lookup(n,ln){if(Object.prototype.hasOwnProperty.call(env,n))return env[n];if(Object.prototype.hasOwnProperty.call(BI,n))return {t:"func",v:n};throw E("NameError","name '"+n+"' is not defined",ln,"La variable «"+n+"» no existe todavía. Revisa que esté bien escrita (Python distingue mayúsculas y minúsculas) y que la hayas creado en una línea anterior. Si es un texto, va entre comillas.")}
 function arith(op,a,b,ln){var A=a.t=="bool"?pyI(+a.v):a,B=b.t=="bool"?pyI(+b.v):b;
  if(op=="+"){if(A.t=="str"&&B.t=="str")return pyS(A.v+B.v);if(A.t=="list"&&B.t=="list")return {t:"list",v:A.v.concat(B.v)};if(A.t=="str")throw E("TypeError",'can only concatenate str (not "'+pyTN(b)+'") to str',ln,"No se puede sumar texto con "+(b.t=="int"||b.t=="float"?"un número":"otro tipo")+". Convierte con str() o usa una f-string: f\"... {variable}\".")}
  if(op=="*"&&((A.t=="str"||A.t=="list")&&B.t=="int"||A.t=="int"&&(B.t=="str"||B.t=="list"))){var s=A.t=="int"?B:A,k=Number(A.t=="int"?A.v:B.v);if(k<0)k=0;if(s.v.length*k>5000)throw E("MemoryError","el resultado sería demasiado grande para este laboratorio",ln,"Usa un número más pequeño.");return s.t=="str"?pyS(s.v.repeat(k)):{t:"list",v:[].concat.apply([],Array(k).fill(s.v))}}
  if(!((A.t=="int"||A.t=="float")&&(B.t=="int"||B.t=="float"))){var ex=op=="*"&&(A.t=="str"||B.t=="str")?"can't multiply sequence by non-int of type '"+(A.t=="str"?pyTN(b):pyTN(a))+"'":"unsupported operand type(s) for "+op+": '"+pyTN(a)+"' and '"+pyTN(b)+"'";throw E("TypeError",ex,ln,"Esa operación no tiene sentido entre "+pyTN(a)+" y "+pyTN(b)+". Revisa los tipos de datos: usa type() para verlos y int(), float() o str() para convertir.")}
  var fl=A.t=="float"||B.t=="float";
  if(op=="/"){var d=pyNum(B);if(d==0)throw E("ZeroDivisionError","division by zero",ln,"No se puede dividir entre cero. Revisa el valor del divisor.");return pyF(pyNum(A)/d)}
  if(op=="//"||op=="%"){if(pyNum(B)==0)throw E("ZeroDivisionError",fl?"float modulo":"integer division or modulo by zero",ln,"No se puede dividir entre cero. Revisa el valor del divisor.");
   if(!fl){var x=A.v,y=B.v,q=x/y;if((x%y!==0n)&&((x<0n)!==(y<0n)))q-=1n;return op=="//"?{t:"int",v:q}:{t:"int",v:x-q*y}}var xf=pyNum(A),yf=pyNum(B);return op=="//"?pyF(Math.floor(xf/yf)):pyF(xf-Math.floor(xf/yf)*yf)}
  if(op=="**"){if(!fl&&B.v>=0n){if(B.v>4000n)throw E("OverflowError","el exponente es demasiado grande para este laboratorio",ln,"Usa un exponente más pequeño.");return {t:"int",v:A.v**B.v}}return pyF(Math.pow(pyNum(A),pyNum(B)))}
  if(fl){var u=pyNum(A),w=pyNum(B);return pyF(op=="+"?u+w:op=="-"?u-w:u*w)}
  return {t:"int",v:op=="+"?A.v+B.v:op=="-"?A.v-B.v:A.v*B.v}}
 function compare(op,a,b,ln){if(op=="==")return pyB(pyEq(a,b));if(op=="!=")return pyB(!pyEq(a,b));
  if(op=="in"||op=="not in"){var r;if(b.t=="str"){if(a.t!="str")throw E("TypeError","'in <string>' requires string as left operand, not "+pyTN(a),ln,"Con «in» sobre un texto, lo que buscas también debe ser texto.");r=b.v.indexOf(a.v)>-1}else if(b.t=="list"||b.t=="tuple")r=b.v.some(function(x){return pyEq(x,a)});else throw E("TypeError","argument of type '"+pyTN(b)+"' is not iterable",ln,"«in» busca dentro de un texto o una lista.");return pyB(op=="in"?r:!r)}
  var l,rr;if(pyIsN(a)&&pyIsN(b)){l=pyNum(a);rr=pyNum(b);if(a.t=="int"&&b.t=="int"){l=a.v;rr=b.v}}else if(a.t=="str"&&b.t=="str"){l=a.v;rr=b.v}else throw E("TypeError","'"+op+"' not supported between instances of '"+pyTN(a)+"' and '"+pyTN(b)+"'",ln,"No se pueden comparar con "+op+" un "+pyTN(a)+" y un "+pyTN(b)+". Convierte uno de los dos (por ejemplo int(...)).");
  return pyB(op=="<"?l<rr:op==">"?l>rr:op=="<="?l<=rr:l>=rr)}
 function toInt(x,ln){if(x.t=="int")return x;if(x.t=="bool")return pyI(+x.v);if(x.t=="float"){if(!isFinite(x.v))throw E("OverflowError","cannot convert float infinity to integer",ln);return {t:"int",v:BigInt(Math.trunc(x.v))}}
  if(x.t=="str"){var s=x.v.trim().replace(/_/g,"");if(!/^[+-]?\d+$/.test(s))throw E("ValueError","invalid literal for int() with base 10: "+pyEs(x.v),ln,"No se puede convertir ese texto a entero: tiene letras, puntos o está vacío. Si es un decimal, usa float().");return {t:"int",v:BigInt(s)}}
  throw E("TypeError","int() argument must be a string or a real number, not '"+pyTN(x)+"'",ln)}
 function call(f,args,kw,ln,self){var n=f.v;
  if(f.t!="func"&&f.t!="meth")throw E("TypeError","'"+pyTN(f)+"' object is not callable",ln,"Los paréntesis ( ) llaman a una función; aquí la variable no es una función. ¿Querías multiplicar? Usa *.");
  if(f.t=="meth")return method(f.self,f.n,args,ln);
  function need(a,b){if(args.length<a||args.length>b)throw E("TypeError",n+"() takes "+(a==b?"exactly "+a:"from "+a+" to "+b)+" argument"+(b==1?"":"s")+" ("+args.length+" given)",ln,"Revisa cuántos datos le das a "+n+"().")}
  if(n=="print"){var sep=kw.sep?pyStr(kw.sep):" ",end=kw.end?pyStr(kw.end):"\n";out.push(args.map(pyStr).join(sep)+end);return PYNONE}
  if(n=="input"){need(0,1);var pr=args.length?pyStr(args[0]):"";if(ip>=inputs.length)throw E("EOFError","EOF when reading a line",ln,"input() espera que el usuario escriba. En este laboratorio escribe los datos en el cuadro «Entradas del teclado», uno por línea, en el orden en que se pedirán.");var v=inputs[ip++];out.push(pr+v+"\n");return pyS(v)}
  if(n=="int"){if(!args.length)return pyI(0);need(0,1);return toInt(args[0],ln)}
  if(n=="float"){if(!args.length)return pyF(0);need(0,1);var a=args[0];if(a.t=="str"){var s=a.v.trim();if(!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s))throw E("ValueError","could not convert string to float: "+pyEs(a.v),ln,"Ese texto no es un número decimal. Usa punto decimal (3.5), sin comas ni letras.");return pyF(parseFloat(s))}if(!pyIsN(a))throw E("TypeError","float() argument must be a string or a real number, not '"+pyTN(a)+"'",ln);return pyF(pyNum(a))}
  if(n=="str"){need(0,1);return pyS(args.length?pyStr(args[0]):"")}
  if(n=="bool"){need(0,1);return pyB(args.length?pyTruth(args[0]):false)}
  if(n=="len"){need(1,1);var x=args[0];if(x.t!="str"&&x.t!="list"&&x.t!="tuple")throw E("TypeError","object of type '"+pyTN(x)+"' has no len()",ln,"len() cuenta los caracteres de un texto o los elementos de una lista; un "+pyTN(x)+" no tiene longitud. Si es un número, conviértelo con str() primero.");return pyI(x.v.length)}
  if(n=="type"){need(1,1);return {t:"type",v:pyTN(args[0])}}
  if(n=="abs"){need(1,1);var y=args[0];if(y.t=="int")return {t:"int",v:y.v<0n?-y.v:y.v};if(y.t=="float")return pyF(Math.abs(y.v));throw E("TypeError","bad operand type for abs(): '"+pyTN(y)+"'",ln)}
  if(n=="round"){need(1,2);var z=args[0];if(!pyIsN(z))throw E("TypeError","type "+pyTN(z)+" doesn't define __round__ method",ln);var nd=args[1]?Number(args[1].v):null;if(nd===null){var r=pyNum(z),fl=Math.floor(r),df=r-fl,rv=df<.5?fl:df>.5?fl+1:(fl%2==0?fl:fl+1);return {t:"int",v:BigInt(rv)}}if(z.t=="int")return z;return pyF(parseFloat(pyNum(z).toFixed(Math.max(0,nd))))}
  if(n=="max"||n=="min"||n=="sum"){var it=args.length==1&&(args[0].t=="list"||args[0].t=="tuple")?args[0].v:args;if(!it.length)throw E("ValueError",n+"() arg is an empty sequence",ln);if(n=="sum"){var acc=pyI(0);it.forEach(function(q){acc=arith("+",acc,q,ln)});return acc}var best=it[0];it.slice(1).forEach(function(q){if(compare(n=="max"?">":"<",q,best,ln).v)best=q});return best}
  throw E("NameError","name '"+n+"' is not defined",ln)}
 function method(o,m,args,ln){function need(a){if(args.length!=a)throw E("TypeError",m+"() takes exactly "+a+" argument"+(a==1?"":"s")+" ("+args.length+" given)",ln)}function str1(){if(!args[0]||args[0].t!="str")throw E("TypeError",m+"() argument must be str, not "+(args[0]?pyTN(args[0]):"missing"),ln)}
  if(o.t=="str"){var s=o.v;switch(m){case "upper":return pyS(s.toUpperCase());case "lower":return pyS(s.toLowerCase());case "title":return pyS(s.toLowerCase().replace(/(^|[^A-Za-z\u00C0-\u024F])([A-Za-z\u00C0-\u024F])/g,function(a,b,c){return b+c.toUpperCase()}));case "capitalize":return pyS(s.charAt(0).toUpperCase()+s.slice(1).toLowerCase());case "strip":return pyS(s.trim());
   case "replace":need(2);str1();return pyS(s.split(args[0].v).join(args[1].v));case "startswith":need(1);str1();return pyB(s.indexOf(args[0].v)==0);case "endswith":need(1);str1();return pyB(s.length>=args[0].v.length&&s.slice(s.length-args[0].v.length)==args[0].v);
   case "count":need(1);str1();return pyI(args[0].v?s.split(args[0].v).length-1:s.length+1);case "find":need(1);str1();return pyI(s.indexOf(args[0].v));case "isdigit":return pyB(/^\d+$/.test(s));case "isalpha":return pyB(/^[A-Za-z\u00C0-\u024F]+$/.test(s));case "isupper":return pyB(/[A-Z\u00C0-\u00DE]/.test(s)&&s==s.toUpperCase());case "islower":return pyB(/[a-z\u00DF-\u00FF]/.test(s)&&s==s.toLowerCase());
   case "split":return {t:"list",v:(args.length?s.split(args[0].v):s.trim().split(/\s+/).filter(Boolean)).map(pyS)};case "join":need(1);if(args[0].t!="list")throw E("TypeError","can only join an iterable",ln);return pyS(args[0].v.map(function(x){if(x.t!="str")throw E("TypeError","sequence item: expected str instance, "+pyTN(x)+" found",ln);return x.v}).join(s))}}
  if(o.t=="list"){switch(m){case "append":need(1);o.v.push(args[0]);return PYNONE;case "pop":if(!o.v.length)throw E("IndexError","pop from empty list",ln);return o.v.pop();case "count":need(1);return pyI(o.v.filter(function(x){return pyEq(x,args[0])}).length);case "sort":o.v.sort(function(a,b){return compare("<",a,b,ln).v?-1:compare(">",a,b,ln).v?1:0});return PYNONE}}
  throw E("AttributeError","'"+pyTN(o)+"' object has no attribute '"+m+"'",ln,"Ese tipo de dato no tiene el método «"+m+"». Revisa cómo se escribe (todo en minúsculas) y que el dato sea del tipo correcto.")}
 function ev(n){switch(n.k){
  case "num":case "const":return n.v;case "str":return pyS(n.v);case "name":return lookup(n.n,n.ln);
  case "fstr":return pyS(n.parts.map(function(pt){return pt.map(function(q){return q.e?pyFmt(ev(q.e),q.spec,n.ln):q.v}).join("")}).join(""));
  case "list":return {t:"list",v:n.a.map(ev)};case "tuple":return {t:"tuple",v:n.a.map(ev)};
  case "un":{var a=ev(n.a);if(!pyIsN(a))throw E("TypeError","bad operand type for unary "+n.op+": '"+pyTN(a)+"'",n.ln,"El signo "+n.op+" solo se aplica a números.");if(n.op=="+")return a.t=="bool"?pyI(+a.v):a;return a.t=="float"?pyF(-a.v):{t:"int",v:-(a.t=="bool"?BigInt(+a.v):a.v)}}
  case "bin":return arith(n.op,ev(n.a),ev(n.b),n.ln);case "cmp":return compare(n.op,ev(n.a),ev(n.b),n.ln);
  case "and":{var l=ev(n.a);return pyTruth(l)?ev(n.b):l}case "or":{var l2=ev(n.a);return pyTruth(l2)?l2:ev(n.b)}case "not":return pyB(!pyTruth(ev(n.a)));
  case "call":{if(++calls>2000)throw E("RuntimeError","demasiadas llamadas",n.ln);var f=ev(n.f),args=n.args.map(ev),kw={};Object.keys(n.kw).forEach(function(k){kw[k]=ev(n.kw[k])});return call(f,args,kw,n.ln)}
  case "attr":{var o=ev(n.a);return {t:"meth",n:n.n,self:o,v:n.n}}
  case "idx":{var s=ev(n.a),i=ev(n.i);if(s.t!="str"&&s.t!="list"&&s.t!="tuple")throw E("TypeError","'"+pyTN(s)+"' object is not subscriptable",n.ln,"Los corchetes [ ] solo funcionan con textos y listas.");if(i.t!="int")throw E("TypeError",(s.t=="str"?"string":s.t)+" indices must be integers or slices, not "+pyTN(i),n.ln,"El índice debe ser un número entero.");var k=Number(i.v),L=s.v.length;if(k<0)k+=L;if(k<0||k>=L)throw E("IndexError",(s.t=="str"?"string":s.t)+" index out of range",n.ln,"Ese índice no existe: el primer elemento es el 0 y el último es len()-1.");return s.t=="str"?pyS(s.v[k]):s.v[k]}
  case "slice":{var s2=ev(n.a);if(s2.t!="str"&&s2.t!="list")throw E("TypeError","'"+pyTN(s2)+"' object is not subscriptable",n.ln);var L2=s2.v.length,i1=n.i?Number(ev(n.i).v):0,j1=n.j?Number(ev(n.j).v):L2;if(i1<0)i1=Math.max(0,i1+L2);if(j1<0)j1+=L2;var sl=s2.v.slice(i1,Math.max(i1,j1));return s2.t=="str"?pyS(sl):{t:"list",v:sl}}}
  throw E("SyntaxError","invalid syntax",n.ln)}
 function assignTo(t,val,ln){if(t.k=="name"){env[t.n]=val;return}if(t.k=="idx"){var s=ev(t.a);if(s.t!="list")throw E("TypeError","'"+pyTN(s)+"' object does not support item assignment",ln,"Los textos no se pueden modificar letra por letra: crea un texto nuevo.");var k=Number(ev(t.i).v);if(k<0)k+=s.v.length;if(k<0||k>=s.v.length)throw E("IndexError","list assignment index out of range",ln);s.v[k]=val;return}
  if(t.k=="tuple"){var seq=val.t=="str"?val.v.split("").map(pyS):val.v;if(!seq||seq.length!=t.a.length)throw E("ValueError",seq&&seq.length>t.a.length?"too many values to unpack (expected "+t.a.length+")":"not enough values to unpack (expected "+t.a.length+", got "+(seq?seq.length:1)+")",ln,"Debe haber tantos valores a la derecha como variables a la izquierda.");t.a.forEach(function(x,i){assignTo(x,seq[i],ln)})}}
 try{prog.body.forEach(function(st){
   if(st.k=="expr"){ev(st.e);return}
   if(st.k=="assign"){var v=ev(st.e);st.t.forEach(function(t){assignTo(t,v,st.ln)});return}
   if(st.k=="aug"){var cur=ev(st.t),v2=ev(st.e);assignTo(st.t,arith(st.op,cur,v2,st.ln),st.ln)}})}
 catch(e){if(e instanceof PyErr)res.err=tb(e);else throw e}
 res.out=out.join("");if(res.out.length>6000)res.out=res.out.slice(0,6000)+"\n… (salida recortada)";
 Object.keys(env).forEach(function(k){var x=env[k];res.vars[k]={t:pyTN(x),r:pyRepr(x),v:x.t=="int"?Number(x.v):x.t=="list"||x.t=="tuple"?x.v.map(pyRepr):x.v}});
 return res}
function pyApi(R,id){var src=R.src||"",out=R.out||"";return {out:out,lines:out.split("\n").filter(function(x){return x!=""}),vars:R.vars||{},src:src,err:R.err,ok:!R.err&&R.ran,
 t:function(n){return R.vars&&R.vars[n]?R.vars[n].t:""},v:function(n){return R.vars&&R.vars[n]?R.vars[n].v:undefined},r:function(n){return R.vars&&R.vars[n]?R.vars[n].r:""},
 uses:function(re){return re.test(src.replace(/#.*$/gm,""))},printed:function(s){return out.indexOf(s)>-1},comments:(src.match(/^\s*#.+$/gm)||[]).length}}
function pyTasks(id,R){var a=pyApi(R,id);return PC[id].tasks.map(function(t){var ok=false;try{ok=!!t[1](a)}catch(e){}return {text:t[0],ok:ok}})}
function pyGet(id){if(!PS[id]){var s=null;try{s=JSON.parse(localStorage.getItem(KEY+"-py-"+id)||"null")}catch(e){}PS[id]=s&&typeof s.code=="string"?s:{code:PC[id].code,inputs:PC[id].inputs||""};PS[id].R=null}return PS[id]}
function pySave(id){try{localStorage.setItem(KEY+"-py-"+id,JSON.stringify({code:PS[id].code,inputs:PS[id].inputs}))}catch(e){}}
var PYTN_ES={int:"entero",float:"decimal",str:"texto",bool:"lógico",NoneType:"nada",list:"lista",tuple:"tupla"};
function pyPaint(d){var b=d.querySelector(".pysim"),id=b.dataset.id,S=pyGet(id),R=S.R,o=b.querySelector(".pyo"),h="";
 if(!R){o.innerHTML='<span class="pymut">Pulsa «▶ Ejecutar» para ver el resultado.</span>'}
 else{h=R.out?'<span class="pyok">'+R.out.replace(/&/g,"&amp;").replace(/</g,"&lt;")+'</span>':"";if(R.err){var e=R.err;h+=(h&&!/\n$/.test(R.out)?"\n":"")+'<span class="pyer">'+(e.kind=="Aviso"?"":"Traceback (most recent call last):\n  Línea "+e.line+": "+(e.src||"").replace(/&/g,"&amp;").replace(/</g,"&lt;")+"\n")+(e.kind=="Aviso"?"ℹ️ ":e.kind+": ")+e.msg.replace(/&/g,"&amp;").replace(/</g,"&lt;")+'</span>'+(e.hint?'\n<span class="pyhint">💡 '+e.hint.replace(/&/g,"&amp;").replace(/</g,"&lt;")+'</span>':"")}else if(!R.out)h='<span class="pymut">(El programa terminó y no mostró nada. Usa print() para mostrar resultados.)</span>';o.innerHTML=h}
 var vs=R&&R.vars?Object.keys(R.vars):[];b.querySelector(".pyv").innerHTML=vs.length?'<table class="pyt"><tr><th>Variable</th><th>Valor</th><th>Tipo</th></tr>'+vs.map(function(k){var x=R.vars[k];return '<tr><td><code>'+k+'</code></td><td><code>'+x.r.replace(/&/g,"&amp;").replace(/</g,"&lt;")+'</code></td><td>'+x.t+(PYTN_ES[x.t]?' <small>('+PYTN_ES[x.t]+')</small>':"")+'</td></tr>'}).join("")+'</table>':'<span class="pymut">Aquí verás las variables que existen en la memoria después de ejecutar.</span>';
 var ts=R?pyTasks(id,R):PC[id].tasks.map(function(t){return {text:t[0],ok:false}});b.querySelector(".pts").innerHTML=ts.map(function(x,i){return '<li class="'+(x.ok?"y":"")+'"><b>'+(x.ok?"✅":(i+1)+".")+'</b> '+x.text+'</li>'}).join("");return ts}
function pyExec(d){var b=d.querySelector(".pysim"),id=b.dataset.id,S=pyGet(id);S.code=b.querySelector(".pyc").value;S.inputs=b.querySelector(".pyi").value;pySave(id);var r;try{r=pyRun(S.code,S.inputs?S.inputs.split("\n"):[])}catch(e){r={out:"",err:new PyErr("Error",String(e&&e.message||e),0),vars:{},src:S.code,ran:true}}S.R=r;return pyPaint(d)}
function pPy(ic,t,inf,cfg){K++;PC[cfg.id]=cfg;return '<article class="lesson"><header><span class="kick">'+ic+' Simulador</span><h1>'+t+'</h1><p class="sub">'+inf+'</p></header><style>'
 +'.pysim .pts{list-style:none;padding:0;margin:0 0 12px;display:grid;gap:6px}.pysim .pts li{border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14.5px}.pysim .pts li.y{border-color:var(--ok);background:var(--ok-soft)}.pysim code{font:600 13px Consolas,monospace;background:var(--pri-soft);padding:1px 5px;border-radius:5px}'
 +'.pyb{border:1.5px solid #30363d;border-radius:12px;overflow:hidden;background:#0d1117;color:#e6edf3}.pybh{display:flex;gap:6px;align-items:center;flex-wrap:wrap;background:#161b22;padding:6px 8px;font:600 12.5px system-ui;color:#9da7b3}.pybh button{width:auto;margin:0;font:600 13px system-ui;border-radius:6px;padding:5px 12px;min-height:30px;cursor:pointer;border:1px solid #30363d;background:#21262d;color:#e6edf3}.pybh .pyrun{background:#238636;border-color:#2ea043;color:#fff}'
 +'.pysim textarea.pyc{display:block;width:100%;margin:0;border:0;border-radius:0;background:#0d1117;color:#e6edf3;font:14px/1.55 Consolas,Menlo,monospace;padding:10px 12px;min-height:170px;resize:vertical;tab-size:4;white-space:pre;overflow:auto}'
 +'.pyl{background:#161b22;padding:6px 10px;font:600 11.5px system-ui;color:#9da7b3;border-top:1px solid #30363d}.pysim textarea.pyi{display:block;width:100%;margin:0;border:0;border-radius:0;background:#0d1117;color:#a5d6ff;font:13px/1.5 Consolas,Menlo,monospace;padding:6px 12px;min-height:46px;resize:vertical}'
 +'.pyo{margin:0;padding:10px 12px;min-height:80px;max-height:260px;overflow:auto;background:#010409;color:#e6edf3;font:13.5px/1.5 Consolas,Menlo,monospace;white-space:pre-wrap;border-top:1px solid #30363d}.pyo .pyer{color:#ff7b72}.pyo .pyhint{color:#f2cc60}.pyo .pymut{color:#7d8590}'
 +'.pyv{background:var(--card);color:var(--ink);padding:8px 10px;border-radius:0 0 12px 12px;overflow:auto;max-height:220px;font-size:13.5px;border-top:1px solid #30363d}.pyt{border-collapse:collapse;width:100%}.pyt th,.pyt td{border:1px solid var(--line);padding:3px 8px;text-align:left}.pyt th{background:var(--pri-soft)}'
 +'</style><div class="pysim" data-id="'+cfg.id+'">'+(cfg.intro?'<p>'+cfg.intro+'</p>':'')+'<h3 style="margin:8px 0">Retos</h3><ol class="pts"></ol>'
 +'<div class="pyb"><div class="pybh"><span>🐍 programa.py</span><button type="button" class="pyrun">▶ Ejecutar</button><button type="button" class="pyrs">↺ Reiniciar</button></div><textarea class="pyc" spellcheck="false" autocapitalize="off" autocomplete="off" aria-label="Código en Python"></textarea>'
 +'<div class="pyl">⌨️ Entradas del teclado (una por línea, para input())</div><textarea class="pyi" spellcheck="false" aria-label="Entradas del teclado" placeholder="Escribe aquí lo que el usuario teclearía, una respuesta por línea"></textarea><div class="pyl">📤 Salida del programa</div><pre class="pyo" role="status" aria-live="polite"></pre><div class="pyl">🧠 Variables en memoria</div><div class="pyv"></div></div></div>'
 +(cfg.hint?'<p class="take"><b>Pista:</b> '+cfg.hint+'</p>':'')+'<div class="chk"><button class="btn c">Revisar retos</button></div><div class="res" role="status"></div></article>'}
function pyInit(d){var b=d.querySelector(".pysim"),id=b.dataset.id,S=pyGet(id),c=b.querySelector(".pyc"),i=b.querySelector(".pyi");c.value=S.code;i.value=S.inputs||"";
 b.querySelector(".pyrun").onclick=function(){pyExec(d)};c.onkeydown=function(e){if((e.ctrlKey||e.metaKey)&&e.key=="Enter"){e.preventDefault();pyExec(d)}if(e.key=="Tab"){e.preventDefault();var s=c.selectionStart;c.value=c.value.slice(0,s)+"    "+c.value.slice(c.selectionEnd);c.selectionStart=c.selectionEnd=s+4}};
 c.oninput=function(){S.code=c.value;pySave(id)};i.oninput=function(){S.inputs=i.value;pySave(id)};
 b.querySelector(".pyrs").onclick=function(){if(!confirm("¿Reiniciar el programa? Se borra lo que escribiste."))return;S.code=PC[id].code;S.inputs=PC[id].inputs||"";c.value=S.code;i.value=S.inputs;S.R=null;pySave(id);pyPaint(d)};
 if(S.code!==PC[id].code)pyExec(d);else pyPaint(d)}
function pyCheck(d){var ts=pyExec(d),ok=ts.filter(function(x){return x.ok}).length,n=ts.length,f=ts.filter(function(x){return !x.ok})[0];return {ok:ok,total:n,msg:ok==n?"¡Todos los retos resueltos! Ahora haz lo mismo en un archivo .py de tu computadora o celular: es tu práctica.":ok+" de "+n+" retos. Sigue con: «"+f.text.replace(/<[^>]*>/g,"")+"»"}}
