# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 03:17:42 2020

@author: Nash
"""

import pygame
from pygame.locals import *
import numpy as np
import pickle  ##for saving known solutions

##define global dictionary to keep track of known solutions##
#KnownSols = {}
with open('KS.p', 'rb') as fp:
    KnownSols = pickle.load(fp)

 
class PygView(object):

    def __init__(self, width=1000, height=600, fps=60):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.initialMat = np.zeros((8,8)).astype(int)
        # ------------- drawing the initial buttons ----------
        button = self.font.render('Solve', True, (0,255,0), (0,0,128))
        buttonRect = button.get_rect()
        buttonRect.center = (500,500)
        self.background.blit(button,buttonRect)
        for num in range(4,9):
            numButton = self.font.render(' '+ str(num) + ' ',True,(0,255,0), (0,0,128))
            numButtonRect = numButton.get_rect()
            numButtonRect.center = (-150 + 50*num, 500)
            self.background.blit(numButton,numButtonRect)
        mess = self.font.render('Choose board size', True, (0,0,0), (255,255,255))
        messRect = mess.get_rect()
        messRect.center = (150,470)
        self.background.blit(mess,messRect)
        randButton = self.font.render('Random', True, (0,255,0),(0,0,128))
        randRect = randButton.get_rect()
        randRect.center = (340,500)
        self.background.blit(randButton,randRect)
        setupButton = self.font.render('Begin', True, (0,255,0), (0,0,128))
        setupRect = setupButton.get_rect()
        setupRect.center = (425,500)
        self.background.blit(setupButton,setupRect)
        
    def checkSolvable(self,Mat = np.zeros((5,5))):
        ##Check whether the current board is solvable
        size = np.sqrt(len(Mat))
        if size == 4:
            Check1 = np.array([1,0,0,0, 1,1,0,0, 1,0,1,0, 0,1,1,1])
            Check2 = np.array([0,0,0,1, 0,0,1,1, 0,1,0,1, 1,1,1,0])
            Check3 = np.array([0,1,0,0, 1,1,1,0, 0,0,0,1, 1,1,0,1])
            Check4 = np.array([0,0,1,0, 0,1,1,1, 1,0,0,0, 1,0,1,1])
            if np.dot(Mat,Check1)%2>0 or np.dot(Mat,Check2)%2>0 or np.dot(Mat,Check3)%2>0 or np.dot(Mat,Check4)%2>0:
                return False
            else:
                return True
        elif size == 5:
            Check1 = np.array([0,1,1,1,0, 1,0,1,0,1, 1,1,0,1,1, 1,0,1,0,1, 0,1,1,1,0])
            Check2 = np.array([1,0,1,0,1, 1,0,1,0,1, 0,0,0,0,0, 1,0,1,0,1, 1,0,1,0,1])
            if np.dot(Mat,Check1)%2>0 or np.dot(Mat,Check2)%2>0:
                return False
            else:
                return True
        else:
            return True
        
        
    def ChooseInitBoard(self,sz = 5):
        ##Not all puzzles are solvable, so only pick a solvable one##
        randMat = np.random.randint(2,size=sz*sz)
        while self.checkSolvable(Mat = randMat) == False:
            randMat = np.random.randint(2,size=sz*sz)
        randMat = randMat.reshape((sz,sz))
        return randMat
    
    def checkWin(self, flag, Mat = np.ones((5,5))):
        size = len(Mat)
        if flag == True:
            for i in range(size):
                if flag == True:
                    for j in range(size):
                        if Mat[i,j]==1:
                            flag = False
                            break
        return flag
    
    def paintInit(self, Mat = np.ones((5,5)), sM = np.zeros((5,5))):
        '''paint the initial boards'''
        size = len(Mat)
        shift = size + 2
        for row in range(size):
            for col in range(size):
                mycell = Cell(col=col, row=row, color=(0,255*Mat[row,col],255),
                              background=self.background)
                mycell.blit(self.background)
                solcell = Cell(col=col+shift, row=row, color=(255*sM[row,col],0,255),
                               background=self.background)
                solcell.blit(self.background)
                
    def paintPuz(self,Mat = np.ones((5,5))):
        '''paint the original puzzle'''
        size = len(Mat)
        for row in range(size):
            for col in range(size):
                mycell = Cell(col=col, row=row, 
                              color=(255*Mat[row,col],255*Mat[row,col],255*(1-Mat[row,col])),
                              background=self.background)
                mycell.blit(self.background)
        

    def paint(self,col=0, row=0, color=(0,0,255)):
        """update a single cell"""
        #------- try out some pygame draw functions --------
        # pygame.draw.line(Surface, color, start, end, width) 
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        #pygame.draw.rect(self.background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        # ------------------- blitting a cell --------------
        mycell = Cell(col=col,row=row,color=color,background=self.background)
        mycell.blit(self.background)
        
        
        
    def click(self, row, col, M = np.ones((5,5)),sM = np.zeros((5,5))):
        size = len(M)
        shift = size + 2
        if row>=size or col >=size:
            pass
        else:
            for i in range(size):
                for j in range(size):
                    if (np.abs(row-i)<2 and col==j) or (row==i and np.abs(col-j)<2):
                        M[i,j] = (M[i,j]+1)%2 ##toggle light and adjacent lights
                        self.paint(row=i,col=j,color=(0,255*M[i,j],255))
            sM[row,col] = sM[row,col]+1
            ##paint the cell clicked on in the solution
            self.paint(col=col+shift,row=row,color=(255*(sM[row,col]%2),0,255)) 
        return M, sM
    
    def toggle(self, row, col, M = np.ones((5,5))):
        size = len(M)
        if row>=size or col >=size:
            pass
        else:
            M[row,col] = (M[row,col]+1)%2 ##toggle the light
            self.paint(row=row,col=col,color=(0,255*M[row,col],255)) 
        return M
    
    def lastRow(self, M=np.ones((5,5))):
        ##create a string of the arrangement in the last column
        size = len(M)
        arr = ''
        for j in range(size):
            arr = arr + str(M[-1,j])    
        return arr
    
    def iterate(self, i, j, step2, size):
        if j<size-1:
            j += 1
        elif step2 == True:
            j = 0
            step2 = False
        else:
            i += 1
            j = 0
            if i == size-1:
                step2 = True
        return i, j, step2
            

##Edit this to run one step of the solving algorithm each frame##
    def run(self):
        """The mainloop"""
        #matrix = self.ChooseInitBoard(sz=8)
        initMat = np.zeros((8,8))
        matrix = np.zeros((8,8))
        size = matrix.shape[0]
        solMatrix = np.zeros((size,size))  ## keep track of the buttons pressed in working to solve
        self.paintInit(Mat=matrix, sM=solMatrix)
        running = True
        setup = True ##this flag is False when the user has finished setup
        stop = False  ##this flag is True when the clock updates should stop
        solving = False  ##this flag is True when the solving process is running
        step2 = False  ##this flag is True to signify step 2 of the solving process
        errorMes = False  ##this flag is True to signify when the error message is visible
        finalRow = ''
        attempt = ''  ##attempt at a solution if solution is unknown
        while running:
            row = -1
            col = -1
            pos = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    errorMes = False
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    if 5<=pos[0]%55 and 5<=pos[1]%55:  ##make sure the click isn't on a boundary 
                        row = pos[1]//55
                        col = pos[0]//55
                
            if setup == True and len(pos)>0:
                if pos[1]<450:  ##it could be on a cell
                    matrix = self.toggle(row,col,matrix)
                elif 485<=pos[1]<=515:  ##it could be on a button
                    if 300<=pos[0]<=385:  ##it's the 'random' button
                        matrix = self.ChooseInitBoard(sz=size)
                        self.paintInit(Mat = matrix, sM = solMatrix)
                    elif 390<=pos[0]<=460:  ##it's the 'begin' button
                        if self.checkSolvable(Mat=matrix.reshape(matrix.size,)):
                            setup = False
                            print('Out of Setup Mode')
                            initMat = matrix.astype(int)
                            matrix = matrix.astype(int)
                            self.clock = pygame.time.Clock()
                            stop = False  ##begin the clock
                        else: ##do not allow the user to set an unsolvable pattern
                            errorMes = True
                    else:  #check if we clicked on a number
                        for num in range(4,9):
                            if -170+50*num<=pos[0]<=-130+50*num:
                                size = num
                                matrix = np.zeros((num,num))
                                solMatrix = np.zeros((num,num))
                                whitescreen = pygame.draw.rect(self.background, (255,255,255), (0,0,1000,450))
                                self.paintInit(Mat = matrix, sM = solMatrix)
                                break ##can only click on one button at a time
            elif solving == False and len(pos)>0:
                ##don't allow clicking while it's solving##
                if 460<=pos[0]<=540 and 485<=pos[1]<=515:  ##then we clicked on the 'solve' button
                    solving = True
                    #set initial position for the solving algorithm#
                    i=0
                    j=0
                elif row>=0 and col>=0:
                    #print(row,col)
                    matrix, solMatrix = self.click(row, col, matrix, solMatrix)
            
            if solving == True:
                ##run through the next step in the solving process##
                if i == 0 and step2 == True:
                    if attempt[j]=='1':
                        matrix, solMatrix = self.click(row=i,col=j,M=matrix, sM=solMatrix)
                elif i<size-1:  ##then we're running the first part of the algorithm
                    ##if a light is lit, use the next row down to clear it
                    if matrix[i,j] == 1:  
                        matrix, solMatrix = self.click(row=i+1,col=j,M=matrix, sM=solMatrix)
                elif i == size-1:
                    ##when reaching the last row, get a string for the arrangement
                    temp = self.lastRow(M = matrix)
                    if '1' in temp:  ##if we haven't finished solving yet
                        if len(finalRow) == len(temp):
                            diff = '' ##measure the difference between the previous final row and new
                            for ch in range(len(finalRow)):
                                diff = diff + str((int(temp[ch]) - int(finalRow[ch]))%2)
                            if diff not in KnownSols:
                                KnownSols[diff] = attempt
                                ## save Known Sols ##
                                with open('KS.p', 'wb') as fp:
                                    pickle.dump(KnownSols, fp, protocol=pickle.HIGHEST_PROTOCOL)
                        finalRow = temp
                        print('Last row: ', finalRow)
                        if finalRow in KnownSols:
                            attempt = KnownSols[finalRow]
                        else:  ##choose a random selection of buttons to press in the top row
                            attempt = ''
                            while '1' not in attempt and attempt not in KnownSols.values():
                                attempt = ''
                                for i in range(size):
                                    attempt = attempt + str(np.random.randint(0,2))
                        step2 = True
                        i=0
                        j=-1
                        print('Attempt: ', attempt)
                    else:  ##if we finished, add the information to the dictionary if it is missing
                        solving = False
                        if finalRow not in KnownSols:
                            KnownSols[finalRow] = attempt
                            ## save Known Sols ##
                            with open('KS.p', 'wb') as fp:
                                pickle.dump(KnownSols, fp, protocol=pickle.HIGHEST_PROTOCOL)
                i,j,step2 = self.iterate(i,j,step2,size)                       
                    
            if stop == False:
                if self.checkWin(True, Mat = matrix): #checkflag == True:
                    print('You Win!!')
                    stop = True
                    if self.playtime != 0: ##if the game was actually played
                        setup = True
                        self.paintPuz(Mat = initMat)
                else:
                    milliseconds = self.clock.tick(self.fps)
                    self.playtime += milliseconds / 1000.0
            self.draw_text("Clicks: {:6.4}{}PLAYTIME: {:6.4} SECONDS".format(
                    np.sum(solMatrix), " "*5, self.playtime))
            self.draw_text("Min Clicks: {:6.3}".format(np.sum(solMatrix%2)), loc=(50,570))
            self.draw_text("Minimal Solution", loc=((3*size/2)*55,(size+0.5)*55))
            
            if errorMes == True:
                self.draw_text("Error: Current Pattern is unsolvable", loc = (50,520), color = (255,0,0))

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()


    def draw_text(self, text,loc=(50,550), color=(0,0,0)):
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, loc)
        
class Cell(object):
    """This is meant to be a method to draw a single cell"""
    def __init__(self, length = 50, col = 0, row = 0, color=(0,0,255), 
                 background = pygame.Surface((400,400))):
        self.length = length
        self.x = col*55
        self.y = row*55
        self.color = color
        self.surface = background
        ##draw background for the cell##
        pygame.draw.rect(self.surface, (0,0,1), (self.x,self.y,self.length+10, self.length+10))
        ##draw the cell##
        pygame.draw.rect(self.surface, self.color, (self.x+5, self.y+5, self.length, self.length))
        self.surface = self.surface.convert() # for faster blitting.
                
    def blit(self,background):
        background.blit(self.surface, (0,0))
            

    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView().run()