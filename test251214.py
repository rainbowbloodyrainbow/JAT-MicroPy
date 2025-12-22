# from machine import Pin 
# #machine是MicroPython的核心模块之一，Pin是machine模块中的一个类，用于控制微控制器的引脚。
# #Pin是控制引脚的类，Pin类的对象都是引脚
# #我们暂时只用到Pin类，所以只导入这个类。
# for i in range(1,6,1):
# #range是Python特有的一个函数，表示生成一个整数序列（左闭右开，比如这里表示1到5）
# #range函数有三个参数：起始值、终止值、步长。事实上，起始值和步长都可以不写，不写时默认起始值为0，步长为1。
# #比如range(3)就表示0，1，2
#     p = Pin(i,Pin.OUT)
#     #Pin()是Pin类的构造函数，用于创建一个Pin类的对象，它有两个参数，第一个参数是引脚编号，第二个参数是引脚模式
#     #Pin是一个类，我们创建了一个属于Pin类的对象p;就好比人类是一个类，生孩子就是创建一个人类的实例化对象
#     #那能不能不要p，直接用Pin(i,Pin.OUT)来控制引脚呢？理论上也可以，但注意它无法调用on()和off()方法,不过可以调用value()方法
#     p.on()
#     #on()是Pin类的一个方法，p.on()就是对p这个Pin类的对象调用on()方法
#     #方法其实就是函数，只不过类里面的函数专门起了个别名，叫做方法
#     #on()方法的作用是把对应引脚对象设置为高电平

from machine import Pin,PWM
import time
led_pwm = PWM(Pin(2,Pin.OUT),freq = 500)
#设置引脚2为PWM模式，频率500Hz，这里的频率是PWM的频率，它和我们看到的呼吸灯变化频率的关系是正相关的，具体关系后面会讲到
duty = 0
step = 10
delay = 0.02
direction = 1
while True:
    duty += step * direction
    if duty >= 1023:
        duty = 1023
        direction = -1
    elif duty <= 0:
        duty = 0
        direction = 1
    led_pwm.duty(duty)
    time.sleep(delay)