export const groups = [
  { id: '111', name: '111', semester: 1, career: 'Pensamiento Matemático I', students: 29 },
  { id: '310', name: '310', semester: 3, career: 'Informática', students: 30 },
  { id: '311', name: '311', semester: 3, career: 'Informática', students: 22 },
  { id: '511', name: '511', semester: 5, career: 'Informática', students: 14 },
]

export const materials = [
  { id: 1, title: 'Pensamiento aritmético', type: 'PDF', group: '111', unit: 'Unidad 1', date: '28 sep' },
  { id: 2, title: 'Riesgos de seguridad informática', type: 'Presentación', group: '310', unit: 'R.A. 1.1', date: '25 sep' },
  { id: 3, title: 'Configuración de comunicación en red', type: 'Video', group: '511', unit: 'R.A. 1.1', date: '22 sep' },
]

export const assessments = [
  { id: 1, title: 'Diagnóstico de pensamiento matemático', group: '111', due: '04 oct', submissions: 21, total: 29, average: 82, status: 'Activa' },
  { id: 2, title: 'R.A. 1.1 Seguridad informática', group: '310', due: '08 oct', submissions: 14, total: 30, average: 76, status: 'Activa' },
  { id: 3, title: 'R.A. 1.1 Documentos digitales', group: '311', due: '26 sep', submissions: 22, total: 22, average: 88, status: 'Cerrada' },
]

export const students = [
  { id: 1, name: 'Alumno de demostración 01', email: 'alumno01@institucional.edu.mx', group: '111', semester: 1, progress: 92, average: 91, pending: 0 },
  { id: 2, name: 'Alumno de demostración 02', email: 'alumno02@institucional.edu.mx', group: '310', semester: 3, progress: 76, average: 78, pending: 1 },
  { id: 3, name: 'Alumno de demostración 03', email: 'alumno03@institucional.edu.mx', group: '311', semester: 3, progress: 84, average: 86, pending: 0 },
  { id: 4, name: 'Alumno de demostración 04', email: 'alumno04@institucional.edu.mx', group: '511', semester: 5, progress: 58, average: 69, pending: 2 },
]
