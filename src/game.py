import socket
import errno
import time
import random
import pickle

GAME_PORT = 6005
# participating clients must use this port for game communication

#GameStatus = True

############## GAME LOGIC ##############



def GenerateMineSweeperMap():
    n=5
    k=3
    arr = [[0 for row in range(n)] for column in range(n)]
    for num in range(k):
        x = random.randint(0,n-1)
        y = random.randint(0,n-1)
        arr[y][x] = 5
        if (x >=0 and x <= n-2) and (y >= 0 and y <= n-1):
            if arr[y][x+1] != 5:
                arr[y][x+1] += 1 # center right
        if (x >=1 and x <= n-1) and (y >= 0 and y <= n-1):
            if arr[y][x-1] != 5:
                arr[y][x-1] += 1 # center left
        if (x >= 1 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x-1] != 5:
                arr[y-1][x-1] += 1 # top left
 
        if (x >= 0 and x <= n-2) and (y >= 1 and y <= n-1):
            if arr[y-1][x+1] != 5:
                arr[y-1][x+1] += 1 # top right
        if (x >= 0 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x] != 5:
                arr[y-1][x] += 1 # top center
 
        if (x >=0 and x <= n-2) and (y >= 0 and y <= n-2):
            if arr[y+1][x+1] != 5:
                arr[y+1][x+1] += 1 # bottom right
        if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x-1] != 5:
                arr[y+1][x-1] += 1 # bottom left
        if (x >= 0 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x] != 5:
                arr[y+1][x] += 1 # bottom center
    return arr

def GeneratePlayerMap(n=5):
    arr = [['-' for row in range(n)] for column in range(n)]
    return arr 

def DisplayMap(map):
    for row in map:
        print(" ".join(str(cell) for cell in row))
        print("")

def CheckWon(map):
    for row in map:
        for cell in row:
            if cell == '-':
                return False
    return True

def CheckContinueGame(score):
    print("Your score: ", score)
    
    return False

def Game():
    global GameStatus
    
    while GameStatus:
        minesweeper_map = GenerateMineSweeperMap()
        player_map = GeneratePlayerMap()
        score = 0
        while True:
            if CheckWon(player_map) == False:
                print("Enter your cell you want to open :")
                x = input("X (1 to 5) :")
                y = input("Y (1 to 5) :")
                x = int(x) - 1 # 0 based indexing
                y = int(y) - 1 # 0 based indexing
                if (minesweeper_map[y][x] == 5):
                    print("Game Over!")
                    DisplayMap(minesweeper_map)
                    GameStatus = CheckContinueGame(score)
                    break
                else:
                    player_map[y][x] = minesweeper_map[y][x]
                    DisplayMap(player_map)
                    score += 1
 
            else:
                DisplayMap(player_map)
                print("You have Won!")
                GameStatus = CheckContinueGame(score)
                break

def print_current_board():
  print('board:..')

def get_users_move():
  move = input('What is your move: ')
  return move

def update_game_state(player, move):
  global board 
  # update the board
  board = board + move

  print(player + ' played ' + move)

def has_game_ended():
  if (board == 'abcd'):
    return True
  else:
    return False


############## EXPORTED FUNCTIONS ##############

def game_server(after_connect):
  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      accepter_socket.bind(('', GAME_PORT))
      accepter_socket.listen(1)

      # non-blocking to allow keyboard interupts (^c)
      accepter_socket.setblocking(False)
      while True:
        try:
          game_socket, addr = accepter_socket.accept()
        except socket.error as e:
          if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            time.sleep(0.1)
            continue
        break

      game_socket.setblocking(True)
      with game_socket:
        after_connect()
        print('Game Started')

        recv_map = game_socket.recv(4096)
        minesweeper_map = pickle.loads(recv_map)
        score = 0

        while True:

          print("waiting for opp's move")
          opp_move = game_socket.recv(4096)
          if not opp_move:
            break
          recv_player_map = pickle.loads(opp_move)
          DisplayMap(recv_player_map)

          #update_game_state('opp', opp_move)

          '''if has_game_ended():
            break'''

          '''print_current_board()
          move = get_users_move()
          update_game_state('user', move)
          game_socket.send(move.encode())
          if has_game_ended():
            break'''
          
          if CheckWon(recv_player_map) == False:
                print("Enter your cell you want to open :")
                x = input("X (1 to 5) :")
                y = input("Y (1 to 5) :")
                x = int(x) - 1 # 0 based indexing
                y = int(y) - 1 # 0 based indexing

                if (minesweeper_map[y][x] == 5):
                    print("Game Over!")
                    DisplayMap(minesweeper_map)
                    GameStatus = CheckContinueGame(score)
                    break
                else:
                    recv_player_map[y][x] = minesweeper_map[y][x]
                    DisplayMap(recv_player_map)
                    score += 1
 
          else:
                DisplayMap(recv_player_map)
                print("You have Won!")
                GameStatus = CheckContinueGame(score)
                break
          
          send_map = pickle.dumps(recv_player_map)
          game_socket.sendall(send_map)



      print_current_board()
      print('Game ended')


def game_client(opponent):
  check = 1

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      print('Game Started')

      player_map = GeneratePlayerMap()
      minesweeper_map = GenerateMineSweeperMap()
      send_map = pickle.dumps(minesweeper_map)
      score = 0
      game_socket.sendall(send_map)
        

      while True:

        #print_current_board()

        '''move = get_users_move()
        update_game_state('user', move)
        game_socket.send(move.encode())
        if has_game_ended():
          break

        print("waiting for opp's move")
        opp_move = game_socket.recv(1024).decode()
        if not opp_move:
          break
        update_game_state('opp', opp_move)
        if has_game_ended():
          break'''
        
        if(check==0):
          recv_map = game_socket.recv(4096)
          player_map = pickle.loads(recv_map)
          DisplayMap(player_map)
        else:
          check=0

        
        if CheckWon(player_map) == False:
                print("Enter your cell you want to open :")
                x = input("X (1 to 5) :")
                y = input("Y (1 to 5) :")
                x = int(x) - 1 # 0 based indexing
                y = int(y) - 1 # 0 based indexing

                if (minesweeper_map[y][x] == 5):
                    print("Game Over!")
                    DisplayMap(minesweeper_map)
                    GameStatus = CheckContinueGame(score)
                    break
                else:
                    player_map[y][x] = minesweeper_map[y][x]
                    DisplayMap(player_map)
                    score += 1
 
        else:
              DisplayMap(player_map)
              print("You have Won!")
              GameStatus = CheckContinueGame(score)
              break
        
        send_map = pickle.dumps(player_map)
        game_socket.sendall(send_map)


  print_current_board()
  print('Game ended')
