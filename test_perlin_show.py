#Made by Igor Michalec

import pygame
import math
import time


def col_rect(colour,x,y,width,height): #creates a rectangle that will resize with the window
    pygame.draw.rect(display,(colour[0],colour[1],colour[2]),(x,y,width,height) )

def write(colour,text, x, y, size):# writes text
    font = pygame.font.SysFont("Arial", size)
    rend = font.render(text,1,(255*colour,255*colour,255*colour))
    display.blit(rend,(x,y))
def line(colour,startx,starty,endx,endy,width):
    pygame.draw.line(display,(colour[0],colour[1],colour[2]),(startx,starty),(endx,endy),width)

#Main loop
pygame.init()#Initializes all of the pygame modules


pygame.display.set_caption("")#Sets the name of the window to what is in teh brackets

display_width = 640
display_height = 700

display = pygame.display.set_mode((display_width,display_height))#Creates the display

cols =[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
while True: 
    display.fill((255,255,255))
    col_rect([0,255,0],100,100,300,300)
    line(cols[0],100,100,200,200,2)
    line(cols[1],400,100,500,200,2)
    line(cols[2],100,400,200,500,2)
    line(cols[3],400,400,500,500,2)
    pygame.display.update()#Updating the display
    for event in pygame.event.get():#Checking for inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                cols =[[255,0,0],[0,0,0],[0,0,0],[0,0,0]]
                
            elif event.key == pygame.K_2:
                cols =[[0,0,0],[255,0,0],[0,0,0],[0,0,0]]
                
            elif event.key == pygame.K_3:
                cols =[[0,0,0],[0,0,0],[255,0,0],[0,0,0]]
            elif event.key == pygame.K_4:
                cols =[[0,0,0],[0,0,0],[0,0,0],[255,0,0]]
        if event.type == pygame.QUIT:#Checking for closing
            pygame.quit()
            quit()



