# Discord Proxy Bot (Render.com Uyumlu)

Bu bot, `proxy.txt` dosyasından rastgele proxy seçerek kullanıcılara DM yoluyla gönderir.

## Özellikler
- `/proxy [adet]` komutu ile çalışır.
- Maksimum 30 adet proxy sınırı vardır.
- Proxyler `proxy.txt` dosyasından rastgele seçilir.
- Sonuçlar kullanıcıya DM olarak gönderilir.
- Render.com'da çalışması için `keep_alive` (Flask) sistemi entegre edilmiştir.

## Kurulum (Render.com)
1. Bu dosyaları bir GitHub deposuna yükleyin.
2. Render.com'da yeni bir **Web Service** oluşturun.
3. GitHub deponuzu bağlayın.
4. **Environment Variables** kısmına şunları ekleyin:
   - `DISCORD_TOKEN`: Discord Bot Token'ınız.
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python bot.py`

## Dosyalar
- `bot.py`: Ana bot kodu.
- `proxy.txt`: Proxy listesinin bulunduğu dosya (Her satıra bir proxy).
- `requirements.txt`: Gerekli kütüphaneler.
- `Procfile`: Render/Heroku için başlatma dosyası.
- `.env`: Yerel testler için token (GitHub'a yüklemeyin).
