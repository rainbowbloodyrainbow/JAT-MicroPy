# #任务一：复习呼吸灯
# import time
# from machine import Pin, PWM
# led_pwm = PWM(Pin(14),freq = 500)

# duty = 0
# step = 10
# delay = 0.02
# while True:
#     for duty in range(0,1024,step):
#         led_pwm.duty(duty)
#         time.sleep(delay)
#         if duty == 1023:
#             print("最亮")
#     for duty in range(1023,-1,-step):
#         pwm.duty(duty)
#         time.sleep(delay)
#         if duty == 0:
#             print("最暗")














# #任务二：pwm控制舵机
# import machine
# import time

# pwm = machine.PWM(machine.Pin(15), freq=50)#舵机的频率为50Hz，这是舵机通信协议规定的
# def set_servo_angle(angle):
#     if 0 <= angle <= 180:
#         duty_ns = int(500000 + (angle / 180) * 200000)
#         pwm.duty_ns(duty_ns)#wokwi中使用ns来设定脉冲宽度，500000ns对应0度，2500000ns对应180度
# print("初始化舵机到0度")#程序开始时，不只是舵机，务必把led,继电器，电机等执行器件初始化到一个安全状态
# set_servo_angle(0)
# time.sleep(1)
# while True:
#     print("Turning to 90 degrees")
#     set_servo_angle(90)
#     time.sleep(2)
#     print("Turning to 180 degrees")
#     set_servo_angle(135)
#     time.sleep(2)

# #以上程序有什么问题？




# #这是老师给的代码
# import machine
# import time

# # ----- 1：适配ESP32 PWM引脚-----
# # ESP32 D15支持PWM功能
# pwm = machine.PWM(machine.Pin(15),freq=50)
# # 设置PWM频率为50Hz（伺服电机标准频率）

# # ----- 核心逻辑：伺服电机角度控制函数-----
# def set_servo_angle(angle):
#     if 0 <= angle <= 180:
#         # 将角度(0-180)映射到脉冲宽度(500k-2.5M纳秒)，适配Wokwi舵机特性
#         duty_ns = int(500000 + (angle / 180) * 2000000)
#         pwm.duty_ns(duty_ns)
# # ----- 关键修正：初始化位置-----
# # 确保电机启动后有明确位置
# print("初始化位置：关闭 (0度)")
# set_servo_angle(0)
# time.sleep(1) # 等待1秒，确保电机到位

# # ----- 主循环：开关测试-----
# while True:
#     print("开启 (90度)")
#     set_servo_angle(135)
#     time.sleep(2)
    
#     print("关闭 (0度)")
#     set_servo_angle(0)
#     time.sleep(2)














# #任务三：串口控制舵机和LED
import sys
import time
import machine

# ----- 关键修改1：适配ESP32硬件引脚-----
print("Initializing hardware...")
# LED：ESP32用D15，输出模式
led = machine.Pin(15, machine.Pin.OUT)
led.off()  # 初始状态关闭

# 伺服电机：ESP32用D2，PWM模式（频率50Hz，与原代码一致）
servo_pwm = machine.PWM(machine.Pin(2))
servo_pwm.freq(50)

# ----- 核心函数：伺服电机角度控制-----
def set_servo_angle(angle):
    """设置伺服电机角度（0-180度）"""
    if 0 <= angle <= 180:
        # 映射角度到脉冲宽度（500k-2.5M纳秒，适配舵机标准）
        duty_ns = int(500000 + (angle / 180) * 2000000)
        servo_pwm.duty_ns(duty_ns)
        print(f"伺服电机已转到 {angle} 度")
    else:
        print("错误: 角度必须在0-180之间")

# ----- 主程序：串口指令解析-----
print("远程命令解析器已就绪。")
print("可用指令: 'led on', 'led off', 'servo:角度值'")
set_servo_angle(0)  # 伺服电机初始位置（与原代码一致）

while True:
    # 读取串口输入指令
    command = sys.stdin.readline()
    
    if command:
        # 清理指令（去除空格、转为小写，不区分大小写）
        clean_command = command.strip().lower()
        print(f"\n收到指令: '{clean_command}'")
        
        # 解析LED控制指令
        if clean_command == "led on":
            led.on()
            print("LED已点亮")
        elif clean_command == "led off":
            led.off()
            print("LED已熄灭")
            
        # 解析伺服电机控制指令（格式：servo:角度值）
        elif clean_command.startswith("servo:"):
            try:
                parts = clean_command.split(':')
                angle_value = int(parts[1])
                set_servo_angle(angle_value)
            except (IndexError, ValueError):
                print("错误: servo指令格式不正确，应为 'servo:角度值'")
        
        # 未知指令处理
        else:
            print(f"未知指令: '{clean_command}'")