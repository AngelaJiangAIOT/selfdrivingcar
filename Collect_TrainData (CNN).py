import numpy as np
import cv2
import pygame
from pygame.locals import *
import time
import os
import  RPi.GPIO as GPIO
from CarControl import CarControl

# set IO and GPIO mod
# GPIO.cleanup()
# pygame init
pygame.init()
car = CarControl()

save_img = True
cap = cv2.VideoCapture(0)  
cap.set(3,320) # 原始寬度。原始圖大小:320*240 = 76800
cap.set(4,240) # 原始高度

# create labels
k = np.eye(3)
# k = np.zeros((3, 3), 'float')
# for i in range(3):
#     k[i, i] = 1
# temp_label = np.zeros((1, 3), 'float')
 
screen=pygame.display.set_mode((320,240))
    
frame = 1
saved_frame = 0
total_frame = 0
label_0 =0
label_1 =1
label_2 =2
# collect images for training
print('開始收集影像資料....')

e1 = cv2.getTickCount()
image_array = np.zeros((1,120, 320,1))
label_array = np.zeros((1, 3), 'float')

# collect cam frames
try:
 
    while save_img:
 
        _, cam = cap.read()    
        roi = cam[120:240, :]  # roi = 120*320 = 38400
        gray = cv2.cvtColor(roi,cv2.COLOR_RGB2GRAY)
        gauss = cv2.GaussianBlur(gray,(3,3),0)
        img = cv2.equalizeHist(gauss)
#         img = gauss/255 #normalization  像素介於0~1之間
        cv2.imshow('img',gauss)
        img = gauss.reshape(1,120,320,1)
        
        frame += 1          
        total_frame += 1
 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            print("離開")  
 
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    car.Forward()
                    image_array = np.vstack((image_array, img))
                    label_array = np.vstack((label_array, k[0]))
                    saved_frame += 1
                    
#                     cv2.imwrite(f'./training_images/Label_{label_0:1}/frame{saved_frame:>05}.jpg',img)                          
                    print("前進，並記錄當前影像")
                    print(saved_frame)

                elif keys[pygame.K_a]:
                    car.turnLeft()
                    image_array = np.vstack((image_array, img))
                    label_array = np.vstack((label_array, k[1]))
                    saved_frame += 1
                    
#                     cv2.imwrite(f'./training_images/Label_{label_1:1}/frame{saved_frame:>05}.jpg',img)
                    print("左轉，並記錄當前影像")
                    print(saved_frame)

                elif keys[pygame.K_d]:
                    car.turnRight()
                    image_array = np.vstack((image_array, img))
                    label_array = np.vstack((label_array, k[2]))
                    saved_frame += 1
                    
#                     cv2.imwrite(f'./training_images/Label_{label_2:1}/frame{saved_frame:>05}.jpg',img)
                    print("右轉，並記錄當前影像")
                    print(saved_frame)

                elif keys[pygame.K_UP]:                                                     
                    car.Forward()
                    print("前進")
 
                elif keys[pygame.K_s]:
                    car.Reverse()                         
                    print("後退")
                elif keys[pygame.K_DOWN]:
                    car.Reverse()                           
                    print("後退")
 
                elif keys[pygame.K_LEFT]:
                    car.turnLeft()
                    print("原地左轉")
 
                elif keys[pygame.K_RIGHT]:
                    car.turnRight()                      
                    print("原地右轉")                      
 
                elif keys[pygame.K_p]:
                    print('離開資料採集!')
                    save_img = False                               
                    break

            elif event.type == KEYUP:
                    car.stop()               
                    
 
    # save training images and labels 
 
    train = image_array[1:, :]
    train_labels = label_array[1:, :]
    # save training data as a numpy file

    file_name = str(int(time.time()))
    directory = "training_data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
    except IOError as e:
        print(e)
    e2 = cv2.getTickCount()
 
    time0 = (e2 - e1) / cv2.getTickFrequency() # 計算程式執行時間的秒數
    print('Video duration:', time0)
    print('Streaming duration:', time0)

    print((train.shape))
    print((train_labels.shape))
    print('Total frame:', total_frame)
    print('Saved frame:', saved_frame)
    print('Dropped frame', total_frame - saved_frame)

finally:
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()    
    GPIO.cleanup()