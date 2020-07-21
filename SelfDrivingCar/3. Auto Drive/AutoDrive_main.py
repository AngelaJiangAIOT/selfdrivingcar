# -*- coding: utf-8 -*-

import cv2
import numpy as np
from modules.ultrasonic import SuperSonic
from modules.CarAutoPilotByPredict import CarAutoPilotByPredict
from keras.models import load_model
import argparse
import time

# ap = argparse.ArgumentParser()
# 
# ap.add_argument("-m", "--model", required=True,      #模型
#     help="model 的架構 (.xml)")
# ap.add_argument("-v", "--weight_bias", required=True,      
#     help="Model's Weight and Bias (.bin)")
# 
# args = vars(ap.parse_args())

cap = cv2.VideoCapture(0)            #取得樹梅派攝影機物件
cap.set(3,320)
cap.set(4,240)

# net = cv2.dnn.readNetFromModelOptimizer( args["model"],args["weight_bias"],)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
car_pre = CarAutoPilotByPredict()
print('模型載入中...')
model = load_model('./models/model.h5')
print('完成模型載入')
s = SuperSonic()
start_point = cv2.getTickCount()

try:    
  while True:
    print('loop start...')
    _, img = cap.read()                    #讀取影像
    cv2.imshow('Watch your step !!', img) 
    img = img[120:240, :]                        #取下半部 (之後要做道路辨識用)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  #灰階
    img = cv2.GaussianBlur(img, (3,3),0)         #高斯模糊使圖像更平滑，減少噪點
#     img = cv2.equalizeHist(img)                  #圖片增亮，強調特徵
    img = img/255                                #歸一化 標準化 Normalization
    img = img.reshape(1,120,320,1)               #圖片轉4D，才能餵進CNN模型
           #顯示攝影機讀取的影像流
    
#     net.setInput(img)
#     Out = net.forward()
#     print(Out)
    prediction = model.predict(img)              #針對當前的影像做預測
    prediction = prediction[0].argmax()
    print(f'prediction_Label:{prediction}')
    sensor_data = s.get_distance()               #取得超音波資料(距離cm)
    

    if sensor_data is not None and sensor_data < 20:  #如果超音波感測器 有感測到數值 而且 數值小於20  就停車!!
         print(f"與障礙物距離{sensor_data:05.2f}")
         print("停車! 前方有障礙物!")
         car_pre.stop()


    else:
        print('good')
        car_pre.steer(prediction)                #車子啟動 並辨識路線自動左右轉
#         car.pre.stop()


    if cv2.waitKey(1) & 0xFF == ord('q'):   
         car_pre.stop()
         end_point = cv2.getTickCount()
         break

    

finally:
    cv2.destroyAllWindows()  # 一旦按下q  關掉所有imshow所產生的影像視窗
    
    Drive_time = ( end_point -start_point)/cv2.getTickFrequency()/60
    print(f'Total Driving Time:{Drive_time:.2f} minute')
    print("結束自動駕駛....")


    
    
