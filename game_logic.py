import random


def minesweeper(n):
    global Index
    Index = []
    x,y=(1,2)
    arr = [[0 for row in range(n)] for column in range(n)]

    for i in range(3):

        while((x,y) in Index):
            x = random.randint(0,4)
            y = random.randint(0,4)

        Index.append((x,y))

        arr[y][x] = 5
        if (x >= 1 and x <= 3):
            arr[y][x+1] += 1 # center right
            arr[y][x-1] += 1 # center left
        if (x == 0):
            arr[y][x+1] += 1 # center right
        if (x == 4):
            arr[y][x-1] += 1 # center left
        if (x >= 1 and x <= 4) and (y >= 1 and y <= 4):
            arr[y-1][x-1] += 1 # top left
    
        if (x >= 0 and x <= 3) and (y >= 1 and y <= 4):
            arr[y-1][x+1] += 1 # top right
        if (x >= 0 and x <= 4) and (y >= 1 and y <= 4):
            arr[y-1][x] += 1 # top center
    
        if (x >=0 and x <= 3) and (y >= 0 and y <= 3):
            arr[y+1][x+1] += 1 # bottom right
        
        if (x >= 1 and x <= 4) and (y >= 0 and y <= 3):
            arr[y+1][x-1] += 1 # bottom left
        if (x >= 0 and x <= 4) and (y >= 0 and y <= 3):
            arr[y+1][x] += 1 # bottom center

        x = random.randint(0,4)
        y = random.randint(0,4)

    for row in arr:
        print(" ".join(str(cell) for cell in row))
        print("")
        

if __name__ == "__main__":
    minesweeper(5)