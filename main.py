import sys, pygame
import random

from pygame.display import set_caption

pygame.init()
pygame.font.init()
pygame.display.init()

size = width, height = 1244, 800
blue = 50, 100, 200
green = 0, 100, 0
pink = 255, 100, 100
black = 0,0,0
yellow = (254, 253, 1)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Clicker z Questami')
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

dog = pygame.image.load("dogLevel2.gif")
dog_rect = dog.get_rect()
background = pygame.image.load("background_level_1.png")
bcgRect = background.get_rect()

credit = 0
def_inc = 1
my_font = pygame.font.SysFont(None, 30)
little_font = pygame.font.SysFont(None, 15)
smaller_font = pygame.font.SysFont(None, 25)
my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)





def mission(screen: pygame.Surface, credit: int):
    counting = 4  # 10
    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
    q_text = my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów za 1 klik myszką!', 1,
                            (255, 100, 100))
    font_20 = pygame.font.SysFont(None, 20)
    mission_description = font_20.render(f'Opis misji nr 1: klikaj na czas w nieruchomy obiekt, tak szybko aby pasek postępu nie spadł do 0!', 1, blue)

    side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
    progress = 0.52
    quest_started = False
    mission_passed = False
    click = False
    click_time = 0
    dog_rect.x = 40
    dog_rect.y = screen.get_height() - dog_rect.height - 80
    while 1:
        #dog_rect.x = 40
        #dog_rect.y = 100
        if quest_started:
            if progress > 0:
                progress -= 0.009  # 0.009
            else:
                return credit, mission_passed
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if dog_rect.x < x < dog_rect.x + dog_rect.width and dog_rect.y < y < dog_rect.y + dog_rect.height:
                    dog_rect.x += 10
                    dog_rect.y += 10
                    credit += def_inc
                    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                    click_text = my_font.render(f'+ {def_inc}', 1, blue)
                    click = True
                    click_time = 10
                    if counting >= 1:
                        counting -= 1
                        side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
                        if counting == 0:
                            quest_started = True
                    elif counting < 1 and progress < 1.0 and progress > 0.0:
                        side_text = my_font.render(f'Quest się zaczął', 1, (255, 100, 100))
                        progress += 0.1
                    else:
                        mission_passed = True
                    dog_rect.x -= 10
                    dog_rect.y -= 10

        if click_time > 0:
            click_time -= 1

        screen.fill(green)
        left = 500
        top = 40
        max_width = 400
        height = 20
        progress_temp = progress
        if progress_temp > 1.0:
            progress_temp = 1.0
        screen.blit(background, bcgRect)
        pygame.draw.rect(screen, pink, pygame.Rect(left, top, max_width * progress_temp, height))
        pygame.draw.rect(screen, blue, pygame.Rect(left, top, max_width, height), 1)
        if click and click_time > 0:
            screen.blit(click_text, (dog_rect.x + dog_rect.width + 10, dog_rect.y + (dog_rect.height / 2.0)))
        screen.blit(dog, dog_rect)
        #Rysowanie napisów
        pygame.draw.rect(screen, pink, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
        screen.blit(q_text, (500, 10))
        pygame.draw.rect(screen, blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
        screen.blit(my_text, (20, 10))
        pygame.draw.rect(screen, pink, pygame.Rect(15, 35, side_text.get_width() + 10, 30), 1)
        screen.blit(side_text, (20, 40))
        pygame.draw.rect(screen, blue, pygame.Rect(495, 70, mission_description.get_width() + 10, 30), 1)
        screen.blit(mission_description, (500, 74))
        pygame.display.flip()
        clock.tick(60)
        if mission_passed:
            return credit, mission_passed


def mission2(screen: pygame.Surface, credit: int, dog_upg_cost: int) -> (int,bool):
    counting = 4  # 10

    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
    q_text = my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów na sekundę!', 1,
                            (255, 100, 100))
    side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
    progress = 0.22
    quest_started = False
    mission_passed = False
    click = False
    click_time = 0
    if dog_upg_cost <= 5:
        dog = pygame.image.load("dog_level2_smaller.gif")
    elif dog_upg_cost ==55:
        dog = pygame.image.load("dog_2_smaller.gif")
    else:
        dog = pygame.image.load("dog_3_little.gif")
    dog_rect = dog.get_rect()
    dog_rect.x = 40
    dog_rect.y = 100
    while 1:


        if quest_started:
            if progress > 0:
                progress -= 0.0019  # 0.009
            else:
                return credit, mission_passed
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if dog_rect.x < x < dog_rect.x + dog_rect.width and dog_rect.y < y < dog_rect.y + dog_rect.height:
                    dog_rect.x += 10
                    dog_rect.y += 10
                    credit += def_inc
                    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                    click_text = my_font.render(f'+ {def_inc}', 1, blue)
                    click = True
                    click_time = 10
                    if counting >= 1:
                        counting -= 1
                        side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
                        if counting == 0:
                            quest_started = True
                    elif counting < 1 and progress < 1.0 and progress > 0.0:
                        side_text = my_font.render(f'Quest się zaczął', 1, (255, 100, 100))
                        progress += 0.1
                        dog_rect.x = random.randint(40, screen.get_width() - dog_rect.width)
                        dog_rect.y = random.randint(100, screen.get_height() - dog_rect.height)
                    else:
                        mission_passed = True
                    dog_rect.x -= 10
                    dog_rect.y -= 10

                if event.type == pygame.USEREVENT:
                    pass



        if click_time > 0:
            click_time -= 1

        screen.fill(green)
        left = 500
        top = 40
        max_width = 400
        height = 20
        progress_temp = progress
        if progress_temp > 1.0:
            progress_temp = 1.0
        screen.blit(background, bcgRect)
        pygame.draw.rect(screen, pink, pygame.Rect(left, top, max_width * progress_temp, height))
        pygame.draw.rect(screen, blue, pygame.Rect(left, top, max_width, height), 1)
        if click and click_time > 0:
            screen.blit(click_text, (dog_rect.x + dog_rect.width + 10, dog_rect.y + (dog_rect.height / 2.0)))
        screen.blit(dog, dog_rect)
        pygame.draw.rect(screen, pink, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
        screen.blit(q_text, (500, 10))
        pygame.draw.rect(screen, blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
        screen.blit(my_text, (20, 10))
        pygame.draw.rect(screen, pink, pygame.Rect(15, 35, side_text.get_width() + 10, 30), 1)
        screen.blit(side_text, (20, 40))
        pygame.display.flip()
        clock.tick(60)
        if mission_passed:
            return credit, mission_passed
    pass


def mission3()->None:
    pass


def draw_texts(points_on_click: int, points_per_second: int) -> None:
    font_19 = pygame.font.SysFont(None, 19)
    points_on_click_txt = font_19.render(f'Punkty od kliknięcia: +{points_on_click}', 1, blue)
    points_per_second_txt = font_19.render(f'Punkty na sekundę: +{points_per_second}',1,blue)

    pygame.draw.rect(screen, blue, pygame.Rect(15, 45, points_on_click_txt.get_width() + 10, 25), 1)
    screen.blit(points_on_click_txt, (20, 50))

    pygame.draw.rect(screen, blue, pygame.Rect(15, 70, points_on_click_txt.get_width() + 10, 21), 1)
    screen.blit(points_per_second_txt, (20, 72))
    pass


def shop_draw(pet_sit_cost: int, clicked: bool, increment_per_s: int) -> int:
    #pet_sit_cost = 10
    pet_sit_upgrade = 1
    if clicked:
        pet_sit_cost*=2
        increment_per_s+=pet_sit_upgrade
    #Rysowanie sklepu
    pet_sitter = pygame.image.load("pet_sitter.gif")
    pet_sit_rect=pet_sitter.get_rect()
    pet_sit_rect.x = 820
    pet_sit_rect.y = 110

    shop_text = my_font.render('Sklep z ulepszeniami', 1, pink)
    upg_title = my_font.render(f'Opiekun dla psa', 1, yellow)
    pet_sit_text = my_font.render(f'Koszt: {pet_sit_cost}', 1, yellow)
    pet_sit_text2 = little_font.render(f'Daje + {pet_sit_upgrade}/s dodatkowych punktów', 1, yellow)

    pygame.draw.rect(screen, pink, pygame.Rect(815, 105, screen.get_width() - 815, screen.get_height() - 145), 1)
    pygame.draw.rect(screen, pink, pygame.Rect(815, 70, screen.get_width() - 815, 30), 1)
    screen.blit(shop_text, (820, 75))
    screen.blit(pet_sitter, pet_sit_rect)
    screen.blit(upg_title, (pet_sit_rect.x+pet_sit_rect.width + 5, pet_sit_rect.y + 5))
    screen.blit(pet_sit_text, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 35))
    screen.blit(pet_sit_text2, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 65))

    return pet_sit_cost, increment_per_s


def draw_second_upgrade(click_upg_cost: int, clicked: bool, increment_on_click: int) -> int:
    # pet_sit_cost = 10
    click_upgrade = 1
    if clicked:
        click_upg_cost *= 2
        increment_on_click += click_upgrade
    # Rysowanie sklepu
    click_upgr_icon = pygame.image.load("on_click_upgrade.gif")
    click_upgr_rect = click_upgr_icon.get_rect()
    click_upgr_rect.x = 820
    click_upgr_rect.y = 246

    upg_title_2 = my_font.render(f'Karma pieska', 1, yellow)
    pet_sit_text = my_font.render(f'Koszt: {click_upg_cost}', 1, yellow)
    pet_sit_text2 = little_font.render(f'Daje + {click_upgrade} punktów na kliknięcie', 1, yellow)

    #pygame.draw.rect(screen, blue, pygame.Rect(815, 70, screen.get_width() - 815, 30), 1)
    screen.blit(click_upgr_icon, click_upgr_rect)
    screen.blit(upg_title_2, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 5))
    screen.blit(pet_sit_text, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 35))
    screen.blit(pet_sit_text2, (click_upgr_rect.x + click_upgr_rect.width + 5, click_upgr_rect.y + 65))

    return click_upg_cost, increment_on_click


def draw_third_upgrade(upg_cost_3: int, clicked: bool) -> int:
    # pet_sit_cost = 10
    click_upgrade = 1
    yellow = (254, 253, 1)
    if clicked and upg_cost_3 <105:
        upg_cost_3 +=50
        #increment_on_click += click_upgrade
    # Rysowanie sklepu
    dog_upgr_icon = pygame.image.load("dogs_shelter.gif")
    dog_upgr_rect = dog_upgr_icon.get_rect()
    dog_upgr_rect.x = 820
    dog_upgr_rect.y = 465


    upg_title_3 = my_font.render(f'Nowy piesek',1,yellow)
    if upg_cost_3 == 105:
        cost_txt = my_font.render(f'Maks. ulepszenie',1,pink)
    else:
        cost_txt = my_font.render(f'Koszt: {upg_cost_3}', 1, yellow)
    description_upgr = little_font.render(f'Nowy piesek i tło', 1, yellow)


    screen.blit(dog_upgr_icon, dog_upgr_rect)
    screen.blit(upg_title_3, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 5))
    #screen.blit(cost_txt, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 5))
    screen.blit(cost_txt, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 35))
    screen.blit(description_upgr, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 65))
    # screen.blit(description_upgr, (dog_upgr_rect.x + dog_upgr_rect.width + 5, dog_upgr_rect.y + 35))

    return upg_cost_3 #, increment_on_click


quest1_started = False
quest2_started = False
quest3_started = False
click = False
click_time = 0
#inicjalizacja zmiennych do sklepu
pet_sit_cost = 500 #500
click_upg_cost = 250 #250
dog_upg_cost = 5 #50
pet_sit_clicked = False
click_upg_clicked = False
dog_upg_clicked = False
inc_per_s = 0


mission_switch = 0
#Położenie początkowe pieska
dog_rect.x = 40
dog_rect.y = screen.get_height()-dog_rect.height-80

while 1:


    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if dog_rect.x < x < dog_rect.x + dog_rect.width and dog_rect.y < y < dog_rect.y + dog_rect.height:
                dog_rect.x += 10
                dog_rect.y += 10
                credit += def_inc
                my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                click_text = my_font.render(f'+ {def_inc}', 1, pink)
                click = True
                click_time = 10
                dog_rect.x -= 10
                dog_rect.y -= 10
            elif 820 <= x <= 1034 and 110 <= y <= 241 and credit >= pet_sit_cost:
                credit -= pet_sit_cost
                my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                pet_sit_clicked = True
            elif 820 <=x <= 1034 and 246 <= y <= 460 and credit >= click_upg_cost:
                credit -= click_upg_cost
                my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                click_upg_clicked = True
            elif 820 <=x <= 1034 and 465 <= y <= 679 and credit >= dog_upg_cost and dog_upg_cost <=55:
                credit -= dog_upg_cost
                my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                dog_upg_clicked = True
        if event.type == pygame.USEREVENT:
            credit += inc_per_s
            my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
            mission_switch = random.randint(1,75)   #(1,75)
            #mission_switch = 2
            print(mission_switch)
    #rozpoczęcie misji nr 1
    # if credit == 5:
    if mission_switch == 1: #credit == 40 and quest1_started == False:
        quest1_started = True
        credit, mission_passed = mission(screen, credit)
        my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
        q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)
        if mission_passed:
            m1_text = smaller_font.render('Przeszedles pierwsza misje i twoje kliknięcia są teraz warte o 1 punkt więcej', 1,
                                     blue)
            def_inc += 1
        else:
            m1_text = my_font.render('Przegrałeś pierwszą misję', 1, blue)
        #dog = pygame.image.load("dog3.gif")
        #dog_rect = dog.get_rect()
        mission_switch=0

    #rozpoczęcie misji nr 2
    if mission_switch ==2 :
        quest2_started = True
        credit, mission2_passed = mission2(screen, credit, dog_upg_cost)
        my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
        q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)
        if mission2_passed:
            m1_text = smaller_font.render('Przeszedles drugą misje i teraz masz +1 punkt na sekundę', 1,
                                     blue)
            inc_per_s += 1
        else:
            m1_text = my_font.render('Przegrałeś drugą misję', 1, blue)
        #Załadowanie z powrotem pieska pierwotnej wielkosci
        if dog_upg_cost <= 5:
            dog = pygame.image.load("dogLevel2.gif")
        elif dog_upg_cost ==55:
            dog = pygame.image.load("dog_2.gif")
        else:
            dog = pygame.image.load("dog_3.gif")
        dog_rect = dog.get_rect()
        dog_rect.x = 40
        dog_rect.y = screen.get_height() - dog_rect.height - 80

        mission_switch = 0

        # rozpoczęcie misji nr 3
        # if credit == 300 and quest3_started == False:
        #     quest3_started = True
        #     credit, mission3_passed = mission3(screen, credit)
        #     my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
        #     q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)
        #     if mission2_passed:
        #         m1_text = smaller_font.render('Przeszedles drugą misje i teraz masz +1 punkt na sekundę', 1,
        #                                       blue)
        #         inc_per_s += 1
        #     else:
        #         m1_text = my_font.render('Przegrałeś drugą misję', 1, blue)
        #     dog = pygame.image.load("dogLevel2.gif")
        #     dog_rect = dog.get_rect()
    if click_time > 0:
        click_time -= 1






    screen.blit(background, bcgRect)
    screen.blit(dog, dog_rect)

    pet_sit_cost, inc_per_s = shop_draw(pet_sit_cost,pet_sit_clicked, inc_per_s)
    pet_sit_clicked = False

    click_upg_cost, def_inc = draw_second_upgrade(click_upg_cost,click_upg_clicked,def_inc)
    click_upg_clicked = False

    dog_upg_cost = draw_third_upgrade(dog_upg_cost, dog_upg_clicked)
    if dog_upg_clicked:
        if dog_upg_cost == 55:
            background = pygame.image.load("background_level_2.gif")
            dog = pygame.image.load("dog_2.gif")
        elif dog_upg_cost == 105:
            background = pygame.image.load("background_3.gif")
            dog = pygame.image.load("dog_3.gif")
        bcgRect = background.get_rect()
        dog_rect = dog.get_rect()
        dog_rect.x = 40
        dog_rect.y = screen.get_height() - dog_rect.height - 80
    dog_upg_clicked = False

    draw_texts(def_inc, inc_per_s)

    pygame.draw.rect(screen, blue, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
    screen.blit(q_text, (500, 10))
    #napis o stanie po misji:
    if quest1_started or quest2_started:
        pygame.draw.rect(screen, blue, pygame.Rect(495, 35, m1_text.get_width() + 10, 30), 1)
        screen.blit(m1_text, (500, 40))
    if click and click_time > 0:
        screen.blit(click_text, (dog_rect.x + dog_rect.width + 10, dog_rect.y + (dog_rect.height / 2.0)))
    pygame.draw.rect(screen, blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
    screen.blit(my_text, (20, 10))
    pygame.display.flip()
    clock.tick(60)
