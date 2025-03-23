import discord
import requests
import asyncio
from discord.ext import tasks

# Token & API Key
DISCORD_BOT_TOKEN = "MTM1MzA4ODQ4NDMxNDg0MTIxMA.G2Ynj2.wTWOzahsSbRZ49Xw-vO2cj1zaGpcebzGwakCRo"
LUNO_API_KEY = "mchcsg8dpzvrs"
LUNO_API_SECRET = "YN_DAK8rKe8qcHsi6XhuzDRQjVchJHbX6W7LlBeZP5A"
DISCORD_CHANNEL_ID = 1353382705429217363  # Gantikan dengan ID channel anda
LUNO_API_URL = "https://api.luno.com/api/1/ticker"

# Simpan harga sebelumnya
previous_prices = {}

# Setup bot dengan intents minimum
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

### 🏆 FUNGSI AMBIL HARGA CRYPTO MENGGUNAKAN API KEY LUNO
def get_luno_prices():
    pairs = ["XBTMYR", "ETHMYR", "XRPMYR", "BCHMYR", "LTCMYR"]
    prices = {}

    for pair in pairs:
        try:
            response = requests.get(f"{LUNO_API_URL}?pair={pair}", auth=(LUNO_API_KEY, LUNO_API_SECRET))
            if response.status_code == 200:
                data = response.json()
                prices[pair] = float(data["last_trade"])
            else:
                print(f"Gagal mendapatkan harga {pair}")
        except Exception as e:
            print(f"Ralat API Luno untuk {pair}: {e}")

    return prices

### 🔔 EVENT: BOT SIAP SEDIA
@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} telah berjaya disambungkan!")
    check_prices.start()

### 💰 TASK: KEMASKINI HARGA (BILA BERUBAH SAHAJA)
@tasks.loop(seconds=30)
async def check_prices():
    global previous_prices
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    if not channel:
        print("❌ Tidak dapat akses channel. Sila periksa ID dan permission bot.")
        return

    prices = get_luno_prices()
    if not prices:
        return

    message = "💰 **Harga Crypto Terkini (MYR)** 💰\n"
    updated = False

    for pair, price in prices.items():
        if pair in previous_prices:
            change = price - previous_prices[pair]
            emoji = "📈" if change > 0 else "📉" if change < 0 else "➖"
            message += f"📌 **{pair}**: RM {price:.2f} {emoji}\n"
        else:
            message += f"📌 **{pair}**: RM {price:.2f}\n"
        if pair not in previous_prices or previous_prices[pair] != price:
            updated = True

    previous_prices = prices

    if updated:
        await channel.send(message)

### 🚀 JALANKAN BOT
bot.run(DISCORD_BOT_TOKEN)
