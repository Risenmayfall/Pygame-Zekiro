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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_play_rect.collidepoint(event.pos):
                            return "PLAY"
                        elif self.btn_quit_rect.collidepoint(event.pos):
                            return "QUIT"
            
            self.draw()