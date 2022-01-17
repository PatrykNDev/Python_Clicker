import sys
import pygame
import os
import random


# Klasa główna gry
class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        # Rozmiar ekranu gry
        size = width, height = 1244, 800
        # Kolory do rysowania
        self.blue = 50, 100, 200
        self.green = 0, 100, 0
        self.pink = 255, 100, 100
        self.black = 0, 0, 0
        self.yellow = (254, 253, 1)

        self.screen = pygame.display.set_mode(size)
        # Tytuł okienka gry
        pygame.display.set_caption('Clicker z Questami')
        # Ustawienie zegara, aby gra po wykupieniu ulepszenia sama dodawała punkty do ogólnego wyniku
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.delta = 0.0
        # Ladowanie obrazków startowych
        self.dog = pygame.image.load("img/dogLevel2.gif")
        self.dog_rect = self.dog.get_rect()
        self.background = pygame.image.load('img/background_level_1.png')
        self.bcgRect = self.background.get_rect()
        # Inicjalizacja zmiennych
        self.credit = 0
        self.def_inc = 1  # Punkty otrzymywane za pojedyncze kliknięcie
        # Inicjalizacja czcionek
        self.my_font = pygame.font.SysFont(None, 30)
        self.little_font = pygame.font.SysFont(None, 15)
        self.smaller_font = pygame.font.SysFont(None, 25)
        # Inicjalizacja napisów
        self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', True, self.blue)
        self.q_text = self.my_font.render(f'Brak aktywnej misji :(', True, self.blue)
        # Inicjalizacja zmiennych
        self.quest1_started = False
        self.quest2_started = False
        self.quest3_started = False
        self.click = False
        self.click_time = 0  # Zmienna służąca do animacji efektu kliknięcia
        # Inicjalizacja zmiennych do narysowania sklepu
        self.pet_sit_cost = 100
        self.click_upg_cost = 100
        self.dog_upg_cost = 5
        self.pet_sit_clicked = False
        self.click_upg_clicked = False
        self.dog_upg_clicked = False
        self.inc_per_s = 0  # Ustalenie przyrostu punktów na sekundę gry

        self.mission_switch = 0  # self.mission_switch == n - rozpoczęcie misji nr n, self.mission_switch == 0 - brak misji
        # Wywołanie głównej pętli gry
        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img/" + img)
            self.textures[img.replace(".png", "")] = texture  # najlepiej używać rozszerzenia png

    def load_sounds(self):
        pass

    def game(self):
        # Położenie początkowe klikanego obiektu
        self.dog_rect.x = 40
        self.dog_rect.y = self.screen.get_height() - self.dog_rect.height - 80
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.dog_rect.x < x < self.dog_rect.x + self.dog_rect.width and self.dog_rect.y < y < self.dog_rect.y + self.dog_rect.height:
                        # Obsłużenie kliknięcia myszką w klikalny obiekt z ekranu gry.
                        # Na początku animacja przesunięcia klikniętego obiektu.
                        self.dog_rect.x += 10
                        self.dog_rect.y += 10
                        self.credit += self.def_inc  # Zwiększenie liczby punktów
                        # Aktualizacja obiektów zawierających teksty
                        self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                        self.click_text = self.my_font.render(f'+ {self.def_inc}', 1, self.pink)
                        # Odliczanie klatek animacji kliknięcia
                        self.click = True
                        self.click_time = 10
                        # Animacja "odkliknięcia" klikalnego obiektu
                        self.dog_rect.x -= 10
                        self.dog_rect.y -= 10
                    elif 820 <= x <= 1034 and 110 <= y <= 241 and self.credit >= self.pet_sit_cost:
                        # Obsłużenie kliknięcia w ulepszenie dające +1 /s.
                        # Ulepszenie jest obsłużone w funkcji self.shop_draw() przez odczytanie wartości obiektu self.pet_sit_clicked == True.
                        self.credit -= self.pet_sit_cost
                        self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                        self.pet_sit_clicked = True
                    elif 820 <= x <= 1034 and 246 <= y <= 460 and self.credit >= self.click_upg_cost:
                        # Obsłużenie kliknięcia w ulepszenie dające więcej punktów za kliknięcie w obiekt dog_rect.
                        # Ulepszenie jest obsłużone w funkcji self.draw_second_upgrade() przez odczytanie wartości obiektu self.click_upg_clicked == True.
                        self.credit -= self.click_upg_cost
                        self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                        self.click_upg_clicked = True
                    elif 820 <= x <= 1034 and 465 <= y <= 679 and self.credit >= self.dog_upg_cost and self.dog_upg_cost <= 55:
                        # Obsłużenie kliknięcia w ulepszenie zmieniające grafikę w grze.
                        # Ulepszenie jest obsłużone w funkcji self.draw_third_upgrade() oraz poniżej w kodzie przez odczytanie wartości obiektu self.dog_upg_clicked == True.
                        self.credit -= self.dog_upg_cost
                        self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                        self.dog_upg_clicked = True
                if event.type == pygame.USEREVENT:
                    # Zwiększanie wyniku gracza co 1s
                    self.credit += self.inc_per_s
                    self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                    # Losowanie misji.
                    # Jeżeli self.mission_switch == n, aktywowana jest n-ta misja.
                    self.mission_switch = random.randint(1, 75)
            # Koniec obsługiwana zdarzeń
            # Sprawdzenie warunków pojawienie się misji
            if self.mission_switch == 1:
                # Rozpoczęcie misji nr 1
                self.quest1_started = True
                self.credit, self.mission_passed = self.mission(self.screen,
                                                                self.credit)  # Funkcja zmieniająca rysowanie ekranu
                # Aktualizowanie obiektów wyświetlanych później na ekranie po zakończeniu działania misji
                self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                self.q_text = self.my_font.render(f'Brak aktywnej misji :(', 1, self.blue)
                # Rozeznanie czy misja została zakończona sukcesem czy porażką
                if self.mission_passed:
                    self.m1_text = self.smaller_font.render(
                        'Przeszedles pierwsza misje i twoje kliknięcia są teraz warte o 1 punkt więcej', 1,
                        self.blue)
                    # Nagroda za misję
                    self.def_inc += 1
                else:
                    self.m1_text = self.my_font.render('Przegrałeś pierwszą misję', 1, self.blue)
                # W następnej klatce animacji warunek rozpoczęcia misji 'self.mission_switch == 1' == False
                self.mission_switch = 0

            # Rozpoczęcie misji nr 2
            if self.mission_switch == 2:
                self.quest2_started = True
                self.credit, self.mission2_passed = self.mission2(self.screen, self.credit,
                                                                  self.dog_upg_cost)  # self.mission2() - funkcja odpowiedzialna za wyświetlanie misji
                # Aktualizacja obiektów wyświetlanych później na ekranie po zakończeniu działania misji
                self.my_text = self.my_font.render(f'Twoje zebrane punkty: {self.credit}', 1, self.blue)
                self.q_text = self.my_font.render(f'Brak aktywnej misji :(', 1, self.blue)
                # Rozeznanie czy misja została zakończona sukcesem czy porażką
                if self.mission2_passed:
                    self.m1_text = self.smaller_font.render('Przeszedles drugą misje i teraz masz +1 punkt na sekundę',
                                                            1,
                                                            self.blue)
                    # Nagroda za misję
                    self.inc_per_s += 1
                else:
                    self.m1_text = self.my_font.render('Przegrałeś drugą misję', 1, self.blue)
                # Załadowanie oryginalnych rozmiarów właściwego obiektu self.dog
                if self.dog_upg_cost <= 5:
                    self.dog = pygame.image.load("img\dogLevel2.gif")
                elif self.dog_upg_cost == 55:
                    self.dog = pygame.image.load("img\dog_2.gif")
                else:
                    self.dog = pygame.image.load("img\dog_3.gif")
                self.dog_rect = self.dog.get_rect()
                # Pozycjonowanie obiektu self.dog_rect
                self.dog_rect.x = 40
                self.dog_rect.y = self.screen.get_height() - self.dog_rect.height - 80
                # W następnej klatce animacji warunek rozpoczęcia misji 'self.mission_switch == 2' == False
                self.mission_switch = 0

            # Rysowanie tła i innych obiektów
            self.screen.blit(self.background, self.bcgRect)
            self.screen.blit(self.dog, self.dog_rect)
            # Rysowanie sklepu i pierwszego ulepszenia
            self.pet_sit_cost, self.inc_per_s = self.shop_draw(self.pet_sit_cost, self.pet_sit_clicked, self.inc_per_s)
            self.pet_sit_clicked = False
            # Rysowanie drugiego ulepszenia w sklepie
            self.click_upg_cost, self.def_inc = self.draw_second_upgrade(self.click_upg_cost, self.click_upg_clicked,
                                                                         self.def_inc)
            self.click_upg_clicked = False
            # Rysowanie trzeciego ulepszenia w sklepie
            self.dog_upg_cost = self.draw_third_upgrade(self.dog_upg_cost, self.dog_upg_clicked)
            # Obsłużenie zmiany obrazków psa i tła
            if self.dog_upg_clicked:
                if self.dog_upg_cost == 55:
                    self.background = pygame.image.load("img/background_level_2.gif")
                    self.dog = pygame.image.load("img/dog_2.gif")
                elif self.dog_upg_cost == 105:
                    self.background = pygame.image.load("img/background_3.gif")
                    self.dog = pygame.image.load("img/dog_3.gif")
                self.bcgRect = self.background.get_rect()
                self.dog_rect = self.dog.get_rect()
                self.dog_rect.x = 40
                self.dog_rect.y = self.screen.get_height() - self.dog_rect.height - 80
            self.dog_upg_clicked = False
            # Rysowanie niektórych tekstów
            self.draw_texts(self.def_inc, self.inc_per_s)
            # Rysowanie tekstów i obramowań wokół tekstu
            pygame.draw.rect(self.screen, self.blue, pygame.Rect(495, 5, self.q_text.get_width() + 10, 30), 1)
            self.screen.blit(self.q_text, (500, 10))
            # Napis o stanie po misji:
            if self.quest1_started or self.quest2_started:
                pygame.draw.rect(self.screen, self.blue, pygame.Rect(495, 35, self.m1_text.get_width() + 10, 30), 1)
                self.screen.blit(self.m1_text, (500, 40))
            # Rozliczenie klatek animacji kliknięcie w psa
            if self.click_time > 0:
                self.click_time -= 1
            # Napis +1' lub  '+2' lub '+3' itd. za każde kliknięcie myszką, zależny od zmiennej def_inc
            if self.click and self.click_time > 0:
                self.screen.blit(self.click_text, (
                    self.dog_rect.x + self.dog_rect.width + 10, self.dog_rect.y + (self.dog_rect.height / 2.0)))
            # Tekst "Twoje zebrane punkty: ..."
            pygame.draw.rect(self.screen, self.blue, pygame.Rect(15, 5, self.my_text.get_width() + 10, 30), 1)
            self.screen.blit(self.my_text, (20, 10))
            pygame.display.flip()
            # Program nie może renderować więcej niż 60 klatek na sekundę
            self.clock.tick(60)

    #Rysowanie sklepu i pierwszego ulepszenia do punktów na sekundę
    def shop_draw(self, pet_sit_cost: int, clicked: bool, increment_per_s: int) -> int:
        pet_sit_upgrade = 1  # Ile punktów więcej dostanie gracz na 1 sekundę
        if clicked:  # Rozpoznanie kliknięcia ulepszenia
            pet_sit_cost *= 2  # Zwiększenie kosztów
            increment_per_s += pet_sit_upgrade  # Zwiększenie punktów zdobywanych
        # Rysowanie sklepu
        # Rysowanie 1 ulepszenia
        pet_sitter = pygame.image.load("img/pet_sitter.gif")
        pet_sit_rect = pet_sitter.get_rect()
        pet_sit_rect.x = 820
        pet_sit_rect.y = 110
        # Inicjalizacja napisów
        shop_text = self.my_font.render('Sklep z ulepszeniami', 1, self.pink)
        upg_title = self.my_font.render(f'Opiekun dla psa', 1, self.yellow)
        pet_sit_text = self.my_font.render(f'Koszt: {pet_sit_cost}', 1, self.yellow)
        pet_sit_text2 = self.little_font.render(f'Daje + {pet_sit_upgrade}/s dodatkowych punktów', 1, self.yellow)
        # Rysowanie obramowań wokół tekstów i wokół całego sklepu
        pygame.draw.rect(self.screen, self.pink,
                         pygame.Rect(815, 105, self.screen.get_width() - 815, self.screen.get_height() - 145), 1)
        pygame.draw.rect(self.screen, self.pink, pygame.Rect(815, 70, self.screen.get_width() - 815, 30), 1)
        # Dodanie napisów i obrazka
        self.screen.blit(shop_text, (820, 75))
        self.screen.blit(pet_sitter, pet_sit_rect)
        self.screen.blit(upg_title, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 5))
        self.screen.blit(pet_sit_text, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 35))
        self.screen.blit(pet_sit_text2, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 65))
        # Zwrócenie nowego kosztu ulepszenia i ulepszonej statystyki
        return pet_sit_cost, increment_per_s

    # Rysowanie ulepszenia do punktów za kliknięcie
    def draw_second_upgrade(self, click_upg_cost: int, clicked: bool, increment_on_click: int) -> int:
        click_upgrade = 1  # O ile zwiększone zostaną punkty
        if clicked:  # Rozpoznanie kliknięcia ulepszenia, clicked == True - > ulepszenie kliknięte
            click_upg_cost *= 2  # Zwiększenie kosztów następnego ulepszenia
            increment_on_click += click_upgrade  # Zwiększenie punktów zdobywanych
        # Inicjalizacja obrazka
        click_upgr_icon = pygame.image.load("img\on_click_upgrade.gif")
        click_upgr_rect = click_upgr_icon.get_rect()
        click_upgr_rect.x = 820
        click_upgr_rect.y = 246
        # Inicjalizacja napisów
        upg_title_2 = self.my_font.render(f'Karma pieska', 1, self.yellow)
        pet_sit_text = self.my_font.render(f'Koszt: {click_upg_cost}', 1, self.yellow)
        pet_sit_text2 = self.little_font.render(f'Daje + {click_upgrade} punktów na kliknięcie', 1, self.yellow)

        # Dodanie napisów i obrazka ulepszenia
        self.screen.blit(click_upgr_icon, click_upgr_rect)
        self.screen.blit(upg_title_2, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 5))
        self.screen.blit(pet_sit_text, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 35))
        self.screen.blit(pet_sit_text2, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 65))
        # Nowe wartości kosztu i punktów za 1 klik
        return click_upg_cost, increment_on_click

    # Ulepszenie dające nowe obrazki psa i tła
    def draw_third_upgrade(self, upg_cost_3: int, clicked: bool) -> int:
        yellow = (254, 253, 1)
        if clicked and upg_cost_3 < 105:  # Rozpoznanie kliknięcia ulepszenia, clicked == True - > ulepszenie kliknięte.  Warunek upg_cost_3 < 105 sprawdza czy jest to ostatnie ulepszenie.
            upg_cost_3 += 50  # Zwiększenie kosztów
        # Obrazek ulepszenia
        dog_upgr_icon = pygame.image.load("img\dogs_shelter.gif")
        dog_upgr_rect = dog_upgr_icon.get_rect()
        dog_upgr_rect.x = 820
        dog_upgr_rect.y = 465
        # Napisy ulepszenia
        upg_title_3 = self.my_font.render(f'Nowy piesek', 1, yellow)
        if upg_cost_3 == 105:
            cost_txt = self.my_font.render(f'Maks. ulepszenie', 1, self.pink)
        else:
            cost_txt = self.my_font.render(f'Koszt: {upg_cost_3}', 1, yellow)
        description_upgr = self.little_font.render(f'Nowy piesek i tło', 1, yellow)
        # Dodanie do ekranu napisów i obrazka
        self.screen.blit(dog_upgr_icon, dog_upgr_rect)
        self.screen.blit(upg_title_3, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 5))
        self.screen.blit(cost_txt, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 35))
        self.screen.blit(description_upgr, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 65))
        # Return nowego kosztu ulepszenia
        return upg_cost_3

    # Logika pisania statystyk na ekranie
    def draw_texts(self, points_on_click: int, points_per_second: int) -> None:
        font_19 = pygame.font.SysFont(None, 19)

        points_on_click_txt = font_19.render(f'Punkty od kliknięcia: +{points_on_click}', 1, self.blue)
        points_per_second_txt = font_19.render(f'Punkty na sekundę: +{points_per_second}', 1, self.blue)

        pygame.draw.rect(self.screen, self.blue, pygame.Rect(15, 45, points_on_click_txt.get_width() + 10, 25), 1)
        self.screen.blit(points_on_click_txt, (20, 50))

        pygame.draw.rect(self.screen, self.blue, pygame.Rect(15, 70, points_on_click_txt.get_width() + 10, 21), 1)
        self.screen.blit(points_per_second_txt, (20, 72))

    # Logika misji ze znikającym obiektem do klikania
    def mission2(self, screen: pygame.Surface, credit: int, dog_upg_cost: int) -> (int, bool):
        counting = 4  # 4 kliki do startu misji
        # Napisy
        my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', 1, self.blue)
        q_text = self.my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów na sekundę!', 1,
                                     (255, 100, 100))
        side_text = self.my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
        # Zmienne pomocnicze
        progress = 0.22  # Startowy postęp misji 0.22/1.0
        quest_started = False  # Quest nie zaczyna się bez interakcji gracza
        mission_passed = False  # Początkowo zakładamy że gracz przegra misję
        click = False  # Do animacji pokazywania wyklikanych punktów obok obiektu
        click_time = 0  # Do animacji pokazywania wyklikanych punktów obok obiektu
        # Logika odpowiedzialna za wykrycie jaki obrazek powinien zostać użyty w grze
        if dog_upg_cost <= 5:
            dog = pygame.image.load("img/dog_level2_smaller.gif")
        elif dog_upg_cost == 55:
            dog = pygame.image.load("img/dog_2_smaller.gif")
        else:
            dog = pygame.image.load("img/dog_3_little.gif")
        # Inicjalizacja obrazka
        dog_rect = dog.get_rect()
        dog_rect.x = 40
        dog_rect.y = 100
        max_tps = 20
        # Główna pętla misji
        while 1:
            # Logika zmniejszania paska postępu misji
            self.delta += self.clock.tick(60)/1000.0  # Konwersja upływającego czasu na sekundy
            # Co 1/max tps sekundy wykonuje sie ponizszy kod pętli
            while self.delta > 1/max_tps:
                self.delta-=1/max_tps
                if quest_started:  # Warunek spełniony po 4 klikach
                    if progress > 0:  # Zmienna progress gdy jest mniejsza równa zero oznacza przegraną
                        progress -= 0.005
                    else:
                        return credit, mission_passed
            # Logika obsługiwania zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Logika obsłużenia kliku w obiekt za punkty
                    if dog_rect.x < x < dog_rect.x + dog_rect.width and dog_rect.y < y < dog_rect.y + dog_rect.height:
                        dog_rect.x += 10
                        dog_rect.y += 10
                        credit += self.def_inc
                        my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', 1, self.blue)
                        click_text = self.my_font.render(f'+ {self.def_inc}', 1, self.blue)
                        click = True
                        click_time = 10
                        # Odliczanie do rozpoczęcia misji
                        if counting >= 1:
                            counting -= 1
                            side_text = self.my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
                            if counting == 0:  # Tutaj program wejdzie po dekrementacji wartości 1 zmiennej counting
                                quest_started = True
                        elif counting < 1 and 0.0 < progress < 1.0:  # Warunek spełniony gdy odliczanie skończone i gdy gracz nie przegrał i nie wygrał jeszcze misji
                            side_text = self.my_font.render(f'Quest się zaczął', 1, (255, 100, 100))
                            progress += 0.1
                            # Losowanie nowego położenia po kliknięciu w obiekt
                            dog_rect.x = random.randint(40, screen.get_width() - dog_rect.width)
                            dog_rect.y = random.randint(100, screen.get_height() - dog_rect.height)
                        elif counting < 1 and 1.0 <= progress:  # Warunek spełniony gdy gracz wygrał misję
                            mission_passed = True
                        dog_rect.x -= 10
                        dog_rect.y -= 10
                # Logika przyznawania punktów co jedną sekundę
                if event.type == pygame.USEREVENT:
                    credit += self.inc_per_s
                    my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', 1, self.blue)
            # Koniec obsługiwana zdarzeń
            # Licznik klatek animacji
            if click_time > 0:
                click_time -= 1

            screen.blit(self.background, self.bcgRect)
            # Zmienne służące do rysowania paska postępu
            left = 500
            top = 40
            max_width = 400
            height = 20
            progress_temp = progress
            if progress_temp > 1.0:  # Normalizacja zmiennej pokazującej postęp w misji
                progress_temp = 1.0
            # Rysowanie paska postępu i obramówki
            pygame.draw.rect(screen, self.pink, pygame.Rect(left, top, max_width * progress_temp, height))
            pygame.draw.rect(screen, self.blue, pygame.Rect(left, top, max_width, height), 1)
            # Logika animacji kliku
            if click and click_time > 0:
                screen.blit(click_text, (dog_rect.x + dog_rect.width + 10, dog_rect.y + (dog_rect.height / 2.0)))
            # Rysowanie obrazka i tekstów
            screen.blit(dog, dog_rect)
            pygame.draw.rect(screen, self.pink, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
            screen.blit(q_text, (500, 10))
            pygame.draw.rect(screen, self.blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
            screen.blit(my_text, (20, 10))
            pygame.draw.rect(screen, self.pink, pygame.Rect(15, 35, side_text.get_width() + 10, 30), 1)
            screen.blit(side_text, (20, 40))
            pygame.display.flip()
            # Sprawdzenie czy misja zakończona sukcesem
            if mission_passed:
                return credit, mission_passed

    # Misja z klikaniem na czas tak szybko aby pasek postępu nie spadł do zera
    def mission(self, screen: pygame.Surface, credit: int):
        # Inicjalizacja zmiennej
        counting = 4
        # Inicjalizacja tekstów
        my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', True, self.blue)
        q_text = self.my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów za 1 klik myszką!', 1,
                                     (255, 100, 100))
        side_text = self.my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
        # Incjalizacja czcionki i tekstu
        font_20 = pygame.font.SysFont(None, 20)
        mission_description = font_20.render(
            f'Opis misji nr 1: klikaj na czas w nieruchomy obiekt, tak szybko aby pasek postępu nie spadł do 0!', 1,
            self.blue)
        # Inicjalizacja zmiennych
        progress = 0.32
        quest_started = False
        mission_passed = False
        click = False
        click_time = 0
        # Inicjalizacja położenia obiektu
        self.dog_rect.x = 40
        self.dog_rect.y = screen.get_height() - self.dog_rect.height - 80
        max_tps = 20
        # Główna pętla
        while 1:
            self.delta += self.clock.tick(60) / 1000.0  # Konwersja upływającego czasu na sekundy
            while self.delta > 1 / max_tps:
                self.delta -= 1 / max_tps
                if quest_started:
                    # Zmniejszanie paska postępu
                    if progress > 0:
                        progress -= 0.025
                    else:  # Misja przegrana
                        return credit, mission_passed
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.dog_rect.x < x < self.dog_rect.x + self.dog_rect.width and self.dog_rect.y < y < self.dog_rect.y + self.dog_rect.height:
                        # Obsługa kliknięcia w obiekt klikalny
                        self.dog_rect.x += 10
                        self.dog_rect.y += 10
                        credit += self.def_inc
                        my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', 1, self.blue)
                        click_text = self.my_font.render(f'+ {self.def_inc}', 1, self.blue)
                        click = True
                        click_time = 10
                        # Obsługa odliczania kliknięć do rozpoczęcia misji
                        if counting >= 1:
                            counting -= 1
                            side_text = self.my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
                            if counting == 0:
                                quest_started = True
                        elif counting < 1 and 0.0 < progress < 1.0:  # Warunek spełniony gdy odliczanie skończone i gdy gracz nie przegrał i nie wygrał jeszcze misji
                            side_text = self.my_font.render(f'Quest się zaczął', 1, (255, 100, 100))
                            progress += 0.1
                        elif counting < 1 and 1.0 <= progress:  # Warunek spełniony gdy gracz wygrał misję
                            mission_passed = True
                        self.dog_rect.x -= 10
                        self.dog_rect.y -= 10
                # Logika przyznawania punktów co jedną sekundę
                if event.type == pygame.USEREVENT:
                    credit += self.inc_per_s
                    my_text = self.my_font.render(f'Twoje zebrane punkty: {credit}', 1, self.blue)
            # Koniec obsługiwana zdarzeń
            # Licznik klatek animacji
            if click_time > 0:
                click_time -= 1
            # Rysowanie tła
            screen.blit(self.background, self.bcgRect)
            # Zmienne służące do rysowania paska postępu
            left = 500
            top = 40
            max_width = 400
            height = 20
            progress_temp = progress
            # Normalizacja zmiennej pokazującej postęp w misji
            if progress_temp > 1.0:
                progress_temp = 1.0
            # Rysowanie paska postępu i obramówki
            pygame.draw.rect(screen, self.pink, pygame.Rect(left, top, max_width * progress_temp, height))
            pygame.draw.rect(screen, self.blue, pygame.Rect(left, top, max_width, height), 1)
            # Logika animacji kliku
            if click and click_time > 0:
                screen.blit(click_text, (
                    self.dog_rect.x + self.dog_rect.width + 10, self.dog_rect.y + (self.dog_rect.height / 2.0)))
            # Rysowanie obrazka do klikania
            screen.blit(self.dog, self.dog_rect)
            # Rysowanie napisów
            pygame.draw.rect(screen, self.pink, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
            screen.blit(q_text, (500, 10))
            pygame.draw.rect(screen, self.blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
            screen.blit(my_text, (20, 10))
            pygame.draw.rect(screen, self.pink, pygame.Rect(15, 35, side_text.get_width() + 10, 30), 1)
            screen.blit(side_text, (20, 40))
            pygame.draw.rect(screen, self.blue, pygame.Rect(495, 70, mission_description.get_width() + 10, 30), 1)
            screen.blit(mission_description, (500, 74))
            pygame.display.flip()
            if mission_passed:  # Jeżeli gracz wygrał misję to poinformuj pętlę główną gry i zwróć jej wynik gracza
                return credit, mission_passed


if __name__ == "__main__":
    Game()
