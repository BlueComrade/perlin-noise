#Made by Igor Michalec

import pygame
import random

def col_rect(colour,x,y,width,height): #creates a rectangle that will resize with the window
    pygame.draw.rect(display,(colour[0],colour[1],colour[2]),(x,y,width,height) )

def write(colour,text, x, y, size):# writes text
    font = pygame.font.SysFont("Arial", size)
    rend = font.render(text,1,(colour))
    display.blit(rend,(x,y))
def line(colour,startx,starty,endx,endy,width):
    pygame.draw.line(display,(colour[0],colour[1],colour[2]),(startx,starty),(endx,endy),width)
#Main loop
pygame.init()#Initializes all of the pygame modules


pygame.display.set_caption("")#Sets the name of the window to what is in teh brackets

display_width = 640
display_height = 700

display = pygame.display.set_mode((display_width,display_height))#Creates the display
movex = 0
movey = 0
seed = 45

def gen_perlin(seed=0,vec_size=1,startx=0,starty=0,grid_size_x=4,grid_size_y=4,pixels_per_grid=40):#will generate a make of perlin noise values from 0-1

    def coord_ran_seed(seed,x,y):#this function allows to get a unique seed based on the universal seed and 2d coordinates
        random.seed(seed)
        next_seed = random.randint(-1000,1000)
        random.seed(next_seed+x)
        next_seed = random.randint(-1000,1000)
        return (next_seed+y)
    
    #sets the arrays needed
    height_map = []#will hold all the heights 0-1
    vectors =[]#will hold the random vectors

    #makes the important variables based on parameters entered 
    per_grid = pixels_per_grid#gets the number of pixels in a grid
    map_num_x = grid_size_x*pixels_per_grid#gets the amount of pixels in the grid 
    map_num_y = grid_size_y*pixels_per_grid#gets the amount of pixels in the grid
    vector_num_x = grid_size_x+1#gives the number of vectors in the grid
    vector_num_y = grid_size_y+1#gives the number of vectors in the grid

    #produces random vectors, seed based
    for x in range(vector_num_x):
        temp = []#temporary array that allows me to make a 2d array
        
        for y in range(vector_num_y):
            random.seed(coord_ran_seed(seed,x+startx,y+starty))#gets the seed of the coordinate 
            x1 = random.uniform(-vec_size,vec_size)#chooses the vector's x value at random
            y1 = random.uniform(-vec_size,vec_size)#chooses the vector's y value at random
            temp.append([x1,y1])#adds the vector's value to the temporary array
            
        vectors.append(temp)#slowly adds to the main vector array


    #gets the heihgt for each vector in the map
    for x in range(map_num_x):
        temp = []#temporary array that allows me to make a 2d array
        
        for y in range(map_num_y):

            #finds the closest main grid point to the pixel
            backx = int(x/per_grid)
            backy = int(y/per_grid)

            #finds the 4 distace vectors from the closest point
            vectors_to = [[(x-backx*per_grid),(y-backy*per_grid)],
                          [(x-backx*per_grid)-(per_grid),(y-backy*per_grid)],
                          [(x-backx*per_grid),(y-backy*per_grid)-(per_grid)],
                          [(x-backx*per_grid)-(per_grid),(y-backy*per_grid)-(per_grid)]]

            #makes an array points with the dot products, which give the gradient of the 4 points
            #(vector to it and the vector on the point are used for the dot produt)
            points = []
            points.append(vectors[backx][backy][0]*vectors_to[0][0]+vectors[backx][backy][1]*vectors_to[0][1])
            points.append(vectors[backx+1][backy][0]*vectors_to[1][0]+vectors[backx+1][backy][1]*vectors_to[1][1])
            points.append(vectors[backx][backy+1][0]*vectors_to[2][0]+vectors[backx][backy+1][1]*vectors_to[2][1])
            points.append(vectors[backx+1][backy+1][0]*vectors_to[3][0]+vectors[backx+1][backy+1][1]*vectors_to[3][1])

            #interpolating bettwen the points with the fade function
            w = ((x-backx*per_grid)/(per_grid-1))
            AB = points[0]+((w*(w*6-15)+10)*w*w*w)*(points[1]-points[0])
            CD = points[2]+((w*(w*6-15)+10)*w*w*w)*(points[3]-points[2])
            w = ((y-backy*per_grid)/(per_grid-1))
            grad = AB +((w*(w*6-15)+10)*w*w*w)*(CD-AB)

            #turning the height into a value bettwen 0-1 for simplicity 
            final = (grad+(per_grid*vec_size))/(2*(per_grid*vec_size))
            
            temp.append(final)
            
        height_map.append(temp)
        
    return height_map#gives the height map
final_x=0
final_y=0
grid_size = 4
square_size = 3
pix_per_grid = 40
v = 1
height_map = gen_perlin(seed,v,final_x,final_y,grid_size,grid_size,pix_per_grid)
mi = 1
ma = 0
display.fill((100,0,0))
keys = [False,False,False,False]
while True:
    for x in range(grid_size*pix_per_grid):#prints the map
        for y in range(grid_size*pix_per_grid):
            if (x+movex)<0 or (y+movey)<0 or (x+movex)>=len(height_map) or (y+movey)>=len(height_map[x]):
                col_rect([0,0,0],x*square_size+100,y*square_size+100,square_size,square_size)
            else:
                try:
                    col = int(height_map[x+movex][y+movey]*255)
                    col_rect([col,col,col],x*square_size+100,y*square_size+100,square_size,square_size)

                except:
                    col_rect([0,0,0],x*square_size+100,y*square_size+100,square_size,square_size)
                    
    pygame.display.update()#Updating the display
    
    if keys[0]:#does all the movment
        movex+=-2
        if movex<0:
            final_x+=-1
            if (len(height_map)==(grid_size+1)*pix_per_grid):
                for i in range(pix_per_grid):
                    height_map.pop()
            temp = gen_perlin(seed,v,final_x,final_y,1,int(len(height_map[0])/pix_per_grid),pix_per_grid)
            for i in range(pix_per_grid-1,-1,-1):
                height_map.insert(0,temp[i])
            movex= pix_per_grid-2
        
    if keys[1]:
        movex+=2
        if movex+grid_size*pix_per_grid>len(height_map):
            if (len(height_map)==(grid_size+1)*pix_per_grid):
                movex-= pix_per_grid
                final_x+=1
                for i in range(pix_per_grid):
                    height_map.pop(0)
            temp = gen_perlin(seed,v,final_x+grid_size,final_y,1,int(len(height_map[0])/pix_per_grid),pix_per_grid)
            for i in range(pix_per_grid):
                height_map.append(temp[i])
                
    
    if keys[2]:
        movey+=-2
        if movey<0:
            final_y+=-1
            if (len(height_map[0])==(grid_size+1)*pix_per_grid):
                for i in range(len(height_map)):
                    for j in range(pix_per_grid):
                        height_map[i].pop()
            temp = gen_perlin(seed,v,final_x,final_y,int(len(height_map)/pix_per_grid),1,pix_per_grid)
            for i in range(len(height_map)):
                for j in range(pix_per_grid-1,-1,-1):
                    height_map[i].insert(0,temp[i][j])
            movey= pix_per_grid-2
        
    if keys[3]:
        movey+=2
        if movey+grid_size*pix_per_grid>len(height_map[0]):
            if (len(height_map[0])==(grid_size+1)*pix_per_grid):
                movey-= pix_per_grid
                final_y+=1
                for i in range(len(height_map)):
                    for j in range(pix_per_grid):
                        height_map[i].pop(0)
            temp = gen_perlin(seed,v,final_x,final_y+grid_size,int(len(height_map)/pix_per_grid),1,pix_per_grid)
            for i in range(len(height_map)):
                for j in range(pix_per_grid):
                    height_map[i].append(temp[i][j])
    for event in pygame.event.get():#Checking for inputs
        if event.type == pygame.KEYDOWN:                
            if event.key == pygame.K_c:
                seed+=2
            elif event.key == pygame.K_a:
                keys[0] = True
            elif event.key == pygame.K_d:
                keys[1] = True
            elif event.key == pygame.K_w:
                keys[2]= True
            elif event.key == pygame.K_s:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keys[0] = False
            elif event.key == pygame.K_d:
                keys[1] = False
            elif event.key == pygame.K_w:
                keys[2] = False
            elif event.key == pygame.K_s:
                keys[3] = False
        if event.type == pygame.QUIT:#Checking for closing
            pygame.quit()
            quit()



