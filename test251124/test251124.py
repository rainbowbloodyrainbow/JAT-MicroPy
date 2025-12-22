from machine import Pin,PWM
import time
import math
print("Hello, ESP32!")
# led_pwm = PWM(Pin(2),freq = 500)
# start_time = time.ticks_ms()

# while True:
#     elapsed = time.ticks_diff(time.ticks_ms(),start_time)
#     duty = int (512 + 512* math.sin(elapsed/1000))
#     led_pwm.duty(duty)
#     time.sleep_ms(10)


#流水灯
# led_pins =[2,22,23,25]
# for i in range(len(led_pins)):
#     led = Pin(led_pins[i],Pin.OUT)
#  #由于python语言的简便性，这里也可以直接for pin in led_pins: led = Pin(pin,Pin.OUT)
#     led.value(1)
#     led.value(1)
#     time.sleep(0.5)
#     led.value(0)
#     time.sleep(0.5)

#按键控制流水呼吸灯
# led_pins =[2,22,23,25]
# key = Pin(15,Pin.IN,Pin.PULL_UP)
# def breathe_led(THEpin,THEstep,THEdelay,THEfreq):
#     led_pwm = PWM(Pin(THEpin),freq = THEfreq)
#     while True:
#         for duty in range(0,1024,THEstep):
#             led_pwm.duty(duty)
#             time.sleep(THEdelay)
#         for duty in range(1023,-1,-THEstep):
#             led_pwm.duty(duty)
#             time.sleep(THEdelay)

# for i in range(0,4):
#     breathe_led(led_pins[i],10,0.01,500)
#     while key.value() == 1:
# #未完待续……







# 简单按键状态轮询
# button = Pin(22,Pin.IN,Pin.PULL_UP)

# while True:
#     state = button.value()
#     print("Pressed"if state == 0 else "Released")
#     time.sleep_ms(100)







# 非阻塞按键检测与消抖
# class Button:
#     def __init__(self, pin_num, debounce_ms=50):
#         self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
#         self.debounce_ms = debounce_ms
#         self.last_state = self.pin.value()
#         self.last_change = time.ticks_ms()

#     def pressed(self):
#         current = self.pin.value()
#         now = time.ticks_ms()
        
#         if current != self.last_state:
#             self.last_change = now
#             self.last_state = current
# # 检测下降沿（按下）且已稳定
#         if (current == 0 and 
#             time.ticks_diff(now, self.last_change) >= self.debounce_ms):
#             # 重置状态防止重复触发
#             self.last_state = 1
#             return True
#         return False

# # 使用
# btn = Button(22)

# while True:
#     if btn.pressed():
#         print("Button DEBOUNCED press!")
#     time.sleep_ms(10)








# #中断方式检测按键
# # 全局标志（必须用 .value 属性或简单变量）
# button_pressed = False

# def button_isr(pin):
#     global button_pressed
#     # 简单防抖：忽略重复触发（需配合主循环清零）
#     if not button_pressed:
#         button_pressed = True

# # 初始化按钮（下降沿触发）
# btn = Pin(22, Pin.IN, Pin.PULL_UP)
# btn.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)

# # 主循环
# counter = 0
# last_press_time = 0
# DEBOUNCE_MS = 150

# while True:
#     if button_pressed:
#         now = time.ticks_ms()
#         # 软件防抖：检查时间间隔
#         if time.ticks_diff(now, last_press_time) > DEBOUNCE_MS:
#             counter += 1
#             print(f"Button pressed! Count: {counter}")
#             last_press_time = now
#         button_pressed = False  # 清除标志
    
#     time.sleep_ms(10)  # 非阻塞主循环

