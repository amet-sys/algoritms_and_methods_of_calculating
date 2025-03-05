import math 
import random

def f(x):
    #Вычисляемая функция
    return x**4 * math.log(x + math.sqrt(x**2 - 0.36), math.e)

def Monte_karlo(a,b,N):
    #Колличество брошенных камней под или на функции
    K=0
    #Высота прямоугольника
    h = 60
    #Площадь прямоугольника
    S = h*(b-a) 
    for i in range(N):
        #Бросаем камни
        x = round(random.uniform(a, b),2)
        y = random.random()*h
        #Проверяем, находится ли камень под функцией или на ней, если да то добавляем к счётчику +1
        if f(x) >= y:
            K+=1
    #выводим интеграл
    return S*K/N
    

a = 1.25 #float(input("Введите значение начала интегрирования: "))
b = 2.45 #float(input("Введите значение конца интегрирования: "))
N = 200000 #int(input("Введите количество камней: "))
p=10
Sums=[]
for i in range(p):
    Sums.append(Monte_karlo(a,b,N))
Sum=0
KV_sum=0
for i in Sums: 
    Sum+=i
    KV_sum+=i**2

Sum = Sum/len(Sums)
KV_sum = KV_sum/len(Sums)


print(f"Результат интегрирования {Sum}, Стандартное отклонение средних {math.sqrt(abs(Sum**2-KV_sum))}")