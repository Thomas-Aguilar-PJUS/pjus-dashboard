#!/usr/bin/env python3
"""
PJUS - Extrator de Dados do Banco Argus (GitHub Actions version)
Uses environment variables for DB credentials.
"""

import json
import os
import sys
from datetime import datetime

import psycopg2
import psycopg2.extras

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

# Robust valor_face conversion
VCONV = """CASE
    WHEN REGEXP_REPLACE(TRIM(COALESCE(valor_face,'')), '^R\\$\\s*', '') ~ '^\\d{1,3}(\\.\\d{3})*(,\\d+)?$' THEN
        REPLACE(REPLACE(REPLACE(REPLACE(valor_face, 'R$ ', ''), 'R$', ''), '.', ''), ',', '.')::numeric
    WHEN REGEXP_REPLACE(TRIM(COALESCE(valor_face,'')), '^R\\$\\s*', '') ~ '^\\d+(\\.\\d+)?$' THEN
        REPLACE(REPLACE(TRIM(valor_face), 'R$ ', ''), 'R$', '')::numeric
    ELSE NULL
END"""

VWHERE = f"({VCONV}) IS NOT NULL"


def serialize(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if hasattr(obj, '__float__'):
        return float(obj)
    return str(obj)


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
    print("PJUS - Extracao de Dados (GitHub Actions)")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    print("\nConectando...")
    try:
        conn = psycopg2.connect(**CONN)
        print("Conectado!\n")
    except Exception as e:
        print(f"ERRO de conexao: {e}")
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

    D["pipeline_fase"] = q(conn, f"""
        SELECT fase_pjus AS fase,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio
        FROM djen_precatorio
        WHERE fase_pjus IS NOT NULL AND fase_pjus != ''
        GROUP BY fase_pjus ORDER BY vol DESC
    """, "pipeline_fase")

    D["pipeline_mensal"] = q(conn, f"""
        SELECT fase_pjus AS fase,
               EXTRACT(YEAR FROM data_disponibilizacao)::int AS y,
               EXTRACT(MONTH FROM data_disponibilizacao)::int AS m,
               COUNT(*) AS vol,
               COALESCE(SUM({VCONV}), 0) AS val
        FROM djen_precatorio
        WHERE fase_pjus IS NOT NULL
          AND data_disponibilizacao >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY fase_pjus, y, m ORDER BY fase, y, m
    """, "pipeline_mensal")

    D["oportunidades"] = q(conn, """
        SELECT data_disponibilizacao AS data,
               sigla_tribunal AS trib,
               score_interesse AS score,
               fase_pjus AS fase,
               acao_pjus AS acao,
               ente_devedor_ia AS ente_devedor,
               valor_face AS valor,
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
               valor_face AS valor,
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

    D["top_beneficiarios"] = q(conn, f"""
        SELECT COALESCE(b->>'nome', b#>>'{{}}') AS nome,
               COUNT(*) AS pubs,
               COALESCE(SUM({VCONV}), 0) AS valor_total,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT sigla_tribunal) AS num_tribs
        FROM djen_precatorio,
             LATERAL jsonb_array_elements(beneficiarios_ia) AS b
        WHERE beneficiarios_ia IS NOT NULL
          AND jsonb_array_length(beneficiarios_ia) > 0
          AND score_interesse >= 3
        GROUP BY nome ORDER BY pubs DESC LIMIT 50
    """, "top_beneficiarios")

    D["top_advogados"] = q(conn, f"""
        SELECT COALESCE(a->>'nome', a#>>'{{}}') AS nome,
               COUNT(*) AS pubs,
               COALESCE(SUM({VCONV}), 0) AS valor_total,
               ROUND(AVG(score_interesse)::numeric, 1) AS score_medio,
               COUNT(DISTINCT sigla_tribunal) AS num_tribs
        FROM djen_precatorio,
             LATERAL jsonb_array_elements(advogados_ia) AS a
        WHERE advogados_ia IS NOT NULL
          AND jsonb_array_length(advogados_ia) > 0
          AND score_interesse >= 3
        GROUP BY nome ORDER BY pubs DESC LIMIT 50
    """, "top_advogados")

    # ── AMAPÁ ──
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

    # Save to repo root as data.json
    path = os.path.join(OUTPUT_DIR, "data", "dados_argus.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False, indent=2, default=serialize)
    size = os.path.getsize(path) / 1024
    print(f"\nSalvo: {path} ({size:.1f} KB)")
    print(f"Concluido! {len(ERROS)} erros.")
    if ERROS:
        for e in ERROS:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
