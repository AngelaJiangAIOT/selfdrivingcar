from modules.CarControl import CarControl
car = CarControl()
class CarAutoPilotByPredict(object):

           
    def steer(self, prediction):      # 控制小車(前,左,右)。
                                                                                                                                                              # 2 : 道路直線的圖片
        if prediction == 0:           # 當預測到 "道路直線的圖片"
            car.Forward(60,60)        # 讓車子直行
            print("Forward")
        elif prediction == 1:         # 當預測到 "道路左彎的圖片"
            car.turnLeft(70,70)       # 車子左彎
            print("Left")                       
        elif prediction == 2:         # 當預測到 "道路右彎的圖片"
            car.turnRight(70,70)      # 車子彎右
            print("Right")
        elif prediction == 3:
            car.Reverse()
            print("Reverse")
        else:                         #
            car.stop()           # 讓車子 停止

    def stop(self):
        
        car.stop()               # 控制小車停止的函數
