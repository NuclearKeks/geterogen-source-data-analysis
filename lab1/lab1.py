import pandas as pd
import yfinance as yf
import seaborn as sn
import matplotlib.pyplot as plt

# Oil&gas
companies = ['XOM',  # Exxon Mobil Corporation
             'CVX',  # Chevron Corporation
             'SHEL',  # Shell plc
             'TTE',  # TotalEnergies SE
             'EQNR',  # Equinor ASA
             'BP',  # BP p.l.c.
             'PBR',  # Petróleo Brasileiro S.A. - Petrobras
             'E',  # Eni S.p.A.
             'SU',  # Suncor Energy Inc.
             'CVE',  # Cenovus Energy Inc.
             ]
data = pd.DataFrame(columns=companies)
for company in companies:
    data[company] = yf.download(
        company, '2021-01-01', '2021-12-31')['Adj Close']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
data_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for i, month in enumerate(months):
    data_month[i] = data.loc[data.index.month == i+1]
    data_corr = data_month[i].corr(method='pearson').round(3)
    ax = plt.axes()
    data_plot = sn.heatmap(data_corr, annot=True, ax=ax)
    ax.set_title(month)
    plt.savefig(f'{month}.png')
    plt.clf()
