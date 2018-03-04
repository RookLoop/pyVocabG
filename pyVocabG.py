import pygame, sys, random, pickle
import dbm.dumb
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((960, 768))

mainCLock = pygame.time.Clock()

pygame.display.set_caption('pyVocab')
TITLE = "pyVocab"

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (0,0,0)

MAINMENUTOPOFFSET = 30
QUESTIONTOPOFFSET = 60

ANSWER1LEFTOFFSET = 40
ANSWER1TOPOFFSET = 200

ANSWER2LEFTTOFFSET = 510
ANSWER2TOPOFFSET = 200

ANSWER3LEFTOFFSET = 40
ANSWER3TOPOFFSET = 350

ANSWER4LEFTOFFSET = 510
ANSWER4TOPOFFSET = 350

fancyFont = pygame.font.Font('whitrabt.ttf',70)
basicFont = pygame.font.Font('whitrabt.ttf', 28)

# uncomment to add music
#pygame.mixer.music.load('safari.mp3')
#pygame.mixer.music.play(-1,0.0)

# load our image objects
background = pygame.image.load('codeart.jpg')
backgroundRect = background.get_rect()

mainmenu = pygame.image.load('mainmenu.png')
mainmenuRect = mainmenu.get_rect()

bottomMenuImage = pygame.image.load('bottommenu.png')
bottomMenuImageRect = bottomMenuImage.get_rect()

mainmenuRect.midtop = backgroundRect.midtop


bottomMenuImageRect.midbottom = backgroundRect.midbottom
bottomMenuImageRect.bottom = bottomMenuImageRect.bottom - 10



# global variables
mousex = 0
mousey = 0

def stringwrap(string, wrapnear,position):
    lofstring = len(string)

    accumlen = 0

    if lofstring > wrapnear:
        splitstring = string.split(" ")
        for index in range(len(splitstring)):
            accumlen += (len(splitstring[index])) + 1
            if accumlen > wrapnear:

                firstlist = splitstring[:index]
                firststring = " ".join(firstlist)
                del splitstring[:index]
                secondstring = " ".join(splitstring)

                textobject = basicFont.render(firststring,True,WHITE)
                textRect = textobject.get_rect()
                textRect.midtop = mainmenuRect.midtop
                textRect.top = textRect.top + (29 * position)
                DISPLAYSURF.blit(textobject,textRect)

                stringwrap(secondstring,wrapnear,(position + 1))
                return


    textobject = basicFont.render(string,True,WHITE)
    textRect = textobject.get_rect()
    textRect.midtop = mainmenuRect.midtop
    textRect.top = textRect.top + (29 * position)
    DISPLAYSURF.blit(textobject,textRect)



def getDict(dictionary):
    database = dbm.open('dbDicts','r')
    unpicklethisstring = database[dictionary]
    return pickle.loads(unpicklethisstring)

def splashscreen():
    global mousex, mousey
    mouseClicked = False
    mouseOverPlayTitle = False
    mouseOverClickToPlay = False
    splash = True
    while splash:
        DISPLAYSURF.blit(background,(0,0))
        titleTextObject = fancyFont.render(TITLE,True,WHITE)
        titleRect = titleTextObject.get_rect()
        titleRect.midtop = backgroundRect.midtop
        titleRect.bottom = titleRect.bottom + 1
        DISPLAYSURF.blit(titleTextObject,titleRect)
        clickToPlay = fancyFont.render("Click to Play",True,WHITE)
        clickToPlayRect = clickToPlay.get_rect()
        clickToPlayRect.midtop = titleRect.midbottom
        DISPLAYSURF.blit(clickToPlay,clickToPlayRect)


        mouseOverPlayTitle = isMouseOverRect(titleRect)
        mouseOverClickToPlay = isMouseOverRect(clickToPlayRect)

        if mouseClicked:
            if mouseOverPlayTitle or mouseOverClickToPlay:
                return
            mouseClicked = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

def displayQuestion(displayquestion):

    question = basicFont.render(displayquestion, True, WHITE,)
    questionRect = question.get_rect()
    questionRect.midtop = mainmenuRect.midtop
    questionRect.top = QUESTIONTOPOFFSET
    DISPLAYSURF.blit(question,questionRect)

def displayanswer(answer,answernumberindex,ismouseover):
    possibleAnswer = answer

    if ismouseover:
        questionHighlight = BLACK
    else:
        questionHighlight = None

    if answernumberindex == 0:
        xoffset = ANSWER1LEFTOFFSET
        yoffset = ANSWER1TOPOFFSET
    elif answernumberindex == 1:
        xoffset =  ANSWER2LEFTTOFFSET
        yoffset = ANSWER2TOPOFFSET
    elif answernumberindex == 2:
        xoffset = ANSWER3LEFTOFFSET
        yoffset = ANSWER3TOPOFFSET
    elif answernumberindex == 3:
        xoffset = ANSWER4LEFTOFFSET
        yoffset = ANSWER4TOPOFFSET

    answerxtxtObj = basicFont.render(answer,True,WHITE,questionHighlight)
    answerxRect = answerxtxtObj.get_rect()
    answerxRect.left = (mainmenuRect.left + xoffset)
    answerxRect.top = (mainmenuRect.top + yoffset)
    DISPLAYSURF.blit(answerxtxtObj,answerxRect)

    return (answerxRect, possibleAnswer)





def isMouseOverRect(rect):

    if rect.left < mousex < rect.right and \
    rect.top < mousey < rect.bottom:
        return True

def getallpossibleanswers(question1):
    correctanwser = dictionary1[question1][0]
    wronganswer1, notused = random.choice(list(dictionary1.values()))
    wronganswer2, notused = random.choice(list(dictionary1.values()))
    wronganswer3, notused = random.choice(list(dictionary1.values()))

    while wronganswer1 == wronganswer2 or wronganswer1 == wronganswer3 or wronganswer1 == correctanwser:
        wronganswer1, notused = random.choice(list(dictionary1.values()))
    while wronganswer2 == wronganswer1 or wronganswer2 == wronganswer3 or wronganswer2 == correctanwser:
        wronganswer2, notused = random.choice(list(dictionary1.values()))
    while wronganswer3 == wronganswer1 or wronganswer3 == wronganswer2 or wronganswer1 == correctanwser:
        wronganswer3, notused = random.choice(list(dictionary1.values()))

    return [correctanwser,wronganswer1,wronganswer2,wronganswer3]

def showscore(score):
    scorestring = "Score: " + str(score) + "/" + str(questionsattempted)
    roundCount = "Question " + str(questionsattempted + 1)  + "/" + str(ROUNDLIMIT)
    scoreTextObject = basicFont.render(scorestring,True,YELLOW)
    scoreTextRect = scoreTextObject.get_rect()
    scoreTextRect.midleft = bottomMenuImageRect.midleft
    scoreTextRect.left = scoreTextRect.left + 10
    DISPLAYSURF.blit(scoreTextObject,scoreTextRect)
    roundTextObject = basicFont.render(roundCount,True,YELLOW)
    roundRect = roundTextObject.get_rect()
    roundRect.midright = bottomMenuImageRect.midright
    roundRect.right = roundRect.right - 10
    DISPLAYSURF.blit(roundTextObject,roundRect)

def questionloop(score):
    global mousex
    global mousey

    mouseClicked = False
    delayafterdraw = False


    mouseOverRect1 = False
    mouseOverRect2 = False
    mouseOverRect3 = False
    mouseOverRect4 = False

    question1 = random.choice(list(dictionary1))
    while dictionary1[question1][1]:
        question1 = random.choice(list(dictionary1))



    possibleanswerlist = getallpossibleanswers(question1)
    correctanswer = possibleanswerlist[0]
    random.shuffle(possibleanswerlist)
    for answerindex in range(len(possibleanswerlist)):
        if possibleanswerlist[answerindex] == correctanswer:
            break



    playerInputIndex = None
    scorePoints = 0

    cycle = True
    while cycle:



        DISPLAYSURF.blit(background,(0,0))
        DISPLAYSURF.blit(mainmenu,mainmenuRect.topleft)
        DISPLAYSURF.blit(bottomMenuImage,bottomMenuImageRect)
        showscore(score)




        stringwrap(question1,40,1)
        rec1PA = displayanswer(possibleanswerlist[0],0,mouseOverRect1)
        rec2PA = displayanswer(possibleanswerlist[1],1,mouseOverRect2)
        rec3PA = displayanswer(possibleanswerlist[2],2,mouseOverRect3)
        rec4PA = displayanswer(possibleanswerlist[3],3,mouseOverRect4)

        mouseOverRect1 = isMouseOverRect(rec1PA[0])
        mouseOverRect2 = isMouseOverRect(rec2PA[0])
        mouseOverRect3 = isMouseOverRect(rec3PA[0])
        mouseOverRect4 = isMouseOverRect(rec4PA[0])


        if mouseClicked:
            if mouseOverRect1:
                playerInputIndex = 0
            elif mouseOverRect2:
                playerInputIndex = 1
            elif mouseOverRect3:
                playerInputIndex = 2
            elif mouseOverRect4:
                playerInputIndex = 3
            mouseClicked = False

        if playerInputIndex != None:
            if playerInputIndex == answerindex:
                dictionary1[question1][1] = True

                correctTxtObject = fancyFont.render("Correct!!!",True,YELLOW)
                correctTxtRect = correctTxtObject.get_rect()
                correctTxtRect.center = mainmenuRect.center
                DISPLAYSURF.blit(correctTxtObject,correctTxtRect)
                delayafterdraw = True
                cycle = False
                score += 1
            else:
                wrongTxtObject = fancyFont.render("Wrong",True,RED)
                wrongTxtRect = wrongTxtObject.get_rect()
                wrongTxtRect.center = mainmenuRect.center
                DISPLAYSURF.blit(wrongTxtObject,wrongTxtRect)
                delayafterdraw = True
                cycle = False





        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

        pygame.display.update()
        if delayafterdraw:
            pygame.time.delay(1000)
            delayafterdraw = False

    return score

dictionary1 = getDict("masterdict")
ROUNDLIMIT = 10
questionsattempted = 0
scorePoints = 0
isMouseOverPlayAgain = False
mouseClicked = False
firsttime = True
while True:
    DISPLAYSURF.blit(background,(0,0))
    if firsttime:
        splashscreen()
        firsttime = False


    if questionsattempted < ROUNDLIMIT:
        scorePoints = questionloop(scorePoints)
        questionsattempted +=1

    if questionsattempted >= ROUNDLIMIT:
        # display play again box, if clicked reset scorePoints and questions attemped
        percentScore = scorePoints / ROUNDLIMIT * 100
        percentString = format(percentScore,'.0f') + "%"
        print(percentString)
        playagainTxtObject = fancyFont.render("Game Over. Play again?",True,WHITE)
        playagainTxtRect = playagainTxtObject.get_rect()
        playagainTxtRect.center = mainmenuRect.center
        DISPLAYSURF.blit(playagainTxtObject,playagainTxtRect)
        scoreTxtObject = fancyFont.render(percentString,True,YELLOW)
        scoreTxtRect = scoreTxtObject.get_rect()
        scoreTxtRect.midbottom = playagainTxtRect.midtop
        DISPLAYSURF.blit(scoreTxtObject,scoreTxtRect)


        isMouseOverPlayAgain = isMouseOverRect(playagainTxtRect)
    if mouseClicked:
        if isMouseOverPlayAgain:
            scorePoints = 0
            questionsattempted = 0
        mouseClicked = False


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

    pygame.display.update()
    mainCLock.tick(30)