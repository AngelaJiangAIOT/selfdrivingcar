# -*- coding: utf-8 -*-
import socket
import cv2
import numpy as np
from moduls.ultrasonic import SuperSonic
from moduls.CarAutoPilotByPredict import CarAutoPilotByPredict
from keras.models import load_model


cap = cv2.VideoCapture(0)            #取得樹梅派攝影機物件
cap.set(3,320)
cap.set(4,240)

car_pre = CarAutoPilotByPredict()
print('模型載入中...')
model = load_model('./models/model.h5')
print('完成模型載入')
s = SuperSonic()


try:    
  while True:
    _, img = cap.read()                    #讀取影像
    img = img[120:240, :]                        #取下半部 (之後要做道路辨識用)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  #灰階
    img = cv2.GaussianBlur(img, (3,3),0)         #高斯模糊使圖像更平滑，減少噪點
    img = cv2.equalizeHist(img)                  #圖片增亮，強調特徵
    img = img/255                                #歸一化 標準化 Normalization
    img = img.reshape(1,120,320,1)               #圖片轉4D，才能餵進CNN模型
    cv2.imshow('Watch your step !!', img)        #顯示攝影機讀取的影像流

    prediction = model.predict(img)              #針對當前的影像做預測
    sensor_data = s.get_distance()               #取得超音波資料(距離cm)
    

    if sensor_data is not None and sensor_data < 20:  #如果超音波感測器 有感測到數值 而且 數值小於20  就停車!!
         print(f"與障礙物距離{sensor_data:05.2f}")
         print("停車! 前方有障礙物!")
         car_pre.stop()


    else:
        car_pre.steer(prediction)                #車子啟動 並辨識路線自動左右轉



    if cv2.waitKey(1) & 0xFF == ord('q'):
         car_pre.stop()
         break



finally:
    cv2.destroyAllWindows()  # 一旦按下q  關掉所有imshow所產生的影像視窗
    print("結束自動駕駛....")


    
    
