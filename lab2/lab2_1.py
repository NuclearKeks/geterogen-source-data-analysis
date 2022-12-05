import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Oil&gas
companies = ['XOM',  # Exxon Mobil Corporation
             'SHEL',  # Shell plc
             'TTE',  # TotalEnergies SE
             'EQNR',  # Equinor ASA
             'BP',  # BP p.l.c.
             ]
data = pd.DataFrame(columns=companies)
for company in companies:
    data[company] = yf.download(
        company, '2021-01-01', '2021-12-31')['Adj Close']

days = list(range(len(data)))

win = 5
weights = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
for company in companies:
    plt.plot(days, data[company], label='Without aliasing')
    sma_company = data[company].rolling(win).mean().iloc[win-1:]
    wma_company = data[company].rolling(win).apply(
        lambda x: np.sum(weights*x)/weights.sum())
    plt.plot(list(range(len(sma_company))), sma_company,
             'y', label=f'SMA, window={win}')
    plt.plot(list(range(len(wma_company))), wma_company,
             'r--', label=f'WMA, window={win}')
    plt.legend()
    plt.xlabel('Дни в году')
    plt.ylabel('Цена закрытия')
    plt.title(company)
    plt.savefig(f'lab2/pictures/{company}.png')
    plt.clf()
