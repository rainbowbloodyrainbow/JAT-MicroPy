# #任务四：显示图片
# import framebuf
# from machine import Pin, I2C
# import ssd1306
# import bmp  # 确保 bmp.py 文件存在，且包含 data = [...] 或 b'...'

# # 初始化 I2C（修复：sda 必须是 Pin 对象）
# i2c = I2C(0, scl= Pin(22), sda= Pin(21))

# # 可选：扫描 I2C 设备地址（调试用）
# devices = i2c.scan()
# if devices:
#     print("I2C 地址:", [hex(addr) for addr in devices])
# else:
#     print("未找到 I2C 设备！")

# # 初始化 OLED（128x64，常见地址 0x3c）
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # 加载图像数据（假设 mypic01.data 是 bytes 或 bytearray）
# mydata = bytearray(bmp.data)

# # 创建 FrameBuffer（格式必须匹配你的图像数据编码）
# fb = framebuf.FrameBuffer(mydata, 128, 64, framebuf.MONO_HMSB)

# # 清屏
# oled.fill(0)

# # 将图像帧缓冲区 blit 到 OLED（修复：使用 .blit 而非 .show_image）
# oled.blit(fb, 0, 0)  # (x=0, y=0)

# # 刷新屏幕
# oled.show()











# #任务五:绘制表情(无奈)
# from machine import Pin, I2C
# import ssd1306
# import time

# # --- 1. 初始化 OLED (请确认你的引脚) ---
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # --- 2. 补充缺失的画圆函数 (Bresenham算法) ---
# def draw_circle(oled, x0, y0, radius, col=1):
#     x = radius
#     y = 0
#     err = 0
#     while x >= y:
#         oled.pixel(x0 + x, y0 + y, col)
#         oled.pixel(x0 + y, y0 + x, col)
#         oled.pixel(x0 - y, y0 + x, col)
#         oled.pixel(x0 - x, y0 + y, col)
#         oled.pixel(x0 - x, y0 - y, col)
#         oled.pixel(x0 - y, y0 - x, col)
#         oled.pixel(x0 + y, y0 - x, col)
#         oled.pixel(x0 + x, y0 - y, col)
#         y += 1
#         if err <= 0:
#             err += 2*y + 1
#         else:
#             x -= 1
#             err += 2*(y-x) + 1

# # --- 3. 修改后的绘图演示函数 ---
# def draw_demo(oled):
#     oled.fill(0)  # 清屏
    

#     # 绘制3横线
#     oled.hline(71, 22, 15, 1)
#     oled.hline(47, 22, 15, 1)
#     oled.hline(59, 42, 15, 1)

#     # 绘制圆 (修改处：调用自定义函数)
#     # 原代码: oled.circle(64, 32, 15, 1) -> 报错
#     # 新代码:
#     draw_circle(oled, 64, 32, 30, 1)
    
#     # 显示
#     oled.show()

# # --- 4. 主循环 ---
# while True:
#     draw_demo(oled)
#     time.sleep(2)

#     oled.show()
#     time.sleep(2)


















# #任务五扩展：画笑脸
# # 基本图形绘制示例
# from machine import Pin, I2C
# import ssd1306
# import time

# # --- 1. 初始化 OLED (请确认你的引脚) ---
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # --- 2. 补充缺失的画圆函数 (Bresenham算法) ---
# def draw_circle(oled, x0, y0, radius, col=1):
#     x = radius
#     y = 0
#     err = 0
#     while x >= y:
#         oled.pixel(x0 + x, y0 + y, col)
#         oled.pixel(x0 + y, y0 + x, col)
#         oled.pixel(x0 - y, y0 + x, col)
#         oled.pixel(x0 - x, y0 + y, col)
#         oled.pixel(x0 - x, y0 - y, col)
#         oled.pixel(x0 - y, y0 - x, col)
#         oled.pixel(x0 + y, y0 - x, col)
#         oled.pixel(x0 + x, y0 - y, col)
#         y += 1
#         if err <= 0:
#             err += 2*y + 1
#         else:
#             x -= 1
#             err += 2*(y-x) + 1

# # --- 3. 修改后的绘图演示函数 ---
# def draw_demo(oled):
#     oled.fill(0)  # 清屏
    

#     # 绘制交叉线
#     oled.hline(71, 22, 15, 1)
#     oled.hline(47, 22, 15, 1)
#     oled.hline(59, 42, 15, 1)
#     oled.line(64, 32, 58, 40, 1)
#     oled.line(58, 40, 70, 40, 1)
#     oled.line(64, 32, 70, 40, 1)
#     #现在鼻子最下面是(58,40)到(70,40)
#     #把鼻子换成倒三角，以上三行应改为
#     #oled.line(58, 45, 70, 45, 1)
#     #oled
#     #计划笑为(58,45),(59,46),(60,47),(61,48),横线，,(67,48)(68,47)(69,46),(70,45)
#     oled.pixel(58, 45, 1)
#     oled.pixel(59, 46, 1)
#     oled.pixel(60, 47, 1)
#     oled.pixel(61, 48, 1)
#     oled.hline(62, 48, 5, 1)
#     oled.pixel(67, 48, 1)
#     oled.pixel(68, 47, 1)
#     oled.pixel(69, 46, 1)
#     oled.pixel(70, 45, 1)
#     # 绘制圆 (修改处：调用自定义函数)
#     # 原代码: oled.circle(64, 32, 15, 1) -> 报错
#     # 新代码:
#     draw_circle(oled, 64, 32, 30, 1)
    
#     # 显示
#     oled.show()

# # --- 4. 主循环 ---
# while True:
#     draw_demo(oled)
#     time.sleep(2)

#     oled.show()
#     time.sleep(2)























# #任务六：进度条动态显示
# import framebuf
# from machine import Pin, I2C
# import ssd1306
# import time

# # 初始化I2C和OLED
# i2c = I2C(0, sda=Pin(21), scl=Pin(22))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# class ProgressBar:
#     def __init__(self, oled, x, y, width, height):
#         self.oled = oled
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.progress = 0
    
#     def set_progress(self, value):
#         """设置进度值 (0-100)"""
#         self.progress = max(0, min(100, value))
    
#     def draw(self):
#         """绘制进度条"""
#         # 绘制边框
#         self.oled.rect(self.x, self.y, self.width, self.height, 1)
        
#         # 计算填充宽度
#         fill_width = int((self.width - 2) * self.progress / 100)
        
#         # 填充进度区域
#         if fill_width > 0:
#             self.oled.fill_rect(
#                 self.x + 1, 
#                 self.y + 1, 
#                 fill_width, 
#                 self.height - 2, 
#                 1
#             )

# # 使用示例
# progress = ProgressBar(oled, 10, 25, 108, 14)

# # 动画演示
# for i in range(101):
#     progress.set_progress(i)
#     oled.fill(0)
#     progress.draw()
#     oled.show()
#     time.sleep_ms(20)



























# #任务七：仪表盘动态显示
# import math
# import time
# from machine import Pin, I2C
# import ssd1306

# # 初始化 OLED (请根据你的实际引脚修改 SDA/SCL)
# # 假设使用的是 ESP32 默认 I2C
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # --- 1. 手动实现画圆函数 ---
# def draw_circle(oled, x0, y0, radius, col=1):
#     x = radius
#     y = 0
#     err = 0
#     while x >= y:
#         oled.pixel(x0 + x, y0 + y, col)
#         oled.pixel(x0 + y, y0 + x, col)
#         oled.pixel(x0 - y, y0 + x, col)
#         oled.pixel(x0 - x, y0 + y, col)
#         oled.pixel(x0 - x, y0 - y, col)
#         oled.pixel(x0 - y, y0 - x, col)
#         oled.pixel(x0 + y, y0 - x, col)
#         oled.pixel(x0 + x, y0 - y, col)
        
#         y += 1
#         if err <= 0:
#             err += 2*y + 1
#         else:
#             x -= 1
#             err += 2*(y-x) + 1

# # --- 2. 修正后的仪表盘函数 ---
# def draw_gauge(oled, value, min_val=0, max_val=100, x=64, y=32, radius=28):
#     # 规范化值到 0-100
#     norm_val = (value - min_val) / (max_val - min_val) * 100
#     norm_val = max(0, min(100, norm_val))
    
#     # --- 绘制表盘外圈 ---
#     draw_circle(oled, x, y, radius, 1)
    
#     # --- 绘制刻度 ---
#     # 这里的角度逻辑：
#     # math.pi (180度) 是左边 (9点钟方向)
#     # 0 是右边 (3点钟方向)
#     # math.pi/2 是上方 (12点钟方向)
#     # 下面的公式是画一个从左(西)到右(东)的半圆拱形
#     for i in range(0, 101, 10):
#         # 刻度角度：从 180度(左) 转到 0度(右)
#         angle = math.pi - (math.pi * i / 100)
        
#         tick_len = 3 # 刻度长度
#         sx = int(x + (radius - tick_len) * math.cos(angle))
#         sy = int(y - (radius - tick_len) * math.sin(angle)) # y轴在屏幕上是向下的，所以减去sin
#         ex = int(x + radius * math.cos(angle))
#         ey = int(y - radius * math.sin(angle))
#         oled.line(sx, sy, ex, ey, 1)

#     # --- 计算并绘制指针 ---
#     # 注意：这里必须使用独立的变量名，不能和刻度循环里的变量混用
#     # 指针角度
#     needle_angle = math.pi - (math.pi * norm_val / 100)
    
#     needle_x = int(x + (radius - 5) * math.cos(needle_angle))
#     needle_y = int(y - (radius - 5) * math.sin(needle_angle))
    
#     oled.line(x, y, needle_x, needle_y, 1)
    
#     # --- 显示数值 ---
#     # 居中显示
#     text = f"{int(value)}"
#     text_x = x - (len(text) * 4) # 简易居中计算
#     oled.text(text, text_x, y + 5)

# # --- 主循环测试 ---
# while True:
#     # 模拟从 0 到 30 的变化
#     for temp in range(0, 31, 2):
#         oled.fill(0)
#         # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#         draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#         oled.show()
#         time.sleep_ms(50)
        
#     # 模拟回落
#     for temp in range(30, -1, -2):
#         oled.fill(0)
#         draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#         oled.show()
#         time.sleep_ms(50)
























#任务八：贪吃蛇
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep_ms
from random import randint

# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

up_btn   =Pin(2,Pin.IN,Pin.PULL_UP)
down_btn =Pin(5, Pin.IN,Pin.PULL_UP)
left_btn =Pin(15, Pin.IN,Pin.PULL_UP)
right_btn=Pin(4, Pin.IN,Pin.PULL_UP)


SCREEN_WIDTH        =128 # OLED display width, in pixels
SCREEN_HEIGHT       =64  # OLED display height, in pixels

SNAKE_PIECE_SIZE     =3
MAX_SANKE_LENGTH     =165
MAP_SIZE_X           =20
MAP_SIZE_Y           =20
STARTING_SNAKE_SIZE  =5
SNAKE_MOVE_DELAY     =30

SSD1306_INVERSE      =0
SSD1306_WHITE        =1

START               =0
RUNNING             =1
GAMEOVER            =2



LEFT                =0
UP                  =1
RIGHT               =2
DOWN                =3

display = SSD1306_I2C(SCREEN_WIDTH ,SCREEN_HEIGHT , i2c)
snake =[[0]*2 for _ in range(MAX_SANKE_LENGTH)] 

fruit = [0]*2

snake_length = 5

gameState = START
newDir = RIGHT

def resetSnake():
    snake_length = STARTING_SNAKE_SIZE
    for i in range(snake_length):
        snake[i][0] = MAP_SIZE_X // 2 - i
        snake[i][1] = MAP_SIZE_Y // 2

def generateFruit():
    fruit[0] = randint(1, MAP_SIZE_X-1)
    fruit[1] = randint(1, MAP_SIZE_Y-1)
    for i in range(snake_length):
        if fruit[0] == snake[i][0] and fruit[1] == snake[i][1]:
            generateFruit()
        else:
            break
def checkFruit():
    global snake_length
    if fruit[0] == snake[0][0] and fruit[1] == snake[0][1]:
        if snake_length <= MAX_SANKE_LENGTH-1:
            snake_length += 1
        generateFruit()
 
def buttonPress():
    global newDir
    if up_btn.value()==0:
        newDir = UP
        return True
    elif down_btn.value()==0:
        newDir = DOWN
        return True
    elif left_btn.value()==0:
        newDir = LEFT
        return True
    elif right_btn.value()==0:
        newDir = RIGHT
        return True
    return False

def drawMap():
    offsetMapX = SCREEN_WIDTH - SNAKE_PIECE_SIZE * MAP_SIZE_X - 2
    offsetMapY = 2

    display.rect(fruit[0] * SNAKE_PIECE_SIZE + offsetMapX, fruit[1] * SNAKE_PIECE_SIZE + offsetMapY, SNAKE_PIECE_SIZE, SNAKE_PIECE_SIZE, SSD1306_WHITE)
    display.rect(offsetMapX - 2, 0, SNAKE_PIECE_SIZE * MAP_SIZE_X + 4, SNAKE_PIECE_SIZE * MAP_SIZE_Y + 4, SSD1306_WHITE)
    for i in range(snake_length):
        display.fill_rect(snake[i][0] * SNAKE_PIECE_SIZE + offsetMapX, snake[i][1] * SNAKE_PIECE_SIZE + offsetMapY, SNAKE_PIECE_SIZE, SNAKE_PIECE_SIZE, SSD1306_WHITE) 

def drawScore():
    display.text('Score:', 0, 0)    
    display.text(str(snake_length - STARTING_SNAKE_SIZE), 10, 12)    

def drawPressToStart():
    display.text("Press a",0,25)
    display.text("button",0,35)
    display.text("to",0,45)
    display.text("start! ",0,55)

def drawGameover():
    display.text("GAME",0,45)
    display.text(" OVER! ",0,55)


def setupGame():
    global snake_length
    snake_length = 5
    gameState = START
    newDir = RIGHT
    resetSnake()
    generateFruit()
    display.fill(0)
    drawMap()
    drawScore()
    drawPressToStart()
    display.show()

def collisionCheck(x,y): 
    for i in range(1,snake_length):
        if x == snake[i][0] and y == snake[i][1]:
            return True
    if x < 0 or y < 0 or x >= MAP_SIZE_X or y >= MAP_SIZE_Y:
        return True
    return False

def moveSnake(direction):
    x = snake[0][0]
    y = snake[0][1]

    if direction==LEFT:
        x -= 1
    elif direction==UP:
        y -= 1
    elif direction==RIGHT:
        x += 1
    elif direction==DOWN:
        y += 1
    
    if collisionCheck(x, y):
        return True

    for i in range(snake_length - 1,0,-1):
        snake[i][0] = snake[i - 1][0]
        snake[i][1] = snake[i - 1][1]

    snake[0][0] = x
    snake[0][1] = y
    return False

moveTime = 0
setupGame()

while True:
    if gameState==START:
        if buttonPress():
            gameState = RUNNING
    elif gameState==RUNNING:
        moveTime+=1
        buttonPress()
        if moveTime >= SNAKE_MOVE_DELAY:
            display.fill(0)
            if moveSnake(newDir):
                gameState = GAMEOVER
                drawGameover()
                sleep_ms(1000)
            drawMap()
            drawScore()
            display.show()
            checkFruit()
            moveTime = 0
    elif  gameState==GAMEOVER:
        if buttonPress():
            setupGame()
            gameState = START
    sleep_ms(5)