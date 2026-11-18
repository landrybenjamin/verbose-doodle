import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.random.seed(42)
plt.rcParams['figure.figsize'] = (7, 4)
print('Ready!')



# ## 1. Savings growth: simple vs compound interest

principal, rate, years = 1000, 0.05, 30
t = np.arange(years + 1)
simple = principal * (1 + rate * t)
compound = principal * (1 + rate) ** t

plt.plot(t, simple, label='Simple interest')
plt.plot(t, compound, label='Compound interest')
plt.xlabel('Years'); plt.ylabel('Euros'); plt.title('Savings growth'); plt.legend(); plt.show()
print(f'After {years} years: simple = {simple[-1]:.0f}, compound = {compound[-1]:.0f}')




# ## 2. Loan payments: how a loan is paid off

P, annual_rate, years = 10000, 0.06, 5
r, n = annual_rate / 12, years * 12
payment = P * r / (1 - (1 + r) ** -n)

balance, balances, interest_paid = P, [P], 0
for _ in range(n):
    interest = balance * r
    interest_paid += interest
    balance = balance - (payment - interest)
    balances.append(balance)

print(f'Monthly payment: {payment:.2f}')
print(f'Total interest paid: {interest_paid:.2f}')
plt.plot(balances); plt.xlabel('Month'); plt.ylabel('Remaining debt'); plt.title('Loan balance'); plt.show()





# ## 3. A cooling cup of coffee

T0, T_room, k = 90, 20, 0.08   # start temp, room temp, cooling rate per minute
dt, minutes = 0.5, 60
times = np.arange(0, minutes, dt)

T, temps = T0, []
for _ in times:
    temps.append(T)
    T = T + dt * (-k * (T - T_room))     # Euler step

exact = T_room + (T0 - T_room) * np.exp(-k * times)
plt.plot(times, temps, label='Euler simulation')
plt.plot(times, exact, '--', label='Exact formula')
plt.axhline(55, color='gray', ls=':', label='Drinkable (55°C)')
plt.xlabel('Minutes'); plt.ylabel('°C'); plt.legend(); plt.show()
print('Drinkable after about', times[np.argmax(np.array(temps) < 55)], 'minutes')




# %% ------------------------------------------------------------
# ## 4. Commute time: Monte Carlo simulation

n_days = 10000
base = np.random.normal(30, 4, n_days)                 # normal commute, minutes
delay = (np.random.rand(n_days) < 0.10) * np.random.exponential(15, n_days)  # 10% of days: a delay
commute = base + delay

print(f'Average commute: {commute.mean():.1f} min')
print(f'Chance commute > 40 min: {(commute > 40).mean():.1%}')
print(f'95% of days it takes under {np.percentile(commute, 95):.0f} min')
plt.hist(commute, bins=50); plt.xlabel('Minutes'); plt.title('Simulated commute times'); plt.show()




# %% ------------------------------------------------------------
# ## 5. The birthday paradox

def theory(n):
    p_all_different = np.prod([(365 - i) / 365 for i in range(n)])
    return 1 - p_all_different

def simulate(n, trials=5000):
    hits = 0
    for _ in range(trials):
        birthdays = np.random.randint(0, 365, n)
        hits += len(set(birthdays)) < n
    return hits / trials

sizes = range(2, 60)
plt.plot(sizes, [theory(n) for n in sizes], label='Theory')
plt.scatter(sizes[::4], [simulate(n) for n in sizes[::4]], color='red', label='Simulation')
plt.axhline(0.5, ls=':', color='gray'); plt.xlabel('People in room'); plt.ylabel('P(shared birthday)'); plt.legend(); plt.show()
print('n = 23 ->', round(theory(23), 3))




# %% ------------------------------------------------------------
# ## 6. A positive medical test: what does it really mean?

def bayes(prevalence, sensitivity, specificity):
    p_pos = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
    return sensitivity * prevalence / p_pos

print('Disease affects 1 in 1000, test is 99% accurate:')
print(f'P(sick | positive) = {bayes(0.001, 0.99, 0.99):.1%}')

prevalences = np.logspace(-4, -0.5, 100)
plt.semilogx(prevalences, [bayes(p, 0.99, 0.99) for p in prevalences])
plt.xlabel('How common the disease is'); plt.ylabel('P(sick | positive test)'); plt.title('Rare diseases fool accurate tests'); plt.show()



# %% ------------------------------------------------------------
# ## 7. Predicting house prices

size = np.random.uniform(30, 150, 80)
price = 2000 * size + 30000 + np.random.normal(0, 20000, 80)   # hidden 'truth' + noise

slope, intercept = np.polyfit(size, price, 1)
plt.scatter(size, price, alpha=0.6)
xs = np.array([30, 150])
plt.plot(xs, slope * xs + intercept, color='red')
plt.xlabel('Size (m²)'); plt.ylabel('Price (€)'); plt.show()
print(f'Model: price = {slope:.0f} × size + {intercept:.0f}')
print(f'Predicted price for 80 m²: €{slope * 80 + intercept:,.0f}')


# %% ------------------------------------------------------------
# ## 8. How machines learn: gradient descent

x = np.random.uniform(0, 10, 50)
y = 3 * x + 5 + np.random.normal(0, 2, 50)

w, b, lr = 0.0, 0.0, 0.01
losses = []
for step in range(500):
    pred = w * x + b
    error = pred - y
    losses.append((error ** 2).mean())
    w -= lr * 2 * (error * x).mean()     # derivative of loss wrt w
    b -= lr * 2 * error.mean()           # derivative of loss wrt b

print(f'Learned: y = {w:.2f}x + {b:.2f}   (true: 3x + 5)')
plt.plot(losses); plt.xlabel('Step'); plt.ylabel('Mean squared error'); plt.title('Loss going down'); plt.show()




# %% ------------------------------------------------------------
# ## 9. A tiny spam filter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

emails = ['win free money now', 'free prize claim now', 'cheap loans win cash',
          'meeting at noon tomorrow', 'lunch with the team', 'project report attached',
          'claim your free cash prize', 'can we move the meeting', 'notes from the lecture']
labels = [1, 1, 1, 0, 0, 0, 1, 0, 0]    # 1 = spam

vec = CountVectorizer()
model = MultinomialNB().fit(vec.fit_transform(emails), labels)

tests = ['free cash prize', 'team meeting tomorrow', 'win a free lunch']
for text, p in zip(tests, model.predict_proba(vec.transform(tests))[:, 1]):
    print(f'{text!r:30} spam probability = {p:.0%}')




# %% ------------------------------------------------------------
# ## 10. Grouping customers without labels

from sklearn.cluster import KMeans

a = np.random.normal([2, 20], [0.8, 5], (60, 2))     # rare visitors, small spend
b = np.random.normal([10, 30], [1.5, 6], (60, 2))    # frequent, small spend
c = np.random.normal([6, 90], [1.5, 10], (60, 2))    # medium visits, big spend
X = np.vstack([a, b, c])

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
plt.scatter(X[:, 0], X[:, 1], c=km.labels_, cmap='viridis', alpha=0.7)
plt.scatter(*km.cluster_centers_.T, c='red', marker='X', s=200)
plt.xlabel('Visits per month'); plt.ylabel('Average spend (€)'); plt.title('Discovered customer groups'); plt.show()



# %% ------------------------------------------------------------
# ## 11. Should I take an umbrella? A decision tree

from sklearn.tree import DecisionTreeClassifier, export_text

humidity = np.random.uniform(20, 100, 300)
clouds = np.random.uniform(0, 100, 300)
rain = ((humidity > 70) & (clouds > 50)) | (np.random.rand(300) < 0.05)

X = np.column_stack([humidity, clouds])
tree = DecisionTreeClassifier(max_depth=2).fit(X, rain)
print(export_text(tree, feature_names=['humidity', 'clouds']))
print('Take umbrella at humidity 85, clouds 80?', bool(tree.predict([[85, 80]])[0]))



# %% ------------------------------------------------------------
# ## 12. Will I pass the exam?

from sklearn.linear_model import LogisticRegression

hours = np.random.uniform(0, 10, 100)
p_true = 1 / (1 + np.exp(-(hours - 5)))
passed = np.random.rand(100) < p_true

clf = LogisticRegression().fit(hours.reshape(-1, 1), passed)
grid = np.linspace(0, 10, 100).reshape(-1, 1)
plt.scatter(hours, passed, alpha=0.4)
plt.plot(grid, clf.predict_proba(grid)[:, 1], color='red')
plt.xlabel('Hours studied'); plt.ylabel('P(pass)'); plt.show()
for h in [2, 5, 8]:
    print(f'{h} hours -> {clf.predict_proba([[h]])[0, 1]:.0%} chance of passing')



# %% ------------------------------------------------------------
# ## 13. The café queue

import heapq

def average_wait(n_servers, arrival_rate=1.0, mean_service=1.8, n_customers=5000):
    arrivals = np.cumsum(np.random.exponential(1 / arrival_rate, n_customers))
    services = np.random.exponential(mean_service, n_customers)
    free_at = [0.0] * n_servers
    heapq.heapify(free_at)
    waits = []
    for arr, svc in zip(arrivals, services):
        earliest = heapq.heappop(free_at)
        start = max(arr, earliest)
        waits.append(start - arr)
        heapq.heappush(free_at, start + svc)
    return np.mean(waits)

servers = [2, 3, 4, 5]
waits = [average_wait(s) for s in servers]
plt.bar([str(s) for s in servers], waits)
plt.xlabel('Number of baristas'); plt.ylabel('Average wait (minutes)'); plt.show()
print(dict(zip(servers, np.round(waits, 2))))



# %% ------------------------------------------------------------
# ## 14. Stock prices as random walks

days, paths = 250, 20
daily_mu, daily_sigma = 0.0004, 0.012
returns = np.random.normal(daily_mu, daily_sigma, (days, paths))
prices = 100 * np.exp(np.cumsum(returns, axis=0))

plt.plot(prices, alpha=0.6); plt.xlabel('Trading day'); plt.ylabel('Price'); plt.title('20 possible years'); plt.show()
print(f'Final price range: {prices[-1].min():.0f} to {prices[-1].max():.0f}')




# %% ------------------------------------------------------------
# ## 15. How an epidemic spreads (SIR model)

def sir(beta, gamma=0.1, days=160, N=1000, I0=1):
    S, I, R = N - I0, I0, 0
    history = []
    for _ in range(days):
        new_inf = beta * S * I / N
        new_rec = gamma * I
        S, I, R = S - new_inf, I + new_inf - new_rec, R + new_rec
        history.append(I)
    return history

plt.plot(sir(0.30), label='No measures (β=0.30)')
plt.plot(sir(0.18), label='Some distancing (β=0.18)')
plt.xlabel('Day'); plt.ylabel('Infected people'); plt.legend(); plt.title('Flattening the curve'); plt.show()




# %% ------------------------------------------------------------
# ## 16. Population growth with limits

r, K, dt = 0.4, 1000, 0.1
t = np.arange(0, 30, dt)
P_limited, P_free = [10], [10]
for _ in t[1:]:
    P_limited.append(P_limited[-1] + dt * r * P_limited[-1] * (1 - P_limited[-1] / K))
    P_free.append(P_free[-1] + dt * r * P_free[-1])

plt.plot(t, P_limited, label='With limited resources')
plt.plot(t, P_free, label='Unlimited (exponential)')
plt.ylim(0, 1500); plt.xlabel('Time'); plt.ylabel('Population'); plt.legend(); plt.show()




# %% ------------------------------------------------------------
# ## 17. A movie recommender

movies = ['Action A', 'Action B', 'Romance A', 'Romance B', 'Sci-fi A']
ratings = pd.DataFrame(
    [[5, 4, 1, 1, 4],
     [4, 5, 2, 1, 5],
     [1, 2, 5, 5, 2],
     [2, 1, 4, 5, 1],
     [5, 0, 0, 0, 0]],      # new user: 0 = not seen
    index=['Ana', 'Ben', 'Chiara', 'Dario', 'You'], columns=movies)

def cosine(u, v):
    return u @ v / (np.linalg.norm(u) * np.linalg.norm(v))

you = ratings.loc['You'].values
sims = {name: cosine(you, ratings.loc[name].values) for name in ratings.index[:-1]}
print('Similarity to you:', {k: round(v, 2) for k, v in sims.items()})

scores = {m: sum(sims[n] * ratings.loc[n, m] for n in sims) / sum(sims.values())
          for m in movies if ratings.loc['You', m] == 0}
print('Recommended (best first):', sorted(scores, key=scores.get, reverse=True))




# %% ------------------------------------------------------------
# ## 18. Who is the most influential person in a network? (PageRank)

names = ['Ana', 'Ben', 'Chiara', 'Dario', 'Elena']
# links[i][j] = 1 if person i follows person j
links = np.array([[0, 1, 1, 0, 0],
                  [0, 0, 1, 0, 0],
                  [1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 1],
                  [0, 0, 1, 1, 0]], dtype=float)

M = (links / links.sum(axis=1, keepdims=True)).T      # column-stochastic
d, n = 0.85, len(names)
rank = np.ones(n) / n
for _ in range(100):
    rank = (1 - d) / n + d * M @ rank

for name, score in sorted(zip(names, rank), key=lambda x: -x[1]):
    print(f'{name:8} {score:.3f}')




# %% ------------------------------------------------------------
# ## 19. Shortest route (Google Maps idea)

import heapq

graph = {'Home': {'Bus stop': 5, 'Metro': 12},
         'Bus stop': {'Park': 10, 'Metro': 4},
         'Metro': {'Bocconi': 8, 'Park': 6},
         'Park': {'Bocconi': 7},
         'Bocconi': {}}

def dijkstra(graph, start, goal):
    queue, seen = [(0, start, [start])], set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return cost, path
        if node in seen:
            continue
        seen.add(node)
        for nxt, w in graph[node].items():
            heapq.heappush(queue, (cost + w, nxt, path + [nxt]))

cost, path = dijkstra(graph, 'Home', 'Bocconi')
print(f'Fastest route: {" -> ".join(path)}  ({cost} minutes)')



# %% ------------------------------------------------------------
# ## 20. A tiny neural network from scratch

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

sigmoid = lambda z: 1 / (1 + np.exp(-z))
W1, b1 = np.random.randn(2, 4), np.zeros((1, 4))
W2, b2 = np.random.randn(4, 1), np.zeros((1, 1))

lr = 1.0
for epoch in range(5000):
    h = sigmoid(X @ W1 + b1)               # forward pass
    out = sigmoid(h @ W2 + b2)
    d_out = (out - y) * out * (1 - out)    # backward pass (chain rule)
    d_h = d_out @ W2.T * h * (1 - h)
    W2 -= lr * h.T @ d_out;  b2 -= lr * d_out.sum(0, keepdims=True)
    W1 -= lr * X.T @ d_h;    b1 -= lr * d_h.sum(0, keepdims=True)

print('Predictions:', out.round(2).ravel(), ' target:', y.ravel())


