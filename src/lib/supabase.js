import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL
const key = import.meta.env.VITE_SUPABASE_ANON_KEY

export const isSupabaseReady = Boolean(url && key && !url.includes('TU-PROYECTO'))
export const supabase = isSupabaseReady ? createClient(url, key) : null

// Supabase entrega como máximo 1000 filas por consulta. Esta función pide
// página por página para que el panel docente nunca pierda registros.
export async function fetchAllRows(makeQuery, pageSize = 1000) {
  const rows = []
  for (let from = 0; ; from += pageSize) {
    const { data, error } = await makeQuery().range(from, from + pageSize - 1)
    if (error) return { data: null, error }
    rows.push(...(data || []))
    if (!data || data.length < pageSize) return { data: rows, error: null }
  }
}
