import discord
from discord.ext import commands
from bot_token import token
import time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}, bir Discord sohbet botuyum!')

@bot.command()
async def hesapla(ctx):
    await ctx.send(f'Aylık Kaç kWH Eneri Kullanıyorsunuz?')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

    try:
        msg = await bot.wait_for("message", check=check, timeout=300.0)

        kwh = int(msg.content)

        elektrik = kwh * 0.4

        if kwh > 350:
            await ctx.send(f"Çok Fazla Elektrik Tüketiyorsunuz! ⚠️ Evinizde Aylık Olarak: {elektrik} kg CO₂e salınımı yapıyorsunuz!")

        elif kwh == 350:
            await ctx.send(f"Ortalama bir değer! ⚡ Evinizde Aylık Olarak: {elektrik} kg CO₂e salınımı yapıyorsunuz!")

        elif kwh < 350:
            await ctx.send(f"Elektriği sizin kadar tasarruflu kullanabilen bir insan daha tanımıyorum! 🌱 Evinizde Aylık Olarak: {elektrik} kg CO₂e salınımı yapıyorsunuz!")

        time.sleep(2)

        await ctx.send(f"Ayda Kaç m³ Doğalgaz Kullanıyorsunuz?")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        dgk = int(msg.content)
        dge = dgk * 1.9

        if dgk > 115:
            await ctx.send(f"Çok fazla Doğalgaz Kullanyorsunuz! Kombiyi biraz kısın! ⚠️ Aylık Olarak {dge} kg CO₂e Salınımı Yapıyorsunuz!")
        elif dgk == 115:
            await ctx.send(f"Ortalama Bir Değer! ⚡ Aylık Olarak {dge} kg CO₂e Salınımı Yapıyorsunuz!")
        elif dgk < 115:
            await ctx.send(f"Sanırım Çok Sıcak Bir Yerde Yaşıyorsunuz! 🌱 Aylık Olarak {dge} kg CO₂e Salınımı Yapıyorsunuz!")

        time.sleep(2)

        await ctx.send(" Hangi tür araç kullanıyorsunuz? (Benzinli / Dizel / LPG / Hibrit / Elektrikli)")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        tur = msg.content.lower()  # Küçük harfe çevirerek işlemi kolaylaştırıyoruz

        # Emisyon faktörleri (kg CO2 / km)
        emisyon_faktörleri = {
            "elektrikli": 0.05,
            "benzinli": 0.20,
            "dizel": 0.17,
            "hibrit": 0.10,
            "lpg": 0.13
        }

        if tur not in emisyon_faktörleri:
            await ctx.send("⚠️ Geçersiz yakıt türü girdiniz. Lütfen 'Benzinli, Dizel, LPG, Hibrit, Elektrikli' seçeneklerinden birini yazın.")
            return

        # KAÇ KM GİDİLDİĞİNİ SOR
        await ctx.send(f"Aracınızla Aylık kaç km yol gidiyorsunuz?")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        yol = int(msg.content)

        # Emisyon hesapla
        arace = emisyon_faktörleri[tur]
        karac = arace * yol

        #  Yol kullanım analiz
        if yol > 170:
            await ctx.send(f"Senin {tur} fiyatlarından haberin var mı? Hem doğaya hem cebine zarar! ⚠️ Aracınızla Aylık Olarak {karac} kg CO₂e salınımı yapıyorsunuz.")
        elif yol == 170:
            await ctx.send(f"Ortalama bir yolculuk yapıyorsunuz. ⚡ Aracınızla Aylık Olarak {karac} kg CO₂e salınımı yapıyorsunuz.")
        elif yol < 170:
            await ctx.send(f"Tebrikler! Çevre dostu bir kullanım gösteriyorsunuz. 🌱 Aracınızla Aylık Olarak {karac} kg CO₂e salınımı yapıyorsunuz.")

        time.sleep(2)

        await ctx.send(f"Ayda Kaç gram Kırmızı Et Tüketiyorsunuz? (Bu dönemde biraz zor ama...)")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        kkg = int(msg.content) * 0.4
        if kkg > 200:
            await ctx.send(f"Kırmızı Et tüketiminizi azaltırsanız iyi olacak!")
        time.sleep(1)

        await ctx.send(f"Ayda Kaç gram Beyaz Et Tüketiyorsunuz?")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        bkg = int(msg.content) * 0.06
        if bkg > 100:
            await ctx.send(f"Beyaz Et tüketiminizi azaltırsanız iyi olacak!")
        time.sleep(1)

        await ctx.send(f"Ayda Kaç kg Süt Tüketiyorsunuz")
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300.0)
        skg = int(msg.content) * 3.2
        if skg > 5.5:
            await ctx.send(f"Süt tüketiminizi biraz azaltırsanız iyi olacak!")

        time.sleep(1)
        
        TB = kkg + bkg + skg

        await ctx.send(f"Yediğiniz hayvansal ürünlerden Aylık Olarak {TB} kg CO₂e Salınımı Yapıyorsunuz.")

        time.sleep(1)

        await ctx.send(f"Tüm Veriler İşleniyor...")

        time.sleep(1)

        await ctx.send(f"İşlenmeye Devam Ediyor...")

        time.sleep(3)
        kayakizi = kwh + karac + TB + dge
        agac = kayakizi / 22

        await ctx.send(f"""# Gelsin Sonuçlar!
Elektrik Tüketiminizle {kwh} kg CO₂e Salınımı Yapılıyor
Doğalgaz Tüketiminizle {dge} kg CO₂e Salınımı Yapılıyor
Kullandığınız Araçla {karac} kg CO₂e Salınımı Yapılıyor
Tükettiğiniz Besinlerle {TB} kg CO₂e Salınımı Yapılıyor
        
**Karbon Ayak İziniz:** {kayakizi} kg CO₂e
        
Her Ay **{round(agac)}** Tane Ağaç Dikerek Doğaya Olan Borcunuzu Kapatabilirsiniz.

Eğer Karbon Ayak İzinizi Nasıl Azaltabileceğiniz Hakkında Bilgi Edinmek İstiyorsanız /neleryapabilirim yazın""")

    except TimeoutError:
        await ctx.send("Yanıt vermediğiniz için işlem iptal edildi. ❌")


@bot.command()
async def neleryapabilirim(ctx):
    await ctx.send(f"""# 1️⃣ Beslenme Alışkanlıklarınızı Değiştirin 🌿
🔹 **Kırmızı eti azaltın:** Sığır eti üretimi çok yüksek karbon salınımına neden olur. Haftada 1 kez kırmızı et tüketmek, karbon ayak izinizi **%30** azaltabilir.
🔹 **Beyaz et ve bitkisel proteinleri artırın:** Tavuk, balık ve baklagiller (mercimek, nohut) daha düşük karbon salınımına sahiptir.
🔹 **Süt ve süt ürünlerini azaltın:** Süt üretimi metan gazı yayar. Alternatif olarak badem, soya veya yulaf sütü tüketebilirsiniz.
🔹 **Yerel ve mevsimsel ürünler tüketin:** Uzak mesafeden gelen gıdalar yüksek taşıma emisyonu oluşturur.

📌 Kazanım: Gıda seçimlerinizi değiştirerek yılda 500-1000 kg CO₂e tasarruf edebilirsiniz.

# 2️⃣ Elektrik Tüketiminizi Azaltın ⚡
🔹 **LED ampuller kullanın:** %80 daha az enerji harcarlar.
🔹 **Enerji tasarruflu cihazlar (A+++) tercih edin.**
🔹 **Cihazları bekleme modunda bırakmayın, prizden çekin.**
🔹 **Doğal ışık ve güneş enerjisinden yararlanın.**
🔹 **Gereksiz klima ve elektrikli ısıtıcı kullanımını azaltın.**

📌 **Kazanım:** A+++ cihazlar ve LED ampuller kullanarak yılda **300-500 kg CO₂e** tasarruf edebilirsiniz.

# 3️⃣ Isınma ve Doğalgaz Kullanımını Azaltın 🔥
🔹 **Oda sıcaklığını 1°C düşürün:** %6 doğalgaz tasarrufu sağlar.
🔹 **Ev yalıtımını güçlendirin:** Çift cam, izolasyon ve kapı fitilleri ile ısı kaybını önleyin.
🔹 **Kombiyi sürekli açıp kapamak yerine düşük sıcaklıkta çalıştırın.**
🔹 **Sıcak su kullanımını azaltın:** Kısa duşlar alın ve düşük sıcaklıkta çamaşır yıkayın.

📌 **Kazanım:** 1°C daha düşük ısınarak yılda **250-400 kg CO₂e** tasarruf edebilirsiniz.""")

    await ctx.send(f"""# 4️⃣ Ulaşım Seçimlerinizi Değiştirin 🚲
🔹 Bireysel araç kullanımını azaltın:
**-**Toplu taşıma, bisiklet veya yürüyüşü tercih edin.
**-**Araç paylaşımı yaparak karbon salınımını yarıya indirebilirsiniz.
🔹 **Elektrikli veya hibrit araç kullanın:**
**-**Elektrikli araçlar, benzinli araçlara göre 3-4 kat daha az karbon salınımı yapar.
🔹 **Uçuşları azaltın:**
**-**1 saatlik uçak yolculuğu = **90-100 kg CO₂e**
**-**Gerekirse tren veya otobüs alternatiflerini değerlendirin.

📌 **Kazanım:** Aylık 500 km özel araç kullanımını toplu taşımaya çevirerek yılda 1000 kg CO₂e tasarruf edebilirsiniz.

# 5️⃣ Daha Az Atık Üretin ve Geri Dönüşüm Yapın ♻️
🔹 **Tek kullanımlık plastikleri hayatınızdan çıkarın.**
🔹 **Kendi çantanızı, mataranızı ve saklama kaplarınızı kullanın.**
🔹 **Kağıt, cam, plastik ve elektronik atıkları geri dönüştürün.**
🔹 **Kompost yaparak organik atıkları değerlendirin.**

📌 **Kazanım:** Geri dönüşüm ve plastik kullanımını azaltarak yılda 500-700 kg CO₂e tasarruf edebilirsiniz.

# 6️⃣ Su Kullanımınızı Azaltın 🚰
🔹 **Sızdıran muslukları tamir edin:** 1 damla/saniye kaçak = yılda **5500 litre su kaybı**
🔹 **Kısa duş alın ve düşük akımlı duş başlığı kullanın.**
🔹 **Bulaşık ve çamaşır makinelerini tam kapasite çalıştırın.**

📌 **Kazanım:** Su tasarrufu yaparak yılda 100-200 kg CO₂e tasarruf edebilirsiniz.

# 🔢 SONUÇ: NE KADAR TASARRUF EDEBİLİRSİNİZ?

**Daha az kırmızı et tüketmek**	= 500 - 1000 kg CO₂e
**Enerji tasarruflu cihazlar kullanmak** = 300 - 500 kg CO₂e
**1°C daha düşük ısınmak** = 250 - 400 kg CO₂e
**Toplu taşıma ve bisiklet kullanmak** = 1000 - 1500 kg CO₂e
**Geri dönüşüm yapmak** = 500 - 700 kg CO₂e
**Su tüketimini azaltmak** = 100 - 200 kg CO₂e

🌍 Tüm bu adımları uygularsanız, yıllık karbon ayak izinizi **2-4 TON CO₂e** azaltabilirsiniz!

✅ Küçük değişiklikler bile büyük fark yaratır. Haydi, sürdürülebilir bir geleceğe adım atalım! ♻️🌱""")



bot.run(token)