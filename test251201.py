#测试1，静态显示数字5

#从上节课的代码改
# from machine import Pin
# from machine import Timer
# import utime
# Show_Num=5
# Seg_pins = [27,32, 33, 13, 12, 14, 26, 25]  # 依次为DP g f e d c b a 
# # Seg_pins = [25,26, 14, 12, 13, 33, 32, 27]
# Segs = [Pin(pin, Pin.OUT,value=1) for pin in Seg_pins]
# dis_table = [0x03, 0x9F, 0x25, 0x0D, 0x99, 0x49, 0x41, 0x1F, 0x01, 0x09]
# def Seg_Show(num,dp) :
#     # 设置是否显示小数点
#     if dp==0:
#         b=0xFF
#     else :
#         b=0xFE
#     a = dis_table[num]&b       #dp 为1 小数点点亮  0 小数点熄灭
#     # 输出要显示的段(包括DP)
#     for i in range(8):      
#         bit = (a >> i) & 1      # 取第i位的值（0或1）
# #比如a=0x0D=0000 1101，则a>>1 = 0000 0110 &1=0; a>>2=0000 0011 &1=1; a>>3=0000 0001 &1=1; a>>4=0000 0000 &1=0;依次类推 
#         Segs[i].value(bit)      # 管脚输出，置段状态（0点亮，1熄灭） 

# '''=================== ========================================================'''
# #/****************************主循环****************************************************/
# while True: 
#     Seg_Show(Show_Num,0)    
#     utime.sleep_ms(200)       





#直接让b,c,e,f,g亮
# Seg_pins = [27,32, 33, 13, 12, 14, 26, 25]
# Segs = [Pin(pin, Pin.OUT,value=1) for pin in Seg_pins]
# while True:
#     Segs[0].value(0)
#     Segs[1].value(0)
#     Segs[2].value(0)
#     Segs[3].value(1)
#     Segs[4].value(0)
#     Segs[5].value(0)
#     Segs[6].value(1)
#     Segs[7].value(1)


















# #电子骰子
# from machine import Pin
# import time
# import random

# # --- 硬件配置 ---
# segment_pins = [25, 26, 14, 12, 13, 33, 32]
# segments = [Pin(p, Pin.OUT) for p in segment_pins]
# button = Pin(15, Pin.IN, Pin.PULL_UP)

# # --- 字形码表（共阳极）---
# # 索引0留空，1-9对应骰子点数（注意：标准七段只能较好显示1-6，7-9可能不标准）
# digit_patterns = [
#     [], # 0号位空置
#     [1, 0, 0, 1, 1, 1, 1], # 1
#     [0, 0, 1, 0, 0, 1, 0], # 2
#     [0, 0, 0, 0, 1, 1, 0], # 3
#     [1, 0, 0, 1, 1, 0, 0], # 4
#     [0, 1, 0, 0, 1, 0, 0], # 5
#     [0, 1, 0, 0, 0, 0, 0], # 6
#     [0, 0, 0, 1, 1, 1, 1], # 7（非标准，仅示意）
#     [0, 0, 0, 0, 0, 0, 0], # 8（全亮）
#     [0, 0, 0, 0, 1, 0, 0]  # 9（非标准）
# ]

# def show_digit(num):
#     if num < 1 or num > 9:
#         return
#     pattern = digit_patterns[num]
#     if len(pattern) != 7:
#         return  # 安全防护
#     for i in range(7):  # ✅ 修正：只遍历 0~6
#         segments[i].value(pattern[i])

# def play_dice_animation():
#     print("正在掷骰子...")
#     speed = 0.05
    
#     # 动画效果：快速变化
#     for _ in range(15):
#         r = random.randint(1, 9)
#         show_digit(r)
#         time.sleep(speed)
#         speed += 0.02  # 逐渐变慢
        
#     # 最终结果
#     final_number = random.randint(1, 9)
#     show_digit(final_number)
#     print(f"结果: {final_number}")
    
#     # 闪烁特效
#     for _ in range(3):
#         time.sleep(0.2)
#         for s in segments:
#             s.value(1)  # 共阳极：1 = 灭
#         time.sleep(0.2)
#         show_digit(final_number)

# print("电子骰子就绪。请按按钮。")

# # 初始状态：可选全灭
# for s in segments:
#     s.value(1)  # 共阳极，初始熄灭

# while True:
#     if button.value() == 0:  # 按下（低电平）
#         play_dice_animation()
#         # 等待按键释放（防抖+避免重复触发）
#         while button.value() == 0:
#             time.sleep(0.01)
#     time.sleep(0.05)




















# # 两位数码管
# print("Hello, ESP32!")
# from machine import Pin, Timer
# import utime

# # === 硬件配置（请根据实际接线修改）===
# LED_Segments = [25, 26, 27, 32, 33, 14, 13]  # a, b, c, d, e, f, g → GPIO 引脚
# LED_Digits   = [2, 4]                       # [个位, 十位] 的位选引脚
# key_incr = Pin(15, Pin.IN, Pin.PULL_UP)  # 增加按钮
# key_decr = Pin(18, Pin.IN, Pin.PULL_UP)  # 减少按钮
# def incr():
#     global count
#     count = (count + 1) % 100
# def decr():
#     global count
#     count = (count - 1) % 100
# key_incr.irq(trigger=Pin.IRQ_FALLING, handler=lambda t: incr())
# key_decr.irq(trigger=Pin.IRQ_FALLING, handler=lambda t: decr())
# #如何添加消抖？答：可以在中断服务程序中添加延时，或者使用软件定时器来实现消抖功能。
# #具体代码如下：
# # import time
# # last_incr_time = 0
# # last_decr_time = 0
# # def incr():
# #     global count, last_incr_time
# #     current_time = time.ticks_ms()
# #     if time.ticks_diff(current_time, last_incr_time) > 200:
# #         count = (count + 1) % 100
# #         last_incr_time = current_time
# # def decr():
# #     global count, last_decr_time     
# #     current_time = time.ticks_ms()
# #     if time.ticks_diff(current_time, last_decr_time) > 200:
# #         count = (count - 1) % 100
# #         last_decr_time = current_time


# # 共阳极数码管：段码 0=亮，1=灭；位选低电平有效
# DIGIT_ACTIVE_LOW = True

# # === 初始化引脚 ===
# seg_pins = [Pin(pin, Pin.OUT, value=1) for pin in LED_Segments]      # 段全灭
# dig_pins = [Pin(pin, Pin.OUT, value=not DIGIT_ACTIVE_LOW) for pin in LED_Digits]  # 位全关

# # === 共阳极段码表（'0'~'9'）===
# SEGMENT_MAP = {
#     '0': (0, 0, 0, 0, 0, 0, 1),
#     '1': (1, 0, 0, 1, 1, 1, 1),
#     '2': (0, 0, 1, 0, 0, 1, 0),
#     '3': (0, 0, 0, 0, 1, 1, 0),
#     '4': (1, 0, 0, 1, 1, 0, 0),
#     '5': (0, 1, 0, 0, 1, 0, 0),
#     '6': (0, 1, 0, 0, 0, 0, 0),
#     '7': (0, 0, 0, 1, 1, 1, 1),
#     '8': (0, 0, 0, 0, 0, 0, 0),
#     '9': (0, 0, 0, 0, 1, 0, 0)
# }

# # === 全局变量 ===
# count = 0
# current_digit = 0  # 0=个位（LED_Digits[0]），1=十位（LED_Digits[1]）

# # === 动态扫描显示回调（由定时器触发）===
# def refresh_display(timer):
#     global current_digit, count
    
#     # 1. 消隐：关闭所有位选（防止重影）
#     for pin in dig_pins:
#         pin.value(not DIGIT_ACTIVE_LOW)
    
#     # 2. 获取当前要显示的数字字符（"00" ~ "99"）
#     display_str = f"{count:02d}"          # 例如：5 → "05"
#     char_to_show = display_str[current_digit]  # current_digit=0 → 个位，=1 → 十位
    
#     # 3. 输出对应段码
#     seg_data = SEGMENT_MAP[char_to_show]
#     for i in range(7):
#         seg_pins[i].value(seg_data[i])
    
#     # 4. 使能当前位
#     dig_pins[current_digit].value(DIGIT_ACTIVE_LOW)
    
#     # 5. 切换到下一位（循环扫描）
#     current_digit = (current_digit + 1) % 2

# # === 启动显示定时器（150Hz，足够避免闪烁）===
# display_timer = Timer(0)
# display_timer.init(freq=150, mode=Timer.PERIODIC, callback=refresh_display)

# # === 主程序 ===
# print("双位数码管计数器启动！每秒 +1，范围 00~99")

# try:
#     while True:
#         utime.sleep(1)           # 每秒更新一次计数值
#         count = (count + 1) % 100
# except KeyboardInterrupt:
#     # 清理资源：关闭所有输出
#     display_timer.deinit()
#     for pin in seg_pins:
#         pin.value(1)  # 段全灭
#     for pin in dig_pins:
#         pin.value(not DIGIT_ACTIVE_LOW)  # 位全关
#     print("\n程序已安全退出")





#对应的接线如下
# {
#   "version": 1,
#   "editor": "wokwi",
#   "parts": [
#     { "type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 47.32, "left": 126.52, "attrs": {} },
#     {
#       "type": "wokwi-7segment",
#       "id": "seg1",
#       "top": 88.27,
#       "left": 8.33,
#       "attrs": { "comAnode": "true" }
#     },
#     {
#       "type": "wokwi-7segment",
#       "id": "seg2",
#       "top": 86.44,
#       "left": -65.3,
#       "attrs": { "comAnode": "true" }
#     },
#     { "type": "wokwi-button", "id": "btnUp", "top": 50, "left": 200, "attrs": { "label": "UP" } },
#     {
#       "type": "wokwi-button",
#       "id": "btnDown",
#       "top": 100,
#       "left": 200,
#       "attrs": { "label": "DOWN" }
#     }
#   ],
#   "connections": [
#     [ "esp:D13", "seg1:G", "green", [ "h-24.64", "v13.15", "h-105.97", "v-107.92" ] ],
#     [ "seg2:A", "seg1:A", "green", [ "v-12.61", "h73.63" ] ],
#     [ "seg2:B", "seg1:B", "green", [ "v-34.62", "h73.63" ] ],
#     [ "seg2:C", "seg1:C", "green", [ "v50.41", "h73.63" ] ],
#     [ "seg2:D", "seg1:D", "green", [ "v59.11", "h73.63" ] ],
#     [ "seg2:E", "seg1:E", "green", [ "v26.35", "h73.63" ] ],
#     [ "seg2:F", "seg1:F", "green", [ "v-28.48", "h73.63" ] ],
#     [ "seg2:G", "seg1:G", "green", [ "v-19.78", "h73.63" ] ],
#     [ "esp:D4", "seg1:COM.1", "black", [ "h19.33", "v89.47", "h- 215.1" ] ],
#     [ "esp:D2", "seg2:COM.2", "black", [ "h30.09", "v92.38", "h- 299.49" ] ],
#     [ "btnUp:1", "esp:D15", "blue", [] ],
#     [ "btnDown:1", "esp:D18", "blue", [] ],
#     [ "btnUp:2", "esp:GND", "", [] ],
#     [ "btnDown:2", "esp:GND", "", [] ],
#     [ "seg1:A", "esp:D25", "green", [ "v-23.22", "h70.92", "v67.53" ] ],
#     [ "esp:D26", "seg1:B", "green", [ "h-28.93", "v-70.28", "h-50.65" ] ],
#     [ "esp:D14", "seg1:F", "green", [ "h-41.21", "v-119.98", "h-9.21" ] ],
#     [ "esp:D33", "seg1:E", "green", [ "h-56.55", "v51.85", "h-62.16", "v-1.53" ] ],
#     [ "esp:D32", "seg1:D", "green", [ "h-64.23", "v68.25", "h-45.28" ] ],
#     [ "esp:D27", "seg1:C", "green", [ "h-22.02", "v16.61", "h-19.18" ] ]
#   ],
#   "dependencies": {}
# }













#纯按键无定时器控制数码管增减
from machine import Pin, Timer
import utime

# === 引脚定义 ===
LED_Segments = [25, 26, 27, 32, 33, 14, 13]  # a, b, c, d, e, f, g
LED_Digits   = [2, 4]                        # [十位, 个位] —— 实际顺序由显示逻辑决定

BTN_UP_PIN   = 19    # UP 按键
BTN_DOWN_PIN = 18    # DOWN 按键

# 共阳极：段码 0=亮，位选低电平有效
DIGIT_ACTIVE_LOW = True

# === 初始化引脚 ===
seg_pins = [Pin(pin, Pin.OUT, value=1) for pin in LED_Segments]
dig_pins = [Pin(pin, Pin.OUT, value=not DIGIT_ACTIVE_LOW) for pin in LED_Digits]

btn_up   = Pin(BTN_UP_PIN,   Pin.IN, Pin.PULL_UP)
btn_down = Pin(BTN_DOWN_PIN, Pin.IN, Pin.PULL_UP)

# === 共阳极段码表 ===
LED_Bits = {
    '0': (0,0,0,0,0,0,1),
    '1': (1,0,0,1,1,1,1),
    '2': (0,0,1,0,0,1,0),
    '3': (0,0,0,0,1,1,0),
    '4': (1,0,0,1,1,0,0),
    '5': (0,1,0,0,1,0,0),
    '6': (0,1,0,0,0,0,0),
    '7': (0,0,0,1,1,1,1),
    '8': (0,0,0,0,0,0,0),
    '9': (0,0,0,0,1,0,0)
}

# === 全局变量 ===
count = 0
current_digit = 0
last_btn_up_state = 1
last_btn_down_state = 1
debounce_time = 0

# === 调试函数：单独测试数码管 ===
def set_digit(digit, value):
    """用于调试，单独点亮一个数码管"""
    # 关闭所有位选
    for pin in dig_pins:
        pin.value(not DIGIT_ACTIVE_LOW)
    # 设置段码
    bits = LED_Bits[str(value)]
    for i in range(7):
        seg_pins[i].value(bits[i])
    # 使能指定数码管位
    dig_pins[digit].value(DIGIT_ACTIVE_LOW)
    utime.sleep(0.5)

# >>> 可选：取消以下注释进行硬件调试 <<<
# print("调试模式：测试数码管...")
# set_digit(0, 1)  # 第一位显示 1
# set_digit(1, 2)  # 第二位显示 2
# utime.sleep(1)

# 恢复默认状态（全灭）
for pin in seg_pins:
    pin.value(1)
for pin in dig_pins:
    pin.value(not DIGIT_ACTIVE_LOW)

# === 刷新显示函数（由定时器调用）===
def refresh_display(timer):
    global current_digit, count
    # 消隐：关闭所有位
    for pin in dig_pins:
        pin.value(not DIGIT_ACTIVE_LOW)
    # 获取当前显示字符串（如 "05"）
    cnt_str = f"{count:02d}"
    char_to_show = cnt_str[current_digit]  # current_digit=0 → 十位, =1 → 个位
    # 输出段码
    bits = LED_Bits[char_to_show]
    for i in range(7):
        seg_pins[i].value(bits[i])
    # 使能当前位
    dig_pins[current_digit].value(DIGIT_ACTIVE_LOW)
    # 切换到下一位
    current_digit = (current_digit + 1) % 2

# === 按键检测函数 ===
def check_buttons():
    global count, last_btn_up_state, last_btn_down_state, debounce_time
    
    current_time = utime.ticks_ms()
    up_state = btn_up.value()
    down_state = btn_down.value()

    # 检测 UP 按键（下降沿：按下时触发）
    if last_btn_up_state == 1 and up_state == 0:
        if utime.ticks_diff(current_time, debounce_time) > 50:
            count = (count + 1) % 100
            print(f"UP 按下，当前值: {count:02d}")
            debounce_time = current_time

    # 检测 DOWN 按键（下降沿：按下时触发）
    if last_btn_down_state == 1 and down_state == 0:
        if utime.ticks_diff(current_time, debounce_time) > 50:
            count = (count - 1) % 100
            print(f"DOWN 按下，当前值: {count:02d}")
            debounce_time = current_time

    # 更新按键状态
    last_btn_up_state = up_state
    last_btn_down_state = down_state

# === 启动定时器（150Hz 动态扫描）===
tim = Timer(0)
tim.init(freq=150, mode=Timer.PERIODIC, callback=refresh_display)

# === 主循环 ===
print("计数器已启动！按 UP 或 DOWN 按键调整数值（00~99）。")
try:
    while True:
        check_buttons()
        utime.sleep_ms(10)  # 避免 CPU 占用过高
except KeyboardInterrupt:
    tim.deinit()
    # 清理：关闭所有输出
    for pin in seg_pins + dig_pins:
        pin.value(1)
    print("\n程序结束")








#多功能

# from machine import Pin, Timer
# import utime

# # === 引脚定义 ===
# LED_Segments = [25, 26, 27, 32, 33, 14, 13]  # a, b, c, d, e, f, g
# LED_Digits   = [4, 2]                        # [十位 (左), 个位 (右)]

# BTN_MODE_PIN   = 19
# BTN_SELECT_PIN = 18

# DIGIT_ACTIVE_LOW = True  # 共阳极：位选低电平有效

# # === 初始化引脚 ===
# seg_pins = [Pin(pin, Pin.OUT, value=1) for pin in LED_Segments]
# dig_pins = [Pin(pin, Pin.OUT, value=not DIGIT_ACTIVE_LOW) for pin in LED_Digits]

# btn_mode   = Pin(BTN_MODE_PIN,   Pin.IN, Pin.PULL_UP)
# btn_select = Pin(BTN_SELECT_PIN, Pin.IN, Pin.PULL_UP)

# # === 段码表（共阳极：0=亮，1=灭）===
# CHAR_Bits = {
#     '0': (0,0,0,0,0,0,1),
#     '1': (1,0,0,1,1,1,1),
#     '2': (0,0,1,0,0,1,0),
#     '3': (0,0,0,0,1,1,0),
#     '4': (1,0,0,1,1,0,0),
#     '5': (0,1,0,0,1,0,0),
#     '6': (0,1,0,0,0,0,0),
#     '7': (0,0,0,1,1,1,1),
#     '8': (0,0,0,0,0,0,0),
#     '9': (0,0,0,0,1,0,0),
#     'A': (0,0,0,1,0,0,0),
#     'B': (1,1,0,0,0,0,0),
#     'C': (0,1,1,0,0,1,1),
#     'D': (1,0,0,0,0,1,0),
#     'E': (0,1,1,0,0,0,0),
#     'F': (0,1,1,1,0,0,0),
#     'H': (1,0,0,1,0,0,0),
#     'L': (1,1,1,0,0,0,1),
#     'P': (0,0,1,1,0,0,0),
#     'U': (1,1,0,0,0,0,1),
#     'O': (0,0,0,0,0,0,1),
#     '-': (1,1,1,1,1,1,0),
#     '_': (1,1,1,0,1,1,1),
#     ' ': (1,1,1,1,1,1,1),  # 空格 = 全灭
# }

# # === 动画帧定义（每帧必须为 2 字符）===
# ANIMATIONS = {
#     'scroll': [" H", "HE", "EL", "LL", "LO", "O ", "  "],
#     'blink':  ["  ", "--", "  ", "--"],
#     'heart':  ["L-", "-L", "L-", "-L"],
#     'run':    ["> ", " >", "  ", " <", "< "]
# }

# # === 全局变量 ===
# display_mode = 0        # 0=计数, 1=滚动, 2=动画
# animation_index = 0
# count = 0
# current_digit = 0       # 0=个位(右), 1=十位(左)

# last_btn_mode = 1
# last_btn_select = 1
# debounce_time = 0

# # === 调试函数 ===
# def set_digit(digit, char):
#     """单独点亮一个数码管用于调试"""
#     if char not in CHAR_Bits:
#         char = ' '
#     # 关闭所有位
#     for pin in dig_pins:
#         pin.value(not DIGIT_ACTIVE_LOW)
#     # 设置段码
#     bits = CHAR_Bits[char]
#     for i in range(7):
#         seg_pins[i].value(bits[i])
#     # 使能指定位
#     dig_pins[digit].value(DIGIT_ACTIVE_LOW)
#     utime.sleep(0.5)

# # >>> 取消注释以下代码进行硬件调试 <<<
# # print("初始化中...测试数码管")
# # set_digit(0, 'H')  # 右边（个位）显示 H
# # set_digit(1, 'L')  # 左边（十位）显示 L
# # utime.sleep(1)

# # 恢复默认状态（全灭）
# for pin in seg_pins:
#     pin.value(1)
# for pin in dig_pins:
#     pin.value(not DIGIT_ACTIVE_LOW)

# # === 刷新显示（动态扫描）===
# def refresh_display(timer):
#     global current_digit, count, display_mode, animation_index
    
#     # 消隐
#     for pin in dig_pins:
#         pin.value(not DIGIT_ACTIVE_LOW)
    
#     # 根据模式生成显示文本（确保为2字符）
#     if display_mode == 0:
#         text = f"{count:02d}"
#     elif display_mode == 1:
#         frames = ANIMATIONS['scroll']
#         text = frames[animation_index % len(frames)]
#     elif display_mode == 2:
#         # 轮换不同动画类型
#         anim_keys = list(ANIMATIONS.keys())
#         current_anim = anim_keys[animation_index % len(anim_keys)]
#         frames = ANIMATIONS[current_anim]
#         frame_idx = (utime.ticks_ms() // 500) % len(frames)
#         text = frames[frame_idx]
#     else:
#         text = "  "
    
#     # 确保 text 为 2 字符
#     if len(text) < 2:
#         text = text.ljust(2, ' ')
#     elif len(text) > 2:
#         text = text[:2]
    
#     # 映射：text[0]=十位(左), text[1]=个位(右)
#     left_char = text[0]
#     right_char = text[1]
#     digit_chars = [right_char, left_char]  # [个位, 十位]
#     char_to_show = digit_chars[current_digit]
    
#     if char_to_show not in CHAR_Bits:
#         char_to_show = ' '
    
#     # 输出段码
#     bits = CHAR_Bits[char_to_show]
#     for i in range(7):
#         seg_pins[i].value(bits[i])
    
#     # 使能当前位
#     dig_pins[current_digit].value(DIGIT_ACTIVE_LOW)
    
#     # 切换下一位
#     current_digit = (current_digit + 1) % 2

# # === 按键检测 ===
# def check_buttons():
#     global display_mode, animation_index, count, debounce_time
#     global last_btn_mode, last_btn_select
    
#     current_time = utime.ticks_ms()
#     mode_state = btn_mode.value()
#     select_state = btn_select.value()
    
#     # MODE 按键：下降沿触发（按下）
#     if last_btn_mode == 1 and mode_state == 0:
#         if utime.ticks_diff(current_time, debounce_time) > 50:
#             display_mode = (display_mode + 1) % 3
#             animation_index = 0
#             debounce_time = current_time
#             modes = ["计数模式", "滚动文字", "动画模式"]
#             print(f"切换到: {modes[display_mode]}")
    
#     # SELECT 按键：下降沿触发
#     if last_btn_select == 1 and select_state == 0:
#         if utime.ticks_diff(current_time, debounce_time) > 50:
#             if display_mode == 0:
#                 count = (count + 1) % 100
#                 print(f"计数: {count:02d}")
#             elif display_mode == 1:
#                 animation_index += 1
#                 print("滚动: 下一帧")
#             elif display_mode == 2:
#                 animation_index += 1
#                 print("动画: 切换类型")
#             debounce_time = current_time
    
#     last_btn_mode = mode_state
#     last_btn_select = select_state

# # === 启动定时器 ===
# tim = Timer(0)
# tim.init(freq=150, mode=Timer.PERIODIC, callback=refresh_display)

# # === 主循环 ===
# print("多功能数码管系统已启动！")
# print("操作说明：")
# print("  MODE 按钮 → 切换模式")
# print("  SELECT 按钮 → 执行操作（+1 / 下一帧）")

# try:
#     while True:
#         check_buttons()
#         utime.sleep_ms(10)
# except KeyboardInterrupt:
#     tim.deinit()
#     for pin in seg_pins + dig_pins:
#         pin.value(1)
#     print("\n程序结束")










