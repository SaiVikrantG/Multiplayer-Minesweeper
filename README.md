# GAME DESCRIPTION

A 2 player minesweeper game over a local area network using sockets. The game consists of a waiting lobby accounting for all the users present on the local network, and any two players on the same network can connect with each other to start playing the game.

## RULES:

- Two players play on a single map.

- MAP SIZE: 8*8

- BOMBS HIDDEN: 10

- Players play by turn.

- If any player encounters a mine, they automatically lose the game.

- In the end after both the players have uncovered all the spaces without any mines, the game ends in a tie.

- In case of a tie, the player who took the least time to play all their moves wins the game.  

- RUN "run.py" file to start game.

## Improvements:

- Need to improve space clearing algo

- Improve GUI

## Dependencies:

- Pygame
  
- Python 3.x

- Pickle

- Sockets
