+++
date = "2019-01-02T09:21:26-05:00"
title = "Stop Writing SQL Backwards"
categories = ['Code', 'SQL']
linktitle = ""
description = ""
+++

How many times have you started off building a complicated analytical SQL query like this?

```
SELECT
.
.
.
.
uh???
.
.
SELECT
*
FROM
.
.
.
SELECT
.
.
.
```

And you get stuck trying to figure out exactly what you want to select. You're thinking about averages, group by's, the order of your results or some change you want to see over time and the query editor is just sitting there, taunting you, because in SQL, _you have to know up front_ what you want to select into your final results.

It's paralyzing...but if you keep reading, you're going to know why it's happening and you'll never freeze up at a SELECT statement again.

## You Are Writing Your Queries Backwards

Any time you start with a SELECT statement and you're attempting to summarize complicated data, you're starting off backwards.

SQL is a descriptive language. Every time you write an analytical SQL query, you are attempting to **describe the underlying data** in your tables. If you're coming from a typical programming background, this is really different than how declarative or imperative programming languages work. Yes, there are SQL tools for transforming data that start looking and feeling like other types of programming with loops and control flow and all that, but here I'm just talking about summarizing, analyzing, and transforming data to get insight into the underlying meaning of it.

Every time you reach for your SELECT statement first, you're going to feel shaky because you haven't explored the foundation of the data you're trying to explain. Not only is uncertainty an stumbling block for composing the query, but later on, if you were wrong about any of your initial assumptions, you end up with invalid conclusions in your summary data.

Instead, treat the SELECT statement like a summary of your findings.

Could you summarize a book for someone if you never even opened a page? Or read a chapter? Trying to fill in your SELECT statement first is like writing your book report sentence by sentence, as you finish reading each chapter. I guess you could do that...but you're sure to miss the big picture and probably a lot of interconnected insights if you don't wait until you've read the whole book.

## Build Your Query Chapter by Chapter

Let's work through an example to put this idea into practice. Suppose we have a group of students who take a quiz in class every day. You want to track their progress by seeing how their quiz scores are changing over time and you've decided that looking at the change in their rolling two-week average is the best way to measure that change.

Before you read this post, you might be tempted to sit down and write:

```
SELECT
  student.first_name,
  student.last_name,
  avg(quiz.score),
.
.
.
wait...how do I limit the average for the last two weeks....and get one score per day...
```

And now we're frozen in the SELECT statement again.

No! We said that approach was backwards. So how do we reverse the query-writing process? At first this might feel really basic and slow and painful, but building chapter by chapter is how you read any book, right?

(You can follow along in your own Postgres database using [this seed file to generate the dataset ](https://gist.github.com/postgres/8c196769fa8b11c6c5aa12ae79ff9c60) we'll use throughout the example.)

### An Important Point About Actually Writing SQL

SQL is fragile!

When you crack open a blank editor and start composing a new query, one misplaced function or statement, can make the whole query collapse in on itself. And you might not even realize it until it's too late. You can get three or four steps through tweaking and editing your query and suddenly find out that you've grouped your data wrong or changed the way a subquery does some calculation and all your results are skewed.

If you've just been changing your main query, then it can be really hard to unwind the steps. That's why I recommend a very simple interative approach to building your queries.

1. Start with a simple query
2. Run it against your database
3. Check the results
4. Looking good?
5. Copy the working query and paste it below itself
6. Make one small change to the copy of your working query
7. Repeat steps 2 - 6 until you have the data you want

If you build queries up step-by-step like this, you can easily move forward and back in time, both to check your query logic and sanity check the data. That's what we're about to do to solve this analytics problem.

### Get Oriented

Now back to our students and quizzes example...

Let's start by writing some simple orientation queries so we know more about our data set. There are basically two ways to get oriented: **by schema** and **by the shape of the data**.

Exploring the schema gives you a sense for what tables we will use, what's in each table, and how they are related.

By schema:

```
postgres=# \dt
                List of relations
 Schema |      Name       |   Type   |   Owner    
--------+-----------------+----------+------------
 public | quiz_results    | table    | postgres
 public | quizzes         | table    | postgres
 public | students        | table    | postgres
(3 rows)
```
Students:

```
postgres=# \d students
                           Table "public.students"
   Column   |  Type   |                       Modifiers                       
------------+---------+-------------------------------------------------------
 id         | integer | not null default nextval('students_id_seq'::regclass)
 first_name | text    | 
 last_name  | text    | 
Indexes:
    "students_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "quiz_results" CONSTRAINT "quiz_results_student_id_fkey" FOREIGN KEY (student_id) REFERENCES students(id)
```

Quizzes:

```

postgres=# \d quizzes
                           Table "public.quizzes"
  Column   |  Type   |                      Modifiers                       
-----------+---------+------------------------------------------------------
 id        | integer | not null default nextval('quizzes_id_seq'::regclass)
 quiz_date | date    | 
 topic     | text    | 
Indexes:
    "quizzes_pkey" PRIMARY KEY, btree (id)
```

Quiz Results:

```
postgres=# \d quiz_results 
        Table "public.quiz_results"
   Column   |       Type       | Modifiers 
------------+------------------+-----------
 quiz_id    | integer          | 
 student_id | integer          | 
 score      | double precision | 
Foreign-key constraints:
    "quiz_results_student_id_fkey" FOREIGN KEY (student_id) REFERENCES students(id)
```

If you're ever worked on a large, legacy code base or with a complicated data set, I'm sure you've seen the limits of this type of exploration. Old, unused columns still show up in legacy schemas. Sparsely populated tables show up just as clearly in a schema as the most heavily used tables. It's a bit like looking at a map of a country with just the city and state boundaries (schema view) vs looking at a map that shows population density or traffic patterns at rush hour(data-shape view).

To understand the shape of the data, ask questions like, how many students are there?

```
postgres=# SELECT count(*) FROM students;
 count 
-------
   100
(1 row)

examp
```

How many quizzes are there?

```
postgres=# SELECT count(*) FROM quizzes;
 count 
-------
    91
(1 row)
```

Has every student taken every quiz?

```
postgres=# SELECT count(*) FROM quiz_results;
 count 
-------
  6940
(1 row
```

Hmmm, we would have 9100 quiz results if 100 students had taken each of 91 quizzes. Are we dealing with student absences? Or is there some other pattern in the shape of the data? At this point, missing quiz results won't necessarily impact our ability to answer the question (moving two-week average score per student), but we should understand the shape of the data we're describing.

Sometimes you get lucky and a single GROUP BY will reveal significant results that explain the missing quiz results, but it looks like that's not the case here.

```
postgres=# SELECT student_id, count(1) as count FROM quiz_results GROUP BY student_id ORDER BY count DESC;

 student_id | count 
------------+-------
         24 |    91
          8 |    91
         11 |    91
         16 |    91
         39 |    91
          3 |    91
         47 |    91
         14 |    91
         46 |    91
         48 |    91
         17 |    91
         28 |    91
         36 |    91
         15 |    91
         .
         .
         .
```

If the pattern doesn't reveal itself at the top-level, you can group the counts themselves, to see if there's a pattern to the distribution of quizzes taken per student.

To write the query, we make our "quizzes per student" query a subquery that we can select from and basically repeat the group by and count approach.

That query looks like this:

```
SELECT
  quizzes,
  count(1) as count
FROM (
  SELECT student_id, count(1) as quizzes FROM quiz_results GROUP BY student_id
) r
GROUP BY quizzes
ORDER BY count DESC;
```

And now we get a much more intelligble result:

```
 quizzes | count 
---------+-------
      91 |    49
      61 |    30
      31 |    21
(3 rows)
```

Which tells us that about half the students did take all 91 quizzes, 30 took 61 and the last 21 students only took 31 quizzes. With clean groupings like this, there's probably some kind of cohort-level reason for the number. In other words, if missing quizzes were due to student absences, you'd expect to see a wider range in "number of quizzes per student" because the count of absences per student would likely have more variation.

If you really wanted to keep poking at the data, you'd have one other nice entry point: date.

Here's our distribution of quiz results by date:

```
SELECT
  quiz_date as quiz_date,
  count(1) as results
FROM
  quiz_results qr
JOIN
  quizzes q
ON
  qr.quiz_id = q.id
GROUP BY quiz_date
ORDER BY quiz_date DESC;
```

I'm not going to put all 91 results here, but if you're following along and run the query, you'll see a pattern that explains the "quizzes per student" data, namely, a new group of students joined every month and everyone who was participating at the time took every quiz.

So:

```
quiz_date  | results 
------------+---------
 2018-12-31 |     100
 2018-12-30 |     100
 2018-12-29 |     100
 2018-12-28 |     100
 2018-12-27 |     100
 2018-12-26 |     100
 2018-12-25 |     100
 2018-12-24 |     100
 .
 .
 .
 2018-11-09 |      79
 2018-11-08 |      79
 2018-11-07 |      79
 2018-11-06 |      79
 2018-11-05 |      79
 2018-11-04 |      79
 2018-11-03 |      79
 2018-11-02 |      79
 2018-11-01 |      79
 .
 .
 .
 2018-10-06 |      49
 2018-10-05 |      49
 2018-10-04 |      49
 2018-10-03 |      49
 2018-10-02 |      49
(91 rows)
```

Even building up this example, I played with half a dozen different ways to poke at the data and get a feel for its shape. I hope that's what you take away from this section more than anything else: **simple, exploratory queries help you get the shape of a data set and build your intuition about the correctness of your query results, which really comes in handy when you try to draw complicated conclusions about the data later on.**

### Get Specific

Once you have a feel for the quiz results we're working with, the next thing to do is take a very specific example all the way from start to finish.

We want to build up a specific case where we look at:

- one student's scores
- the average of all those scores
- the average of all those scores for multiple two-week periods

With these specific results, we can check the summary data in the more complicated case of calculating the moving two-week average for all students and be confident that we've done our summary calculation correctly.

First, pick a student:

```
SELECT * FROM quiz_results WHERE student_id = 2
```

Wait, that's not going to give us rich enough data to build intuition about what's happening in the data, is it? Let's spend a little more time joining onto the student and quiz tables to inflate our normalized data:

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
ORDER BY q.quiz_date
```

Which gives us the much more readable:

```
 quiz_date  | first_name | last_name | score 
------------+------------+-----------+-------
 2018-10-02 | Bernadette | Stanton   |    72
 2018-10-03 | Bernadette | Stanton   |  98.2
 2018-10-04 | Bernadette | Stanton   |    93
 2018-10-05 | Bernadette | Stanton   |  82.4
 2018-10-06 | Bernadette | Stanton   |  87.6
 2018-10-07 | Bernadette | Stanton   |  73.4
 2018-10-08 | Bernadette | Stanton   |  81.1
 2018-10-09 | Bernadette | Stanton   |  79.9
 2018-10-10 | Bernadette | Stanton   |  83.9
 2018-10-11 | Bernadette | Stanton   |  76.9
 2018-10-12 | Bernadette | Stanton   |  86.8
 2018-10-13 | Bernadette | Stanton   |  86.5
 2018-10-14 | Bernadette | Stanton   |  73.2
 2018-10-15 | Bernadette | Stanton   |  82.2
```

If we calculate the average across all scores for Bernadette, our data collapses down to a single value:

```
SELECT
  first_name,
  last_name,
  AVG(score) as average
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
GROUP BY first_name, last_name

 first_name | last_name |     average      
------------+-----------+------------------
 Bernadette | Stanton   | 86.6978021978022
(1 row)
```

Maybe that's useful? We could add a two-week date range and find her current two-week average.

First, verify that's we're capturing the correct time range in the WHERE clause:

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
  AND quiz_date <= '2018-12-31'::timestamp
  AND quiz_date > '2018-12-31'::timestamp - '2 weeks'::interval
ORDER BY quiz_date

 quiz_date  | first_name | last_name | score 
------------+------------+-----------+-------
 2018-12-18 | Bernadette | Stanton   |    99
 2018-12-19 | Bernadette | Stanton   |  97.9
 2018-12-20 | Bernadette | Stanton   |  75.2
 2018-12-21 | Bernadette | Stanton   |  97.9
 2018-12-22 | Bernadette | Stanton   |  89.6
 2018-12-23 | Bernadette | Stanton   |  85.4
 2018-12-24 | Bernadette | Stanton   |  80.4
 2018-12-25 | Bernadette | Stanton   |  91.8
 2018-12-26 | Bernadette | Stanton   |  88.2
 2018-12-27 | Bernadette | Stanton   |  97.2
 2018-12-28 | Bernadette | Stanton   |  96.6
 2018-12-29 | Bernadette | Stanton   |  91.4
 2018-12-30 | Bernadette | Stanton   |  81.5
 2018-12-31 | Bernadette | Stanton   |  85.6
(14 rows)
```

And now calculate the average for those 14 quizzes:

```
SELECT
  first_name,
  last_name,
  AVG(score) as average
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
  AND quiz_date <= '2018-12-31'::timestamp
  AND quiz_date > '2018-12-31'::timestamp - '2 weeks'::interval
GROUP BY first_name, last_name

 first_name | last_name |     average      
------------+-----------+------------------
 Bernadette | Stanton   | 89.8357142857143
(1 row)
```

One more for reference:

```
SELECT
  first_name,
  last_name,
  AVG(score) as average
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
  AND quiz_date <= '2018-12-31'::timestamp - '2 weeks'::interval
  AND quiz_date > '2018-12-31'::timestamp - '4 weeks'::interval
GROUP BY first_name, last_name

 first_name | last_name |     average      
------------+-----------+------------------
 Bernadette | Stanton   | 88.5142857142857
(1 row)
```

This next step is going to feel like a little bit of SQL magic, but there is a key concept that lets us combine the last two queries (and more) into a single function call: [window functions](https://www.postgresql.org/docs/9.1/tutorial-window.html). Window functions in SQL allow you to perform an aggregation (e.g. COUNT, SUM, AVG, etc) over a paritcular _window_ of data that is a subset of the total data you are scanning in a single query.

With a window function, instead of one query for each two week period, where the "window" is specified in the where clause, we can calculate all the moving averages in a single query. We can specify the range of time within the magical window function and get a two-week average for each row of data, i.e. each quiz date in our result set.

Here's an example of a window function, ROW_NUMBER, that illustrates the windowing clearly. ROW_NUMBER assigns a row number based on the framing clause in the OVER statment, which here is just `ORDER BY quiz_date`.

So we end up with: 

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score,
  ROW_NUMBER() OVER(ORDER BY quiz_date) as quiz_number
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
ORDER BY q.quiz_date

 quiz_date  | first_name | last_name | score | quiz_number 
------------+------------+-----------+-------+-------------
 2018-10-02 | Bernadette | Stanton   |    72 |           1
 2018-10-03 | Bernadette | Stanton   |  98.2 |           2
 2018-10-04 | Bernadette | Stanton   |    93 |           3
 2018-10-05 | Bernadette | Stanton   |  82.4 |           4
 2018-10-06 | Bernadette | Stanton   |  87.6 |           5
 2018-10-07 | Bernadette | Stanton   |  73.4 |           6
 2018-10-08 | Bernadette | Stanton   |  81.1 |           7
 2018-10-09 | Bernadette | Stanton   |  79.9 |           8
 2018-10-10 | Bernadette | Stanton   |  83.9 |           9
 2018-10-11 | Bernadette | Stanton   |  76.9 |          10
```

All we're doing is giving an incrementing integer to each quiz result, based on the quiz date. You can see that the earlierst quiz gets number 1, then 2,3,4, etc.

It starts to look more magical when we apply the same concept to the average:

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score,
  AVG(score) OVER(ORDER BY quiz_date) as average_score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
ORDER BY q.quiz_date
LIMIT 10

 quiz_date  | first_name | last_name | score |   average_score  
------------+------------+-----------+-------+------------------
 2018-10-02 | Bernadette | Stanton   |    72 |               72
 2018-10-03 | Bernadette | Stanton   |  98.2 |             85.1
 2018-10-04 | Bernadette | Stanton   |    93 | 87.7333333333333
 2018-10-05 | Bernadette | Stanton   |  82.4 |             86.4
 2018-10-06 | Bernadette | Stanton   |  87.6 |            86.64
 2018-10-07 | Bernadette | Stanton   |  73.4 | 84.4333333333333
 2018-10-08 | Bernadette | Stanton   |  81.1 | 83.9571428571429
 2018-10-09 | Bernadette | Stanton   |  79.9 |            83.45
 2018-10-10 | Bernadette | Stanton   |  83.9 |             83.5
 2018-10-11 | Bernadette | Stanton   |  76.9 |            82.84
(10 rows)
```
If you check the first 4 rows, you can see that the averages we're getting back are the cumulative averages of each new quiz and the preceding quizzes:

```
postgres=# select(72 +98.2)/2 as average_score;
     average_score   
---------------------
 85.1000000000000000
(1 row)

postgres=# select (72 + 98.2 + 93) / 3 as average_score;
     average_score   
---------------------
 87.7333333333333333
(1 row)

postgres=# select (72 + 98.2 + 93 + 82.4) / 4 as average_score;
     average_score   
---------------------
 86.4000000000000000
(1 row)
```
There's one more concept we need to add here, which might not be obivous from our last query. We need to define a boundary around which rows get included in the average calculation. Since we're aiming to get to the two-week average, we want to only include the preceding two weeks in the average score each day (or for the first two weeks, as many quizzes are available up to and including the current day).

Window functions do indeed [allow us to specific the range or rows we query over](https://www.postgresql.org/docs/9.1/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS).

Check out this slight tweek, adding `ROWS 2 PRECIDING` to the OVER statement:

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score,
  AVG(score) OVER(ORDER BY quiz_date ROWS 2 PRECEDING) as average_score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
ORDER BY q.quiz_date
LIMIT 10
```

Which returns:

```
 quiz_date  | first_name | last_name | score |  average_score   
------------+------------+-----------+-------+------------------
 2018-10-02 | Bernadette | Stanton   |    72 |               72
 2018-10-03 | Bernadette | Stanton   |  98.2 |             85.1
 2018-10-04 | Bernadette | Stanton   |    93 | 87.7333333333333
 2018-10-05 | Bernadette | Stanton   |  82.4 |             91.2
 2018-10-06 | Bernadette | Stanton   |  87.6 | 87.6666666666667
 2018-10-07 | Bernadette | Stanton   |  73.4 | 81.1333333333333
 2018-10-08 | Bernadette | Stanton   |  81.1 |             80.7
 2018-10-09 | Bernadette | Stanton   |  79.9 | 78.1333333333333
 2018-10-10 | Bernadette | Stanton   |  83.9 | 81.6333333333333
 2018-10-11 | Bernadette | Stanton   |  76.9 | 80.2333333333333
(10 rows)
```

Our results for 2018-10-05 are different now. Last time we got 86.4 and now we have 91.2. If you calculate out the averages, you can see that we are now adding 3 numbers  (current row + 2 preceding) instead of 4 (all preceding), when we didn't specify which rows to use:

```
postgres=# select (82.4 +93 +98.2 + 72) / 4 as average_score;
    average_score    
---------------------
 86.4000000000000000
(1 row)

postgres=# select (82.4 +93 +98.2) / 3 as average_score;
    average_score    
---------------------
 91.2000000000000000
(1 row)
```

**This is a perfect example of a small, easy-to-miss, but important detail. If you just apply the formula to the aggregate results instead of taking the time to look at the expanded row data, you might never see the calculation change.**

Now that we know how to apply the window function correctly, we can build our final query for the specific case.

First, make three small changes:

1. add `ROWS 13 PRECEDING` to get two-week average
2. round the averages for easy of reading
3. change the order of the display results (which is independent of over in the frame clause, so we can calculate and display rows with different sort orders)

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score,
  ROUND(AVG(score) OVER(ORDER BY quiz_date ROWS 13 PRECEDING)::numeric, 2) as average_score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
WHERE
  s.id = 2
ORDER BY q.quiz_date DESC

 quiz_date  | first_name | last_name | score | average_score 
------------+------------+-----------+-------+---------------
 2018-12-31 | Bernadette | Stanton   |  85.6 |         89.84
 2018-12-30 | Bernadette | Stanton   |  81.5 |         90.69
 2018-12-29 | Bernadette | Stanton   |  91.4 |         90.79
 2018-12-28 | Bernadette | Stanton   |  96.6 |         91.10
 2018-12-27 | Bernadette | Stanton   |  97.2 |         89.44
 2018-12-26 | Bernadette | Stanton   |  88.2 |         89.19
 2018-12-25 | Bernadette | Stanton   |  91.8 |         88.55
 2018-12-24 | Bernadette | Stanton   |  80.4 |         88.33
 2018-12-23 | Bernadette | Stanton   |  85.4 |         88.11
 2018-12-22 | Bernadette | Stanton   |  89.6 |         89.00
 2018-12-21 | Bernadette | Stanton   |  97.9 |         88.98
 2018-12-20 | Bernadette | Stanton   |  75.2 |         88.94
 2018-12-19 | Bernadette | Stanton   |  97.9 |         90.69
 2018-12-18 | Bernadette | Stanton   |    99 |         89.71
 2018-12-17 | Bernadette | Stanton   |  97.5 |         88.51
```

Compare the average scores for 2018-12-31 and 2018-12-17 to the ones we calculated manually at the beginning of this section. They match!

### Summarize Your Findings

Now that we are confident about calculating our moving two-week average for one student, we can generalize to all students...probably.

Let's try removing `WHERE s.id = 2`:

```
SELECT
  quiz_date,
  first_name,
  last_name,
  score,
  ROUND(AVG(score) OVER(ORDER BY quiz_date ROWS 13 PRECEDING)::numeric, 2) as average_score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
ORDER BY q.quiz_date DESC

 quiz_date  | first_name |  last_name  | score | average_score 
------------+------------+-------------+-------+---------------
 2018-12-31 | Bernadette | Stanton     |  85.6 |         83.91
 2018-12-31 | Claudie    | Turner      |  89.5 |         85.05
 2018-12-31 | Karson     | Bergstrom   |    85 |         85.52
 2018-12-31 | Libbie     | Farrell     |    83 |         86.35
 2018-12-31 | Eliezer    | Bruen       |  74.9 |         85.95
 2018-12-31 | Constantin | Walker      |  98.2 |         85.92
 2018-12-31 | Luisa      | Altenwerth  |  90.2 |         84.09
 2018-12-31 | Rebeca     | Welch       |  84.3 |         83.26
 2018-12-31 | Deonte     | Leffler     |  91.8 |         83.89
 2018-12-31 | Gilbert    | Wiegand     |  91.2 |         82.74
 2018-12-31 | Kathlyn    | Emmerich    |  81.6 |         82.83
 2018-12-31 | Jimmy      | Kemmer      |  97.4 |         82.88
 2018-12-31 | Rosemarie  | Schmeler    |  73.4 |         81.68
 2018-12-31 | Elissa     | Schroeder   |  77.4 |         82.96
 2018-12-31 | Maribel    | Lakin       |  72.8 |         82.62
 2018-12-31 | Loraine    | Koss        |  96.1 |         83.70
 2018-12-31 | Gladyce    | Rath        |  96.6 |         83.13
 2018-12-31 | Princess   | Bechtelar   |  77.4 |         81.71
 2018-12-31 | Niko       | MacGyver    |  74.5 |         81.57
 2018-12-31 | Buster     | Hagenes     |  72.6 |         83.10
 2018-12-31 | Eunice     | Trantow     |  78.6 |         84.78
```

That looks like kind of a mess! You can see that Bernadette's 2018-12-31 is wrong.

To fix this summary calculation, we need one more key window function concept: PARTITION BY. We can partition the data so that we can do calculations for each student individually, just like we did for Bernadette, but all at once.

```
SELECT
  quiz_date,
  student_id,
  first_name,
  last_name,
  score,
  ROUND(AVG(score) OVER(PARTITION BY student_id ORDER BY quiz_date ROWS 13 PRECEDING)::numeric, 2) as average_score
FROM
  quiz_results r
JOIN
  students s
ON
  r.student_id = s.id
JOIN
  quizzes q
ON
  r.quiz_id = q.id
ORDER BY student_id, quiz_date DESC

 quiz_date  | student_id | first_name |  last_name  | score | average_score 
------------+------------+------------+-------------+-------+---------------
 2018-12-31 |          2 | Bernadette | Stanton     |  85.6 |         89.84
 2018-12-30 |          2 | Bernadette | Stanton     |  81.5 |         90.69
 2018-12-29 |          2 | Bernadette | Stanton     |  91.4 |         90.79
 2018-12-28 |          2 | Bernadette | Stanton     |  96.6 |         91.10
 2018-12-27 |          2 | Bernadette | Stanton     |  97.2 |         89.44
 2018-12-26 |          2 | Bernadette | Stanton     |  88.2 |         89.19
 2018-12-25 |          2 | Bernadette | Stanton     |  91.8 |         88.55
 2018-12-24 |          2 | Bernadette | Stanton     |  80.4 |         88.33
 2018-12-23 |          2 | Bernadette | Stanton     |  85.4 |         88.11
 2018-12-22 |          2 | Bernadette | Stanton     |  89.6 |         89.00
 2018-12-21 |          2 | Bernadette | Stanton     |  97.9 |         88.98
 2018-12-20 |          2 | Bernadette | Stanton     |  75.2 |         88.94
 2018-12-19 |          2 | Bernadette | Stanton     |  97.9 |         90.69
 2018-12-18 |          2 | Bernadette | Stanton     |    99 |         89.71
 2018-12-17 |          2 | Bernadette | Stanton     |  97.5 |         88.51
```

We made three changes to the query:

1. add student_id, which we know is unique, so that we can cleanly group scores by student
2. add `PARTITION BY student_id` in the window function
3. and `ORDER BY student_id` so we can see Bernadette's results (which are now correct again)

For completeness, I would probaby run through specific averages for one more student and then check their results in the final aggregate, but we seem to be heading in the right direction.

## One More Time: Step-by-Step

Thanks for following along through this example!

I know building queries up section-by-section like this probably seems tedious. It can definitely feel that way at times, but this approach has saved me from making small mistakes so many times that I'm convinced it's worth it.

Just to say it again, the step-by-step approach to building complicated analytical SQL queries is:

1. Start with a simple query
2. Run it against your database
3. Check the results
4. Looking good?
5. Copy the working query and paste it below itself
6. Make one small change to the copy of your working query
7. Repeat steps 2 - 6 until you have the data you want

If you follow those steps, you'll have proof that your data adds up and you'll have a much stronger feel for what's inside your tables.

Try it! Let me know how it goes...