import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import random
from math import isnan

companies = ['V',  # Visa
             'MA']  # Mastercard
data = pd.DataFrame(columns=companies)
for company in companies:
    data[company] = yf.download(
        company, '2021-01-01', '2021-12-31')['Adj Close']
weeks = list(range(1, 53))


def corr_matrix(koeffs_list: list, dataset):
    for week in weeks:
        weekly_data = dataset.loc[dataset.index.isocalendar().week == week]
        data_corr = weekly_data.corr(method='pearson').round(8)
        koeffs_list.append(data_corr['V'][1])


corr_coefs = []
corr_matrix(corr_coefs, data)
plt.plot(weeks, corr_coefs)
plt.xlabel('Weeks of year')
plt.ylabel('Pearson coef')
plt.savefig('lab1_3.png')
plt.clf()

# Удаление случайных данных
incomplete_data = data.copy()
diapason1 = list(range(20, 360))
diapason2 = list(range(20, 360))
for i in range(0, len(data)//3):
    n1 = random.choice(diapason1)
    n2 = random.choice(diapason2)
    incomplete_data['V'].loc[incomplete_data.index.day_of_year ==
                             n1] = None
    incomplete_data['MA'].loc[incomplete_data.index.day_of_year ==
                              n2] = None
    diapason1.pop(diapason1.index(n1))
    diapason2.pop(diapason2.index(n2))
missing_coefs = []
corr_matrix(missing_coefs, incomplete_data)
plt.plot(weeks, missing_coefs)
plt.savefig('lab1_3-1.png')
plt.clf()

# Винзорирование(с заменой на предыдущие значения)
vins_data = incomplete_data.copy()


def vins():
    for i, day in enumerate(vins_data.index.day_of_year):
        visa = vins_data['V'][i]
        master = vins_data['MA'][i]
        if isnan(visa) or isnan(master):
            if isnan(visa):
                vins_data['V'][i] = vins_data['V'][i-1]
                vins()
            if isnan(master):
                vins_data['MA'][i] = vins_data['MA'][i-1]
                vins()
            continue


vins()

vins_coefs = []
corr_matrix(vins_coefs, vins_data)
plt.plot(weeks, vins_coefs, 'r')
plt.savefig('lab1_3-2.png')
plt.clf()


# Линейная аппроксимация
linear_data = incomplete_data.copy()


def linear():
    for company in companies:
        for i, day in enumerate(linear_data.index.day_of_year):
            price = linear_data[company][i]
            if isnan(price):
                x1 = i-1
                y1 = linear_data[company][i-1]
                for j in range(x1+1, len(linear_data)):
                    if not isnan(linear_data[company][j]):
                        x2 = j
                        y2 = linear_data[company][j]
                        break
                for k in range(x1+1, x2):
                    linear_data[company][k] = (k-x1)*(y2-y1)/(x2-x1)+y1
                linear()


linear()

linear_coefs = []
corr_matrix(linear_coefs, linear_data)
plt.plot(weeks, linear_coefs, 'g')
plt.savefig('lab1_3-3.png')
plt.clf()

# Корреляционное восстановление

corr_rep_data = incomplete_data.copy()


def corr():
    for i, day in enumerate(corr_rep_data.index.day_of_year):
        for company in ['V', 'MA']:
            price = corr_rep_data[company][i]
            if isnan(price):
                if company == 'V' and not isnan(corr_rep_data['MA'][i]):
                    corr_rep_data['V'][i] = corr_rep_data['V'][i-1] * \
                        corr_rep_data['MA'][i]/corr_rep_data['MA'][i-1]
                elif company == 'MA' and not isnan(corr_rep_data['V'][i]):
                    corr_rep_data['MA'][i] = corr_rep_data['MA'][i-1] * \
                        corr_rep_data['V'][i]/corr_rep_data['V'][i-1]


corr()
corr_rep_coefs = []
corr_matrix(corr_rep_coefs, corr_rep_data)
plt.plot(weeks, corr_rep_coefs, 'c')
plt.savefig('lab1_3-4.png')
plt.clf()

figure, axis = plt.subplots(2, 2)

axis[0, 0].plot(weeks, missing_coefs)
axis[0, 0].set_title('С пропусками')
axis[0, 1].plot(weeks, vins_coefs, 'r')
axis[0, 1].set_title('Винзорирование')
axis[1, 0].plot(weeks, linear_coefs, 'g')
axis[1, 0].set_title('Линейн. аппрокс.')
axis[1, 1].plot(weeks, corr_rep_coefs, 'c')
axis[1, 1].set_title('Корр. восст.')

plt.savefig('lab1_3-methods.png')
plt.clf()
