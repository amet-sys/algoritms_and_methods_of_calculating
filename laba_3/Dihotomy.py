import math
import matplotlib.pyplot as mt
import seaborn

seaborn.set_style('darkgrid')

def f(x):
    return x - math.sin(2*x)

#Рисуем график функции, чтобы выяснить где примерно находятся точки 
x=[]
i=-10
while i<=11:
    x.append(i) #заполняем значения х
    i+=0.125
y = [f(i) for i in x]  # Создаем список y для всех значений x

fig, axes = mt.subplots(figsize=(100,100)) 

axes.plot(x, y) 
shags=[]
for j in range(-10,11):
    shags.append(j)
mt.xticks(shags)
mt.yticks(shags)
mt.show()


a=-0.5
b=0.5
eps=0.0001
n=int(math.log((b-a)/eps,math.e)/math.log(2,math.e))+1
x=0
y=0
for i in range(n):
    x=(a+b)/2
    print(x)
    if abs(b-x) < eps:
        print("Корень уравнения: ",x," значение функции в корне: ",f(x))
        break 
    else:
        if (f(x) * f(a)) > 0:
            a=x 
        else:
            b=x
    


#source ~/me/create/bin/activate