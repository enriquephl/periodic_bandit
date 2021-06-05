import numpy as np

d_min, d_max = 1,100
p_min, p_max = 5,20

def demand(t):
  return np.random.normal(low=d_min, high=d_max)

def price(t):
  return np.random.normal(low=p_min, high=p_max)

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
  card_price = 600

  demand_origin = [0]
  price_origin = [0]

  cost_origin, buy_origin, win_origin = [0], [], []
  cost_random, buy_random, win_random  = [0], [], []
  cost_observed, buy_observed, win_observed, = [0], [], []
  cost_always, buy_always, win_always = [0], [], []
  cost_compare, buy_compare, win_compare= [0], [], []
  cost_predict, buy_predict, win_predict= [0], [], []
  cost_moving, buy_moving, win_moving= [0], [], []
  cost_optimal, buy_optimal, win_optimal = [0], [], []

  for i in range(1,T+1):
    demand_avg, price_avg = np.average(demand_origin), np.average(price_origin)
    print(demand_avg, price_avg)
    cost_avg = np.average(cost_origin)

    demand_t, price_t = demand(i), price(i)

    # Origin cost without any cards
    dailycost_origin = np.multiply(demand_t, price_t)
    cost_origin.append(dailycost_origin)
    buy_origin.append(False)
    win_origin.append(True if dailycost_origin <= card_price else False)

    # Random buy card with probability
    daily_decision = np.random.uniform(low=0,high=1)
    dailycost_random = card_price if daily_decision >= 0.6 else dailycost_origin
    cost_random.append(dailycost_random)
    buy_random.append(True if daily_decision >= 0.6 else False)
    win_random.append(True if dailycost_random <= dailycost_origin else False)

    # by observed average
    dailycost_observed = card_price if np.multiply(demand_avg,price_avg) > card_price else dailycost_origin
    cost_observed.append(dailycost_observed)
    buy_observed.append(True if np.multiply(demand_avg,price_avg) > card_price else False)
    win_observed.append(True if dailycost_observed <= dailycost_origin else False)

    # by predict
    demand_predict = np.random.uniform(low=np.array(demand_origin).min(), high=np.array(demand_origin).max())
    price_predict = np.random.uniform(low=np.array(price_origin).min(), high=np.array(price_origin).max())
    print(demand_predict, price_predict)
    dailycost_predict= card_price if np.multiply(demand_predict,price_predict) * 3 > card_price else dailycost_origin
    cost_predict.append(dailycost_predict)
    buy_predict.append(True if np.multiply(demand_predict,price_predict) * 3 > card_price else False)
    win_predict.append(True if dailycost_predict <= dailycost_origin else False)

    # Always buy card
    cost_always.append(card_price)
    buy_always.append(True)
    win_always.append(True if card_price <= dailycost_origin else False)

    # epsilon greddy
    win_ratio = np.divide(np.sum(compare_pairwise(cost_compare, cost_origin)), i)
    print(win_ratio)
    comp_decision = np.random.uniform(low=0,high=1)
    dailycost_compare = card_price if comp_decision >= (1 - win_ratio) else dailycost_origin
    cost_compare.append(dailycost_compare)
    buy_compare.append(True if comp_decision >= (1 - win_ratio) else False)
    win_compare.append(True if dailycost_compare <= dailycost_origin else False)

    # moving average
    win_ratio_moving = np.divide(np.sum(compare_pairwise(cost_moving, cost_origin)), i)
    dailycost_moving= card_price if cost_avg / np.exp(win_ratio_moving) > card_price else dailycost_origin
    cost_moving.append(dailycost_moving)
    buy_moving.append(True if cost_avg / np.exp(win_ratio_moving) > card_price else False)
    win_moving.append(True if dailycost_predict <= dailycost_origin else False)

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
  print("Total Cost (Observed Strategy):", np.ceil(np.sum(cost_observed)),
  "Buy days:", np.sum(buy_observed), "Win days", np.sum(win_observed))
  print("Total Cost (Compare Strategy):", np.ceil(np.sum(cost_compare)),
  "Buy days:", np.sum(buy_compare), "Win days", np.sum(win_compare))
  print("Total Cost (Always Strategy):", np.ceil(np.sum(cost_always)),
  "Buy days:", np.sum(buy_always), "Win days", np.sum(win_always))
  print("Total Cost (Predict Strategy):", np.ceil(np.sum(cost_predict)),
  "Buy days:", np.sum(buy_predict), "Win days", np.sum(win_predict))
  print("Total Cost (Moving Strategy):", np.ceil(np.sum(cost_moving)),
  "Buy days:", np.sum(buy_moving), "Win days", np.sum(win_moving))
  print("Total Cost (Optimal):", np.ceil(np.sum(cost_optimal)),
  "Buy days:", np.sum(buy_optimal), "Win days", np.sum(win_optimal))