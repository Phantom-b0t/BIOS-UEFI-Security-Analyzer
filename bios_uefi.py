import os
import sys

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QUrl, Qt, QStandardPaths
    from PyQt5.QtGui import QIcon
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install PyQt5 PyQtWebEngine")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — Enhanced styles preserving original design
# ══════════════════════════════════════════════════════════════════════════════
CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
  --bg-deep: #050810;
  --bg-base: #080d1a;
  --bg-panel: #0d1525;
  --bg-card: #111c2e;
  --bg-hover: #162035;
  --border: #1e3050;
  --border-bright: #2a4570;
  --blue: #3b82f6;
  --blue-dim: #1d4ed8;
  --blue-glow: rgba(59,130,246,0.15);
  --cyan: #22d3ee;
  --green: #22c55e;
  --green-dim: rgba(34,197,94,0.12);
  --amber: #f59e0b;
  --amber-dim: rgba(245,158,11,0.12);
  --red: #ef4444;
  --red-dim: rgba(239,68,68,0.12);
  --purple: #a855f7;
  --purple-dim: rgba(168,85,247,0.12);
  --text-primary: #e2e8f0;
  --text-secondary: #7090b0;
  --text-muted: #718296;
  --mono: 'JetBrains Mono', monospace;
  --display: 'Rajdhani', sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--mono);
  background: var(--bg-deep);
  color: var(--text-primary);
  min-height: 100vh;
  overflow-x: hidden;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

/* ── LAYOUT ── */
.app { position: relative; z-index: 1; display: flex; flex-direction: column; min-height: 100vh; }

/* ── HEADER ── */
header {
  background: linear-gradient(180deg, #060c1a 0%, var(--bg-base) 100%);
  border-bottom: 1px solid var(--border);
  padding: 0 2vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-left { display: flex; align-items: center; gap: 14px; }
.header-logo {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--blue) 0%, var(--cyan) 100%);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  box-shadow: 0 0 16px rgba(59,130,246,0.4);
}
.header-title { font-family: var(--display); font-size: 24px; font-weight: 700; letter-spacing: 1px; color: var(--text-primary); }
.header-title span { color: var(--blue); }
.header-sub { font-size: 11px; color: var(--text-secondary); letter-spacing: 0.5px; }
.header-right { display: flex; align-items: center; gap: 10px; }
.status-badge {
  display: flex; align-items: center; gap: 6px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 7px; padding: 8px 12px; font-size: 11px; color: var(--text-secondary);
}
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--text-muted); }
.status-dot.active { background: var(--green); box-shadow: 0 0 6px var(--green); animation: pulse 2s infinite; }
.status-dot.warn { background: var(--amber); box-shadow: 0 0 6px var(--amber); animation: pulse 2s infinite; }
.status-dot.err { background: var(--red); box-shadow: 0 0 6px var(--red); animation: pulse 1s infinite; }
@keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.5} }

/* ── SCENARIO BADGE ── */
.scenario-badge {
  display: flex; align-items: center; gap: 8px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 7px; padding: 7px 14px; font-size: 11px;
  transition: all 0.3s;
}
.scenario-badge.secure { border-color: rgba(34,197,94,0.5); color: var(--green); }
.scenario-badge.misconfigured { border-color: rgba(245,158,11,0.5); color: var(--amber); }
.scenario-badge.vulnerable { border-color: rgba(239,68,68,0.5); color: var(--red); }
.scenario-badge.attacked { border-color: rgba(168,85,247,0.5); color: var(--purple); animation: attackPulse 0.8s ease-in-out infinite; }
@keyframes attackPulse { 0%,100%{box-shadow:0 0 0 0 rgba(168,85,247,0)} 50%{box-shadow:0 0 12px 2px rgba(168,85,247,0.3)} }

/* ── NAV TABS ── */
.nav-tabs {
  background: var(--bg-base);
  border-bottom: 1px solid var(--border);
  padding: 0 24px;
  display: flex;
  gap: 0;
  overflow-x: auto;
}
.nav-tab {
  padding: 12px 18px;
  font-family: var(--mono);
  font-size: 11.5px;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  border: none;
  background: none;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all 0.2s;
  letter-spacing: 0.3px;
}
.nav-tab:hover { color: var(--text-secondary); }
.nav-tab.active { color: var(--blue); border-bottom-color: var(--blue); }

/* ── MAIN BODY ── */
.main { display: flex; flex: 1; gap: 0; }

/* ── SIDEBAR ── */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: var(--bg-base);
  border-right: 1px solid var(--border);
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.sidebar-section { padding: 0 16px 8px; font-size: 10px; font-weight: 600; color: var(--text-muted); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 8px; }
.phase-item {
  margin: 0 10px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: transform 0.28s ease, background 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
  border: 1px solid transparent;
  font-size: 12.5px;
  position: relative;
  overflow: hidden;
  background: rgba(255,255,255,0.02);
}
.phase-item::before {
  content: '';
  position: absolute;
  left: 0; top: 0;
  width: 3px; height: 100%;
  background: transparent;
  transform: scaleY(0);
  transform-origin: top;
  transition: background 0.3s ease, transform 0.3s ease;
}
.phase-item:hover { background: rgba(59,130,246,0.08); transform: translateX(2px); }
.phase-item.active {
  background: linear-gradient(180deg, rgba(14,56,124,0.2), rgba(10,30,58,0.85));
  border-color: rgba(59,130,246,0.35);
  box-shadow: 0 18px 40px rgba(18,56,110,0.18);
}
.phase-item.active::before {
  background: linear-gradient(180deg, rgba(59,130,246,1), rgba(34,197,94,0.9));
  transform: scaleY(1);
}
.phase-num {
  width: 26px; height: 26px;
  border-radius: 12px;
  background: rgba(255,255,255,0.04);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
}
.phase-item.active .phase-num { background: var(--blue); color: #fff; box-shadow: 0 0 0 6px rgba(59,130,246,0.08); }
.phase-item.done .phase-num { background: var(--green); color: #fff; }
.phase-item.warn .phase-num { background: var(--amber); color: #000; }
.phase-item.err .phase-num { background: var(--red); color: #fff; }
.phase-info { flex: 1; min-width: 0; margin-left:10px; }
.phase-name { color: var(--text-secondary); font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.phase-item.active .phase-name { color: var(--text-primary); }
.phase-status { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
.phase-status.ok { color: var(--green); }
.phase-status.warn { color: var(--amber); }
.phase-status.err { color: var(--red); }

.sidebar-score {
  margin: 16px 10px 0;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
}
.score-label { font-size: 10px; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }
.score-ring { position: relative; width: 80px; height: 80px; margin: 0 auto 10px; }
.score-ring svg { transform: rotate(-90deg); }
.score-ring-text { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.score-val { font-family: var(--display); font-size: 22px; font-weight: 700; color: var(--amber); line-height: 1; }
.score-out { font-size: 9px; color: var(--text-muted); }
.risk-level-badge {
  text-align: center; margin: 4px 0 10px;
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
  padding: 3px 10px; border-radius: 4px; display: inline-block;
}
.risk-level-badge.low { background: var(--green-dim); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
.risk-level-badge.medium { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,158,11,0.3); }
.risk-level-badge.high { background: var(--red-dim); color: var(--red); border: 1px solid rgba(239,68,68,0.3); }
.risk-level-badge.critical { background: var(--purple-dim); color: var(--purple); border: 1px solid rgba(168,85,247,0.3); animation: attackPulse 1s infinite; }
.score-bars { display: flex; flex-direction: column; gap: 5px; margin-top: 8px; }
.score-bar-row { display: flex; align-items: center; gap: 6px; font-size: 10px; }
.score-bar-label { width: 50px; color: var(--text-muted); flex-shrink: 0; }
.score-bar-track { flex: 1; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.score-bar-fill { height: 100%; border-radius: 2px; transition: width 1s ease; }
.score-bar-val { width: 20px; text-align: right; color: var(--text-secondary); flex-shrink: 0; }

/* ── CONTENT AREA ── */
.content { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px; min-width: 0; }

/* ── CONTROL BAR ── */
.control-bar {
  display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 18px;
}
.control-bar-left { display: flex; gap: 8px; flex-wrap: wrap; flex: 1; }
.btn {
  padding: 7px 16px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-family: var(--mono);
  font-size: 11.5px;
  cursor: pointer;
  transition: all 0.2s;
  margin-left:10px;
  display: flex; align-items: center; gap: 6px;
  white-space: nowrap;
}
.btn:hover { border-color: var(--border-bright); color: var(--text-primary); background: var(--bg-hover); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-primary { background: var(--blue); border-color: var(--blue); color: #fff; font-weight: 600; }
.btn-primary:hover { background: #2563eb; border-color: #2563eb; color: #fff; box-shadow: 0 0 16px rgba(59,130,246,0.4); }
.btn-danger { border-color: rgba(239,68,68,0.4); color: var(--red); }
.btn-danger:hover { background: var(--red-dim); border-color: var(--red); color: var(--red); }
.btn-success { border-color: rgba(34,197,94,0.4); color: var(--green); }
.btn-success:hover { background: var(--green-dim); border-color: var(--green); }
.btn-purple { border-color: rgba(168,85,247,0.4); color: var(--purple); }
.btn-purple:hover { background: var(--purple-dim); border-color: var(--purple); }

/* ── SCENARIO SELECTOR ── */
.scenario-select {
  background: var(--bg-card); border: 1px solid var(--border-bright);
  color: var(--cyan); font-family: var(--mono); font-size: 11.5px;
  border-radius: 6px; padding: 7px 12px; cursor: pointer; outline: none;
  transition: all 0.2s;
}
.scenario-select:hover, .scenario-select:focus { border-color: var(--blue); box-shadow: 0 0 0 2px var(--blue-glow); }

/* ── PHASE PANELS ── */
.phase-section { display: flex; flex-direction: column; gap: 12px; }
.phase-header {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px;
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 10px 10px 0 0;
  border-bottom: none;
}
.phase-tag {
  background: var(--blue-glow);
  border: 1px solid rgba(59,130,246,0.3);
  color: var(--blue);
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  flex-shrink: 0;
}
.phase-tag.green { background: var(--green-dim); border-color: rgba(34,197,94,0.3); color: var(--green); }
.phase-tag.amber { background: var(--amber-dim); border-color: rgba(245,158,11,0.3); color: var(--amber); }
.phase-tag.red { background: var(--red-dim); border-color: rgba(239,68,68,0.3); color: var(--red); }
.phase-tag.cyan { background: rgba(34,211,238,0.08); border-color: rgba(34,211,238,0.3); color: var(--cyan); }
.phase-h-title { font-family: var(--display); font-size: 16px; font-weight: 700; color: var(--text-primary); margin-left:10px; letter-spacing: 0.5px; }
.phase-h-sub { font-size: 11px; color: var(--text-muted); margin-left: auto; }
.phase-body {
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 10px 10px;
  padding: 16px;
  display: grid;
  gap: 14px;
}
.phase-body.cols2 { grid-template-columns: 1fr 1fr; }
.phase-body.cols3 { grid-template-columns: 1fr 1fr 1fr; }

/* ── LOG PANE ── */
.log-pane {
  background: #020408;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.log-pane-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 8px 14px;
  font-size: 10px; color: var(--text-muted);
  display: flex; align-items: center; gap: 8px;
  letter-spacing: 0.5px;
}
.log-pane-header::before { content:'●'; color: var(--red); font-size: 8px; }
.log-pane-header::after { content:''; flex:1; }
.log-body {
  padding: 12px;
  font-size: 11.5px;
  line-height: 1.7;
  max-height: 220px;
  overflow-y: auto;
  color: var(--text-secondary);
}
.log-body::-webkit-scrollbar { width: 4px; }
.log-body::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }

/* log colors */
.lc { color: var(--cyan); }
.lg { color: var(--green); }
.la { color: var(--amber); }
.lr { color: var(--red); }
.lb { color: var(--blue); }
.lm { color: var(--text-muted); }
.lp { color: var(--purple); }

/* ── RESULT PANE ── */
.result-pane {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  margin-top: 10px;
}
.result-pane-title { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
.result-pane-title::before { content:'▸'; color: var(--blue); }

/* ── STATUS INDICATORS ── */
.hw-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
.hw-item {
  background: linear-gradient(180deg, #0b1320, #0d1728);
  border: 1px solid rgba(59,130,246,0.12);
  border-radius: 18px;
  padding: 18px 14px;
  text-align: center;
  box-shadow: 0 18px 40px rgba(10,24,48,0.24);
  transition: transform 0.32s ease, box-shadow 0.32s ease, border-color 0.32s ease, background 0.32s ease;
}
.hw-item:hover { transform: translateY(-3px) scale(1.02); border-color: rgba(59,130,246,0.28); box-shadow: 0 26px 48px rgba(10,24,48,0.3); }
.hw-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin: 10px 0 4px; }
.hw-val { font-family: var(--display); font-size: 16px; font-weight: 700; }
.hw-val.ok { color: var(--green); }
.hw-val.warn { color: var(--amber); }
.hw-val.err { color: var(--red); }
.hw-sub { font-size: 10px; color: var(--text-muted); margin-top: 6px; }

/* ── PROGRESS BAR ── */
.progress-row { display: flex; flex-direction: column; gap: 6px; }
.prog-item { display: flex; align-items: center; gap: 10px; font-size: 11px; }
.prog-label { width: 120px; color: var(--text-secondary); flex-shrink: 0; }
.prog-track { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; transition: width 1.5s ease; }
.prog-pct { width: 36px; text-align: right; font-size: 11px; color: var(--text-muted); }

/* ── UEFI FLOW ── */
.uefi-flow { display: flex; align-items: center; justify-content: center; gap: 0; flex-wrap: wrap; }
.uefi-step {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 12px 16px;
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  min-width: 80px; text-align: center;
  transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
}
.uefi-step.active {
  background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(34,211,238,0.1));
  border-color: var(--blue); color: var(--blue);
  box-shadow: 0 0 20px rgba(59,130,246,0.3);
  transform: translateY(-4px) scale(1.05);
}
.uefi-step.done {
  background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(34,211,238,0.05));
  border-color: rgba(34,197,94,0.5); color: var(--green);
  box-shadow: 0 0 12px rgba(34,197,94,0.2);
}
.uefi-step.err {
  background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(168,85,247,0.05));
  border-color: rgba(239,68,68,0.5); color: var(--red);
  box-shadow: 0 0 12px rgba(239,68,68,0.3);
}
.uefi-step-name { font-family: var(--display); font-size: 15px; font-weight: 700; }
.uefi-step-sub { font-size: 9px; color: var(--text-muted); }
.uefi-arrow { font-size: 18px; color: var(--border-bright); margin: 0 4px; }

/* ── CHIPSEC TERMINAL ── */
.chip-terminal {
  background: #020408;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.chip-term-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 10px 14px;
  display: flex; align-items: center; gap: 6px;
}
.term-dot { width: 10px; height: 10px; border-radius: 50%; }
.term-dot-r { background: #ef4444; }
.term-dot-y { background: #f59e0b; }
.term-dot-g { background: #22c55e; }
.term-title { margin-left: 8px; font-size: 11px; color: var(--text-muted); }
.chip-cmd-area {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: #030609;
}
.chip-prompt { color: var(--green); font-size: 11px; white-space: nowrap; }
.chip-cmd-area input {
  flex: 1; background: none; border: none; font-family: var(--mono);
  font-size: 11.5px; color: var(--cyan); outline: none; caret-color: var(--cyan);
}
.chip-run-btn {
  background: var(--blue); border: none; border-radius: 4px;
  color: #fff; font-family: var(--mono); font-size: 11px;
  padding: 4px 12px; cursor: pointer; transition: background 0.2s;
}
.chip-run-btn:hover { background: #2563eb; }
.chip-output {
  padding: 12px 14px; min-height: 180px; max-height: 260px;
  overflow-y: auto; font-size: 11.5px; line-height: 1.75;
  color: var(--text-secondary);
}
.chip-output::-webkit-scrollbar { width: 4px; }
.chip-output::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
.chip-suggestions {
  padding: 10px 14px; border-top: 1px solid var(--border);
  display: flex; flex-wrap: wrap; gap: 6px;
}
.chip-suggest-btn {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 4px; color: var(--text-muted); font-family: var(--mono);
  font-size: 10.5px; padding: 4px 10px; cursor: pointer; transition: all 0.2s;
}
.chip-suggest-btn:hover { border-color: var(--blue); color: var(--blue); }

/* ── BAR CHART ── */
.chart-wrap { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
.chart-title { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.bar-chart { display: flex; flex-direction: column; gap: 8px; }
.bar-row { display: flex; align-items: center; gap: 10px; }
.bar-lbl { width: 120px; font-size: 10.5px; color: var(--text-secondary); flex-shrink: 0; }
.bar-outer { flex: 1; height: 20px; background: var(--border); border-radius: 3px; overflow: hidden; }
.bar-inner { height: 100%; border-radius: 3px; display: flex; align-items: center; padding: 0 8px; font-size: 10px; font-weight: 700; transition: width 1.2s cubic-bezier(0.4,0,0.2,1); }
.bar-inner.red-b { background: linear-gradient(90deg, #b91c1c, var(--red)); color: #fff; }
.bar-inner.amber-b { background: linear-gradient(90deg, #b45309, var(--amber)); }
.bar-inner.green-b { background: linear-gradient(90deg, #15803d, var(--green)); }
.bar-inner.blue-b { background: linear-gradient(90deg, var(--blue-dim), var(--blue)); color: #fff; }

/* ── GLOBAL TERMINAL ── */
.global-terminal {
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.gt-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 10px 16px;
  display: flex; align-items: center; gap: 8px;
}
.gt-dots { display: flex; gap: 5px; }
.gt-title { margin-left: 10px; font-size: 11px; color: var(--text-muted); font-family: var(--mono); }
.gt-body {
  padding: 14px;
  min-height: 200px; max-height: 340px;
  overflow-y: auto;
  font-size: 12px; line-height: 1.7; color: var(--text-secondary);
  white-space: pre-wrap;
}
.gt-body::-webkit-scrollbar { width: 4px; }
.gt-body::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
.gt-input-row {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid var(--border);
  background: #020408;
}
.gt-prompt { color: var(--green); font-size: 12px; white-space: nowrap; }
.gt-input {
  flex: 1; background: none; border: none; font-family: var(--mono);
  font-size: 12px; color: var(--cyan); outline: none; caret-color: var(--cyan);
}
.gt-input::placeholder { color: var(--text-muted); }
.gt-enter-hint { font-size: 10px; color: var(--text-muted); }

/* ── VULN CARDS ── */
.vuln-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
.vuln-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}
.vuln-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.vuln-card.critical::before { background: linear-gradient(90deg, var(--purple), var(--red)); }
.vuln-card.high::before { background: var(--red); }
.vuln-card.medium::before { background: var(--amber); }
.vuln-card.low::before { background: var(--green); }
.vuln-card.high.flash { animation: vulnFlash 1.5s ease-in-out infinite alternate; }
.vuln-card.critical.flash { animation: critFlash 0.8s ease-in-out infinite alternate; }
.vuln-sev {
  font-size: 9px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
  padding: 2px 8px; border-radius: 3px; display: inline-block; margin-bottom: 8px;
}
.vuln-sev.critical { background: var(--purple-dim); color: var(--purple); border: 1px solid rgba(168,85,247,0.4); }
.vuln-sev.high { background: var(--red-dim); color: var(--red); border: 1px solid rgba(239,68,68,0.4); }
.vuln-sev.medium { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,158,11,0.4); }
.vuln-sev.low { background: var(--green-dim); color: var(--green); border: 1px solid rgba(34,197,94,0.4); }
.vuln-title { font-family: var(--display); font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.vuln-desc { font-size: 11px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 10px; }
.vuln-rec { font-size: 10.5px; color: var(--cyan); border-left: 2px solid var(--cyan); padding-left: 8px; line-height: 1.5; }
.vuln-hash { font-size: 9px; color: var(--text-muted); font-family: var(--mono); margin-top: 8px; }
.vuln-actions { display: flex; gap: 6px; margin-top: 12px; flex-wrap: wrap; }
.vuln-btn {
  font-size: 10px; font-family: var(--mono);
  padding: 4px 10px; border-radius: 4px; cursor: pointer;
  border: 1px solid; transition: all 0.2s; background: none;
}
.vuln-btn.why { border-color: rgba(245,158,11,0.4); color: var(--amber); }
.vuln-btn.why:hover { background: var(--amber-dim); }
.vuln-btn.fix { border-color: rgba(34,197,94,0.4); color: var(--green); }
.vuln-btn.fix:hover { background: var(--green-dim); }
.vuln-btn.cve { border-color: rgba(59,130,246,0.4); color: var(--blue); }
.vuln-btn.cve:hover { background: var(--blue-glow); }

/* ── LEARNING PANEL (Modal) ── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(2,4,8,0.85);
  backdrop-filter: blur(6px);
  z-index: 1000;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none;
  transition: opacity 0.3s;
}
.modal-overlay.show { opacity: 1; pointer-events: all; }
.modal-panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-bright);
  border-radius: 14px;
  width: min(700px, 94vw);
  max-height: 85vh;
  overflow-y: auto;
  padding: 32px;
  position: relative;
  transform: translateY(20px) scale(0.97);
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
  box-shadow: 0 40px 100px rgba(0,0,0,0.6), 0 0 0 1px rgba(59,130,246,0.1);
}
.modal-overlay.show .modal-panel { transform: translateY(0) scale(1); }
.modal-close {
  position: absolute; top: 16px; right: 20px;
  background: none; border: 1px solid var(--border); color: var(--text-muted);
  border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 12px;
  transition: all 0.2s;
}
.modal-close:hover { border-color: var(--red); color: var(--red); }
.modal-badge { font-size: 9px; font-weight: 800; letter-spacing: 2px; padding: 3px 10px; border-radius: 4px; text-transform: uppercase; display: inline-block; margin-bottom: 12px; }
.modal-title { font-family: var(--display); font-size: 22px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.modal-subtitle { font-size: 11px; color: var(--text-muted); margin-bottom: 24px; }
.modal-section { margin-bottom: 22px; }
.modal-section-title {
  font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
  color: var(--blue); margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}
.modal-section-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.modal-section p { font-size: 12px; color: var(--text-secondary); line-height: 1.8; }
.modal-impact-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-top: 10px; }
.modal-impact-item {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px;
  padding: 12px; text-align: center;
}
.modal-impact-score { font-family: var(--display); font-size: 20px; font-weight: 700; }
.modal-impact-label { font-size: 9px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.modal-steps { display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }
.modal-step {
  display: flex; gap: 12px; align-items: flex-start;
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 12px;
}
.modal-step-num {
  width: 22px; height: 22px; border-radius: 50%; background: var(--blue);
  color: #fff; font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.modal-step-text { font-size: 11.5px; color: var(--text-secondary); line-height: 1.6; }
.modal-cve-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.modal-cve-tag {
  background: var(--blue-glow); border: 1px solid rgba(59,130,246,0.3);
  color: var(--blue); font-size: 10px; padding: 3px 8px; border-radius: 4px;
  font-family: var(--mono);
}
.modal-code {
  background: #020408; border: 1px solid var(--border); border-radius: 6px;
  padding: 12px; font-size: 11px; color: var(--cyan);
  font-family: var(--mono); line-height: 1.6; margin-top: 8px;
  white-space: pre-wrap;
}

/* ── HEX VIEWER ── */
.hex-viewer {
  background: #020408; border: 1px solid var(--border); border-radius: 8px;
  padding: 12px; font-size: 11px; line-height: 1.6;
  max-height: 200px; overflow-y: auto; font-family: var(--mono);
}
.hex-addr { color: #4a6080; margin-right: 12px; user-select: none; }
.hex-bytes { color: var(--text-secondary); margin-right: 12px; }
.hex-ascii { color: #506878; }

/* ── FIRMWARE TREE ── */
.fw-tree { font-size: 11px; line-height: 1.8; color: var(--text-secondary); font-family: var(--mono); }
.fw-dir { color: var(--blue); }
.fw-ok { color: var(--green); }
.fw-warn { color: var(--amber); }
.fw-err { color: var(--red); }

/* ── MINI TABS ── */
.mini-tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 12px; }
.mini-tab { padding: 6px 14px; font-size: 11px; color: var(--text-muted); cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.2s; }
.mini-tab:hover { color: var(--text-secondary); }
.mini-tab.active { color: var(--blue); border-bottom-color: var(--blue); }

/* ── TOAST ── */
.toast-container {
  position: fixed; top: 22px; right: 22px;
  display: flex; flex-direction: column; gap: 12px;
  z-index: 9999; pointer-events: none;
}
.toast {
  pointer-events: auto; opacity: 0;
  transform: translateY(-12px) scale(0.98);
  border-radius: 16px; padding: 14px 16px;
  background: rgba(8,15,27,0.96);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 24px 70px rgba(0,0,0,0.35);
  color: #f8fafc; font-size: 13px; line-height: 1.5;
  animation: toastIn 0.35s ease forwards;
  max-width: 340px;
}
.toast--info { border-left: 4px solid var(--blue); }
.toast--error { border-left: 4px solid var(--red); }
.toast--warn { border-left: 4px solid var(--amber); }
.toast--success { border-left: 4px solid var(--green); }
.toast--critical { border-left: 4px solid var(--purple); }
.toast-title { font-weight: 700; margin-bottom: 4px; }
.toast-text { color: var(--text-secondary); font-size: 12px; }
.toast-hide { animation: toastOut 0.35s ease forwards; }
@keyframes toastIn { from{opacity:0;transform:translateY(-12px) scale(0.98)} to{opacity:1;transform:translateY(0) scale(1)} }
@keyframes toastOut { from{opacity:1;transform:translateY(0) scale(1)} to{opacity:0;transform:translateY(-12px) scale(0.98)} }
@keyframes vulnFlash { from{box-shadow:0 18px 40px rgba(10,20,40,0.24)} to{box-shadow:0 24px 48px rgba(239,68,68,0.28)} }
@keyframes critFlash { from{box-shadow:0 18px 40px rgba(10,20,40,0.24);border-color:var(--border)} to{box-shadow:0 24px 48px rgba(168,85,247,0.35);border-color:rgba(168,85,247,0.5)} }

/* ── LOADING BAR ── */
.loading-bar {
  height: 2px; background: var(--blue); width: 0%;
  transition: width 0.3s ease; border-radius: 1px;
  box-shadow: 0 0 6px var(--blue);
}
.loading-bar.scan { background: var(--red); box-shadow: 0 0 6px var(--red); }
.loading-bar.attack { background: var(--purple); box-shadow: 0 0 10px var(--purple); animation: attackBar 0.5s ease-in-out; }
@keyframes attackBar { 0%{opacity:1}50%{opacity:0.4}100%{opacity:1} }

/* ── OVERVIEW CARDS ── */
.overview-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }

/* ── SECURE BOOT BADGE ── */
.secure-boot-badge {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 16px; border-radius: 8px;
  font-size: 13px; font-weight: 600;
  background: var(--bg-panel); border: 1px solid var(--border);
  transition: all 0.4s;
}

/* ── MISC ── */
.stack-col { display: flex; flex-direction: column; gap: 12px; }
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.timeline-list { display: flex; flex-direction: column; gap: 6px; font-size: 11.5px; }
.timeline-item { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.timeline-item span { margin-left: 5px; }
.timeline-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); flex-shrink: 0; transition: background 0.5s; }
.flow-summary { display: flex; flex-wrap: wrap; gap: 16px; font-family: var(--display); justify-content: space-between; }
.gap-8 { gap: 8px; }
.mt-4 { margin-top: 4px; }
.center-text { text-align: center; }
.full-span { grid-column: 1 / -1; }
.detail-text { font-size: 11.5px; color: var(--text-muted); line-height: 1.8; }
.padded-large { padding: 32px; }

/* ── ATTACK OVERLAY ── */
.attack-warning-bar {
  display: none;
  background: linear-gradient(90deg, rgba(168,85,247,0.15), rgba(239,68,68,0.1), rgba(168,85,247,0.15));
  border: 1px solid rgba(168,85,247,0.4);
  border-radius: 8px; padding: 10px 18px; margin-bottom: 8px;
  font-size: 11.5px; color: var(--purple); font-weight: 600;
  animation: attackPulse 1s infinite;
  letter-spacing: 0.5px;
}
.attack-warning-bar.show { display: flex; align-items: center; gap: 10px; }

/* ── ANIMATIONS ── */
@keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.phase-section { animation: fadeIn 0.4s ease both; }
.phase-section:nth-child(2){animation-delay:0.05s}
.phase-section:nth-child(3){animation-delay:0.1s}
.phase-section:nth-child(4){animation-delay:0.15s}
.phase-section:nth-child(5){animation-delay:0.2s}
.phase-section:nth-child(6){animation-delay:0.25s}

@keyframes typeCharIn { from{opacity:0} to{opacity:1} }
.type-in { animation: typeCharIn 0.08s ease forwards; }

.blink { animation: blink-anim 1s step-end infinite; }
@keyframes blink-anim { 50%{opacity:0} }

/* ── RESPONSIVE ── */
@media (max-width: 1200px) {
  .overview-grid { grid-template-columns: repeat(2, 1fr); }
  .summary-grid { grid-template-columns: repeat(2, 1fr); }
  .nav-tabs { padding: 0 16px; padding-top:26px; }
  .nav-tab { font-size: 10.8px; padding: 10px 14px; }
}
@media (max-width: 900px) {
  .main { flex-direction: column; }
  .sidebar { display: none; }
  .content { padding: 18px 16px 24px; }
  .control-bar { flex-direction: column; align-items: stretch; }
  .overview-grid, .summary-grid, .hw-grid { grid-template-columns: 1fr; }
  .phase-body.cols2, .phase-body.cols3 { grid-template-columns: 1fr; }
  .modal-impact-grid { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
  .btn { font-size: 2vw; padding: 5px 10px; }
  .status-badge { font-size: 2vw; padding: 5px 10px; }
  #globalStatus { margin-left:10px; }
  .header-logo { width: fit-content; height: fit-content; padding: 4px 5px; }
  .header-title { font-size: 3vw; }
  .header-right { border-radius: 99px; justify-content: end; gap: 4px; }
  .header-left { width: 100%; }
  .phase-h-title { font-size: 3vw; }
  .vuln-grid { grid-template-columns: 1fr; }
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# HTML — Full page structure with scenario selector & modal
# ══════════════════════════════════════════════════════════════════════════════
HTML_BODY = """<div class="app">

<!-- ── HEADER ── -->
<header>
  <div class="header-left">
    <div class="header-logo">🔒</div>
    <div>
      <div class="header-title">BIOS/<span>UEFI</span> Security Analyzer</div>
    </div>
  </div>
  <div class="header-right">
    <div class="scenario-badge" id="scenarioBadge">⚙ Scenario: NONE</div>
    <div class="status-badge"><div class="status-dot" id="globalDot"></div><span id="globalStatus">IDLE</span></div>
    <button class="btn btn-primary" id="masterBtn" onclick="runFullSim()">▶ Run Simulation</button>
  </div>
</header>

<!-- ── NAV TABS ── -->
<div class="nav-tabs">
  <button class="nav-tab active" data-tab="dashboard" onclick="showTab('dashboard',this)">Dashboard</button>
  <button class="nav-tab" data-tab="bios" onclick="showTab('bios',this)">Phase 1–2: Boot</button>
  <button class="nav-tab" data-tab="uefi" onclick="showTab('uefi',this)">Phase 3: UEFI</button>
  <button class="nav-tab" data-tab="security" onclick="showTab('security',this)">Phase 4: CHIPSEC</button>
  <button class="nav-tab" data-tab="firmware" onclick="showTab('firmware',this)">Phase 5: Firmware</button>
  <button class="nav-tab" data-tab="findings" onclick="showTab('findings',this)">Phase 6: Findings</button>
  <button class="nav-tab" data-tab="terminal" onclick="showTab('terminal',this)">Terminal</button>
  <button class="nav-tab" data-tab="learn" onclick="showTab('learn',this)">📚 Learn</button>
</div>

<!-- ── MAIN ── -->
<div class="main">

  <!-- ── SIDEBAR ── -->
  <aside class="sidebar">
    <div class="sidebar-section">Phases</div>
    <div class="phase-item active" id="si-1" onclick="showTab('bios', null, 1)">
      <div class="phase-num" id="sn-1">1</div>
      <div class="phase-info"><div class="phase-name">System Start</div><div class="phase-status" id="ss-1">Awaiting run…</div></div>
    </div>
    <div class="phase-item" id="si-2" onclick="showTab('bios', null, 2)">
      <div class="phase-num" id="sn-2">2</div>
      <div class="phase-info"><div class="phase-name">BIOS Boot (Bochs)</div><div class="phase-status" id="ss-2">Awaiting run…</div></div>
    </div>
    <div class="phase-item" id="si-3" onclick="showTab('uefi', null, 3)">
      <div class="phase-num" id="sn-3">3</div>
      <div class="phase-info"><div class="phase-name">UEFI Boot (QEMU)</div><div class="phase-status" id="ss-3">Awaiting run…</div></div>
    </div>
    <div class="phase-item" id="si-4" onclick="showTab('security', null, 4)">
      <div class="phase-num" id="sn-4">4</div>
      <div class="phase-info"><div class="phase-name">CHIPSEC Analysis</div><div class="phase-status" id="ss-4">Awaiting run…</div></div>
    </div>
    <div class="phase-item" id="si-5" onclick="showTab('firmware', null, 5)">
      <div class="phase-num" id="sn-5">5</div>
      <div class="phase-info"><div class="phase-name">Firmware Inspection</div><div class="phase-status" id="ss-5">Awaiting run…</div></div>
    </div>
    <div class="phase-item" id="si-6" onclick="showTab('findings', null, 6)">
      <div class="phase-num" id="sn-6">6</div>
      <div class="phase-info"><div class="phase-name">Security Findings</div><div class="phase-status" id="ss-6">Awaiting run…</div></div>
    </div>

    <div class="sidebar-section" style="margin-top:16px">Risk Score</div>
    <div class="sidebar-score">
      <div class="score-label">Overall Security</div>
      <div class="score-ring">
        <svg viewBox="0 0 80 80" width="80" height="80">
          <circle cx="40" cy="40" r="32" fill="none" stroke="#1e3050" stroke-width="7"/>
          <circle id="scoreArc" cx="40" cy="40" r="32" fill="none" stroke="#f59e0b" stroke-width="7"
            stroke-dasharray="201" stroke-dashoffset="201" stroke-linecap="round"
            style="transition:stroke-dashoffset 1.5s ease, stroke 0.5s ease"/>
        </svg>
        <div class="score-ring-text">
          <span class="score-val" id="scoreVal">--</span>
          <span class="score-out">/100</span>
        </div>
      </div>
      <div style="text-align:center"><span class="risk-level-badge" id="riskLevelBadge">—</span></div>
      <div class="score-bars">
        <div class="score-bar-row">
          <div class="score-bar-label">Critical</div>
          <div class="score-bar-track"><div class="score-bar-fill" id="sb-crit" style="width:0%;background:var(--red)"></div></div>
          <div class="score-bar-val" id="sv-crit">--</div>
        </div>
        <div class="score-bar-row">
          <div class="score-bar-label">Medium</div>
          <div class="score-bar-track"><div class="score-bar-fill" id="sb-med" style="width:0%;background:var(--amber)"></div></div>
          <div class="score-bar-val" id="sv-med">--</div>
        </div>
        <div class="score-bar-row">
          <div class="score-bar-label">Secure</div>
          <div class="score-bar-track"><div class="score-bar-fill" id="sb-sec" style="width:0%;background:var(--green)"></div></div>
          <div class="score-bar-val" id="sv-sec">--</div>
        </div>
      </div>
    </div>
  </aside>

  <!-- ── CONTENT ── -->
  <div class="content" id="content">

    <!-- ══ DASHBOARD TAB ══ -->
    <div id="tab-dashboard">
      <!-- Attack warning bar -->
      <div class="attack-warning-bar" id="attackBar">
        ☠ ACTIVE ATTACK DETECTED — FIRMWARE TAMPERING IN PROGRESS — SYSTEM COMPROMISED
      </div>
      <div class="control-bar">
        <div class="control-bar-left">
          <button class="btn btn-primary" id="btnFull" onclick="runFullSim()">▶ Run Full Simulation</button>
          <button class="btn" onclick="runPhase([1,2],'bios')">🖥 BIOS Boot</button>
          <button class="btn" onclick="runPhase([3],'uefi')">⚡ UEFI Boot</button>
          <button class="btn" onclick="runPhase([4,5,6],'security')">🔍 Security Scan</button>
          <button class="btn btn-danger" onclick="resetAll()">↺ Reset</button>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          <label style="font-size:10px;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase">Scenario:</label>
          <select class="scenario-select" id="scenarioSelect" onchange="changeScenario(this.value)">
            <option value="random">🎲 Random</option>
            <option value="secure">✅ Secure System</option>
            <option value="misconfigured">⚠️ Misconfigured</option>
            <option value="vulnerable">🔓 Vulnerable</option>
            <option value="attacked">☠️ Under Attack</option>
          </select>
          <button class="btn btn-success" onclick="exportPDF()">⬇ Export PDF</button>
        </div>
      </div>

      <!-- Overview cards -->
      <div class="overview-grid">
        <div class="result-pane" style="text-align:center">
          <div class="result-pane-title" style="justify-content:center">Platform</div>
          <div style="font-family:var(--display);font-size:18px;font-weight:700;color:var(--cyan)">Intel i7-11700K</div>
          <div style="font-size:10px;color:var(--text-muted);margin-top:4px">8C/16T · 16 GB DDR4-3200</div>
        </div>
        <div class="result-pane" style="text-align:center">
          <div class="result-pane-title" style="justify-content:center">Firmware</div>
          <div style="font-family:var(--display);font-size:18px;font-weight:700;color:var(--blue)">UEFI 2.7</div>
          <div style="font-size:10px;color:var(--text-muted);margin-top:4px">Winbond W25Q128 · 16 MB SPI</div>
        </div>
        <div class="result-pane" style="text-align:center">
          <div class="result-pane-title" style="justify-content:center">Secure Boot</div>
          <div style="font-family:var(--display);font-size:18px;font-weight:700;color:var(--green)" id="dash-sb">--</div>
          <div style="font-size:10px;color:var(--text-muted);margin-top:4px">PK + KEK + db/dbx</div>
        </div>
        <div class="result-pane" style="text-align:center">
          <div class="result-pane-title" style="justify-content:center">Risk Score</div>
          <div style="font-family:var(--display);font-size:18px;font-weight:700;color:var(--amber)" id="dash-score">--/100</div>
          <div style="font-size:10px;color:var(--text-muted);margin-top:4px" id="dash-risk">Simulation not run</div>
        </div>
      </div>

      <div class="loading-bar" id="globalProgress"></div>

      <div class="summary-grid">
        <div class="result-pane">
          <div class="result-pane-title">Boot Sequence</div>
          <div style="font-size:11px;color:var(--text-muted);line-height:1.9" id="dash-boot-sum">Run simulation to populate…</div>
        </div>
        <div class="result-pane">
          <div class="result-pane-title">CHIPSEC Results</div>
          <div style="font-size:11px;color:var(--text-muted);line-height:1.9" id="dash-chip-sum">Run simulation to populate…</div>
        </div>
        <div class="result-pane">
          <div class="result-pane-title">Vulnerability Summary</div>
          <div style="font-size:11px;color:var(--text-muted);line-height:1.9" id="dash-vuln-sum">Run simulation to populate…</div>
        </div>
      </div>
    </div>

    <!-- ══ BIOS TAB ══ -->
    <div id="tab-bios" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag">Phase 1</div>
          <div class="phase-h-title">System Power-On &amp; Hardware Init</div>
          <div class="phase-h-sub">Bochs x86 Emulator</div>
        </div>
        <div class="phase-body cols2">
          <div>
            <div class="result-pane-title">Boot Log</div>
            <div class="log-pane">
              <div class="log-pane-header">system · power-on sequence</div>
              <div class="log-body" id="log-p1"><span class="lm">[ Simulation not started ]</span></div>
            </div>
          </div>
          <div class="stack-col">
            <div class="result-pane">
              <div class="result-pane-title">Hardware Status</div>
              <div class="hw-grid">
                <div class="hw-item"><div class="hw-label">CPU</div><div class="hw-val" id="hw-cpu">—</div><div class="hw-sub">i7-11700K</div></div>
                <div class="hw-item"><div class="hw-label">RAM</div><div class="hw-val" id="hw-ram">—</div><div class="hw-sub">16 GB DDR4</div></div>
                <div class="hw-item"><div class="hw-label">Storage</div><div class="hw-val" id="hw-disk">—</div><div class="hw-sub">WD 1TB HDD</div></div>
                <div class="hw-item"><div class="hw-label">PSU</div><div class="hw-val" id="hw-psu">—</div><div class="hw-sub">12V/5V/3.3V</div></div>
                <div class="hw-item"><div class="hw-label">GPU</div><div class="hw-val" id="hw-gpu">—</div><div class="hw-sub">VGA Adapter</div></div>
                <div class="hw-item"><div class="hw-label">TPM</div><div class="hw-val" id="hw-tpm">—</div><div class="hw-sub">TPM 2.0</div></div>
              </div>
            </div>
            <div class="result-pane">
              <div class="result-pane-title">Initialization Progress</div>
              <div class="progress-row">
                <div class="prog-item"><div class="prog-label">Power Supply</div><div class="prog-track"><div class="prog-fill" id="pf-psu" style="width:0%;background:var(--green)"></div></div><div class="prog-pct" id="pp-psu">0%</div></div>
                <div class="prog-item"><div class="prog-label">CPU Init</div><div class="prog-track"><div class="prog-fill" id="pf-cpu" style="width:0%;background:var(--blue)"></div></div><div class="prog-pct" id="pp-cpu">0%</div></div>
                <div class="prog-item"><div class="prog-label">RAM Test</div><div class="prog-track"><div class="prog-fill" id="pf-ram" style="width:0%;background:var(--cyan)"></div></div><div class="prog-pct" id="pp-ram">0%</div></div>
                <div class="prog-item"><div class="prog-label">Device Enum</div><div class="prog-track"><div class="prog-fill" id="pf-dev" style="width:0%;background:var(--amber)"></div></div><div class="prog-pct" id="pp-dev">0%</div></div>
                <div class="prog-item"><div class="prog-label">POST</div><div class="prog-track"><div class="prog-fill" id="pf-post" style="width:0%;background:var(--green)"></div></div><div class="prog-pct" id="pp-post">0%</div></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag amber">Phase 2</div>
          <div class="phase-h-title">Legacy BIOS Boot Process</div>
          <div class="phase-h-sub">Bochs MBR Simulation</div>
        </div>
        <div class="phase-body cols2">
          <div>
            <div class="result-pane-title">POST &amp; MBR Log</div>
            <div class="log-pane">
              <div class="log-pane-header">bochs · bios-config.bxrc</div>
              <div class="log-body" id="log-p2"><span class="lm">[ Awaiting phase 2 ]</span></div>
            </div>
          </div>
          <div class="stack-col">
            <div class="result-pane">
              <div class="result-pane-title">Boot Timeline</div>
              <div class="timeline-list">
                <div class="timeline-item"><div class="timeline-dot" id="tl-1"></div><span>POST Initiated</span><span class="lm" id="tl-1-s">—</span></div>
                <div class="timeline-item"><div class="timeline-dot" id="tl-2"></div><span>Hardware Checked</span><span class="lm" id="tl-2-s">—</span></div>
                <div class="timeline-item"><div class="timeline-dot" id="tl-3"></div><span>MBR Loaded (0x7C00)</span><span class="lm" id="tl-3-s">—</span></div>
                <div class="timeline-item"><div class="timeline-dot" id="tl-4"></div><span>Bootloader Verified</span><span class="lm" id="tl-4-s">—</span></div>
                <div class="timeline-item"><div class="timeline-dot" id="tl-5"></div><span>Bootloader Executing</span><span class="lm" id="tl-5-s">—</span></div>
              </div>
            </div>
            <div class="result-pane">
              <div class="result-pane-title">MBR Result</div>
              <div id="mbr-result" class="detail-text">Awaiting simulation…</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ UEFI TAB ══ -->
    <div id="tab-uefi" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag cyan">Phase 3</div>
          <div class="phase-h-title">UEFI Boot — SEC → PEI → DXE → BDS</div>
          <div class="phase-h-sub">QEMU/EDK2 Simulation</div>
        </div>
        <div class="phase-body">
          <div class="result-pane">
            <div class="result-pane-title">UEFI Phase Flow</div>
            <div class="uefi-flow">
              <div class="uefi-step" id="uf-sec"><div class="uefi-step-name">SEC</div><div class="uefi-step-sub">Security Phase</div></div>
              <div class="uefi-arrow">→</div>
              <div class="uefi-step" id="uf-pei"><div class="uefi-step-name">PEI</div><div class="uefi-step-sub">Pre-EFI Init</div></div>
              <div class="uefi-arrow">→</div>
              <div class="uefi-step" id="uf-dxe"><div class="uefi-step-name">DXE</div><div class="uefi-step-sub">Driver Execution</div></div>
              <div class="uefi-arrow">→</div>
              <div class="uefi-step" id="uf-bds"><div class="uefi-step-name">BDS</div><div class="uefi-step-sub">Boot Dev Sel</div></div>
              <div class="uefi-arrow">→</div>
              <div class="uefi-step" id="uf-os"><div class="uefi-step-name">OS Loader</div><div class="uefi-step-sub">Handoff</div></div>
            </div>
          </div>
          <div class="grid-2">
            <div>
              <div class="result-pane-title">UEFI Boot Log</div>
              <div class="log-pane">
                <div class="log-pane-header">qemu-system-x86_64 · OVMF</div>
                <div class="log-body" id="log-p3"><span class="lm">[ Awaiting phase 3 ]</span></div>
              </div>
            </div>
            <div class="stack-col">
              <div class="result-pane">
                <div class="result-pane-title">Secure Boot Status</div>
                <div class="secure-boot-badge" id="sb-badge"><span>⏸</span> <span id="sb-text">Not yet checked</span></div>
              </div>
              <div class="result-pane">
                <div class="result-pane-title">OS Loading Output</div>
                <div class="detail-text" id="os-output">Awaiting simulation…</div>
              </div>
              <div class="result-pane">
                <div class="result-pane-title">Driver Count</div>
                <div class="flow-summary">
                  <div class="center-text"><div style="font-size:26px;font-weight:700;color:var(--blue)" id="dc-pei">--</div><div style="font-size:10px;color:var(--text-muted)">PEI Modules</div></div>
                  <div class="center-text"><div style="font-size:26px;font-weight:700;color:var(--cyan)" id="dc-dxe">--</div><div style="font-size:10px;color:var(--text-muted)">DXE Drivers</div></div>
                  <div class="center-text"><div style="font-size:26px;font-weight:700;color:var(--green)" id="dc-total">--</div><div style="font-size:10px;color:var(--text-muted)">Total Modules</div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ SECURITY TAB ══ -->
    <div id="tab-security" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag red">Phase 4</div>
          <div class="phase-h-title">CHIPSEC Security Analysis</div>
          <div class="phase-h-sub">Platform Security Assessment Framework</div>
        </div>
        <div class="phase-body cols2">
          <div>
            <div class="result-pane-title">Interactive CHIPSEC Terminal</div>
            <div class="chip-terminal">
              <div class="chip-term-header">
                <div class="term-dot term-dot-r"></div>
                <div class="term-dot term-dot-y"></div>
                <div class="term-dot term-dot-g"></div>
                <div class="term-title">root@security-lab:~# chipsec_main</div>
              </div>
              <div class="chip-cmd-area">
                <span class="chip-prompt">root@lab:~$</span>
                <input id="chipInput" type="text" placeholder="Type a chipsec command…" onkeydown="handleChip(event)"/>
                <button class="chip-run-btn" onclick="execChip()">Run</button>
              </div>
              <div class="chip-output" id="chipOutput"><span class="lm">Type a command or click a suggestion below. Try: chipsec_main -m common.bios_wp</span></div>
              <div class="chip-suggestions">
                <button class="chip-suggest-btn" onclick="setChip('chipsec_main -m common.bios_wp')">common.bios_wp</button>
                <button class="chip-suggest-btn" onclick="setChip('chipsec_main -m common.secureboot')">common.secureboot</button>
                <button class="chip-suggest-btn" onclick="setChip('chipsec_main -m common.spi')">common.spi</button>
                <button class="chip-suggest-btn" onclick="setChip('chipsec_main -m common.smm')">common.smm</button>
                <button class="chip-suggest-btn" onclick="setChip('chipsec_main --help')">--help</button>
              </div>
            </div>
          </div>
          <div class="stack-col">
            <div class="result-pane">
              <div class="result-pane-title">Scan Results Summary</div>
              <div class="detail-text" id="chip-summary">Run the full simulation or type commands to see results.</div>
            </div>
            <div class="chart-wrap">
              <div class="chart-title">Risk Distribution</div>
              <div class="bar-chart">
                <div class="bar-row"><div class="bar-lbl">SMM Protection</div><div class="bar-outer"><div class="bar-inner red-b" id="rc-smm" style="width:0%">0%</div></div></div>
                <div class="bar-row"><div class="bar-lbl">BIOS Write Prot</div><div class="bar-outer"><div class="bar-inner red-b" id="rc-bwp" style="width:0%">0%</div></div></div>
                <div class="bar-row"><div class="bar-lbl">SPI Flash Lock</div><div class="bar-outer"><div class="bar-inner green-b" id="rc-spi" style="width:0%">0%</div></div></div>
                <div class="bar-row"><div class="bar-lbl">Secure Boot</div><div class="bar-outer"><div class="bar-inner green-b" id="rc-sb" style="width:0%">0%</div></div></div>
                <div class="bar-row"><div class="bar-lbl">SMRAM Lock</div><div class="bar-outer"><div class="bar-inner amber-b" id="rc-smram" style="width:0%">0%</div></div></div>
                <div class="bar-row"><div class="bar-lbl">TPM 2.0</div><div class="bar-outer"><div class="bar-inner blue-b" id="rc-tpm" style="width:0%">0%</div></div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ FIRMWARE TAB ══ -->
    <div id="tab-firmware" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag">Phase 5</div>
          <div class="phase-h-title">Firmware Dump &amp; Inspection</div>
          <div class="phase-h-sub">flashrom + UEFITool NE</div>
        </div>
        <div class="phase-body cols2">
          <div>
            <div class="result-pane-title">Hex Viewer — firmware.bin</div>
            <div class="hex-viewer" id="hex-viewer"><span class="lm">[ Awaiting firmware dump ]</span></div>
            <div style="margin-top:12px">
              <div class="result-pane-title">Dump Log</div>
              <div class="log-pane">
                <div class="log-pane-header">flashrom v1.2 · internal</div>
                <div class="log-body" id="log-p5"><span class="lm">[ Awaiting phase 5 ]</span></div>
              </div>
            </div>
          </div>
          <div>
            <div class="result-pane-title">Firmware Volume Structure — UEFITool</div>
            <div class="result-pane" style="min-height:200px">
              <div class="fw-tree" id="fw-tree"><span class="lm">[ Awaiting parse ]</span></div>
            </div>
            <div style="margin-top:12px">
              <div class="result-pane-title">Module Counts</div>
              <div class="grid-3 gap-8">
                <div class="hw-item"><div class="hw-label">PEI Modules</div><div class="hw-val ok" id="fm-pei">--</div></div>
                <div class="hw-item"><div class="hw-label">DXE Drivers</div><div class="hw-val ok" id="fm-dxe">--</div></div>
                <div class="hw-item"><div class="hw-label">Total Size</div><div class="hw-val" style="color:var(--blue)" id="fm-size">--</div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ FINDINGS TAB ══ -->
    <div id="tab-findings" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag red">Phase 6</div>
          <div class="phase-h-title">Security Findings &amp; Recommendations</div>
          <div class="phase-h-sub">Vulnerability Assessment Report</div>
        </div>
        <div class="phase-body">
          <div class="vuln-grid" id="vuln-grid">
            <div class="result-pane full-span center-text padded-large" style="font-size:12px;color:var(--text-muted);">
              Run simulation to generate findings…
            </div>
          </div>
          <div class="grid-2 mt-4">
            <div class="chart-wrap">
              <div class="chart-title">Severity Breakdown</div>
              <canvas id="sevChart" width="260" height="140"></canvas>
            </div>
            <div class="result-pane">
              <div class="result-pane-title">Immediate Action Items</div>
              <div id="action-items" style="font-size:11.5px;line-height:2;color:var(--text-muted)">Awaiting analysis…</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ TERMINAL TAB ══ -->
    <div id="tab-terminal" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag green">Terminal</div>
          <div class="phase-h-title">Interactive Security Lab Terminal</div>
          <div class="phase-h-sub">Simulated Linux Shell — root@security-lab</div>
        </div>
        <div class="phase-body">
          <div class="global-terminal">
            <div class="gt-header">
              <div class="gt-dots">
                <div class="term-dot term-dot-r"></div>
                <div class="term-dot term-dot-y"></div>
                <div class="term-dot term-dot-g"></div>
              </div>
              <div class="gt-title">root@security-lab:~$ — bash 5.1.16</div>
            </div>
            <div class="gt-body" id="gtBody"><span class="lg">root@security-lab</span><span class="lm">:</span><span class="lb">~</span><span class="lm">$</span> <span class="lc">echo "BIOS/UEFI Security Lab Terminal Ready"</span>
<span class="lg">BIOS/UEFI Security Lab Terminal Ready</span>
<span class="lm">Type 'help' for available commands. Type 'scan' to run a quick security scan.</span>

</div>
            <div class="gt-input-row">
              <span class="gt-prompt">root@security-lab:~$</span>
              <input class="gt-input" id="gtInput" type="text" placeholder="Enter command…" onkeydown="handleGT(event)" autocomplete="off" spellcheck="false"/>
              <span class="gt-enter-hint">↵ Enter</span>
            </div>
          </div>
          <div class="result-pane" style="margin-top:0">
            <div class="result-pane-title">Command History</div>
            <div id="gt-history" style="font-size:11px;color:var(--text-muted);line-height:2;max-height:100px;overflow-y:auto">No commands run yet.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ LEARN TAB ══ -->
    <div id="tab-learn" style="display:none">
      <div class="phase-section">
        <div class="phase-header">
          <div class="phase-tag cyan">Education</div>
          <div class="phase-h-title">BIOS/UEFI Security — Learning Center</div>
          <div class="phase-h-sub">Interactive Reference Guide</div>
        </div>
        <div class="phase-body">
          <div class="grid-2">
            <div>
              <div class="result-pane-title">Key Concepts</div>
              <div class="stack-col" style="gap:8px">
                <div class="result-pane" style="cursor:pointer" onclick="showLearnModal('secureboot')">
                  <div style="font-family:var(--display);font-size:14px;color:var(--cyan);font-weight:700">🔒 Secure Boot</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">UEFI feature that ensures only signed bootloaders execute. Uses PKI chain of trust.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer" onclick="showLearnModal('smm')">
                  <div style="font-family:var(--display);font-size:14px;color:var(--amber);font-weight:700">⚡ SMM (System Management Mode)</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Privileged CPU mode invisible to OS. Used for power management, hardware control.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer" onclick="showLearnModal('spi')">
                  <div style="font-family:var(--display);font-size:14px;color:var(--green);font-weight:700">💾 SPI Flash &amp; Write Protection</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">The chip storing UEFI firmware. Protected via hardware registers (PR0-PR4, SMM_BWP).</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer" onclick="showLearnModal('tpm')">
                  <div style="font-family:var(--display);font-size:14px;color:var(--blue);font-weight:700">🔑 TPM 2.0</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Trusted Platform Module — hardware root of trust for cryptographic operations.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
              </div>
            </div>
            <div>
              <div class="result-pane-title">Threat Landscape</div>
              <div class="stack-col" style="gap:8px">
                <div class="result-pane" style="cursor:pointer;border-left:3px solid var(--red)" onclick="showLearnModal('bootkits')">
                  <div style="font-family:var(--display);font-size:13px;color:var(--red);font-weight:700">☠ UEFI Bootkits</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Malware that survives OS reinstalls. Examples: BlackLotus, CosmicStrand, MosaicRegressor.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer;border-left:3px solid var(--purple)" onclick="showLearnModal('smmrootkit')">
                  <div style="font-family:var(--display);font-size:13px;color:var(--purple);font-weight:700">👻 SMM Rootkits</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Firmware rootkits in SMM space. Highest privilege, invisible to OS and hypervisors.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer;border-left:3px solid var(--amber)" onclick="showLearnModal('supplychain')">
                  <div style="font-family:var(--display);font-size:13px;color:var(--amber);font-weight:700">🏭 Supply Chain Attacks</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Compromise firmware at manufacturing stage. Extremely difficult to detect.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
                <div class="result-pane" style="cursor:pointer;border-left:3px solid var(--cyan)" onclick="showLearnModal('chipsec')">
                  <div style="font-family:var(--display);font-size:13px;color:var(--cyan);font-weight:700">🛡 CHIPSEC Tool</div>
                  <div style="font-size:11px;color:var(--text-muted);margin-top:4px">Intel's open-source platform security assessment framework. Tests firmware config.</div>
                  <div style="font-size:10px;color:var(--blue);margin-top:8px">→ Click to learn more</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /content -->
</div><!-- /main -->
</div><!-- /app -->

<!-- ── LEARNING MODAL ── -->
<div class="modal-overlay" id="learnModal" onclick="closeModal(event)">
  <div class="modal-panel" id="learnModalPanel">
    <button class="modal-close" onclick="closeLearnModal()">✕ Close</button>
    <div id="learnModalContent"></div>
  </div>
</div>

<div id="toastContainer" class="toast-container"></div>"""

# ══════════════════════════════════════════════════════════════════════════════
# JavaScript — Modular Smart Simulation Engine
# ══════════════════════════════════════════════════════════════════════════════
JS = r"""
// ═══════════════════════════════════════════════════════════════
// MODULE: SimConfig — Constants & Utilities
// ═══════════════════════════════════════════════════════════════
console.log('BIOS/UEFI Smart Simulation Engine v2.0 loaded');
window.addEventListener('error', e => console.error('JS Error:', e.message, e.filename + ':' + e.lineno));
window.addEventListener('unhandledrejection', e => console.error('Promise rejection:', e.reason));

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Generate a realistic-looking random hex string
function randHex(len) {
  return Array.from({length: len}, () => Math.floor(Math.random()*256).toString(16).padStart(2,'0')).join(' ');
}
function randHash(len = 32) {
  return Array.from({length: len}, () => Math.floor(Math.random()*256).toString(16).padStart(2,'0')).join('');
}
function randVersion() {
  return `${Math.floor(Math.random()*3)+1}.${Math.floor(Math.random()*9)+1}${Math.floor(Math.random()*9)}`;
}
function randBetween(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
function pickRandom(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

// Simulate realistic timestamps
let simStartTime = Date.now();
function simTime() {
  const elapsed = (Date.now() - simStartTime) / 1000;
  return `[ ${elapsed.toFixed(6).padStart(10)} ]`;
}

// ═══════════════════════════════════════════════════════════════
// MODULE: Scenarios — 4 Distinct Security Scenario Definitions
// ═══════════════════════════════════════════════════════════════
const SCENARIOS = {

  secure: {
    id: 'secure',
    label: '✅ Secure System',
    badgeClass: 'secure',
    description: 'Fully hardened UEFI system with all security features active.',

    // Boot behavior
    bootErrors: [],
    biosMode: 'UEFI + Secure Boot',
    secureBoot: true,
    tpmActive: true,

    // Risk scoring
    score: 96,
    riskLevel: 'low',
    riskLabel: 'LOW RISK',
    critCount: 0, medCount: 0, secCount: 7,

    // CHIPSEC results per module (true = PASSED, false = FAILED, 'warn' = WARNING)
    chipsec: {
      bios_wp: true,
      secureboot: true,
      spi: true,
      smm: true,
      smm_bwp: true,
      tpm: true,
    },

    // Bar chart values (0-100)
    riskBars: { smm: 95, bwp: 95, spi: 98, sb: 100, smram: 90, tpm: 100 },
    riskBarColors: { smm:'green-b', bwp:'green-b', spi:'green-b', sb:'green-b', smram:'green-b', tpm:'green-b' },

    // Vulnerability findings
    vulns: [
      { sev:'low', title:'Secure Boot: ENABLED', desc:'Platform Key (PK) installed. KEK and db/dbx databases populated and valid. All signatures verified.', rec:'→ No action required. Keep databases updated via firmware update mechanism.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'SMM_BWP Bit: SET', desc:'SMM-based BIOS write protection is active. Firmware modifications from SMM context are blocked.', rec:'→ No action required. Verify bit on each firmware update.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'SPI Protected Ranges: CONFIGURED', desc:'PR0–PR3 ranges are configured. BIOS region is write-protected at hardware level.', rec:'→ No action required. Periodically audit PR configuration.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'SMRAM Locked', desc:'SMRAM closed and locked. D_LCK=1, G_SMRAME=1. No unauthorized SMM access possible.', rec:'→ No action required.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'TPM 2.0 Active + Measured Boot', desc:'Infineon SLB 9670 active. PCR0-7 populated. Measured boot chain verified. BitLocker enabled.', rec:'→ No action required. Monitor PCR drift.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'Intel Boot Guard: ENABLED', desc:'Boot Guard OBB measurement verified. ACM (Authenticated Code Module) validated.', rec:'→ No action required. Do not reflash without Boot Guard key.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'Flash Descriptor Locked', desc:'FLOCKDN=1. Flash descriptor, ME region, and BIOS region permissions locked at boot.', rec:'→ No action required.', cves:[], impact:{conf:0,integ:0,avail:0} },
    ],

    actionItems: [
      { color: 'lg', text: '✓ No immediate action required' },
      { color: 'lg', text: '✓ Schedule routine firmware update review quarterly' },
      { color: 'lg', text: '✓ Monitor Secure Boot database for revoked certificates' },
      { color: 'lg', text: '✓ Audit TPM PCR values against known-good baseline' },
      { color: 'lg', text: '✓ Maintain Boot Guard key security and escrow' },
    ],

    dashSummary: {
      boot: '<span class="lg">✓ POST: PASS</span>\n<span class="lg">✓ MBR: VALID</span>\n<span class="lg">✓ UEFI Secure Boot ACTIVE</span>',
      chip: '<span class="lg">✓ bios_wp: PASSED</span>\n<span class="lg">✓ secureboot: PASSED</span>\n<span class="lg">✓ spi: PASSED</span>\n<span class="lg">✓ smm: PASSED</span>',
      vuln: '<span class="lg">✓ 0 Critical findings</span>\n<span class="lg">✓ 0 Medium findings</span>\n<span class="lg">✓ 7 Secure features</span>\n<span class="lg">Score: 96/100</span>',
    },

    // Terminal outputs override (scenario-aware)
    terminalOverrides: {
      'mokutil --sb-state': [['SecureBoot enabled', 'lg'],['Platform Key (PK) enrolled', 'lg']],
      'cat /sys/firmware/efi/efivars/SecureBoot-*': [['0x01 — Secure Boot ENABLED', 'lg']],
    },
  },

  misconfigured: {
    id: 'misconfigured',
    label: '⚠️ Misconfigured',
    badgeClass: 'misconfigured',
    description: 'Partially secured system with some misconfigured security settings.',

    bootErrors: ['[WARN] SMM_BWP bit not set — BIOS region partially exposed'],
    biosMode: 'UEFI + Secure Boot',
    secureBoot: true,
    tpmActive: true,

    score: 63,
    riskLevel: 'medium',
    riskLabel: 'MEDIUM RISK',
    critCount: 1, medCount: 2, secCount: 4,

    chipsec: { bios_wp: false, secureboot: true, spi: 'warn', smm: 'warn', smm_bwp: false, tpm: true },

    riskBars: { smm: 45, bwp: 20, spi: 55, sb: 95, smram: 75, tpm: 90 },
    riskBarColors: { smm:'amber-b', bwp:'red-b', spi:'amber-b', sb:'green-b', smram:'amber-b', tpm:'green-b' },

    vulns: [
      { sev:'high', title:'SMM_BWP Not Set', desc:'SMM-based BIOS write protection bit is disabled. Privileged code in SMM context can modify firmware without restriction. This is a well-known attack vector.', rec:'→ Enable SMM_BWP in BIOS configuration; update to latest BIOS firmware.', cves:['CVE-2019-11098','CVE-2020-3704'], impact:{conf:3,integ:9,avail:3} },
      { sev:'medium', title:'SPI Protected Ranges Unconfigured', desc:'PR0–PR4 registers not configured. While FLOCKDN is set, the BIOS region can still be overwritten by privileged OS code via SPI commands.', rec:'→ Configure SPI Protected Ranges PR0–PR4 via BIOS update. Enable Intel Boot Guard.', cves:['CVE-2017-5703'], impact:{conf:2,integ:7,avail:2} },
      { sev:'medium', title:'SMI Lock Unavailable', desc:'System Management Interrupt lock not implemented on this platform revision. Attacker could register malicious SMI handlers if SMM memory is compromised.', rec:'→ Review SMM code surface area. Consider hardware upgrade for full mitigation.', cves:[], impact:{conf:2,integ:6,avail:2} },
      { sev:'low', title:'Secure Boot: ENABLED', desc:'Platform Key (PK) installed. KEK and db/dbx populated. Image verification active.', rec:'→ Keep Secure Boot databases current through firmware updates.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'Flash Descriptor Locked', desc:'FLOCKDN bit set. Flash descriptor protected. Configuration locked at boot.', rec:'→ No action required.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'SMRAM Locked', desc:'SMRAM closed and locked. D_LCK=1, G_SMRAME=1. Global SMRAM protection active.', rec:'→ No action required.', cves:[], impact:{conf:0,integ:0,avail:0} },
      { sev:'low', title:'TPM 2.0 Functional', desc:'Infineon SLB 9670 active. Measured boot available. PCR values populated.', rec:'→ Configure PCR policies for OS integrity checking.', cves:[], impact:{conf:0,integ:0,avail:0} },
    ],

    actionItems: [
      { color: 'lr', text: '1. ⚠ Enable SMM_BWP bit in BIOS settings (Critical)' },
      { color: 'la', text: '2. ⚠ Configure SPI Protected Ranges PR0–PR4' },
      { color: 'la', text: '3. ⚠ Update BIOS to obtain SMM lock support' },
      { color: 'lg', text: '4. ✓ Maintain Secure Boot database integrity' },
      { color: 'lg', text: '5. ✓ Enable TPM-based Measured Boot policies' },
    ],

    dashSummary: {
      boot: '<span class="lg">✓ POST: PASS</span>\n<span class="lg">✓ MBR: VALID</span>\n<span class="la">⚠ SMM_BWP Warning</span>',
      chip: '<span class="lr">✗ bios_wp: FAILED</span>\n<span class="lg">✓ secureboot: PASSED</span>\n<span class="la">⚠ spi: WARNING</span>\n<span class="la">⚠ smm: WARNING</span>',
      vuln: '<span class="lr">✗ 1 Critical finding</span>\n<span class="la">⚠ 2 Medium findings</span>\n<span class="lg">✓ 4 Secure features</span>\n<span class="la">Score: 63/100</span>',
    },

    terminalOverrides: {
      'mokutil --sb-state': [['SecureBoot enabled', 'lg']],
    },
  },

  vulnerable: {
    id: 'vulnerable',
    label: '🔓 Vulnerable System',
    badgeClass: 'vulnerable',
    description: 'Multiple critical security misconfigurations detected. High exploitation risk.',

    bootErrors: [
      '[WARN] Secure Boot is DISABLED',
      '[WARN] SMM_BWP not set — BIOS region unprotected',
      '[WARN] Boot Guard not active — no hardware root of trust',
      '[ERROR] TPM not responding on LPC bus',
    ],
    biosMode: 'UEFI (No Secure Boot)',
    secureBoot: false,
    tpmActive: false,

    score: 28,
    riskLevel: 'high',
    riskLabel: 'HIGH RISK',
    critCount: 3, medCount: 2, secCount: 2,

    chipsec: { bios_wp: false, secureboot: false, spi: false, smm: 'warn', smm_bwp: false, tpm: false },

    riskBars: { smm: 15, bwp: 5, spi: 10, sb: 0, smram: 60, tpm: 0 },
    riskBarColors: { smm:'red-b', bwp:'red-b', spi:'red-b', sb:'red-b', smram:'amber-b', tpm:'red-b' },

    vulns: [
      { sev:'high', title:'Secure Boot: DISABLED', desc:'No image signature verification at boot. Any unsigned or tampered bootloader will execute without restriction. Critical attack vector for bootkit installation.', rec:'→ Enable Secure Boot in UEFI setup. Enroll Platform Key (PK) and configure KEK/db/dbx databases.', cves:['CVE-2022-21894','CVE-2022-34301'], impact:{conf:9,integ:9,avail:7} },
      { sev:'high', title:'SMM_BWP Not Set + SPI Unprotected', desc:'Both hardware-based BIOS write protections are disabled. An attacker with Ring-0 access can overwrite UEFI firmware via direct SPI flash commands. Enables persistent rootkit installation.', rec:'→ Enable SMM_BWP bit. Configure SPI Protected Ranges PR0–PR4. Enable Intel Boot Guard.', cves:['CVE-2019-11098','CVE-2017-5703','CVE-2021-33164'], impact:{conf:9,integ:9,avail:9} },
      { sev:'high', title:'Boot Guard: NOT ACTIVE', desc:'Intel Boot Guard hardware root of trust is not provisioned. No authenticated code module (ACM) verification occurs. First instruction of firmware is unverified.', rec:'→ Provision Boot Guard in manufacturing phase. Not configurable post-deployment.', cves:['CVE-2022-26343'], impact:{conf:7,integ:9,avail:5} },
      { sev:'medium', title:'TPM 2.0 Not Responding', desc:'TPM chip not detected on LPC bus. Measured boot chain broken. Platform integrity attestation unavailable. BitLocker and similar protections non-functional.', rec:'→ Check TPM physical presence. Ensure TPM enabled in BIOS. Re-provision if hardware fault.', cves:[], impact:{conf:5,integ:5,avail:3} },
      { sev:'medium', title:'SMI Lock Unavailable', desc:'Platform does not support SMI locking. Combined with unprotected BIOS region, this represents a compounding risk for SMM-based attacks.', rec:'→ Platform replacement recommended for high-security environments.', cves:[], impact:{conf:4,integ:7,avail:3} },
      { sev:'low', title:'SMRAM Locked (Partial)', desc:'SMRAM D_LCK bit is set but G_SMRAME protection is not fully effective given other misconfigurations.', rec:'→ SMRAM lock is necessary but insufficient without other protections.', cves:[], impact:{conf:0,integ:2,avail:0} },
      { sev:'low', title:'Flash Descriptor Locked', desc:'FLOCKDN is set. Flash descriptor region is locked.', rec:'→ Insufficient alone without PR or SMM_BWP protection.', cves:[], impact:{conf:0,integ:0,avail:0} },
    ],

    actionItems: [
      { color: 'lr', text: '1. 🔴 ENABLE SECURE BOOT IMMEDIATELY (Critical)' },
      { color: 'lr', text: '2. 🔴 Enable SMM_BWP and configure SPI PR0–PR4' },
      { color: 'lr', text: '3. 🔴 Investigate Boot Guard provisioning status' },
      { color: 'la', text: '4. ⚠ Diagnose and restore TPM functionality' },
      { color: 'la', text: '5. ⚠ Apply all available BIOS vendor security patches' },
    ],

    dashSummary: {
      boot: '<span class="lr">✗ POST: WARNING</span>\n<span class="lr">✗ Secure Boot: DISABLED</span>\n<span class="lr">✗ Boot Guard: INACTIVE</span>',
      chip: '<span class="lr">✗ bios_wp: FAILED</span>\n<span class="lr">✗ secureboot: FAILED</span>\n<span class="lr">✗ spi: FAILED</span>\n<span class="la">⚠ smm: WARNING</span>',
      vuln: '<span class="lr">✗ 3 Critical findings</span>\n<span class="la">⚠ 2 Medium findings</span>\n<span class="la">Score: 28/100</span>',
    },

    terminalOverrides: {
      'mokutil --sb-state': [['SecureBoot disabled', 'lr'],['Platform is in SETUP MODE', 'lr']],
      'tpm2_getcap properties-fixed': [['Error: could not connect to tpm', 'lr'],['tcti initialization failed (0x000A0013)', 'lr']],
    },
  },

  attacked: {
    id: 'attacked',
    label: '☠️ Under Attack',
    badgeClass: 'attacked',
    description: 'ACTIVE ATTACK DETECTED. Firmware tampering in progress. System critically compromised.',

    bootErrors: [
      '[CRITICAL] Firmware hash mismatch — TAMPERING DETECTED',
      '[CRITICAL] Secure Boot enforcement bypassed via vulnerability CVE-2022-21894',
      '[CRITICAL] Unknown SMM module injected at address 0x7B000000',
      '[ERROR] TPM PCR values do not match baseline — CHAIN OF TRUST BROKEN',
      '[ALERT] Rootkit signature detected in BIOS region offset 0x005E0000',
      '[ALERT] Bootkit dropper found in MBR sector 0',
    ],
    biosMode: 'COMPROMISED',
    secureBoot: false,
    tpmActive: false,

    score: 8,
    riskLevel: 'critical',
    riskLabel: 'CRITICAL',
    critCount: 5, medCount: 1, secCount: 1,

    chipsec: { bios_wp: false, secureboot: false, spi: false, smm: false, smm_bwp: false, tpm: false },

    riskBars: { smm: 3, bwp: 0, spi: 0, sb: 0, smram: 10, tpm: 0 },
    riskBarColors: { smm:'red-b', bwp:'red-b', spi:'red-b', sb:'red-b', smram:'red-b', tpm:'red-b' },

    vulns: [
      { sev:'critical', title:'☠ ACTIVE FIRMWARE ROOTKIT DETECTED', desc:'CHIPSEC detected unauthorized code at BIOS region offset 0x5E0000. Hash: see firmware tab. Rootkit survives OS reinstall and disk wipe. Consistent with MosaicRegressor/CosmicStrand methodology.', rec:'→ IMMEDIATE: Power off system. Reflash BIOS from known-good source. Verify with Boot Guard. Escalate to IR team.', cves:['CVE-2022-21894','CVE-2022-34303'], impact:{conf:10,integ:10,avail:10} },
      { sev:'critical', title:'☠ Secure Boot Bypass (CVE-2022-21894)', desc:'BlackLotus-style exploit used to bypass Secure Boot enforcement. Bootkit installed in EFI System Partition. Shim vulnerability exploited. All subsequent boot measurements are compromised.', rec:'→ Revoke affected UEFI certificates via dbx update (KB5025885). Patch and reflash.', cves:['CVE-2022-21894','CVE-2022-34301'], impact:{conf:10,integ:10,avail:7} },
      { sev:'critical', title:'☠ SMM Module Injection', desc:'Unauthorized SMM handler registered at 0x7B000000. Code executes in Ring -2 context. Invisible to OS, hypervisors, and AV solutions. Provides persistent stealth backdoor.', rec:'→ Hardware reflash required. SMM code cannot be removed by OS-level tools.', cves:['CVE-2021-33164','CVE-2019-11098'], impact:{conf:10,integ:10,avail:9} },
      { sev:'critical', title:'☠ TPM PCR Tampering', desc:'PCR0 (BIOS measurement), PCR4 (MBR), and PCR7 (Secure Boot policy) values do not match established baseline. Chain of trust completely broken. Attestation is meaningless.', rec:'→ TPM clear required. New baseline must be established from clean hardware only.', cves:[], impact:{conf:9,integ:9,avail:7} },
      { sev:'critical', title:'☠ Bootkit in MBR (Sector 0)', desc:'MBR has been overwritten with bootkit dropper code. Hash: does not match vendor signature. Executes before OS bootloader, loads rootkit components. Persistent across OS reinstalls.', rec:'→ Wipe MBR with dd if=/dev/zero. Reinitialize GPT. Reflash BIOS. Verify hardware integrity.', cves:[], impact:{conf:9,integ:10,avail:8} },
      { sev:'medium', title:'BIOS Flash Fully Writable', desc:'All hardware write protections disabled to facilitate rootkit installation. Both SMM_BWP and SPI PR ranges cleared by attack.', rec:'→ Restore BIOS write protections after complete remediation.', cves:[], impact:{conf:3,integ:9,avail:3} },
      { sev:'low', title:'Flash Descriptor: Partially Readable', desc:'Flash descriptor region can be read but has been modified. Permissions may have been altered by attacker tooling.', rec:'→ Verify descriptor integrity against vendor reference.', cves:[], impact:{conf:2,integ:3,avail:0} },
    ],

    actionItems: [
      { color: 'lp', text: '☠ EMERGENCY: Power off and isolate system NOW' },
      { color: 'lr', text: '1. INCIDENT RESPONSE: Notify security team immediately' },
      { color: 'lr', text: '2. Forensic image all storage before any changes' },
      { color: 'lr', text: '3. Reflash BIOS from vendor-signed image on clean media' },
      { color: 'lr', text: '4. Apply KB5025885 dbx update to prevent re-infection' },
      { color: 'la', text: '5. Re-establish TPM baseline from verified clean state' },
    ],

    dashSummary: {
      boot: '<span class="lp">☠ FIRMWARE TAMPERED</span>\n<span class="lr">✗ Bootkit in MBR</span>\n<span class="lr">✗ Secure Boot BYPASSED</span>',
      chip: '<span class="lp">☠ ALL CHECKS FAILED</span>\n<span class="lr">✗ SMM ROOTKIT FOUND</span>\n<span class="lr">✗ SYSTEM COMPROMISED</span>',
      vuln: '<span class="lp">☠ 5 CRITICAL FINDINGS</span>\n<span class="lr">✗ Active compromise</span>\n<span class="lp">Score: 8/100</span>',
    },

    terminalOverrides: {
      'mokutil --sb-state': [['SecureBoot disabled', 'lr'],['WARNING: Secure Boot bypass detected', 'lp'],['System may be compromised', 'lp']],
      'tpm2_getcap properties-fixed': [['Error: TPM attestation failure', 'lr'],['PCR mismatch — chain of trust broken', 'lp']],
      'hexdump firmware.bin | head': [
        ['00000000  d9 54 93 7a 68 04 4a 44  bc 81 f3 89 f3 82 6b 95  |.T.zh.JD......k.|', 'la'],
        ['00001000  4d 5a 90 00 03 00 00 00  04 00 00 00 ff ff 00 00  |MZ..............  ← BOOTKIT|', 'lr'],
        ['005E0000  52 4f 4f 54 4b 49 54 20  53 49 47 4e 41 54 55 52  |ROOTKIT SIGNATUR|', 'lp'],
        ['005E0010  45 20 44 45 54 45 43 54  45 44 20 21 21 21 00 00  |E DETECTED !!!..|', 'lp'],
      ],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// MODULE: SimState — Shared mutable state
// ═══════════════════════════════════════════════════════════════
const SimState = {
  isRunning: false,
  currentScenario: null,    // reference to active SCENARIOS entry
  cmdHistory: [],
  histIdx: -1,
  gtHistory: [],
};

// ═══════════════════════════════════════════════════════════════
// MODULE: RiskScorer — Dynamic risk scoring logic
// ═══════════════════════════════════════════════════════════════
const RiskScorer = {
  // Calculate score from scenario config
  calculate(scenario) {
    let score = 100;
    const c = scenario.chipsec;
    if (c.bios_wp !== true)     score -= 30;
    if (c.secureboot !== true)  score -= 25;
    if (c.spi !== true)         score -= 15;
    if (c.smm !== true && c.smm !== false) score -= 8;   // warn
    if (c.smm === false)        score -= 12;
    if (c.smm_bwp !== true)     score -= 10;
    if (c.tpm !== true)         score -= 8;
    // Extra penalty for attack scenarios
    if (scenario.id === 'attacked') score = Math.min(score, 10);
    return Math.max(0, Math.min(100, scenario.score)); // use scenario's pre-set score
  },

  // Get arc stroke-dashoffset for SVG ring (201 = full circle)
  scoreToArc(score) { return 201 - (201 * score / 100); },

  // Get arc color based on score
  scoreToColor(score) {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#f59e0b';
    if (score >= 30) return '#ef4444';
    return '#a855f7';
  },

  // Update all score UI elements
  updateUI(scenario) {
    const score = this.calculate(scenario);
    const arc = document.getElementById('scoreArc');
    const scoreValEl = document.getElementById('scoreVal');
    const riskBadge = document.getElementById('riskLevelBadge');
    const dashScore = document.getElementById('dash-score');
    const dashRisk = document.getElementById('dash-risk');

    if (arc) {
      arc.style.strokeDashoffset = this.scoreToArc(score);
      arc.style.stroke = this.scoreToColor(score);
    }
    if (scoreValEl) scoreValEl.textContent = score;
    if (riskBadge) {
      riskBadge.textContent = scenario.riskLabel;
      riskBadge.className = 'risk-level-badge ' + scenario.riskLevel;
    }
    if (dashScore) {
      dashScore.textContent = score + '/100';
      dashScore.style.color = this.scoreToColor(score);
    }
    if (dashRisk) {
      dashRisk.textContent = scenario.riskLabel;
      dashRisk.style.color = this.scoreToColor(score);
    }

    // Score bars
    const total = scenario.critCount + scenario.medCount + scenario.secCount || 1;
    const sb_crit = document.getElementById('sb-crit');
    const sv_crit = document.getElementById('sv-crit');
    const sb_med  = document.getElementById('sb-med');
    const sv_med  = document.getElementById('sv-med');
    const sb_sec  = document.getElementById('sb-sec');
    const sv_sec  = document.getElementById('sv-sec');
    if (sb_crit) sb_crit.style.width = Math.round((scenario.critCount/total)*100) + '%';
    if (sv_crit) sv_crit.textContent = scenario.critCount;
    if (sb_med)  sb_med.style.width  = Math.round((scenario.medCount/total)*100) + '%';
    if (sv_med)  sv_med.textContent  = scenario.medCount;
    if (sb_sec)  sb_sec.style.width  = Math.round((scenario.secCount/total)*100) + '%';
    if (sv_sec)  sv_sec.textContent  = scenario.secCount;
  }
};

// ═══════════════════════════════════════════════════════════════
// MODULE: UI — Tabs, toasts, general utilities
// ═══════════════════════════════════════════════════════════════
function showTab(name, btn, phase) {
  document.querySelectorAll('[id^="tab-"]').forEach(el => el.style.display = 'none');
  const tab = document.getElementById('tab-' + name);
  if (!tab) return;
  tab.style.display = '';

  let activeBtn = btn;
  if (!activeBtn) activeBtn = document.querySelector(`.nav-tab[data-tab="${name}"]`);
  if (activeBtn) {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    activeBtn.classList.add('active');
  }

  const defaultPhase = { dashboard:1, bios:1, uefi:3, security:4, firmware:5, findings:6 }[name];
  const targetPhase = phase || defaultPhase;
  if (targetPhase) {
    document.querySelectorAll('.phase-item').forEach(item => item.classList.remove('active'));
    const ai = document.getElementById('si-' + targetPhase);
    if (ai) ai.classList.add('active');
  }
}

function appendLog(id, text, cls = '') {
  const el = document.getElementById(id);
  if (!el) return;
  const span = document.createElement('span');
  span.className = cls + ' type-in';
  span.textContent = text;
  el.appendChild(span);
  el.appendChild(document.createTextNode('\n'));
  el.scrollTop = el.scrollHeight;
}

function setLog(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

function setEl(id, text, cls) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text;
  if (cls !== undefined) el.className = cls;
}

function setProgress(id, pctId, pct) {
  const pfEl = document.getElementById(id);
  const ppEl = document.getElementById(pctId);
  if (pfEl) pfEl.style.width = pct + '%';
  if (ppEl) ppEl.textContent = pct + '%';
}

function tlDone(n, time, isErr = false) {
  const dot = document.getElementById('tl-' + n);
  const s = document.getElementById('tl-' + n + '-s');
  if (dot) dot.style.background = isErr ? 'var(--red)' : 'var(--green)';
  if (s) { s.textContent = time; s.className = isErr ? 'lr' : 'lg'; }
}

function phaseStatus(n, text, cls = '') {
  const el = document.getElementById('ss-' + n);
  if (el) { el.textContent = text; el.className = 'phase-status ' + cls; }
  const item = document.getElementById('si-' + n);
  const num  = document.getElementById('sn-' + n);
  if (item && num) {
    const af = item.classList.contains('active') ? 'active' : '';
    const sf = cls === 'ok' ? 'done' : cls === 'warn' ? 'warn' : cls === 'err' ? 'err' : '';
    item.className = ['phase-item', af, sf].filter(Boolean).join(' ');
    num.textContent = n;
  }
}

function globalBar(pct, style = '') {
  const el = document.getElementById('globalProgress');
  if (!el) return;
  el.style.width = pct + '%';
  el.className = 'loading-bar' + (style ? ' ' + style : '');
}

function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  const titleMap = { info:'Notice', error:'Warning', warn:'Caution', success:'Success', critical:'⚠ CRITICAL ALERT' };
  toast.className = 'toast toast--' + type;
  toast.innerHTML = `<div class="toast-title">${titleMap[type]||'Notice'}</div><div class="toast-text">${message}</div>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('toast-hide');
    toast.addEventListener('animationend', () => toast.remove());
  }, duration);
}

// Update the scenario badge in header
function updateScenarioBadge(scenario) {
  const badge = document.getElementById('scenarioBadge');
  if (!badge) return;
  badge.textContent = '⚙ Scenario: ' + scenario.id.toUpperCase();
  badge.className = 'scenario-badge ' + scenario.badgeClass;
}

// Attack warning bar
function setAttackBar(visible) {
  const bar = document.getElementById('attackBar');
  if (bar) bar.className = 'attack-warning-bar' + (visible ? ' show' : '');
}

// Change scenario selection
function changeScenario(val) {
  if (val === 'random') return;
  const scenario = SCENARIOS[val];
  if (scenario) {
    SimState.currentScenario = scenario;
    updateScenarioBadge(scenario);
    showToast(`Scenario set: ${scenario.label} — ${scenario.description}`, 'info', 4000);
  }
}

// Resolve scenario (pick random if needed)
function resolveScenario() {
  const sel = document.getElementById('scenarioSelect');
  const val = sel ? sel.value : 'random';
  if (val === 'random') {
    const keys = Object.keys(SCENARIOS);
    const picked = keys[Math.floor(Math.random() * keys.length)];
    SimState.currentScenario = SCENARIOS[picked];
  } else {
    SimState.currentScenario = SCENARIOS[val] || SCENARIOS.misconfigured;
  }
  updateScenarioBadge(SimState.currentScenario);
  return SimState.currentScenario;
}

// ═══════════════════════════════════════════════════════════════
// MODULE: BootEngine — Phase simulation runners
// ═══════════════════════════════════════════════════════════════

// Phase 1: System Power-On
async function phase1(scenario) {
  setLog('log-p1', '');
  phaseStatus(1, 'Running…');
  document.getElementById('globalDot').className = 'status-dot active';
  setEl('globalStatus', 'RUNNING');
  simStartTime = Date.now();

  const log = (t, c) => { appendLog('log-p1', t, c); return sleep(100); };
  const fw = randHash(8); // fake firmware version hash

  await log(`$ echo "Power button pressed — boot sequence initiated"`, 'lc');
  await sleep(randBetween(200, 400)); // simulate realistic boot delay

  await log(`[${simTime()}] Power supply: 12V OK, 5V OK, 3.3V OK`, 'lg');
  setProgress('pf-psu', 'pp-psu', 100);
  await sleep(150);

  await log(`[${simTime()}] Voltage stabilized — rails nominal`, 'lg');
  await log(`[${simTime()}] Motherboard POST start signal received`, 'lg');
  await sleep(randBetween(200, 350));

  await log(`$ dmesg | grep -i cpu`, 'lc');
  await log(`[${simTime()}] CPU 0: Intel(R) Core(TM) i7-11700K @ 3.60GHz`, 'lg');
  await log(`[${simTime()}] CPU cores: 8 physical, 16 logical (HT enabled)`, 'lg');
  await log(`[${simTime()}] CPU features: SSE4.2 AVX2 AES-NI VMX TXT SGX`, 'lg');
  setProgress('pf-cpu', 'pp-cpu', 100);
  setEl('hw-cpu', 'OK', 'hw-val ok');
  await sleep(200);

  // Inject random minor error for realism
  if (Math.random() > 0.6) {
    await log(`[${simTime()}] ACPI: DSDT table minor checksum warning — non-fatal`, 'la');
  }

  await log(`$ dmidecode -t memory`, 'lc');
  await log(`[${simTime()}] DIMM 0: 8192 MB DDR4 @ 3200 MHz — Samsung`, 'lg');
  await log(`[${simTime()}] DIMM 1: 8192 MB DDR4 @ 3200 MHz — Samsung`, 'lg');
  await log(`[${simTime()}] Total Memory: 16 GB — ECC disabled`, 'lg');
  await log(`[${simTime()}] Memory Test: PASSED ✓`, 'lg');
  setProgress('pf-ram', 'pp-ram', 100);
  setEl('hw-ram', 'OK', 'hw-val ok');
  await sleep(200);

  await log(`$ lspci | head -6`, 'lc');
  await log(`[${simTime()}] PCI device: Intel C620 PCH — host bridge`, 'lg');
  await log(`[${simTime()}] PCI device: WDC WD10EZEX-60M2NA0 1TB`, 'lg');
  await log(`[${simTime()}] PCI device: VGA controller detected`, 'lg');
  setProgress('pf-dev', 'pp-dev', 100);
  setEl('hw-disk', 'OK', 'hw-val ok');
  setEl('hw-psu', 'OK', 'hw-val ok');
  setEl('hw-gpu', 'OK', 'hw-val ok');
  await sleep(200);

  await log(`$ tpm2_getcap properties-fixed | head`, 'lc');
  if (scenario.tpmActive) {
    await log(`[${simTime()}] TPM 2.0 detected — Infineon SLB 9670`, 'lg');
    await log(`[${simTime()}] TPM Active, firmware 7.85.${randBetween(4000,5000)}.0`, 'lg');
    setEl('hw-tpm', 'OK', 'hw-val ok');
  } else {
    await log(`[${simTime()}] TPM: ERROR — device not responding on LPC bus`, 'lr');
    await log(`[${simTime()}] TPM attestation unavailable`, 'lr');
    setEl('hw-tpm', 'ERR', 'hw-val err');
    showToast('TPM not detected — platform integrity attestation unavailable', 'warn');
  }
  await sleep(250);

  // Inject scenario-specific boot errors
  for (const errMsg of scenario.bootErrors) {
    const cls = errMsg.startsWith('[CRITICAL]') ? 'lp' : errMsg.startsWith('[ERROR]') ? 'lr' : errMsg.startsWith('[ALERT]') ? 'lp' : 'la';
    await log(`[${simTime()}] ${errMsg}`, cls);
    await sleep(80);
  }

  if (scenario.bootErrors.length > 0) {
    showToast(`${scenario.bootErrors.length} boot warning(s) detected — review logs`, 'warn');
  }

  await log(`[${simTime()}] Firmware initialization complete — hash: 0x${fw}`, scenario.secureBoot ? 'lg' : 'la');
  await log(`[${simTime()}] Handing control to bootloader...`, 'la');
  setProgress('pf-post', 'pp-post', 100);
  phaseStatus(1, 'Complete', scenario.bootErrors.length > 0 ? 'warn' : 'ok');
}

// Phase 2: BIOS Boot
async function phase2(scenario) {
  setLog('log-p2', '');
  phaseStatus(2, 'Running…');

  const log = (t, c) => { appendLog('log-p2', t, c); return sleep(110); };

  await log(`$ bochs -q -f bios-config.bxrc`, 'lc');
  await log(`Bochs x86 Emulator v2.7 — Copyright 2001-2021`, 'lb');
  await log(`Starting BIOS boot sequence...`, 'la');
  await sleep(randBetween(250, 400));

  await log(`[BIOS] Power-On Self Test (POST) initiated`, 'la');
  tlDone(1, `${(Math.random()*0.1).toFixed(2)}s`);
  await log(`[BIOS] Testing CPU registers... OK`, 'lg');
  await log(`[BIOS] Testing interrupt controller... OK`, 'lg');
  await log(`[BIOS] Testing RAM 16384 KB... PASS`, 'lg');
  await log(`[BIOS] Testing keyboard controller... OK`, 'lg');
  await log(`[BIOS] Testing VGA adapter... OK`, 'lg');
  tlDone(2, `0.${randBetween(20,28)}s`);
  await sleep(200);

  await log(`[BIOS] Detecting storage devices...`, 'la');
  await log(`[BIOS] Primary Master: WDC WD10EZEX-60M2NA0 (1TB HDD)`, 'lg');
  await log(`[BIOS] Secondary Master: None detected`, 'lm');
  await sleep(150);

  await log(`[BIOS] Reading Master Boot Record at sector 0...`, 'la');
  if (scenario.id === 'attacked') {
    await log(`[BIOS] Loading MBR into memory at 0x7C00`, 'lb');
    await log(`[BIOS] MBR signature: 0x55AA — VALID (but content TAMPERED)`, 'lr');
    await log(`[BIOS] WARNING: MBR hash does not match vendor baseline!`, 'lp');
    tlDone(3, `0.${randBetween(40,45)}s`, true);
  } else {
    await log(`[BIOS] Loading MBR into memory at 0x7C00`, 'lb');
    await log(`[BIOS] MBR signature: 0x55AA — VALID ✓`, 'lg');
    tlDone(3, `0.${randBetween(38,45)}s`);
  }
  await sleep(150);

  await log(`[BIOS] Verifying bootloader signature...`, 'la');
  if (scenario.secureBoot) {
    await log(`[BIOS] GRUB2 MBR detected (v2.06) — signature VALID`, 'lg');
  } else {
    await log(`[BIOS] GRUB2 MBR detected (v2.06) — NO SIGNATURE CHECK`, 'la');
  }
  await log(`[BIOS] Partition table: GPT hybrid detected`, 'la');
  tlDone(4, `0.${randBetween(50,58)}s`, scenario.id === 'attacked');
  await sleep(150);

  await log(`[GRUB] Loading Stage 1.5 from sectors 1-63`, 'lb');
  await log(`[GRUB] Locating /boot/grub/grub.cfg...`, 'lb');
  await log(`[GRUB] Found Linux kernel: vmlinuz-5.15.0-91-generic`, 'lg');
  if (scenario.id === 'attacked') {
    await log(`[GRUB] WARNING: Kernel command line modified — potential bootkit`, 'lp');
  }
  await log(`[GRUB] Bootloader executing — handing off to UEFI...`, 'la');
  tlDone(5, `0.${randBetween(62,70)}s`, scenario.id === 'attacked');

  const mbrHtml = scenario.id === 'attacked'
    ? '<span class="lp">☠ MBR TAMPERED — Bootkit Detected</span><br><span class="lr">✗ Partition Table: Compromised</span><br><span class="lr">✗ GRUB2 Signature: INVALID</span><br><span class="lp">☠ Bootkit dropper executing</span>'
    : scenario.secureBoot
      ? '<span class="lg">✓ MBR Signature Valid (0x55AA)</span><br><span class="lg">✓ Partition Table: GPT</span><br><span class="lg">✓ GRUB2 v2.06 Signature Verified</span><br><span class="lg">✓ Secure Boot active</span>'
      : '<span class="lg">✓ MBR Signature Valid (0x55AA)</span><br><span class="lg">✓ Partition Table: GPT / Hybrid</span><br><span class="lg">✓ GRUB2 v2.06 Loaded</span><br><span class="la">⚠ NO Secure Boot verification</span>';
  document.getElementById('mbr-result').innerHTML = mbrHtml;

  phaseStatus(2, scenario.id === 'attacked' ? 'TAMPERED' : 'Complete',
    scenario.id === 'attacked' ? 'err' : 'ok');

  document.getElementById('dash-boot-sum').innerHTML = scenario.dashSummary.boot;
}

// Phase 3: UEFI Boot
async function phase3(scenario) {
  setLog('log-p3', '');
  phaseStatus(3, 'Running…');

  const log = (t, c) => { appendLog('log-p3', t, c); return sleep(100); };
  const uf = id => { document.getElementById(id).className = 'uefi-step active'; return sleep(350); };
  const ud = (id, err) => { document.getElementById(id).className = 'uefi-step ' + (err ? 'err' : 'done'); };

  await log(`$ qemu-system-x86_64 -bios OVMF.fd -m 4G -enable-kvm`, 'lc');
  await log(`QEMU 7.2.0 — Booting OVMF (Open Virtual Machine Firmware)`, 'lb');
  await log(`BIOS vendor: American Megatrends Int. v${randVersion()}`, 'lm');
  await sleep(200);

  // SEC Phase
  await uf('uf-sec');
  await log(`[SEC] Security Phase: CPU microcode ${randBetween(100,150)} applied`, 'lb');
  await log(`[SEC] Establishing temporary memory (CAR) at 0xFEF00000`, 'lb');
  if (scenario.id === 'attacked') {
    await log(`[SEC] WARNING: Microcode integrity check anomaly detected`, 'lp');
  }
  await log(`[SEC] Verifying firmware integrity... ${scenario.id === 'attacked' ? 'MISMATCH!' : 'OK'}`, scenario.id === 'attacked' ? 'lr' : 'lg');
  await log(`[SEC] Handing off to PEI Core`, 'lg');
  ud('uf-sec', scenario.id === 'attacked');
  await sleep(200);

  // PEI Phase
  await uf('uf-pei');
  const peiCount = randBetween(38, 48);
  await log(`[PEI] Pre-EFI Initialization Phase`, 'lb');
  await log(`[PEI] Memory Init: Training DDR4 channels at 3200 MHz...`, 'la');
  await sleep(randBetween(250, 400));
  await log(`[PEI] Memory training: ${randBetween(2100,2800)} iterations — PASS`, 'lg');
  await log(`[PEI] Loading ${peiCount} PEI modules...`, 'lb');
  await log(`[PEI] HOB (Hand-Off Block) list constructed at 0x${randHash(4)}`, 'lm');
  ud('uf-pei', false);
  setEl('dc-pei', String(peiCount));
  await sleep(200);

  // DXE Phase
  await uf('uf-dxe');
  const dxeCount = randBetween(160, 195);
  await log(`[DXE] Driver Execution Environment Phase`, 'lb');
  await log(`[DXE] Loading ${dxeCount} DXE drivers...`, 'lb');
  if (scenario.id === 'attacked') {
    await log(`[DXE] WARNING: Unknown DXE driver detected (hash mismatch)`, 'lp');
    await log(`[DXE]   Driver GUID: {${randHash(4)}-${randHash(2)}-${randHash(2)}-${randHash(2)}-${randHash(6)}}`, 'lp');
  }
  await log(`[DXE] Secure Boot DXE: ${scenario.secureBoot ? 'Loaded ✓' : 'BYPASSED ✗'}`, scenario.secureBoot ? 'lg' : 'lr');
  await log(`[DXE] TPM 2.0 DXE: ${scenario.tpmActive ? 'Loaded ✓' : 'FAILED ✗'}`, scenario.tpmActive ? 'lg' : 'lr');
  await log(`[DXE] Dispatching complete — ${dxeCount} drivers active`, 'lg');
  ud('uf-dxe', scenario.id === 'attacked');
  setEl('dc-dxe', String(dxeCount));
  setEl('dc-total', String(peiCount + dxeCount));
  await sleep(200);

  // BDS Phase
  await uf('uf-bds');
  await log(`[BDS] Boot Device Selection Phase`, 'lb');
  await log(`[BDS] Checking Secure Boot variables...`, 'la');
  const sbColor = scenario.secureBoot ? 'lg' : 'lr';
  await log(`[BDS] SecureBoot EFI var: ${scenario.secureBoot ? '0x01 — ENABLED' : '0x00 — DISABLED'}`, sbColor);
  await log(`[BDS] Processing boot order: Boot0000 → Boot0001 → Boot0002`, 'lm');
  await log(`[BDS] Loading boot manager...`, 'lb');
  ud('uf-bds', !scenario.secureBoot && scenario.id === 'attacked');
  await sleep(200);

  // OS Loader
  await uf('uf-os');
  await log(`[OS] ExitBootServices() called`, 'lb');
  await log(`[OS] Virtual address map installed`, 'lb');
  if (scenario.id === 'attacked') {
    await log(`[OS] ALERT: Rootkit module intercepted ExitBootServices()`, 'lp');
    await log(`[OS] Malicious code executing in Ring-0 context`, 'lp');
  }
  await log(`[OS] Control transferred to OS kernel`, 'lg');
  ud('uf-os', scenario.id === 'attacked');

  // Update Secure Boot badge
  const sbBadge = document.getElementById('sb-badge');
  const sbText = document.getElementById('sb-text');
  if (sbBadge && sbText) {
    if (scenario.id === 'attacked') {
      sbBadge.style.cssText = 'background:rgba(168,85,247,0.1);border-color:rgba(168,85,247,0.4);color:var(--purple)';
      sbText.textContent = 'BYPASSED — Active Attack';
    } else if (scenario.secureBoot) {
      sbBadge.style.cssText = 'background:var(--green-dim);border-color:rgba(34,197,94,0.4);color:var(--green)';
      sbText.textContent = 'ENABLED — PK/KEK/db configured';
    } else {
      sbBadge.style.cssText = 'background:var(--red-dim);border-color:rgba(239,68,68,0.4);color:var(--red)';
      sbText.textContent = 'DISABLED — No signature verification';
    }
  }

  document.getElementById('dash-sb').textContent = scenario.secureBoot ? 'ENABLED' : 'DISABLED';
  document.getElementById('dash-sb').style.color = scenario.secureBoot ? 'var(--green)' : 'var(--red)';
  document.getElementById('os-output').innerHTML = scenario.id === 'attacked'
    ? '<span class="lp">☠ Bootkit executed before kernel</span>'
    : scenario.secureBoot
      ? '<span class="lg">✓ Kernel loaded with verified signature</span><br><span class="lg">✓ Secure Boot chain intact</span>'
      : '<span class="la">⚠ Kernel loaded — no Secure Boot</span><br><span class="la">⚠ Unsigned drivers permitted</span>';

  phaseStatus(3, scenario.id === 'attacked' ? 'COMPROMISED' : 'Complete',
    scenario.id === 'attacked' ? 'err' : 'ok');
}

// Phase 4: CHIPSEC Analysis
async function phase4(scenario) {
  phaseStatus(4, 'Running…');
  const out = document.getElementById('chipOutput');
  out.innerHTML = '';

  // Helper to append to CHIPSEC output
  const chip = async (text, cls, delay = 70) => {
    const span = document.createElement('span');
    span.className = cls;
    span.textContent = text;
    out.appendChild(span);
    out.appendChild(document.createTextNode('\n'));
    out.scrollTop = out.scrollHeight;
    await sleep(delay);
  };

  await chip(`[*] CHIPSEC Platform Security Assessment Framework v1.10.6`, 'lb', 100);
  await chip(`[*] Scenario: ${scenario.label}`, 'lm', 80);
  await chip(`[*] Detecting platform: Intel Tiger Lake (i7-11700K)`, 'lb', 80);
  await chip(``, 'lm', 50);

  // Run each module
  const modules = [
    { name: 'common.bios_wp', key: 'bios_wp' },
    { name: 'common.secureboot', key: 'secureboot' },
    { name: 'common.spi', key: 'spi' },
    { name: 'common.smm', key: 'smm' },
  ];

  let passCount = 0, failCount = 0, warnCount = 0;

  for (const mod of modules) {
    await chip(`[*] Running module: ${mod.name}`, 'la', 100);
    await sleep(randBetween(200, 400));
    const result = scenario.chipsec[mod.key];
    if (result === true) {
      await chip(`[RESULT] PASSED ✓`, 'lg', 80);
      passCount++;
    } else if (result === false) {
      await chip(`[RESULT] FAILED ✗ — Security issue detected`, 'lr', 80);
      failCount++;
    } else {
      await chip(`[RESULT] WARNING — Review recommended`, 'la', 80);
      warnCount++;
    }
    await chip(``, 'lm', 40);
  }

  await chip(`[*] Analysis complete`, 'lb', 80);
  await chip(`[*] PASSED: ${passCount}  FAILED: ${failCount}  WARNING: ${warnCount}`, failCount > 0 ? 'lr' : 'lg', 80);

  // Update bar chart
  const bars = scenario.riskBars;
  const colors = scenario.riskBarColors;
  const barIds = { smm:'rc-smm', bwp:'rc-bwp', spi:'rc-spi', sb:'rc-sb', smram:'rc-smram', tpm:'rc-tpm' };
  for (const [key, id] of Object.entries(barIds)) {
    const el = document.getElementById(id);
    if (el) {
      const val = bars[key] || 0;
      const colorClass = colors[key] || 'amber-b';
      el.className = 'bar-inner ' + colorClass;
      setTimeout(() => { el.style.width = val + '%'; el.textContent = val + '%'; }, 200);
    }
  }

  // Chip summary
  document.getElementById('chip-summary').innerHTML = scenario.dashSummary.chip;
  document.getElementById('dash-chip-sum').innerHTML = scenario.dashSummary.chip;
  phaseStatus(4, failCount > 0 ? `${failCount} FAILED` : 'Complete', failCount > 0 ? 'err' : warnCount > 0 ? 'warn' : 'ok');
}

// Phase 5: Firmware Dump
async function phase5(scenario) {
  setLog('log-p5', '');
  phaseStatus(5, 'Running…');

  const log = (t, c) => { appendLog('log-p5', t, c); return sleep(100); };
  const fwHash = randHash(32);
  const fwHash2 = randHash(32);

  await log(`$ flashrom -p internal -r firmware.bin`, 'lc');
  await log(`flashrom v1.2 on Linux 5.15.0`, 'lb');
  await log(`Found chipset: Intel C620 series PCH`, 'lg');
  await log(`Found flash chip "W25Q128.V" (16384 kB, SPI) at physical address 0xFF000000`, 'lg');
  await sleep(randBetween(300, 500));
  await log(`Reading flash... ${Math.floor(Math.random()*10)+1}%`, 'la');
  await sleep(200);
  await log(`Reading flash... 47%`, 'la');
  await sleep(200);
  await log(`Reading flash... 100% — done.`, 'lg');
  await log(`Firmware dump: firmware.bin (16777216 bytes)`, 'lg');
  await log(`SHA256: ${fwHash}`, scenario.id === 'attacked' ? 'lr' : 'lm');

  if (scenario.id === 'attacked') {
    await log(`ALERT: Hash does not match vendor baseline!`, 'lp');
    await log(`Expected: ${fwHash2}`, 'lm');
    await log(`Got:      ${fwHash}`, 'lr');
    await log(`FIRMWARE TAMPERING DETECTED`, 'lp');
    showToast('🔴 Firmware hash mismatch — possible rootkit!', 'critical', 8000);
  }

  // Generate dynamic hex viewer content
  const hexLines = [
    ['00000000', randHex(16), '................'],
    ['00000010', 'ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff', '................'],
    ['00000500', randHex(16), '................'],
    ['00001000', '4d 5a 90 00 03 00 00 00  04 00 00 00 ff ff 00 00', 'MZ..............'],
    ['00001010', `b8 00 00 00 00 00 00 00  40 00 00 00 00 00 00 00`, '........@.......'],
    ['00005000', `00 00 00 00 5f 46 56 48  00 08 00 00 ff ff ff ff`, '...._FVH........'],
    ['00005010', randHex(16), '................'],
    ['00100000', '45 46 49 20 50 41 52 54  00 00 01 00 5c 00 00 00', 'EFI PART....\\...'],
  ];
  if (scenario.id === 'attacked') {
    hexLines.push(['005e0000', '52 4f 4f 54 4b 49 54 20  53 49 47 4e 41 54 55 52', 'ROOTKIT SIGNATUR']);
    hexLines.push(['005e0010', '45 20 44 45 54 45 43 54  45 44 20 21 21 21 00 00', 'E DETECTED !!!..']);
  }

  const hv = document.getElementById('hex-viewer');
  if (hv) {
    hv.innerHTML = hexLines.map(([addr, bytes, asc]) => {
      const cls = (addr.startsWith('005e') && scenario.id === 'attacked') ? 'lp' : '';
      return `<span class="hex-addr">${addr}</span><span class="hex-bytes ${cls}">${bytes}</span>  <span class="hex-ascii ${cls}">|${asc}|</span>`;
    }).join('\n');
  }

  // Parse FW tree
  await sleep(300);
  await log(`$ UEFITool firmware.bin`, 'lc');
  await log(`UEFITool NE v0.28.0 — parsing 16 MB image...`, 'lb');
  await sleep(400);
  await log(`Found ${randBetween(210,230)} UEFI modules`, 'lg');
  if (scenario.id === 'attacked') {
    await log(`ALERT: 1 unknown module with no GUID match found!`, 'lp');
  }

  const peiCount = randBetween(40, 46);
  const dxeCount = randBetween(170, 190);
  const rootkitLine = scenario.id === 'attacked'
    ? '\n<span class="lp">   ├─ UNKNOWN MODULE (no GUID match) ← ROOTKIT?</span>' : '';
  document.getElementById('fw-tree').innerHTML = `
<span class="fw-dir">├─ Flash Descriptor</span>
<span class="lm">│  ├─ Component Section (FLOCKDN=${scenario.chipsec.spi ? '1' : '0'})</span>
<span class="lm">│  ├─ Region Section</span>
<span class="lm">│  └─ Master Section</span>
<span class="fw-dir">├─ ME Region (Intel ME)</span>
<span class="lm">│  └─ Size: 6 MB</span>
<span class="fw-dir">└─ BIOS Region (10 MB)</span>
<span class="lm">   ├─ FV_MAIN (Main Volume)</span>
<span class="${scenario.id === 'attacked' ? 'fw-err' : 'fw-ok'}">   │  ├─ PEI Core ${scenario.id === 'attacked' ? '← MODIFIED' : '✓'}</span>
<span class="lm">   │  ├─ PEI Modules (${peiCount})</span>
<span class="lm">   │  │  ├─ CpuIo PEI</span>
<span class="lm">   │  │  ├─ MemoryInit PEI</span>
<span class="lm">   │  │  └─ [+${peiCount-2} more]</span>
<span class="${scenario.secureBoot ? 'fw-ok' : 'fw-warn'}">   │  ├─ DXE Core</span>
<span class="lm">   │  └─ DXE Drivers (${dxeCount})${rootkitLine}</span>
<span class="${scenario.secureBoot ? 'fw-ok' : 'fw-err'}">   │     ├─ Secure Boot DXE ${scenario.secureBoot ? '✓' : '✗ DISABLED'}</span>
<span class="${scenario.tpmActive ? 'fw-ok' : 'fw-err'}">   │     ├─ TPM 2.0 DXE ${scenario.tpmActive ? '✓' : '✗ NOT LOADED'}</span>
<span class="lm">   │     ├─ PCI Bus Driver</span>
<span class="lm">   │     └─ [+${dxeCount-3} more]</span>
<span class="${scenario.chipsec.spi ? 'fw-ok' : 'fw-warn'}">   ├─ FV_RECOVERY</span>
<span class="lm">   └─ FV_NVRAM (UEFI Variables)</span>
<span class="${scenario.secureBoot ? 'fw-ok' : 'fw-err'}">      ├─ SecureBoot var: ${scenario.secureBoot ? '0x01 ✓' : '0x00 ✗'}</span>
<span class="lm">      └─ Boot Options</span>`;

  setEl('fm-pei', String(peiCount));
  setEl('fm-dxe', String(dxeCount));
  setEl('fm-size', '16 MB');
  phaseStatus(5, scenario.id === 'attacked' ? 'TAMPERED' : 'Complete',
    scenario.id === 'attacked' ? 'err' : 'ok');
}

// Phase 6: Findings & Scoring
async function phase6(scenario) {
  phaseStatus(6, 'Running…');

  // Build vuln cards
  const grid = document.getElementById('vuln-grid');
  grid.innerHTML = '';
  for (const v of scenario.vulns) {
    const card = document.createElement('div');
    card.className = 'vuln-card ' + v.sev + (v.sev === 'high' || v.sev === 'critical' ? ' flash' : '');

    // Generate a fake firmware hash for each finding
    const hash = `0x${randHash(8).toUpperCase()}`;
    const cveHtml = v.cves.length
      ? `<div class="vuln-hash">CVEs: ${v.cves.join(', ')}</div>`
      : '';
    const impactHtml = (v.impact && (v.impact.conf + v.impact.integ + v.impact.avail) > 0)
      ? `<div style="font-size:9px;color:var(--text-muted);margin-top:6px">CVSS: C:${v.impact.conf}/I:${v.impact.integ}/A:${v.impact.avail}</div>`
      : '';

    card.innerHTML = `
      <div class="vuln-sev ${v.sev}">${v.sev.toUpperCase()}</div>
      <div class="vuln-title">${v.title}</div>
      <div class="vuln-desc">${v.desc}</div>
      <div class="vuln-rec">${v.rec}</div>
      ${cveHtml}
      ${impactHtml}
      <div class="vuln-hash">Finding hash: ${hash} · ${new Date().toISOString().slice(0,19).replace('T',' ')}</div>
      <div class="vuln-actions">
        <button class="vuln-btn why" onclick="showVulnModal(${JSON.stringify(v).replace(/"/g,'&quot;')}, 'why')">❓ Why Vulnerable?</button>
        <button class="vuln-btn fix" onclick="showVulnModal(${JSON.stringify(v).replace(/"/g,'&quot;')}, 'fix')">🔧 How to Fix?</button>
        ${v.cves.length ? `<button class="vuln-btn cve" onclick="showVulnModal(${JSON.stringify(v).replace(/"/g,'&quot;')}, 'cve')">📋 CVE Info</button>` : ''}
      </div>`;
    grid.appendChild(card);
    await sleep(60);
  }

  // Action items
  document.getElementById('action-items').innerHTML =
    scenario.actionItems.map(item => `<span class="${item.color}">${item.text}</span>`).join('<br>');

  document.getElementById('dash-vuln-sum').innerHTML = scenario.dashSummary.vuln;

  // Risk score update
  RiskScorer.updateUI(scenario);

  // Canvas chart
  const critCount = scenario.vulns.filter(v=>v.sev==='critical').length;
  drawSevChart(critCount, scenario.medCount, scenario.secCount);

  const statusText = scenario.critCount > 0
    ? `${scenario.critCount} Critical`
    : scenario.medCount > 0 ? `${scenario.medCount} Medium` : 'Clean';
  phaseStatus(6, statusText, scenario.critCount > 0 ? 'err' : scenario.medCount > 0 ? 'warn' : 'ok');

  if (scenario.id === 'attacked') {
    showToast('☠ CRITICAL: Active compromise detected! Immediate action required.', 'critical', 10000);
    setAttackBar(true);
  } else if (scenario.critCount > 0) {
    showToast(`${scenario.critCount} critical vulnerabilities found — review Phase 6 findings.`, 'error');
  } else if (scenario.medCount > 0) {
    showToast(`${scenario.medCount} medium-severity issues found — review recommendations.`, 'warn');
  } else {
    showToast('System is well-hardened. No critical vulnerabilities detected.', 'success');
  }
}

function drawSevChart(crit, med, sec) {
  const canvas = document.getElementById('sevChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const data = [
    { label: 'Critical', count: crit, color: '#a855f7' },
    { label: 'High/Med', count: med, color: '#f59e0b' },
    { label: 'Low/OK', count: sec, color: '#22c55e' },
  ];
  const total = data.reduce((s,d) => s + d.count, 0) || 1;
  const barW = 40, gap = 28, startX = 36;
  const maxH = H - 50;
  ctx.font = '10px JetBrains Mono, monospace';

  data.forEach((d, i) => {
    const x = startX + i * (barW + gap);
    const bH = Math.max(4, (d.count / total) * maxH);
    const y = H - 30 - bH;
    ctx.fillStyle = d.color + '33';
    ctx.fillRect(x, y, barW, bH);
    ctx.fillStyle = d.color;
    ctx.fillRect(x, y, barW, 3);
    ctx.textAlign = 'center';
    ctx.fillText(d.count, x + barW/2, y - 6);
    ctx.fillStyle = '#7090b0';
    ctx.fillText(d.label, x + barW/2, H - 10);
  });
}

// ═══════════════════════════════════════════════════════════════
// MODULE: LearningPanel — Vulnerability Education System
// ═══════════════════════════════════════════════════════════════

// Vulnerability detail database
const VULN_DETAILS = {
  default: {
    whyText: 'This security control protects the system from unauthorized modification of firmware or boot components. When disabled or misconfigured, an attacker with sufficient privileges can exploit this gap to install persistent malware that survives OS reinstalls.',
    techDetails: 'Modern platforms implement defense-in-depth firmware security through multiple hardware mechanisms. The absence of any single layer increases the attack surface significantly.',
    steps: [
      'Review BIOS/UEFI setup utility for the relevant security setting',
      'Apply the latest vendor BIOS update which may patch related vulnerabilities',
      'Use CHIPSEC to verify the setting is correctly applied at hardware register level',
      'Establish a baseline configuration and monitor for drift',
    ],
  }
};

function showVulnModal(vuln, mode) {
  const content = document.getElementById('learnModalContent');
  const sevColors = { critical:'var(--purple)', high:'var(--red)', medium:'var(--amber)', low:'var(--green)' };
  const color = sevColors[vuln.sev] || 'var(--blue)';

  const impactBar = (val, max=10) => {
    const pct = (val/max)*100;
    const color = pct > 70 ? 'var(--red)' : pct > 40 ? 'var(--amber)' : 'var(--green)';
    return `<div style="flex:1;height:4px;background:var(--border);border-radius:2px;overflow:hidden"><div style="width:${pct}%;height:100%;background:${color};border-radius:2px;transition:width 0.8s ease"></div></div><span style="font-size:10px;color:var(--text-muted);width:20px;text-align:right">${val}</span>`;
  };

  let html = `
    <div class="modal-badge" style="background:${color}22;color:${color};border:1px solid ${color}44">${vuln.sev.toUpperCase()}</div>
    <div class="modal-title">${vuln.title}</div>
    <div class="modal-subtitle">${vuln.desc}</div>`;

  if (mode === 'why') {
    html += `
      <div class="modal-section">
        <div class="modal-section-title">Why Is This A Vulnerability?</div>
        <p>${VULN_DETAILS.default.whyText}</p>
        <p style="margin-top:10px">${VULN_DETAILS.default.techDetails}</p>
      </div>`;

    if (vuln.impact && (vuln.impact.conf + vuln.impact.integ + vuln.impact.avail) > 0) {
      html += `
        <div class="modal-section">
          <div class="modal-section-title">Impact Assessment (CVSS)</div>
          <div class="modal-impact-grid">
            <div class="modal-impact-item">
              <div class="modal-impact-score" style="color:${vuln.impact.conf>6?'var(--red)':vuln.impact.conf>3?'var(--amber)':'var(--green)'}">${vuln.impact.conf}/10</div>
              <div class="modal-impact-label">Confidentiality</div>
            </div>
            <div class="modal-impact-item">
              <div class="modal-impact-score" style="color:${vuln.impact.integ>6?'var(--red)':vuln.impact.integ>3?'var(--amber)':'var(--green)'}">${vuln.impact.integ}/10</div>
              <div class="modal-impact-label">Integrity</div>
            </div>
            <div class="modal-impact-item">
              <div class="modal-impact-score" style="color:${vuln.impact.avail>6?'var(--red)':vuln.impact.avail>3?'var(--amber)':'var(--green)'}">${vuln.impact.avail}/10</div>
              <div class="modal-impact-label">Availability</div>
            </div>
          </div>
          <div style="margin-top:12px;display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;align-items:center;gap:8px;font-size:11px"><span style="width:100px;color:var(--text-muted)">Confidentiality</span>${impactBar(vuln.impact.conf)}</div>
            <div style="display:flex;align-items:center;gap:8px;font-size:11px"><span style="width:100px;color:var(--text-muted)">Integrity</span>${impactBar(vuln.impact.integ)}</div>
            <div style="display:flex;align-items:center;gap:8px;font-size:11px"><span style="width:100px;color:var(--text-muted)">Availability</span>${impactBar(vuln.impact.avail)}</div>
          </div>
        </div>`;
    }

    html += `
      <div class="modal-section">
        <div class="modal-section-title">Attack Scenario</div>
        <p>An attacker who obtains kernel-level code execution (Ring-0, e.g. via a driver exploit) can use this vulnerability to write arbitrary code to the system firmware. This code persists across OS reinstalls, disk replacement, and factory resets — only a full BIOS flash from a clean source can remove it.</p>
        <div class="modal-code">Attacker path: User-space exploit → Kernel (Ring-0) → SMM (Ring -2) → SPI Flash write → Persistent rootkit
Known malware using this vector: MosaicRegressor, CosmicStrand, BlackLotus, LoJax</div>
      </div>`;

  } else if (mode === 'fix') {
    const steps = VULN_DETAILS.default.steps;
    // Add recommendation from vuln if present
    const recText = vuln.rec.replace('→ ', '');
    html += `
      <div class="modal-section">
        <div class="modal-section-title">Remediation Steps</div>
        <p style="color:var(--cyan);margin-bottom:12px">${recText}</p>
        <div class="modal-steps">
          ${steps.map((s, i) => `<div class="modal-step"><div class="modal-step-num">${i+1}</div><div class="modal-step-text">${s}</div></div>`).join('')}
        </div>
      </div>
      <div class="modal-section">
        <div class="modal-section-title">Verification Commands</div>
        <div class="modal-code">
# Verify with CHIPSEC (run as root):
sudo python3 chipsec_main.py -m common.bios_wp
sudo python3 chipsec_main.py -m common.spi
sudo python3 chipsec_main.py -m common.smm

# Check Secure Boot status:
mokutil --sb-state
efivar -l | grep -i SecureBoot

# TPM verification:
tpm2_getcap properties-fixed
tpm2_pcrread sha256:0,1,2,3,4,5,6,7</div>
      </div>
      <div class="modal-section">
        <div class="modal-section-title">Estimated Remediation Effort</div>
        <div class="modal-impact-grid">
          <div class="modal-impact-item"><div class="modal-impact-score" style="color:var(--amber)">~2h</div><div class="modal-impact-label">Config Change</div></div>
          <div class="modal-impact-item"><div class="modal-impact-score" style="color:var(--blue)">Low</div><div class="modal-impact-label">Risk</div></div>
          <div class="modal-impact-item"><div class="modal-impact-score" style="color:var(--green)">High</div><div class="modal-impact-label">Impact</div></div>
        </div>
      </div>`;

  } else if (mode === 'cve') {
    html += `
      <div class="modal-section">
        <div class="modal-section-title">Associated CVEs</div>
        <div class="modal-cve-list">
          ${vuln.cves.map(c => `<span class="modal-cve-tag">${c}</span>`).join('')}
        </div>
      </div>
      <div class="modal-section">
        <div class="modal-section-title">CVE Details</div>
        ${vuln.cves.map(cve => `
          <div style="margin-bottom:14px;padding:12px;background:var(--bg-card);border:1px solid var(--border);border-radius:8px">
            <div style="font-family:var(--display);color:var(--cyan);font-weight:700;margin-bottom:6px">${cve}</div>
            <div style="font-size:11px;color:var(--text-secondary)">
              ${cve === 'CVE-2022-21894' ? 'Secure Boot Security Feature Bypass Vulnerability (BlackLotus). CVSS 4.4 (Medium). Allows bypass of UEFI Secure Boot to load unsigned bootkit.' :
                cve === 'CVE-2019-11098' ? 'Intel® Server Board SMM protection bypass via BIOS_CNTL.SMM_BWP bit. Allows privileged code to modify firmware.' :
                cve === 'CVE-2017-5703' ? 'Configuration of SPI Flash in Intel Platforms may allow privileged user to directly write to flash, enabling persistent attack.' :
                cve === 'CVE-2021-33164' ? 'Improper access control in BIOS firmware allows privileged user to enable escalation of privilege via local access (SMM).' :
                'See NVD (nvd.nist.gov) for full details.'}
            </div>
          </div>`).join('')}
      </div>`;
  }

  content.innerHTML = html;
  document.getElementById('learnModal').classList.add('show');
}

function closeLearnModal() {
  document.getElementById('learnModal').classList.remove('show');
}
function closeModal(e) {
  if (e.target === document.getElementById('learnModal')) closeLearnModal();
}

// Learn tab modals
const LEARN_CONTENT = {
  secureboot: {
    title: '🔒 Secure Boot', sev: 'PROTECTION', color: 'var(--cyan)',
    body: `<div class="modal-section"><div class="modal-section-title">What is Secure Boot?</div><p>Secure Boot is a UEFI feature that ensures only cryptographically signed bootloaders, drivers, and operating system kernels are allowed to execute during the boot process. It uses a PKI (Public Key Infrastructure) chain of trust anchored in the Platform Key (PK) stored in NVRAM.</p></div>
<div class="modal-section"><div class="modal-section-title">The Chain of Trust</div><div class="modal-code">Platform Key (PK)          ← Root CA, set by OEM
    └── Key Exchange Key (KEK)   ← Intermediate CA
             └── Signature DB (db)  ← Allowed hashes/certs
             └── Forbidden DB (dbx) ← Revocation list
                      └── Bootloader (e.g., shim, GRUB2)
                               └── OS Kernel (signed)
                                        └── OS (trusted)</div></div>
<div class="modal-section"><div class="modal-section-title">Common Weaknesses</div><p>Secure Boot can be bypassed through: (1) stolen signing keys, (2) vulnerable shim/bootloader code (e.g., BootHole CVE-2020-10713), (3) rollback attacks using older vulnerable versions, (4) direct UEFI variable modification if write-protected controls are absent.</p></div>`
  },
  smm: {
    title: '⚡ System Management Mode (SMM)', sev: 'ADVANCED', color: 'var(--amber)',
    body: `<div class="modal-section"><div class="modal-section-title">What is SMM?</div><p>System Management Mode (SMM) is a special-purpose CPU operating mode available on x86 processors. It's sometimes called "Ring -2" because it has higher privilege than even the OS kernel (Ring 0) or hypervisor (Ring -1). SMM code is isolated in SMRAM — a protected memory region invisible to the OS.</p></div>
<div class="modal-section"><div class="modal-section-title">Privilege Levels</div><div class="modal-code">Ring 3 — User space applications
Ring 0 — OS kernel, drivers
Ring -1 — Hypervisor (VMX root)
Ring -2 — SMM (highest privilege, invisible to OS)
Ring -3 — Intel ME / AMD PSP (firmware coprocessors)</div></div>
<div class="modal-section"><div class="modal-section-title">SMM Security Controls</div><p>The SMRAMC register controls SMRAM access: D_LCK locks the region, D_CLS closes it to outside access, G_SMRAME enables global protection. SMM_BWP in the BIOS Control Register prevents firmware writes from SMM itself.</p></div>`
  },
  spi: {
    title: '💾 SPI Flash & Write Protection', sev: 'STORAGE', color: 'var(--green)',
    body: `<div class="modal-section"><div class="modal-section-title">What is the SPI Flash?</div><p>The SPI (Serial Peripheral Interface) flash chip stores the UEFI firmware. It typically contains the Flash Descriptor, Intel ME region, and BIOS region. On most platforms, this is a Winbond or Micron NOR flash chip accessed via the PCH SPI controller.</p></div>
<div class="modal-section"><div class="modal-section-title">Write Protection Mechanisms</div><div class="modal-code">1. FLOCKDN (Flash Lock Down):
   - Locks HSFS and PR registers after POST
   - Prevents PR reconfiguration
2. PR0–PR4 (Protected Ranges):
   - Hardware-enforced write-protect regions
   - Configured by BIOS, covers firmware regions
3. SMM_BWP (SMM Write Protect):
   - BC register bit, prevents BIOS writes
   - Even SMM code cannot bypass this
4. Intel Boot Guard:
   - Hardware ACM verifies IBB before BIOS runs
   - Fused into CPU, cannot be disabled</div></div>`
  },
  tpm: {
    title: '🔑 TPM 2.0 — Trusted Platform Module', sev: 'HARDWARE', color: 'var(--blue)',
    body: `<div class="modal-section"><div class="modal-section-title">What is a TPM?</div><p>The Trusted Platform Module (TPM) is a dedicated hardware security chip that provides a hardware root of trust. It stores cryptographic keys, performs secure hashing, and supports platform attestation through Platform Configuration Registers (PCRs).</p></div>
<div class="modal-section"><div class="modal-section-title">Measured Boot with TPM</div><div class="modal-code">PCR0: BIOS/UEFI firmware measurement
PCR1: BIOS configuration
PCR2: Option ROM code
PCR4: MBR / Bootloader code
PCR7: Secure Boot state
PCR8-15: OS and application measurements</div></div>
<div class="modal-section"><div class="modal-section-title">Use Cases</div><p>BitLocker drive encryption (binds to PCR values), Remote attestation (prove to remote party that system is trustworthy), SSH key storage, Certificate storage, Platform integrity monitoring.</p></div>`
  },
  bootkits: {
    title: '☠ UEFI Bootkits', sev: 'THREAT', color: 'var(--red)',
    body: `<div class="modal-section"><div class="modal-section-title">What are UEFI Bootkits?</div><p>UEFI bootkits are malware that embed themselves into the UEFI firmware or EFI System Partition, executing before the OS loads. This gives them persistence that survives OS reinstalls, disk replacement, and factory resets.</p></div>
<div class="modal-section"><div class="modal-section-title">Notable Examples</div><div class="modal-code">LoJax (2018):      First UEFI rootkit in the wild (APT28)
MosaicRegressor (2020): Compromised firmware update mechanism
CosmicStrand (2021): Found in MSI and Gigabyte motherboards
BlackLotus (2022): First in-the-wild Secure Boot bypass (CVE-2022-21894)
ESPecter (2021):   Bootkit in EFI System Partition</div></div>
<div class="modal-section"><div class="modal-section-title">Detection Methods</div><p>CHIPSEC firmware analysis, Measured boot PCR comparison, Vendor-provided firmware scanners (e.g., ESET UEFI Scanner), Binary diffing against known-good firmware images, Runtime memory inspection tools.</p></div>`
  },
  smmrootkit: {
    title: '👻 SMM Rootkits', sev: 'THREAT', color: 'var(--purple)',
    body: `<div class="modal-section"><div class="modal-section-title">SMM Rootkit Characteristics</div><p>SMM rootkits execute in System Management Mode (Ring -2) and are invisible to: the OS, hypervisors (VMX), antivirus software, and most forensic tools. They can intercept hardware events, modify memory, and exfiltrate data — all without the OS knowing.</p></div>
<div class="modal-section"><div class="modal-section-title">Attack Chain</div><div class="modal-code">1. Attain kernel (Ring-0) code execution
2. Exploit SMM communication interface vulnerability
3. Inject malicious SMI handler into SMRAM
4. Rootkit executes on every SMI interrupt
5. Can: modify OS memory, bypass security checks,
        maintain persistent backdoor, exfiltrate data</div></div>
<div class="modal-section"><div class="modal-section-title">Mitigations</div><p>Lock SMRAM (D_LCK=1), Enable SMM_BWP bit, Use TSEG-based SMRAM protection, Apply vendor SMM hardening patches, Enable Intel TXT/SGX for hardware isolation boundaries.</p></div>`
  },
  supplychain: {
    title: '🏭 Supply Chain Attacks', sev: 'THREAT', color: 'var(--amber)',
    body: `<div class="modal-section"><div class="modal-section-title">Firmware Supply Chain Threats</div><p>Supply chain attacks compromise firmware during manufacturing, distribution, or update processes. Unlike runtime attacks, they may be present from day one, making detection extremely difficult without hardware-level verification.</p></div>
<div class="modal-section"><div class="modal-section-title">Attack Vectors</div><div class="modal-code">1. Compromised vendor update servers
2. Tampered firmware packages (MITM)
3. Malicious firmware inserted at manufacturing
4. Compromised development toolchain
5. Rogue internal actors at OEM/ODM</div></div>
<div class="modal-section"><div class="modal-section-title">Defense Strategies</div><p>Intel Boot Guard (hardware roots of trust from manufacturing), Secure firmware update channels with code signing, SBOM (Software Bill of Materials) for firmware, Binary verification against reproducible builds, Hardware security modules for update signing keys.</p></div>`
  },
  chipsec: {
    title: '🛡 CHIPSEC Security Framework', sev: 'TOOL', color: 'var(--cyan)',
    body: `<div class="modal-section"><div class="modal-section-title">What is CHIPSEC?</div><p>CHIPSEC (Platform Security Assessment Framework) is an open-source tool developed by Intel Security Research that allows security researchers to assess the security configuration of platform firmware and hardware. It directly accesses hardware registers to verify security settings.</p></div>
<div class="modal-section"><div class="modal-section-title">Key Modules</div><div class="modal-code">common.bios_wp     — BIOS write protection check
common.secureboot  — Secure Boot configuration
common.spi         — SPI controller security
common.smm         — SMM protection checks
common.bios_ts     — BIOS TS range protection
common.memconfig   — Memory configuration
common.remap       — Memory remapping attacks
tools.cpu.sinkhole — CPU SMM rootkit detection</div></div>
<div class="modal-section"><div class="modal-section-title">Usage</div><div class="modal-code">sudo python3 chipsec_main.py         # Run all checks
sudo python3 chipsec_main.py -m common.bios_wp   # Single module
sudo python3 chipsec_main.py -l     # List all modules
sudo python3 chipsec_main.py --xml output.xml    # XML report</div></div>`
  },
};

function showLearnModal(key) {
  const info = LEARN_CONTENT[key];
  if (!info) return;
  const content = document.getElementById('learnModalContent');
  content.innerHTML = `
    <div class="modal-badge" style="background:${info.color}22;color:${info.color};border:1px solid ${info.color}44">${info.sev}</div>
    <div class="modal-title">${info.title}</div>
    ${info.body}`;
  document.getElementById('learnModal').classList.add('show');
}

// ═══════════════════════════════════════════════════════════════
// MODULE: SmartTerminal — Scenario-Aware CLI
// ═══════════════════════════════════════════════════════════════

// Base command outputs (scenario-independent)
const GT_COMMANDS_BASE = {
  help: [
    ['═══════════════════════════════════════════════', 'lb'],
    ['  BIOS/UEFI Security Lab — Available Commands', 'lb'],
    ['═══════════════════════════════════════════════', 'lb'],
    ['  help                     — Show this help', 'lm'],
    ['  scan                     — Quick security scan', 'lm'],
    ['  scenario                 — Show current scenario', 'lm'],
    ['  uname -a                 — System info', 'lm'],
    ['  dmesg | tail             — Kernel messages', 'lm'],
    ['  lspci                    — PCI devices', 'lm'],
    ['  dmidecode -t 0           — BIOS info', 'lm'],
    ['  flashrom -p internal --get-size  — Flash size', 'lm'],
    ['  mokutil --sb-state       — Secure Boot state', 'lm'],
    ['  tpm2_getcap properties-fixed  — TPM info', 'lm'],
    ['  hexdump firmware.bin | head  — Hex view', 'lm'],
    ['  chipsec_main -m common.bios_wp  — CHIPSEC', 'lm'],
    ['  cat /proc/iomem | grep BIOS  — Memory map', 'lm'],
    ['  sudo cat /sys/class/tpm/tpm0/pcr-sha256/0  — PCR0', 'lm'],
    ['  clear                    — Clear terminal', 'lm'],
    ['', ''],
    ['  Tip: Run the Full Simulation first for scenario-specific outputs.', 'la'],
  ],
  'uname -a': [['Linux security-lab 5.15.0-91-generic #101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux', 'lg']],
  'dmesg | tail': [
    ['[  0.000000] Linux version 5.15.0-91-generic', 'lm'],
    ['[  0.003456] CPU: Intel i7-11700K (8C/16T) @ 3.60GHz', 'lg'],
    ['[  0.008456] Memory: 16384 MB total, 16200 MB available', 'lg'],
    ['[  0.013500] ACPI: FADT 0x000E4B90 000114 (v05 INTEL  HW  )', 'lm'],
    ['[  0.014500] TPM 2.0 (device-id 0x000B, rev-id 1)', 'lg'],
  ],
  lspci: [
    ['00:00.0 Host bridge: Intel Corporation 11th Gen Core (rev 05)', 'lm'],
    ['00:02.0 VGA compatible: Intel UHD Graphics 750', 'lm'],
    ['00:08.0 System peripheral: Intel GNA Scoring Accelerator', 'lm'],
    ['00:14.0 USB controller: Intel Tiger Lake USB 3.2 Gen 2', 'lm'],
    ['00:17.0 SATA controller: Intel 500 Series PCH AHCI (rev 11)', 'lm'],
    ['00:1f.5 Serial bus controller: Intel PCH SPI Controller (rev 11)', 'lm'],
  ],
  'dmidecode -t 0': [
    ['BIOS Information', 'la'],
    ['  Vendor:  American Megatrends International, LLC.', 'lm'],
    ['  Version: 1.40', 'lm'],
    ['  Release Date: 06/30/2023', 'lm'],
    ['  ROM Size: 16 MB', 'lm'],
    ['  Characteristics: PCI supported, BIOS upgradeable', 'lm'],
    ['  BIOS Revision: 5.18', 'lm'],
  ],
  'flashrom -p internal --get-size': [
    ['flashrom v1.2 on Linux 5.15.0', 'lb'],
    ['Found chipset: Intel C620 series', 'lg'],
    ['Found flash chip "W25Q128.V" (16384 kB, SPI)', 'lg'],
    ['16777216', 'lg'],
  ],
  'hexdump firmware.bin | head': [
    ['00000000  d9 54 93 7a 68 04 4a 44  bc 81 f3 89 f3 82 6b 95  |.T.zh.JD......k.|', 'lm'],
    ['00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|', 'lm'],
    ['*', 'lm'],
    ['00001000  4d 5a 90 00 03 00 00 00  04 00 00 00 ff ff 00 00  |MZ..............|', 'lm'],
    ['00005000  5f 46 56 48 00 08 00 00  ff ff ff ff ff ff ff ff  |_FVH............|', 'lm'],
  ],
  'cat /proc/iomem | grep BIOS': [
    ['ff000000-ffffffff : BIOS', 'lg'],
    ['fec00000-fec00fff : IOAPIC 0', 'lm'],
    ['fed00000-fed003ff : HPET 0', 'lm'],
  ],
  'chipsec_main --help': null,  // Delegate to chipsec terminal
  'chipsec_main -m common.bios_wp': null,
};

// Commands that change output based on scenario
function getScenarioCommand(cmd) {
  const scenario = SimState.currentScenario;
  if (!scenario) return null;

  // Check for terminal overrides in scenario
  if (scenario.terminalOverrides && scenario.terminalOverrides[cmd]) {
    return scenario.terminalOverrides[cmd];
  }

  if (cmd === 'scan') {
    return buildScanOutput(scenario);
  }
  if (cmd === 'scenario') {
    return [
      [`Current scenario: ${scenario.label}`, 'lc'],
      [`Risk level:       ${scenario.riskLabel}`, scenario.riskLevel === 'low' ? 'lg' : scenario.riskLevel === 'critical' ? 'lp' : 'la'],
      [`Risk score:       ${scenario.score}/100`, 'lm'],
      [`Description:      ${scenario.description}`, 'lm'],
      [`Secure Boot:      ${scenario.secureBoot ? 'ENABLED' : 'DISABLED'}`, scenario.secureBoot ? 'lg' : 'lr'],
      [`TPM:              ${scenario.tpmActive ? 'ACTIVE' : 'INACTIVE'}`, scenario.tpmActive ? 'lg' : 'lr'],
      [`Critical vulns:   ${scenario.critCount}`, scenario.critCount > 0 ? 'lr' : 'lg'],
    ];
  }
  if (cmd === 'sudo cat /sys/class/tpm/tpm0/pcr-sha256/0') {
    if (!scenario || !scenario.tpmActive) {
      return [['cat: /sys/class/tpm/tpm0: No such file or directory', 'lr']];
    }
    if (scenario.id === 'attacked') {
      return [
        [`${randHash(64)}`, 'lr'],
        ['WARNING: PCR0 does not match baseline — firmware may be tampered', 'lp'],
      ];
    }
    return [[`${randHash(64)}`, 'lg']];
  }
  if (cmd === 'dmesg | tail' && scenario.id === 'attacked') {
    return [
      ['[  0.000000] Linux version 5.15.0-91-generic', 'lm'],
      ['[  0.003456] CPU: Intel i7-11700K (8C/16T) @ 3.60GHz', 'lg'],
      ['[  0.014000] ALERT: Secure Boot bypass detected in boot chain', 'lp'],
      ['[  0.014500] SMM rootkit signatures detected in memory', 'lp'],
      ['[  0.015000] WARNING: Firmware measurements do not match TPM baseline', 'lr'],
    ];
  }
  return null; // fall through to base
}

function buildScanOutput(scenario) {
  const lines = [
    ['', ''],
    ['╔══════════════════════════════════════════╗', 'lb'],
    ['║  BIOS/UEFI Quick Security Scan          ║', 'lb'],
    ['╚══════════════════════════════════════════╝', 'lb'],
    ['', ''],
  ];
  const checks = [
    { label: 'Secure Boot', pass: scenario.secureBoot },
    { label: 'TPM 2.0 Active', pass: scenario.tpmActive },
    { label: 'SMM_BWP Bit', pass: scenario.chipsec.smm_bwp },
    { label: 'SPI PR Config', pass: scenario.chipsec.spi === true },
    { label: 'SMRAM Lock', pass: scenario.chipsec.smm !== false },
    { label: 'Flash Locked', pass: true },
  ];
  checks.forEach(c => {
    const icon = c.pass ? '✓' : '✗';
    const cls = c.pass ? 'lg' : 'lr';
    lines.push([`  [${icon}] ${c.label.padEnd(20)} ${c.pass ? 'PASS' : 'FAIL'}`, cls]);
  });
  lines.push(['', '']);
  lines.push([`  Overall Risk Score: ${scenario.score}/100 — ${scenario.riskLabel}`, scenario.score > 70 ? 'lg' : scenario.score > 40 ? 'la' : 'lr']);
  lines.push(['', '']);
  return lines;
}

async function handleGT(e) {
  const inp = document.getElementById('gtInput');
  if (e.key === 'ArrowUp') { e.preventDefault(); SimState.histIdx = Math.min(SimState.histIdx+1, SimState.gtHistory.length-1); inp.value = SimState.gtHistory[SimState.histIdx] || ''; return; }
  if (e.key === 'ArrowDown') { e.preventDefault(); SimState.histIdx = Math.max(SimState.histIdx-1, -1); inp.value = SimState.histIdx === -1 ? '' : SimState.gtHistory[SimState.histIdx]; return; }
  if (e.key !== 'Enter') return;

  const cmd = inp.value.trim();
  if (!cmd) return;
  inp.value = '';
  SimState.gtHistory.unshift(cmd);
  SimState.histIdx = -1;

  const body = document.getElementById('gtBody');
  const hist = document.getElementById('gt-history');
  hist.innerHTML = SimState.gtHistory.slice(0, 20).map(c => `<span class="lc">${c}</span>`).join('<br>');

  body.innerHTML += `<span class="lg">root@security-lab</span><span class="lm">:~$</span> <span class="lc">${cmd}</span>\n`;

  if (cmd === 'clear') { body.innerHTML = ''; return; }

  // Scenario-specific overrides first
  const scenarioCmdOutput = getScenarioCommand(cmd);
  if (scenarioCmdOutput) {
    for (const [text, cls] of scenarioCmdOutput) {
      const span = document.createElement('span');
      span.className = cls;
      span.textContent = text;
      body.appendChild(span);
      body.appendChild(document.createTextNode('\n'));
      body.scrollTop = body.scrollHeight;
      await sleep(50);
    }
    body.innerHTML += '\n';
    body.scrollTop = body.scrollHeight;
    return;
  }

  // Base commands
  const lines = GT_COMMANDS_BASE[cmd];
  if (lines === undefined) {
    body.innerHTML += `<span class="lr">bash: ${cmd}: command not found</span>\n<span class="lm">Type 'help' for available commands</span>\n`;
  } else if (lines === null) {
    showTab('security', null);
    await runChipCmd(cmd);
    return;
  } else {
    for (const [text, cls] of lines) {
      const span = document.createElement('span');
      span.className = cls;
      span.textContent = text;
      body.appendChild(span);
      body.appendChild(document.createTextNode('\n'));
      body.scrollTop = body.scrollHeight;
      await sleep(40);
    }
  }
  body.innerHTML += '\n';
  body.scrollTop = body.scrollHeight;
}

// ═══════════════════════════════════════════════════════════════
// MODULE: CHIPSEC Terminal — Scenario-aware outputs
// ═══════════════════════════════════════════════════════════════
function buildChipOutput(modName, scenario) {
  const c = scenario ? scenario.chipsec : {};
  const outputs = {
    'chipsec_main -m common.bios_wp': [
      ['[*] Module: BIOS Write Protection Check', 'lb'],
      ['[*] Checking BIOS Control Register (BC)...', 'la'],
      ...(c.bios_wp ? [
        ['    BC Register value: 0xAB', 'lm'],
        ['      WPD (Write Protect Disable): 0  — PROTECTED ✓', 'lg'],
        ['      BLE (BIOS Lock Enable):      1  — ENABLED ✓', 'lg'],
        ['      SMM_BWP (SMM Write Protect):  1  — SET ✓', 'lg'],
        ['', ''],
        ['[RESULT] PASSED — BIOS write protection fully enabled ✓', 'lg'],
      ] : [
        ['    BC Register value: 0x89', 'lm'],
        ['      WPD (Write Protect Disable): 1  — UNPROTECTED', 'lr'],
        ['      BLE (BIOS Lock Enable):      0  — DISABLED', 'lr'],
        ['      SMM_BWP (SMM Write Protect):  0  — NOT SET ⚠', 'lr'],
        ['', ''],
        ['[!] WARNING: BIOS region is not protected against writes', 'lr'],
        ['[RESULT] FAILED — SMM_BWP bit not set', 'lr'],
      ]),
    ],
    'chipsec_main -m common.secureboot': [
      ['[*] Module: Secure Boot Configuration', 'lb'],
      ['[*] Checking EFI variables...', 'la'],
      ...(c.secureboot ? [
        ['    SecureBoot: 0x01  — ENABLED ✓', 'lg'],
        ['    SetupMode:  0x00  — Not in setup mode ✓', 'lg'],
        ['    PK:  Present  (Platform Key installed)', 'lg'],
        ['    KEK: Present  (Key Exchange Key valid)', 'lg'],
        ['    db:  Present  (Signature database populated)', 'lg'],
        ['    dbx: Present  (Forbidden signature database set)', 'lg'],
        ['', ''],
        ['[RESULT] PASSED — Secure Boot properly configured ✓', 'lg'],
      ] : [
        ['    SecureBoot: 0x00  — DISABLED ✗', 'lr'],
        ['    SetupMode:  0x01  — IN SETUP MODE (no PK!)', 'lr'],
        ['    PK:  NOT PRESENT', 'lr'],
        ['    KEK: NOT PRESENT', 'lr'],
        ['    db:  Empty', 'lr'],
        ...(scenario && scenario.id === 'attacked' ? [['    ALERT: Secure Boot bypass signature detected', 'lp']] : []),
        ['', ''],
        ['[RESULT] FAILED — Secure Boot not configured or bypassed ✗', 'lr'],
      ]),
    ],
    'chipsec_main -m common.spi': [
      ['[*] Module: SPI Flash Controller Security', 'lb'],
      ['[*] Checking HSFS register...', 'la'],
      ['    HSFS.FLOCKDN (Flash Conf Lock): 1  — LOCKED ✓', 'lg'],
      ['    HSFS.FDV    (Flash Desc Valid): 1  — VALID ✓', 'lg'],
      ['[*] Checking Protected Ranges (PR0–PR4)...', 'la'],
      ...(c.spi === true ? [
        ['    PR0: 0xFF000000–0xFF7FFFFF — BIOS region protected ✓', 'lg'],
        ['    PR1: 0xFFF00000–0xFFFFFFFF — Recovery region ✓', 'lg'],
        ['    PR2–PR4: Additional ranges configured', 'lg'],
        ['', ''],
        ['[RESULT] PASSED — SPI protected ranges fully configured ✓', 'lg'],
      ] : [
        ['    PR0: 0x00000000 — Not configured', 'lr'],
        ['    PR1: 0x00000000 — Not configured', 'lr'],
        ['    PR2–PR4: Not configured', 'lr'],
        ['', ''],
        ['[!] SPI protected ranges not set — BIOS region writable', 'lr'],
        ['[RESULT] ' + (c.spi === 'warn' ? 'WARNING' : 'FAILED') + ' — Flash locked but no PR protection', c.spi === 'warn' ? 'la' : 'lr'],
      ]),
    ],
    'chipsec_main -m common.smm': [
      ['[*] Module: System Management Mode Security', 'lb'],
      ['[*] Checking SMRAMC register...', 'la'],
      ['    D_OPEN  (SMRAM Open):   0 — Closed ✓', 'lg'],
      ['    D_CLS   (SMRAM Closed): 1 — Locked ✓', 'lg'],
      ['    D_LCK   (SMRAM Lock):   1 — Locked ✓', 'lg'],
      ...(scenario && scenario.id === 'attacked' ? [
        ['    G_SMRAME (Global Enable): 1 — (Rootkit present in SMRAM!)', 'lp'],
        ['    ALERT: Unknown SMM handler at 0x7B000000 detected', 'lp'],
      ] : [
        ['    G_SMRAME (Global Enable): 1 — Enabled ✓', 'lg'],
      ]),
      ['[*] Checking SMI suppression...', 'la'],
      ['    SMI Lock: Not Implemented on this platform', 'la'],
      ['', ''],
      ...(scenario && scenario.id === 'attacked' ? [
        ['[CRITICAL] SMM ROOTKIT DETECTED — Unauthorized handler found', 'lp'],
        ['[RESULT] FAILED — System compromised', 'lr'],
      ] : [
        ['[!] WARNING: SMI lock not available on this platform', 'la'],
        ['[RESULT] WARNING — SMRAM locked, SMI lock not available', 'la'],
      ]),
    ],
    'chipsec_main --help': [
      ['CHIPSEC: Platform Security Assessment Framework v1.10.6', 'lb'],
      ['Usage: chipsec_main -m <module> [options]', 'lm'],
      ['', ''],
      ['Available modules:', 'la'],
      ['  common.bios_wp          — BIOS write protection check', 'lm'],
      ['  common.secureboot       — Secure Boot configuration', 'lm'],
      ['  common.spi              — SPI flash controller check', 'lm'],
      ['  common.smm              — SMM protection check', 'lm'],
      ['  common.bios_ts          — BIOS TS range check', 'lm'],
      ['  common.memconfig        — Memory configuration check', 'lm'],
      ['  tools.cpu.sinkhole      — CPU SMM rootkit detection', 'lm'],
      ['', ''],
      ['Options:', 'la'],
      ['  -l          — List all modules', 'lm'],
      ['  -v          — Verbose output', 'lm'],
      ['  --xml FILE  — Save XML report', 'lm'],
      ['  --no-driver — Run without kernel driver', 'lm'],
    ],
  };
  return outputs[modName] || [['[ERROR] Unknown module: ' + modName, 'lr']];
}

async function runChipCmd(cmd) {
  const out = document.getElementById('chipOutput');
  out.innerHTML += `<span class="lg">root@lab:~$</span> <span class="lc">${cmd}</span>\n`;
  out.scrollTop = out.scrollHeight;
  await sleep(200);

  const lines = buildChipOutput(cmd, SimState.currentScenario);
  for (const [text, cls] of lines) {
    const span = document.createElement('span');
    span.className = cls;
    span.textContent = text;
    out.appendChild(span);
    out.appendChild(document.createTextNode('\n'));
    out.scrollTop = out.scrollHeight;
    await sleep(65);
  }
  out.innerHTML += '\n';
  out.scrollTop = out.scrollHeight;
}

function setChip(cmd) {
  document.getElementById('chipInput').value = cmd;
  document.getElementById('chipInput').focus();
}

async function execChip() {
  const inp = document.getElementById('chipInput');
  const cmd = inp.value.trim();
  if (!cmd) return;
  inp.value = '';
  SimState.cmdHistory.unshift(cmd);
  SimState.histIdx = -1;
  await runChipCmd(cmd);
}

function handleChip(e) {
  const inp = document.getElementById('chipInput');
  if (e.key === 'Enter') { execChip(); return; }
  if (e.key === 'ArrowUp') { e.preventDefault(); SimState.histIdx = Math.min(SimState.histIdx+1, SimState.cmdHistory.length-1); inp.value = SimState.cmdHistory[SimState.histIdx] || ''; }
  if (e.key === 'ArrowDown') { e.preventDefault(); SimState.histIdx = Math.max(SimState.histIdx-1, -1); inp.value = SimState.histIdx === -1 ? '' : SimState.cmdHistory[SimState.histIdx]; }
}

// ═══════════════════════════════════════════════════════════════
// MODULE: Orchestrator — Main simulation flow
// ═══════════════════════════════════════════════════════════════
async function runFullSim() {
  if (SimState.isRunning) return;
  SimState.isRunning = true;
  document.getElementById('btnFull').disabled = true;
  document.getElementById('masterBtn').disabled = true;

  // Resolve scenario
  const scenario = resolveScenario();
  showToast(`Starting ${scenario.label} simulation…`, 'info', 3000);

  // Clear attack bar initially
  setAttackBar(false);

  showTab('dashboard', null);
  document.querySelectorAll('.nav-tab')[0].click();

  // Animate global progress bar with scenario-appropriate style
  const barStyle = scenario.id === 'attacked' ? 'attack' : scenario.id === 'vulnerable' ? 'scan' : '';
  globalBar(5, barStyle);

  await phase1(scenario); globalBar(18, barStyle);
  showTab('bios', null);
  await phase2(scenario); globalBar(36, barStyle);
  showTab('uefi', null);
  await phase3(scenario); globalBar(54, barStyle);
  showTab('security', null);
  await phase4(scenario); globalBar(72, barStyle);
  showTab('firmware', null);
  await phase5(scenario); globalBar(88, barStyle);
  showTab('findings', null);
  await phase6(scenario); globalBar(100, barStyle);

  // Final status
  document.getElementById('globalDot').className = scenario.id === 'attacked'
    ? 'status-dot err' : scenario.critCount > 0 ? 'status-dot warn' : 'status-dot';
  setEl('globalStatus', scenario.id === 'attacked' ? 'COMPROMISED' : 'COMPLETE');

  SimState.isRunning = false;
  document.getElementById('btnFull').disabled = false;
  document.getElementById('masterBtn').disabled = false;
}

async function runPhase(phases, tab) {
  if (SimState.isRunning) return;
  SimState.isRunning = true;
  const scenario = SimState.currentScenario || resolveScenario();
  showTab(tab, null);
  for (const p of phases) {
    if (p === 1) await phase1(scenario);
    if (p === 2) await phase2(scenario);
    if (p === 3) await phase3(scenario);
    if (p === 4) await phase4(scenario);
    if (p === 5) await phase5(scenario);
    if (p === 6) await phase6(scenario);
  }
  SimState.isRunning = false;
}

function resetAll() {
  if (SimState.isRunning) { showToast('Cannot reset while simulation is running.', 'error'); return; }

  // UI resets
  document.getElementById('btnFull').disabled = false;
  document.getElementById('masterBtn').disabled = false;
  document.getElementById('globalDot').className = 'status-dot';
  setEl('globalStatus', 'IDLE');
  globalBar(0);
  setAttackBar(false);

  const dashTab = document.querySelector('.nav-tab[data-tab="dashboard"]');
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  if (dashTab) dashTab.classList.add('active');
  showTab('dashboard', dashTab);

  document.querySelectorAll('.phase-item').forEach((item, i) => {
    item.className = i === 0 ? 'phase-item active' : 'phase-item';
  });
  for (let i = 1; i <= 6; i++) phaseStatus(i, 'Awaiting run…');

  // Dashboard
  setEl('dash-sb', '--'); setEl('dash-score', '--/100'); setEl('dash-risk', 'Simulation not run');
  document.getElementById('dash-sb').style.color = '';
  document.getElementById('dash-score').style.color = '';
  setEl('dash-boot-sum', 'Run simulation to populate…');
  setEl('dash-chip-sum', 'Run simulation to populate…');
  setEl('dash-vuln-sum', 'Run simulation to populate…');

  // Hardware
  ['cpu','ram','disk','psu','gpu','tpm'].forEach(hw => setEl('hw-' + hw, '—', 'hw-val'));
  ['psu','cpu','ram','dev','post'].forEach(id => { setProgress('pf-' + id, 'pp-' + id, 0); });

  // Score ring
  const arc = document.getElementById('scoreArc');
  if (arc) { arc.style.strokeDashoffset = 201; arc.style.stroke = '#f59e0b'; }
  const badge = document.getElementById('riskLevelBadge');
  if (badge) { badge.textContent = '—'; badge.className = 'risk-level-badge'; }

  // Logs
  setLog('log-p1', '<span class="lm">[ Simulation not started ]</span>');
  setLog('log-p2', '<span class="lm">[ Awaiting phase 2 ]</span>');
  setLog('log-p3', '<span class="lm">[ Awaiting phase 3 ]</span>');
  setLog('log-p5', '<span class="lm">[ Awaiting phase 5 ]</span>');

  // UEFI steps
  document.querySelectorAll('.uefi-step').forEach(s => s.className = 'uefi-step');

  // Score bars
  ['crit','med','sec'].forEach(k => { document.getElementById('sb-' + k).style.width = '0%'; setEl('sv-' + k, '--'); });
  setEl('scoreVal', '--');

  // Secure Boot badge
  const sb = document.getElementById('sb-badge');
  if (sb) sb.style.cssText = '';
  setEl('sb-text', 'Not yet checked');
  setEl('os-output', 'Awaiting simulation…');
  setEl('dc-pei', '--'); setEl('dc-dxe', '--'); setEl('dc-total', '--');

  // CHIPSEC
  setLog('chipOutput', '<span class="lm">Type a command or click a suggestion below. Try: chipsec_main -m common.bios_wp</span>');
  setEl('chip-summary', 'Run the full simulation or type commands to see results.');
  ['smm','bwp','spi','sb','smram','tpm'].forEach(k => {
    const el = document.getElementById('rc-' + k);
    if (el) { el.style.width = '0%'; el.textContent = '0%'; }
  });

  // Firmware
  document.getElementById('hex-viewer').innerHTML = '<span class="lm">[ Awaiting firmware dump ]</span>';
  document.getElementById('fw-tree').innerHTML = '<span class="lm">[ Awaiting parse ]</span>';
  setEl('fm-pei', '--'); setEl('fm-dxe', '--'); setEl('fm-size', '--');

  // Findings
  document.getElementById('vuln-grid').innerHTML = '<div class="result-pane full-span center-text padded-large" style="font-size:12px;color:var(--text-muted);">Run simulation to generate findings…</div>';
  setEl('action-items', 'Awaiting analysis…');

  // Terminal
  document.getElementById('gtBody').innerHTML = '<span class="lg">root@security-lab</span><span class="lm">:</span><span class="lb">~</span><span class="lm">$</span> <span class="lc">echo "BIOS/UEFI Security Lab Terminal Ready"</span>\n<span class="lg">BIOS/UEFI Security Lab Terminal Ready</span>\n<span class="lm">Type \'help\' for available commands.</span>\n';
  setEl('gt-history', 'No commands run yet.');

  // Scenario badge reset
  const badge2 = document.getElementById('scenarioBadge');
  if (badge2) { badge2.textContent = '⚙ Scenario: NONE'; badge2.className = 'scenario-badge'; }

  SimState.gtHistory = [];
  SimState.cmdHistory = [];
  SimState.histIdx = -1;
  SimState.currentScenario = null;
  SimState.isRunning = false;

  // Clear canvas
  const canvas = document.getElementById('sevChart');
  if (canvas) canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);

  showToast('Simulation reset. Select a scenario and run again.', 'info', 3000);
}

// ═══════════════════════════════════════════════════════════════
// EXPORT PDF — Dynamic based on scenario
// ═══════════════════════════════════════════════════════════════
function exportPDF() {
  const scenario = SimState.currentScenario;
  const now = new Date().toLocaleString();
  const scoreColor = scenario ? (scenario.score >= 70 ? '#16a34a' : scenario.score >= 40 ? '#d97706' : '#dc2626') : '#d97706';

  const vulnRows = scenario ? scenario.vulns.map(v => `
    <tr>
      <td style="border:1px solid #ddd;padding:6px 10px;font-weight:700;color:${v.sev==='critical'?'#7c3aed':v.sev==='high'?'#dc2626':v.sev==='medium'?'#d97706':'#16a34a'}">${v.sev.toUpperCase()}</td>
      <td style="border:1px solid #ddd;padding:6px 10px;font-weight:600">${v.title}</td>
      <td style="border:1px solid #ddd;padding:6px 10px;font-size:11px">${v.desc.slice(0,120)}...</td>
    </tr>`).join('') : '';

  const reportHtml = `
    <div style="font-family:'Courier New',monospace;padding:32px;color:#111;max-width:900px;margin:0 auto">
      <h1 style="text-align:center;border-bottom:2px solid #333;padding-bottom:12px;font-size:22px">🔒 BIOS/UEFI Security Analysis Report</h1>
      <div style="text-align:center;color:#666;font-size:12px;margin-bottom:24px">
        <p>Generated: ${now} · Simulation Mode · Scenario: ${scenario ? scenario.label : 'N/A'}</p>
        <p>CHIPSEC v1.10.6 Platform Assessment Framework</p>
      </div>
      <h2 style="font-size:16px;margin-top:24px;border-left:4px solid #3b82f6;padding-left:8px">1. Platform Summary</h2>
      <table style="width:100%;border-collapse:collapse;font-size:12px;margin:12px 0">
        <tr><th style="border:1px solid #ddd;padding:6px 10px;text-align:left;background:#f3f4f6">Property</th><th style="border:1px solid #ddd;padding:6px 10px;text-align:left;background:#f3f4f6">Value</th></tr>
        <tr><td style="border:1px solid #ddd;padding:6px 10px">CPU</td><td style="border:1px solid #ddd;padding:6px 10px">Intel Core i7-11700K @ 3.60GHz (8C/16T)</td></tr>
        <tr><td style="border:1px solid #ddd;padding:6px 10px">Scenario</td><td style="border:1px solid #ddd;padding:6px 10px;font-weight:700;color:${scoreColor}">${scenario ? scenario.label : 'N/A'}</td></tr>
        <tr><td style="border:1px solid #ddd;padding:6px 10px">Secure Boot</td><td style="border:1px solid #ddd;padding:6px 10px;color:${scenario&&scenario.secureBoot?'#16a34a':'#dc2626'};font-weight:700">${scenario ? (scenario.secureBoot ? 'ENABLED' : 'DISABLED') : 'N/A'}</td></tr>
        <tr><td style="border:1px solid #ddd;padding:6px 10px">Risk Score</td><td style="border:1px solid #ddd;padding:6px 10px;font-weight:700;color:${scoreColor}">${scenario ? scenario.score + '/100 — ' + scenario.riskLabel : 'N/A'}</td></tr>
      </table>
      <h2 style="font-size:16px;margin-top:24px;border-left:4px solid #3b82f6;padding-left:8px">2. Security Findings</h2>
      <table style="width:100%;border-collapse:collapse;font-size:12px;margin:12px 0">
        <tr><th style="border:1px solid #ddd;padding:6px 10px;text-align:left;background:#f3f4f6">Severity</th><th style="border:1px solid #ddd;padding:6px 10px;text-align:left;background:#f3f4f6">Finding</th><th style="border:1px solid #ddd;padding:6px 10px;text-align:left;background:#f3f4f6">Description</th></tr>
        ${vulnRows}
      </table>
      <h2 style="font-size:16px;margin-top:24px;border-left:4px solid #3b82f6;padding-left:8px">3. Action Items</h2>
      <ol style="font-size:13px;line-height:2">
        ${scenario ? scenario.actionItems.map(a => `<li>${a.text}</li>`).join('') : '<li>Run a simulation first.</li>'}
      </ol>
      <footer style="text-align:center;margin-top:40px;font-size:11px;color:#999;border-top:1px solid #eee;padding-top:12px">BIOS/UEFI Security Analysis Simulator v2.0 · Hardware Security Lab</footer>
    </div>`;

  const script = document.createElement('script');
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
  script.onload = () => {
    const element = document.createElement('div');
    element.innerHTML = reportHtml;
    html2pdf().set({ margin:10, filename:'bios_uefi_security_report.pdf', image:{type:'jpeg',quality:0.98}, html2canvas:{scale:2}, jsPDF:{orientation:'portrait',unit:'mm',format:'a4'} }).from(element).save();
    showToast('PDF report generated. Check your downloads folder.', 'success');
  };
  script.onerror = () => {
    const blob = new Blob([reportHtml], {type:'text/html'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'bios_uefi_security_report.html';
    document.body.appendChild(link);
    link.click();
    link.remove();
    showToast('PDF library unavailable — HTML report downloaded instead.', 'warn');
  };
  document.head.appendChild(script);
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# Build the complete HTML document
# ══════════════════════════════════════════════════════════════════════════════
def build_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BIOS/UEFI Security Analysis Dashboard v2.0</title>
  <style>
{CSS}
  </style>
</head>
<body>
{HTML_BODY}
<script>
{JS}
</script>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PyQt5 Desktop Application
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIOS/UEFI Security Analysis Dashboard v2.0")
        self.resize(1440, 900)
        self.setMinimumSize(900, 600)

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 1440) // 2
        y = (screen.height() - 900) // 2
        self.move(max(0, x), max(0, y))

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        self.web_view.page().profile().downloadRequested.connect(self.handle_download)
        self.web_view.setHtml(build_html(), QUrl("about:blank"))
        self.web_view.page().createWindow = self._create_popup

    def _create_popup(self, win_type):
        popup = QWebEngineView()
        popup.setWindowTitle("BIOS/UEFI Security Report")
        popup.resize(900, 700)
        popup.show()
        return popup.page()

    def handle_download(self, download):
        dl_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation) or os.path.expanduser("~")
        filename = download.downloadFileName() or "bios_uefi_security_report.html"
        path = os.path.join(dl_dir, filename)
        download.setPath(path)
        download.accept()
        print(f"Download saved to: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu-sandbox")
    app = QApplication(sys.argv)
    app.setApplicationName("BIOS/UEFI Security Analyzer v2.0")
    app.setOrganizationName("Hardware Security Lab")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())