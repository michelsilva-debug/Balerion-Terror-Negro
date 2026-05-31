import requests
import time

# ==========================================
# TELEGRAM
# ==========================================

TOKEN = "8998510153:AAFTW6blkTJn4RgSb-xzH9huAIVFDmnHOwY"
CHAT_ID = "8381462754"

# ==========================================
# API
# ==========================================

API_KEY = "1100741a3689b93a91053f60dd2e7ac5"

SPORTS = [
    # ---- LIGAS ORIGINAIS ----
    "soccer_japan_j_league",
    "soccer_korea_kleague1",
    "soccer_china_superleague",
    "soccer_saudi_arabia_pro_league",
    "soccer_australia_aleague",
    "soccer_epl",
    # ---- NOVAS LIGAS ----
    "soccer_brazil_campeonato",       # Brasileirão Série A
    "soccer_spain_la_liga",           # La Liga
    "soccer_uefa_champs_league",      # Champions League
    "soccer_italy_serie_a",           # Serie A
    "soccer_germany_bundesliga",      # Bundesliga
]

# ==========================================
# CASAS
# ==========================================

CASAS = [
    "Bet365",
    "Betano",
    "Pinnacle",
    "Betfair",
    "Sportingbet"
]

# ==========================================
# ENVIAR TELEGRAM
# ==========================================

def enviar_telegram(msg):

    try:

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg
            },
            timeout=10
        )

    except Exception as erro:

        print("ERRO TELEGRAM:", erro)

# ==========================================
# CALCULAR SUREBET
# ==========================================

def calcular_surebet(odd1, odd2):

    try:

        odd1 = float(odd1)
        odd2 = float(odd2)

        lucro = round(
            (1 - ((1 / odd1) + (1 / odd2))) * 100,
            2
        )

        return lucro

    except:

        return -100

# ==========================================
# VALIDAR ODD
# ==========================================

def odd_valida(valor):

    try:

        valor = float(valor)

        if valor >= 1.01 and valor <= 50:
            return True

        return False

    except:

        return False

# ==========================================
# DUPLA CHANCE
# ==========================================

def calcular_dupla_chance(odd_vitoria, odd_empate):

    try:

        resultado = round(
            1 / (
                (1 / odd_vitoria) +
                (1 / odd_empate)
            ),
            2
        )

        return resultado

    except:

        return None

# ==========================================
# VERIFICAR SUREBET
# ==========================================

def verificar_surebet(lista1, lista2, mercado, jogo):

    try:

        if not lista1 or not lista2:
            return

        melhor1 = max(
            lista1,
            key=lambda x: x["odd"]
        )

        melhor2 = max(
            lista2,
            key=lambda x: x["odd"]
        )

        # ======================================
        # BLOQUEAR MESMA CASA
        # ======================================

        if melhor1["casa"] == melhor2["casa"]:
            return

        lucro = calcular_surebet(
            melhor1["odd"],
            melhor2["odd"]
        )

        # ======================================
        # FILTRAR FALSAS
        # ======================================

        if lucro <= 1:
            return

        if lucro >= 35:
            return

        mensagem = f"""
🚨 SUREBET ENCONTRADA

⚽ {jogo['home_team']} vs {jogo['away_team']}

🎯 Mercado:
{mercado}

✅ Aposta 1:
{melhor1['aposta']}
📈 {melhor1['casa']} → odd {melhor1['odd']}

✅ Aposta 2:
{melhor2['aposta']}
📈 {melhor2['casa']} → odd {melhor2['odd']}

💰 Lucro estimado: {lucro}%

🔥 Arbitragem REAL detectada
"""

        print(mensagem)

        enviar_telegram(mensagem)

    except Exception as erro:

        print("ERRO SUREBET:", erro)

# ==========================================
# INICIAR
# ==========================================

print("🚀 TERRORNEGRO SUREBET ELITE ONLINE!")
print(f"📋 Monitorando {len(SPORTS)} ligas...")

# ==========================================
# LOOP PRINCIPAL INFINITO
# ==========================================

while True:

    for SPORT in SPORTS:

        url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

        response = requests.get(
            url,
            params={
                "apiKey": API_KEY,
                "regions": "eu",
                "markets": "h2h,totals",
                "oddsFormat": "decimal"
            },
            timeout=15
        )

        print("Consultando:", SPORT)
        print("Status:", response.status_code)

        if response.status_code != 200:
            print("ERRO API:", response.status_code)
            continue

        dados = response.json()

        if not isinstance(dados, list):
            print("JSON INVÁLIDO")
            continue

        for jogo in dados:

            try:

                if not isinstance(jogo, dict):
                    continue

                home_team = jogo.get("home_team")
                away_team = jogo.get("away_team")

                if not home_team or not away_team:
                    continue

                bookmakers = jogo.get("bookmakers", [])

                if not isinstance(bookmakers, list):
                    continue

                # ======================================
                # LISTAS
                # ======================================

                vitoria_a = []
                dupla_b = []

                vitoria_b = []
                dupla_a = []

                over15 = []
                under15 = []

                over25 = []
                under25 = []

                over35 = []
                under35 = []

                # ======================================
                # BOOKMAKERS
                # ======================================

                for casa in bookmakers:

                    try:

                        if not isinstance(casa, dict):
                            continue

                        nome_casa = casa.get("title")

                        if nome_casa not in CASAS:
                            continue

                        markets = casa.get("markets", [])

                        if not isinstance(markets, list):
                            continue

                        # ======================================
                        # MERCADOS
                        # ======================================

                        for market in markets:

                            try:

                                if not isinstance(market, dict):
                                    continue

                                market_key = market.get("key")

                                outcomes = market.get("outcomes", [])

                                if not isinstance(outcomes, list):
                                    continue

                                # ======================================
                                # RESULTADO / DUPLA CHANCE
                                # ======================================

                                if market_key == "h2h":

                                    empate_item = None
                                    times = []

                                    for o in outcomes:

                                        if not isinstance(o, dict):
                                            continue

                                        nome = str(
                                            o.get("name", "")
                                        ).lower()

                                        if nome in [
                                            "draw",
                                            "empate"
                                        ]:

                                            empate_item = o

                                        else:

                                            times.append(o)

                                    if (
                                        len(times) != 2
                                        or empate_item is None
                                    ):
                                        continue

                                    time_a = times[0]["name"]
                                    time_b = times[1]["name"]

                                    odd_a = times[0]["price"]
                                    odd_b = times[1]["price"]

                                    odd_empate = empate_item["price"]

                                    if not (
                                        odd_valida(odd_a)
                                        and odd_valida(odd_b)
                                        and odd_valida(odd_empate)
                                    ):
                                        continue

                                    vitoria_a.append({
                                        "casa": nome_casa,
                                        "aposta": f"Vitória {time_a}",
                                        "odd": odd_a
                                    })

                                    vitoria_b.append({
                                        "casa": nome_casa,
                                        "aposta": f"Vitória {time_b}",
                                        "odd": odd_b
                                    })

                                    odd_dc_a = calcular_dupla_chance(
                                        odd_a,
                                        odd_empate
                                    )

                                    odd_dc_b = calcular_dupla_chance(
                                        odd_b,
                                        odd_empate
                                    )

                                    if odd_dc_a:

                                        dupla_a.append({
                                            "casa": nome_casa,
                                            "aposta": f"{time_a} ou empate",
                                            "odd": odd_dc_a
                                        })

                                    if odd_dc_b:

                                        dupla_b.append({
                                            "casa": nome_casa,
                                            "aposta": f"{time_b} ou empate",
                                            "odd": odd_dc_b
                                        })

                                # ======================================
                                # OVER / UNDER
                                # ======================================

                                elif market_key == "totals":

                                    for item in outcomes:

                                        try:

                                            if not isinstance(item, dict):
                                                continue

                                            nome = item.get("name")
                                            odd = item.get("price")
                                            ponto = item.get("point")

                                            if not odd_valida(odd):
                                                continue

                                            if ponto == 1.5:

                                                if nome == "Over":
                                                    over15.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Mais de 1.5 gols",
                                                        "odd": odd
                                                    })
                                                elif nome == "Under":
                                                    under15.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Menos de 1.5 gols",
                                                        "odd": odd
                                                    })

                                            elif ponto == 2.5:

                                                if nome == "Over":
                                                    over25.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Mais de 2.5 gols",
                                                        "odd": odd
                                                    })
                                                elif nome == "Under":
                                                    under25.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Menos de 2.5 gols",
                                                        "odd": odd
                                                    })

                                            elif ponto == 3.5:

                                                if nome == "Over":
                                                    over35.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Mais de 3.5 gols",
                                                        "odd": odd
                                                    })
                                                elif nome == "Under":
                                                    under35.append({
                                                        "casa": nome_casa,
                                                        "aposta": "Menos de 3.5 gols",
                                                        "odd": odd
                                                    })

                                        except:
                                            continue

                            except:
                                continue

                    except:
                        continue

                # ======================================
                # VERIFICAR SUREBETS
                # ======================================

                verificar_surebet(
                    vitoria_a,
                    dupla_b,
                    "Vitória Time A vs Time B ou empate",
                    jogo
                )

                verificar_surebet(
                    vitoria_b,
                    dupla_a,
                    "Vitória Time B vs Time A ou empate",
                    jogo
                )

                verificar_surebet(
                    over15,
                    under15,
                    "Over 1.5 vs Under 1.5",
                    jogo
                )

                verificar_surebet(
                    over25,
                    under25,
                    "Over 2.5 vs Under 2.5",
                    jogo
                )

                verificar_surebet(
                    over35,
                    under35,
                    "Over 3.5 vs Under 3.5",
                    jogo
                )

            except Exception as erro_jogo:

                print("ERRO JOGO:", erro_jogo)

    # ======================================
    # AGUARDAR 60 SEGUNDOS E REPETIR
    # ======================================

    print("⏳ Aguardando 10 minutos para próxima varredura...")
    time.sleep(600)
