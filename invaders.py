# Name:                 Jamie O'Donovan
# Student Number:       121776739

import sys, pygame as pyg

class MyGame(object):
    def __init__(self):
        pyg.init()

        self._size = self._width, self._height = 800, 600
        self._background = 80, 80, 80
        self._score = 0
        pyg.display.set_caption(f"Score: {self._score}")
        self._myFont = pyg.font.SysFont("monospace", 16)
        self._WHITE = (255,255,255)

        self._screen = pyg.display.set_mode(self._size)

        self._playerView = pyg.image.load("player.png")
        self._playerModel = Player(self._width/2 - 16, self._height - 64, self._width - 16, 15)

        # invader list should be implemented as matrix and not just a long list, fix later?
        self._invaderList = []
        self._missileList = []

        i = 0
        x = 32
        y = 0
        for i in range(10):
            if i % 5 == 0:
                y += 64
                x = 32
            invader = Invader(x, y, self._width - 16, 0.05)
            self._invaderList.append(invader)
            i += 1
            x += 64

    def rungame(self):
        while True:
            for event in pyg.event.get():
                if event.type == pyg.QUIT: 
                    sys.exit()

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                        self._playerModel.handleMoveLeft()

                    if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                        self._playerModel.handleMoveRight()

                    if event.key == pyg.K_SPACE:
                        missile = Missile(self._playerModel.x + 12, self._playerModel.y)
                        self._missileList.append(missile)

                if event.type == pyg.KEYUP:
                    self._playerModel.handleStopMove()

            self._screen.fill(self._background)
            self._screen.blit(self._playerView, (self._playerModel.x, self._playerModel.y))
            scoreText = self._myFont.render("Score {0}".format(self._score), 1, (0,0,0))
            self._screen.blit(scoreText, (5, 10))

            i = 0
            while i < len(self._invaderList):
                self._invaderList[i].moveInvader()
                self._screen.blit(self._invaderList[i].icon, (self._invaderList[i].x, self._invaderList[i].y))
                i += 1

            if len(self._invaderList) != 0:
                if self._invaderList[len(self._invaderList) - 1].x > self._width - 32:
                    for i in range(len(self._invaderList)):
                        self._invaderList[i]._change = -0.05
                        self._invaderList[i]._yPos += self._invaderList[i]._height * 2

                if self._invaderList[0].x < 0:
                    for i in range(len(self._invaderList)):
                        self._invaderList[i]._change = 0.05
                        self._invaderList[i]._yPos += self._invaderList[i]._height * 2

                if self._invaderList[0].y > self._height - self._invaderList[0].height:
                    sys.exit()

            for i in range(len(self._invaderList)):
                if self._playerModel.collisionCheck(self._invaderList[i].x, self._invaderList[i].y):
                    sys.exit()

            i = 0
            while i < len(self._missileList):
                self._missileList[i].moveMissile()
                self._screen.blit(self._missileList[i].icon, (self._missileList[i].x, self._missileList[i].y))

                for j in range(len(self._invaderList)):
                    if self._missileList[i].collisionCheck(self._invaderList[j].x, self._invaderList[j].y):
                        del self._invaderList[j]
                        del self._missileList[i]
                        self._score += 5 
                        break

                i += 1

            pyg.display.flip()

class Missile(object):
    def __init__(self, x, y):
        self._xPos = x
        self._yPos = y
        self._icon = pyg.image.load("missile.png")
        self._change = 0.4

    def collisionCheck(self, invaderX, invaderY):
        if self._xPos < invaderX + 32 and self._xPos + 12 > invaderX and self._yPos < invaderY + 32 and 24 + self._yPos > invaderY:
            return True
        else:
            return False

    def getXPos(self):
        return self._xPos

    def getYPos(self):
        return self._yPos

    def moveMissile(self):
            self._yPos -= self._change

    def getIcon(self):
        return self._icon

    x = property(getXPos)
    y = property(getYPos)
    icon = property(getIcon)
class Invader(object):
    def __init__(self, x, y, maxX, change):
        self._xPos = x
        self._yPos = y
        self._maxX = maxX
        self._icon = pyg.image.load("invader.png")
        self._change = change
        self._size = self._width, self._height = 32, 32

    def getXPos(self):
        return self._xPos

    def getYPos(self):
        return self._yPos

    def moveInvader(self):
            self._xPos += self._change

    def getIcon(self):
        return self._icon

    def getHeight(self):
        return self._height

    x = property(getXPos)
    y = property(getYPos)
    icon = property(getIcon)
    height = property(getHeight)
class Player(object):
    def __init__(self, x, y, maxX, change):
        self._xPos = x
        self._yPos = y
        self._maxX = maxX
        self._change = change

    def collisionCheck(self, invaderX, invaderY):
        if self._xPos < invaderX + 32 and self._xPos + 12 > invaderX and self._yPos < invaderY + 32 and 24 + self._yPos > invaderY:
            return True
        else:
            return False

    def getXPos(self):
        return self._xPos

    def getYPos(self):
        return self._yPos

    def handleMoveRight(self):
        if self._xPos + self._change < self._maxX:
            self._xPos += self._change

    def handleMoveLeft(self):
        if self._xPos - self._change > 0:
            self._xPos -= self._change

    def handleStopMove(self):
        self._xPos = self._xPos

    x = property(getXPos)
    y = property(getYPos)

if __name__ == "__main__":
    mygame = MyGame()
    mygame.rungame()