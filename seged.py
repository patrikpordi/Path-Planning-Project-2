# Importing the library
import cv2 as cv
import numpy as np
import heapq as hq
import pygame
from queue import PriorityQueue
import re
 
# Initializing Pygame
pygame.init()

# Initializing Color
color = (255,255,255)
color_2 = (255,200,150)
color_3=(0,0,0)
 
# Initializing surface
surface = pygame.display.set_mode((600,250))
surface.fill(color_2)

 
# Drawing Rectangle
pygame.draw.rect(surface, color, pygame.Rect(5, 5, 590, 240))
pygame.draw.rect(surface, color_2, pygame.Rect(95, 145, 60, 100))
pygame.draw.rect(surface, color_2, pygame.Rect(95, 5, 60, 105))
pygame.draw.polygon(surface,color_2,[(230.5,84.61),(300,44.23),(369.5,84.61),(369.5,165.39),(300,205.77),(230.5,165.39)])
pygame.draw.polygon(surface,color_2,[(455,3.82),(515.59,125),(455,246.18)])
pygame.display.flip()


# Convert surface to a 2D array with 0 for the specific color and 1 for other colors
arr = np.zeros((surface.get_width(), surface.get_height()))
pixel = pygame.surfarray.pixels3d(surface)
arr[np.where((pixel == color_2).all(axis=2))] = 1


# Get coordinates of all pixels with color_2
obstacles_list = [(x, y) for x in range(surface.get_width()) for y in range(surface.get_height()) if surface.get_at((x, y)) == color_2]
obstacles=set(obstacles_list)
# print(arr[(10,10)])
# Define the background colour
# using RGB color coding.
#background_colour = (234, 212, 252)
  
# Define the dimensions of
# screen object(width,height)
#screen = pygame.display.set_mode((300, 300))
  
# Set the caption of the screen
#pygame.display.set_caption('Dijkstra')
  
# Fill the background colour to the screen
#screen.fill(background_colour)
  
# Update the display using flip
#pygame.display.flip()
  
# Variable to keep our game loop running


# 0:right,1:rightdown,2:down,3:leftdown,4:left,5:leftup,6:up,7:rightup
def move(lst,i):
    coords=list(lst[3])
    cost=lst[0]
    if i==0:
        coords[0]+=1
        cost+=1
    elif i==1:
        coords[0]+=1
        coords[1]+=1
        cost+=1.4
    elif i==2:       
       coords[1]+=1
       cost+=1
    elif i==3:
        coords[0]-=1
        coords[1]+=1
        cost+=1.4
    elif i==4:
        coords[0]-=1
        cost+=1
    elif i==5:       
        coords[0]-=1
        coords[1]-=1
        cost+=1.4
    elif i==6:
        coords[1]-=1
        cost+=1
    elif i==7:
        coords[0]+=1
        coords[1]-=1
        cost+=1.4   
    return(tuple(coords), cost)

while True:
    user_input = input("Enter x,y coordinates (e.g. 2,3): ")
    match = re.match(r'^\s*(\d+)\s*,\s*(\d+)\s*$', user_input)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        # Do something with x and y
        break
    else:
        print("Invalid input. Please enter x,y coordinates in the format 'x,y'.")

while True:
    print("Enter the start position (x,y):")
    user_input = input("Enter a valid input: ")
    if :
        # Start your main program here
        print("Valid input received:", user_input)
        break
    else:
        print("Invalid input, please try again.")

start=(6,6)
# goal=(150,160)
goal=(90,50)
surface.set_at(start, (255, 0, 0))
surface.set_at(goal, (255, 0, 0))
pygame.display.update()

pixels={}

d1 = [0, 0, -1, start]
# Q = PriorityQueue()
# Q.put(d1)
# hq.heappush(Q, d1)
Q = []
hq.heappush(Q, d1)

parent=-1
child=1


if((arr[start]==1)):
    print("Start is inside of an obstacle")
if(arr[goal]==1):
    print("Goal is inside of an obstacle")

if(not ((arr[start]==1) or (arr[goal]==1) )):
    while(True):
        # hq.heapify(Q)
        if(len(Q)==0):
            print("Goal is unreachable")
            break
       
        first = hq.heappop(Q)
        # first = Q.get()
        pixels[first[1]]=[first[0],first[2],first[3]]
        parent=first[1]
        surface.set_at(first[3], (255, 0, 0))
        pygame.display.update()
        if(first[3]==goal):
            print("goal reached")
            break
        for i in range(0,8):
            coords,cost=move(first,i)
            #print(i)

            pixel_found = False
            for pixel in pixels.items():
                if pixel[-1] == coords:
                    pixel_found = True
                    break

            
            if(not(arr[coords]==1) and ( not(pixel_found)) and not(any(value[-1] == coords for value in pixels.values()))):
                if not(any(x[-1] == coords for x in Q)): 
                    hq.heappush(Q, [cost, child, parent, coords])
                    child += 1

                elif (any(x[-1] == coords and x[0] > cost for x in Q)): 
                    index = next((i for i, item in enumerate(Q) if item[-1] == coords), None)
                    Q[index][0] = cost
                    Q[index][2]=parent
                    hq.heapify(Q)
        
    if(not (len(Q)==0)):
              
        value = next(i for i in pixels if pixels[i][-1] == goal)
        print(pixels[value])
        # print(Q.queue)
        #Backtrack and generate the solution path
        path=[]
        print(pixels[value][0])
        print(value)
        while(pixels[value][1]!=-1):
            path.append(pixels[value][-1])
            value=pixels[value][1]
        path.append(pixels[value][-1])
        path.reverse()
        print(path)

        pygame.draw.lines(surface, color_3, False, path, 1)
        pygame.display.update()


running = True
  
# game loop
while running:
# for loop through the event queue  
    for event in pygame.event.get():
        
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
#pygame.display.update
