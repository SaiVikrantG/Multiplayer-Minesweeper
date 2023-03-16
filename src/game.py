import socket
import errno
import time
import random
import pickle
import pygame 
import threading


GAME_PORT = 6005
# participating clients must use this port for game communication

#time_flag = 0
n=8
k=10

############## GAME LOGIC ##############



def GenerateMineSweeperMap():
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

def GeneratePlayerMap():
    arr = [['-' for row in range(n)] for column in range(n)]
    return arr 

def DisplayMap(map):
    for row in map:
        print(" ".join(str(cell) for cell in row))
        print("")

def CheckWon(score):
    if(score==((n*n)-k)/2):
      return True
    return False

def CheckContinueGame(score):
    print("Your score: ", score)



############## EXPORTED FUNCTIONS ##############

def game_server(after_connect):
  check1 = 0
  check1=2
  

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      
      pygame.init()
      width = 500
      height = 500
      win = pygame.display.set_mode((width,height))
      pygame.display.set_caption("Server")
      font = pygame.font.SysFont('Pokemon GB.ttf', 30)
      

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


        #TIMER 
        time_flag = 0
        
        def timer():
            global time_elapsed

            time_elapsed = 0
            while True:
                if(time_flag==1):
                  time_elapsed += 1 
                  time.sleep(1)

                elif(time_flag==0):
                  time.sleep(0.1)

                elif(time_flag==2):
                  break

        t2 = threading.Thread(target = timer)
        t2.start()

        while True:

          print("waiting for opp's move")
          opp_move = game_socket.recv(4096)
          if(not opp_move and score!=((n*n)-k)/2):
            check1 = 1
            break
          if(not opp_move and score==((n*n)-k)/2):
             check1=0
             break
          recv_player_map = pickle.loads(opp_move)
          DisplayMap(recv_player_map)

          

          #GUI  
          def thread():
              run = True
              while run:
                  for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                          pygame.quit()   
                          run = False
                          break 

                  win.fill((255,255,255))
                  height = 500

                  for i in recv_player_map:
                          string = ""
                          for j in i:
                              string += str(j) + "  "
                          text1 = font.render(string, True, (0,0,0))
                          textRect = text1.get_rect()
                          textRect.center = ((width // 2), (height // 2)-70)
                          win.blit(text1, textRect)

                          height += 53
                      
                  text = font.render("Minesweeper",True,(0,0,0))
                  textRect1 = text.get_rect()
                  textRect1.center = ((width // 2), 100)
                  win.blit(text, textRect1)

                  pygame.display.update()

                  run = False

          t1 = threading.Thread(target = thread)  
          t1.run()


          
          if CheckWon(score) == False:
                time_flag = 1
                print("Enter your cell you want to open :")
                x = input("X (1 to 8) :")
                y = input("Y (1 to 8) :")
                time_flag = 0

                x = int(x) - 1 # 0 based indexing
                y = int(y) - 1 # 0 based indexing

                if (minesweeper_map[y][x] == 5):
                    print("Game Over! You lost.")
                    DisplayMap(minesweeper_map)
                    CheckContinueGame(score)
                    break
                else:
                    recv_player_map[y][x] = minesweeper_map[y][x]
                    DisplayMap(recv_player_map)

                    score += 1
 
          else:
                DisplayMap(minesweeper_map)
                check1 = 0
                CheckContinueGame(score)
                break
          
          send_map = pickle.dumps(recv_player_map)
          game_socket.sendall(send_map)
          


      if(check1==0):
        CheckContinueGame(score)
        print("Tie!")
      elif(check1==1):
        CheckContinueGame(score)
        print("Your opponet tripped on a mine. You won!")  
      else:
        print('Game ended')

      pygame.quit()
      print("Time Elapsed: {}".format(time_elapsed))


def game_client(opponent):
  check = 1
  check1=2

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      
      pygame.init()
      width = 500
      height = 500
      win = pygame.display.set_mode((width,height))
      pygame.display.set_caption("Client")
      font = pygame.font.SysFont('Pokemon GB.ttf', 30)



      game_socket.connect((opponent, GAME_PORT))
      print('Game Started')

      player_map = GeneratePlayerMap()
      minesweeper_map = GenerateMineSweeperMap()
      send_map = pickle.dumps(minesweeper_map)
      score = 0
      game_socket.sendall(send_map)


      #TIMER
      time_flag = 0

      def timer():
          global time_elapsed

          time_elapsed = 0
          while True:
              if(time_flag==1):
                time_elapsed += 1 
                time.sleep(1)

              elif(time_flag==0):
                time.sleep(0.1)

              elif(time_flag==2):
                  break

      t2 = threading.Thread(target = timer)
      t2.start()
        

      while True:
        
        if(check==0):
          print("Waiting for opponent's move")
          recv_map = game_socket.recv(4096)
          if(not recv_map and score!=((n*n)-k)/2):
            check1 = 1
            break
          if(not recv_map and score==((n*n)-k)/2):
             check1=0
             break 
          player_map = pickle.loads(recv_map)
          DisplayMap(player_map)
        else:
          check=0  

        #GUI
        def thread():
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()   
                        run = False 
                         

                win.fill((255,255,255))
                height = 500

                for i in player_map:
                        string = ""
                        for j in i:
                            string += str(j) + "  "
                        text1 = font.render(string, True, (0,0,0))
                        textRect = text1.get_rect()
                        textRect.center = ((width // 2), (height // 2)-70)
                        win.blit(text1, textRect)

                        height += 53
                    
                text = font.render("Minesweeper",True,(0,0,0))
                textRect1 = text.get_rect()
                textRect1.center = ((width // 2), 100)
                win.blit(text, textRect1)

                pygame.display.update()

                run = False


        t1 = threading.Thread(target = thread)  
        t1.run()
        
        
        
        
        if CheckWon(player_map) == False:
                time_flag = 1
                print("Enter your cell you want to open :")
                x = input("X (1 to 8) :")
                y = input("Y (1 to 8) :")
                time_flag = 0
                
                x = int(x) - 1 # 0 based indexing
                y = int(y) - 1 # 0 based indexing

                if (minesweeper_map[y][x] == 5):
                    print("Game Over! You lost.")
                    DisplayMap(minesweeper_map)
                    CheckContinueGame(score)
                    break
                else:
                    player_map[y][x] = minesweeper_map[y][x]
                    DisplayMap(player_map)
                    score += 1
 
        else:
              DisplayMap(minesweeper_map)
              check1 = 0
              CheckContinueGame(score)
              break
        
        send_map = pickle.dumps(player_map)
        game_socket.sendall(send_map)
        




  if(check1==0):
        CheckContinueGame(score)
        print("Tie!")
  elif(check1==1):
        CheckContinueGame(score)
        print("Your opponet tripped on a mine. You won!")
  else:
        print('Game ended')

  pygame.quit()
  print("Time Elapsed: {}".format(time_elapsed))
  