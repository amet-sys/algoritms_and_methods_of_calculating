import math
import matplotlib.pyplot 

def f(x):
    return x - math.sin(2*x)


fig, axes = matplotlib.pyplot.subplots(10,10)
print(fig)