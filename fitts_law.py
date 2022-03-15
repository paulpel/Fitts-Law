import os
import random
import math
import sys
import time
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
 
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        win_width = 800
        win_height = 800
        self.btn_width = 80
        self.btn_height = 20

        self.first = True
        self.counter = 0
        self.data = []

        self.setGeometry(1920/2-win_width/2, 1080/2-win_height/2, win_width, win_height)
        self.setWindowTitle("Fitts Law App")

        self.button = QPushButton("Start", self)
        self.button.setStyleSheet("background-color : #9CB380")

        self.button.setGeometry(
            win_width/2-self.btn_width/2, win_height/2-self.btn_height/2, self.btn_width, self.btn_height)
        self.button.clicked.connect(self.clickme)

        self.test_btn = QPushButton(self)
        self.test_btn.setStyleSheet("background-color : #E15634")
        self.test_btn.setGeometry(0, 0, self.btn_width, self.btn_height)
        self.test_btn.clicked.connect(self.test)
        self.test_btn.hide()
 
        self.show()
 
    def clickme(self):
        self.button.hide()
        self.test_btn.show()

    def test(self):
        time_dif = 0
        
        current_x = self.test_btn.x() + self.test_btn.width()/2
        current_y = self.test_btn.x() + self.test_btn.height()/2
        current_wid = self.test_btn.width()
        
        new_b_wid = random.randint(10, 300)
        new_x = random.randint(0,800-new_b_wid)
        new_y = random.randint(0,800-self.btn_height)
        distance = math.hypot(
            current_x - (new_x+ self.test_btn.width()/2), current_y - (new_y + self.test_btn.height()/2))
        self.test_btn.setGeometry(new_x, new_y, new_b_wid, self.btn_height)

        if self.first:
            self.start_time = time.time()
            self.first = False
        else:
            self.now = time.time()
            time_dif = self.now - self.start_time
            self.start_time = self.now
            self.counter += 1

            measuere = {
                "distance": distance,
                "width": current_wid,
                "time": time_dif,
                "calc": math.log2(distance/current_wid)
            }

            self.data.append(measuere)
        
        if self.counter == 10:
            js_data = {"data": self.data}
            
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, "results.json")
            
            with open(path, 'w') as jf:
                json.dump(js_data, jf, indent=4)
            self.close()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())