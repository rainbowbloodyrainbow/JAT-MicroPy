# from machine import Pin,PWM
# import time
# import math
# print("Hello, ESP32!")
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




# #软件延时消抖法
# import time
# from machine import Pin

# button = Pin(22,Pin.IN,Pin.PULL_UP)

# def key_scan():
#     state = button.value()
#     if state == 0:
#         time.sleep_ms(10)
#         if button.value() == 0:
#             return True
#     return False

# while True:
#     if key_scan():
#         print("Button pressed!")
#         time.sleep_ms(100)
# # 思考：key_scan()中延时10ms和while中延时100ms的作用分别是什么？
# # 参考答案：
# # key_scan()中延时10ms的目的是消抖，即在按键按下时，如果在10ms内又按下，则忽略掉第二次按键。
# # while中延时100ms的目的是防止程序过快
        













# # 计数消抖法：设置一计数器，检测按键状态，若按键按下，则计数器加1，若计数器大于一定值(这里以50为例)，则执行动作，否则继续等待
# import time
# from machine import Pin

# button = Pin(22,Pin.IN,Pin.PULL_UP)
# counter = 0
# counter_max = 50
# def key_scan():
#     global counter
#     state = button.value()
#     if state == 0:
#         counter += 1
#         if counter > counter_max:
#             return True
#     return False

# while True:
#     if key_scan():
#         print("Button pressed!")
#         counter = 0
#         time.sleep_ms(100)











# # 状态机编程处理按键
# # 使用四个状态UP,DOWN_delay，DOWN,UP_delay,表示按键的四种状态：抬起、按下消抖、按下、抬起消抖
# # 状态转换关系如下：
# # 对于UP状态：button.value() == 0 时 转换为DOWN_delay
# # 对于DOWN_delay状态：延时50ms，若button.value() == 0，则转换为DOWN;若button.value() == 1，则转换为UP
# # 对于DOWN状态：button.value() == 1 时 转换为UP_delay
# # 对于UP_delay状态：延时50ms，若button.value() == 1，则转换为UP;若button.value() == 0，则转换为DOWN
# # 初始状态为UP

# from machine import Pin
# import time

# button = Pin(22,Pin.IN,Pin.PULL_UP)

# state = "UP"

# def key_scan_StateMachine():
#     global state
# # python中没有switch语句，因此用if来实现状态转移
#     if state == "UP":
#         if button.value() == 0:
#             state = "DOWN_delay"
#     elif state == "DOWN_delay":
#         time.sleep_ms(50)
#         if button.value() == 0:
#             state = "DOWN"
#         elif button.value() == 1:
#             state = "UP"
#     elif state == "DOWN":
#         if button.value() == 1:
#             state = "UP_delay"
#     elif state == "UP_delay":
#         time.sleep_ms(50)
#         if button.value() == 1:
#             state = "UP"
#         elif button.value() == 0:
#             state = "DOWN"
#     return state

# while True:
#     if key_scan_StateMachine() == "DOWN":
#         print("Button pressed!")
#         time.sleep_ms(100) # 按下后延时100ms再检测按键状态，防止抖动




















# 状态机处理按键进阶版：增加长按功能
# 增加状态：LONG_DOWN, LONG_UP, LONG_PRESS
# 状态转换关系如下：
# 对于UP状态：button.value() == 0 时 转换为DOWN_delay
# 对于DOWN_delay状态：延时50ms，若button.value() == 0，则转换为DOWN; 若button.value() == 1，则转换为UP
# 对于DOWN状态：button.value() == 1 时 转换为LONG_DOWN
# 对于LONG_DOWN状态：延时500ms，若button.value() == 1，则转换为LONG_UP; 若button.value() == 0，则转换为UP
# 对于LONG_UP状态：延时500ms，若button.value() == 0，则转换为UP; 若button.value() == 1，则转换为LONG_PRESS
# 对于LONG_PRESS状态：延时500ms，若button.value() == 0，则转换为UP; 若button.value() == 1，则转换为LONG_UP
# 初始状态为UP

from machine import Pin
import time

button = Pin(22, Pin.IN, Pin.PULL_UP)

state = "UP"

def key_scan_StateMachine():
    global state
    if state == "UP":
        if button.value() == 0:
            state = "DOWN_delay"
    elif state == "DOWN_delay":
        time.sleep_ms(50)
        if button.value() == 0:
            state = "DOWN"
        elif button.value() == 1:
            state = "UP"
    elif state == "DOWN":
        if button.value() == 1:
            state = "LONG_DOWN"
    elif state == "LONG_DOWN":
        time.sleep_ms(500)
        if button.value() == 1:
            state = "LONG_UP"
        elif button.value() == 0:
            state = "UP"
    elif state == "LONG_UP":
        time.sleep_ms(500)
        if button.value() == 0:
            state = "UP"
        elif button.value() == 1:
            state = "LONG_PRESS"
    elif state == "LONG_PRESS":
        time.sleep_ms(500)
        if button.value() == 0:
            state = "UP"
        elif button.value() == 1:
            state = "LONG_UP"
    return state

while True:
    current_state = key_scan_StateMachine()
    if current_state == "DOWN":
        print("Short pressed!")
        time.sleep_ms(100)  # 防止抖动
    elif current_state == "LONG_PRESS":
        print("Long pressed!")
        time.sleep_ms(100)  # 长按后延时100ms再检测按键状态，防止抖动














# # 非阻塞按键检测与消抖
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
#         if (current == 0 and # 为什么是current == 0？因为按下时为0，松开时为1
#             time.ticks_diff(now, self.last_change) >= self.debounce_ms):
#             # 重置状态防止重复触发
#             self.last_state = 1
#             return True
#         return False 

# # 使用
# btn = Button(22)

# while True:
#     if btn.pressed():#pressed方法会返回True或False
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
# last_press_time = 0 # 这里为什么不是 last_press_time = time.ticks_ms()？答：因为 ticks_ms() 耗时，不宜在中断中使用，消抖的本质是延时，所以我们虽然有了中断，但下面还是把消抖放在主循环中。
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














# #关于time.sleep_ms()等延时函数，它们在延时过程中程序会进入阻塞状态，即CPU不会执行其他任务，直到延时结束吗？比如如果在延时时触发中断，是中断丢失还是延时结束后触发，亦或中止延时去执行中断处理函数？

# #答：这些延时函数在执行时，会暂停当前正在执行的任务，并切换到其他任务，直到延时结束。因此，它们不会影响其他任务的执行。
# #我想用按键中断的代码来验证这个问题。

# from machine import Pin
# import time

# button = Pin(22, Pin.IN, Pin.PULL_UP)


# def button_isr(pin):

#     print("Button pressed!")

# button.irq(trigger=Pin.IRQ_FALLING, handler=button_isr) # irq是Pin类的中断方法，第一个参数是中断类型，第二个参数是中断处理函数

# while True:
#     time.sleep_ms(100)  # 延时不会影响其他任务的执行
    








