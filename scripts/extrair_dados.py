#!/usr/bin/env python3
"""
PJUS - Extrator de Dados do Banco Argus (v6 - robust valor_face conversion)
GitHub Actions version - uses environment variables for DB credentials.
Handles: "R$ 130.000,00", "R$8211.21", "60 salarios minimos", "A CALCULAR", "106.421.15", etc.

RESTORED from original extrair_dados_argus.py with minimal path changes.
"""

import json
import os
import sys
import traceback
import math
from datetime import datetime

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Erro: psycopg2 nao encontrado. Rode: pip install psycopg2-binary")
    sys.exit(1)

CONN = {
    "host": os.environ.get("DB_HOST", "35.247.210.198"),
    "port": int(os.environ.get("DB_PORT", "5432")),
    "dbname": os.environ.get("DB_NAME", "argus"),
    "user": os.environ.get("DB_USER", "pjus_readonly"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "connect_timeout": 30,
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..")
ERROS = []

# Robust valor_face conversion using regex validation BEFORE casting
# Pattern 1: BRL format like "R$ 130.000,00" or "130.000,00" -> validated by regex
# Pattern 2: US/plain format like "R$8211.21" or "8211.21" -> validated by regex
# Anything else (text, malformed) -> NULL
VCONV = """CASE
    WHEN REGEXP_REPLACE(TRIM(COALESCE(valor_face,'')), '^R\\$\\s*', '') ~ '^\\d{1,3}(\\.\\d{3})*(,\\d+)?$' THEN
        REPLACE(REPLACE(REPLACE(REPLACE(valor_face, 'R$ ', ''), 'R$', ''), '.', ''), ',', '.')::numeric
    WHEN REGEXP_REPLACE(TRIM(COALESCE(valor_face,'')), '^R\\$\\s*', '') ~ '^\\d+(\\.\\d+)?$' THEN
        REPLACE(REPLACE(TRIM(valor_face), 'R$ ', ''), 'R$', '')::numeric
    ELSE NULL
END"""

# WHERE clause to filter only valid valor_face
VWHERE = f"({VCONV}) IS NOT NULL"

def serialize(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if hasattr(obj, '__float__'):
        return float(obj)
    return str(obj)

def save(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=serialize)
    size = os.path.getsize(path) / 1024
    print(f"  Salvo: {path} ({size:.1f} KB)")

def q(conn, sql, name):
    print(f"  [{name}]...", end=" ", flush=True)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        print(f"OK - {len(rows)} registros")
        cur.close()
        return rows
    except Exception as e:
        conn.rollback()
        msg = f"ERRO em {name}: {e}"
        print(msg)
        ERROS.append(msg)
        return []

def main():
    print("=" * 60)
    print("PJUS - Extracao de Dados v6 (GitHub Actions)")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    print("\nConectando...")
    try:
        conn = psycopg2.connect(**CONN)
        print("Conectado!\n")
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)

    D = {"meta": {"data_extracao": datetime.now().isoformat()}}

    # ── CONTAGENS ──
    print("--- CONTAGENS ---")
    D["contagens"] = q(conn, """
        SELECT
            (SELECT COUNT(*) FROM diarios_analise) AS diarios_analise,
            (SELECT COUNT(*) FROM djen_precatorio) AS djen_precatorio,
            (SELECT COUNT(*) FROM djen_publicacoes) AS djen_publicacoes
    """, "contagens")

    # ── DIARIOS_ANALISE ──
    print("\n--- DIARIOS_ANALISE ---")

    D["fontes_cobertura"] = q(conn, """
        SELECT fonte, COUNT(*) AS total,
               COUNT(DISTINCT data) AS dias,
               MIN(data) AS data_inicio, MAX(data) AS data_fim
        FROM diarios_analise
        GROUP BY fonte ORDER BY total DESC
    """, "fontes_cobertura")

    D["volume_diario_fonte"] = q(conn, """
        SELECT data, fonte, COUNT(*) AS total
        FROM diarios_analise
        WHERE data >= CURRENT_DATE - INTERVAL '60 days'
        GROUP BY data, fonte ORDER BY data DESC, total DESC
    """, "volume_diario_fonte")

    D["volume_diario_total"] = q(conn, """
        SELECT data, COUNT(*) AS total
        FROM diarios_analise
        GROUP BY data ORDER BY data DESC
    """, "volume_diario_total")

    D["top_precatorios_analise"] = q(conn, """
        SELECT hash, data, fonte, tipo, area,
               relevancia_precatorio, relevancia_negocios, resumo,
               detalhes_precatorio
        FROM diarios_analise
        WHERE relevancia_precatorio >= 4
        ORDER BY data DESC, relevancia_precatorio DESC
        LIMIT 300
    """, "top_precatorios_analise")

    D["areas_legais"] = q(conn, """
        SELECT area, COUNT(*) AS total,
               ROUND(AVG(relevancia_precatorio)::numeric, 1) AS avg_prec,
               ROUND(AVG(relevancia_negocios)::numeric, 1) AS avg_neg
        FROM diarios_analise WHERE area IS NOT NULL
        GROUP BY area ORDER BY total DESC
    """, "areas_legais")

    # ── DJEN_PRECATORIO ──
    print("\n--- DJEN_PRECATORIO ---")

    D["entes_devedores"] = q(conn, f"""
        SELECT ente_devedor_ia AS nome,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT sigla_tribunal) AS num_tribs
        FROM djen_precatorio
        WHERE ente_devedor_ia IS NOT NULL AND ente_devedor_ia != ''
        GROUP BY ente_devedor_ia
        ORDER BY val DESC NULLS LAST
        LIMIT 50
    """, "entes_devedores")

    # Pipeline: only commercially actionable phases
    # Excluded: 'outro' (classification residue), 'pago_levantado' (already paid, score ~1),
    # 'cedido' (already assigned, score ~1), 'muito_cedo' (immature, score ~1),
    # 'coletiva_servidores' (different context), plus rare/invalid phases
    PIPELINE_FASES = (
        "'calculo_homologado',"   # Calculation approved — monitor
        "'expedicao_ativa',"      # Active expedition — hot opportunity
        "'expedicao_bloqueada',"  # Blocked expedition — investigate
        "'honorarios_sucumbenciais'"  # Attorney fees — niche
    )

    D["pipeline_fase"] = q(conn, f"""
        SELECT fase_pjus AS fase,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio
        FROM djen_precatorio
        WHERE fase_pjus IN ({PIPELINE_FASES})
        GROUP BY fase_pjus ORDER BY vol DESC
    """, "pipeline_fase")

    D["pipeline_mensal"] = q(conn, f"""
        SELECT fase_pjus AS fase,
               EXTRACT(YEAR FROM data_disponibilizacao)::int AS y,
               EXTRACT(MONTH FROM data_disponibilizacao)::int AS m,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val
        FROM djen_precatorio
        WHERE fase_pjus IN ({PIPELINE_FASES})
          AND data_disponibilizacao >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY fase_pjus, y, m ORDER BY fase, y, m
    """, "pipeline_mensal")

    # Oportunidades query — uses VCONV for robust valor conversion
    D["oportunidades"] = q(conn, f"""
        SELECT data_disponibilizacao AS data,
               sigla_tribunal AS trib,
               score_interesse AS score,
               fase_pjus AS fase,
               acao_pjus AS acao,
               ente_devedor_ia AS ente_devedor,
               ({VCONV}) AS valor,
               beneficiarios_ia AS beneficiarios,
               advogados_ia AS advogados,
               resumo_ia AS resumo
        FROM djen_precatorio
        WHERE score_interesse >= 3
          AND data_disponibilizacao >= CURRENT_DATE - INTERVAL '3 months'
        ORDER BY data_disponibilizacao DESC, score_interesse DESC
        LIMIT 500
    """, "oportunidades")

    D["alertas"] = q(conn, f"""
        SELECT data_disponibilizacao AS data,
               sigla_tribunal AS trib,
               score_interesse AS score,
               fase_pjus AS fase,
               acao_pjus AS acao,
               ente_devedor_ia AS ente_devedor,
               ({VCONV}) AS valor,
               beneficiarios_ia AS beneficiarios,
               advogados_ia AS advogados,
               resumo_ia AS resumo
        FROM djen_precatorio
        WHERE score_interesse >= 4
          AND data_disponibilizacao >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY score_interesse DESC, ({VCONV}) DESC NULLS LAST
        LIMIT 200
    """, "alertas")

    D["faixas_valor"] = q(conn, f"""
        SELECT
            CASE
                WHEN ({VCONV}) < 100000 THEN '< 100K'
                WHEN ({VCONV}) < 500000 THEN '100K - 500K'
                WHEN ({VCONV}) < 1000000 THEN '500K - 1M'
                WHEN ({VCONV}) < 5000000 THEN '1M - 5M'
                WHEN ({VCONV}) < 10000000 THEN '5M - 10M'
                ELSE '> 10M'
            END AS faixa,
            COUNT(*) AS qtd,
            COALESCE(SUM({VCONV}), 0) AS valor_total,
            ROUND(AVG(score_interesse)::numeric, 1) AS score_medio
        FROM djen_precatorio
        WHERE {VWHERE} AND ({VCONV}) > 0
        GROUP BY faixa ORDER BY MIN({VCONV})
    """, "faixas_valor")

    D["heatmap_tribunal"] = q(conn, f"""
        SELECT sigla_tribunal AS trib,
               EXTRACT(YEAR FROM data_disponibilizacao)::int AS y,
               EXTRACT(MONTH FROM data_disponibilizacao)::int AS m,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio
        FROM djen_precatorio
        WHERE data_disponibilizacao >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY sigla_tribunal, y, m ORDER BY trib, y, m
    """, "heatmap_tribunal")

    D["volume_tribunal"] = q(conn, f"""
        SELECT sigla_tribunal AS trib,
               COUNT(*) AS total,
               COALESCE(SUM({VCONV}), 0) AS valor_total,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT data_disponibilizacao) AS dias,
               MIN(data_disponibilizacao) AS data_inicio,
               MAX(data_disponibilizacao) AS data_fim
        FROM djen_precatorio
        GROUP BY sigla_tribunal ORDER BY total DESC
    """, "volume_tribunal")

    D["tendencia_tribunal"] = q(conn, f"""
        SELECT sigla_tribunal AS trib,
               EXTRACT(YEAR FROM data_disponibilizacao)::int AS y,
               EXTRACT(MONTH FROM data_disponibilizacao)::int AS m,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val
        FROM djen_precatorio
        WHERE data_disponibilizacao >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY sigla_tribunal, y, m ORDER BY trib, y, m
    """, "tendencia_tribunal")

    # Top beneficiarios — hybrid ranking: valor + volume
    # Merges top-30-by-valor + top-30-by-pubs, ranked by composite score
    BENEF_BASE = f"""
        SELECT COALESCE(b->>'nome', b::text) AS nome,
               COUNT(*) AS pubs,
               COALESCE(SUM({VCONV}), 0) AS valor_total,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT sigla_tribunal) AS num_tribs
        FROM djen_precatorio,
             LATERAL jsonb_array_elements(beneficiarios_ia) AS b
        WHERE beneficiarios_ia IS NOT NULL
          AND jsonb_array_length(beneficiarios_ia) > 0
          AND score_interesse >= 3
        GROUP BY COALESCE(b->>'nome', b::text)
        HAVING COALESCE(b->>'nome', b::text) IS NOT NULL
           AND COALESCE(b->>'nome', b::text) != ''
           AND LENGTH(COALESCE(b->>'nome', b::text)) > 3
    """
    benef_by_val = q(conn, BENEF_BASE + f" AND COALESCE(SUM({VCONV}), 0) > 0 ORDER BY valor_total DESC LIMIT 30", "benef_by_valor")
    benef_by_pub = q(conn, BENEF_BASE + " ORDER BY pubs DESC LIMIT 30", "benef_by_pubs")

    benef_merged = {}
    for b in (benef_by_val or []):
        benef_merged[b['nome']] = b
    for b in (benef_by_pub or []):
        if b['nome'] not in benef_merged:
            benef_merged[b['nome']] = b

    for b in benef_merged.values():
        val = float(b.get('valor_total') or 0)
        pubs = int(b.get('pubs') or 1)
        b['_score'] = (math.log10(val + 1) * 10 if val > 0 else 0) + math.log10(pubs + 1) * 5

    benef_sorted = sorted(benef_merged.values(), key=lambda x: -x['_score'])[:50]

    # Get advogado principal for each beneficiario
    print("  [benef_advogados]...", end=" ", flush=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    for b in benef_sorted:
        try:
            cur.execute("""
                SELECT COALESCE(a->>'nome', '') AS adv_nome, a->>'oab' AS adv_oab, COUNT(*) AS n
                FROM djen_precatorio dp,
                     LATERAL jsonb_array_elements(dp.beneficiarios_ia) AS b2,
                     LATERAL jsonb_array_elements(dp.advogados_ia) AS a
                WHERE COALESCE(b2->>'nome', b2::text) = %s
                  AND dp.advogados_ia IS NOT NULL AND jsonb_array_length(dp.advogados_ia) > 0
                GROUP BY COALESCE(a->>'nome', ''), a->>'oab'
                ORDER BY n DESC LIMIT 1
            """, (b['nome'],))
            row = cur.fetchone()
            b['advogado_principal'] = row['adv_nome'] if row and row['adv_nome'] else None
            b['oab_principal'] = row['adv_oab'] if row else None
        except Exception:
            b['advogado_principal'] = None
            b['oab_principal'] = None
    for b in benef_sorted:
        b.pop('_score', None)
    print(f"{len(benef_sorted)} OK")
    D["top_beneficiarios"] = benef_sorted

    # Top advogados — hybrid ranking: valor + volume
    ADV_BASE = f"""
        SELECT COALESCE(a->>'nome', a::text) AS nome,
               a->>'oab' AS oab,
               COUNT(*) AS pubs,
               COALESCE(SUM({VCONV}), 0) AS valor_total,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT sigla_tribunal) AS num_tribs
        FROM djen_precatorio,
             LATERAL jsonb_array_elements(advogados_ia) AS a
        WHERE advogados_ia IS NOT NULL
          AND jsonb_array_length(advogados_ia) > 0
          AND score_interesse >= 3
        GROUP BY COALESCE(a->>'nome', a::text), a->>'oab'
        HAVING COALESCE(a->>'nome', a::text) IS NOT NULL
           AND COALESCE(a->>'nome', a::text) != ''
           AND LENGTH(COALESCE(a->>'nome', a::text)) > 3
    """
    adv_by_val = q(conn, ADV_BASE + f" AND COALESCE(SUM({VCONV}), 0) > 0 ORDER BY valor_total DESC LIMIT 30", "adv_by_valor")
    adv_by_pub = q(conn, ADV_BASE + " ORDER BY pubs DESC LIMIT 30", "adv_by_pubs")

    adv_merged = {}
    for a in (adv_by_val or []):
        adv_merged[a['nome']] = a
    for a in (adv_by_pub or []):
        if a['nome'] not in adv_merged:
            adv_merged[a['nome']] = a

    for a in adv_merged.values():
        val = float(a.get('valor_total') or 0)
        pubs = int(a.get('pubs') or 1)
        a['_score'] = (math.log10(val + 1) * 10 if val > 0 else 0) + math.log10(pubs + 1) * 5

    adv_sorted = sorted(adv_merged.values(), key=lambda x: -x['_score'])[:50]
    adv_sorted = [a for a in adv_sorted if a.get('nome') and 'null' not in str(a['nome']).lower()]
    for a in adv_sorted:
        a.pop('_score', None)
    D["top_advogados"] = adv_sorted

    # ── AMAPÁ DETALHADO ──
    print("\n--- AMAPA ---")

    D["amapa_precatorio"] = q(conn, f"""
        SELECT sigla_tribunal AS trib,
               EXTRACT(YEAR FROM data_disponibilizacao)::int AS y,
               EXTRACT(MONTH FROM data_disponibilizacao)::int AS m,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(CASE WHEN score_interesse >= 4 THEN 1 END) AS high_score
        FROM djen_precatorio WHERE sigla_tribunal = 'TJAP'
        GROUP BY sigla_tribunal, y, m ORDER BY y, m
    """, "amapa_precatorio")

    D["amapa_oportunidades"] = q(conn, """
        SELECT data_disponibilizacao AS data,
               score_interesse AS score,
               fase_pjus AS fase,
               ente_devedor_ia AS ente_devedor,
               valor_face AS valor,
               resumo_ia AS resumo
        FROM djen_precatorio
        WHERE sigla_tribunal = 'TJAP' AND score_interesse >= 3
        ORDER BY data_disponibilizacao DESC, score_interesse DESC
        LIMIT 50
    """, "amapa_oportunidades")

    conn.close()
    D["erros"] = ERROS

    print("\n--- SALVANDO ---")
    path = os.path.join(OUTPUT_DIR, "data", "dados_argus.json")
    save(D, path)

    print(f"\nConcluido! {len(ERROS)} erros.")
    if ERROS:
        for e in ERROS:
            print(f"  - {e}")
    print()

if __name__ == "__main__":
    main()
