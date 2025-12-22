# #任务一：初识SSD1306 OLED显示屏

# from machine import Pin,I2C
# import ssd1306

# i2c=I2C(0,scl=Pin(22),sda=Pin(21))
# #类似于led=Pin(2,Pin.OUT)，创造一个Pin对象led，2号引脚，输出模式
# #这里是创造一个I2C对象i2c，0号I2C总线，22号引脚为SCL，21号引脚为SDA
# #Pin类对象可以作为I2C类的参数来指定I2C总线的引脚
# #那是不是说，写I2C这个类的时候，必然要import Pin模块呢？答案是肯定的

# oled_width=128
# oled_height=64
# display=ssd1306.SSD1306_I2C(oled_width,oled_height,i2c)

# display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)#在点(0,0)开始画32x32像素的白色方块
# display.fill_rect(2, 2, 28, 28, 0)#在点(2,2)开始画28x28像素的黑色方块
# display.vline(9,8,22,1)#在点(9,8)开始画22像素的白色竖线,注意最后一个参数1表示白色，0表示黑色，下面类似
# display.vline(16,2,22,1)#在点(16,2)开始画22像素的白色竖线
# display.vline(23,8,22,1)#在点(23,8)开始画22像素的白色竖线
# display.fill_rect(26,24,2,4,1)#在点(26,24)开始画2x4像素的白色方块   
# display.text('MicroPython',40,0,1)#在点(40,0)开始显示文本"MicroPython"
# display.text('SSD1306',40,12,1)#在点(40,12)开始显示文本"SSD1306"
# display.text('OLED',40,24,1)#在点(40,24)开始显示文本"OLED"
# display.show()#上面仅仅是把数据写入内存，并没有显示出来，必须调用show()方法才会显示出来






# #任务二: 滚动显示文本
# import framebuf
# from machine import Pin, I2C
# import ssd1306
# import time

# # 初始化I2C和OLED
# i2c = I2C(0, sda=Pin(21), scl=Pin(22))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # 创建滚动文本
# text = "MicroPython OLED Demo - Scrolling Text"

# # 滚动显示
# x = 128
# while True:
#     oled.fill(0)  # 清屏
#     oled.text(text, x, 25)# 在y=25位置显示文本
#     oled.show()
    
#     x -= 1  #x最开始是128，每次循环减1，实现向左滚动；如果想从左往右滚动，需要把这里改成x += 1，然后下面的判断条件也要改成 x > len(text) * 8
#     if x < -len(text) * 8:  # 假设字体宽度8px,其实直接写常数
#         x = 128
    
#     time.sleep_ms(50)


#任务三: 显示中文字符
import framebuf
from machine import Pin, I2C
import ssd1306
from time import sleep_ms
from font import font16


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def draw_chinese(oled, font, word, x, y):
    for ch in word:#ch只是一个名字，代表字符串word中的每一个字符，叫什么都可以，重点是要和下面的font.get(ch...)对应上
        data = bytearray(font.get(ch, [0x00] * 32))
        #bytearray()函数将一个可迭代对象转换为字节数组
        fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
        oled.framebuf.blit(fb, x, y)  # 使用 oled.framebuf 的 blit
        x += 16

# 显示测试
oled.fill(0)
draw_chinese(oled, font16, '哈尔滨工程大学', 10, 20)
oled.show()