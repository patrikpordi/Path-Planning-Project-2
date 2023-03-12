# Importing the library
import cv2 as cv
import numpy as np
import heapq as hq
import pygame
from queue import PriorityQueue
import re
import time

  
# Variable to keep our game loop running
goal_found=False
color = (255,255,255)
color_2 = (255,200,150)
color_3=(0,0,0)

pygame.init()
width, height = 600, 250

# Initializing surface
surface = pygame.Surface((width,height))
surface.fill(color_2)

 
# Drawing Rectangle
pygame.draw.rect(surface, color, pygame.Rect(5, 5, 590, 240))
pygame.draw.rect(surface, color_2, pygame.Rect(95, 145, 60, 100))
pygame.draw.rect(surface, color_2, pygame.Rect(95, 5, 60, 105))
pygame.draw.polygon(surface,color_2,[(230.5,84.61),(300,44.23),(369.5,84.61),(369.5,165.39),(300,205.77),(230.5,165.39)])
pygame.draw.polygon(surface,color_2,[(455,3.82),(515.59,125),(455,246.18)])
# pygame.display.flip()


# Convert surface to a 2D array with 0 for the specific color and 1 for other colors
arr = np.zeros((surface.get_width(), surface.get_height()))
pixel = pygame.surfarray.pixels3d(surface)
arr[np.where((pixel == color_2).all(axis=2))] = 1


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


start_time=time.time()
while True:
    print("Enter start x,y coordinates (e.g. 2,3): ")
    user_input = input()
    match = re.match(r'^\s*(\d+)\s*,\s*(\d+)\s*$', user_input)
    if match:
        x = int(match.group(1))
        y = 250-int(match.group(2))
        # Do something with x and y
        if(arr[x,y]==1):
            print("Start is inside of an obstacle, please try again")
        else:
            start=(x,y)
            break
    else:
        print("Invalid input. Please enter x,y coordinates in the format 'x,y'.")

while True:
    print("Enter goal x,y coordinates (e.g. 2,3): ")
    user_input = input()
    match = re.match(r'^\s*(\d+)\s*,\s*(\d+)\s*$', user_input)
    if match:
        x = int(match.group(1))
        y = 250-int(match.group(2))
        # Do something with x and y
        if(arr[x,y]==1):
            print("Goal is inside of an obstacle, please try again")
        else:
            goal=(x,y)
            break
    else:
        print("Invalid input. Please enter x,y coordinates in the format 'x,y'.")


pixels={}

d1 = [0, 0, -1, start]
Q = PriorityQueue()
Q.put(d1)


parent=-1
child=1
if(not ((arr[start]==1) or (arr[goal]==1) )):
    while(True):
        
        if(Q.empty()):
            print("Goal is unreachable")
            end_time=time.time()
            break
        first = Q.get()
        pixels[first[1]]=[first[0],first[2],first[3]]
        parent=first[1]
        print(pixels[first[1]])
       
        if(first[3]==goal):
            print("Goal reached")
            end_time=time.time()
            break
        for i in range(0,8):
            coords,cost=move(first,i)
            
            pixel_found = False
            for pixel in pixels.items():
                if pixel[-1] == coords:
                    pixel_found = True
                    break

            
            if(not(arr[coords]==1) and ( not(pixel_found)) and not(any(value[-1] == coords for value in pixels.values()))):
                if not(any(x[-1] == coords for x in Q.queue)): 
                    Q.put([cost, child, parent, coords])
                    child += 1

                elif (any(x[-1] == coords and x[0] > cost for x in Q.queue)): 
                    index = next((i for i, item in enumerate(Q.queue) if item[-1] == coords), None)
                    Q.queue[index][0] = cost
                    Q.queue[index][2]=parent
    
    s=pygame.display.set_mode((width,height))
    s.blit(surface,(0,0))
    pygame.display.update()

    for value in pixels.values():
        s.set_at(value[-1],(255,0,0))
        pygame.display.update()
        
    if(not (Q.empty())):

                
        value = next(i for i in pixels if pixels[i][-1] == goal)
       
        # Backtrack and generate the solution path
        path=[]
        while(pixels[value][1]!=-1):
            path.append(pixels[value][-1])
            value=pixels[value][1]
        path.append(pixels[value][-1])
        path.reverse()
        
        for walk in path:
            s.set_at(walk,(0,0,0))
            pygame.display.update()

print(end_time-start_time)
   

running = True
pygame.time.wait(10000)
# game loop
while running:
# for loop through the event queue  
    for event in pygame.event.get():
        
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False



