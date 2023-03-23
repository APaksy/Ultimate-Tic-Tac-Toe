import pygame

class Box:

    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple, rounding: int = 0, visible=True):
        self.pos = pygame.math.Vector2(x, y)
        self.dimensions = pygame.math.Vector2(width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.rounding = rounding
        self.visible = visible

    def get_centre(self):
        return (self.pos.x + (self.dimensions.x / 2), self.pos.y + (self.dimensions.y / 2))
    
    def pos_is_in(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def display(self, screen):
        if not self.visible:
            return
        pygame.draw.rect(screen, self.colour, self.rect, 0, self.rounding)

class Text:

    def __init__(self, x:int, y:int, text:str, textColour:tuple, fontSize:float, anchor='tl', maxWidth=0):
        self.pos = pygame.math.Vector2(x, y)
        self.text = text
        self.textColour = textColour
        self.fontSize = fontSize
        self.anchor = anchor
        self.maxWidth = maxWidth
        self.textObj = self.get_text()
        self.rect = self.get_rect()
        self.fit_text()

    def get_text(self):
        font = pygame.font.Font('_Roboto-Bold.ttf', self.fontSize)
        textObj = font.render(self.text, True, self.textColour)
        return textObj

    def get_rect(self):
        textRect = self.textObj.get_rect()
        anchorOffsets = {
            'tl' : (0, 0),
            'l' : (0, textRect.height / 2),
            'bl' : (0, textRect.height),
            'tc' : (textRect.width / 2, 0),
            'c' : (textRect.width / 2, textRect.height / 2),
            'bc' : (textRect.width / 2, textRect.height),
            'tr' : (textRect.width, 0),
            'r' : (textRect.width, textRect.height / 2),
            'br' : (textRect.width, textRect.height)
        }
        offset = anchorOffsets[self.anchor]
        textRect.topleft = (self.pos.x - offset[0], self.pos.y - offset[1])
        return textRect

    def fit_text(self):
        if self.maxWidth == 0:
            return
        while self.rect.width >= self.maxWidth:
            self.fontSize-=1
            self.textObj = self.get_text()
            self.rect = self.get_rect()

    def set_text(self, text):
        self.text = text
        self.textObj = self.get_text()
        self.rect = self.get_rect()
        self.fit_text() 

    def set_pos(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.textObj = self.get_text()
        self.rect = self.get_rect()

    def display(self, screen):
        screen.blit(self.textObj, self.rect)

class Button(Box):

    def __init__(self, x, y, width, height, colour, text, textColour, fontSize, function, enabled=True, maxWidth=0):
        super().__init__(x, y, width, height, colour, rounding=20)
        self.text = Text(self.get_centre()[0], self.get_centre()[1], text, textColour, fontSize, 'c', maxWidth=maxWidth)
        self.function = function
        self.enabled = enabled

    def check_press(self, mousePos):
        if not self.enabled:
            return False
        return self.rect.collidepoint(mousePos)
    
    def set_enabled(self, enabled):
        self.enabled = enabled

    def update_text(self, text):
        self.text.set_text(text)

    def display(self, screen):
        if not self.enabled:
            return
        super().display(screen)
        self.text.display(screen)

class MainBoard_UI:

    def __init__(self, x, y, size, board):
        self.board = board
        self.lines = []
        self.text = []
        lineColour = (60, 60, 60)
        lineWidth = int(size * 0.03)
        tileWidth = int((size * 0.94)/3)
        for i in range(3):
            for j in range(3):
                posX = x + j*(tileWidth + lineWidth) + 0.5*tileWidth
                posY = y + i*(tileWidth + lineWidth) + 0.5*tileWidth
                self.text.append(Text(posX, posY, '', (4, 78, 174), 250, 'c'))
        self.lines.append(Box(x+2*tileWidth+lineWidth, y, lineWidth, size, lineColour, rounding=4))
        self.lines.append(Box(x, y+tileWidth, size, lineWidth, lineColour, rounding=4))
        self.lines.append(Box(x, y+2*tileWidth+lineWidth, size, lineWidth, lineColour, rounding=4))
        self.lines.append(Box(x+tileWidth, y, lineWidth, size, lineColour, rounding=4))

    def update_tiles(self):
        playerCharDict = {-1 : 'O', 0 : '', 1 : 'X', 2 : ''}
        for i, player in enumerate(self.board.get_board()):
            self.text[i].set_text(playerCharDict[player])

    def display(self, screen):
        self.update_tiles()
        for line in self.lines:
            line.display(screen)
        for text in self.text:
            text.display(screen)
        
class Board_UI:

    def __init__(self, x, y, size, board):
        self.pos = pygame.Vector2(x, y)
        self.coverSurface = pygame.Surface((size, size), pygame.SRCALPHA)
        self.cover = Box(0, 0, size, size, (130, 130, 130, 150))
        self.active = True
        self.board = board
        lineColour = (190, 190, 190)
        lineWidth = int(size * 0.03)
        tileWidth = int((size * 0.94)/3)
        self.tiles = []
        self.lines = []
        for i in range(3):
            for j in range(3):
                posX = x + j*(tileWidth+lineWidth)
                posY = y + i*(tileWidth+lineWidth)
                tile = Button(posX, posY, tileWidth, tileWidth, (0, 0, 0, 0), '', (40, 40, 40), 100, None, maxWidth=tileWidth*0.6)
                self.tiles.append(tile)
        self.lines.append(Box(x+2*tileWidth+lineWidth, y, lineWidth, size, lineColour, rounding=4))
        self.lines.append(Box(x, y+tileWidth, size, lineWidth, lineColour, rounding=4))
        self.lines.append(Box(x, y+2*tileWidth+lineWidth, size, lineWidth, lineColour, rounding=4))
        self.lines.append(Box(x+tileWidth, y, lineWidth, size, lineColour, rounding=4))

    def check_press(self, pos):
        for i, tile in enumerate(self.tiles):
            if tile.check_press(pos) and self.board.get_board()[i] == 0:
                return i
            
    def set_active(self, active):
        self.active = active
            
    def update_tiles(self):
        playerCharDict = {-1 : 'O', 0 : '', 1 : 'X'}
        for i, player in enumerate(self.board.get_board()):
            self.tiles[i].update_text(playerCharDict[player])

    def display(self, screen):
        self.update_tiles()
        for tile in self.tiles:
            tile.display(screen)
        for line in self.lines:
            line.display(screen)
        if not self.active:
            self.cover.display(self.coverSurface)
            screen.blit(self.coverSurface, self.pos)
