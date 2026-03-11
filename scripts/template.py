
# ══════════════════════════════════════
# BUILD HTML — Part 1: Head + CSS
# ══════════════════════════════════════

html_parts = []
html_parts.append(f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PJUS — Inteligência Estratégica de Precatórios</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#F5F7FA;--card:#FFF;--border:#E2E8F0;--border2:#CBD5E1;--accent:#0074FF;--green:#00A68C;--blue:#0074FF;--purple:#0E2F5D;--yellow:#F59E0B;--orange:#F97316;--red:#EF4444;--text:#2B313B;--text2:#475569;--text3:#64748B;--text4:#94A3B8}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:13px}}
.hdr{{padding:14px 32px 8px;background:linear-gradient(135deg,#0E2F5D 0%,#0074FF 100%);color:#fff;display:flex;align-items:center;gap:14px}}
.hdr h1{{font-size:18px;font-weight:700;letter-spacing:-.5px}}
.hdr p{{font-size:10px;color:rgba(255,255,255,.6);margin-top:1px}}
.hdr-right{{margin-left:auto;text-align:right}}
.hdr-right .slogan{{font-size:8px;color:rgba(255,255,255,.4);font-weight:300;letter-spacing:.5px;text-transform:uppercase}}
.hdr-right .update{{font-size:9px;color:rgba(255,255,255,.5);margin-top:1px}}
.tabs{{padding:0 32px;display:flex;gap:0;border-bottom:1px solid var(--border);background:#fff;position:sticky;top:0;z-index:100}}
.tab{{padding:9px 16px;font-size:11px;font-weight:600;color:var(--text3);cursor:pointer;border:none;background:none;border-bottom:2.5px solid transparent;transition:all .12s;white-space:nowrap;display:flex;align-items:center;gap:4px}}
.tab:hover{{color:var(--text2);background:rgba(0,116,255,.02)}}
.tab.on{{color:var(--accent);border-bottom-color:var(--accent)}}
.tab .ico{{font-size:12px}}
.gbar{{padding:7px 32px;display:flex;gap:6px;align-items:center;flex-wrap:wrap;background:#fff;border-bottom:1px solid var(--border);position:sticky;top:38px;z-index:99}}
.gbar .fl{{font-size:8px;color:var(--text4);font-weight:700;text-transform:uppercase;letter-spacing:.6px}}
.gbar select{{padding:4px 8px;border-radius:5px;font-size:10px;font-weight:600;border:1px solid var(--border);background:#fff;color:var(--text2);cursor:pointer;font-family:inherit;max-width:140px}}
.gbar select:focus{{border-color:var(--accent);outline:none}}
/* Multi-select dropdown */
.ms-wrap{{position:relative;display:inline-block;vertical-align:middle}}
.ms-btn{{padding:4px 8px;border-radius:5px;font-size:10px;font-weight:600;border:1px solid var(--border);background:#fff;color:var(--text2);cursor:pointer;font-family:inherit;min-width:80px;max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:3px}}
.ms-btn:hover{{border-color:var(--accent)}}
.ms-btn.active{{border-color:var(--accent);color:var(--accent)}}
.ms-btn .arrow{{font-size:7px;margin-left:auto;transition:transform .15s}}
.ms-btn.open .arrow{{transform:rotate(180deg)}}
.ms-drop{{position:absolute;top:100%;left:0;z-index:200;background:#fff;border:1px solid var(--border);border-radius:6px;box-shadow:0 4px 16px rgba(0,0,0,.1);min-width:160px;max-height:230px;overflow-y:auto;display:none;margin-top:2px}}
.ms-drop.show{{display:block}}
.ms-opt{{display:flex;align-items:center;gap:5px;padding:4px 9px;font-size:10px;cursor:pointer;transition:background .1s}}
.ms-opt:hover{{background:rgba(0,116,255,.05)}}
.ms-opt input{{margin:0;accent-color:var(--accent)}}
.ms-opt label{{cursor:pointer;flex:1;user-select:none}}
.ms-opt.all-opt{{border-bottom:1px solid var(--border);font-weight:700}}
.ms-count{{display:inline-flex;align-items:center;justify-content:center;min-width:14px;height:14px;border-radius:7px;background:var(--accent);color:#fff;font-size:7px;font-weight:800;padding:0 3px}}
.gbar .sep{{width:1px;height:18px;background:var(--border2);margin:0 3px}}
.gbar .filter-info{{margin-left:auto;font-size:9px;color:var(--text4)}}
.gbar .filter-info strong{{color:var(--accent)}}
.gbar .btn-clear{{padding:3px 10px;border-radius:5px;font-size:9px;font-weight:600;border:1px solid var(--border);background:transparent;color:var(--text3);cursor:pointer}}
.gbar .btn-clear:hover{{border-color:var(--red);color:var(--red)}}
.ct{{padding:12px 32px 40px;max-width:1800px;margin:0 auto}}
/* Tab objective header */
.tab-obj{{background:linear-gradient(135deg,rgba(14,47,93,.03),rgba(0,116,255,.03));border:1px solid rgba(0,116,255,.1);border-radius:9px;padding:10px 16px;margin-bottom:14px;display:flex;align-items:center;gap:10px}}
.tab-obj .obj-ico{{font-size:22px}}
.tab-obj h2{{font-size:13px;font-weight:700;color:var(--purple)}}
.tab-obj p{{font-size:10px;color:var(--text3);margin-top:2px;line-height:1.4}}
/* Drill-down indicator */
.drill-active{{border:2px solid var(--accent)!important;box-shadow:0 0 0 3px rgba(0,116,255,.1)!important}}
.drill-bar{{display:none;padding:6px 16px;background:rgba(0,116,255,.06);border-radius:6px;margin-bottom:10px;font-size:10px;color:var(--accent);font-weight:600;align-items:center;gap:6px}}
.drill-bar.show{{display:flex}}
.drill-bar .drill-clear{{cursor:pointer;padding:2px 8px;border-radius:4px;border:1px solid var(--accent);background:transparent;color:var(--accent);font-size:9px;font-weight:700;margin-left:auto}}
.drill-bar .drill-clear:hover{{background:rgba(0,116,255,.1)}}
.st{{font-size:12px;font-weight:700;margin:16px 0 8px;padding-bottom:4px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:5px}}
.st .ico{{font-size:13px}}
.st:first-child{{margin-top:0}}
.krow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:9px;margin-bottom:12px}}
.kc{{background:var(--card);border:1px solid var(--border);border-radius:9px;padding:11px 13px;position:relative;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.03)}}
.kc::before{{content:'';position:absolute;top:0;left:0;right:0;height:2.5px}}
.kc.kg::before{{background:var(--green)}}.kc.kb::before{{background:var(--blue)}}.kc.ky::before{{background:var(--yellow)}}.kc.kr::before{{background:var(--red)}}.kc.kp::before{{background:var(--purple)}}.kc.ko::before{{background:var(--orange)}}
.kc-label{{font-size:8px;color:var(--text4);text-transform:uppercase;letter-spacing:.5px;font-weight:700}}
.kc-val{{font-size:20px;font-weight:800;margin:3px 0 1px;letter-spacing:-.7px;line-height:1}}
.kc-sub{{font-size:8px;color:var(--text4)}}
.row2{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}}
.row3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px}}
.row1{{margin-bottom:10px}}
.cd{{background:var(--card);border:1px solid var(--border);border-radius:9px;padding:12px 16px;box-shadow:0 1px 2px rgba(0,0,0,.03);transition:border-color .15s,box-shadow .15s}}
.cd h3{{font-size:11px;font-weight:700;margin-bottom:1px;display:flex;align-items:center;gap:4px}}
.cd .sub{{font-size:8px;color:var(--text4);margin-bottom:8px}}
.cw{{position:relative;width:100%}}
.cw canvas{{width:100%!important;cursor:pointer}}
.tw{{overflow-x:auto;border-radius:5px;border:1px solid var(--border);max-height:350px;overflow-y:auto}}
table{{width:100%;border-collapse:collapse;font-size:10px}}
th{{background:#F8FAFC;padding:5px 7px;text-align:left;font-weight:600;font-size:8px;text-transform:uppercase;letter-spacing:.4px;color:var(--text3);white-space:nowrap;position:sticky;top:0;z-index:1}}
td{{padding:4px 7px;border-bottom:1px solid var(--border);white-space:nowrap}}
tr:hover td{{background:rgba(0,116,255,.02)}}
.bd{{display:inline-block;padding:1px 6px;border-radius:3px;font-size:8px;font-weight:700}}
.bg{{background:rgba(0,166,140,.12);color:var(--green)}}.br{{background:rgba(239,68,68,.12);color:var(--red)}}.by{{background:rgba(245,158,11,.12);color:var(--yellow)}}.bb{{background:rgba(0,116,255,.12);color:var(--blue)}}.bp{{background:rgba(14,47,93,.1);color:var(--purple)}}
.score-pill{{display:inline-flex;align-items:center;justify-content:center;width:22px;height:16px;border-radius:3px;font-size:9px;font-weight:800}}
.s5{{background:linear-gradient(135deg,#00A68C,#059669);color:#fff}}.s4{{background:rgba(0,116,255,.15);color:#0074FF}}.s3{{background:rgba(245,158,11,.15);color:#D97706}}.s2{{background:rgba(100,116,139,.12);color:#64748B}}.s1{{background:rgba(100,116,139,.08);color:#94A3B8}}
.prio-badge{{padding:1px 7px;border-radius:8px;font-size:8px;font-weight:700}}
.p-max{{background:linear-gradient(135deg,#00A68C,#059669);color:#fff}}.p-alta{{background:rgba(0,116,255,.12);color:#0074FF}}.p-media{{background:rgba(245,158,11,.12);color:#D97706}}.p-baixa{{background:rgba(100,116,139,.1);color:#64748B}}.p-min{{background:rgba(100,116,139,.06);color:#94A3B8}}
.rn{{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;border-radius:4px;font-size:8px;font-weight:800}}
.r1{{background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#000}}.r2{{background:linear-gradient(135deg,#94a3b8,#64748b);color:#fff}}.r3{{background:linear-gradient(135deg,#d97706,#b45309);color:#fff}}.rx{{background:var(--border);color:var(--text4)}}
.pb{{width:45px;height:3px;background:rgba(0,0,0,.05);border-radius:2px;overflow:hidden;display:inline-block;vertical-align:middle;margin-right:3px}}
.pf{{height:100%;border-radius:2px}}
.prio-box{{background:linear-gradient(135deg,rgba(0,116,255,.04),rgba(0,166,140,.04));border:1px solid rgba(0,116,255,.15);border-radius:9px;padding:12px 16px;margin-bottom:12px}}
.prio-box h4{{font-size:11px;font-weight:700;color:var(--purple);margin-bottom:6px;display:flex;align-items:center;gap:5px}}
.prio-box .prio-item{{display:flex;align-items:flex-start;gap:6px;padding:4px 0;font-size:10px;color:var(--text2);line-height:1.4}}
.prio-box .prio-item:not(:last-child){{border-bottom:1px solid rgba(0,116,255,.08);padding-bottom:6px;margin-bottom:2px}}
.prio-dot{{width:6px;height:6px;border-radius:50%;margin-top:4px;flex-shrink:0}}
.prio-dot.high{{background:var(--red)}}.prio-dot.med{{background:var(--yellow)}}.prio-dot.low{{background:var(--green)}}
.alert-row{{display:flex;align-items:center;gap:6px;padding:5px 8px;border-bottom:1px solid var(--border);font-size:9px}}
.alert-row:last-child{{border-bottom:none}}
.alert-row:hover{{background:rgba(0,116,255,.02)}}
.alert-tipo{{font-size:8px;font-weight:700;min-width:120px}}
.gloss-section{{margin-bottom:20px}}
.gloss-section h3{{font-size:13px;font-weight:700;color:var(--purple);margin-bottom:8px;padding-bottom:4px;border-bottom:2px solid var(--accent)}}
.gloss-table{{width:100%;border-collapse:collapse;font-size:11px}}
.gloss-table th{{background:var(--purple);color:#fff;padding:8px 12px;text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.5px}}
.gloss-table td{{padding:7px 12px;border-bottom:1px solid var(--border);vertical-align:top}}
.gloss-table tr:hover td{{background:rgba(0,116,255,.03)}}
.gloss-note{{background:rgba(245,158,11,.08);border-left:3px solid var(--yellow);padding:10px 14px;border-radius:0 6px 6px 0;margin:10px 0;font-size:10px;color:var(--text2);line-height:1.5}}
.btn-export{{padding:6px 14px;border-radius:6px;font-size:10px;font-weight:700;border:1px solid var(--accent);background:rgba(0,116,255,.05);color:var(--accent);cursor:pointer;transition:all .12s;margin-bottom:10px}}
.btn-export:hover{{background:rgba(0,116,255,.12)}}
/* PJUS Performance badge */
.pjus-perf{{display:inline-flex;align-items:center;gap:3px;padding:2px 7px;border-radius:4px;font-size:8px;font-weight:700}}
.pjus-up{{background:rgba(0,166,140,.1);color:#00A68C}}.pjus-down{{background:rgba(239,68,68,.1);color:#EF4444}}.pjus-neutral{{background:rgba(100,116,139,.08);color:#64748B}}
.hidden{{display:none!important}}
@media(max-width:1200px){{.krow{{grid-template-columns:repeat(3,1fr)}}.row3{{grid-template-columns:1fr 1fr}}}}
@media(max-width:900px){{.krow{{grid-template-columns:repeat(2,1fr)}}.row2,.row3{{grid-template-columns:1fr}}.ct{{padding:8px 14px}}.gbar{{padding:6px 14px;gap:4px}}}}
</style>
</head>
<body>

<div class="hdr">
  {LOGO}
  <div>
    <h1>Inteligência Estratégica de Precatórios</h1>
    <p>Base Argus · diarios_analise · djen_precatorio · {len(TRIBS)} tribunais · Base Compras PJUS 2024-2026</p>
  </div>
  <div class="hdr-right">
    <div class="slogan">Liquidez com Segurança Jurídica</div>
    <div class="update">Atualizado {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
  </div>
</div>

<div class="tabs" id="mainTabs">
  <button class="tab on" onclick="sw('intel')"><span class="ico">📊</span> Inteligência de Mercado</button>
  <button class="tab" onclick="sw('prosp')"><span class="ico">🎯</span> Prospecção Comercial</button>
  <button class="tab" onclick="sw('pipe')"><span class="ico">⚡</span> Pipeline</button>
  <button class="tab" onclick="sw('report')"><span class="ico">📋</span> Relatórios</button>
  <button class="tab" onclick="sw('pjus')"><span class="ico">🏢</span> Performance PJUS</button>
  <button class="tab" onclick="sw('gloss')"><span class="ico">📖</span> Glossário</button>
</div>

<div class="gbar">
  <span class="fl">Ano:</span>
  <div class="ms-wrap" id="msY"></div>
  <span class="fl">Mês:</span>
  <div class="ms-wrap" id="msM"></div>
  <div class="sep"></div>
  <span class="fl" id="lbT">Tribunal:</span>
  <div class="ms-wrap" id="msT"></div>
  <span class="fl" id="lbF">Fase:</span>
  <div class="ms-wrap" id="msF"></div>
  <span class="fl" id="lbMat">Maturidade:</span>
  <div class="ms-wrap" id="msMat"></div>
  <div class="sep" id="sepScore"></div>
  <span class="fl" id="lbS">Score:</span>
  <div class="ms-wrap" id="msS"></div>
  <div class="sep"></div>
  <button class="btn-clear" onclick="clearF()">Limpar Filtros</button>
  <div class="filter-info" id="fInfo"></div>
</div>
''')
print("Part 1 CSS/Header OK")

# ══════════════════════════════════════
# Part 2: HTML Body — Tab content
# ══════════════════════════════════════
html_parts.append('''
<div class="ct">

<div id="v-intel">
  <div class="tab-obj"><div class="obj-ico">📊</div><div><h2>Inteligência de Mercado</h2><p>Visão panorâmica do mercado de precatórios: ranking de entes devedores por volume e valor, tendências por tribunal e volume diário de publicações. Use para identificar concentrações de mercado e oportunidades regionais.</p></div></div>
  <div id="kI" class="krow"></div>
  <div id="drillIntel" class="drill-bar">🔍 Drill-down ativo: <span id="drillIntelLabel"></span><button class="drill-clear" onclick="clearDrill('intel')">✕ Limpar</button></div>
  <div id="prioIntel" class="prio-box"></div>
  <div class="st"><span class="ico">🏛️</span> Ranking Entes Devedores</div>
  <div class="row2">
    <div class="cd" id="cdEV"><h3>Top 10 por Valor</h3><div class="sub">R$ Milhões acumulados · Clique para filtrar</div><div class="cw" style="height:280px"><canvas id="cEV"></canvas></div></div>
    <div class="cd" id="cdEVo"><h3>Top 10 por Volume</h3><div class="sub">Publicações classificadas · Clique para filtrar</div><div class="cw" style="height:280px"><canvas id="cEVo"></canvas></div></div>
  </div>
  <div class="cd row1"><h3>Tabela Completa</h3><div class="tw" id="tE"></div></div>
  <div class="st"><span class="ico">📈</span> Tendência por Tribunal</div>
  <div class="cd row1"><div class="cw" style="height:280px"><canvas id="cTr"></canvas></div></div>
  <div class="st"><span class="ico">📅</span> Volume Diário</div>
  <div class="cd row1"><div class="cw" style="height:260px"><canvas id="cDa"></canvas></div></div>
</div>

<div id="v-prosp" class="hidden">
  <div class="tab-obj"><div class="obj-ico">🎯</div><div><h2>Prospecção Comercial</h2><p>Identificação e qualificação de oportunidades de aquisição de créditos. Filtra publicações com alta relevância (score ≥ 3), mapeia beneficiários e advogados recorrentes, e prioriza ações comerciais por valor e maturidade.</p></div></div>
  <div id="kP" class="krow"></div>
  <div id="drillProsp" class="drill-bar">🔍 Drill-down ativo: <span id="drillProspLabel"></span><button class="drill-clear" onclick="clearDrill('prosp')">✕ Limpar</button></div>
  <div id="prioProsp" class="prio-box"></div>
  <div class="st"><span class="ico">💎</span> Oportunidades Score ≥ 3</div>
  <div class="row2">
    <div class="cd" id="cdSD"><h3>Por Score</h3><div class="sub">Clique para filtrar por score</div><div class="cw" style="height:190px"><canvas id="cSD"></canvas></div></div>
    <div class="cd" id="cdFV"><h3>Valor por Fase (R$ Mi)</h3><div class="sub">Clique para filtrar por fase</div><div class="cw" style="height:190px"><canvas id="cFV"></canvas></div></div>
  </div>
  <div class="cd row1"><h3>Oportunidades</h3><div class="tw" id="tO"></div></div>
  <div class="st"><span class="ico">👤</span> Beneficiários Recorrentes</div>
  <div class="cd row1"><div class="tw" id="tB"></div></div>
  <div class="st"><span class="ico">⚖️</span> Advogados Recorrentes</div>
  <div class="cd row1"><div class="tw" id="tA"></div></div>
</div>

<div id="v-pipe" class="hidden">
  <div class="tab-obj"><div class="obj-ico">⚡</div><div><h2>Análise de Pipeline</h2><p>Mapeamento das fases processuais e maturidade dos precatórios monitorados. Permite avaliar a saúde do pipeline, identificar gargalos por fase e priorizar os ativos mais próximos à liquidez para ação comercial imediata.</p></div></div>
  <div id="kPi" class="krow"></div>
  <div id="drillPipe" class="drill-bar">🔍 Drill-down ativo: <span id="drillPipeLabel"></span><button class="drill-clear" onclick="clearDrill('pipe')">✕ Limpar</button></div>
  <div id="prioPipe" class="prio-box"></div>
  <div class="st"><span class="ico">🔄</span> Fases Processuais</div>
  <div class="row2">
    <div class="cd" id="cdPV"><h3>Volume por Fase</h3><div class="sub">Clique para drill-down</div><div class="cw" style="height:270px"><canvas id="cPV"></canvas></div></div>
    <div class="cd" id="cdPB"><h3>Score × Dias × Valor</h3><div class="sub">Bubble: tamanho = valor</div><div class="cw" style="height:270px"><canvas id="cPB"></canvas></div></div>
  </div>
  <div class="cd row1"><h3>Detalhamento</h3><div class="tw" id="tPi"></div></div>
  <div class="st"><span class="ico">🏆</span> Top Oportunidades Priorizadas</div>
  <div class="cd row1"><div class="tw" id="tTO"></div></div>
</div>

<div id="v-report" class="hidden">
  <div class="tab-obj"><div class="obj-ico">📋</div><div><h2>Relatórios Periódicos</h2><p>Consolidação analítica para reporting executivo: heatmap de volume por tribunal, distribuição de valores por faixa, alertas prioritários e base exportável para análises complementares em Excel.</p></div></div>
  <div id="kR" class="krow"></div>
  <div id="drillReport" class="drill-bar">🔍 Drill-down ativo: <span id="drillReportLabel"></span><button class="drill-clear" onclick="clearDrill('report')">✕ Limpar</button></div>
  <div id="prioReport" class="prio-box"></div>
  <div class="st"><span class="ico">📊</span> Heatmap por Tribunal</div>
  <div class="cd row1"><div class="tw" id="tH"></div></div>
  <div class="st"><span class="ico">💰</span> Distribuição de Valores</div>
  <div class="row2">
    <div class="cd" id="cdFxV"><h3>Volume por Faixa</h3><div class="sub">Clique para filtrar</div><div class="cw" style="height:220px"><canvas id="cFxV"></canvas></div></div>
    <div class="cd" id="cdFxVl"><h3>Valor por Faixa</h3><div class="sub">Clique para filtrar</div><div class="cw" style="height:220px"><canvas id="cFxVl"></canvas></div></div>
  </div>
  <div class="cd row1"><div class="tw" id="tFx"></div></div>
  <div class="st"><span class="ico">🚨</span> Alertas</div>
  <button class="btn-export" onclick="exportCSV()">⬇ Exportar Alertas em CSV</button>
  <div class="cd row1"><div class="tw" id="alC"></div></div>
  <div class="st"><span class="ico">📥</span> Base Analítica — Exportável</div>
  <button class="btn-export" onclick="exportFullCSV()">⬇ Exportar Base Completa em CSV</button>
  <div class="cd row1"><div class="tw" id="tAnalytic" style="max-height:300px"></div></div>
</div>

<div id="v-pjus" class="hidden">
  <div class="tab-obj"><div class="obj-ico">🏢</div><div><h2>Performance PJUS — Compras de Créditos</h2><p>Análise da produção real de compras da PJUS (Jan/2024 a Fev/2026): evolução mensal de processos adquiridos, valor de face e valor desembolsado, distribuição por tribunal, esfera e órgão pagador. Cruzamento com dados de mercado para avaliar penetração e oportunidades de crescimento.</p></div></div>
  <div id="kPJ" class="krow"></div>
  <div id="drillPjus" class="drill-bar">🔍 Drill-down ativo: <span id="drillPjusLabel"></span><button class="drill-clear" onclick="clearDrill('pjus')">✕ Limpar</button></div>
  <div id="prioPjus" class="prio-box"></div>
  <div class="st"><span class="ico">📈</span> Evolução Mensal de Compras</div>
  <div class="row2">
    <div class="cd" id="cdPjM"><h3>Processos Comprados / Mês</h3><div class="sub">Clique para drill-down</div><div class="cw" style="height:240px"><canvas id="cPjM"></canvas></div></div>
    <div class="cd" id="cdPjV"><h3>Valor de Face Adquirido / Mês</h3><div class="sub">R$ Milhões · Clique para drill-down</div><div class="cw" style="height:240px"><canvas id="cPjV"></canvas></div></div>
  </div>
  <div class="st"><span class="ico">🏛️</span> Distribuição por Tribunal</div>
  <div class="row2">
    <div class="cd" id="cdPjT"><h3>Valor de Face por Tribunal</h3><div class="sub">Clique para drill-down</div><div class="cw" style="height:260px"><canvas id="cPjT"></canvas></div></div>
    <div class="cd" id="cdPjE"><h3>Distribuição por Esfera</h3><div class="sub">Clique para drill-down</div><div class="cw" style="height:260px"><canvas id="cPjE"></canvas></div></div>
  </div>
  <div class="cd row1"><h3>Detalhamento por Tribunal</h3><div class="tw" id="tPjT"></div></div>
  <div class="st"><span class="ico">🏦</span> Top Órgãos Pagadores</div>
  <div class="cd row1"><div class="tw" id="tPjO"></div></div>
</div>
''')
print("Part 2 Body OK")

# Glossary tab HTML
html_parts.append('''
<div id="v-gloss" class="hidden">
  <div class="tab-obj"><div class="obj-ico">📖</div><div><h2>Glossário & Premissas Metodológicas</h2><p>Documentação das premissas utilizadas em todos os indicadores: metodologia de score, classificação de maturidade, fórmula de priorização, fontes de dados e definições de filtros. Referência obrigatória para interpretação dos dados.</p></div></div>
  <div class="gloss-section">
    <h3>Metodologia de Score — Relevância para Negócios</h3>
    <div class="gloss-note"><strong>Premissa:</strong> O score de relevância (1-5) é atribuído por IA (Gemini 2.5 Flash-Lite) com base no conteúdo da publicação. Reflete o potencial de conversão em oportunidade de aquisição de crédito pela PJUS.</div>
    <table class="gloss-table">
      <thead><tr><th>Score</th><th>Classificação</th><th>Critérios</th><th>Ação</th></tr></thead>
      <tbody>
        <tr><td><span class="score-pill s5">5</span></td><td><strong>Máxima</strong></td><td>Precatório com valor definido, fase de pagamento iminente, beneficiário identificado, sem impedimentos.</td><td>Contato imediato.</td></tr>
        <tr><td><span class="score-pill s4">4</span></td><td><strong>Alta</strong></td><td>Precatório expedido ou cessão homologada. Valor estimável, partes identificadas.</td><td>Priorizar em até 7 dias.</td></tr>
        <tr><td><span class="score-pill s3">3</span></td><td><strong>Moderada</strong></td><td>Fase intermediária. Valor pode não estar definido.</td><td>Monitorar evolução.</td></tr>
        <tr><td><span class="score-pill s2">2</span></td><td><strong>Baixa</strong></td><td>Referência genérica, fase inicial ou embargos pendentes.</td><td>Monitoramento passivo.</td></tr>
        <tr><td><span class="score-pill s1">1</span></td><td><strong>Mínima</strong></td><td>Menção tangencial, dados insuficientes.</td><td>Desconsiderar para fins comerciais.</td></tr>
      </tbody>
    </table>
  </div>
  <div class="gloss-section">
    <h3>Classificação de Maturidade</h3>
    <div class="gloss-note"><strong>Premissa:</strong> Derivada da fase processual. Quanto mais avançada, maior a maturidade e menor o risco.</div>
    <table class="gloss-table">
      <thead><tr><th>Maturidade</th><th>Fases</th><th>Significado</th><th>Dias Médios</th></tr></thead>
      <tbody>
        <tr><td><span class="bd bg">Muito Alta</span></td><td>Pagamento Iminente</td><td>Em fila de pagamento, sem bloqueios.</td><td>15 dias</td></tr>
        <tr><td><span class="bd bg">Alta</span></td><td>Prec. Expedido, Cessão</td><td>Crédito formalizado, documentação disponível.</td><td>45-60 dias</td></tr>
        <tr><td><span class="bd by">Média-Alta</span></td><td>Habilitação</td><td>Habilitação em andamento.</td><td>90 dias</td></tr>
        <tr><td><span class="bd by">Média</span></td><td>Ofício Req., Homologação</td><td>Fase intermediária.</td><td>75-120 dias</td></tr>
        <tr><td><span class="bd bb">Média-Baixa</span></td><td>Atualização de Valores</td><td>Valor final não consolidado.</td><td>30 dias (pós)</td></tr>
        <tr><td><span class="bd br">Baixa</span></td><td>Embargos, Liquidação</td><td>Risco processual elevado.</td><td>150-180 dias</td></tr>
        <tr><td><span class="bd br">Muito Baixa</span></td><td>Outros</td><td>Sem classificação precisa.</td><td>200+ dias</td></tr>
      </tbody>
    </table>
  </div>
  <div class="gloss-section">
    <h3>Índice de Priorização</h3>
    <div class="gloss-note"><strong>Fórmula:</strong> <code>Índice = Score × (Valor / R$ 1M) / (1 + Dias / 100)</code><br><br>Combina relevância, magnitude financeira e urgência. <u>Não é ROI</u> — é métrica de priorização operacional.</div>
  </div>
  <div class="gloss-section">
    <h3>Dados PJUS — Base de Compras</h3>
    <div class="gloss-note"><strong>Fonte:</strong> Base de compras PJUS (Jan/2024 a Fev/2026), 4.798 processos adquiridos.<br><br><strong>Valor de Face:</strong> Valor nominal do precatório no momento da aquisição — comparável com valores publicados no DJEN.<br><strong>Valor Desembolsado (Valor Presente):</strong> Valor efetivamente pago ao credor na aquisição.<br><strong>Valor Líquido a Receber (Líq. Ofício Acordo Ajustado):</strong> Valor esperado a receber pelo crédito, considerando TIR real do precatório.</div>
  </div>
  <div class="gloss-section">
    <h3>Fontes de Dados</h3>
    <table class="gloss-table">
      <thead><tr><th>Fonte</th><th>Descrição</th><th>Volume</th><th>Frequência</th></tr></thead>
      <tbody>
        <tr><td><strong>DJEN</strong></td><td>Diário de Justiça Eletrônico Nacional — 38 tribunais</td><td>~17.000 pub./dia</td><td>Diária</td></tr>
        <tr><td><strong>Diários Estaduais</strong></td><td>12 diários oficiais estaduais</td><td>~20.000 pub./dia</td><td>Diária</td></tr>
        <tr><td><strong>IA</strong></td><td>Gemini 2.5 Flash-Lite — classificação</td><td>100%</td><td>Tempo real</td></tr>
        <tr><td><strong>Base PJUS</strong></td><td>Histórico de compras de créditos PJUS</td><td>4.798 processos</td><td>Jan/24-Fev/26</td></tr>
      </tbody>
    </table>
  </div>
  <div class="gloss-section">
    <h3>Definições dos Filtros</h3>
    <table class="gloss-table">
      <thead><tr><th>Filtro</th><th>Descrição</th><th>Efeito</th></tr></thead>
      <tbody>
        <tr><td><strong>Ano / Mês</strong></td><td>Período temporal</td><td>Filtra todos os dados em todas as abas</td></tr>
        <tr><td><strong>Tribunal</strong></td><td>Tribunal de origem</td><td>Restringe ao tribunal selecionado</td></tr>
        <tr><td><strong>Fase</strong></td><td>Etapa processual</td><td>Foca em uma fase do pipeline</td></tr>
        <tr><td><strong>Maturidade</strong></td><td>Derivada da fase</td><td>Isola por proximidade à liquidez</td></tr>
      </tbody>
    </table>
  </div>
</div>

</div>
''')
print("Part 2b Glossary OK")

# ══════════════════════════════════════
# Part 3: JavaScript
# ══════════════════════════════════════
html_parts.append(f'''<script>
const ENTES={json.dumps(ENTES,ensure_ascii=False)};
const FONTES={json.dumps(FONTES)};
const DAILY={json.dumps(DAILY,ensure_ascii=False)};
const MI={json.dumps(MESES_IDX,ensure_ascii=False)};
const TRIBS={json.dumps(TRIBS)};
const TREND={json.dumps(TREND,ensure_ascii=False)};
const OPPS={json.dumps(OPPS,ensure_ascii=False)};
const BENEFS={json.dumps(BENEFS,ensure_ascii=False)};
const ADV_DATA={json.dumps(ADV_DATA,ensure_ascii=False)};
const PIPELINE={json.dumps(PIPELINE,ensure_ascii=False)};
const TOP_OPPS={json.dumps(TOP_OPPS,ensure_ascii=False)};
const FAIXAS={json.dumps(FAIXAS,ensure_ascii=False)};
const ALERTS={json.dumps(ALERTS,ensure_ascii=False)};
const ALL_FASES={json.dumps(FASES,ensure_ascii=False)};
const ALL_MATS={json.dumps(MATS,ensure_ascii=False)};
const PJUS_M={json.dumps(PJUS['monthly'],ensure_ascii=False)};
const PJUS_T={json.dumps(PJUS['trib'],ensure_ascii=False)};
const PJUS_E={json.dumps(PJUS['esfera'],ensure_ascii=False)};
const PJUS_TM={json.dumps(PJUS['trib_month'],ensure_ascii=False)};
const PJUS_O={json.dumps(PJUS['orgao'],ensure_ascii=False)};
const PJUS_S={json.dumps(PJUS['stats'],ensure_ascii=False)};

// ═══ MULTI-SELECT SYSTEM ═══
function createMS(containerId,label,options){{
  // options: [{{value,text}}]
  const wrap=document.getElementById(containerId);
  const btn=document.createElement('div');btn.className='ms-btn';btn.innerHTML=label+' <span class="arrow">▼</span>';
  const drop=document.createElement('div');drop.className='ms-drop';
  // "All" option
  const allOpt=document.createElement('div');allOpt.className='ms-opt all-opt';
  allOpt.innerHTML='<input type="checkbox" checked id="'+containerId+'_all"><label>Todos</label>';
  drop.appendChild(allOpt);
  options.forEach(o=>{{
    const opt=document.createElement('div');opt.className='ms-opt';
    opt.innerHTML='<input type="checkbox" value="'+o.value+'" id="'+containerId+'_'+o.value+'"><label>'+o.text+'</label>';
    drop.appendChild(opt);
  }});
  wrap.appendChild(btn);wrap.appendChild(drop);
  // Toggle
  btn.onclick=function(e){{e.stopPropagation();
    document.querySelectorAll('.ms-drop.show').forEach(d=>{{if(d!==drop)d.classList.remove('show')}});
    document.querySelectorAll('.ms-btn.open').forEach(b=>{{if(b!==btn)b.classList.remove('open')}});
    drop.classList.toggle('show');btn.classList.toggle('open');
  }};
  // Checkbox logic
  drop.addEventListener('change',function(e){{
    const cb=e.target;const allCb=drop.querySelector('.all-opt input');
    if(cb===allCb){{
      drop.querySelectorAll('.ms-opt:not(.all-opt) input').forEach(c=>c.checked=false);
      allCb.checked=true;
    }}else{{
      allCb.checked=false;
      const checked=drop.querySelectorAll('.ms-opt:not(.all-opt) input:checked');
      if(checked.length===0)allCb.checked=true;
    }}
    updateMSLabel(containerId,label,btn,drop);
    onF();
  }});
  // Click on label also toggles checkbox
  drop.querySelectorAll('.ms-opt label').forEach(l=>{{
    l.onclick=function(e){{e.preventDefault();const cb=this.parentNode.querySelector('input');cb.checked=!cb.checked;cb.dispatchEvent(new Event('change',{{bubbles:true}}))}};
  }});
  wrap._drop=drop;wrap._btn=btn;wrap._label=label;
}}
function updateMSLabel(containerId,label,btn,drop){{
  const allCb=drop.querySelector('.all-opt input');
  if(allCb.checked){{btn.innerHTML=label+' <span class="arrow">▼</span>';btn.classList.remove('active');return}}
  const checked=[...drop.querySelectorAll('.ms-opt:not(.all-opt) input:checked')];
  const n=checked.length;
  if(n===1){{btn.innerHTML=checked[0].parentNode.querySelector('label').textContent+' <span class="arrow">▼</span>';btn.classList.add('active')}}
  else if(n>1){{btn.innerHTML=n+' selecionados <span class="arrow">▼</span>';btn.classList.add('active')}}
}}
function getMSValues(containerId){{
  const wrap=document.getElementById(containerId);if(!wrap||!wrap._drop)return 'all';
  const allCb=wrap._drop.querySelector('.all-opt input');
  if(allCb.checked)return 'all';
  const vals=[...wrap._drop.querySelectorAll('.ms-opt:not(.all-opt) input:checked')].map(c=>c.value);
  return vals.length===0?'all':new Set(vals);
}}
function resetMS(containerId){{
  const wrap=document.getElementById(containerId);if(!wrap||!wrap._drop)return;
  const allCb=wrap._drop.querySelector('.all-opt input');allCb.checked=true;
  wrap._drop.querySelectorAll('.ms-opt:not(.all-opt) input').forEach(c=>c.checked=false);
  updateMSLabel(containerId,wrap._label,wrap._btn,wrap._drop);
}}
function setMSSingle(containerId,value){{
  const wrap=document.getElementById(containerId);if(!wrap||!wrap._drop)return;
  const allCb=wrap._drop.querySelector('.all-opt input');allCb.checked=false;
  wrap._drop.querySelectorAll('.ms-opt:not(.all-opt) input').forEach(c=>{{c.checked=(c.value==value)}});
  updateMSLabel(containerId,wrap._label,wrap._btn,wrap._drop);
}}
// Close dropdowns on outside click
document.addEventListener('click',function(){{document.querySelectorAll('.ms-drop.show').forEach(d=>d.classList.remove('show'));document.querySelectorAll('.ms-btn.open').forEach(b=>b.classList.remove('open'))}});

(function(){{
  createMS('msY','Todos',[{{value:'2024',text:'2024'}},{{value:'2025',text:'2025'}},{{value:'2026',text:'2026'}}]);
  createMS('msM','Todos',[{{value:'1',text:'Jan'}},{{value:'2',text:'Fev'}},{{value:'3',text:'Mar'}},{{value:'4',text:'Abr'}},{{value:'5',text:'Mai'}},{{value:'6',text:'Jun'}},{{value:'7',text:'Jul'}},{{value:'8',text:'Ago'}},{{value:'9',text:'Set'}},{{value:'10',text:'Out'}},{{value:'11',text:'Nov'}},{{value:'12',text:'Dez'}}]);
  createMS('msT','Todos',TRIBS.map(t=>({{value:t,text:t}})));
  createMS('msF','Todas',ALL_FASES.map(f=>({{value:f,text:f}})));
  createMS('msMat','Todas',ALL_MATS.map(m=>({{value:m,text:m}})));
  createMS('msS','Todos',[{{value:'5',text:'5 — Máxima'}},{{value:'4',text:'4 — Alta'}},{{value:'3',text:'3 — Moderada'}},{{value:'2',text:'2 — Baixa'}},{{value:'1',text:'1 — Mínima'}}]);
}})();

const ch={{}};function dc(id){{if(ch[id]){{ch[id].destroy();delete ch[id]}}}}
function Fv(v){{return 'R$ '+v.toLocaleString('pt-BR',{{minimumFractionDigits:1,maximumFractionDigits:1}})+'M'}}
function Fr(v){{return 'R$ '+v.toLocaleString('pt-BR',{{maximumFractionDigits:0}})}}
function Fn(v){{return v.toLocaleString('pt-BR')}}
function sC(s){{return s>=5?'s5':s>=4?'s4':s>=3?'s3':s>=2?'s2':'s1'}}
function rC(i){{return i===0?'r1':i===1?'r2':i===2?'r3':'rx'}}
const C10=['#0074FF','#0E2F5D','#00A68C','#F59E0B','#F97316','#EF4444','#8B5CF6','#06B6D4','#EC4899','#64748B'];

let fY='all',fM='all',fT='all',fF='all',fMat='all',fS='all',curTab='intel';
// Drill-down state per tab
const drill={{}};

function _m(fv,rv){{if(fv==='all')return true;return fv.has(String(rv))}}
function gf(arr){{
  return arr.filter(r=>
    (fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))
    &&(fT==='all'||!r.trib||_m(fT,r.trib))
    &&(fF==='all'||!r.fase||_m(fF,r.fase))
    &&(fMat==='all'||!r.mat||_m(fMat,r.mat))
    &&(fS==='all'||(!r.score&&r.score!==0&&!r.scoreN&&r.scoreN!==0)||(r.score!=null&&_m(fS,Math.round(r.score)))||(r.scoreN!=null&&_m(fS,Math.round(r.scoreN))))
  )}}
function gfmi(){{return MI.filter(mi=>(fY==='all'||_m(fY,mi.y))&&(fM==='all'||_m(fM,mi.m)))}}

function _desc(fv,names){{if(fv==='all')return null;const arr=[...fv];if(names)return arr.map(v=>names[v]||v).join(', ');return arr.join(', ')}}
function onF(){{
  fY=getMSValues('msY');fM=getMSValues('msM');
  fT=getMSValues('msT');fF=getMSValues('msF');
  fMat=getMSValues('msMat');fS=getMSValues('msS');
  const parts=[];const mNames={{'1':'Jan','2':'Fev','3':'Mar','4':'Abr','5':'Mai','6':'Jun','7':'Jul','8':'Ago','9':'Set','10':'Out','11':'Nov','12':'Dez'}};
  let d;
  if((d=_desc(fY))!==null) parts.push(d);
  if((d=_desc(fM,mNames))!==null) parts.push(d);
  if((d=_desc(fT))!==null) parts.push(d);
  if((d=_desc(fF))!==null) parts.push(d);
  if((d=_desc(fMat))!==null) parts.push('Mat: '+d);
  if((d=_desc(fS))!==null) parts.push('Score: '+d);
  document.getElementById('fInfo').innerHTML=parts.length?'Filtros: <strong>'+parts.join(' · ')+'</strong>':'<strong>Todos os dados</strong>';
  render();
}}
function clearF(){{
  ['msY','msM','msT','msF','msMat','msS'].forEach(id=>resetMS(id));
  fY=fM=fT=fF=fMat=fS='all';
  document.getElementById('fInfo').innerHTML='<strong>Todos os dados</strong>';
  render();
}}
function sw(tab){{
  curTab=tab;const ids=['intel','prosp','pipe','report','pjus','gloss'];
  document.querySelectorAll('#mainTabs .tab').forEach((t,i)=>t.classList.toggle('on',ids[i]===tab));
  ids.forEach(id=>{{const el=document.getElementById('v-'+id);if(el)el.classList.toggle('hidden',id!==tab)}});
  // Hide fase/mat/score filters on PJUS tab
  const isPjus=tab==='pjus';const d=isPjus?'none':'';
  ['msF','msF','msMat','msS'].forEach(id=>{{const el=document.getElementById(id);if(el)el.style.display=d}});
  ['lbF','lbMat','lbS','sepScore'].forEach(id=>{{const el=document.getElementById(id);if(el)el.style.display=d}});
  render();
}}

// ═══ DRILL-DOWN ENGINE ═══
function setDrill(tab,key,val,label){{
  drill[tab]={{key,val}};
  const bar=document.getElementById('drill'+tab.charAt(0).toUpperCase()+tab.slice(1));
  const lbl=document.getElementById('drill'+tab.charAt(0).toUpperCase()+tab.slice(1)+'Label');
  if(bar){{bar.classList.add('show');lbl.textContent=label}}
  render();
}}
function clearDrill(tab){{
  delete drill[tab];
  const bar=document.getElementById('drill'+tab.charAt(0).toUpperCase()+tab.slice(1));
  if(bar) bar.classList.remove('show');
  // Remove active borders
  document.querySelectorAll('#v-'+tab+' .drill-active').forEach(e=>e.classList.remove('drill-active'));
  render();
}}
function applyDrill(arr,tab){{
  if(!drill[tab]) return arr;
  const {{key,val}}=drill[tab];
  return arr.filter(r=>r[key]===val||(key==='scoreN'&&r.scoreN==val)||(key==='score'&&r.score==val));
}}
function addClickHandler(chartId,chart,labels,key,tab,cardId){{
  const canvas=document.getElementById(chartId);
  canvas.onclick=function(evt){{
    const pts=chart.getElementsAtEventForMode(evt,'nearest',{{intersect:true}},true);
    if(pts.length>0){{
      const idx=pts[0].index;
      const val=labels[idx];
      // Toggle
      if(drill[tab]&&drill[tab].val===val) clearDrill(tab);
      else{{
        document.querySelectorAll('#v-'+tab+' .drill-active').forEach(e=>e.classList.remove('drill-active'));
        document.getElementById(cardId).classList.add('drill-active');
        setDrill(tab,key,val,''+val);
      }}
    }}
  }};
}}

// ═══ PRIORITY INSIGHTS ═══
function genPrio(context,data){{
  const items=[];
  if(context==='intel'){{
    const agg={{}};data.forEach(e=>{{if(!agg[e.nome])agg[e.nome]={{val:0,vol:0}};agg[e.nome].val+=e.val;agg[e.nome].vol+=e.vol}});
    const sorted=Object.entries(agg).sort((a,b)=>b[1].val-a[1].val);
    const totalVal=sorted.reduce((a,[_,v])=>a+v.val,0);
    if(sorted.length>0){{const [n,v]=sorted[0];const pct=(v.val/totalVal*100).toFixed(1);
      items.push({{dot:'high',text:`<strong>${{n}}</strong> concentra ${{pct}}% do valor total (${{Fv(v.val)}}). Concentração elevada = risco de mercado.`}})}}
    if(sorted.length>=3){{const top3pct=sorted.slice(0,3).reduce((a,[_,v])=>a+v.val,0)/totalVal*100;
      items.push({{dot:top3pct>60?'high':'med',text:`Top 3 entes representam ${{top3pct.toFixed(1)}}% do mercado. ${{top3pct>60?'Alta concentração — diversificar fontes.':'Diversificação saudável.'}}`}})}}
  }}
  if(context==='prosp'){{
    const s5=data.filter(o=>o.scoreN===5);
    if(s5.length>0){{const topS5=s5.sort((a,b)=>b.valor-a.valor)[0];
      items.push({{dot:'high',text:`<strong>${{s5.length}} oportunidades Score 5</strong>. Maior: ${{Fr(topS5.valor)}} (${{topS5.ente}}). Ação imediata recomendada.`}})}}
    const faseCount={{}};data.forEach(o=>faseCount[o.fase]=(faseCount[o.fase]||0)+1);
    const topFase=Object.entries(faseCount).sort((a,b)=>b[1]-a[1])[0];
    if(topFase) items.push({{dot:'med',text:`Fase predominante: <strong>${{topFase[0]}}</strong> (${{topFase[1]}} oportunidades).`}});
  }}
  if(context==='pipe'){{
    const mature=data.filter(p=>['Muito Alta','Alta'].includes(p.mat));
    const matureVal=mature.reduce((a,p)=>a+p.val,0);const totalVal=data.reduce((a,p)=>a+p.val,0);
    if(totalVal>0) items.push({{dot:matureVal/totalVal>.4?'low':'high',text:`<strong>${{Fv(matureVal)}}</strong> (${{(matureVal/totalVal*100).toFixed(1)}}%) em alta/muito alta maturidade. ${{matureVal/totalVal>.4?'Pipeline saudável.':'Ampliar captação em fases avançadas.'}}`}});
  }}
  if(context==='report'){{
    const s5a=data.filter(a=>a.score===5);
    if(s5a.length>0) items.push({{dot:'high',text:`<strong>${{s5a.length}} alertas Score 5</strong> no período. ${{s5a.length>=5?'Volume elevado — alocar equipe.':'Volume gerenciável.'}}`}});
  }}
  if(context==='pjus'){{
    // PJUS-specific insights using real data
    const pjTot=PJUS_S.total_vf;const pjProcs=PJUS_S.total_procs;
    items.push({{dot:'low',text:`<strong>${{Fn(pjProcs)}}</strong> processos adquiridos totalizando <strong>${{Fv(pjTot/1e6)}}</strong> em valor de face. Ticket médio: ${{Fr(PJUS_S.ticket_medio)}}.`}});
    const topTrib=PJUS_T[0];if(topTrib) items.push({{dot:'med',text:`<strong>${{topTrib.trib}}</strong> é o tribunal com maior volume: ${{Fv(topTrib.vf/1e6)}} (${{(topTrib.vf/pjTot*100).toFixed(1)}}% do total). Avaliar diversificação.`}});
    const topEsf=PJUS_E[0];if(topEsf) items.push({{dot:'low',text:`Esfera <strong>${{topEsf.esfera}}</strong> concentra ${{Fv(topEsf.vf/1e6)}} em VF. Acompanhar diversificação entre esferas.`}});
  }}
  if(items.length===0) items.push({{dot:'low',text:'Operação dentro do esperado nos filtros atuais.'}});
  return items;
}}
function renderPrio(elId,items,title){{
  let h=`<h4>🔎 ${{title}}</h4>`;
  items.forEach(it=>h+=`<div class="prio-item"><div class="prio-dot ${{it.dot}}"></div><div>${{it.text}}</div></div>`);
  document.getElementById(elId).innerHTML=h;
}}
''')
print("Part 3a JS core OK")

# Part 3b: Render functions for Intel, Prosp, Pipe tabs
html_parts.append(f'''
// ═══ INTEL ═══
function rIntel(){{
  let d=gf(ENTES);
  d=applyDrill(d,'intel');
  const agg={{}};d.forEach(e=>{{if(!agg[e.nome])agg[e.nome]={{nome:e.nome,uf:e.uf,trib:e.trib,vol:0,val:0}};agg[e.nome].vol+=e.vol;agg[e.nome].val+=e.val}});
  const sorted=Object.values(agg).sort((a,b)=>b.val-a.val);
  const totalVol=sorted.reduce((a,e)=>a+e.vol,0);
  const totalVal=sorted.reduce((a,e)=>a+e.val,0);
  const top=sorted[0]||{{nome:'—',val:0,vol:0}};
  const fd=DAILY.filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m)));
  const FONTE_TRIB={{'DJEN':'DJEN','DJSP':'TJSP','DJMG':'TJMG','DJRJ':'TJRJ','DJBA':'TJBA','DJPR':'TJPR','DJGO':'TJGO','DJPE':'TJPE','DJRS':'TJRS','DJSC':'TJSC','DJCE':'TJCE','DJMA':'TJMA','DJPA':'TJPA','DJAP':'TJAP'}};
  const activeFontes=fT==='all'?FONTES:FONTES.filter(f=>{{const t=FONTE_TRIB[f];return f==='DJEN'||(t&&_m(fT,t))}});
  const dailyT=fd.reduce((a,r)=>a+activeFontes.reduce((s,f)=>s+(r[f]||0),0),0);
  const wd=fd.filter(r=>FONTES.some(f=>r[f]>0)).length||1;

  document.getElementById('kI').innerHTML=`
    <div class="kc kg"><div class="kc-label">VALOR TOTAL</div><div class="kc-val" style="color:var(--green)">${{Fv(totalVal)}}</div><div class="kc-sub">${{Fn(totalVol)}} pub.</div></div>
    <div class="kc kb"><div class="kc-label">ENTES</div><div class="kc-val" style="color:var(--blue)">${{sorted.length}}</div><div class="kc-sub">${{TRIBS.length}} tribunais</div></div>
    <div class="kc ky"><div class="kc-label">TICKET MÉDIO</div><div class="kc-val" style="color:var(--yellow)">${{totalVol?Fv(totalVal/totalVol):'—'}}</div><div class="kc-sub">Valor/pub.</div></div>
    <div class="kc kp"><div class="kc-label">MAIOR ENTE</div><div class="kc-val" style="color:var(--purple);font-size:13px">${{top.nome}}</div><div class="kc-sub">${{Fv(top.val)}}</div></div>
    <div class="kc ko"><div class="kc-label">VOL. DIÁRIO</div><div class="kc-val" style="color:var(--orange)">${{Fn(Math.round(dailyT/wd))}}</div><div class="kc-sub">${{wd}} dias úteis</div></div>
  `;
  renderPrio('prioIntel',genPrio('intel',d),'Leitura de Oportunidade — Inteligência de Mercado');

  const t10=sorted.slice(0,10);
  dc('cEV');ch['cEV']=new Chart(document.getElementById('cEV'),{{type:'bar',data:{{labels:t10.map(e=>e.nome.replace('Estado d','d').replace('Município d','Mun. d')),datasets:[{{data:t10.map(e=>e.val),backgroundColor:C10.map(c=>c+'33'),borderColor:C10,borderWidth:1.5,borderRadius:4}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>'R$ '+c.raw.toFixed(1)+'M'}}}}}},scales:{{x:{{grid:{{color:'rgba(224,231,245,.4)'}}}},y:{{grid:{{display:false}}}}}}}}}});
  addClickHandler('cEV',ch['cEV'],t10.map(e=>e.nome),'nome','intel','cdEV');

  dc('cEVo');ch['cEVo']=new Chart(document.getElementById('cEVo'),{{type:'bar',data:{{labels:t10.map(e=>e.nome.replace('Estado d','d').replace('Município d','Mun. d')),datasets:[{{data:t10.map(e=>e.vol),backgroundColor:'rgba(14,47,93,.1)',borderColor:'#0E2F5D',borderWidth:1.5,borderRadius:4}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(224,231,245,.4)'}}}},y:{{grid:{{display:false}}}}}}}}}});
  addClickHandler('cEVo',ch['cEVo'],t10.map(e=>e.nome),'nome','intel','cdEVo');

  let h='<table><thead><tr><th>#</th><th>Ente</th><th>UF</th><th>Tribunal</th><th>Vol.</th><th>Valor</th><th>Ticket</th><th>%</th></tr></thead><tbody>';
  sorted.forEach((e,i)=>{{const p=totalVal?e.val/totalVal*100:0;h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{e.nome}}</td><td>${{e.uf}}</td><td>${{e.trib}}</td><td>${{Fn(e.vol)}}</td><td style="font-weight:600">${{Fv(e.val)}}</td><td>${{e.vol?Fv(e.val/e.vol):'—'}}</td><td><div class="pb"><div class="pf" style="width:${{p}}%;background:${{i<3?'var(--accent)':'var(--text4)'}}"></div></div>${{p.toFixed(1)}}%</td></tr>`}});
  document.getElementById('tE').innerHTML=h+'</tbody></table>';

  const fmi=gfmi();
  const trendTribs=fT==='all'?TRIBS.slice(0,6):TRIBS.filter(t=>_m(fT,t)).slice(0,8);
  dc('cTr');const ds=trendTribs.map((t,i)=>({{label:t,data:TREND[t]?TREND[t].filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))).map(r=>r.v):[],borderColor:C10[i%10],backgroundColor:'transparent',tension:.3,borderWidth:2,pointRadius:2,pointBackgroundColor:C10[i%10]}}));
  ch['cTr']=new Chart(document.getElementById('cTr'),{{type:'line',data:{{labels:fmi.map(m=>m.label),datasets:ds}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:true,position:'top',labels:{{font:{{size:9}},usePointStyle:true,pointStyleWidth:6,padding:6}}}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}}}},x:{{grid:{{display:false}}}}}}}}}});

  dc('cDa');const topF=activeFontes.slice(0,5);const dDS=topF.map((f,i)=>({{label:f,data:fd.map(r=>r[f]||0),backgroundColor:C10[i]+'77',borderColor:C10[i],borderWidth:1}}));
  ch['cDa']=new Chart(document.getElementById('cDa'),{{type:'bar',data:{{labels:fd.map(r=>r.date),datasets:dDS}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:true,position:'top',labels:{{font:{{size:8}},usePointStyle:true,pointStyleWidth:6,padding:6}}}}}},scales:{{x:{{stacked:true,grid:{{display:false}},ticks:{{font:{{size:7}},maxRotation:60,maxTicksLimit:25}}}},y:{{stacked:true,grid:{{color:'rgba(224,231,245,.4)'}}}}}}}}}});
}}

// ═══ PROSPECÇÃO ═══
function rProsp(){{
  let d=gf(OPPS);d=applyDrill(d,'prosp');
  const tV=d.reduce((a,o)=>a+o.valor,0);const s5=d.filter(o=>o.scoreN===5).length;const s4=d.filter(o=>o.scoreN===4).length;

  document.getElementById('kP').innerHTML=`
    <div class="kc kg"><div class="kc-label">OPORTUNIDADES</div><div class="kc-val" style="color:var(--green)">${{d.length}}</div><div class="kc-sub">Score ≥ 3</div></div>
    <div class="kc kb"><div class="kc-label">VALOR PIPELINE</div><div class="kc-val" style="color:var(--blue)">${{Fr(tV)}}</div><div class="kc-sub">Total</div></div>
    <div class="kc kr"><div class="kc-label">SCORE 5</div><div class="kc-val" style="color:var(--red)">${{s5}}</div><div class="kc-sub">Urgente</div></div>
    <div class="kc ky"><div class="kc-label">SCORE 4</div><div class="kc-val" style="color:var(--yellow)">${{s4}}</div><div class="kc-sub">Alta</div></div>
    <div class="kc kp"><div class="kc-label">CEDENTES</div><div class="kc-val">${{new Set(d.map(o=>o.benef)).size}}</div><div class="kc-sub">${{new Set(d.map(o=>o.adv)).size}} advs</div></div>
  `;
  renderPrio('prioProsp',genPrio('prosp',d),'Leitura de Oportunidade — Prospecção Comercial');

  dc('cSD');const sc=[3,4,5].map(s=>d.filter(o=>o.scoreN===s).length);
  ch['cSD']=new Chart(document.getElementById('cSD'),{{type:'doughnut',data:{{labels:['Score 3','Score 4','Score 5'],datasets:[{{data:sc,backgroundColor:['#F59E0B','#0074FF','#00A68C'],borderWidth:2,borderColor:'#fff'}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},padding:6,usePointStyle:true}}}}}}}}}});
  addClickHandler('cSD',ch['cSD'],[3,4,5],'scoreN','prosp','cdSD');

  dc('cFV');const fMap={{}};d.forEach(o=>fMap[o.fase]=(fMap[o.fase]||0)+o.valor);const fL=Object.keys(fMap).sort((a,b)=>fMap[b]-fMap[a]);
  ch['cFV']=new Chart(document.getElementById('cFV'),{{type:'bar',data:{{labels:fL,datasets:[{{data:fL.map(f=>fMap[f]/1e6),backgroundColor:fL.map((_,i)=>C10[i]+'44'),borderColor:fL.map((_,i)=>C10[i]),borderWidth:1.5,borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}}}},x:{{grid:{{display:false}},ticks:{{font:{{size:8}},maxRotation:20}}}}}}}}}});
  addClickHandler('cFV',ch['cFV'],fL,'fase','prosp','cdFV');

  let h='<table><thead><tr><th>Data</th><th>Score</th><th>Ente</th><th>Beneficiário</th><th>Advogado</th><th>Valor</th><th>Fase</th><th>Mat.</th><th>Trib.</th></tr></thead><tbody>';
  d.sort((a,b)=>b.scoreN-a.scoreN||b.valor-a.valor).slice(0,50).forEach(o=>{{const mc=o.mat.includes('Alta')?'bg':o.mat.includes('Média')?'by':'br';h+=`<tr><td>${{o.date}}</td><td><span class="score-pill ${{sC(o.scoreN)}}">${{o.scoreN}}</span></td><td>${{o.ente}}</td><td style="font-weight:600">${{o.benef}}</td><td style="color:var(--text3);font-size:9px">${{o.adv}}</td><td style="font-weight:600">${{Fr(o.valor)}}</td><td><span class="bd bb">${{o.fase}}</span></td><td><span class="bd ${{mc}}">${{o.mat}}</span></td><td>${{o.trib}}</td></tr>`}});
  document.getElementById('tO').innerHTML=h+'</tbody></table>';

  const fb=gf(BENEFS);const bA={{}};fb.forEach(b=>{{if(!bA[b.nome])bA[b.nome]={{nome:b.nome,pubs:0,tribs:new Set(),valor:0,scores:[],adv:{{}}}};bA[b.nome].pubs+=b.pubs;bA[b.nome].tribs.add(b.tribs);bA[b.nome].valor+=b.valor;bA[b.nome].scores.push(b.score);bA[b.nome].adv[b.adv]=(bA[b.nome].adv[b.adv]||0)+1}});
  const bS=Object.values(bA).sort((a,b)=>b.pubs-a.pubs);
  h='<table><thead><tr><th>#</th><th>Beneficiário</th><th>Pub.</th><th>Tribs</th><th>Valor</th><th>Score</th><th>Adv. Princ.</th><th>Prio.</th></tr></thead><tbody>';
  bS.slice(0,20).forEach((b,i)=>{{const avg=b.scores.reduce((a,s)=>a+s,0)/b.scores.length;const ta=Object.entries(b.adv).sort((a,c)=>c[1]-a[1])[0][0];const pr=b.pubs>=15?'ALTA':b.pubs>=8?'MÉDIA':'BAIXA';const pc=pr==='ALTA'?'p-max':pr==='MÉDIA'?'p-alta':'p-media';
    h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{b.nome}}</td><td>${{b.pubs}}</td><td>${{b.tribs.size}}</td><td style="font-weight:600">${{Fr(b.valor)}}</td><td><span class="score-pill ${{sC(Math.round(avg))}}">${{avg.toFixed(1)}}</span></td><td style="color:var(--text3);font-size:9px">${{ta}}</td><td><span class="prio-badge ${{pc}}">${{pr}}</span></td></tr>`}});
  document.getElementById('tB').innerHTML=h+'</tbody></table>';

  const fa=gf(ADV_DATA);const aA={{}};fa.forEach(a=>{{if(!aA[a.nome])aA[a.nome]={{nome:a.nome,pubs:0,benefs:0,valor:0,tribs:new Set(),scores:[]}};aA[a.nome].pubs+=a.pubs;aA[a.nome].benefs+=a.benefs;aA[a.nome].valor+=a.valor;if(a.tribs)a.tribs.forEach(t=>aA[a.nome].tribs.add(t));aA[a.nome].scores.push(a.score)}});
  const aS=Object.values(aA).sort((a,b)=>b.pubs-a.pubs);
  h='<table><thead><tr><th>#</th><th>Advogado</th><th>Pub.</th><th>Benef.</th><th>Valor</th><th>Tribunais</th><th>Score</th><th>Potencial</th></tr></thead><tbody>';
  aS.forEach((a,i)=>{{const avg=a.scores.reduce((s,v)=>s+v,0)/a.scores.length;const pot=a.pubs>=60?'ALTO':a.pubs>=30?'MÉDIO':'BAIXO';const pc=pot==='ALTO'?'p-max':pot==='MÉDIO'?'p-alta':'p-media';
    h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{a.nome}}</td><td>${{a.pubs}}</td><td>${{a.benefs}}</td><td style="font-weight:600">${{Fr(a.valor)}}</td><td style="font-size:8px;color:var(--text3)">${{[...a.tribs].join(',')}}</td><td><span class="score-pill ${{sC(Math.round(avg))}}">${{avg.toFixed(1)}}</span></td><td><span class="prio-badge ${{pc}}">${{pot}}</span></td></tr>`}});
  document.getElementById('tA').innerHTML=h+'</tbody></table>';
}}

// ═══ PIPELINE ═══
function rPipe(){{
  let d=gf(PIPELINE);d=applyDrill(d,'pipe');
  const pA={{}};d.forEach(p=>{{if(!pA[p.fase])pA[p.fase]={{fase:p.fase,vol:0,val:0,score:p.score,dias:p.dias,mat:p.mat,acao:p.acao}};pA[p.fase].vol+=p.vol;pA[p.fase].val+=p.val}});
  const pipes=Object.values(pA).sort((a,b)=>b.val-a.val);
  const tV=pipes.reduce((a,p)=>a+p.vol,0);const tVl=pipes.reduce((a,p)=>a+p.val,0);
  const mature=pipes.filter(p=>['Muito Alta','Alta'].includes(p.mat)).reduce((a,p)=>a+p.vol,0);
  const avgS=tV?(pipes.reduce((a,p)=>a+p.score*p.vol,0)/tV).toFixed(1):'—';

  document.getElementById('kPi').innerHTML=`
    <div class="kc kg"><div class="kc-label">PIPELINE</div><div class="kc-val" style="color:var(--green)">${{Fv(tVl)}}</div><div class="kc-sub">${{Fn(tV)}} prec.</div></div>
    <div class="kc kb"><div class="kc-label">MADUROS</div><div class="kc-val" style="color:var(--blue)">${{Fn(mature)}}</div><div class="kc-sub">${{tV?(mature/tV*100).toFixed(1):0}}%</div></div>
    <div class="kc ky"><div class="kc-label">SCORE MÉDIO</div><div class="kc-val" style="color:var(--yellow)">${{avgS}}</div><div class="kc-sub">Ponderado</div></div>
    <div class="kc ko"><div class="kc-label">FASES</div><div class="kc-val">${{pipes.length}}</div><div class="kc-sub">Mapeadas</div></div>
  `;
  renderPrio('prioPipe',genPrio('pipe',d),'Leitura de Oportunidade — Pipeline');

  const pCo=pipes.map(p=>p.score>=4?'#00A68C':p.score>=3?'#0074FF':p.score>=2?'#F59E0B':'#EF4444');
  dc('cPV');ch['cPV']=new Chart(document.getElementById('cPV'),{{type:'bar',data:{{labels:pipes.map(p=>p.fase),datasets:[{{data:pipes.map(p=>p.vol),backgroundColor:pCo.map(c=>c+'33'),borderColor:pCo,borderWidth:1.5,borderRadius:4}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(224,231,245,.4)'}}}},y:{{grid:{{display:false}},ticks:{{font:{{size:8}}}}}}}}}}}});
  addClickHandler('cPV',ch['cPV'],pipes.map(p=>p.fase),'fase','pipe','cdPV');

  dc('cPB');ch['cPB']=new Chart(document.getElementById('cPB'),{{type:'bubble',data:{{datasets:[{{data:pipes.map(p=>({{x:p.dias,y:p.score,r:Math.sqrt(p.val)*1.3}})),backgroundColor:pCo.map(c=>c+'55'),borderColor:pCo,borderWidth:1.5}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>pipes[c.dataIndex].fase}}}}}},scales:{{x:{{title:{{display:true,text:'Dias'}},grid:{{color:'rgba(224,231,245,.4)'}}}},y:{{title:{{display:true,text:'Score'}},min:1,max:5.5,grid:{{color:'rgba(224,231,245,.4)'}}}}}}}}}});

  let h='<table><thead><tr><th>Fase</th><th>Vol.</th><th>%</th><th>Valor</th><th>Score</th><th>Dias</th><th>Maturidade</th><th>Ação</th></tr></thead><tbody>';
  pipes.forEach(p=>{{const pct=tV?p.vol/tV*100:0;const mc=p.mat.includes('Alta')?'bg':p.mat.includes('Média')?'by':'br';h+=`<tr><td style="font-weight:600">${{p.fase}}</td><td>${{Fn(p.vol)}}</td><td><div class="pb"><div class="pf" style="width:${{pct}}%;background:var(--accent)"></div></div>${{pct.toFixed(1)}}%</td><td style="font-weight:600">${{Fv(p.val)}}</td><td><span class="score-pill ${{sC(Math.round(p.score))}}">${{p.score}}</span></td><td>${{p.dias}}d</td><td><span class="bd ${{mc}}">${{p.mat}}</span></td><td style="color:var(--text3);font-size:8px">${{p.acao}}</td></tr>`}});
  document.getElementById('tPi').innerHTML=h+'</tbody></table>';

  const td=gf(TOP_OPPS).sort((a,b)=>b.idx-a.idx).slice(0,20);
  h='<table><thead><tr><th>#</th><th>Beneficiário</th><th>Ente</th><th>Trib.</th><th>Valor</th><th>Score</th><th>Fase</th><th>Mat.</th><th>Dias</th><th>Índice</th></tr></thead><tbody>';
  td.forEach((o,i)=>{{const mc=o.mat&&o.mat.includes('Alta')?'bg':o.mat&&o.mat.includes('Média')?'by':'br';h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{o.benef}}</td><td>${{o.ente}}</td><td>${{o.trib}}</td><td style="font-weight:600">${{Fr(o.valor)}}</td><td><span class="score-pill ${{sC(o.score)}}">${{o.score}}</span></td><td><span class="bd bb">${{o.fase}}</span></td><td><span class="bd ${{mc}}">${{o.mat||'—'}}</span></td><td>${{o.dias}}d</td><td style="font-weight:800;color:var(--accent)">${{o.idx}}</td></tr>`}});
  document.getElementById('tTO').innerHTML=h+'</tbody></table>';
}}
''')
print("Part 3b render Intel/Prosp/Pipe OK")

# Part 3c: Report, PJUS Performance, Export, Render
html_parts.append(f'''
// ═══ RELATÓRIOS ═══
function rReport(){{
  const fmi=gfmi();
  const heatTribs=fT==='all'?TRIBS:TRIBS.filter(t=>_m(fT,t));
  const tP=heatTribs.reduce((a,t)=>a+(TREND[t]?TREND[t].filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))).reduce((s,v)=>s+v.v,0):0),0);
  const fd=gf(FAIXAS);const fA={{}};fd.forEach(f=>{{if(!fA[f.faixa])fA[f.faixa]={{faixa:f.faixa,vol:0,val:0,tend:f.tend}};fA[f.faixa].vol+=f.vol;fA[f.faixa].val+=f.val}});
  const fArr=Object.values(fA);const tFV=fArr.reduce((a,f)=>a+f.vol,0);const tFVl=fArr.reduce((a,f)=>a+f.val,0);
  let alerts=gf(ALERTS);alerts=applyDrill(alerts,'report');const a5=alerts.filter(a=>a.score===5).length;

  document.getElementById('kR').innerHTML=`
    <div class="kc kg"><div class="kc-label">PUBLICAÇÕES</div><div class="kc-val" style="color:var(--green)">${{Fn(tP)}}</div><div class="kc-sub">${{TRIBS.length}} tribs</div></div>
    <div class="kc kb"><div class="kc-label">CLASSIFICADOS</div><div class="kc-val" style="color:var(--blue)">${{Fn(tFV)}}</div><div class="kc-sub">7 faixas</div></div>
    <div class="kc ky"><div class="kc-label">VALOR</div><div class="kc-val" style="color:var(--yellow)">${{Fv(tFVl)}}</div><div class="kc-sub">Total</div></div>
    <div class="kc kr"><div class="kc-label">SCORE 5</div><div class="kc-val" style="color:var(--red)">${{a5}}</div><div class="kc-sub">Alertas</div></div>
    <div class="kc ko"><div class="kc-label">ALERTAS</div><div class="kc-val" style="color:var(--orange)">${{alerts.length}}</div><div class="kc-sub">Total</div></div>
  `;
  renderPrio('prioReport',genPrio('report',alerts),'Leitura de Oportunidade — Relatórios');

  const maxV=Math.max(...heatTribs.flatMap(t=>TREND[t]?TREND[t].filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))).map(r=>r.v):[]),1);
  let h='<table><thead><tr><th>Tribunal</th>';fmi.forEach(m=>h+=`<th>${{m.label}}</th>`);h+='<th>Total</th></tr></thead><tbody>';
  heatTribs.forEach(t=>{{h+=`<tr><td style="font-weight:600">${{t}}</td>`;let tot=0;
    if(TREND[t])TREND[t].filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))).forEach(r=>{{tot+=r.v;const i=r.v/maxV;const bg=i>.7?'rgba(0,116,255,.25)':i>.4?'rgba(0,116,255,.12)':'rgba(0,116,255,.04)';h+=`<td style="background:${{bg}};text-align:center;font-weight:${{i>.7?'700':'400'}}">${{Fn(r.v)}}</td>`}});
    h+=`<td style="font-weight:700">${{Fn(tot)}}</td></tr>`}});
  document.getElementById('tH').innerHTML=h+'</tbody></table>';

  dc('cFxV');ch['cFxV']=new Chart(document.getElementById('cFxV'),{{type:'bar',data:{{labels:fArr.map(f=>f.faixa),datasets:[{{data:fArr.map(f=>f.vol),backgroundColor:fArr.map((_,i)=>C10[i]+'44'),borderColor:fArr.map((_,i)=>C10[i]),borderWidth:1.5,borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}}}},x:{{grid:{{display:false}},ticks:{{font:{{size:7}},maxRotation:20}}}}}}}}}});
  addClickHandler('cFxV',ch['cFxV'],fArr.map(f=>f.faixa),'faixa','report','cdFxV');

  dc('cFxVl');ch['cFxVl']=new Chart(document.getElementById('cFxVl'),{{type:'bar',data:{{labels:fArr.map(f=>f.faixa),datasets:[{{data:fArr.map(f=>f.val),backgroundColor:fArr.map((_,i)=>C10[i]+'44'),borderColor:fArr.map((_,i)=>C10[i]),borderWidth:1.5,borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}}}},x:{{grid:{{display:false}},ticks:{{font:{{size:7}},maxRotation:20}}}}}}}}}});
  addClickHandler('cFxVl',ch['cFxVl'],fArr.map(f=>f.faixa),'faixa','report','cdFxVl');

  h='<table><thead><tr><th>Faixa</th><th>Vol.</th><th>%</th><th>Valor</th><th>%</th><th>Ticket</th><th>Tend.</th></tr></thead><tbody>';
  fArr.forEach(f=>{{const pv=tFV?f.vol/tFV*100:0;const pvl=tFVl?f.val/tFVl*100:0;const tc=f.tend.includes('▲')?'bg':f.tend.includes('▼')?'br':'by';
    h+=`<tr><td style="font-weight:600">${{f.faixa}}</td><td>${{Fn(f.vol)}}</td><td>${{pv.toFixed(1)}}%</td><td style="font-weight:600">${{Fv(f.val)}}</td><td>${{pvl.toFixed(1)}}%</td><td>${{f.vol?Fr(f.val*1e6/f.vol):'—'}}</td><td><span class="bd ${{tc}}">${{f.tend}}</span></td></tr>`}});
  document.getElementById('tFx').innerHTML=h+'</tbody></table>';

  h='<table><thead><tr><th>Score</th><th>Beneficiário</th><th>Ente</th><th>Valor</th><th>Fase</th><th>Tribunal</th><th>Data</th><th>Ação</th></tr></thead><tbody>';
  alerts.sort((a,b)=>b.score-a.score).slice(0,30).forEach(a=>{{
    h+=`<tr><td><span class="score-pill ${{sC(a.score)}}">${{a.score}}</span></td><td style="font-weight:600">${{a.benef}}</td><td style="color:var(--text3)">${{a.ente}}</td><td style="font-weight:700">${{Fr(a.valor)}}</td><td><span class="bd bb">${{a.fase}}</span></td><td>${{a.trib}}</td><td style="color:var(--text4);font-size:8px">${{a.date}}</td><td style="color:var(--accent);font-weight:600;font-size:8px">${{a.acao}}</td></tr>`}});
  document.getElementById('alC').innerHTML=h+'</tbody></table>';

  h='<table><thead><tr><th>Data</th><th>Tipo</th><th>Tribunal</th><th>Ente</th><th>Beneficiário</th><th>Valor</th><th>Score</th><th>Fase</th><th>Maturidade</th><th>Ação</th></tr></thead><tbody>';
  alerts.forEach(a=>{{const mc=a.mat&&a.mat.includes('Alta')?'bg':a.mat&&a.mat.includes('Média')?'by':'br';
    h+=`<tr><td>${{a.date}}</td><td style="font-size:8px">${{a.tipo}}</td><td>${{a.trib}}</td><td>${{a.ente}}</td><td style="font-weight:600">${{a.benef}}</td><td style="font-weight:600">${{Fr(a.valor)}}</td><td><span class="score-pill ${{sC(a.score)}}">${{a.score}}</span></td><td>${{a.fase}}</td><td><span class="bd ${{mc}}">${{a.mat||'—'}}</span></td><td style="color:var(--text3);font-size:8px">${{a.acao}}</td></tr>`}});
  document.getElementById('tAnalytic').innerHTML=h+'</tbody></table>';
}}

// ═══ PJUS PERFORMANCE ═══
function rPjus(){{
  const ptm=PJUS_TM.filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))&&(fT==='all'||_m(fT,r.trib)));
  // Build monthly aggregation from ptm (respects tribunal filter)
  const pmAgg={{}};ptm.forEach(r=>{{const k=r.y+'-'+r.m;if(!pmAgg[k])pmAgg[k]={{y:r.y,m:r.m,ml:['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][r.m]+'/'+String(r.y).slice(2),qtd:0,vf:0,vp:0,liq:0}};pmAgg[k].qtd+=r.qtd;pmAgg[k].vf+=r.vf;pmAgg[k].vp+=r.vp;pmAgg[k].liq=pmAgg[k].liq||(r.liq||0)}});
  // Fallback to PJUS_M for liq when available
  if(fT==='all'){{PJUS_M.filter(r=>(fY==='all'||_m(fY,r.y))&&(fM==='all'||_m(fM,r.m))).forEach(r=>{{const k=r.y+'-'+r.m;if(pmAgg[k])pmAgg[k].liq=r.liq}})}}
  const pm=Object.values(pmAgg).sort((a,b)=>a.y-b.y||a.m-b.m);

  const totProcs=pm.reduce((a,r)=>a+r.qtd,0);
  const totVF=pm.reduce((a,r)=>a+r.vf,0);
  const totVP=pm.reduce((a,r)=>a+r.vp,0);
  const totLiq=pm.reduce((a,r)=>a+r.liq,0);
  const ticket=totProcs?totLiq/totProcs:0;
  document.getElementById('kPJ').innerHTML=`
    <div class="kc kg"><div class="kc-label">PROCESSOS COMPRADOS</div><div class="kc-val" style="color:var(--green)">${{Fn(totProcs)}}</div><div class="kc-sub">${{pm.length}} meses</div></div>
    <div class="kc kb"><div class="kc-label">VALOR DE FACE</div><div class="kc-val" style="color:var(--blue)">${{Fv(totVF/1e6)}}</div><div class="kc-sub">Total adquirido</div></div>
    <div class="kc ky"><div class="kc-label">VLR. DESEMBOLSADO</div><div class="kc-val" style="color:var(--yellow)">${{Fv(totVP/1e6)}}</div><div class="kc-sub">Pago ao credor</div></div>
    <div class="kc kp"><div class="kc-label">VLR. LÍQ. A RECEBER</div><div class="kc-val" style="color:var(--purple)">${{Fv(totLiq/1e6)}}</div><div class="kc-sub">Esperado receber</div></div>
    <div class="kc ko"><div class="kc-label">TICKET MÉDIO</div><div class="kc-val" style="color:var(--orange)">${{Fr(ticket)}}</div><div class="kc-sub">Líq. Receber / Processo</div></div>
  `;
  renderPrio('prioPjus',genPrio('pjus',pm),'Leitura de Oportunidade — Performance PJUS');

  // Monthly charts
  dc('cPjM');ch['cPjM']=new Chart(document.getElementById('cPjM'),{{type:'bar',data:{{labels:pm.map(r=>r.ml),datasets:[{{label:'Processos',data:pm.map(r=>r.qtd),backgroundColor:'rgba(0,116,255,.25)',borderColor:'#0074FF',borderWidth:1.5,borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}}}},x:{{grid:{{display:false}},ticks:{{font:{{size:8}},maxRotation:45}}}}}}}}}});
  const pmLabels=pm.map(r=>r.ml);
  const canvasM=document.getElementById('cPjM');
  canvasM.onclick=function(evt){{
    const pts=ch['cPjM'].getElementsAtEventForMode(evt,'nearest',{{intersect:true}},true);
    if(pts.length>0){{
      const idx=pts[0].index;const r=pm[idx];
      setMSSingle('msY',r.y);setMSSingle('msM',r.m);onF();
    }}
  }};

  dc('cPjV');ch['cPjV']=new Chart(document.getElementById('cPjV'),{{type:'bar',data:{{labels:pm.map(r=>r.ml),datasets:[
    {{label:'Valor de Face',data:pm.map(r=>r.vf/1e6),backgroundColor:'rgba(0,116,255,.2)',borderColor:'#0074FF',borderWidth:1.5,borderRadius:4}},
    {{label:'Vlr. Desembolsado',data:pm.map(r=>r.vp/1e6),backgroundColor:'rgba(0,166,140,.2)',borderColor:'#00A68C',borderWidth:1.5,borderRadius:4}},
    {{label:'Vlr. Líq. a Receber',data:pm.map(r=>r.liq/1e6),backgroundColor:'rgba(14,47,93,.15)',borderColor:'#0E2F5D',borderWidth:1.5,borderRadius:4}}
  ]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:true,position:'top',labels:{{font:{{size:8}},usePointStyle:true,padding:6}}}}}},scales:{{y:{{grid:{{color:'rgba(224,231,245,.4)'}},ticks:{{callback:v=>Fv(v)}}}},x:{{grid:{{display:false}},ticks:{{font:{{size:8}},maxRotation:45}}}}}}}}}});

  // Tribunal charts
  const tribAgg={{}};ptm.forEach(r=>{{if(!tribAgg[r.trib])tribAgg[r.trib]={{trib:r.trib,qtd:0,vf:0,vp:0,liq:0}};tribAgg[r.trib].qtd+=r.qtd;tribAgg[r.trib].vf+=r.vf;tribAgg[r.trib].vp+=r.vp}});
  // Enrich with liq from PJUS_T
  PJUS_T.forEach(t=>{{if(tribAgg[t.trib])tribAgg[t.trib].liq=t.liq||0}});
  const tribArr=Object.values(tribAgg).sort((a,b)=>b.vf-a.vf).slice(0,12);

  dc('cPjT');ch['cPjT']=new Chart(document.getElementById('cPjT'),{{type:'bar',data:{{labels:tribArr.map(t=>t.trib),datasets:[{{data:tribArr.map(t=>t.vf/1e6),backgroundColor:tribArr.map((_,i)=>C10[i%10]+'33'),borderColor:tribArr.map((_,i)=>C10[i%10]),borderWidth:1.5,borderRadius:4}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:c=>Fv(c.raw)}}}}}},scales:{{x:{{grid:{{color:'rgba(224,231,245,.4)'}}}},y:{{grid:{{display:false}}}}}}}}}});
  addClickHandler('cPjT',ch['cPjT'],tribArr.map(t=>t.trib),'trib','pjus','cdPjT');

  // Esfera donut
  const esfAgg={{}};pm.forEach(r=>{{/* use full PJUS_E */}});
  const pe=PJUS_E;
  dc('cPjE');ch['cPjE']=new Chart(document.getElementById('cPjE'),{{type:'doughnut',data:{{labels:pe.map(e=>e.esfera),datasets:[{{data:pe.map(e=>e.vf),backgroundColor:['#0074FF','#00A68C','#F59E0B'],borderWidth:2,borderColor:'#fff'}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},padding:6,usePointStyle:true}},generateLabels:c=>c.data.labels.map((l,i)=>({{text:l+' ('+Fv(c.data.datasets[0].data[i]/1e6)+')',fillStyle:c.data.datasets[0].backgroundColor[i],strokeStyle:'#fff',lineWidth:2,pointStyle:'circle'}}))}}}}}}}});

  // Tribunal table
  h='<table><thead><tr><th>#</th><th>Tribunal</th><th>Processos</th><th>Valor Face</th><th>Vlr. Desembolsado</th><th>Vlr. Líq. a Receber</th><th>Ticket Médio</th><th>%</th></tr></thead><tbody>';
  tribArr.forEach((t,i)=>{{const pct=totVF?t.vf/totVF*100:0;const tkt=t.qtd?t.liq/t.qtd:0;
    h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{t.trib}}</td><td>${{Fn(t.qtd)}}</td><td style="font-weight:600">${{Fv(t.vf/1e6)}}</td><td>${{Fv(t.vp/1e6)}}</td><td style="font-weight:600">${{Fv(t.liq/1e6)}}</td><td>${{Fr(tkt)}}</td><td><div class="pb"><div class="pf" style="width:${{pct}}%;background:var(--accent)"></div></div>${{pct.toFixed(1)}}%</td></tr>`}});
  document.getElementById('tPjT').innerHTML=h+'</tbody></table>';

  // Orgao table
  const orgArr=PJUS_O;
  h='<table><thead><tr><th>#</th><th>Órgão Pagador</th><th>Processos</th><th>Valor Face</th><th>Vlr. Desembolsado</th><th>Vlr. Líq. a Receber</th><th>Ticket Médio</th></tr></thead><tbody>';
  orgArr.slice(0,15).forEach((o,i)=>{{const tkt=o.qtd?(o.liq||0)/o.qtd:0;
    h+=`<tr><td><span class="rn ${{rC(i)}}">${{i+1}}</span></td><td style="font-weight:600">${{o.orgao}}</td><td>${{Fn(o.qtd)}}</td><td style="font-weight:600">${{Fv(o.vf/1e6)}}</td><td>${{Fv(o.vp/1e6)}}</td><td style="font-weight:600">${{Fv((o.liq||0)/1e6)}}</td><td>${{Fr(tkt)}}</td></tr>`}});
  document.getElementById('tPjO').innerHTML=h+'</tbody></table>';
}}

// ═══ EXPORT CSV ═══
function toCSV(headers,rows){{
  const bom='\\uFEFF';const h=headers.join(';');
  const r=rows.map(row=>row.map(c=>(typeof c==='string'&&(c.includes(';')||c.includes('"')))?'"'+c.replace(/"/g,'""')+'"':c).join(';'));
  return bom+h+'\\n'+r.join('\\n');
}}
function download(content,filename){{
  const blob=new Blob([content],{{type:'text/csv;charset=utf-8'}});
  const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;a.click();URL.revokeObjectURL(url);
}}
function exportCSV(){{
  const alerts=gf(ALERTS).sort((a,b)=>b.score-a.score);
  const headers=['Data','Tipo','Tribunal','Ente','Beneficiário','Valor','Score','Fase','Maturidade','Ação'];
  const rows=alerts.map(a=>[a.date,a.tipo.replace(/[🔴🟡🟢🔵⚡]/g,'').trim(),a.trib,a.ente,a.benef,a.valor,a.score,a.fase,a.mat||'',a.acao]);
  download(toCSV(headers,rows),'alertas_pjus_'+new Date().toISOString().slice(0,10)+'.csv');
}}
function exportFullCSV(){{
  const all=[...gf(ALERTS),...gf(OPPS).map(o=>({{...o,tipo:'Oportunidade',acao:'Avaliar'}}))];
  all.sort((a,b)=>(b.score||b.scoreN||0)-(a.score||a.scoreN||0));
  const headers=['Data','Tipo','Tribunal','Ente','Beneficiário','Advogado','Valor','Score','Fase','Maturidade','Ação'];
  const rows=all.map(a=>[a.date,a.tipo?(typeof a.tipo==='string'?a.tipo.replace(/[🔴🟡🟢🔵⚡]/g,'').trim():'Oportunidade'):'',a.trib||'',a.ente||'',a.benef||'',a.adv||'',a.valor||0,a.score||a.scoreN||'',a.fase||'',a.mat||'',a.acao||'']);
  download(toCSV(headers,rows),'base_analitica_pjus_'+new Date().toISOString().slice(0,10)+'.csv');
}}

function render(){{
  if(curTab==='intel')rIntel();
  if(curTab==='prosp')rProsp();
  if(curTab==='pipe')rPipe();
  if(curTab==='report')rReport();
  if(curTab==='pjus')rPjus();
}}
render();
</script>
</body>
</html>''')
print("Part 3c Report/PJUS/Export/Render OK")

# ══════════════════════════════════════
# WRITE OUTPUT
# ══════════════════════════════════════
html = ''.join(html_parts)
out = OUTPUT_PATH
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'OK — {len(html):,} bytes')
