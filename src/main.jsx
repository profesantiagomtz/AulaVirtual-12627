import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import App from './App'
import { supabase } from './lib/supabase'
import './styles.css'

// El enlace de "olvidé mi contraseña" llega con los datos de acceso en el hash (#access_token=…&type=recovery).
// Se procesan antes de montar el router, que usa el hash para navegar.
const authHash = window.location.hash
const recovering = /type=recovery/.test(authHash)
if (recovering) sessionStorage.setItem('aula-recovery', '1')
if (/error_code=/.test(authHash)) sessionStorage.setItem('aula-auth-notice', 'El enlace para restablecer la contraseña ya venció o no es válido. Pide uno nuevo.')
const ready = recovering && supabase ? supabase.auth.getSession() : Promise.resolve()

ready.finally(() => {
  if (/access_token=|error_code=/.test(window.location.hash)) window.history.replaceState(null, '', `${window.location.pathname}#/acceso`)
  ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
      <HashRouter>
        <App />
      </HashRouter>
    </React.StrictMode>,
  )
})
