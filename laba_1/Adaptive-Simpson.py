import math 

def f(x):
    return 1/(0.01+abs(x))
def Simpson(a,b,N):
    h=(b-a)/N
    Simpson_sum=f(a)+f(b)
    for i in range(1,N):
        if i%2==0:
            Simpson_sum += 2*f(a+i*h)
        else:
            Simpson_sum += 4*f(a+i*h)
    return Simpson_sum/3*h

def Runge(a,b,N,eps):
    #Переменная суммы двух вызовов метода Симпсона
    S=0
    #Массив для сохранения разделённых отрезков
    Dels=[]
    Sum=0
    S_old=Simpson(a,b,N)
    #Деление первого отрезка [a,b] и рассчёт по ним интегралов 
    m = a+((b-a)/2)
    S1 = Simpson(a,m,N)
    S2 = Simpson(m,b,N)
    #Проверяем по методу Рунге, если точность подходит, возвращаем сумму двух рассчитанных интервалов,
    #иначе добавляем оба интервала в массив и делим эпсилон пополам
    if abs(S1+S2-S_old) < eps:
        Sum+= S1+S2
        return Sum
    else:
        eps /= 2
        Dels.append([a,m])
        Dels.append([m,b])
    #Запускаем данную функцию для каждого интервала в массиве
    for i in Dels:
        S = Runge(i[0],i[1],N,eps)
        Sum += S
    return  Sum


a = -1 #float(input("Введите значение начала интегрирования: "))
b = 1 #float(input("Введите значение конца интегрирования: "))
N = 2 #int(input("Введите количество камней: "))
eps = 0.0001

result = Runge(a,b,N,eps)
print(f"Результат интегрирования {result:.5f}")