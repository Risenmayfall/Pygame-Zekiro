import sys
import pygame
import json
from dataclasses import dataclass
import random
from PIL import Image, ImageSequence

@dataclass
class Soru:
    soru_metni: str
    secenekler: list[str]
    dogru_cevap_index: int

# Genel class
class Chars:
    def __init__(self, isim: str, can: int, guc: int, kalkan: int):
        self.isim = isim
        self.can = can
        self.guc = guc
        self.kalkan = kalkan

    def hayatta_mi(self) -> bool:
        return self.can > 0
    
    def _hasar_hesapla(self, ham_hasar: float) -> int:
        net = int(max(0, ham_hasar - self.kalkan))
        return net

    def saldir(self, dusman: "Chars") -> int:
        net_hasar = self._hasar_hesapla(self.guc) #ham_hasar = self.guc
        dusman.can -= net_hasar
        dusman.can = max(0,dusman.can)
        return net_hasar

# Ana karakter 
class Samurai(Chars):
    def celik_firtina(self, dusman: Chars) -> int:
        ham = self.guc * 1.5
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net

# Bosses
class Gyoubu(Chars):
    def savas_baltasi(self, dusman: Chars) -> int:
        ham = self.guc * 1.10
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
class Genichiro(Chars):
    def yildirim_katana(self, dusman: Chars) -> int:
        ham = self.guc * 1.25
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
class Isshin(Chars):
    def mizrak_sarj(self, dusman: Chars) -> int:
        ham = self.guc * 1.5
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
# -------------------------------------------------------------

@dataclass
class CharView:
    """
    Bir karakterin ekrandaki temsili:
    States: Normal, Attack, Damage
    pos: ekrandaki merkez konum
    """
    def __init__(self, karakter: Chars, img_normal_path: str, img_attack_path: str, img_damage_path: str, pos: pygame.Vector2):
        self.karakter = karakter
        self.pos = pos
        self.base_x = pos.x # Orijinal konum (geri döneceği yer)
        self.target_x = pos.x # Anlık gitmek istediği yer
        self.alive = True

        try:
            self.images = {
                "normal": pygame.image.load(img_normal_path).convert_alpha(),
                "attack": pygame.image.load(img_attack_path).convert_alpha(),
                "damage": pygame.image.load(img_damage_path).convert_alpha()
            }
        except pygame.error as e:
            print(f"{karakter.isim} görselleri yüklenirken hata oluştu!")
            print("Hata detay: ", e)
            pygame.quit()
            sys.exit()

        # Aktif durum ve zamanlayıcılar
        self.current_state = "normal"
        self.state_timer = 0 # Özel durumların ekranda kalma süresi
        self.dash_speed = 10 # Karakterlerin kayma hızı
    
    @property
    def image(self) -> pygame.Surface:
        """O anki duruma göre doğru görseli döndürür."""
        return self.images[self.current_state]
    
    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    
    def trigger_state(self, new_state: str, duration: int = 500, dash_offset: int = 0):
        """Karakterin durumunu değiştirir (Örnek attack yapar ve 500ms sonra normale döndürür)
            Ayrıca gitmesi istenilen konumu belirler
        """
        self.current_state = new_state
        self.state_timer = pygame.time.get_ticks() + duration

        # Eğer karakter saldırı durumuna geçtiyse x konumunu ileri kaydır
        if new_state == "attack":
            self.pos.x = self.base_x + dash_offset
        else:
            self.target_x = self.base_x

    def update_animation(self):
        """Saldırı veya hasar görselinin süresi bittiyse otomatik normale döndürür"""
        if self.current_state != "normal":
            if pygame.time.get_ticks() > self.state_timer:
                self.current_state = "normal"
                self.pos.x = self.base_x  # Karakteri orijinal pozisyonuna geri getirir.
        
        if self.pos.x < self.target_x:
            # Sağa doğru kayma
            self.pos.x = min(self.target_x, self.pos.x + self.dash_speed)
        elif self.pos.x > self.target_x:
            # Sola doğru kayma
            self.pos.x = max(self.target_x, self.pos.x - self.dash_speed)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, highlight: bool = False, scale: float = 1.0):
        if not self.alive or self.karakter.can <= 0:
            self.alive = False
            return
        
        # Zamanlayıcıyı kontrol et ve durumu güncelle
        self.update_animation()

        img = self.image
        if abs(scale - 1.0) > 1e-3:
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
        
        draw_rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(img, draw_rect)

        if highlight:
            pygame.draw.rect(screen, (255,215,0), draw_rect.inflate(6,6), 3)
    
    def hit_test(self, mouse_pos) -> bool:
        if not self.alive:
            return False
        return self.rect.collidepoint(mouse_pos)

# Gyoubu Background
class Background1:
    def __init__(self, screen_width, screen_height):
        try:
            self.image = pygame.image.load("Images/Arkaplan/Gyoubuarkaplan.png").convert()
            self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        except pygame.error as e:
            print("Görseller yüklenirken hata oluştu! Lütfen dosyaları kontrol ediniz.")
            print("Hata detayı: ", e)
            pygame.quit()
            sys.exit()

        self.text_title = "Bölüm 1: Kaleye Giriş"
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))

# Genichiro Background
class Background2:
    def __init__(self, screen_width, screen_height):
        try:
            self.image = pygame.image.load("Images/Arkaplan/Genichiroarkaplan.png").convert()
            self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        except pygame.error as e:
            print("Görseller yüklenirken hata oluştu! Lütfen dosyaları kontrol ediniz.")
            print("Hata detayı: ", e)
            pygame.quit()
            sys.exit()

        self.text_title = "Bölüm 2: Lordu Kurtarma"
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))

# Isshin Background
class Background3:
    def __init__(self, screen_width, screen_height):
        try:
            self.image = pygame.image.load("Images/Arkaplan/Isshinarkaplan.png").convert()
            self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        except pygame.error as e:
            print("Görseller yüklenirken hata oluştu! Lütfen dosyaları kontrol ediniz.")
            print("Hata detayı: ", e)
            pygame.quit()
            sys.exit()

        self.text_title = "Bölüm 3: Lordu Arındırma"
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))

class BattleGame:
    def __init__(self, screen, oyuncu_adi: str = "Samurai", zorluk_modu: str = "NORMAL"):
        # Pygame start
        pygame.init()
        pygame.mixer.init()

        # Pencere boyutu ayarları
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 750
        self.screen = screen
        self.zorluk_modu = zorluk_modu
        pygame.display.set_caption("Zekiro: Shadows Die Once")

        # Zamanlayıcı ve font
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ATC Laurel Black", 50, bold = True)
        self.hp_font = pygame.font.SysFont("Arial", 23, bold = True)
        self.soru_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.title_card_font = pygame.font.SysFont("Times New Roman", 72, bold=True)
        self.victory_font = pygame.font.SysFont("Georgia", 90, bold = True)

        # Arka plan tanımlama
        self.bg_level1 = Background1(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bg_level2 = Background2(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bg_level3 = Background3(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.current_bg = self.bg_level1

        # Ses efektleri
        try:
            self.snd_player_attack = pygame.mixer.Sound("Sounds/Sekiro_attack.mp3")
            self.snd_boss_attack = pygame.mixer.Sound("Sounds/Boss_attack.mp3")
            self.snd_victory = pygame.mixer.Sound("Sounds/Victory.mp3")
            self.snd_defeat = pygame.mixer.Sound("Sounds/Death.mp3")

            # Ses seviyelerini ayarlayabileceğimiz yer ( 0 - 1 arasında )
            self.snd_player_attack.set_volume(0.6)
            self.snd_boss_attack.set_volume(0.8)
            self.snd_victory.set_volume(0.8)
            self.snd_defeat.set_volume(0.8)
        except pygame.error as e:
            print("Ses efektleri yüklenirken hata oluştu!")
            print("Hata detayı: ", e)
        
        self.level_musics = {
            self.bg_level1: "Sounds/Gyoubu_soundtrack.mp3",
            self.bg_level2: "Sounds/Genichiro_soundtrack.mp3",
            self.bg_level3: "Sounds/Isshin_soundtrack.mp3"
        }

        # Karakterlerin oluşturulması
        self.oyuncu = Samurai(oyuncu_adi, can = 100, guc = 20, kalkan = 5)
        self.oyuncu_max_can = self.oyuncu.can

        self.boss_gyoubu = Gyoubu("Gyoubu Oniwa", can = 150, guc = 20, kalkan = 5)
        self.boss_genichiro = Genichiro("Genichiro Ashina", can = 200, guc = 25, kalkan = 5)
        self.boss_isshin = Isshin("Isshin Ashina", can = 300, guc = 35, kalkan = 5)

        # Oyuncu görünümü (Sol tarafta, ekranın ortasında)
        self.oyuncu_view = CharView(
            karakter = self.oyuncu,
            img_normal_path = "Images/Chars/Samurai/SamuraiIdleFinal.png",
            img_attack_path = "Images/Chars/Samurai/SamuraiAttackFinal.png",
            img_damage_path = "Images/Chars/Samurai/SamuraiDamageFinal.png",
            pos = pygame.Vector2(350, self.SCREEN_HEIGHT // 2 + 240)
        )

        # Boss görünümleri (Sağ tarafta)
        self.boss_views = {
            self.bg_level1: CharView(self.boss_gyoubu, "Images/Chars/Gyoubu/GyoubuIdleFinal.png", "Images/Chars/Gyoubu/GyoubuAttackFinal.png", "Images/Chars/Gyoubu/GyoubuDamageFinal.png", pygame.Vector2(1150, self.SCREEN_HEIGHT // 2 + 150)),
            self.bg_level2: CharView(self.boss_genichiro, "Images/Chars/Genichiro/GenichiroIdleFinal.png", "Images/Chars/Genichiro/GenichiroAttackFinal.png", "Images/Chars/Genichiro/GenichiroDamageFinal.png", pygame.Vector2(1150, self.SCREEN_HEIGHT // 2 + 185)),
            self.bg_level3: CharView(self.boss_isshin, "Images/Chars/Isshin/IsshinIdleFinal.png", "Images/Chars/Isshin/IsshinAttackFinal.png", "Images/Chars/Isshin/IsshinDamageFinal.png", pygame.Vector2(1150, self.SCREEN_HEIGHT // 2 + 190))
        }

        # Maksimum canları sözlükte tutarak seviyeye göre kolayca çekebiliriz
        self.boss_max_cans = {
            self.bg_level1: self.boss_gyoubu.can,
            self.bg_level2: self.boss_genichiro.can,
            self.bg_level3: self.boss_isshin.can
        }

        # Log paneli
        self.logs: list[str] = []

        self.running = True

        self.soru_havuzu = self.json_soru_yukle("sorular.json")
        self.soru_bekleniyor = False
        
        # Havuzu karıştırarak ilk indexten itibaren soruları oyuncuya yönlendiriyoruz
        random.shuffle(self.soru_havuzu)
        self.aktif_soru_index = 0
        self.mevcut_soru = self.soru_havuzu[self.aktif_soru_index]

        # Buton konumları
        self.butonlar = []
        bx, by, bw, bh = 180, 610, 500, 60
        self.butonlar.append(pygame.Rect(bx, by, bw, bh)) # A şıkkı
        self.butonlar.append(pygame.Rect(bx + 620, by, bw, bh)) # B
        self.butonlar.append(pygame.Rect(bx, by + 80, bw, bh)) # C
        self.butonlar.append(pygame.Rect(bx + 620, by + 80, bw, bh)) # D

        self.muzik_cal(self.current_bg)
        self.bolum_ekrani_goster("BÖLÜM 1: KALEYE GİRİŞ")

        self.dogru_serisi = 0 # Doğru cevap sayacı
        self.odul_ekrani_aktif = False # Ödül seçimi açık mı kontrol et

        # Ekranın ortasında yan yana duracak iki büyük kart butonu 
        self.btn_can_odul = pygame.Rect(self.SCREEN_WIDTH // 2 - 400, self.SCREEN_HEIGHT // 2 - 50, 350, 180)
        self.btn_hasar_odul = pygame.Rect(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2 - 50, 350, 180)

    def yeni_soru_gec(self):
        """Soru cevaplandıktan sonra yeni soruya geçer."""
        self.aktif_soru_index += 1
        # Eğer havuz bittiyse soruları tekrar karıştırıp sıfırla
        if self.aktif_soru_index >= len(self.soru_havuzu):
            random.shuffle(self.soru_havuzu)
            self.aktif_soru_index = 0
        self.mevcut_soru = self.soru_havuzu[self.aktif_soru_index]

    def json_soru_yukle(self, dosya_yolu: str) -> list[Soru]:
        """TAMAMEN AI, Çünkü JSON ilk defa kullanıyorum"""
        """JSON dosyasını okur ve içindeki verileri Soru nesnelerine dönüştürür."""
        gecici_havuz = []
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                soru_listesi = json.load(f) # JSON'ı Python listesine çevirir

                # Her bir sözlüğü (dict) bizim yazdığımız Soru veri modeline çeviriyoruz
                for s in soru_listesi:
                    yeni_soru = Soru(
                        soru_metni= s["soru_metni"],
                        secenekler= s["secenekler"],
                        dogru_cevap_index= s["dogru_cevap_index"]
                    )
                    gecici_havuz.append(yeni_soru)
        except FileNotFoundError:
            print(f"HATA: '{dosya_yolu}' dosyası bulunamadı! Lütfen dosya adını kontrol edin.")
            # Eğer dosya yoksa oyun çökmesin diye yedek bir soru oluşturuyoruz
            gecici_havuz.append(Soru("Yedek Soru: JSON dosyası yüklenemedi?", ["A", "B", "C", "D"], 0))
        except json.JSONDecodeError:
            print(f"HATA: '{dosya_yolu}' dosyasının JSON formatında bir yazım hatası var (Virgül veya parantez eksik olabilir)!")
            gecici_havuz.append(Soru("Yedek Soru: JSON format hatası?", ["A", "B", "C", "D"], 0))
            
        return gecici_havuz

    def muzik_cal(self, bg_level):
        """Verilen bölüme ait arka plan müziğini çalar ve loopa alır"""
        try:
            pygame.mixer.music.load(self.level_musics[bg_level])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except:
            print(f"Müzik dosyası yüklenemedi: {self.level_musics[bg_level]}")
    
    def boss_yenildi_ekrani(self, boss_ismi: str):
        """Mevcut ekranı hafifçe karartır, 'Düşman yenildi' yazar ve 3 saniye bekler"""

        self.logs.append(f"{boss_ismi} yenildi.")
        # 1- Ekranı hafifçe karartmak için yarı saydam bir yüzey oluştur
        karartma_yuzeyi = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        karartma_yuzeyi.fill((0,0,0, 180))
        
        # 2- Mevcut arka planı ve karakterleri son kez çizdiriyoruz (alt katman güncel kalsın diye)
        self.current_bg.draw(self.screen)
        self.draw_health_bars()

        # 3- Hazırladığımız yarı saydam karartmayı oyunun üstüne seriyoruz
        self.screen.blit(karartma_yuzeyi,(0,0))

        # 4- Burada Sekiro'daki gibi bir sembol yapabilirdim ama zor, o yüzden kırmızı şerit çekmeye karar verdim
        pygame.draw.rect(self.screen, (150, 0, 0), (0, self.SCREEN_HEIGHT // 2 - 60, self.SCREEN_WIDTH, 120))

        # 5- Zafer yazısı
        zafer_metni = self.victory_font.render("BOSS DEFEATED", True, (255,255,255))
        zafer_rect = zafer_metni.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(zafer_metni, zafer_rect)

        # 6- Ekranı güncelle ve 3 saniye boyunca zafer anı kalsın
        pygame.display.flip()

        pygame.event.clear()
        pygame.time.delay(3000)

    def bolum_ekrani_goster(self, metin: str):
        """Ekranı karartıp 2.5 saniye boyunca bölüm adını gösterir."""
        # 1- Ekranı tamamen siyaha boya
        self.screen.fill((0,0,0))

        # 2- Yazıyı oluştur ve hizala
        yazi_yuzeyi = self.title_card_font.render(metin, True, (240, 240, 240))
        yazi_rect = yazi_yuzeyi.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # 3- Yazıyı ekrana bas ve güncelle
        self.screen.blit(yazi_yuzeyi, yazi_rect)
        pygame.display.flip()

        # 4- Geçiş hissi için arkadaki eventleri temizle
        pygame.event.clear()
        pygame.time.delay(2500)
    
    @property
    def current_boss(self) -> Chars:
        """Mevcut arka plana göre aktif Boss gelir."""
        if self.current_bg == self.bg_level1:
            return self.boss_gyoubu
        elif self.current_bg == self.bg_level2:
            return self.boss_genichiro
        elif self.current_bg == self.bg_level3:
            return self.boss_isshin
        
    @property
    def current_boss_view(self) -> CharView:
        """Mevcut arka plana göre aktif bossun görsel temsilini getirir."""
        return self.boss_views[self.current_bg]

    def handle_events(self):
        """Klavye, fare ve sistem olaylarını yönetir."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Tıklama kontrolü
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.odul_ekrani_aktif:
                    # Kart 1 can yenileme
                    if self.btn_can_odul.collidepoint(mouse_pos):
                        yenilenecek_can = self.oyuncu_max_can // 4
                        self.oyuncu.can = min(self.oyuncu_max_can, self.oyuncu.can + yenilenecek_can)

                        self.odul_ekrani_aktif = False
                        self.soru_bekleniyor = True
                        return
                    
                    # Kart 2 hasar
                    elif self.btn_hasar_odul.collidepoint(mouse_pos):
                        kritik_hasar = int(self.oyuncu.guc * 1.5)

                        self.current_boss.can -= kritik_hasar
                        
                        # Görsel ve ses
                        self.snd_player_attack.play()
                        self.oyuncu_view.trigger_state("attack", duration=450, dash_offset=580)
                        self.current_boss_view.trigger_state("damage", duration=450)

                        self.odul_ekrani_aktif = False
                        self.soru_bekleniyor = True
                        return
                    continue

                if self.mevcut_soru is None or self.soru_bekleniyor:
                    continue # Döngünün başına dön, hiçbir işlem yapma
                # 4 butondan hangisine tıkladığını kontrol et
                for i, buton in enumerate(self.butonlar):
                    if buton.collidepoint(mouse_pos):
                        self.cevap_kontrol_et(secilen_index=i)
                        return

    def cevap_kontrol_et(self, secilen_index: int):
        """Cevabı kontrol eder, hasar mekanizmalarını ve animasyonlarını tetikler."""
        dogru_mu = (secilen_index == self.mevcut_soru.dogru_cevap_index)
        self.mevcut_soru = None

        self.cevap_bildirim_ekrani_goster(dogru_mu)

        if dogru_mu:
            self.dogru_serisi += 1
            # Doğru cevap aksiyonu
            self.oyuncu.celik_firtina(self.current_boss)
            self.snd_player_attack.play()

            # Atılma animasyonu
            self.oyuncu_view.trigger_state("attack", duration=450, dash_offset=580)
            self.current_boss_view.trigger_state("damage", duration=450)

            # 3 DOĞRUYA ULAŞILDI MI
            if self.dogru_serisi == 3:
                self.odul_ekrani_aktif = True
                self.dogru_serisi = 0

        else: 
            self.dogru_serisi = 0

            if self.current_bg == self.bg_level1:
                self.boss_gyoubu.savas_baltasi(self.oyuncu)
            elif self.current_bg == self.bg_level2:
                self.boss_genichiro.yildirim_katana(self.oyuncu)
            elif self.current_bg == self.bg_level3:
                self.boss_isshin.mizrak_sarj(self.oyuncu)
            
            self.snd_boss_attack.play()
            self.current_boss_view.trigger_state("attack", duration=450, dash_offset=-580)
            self.oyuncu_view.trigger_state("damage", duration=450)

        # Savaş algoritması çalıştıktan sonra yeni soruya geç
        if not self.odul_ekrani_aktif:
            self.soru_bekleniyor = True
    
    def cevap_bildirim_ekrani_goster(self, dogru_mu: bool):
        """Soru kaybolduktan sonra ekrana cevap çıkar"""

        # 1. Arka planı hafif karartmak için transparan yüzey
        karartma_yuzeyi = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        karartma_yuzeyi.fill((0, 0, 0, 120)) # Hafif bir karartma
        
        # 2. Soru ve şıklar kalkmış haliyle ekranı bir kez temiz çizdiriyoruz
        self.current_bg.draw(self.screen)
        self.oyuncu_view.draw(self.screen, self.hp_font, scale= 1.2)
        if self.current_boss == self.boss_isshin:
            self.current_boss_view.draw(self.screen, self.hp_font, scale=1.5)
        elif self.current_boss == self.boss_genichiro:
            self.current_boss_view.draw(self.screen, self.hp_font, scale=1.2)
        else:
            self.current_boss_view.draw(self.screen, self.hp_font, scale=1.0)
        self.draw_health_bars()
        
        # Karartmayı ekrana ser
        self.screen.blit(karartma_yuzeyi, (0, 0))
        
        # 3. Duruma göre Renk ve Metin Belirleme
        if dogru_mu:
            şerit_rengi = (0, 120, 50)     # Koyu Yeşil Şerit
            metin_rengi = (150, 255, 150)  # Açık Yeşil Yazı
            durum_metni = "DOĞRU"
        else:
            şerit_rengi = (150, 0, 0)      # Koyu Kırmızı Şerit
            metin_rengi = (255, 150, 150)  # Açık Kırmızı Yazı
            durum_metni = "YANLIŞ"
            
        # 4. Sinematik yatay bandı çiz (Ekranın tam ortasına)
        pygame.draw.rect(self.screen, şerit_rengi, (0, self.SCREEN_HEIGHT // 2 - 60, self.SCREEN_WIDTH, 120))
        
        # 5. Yazıyı bas
        bildirim_surface = self.victory_font.render(durum_metni, True, metin_rengi)
        bildirim_rect = bildirim_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(bildirim_surface, bildirim_rect)
        
        # 6. Ekranı güncelle ve 1.2 saniye (1200 milisaniye) ekranda tut
        pygame.display.flip()
        pygame.event.clear()
        pygame.time.delay(1200)

    def update(self):
        # Eğer bir soru cevaplandıysa ve şu an animasyonların bitmesini bekliyorsak
        if self.soru_bekleniyor and not self.odul_ekrani_aktif:
            # Oyuncu ve boss konumlarına geri döndü mü ve normal mi?
            if self.oyuncu_view.current_state == "normal" and self.current_boss_view.current_state == "normal":
                if self.oyuncu_view.pos.x == self.oyuncu_view.base_x and self.current_boss_view.pos.x == self.current_boss_view.base_x:
                    # Karakterler tamamen durdu, şimdi yeni soruyu getirebiliriz.
                    self.yeni_soru_gec()
                    self.soru_bekleniyor = False # Kilidi aç

        # --- OYUNCUNUN CANLI OLUP OLMADIĞINI KONTROL EDER ---
        if not self.oyuncu.hayatta_mi():
            pygame.mixer.music.stop()
            self.snd_defeat.play()
            self.bolum_ekrani_goster("DEATH")
            self.running = False
            return
        
        # --- BÖLÜM 1 -> BÖLÜM 2 GEÇİŞİ ---
        if self.current_bg == self.bg_level1 and not self.boss_gyoubu.hayatta_mi():
            # 1- Mevcut arka plan üzerinde karartma ve zafer yazısı çıkar
            pygame.mixer.music.stop()
            self.snd_victory.play()
            self.boss_yenildi_ekrani("Gyoubu Oniwa")

            if self.zorluk_modu == "NORMAL":
                self.oyuncu.can = self.oyuncu_max_can
            
            # 2- Arka planı değiştir
            self.current_bg = self.bg_level2
            self.muzik_cal(self.current_bg)
            
            # 3- Tamamen siyah sinematik Bölüm Geçiş ekranını göster
            self.bolum_ekrani_goster("BÖLÜM 2: LORDU KURTARMA")
            
        # --- BÖLÜM 2 -> BÖLÜM 3 GEÇİŞİ ---
        elif self.current_bg == self.bg_level2 and not self.boss_genichiro.hayatta_mi():
            # 1- Zafer Ekranı
            pygame.mixer.music.stop()
            self.snd_victory.play()
            self.boss_yenildi_ekrani("Genichiro Ashina")

            if self.zorluk_modu == "NORMAL":
                self.oyuncu.can = self.oyuncu_max_can
            
            # 2- Arka Plan Değişimi
            self.current_bg = self.bg_level3
            self.muzik_cal(self.current_bg)
            self.oyuncu.can = 100
            
            # 3- Bölüm Geçiş Ekranı
            self.bolum_ekrani_goster("BÖLÜM 3: LORDU ARINDIRMA")
            
        # --- OYUN BİTİŞİ (BÖLÜM 3 SONU) ---
        elif self.current_bg == self.bg_level3 and not self.boss_isshin.hayatta_mi():
            pygame.mixer.music.stop()
            self.snd_victory.play()
            self.boss_yenildi_ekrani("Isshin Ashina")

            if self.zorluk_modu == "NORMAL":
                self.oyuncu.can = self.oyuncu_max_can

            # Burası şimdilik böyle, belki farklı bir oyun sonu yaparım, yazı yerine
            self.bolum_ekrani_goster("TEBRİKLER, OYUNU TAMAMLADINIZ!")
            self.running = False

    def draw_health_bars(self):
        """Ekranın üst kısmına oyuncu ve boss can barlarını çizer."""
        # --- Tasarım Ayarları ---
        bar_width = 450
        bar_height = 25
        y_pos = 80 # Bölüm isminin biraz altına yerleştiriyoruz
        
        # Renkler (RGB)
        KIRMIZI = (180, 0, 0)
        YESIL = (0, 180, 70)
        ARKA_PLAN_GRI = (50, 50, 50)
        BEYAZ = (255, 255, 255)
        CERCEVE_RENGI = (200, 200, 200)

        # 1. OYUNCU CAN BARI (Ekranın Sol Üstü)
        x_oyuncu = 100
        # Can oranını hesapla (0 ile 1 arasında sınırla)
        oyuncu_oran = max(0.0, min(1.0, self.oyuncu.can / self.oyuncu_max_can))
        
        # Arka plan (Boş bar) ve Dolu bar dikdörtgenleri
        pygame.draw.rect(self.screen, ARKA_PLAN_GRI, (x_oyuncu, y_pos, bar_width, bar_height))
        pygame.draw.rect(self.screen, YESIL, (x_oyuncu, y_pos, int(bar_width * oyuncu_oran), bar_height))
        pygame.draw.rect(self.screen, CERCEVE_RENGI, (x_oyuncu, y_pos, bar_width, bar_height), 2) # Çerçeve

        # Oyuncu Metni
        oyuncu_text = self.hp_font.render(f"{self.oyuncu.isim}: {self.oyuncu.can}/{self.oyuncu_max_can}", True, BEYAZ)
        self.screen.blit(oyuncu_text, (x_oyuncu, y_pos - 25))

        # 2. BOSS CAN BARI (Ekranın Sağ Üstü)
        x_boss = self.SCREEN_WIDTH - bar_width - 100
        aktif_boss = self.current_boss
        boss_max_can = self.boss_max_cans[self.current_bg]
        boss_oran = max(0.0, min(1.0, aktif_boss.can / boss_max_can))

        # Arka plan (Boş bar) ve Dolu bar dikdörtgenleri
        pygame.draw.rect(self.screen, ARKA_PLAN_GRI, (x_boss, y_pos, bar_width, bar_height))
        pygame.draw.rect(self.screen, KIRMIZI, (x_boss, y_pos, int(bar_width * boss_oran), bar_height))
        pygame.draw.rect(self.screen, CERCEVE_RENGI, (x_boss, y_pos, bar_width, bar_height), 2) # Çerçeve

        # Boss Metni
        boss_text = self.hp_font.render(f"{aktif_boss.isim}: {aktif_boss.can}/{boss_max_can}", True, BEYAZ)
        # Sağ hizalama için metnin genişliğini hesaba katıyoruz
        self.screen.blit(boss_text, (x_boss + bar_width - boss_text.get_width(), y_pos - 25))

    def draw(self):
        """Ekrana çizim işlemlerini gerçekleştirir."""
        # 1- Current backgroundın kendi çizim fonksiyonunu çağırıyoruz.
        self.current_bg.draw(self.screen)

        # 2- Bölüm ismini ekrana yazdırıyoruz.
        text_surface = self.font.render(self.current_bg.text_title, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 40))
        self.screen.blit(text_surface, text_rect)

        # 3- Karakterleri çiz
        self.oyuncu_view.draw(self.screen, self.hp_font, scale = 1.2)
        if self.current_boss == self.boss_isshin:
            self.current_boss_view.draw(self.screen, self.hp_font, scale = 1.5)
        elif self.current_boss == self.boss_genichiro:
            self.current_boss_view.draw(self.screen, self.hp_font, scale=1.2)
        else:
            self.current_boss_view.draw(self.screen, self.hp_font, scale=1.0)

        # 4- Can barlarını çiz
        self.draw_health_bars()
        if self.odul_ekrani_aktif:
            karartma = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            karartma.fill((0,0,0,100))
            self.screen.blit(karartma,(0,0))

            mouse_pos = pygame.mouse.get_pos()
            card_title_font = pygame.font.SysFont("Arial", 26, bold=True)
            card_desc_font = pygame.font.SysFont("Arial", 18)

            # Can kart çizimi
            if self.btn_can_odul.collidepoint(mouse_pos):
                c_bg, c_border = (30,55,35), (0,230,100) # Yeşil hover
            else:
                c_bg, c_border = (40,40,40), (150,150,150)

            pygame.draw.rect(self.screen, c_bg, self.btn_can_odul, border_radius=15)
            pygame.draw.rect(self.screen, c_border, self.btn_can_odul,3, border_radius=15)

            t1 = card_title_font.render("ŞİFA KARTINI SEÇ", True, (0,255,120))
            d1 = card_desc_font.render("Maksimum canınızın %25'ini", True, (220,220,220))
            d1_2 = card_desc_font.render("anında yeniler.", True, (220,220,220))
            self.screen.blit(t1, t1.get_rect(center=(self.btn_can_odul.centerx, self.btn_can_odul.y + 40)))
            self.screen.blit(d1, d1.get_rect(center=(self.btn_can_odul.centerx, self.btn_can_odul.y + 90)))
            self.screen.blit(d1_2, d1_2.get_rect(center=(self.btn_can_odul.centerx, self.btn_can_odul.y + 120)))

            # Hasar kart çizimi
            if self.btn_hasar_odul.collidepoint(mouse_pos):
                h_bg, h_border = (60,35,35), (255,60,60) # Kırmızı hover
            else:
                h_bg, h_border = (40,40,40), (150,150,150)
            
            pygame.draw.rect(self.screen, h_bg, self.btn_hasar_odul, border_radius=15)
            pygame.draw.rect(self.screen, h_border, self.btn_hasar_odul, 3, border_radius=15)

            t2 = card_title_font.render("ÖFKE KARTINI SEÇ", True, (255,100,100))
            d2 = card_desc_font.render("Boss'a anlık olarak gücünüzün", True, (220,220,220))
            d2_2 = card_desc_font.render("1.5 katı hasar vurur.", True, (220,220,220))
            self.screen.blit(t2, t2.get_rect(center=(self.btn_hasar_odul.centerx, self.btn_hasar_odul.y + 40)))
            self.screen.blit(d2, d2.get_rect(center=(self.btn_hasar_odul.centerx, self.btn_hasar_odul.y + 90)))
            self.screen.blit(d2_2, d2_2.get_rect(center=(self.btn_hasar_odul.centerx, self.btn_hasar_odul.y + 120)))

        # 5- Soru paneli
        elif self.mevcut_soru:
            soru_panel_rect = pygame.Rect(100,150,1300,60)
            pygame.draw.rect(self.screen, (30,30,30), soru_panel_rect, border_radius=10)

            """Soru metni yazdırma"""
            soru_text = self.soru_font.render(self.mevcut_soru.soru_metni, True, (255,215,0))
            soru_rect = soru_text.get_rect(center=soru_panel_rect.center)
            self.screen.blit(soru_text,soru_rect)

            """Buton çizme"""
            mouse_pos = pygame.mouse.get_pos()
            harfler = ["A) ", "B) ", "C) ", "D) "]

            for i, buton in enumerate(self.butonlar):
                # Hover
                if buton.collidepoint(mouse_pos):
                    bg_color = (70,70,70)
                    text_color = (255,215,0)
                else:
                    bg_color = (45,45,45)
                    text_color = (230,230,230)
                
                # Buton kutusunu çiz
                pygame.draw.rect(self.screen, bg_color, buton, border_radius=8)
                pygame.draw.rect(self.screen, (100,100,100), buton, 2, border_radius=8)

                sik_metni = harfler[i] + self. mevcut_soru.secenekler[i]
                sik_surface = self.soru_font.render(sik_metni, True, text_color)
                sik_rect = sik_surface.get_rect(midleft=(buton.x + 20, buton.centery))
                self.screen.blit(sik_surface, sik_rect)

        # 6- Ekranı güncelle
        pygame.display.flip()
        

    def run(self):
        """Main loop fonksiyonu"""
        while self.running:
            self.clock.tick(60) # 60 FPS
            self.handle_events()
            self.update()
            self.draw()

        # Döngü bittiğinde oyun da biter
        pygame.quit()
        sys.exit()