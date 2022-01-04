import sys, pygame
import random

pygame.init()
pygame.font.init()
pygame.display.init()

size = width, height = 1244, 800
blue = 50, 100, 200
green = 0, 100, 0

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
my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)


def mission(screen: pygame.Surface, credit: int):
    counting = 4 #10
    my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
    q_text = my_font.render(f'Masz nowy quest, ukończ go aby uzyskać więcej punktów za 1 klik myszką!', 1, (255, 100, 100))
    side_text = my_font.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
    progress = 0.52
    quest_started = False
    mission_passed = False

    while 1:
        dog_rect.x = 40
        dog_rect.y = 100
        if quest_started:
            if progress > 0:
                progress -= 0.009#0.001
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

        screen.fill(green)
        left = 500
        top = 40
        max_width = 400
        height = 20
        progress_temp = progress
        if progress_temp > 1.0:
            progress_temp = 1.0
        screen.blit(background, bcgRect)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(left, top, max_width * progress_temp, height))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(left, top, max_width, height), 1)
        screen.blit(dog, dog_rect)
        screen.blit(q_text, (500, 10))
        screen.blit(my_text, (20, 10))
        screen.blit(side_text, (20, 30 ))
        pygame.display.flip()
        clock.tick(60)
        if mission_passed:
            return credit, mission_passed


quest1_started = False
click = False
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

    if credit == 5:
        quest1_started = True
        credit, mission_passed = mission(screen, credit)
        my_text = my_font.render(f'Twoje zebrane punkty: {credit}', 1, blue)
        q_text = my_font.render(f'Brak aktywnej misji :(', 1, blue)
        if mission_passed:
            m1_text = my_font.render('Przeszedles pierwsza misje i twoje kliknięcia są teraz warte o 1 punkt więcej', 1, blue)
            def_inc += 1
        else:
            m1_text = my_font.render('Przegrałeś pierwszą misję', 1, blue)
        dog = pygame.image.load("dog3.gif")
        dog_rect = dog.get_rect()

    screen.blit(background, bcgRect)
    screen.blit(dog, dog_rect)
    screen.blit(q_text, (500, 10))
    if quest1_started:
        screen.blit(m1_text, (500, 30))
    if click:
        screen.blit(click_text, (dog_rect.x+dog_rect.width + 10, dog_rect.y+(dog_rect.height/2.0)))
    screen.blit(my_text, (20, 10))
    pygame.display.flip()
    clock.tick(60)


