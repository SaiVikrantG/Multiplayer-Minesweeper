import time 
import threading

start_time = time.time()
time_flag = 1

time_elapsed = 0

def timer():
    global time_elapsed
    while True:
        if(time_flag!=0):
          time_elapsed += 1 
          print(time_elapsed)
          time.sleep(1)

        elif(time_flag==0):
          print("waiting")
          time.sleep(0.1)

t = threading.Thread(target = timer)


print("check0")
t.start()
print("check1")
time.sleep(10)
print("check2")
time_flag = 0
print("check3")
time.sleep(10)
time_flag =1
print("check4")
