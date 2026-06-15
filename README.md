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

                               ┌────────────────────────┐
                               │     [MİMARİ BAŞLA]     │
                               │        main.py         │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │  pygame.mixer.init()   │
                               │  Ses Motoru Tetiklenir │
                               └───────────┬────────────┘
                                           │
                                           ▼
 ┌─────────────────────────────────────────┴─────────────────────────────────────────┐
 │                                   SAHNE YÖNETİMİ                                  │
 ├───────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                   │
 │  ┌────────────────────────┐       [OYNA]       ┌────────────────────────┐         │
 │  │    STAGE 1: MENU       ├───────────────────►│ STAGE 2: NAME INPUT    │         │
 │  │   (MainMenu Sınıfı)    │                    │ (NameInputScreen S.)   │         │
 │  └──────────┬─────────────┘                    └───────────┬────────────┘         │
 │             │                                              │ (Enter / Valid)      │
 │             │ [ÇIKIŞ]                                      ▼                      │
 │             ▼                                  ┌────────────────────────┐         │
 │     [sys.exit()]                               │ STAGE 3: DIFFICULTY    │         │
 │   Programı Sonlandır                           │ (DiffSelectionScreen)  │         │
 │                                                └───────────┬────────────┘         │
 │                                                            │                      │
 │                                                            │ "NORMAL" /           │
 │                                                            │ "ZORLAYICI"          │
 │                                                            ▼                      │
 │                                                ┌────────────────────────┐         │
 │                                                │  STAGE 4: BATTLE GAME  │         │
 │                                                │  (BattleGame Nesnesi)  │         │
 │                                                └───────────┬────────────┘         │
 └────────────────────────────────────────────────────────────┼──────────────────────┘
                                                              │
                                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│ BATTLE GAME ÇEKİRDEK DÖNGÜSÜ (BattleGame.run)                                      │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  [1] VERİ BAĞLAMI: json_soru_yukle("sorular.json") -> Soru listesi yüklenir/karışır│
│  [2] SİNEMATİK: bolum_ekrani_goster() -> Siyah perde çekilir (2.5 saniye)         │
│  [3] AUDIO: level_musics[current_bg] -> İlgili boss arka plan müziği başlar        │
│                                                                                    │
│       ┌◄────────────────────────────────────────────────────────────────────────┐  │
│       │ ANA DÖNGÜ (clock.tick(60))                                              │  │
│       ├─────────────────────────────────────────────────────────────────────────┤  │
│       │  A. Ekrana Çizim (draw):                                                │  │
│       │     - current_bg.draw() (Arka plan render edilir)                       │  │
│       │     - oyuncu_view & current_boss_view render edilir                     │  │
│       │     - draw_health_bars() (Can barları güncellenir)                      │  │
│       │     - if mevcut_soru ve not odul_ekrani_aktif: Soru & 4 Buton basılır   │  │
│       │     - if odul_ekrani_aktif: Ödül Kartları (Şifa/Öfke) render edilir    │  │
│       │                                                                         │  │
│       │  B. Olay Yakalama (handle_events) & Karar Mekanizması:                  │  │
│       │                                                                         │  │
│       │     [DURUM I: ÖDÜL EKRANI AKTİF]                                        │  │
│       │     ( Fare Tıklaması? )                                                 │  │
│       │       ├──► [Şifa Kartı] ──► Can %25 İyileşir ──► odul_ekrani_aktif=False│  │
│       │       └──► [Öfke Kartı] ──► GÜÇ * 1.5 Hasar  ──► odul_ekrani_aktif=False│  │
│       │                                                                         │  │
│       │     [DURUM II: NORMAL OYUN AKIŞI]                                       │  │
│       │     ( Fare Tıklaması? )                                                 │  │
│       │       └──► Tıklanan Buton İndeksi Kontrol Edilir                        │  │
│       │               │                                                         │  │
│       │               ▼                                                         │  │
│       │       ( Tıklama == dogru_cevap_index? )                                 │  │
│       │          /                         \                                    │  │
│       │      [DOĞRU]                    [YANLIŞ]                                │  │
│       │         │                          │                                    │  │
│       │         ▼                          ▼                                    │  │
│       │   dogru_serisi += 1          dogru_serisi = 0                           │  │
│       │   "DOĞRU CEVAP" Bandı        "YANLIŞ CEVAP" Bandı                       │  │
│       │   oyuncu.celik_firtina()     boss.ozel_yetenek()                        │  │
│       │   Player Dash (+200px)       Boss Dash (-200px)                         │  │
│       │   snd_player_attack.play()   snd_boss_attack.play()                     │  │
│       │         │                          │                                    │  │
│       │         └────────────┬─────────────┘                                    │  │
│       │                      ▼                                                  │  │
│       │             soru_bekleniyor = True                                      │  │
│       │             mevcut_soru = None                                          │  │
│       │                                                                         │  │
│       │  C. Durum Güncelleme (update):                                          │  │
│       │     - CharView.update_animation() -> Karakterlerin X konumları          │  │
│       │       kare başına (dash_speed) kadar target_x'e yaklaştırılır.         │  │
│       │     - Animasyon bittiğinde ve karakterler base_x'e döndüğünde:          │  │
│       │          │                                                              │  │
│       │          ▼                                                              │  │
│       │       ( if dogru_serisi == 3? ) ──► odul_ekrani_aktif = True            │  │
│       │          │                                                              │  │
│       │          ▼                                                              │  │
│       │       ( if oyuncu.can <= 0? )   ──► [YENİLGİ] ──► Defeat Sesi ──► MENU  │  │
│       │          │                                                              │  │
│       │          ▼                                                              │  │
│       │       ( if boss.can <= 0? )                                             │  │
│       │          ├──► [EVET] ──► boss_yenildi_ekrani()                          │  │
│       │          │                  │                                           │  │
│       │          │                  ▼                                           │  │
│       │          │               ( if Son Seviye/Isshin? )                      │  │
│       │          │                  ├──► [EVET] ──► [ZAFER] ──► Victory ──►MENU │  │
│       │          │                  └──► [HAYIR]──► Seviye Atla (current_bg++)  │  │
│       │          │                                  - Zorluk Modu == "NORMAL"   │  │
│       │          │                                    ise oyuncu canı fulle.    │  │
│       │          │                                  - bolum_ekrani_goster()     │  │
│       │          │                                  - soru_bekleniyor = False   │  │
│       │          │                                                              │  │
│       │          └──► [HAYIR] ──► if not odul_ekrani_aktif:                      │  │
│       │                           yeni_soru_sec()                               │  │
│       │                           soru_bekleniyor = False                       │  │
│       │                                                                         │  │
│       └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
