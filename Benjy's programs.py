"""20 Simple Models & Programs to Understand Everyday Life: beginner edition.
Split at the "# %%" markers to use as Colab cells, or run: python bocconi_20_programs_beginner.py
"""


# %% ------------------------------------------------------------
# ## 🧭 How to use this notebook (read this first!)
# You do **not** need any background. Every program has three parts:
# 1. A **title + question** from everyday life (the grey/white text),
# 2. A **code cell** (the box with a ▶ play button on its left). Click ▶ to run it, or use *Runtime → Run all*.
# 3. A **🧠 Explained for beginners** box right after it, telling you in plain words what happened and why.
#
# **Tip:** run the cells in order, from the top. Then change a number in a code cell, run it again, and see what changes. Experimenting is how you learn.
#
# ### Python in 2 minutes (the only things you need)
# | Word | What it means | Example |
# |---|---|---|
# | **Variable** | A labelled box that holds a value | `rate = 0.05` |
# | **List / array** | Many values in one row | `[1, 2, 3]` or `np.arange(5)` → 0,1,2,3,4 |
# | **Loop** | Repeat something many times | `for month in range(12): ...` |
# | **Function** | A reusable recipe you give a name to | `def bayes(...): ...` |
# | **Library / import** | A toolbox someone else wrote | `import numpy as np` |
# | **Comment** | A note for humans; the computer ignores it | `# this is a note` |
# | **Plot** | A picture of numbers | `plt.plot(x, y)` |
# | `**` | "to the power of" | `2 ** 3` = 8 |
# | `f'...{x}...'` | Put a variable's value inside text | `f'Total: {total}'` |
# | **Random seed** | Makes "random" numbers repeat the same each run | `np.random.seed(42)` |
#
# You will not be graded on memorising any of this. Just run, look, and read the explanation.

# %% ------------------------------------------------------------
# ## 0. Setup: loading our toolboxes
# **In plain words:** Python can do basic things on its own, but for maths and graphs we borrow "toolboxes" (libraries).
# - `numpy` (shortened to `np`): fast maths on many numbers at once
# - `pandas` (`pd`): tables of data, like a spreadsheet
# - `matplotlib` (`plt`): drawing graphs
# - `np.random.seed(42)`: makes the random numbers the same every time, so your results match this explanation
#
# Run the next cell once. It should print `Ready!`.
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.random.seed(42)
plt.rcParams['figure.figsize'] = (7, 4)
print('Ready!')


# %% ------------------------------------------------------------
# ## 1. Savings growth: simple vs compound interest
# **Everyday question:** If I save €1000 at 5% a year, how much will I have in 30 years?
# **Math:** exponential growth, A = P(1+r)^t
# %%
principal, rate, years = 1000, 0.05, 30
t = np.arange(years + 1)
simple = principal * (1 + rate * t)
compound = principal * (1 + rate) ** t

plt.plot(t, simple, label='Simple interest')
plt.plot(t, compound, label='Compound interest')
plt.xlabel('Years'); plt.ylabel('Euros'); plt.title('Savings growth'); plt.legend(); plt.show()
print(f'After {years} years: simple = {simple[-1]:.0f}, compound = {compound[-1]:.0f}')


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** Imagine you put €1000 in a bank. With **simple interest** the bank pays you 5% of the *original* €1000 each year (€50, always). With **compound interest** the bank pays 5% of *everything you have so far*, so your interest also earns interest. That "snowball" effect is called **exponential growth**.
#
# **What the code does, step by step**
# 1. Set the starting money (`principal`), the yearly rate (0.05 = 5%) and the number of years.
# 2. `t = np.arange(years + 1)` makes the list 0, 1, 2, … 30 (every year).
# 3. `simple` adds the same €50 each year. `compound` multiplies by 1.05 each year: `(1 + rate) ** t`.
# 4. `plt.plot` draws both lines; the `print` shows the final amounts.
#
# **What to look for:** the two lines start together, but the compound line curves upward and ends much higher.
# **Try this:** change `rate` to 0.08 or `years` to 40. Notice how time matters even more than the rate.
# **New words:** principal (starting money), interest rate, exponential growth.

# %% ------------------------------------------------------------
# ## 2. Loan payments: how a loan is paid off
# **Everyday question:** What is my monthly payment, and how much of it is interest?
# **Math:** geometric series, payment = P·r / (1 − (1+r)^−n)
# %%
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


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** You borrow €10,000 and repay it with the *same payment every month*. But each month the bank charges interest on what you *still owe*, so at the start most of your payment is just interest, and only a little reduces the debt. Later it flips.
#
# **What the code does, step by step**
# 1. Convert the yearly rate to a monthly one (`/ 12`) and count the total months `n`.
# 2. Use a known formula to compute the fixed monthly `payment`.
# 3. The `for` loop goes month by month: interest = balance × monthly rate; the rest of the payment reduces the debt; save the new balance.
# 4. Add up all interest and plot the remaining debt.
#
# **What to look for:** the debt line falls slowly at first and then faster. The total interest is the real "price" of the loan.
# **Try this:** set `years = 10`. The monthly payment gets smaller, but the total interest gets bigger!
# **New words:** balance (what you still owe), amortization (paying off a debt gradually).

# %% ------------------------------------------------------------
# ## 3. A cooling cup of coffee
# **Everyday question:** How long until my coffee is drinkable?
# **Math:** Newton's law of cooling, dT/dt = −k (T − T_room). We solve it numerically (Euler's method) and compare with the exact solution.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** A very hot coffee cools quickly, and a lukewarm coffee cools slowly. The rule is: *the bigger the gap between coffee and room temperature, the faster it cools.* A rule that describes **how something changes** is called a **differential equation**.
#
# **What the code does, step by step**
# 1. Set the coffee temperature (90°C), room temperature (20°C) and how fast it cools (`k`).
# 2. We can't jump to the answer, so we walk forward in tiny steps of half a minute (`dt = 0.5`).
# 3. Each step: new temperature = old temperature + (small change from the rule). This trick is called **Euler's method**.
# 4. We also draw the exact mathematical formula (dashed line) to check our step-by-step answer.
#
# **What to look for:** both lines almost overlap. The coffee drops fast at first, then slowly approaches 20°C. The code prints when it falls under 55°C.
# **Try this:** set `dt = 5`. The steps are bigger, so the simulation becomes less accurate.
# **New words:** differential equation, simulation, step size.

# %% ------------------------------------------------------------
# ## 4. Commute time: Monte Carlo simulation
# **Everyday question:** Will I be late if I leave at 8:00?
# **Math:** random variables; we simulate 10,000 mornings instead of solving by hand.
# %%
n_days = 10000
base = np.random.normal(30, 4, n_days)                 # normal commute, minutes
delay = (np.random.rand(n_days) < 0.10) * np.random.exponential(15, n_days)  # 10% of days: a delay
commute = base + delay

print(f'Average commute: {commute.mean():.1f} min')
print(f'Chance commute > 40 min: {(commute > 40).mean():.1%}')
print(f'95% of days it takes under {np.percentile(commute, 95):.0f} min')
plt.hist(commute, bins=50); plt.xlabel('Minutes'); plt.title('Simulated commute times'); plt.show()


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** Your trip is not *exactly* 30 minutes every day. It varies, and sometimes there is a big delay. Rather than solving a hard formula, we let the computer **pretend to live 10,000 mornings** and then we count how often things happen. This is called a **Monte Carlo simulation**.
#
# **What the code does, step by step**
# 1. `np.random.normal(30, 4, n_days)` gives 10,000 trip times around 30 minutes (a bell curve, typically ±4 minutes).
# 2. `np.random.rand(n_days) < 0.10` is True on about 10% of days. On those days we add a random extra delay (`exponential`: many small delays, a few huge ones).
# 3. Add them together. Then `.mean()` is the average, `(commute > 40).mean()` is the share of days over 40 minutes, and `percentile(…, 95)` is the time you beat on 95% of days.
#
# **What to look for:** a bell shape with a long tail to the right (the bad days).
# **Try this:** change `0.10` to `0.30` (a very unreliable bus) and see how the numbers move.
# **New words:** Monte Carlo, random variable, distribution, percentile.

# %% ------------------------------------------------------------
# ## 5. The birthday paradox
# **Everyday question:** In a class of 23 people, how likely is it that two share a birthday? (Surprisingly high!)
# **Math:** probability and complements.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Surprisingly, in a room of just 23 people there is about a 50% chance that two share a birthday. It feels wrong because we think of *our* birthday, but with 23 people there are 253 *pairs* of people who could match.
#
# **What the code does, step by step**
# 1. `theory(n)`: it's easier to compute the chance that everyone has *different* birthdays (364/365 × 363/365 × …), then do 1 minus that. This trick is called the **complement**.
# 2. `simulate(n)`: give each of n people a random birthday, then check for duplicates. A `set` removes duplicates, so if the set is smaller than the group, someone matched. Repeat 5000 times and count.
# 3. Plot the theory (blue line) and the simulation (red dots).
#
# **What to look for:** the red dots sit on the blue line, and the curve crosses 50% around 23 people.
# **Try this:** increase `trials` to 20000 for dots closer to the line.
# **New words:** probability, complement, theory vs simulation.

# %% ------------------------------------------------------------
# ## 6. A positive medical test: what does it really mean?
# **Everyday question:** A test is 99% accurate and I test positive for a rare disease. Am I probably sick?
# **Math:** Bayes' theorem, P(sick | positive) = P(positive | sick)·P(sick) / P(positive)
# %%
def bayes(prevalence, sensitivity, specificity):
    p_pos = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
    return sensitivity * prevalence / p_pos

print('Disease affects 1 in 1000, test is 99% accurate:')
print(f'P(sick | positive) = {bayes(0.001, 0.99, 0.99):.1%}')

prevalences = np.logspace(-4, -0.5, 100)
plt.semilogx(prevalences, [bayes(p, 0.99, 0.99) for p in prevalences])
plt.xlabel('How common the disease is'); plt.ylabel('P(sick | positive test)'); plt.title('Rare diseases fool accurate tests'); plt.show()


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** Imagine 100,000 people. A rare disease affects 1 in 1000, so 100 are sick. The test catches 99 of them. Among the 99,900 healthy people, a 1% error still gives about 999 false alarms. So of roughly 1,100 positive tests, only 99 are truly sick: **about 9%**, not 99%! Rare events make even accurate tests misleading.
#
# **What the code does, step by step**
# 1. `bayes(...)` takes three numbers: how common the disease is (`prevalence`), how often the test catches sick people (`sensitivity`), and how often it correctly clears healthy people (`specificity`).
# 2. `p_pos` = the total chance of a positive test (true positives + false positives).
# 3. Bayes' theorem divides "positives that are truly sick" by "all positives".
# 4. We then try many prevalences and plot the result.
#
# **What to look for:** the rarer the disease (left side of the graph), the lower the chance a positive test means you're sick.
# **New words:** Bayes' theorem (updating a belief with new evidence), false positive, prevalence.

# %% ------------------------------------------------------------
# ## 7. Predicting house prices
# **Everyday question:** How much should a 80 m² flat cost?
# **Math:** linear regression, least squares: find the line that minimises squared errors.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Bigger flats usually cost more. If we plot size against price, the dots roughly form a line. **Linear regression** finds the straight line that fits the dots best, and then we use it to predict the price of a flat we haven't seen.
#
# **What the code does, step by step**
# 1. We invent 80 flats using a secret rule (€2000 per m² + €30,000) plus random **noise** (real life is messy).
# 2. `np.polyfit(size, price, 1)` finds the best line. "Best" means the one that makes the sum of the squared vertical distances from the dots as small as possible (**least squares**).
# 3. It returns the **slope** (extra euros per extra m²) and the **intercept** (where the line starts).
# 4. We plot the dots and the line, then predict the price for 80 m².
#
# **What to look for:** the learned slope is close to the secret 2000. The computer *discovered* the rule from data.
# **Try this:** raise the noise from `20000` to `60000`. Notice the estimate gets less reliable.
# **New words:** regression, slope, intercept, noise, prediction.

# %% ------------------------------------------------------------
# ## 8. How machines learn: gradient descent
# **Everyday question:** How does a computer "find" the best line?
# **Math:** derivatives. It repeatedly steps downhill on the error surface. This is the engine of almost all AI training.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Imagine standing on a foggy hill and you want to reach the bottom. You feel which way the ground slopes down and take a small step that way, again and again. **Gradient descent** does exactly that, where "height" is the computer's **error**. It is how almost all AI models learn.
#
# **What the code does, step by step**
# 1. Make data that follows y = 3x + 5 plus noise. The computer doesn't know 3 and 5.
# 2. Start with a bad guess: `w = 0`, `b = 0`.
# 3. Repeat 500 times: (a) predict, (b) measure the error, (c) compute the slope of the error with respect to `w` and `b` (a **derivative**), (d) nudge `w` and `b` a little in the downhill direction. The size of the nudge is the **learning rate** `lr`.
# 4. Plot how the error shrinks.
#
# **What to look for:** the error drops fast and then flattens; the final `w` and `b` are close to 3 and 5.
# **Try this:** set `lr = 0.001` (very slow learning) and then `lr = 0.05` (too big a step and it may blow up).
# **New words:** loss/error, parameter, learning rate, derivative, training.

# %% ------------------------------------------------------------
# ## 9. A tiny spam filter
# **Everyday question:** How does my email know what is spam?
# **Math:** conditional probability, Naive Bayes on word counts.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** The filter reads example emails already marked "spam" or "not spam" and learns which words appear more in each type ("free", "win", "cash" scream spam). For a new email it combines the evidence from all its words into a probability. It's called *naive* because it pretends words are independent of each other, which is a simplification that still works well.
#
# **What the code does, step by step**
# 1. We list 9 short example emails and their labels (1 = spam, 0 = not spam).
# 2. `CountVectorizer` turns text into numbers (how many times each word appears), since computers need numbers.
# 3. `MultinomialNB().fit(...)` is the **training**: it learns word frequencies per label.
# 4. `predict_proba` gives the spam probability for three new emails.
#
# **What to look for:** "free cash prize" scores high, "team meeting tomorrow" scores low, and "win a free lunch" is in between.
# **Try this:** add your own sentences to `emails` and re-run.
# **New words:** training data, label, feature, classifier.

# %% ------------------------------------------------------------
# ## 10. Grouping customers without labels
# **Everyday question:** How does a shop discover types of customers on its own?
# **Math:** distances in space; k-means repeats "assign to nearest centre, move centre".
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** A shop has data on customers but nobody told it who is "type A" or "type B". **Clustering** lets the computer discover natural groups by itself. This is called **unsupervised learning** (no answers given).
#
# **What the code does, step by step**
# 1. We invent three kinds of customers: occasional low spenders, frequent low spenders, and big spenders. Each customer is a point (visits, spend).
# 2. `KMeans(n_clusters=3)` repeats: place 3 centres, assign each customer to the nearest centre, move each centre to the average of its customers, until nothing changes.
# 3. We colour each customer by its group and mark the centres with red X.
#
# **What to look for:** three clean colour groups matching the three invented types, found without any labels.
# **Try this:** change `n_clusters` to 2 or 5. How do the groups change?
# **New words:** cluster, centroid (the centre), unsupervised learning.

# %% ------------------------------------------------------------
# ## 11. Should I take an umbrella? A decision tree
# **Everyday question:** Can a computer learn simple rules from past days?
# **Math:** entropy / information gain; the tree asks the most informative question first.
# %%
from sklearn.tree import DecisionTreeClassifier, export_text

humidity = np.random.uniform(20, 100, 300)
clouds = np.random.uniform(0, 100, 300)
rain = ((humidity > 70) & (clouds > 50)) | (np.random.rand(300) < 0.05)

X = np.column_stack([humidity, clouds])
tree = DecisionTreeClassifier(max_depth=2).fit(X, rain)
print(export_text(tree, feature_names=['humidity', 'clouds']))
print('Take umbrella at humidity 85, clouds 80?', bool(tree.predict([[85, 80]])[0]))


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** A decision tree is a game of 20 questions. Example: "Is humidity above 70%? If yes: are clouds above 50%? If yes: take an umbrella." The computer learns the best questions from past days.
#
# **What the code does, step by step**
# 1. We create 300 pretend days. Rain happens when humidity > 70 and clouds > 50 (plus 5% random surprises).
# 2. `DecisionTreeClassifier(max_depth=2)` learns at most two levels of questions, choosing the questions that separate rainy from dry days best.
# 3. `export_text` prints the learned rules in readable form.
# 4. `tree.predict` tests a new day (humidity 85, clouds 80).
#
# **What to look for:** the thresholds in the printed rules are close to 70 and 50, the secret rule the computer rediscovered.
# **Try this:** change `max_depth` to 1 (too simple) or 6 (too complicated, memorising noise).
# **New words:** feature, rule, depth, overfitting (memorising noise instead of learning the pattern).

# %% ------------------------------------------------------------
# ## 12. Will I pass the exam?
# **Everyday question:** How do study hours change my chance of passing?
# **Math:** logistic (sigmoid) function turns any number into a probability between 0 and 1.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** The result is yes/no (pass or fail), so a straight line doesn't work: it could predict "130% chance". Instead, **logistic regression** bends the line into an S-shaped curve that always stays between 0% and 100%.
#
# **What the code does, step by step**
# 1. Make 100 students with hours studied (0 to 10). The chance of passing rises with hours; each student passes or fails randomly according to that chance.
# 2. `LogisticRegression().fit(...)` learns the S curve from the hours and the pass/fail results.
# 3. We plot the dots (0 = fail, 1 = pass) and the red probability curve, then ask for the chance at 2, 5 and 8 hours.
#
# **What to look for:** around 5 hours the chance is about 50%, and it climbs toward 100% as hours increase.
# **Try this:** change the `-5` in `p_true` to `-3` (an easier exam) and see how the curve shifts.
# **New words:** classification, probability, sigmoid (the S-shaped function).

# %% ------------------------------------------------------------
# ## 13. The café queue
# **Everyday question:** Is a second barista worth it?
# **Math:** queueing theory, random arrivals and service times (exponential distributions).
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Customers arrive at random times and each order takes a random time. If baristas are just barely fast enough, waiting times explode. Queueing theory studies this, and a simulation lets us test "what if we add a barista?" without a real café.
#
# **What the code does, step by step**
# 1. `arrivals`: random gaps between customers (on average 1 per minute), added up into arrival times. `services`: random order durations (about 1.8 min).
# 2. `free_at` keeps track of when each barista becomes free. A `heap` is a list that quickly gives the smallest value, i.e. the next free barista.
# 3. For each customer: take the earliest-free barista. If the customer arrived earlier than that, they wait. Record the wait.
# 4. Repeat for 2, 3, 4, 5 baristas and compare the average waits in a bar chart.
#
# **What to look for:** with 2 baristas the wait is long; one extra barista cuts it dramatically, and after that extra staff helps much less. That's the "diminishing returns" pattern.
# **Try this:** make customers arrive faster (`arrival_rate=1.5`).
# **New words:** queue, arrival rate, server, average wait.

# %% ------------------------------------------------------------
# ## 14. Stock prices as random walks
# **Everyday question:** Can I predict tomorrow's price?
# **Math:** geometric random walk, many possible futures, none certain.
# %%
days, paths = 250, 20
daily_mu, daily_sigma = 0.0004, 0.012
returns = np.random.normal(daily_mu, daily_sigma, (days, paths))
prices = 100 * np.exp(np.cumsum(returns, axis=0))

plt.plot(prices, alpha=0.6); plt.xlabel('Trading day'); plt.ylabel('Price'); plt.title('20 possible years'); plt.show()
print(f'Final price range: {prices[-1].min():.0f} to {prices[-1].max():.0f}')


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** Each day the price moves up or down by a small random percentage, with a tiny upward drift on average. From the *same rules* you get many different possible years. This shows why nobody can predict a stock exactly. (This is a toy model, not investment advice.)
#
# **What the code does, step by step**
# 1. Create a table of random daily returns: 250 days × 20 imaginary stocks. `daily_mu` is the average daily move; `daily_sigma` is how wildly it jumps (**volatility**).
# 2. `np.cumsum` adds returns day after day; `np.exp` converts them back into prices. Start value: 100.
# 3. Plot all 20 paths and print the lowest and highest final price.
#
# **What to look for:** same rules, very different outcomes. Some paths end below 100, some above.
# **Try this:** double `daily_sigma` and see the paths spread out.
# **New words:** random walk, return, drift, volatility.

# %% ------------------------------------------------------------
# ## 15. How an epidemic spreads (SIR model)
# **Everyday question:** Why do flu waves rise and fall?
# **Math:** system of differential equations: Susceptible → Infected → Recovered.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Split people into three groups: **S**usceptible (can catch it), **I**nfected, **R**ecovered. Every day some Susceptible people meet Infected people and get sick, and some Infected people recover. The two simple rules make an epidemic wave rise and fall.
#
# **What the code does, step by step**
# 1. `beta` = how easily the disease spreads. `gamma = 0.1` = 10% of infected recover each day (about 10 days of illness). `N` = 1000 people, starting with 1 infected.
# 2. Each day: new infections = `beta × S × I / N` (more meetings when many are both susceptible and infected); new recoveries = `gamma × I`.
# 3. Update S, I, R and record I (infected people) each day.
# 4. Compare two worlds: no measures (β = 0.30) and distancing (β = 0.18).
#
# **What to look for:** with lower β the peak is lower and later, so hospitals face less pressure. This is "flattening the curve".
# **Try this:** try `beta = 0.10` (equal to gamma). Does the epidemic still take off?
# **New words:** model, parameter, SIR.

# %% ------------------------------------------------------------
# ## 16. Population growth with limits
# **Everyday question:** Why don't populations (or social media trends) grow forever?
# **Math:** logistic growth, dP/dt = rP(1 − P/K).
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Without limits, a population (or a viral video's audience) grows by a percentage each period, faster and faster. In reality there is a limit (food, space, number of people): the **carrying capacity** `K`. Growth slows as the population approaches it, producing an S-shaped curve.
#
# **What the code does, step by step**
# 1. `r` = growth rate, `K` = the limit (1000), `dt` = time step. Start both populations at 10.
# 2. Free growth: `P + dt × r × P`.
# 3. Limited growth: the same, but multiplied by `(1 − P/K)`. This factor is almost 1 when P is small (growth is free) and almost 0 when P is near K (growth stops).
# 4. Plot both (the unlimited one is cut off at the top of the graph).
#
# **What to look for:** the limited curve levels off at 1000; the unlimited one explodes.
# **Try this:** change `K` to 500 and watch the new ceiling.
# **New words:** carrying capacity, growth rate, logistic growth.

# %% ------------------------------------------------------------
# ## 17. A movie recommender
# **Everyday question:** How does a streaming service suggest what to watch?
# **Math:** vectors and cosine similarity: people with similar rating vectors have similar taste.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** Each person's taste is a list of numbers (their ratings). Two people with similar lists have similar taste. To recommend movies, find people similar to you, then suggest what they liked that you haven't seen.
#
# **What the code does, step by step**
# 1. A table of ratings from 1 to 5 (0 means "not seen"). "You" only watched and loved *Action A*.
# 2. `cosine(u, v)` measures how similar two lists are: 1 means the same direction (same taste), 0 means unrelated.
# 3. We compute your similarity to each other person. The symbol `@` multiplies two lists element by element and adds the results (a **dot product**).
# 4. For each unseen movie we take a weighted average of others' ratings: more weight for people more similar to you. Then we sort.
#
# **What to look for:** Ana and Ben (action fans) are most similar to you, so action and sci-fi movies rank first and romance last.
# **Try this:** change your ratings to love *Romance A* instead and see the list flip.
# **New words:** vector, similarity, dot product, recommendation system.

# %% ------------------------------------------------------------
# ## 18. Who is the most influential person in a network? (PageRank)
# **Everyday question:** How does Google rank pages, or how do we find the "influencer" in a friend group?
# **Math:** matrices and eigenvectors; repeated multiplication converges to the importance scores.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** A person (or web page) is important if *important* people point to it. PageRank imagines someone randomly clicking links forever; the pages they visit most are the most important. Google started this way.
#
# **What the code does, step by step**
# 1. `links` is a **matrix** (a grid of numbers): a 1 means "row person follows column person".
# 2. We turn each person's follows into probabilities (if Ana follows 2 people, each gets 50%).
# 3. Start with equal scores for all. 100 times, update each score using the scores of the people who follow you. `d = 0.85` means the surfer follows a link 85% of the time and jumps to a random person 15% of the time.
# 4. Print the ranking.
#
# **What to look for:** Chiara comes first, since nearly everyone follows her.
# **Try this:** make Chiara follow nobody-important (change her row) or have Elena follow Ana, and see the ranking move.
# **New words:** matrix, iteration, rank, damping.

# %% ------------------------------------------------------------
# ## 19. Shortest route (Google Maps idea)
# **Everyday question:** What is the fastest way from home to university?
# **Math:** graph theory, Dijkstra's algorithm.
# %%
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
# ### 🧠 Explained for beginners
# **In plain words:** A map is a **graph**: places are **nodes** and the roads between them are **edges**, each with a cost (minutes). **Dijkstra's algorithm** finds the cheapest route by always exploring the cheapest unfinished path first. Navigation apps use ideas like this.
#
# **What the code does, step by step**
# 1. `graph` is a dictionary: for each place, the neighbours and the minutes to get there.
# 2. `queue` always gives us the cheapest path found so far (`heapq` is a list that quickly returns the smallest item).
# 3. Take the cheapest path, and if it reached the goal, we're done. Otherwise, extend it to every neighbour and add the new paths to the queue.
# 4. `seen` remembers places already finished so we don't repeat work.
#
# **What to look for:** the best route is Home → Bus stop → Metro → Bocconi (17 min), faster than going straight to the Metro (20 min).
# **Try this:** change the Home→Bus stop time from 5 to 15. The route changes!
# **New words:** graph, node, edge, weight, algorithm.

# %% ------------------------------------------------------------
# ## 20. A tiny neural network from scratch
# **Everyday question:** How can a computer learn something no straight line can separate?
# **Math:** matrix multiplication, sigmoid, the chain rule (backpropagation). We teach it XOR: "exactly one of two switches is on".
# %%
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


# %% ------------------------------------------------------------
# ### 🧠 Explained for beginners
# **In plain words:** A **neural network** is many tiny calculators (neurons) in layers. Each neuron mixes its inputs with adjustable **weights** and passes the result through a squashing function. Learning means adjusting the weights to reduce error. We teach it XOR: output 1 when exactly one of two switches is on. No single straight line can solve this, so it needs a hidden layer.
#
# **What the code does, step by step**
# 1. `X` = the four switch combinations; `y` = the correct answers.
# 2. The network: 2 inputs → 4 hidden neurons → 1 output. Weights start random.
# 3. **Forward pass:** compute the network's answer. **Backward pass (backpropagation):** use the chain rule from calculus to find how much each weight contributed to the error, then nudge each weight to reduce it.
# 4. Repeat 5000 times (each full pass is an **epoch**).
#
# **What to look for:** the final predictions are close to 0, 1, 1, 0, matching the targets.
# **Try this:** if it doesn't converge (random start), run the cell again. Try 2 hidden neurons instead of 4.
# **New words:** neuron, weights, layer, backpropagation, epoch. This is the building block of modern AI, which you'll study in depth at university.