from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pino sensor 1
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)     #pino sensor 2
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)     #pino sensor 3
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #pino sensor 4
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pino sensor 5
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pino sensor 6
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pino sensor 7
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #pino sensor 8
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)      #pino sensor 9
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pino master
GPIO.setup(12, GPIO.OUT) #pino buzzer


pin_Master = 19
pin_1 = 26
pin_2 = 20
pin_3 = 21
pin_4 = 4
pin_5 = 17
pin_6 = 27
pin_7 = 22
pin_8 = 10
pin_9 = 9


class MainLayout(FloatLayout):
    pass 

class bar(Widget):
    r = NumericProperty(1)
    g = NumericProperty(0)

    def __init__(self, pin, p1, p2, **kwargs):
        super(bar, self).__init__(**kwargs)
        self.pin = pin
        self.p1  = p1
        self.p2  = p2
        self.pin_Buzzer = 12
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        self.canvas.clear()
        if  self.read_SensorGeral(self.pin) == True:
            with self.canvas:
                Color(self.g, 1, 0, 1)
                Rectangle(pos=(self.p1,self.p2), size=(35,300))
            GPIO.output(12, 0)
        else:
            with self.canvas:
                Color(self.r, 0, 0, 1)
                Rectangle(pos=(self.p1,self.p2), size=(35,30))
            GPIO.output(12, 1)
    def read_Sensor(self, pin):
        sensor = GPIO.wait_for_edge(pin, GPIO.BOTH, timeout=200)                                                                   
        if sensor is None:
            return False
        else:
            return True

    def read_SensorGeral(self, pin):
        sensor = GPIO.wait_for_edge(pin, GPIO.BOTH, timeout=200)                                                                   
        if sensor is None:
            return False
        else:
            return True

    class MainApp(App):
        def build(self):
            Window.clearcolor = (1, 1, 1, 1)
            self.mainlayout = Widget()
            barGeral = bar(pin_Master, 26, 100)
            bar1 = bar(pin_1, 26, 30)
            bar2 = bar(pin_2, 106, 30)
            bar3 = bar(pin_3, 186, 30)
            bar4 = bar(pin_4, 266, 30)
            bar5 = bar(pin_5, 346, 30)
            bar6 = bar(pin_6, 426, 30)
            bar7 = bar(pin_7, 506, 30)
            bar8 = bar(pin_8, 586, 30)
            bar9 = bar(pin_9, 666, 30)

            self.mainlayout.add_widget(barGeral)
            self.mainlayout.add_widget(bar1)
            self.mainlayout.add_widget(bar2)
            self.mainlayout.add_widget(bar3)
            self.mainlayout.add_widget(bar4)
            self.mainlayout.add_widget(bar5)
            self.mainlayout.add_widget(bar6)
            self.mainlayout.add_widget(bar7)
            self.mainlayout.add_widget(bar8)
            self.mainlayout.add_widget(bar9)
            return self.mainlayout
    try:
        if __name__ == '__main__':
            MainApp().run()

    except KeyboardInterrupt:
        print("Programa finalizado!")
        GPIO.cleanup()
