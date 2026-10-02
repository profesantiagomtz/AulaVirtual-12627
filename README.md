# Aula Virtual

Plataforma web para publicar material didáctico, aplicar evaluaciones y dar seguimiento por alumno y grupo. Está preparada para alojarse en GitHub Pages y usar Supabase para autenticación, base de datos y archivos.

## Probar la versión local

1. Instala las dependencias con `npm install`.
2. Inicia la plataforma con `npm run dev`.
3. Mientras no exista un archivo `.env`, funciona en modo demostración. Entra como docente o alumno con cualquier contraseña. Para alumnos, el correo debe terminar en `@tam.conalep.edu.mx`.

## Conectar Supabase

1. Crea un proyecto en Supabase.
2. Abre **SQL Editor**, pega el contenido de `supabase/schema.sql` y ejecútalo.
3. En **Authentication > URL Configuration**, agrega la dirección final de GitHub Pages a las URL permitidas.
4. Copia `.env.example` como `.env` y coloca la URL y la clave pública `anon` de tu proyecto.
5. En la tabla `groups`, registra los grupos reales. En `enrollment_rules`, agrega los prefijos de matrícula o patrones de correo que correspondan a cada grupo.
6. Registra la cuenta docente; después cambia su campo `role` en `profiles` de `student` a `teacher` desde el editor de tablas de Supabase.

La clave pública `anon` puede usarse en el navegador. Nunca agregues la clave `service_role` al sitio ni a GitHub Pages.

## Asignación automática de grupo

El correo institucional solo confirma que el alumno pertenece al dominio autorizado. Para obtener el grupo y semestre de forma confiable, el alta envía también la matrícula del alumno. La función `handle_new_user` compara la matrícula o correo con `enrollment_rules` y asigna el grupo; el semestre se obtiene de `groups`.

Ejemplo de regla por prefijo:

```sql
insert into public.enrollment_rules(enrollment_prefix, group_id, priority)
select '242401', id, 10 from public.groups where code='401';
```

## Publicar en GitHub Pages

1. Crea un repositorio de GitHub y sube estos archivos a la rama `main`.
2. En **Settings > Secrets and variables > Actions**, crea los secretos `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY`.
3. En **Settings > Pages > Source**, selecciona **GitHub Actions**.
4. Cada actualización de `main` se compilará y publicará automáticamente.

## Alcance de esta primera versión

La interfaz y el modelo de seguridad ya cubren perfiles, grupos, materiales, evaluaciones, preguntas, entregas, calificaciones y registro de consulta de recursos. El modo demostración permite revisar toda la experiencia visual. Al conectar Supabase, el inicio de sesión utiliza autenticación real; las operaciones de demostración deben sustituirse por las consultas indicadas por las tablas del esquema durante la siguiente integración.
