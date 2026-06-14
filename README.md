# Pygame-Zekiro
# ⚔️ Zekiro: Shadows Die Once

**Zekiro: Shadows Die Once**, souls-like türünün ikonik atmosferini ve sinematik dövüş mekaniklerini **soru-cevap tabanlı eğitsel oyun (Educational RPG)** dinamikleriyle birleştiren 2D bir Pygame projesidir. 

Oyuncular kendi isimlerini seçerek zorlu bir kılıç dövüşü arenasındaki yerlerini alırlar. Bilgi en güçlü silahınızdır; doğru cevaplar bossları dize getirirken, yanlış cevaplar efsanevi düşmanların ölümcül özel yeteneklerini tetikler!

---

## 🚀 Öne Çıkan Özellikler

* **Dinamik İsim Giriş Ekranı:** Oyuncuların klavyeden kendi adlarını yazarak oyuna dahil olabilecekleri, Türkçe karakter destekli giriş arayüzü.
* **3 Benzersiz Bölüm ve Boss:** * *Bölüm 1: Kaleye Giriş* -> **Gyoubu Oniwa** (Savaş Baltası Yeteneği)
    * *Bölüm 2: Lordu Kurtarma* -> **Genichiro Ashina** (Yıldırım Katana Yeteneği)
    * *Bölüm 3: Lordu Arındırma* -> **Isshin Ashina** (Mızrak Şarjı - %50 Daha Büyük Heybetli Görünüm)
* **Sinematik Savaş Akışı:** 1. Oyuncu bir şıkka tıklar ve soru paneli anında gizlenir.
    2. Ekran hafifçe buğulanarak tam ortada yeşil **"DOĞRU CEVAP"** veya kırmızı **"YANLIŞ CEVAP"** bandı belirir.
    3. Bildirim bandı kaybolduğunda karakterler birbirine doğru **akıcı, süzülen bir atılma animasyonuyla (Smooth Dash)** fırlar ve ses efektleri eşliğinde dövüşürler.
    4. Karakterler eski savunma pozisyonlarına tam olarak döndükleri an alt tarafta yeni soru belirir.
* **Modüler JSON Altyapısı:** Sorular kaynak kodların içinde değil, tamamen harici bir `sorular.json` dosyasından UTF-8 kodlamasıyla (Türkçe karakter uyumlu) dinamik olarak çekilir.
* **Epik Ses ve Müzik Yönetimi:** Her boss'un kendi savaşına özel arka plan müziği (BGM) ve her aksiyona özel (Vuruş, Zafer, Ölüm) ses efektleri.

---

## 📂 Proje Klasör Yapısı

Projenin sorunsuz çalışabilmesi için dosya ve klasör hiyerarşisinin aşağıdaki gibi yapılandırılması gerekmektedir:

```text
Samuraipygame/
│
├── main.py                 # Oyunu başlatan ve pencereler arası köprüyü kuran ana dosya
├── classes.py              # Oyun mantığı, karakterler, animasyonlar ve dövüş döngüsü
├── menu.py                 # Başlangıç menüsü ve isim giriş ekranı arayüzleri
├── sorular.json            # Soruların, şıkların ve doğru cevap indislerinin tutulduğu veri dosyası
│
├── Images/
│   ├── Arkaplan/
│   │   ├── ZekiroShadowsDieOnce2.png   # Menü arka planı
│   │   ├── Gyoubuarkaplan.png          # 1. Bölüm arka planı
│   │   ├── Genichiroarkaplan.png        # 2. Bölüm arka planı
│   │   └── Isshinarkaplan.png           # 3. Bölüm arka planı
│   └── Karakter/
│       ├── Sekiro_normal.png
│       ├── Sekiro_attack.png
│       └── Sekiro_damage.png
│
└── Audio/
    ├── bgm_boss1.mp3, bgm_boss2.mp3, bgm_boss3.mp3  # Boss müzikleri
    ├── player_attack.wav                            # Oyuncu vuruş sesi
    ├── boss_attack.wav                              # Boss vuruş sesi
    ├── victory.wav                                  # Genel oyun bitiş zafer sesi
    └── defeat.wav                                   # Ölüm ekranı sesi

[BAŞLA: main.py]
              │
              ▼
   [Pygame & Ekran Başlatma]
              │
              ▼
    ┌───────────────────┐
    │  ANA MENÜ EKRANI  │ ◄────────────────────────┐
    └───────────────────┘                          │
              │                                    │
              ▼                                    │
     ( Oyuncu Ne Seçti? )                          │
      /                \                           │
  [OYNA]             [ÇIKIŞ]                       │
    │                    │                         │
    ▼                    ▼                         │
┌───────────────────┐ [Sistemden Çık]              │
│ İSİM GİRİŞ EKRANI │                              │
└───────────────────┘                              │
    │ (Enter tuşu)                                 │
    ▼                                              │
[İsim Alınır & BattleGame Başlatılır]              │
    │                                              │
    ▼                                              │
┌────────────────────────────────────────────────┐ │
│ SAVAŞ DÖNGÜSÜ (BattleGame.run)                 │ │
├────────────────────────────────────────────────┤ │
│                                                │ │
│ 1. JSON'dan soruları yükle ve karıştır.        │ │
│ 2. Siyah ekran: "BÖLÜM X: ..." başlığını bas.  │ │
│ 3. Bölüm arka plan müziğini (BGM) oynat.       │ │
│                                                │ │
│  ┌◄─────────────────────────────────────────┐  │ │
│  │ OYUN DÖNGÜSÜ (60 FPS)                    │  │ │
│  ├──────────────────────────────────────────┤  │ │
│  │  - Ekranı ve Karakterleri Çizdir.        │  │ │
│  │  - Ekranda soru varsa tıklama bekle.     │  │ │
│  │                                          │  │ │
│  │  ( Oyuncu Bir Şıkka Tıkladı mı? )        │  │ │
│  │         /                    \           │  │ │
│  │     [EVET]                  [HAYIR]      │  │ │
│  │       │                        │         │  │ │
│  │       ▼                        └─────────┼──┘
│  │  [Soru Panelini Gizle]                   │
│  │       │                                  │
│  │  ( Cevap Doğru mu? )                     │
│  │     /          \                         │
│  │ [DOĞRU]      [YANLIŞ]                    │
│  │   │              │                       │
│  │   ▼              ▼                       │
│  │[Yeşil Bant]  [Kırmızı Bant]              │
│  │[Oyuncu Atılır][Boss Özel Vurur]          │
│  │   │              │                       │
│  │   └──────┬───────┘                       │
│  │          ▼                               │
│  │   ( Animasyon Bitti mi? )                │
│  │      /              \                    │
│  │  [HAYIR]          [EVET]                 │
│  │    │                │                    │
│  │    └─►(Bekle)       ▼                    │
│  │               ( Oyuncu Canı <= 0? )      │
│  │                  /            \          │
│  │              [EVET]          [HAYIR]     │
│  │                │                │        │
│  │                ▼                ▼        │
│  │          [OYUN BİTTİ]    ( Boss Canı <= 0? )
│  │          [Defeat Sesi]      /          \ │
│  │          [Menüye Dön]   [EVET]       [HAYIR]
│  │                            │             │
│  │                            ▼             ▼
│  │                    [Düşman Yenildi] [Yeni Soru]
│  │                    [Bant & Müziği Kes]   ▲
│  │                            │             │
│  │                    ( Son Boss mu? )      │
│  │                       /        \         │
│  │                   [EVET]      [HAYIR]    │
│  │                     │            │       │
│  │                     ▼            ▼       │
│  │                [ZAFER]     [Sonraki Bölüm]
│  │              [Victory Sesi] [Siyah Ekran]
│  │              [Menüye Dön]        │       │
│  │                                  └───────┘
└────────────────────────────────────────────────┘
