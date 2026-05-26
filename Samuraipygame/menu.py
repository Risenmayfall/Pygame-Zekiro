import sys
import pygame

class MainMenu:
    def __init__(self,screen, screen_width, screen_height):
        self.screen = screen
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        try:
            self.bg_image = pygame.image.load("Images\Arkaplan\ZekiroShadowsDieOnce2.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error as e:
            print("Başlangıç arka plan görseli yüklenirken hata oluştu!")
            print("Hata detay: ", e)
            pygame.quit()
            sys.exit()

        # Yazı tipleri ve renkler
        self.font = pygame.font.SysFont("Arial", 40, bold = True)
        self.COLOR_NORMAL = (200, 200, 200)
        self.COLOR_HOVER = (255, 215, 0)

        # Buton konumları ve alanları
        self.btn_play_rect = pygame.Rect(0,0,200,60)
        self.btn_play_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 150)

        self.btn_quit_rect = pygame.Rect(0,0,200,60)
        self.btn_quit_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 250)
    
    def draw(self):
        # Arka plan görselini getir
        self.screen.blit(self.bg_image, (0,0))

        # Fare konumu al (Çünkü hover efekti yapacağız)
        mouse_pos = pygame.mouse.get_pos()

        # OYNA BUTONU
        if self.btn_play_rect.collidepoint(mouse_pos):
            play_text = self.font.render("OYNA", True, self.COLOR_HOVER)
        else:
            play_text = self.font.render("OYNA", True, self.COLOR_NORMAL)
        
        play_rect = play_text.get_rect(center=self.btn_play_rect.center)
        self.screen.blit(play_text, play_rect)

        # ÇIKIŞ BUTONU
        if self.btn_quit_rect.collidepoint(mouse_pos):
            quit_text = self.font.render("ÇIKIŞ", True, self.COLOR_HOVER)
        else:
            quit_text = self.font.render("ÇIKIŞ", True, self.COLOR_NORMAL)
        
        quit_rect = quit_text.get_rect(center=self.btn_quit_rect.center)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    def ren_menu(self) -> str:
        """Menü döngüsü, Seçilen aksiyonu string olarak döner."""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_play_rect.collidepoint(event.pos):
                        return "PLAY"
                    elif self.btn_quit_rect.collidepoint(event.pos):
                        return "QUIT"
            
            self.draw()

class NameInputScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        # Yazı tipleri
        self.title_font = pygame.font.SysFont("Arial", 40, bold = True)
        self.input_font = pygame.font.SysFont("Arial", 36)
        self.hint_font = pygame.font.SysFont("Arial", 20, italic = True)

        self.player_name = ""
        self.max_chars = 12 # İsim sınırı

    def draw(self):
        # Arka plan siyah
        self.screen.fill((20,20,20))

        # 1- Başlık metni
        title_text = self.title_font.render("LÜTFEN ADINIZI GİRİNİZ.", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # 2- İsim kutusu ve girilen isim
        # Bir şey yazılmamışsa görünüş olarak ...
        display_name = self.player_name if self.player_name != "" else "..."
        name_text = self.input_font.render(display_name, True, (255,255,255))
        name_rect = name_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # İsmin altına çizgi
        pygame.draw.line(self.screen, (150, 150, 150), 
                         (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 30), 
                         (self.SCREEN_WIDTH // 2 + 150, self.SCREEN_HEIGHT // 2 + 30), 2)
        
        self.screen.blit(name_text, name_rect)

        # 3- İpucu
        hint_text = self.hint_font.render("Onaylamak için ENTER'a basın.", True, (100, 100, 100))
        hint_rect = hint_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()

    def run(self) -> str:
        """Kullanıcı Enter'a basana kadar klavye girdilerini dinler."""
        clock = pygame.time.Clock()
        
        # Klavyede basılı tutulduğunda harfleri tekrar etmesi için (Silme tuşu basılı tutulursa hızlı silsin diye)
        pygame.key.set_repeat(200, 50)
        
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Enter tuşu
                        if self.player_name.strip() == "":
                            self.player_name = "Samurai"
                        # Tuş tekrarlarını kapat ki oyun içinde sorun olmasın
                        pygame.key.set_repeat(0, 0)
                        return self.player_name.strip()
                        
                    elif event.key == pygame.K_BACKSPACE: # Silme tuşu
                        self.player_name = self.player_name[:-1]
                        
                    elif event.key == pygame.K_SPACE: # Boşluk tuşu
                        if len(self.player_name) < self.max_chars:
                            self.player_name += " "
                            
                    else:
                        # Eğer event.unicode dolu geliyorsa (Normal standart)
                        if event.unicode and event.unicode.isprintable() and len(event.unicode) == 1:
                            if len(self.player_name) < self.max_chars:
                                self.player_name += event.unicode
                        else:
                            # EĞER EVENT.UNICODE ÇALIŞMIYORSA (Yedek Plan):
                            # Basılan tuşun adını alıp karakter sınırına göre ekliyoruz
                            key_name = pygame.key.name(event.key)
                            if len(key_name) == 1 and len(self.player_name) < self.max_chars:
                                # Shift basılı mı kontrolü (Büyük/Küçük harf uyumu için)
                                mods = pygame.key.get_mods()
                                if mods & pygame.KMOD_SHIFT:
                                    self.player_name += key_name.upper()
                                else:
                                    self.player_name += key_name
            
            self.draw()