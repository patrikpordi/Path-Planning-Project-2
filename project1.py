import numpy as np

# Giving the start end goal values, please insert it as rows and use transpose!
start = np.array([[1, 6, 7], [2, 0, 5], [4, 3, 8]]).T
goal = np.array([[1, 4, 7], [2, 5, 8], [3, 0, 6]]).T
start_2=np.array([[4, 7, 8], [2, 1, 5], [3, 6, 0]]).T
goal_2=np.array([[1, 4, 7], [2, 5, 8], [3, 6, 0]]).T
start=start_2
goal=goal_2

#Function for moving the 0
#0 right,1 left,2 up, 3 down
def move_(array,i):
    array=np.array(array)
    moved=array
    find_0 = np.argwhere(array == 0)
    if i==0:
        if(find_0[0][1]!=2):
            c=moved[find_0[0][0],find_0[0][1]+1]
            moved[find_0[0][0],find_0[0][1]+1]=0
            moved[find_0[0][0],find_0[0][1]]=c
    elif i==1:
        if(find_0[0][1]!=0):
            c=moved[find_0[0][0],find_0[0][1]-1]
            moved[find_0[0][0],find_0[0][1]-1]=0
            moved[find_0[0][0],find_0[0][1]]=c
    elif i==2:       
        if(find_0[0][0]!=0):
            c=moved[find_0[0][0]-1,find_0[0][1]]
            moved[find_0[0][0]-1,find_0[0][1]]=0
            moved[find_0[0][0],find_0[0][1]]=c
    elif i==3:
        if(find_0[0][0]!=2):
            c=moved[find_0[0][0]+1,find_0[0][1]]
            moved[find_0[0][0]+1,find_0[0][1]]=0
            moved[find_0[0][0],find_0[0][1]]=c 
    return(moved)

# I used a list for the unique generated nodes
# I also added a visited node list since you asked for it,
# but for me it does not make sense to save that, since
# the goal won't be in it
lst=[]
visited=[]
lst.append(start)

# Dictionary to save the relationships and state of the nodes
nodes={1:[None,start]}

parent=1
child=1

# Loop until the goal is in the list
while(not any(map(lambda x: (x == goal).all(), lst))):
    # 4 moves
    for i in range(0,4):
        a=move_(lst[0],i)
        # If the generated array is unique then it will append to the list and the dictionary
        if(not np.array_equal(a, lst[0]) and not any(map(lambda x: (x == a).all(), visited))):
            lst.append(a)
            child+=1
            nodes[child]=[parent,a]
    parent+=1
    visited.append(lst.pop(0))

# Getting the key(index) of the goal
value = next(i for i in nodes if np.array_equal(nodes[i][1], goal))

# Backtrack and generate the solution path
path=[]
while(nodes[value][0]!=None):
    path.append(nodes[value][1])
    value=nodes[value][0]
path.append(nodes[value][1])
path.reverse()
print(path)

# Write nodePath
with open("nodePath.txt", "w") as file:
    for i in path:
        # Flatten the array and write it to the file as comma-separated values
        i_flat = i.flatten("F")
        i_flat_str = " ".join(map(str, i_flat))
        file.write(i_flat_str + "\n")

# Write nodeInfo       
with open("nodeInfo.txt","w") as file:
    for i in nodes:
        # Flatten the array and write it to the file as comma-separated values
        i_flat = nodes[i][1].flatten('F')

        # Flattened tuple
        tup_flat = (i, nodes[i][0], i_flat)
        tup_flat_str = " ".join(map(str, tup_flat))
        file.write(tup_flat_str + "\n")

# Write Nodes
with open("Nodes.txt", "w") as file:
        for i in nodes:
            # Flatten the array and write it to the file as comma-separated values
            i_flat = nodes[i][1].flatten('F')
            tup_flat_str = " ".join(map(str, i_flat))
            file.write(tup_flat_str + "\n")
