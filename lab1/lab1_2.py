from matplotlib import pyplot as plt
import random
import numpy as np

y = [i + random.randint(-10, 10) for i in range(100)]
mean = np.mean(y)
print(f"Mean: {mean}")
std = np.std(y)
print(f"Standart diviation: {round(std,2)}")
x = np.array(list(range(100)))
plt.scatter(x, y)

b = (np.mean(x*y) - np.mean(x)*np.mean(y))/(np.mean(x**2)-np.mean(x)**2)
a = np.mean(y)-b*np.mean(x)
y2 = a+b*x
plt.plot(
    x, y2, 'r', label=f"y = {round(a,2)}+{round(b,2)}x")
plt.legend()

plt.savefig("data.png")
plt.clf()
