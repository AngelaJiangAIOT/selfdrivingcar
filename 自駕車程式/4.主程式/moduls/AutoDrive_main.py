# -*- coding: utf-8 -*-
import socket
import cv2
import numpy as np
# import ObjectDetection
from NeuralNetwork import NeuralNetwork
# import DistanceToCamera
from ultrasonic import SuperSonic
from CarAutoPilotByPredict import CarAutoPilotByPredict

print("OpenCV:",  cv2.__version__)
print("Numpy : ", np.__version__)


# HOST = 'localhost'
# PORT = 5438
# s = socket.socket()
# s.bind((HOST,PORT))
# s.listen(1)
# print('{}伺服器在{}開通了!'.format(HOST, PORT))
# client, addr =s.accept()
# print('用戶端位址:{},阜號:{}'.format(addr[0], addr[1]))
# class NeuralNetwork(object):
# 
#     def __init__(self):
#         self.annmodel = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')
#  
#     def predict(self, samples):
#         ret, resp = self.annmodel.predict(samples)
#         return resp.argmax(-1)  #find max
        
cap = cv2.VideoCapture(0)            #取得樹梅派攝影機物件
cap.set(3,320)
cap.set(4,240)
# obj_detection = ObjectDetection()    #實例化物件辨識函式 (辨識紅綠燈及交通號誌)
# d_to_camera = DistanceToCamera()     #實例化"計算攝影機及障礙物"函式
car_pre = CarAutoPilotByPredict()
# model = NeuralNetwork()              #實例化 神經網路函式 使用"感知器神經網絡分類器"
                      #建立模型(已導入訓練好的參數) 神經網路為[38400, 32, 4]架構
# cascade classifiers 利用 cv2.CascadeClassifier導入辨識工具，其中選擇了StopSign和紅綠燈的辨識工具。
# stop_cascade = cv2.CascadeClassifier('cascade_xml/stop_sign.xml')    #StopSign辨識工具
# light_cascade = cv2.CascadeClassifier('cascade_xml/traffic_light.xml') #紅綠燈的辨識工具
# h1: stop sign
# h1 = 15.5 - 10  # cm
# # h2: traffic light
# h2 = 15.5 - 10

# d_stop_sign = 25
# d_light = 25   
#從影片中發現 車子在StopSign停了5秒 就會前進 所以下面的參數是在計算小車在StopSign停的時間用的
# stop_start = 0              # start time when stop at the stop sign 
# stop_finish = 0
# stop_time = 0
# drive_time_after_stop = 0
        
# stop_flag = False         #表示尚未開始計算在StopSign停得時間 或  剛結束停在StopSign的時間計算 
# stop_sign_active = True   #StopSign是否存在(有無被移走)  存在:True(預設)  不存在:False
model = NeuralNetwork()
s = SuperSonic()

print('load ANN model.')
try:    
  while True:
    success, img = cap.read()
    # cv2.imshow("Result", img)
    roi = img[120:240, :] #取下半部 (之後要做道路辨識用)
    gauss = cv2.GaussianBlur(roi,(5,5),0)
    gray = cv2.cvtColor(gauss, cv2.COLOR_BGR2GRAY)  #將圖片轉成灰階
#     ret,th3 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
   
    # object detection  物件辨識      #呼叫Obj_detection 的detect的方法 回傳 v值 (y+寬-5)
    # v_param1 = obj_detection.detect(stop_cascade, gray, img)  #回傳StopSign辨識結果 算出來的 v值
    # v_param2 = obj_detection.detect(light_cascade, gray, img) #回傳紅綠燈辨識結果 算出來的 v值
    
    # Cv2.ANN.ML 要改這個https://www.twblogs.net/a/5b7f6df62b717767c6af9095
    # https://zhuanlan.zhihu.com/p/100962973 參考
    
    # if v_param1 > 0 or v_param2 > 0:   #如果StopSign或紅綠燈 有變辨識出結果 (有辨識出結果就會有(x,y),寬跟高，所以v值一定大於1)
    #      d1 = d_to_camera.calculate(v_param1, h1, 300, img)  #計算車子與StopSign的距離
    #      d2 = d_to_camera.calculate(v_param2, h2, 100, img)  #計算車子與紅綠燈的距離
    #      d_stop_sign = d1   #d1 = 車子與StopSign的距離
    #      d_light = d2       #d2 = 車子與紅綠燈的距離

    cv2.imshow('image', gray)   #顯示攝影機讀取的影像 並命名為'image'
    #cv2.imshow('mlp_image', half_gray)  #顯示攝影機讀取的灰階影像

    # reshape image
    image_array = gray.reshape(1, 38400).astype(np.float32)  # reshape
                    
    # neural network makes prediction
#     prediction = model.predict(image_array)   #將reshape完的圖片 導入 神經網路模型 做預測 (給小車行駛判斷方向用)
    prediction = model.predict(image_array)
    sensor_data = s.get_distance()
    
    # stop conditions #小車停止條件:
                                                    #1.與前方障礙物距離小於30以內 
                                                    #2.辨識到StopSign而且與其距離小於25
                                                    #3.遇到紅燈
    if sensor_data is not None and sensor_data < 20:  #如果超音波感測器 有感測到數值 而且 數值小於30  就停車!!
         print("與障礙物距離{:05.2f}".format(sensor_data))
         print("停車! 前方有障礙物!")
         car_pre.stop()
                    
    # elif 0 < d_stop_sign < 25 and stop_sign_active: #如果有辨識到StopSign 而且車子(攝影機)與StopSign的距離 < 25 就停車!!
    #      print("前方有STOP 標誌")
    #      car_pre.stop()

    #                     # stop for 5 seconds
    #      if stop_flag is False:                                   # 一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一
    #         stop_start = cv2.getTickCount()                      # | getTickCount() 用於返回從作業系統啟動到當前所經的計時週期數
    #         stop_flag = True  #表示在正計算停留StopSign的時間       # | getTickFrequency()：用於返回CPU的頻率。這裡的單位是秒，也就是一秒內重複的次數。
    #         stop_finish = cv2.getTickCount()                     # | getTickCount()/getTickFrequency() = 總共花了幾秒
    #                                                               # 一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一
    #         stop_time = (stop_finish - stop_start)/cv2.getTickFrequency() #計算在StopSign停了幾秒
    #         print("停止時間: %.2fs" % stop_time)

    #            # 5 seconds later, continue driving
    #      if stop_time > 5:           #在StopSign前面停了5秒以上
    #         print("等待五秒...")
    #         stop_flag = False            #stop_flag 設成False  表示結束停在StopSign的時間計算 
    #         stop_sign_active = False     #top_sign_active 設成False 表示離開 車子還在StopSign前面 才剛辨識過!! 
                                                            #(等車子離開StopSign後才設定成true，這時候再遇到StopSign就可以再辨識一次)
                            
                            #如果不設定 stop_sign_active 會造成 車子一直停在 StopSign的窘境(無窮迴圈) (不了解的話 就拿掉 模擬看看)

    # elif 0 < d_light < 30:   #車子與紅綠燈的距離如果在0~30的範圍 
    #                     #print("Traffic light ahead")
    #      if obj_detection.red_light:       #如果有偵測到紅燈(red_light=true) 126行   就停車!!
    #         print("Red light")
    #         car_pre.stop()
    #      elif obj_detection.green_light:   #如果有偵測到燈(red_light=true) 131行   就忽略 pass
    #         print("Green light")
    #         pass
    #      elif obj_detection.yellow_light:  #如果有偵測到燈(red_light=true) 136行   就忽略 pass
    #         print("Yellow light flashing")
    #         pass
                        
    #      d_light = 30              #設定30 回到此(256行)就不會再進來判斷 
    #      obj_detection.red_light = False
    #      obj_detection.green_light = False
    #      obj_detection.yellow_light = False

    else:
        car_pre.steer(prediction)    #車子啟動 並辨識路線自動左右轉
        stop_start = cv2.getTickCount()  #計時qql
         # if stop_sign_active is False:   #等車子往前5秒後(表示離開StopSign) 在將stop_sign_active = True。以防車子還沒離開StopSign就又辨識到一次.. 然後又停車
         #    drive_time_after_stop = (stop_start - stop_finish)/cv2.getTickFrequency()
         #    if drive_time_after_stop > 5:
         #        stop_sign_active = True

    if cv2.waitKey(1) & 0xFF == ord('q'):  #按下q 跳出 194行 while迴圈(等於停止影像串流) 並 停止車子 ??
         car_pre.stop()
         break

  cv2.destroyAllWindows() #一旦按下q 跳出194行迴圈之後 關掉所有imshow所產生的影像視窗

finally:
    print("自動駕駛執行中....")


    
    
