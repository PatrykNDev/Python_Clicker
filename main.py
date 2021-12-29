import sys, pygame
import random

pygame.init()
pygame.font.init()
pygame.display.init()

size = width, height = 1320, 780
black = 0, 0, 0
green = 0, 100, 0

screen = pygame.display.set_mode(size)
print(type(screen))

dog = pygame.image.load("dogLevel2.gif")
dogrect = dog.get_rect()

licznikPetliGlownej = 0
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
    progress = 0.52
    questStarted = False
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        dogrect.x = 40
        dogrect.y = 100

        event = pygame.event.wait()
        x, y = pygame.mouse.get_pos()
        if questStarted == True:
            progress -= 0.02
        if event.type == pygame.MOUSEBUTTONDOWN and dogrect.x < x < dogrect.x + dogrect.width and dogrect.y < y < dogrect.y + dogrect.height:
            dogrect.x += 10
            dogrect.y += 10
            credit += definc
            mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)
            if counting >=1:
                counting -= 1
                sidetext = myfont.render(f'Quest zacznie się za: {counting} ', 1, (255, 100, 100))
                if counting == 0:
                    questStarted = True
            elif counting < 1 and progress < 1.0 and progress > 0.0:
                sidetext = myfont.render(f'Quest się zaczął', 1, (255, 100, 100))
                progress += 0.1

                #counting -= 1
            else:
                return credit


        screen.fill(green)
        left = 500
        top = 40
        maxwidth = 400
        height = 20
        progressTemp = progress
        if progressTemp > 1.0:
            progressTemp = 1.0
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(left, top, maxwidth * progressTemp, height))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(left, top, maxwidth, height), 1)
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

    x = random.randint(1,100)

    event = pygame.event.wait()
    x,y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and dogrect.x < x < dogrect.x + dogrect.width and dogrect.y < y <dogrect.y + dogrect.height:
        dogrect.x += 10
        dogrect.y += 10
        credit+=definc
        mytext = myfont.render(f'Twoje zebrane punkty: {credit}', 1, black)

    if credit == 2:
        qtext = myfont.render(f'Masz nowy quest, ukończ go aby uzyskać nagrodę!', 1, (255,100,100))
        credit = mission(screen, credit)
        qtext = myfont.render(f'Brak aktywnej misji :(', 1, black)
        dog = pygame.image.load("dog3.gif")
        definc +=1

    licznikPetliGlownej+=1

    screen.fill(green)
    screen.blit(dog, dogrect)
    screen.blit(qtext, (500, 10))
    screen.blit(mytext, (20,10))
    pygame.display.flip()


