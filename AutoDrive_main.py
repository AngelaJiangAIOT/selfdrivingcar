import socket
import cv2
import numpy as np
from NeuralNetwork import NeuralNetwork
from ultrasonic import SuperSonic # import DistanceToCamera
from CarAutoPilotByPredict import CarAutoPilotByPredict
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
        _ , img = cap.read()
        img = img[120:240, :] # step 1: 取下半部 (之後要做道路辨識用)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # step2: 將圖片轉成灰階
        img = cv2.GaussianBlur(img,(5,5),0) # step3: 高斯模糊
        img = cv2.equalizeHist(img) # step4: histogram equalization 增亮
        img = img/255 # step5: normalization
        cv2.imshow('image', img)   #顯示攝影機讀取的影像 並命名為'image'
        img = img.reshape(1,120,320,1) # step6: 3D->4D. reshape    
           
        prediction = model.predict(img) # 預測標籤 0,1,2
        sensor_data = s.get_distance() # 取得超音波資料(距離cm)
        
        # stop conditions #小車停止條件:
                                                        #1.與前方障礙物距離小於30以內 
                                                        #2.辨識到StopSign而且與其距離小於25
                                                        #3.遇到紅燈
        if sensor_data is not None and sensor_data < 20:  #如果超音波感測器 有感測到數值 而且 數值小於30  就停車!!
            print(f'與障礙物距離{sensor_data:05.2f}')
            print("停車! 前方有障礙物!")
            car_pre.stop()
                        
        else:
            car_pre.steer(prediction)    #車子啟動 並辨識路線自動左右轉
      
        if cv2.waitKey(1) & 0xFF == ord('q'):  #按下q 跳出 194行 while迴圈(等於停止影像串流) 並 停止車子 ??
            car_pre.stop()
            break

finally:
    cv2.destroyAllWindows() #一旦按下q 跳出迴圈之後 關掉所有imshow所產生的影像視窗
    print("結束自動駕駛")