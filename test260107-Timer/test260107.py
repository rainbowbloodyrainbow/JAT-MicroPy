# # Task1: 初识定时器
# # 使用定时器实现定时打印信息
# from machine import Timer



# def callback1(timer1):
#     print("Timer callback1")

# timer1 = Timer(0)
# timer1.init(period=1000, mode=Timer.PERIODIC, callback=callback1)
# # 我们创建了一个0号定时器的对象timer1，将它的周期(period，单位为ms)设为1000，
# # 触发模式为周期模式(PERIODIC)，还有另一种触发模式，是一次模式(ONE_SHOT)
# # callback参数，即回调函数，是每次触发定时器时执行的函数，为我们上面定义的callback1函数






# # Task2: Benny被邮差追杀
# from machine import Timer

# def day_end(timer1):
#     print("A day has passed")


# def Here_comes_CourierSix(timer1,timer2):
#     print("Benny, you dirty coward!")
#     print("Time to go die!")
#     timer1.deinit()

# timer1 = Timer(0)
# timer1.init(period=1000, mode=Timer.PERIODIC, callback=day_end)

# timer2 = Timer(1)
# timer2.init(period=5000, mode=Timer.ONE_SHOT, callback=Here_comes_CourierSix)

# # 如何让Benny被邮差杀掉后，定时器停止工作？
# # 答：只需在Here_comes_CourierSix函数中调用timer1.deinit(),即可让定时器1停止工作，而定时器2是单次触发的，所以不需要停止。














# Task3: Benny在九重天听熙熙攘攘，同时被追杀
from machine import Timer, Pin, PWM
import utime




def day_end(timer1):
    print("A day has passed")


def Here_comes_CourierSix(timer2):
    print("Benny, you dirty coward!")
    print("Time to go die!")
    timer1.deinit()

timer1 = Timer(0)
timer1.init(period=1000, mode=Timer.PERIODIC, callback=day_end)

timer2 = Timer(1)
timer2.init(period=50000, mode=Timer.ONE_SHOT, callback=Here_comes_CourierSix)






# ----- ESP32 PWM引脚（D15） -----
buzzer = PWM(Pin(4))  

# ----- 核心乐谱数据-----
#用字典来封装乐谱，好处是数据与逻辑分离，更换乐谱时只需修改数据部分，这是面向对象编程的思想之一
NOTES = {
    'NOTE_C0': 16,
    'NOTE_C1': 33,
    'NOTE_C2': 65,
    'NOTE_C3': 131,
    'NOTE_C4': 262,
    'NOTE_C5': 523,
    'NOTE_C6': 1047,
    'NOTE_C7': 2093,
    'NOTE_C8': 4186,
    'NOTE_CS0': 17,
    'NOTE_CS1': 35,
    'NOTE_CS2': 69,
    'NOTE_CS3': 139,
    'NOTE_CS4': 277,
    'NOTE_CS5': 554,
    'NOTE_CS6': 1109,
    'NOTE_CS7': 2217,
    'NOTE_CS8': 4435,
    'NOTE_D0': 18,
    'NOTE_D1': 37,
    'NOTE_D2': 73,
    'NOTE_D3': 147,
    'NOTE_D4': 294,
    'NOTE_D5': 587,
    'NOTE_D6': 1175,
    'NOTE_D7': 2349,
    'NOTE_D8': 4699,
    'NOTE_DS0': 19,
    'NOTE_DS1': 39,
    'NOTE_DS2': 78,
    'NOTE_DS3': 156,
    'NOTE_DS4': 311,
    'NOTE_DS5': 622,
    'NOTE_DS6': 1245,
    'NOTE_DS7': 2489,
    'NOTE_DS8': 4978,
    'NOTE_E0': 21,
    'NOTE_E1': 41,
    'NOTE_E2': 82,
    'NOTE_E3': 165,
    'NOTE_E4': 330,
    'NOTE_E5': 659,
    'NOTE_E6': 1319,
    'NOTE_E7': 2637,
    'NOTE_E8': 5274,
    'NOTE_F0': 22,
    'NOTE_F1': 44,
    'NOTE_F2': 87,
    'NOTE_F3': 175,
    'NOTE_F4': 349,
    'NOTE_F5': 698,
    'NOTE_F6': 1397,
    'NOTE_F7': 2794,
    'NOTE_F8': 5588,
    'NOTE_FS0': 23,
    'NOTE_FS1': 46,
    'NOTE_FS2': 93,
    'NOTE_FS3': 185,
    'NOTE_FS4': 370,
    'NOTE_FS5': 740,
    'NOTE_FS6': 1480,
    'NOTE_FS7': 2960,
    'NOTE_FS8': 5920,
    'NOTE_G0': 24,
    'NOTE_G1': 49,
    'NOTE_G2': 98,
    'NOTE_G3': 196,
    'NOTE_G4': 392,
    'NOTE_G5': 784,
    'NOTE_G6': 1568,
    'NOTE_G7': 3136,
    'NOTE_G8': 6272,
    'NOTE_GS0': 26,
    'NOTE_GS1': 52,
    'NOTE_GS2': 103,
    'NOTE_GS3': 207,
    'NOTE_GS4': 416,
    'NOTE_GS5': 831,
    'NOTE_GS6': 1663,
    'NOTE_GS7': 3325,
    'NOTE_GS8': 6651,
    'NOTE_A0': 28,
    'NOTE_A1': 55,
    'NOTE_A2': 110,
    'NOTE_A3': 220,
    'NOTE_A4': 440,
    'NOTE_A5': 880,
    'NOTE_A6': 1760,
    'NOTE_A7': 3520,
    'NOTE_A8': 7040,
    'NOTE_AS0': 29,
    'NOTE_AS1': 58,
    'NOTE_AS2': 117,
    'NOTE_AS3': 233,
    'NOTE_AS4': 466,
    'NOTE_AS5': 932,
    'NOTE_AS6': 1865,
    'NOTE_AS7': 3729,
    'NOTE_AS8': 7459,
    'NOTE_B0': 31,
    'NOTE_B1': 62,
    'NOTE_B2': 123,
    'NOTE_B3': 247,
    'NOTE_B4': 494,
    'NOTE_B5': 988,
    'NOTE_B6': 1976,
    'NOTE_B7': 3951,
    'NOTE_B8': 7902,
    'REST': 0
}


# 歌曲旋律（熙熙攘攘）：(音符, 节拍)
SONG = [
    ('NOTE_A3', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.15), ('NOTE_D4', 0.15), ('NOTE_C4', 0.25), ('NOTE_G3', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.25), ('NOTE_E3', 0.25),
    ('NOTE_A3', 0.25), ('NOTE_E4', 0.15), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.15), ('NOTE_D4', 0.15), ('NOTE_D4', 0.15), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25), ('NOTE_A3', 0.25), ('NOTE_A3', 0.15), ('NOTE_G3', 0.25), ('NOTE_E3', 0.25),
    ('NOTE_A3', 0.25), ('NOTE_G4', 0.15), ('NOTE_G4', 0.25), ('NOTE_E4', 0.15), ('NOTE_A3', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_E4', 0.15), ('NOTE_E4', 0.15), ('NOTE_D4', 0.15), ('NOTE_E4', 0.25), ('NOTE_D4', 0.15), ('NOTE_E4', 0.25), ('NOTE_D4', 0.15), ('NOTE_E4', 0.5),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_G4', 0.25), ('NOTE_D4', 0.5), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.125), ('NOTE_A3', 0.125),
    ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.5), ('NOTE_C5', 0.125), ('NOTE_B4', 0.125), ('NOTE_G4', 0.125),
    ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_G4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_C3', 0.125), ('NOTE_B4', 0.125), ('NOTE_G4', 0.125), ('NOTE_E4', 0.125),
    ('NOTE_E4', 0.125), ('NOTE_G4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_A4', 0.125), ('NOTE_G4', 0.125), ('NOTE_A4', 0.125), ('NOTE_B4', 0.125), ('NOTE_C5', 0.125),
    ('NOTE_D5', 0.125), ('NOTE_B4', 0.125), ('NOTE_C5', 0.125), ('NOTE_D5', 0.125), ('NOTE_B4', 0.125), ('NOTE_C5', 0.125), ('NOTE_G5', 0.125), ('NOTE_F5', 0.125), ('NOTE_E5', 0.125),
    ('NOTE_D5', 0.125), ('NOTE_C5', 0.125), ('NOTE_A5', 0.125), ('NOTE_G5', 0.125), ('NOTE_A5', 0.125), ('NOTE_B5', 0.125), ('NOTE_C6', 0.125), ('NOTE_B5', 0.125), ('NOTE_C6', 0.125),
    ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_G6', 0.125), ('NOTE_G6', 0.125), ('NOTE_E6', 0.125), ('NOTE_D6', 0.125), ('NOTE_C6', 0.125),
    ('NOTE_A5', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_A5', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_A5', 0.125), ('NOTE_G6', 0.125), ('NOTE_A6', 0.125),
    ('NOTE_E6', 0.125), ('NOTE_G6', 0.125), ('NOTE_A6', 0.125), ('NOTE_A5', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.25),
    ('NOTE_E3', 0.25), ('NOTE_E3', 0.125), ('NOTE_E3', 0.125), ('NOTE_D3', 0.25), ('NOTE_E3', 0.25), ('NOTE_G3', 0.25), ('NOTE_G3', 0.5),
    ('NOTE_E3', 0.25), ('NOTE_F3', 0.25), ('NOTE_G3', 0.25), ('NOTE_G3', 0.125), ('NOTE_G3', 0.25), ('NOTE_F3', 0.25), ('NOTE_E3', 0.25),
    ('NOTE_D3', 0.25), ('NOTE_D3', 0.25), ('NOTE_E3', 0.125), ('NOTE_E3', 0.25), ('NOTE_F3', 0.25), ('NOTE_E3', 0.5), ('NOTE_E3', 0.25),
    ('NOTE_E3', 0.125), ('NOTE_E3', 0.125), ('NOTE_D3', 0.25), ('NOTE_E3', 0.25), ('NOTE_F3', 0.25), ('NOTE_G3', 0.5), ('NOTE_E3', 0.25),
    ('NOTE_F3', 0.25), ('NOTE_G3', 0.25), ('NOTE_G3', 0.125), ('NOTE_G3', 0.25), ('NOTE_C4', 0.25), ('NOTE_B3', 0.25), ('NOTE_G3', 0.25),
    ('NOTE_D4', 0.25), ('NOTE_D4', 0.125), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_E4', 0.5), ('NOTE_E4', 0.25), ('NOTE_E4', 0.125),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_B3', 0.5), ('NOTE_G3', 0.25), ('NOTE_G3', 0.25), ('NOTE_A3', 0.5), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_E4', 0.5), ('NOTE_E3', 0.25), ('NOTE_E4', 0.5), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_B3', 0.5), ('NOTE_G3', 0.25), ('NOTE_G3', 0.25), ('NOTE_A3', 0.5), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_G4', 0.25), ('NOTE_D4', 0.5), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.125), ('NOTE_A3', 0.125), ('NOTE_A3', 0.125), ('NOTE_E3', 0.125), ('NOTE_G3', 0.25), ('NOTE_D3', 0.25), ('NOTE_E3', 0.25), ('NOTE_A2', 0.125),
    ('NOTE_D3', 0.25), ('NOTE_E3', 0.25), ('NOTE_A4', 0.25), ('NOTE_C5', 0.25), ('NOTE_D5', 0.25), ('NOTE_A4', 0.25), ('NOTE_E5', 0.125), ('NOTE_G5', 0.125), ('NOTE_E5', 0.125), ('NOTE_C5', 0.125), ('NOTE_C5', 0.25), ('NOTE_D5', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.125),
    ('NOTE_A3', 0.125), ('NOTE_A3', 0.125), ('NOTE_E3', 0.125), ('NOTE_G3', 0.25), ('NOTE_D3', 0.125), ('NOTE_E3', 0.125), ('NOTE_D3', 0.25),
    ('NOTE_D3', 0.25), ('NOTE_E3', 0.125), ('NOTE_C6', 0.25), ('NOTE_B5', 0.25), ('NOTE_G5', 0.25), ('NOTE_E5', 0.25), ('NOTE_D5', 0.125),
    ('NOTE_C5', 0.125), ('NOTE_D5', 0.125), ('NOTE_A5', 0.125), ('NOTE_A3', 0.25), ('NOTE_B3', 0.125), ('NOTE_C4', 0.25), ('NOTE_B3', 0.125),
    ('NOTE_G3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.125), ('NOTE_E3', 0.25), ('NOTE_E3', 0.25), ('NOTE_E3', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_C3', 0.125), ('NOTE_B3', 0.125), ('NOTE_G3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_A3', 0.25), ('NOTE_A3', 0.25),
    ('NOTE_A4', 0.25), ('NOTE_D4', 0.125), ('NOTE_C4', 0.125), ('NOTE_D4', 0.125), ('NOTE_D4', 0.125), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_C4', 0.5), ('NOTE_E4', 0.25), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_B3', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.5), ('NOTE_D4', 0.5), ('NOTE_E4', 0.25),
    ('NOTE_F4', 0.125), ('NOTE_F4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.5), ('NOTE_E4', 0.150), ('NOTE_E4', 0.2), ('NOTE_B3', 0.25),
    ('NOTE_G3', 0.25), ('NOTE_B3', 0.25), ('NOTE_C4', 0.25), ('NOTE_B3', 0.125), ('NOTE_C4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125),
    ('NOTE_E4', 0.125), ('NOTE_D4', 0.125), ('NOTE_C4', 0.125), ('NOTE_E4', 0.25), ('NOTE_A4', 0.25), ('NOTE_G4', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_A3', 0.25), ('NOTE_E4', 0.125), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_B3', 0.125), ('NOTE_B3', 0.125), ('NOTE_G3', 0.25), ('NOTE_C4', 0.25), ('NOTE_G4', 0.125), ('NOTE_G4', 0.25), ('NOTE_F4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_C4', 0.25), ('NOTE_G3', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_G4', 0.25), ('NOTE_E4', 0.25), ('NOTE_B3', 0.25), ('NOTE_D4', 0.5), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_C4', 0.125), ('NOTE_D4', 0.125), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_D4', 0.25), ('NOTE_C4', 0.125), ('NOTE_D4', 0.125), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_C4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.25), ('NOTE_G4', 0.25), ('NOTE_G4', 0.5), ('NOTE_A4', 0.5), ('NOTE_G4', 0.5),
    ('NOTE_E4', 0.25), ('NOTE_E4', 0.125), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_C4', 0.5), ('NOTE_C4', 0.125), ('NOTE_C4', 0.125), ('NOTE_C4', 0.125),
    ('NOTE_C4', 0.125), ('NOTE_C4', 0.125), ('NOTE_C4', 0.125), ('NOTE_C4', 0.125), ('NOTE_C4', 0.125), ('NOTE_C4', 0.25), ('NOTE_G4', 0.25),
    ('NOTE_C4', 0.5), ('NOTE_E4', 0.5), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_G4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125),
    ('NOTE_D4', 0.125), ('NOTE_D4', 0.125), ('NOTE_C4', 0.25), ('NOTE_C4', 0.125), ('NOTE_A3', 0.25), ('NOTE_A3', 0.125), ('NOTE_G3', 0.25),
    ('NOTE_E3', 0.25), ('NOTE_A3', 0.25), ('NOTE_E4', 0.125), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_C4', 0.25),
    ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_D4', 0.125), ('NOTE_D4', 0.125), ('NOTE_C4', 0.25), ('NOTE_C4', 0.125),
    ('NOTE_A3', 0.25), ('NOTE_A3', 0.125), ('NOTE_G3', 0.25), ('NOTE_E3', 0.25), ('NOTE_A3', 0.25), ('NOTE_G4', 0.125), ('NOTE_G4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125),
    ('NOTE_D4', 0.125), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_E4', 0.5), ('NOTE_E4', 0.25),
    ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_C4', 0.25), ('NOTE_G4', 0.25), ('NOTE_D4', 0.5), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.125), ('NOTE_E4', 0.25),
    ('NOTE_A3', 0.25), ('NOTE_A3', 0.125), ('NOTE_A3', 0.125), ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_A3', 0.125),
    ('NOTE_G3', 0.125), ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_E4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_D4', 0.25), ('NOTE_C4', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.5), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.25),
    ('NOTE_A3', 0.25), ('NOTE_E4', 0.25), ('NOTE_A3', 0.25), ('NOTE_G3', 0.25), ('NOTE_A3', 0.25), ('NOTE_A3', 0.25), ('NOTE_E4', 0.25),
    ('NOTE_E5', 0.25), ('NOTE_D5', 0.25), ('NOTE_C5', 0.25), ('NOTE_B4', 0.25), ('NOTE_G4', 0.25), ('NOTE_A3', 0.25), ('NOTE_A3', 0.125),
    ('NOTE_A3', 0.125), ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_A3', 0.125), ('NOTE_G3', 0.125), ('NOTE_A3', 0.125),
    ('NOTE_G3', 0.125), ('NOTE_A3', 0.25), ('NOTE_F4', 0.125), ('NOTE_G4', 0.25), ('NOTE_G4', 0.25), ('NOTE_E4', 0.25), ('NOTE_D4', 0.25),
    ('NOTE_C4', 0.25), ('NOTE_E4', 0.5), ('NOTE_A3', 0.5), ('NOTE_C5', 0.125), ('NOTE_B4', 0.125), ('NOTE_G4', 0.125), ('NOTE_E4', 0.125),
    ('NOTE_E4', 0.125), ('NOTE_G4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_C5', 0.125), ('NOTE_B4', 0.125), ('NOTE_G4', 0.125),
    ('NOTE_E4', 0.125), ('NOTE_E4', 0.125), ('NOTE_G4', 0.125), ('NOTE_D4', 0.125), ('NOTE_E4', 0.125), ('NOTE_A4', 0.125), ('NOTE_G4', 0.125),
    ('NOTE_A4', 0.125), ('NOTE_B4', 0.125), ('NOTE_C5', 0.125), ('NOTE_D5', 0.125), ('NOTE_B4', 0.125), ('NOTE_C5', 0.125), ('NOTE_D5', 0.125),
    ('NOTE_B4', 0.125), ('NOTE_C5', 0.125), ('NOTE_G5', 0.125), ('NOTE_F5', 0.125), ('NOTE_E5', 0.125), ('NOTE_D5', 0.125), ('NOTE_C5', 0.125),
    ('NOTE_A5', 0.125), ('NOTE_G5', 0.125), ('NOTE_A5', 0.125), ('NOTE_B5', 0.125), ('NOTE_C6', 0.125), ('NOTE_B5', 0.125), ('NOTE_C6', 0.125),
    ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_G6', 0.125), ('NOTE_G6', 0.125), ('NOTE_E6', 0.125),
    ('NOTE_D6', 0.125), ('NOTE_C6', 0.125), ('NOTE_A5', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.125), ('NOTE_A5', 0.125), ('NOTE_D6', 0.125),
    ('NOTE_E6', 0.125), ('NOTE_A5', 0.125), ('NOTE_G6', 0.125), ('NOTE_A6', 0.125), ('NOTE_E6', 0.125), ('NOTE_G6', 0.125), ('NOTE_A6', 0.125),
    ('NOTE_A5', 0.125), ('NOTE_D6', 0.125), ('NOTE_E6', 0.25), ('NOTE_C5', 0.25), ('NOTE_B4', 0.25), ('NOTE_G4', 0.25), ('NOTE_A4', 0.25),
    ('NOTE_E4', 0.25), ('NOTE_G4', 0.25), ('NOTE_D4', 0.25), ('NOTE_E4', 0.25), ('NOTE_C4', 0.25), ('NOTE_D4', 0.25), ('NOTE_B3', 0.25),
    ('NOTE_C4', 0.25), ('NOTE_G3', 0.25), ('NOTE_B3', 0.25), ('NOTE_E3', 0.25), ('NOTE_G3', 0.25), ('NOTE_A3', 0.5), ('NOTE_E4', 0.5),
    ('NOTE_D4', 0.5), ('NOTE_E4', 0.5), ('NOTE_B3', 0.5), ('NOTE_A3', 0.5), ('NOTE_C4', 0.5), ('NOTE_D4', 0.5), ('NOTE_E4', 0.5),
    ('NOTE_G4', 0.5), ('NOTE_A4', 0.5)
]


# 歌曲速度：每拍持续时间（秒）
BEAT_DURATION = 0.5

# ----- 核心播放函数-----
def play_note(note, duration_beats):
    """播放单个音符,包含PWM频率设置与持续时间控制"""
    frequency = NOTES.get(note, 0)
    
    if frequency > 0:
        buzzer.freq(frequency)  # 直接调用PWM的freq方法
        buzzer.duty_u16(32768)  # 50%占空比（控制音量）
    
    utime.sleep(duration_beats * BEAT_DURATION)
    
    buzzer.duty_u16(0)  # 停止发声
    utime.sleep(0.05)  # 音符间隔 

# ----- 主循环-----
print("音乐播放器已启动...")

while True:
    print("\n--- Playing '熙熙攘攘我们的城市' ---")
    for note, beats in SONG:
        play_note(note, beats)
    
    print("--- Song Finished. Restarting in 2 seconds. ---")
    utime.sleep(2)

# 呃，回到那个老问题，我们可以在Benny被杀后停止播放音乐吗？
# 答：添加一个标志位Music,While循环中判断Music是否为True,如果为True才正常播放音乐
# 然后在Here_comes_CourierSix中,加一行Music = False 即可
# 修改如下
# Music = True

# Here_comes_CourierSix修改如下：
# def Here_comes_CourierSix(timer2):
#     print("Benny, you dirty coward!")
#     print("Time to go die!")
#     timer1.deinit()
#     Music = False

# While循环修改如下：
# while Music:
#     print("\n--- Playing '熙熙攘攘我们的城市' ---")
#     for note, beats in SONG:
#         play_note(note, beats)
    
#     print("--- Song Finished. Restarting in 2 seconds. ---")
#     utime.sleep(2)
# 奇怪，这不起作用，我回头再想想吧