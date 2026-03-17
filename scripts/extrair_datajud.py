#!/usr/bin/env python3
"""
Extrator Histórico via API DataJud (CNJ)
=========================================
Consulta a API pública DataJud para obter movimentações históricas de
processos de precatórios e gera dados compatíveis com o dashboard.

A API DataJud retorna metadados processuais (movimentos, classe, órgão)
por tribunal, com filtros de data funcionais.

Uso:
  python extrair_historico_datajud.py --test            # 1 tribunal, 1 mês
  python extrair_historico_datajud.py --months 12       # 12 meses
  python extrair_historico_datajud.py --aggregate       # Gerar JSON para dashboard
  python extrair_historico_datajud.py --status          # Status do banco
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import date, datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ── Configuração ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "data", "dados_historico.db")

API_KEY = os.environ.get("DATAJUD_API_KEY", "")
API_BASE = "https://api-publica.datajud.cnj.jus.br"

# Rate limiting
DELAY_BETWEEN_REQUESTS = 1.0
DELAY_ON_ERROR = 10.0
MAX_RETRIES = 3
BATCH_SIZE = 500  # items per search request (API limit ~10K)

# Tribunais com alias DataJud
TRIBUNAIS = {
    # Estaduais
    "TJAC": "api_publica_tjac", "TJAL": "api_publica_tjal", "TJAM": "api_publica_tjam",
    "TJAP": "api_publica_tjap", "TJBA": "api_publica_tjba", "TJCE": "api_publica_tjce",
    "TJDFT": "api_publica_tjdft", "TJES": "api_publica_tjes", "TJGO": "api_publica_tjgo",
    "TJMA": "api_publica_tjma", "TJMG": "api_publica_tjmg", "TJMS": "api_publica_tjms",
    "TJMT": "api_publica_tjmt", "TJPA": "api_publica_tjpa", "TJPB": "api_publica_tjpb",
    "TJPE": "api_publica_tjpe", "TJPI": "api_publica_tjpi", "TJPR": "api_publica_tjpr",
    "TJRJ": "api_publica_tjrj", "TJRN": "api_publica_tjrn", "TJRO": "api_publica_tjro",
    "TJRR": "api_publica_tjrr", "TJRS": "api_publica_tjrs", "TJSC": "api_publica_tjsc",
    "TJSE": "api_publica_tjse", "TJSP": "api_publica_tjsp", "TJTO": "api_publica_tjto",
    # Federais
    "TRF1": "api_publica_trf1", "TRF2": "api_publica_trf2", "TRF3": "api_publica_trf3",
    "TRF4": "api_publica_trf4", "TRF5": "api_publica_trf5", "TRF6": "api_publica_trf6",
    # Trabalhistas
    "TRT1": "api_publica_trt1", "TRT2": "api_publica_trt2", "TRT3": "api_publica_trt3",
    "TRT4": "api_publica_trt4", "TRT5": "api_publica_trt5",
    # Superiores
    "STJ": "api_publica_stj", "TST": "api_publica_tst",
}


# ── SQLite ────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS movimentos_mensais (
            tribunal TEXT NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            classe TEXT NOT NULL,
            total_processos INTEGER NOT NULL,
            extraido_em TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (tribunal, ano, mes, classe)
        );
        CREATE TABLE IF NOT EXISTS extracao_log (
            tribunal TEXT NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            extraido_em TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (tribunal, ano, mes)
        );
    """)
    conn.commit()
    return conn


# ── API DataJud ───────────────────────────────────────────────
def datajud_search(alias, query, size=0):
    """Executa busca na API DataJud. Retorna response JSON ou None."""
    url = f"{API_BASE}/{alias}/_search"
    payload = json.dumps(query).encode("utf-8")
    headers = {
        "Authorization": f"APIKey {API_KEY}",
        "Content-Type": "application/json",
    }
    req = Request(url, data=payload, headers=headers, method="POST")

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES:
                wait = DELAY_ON_ERROR * (attempt + 1)
                print(f"      429, aguardando {wait:.0f}s...")
                time.sleep(wait)
                continue
            elif e.code >= 500 and attempt < MAX_RETRIES:
                time.sleep(DELAY_ON_ERROR)
                continue
            else:
                print(f"      ERRO: {e}")
                return None
        except (URLError, TimeoutError) as e:
            if attempt < MAX_RETRIES:
                time.sleep(DELAY_ON_ERROR)
                continue
            print(f"      ERRO: {e}")
            return None


def count_by_movements(alias, start_date, end_date, classe=None):
    """Conta processos com movimentos no período, opcionalmente por classe."""
    must = [
        {"range": {"movimentos.dataHora": {"gte": start_date, "lt": end_date}}}
    ]
    if classe:
        must.append({"match": {"classe.nome": classe}})

    query = {
        "query": {"bool": {"must": must}},
        "size": 0,
        "track_total_hits": True,
    }
    result = datajud_search(alias, query)
    if result:
        return result.get("hits", {}).get("total", {}).get("value", 0)
    return 0


def count_all_classes(alias, start_date, end_date):
    """Conta processos por classe relevante no período."""
    classes = [
        "Precatório",
        "Requisição de Pequeno Valor",
        "Cumprimento de Sentença contra a Fazenda Pública",
        "Execução contra a Fazenda Pública",
        "Cumprimento de Sentença",
    ]
    results = {}
    for cls in classes:
        count = count_by_movements(alias, start_date, end_date, cls)
        if count > 0:
            results[cls] = count
        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Also get total (all classes with movements)
    total = count_by_movements(alias, start_date, end_date)
    results["_total"] = total

    return results


# ── Extração ──────────────────────────────────────────────────
def already_extracted(conn, tribunal, ano, mes):
    cur = conn.execute(
        "SELECT 1 FROM extracao_log WHERE tribunal=? AND ano=? AND mes=?",
        (tribunal, ano, mes)
    )
    return cur.fetchone() is not None


def run_extraction(conn, start_year, start_month, end_year, end_month,
                   tribunais=None, force=False):
    """Extrai contagens mensais por tribunal e classe."""
    if tribunais is None:
        tribunais = list(TRIBUNAIS.keys())

    # Generate month list
    months = []
    y, m = start_year, start_month
    while (y, m) <= (end_year, end_month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1

    total_combos = len(months) * len(tribunais)
    done = 0
    extracted = 0

    print(f"\n{'='*60}")
    print(f"  EXTRAÇÃO HISTÓRICA DataJud")
    print(f"  Período: {start_year}-{start_month:02d} a {end_year}-{end_month:02d} ({len(months)} meses)")
    print(f"  Tribunais: {len(tribunais)}")
    print(f"  Combinações: {total_combos}")
    print(f"{'='*60}\n")

    for y, m in months:
        start_date = f"{y}-{m:02d}-01"
        if m == 12:
            end_date = f"{y+1}-01-01"
        else:
            end_date = f"{y}-{m+1:02d}-01"

        month_total = 0

        for trib in tribunais:
            done += 1
            pct = done / total_combos * 100

            if not force and already_extracted(conn, trib, y, m):
                continue

            alias = TRIBUNAIS[trib]
            counts = count_all_classes(alias, start_date, end_date)

            # Store each class count
            for cls, cnt in counts.items():
                if cls == "_total":
                    continue
                conn.execute("""
                    INSERT OR REPLACE INTO movimentos_mensais
                    (tribunal, ano, mes, classe, total_processos)
                    VALUES (?, ?, ?, ?, ?)
                """, (trib, y, m, cls, cnt))

            # Store total
            total = counts.get("_total", 0)
            conn.execute("""
                INSERT OR REPLACE INTO movimentos_mensais
                (tribunal, ano, mes, classe, total_processos)
                VALUES (?, ?, ?, ?, ?)
            """, (trib, y, m, "_total", total))

            conn.execute("""
                INSERT OR REPLACE INTO extracao_log (tribunal, ano, mes)
                VALUES (?, ?, ?)
            """, (trib, y, m))
            conn.commit()

            prec = counts.get("Precatório", 0)
            month_total += total
            extracted += 1

            print(f"  [{pct:5.1f}%] {y}-{m:02d} {trib:6s}: "
                  f"total={total:>8,}, precatório={prec:>6,}")

            time.sleep(DELAY_BETWEEN_REQUESTS)

        if month_total > 0:
            print(f"  --- {y}-{m:02d} total: {month_total:,} ---\n")

    print(f"\n  Concluído: {extracted} extrações de {total_combos} combinações")


# ── Agregações ────────────────────────────────────────────────
def generate_aggregations(conn, argus_path=None):
    """Gera dados compatíveis com dados_argus.json."""
    cur = conn.cursor()

    # Load Argus for non-temporal sections
    argus = {}
    if argus_path and os.path.exists(argus_path):
        with open(argus_path, encoding="utf-8") as f:
            argus = json.load(f)
        print(f"  Loaded Argus: {len(argus)} keys")

    result = {}
    result["meta"] = {
        "data_extracao": datetime.now().isoformat(),
        "fontes": {
            "mercado": "DataJud/CNJ (tendencia, heatmap, volume - escala de mercado)",
            "comercial": "Argus DB/IA (prospeccao, pipeline, alertas, oportunidades)",
        },
    }

    # Contagens
    cur.execute("SELECT SUM(total_processos) FROM movimentos_mensais WHERE classe = '_total'")
    total_hist = cur.fetchone()[0] or 0
    contagens = argus.get("contagens", [{}])[0].copy() if argus.get("contagens") else {}
    contagens["historico_datajud"] = total_hist
    result["contagens"] = [contagens]

    # ══════════════════════════════════════════════════════════════
    # SEÇÕES DE MERCADO — DataJud (13 meses, escala real de mercado)
    # ══════════════════════════════════════════════════════════════

    # ── Tendência tribunal (mensal) — DataJud puro ──
    # Mostra o TAMANHO DE MERCADO real: movimentos judiciais por tribunal/mês
    cur.execute("""
        SELECT tribunal AS trib, ano AS y, mes AS m, SUM(total_processos) AS vol
        FROM movimentos_mensais
        WHERE classe = '_total'
        GROUP BY tribunal, ano, mes
        ORDER BY tribunal, ano, mes
    """)
    result["tendencia_tribunal"] = [
        {"trib": r[0], "y": r[1], "m": r[2], "vol": r[3], "val": 0}
        for r in cur.fetchall()
    ]

    # ── Heatmap tribunal — DataJud puro ──
    result["heatmap_tribunal"] = [
        {"trib": r["trib"], "y": r["y"], "m": r["m"],
         "vol": r["vol"], "val": 0, "score_medio": 0}
        for r in result["tendencia_tribunal"]
    ]

    # ── Volume tribunal — DataJud puro ──
    cur.execute("""
        SELECT tribunal, SUM(total_processos),
               MIN(ano || '-' || printf('%02d', mes) || '-01'),
               MAX(ano || '-' || printf('%02d', mes) || '-28')
        FROM movimentos_mensais WHERE classe = '_total'
        GROUP BY tribunal ORDER BY SUM(total_processos) DESC
    """)
    result["volume_tribunal"] = [
        {"trib": r[0], "total": r[1], "valor_total": 0, "score_medio": 0,
         "dias": 0, "data_inicio": r[2], "data_fim": r[3]}
        for r in cur.fetchall()
    ]

    # ── Fontes cobertura — DataJud ──
    cur.execute("""
        SELECT tribunal, MIN(ano || '-' || printf('%02d', mes) || '-01') AS inicio,
               MAX(ano || '-' || printf('%02d', mes) || '-28') AS fim,
               SUM(total_processos), COUNT(DISTINCT ano || '-' || mes) AS meses
        FROM movimentos_mensais WHERE classe = '_total'
        GROUP BY tribunal ORDER BY SUM(total_processos) DESC
    """)
    result["fontes_cobertura"] = [
        {"fonte": r[0].lower(), "total": r[3], "dias": r[4] * 20,
         "data_inicio": r[1], "data_fim": r[2]}
        for r in cur.fetchall()
    ]

    # ══════════════════════════════════════════════════════════════
    # SEÇÕES COMERCIAIS — Argus (14 dias, inteligência IA)
    # ══════════════════════════════════════════════════════════════

    # ── Pipeline — SOMENTE Argus (fase_pjus é classificação IA exclusiva) ──
    result["pipeline_mensal"] = argus.get("pipeline_mensal", [])
    result["pipeline_fase"] = argus.get("pipeline_fase", [])

    # ── Volume diário — Argus (granularidade diária só existe aqui) ──
    result["volume_diario_total"] = argus.get("volume_diario_total", [])
    result["volume_diario_fonte"] = argus.get("volume_diario_fonte", [])

    # ── Seções do Argus (ricas em IA) ──
    for key in ["entes_devedores", "top_beneficiarios", "top_advogados",
                "oportunidades", "alertas", "top_precatorios_analise",
                "faixas_valor", "areas_legais", "amapa_precatorio",
                "amapa_oportunidades"]:
        result[key] = argus.get(key, [])

    result["erros"] = []
    return result


# ── Status ────────────────────────────────────────────────────
def show_status(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM extracao_log")
    logs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT tribunal) FROM movimentos_mensais")
    tribs = cur.fetchone()[0]
    cur.execute("SELECT MIN(ano||'-'||printf('%02d',mes)), MAX(ano||'-'||printf('%02d',mes)) FROM movimentos_mensais")
    r = cur.fetchone()
    cur.execute("SELECT SUM(total_processos) FROM movimentos_mensais WHERE classe='_total'")
    total = cur.fetchone()[0] or 0

    print(f"\n{'='*50}")
    print(f"  STATUS DO BANCO HISTÓRICO (DataJud)")
    print(f"{'='*50}")
    print(f"  Extrações: {logs}")
    print(f"  Tribunais: {tribs}")
    print(f"  Período: {r[0]} a {r[1]}")
    print(f"  Total movimentações: {total:,}")

    cur.execute("""
        SELECT tribunal, SUM(total_processos) AS total
        FROM movimentos_mensais WHERE classe = '_total'
        GROUP BY tribunal ORDER BY total DESC LIMIT 15
    """)
    print(f"\n  Top tribunais:")
    for r in cur.fetchall():
        print(f"    {r[0]:6s}: {r[1]:>10,}")

    cur.execute("""
        SELECT ano||'-'||printf('%02d',mes) AS m, SUM(total_processos)
        FROM movimentos_mensais WHERE classe = '_total'
        GROUP BY m ORDER BY m
    """)
    print(f"\n  Distribuição mensal:")
    for r in cur.fetchall():
        print(f"    {r[0]}: {r[1]:>10,}")

    cur.execute("""
        SELECT classe, SUM(total_processos) AS total
        FROM movimentos_mensais WHERE classe <> '_total'
        GROUP BY classe ORDER BY total DESC
    """)
    print(f"\n  Por classe:")
    for r in cur.fetchall():
        print(f"    {r[0]:50s}: {r[1]:>10,}")
    print()


# ── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Extrator Histórico DataJud")
    parser.add_argument("--test", action="store_true", help="Modo teste: 3 tribs, 2 meses")
    parser.add_argument("--months", type=int, default=12, help="Meses retroativos")
    parser.add_argument("--aggregate", action="store_true", help="Gerar JSON para dashboard")
    parser.add_argument("--merge", type=str, help="Path dados_argus.json para merge")
    parser.add_argument("--output", type=str, help="Path saída JSON")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--tribunais", type=str, help="Tribunais (comma-sep)")
    args = parser.parse_args()

    conn = init_db()

    if args.status:
        show_status(conn)
        conn.close()
        return

    if args.aggregate:
        argus_path = args.merge or os.path.join(SCRIPT_DIR, "dados_argus_completo.json")
        output_path = args.output or os.path.join(SCRIPT_DIR, "dados_argus_historico.json")

        print("Gerando agregações DataJud + Argus...")
        result = generate_aggregations(conn, argus_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print(f"Salvo: {output_path} ({os.path.getsize(output_path):,} bytes)")
        conn.close()
        return

    # Determine period
    today = date.today()
    if args.test:
        start_y, start_m = today.year, today.month - 2
        if start_m <= 0:
            start_m += 12
            start_y -= 1
        tribunais = ["TJAP", "TJAC", "TJSP"]
    else:
        months_back = args.months
        start_y = today.year
        start_m = today.month - months_back
        while start_m <= 0:
            start_m += 12
            start_y -= 1
        tribunais = args.tribunais.split(",") if args.tribunais else list(TRIBUNAIS.keys())

    end_y, end_m = today.year, today.month

    run_extraction(conn, start_y, start_m, end_y, end_m, tribunais, force=args.force)
    show_status(conn)
    conn.close()


if __name__ == "__main__":
    main()
