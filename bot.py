import discord
from discord import app_commands
import random
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# .env dosyasını yükle
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Render.com'un dinamik portunu al
PORT = int(os.environ.get('PORT', 8080))

# Web sunucusu yapılandırması
app = Flask('')

@app.route('/')
def home():
    # Site açıldığında görünecek mesaj
    return """
    <html>
        <head>
            <title>Proxy Bot Durumu</title>
            <style>
                body { background-color: #2c2f33; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .status-card { background-color: #23272a; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; }
                .active { color: #43b581; font-weight: bold; font-size: 2rem; }
            </style>
        </head>
        <body>
            <div class="status-card">
                <h1>Proxy Bot</h1>
                <p class="active">Bot Aktif!</p>
                <p>Ping servisleri için sistem çalışıyor.</p>
            </div>
        </body>
    </html>
    """

def run():
    app.run(host='0.0.0.0', port=PORT)

def keep_alive():
    t = Thread(target=run)
    t.start()

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Komutlar senkronize edildi.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user} (ID: {bot.user.id})')
    print(f'Web sunucusu {PORT} portunda aktif.')
    print('------')

@bot.tree.command(name="proxy", description="Belirtilen adette rastgele proxy gönderir.")
@app_commands.describe(adet="Almak istediğiniz proxy adeti (Maksimum 30)")
async def proxy(interaction: discord.Interaction, adet: int):
    if adet > 30:
        await interaction.response.send_message("Maksimum 30 adet proxy alabilirsiniz!", ephemeral=True)
        return
    
    if adet <= 0:
        await interaction.response.send_message("Lütfen geçerli bir sayı girin!", ephemeral=True)
        return

    try:
        if not os.path.exists('proxy.txt'):
            await interaction.response.send_message("Sistemde proxy dosyası bulunamadı.", ephemeral=True)
            return

        with open('proxy.txt', 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]

        if not proxies:
            await interaction.response.send_message("Proxy listesi boş.", ephemeral=True)
            return

        count = min(adet, len(proxies))
        selected_proxies = random.sample(proxies, count)
        
        proxy_text = "\n".join(selected_proxies)
        
        try:
            await interaction.user.send(f"İşte istediğin {count} adet proxy:\n```\n{proxy_text}\n```")
            await interaction.response.send_message("Proxyler DM kutuna gönderildi!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Sana DM gönderemiyorum. Lütfen DM ayarlarını kontrol et.", ephemeral=True)

    except Exception as e:
        print(f"Hata: {e}")
        await interaction.response.send_message("Bir hata oluştu.", ephemeral=True)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
