import sys
import pygame
from dataclasses import dataclass
from PIL import Image, ImageSequence
from classes import BattleGame
from menu import MainMenu, NameInputScreen

def main():
    pygame.init()

    """
    BattleGame içinde de ekran boyutu bulunuyor ancak
    Burada bir daha değer vermemin sebebi menuden bir string dönüt alacağım, ona göre battlegame'i çalıştıracağım
    """

    # Ekran boyutları
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 750
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Zekiro: Shadows Die Once")

    # 1- Başlangıç ekranı (Menü)
    menu = MainMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    menu_choice = menu.ren_menu() # Str dönüt

    # 2- Seçime göre aksiyon
    if menu_choice == "PLAY":
        # Başlangıç ekranından sonra isim alma ekranı
        input_screen = NameInputScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        secilen_isim = input_screen.run() # Oyuncunun girdiği adı veya Samurai ismini döndürür

        # Oyunu, seçilen isimle başlatıyoruz
        game = BattleGame(oyuncu_adi = secilen_isim)
        game.run()
    else:
        pygame.quit()
        sys.exit()


"""OYUNU BAŞLATMA"""
if __name__ == "__main__":
   main()