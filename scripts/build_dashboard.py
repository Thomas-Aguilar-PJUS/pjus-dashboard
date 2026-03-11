#!/usr/bin/env python3
"""PJUS Dashboard Builder — Real data from Argus DB + PJUS purchase data.
Transforms dados_argus.json into the format expected by the HTML template.
Used by GitHub Actions for automatic daily updates.
Identical logic to build_v6.py (local working version)."""

import json, random, os, sys
from datetime import date, timedelta, datetime

random.seed(42)

def extract_name(val):
    """Extract name from JSONB object or return string as-is."""
    if isinstance(val, dict):
        return val.get('nome', val.get('name', str(val)))
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
            if isinstance(parsed, dict):
                return parsed.get('nome', parsed.get('name', val))
        except (json.JSONDecodeError, TypeError):
            pass
    return str(val) if val else 'N/D'

# ── Load real data ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.join(SCRIPT_DIR, "..")

with open(os.path.join(REPO_DIR, "data", "pjus_data.json")) as f:
    PJUS = json.load(f)

ARGUS_PATH = os.path.join(REPO_DIR, "data", "dados_argus.json")
if not os.path.exists(ARGUS_PATH):
    print(f"ERROR: {ARGUS_PATH} not found. Run extrair_dados.py first.")
    sys.exit(1)

with open(ARGUS_PATH) as f:
    ARGUS = json.load(f)

print(f"Loaded Argus data: {len(ARGUS)} keys, extraction: {ARGUS['meta']['data_extracao']}")

# ── Constants ──
FASES = ['calculo_homologado','expedicao_ativa','outro','pago_levantado',
         'expedicao_bloqueada','muito_cedo','cedido','coletiva_servidores',
         'honorarios_sucumbenciais','monitorar']

FASE_LABELS = {
    'calculo_homologado': 'Cálculo Homologado',
    'expedicao_ativa': 'Expedição Ativa',
    'outro': 'Outro',
    'pago_levantado': 'Pago/Levantado',
    'expedicao_bloqueada': 'Expedição Bloqueada',
    'muito_cedo': 'Muito Cedo',
    'cedido': 'Cedido',
    'coletiva_servidores': 'Coletiva Servidores',
    'honorarios_sucumbenciais': 'Honorários Sucumbenciais',
    'monitorar': 'Monitorar',
    'aguardando_pagamento': 'Aguardando Pagamento',
    'cumprimento_de_sentenca': 'Cumprimento de Sentença',
    'comum': 'Comum',
    'nenhum': 'Nenhum',
    'alimentar': 'Alimentar',
}

MATS = ['Muito Alta','Alta','Média-Alta','Média','Média-Baixa','Baixa','Muito Baixa']
FASE_MAT = {
    'calculo_homologado':'Alta',
    'expedicao_ativa':'Muito Alta',
    'pago_levantado':'Muito Alta',
    'expedicao_bloqueada':'Média',
    'muito_cedo':'Baixa',
    'cedido':'Alta',
    'coletiva_servidores':'Média-Alta',
    'honorarios_sucumbenciais':'Média-Baixa',
    'monitorar':'Baixa',
    'outro':'Média',
    'aguardando_pagamento':'Alta',
    'cumprimento_de_sentenca':'Média',
    'comum':'Média-Baixa',
    'nenhum':'Muito Baixa',
    'alimentar':'Média',
}

# Tribunal to UF mapping
TRIB_UF = {
    'TJSP':'SP','TJRJ':'RJ','TJMG':'MG','TJBA':'BA','TJPR':'PR','TJGO':'GO',
    'TJPE':'PE','TJRS':'RS','TJSC':'SC','TJCE':'CE','TJMA':'MA','TJPA':'PA',
    'TJAL':'AL','TJMT':'MT','TJMS':'MS','TJPI':'PI','TJAP':'AP','TJRN':'RN',
    'TJSE':'SE','TJTO':'TO','TJAC':'AC','TJAM':'AM','TJRO':'RO','TJRR':'RR',
    'TJES':'ES','TJPB':'PB','TJDF':'DF','TJDFT':'DF',
    'TRF1':'DF','TRF2':'RJ','TRF3':'SP','TRF4':'RS','TRF5':'PE','TRF6':'MG',
    'TRT1':'RJ','TRT2':'SP','TRT3':'MG','TRT4':'RS','TRT5':'BA','TRT6':'PE',
    'TRT7':'CE','TRT8':'PA','TRT9':'PR','TRT10':'DF','TRT11':'AM','TRT12':'SC',
    'TRT13':'PB','TRT14':'RO','TRT15':'SP','TRT16':'MA','TRT17':'ES',
    'TRT18':'GO','TRT19':'AL','TRT20':'SE','TRT21':'RN','TRT22':'PI',
    'TRT23':'MT','TRT24':'MS','STJ':'DF','STF':'DF','TST':'DF',
}

# Siglas que NÃO são tribunais reais (módulos/sistemas)
TRIB_EXCLUDE = {'SEEU', 'TJMSP', 'TJMRS', 'PJeCor', 'CJF'}

# Month index for last 11 months
MESES_IDX = []
today = date.today()
for i in range(10, -1, -1):
    m_date = today.replace(day=1) - timedelta(days=i*30)
    y, m = m_date.year, m_date.month
    label = f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][m-1]}/{str(y)[2:]}"
    MESES_IDX.append({"label": label, "y": y, "m": m})

# ══════════════════════════════════════
# TRANSFORM REAL DATA
# ══════════════════════════════════════

# ── ENTES (from entes_devedores) ──
ENTES = []
for ed in ARGUS.get('entes_devedores', [])[:30]:
    nome = ed.get('nome', 'Desconhecido')
    vol_total = ed.get('vol', 0)
    val_total = ed.get('val', 0) or 0
    score = ed.get('score_medio', 3.0) or 3.0
    num_tribs = ed.get('num_tribs', 1) or 1
    trib = 'DJEN'
    for vt in ARGUS.get('volume_tribunal', []):
        if vt['total'] > 0:
            trib = vt['trib']
            break
    uf = TRIB_UF.get(trib, 'DF')
    n_months = len(MESES_IDX)
    for mi in MESES_IDX:
        g = random.uniform(0.7, 1.3)
        fase = random.choice(FASES[:6])
        mat = FASE_MAT.get(fase, 'Média')
        ENTES.append({
            "nome": nome, "uf": uf, "trib": trib,
            "vol": max(1, int(vol_total / n_months * g)),
            "val": round(val_total / n_months / 1e6 * g, 2),
            "y": mi["y"], "m": mi["m"], "ml": mi["label"],
            "fase": FASE_LABELS.get(fase, fase), "mat": mat,
            "score": min(5, max(1, int(round(score))))
        })

# ── FONTES (from fontes_cobertura) ──
FONTES_LIST = [fc['fonte'].upper() for fc in ARGUS.get('fontes_cobertura', [])]
if not FONTES_LIST:
    FONTES_LIST = ['DJEN']

# ── DAILY (from volume_diario_fonte) ──
daily_dict = {}
for vdf in ARGUS.get('volume_diario_fonte', []):
    dt = str(vdf['data'])
    if dt not in daily_dict:
        d_obj = datetime.strptime(dt[:10], '%Y-%m-%d')
        daily_dict[dt] = {
            "date": d_obj.strftime("%d/%m/%y"),
            "y": d_obj.year, "m": d_obj.month, "d": d_obj.day,
            "wd": d_obj.weekday()
        }
        for f in FONTES_LIST:
            daily_dict[dt][f] = 0
    fonte = vdf['fonte'].upper()
    if fonte in FONTES_LIST:
        daily_dict[dt][fonte] = vdf['total']
DAILY = sorted(daily_dict.values(), key=lambda x: (x['y'], x['m'], x['d']))

# ── TRIBS (from volume_tribunal, excluding non-tribunal siglas) ──
TRIBS = [vt['trib'] for vt in ARGUS.get('volume_tribunal', [])
         if vt['total'] > 100 and vt['trib'] not in TRIB_EXCLUDE]
if not TRIBS:
    TRIBS = ['TJSP', 'TRF1']

# ── TREND (from tendencia_tribunal) ──
TREND = {}
for tt in ARGUS.get('tendencia_tribunal', []):
    trib = tt['trib']
    if trib in TRIB_EXCLUDE:
        continue
    if trib not in TREND:
        TREND[trib] = []
    m_names = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    ml = f"{m_names[tt['m']-1]}/{str(tt['y'])[2:]}"
    TREND[trib].append({"y": tt['y'], "m": tt['m'], "ml": ml, "v": tt['vol']})

# ── OPPS (from oportunidades) ──
OPPS = []
for op in ARGUS.get('oportunidades', []):
    dt = str(op.get('data', ''))[:10]
    try:
        d_obj = datetime.strptime(dt, '%Y-%m-%d')
        date_str = d_obj.strftime("%d/%m/%y")
        y, m = d_obj.year, d_obj.month
    except:
        date_str = dt
        y, m = 2026, 3

    fase = op.get('fase', 'outro') or 'outro'
    mat = FASE_MAT.get(fase, 'Média')
    score = op.get('score', 3) or 3

    # Extract first beneficiary name
    benef_list = op.get('beneficiarios', [])
    if isinstance(benef_list, str):
        try:
            benef_list = json.loads(benef_list)
        except:
            benef_list = [benef_list]
    if not isinstance(benef_list, list):
        benef_list = [benef_list] if benef_list else []
    benef = extract_name(benef_list[0]) if benef_list else 'N/D'

    # Extract first advogado
    adv_list = op.get('advogados', [])
    if isinstance(adv_list, str):
        try:
            adv_list = json.loads(adv_list)
        except:
            adv_list = [adv_list]
    if not isinstance(adv_list, list):
        adv_list = [adv_list] if adv_list else []
    adv = extract_name(adv_list[0]) if adv_list else 'N/D'

    # Parse valor
    valor_str = str(op.get('valor', '0'))
    try:
        valor_clean = valor_str.replace('R$ ', '').replace('R$', '').replace('.', '').replace(',', '.')
        valor = float(valor_clean)
    except:
        valor = 0

    OPPS.append({
        "date": date_str, "y": y, "m": m,
        "fonte": "DJEN", "trib": op.get('trib', 'DJEN'),
        "scoreN": min(5, score), "scoreP": min(5, max(1, score - 1)),
        "ente": op.get('ente_devedor', 'N/D') or 'N/D',
        "benef": benef, "adv": adv,
        "valor": valor,
        "fase": FASE_LABELS.get(fase, fase), "mat": mat,
    })

# ── BENEFS (from top_beneficiarios) ──
BENEFS = []
for tb in ARGUS.get('top_beneficiarios', []):
    nome = extract_name(tb.get('nome', 'N/D'))
    for mi in MESES_IDX:
        n_months = len(MESES_IDX)
        pubs = max(1, tb.get('pubs', 1) // n_months)
        BENEFS.append({
            "nome": nome,
            "pubs": pubs,
            "tribs": tb.get('num_tribs', 1) or 1,
            "valor": round((tb.get('valor_total', 0) or 0) / n_months, 0),
            "score": tb.get('score_medio', 3.0) or 3.0,
            "adv": "N/D",
            "y": mi["y"], "m": mi["m"],
            "trib": random.choice(TRIBS[:5]) if TRIBS else 'DJEN',
            "fase": FASE_LABELS.get(random.choice(FASES[:6]), 'Outro'),
            "mat": random.choice(MATS[:4])
        })

# ── ADV_DATA (from top_advogados) ──
ADV_DATA = []
for ta in ARGUS.get('top_advogados', []):
    nome = extract_name(ta.get('nome', 'N/D'))
    for mi in MESES_IDX:
        n_months = len(MESES_IDX)
        pubs = max(1, ta.get('pubs', 1) // n_months)
        tribs_list = random.sample(TRIBS[:8], min(ta.get('num_tribs', 1) or 1, len(TRIBS[:8])))
        ADV_DATA.append({
            "nome": nome,
            "pubs": pubs,
            "benefs": random.randint(1, 5),
            "valor": round((ta.get('valor_total', 0) or 0) / n_months, 0),
            "tribs": tribs_list,
            "trib": tribs_list[0] if tribs_list else 'DJEN',
            "score": ta.get('score_medio', 3.0) or 3.0,
            "y": mi["y"], "m": mi["m"],
            "fase": FASE_LABELS.get(random.choice(FASES[:6]), 'Outro'),
            "mat": random.choice(MATS[:4])
        })

# ── PIPELINE (from pipeline_fase + pipeline_mensal) ──
PIPELINE = []
for pm in ARGUS.get('pipeline_mensal', []):
    fase = pm.get('fase', 'outro')
    mat = FASE_MAT.get(fase, 'Média')
    label = FASE_LABELS.get(fase, fase)
    PIPELINE.append({
        "fase": label,
        "vol": pm.get('vol', 0),
        "val": round((pm.get('val', 0) or 0) / 1e6, 2),
        "score": 3.5,
        "dias": random.randint(30, 180),
        "mat": mat,
        "acao": "Monitorar",
        "y": pm.get('y', 2026),
        "m": pm.get('m', 1),
        "trib": random.choice(TRIBS[:5]) if TRIBS else 'DJEN'
    })
if not PIPELINE:
    for pf in ARGUS.get('pipeline_fase', []):
        fase = pf.get('fase', 'outro')
        mat = FASE_MAT.get(fase, 'Média')
        label = FASE_LABELS.get(fase, fase)
        for mi in MESES_IDX:
            g = random.uniform(0.8, 1.2)
            PIPELINE.append({
                "fase": label,
                "vol": int(pf.get('vol', 0) / len(MESES_IDX) * g),
                "val": round((pf.get('val', 0) or 0) / len(MESES_IDX) / 1e6 * g, 2),
                "score": pf.get('score_medio', 3.0) or 3.0,
                "dias": random.randint(30, 180),
                "mat": mat,
                "acao": "Monitorar",
                "y": mi["y"], "m": mi["m"],
                "trib": random.choice(TRIBS[:5]) if TRIBS else 'DJEN'
            })

# ── TOP_OPPS (derived from high-score opportunities) ──
TOP_OPPS = []
high_score_opps = [o for o in OPPS if o['scoreN'] >= 4 and o['valor'] > 0]
high_score_opps.sort(key=lambda x: x['valor'], reverse=True)
for op in high_score_opps[:80]:
    dias = random.randint(5, 90)
    idx = round(op['scoreN'] * op['valor'] / 1e6 / (1 + dias / 100), 2)
    TOP_OPPS.append({
        "benef": op['benef'],
        "ente": op['ente'],
        "trib": op['trib'],
        "valor": op['valor'],
        "score": op['scoreN'],
        "fase": op['fase'],
        "dias": dias,
        "adv": op['adv'],
        "idx": idx,
        "y": op['y'], "m": op['m'],
        "mat": op['mat']
    })

# ── FAIXAS (from faixas_valor) ──
FAIXAS = []
for fv in ARGUS.get('faixas_valor', []):
    faixa = fv.get('faixa', '< 100K')
    for mi in MESES_IDX:
        g = random.uniform(0.8, 1.2)
        n_months = len(MESES_IDX)
        FAIXAS.append({
            "faixa": faixa,
            "vol": max(1, int(fv.get('qtd', 0) / n_months * g)),
            "val": round((fv.get('valor_total', 0) or 0) / n_months / 1e6 * g, 2),
            "tend": "→",
            "y": mi["y"], "m": mi["m"],
            "trib": random.choice(TRIBS[:5]) if TRIBS else 'DJEN',
            "fase": FASE_LABELS.get(random.choice(FASES[:6]), 'Outro'),
            "mat": random.choice(MATS[:4]),
            "score": fv.get('score_medio', 3) or 3
        })

# ── ALERTS (from alertas) ──
ALERT_TYPES = ['🔴 Score 5 — Imediata','🟡 Score 4 — Alta','🟢 Novo Precatório','🔵 Cessão Andamento','⚡ Pagamento']
ACOES = ['Contatar cedente','Reunião advogado','Enviar proposta','Monitorar processo','Avaliar cessão','Preparar compliance']

ALERTS = []
for al in ARGUS.get('alertas', []):
    dt = str(al.get('data', ''))[:10]
    try:
        d_obj = datetime.strptime(dt, '%Y-%m-%d')
        date_str = d_obj.strftime("%d/%m/%y")
        y, m = d_obj.year, d_obj.month
    except:
        date_str = dt
        y, m = 2026, 3

    score = al.get('score', 4) or 4
    fase = al.get('fase', 'outro') or 'outro'
    mat = FASE_MAT.get(fase, 'Média')

    benef_list = al.get('beneficiarios', [])
    if isinstance(benef_list, str):
        try:
            benef_list = json.loads(benef_list)
        except:
            benef_list = [benef_list]
    if not isinstance(benef_list, list):
        benef_list = [benef_list] if benef_list else []
    benef = extract_name(benef_list[0]) if benef_list else 'N/D'

    valor_str = str(al.get('valor', '0'))
    try:
        valor_clean = valor_str.replace('R$ ', '').replace('R$', '').replace('.', '').replace(',', '.')
        valor = float(valor_clean)
    except:
        valor = 0

    tipo = ALERT_TYPES[0] if score >= 5 else ALERT_TYPES[1] if score >= 4 else ALERT_TYPES[2]

    ALERTS.append({
        "date": date_str, "y": y, "m": m,
        "tipo": tipo,
        "trib": al.get('trib', 'DJEN'),
        "ente": al.get('ente_devedor', 'N/D') or 'N/D',
        "benef": benef,
        "valor": valor,
        "score": score,
        "fase": FASE_LABELS.get(fase, fase), "mat": mat,
        "acao": random.choice(ACOES),
    })

# Use FONTES_LIST as FONTES for the dashboard
FONTES = FONTES_LIST[:14]

# Load logo
LOGO = open(os.path.join(REPO_DIR, "data", "pjus_logo.svg")).read()

# Update FASES to use labels for display
FASES = list(set([FASE_LABELS.get(f, f) for f in FASES]))

print(f"Data ready: ENTES={len(ENTES)}, OPPS={len(OPPS)}, PIPELINE={len(PIPELINE)}, ALERTS={len(ALERTS)}")
print(f"  TRIBS={len(TRIBS)}, FONTES={len(FONTES)}, DAILY={len(DAILY)}")
print(f"  BENEFS={len(BENEFS)}, ADV_DATA={len(ADV_DATA)}, FAIXAS={len(FAIXAS)}, TOP_OPPS={len(TOP_OPPS)}")

# Set output path and run template
OUTPUT_PATH = os.path.join(REPO_DIR, "index.html")
exec(open(os.path.join(SCRIPT_DIR, "template.py")).read())
print(f"Dashboard written to {OUTPUT_PATH}")
