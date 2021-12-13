import sys, pygame

from pygame.key import get_pressed
from pygame.locals import *
pygame.init()
pygame.font.init()

size = width, height = 1520, 980
black = 0, 0, 0
green = 0, 100, 0

screen = pygame.display.set_mode(size)
print(type(screen))

dog = pygame.image.load("dog.png")
dogrect = dog.get_rect()

credit = 0
definc = 1
myfont = pygame.font.SysFont(None, 30)
mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)
qtext = myfont.render(f'Brak aktywnej misji :(', 1, black)


def mission(screen: pygame.Surface, credit: int):
    counting = 10
    mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)
    qtext = myfont.render(f'Masz nowy quest, ukończ go aby uzyskać nagrodę!', 1, (255, 100, 100))
    sidetext = myfont.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        dogrect.x = 40
        dogrect.y = 100

        event = pygame.event.wait()
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and dogrect.x < x < dogrect.x + dogrect.width and dogrect.y < y < dogrect.y + dogrect.height:
            dogrect.x += 10
            dogrect.y += 10
            credit += definc
            mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)
            if counting >=1:
                counting -= 1
                sidetext = myfont.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
            else:
                sidetext = myfont.render(f'Quest się zaczął', 1, (255, 100, 100))

        screen.fill(green)
        screen.blit(dog, dogrect)
        screen.blit(qtext, (500, 10))
        screen.blit(mytext, (20, 10))
        screen.blit(sidetext, (20, 30 ))
        pygame.display.flip()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    dogrect.x = 40
    dogrect.y = 100

    event = pygame.event.wait()
    x,y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and dogrect.x < x < dogrect.x + dogrect.width and dogrect.y < y <dogrect.y + dogrect.height:
        dogrect.x += 10
        dogrect.y += 10
        credit+=definc
        mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)

    if credit % 5 == 4:
        qtext = myfont.render(f'Masz nowy quest, ukończ go aby uzyskać nagrodę!', 1, (255,100,100))
        mission(screen, credit)

    screen.fill(green)
    screen.blit(dog, dogrect)
    screen.blit(qtext, (500, 10))
    screen.blit(mytext, (20,10))
    pygame.display.flip()


