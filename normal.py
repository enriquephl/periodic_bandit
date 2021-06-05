import numpy as np

d_mu, d_sigma = 30, 10
p_mu, p_sigma = 25, 15

def demand(t):
  return np.random.normal(d_mu, d_sigma)

def price(t):
  return np.random.normal(p_mu, p_sigma)

def compare_pairwise(arr1, arr2):
  if(len(arr1) == 0 and len(arr2) == 0):
    return [False]
  z=[]
  for x in zip(arr1,arr2):
    if x[0] <= x[1]:
      z.append(True)
    else:
      z.append(False)
  return z

if __name__ == "__main__":
  T = 100
  card_price = 800

  demand_origin = [0]
  price_origin = [0]

  cost_origin, buy_origin, win_origin = [0], [], []
  cost_random, buy_random, win_random  = [0], [], []
  cost_predict, buy_predict, win_predict= [0], [], []
  cost_always, buy_always, win_always = [0], [], []
  cost_optimal, buy_optimal, win_optimal = [0], [], []

  for i in range(1,T+1):
    demand_avg, price_avg = np.mean(demand_origin), np.mean(price_origin)
    cost_avg = np.average(cost_origin)
    print()

    demand_t, price_t = demand(i), price(i)

    # Origin cost without any cards
    dailycost_origin = np.multiply(demand_t, price_t)
    cost_origin.append(dailycost_origin)
    buy_origin.append(False)
    win_origin.append(True if dailycost_origin <= card_price else False)

    # Random buy card with probability
    daily_decision = np.random.uniform(low=0,high=1)
    dailycost_random = card_price if daily_decision >= 0.5 else dailycost_origin
    cost_random.append(dailycost_random)
    buy_random.append(True if daily_decision >= 0.5 else False)
    win_random.append(True if dailycost_random <= dailycost_origin else False)

    # Always buy card
    cost_always.append(card_price)
    buy_always.append(True)
    win_always.append(True if card_price <= dailycost_origin else False)

    # predict demand
    demand_predict = demand_t if np.random.uniform(low=0,high=1) >= 0.2 else np.random.uniform(low=20,high=50)

    buy_card = (np.multiply(demand_predict, price_avg) > card_price) and (np.random.uniform(low=0,high=1) >= 0.2)
    dailycost_predict = card_price if buy_card else dailycost_origin
    cost_predict.append(dailycost_predict)
    buy_predict.append(buy_card)
    win_predict.append(True if dailycost_predict <= dailycost_origin else False)

    # Optimal cost
    dailycost_optimal = card_price if dailycost_origin > card_price else dailycost_origin
    cost_optimal.append(dailycost_optimal)
    buy_optimal.append(True if dailycost_origin > card_price else False)
    win_optimal.append(True if dailycost_optimal <= dailycost_origin else False)

    demand_origin.append(demand_t)
    price_origin.append(price_t)

  print("Total Cost (Without Card):", np.ceil(np.sum(cost_origin)),
  "Buy days:", np.sum(buy_origin), "Win days", np.sum(win_origin))
  print("Total Cost (Random Strategy):", np.ceil(np.sum(cost_random)),
  "Buy days:", np.sum(buy_random), "Win days", np.sum(win_random))
  print("Total Cost (Predict Strategy):", np.ceil(np.sum(cost_predict)),
  "Buy days:", np.sum(buy_predict), "Win days", np.sum(win_predict))
  print("Total Cost (Always Strategy):", np.ceil(np.sum(cost_always)),
  "Buy days:", np.sum(buy_always), "Win days", np.sum(win_always))
  print("Total Cost (Optimal):", np.ceil(np.sum(cost_optimal)),
  "Buy days:", np.sum(buy_optimal), "Win days", np.sum(win_optimal))