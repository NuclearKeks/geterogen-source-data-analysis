# Monte-Carlo method, case 2
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')
avg = 1
std = 0.1
num_reps = 500
num_simulations = 1000
distribution = np.random.normal(avg, std, num_reps).round(2)

sales_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
sales_prob = [0.3, 0.3, 0.2, 0.1, 0.05, 0.05]
sales = np.random.choice(sales_values, num_reps, p=sales_prob)

df = pd.DataFrame(index=range(num_reps),
                  data={'Pct_To_Target': distribution,
                        'Sales_Target': sales})

plt.hist(df['Pct_To_Target'])
plt.title('Распределение за прошлый год')
plt.savefig('lab3/Распределение за прошлый год.png')
plt.clf()
plt.hist(df['Sales_Target'])
plt.title('Цель продаж')
plt.savefig('lab3/Цель продаж.png')
plt.clf()


def calc_commission(x):
    """ Вернуть комиссию по принципу:
    \n0-90% = 2%
    \n91-99% = 3%
    \n>= 100 = 4%
    """
    if x <= .90:
        return .02
    if x <= .99:
        return .03
    else:
        return .04


all_stats = []
num_sims = 1000

for i in range(num_sims):
    # Cлучайные входные данные для целей продаж и процент для целей
    sales_target = np.random.choice(sales_values, num_reps, p=sales_prob)
    pct_to_target = np.random.normal(avg, std, num_reps).round(2)
    df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
                                                   'Sales_Target': sales_target})
    #
    df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']
    df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission)
    df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']
    # Продажи, суммы комиссионных и целевые показатели продаж по всем симуляциям
    all_stats.append([df['Sales'].sum().round(0),
                      df['Commission_Amount'].sum().round(0),
                      df['Sales_Target'].sum().round(0)])

results_df = pd.DataFrame.from_records(all_stats, columns=['Sales',
                                                           'Commission_Amount',
                                                           'Sales_Target'])
plt.hist(results_df['Commission_Amount'])
plt.title('Комиссионные')
plt.savefig('lab3/Комиссионные.png')
plt.clf()
