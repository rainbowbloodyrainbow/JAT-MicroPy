# Task1: 初识定时器
# 使用定时器实现定时打印信息
from machine import Timer



def callback1(timer1):
    print("Timer callback1")

timer1 = Timer(0)
timer1.init(period=1000, mode=Timer.PERIODIC, callback=callback1)
# 我们创建了一个0号定时器的对象timer1，将它的周期(period，单位为ms)设为1000，
# 触发模式为周期模式(PERIODIC)，还有另一种触发模式，是一次模式(ONE_SHOT)
# callback参数，即回调函数，是每次触发定时器时执行的函数，为我们上面定义的callback1函数






# Task2: Benny被邮差追杀
from machine import Timer

def day_end(timer1):
    print("A day has passed")


def Here_comes_CourierSix(timer1,timer2):
    print("Benny, you dirty coward!")
    print("Time to go die!")
    timer1.deinit()

timer1 = Timer(0)
timer1.init(period=1000, mode=Timer.PERIODIC, callback=day_end)

timer2 = Timer(1)
timer2.init(period=5000, mode=Timer.ONE_SHOT, callback=Here_comes_CourierSix)

# 如何让Benny被邮差杀掉后，定时器停止工作？
