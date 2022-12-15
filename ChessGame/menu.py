''' Include class for button, menu and timer'''
import pygame

class Menu:
    def __init__(self,surface):
        self.surface = surface
        self.bg = pygame.image.load("menu.png")
        self.bg = pygame.transform.scale(self.bg, (650,600))
        # True if chosen 
        self.onePlayer = False
        self.twoPlayers = False
        self.closeClicked = False
        self.time = pygame.time.Clock()
        self.FPS = 60
        self.rect1, self.option1 = self.initOption("Menu1.png",(240,370))
        self.rect2, self.option2 = self.initOption("Menu2.png",(410,370))

    def initOption(self, imageName,pos):
        # Function to create rect obj for each option/imageName
        option = pygame.image.load(imageName)
        rect = option.get_rect()
        rect.center = pos
        return rect, option

    def play(self):
            while not self.closeClicked:  # until player clicks close box
            # play frame
                if self.onePlayer:
                    return 1
                elif self.twoPlayers:
                    return 2
                self.handleEvents()
                self.draw()            
                self.time.tick(self.FPS) # run at most with FPS Frames Per Second 
            return 0
          
    def handleEvents(self):
        # Function to handle all events 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.closeClicked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleMouseDown(event)
    
    def handleMouseDown(self,event):
        # Function to check if player choose either choice/rect obj
        if self.rect1.collidepoint(event.pos):
            self.onePlayer = True
        elif self.rect2.collidepoint(event.pos):
            self.twoPlayers = True
            
    def draw(self):
        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.option1, (self.rect1))
        self.surface.blit(self.option2, (self.rect2))
        pygame.display.update()

class Button:
    def __init__(self,surface,text,width,height,pos,size,color,radius):
        self.pressed = False
        self.surface = surface
        # rec obj
        self.rect = pygame.Rect(pos,(width,height))
        self.color = '#BBB9AB'
        self.colorTouched = color
        self.radius = radius
        # context
        self.fontSize = size
        self.font = pygame.font.SysFont('Consolas', self.fontSize)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.textRect = self.text.get_rect(center = self.rect.center)
        
    def changeName(self,newName):
        # Function to change content of the button when chosen
        self.text = self.font.render(newName, True, (0, 0, 0))
        self.textRect = self.text.get_rect(center = self.rect.center)
    
    def draw(self):
        pygame.draw.rect(self.surface,self.color,self.rect,border_radius = 12)
        self.surface.blit(self.text,self.textRect)
        self.checkTouched()
    
    def checkTouched(self):
        # Function to change button's color when touched
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.color = self.colorTouched
        else:
            self.color = '#BBB9AB'
    
    def handleMouseDown(self,mousePos):
        if self.rect.collidepoint(mousePos):
            return True
        return False

class Timing:
    def __init__(self,surface):
        self.surface = surface
        # Timing
        self.timingBg = pygame.image.load("timingbg.png")
        self.timingBg = pygame.transform.scale(self.timingBg, (150,600))
        self.watch = pygame.image.load("time.png")
        self.maxT = 1800*60 #game time frame
        # Player's initial time
        self.timeR = 1800
        self.timeB = 1800  
    
    def draw(self):
        font = pygame.font.SysFont('Consolas', 30)
        self.surface.blit(self.timingBg,(500,0))
        self.surface.blit(self.watch, (510,20))
        self.surface.blit(self.watch, (510,540))
        self.surface.blit(font.render(self.showTime(self.timeB), True, (0, 0, 0)), (545, 30))
        self.surface.blit(font.render(self.showTime(self.timeR), True, (0, 0, 0)), (545, 550))  
        
    def update(self, turn):
        # Keep track with time frame 
        self.maxT -= 1
        # Stop game if either player runs out of time
        if self.timeR == 0 or self.timeB == 0:
            return False
        # Minus each second pass by
        if self.maxT % 60 == 0:
            if turn == 'black':
                self.timeB -= 1
            else:
                self.timeR -= 1        
        return True
    
    def showTime(self,time):
        # Return time in "minute:second" format
        div = int(time/60)
        mod = int(time%60)
        mod = "%02d" % mod
        time = str(div)+':'+ mod
        return time     
    
    def reset(self):
        self.timeR, self.timeB = 1800,1800