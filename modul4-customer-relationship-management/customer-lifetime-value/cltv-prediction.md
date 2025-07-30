# Customer Lifetime Value Prediction

CLTV : Customer Lifetime Value

```CLTV = Expected Number of Transaction * Expected Average Profit```

```CLTV = BG/NBD Model * Gamma Gamma Submodel```

 -------

## Model 1.  BG/NBD (Beta Geometric/Negative Binomial Distribution) "Buy Till You Die" Model


The BG/NBD model predicts the expected number of transactions for a customer during a given time period. It is based on two key processes:

### 1. Transaction Process (Buy)

- While a customer is "alive," the number of transactions they make in a given time period follows a Poisson distribution with a transaction rate parameter.
- A customer continues to make random purchases around their transaction rate as long as they are alive.
- Transaction rates vary across customers and follow a Gamma distribution with parameters \( r \) and \( a \).

### 2. Dropout Process (Till You Die)

- Each customer has a dropout rate with probability \( p \).
- Dropout rates vary across customers and follow a Beta distribution with parameters \( a \) and \( b \).

### Expected Number of Transactions Formula

The expected number of transactions for a customer during a given time period \( t \), given their past behavior, is calculated as:

$$E[Y(t) | X = x, t_x, T, r, a, a, b] = \frac{\Gamma(r + x) \cdot \Gamma(a + b) \cdot B(a + t, b + T - t)}{\Gamma(r) \cdot \Gamma(a) \cdot \Gamma(b) \cdot B(a, b)}$$


Where:
- \( X \): Number of transactions observed.
- \( t_x \): Time of the last transaction.
- \( T \): Observation period.
- \( r, a, b \): Model parameters.
- \( \Gamma \): Gamma function.
- \( B \): Beta function.


## Model 2. Gamma Gamma Submodel

The Gamma-Gamma Submodel is used to predict the average profit per transaction for a customer.

- The monetary value of a customer's transactions (transaction value) is randomly distributed around their average transaction value.
- The average transaction value may vary across customers over time but remains constant for a single customer.
- The average transaction value follows a Gamma distribution across all customers.

The expected monetary value for a customer, given their past behavior, is calculated as:

$$E[M | p, q, γ, m_x, x] = (q + x) / (p - 1)$$

Where:
- \( M \): Expected monetary value.
- \( p, q, γ \): Model parameters.
- \( m_x \): Average transaction value observed for the customer.
- \( x \): Number of transactions observed for the customer.
