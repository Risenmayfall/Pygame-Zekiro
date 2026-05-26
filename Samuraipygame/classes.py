import sys
import pygame
from dataclasses import dataclass
from PIL import Image, ImageSequence

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
        ham = self.guc * 1.33
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
class Genichiro(Chars):
    def yildirim_katana(self, dusman: Chars) -> int:
        ham = self.guc * 1.66
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
class Isshin(Chars):
    def mizrak_sarj(self, dusman: Chars) -> int:
        ham = self.guc * 2
        net = self._hasar_hesapla(ham)
        dusman.can = max(0,dusman.can - net)
        return net
    
# -------------------------------------------------------------

@dataclass
class CharView:
    """
    Bir karakterin ekrandaki temsili:
    karakter
    image
    pos: ekrandaki merkez konum
    """
    karakter: Chars
    image: pygame.Surface
    pos: pygame.Vector2
    alive: bool = True

    @property
    def rect(self) -> pygame.Rect:
        r = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        return r
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, highlight: bool = False, scale: float = 1.0):
        # Highlight true ise etrafına çerçeve atar
        if not self.alive:
            return
        
        img = self.image
        if abs(scale - 1.0) > 1e-3:
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))

        draw_rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(img, draw_rect)

    def hit_test(self, mouse_pos) -> bool:
        # Point n click?
        if not self.alive:
            return False
        return self.rect.collidepoint(mouse_pos)

# Gyoubu Background
class Background1:
    def __init__(self, screen_width, screen_height):
        try:
            self.image = pygame.image.load("Images\Arkaplan\Gyoubuarkaplan.png").convert()
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
            self.image = pygame.image.load("Images\Arkaplan\Genichiroarkaplan.png").convert()
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
            self.image = pygame.image.load("Images\Arkaplan\Isshinarkaplan.png").convert()
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
    def __init__(self, screen, oyuncu_adi: str = "Samurai"):
        # Pygame start
        pygame.init()

        # Pencere boyutu ayarları
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 750
        self.screen = screen
        pygame.display.set_caption("Zekiro: Shadows Die Once")

        # Zamanlayıcı ve font
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ATC Laurel Black", 36, bold = True)
        self.hp_font = pygame.font.SysFont("Arial", 20, bold = True)
        self.title_card_font = pygame.font.SysFont("Times New Roman", 72, bold=True)
        self.victory_font = pygame.font.SysFont("Georgia", 90, bold = True)


        # Arka plan tanımlama
        self.bg_level1 = Background1(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bg_level2 = Background2(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bg_level3 = Background3(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.current_bg = self.bg_level1

        # Karakterlerin oluşturulması
        self.oyuncu = Samurai(oyuncu_adi, can = 100, guc = 20, kalkan = 5)
        self.oyuncu_max_can = self.oyuncu.can

        self.boss_gyoubu = Gyoubu("Gyoubu Oniwa", can = 150, guc = 20, kalkan = 5)
        self.boss_genichiro = Genichiro("Genichiro Ashina", can = 200, guc = 25, kalkan = 5)
        self.boss_isshin = Isshin("Isshin Ashina", can = 300, guc = 35, kalkan = 5)

        # Maksimum canları sözlükte tutarak seviyeye göre kolayca çekebiliriz
        self.boss_max_cans = {
            self.bg_level1: self.boss_gyoubu.can,
            self.bg_level2: self.boss_genichiro.can,
            self.bg_level3: self.boss_isshin.can
        }

        # Log paneli
        self.logs: list[str] = []

        self.running = True

        self.bolum_ekrani_goster("BÖLÜM 1: KALEYE GİRİŞ")
    
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

    def handle_events(self):
        """Klavye, fare ve sistem olaylarını yönetir."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            
           # Burayı şu anlık silmedim, 1 2 3 basınca ekran değişiyor
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_bg = self.bg_level1
                elif event.key == pygame.K_2:
                    self.current_bg = self.bg_level2
                elif event.key == pygame.K_3:
                    self.current_bg = self.bg_level3
                elif event.key == pygame.K_SPACE:
                    self.current_boss.saldir(self.oyuncu)
                elif event.key == pygame.K_h:
                    self.oyuncu.celik_firtina(self.current_boss)
            

    def update(self):
        # --- BÖLÜM 1 -> BÖLÜM 2 GEÇİŞİ ---
        if self.current_bg == self.bg_level1 and not self.boss_gyoubu.hayatta_mi():
            # 1- Mevcut arka plan üzerinde karartma ve zafer yazısı çıkar
            self.boss_yenildi_ekrani("Gyoubu Oniwa")
            
            # 2- Arka planı değiştir
            self.current_bg = self.bg_level2
            
            # 3- Tamamen siyah sinematik Bölüm Geçiş ekranını göster
            self.bolum_ekrani_goster("BÖLÜM 2: LORDU KURTARMA")
            
        # --- BÖLÜM 2 -> BÖLÜM 3 GEÇİŞİ ---
        elif self.current_bg == self.bg_level2 and not self.boss_genichiro.hayatta_mi():
            # 1- Zafer Ekranı
            self.boss_yenildi_ekrani("Genichiro Ashina")
            
            # 2- Arka Plan Değişimi
            self.current_bg = self.bg_level3
            
            # 3- Bölüm Geçiş Ekranı
            self.bolum_ekrani_goster("BÖLÜM 3: LORDU ARINDIRMA")
            
        # --- OYUN BİTİŞİ (BÖLÜM 3 SONU) ---
        elif self.current_bg == self.bg_level3 and not self.boss_isshin.hayatta_mi():
            self.boss_yenildi_ekrani("Isshin Ashina")
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

        # 3- Can barlarını çiz
        self.draw_health_bars()

        # 4- Ekranı güncelle
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