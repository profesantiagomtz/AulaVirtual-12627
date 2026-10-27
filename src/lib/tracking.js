import { useEffect, useRef } from 'react'
import { isSupabaseReady, supabase } from './supabase'

// Seguimiento del alumno: cada minuto que la pestaña está abierta avisa a la plataforma qué está viendo.
// Con eso el docente ve quién está en línea, cuánto tiempo trabaja y quién se conectó el día de clase.
const HEARTBEAT_MS = 60000
let current = { view: '', detail: '' }
let notify = null
let disabled = false

async function beat(entry = false) {
  if (disabled || !isSupabaseReady || document.visibilityState === 'hidden') return
  const { error } = await supabase.rpc('aula_heartbeat', { p_view: current.view, p_detail: current.detail || null, p_entry: entry })
  // Si aún no se corre supabase/seguimiento_asistencia.sql, se deja de intentar sin molestar al alumno.
  if (error && /aula_heartbeat|function|schema cache/i.test(error.message || '')) disabled = true
}

export function useStudentTracking(session, viewLabel) {
  const active = Boolean(session && session.role === 'student' && !session.preview && viewLabel)
  // El detalle lo limpia el componente que lo puso al cerrarse; aquí solo cambia la sección.
  const first = useRef(true)
  useEffect(() => {
    current = { ...current, view: viewLabel || '' }
    if (first.current) { first.current = false; return }
    if (active) notify?.()
  }, [active, viewLabel])
  useEffect(() => {
    if (!active) return undefined
    notify = () => beat()
    const timer = window.setInterval(() => beat(), HEARTBEAT_MS)
    const onVisible = () => { if (document.visibilityState === 'visible') beat() }
    document.addEventListener('visibilitychange', onVisible)
    beat(true)
    return () => { window.clearInterval(timer); document.removeEventListener('visibilitychange', onVisible); notify = null }
  }, [active, session?.id])
}

// Lo que el alumno tiene abierto dentro de una sección (un material o una tarea).
export function useActivityDetail(detail) {
  useEffect(() => {
    if (!detail) return undefined
    current = { ...current, detail }
    notify?.()
    return () => { if (current.detail === detail) current = { ...current, detail: '' } }
  }, [detail])
}
