# import machine
# import time
# # 配置LED和按键
# led = machine.Pin(21, machine.Pin.OUT)
# button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
# # 中断回调函数
# def button_pressed(pin):
#     led.value(not led.value()) # 切换LED状态
# # 注册中断（下降沿触发）
# button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)
# # 主循环保持运行
# while True:
#     pass # 中断处理在后台进行














# import machine
# import time

# # 配置两个按键和LED
# leds = [machine.Pin(21, machine.Pin.OUT), machine.Pin(25, machine.Pin.OUT)]
# btn_up = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
# btn_down = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)

# # 共享状态（使用列表避免全局变量问题）
# state = [0]  # 使用列表封装状态，便于在回调中修改
# def increment(pin):
#     state[0] = (state[0] + 1) % 4
#     update_leds()
# def decrement(pin):
#     state[0] = (state[0] - 1) % 4
#     update_leds()
# def update_leds():
#     # 根据状态值点亮相应LED
#     for i in range(2):
#         leds[i].value(1 if (state[0] >> i) & 1 else 0)
# # 注册中断
# btn_up.irq(trigger=machine.Pin.IRQ_FALLING, handler=increment)
# btn_down.irq(trigger=machine.Pin.IRQ_FALLING, handler=decrement)
# # 初始化LED
# update_leds()
# # 主循环
# while True:
#     pass













# # 导入 machine 模块，用于控制微控制器的硬件（如 GPIO 引脚） 
# import machine 

# # 导入 time 模块，用于获取时间、实现延时或去抖动 
# import time 

# # ========== 硬件配置部分 ==========

# # 创建一个包含两个 LED 的列表： # - 第一个 LED 接在 GPIO 21 引脚，设置为输出模式（OUT） # - 第二个 LED 接在 GPIO 25 引脚，也设置为输出模式 # 注意：Pin.OUT 表示这个引脚用来"输出"高低电平，从而控制 LED 亮灭 
# leds = [ 
#     machine.Pin(21, machine.Pin.OUT),   # leds[0] 对应 GPIO21 
#     machine.Pin(25, machine.Pin.OUT)   ] # leds[1] 对应 GPIO25 ]

# # 配置"增加"按键（Up 按键）： # - 接在 GPIO 22 # - 设置为输入模式（IN） # - 启用内部上拉电阻（PULL_UP）：当按键没按下时，引脚默认是高电平（1）；按下时接地变成低电平（0） 
# btn_up = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP) 

# # 配置"减少"按键（Down 按键）： # - 接在 GPIO 23 # - 同样设置为输入 + 内部上拉 
# btn_down = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP) 

# # ========== 全局状态变量 ==========

# # 使用一个列表来保存当前的状态值（0 到 3） # 为什么用列表？因为在 Python 中，普通变量在函数内部不能直接修改全局值， # 而列表是"可变对象"，可以在函数里修改它的内容（比如 state[0] = ...） 
# state = [0]  # 初始状态为 0（两个 LED 都灭） 

# # 记录上次 Up 按键被按下的时间（单位：毫秒） # 同样用列表，方便在回调函数中修改 
# last_up_time = [0] 

# # 记录上次 Down 按键被按下的时间 
# last_down_time = [0] 

# # 定义去抖动的时间阈值：200 毫秒 # 机械按键按下时会有"抖动"（几毫秒内反复通断），我们只认第一次有效按下， # 之后 200 毫秒内的任何信号都当作抖动忽略 
# DEBOUNCE_DELAY_MS = 5000

# # ========== 功能函数定义 ==========

# def increment(pin): 
#     """
#     当 Up 按键被按下时调用此函数（由中断触发） 
#     参数 'pin' 是触发中断的引脚对象（这里用不到，但必须保留） 
#     """
#     # 获取当前系统运行时间（从开机到现在经过了多少毫秒） 
#     current = time.ticks_ms() 
    
#     # 计算距离上次 Up 按键触发过了多久 
#     # time.ticks_diff(a, b) 安全地计算 a - b（即使计时器溢出也不会错） 
#     if time.ticks_diff(current, last_up_time[0]) < DEBOUNCE_DELAY_MS: 
#         return  # 如果还没过 200ms，说明是抖动，直接退出，不做任何操作 
    
#     # 更新上次 Up 按键的时间为现在 
#     last_up_time[0] = current 
    
#     # 将状态值加 1，并对 4 取模（确保值始终在 0~3 之间循环） 
#     # 例如：3 + 1 = 4 → 4 % 4 = 0 
#     state[0] = (state[0] + 1) % 4 
    
#     # 更新 LED 显示 
#     update_leds() 

# def decrement(pin): 
#     """
#     当 Down 按键被按下时调用此函数（由中断触发） 
#     """
#     current = time.ticks_ms() 
    
#     # 检查是否在去抖时间内 
#     if time.ticks_diff(current, last_down_time[0]) < DEBOUNCE_DELAY_MS: 
#         return  # 抖动，忽略 
    
#     last_down_time[0] = current 
    
#     # 将状态值减 1，并对 4 取模 
#     # Python 中负数取模会自动转为正数：-1 % 4 = 3，-2 % 4 = 2，等等 
#     state[0] = (state[0] - 1) % 4 
    
#     update_leds() 

# def update_leds(): 
#     """
#     根据当前状态值（0~3）控制两个 LED 的亮灭 
#     状态用 2 位二进制表示： 
#         状态 0 → 00 → 两个都灭 
#         状态 1 → 01 → LED0 亮（GPIO21） 
#         状态 2 → 10 → LED1 亮（GPIO25） 
#         状态 3 → 11 → 两个都亮 
#     """
#     # 循环处理两个 LED（i = 0 和 i = 1） 
#     for i in range(2): 
#         # 检查状态值的第 i 位是否为 1： 
#         # - (state[0] >> i) 把第 i 位移到最低位 
#         # - & 1 取出最低位的值（0 或 1） 
#         bit = (state[0] >> i) & 1 
        
#         # 如果这一位是 1，LED 点亮（输出高电平）；否则熄灭（输出低电平） 
#         # 注意：这假设你的 LED 是"高电平点亮"（即 GPIO 输出 1 时 LED 亮） 
#         leds[i].value(1 if bit else 0) 

# # ========== 中断注册 ==========

# # 为 Up 按键设置中断： # - trigger=machine.Pin.IRQ_FALLING：当引脚电平从高变低时触发（即按键按下瞬间） # - handler=increment：触发时调用 increment 函数 
# btn_up.irq(trigger=machine.Pin.IRQ_FALLING, handler=increment) 

# # 为 Down 按键设置中断（同样在下降沿触发） 
# btn_down.irq(trigger=machine.Pin.IRQ_FALLING, handler=decrement) 

# # ========== 初始化 ==========

# # 程序开始时，根据初始状态（state[0] = 0）设置 LED 
# update_leds() 

# # ========== 主程序循环 ==========

# # 主循环什么都不做（pass） # 因为所有操作都由"中断"自动完成，不需要轮询 # 微控制器会在这里空转，等待按键中断发生 
# while True: 
#     pass















import machine
import time

SHORT_PRESS = 300   # 短按阈值：300ms
LONG_PRESS = 1000   # 长按阈值：1000ms

led = machine.Pin(21, machine.Pin.OUT)
button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
# 状态定义
STATE_WAITING = 0
STATE_PRESSED = 1
STATE_LONG_PRESS = 2

state = STATE_WAITING
press_start = 0
while True:
    current_state = button.value()
    current_time = time.ticks_ms()
    
    if state == STATE_WAITING:
        if current_state == 0:  # 按键按下
            press_start = current_time
            state = STATE_PRESSED
    
    elif state == STATE_PRESSED:
        if current_state == 1:  # 按键释放
            # 检查是否为短按
            if time.ticks_diff(current_time, press_start) < SHORT_PRESS:
                # 短按：切换LED
                led.value(not led.value())
            state = STATE_WAITING
        
        elif time.ticks_diff(current_time, press_start) > LONG_PRESS:
            # 检测到长按
            state = STATE_LONG_PRESS
            # 长按动作：例如全亮
            led.value(1)
    
    elif state == STATE_LONG_PRESS:
        if current_state == 1:  # 按键释放
            state = STATE_WAITING
        # 长按持续动作可在此添加
    
    time.sleep_ms(10)








#以上代码都使用如下接线
# {
#   "version": 1,
#   "author": "Anonymous maker",
#   "editor": "wokwi",
#   "parts": [
#     {
#       "type": "wokwi-esp32-devkit-v1",
#       "id": "esp",
#       "top": -49.57,
#       "left": -97.12,
#       "attrs": { "env": "micropython-20220618-v1.19.1" }
#     },
#     {
#       "type": "wokwi-pushbutton",
#       "id": "btn1",
#       "top": 17.27,
#       "left": 201.07,
#       "attrs": { "color": "green" }
#     },
#     {
#       "type": "wokwi-led",
#       "id": "led1",
#       "top": -54.27,
#       "left": 115.27,
#       "attrs": { "color": "red" }
#     },
#     {
#       "type": "wokwi-resistor",
#       "id": "r1",
#       "top": 121.68,
#       "left": 139.73,
#       "rotate": 270,
#       "attrs": { "value": "1000" }
#     },
#     {
#       "type": "wokwi-led",
#       "id": "led2",
#       "top": -58.93,
#       "left": 62.6,
#       "attrs": { "color": "green" }
#     },
#     {
#       "type": "wokwi-pushbutton",
#       "id": "btn2",
#       "top": 96.6,
#       "left": 208.4,
#       "attrs": { "color": "green" }
#     },
#     {
#       "type": "wokwi-resistor",
#       "id": "r2",
#       "top": 118.5,
#       "left": 58.64,
#       "attrs": { "value": "1000" }
#     }
#   ],
#   "connections": [
#     [ "esp:TX0", "$serialMonitor:RX", "", [] ],
#     [ "esp:RX0", "$serialMonitor:TX", "", [] ],
#     [ "btn1:2.l", "esp:GND.1", "green", [ "h0" ] ],
#     [ "led1:A", "r1:2", "green", [ "v0" ] ],
#     [ "led1:C", "esp:GND.1", "green", [ "v0" ] ],
#     [ "btn2:2.l", "esp:GND.1", "green", [ "h0" ] ],
#     [ "btn2:1.l", "esp:D23", "green", [ "h0" ] ],
#     [ "led2:C", "esp:GND.1", "green", [ "v0" ] ],
#     [ "led2:A", "r2:2", "green", [ "v0" ] ],
#     [ "esp:D25", "r2:1", "green", [ "h0" ] ],
#     [ "btn1:1.l", "esp:D22", "green", [ "h0" ] ],
#     [ "r1:1", "esp:D21", "green", [ "h0" ] ]
#   ],
#   "dependencies": {}
# }


from machine import Pin
import time

class Button:
    def __init__(self, pin_num, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self.last_state = self.pin.value()
        self.last_change = time.ticks_ms()

    def pressed(self):
        current = self.pin.value()
        now = time.ticks_ms()
        
        if current != self.last_state:
            self.last_change = now
            self.last_state = current
# 检测下降沿（按下）且已稳定
        if (current == 0 and 
            time.ticks_diff(now, self.last_change) >= self.debounce_ms):
            # 重置状态防止重复触发
            self.last_state = 1
            return True
        return False

# 使用
btn = Button(4)


# GPIO 引脚（a 到 dp）
pins = [25,26,14,12,13,33,32,27]
segment_pins = [Pin(p, Pin.OUT) for p in pins]

# 共阳段码表
SEGMENTS_CA = {
    '0': (0,0,0,0,0,0,1,1),
    '1': (1,0,0,1,1,1,1,1),
    '2': (0,0,1,0,0,1,0,1),
    '3': (0,0,0,0,1,1,0,1),
    '4': (1,0,0,1,1,0,0,1),
    '5': (0,1,0,0,1,0,0,1),
    '6': (0,1,0,0,0,0,0,1),
    '7': (0,0,0,1,1,1,1,1),
    '8': (0,0,0,0,0,0,0,1),
    '9': (0,0,0,0,1,0,0,1),
    ' ': (1,1,1,1,1,1,1,1),
}

def show_char(char):
    bits = SEGMENTS_CA.get(char, SEGMENTS_CA[' '])
    for pin, bit in zip(segment_pins, bits):
        pin.value(bit)

# 测试：循环显示 0-9
# 现在我想改成按键切换显示数字，每次按键显示下一个数字
digit = 0
while True:
    
    if btn.pressed():
        digit = (digit + 1) % 10
    show_char(str(digit))#str(digit)和直接digit有什么区别？答：str(digit)将数字转换为字符串，方便查找对应的段码；直接digit是整数，无法直接用于字典查找
    time.sleep(1)





from machine import Pin
from machine import Timer
import utime
'''===================LED管脚配置======================'''
Led_G = Pin(15,Pin.OUT)
key = Pin( 4,Pin.IN , Pin.PULL_UP)
#==============外部输入中断 配置 及 中断服务函数==========
Show_Num=0
def Key_trig(t):  #t可以省略吗？答
    #注意 diagram中按钮设置了"bounce": "0"，没有抖动 
    global Show_Num  # 使用外部的全局变量
    Show_Num = Show_Num+1
    if Show_Num>=10:
        Show_Num=0
    print(f"数码管显示的数字为：{Show_Num} ")
key.irq(trigger=Pin.IRQ_FALLING, handler=Key_trig)
'''=========8位数码管显示  ========================================================'''
#===================8位数码管==============================
'''
数码管默认共阳极,相应的段为0 时，亮
输出的数据与数码管段的对应关系
D25  D26  D14  D12  D13  D33  D32  D27
 a    b    c    d    e    f    g   DP
'''
Seg_pins = [27,32, 33, 13, 12, 14, 26, 25]  # 依次为DP g f e d c b a 
#代码里的Seg_pins列表是从dp开始到a，与我们平时的习惯正好相反，为什么没造成乱码呢？答：因为在Seg_Show函数中，输出是根据dis_table中的值按位处理的，与列表顺序无关，只要每个位对应正确即可
Segs = [Pin(pin, Pin.OUT,value=1) for pin in Seg_pins]
dis_table = [0x03, 0x9F, 0x25, 0x0D, 0x99, 0x49, 0x41, 0x1F, 0x01, 0x09]
#这些数分别对应二进制的0000 0011, 1001 1111, 0010 0101, 0000 1101, 1001 1001,0100 1001, 0100 0001, 0001 1111, 0000 0001, 0000 1001
#即分别对应数字0~9的段选状态
#注意0表示点亮，1表示熄灭
#定义数码管输出的函数  
# num:   要显示的数字 0~9  
# dp:    小数点状态   0：点亮  1：熄灭
def Seg_Show(num,dp) :
    # 设置是否显示小数点
    if dp==0:
        b=0xFF
    else :
        b=0xFE
    a = dis_table[num]&b       #比如要显示数字3，dp=1，则a=0x0D & 0xFE=0x0C;dp=0，则a=0x0D & 0xFF=0x0D;其实差别就是最后一位是否需要点亮
    # 输出要显示的段(包括DP)
    for i in range(8):      
        bit = (a >> i) & 1      #比如a=0x0D=0000 1101，则a>>1 = 0000 0110 &1=0; a>>2=0000 0011 &1=1; a>>3=0000 0001 &1=1; a>>4=0000 0000 &1=0;依次类推 
        Segs[i].value(bit)      # 管脚输出，置段状态（0点亮，1熄灭） 

'''=================== ========================================================'''
#/****************************主循环****************************************************/
while True: 
    Led_G.value(not Led_G.value())  #指示灯闪烁指示主循环正常进行
    Seg_Show(Show_Num,0)    
    utime.sleep_ms(200)       
#/*************************************************************************************/

{
  "version": 1,
  "author": "Anonymous maker",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-esp32-devkit-v1",
      "id": "esp",
      "top": 46.03,
      "left": 303.4,
      "attrs": { "env": "micropython-20220618-v1.19.1" }
    },
    {
      "type": "wokwi-led",
      "id": "led2",
      "top": 175.14,
      "left": 467.65,
      "attrs": { "color": "green", "flip": "1" }
    },
    {
      "type": "wokwi-led",
      "id": "led4",
      "top": 222.87,
      "left": 468.89,
      "attrs": { "color": "red", "flip": "1" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r1",
      "top": 212.66,
      "left": 497.22,
      "attrs": { "value": "1000" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r2",
      "top": 261,
      "left": 497.69,
      "attrs": { "value": "1000" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn2",
      "top": 79.46,
      "left": 512.82,
      "attrs": { "color": "blue", "bounce": "0" }
    },
    { "type": "wokwi-7segment", "id": "sevseg15", "top": 150.08, "left": 106.34, "attrs": {} },
    {
      "type": "wokwi-vcc",
      "id": "vcc5",
      "top": 352.34,
      "left": -566.58,
      "rotate": 180,
      "attrs": {}
    }
  ],
  "connections": [
    [ "esp:TX0", "$serialMonitor:RX", "", [] ],
    [ "esp:RX0", "$serialMonitor:TX", "", [] ],
    [ "esp:GND.1", "r1:2", "black", [ "h50.36", "v35.57", "h100.96" ] ],
    [ "led2:C", "r1:1", "green", [ "v0" ] ],
    [ "esp:D15", "led2:A", "green", [ "h59.18", "v25.78" ] ],
    [ "led4:C", "r2:1", "green", [ "v0" ] ],
    [ "r1:2", "r2:2", "black", [ "v0" ] ],
    [ "esp:D4", "btn2:1.l", "green", [ "h47.19", "v-0.15", "h123.98", "v-77.36" ] ],
    [ "btn2:2.r", "r1:2", "black", [ "h24.79", "v122.2", "h-120.55" ] ],
    [ "esp:3V3", "led4:A", "red", [ "h20.81", "v60.34" ] ],
    [ "esp:D32", "sevseg15:G", "green", [ "h0" ] ],
    [ "esp:D33", "sevseg15:F", "green", [ "h0" ] ],
    [ "esp:D25", "sevseg15:A", "green", [ "h0" ] ],
    [ "esp:D26", "sevseg15:B", "green", [ "h0" ] ],
    [ "esp:D27", "sevseg15:DP", "green", [ "h-140.77", "v82.34", "h-17.49" ] ],
    [ "esp:D14", "sevseg15:C", "green", [ "h-129.11", "v81.89", "h-29.15" ] ],
    [ "esp:D12", "sevseg15:D", "green", [ "h-118.42", "v80.23", "h-38.87" ] ],
    [ "esp:D13", "sevseg15:E", "green", [ "h-107.73", "v80.85", "h-61.21" ] ],
    [ "esp:3V3", "sevseg15:COM.1", "green", [ "v93.04", "h-243.22" ] ]
  ],
  "dependencies": {}
}