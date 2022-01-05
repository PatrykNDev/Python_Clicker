import sys, pygame
import random

pygame.init()
pygame.font.init()
pygame.display.init()

size = width, height = 1244, 800
blue = 50, 100, 200
green = 0, 100, 0
pink = 255, 100, 100
black = 0,0,0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

dog = pygame.image.load("dogLevel2.gif")
dog_rect = dog.get_rect()
background = pygame.image.load("aurora-02.gif")
bcgRect = background.get_rect()

credit = 0
def_inc = 1
my_font = pygame.font.SysFont(None, 30)
little_font = pygame.font.SysFont(None, 15)
my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)


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
    pet_sit_rect.y = 80

    shop_text = my_font.render('Sklep z ulepszeniami', 1, pink)
    pet_sit_text = my_font.render(f'Koszt: {pet_sit_cost}', 1, blue)
    pet_sit_text2 = little_font.render(f'Daje + {pet_sit_upgrade}/s dodatkowych punktów', 1, blue)

    pygame.draw.rect(screen, blue, pygame.Rect(815, 75, screen.get_width() - 815, screen.get_height() - 145), 1)
    pygame.draw.rect(screen, blue, pygame.Rect(815, 40, screen.get_width() - 815, 30), 1)
    screen.blit(shop_text, (820, 45))
    screen.blit(pet_sitter, pet_sit_rect)
    screen.blit(pet_sit_text, (pet_sit_rect.x+pet_sit_rect.width + 5, pet_sit_rect.y + 5))
    screen.blit(pet_sit_text2, (pet_sit_rect.x + pet_sit_rect.width + 5, pet_sit_rect.y + 35))
    return pet_sit_cost, increment_per_s


def mission(screen: pygame.Surface, credit: int):
    counting = 4  # 10
    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
    q_text = my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów za 1 klik myszką!', 1,
                            (255, 100, 100))
    side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
    progress = 0.52
    quest_started = False
    mission_passed = False
    click = False
    click_time = 0

    while 1:
        dog_rect.x = 40
        dog_rect.y = 100
        if quest_started:
            if progress > 0:
                progress -= 0.009  # 0.001
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


quest1_started = False
click = False
click_time = 0
pet_sit_cost = 10
pet_sit_clicked = False
inc_per_s = 0
while 1:

    dog_rect.x = 40
    dog_rect.y = 100
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
            elif 820 <= x <= 1034 and 80 <= y <= 211 and credit >= pet_sit_cost:
                credit -= pet_sit_cost
                my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
                pet_sit_clicked = True
    # if credit == 5:
    if credit == 5 and quest1_started == False:
        quest1_started = True
        credit, mission_passed = mission(screen, credit)
        my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
        q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)
        if mission_passed:
            m1_text = my_font.render('Przeszedles pierwsza misje i twoje kliknięcia są teraz warte o 1 punkt więcej', 1,
                                     blue)
            def_inc += 1
        else:
            m1_text = my_font.render('Przegrałeś pierwszą misję', 1, blue)
        dog = pygame.image.load("dog3.gif")
        dog_rect = dog.get_rect()
    if click_time > 0:
        click_time -= 1

    credit+=inc_per_s
    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)

    screen.blit(background, bcgRect)
    screen.blit(dog, dog_rect)

    pet_sit_cost, inc_per_s = shop_draw(pet_sit_cost,pet_sit_clicked, inc_per_s)
    pet_sit_clicked = False

    pygame.draw.rect(screen, blue, pygame.Rect(495, 5, q_text.get_width() + 10, 30), 1)
    screen.blit(q_text, (500, 10))
    if quest1_started:
        pygame.draw.rect(screen, blue, pygame.Rect(495, 35, m1_text.get_width() + 10, 30), 1)
        screen.blit(m1_text, (500, 40))
    if click and click_time > 0:
        screen.blit(click_text, (dog_rect.x + dog_rect.width + 10, dog_rect.y + (dog_rect.height / 2.0)))
    pygame.draw.rect(screen, blue, pygame.Rect(15, 5, my_text.get_width() + 10, 30), 1)
    screen.blit(my_text, (20, 10))
    pygame.display.flip()
    clock.tick(60)
