import numpy as np

d_mu, d_sigma = 30, 10
p_mu = np.random.uniform(low=20,high=100)

def demand(t):
  return np.random.normal(d_mu, d_sigma)

def price(t):
  p_low = 20 + np.abs(np.sin(t)) * np.random.random() * 180
  p_high = 300 - np.abs(np.sin(t)) * np.random.random() * 100
  if np.random.random() >= 0.6:
      p_final = 20 + np.random.random() * 10
  else:
      p_final = np.random.uniform(low=p_low,high=p_high)
  return p_final

if __name__ == "__main__":
  T = 100
  price_expectaion = np.mean([price(x)*demand(x) for x in range(T)])
  card_price = price_expectaion + 1000
  print(price_expectaion, price_expectaion * T)

  demand_origin = [0]
  price_origin = [0]

  cost_origin, buy_origin, win_origin = [0], [], []
  cost_random, buy_random, win_random  = [0], [], []
  cost_predict, buy_predict, win_predict= [0], [], []
  cost_always, buy_always, win_always = [0], [], []
  cost_optimal, buy_optimal, win_optimal = [0], [], []

  for i in range(1,T+1):
    demand_avg = np.mean(demand_origin)
    price_avg = np.mean(price_origin)
    #price_avg = np.mean(price_origin) if i < 100 else np.mean(price_origin[i-100:i-1])
    cost_avg = np.average(cost_origin)

    demand_t, price_t = demand(i), price(i)

    # Origin cost without any cards
    dailycost_origin = np.multiply(demand_t, price_t)
    cost_origin.append(dailycost_origin)
    buy_origin.append(False)
    win_origin.append(True if dailycost_origin <= card_price else False)

    # Random buy card with probability
    daily_decision = np.random.uniform(low=0,high=1)
    dailycost_random = card_price if daily_decision >= 0.4 else dailycost_origin
    cost_random.append(dailycost_random)
    buy_random.append(True if daily_decision >= 0.4 else False)
    win_random.append(True if dailycost_random == np.min([dailycost_origin,card_price]) else False)

    # Always buy card
    cost_always.append(card_price)
    buy_always.append(True)
    win_always.append(True if card_price == np.min([dailycost_origin,card_price]) else False)

    # predict demand
    correct_ratio = 0.7

    buy_card = (np.multiply(demand_t, price_avg) > card_price) and (np.random.random() >= (1 - correct_ratio))
    dailycost_predict = card_price if buy_card else dailycost_origin
    cost_predict.append(dailycost_predict)
    buy_predict.append(buy_card)
    win_predict.append(True if dailycost_predict == np.min([dailycost_origin,card_price]) else False)

    # Optimal cost
    dailycost_optimal = card_price if dailycost_origin > card_price else dailycost_origin
    cost_optimal.append(dailycost_optimal)
    buy_optimal.append(True if dailycost_origin > card_price else False)
    win_optimal.append(True if dailycost_optimal == np.min([dailycost_origin,card_price]) else False)

    demand_origin.append(demand_t)
    price_origin.append(price_t)

  print("Total Cost (Without Card):", np.ceil(np.sum(cost_origin)),
  "Buy days:", np.sum(buy_origin), "Win days", np.sum(win_origin))
  print("Total Cost (Random Strategy):", np.ceil(np.sum(cost_random)),
  "Buy days:", np.sum(buy_random), "Win days", np.sum(win_random))
  print("Total Cost (Always Strategy):", np.ceil(np.sum(cost_always)),
  "Buy days:", np.sum(buy_always), "Win days", np.sum(win_always))
  print("Total Cost (Predict Strategy):", np.ceil(np.sum(cost_predict)),
  "Buy days:", np.sum(buy_predict), "Win days", np.sum(win_predict))
  print("Total Cost (Optimal):", np.ceil(np.sum(cost_optimal)),
  "Buy days:", np.sum(buy_optimal), "Win days", np.sum(win_optimal))