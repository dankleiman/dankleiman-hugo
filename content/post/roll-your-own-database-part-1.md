+++
categories = ['Code', 'SQL']
date = "2019-02-16T11:31:03-05:00"
title = "Roll Your Own Database: Part 1"
+++

**Warning: This post is NSFW. In this series, we are going to build a really, really simple database management system that you should by no means use in a production work environment.**

Here's the experiment:

- Start with a naive implementation of a database -- read and write from a local csv file
- Reach for all the normal features we use every day: basic CRUD, aggregate queries, complex joins 
- Realize that our basic implementation falls short
- Look at how these problems are solved in modern systems

Think of the whole series as one giant experiment in [Cunningham's Law](https://meta.wikimedia.org/wiki/Cunningham%27s_Law): "the best way to get the right answer on the internet is not to ask a question; it's to post the wrong answer."

We're not setting out to be wrong here, but instead, by taking a really basic implementation as our starting point, we want to realize over and over again how the simplistic solution is lacking. Is it inefficient? Difficult to work with? Does it fall down on a basic use case we should support?

We're going to keep a running list of nice-to-have features each time we bump up against something that doesn't work and follow-up with a solution to that problem in a later part of the series. We're aiming for as many "oh, so that's why they do that" moments as possible, where we realize how or why modern database management systems are implemented the way they are.

If that sounds good to you, let's go!

## A Flat File Database

We're going to start with a single CSV file as our data source. Browsing Kaggle for datasets, I picked [one with Olympic atheletes and their events over time](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results/version/2). You can visit the site and download the file if you want to follow along.

The data in the file looks like this:

```
"ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"
"1","A Dijiang","M",24,180,80,"China","CHN","1992 Summer",1992,"Summer","Barcelona","Basketball","Basketball Men's Basketball",NA
"2","A Lamusi","M",23,170,60,"China","CHN","2012 Summer",2012,"Summer","London","Judo","Judo Men's Extra-Lightweight",NA
"3","Gunnar Nielsen Aaby","M",24,NA,NA,"Denmark","DEN","1920 Summer",1920,"Summer","Antwerpen","Football","Football Men's Football",NA
"4","Edgar Lindenau Aabye","M",34,NA,NA,"Denmark/Sweden","DEN","1900 Summer",1900,"Summer","Paris","Tug-Of-War","Tug-Of-War Men's Tug-Of-War","Gold"
"5","Christine Jacoba Aaftink","F",21,185,82,"Netherlands","NED","1988 Winter",1988,"Winter","Calgary","Speed Skating","Speed Skating Women's 500 metres",NA
"5","Christine Jacoba Aaftink","F",21,185,82,"Netherlands","NED","1988 Winter",1988,"Winter","Calgary","Speed Skating","Speed Skating Women's 1,000 metres",NA
"5","Christine Jacoba Aaftink","F",25,185,82,"Netherlands","NED","1992 Winter",1992,"Winter","Albertville","Speed Skating","Speed Skating Women's 500 metres",NA
"5","Christine Jacoba Aaftink","F",25,185,82,"Netherlands","NED","1992 Winter",1992,"Winter","Albertville","Speed Skating","Speed Skating Women's 1,000 metres",NA
"5","Christine Jacoba Aaftink","F",27,185,82,"Netherlands","NED","1994 Winter",1994,"Winter","Lillehammer","Speed Skating","Speed Skating Women's 500 metres",NA
```

From these columns, we can ask questions like "who was on the Men's Basketball Team for China in the 1992 Summer Olympics?" or "what city was that in?" or "who has the most Speed Skating medals of all time?".

## Asking Questions of the Database

If you want to ask these questions, what do you have to do? You need to be able to read the data in the file, the filter it, sort it, group it and display it.

First, let's build a simple ruby wrapper for our file system commands to read data, where our new `FlatDB` class is initialized with a file path to the csv file. When we read the data, we get an array of `CSV::Row` objects back:

```
require 'csv'


class FlatDB
  attr_accessor :path, :columns

  def initialize(path)
    self.path = path
  end

  def read()
    rows = []
    CSV.parse(File.read(self.path), headers: true).each do |row|
        rows << row
    end
    rows
  end
end
```

See? We're already making assumptions about how we want to handle data once we pull it out of the database. We're jumping right over reading lines of text to starting to structure our data in a way that will probably be more useful for the things we want to do later. For example, a `CSV::Row` gives us access to `headers`, which look a lot like our future column names. The `fields` could become our row values.

You can probably also see our first limitation when it comes to asking the database for data, right? **With this implementation you're going to get back all the data every time!**

And if your inclination is then to say, "we should be able to ask for a filtered subset of the data", you've opened up the question of whose job it is to make those decisions and do that subsetting work. What are the trade-offs of an implementation where we get back all the data and our "application" does the filtering work versus one where our database exposes a query language that allows the application to ask for more specific subsets of data?

In later parts of this series we're going to develop a query language, but for now, let's throw some basic filters on and see where that gets us:

```
require 'csv'


class FlatDB
  attr_accessor :path, :columns

  def initialize(path)
    self.path = path
    self.columns = data.headers()
  end

  def data
    CSV.parse(File.read(self.path), headers: true)
  end

  def read(filters={})
    rows = []
    data.each do |row|
      if filters.empty? || filters.all? { |col, value| row[col.to_s] == value }
        rows << row
      end
    end
    rows
  end
end
```

Now we've moved a couple of things around in order to expose a `filters` argument to our `read` method. We have to give our `FlatDB` instance the ability to tell whoever is using it (let's just refer to this as our "application" vs our "database" going forward) what they can filter on. So now the instance has a `columns` attribute that reads the headers out of the data when we initialize the `FlatDB` instance.

```
irb(main):002:0> f = FlatDB.new('data/athlete_events.csv')
=> #<FlatDB:0x007f867b9eb570 @path="data/athlete_events.csv", @columns=["ID", "Name", "Sex", "Age", "Height", "Weight", "Team", "NOC", "Games", "Year", "Season", "City", "Sport", "Event", "Medal"]>
irb(main):003:0> f.columns
=> ["ID", "Name", "Sex", "Age", "Height", "Weight", "Team", "NOC", "Games", "Year", "Season", "City", "Sport", "Event", "Medal"]
```

Exposing the columns helps you construct a filter for a more specific read query.

So who was on the Chinese Men's Basketball Team in Barcelona? Now we can get closer to that answer:

```
irb(main):040:0> f = FlatDB.new('data/athlete_events.csv')
irb(main):041:0> filters = {:Team=>"China", :Year=>"1992", :City=>"Barcelona", :Event=>"Basketball Men's Basketball"}
=> {:Year=>1992, :City=>"Barcelona", :NOC=>"CHN", :Sport=>"Basketball Men's Basketball"}
irb(main):042:0> rows = f.read(filters)
irb(main):043:0> rows.each { |row| puts row["Name"] }
A Dijiang
Gong Xiaobin
Hu Weidong
Li Chunjiang
Ma Jian
Shan Tao
Song Ligang
Sun Fengwu
Sun Jun
Wang Zhidan
Wu Qinglong
Zhang Yongjun
```

Great! Because we knew exactly what we wanted to ask for, we can write a filter that finds exactly what we want and we can pull out any attribute we want, e.g. `Name`, after we get the results back from the database.

## What If You Don't Know

If you don't know what you want ask or are just trying to explore the data, this method is going to be pretty painful and slow. Every time you try to refine your filters, you're rescanning the data, i.e. re-reading the file.

Would it be faster to read everything into memory when you initialize the database? Maybe...it depends on the data and how much you need to read and re-read, right?

If you wanted to load all your file data into memory at once, you could do something like this:

```
require 'csv'


class FlatDB
  attr_accessor :path, :columns, :data

  def initialize(path)
    self.path = path
    self.columns = data.headers()
    self.data = data
    
    self.columns.each do |colname|
      self.class.send(:define_method, colname.downcase.to_sym) { self.data.by_col()[colname]}
    end
  end

  def data
    CSV.parse(File.read(self.path), headers: true)
  end

  def read(filters={})
    rows = []
    self.data.each do |row|
      if filters.empty? || filters.all? { |col, value| row[col.to_s] == value }
        rows << row
      end
    end
    rows
  end
end
```

Notice, we also did something dangerous in the name of more convenient exploration by dynamically generating reader methods for each column in our database.

```
self.columns.each do |colname|
  self.class.send(:define_method, colname.downcase.to_sym) { self.data.by_col()[colname]}
end
```

With no idea what the column names are and no way to sanitize allowed values, this is a bad idea. It's ok, though, we already said this whole thing was NSFW.

Ruby's `CSV::Table` has a `by_col` mode that allows us to pull a whole column, which is what this means: `self.data.by_col()[colname]`. It's easier to understand this data with dynamic methods that pull slices of that data for us.

So we can look at all the `Name` values in the database to get a feel for what we want to find.

```
irb(main):037:0> f.name
=> ["A Dijiang", "A Lamusi", "Gunnar Nielsen Aaby", "Edgar Lindenau Aabye", "Christine Jacoba Aaftink", "Christine Jacoba Aaftink", "Christine Jacoba Aaftink", "Christine Jacoba Aaftink", "Christine Jacoba Aaftink", "Christine Jacoba Aaftink", "Per Knut Aaland", "Per Knut Aaland", "Per Knut Aaland", "Per Knut Aaland", "Per Knut Aaland", "Per Knut Aaland....]
```

Even so, with these two changes we've made in the name of convenient data access, we see just how much we're fighting with our data storage choice (the csv file) in our application logic and how limited we are when it comes to exploring the data. For every new access pattern, we need to write new and more convenient access methods, all due to the inflexibility of our query language.

Now I am feeling highly motivated to get something SQL-like in place to make querying more flexible. That's coming up later in the series, though!

## The Rest of the CRUD

For completeness, we can add "create", "update", and "delete" functions as well, but I bet you can guess how we will still be constrained by our expensive and slow file reading design:

```
require 'csv'
require 'fileutils'

class FlatDB
  attr_accessor :path, :columns
  TEMP_PATH = 'tmp/data.csv'

  def initialize(path)
    self.path = path
    self.columns = data.headers()
  end

  def data
    CSV.parse(File.read(self.path), headers: true)
  end

  def create(data_to_insert={})
    fields = []
    self.columns.each do |column_key|
      fields << data_to_insert[column_key.to_sym]
    end
    CSV.open(self.path, 'a') do |csv|
      csv << CSV::Row.new(self.columns, fields)
    end
  end

  def read(filters={})
    rows = []
    data.each do |row|
      if filters.empty? || filters.all? { |col, value| row[col.to_s] == value }
        rows << row
      end
    end
    rows
  end

  def update(old_fields, new_fields)
    CSV.open(TEMP_PATH, 'w') do |csv|
      csv << self.columns
      data.each do |row|
        if row.fields == old_fields
          csv << new_fields
        else
          csv << row.fields
        end
      end
    end
    
    FileUtils.mv(TEMP_PATH, self.path)
  end

  def delete(target_row)
    CSV.open(TEMP_PATH, 'w') do |csv|
      csv << self.columns
      data.each do |row|
        unless row.fields == target_row
          csv << row.fields
        end
      end
    end
    
    FileUtils.mv(TEMP_PATH, self.path)
  end
end
```

While "creating" new data is just appending to our data file, when we want to update something, we have to find it -> update the row -> re-write the whole file -> replace the old file with the new file.

If only we could update a row directly! (Coming soon...)

## Our Feature List

By working through our initial implementation in part one, we've uncovered some pain. Going forward, it would be nice to have:

- a lighter way to load data
- a more flexible query language
- a more efficient update/delete approach

Stay tuned for the rest of this series where we'll either figure out how to do the things on our list or add to it because we realize there's more we don't know about implementing a database management system.

