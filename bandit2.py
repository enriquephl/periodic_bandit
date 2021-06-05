import numpy as np

d_mu, d_sigma = 30, 10
p_mu, p_sigma = 200, 20
b_mu, b_sigma = 3000, 200
c_mu, c_sigma = 5000, 300

def demand(t):
  return np.random.normal(d_mu, d_sigma)

def price(t):
  return np.random.normal(p_mu, p_sigma)

def B(t):
  return np.random.normal(b_mu, b_sigma)

def C(t):
  return np.random.normal(c_mu, c_sigma)

if __name__ == "__main__":
  T = 100
  K = 3

  demand_origin = [0]
  price_origin = [0]

  cost_origin, action_origin, win_origin, regret_origin = [0], [-1], [False], [0]
  cost_exp3, action_exp3, win_exp3, regret_exp3= [0], [-1], [False], [0]
  cost_always, action_always, win_always, regret_always = [0], [-1], [False], [0]
  cost_optimal, action_optimal, win_optimal, regret_optimal = [0], [-1], [False], [0]

  weight=[[1] * K for x in range(0,T+2)]
  prob=[[1] * K for x in range(0,T+2)] # 0: use origin, 1: use card

  gamma = 0.5

  for i in range(1,T+1):
    demand_avg = np.mean(demand_origin)
    price_avg = np.mean(price_origin)
    cost_avg = np.average(cost_origin)

    demand_t, price_t = demand(i), price(i)
    card_B, card_C = B(i), C(i)
    daily_optimal = np.min([np.multiply(demand_t, price_t), card_B, card_C])
    daily_div = np.max([np.multiply(demand_t, price_t), card_B, card_C]) - np.min([np.multiply(demand_t, price_t), card_B, card_C])

    # Origin cost without any cards
    dailycost_origin = np.multiply(demand_t, price_t)
    cost_origin.append(dailycost_origin)
    win_origin.append(dailycost_origin == daily_optimal)
    regret_origin.append(np.max([0,dailycost_origin - daily_optimal]) / daily_div)

    # exp3
    for arm in range(K):
      prob[i][arm] = (1 - gamma)*(weight[i][arm])/np.sum(weight[i]) + gamma/2

    draw = np.random.choice([0,1,2], 1, p=np.array(prob[i])/np.sum(prob[i]))

    print(draw, prob[i])

    if draw == 0: # not buy
      dailycost_exp3 = dailycost_origin
    elif draw == 1:
      dailycost_exp3 = card_B
    else:
      dailycost_exp3 = card_C

    x_hat = [0] * K
    for arm in range(K):
      if arm == draw:
        x_hat[arm] = (np.max([0,dailycost_exp3 - daily_optimal]) / daily_div) / prob[i][arm]
      else:
        x_hat[arm] = 0
      weight[i+1][arm] = weight[i][arm]*np.exp(gamma*x_hat[arm]/K)

    cost_exp3.append(dailycost_exp3)
    win_exp3.append(dailycost_exp3 == daily_optimal)
    regret_exp3.append(np.max([0,dailycost_exp3 - daily_optimal]) / daily_div)

    # Optimal cost
    cost_optimal.append(daily_optimal)
    win_optimal.append(True)
    regret_optimal.append(0)

    demand_origin.append(demand_t)
    price_origin.append(price_t)

  print("Total Cost (Without Card):", np.ceil(np.sum(cost_origin)),
  "Regret: ", np.sum(regret_origin),
  "Win days", np.sum(win_origin))
  print("Total Cost (Exp3 Strategy):", np.ceil(np.sum(cost_exp3)),
  "Regret: ", np.sum(regret_exp3),
  "Win days", np.sum(win_exp3))
  print("Total Cost (Optimal):", np.ceil(np.sum(cost_optimal)),
  "Regret: ", np.sum(regret_optimal),
  "Win days", np.sum(win_optimal))