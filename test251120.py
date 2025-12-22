# from machine import Pin, PWM
# import time
# print("Hello, ESP32!")
# led = Pin(25,Pin.OUT)
# led2 = Pin(4 ,Pin.OUT)

# while True:
#     led.on()
#     led2.value(not led.value())
#     time.sleep(0.25)    
#     led.off()
#     led2.value(not led.value())        
#     time.sleep(0.25)    
# led_pwm = PWM(Pin(2),freq = 500)
# duty = 0
# step = 10
# delay = 0.02
# direction = 1
# while True:
#     duty += step * direction
#     if duty >= 1023:
#         duty = 1023
#         direction = -1
#     elif duty <= 0:
#         duty = 0
#         direction = 1
#     led_pwm.duty(duty)
#     time.sleep(delay)

#for循环实现呼吸灯

# while True:
#     for duty in range(0,1024,step):
#         pwm.duty(duty)
#         time.sleep(delay)
#         if duty == 1023:
#             print("最亮")
#     for duty in range(1023,-1,-step):
#         pwm.duty(duty)
#         time.sleep(delay)
#         if duty == 0:
#             print("最暗")

#有没有办法不依靠while True？


