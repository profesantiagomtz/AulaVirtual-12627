// Calcula la escala de impresión de los apuntes de cada material (R.A. 2.1 en adelante) para no gastar
// una hoja casi vacía: si al reducir la letra hasta 86 % cabe en una hoja menos, guarda esa escala.
// Uso: node scripts/courseware/fit_notes.cjs && python3 scripts/courseware/embed_patch.py
const { chromium } = require('playwright')
const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '../..')
const OUT = path.join(__dirname, 'print_fit.json')
const pages = pdf => (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length

;(async () => {
  const browser = await chromium.launch()
  const fit = {}
  const files = fs.readdirSync(path.join(ROOT, 'public/courses')).filter(f => /-ra[2-9]\d-material\.html$/.test(f)).sort()
  for (const file of files) {
    const ctx = await browser.newContext()
    const page = await ctx.newPage()
    await page.goto('file://' + path.join(ROOT, 'public/courses', file))
    await page.click('#tabs button[data-t="a"]')
    const [notes] = await Promise.all([ctx.waitForEvent('page'), page.click('.crumb .apx')])
    await notes.waitForLoadState()
    await notes.emulateMedia({ media: 'print' })
    const count = async z => {
      await notes.evaluate(v => document.documentElement.style.setProperty('--z', v), z)
      return pages(await notes.pdf({ format: 'Letter', preferCSSPageSize: true }))
    }
    const base = await count(1)
    let best = 1
    for (let z = 0.98; base > 1 && z >= 0.86; z = Math.round((z - 0.02) * 100) / 100) {
      // Un 2 % de holgura para celulares y navegadores con otras fuentes.
      if (await count(z) < base) { best = Math.round((z - 0.02) * 100) / 100; break }
    }
    const key = file.replace('-material.html', '')
    if (best < 1) fit[key] = best
    console.log(`${key}: ${base} hojas${best < 1 ? ` → ${base - 1} con escala ${best}` : ''}`)
    await ctx.close()
  }
  await browser.close()
  fs.writeFileSync(OUT, JSON.stringify(fit, null, 2) + '\n')
})()
