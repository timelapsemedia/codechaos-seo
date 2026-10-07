// Syntaxprüfung für Lua/ReaScript mit luaparse (MIT, vendor/). Meldet zusätzlich unbekannte Globale (Tippfehler-Verdacht).
const fs = require('fs')
const path = require('path')
const luaparse = require(path.join(__dirname, 'vendor', 'luaparse.js'))
const STD = new Set(['_G', '_VERSION', 'assert', 'collectgarbage', 'dofile', 'error', 'getmetatable', 'ipairs', 'load', 'loadfile', 'next', 'pairs', 'pcall', 'print', 'rawequal', 'rawget', 'rawlen', 'rawset', 'require', 'select', 'setmetatable', 'tonumber', 'tostring', 'type', 'xpcall', 'coroutine', 'debug', 'io', 'math', 'os', 'package', 'string', 'table', 'utf8', 'unpack', 'reaper', 'gfx', 'arg'])
const file = process.argv[2]
const src = fs.readFileSync(file, 'utf8')
const out = { datei: file, zeilen: src.split('\n').length }
try {
  const globals = new Map()
  const ast = luaparse.parse(src, { luaVersion: '5.3', scope: true, locations: true, comments: false, onCreateNode: n => {
    if (n.type === 'Identifier' && n.isLocal === false && !STD.has(n.name)) globals.set(n.name, (globals.get(n.name) || []).concat(n.loc ? n.loc.start.line : 0))
  } })
  const reaperCalls = new Map()
  const walk = n => {
    if (!n || typeof n !== 'object') return
    if (n.type === 'MemberExpression' && n.base && n.base.name === 'reaper' && n.identifier) reaperCalls.set(n.identifier.name, (reaperCalls.get(n.identifier.name) || 0) + 1)
    for (const k of Object.keys(n)) { const v = n[k]; if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v === 'object' && k !== 'loc') walk(v) }
  }
  walk(ast)
  // Globale, die nur gelesen und nie zugewiesen werden, sind Tippfehler-Verdacht.
  const assigned = new Set()
  const walkA = n => {
    if (!n || typeof n !== 'object') return
    if ((n.type === 'AssignmentStatement') ) n.variables.forEach(v => v.type === 'Identifier' && assigned.add(v.name))
    if (n.type === 'FunctionDeclaration' && n.identifier && n.identifier.type === 'Identifier' && !n.isLocal) assigned.add(n.identifier.name)
    for (const k of Object.keys(n)) { const v = n[k]; if (Array.isArray(v)) v.forEach(walkA); else if (v && typeof v === 'object' && k !== 'loc') walkA(v) }
  }
  walkA(ast)
  out.syntax = 'ok'
  out.reaper_funktionen = Object.fromEntries([...reaperCalls.entries()].sort((a, b) => b[1] - a[1]))
  out.unbekannte_globale = [...globals.entries()].filter(([g]) => !assigned.has(g)).map(([g, lines]) => ({ name: g, zeilen: [...new Set(lines)].slice(0, 5) }))
} catch (e) {
  out.syntax = 'FEHLER'
  out.fehler = String(e.message || e)
}
console.log(JSON.stringify(out))
