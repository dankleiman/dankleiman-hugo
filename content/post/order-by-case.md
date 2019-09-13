+++
date = "2019-08-30T19:40:40-04:00"
title = "SQL Quick Tip: Present Cleaner Results with Custom Ordering"
categories = ['Code', 'SQL', 'Quick Tip']
+++

Usually, when you add an `ORDER BY` clause to your SQL query, you want to sort by your columns' values.

To track the top 10 cryptocurrencies by price over the last 90 days, for example, you would write a query like this:

<!--more-->

```
SELECT
  symbol,
  round(avg(price),2) as avg_price
FROM
  prices
WHERE recorded_at > getdate() - interval '90 days'
GROUP BY symbol
ORDER BY avg_price DESC
LIMIT 10
```

Returning ten averages, ordered by price:

```
 symbol | avg_price 
--------+-----------
 42     |  23417.22
 NANOX  |  22243.17
 MAPR   |  11725.55
 BTCB   |   10774.5
 BTC    |   10260.7
 RBTC   |  10243.69
 WBTC   |  10219.67
 PBT    |   3777.12
 BITBTC |   3747.21
 THR    |   1658.02
(10 rows)
```

Alternatively in this example, you could sort by symbol and get back an arbitrary alphabetic range of assets. It really depends on what kind of question you are asking.

What if, instead, you wanted to track a particular subset of assets?

```
SELECT
  symbol,
  round(avg(price),2) as avg_price
FROM
  prices
WHERE symbol IN ('BTC', 'MKR', 'BCH', 'ETH', 'BSV', 'DASH', 'ZEC', 'XMR', 'LTC','BNB')
AND recorded_at > getdate() - interval '90 days'
GROUP BY symbol
```

Returning averages for your predetermined group of assets:

```
 symbol | avg_price 
--------+-----------
 BCH    |    361.92
 BTC    |  10260.79
 XMR    |     89.12
 BNB    |     30.58
 ZEC    |     78.75
 BSV    |    172.96
 LTC    |     103.4
 MKR    |    617.88
 ETH    |    241.78
 DASH   |    128.97
(10 rows)
```

Great.

Up to now, that's all pretty straightforward, but here's where we can improve things.

If you are going to track the same data over time, having a consistent format is better for two reasons:

- it's easier to compare a series of results when the results look the same each time
- context-switch into the data set goes faster because of the familiar format

Plus, values-ordered data might not make as much sense, depending on the question you are trying to answer. Do you always want to see the top price? Maybe, if you were tracking relative price changes. What about an alphabetical list? It's consistent, but also arbitrary in terms what the underlying assets mean in your specific context.

## Case Statement for Custom Order

In order to create a custom list, you can create a custom `ORDER BY` clause using a `CASE` statement.

Once you decide what a meaningful ordering is for these results, you can ensure that your results will always come back the same way:

```
SELECT
  symbol,
  round(avg(price),2) as price
FROM
  prices
WHERE symbol IN ('BTC', 'MKR', 'BCH', 'ETH', 'BSV', 'DASH', 'ZEC', 'XMR', 'LTC','BNB')
AND recorded_at > getdate() - interval '90 days'
GROUP BY symbol
ORDER BY
CASE 
  WHEN symbol = 'BTC' THEN 1
  WHEN symbol = 'ETH' THEN 2
  WHEN symbol = 'BCH' THEN 3
  WHEN symbol = 'LTC' THEN 4
  WHEN symbol = 'BNB' THEN 5
  WHEN symbol = 'BSV' THEN 6
  WHEN symbol = 'XMR' THEN 7
  WHEN symbol = 'DASH' THEN 8
  WHEN symbol = 'MKR' THEN 9
  WHEN symbol = 'ZEC' THEN 10
END
```

Now every day, when you run this query or compare results over time, you have a consistent view of your data.

Obviously there are any number of tools downstream from your actual query that you can use to manipulate the data, but if you're like me and do quick data checks here and there throughout the day with reusable SQL snippets, every bit of extra consistency like this helps.

**[Check out more of my recent writing on Blockchain Data Engineering here.](https://medium.com/flipside-crypto-engineering-data-science)**