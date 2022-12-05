import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Oil&gas
companies = ['XOM',  # Exxon Mobil Corporation
             'SHEL',  # Shell plc
             'TTE',  # TotalEnergies SE
             'EQNR',  # Equinor ASA
             'BP',  # BP p.l.c.
             ]
values = ['Open', 'High', 'Low', 'Close', 'Volume']
# example = companies['XOM']
for company in companies:
    example = yf.download(
        company, '2021-01-01', '2021-12-31')
    # удаляем цену, т.к. смотрим влияние на неё
    x = example.drop(columns='Adj Close')
    y = example['Adj Close']

    # разделение данных на тренировочные и тестовые 20%/80%
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0)
    # нормализация данных
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    # PCA
    pca = PCA()
    X_train = pca.fit_transform(X_train)
    X_test = pca.fit_transform(X_test)
    # объяснённый коэффициент дисперсии
    explained_variance = np.round(pca.explained_variance_ratio_, 3)*100

    final = {
        values[i]: f'{explained_variance[i]}%' for i in range(len(values))}
    print('-----------', company, final, sep='\n')
