# Monte-Carlo method, case 1
import matplotlib.pyplot as plt
import random
from numpy import std, sqrt


def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    if dice1 == dice2:
        return True
    else:
        return False


num_sim = 1000
num_throws = 500
bet = 1
win_coef = 5

win_prob = []
end_balance = []

fig = plt.figure()
plt.title(f'Игра в кости, метод Монте-Карло, {num_sim} симуляций')
plt.xlabel('Бросок кубика')
plt.ylabel('Баланс игрока')
plt.xlim([0, num_throws])

for i in range(num_sim):
    balance = [1000]
    num_rolls = [0]
    num_wins = 0
    while num_rolls[-1] < num_throws:
        same = roll_dice()
        if same:
            balance.append(balance[-1] + win_coef * bet)
            num_wins += 1
        else:
            balance.append(balance[-1] - bet)

        num_rolls.append(num_rolls[-1] + 1)
    win_prob.append(num_wins/num_rolls[-1])
    end_balance.append(balance[-1])
    plt.plot(num_rolls, balance)
#
plt.savefig('lab3/lab3_1.png')
#
overall_win_probability = round(sum(win_prob)/len(win_prob)*100, 2)
overall_end_balance = round(sum(end_balance)/len(end_balance), 2)
print(
    f"Усреднённая вероятность выигрыша среди {num_sim} попыток: {overall_win_probability}%")
print(
    f"Усреднённый конечный баланс среди {num_sim} попыток: {overall_end_balance}₽")
# error estimation
delta = 1.6463788*std(win_prob)/sqrt(len(win_prob))
print(f'Оценка погрешности δ: {delta}')
