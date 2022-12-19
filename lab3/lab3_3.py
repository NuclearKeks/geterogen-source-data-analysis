# Monte-Carlo integrals
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


def monte_carlo_inegral(func, a=0, b=1, n=1000):

    subsets = np.arange(0, n+1, n/10)
    u = np.zeros(n)
    for i in range(10):
        start = int(subsets[i])
        stop = int(subsets[i+1])
        u[start:stop] = np.random.uniform(
            low=i/10, high=(i+1)/10, size=stop-start)
    np.random.shuffle(u)
    u_func = func(a+(b-a)*u)
    s = ((b-a)/n)*u_func.sum()
    return s


def f(x):
    return(62*x**5+21*x**2-11*x+8)**(1/3)


integral = monte_carlo_inegral(f, a=0, b=5, n=100)
integral_classic = integrate.quad(f, 0, 5)
print(integral)
print(integral_classic[0])

x = list(range(10, 1000, 5))
classic_graph = [integral_classic[0] for i in x]
monte_graph = [monte_carlo_inegral(f, a=0, b=5, n=i) for i in x]

plt.title(f'Интегрирование классическим методом и методом Монте-Карло')
plt.xlabel('Количество выборок')
plt.ylabel('Значение интеграла')
plt.plot(x, classic_graph, label='Классический метод')
plt.plot(x, monte_graph, label='Метод Монте-Карло')
plt.legend()
plt.savefig('lab3/lab3_3.png')
plt.clf()
