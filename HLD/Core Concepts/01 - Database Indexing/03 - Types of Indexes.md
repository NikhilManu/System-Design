## Geospatial Indexes

Geospatial indexes are specialized, we use them only when there is location data.

### The Challenge with Location Data

Lets say we query restaurants within 5 miles, we'll get hit with one of two performance problems

1. If we use latitude, we'' find all resturants in the right latitude range, but thats a long strip spanning entire globe. Then for each of restuarant we need to check if it is in the right longitude range.
2. If we try to use index intersection, the database still has to merge two large set of results - all restaurants in right latitude and all restaurants in right longitude range.

### Core Approach

There are three main approaches
- Geohash
- Quadtrees
- R-trees

#### Geohash

The core idea is convert a 2D location into a 1D string in a way that preserves proximity.

Imagine dividing world into four squares and labeling them 0-3. Then divide each of those into four smaller squares and so on. A geohash is same but uses a base32 encoding that creates string "dr5ru" for locations.
* "9q8y" might represent San Fransisco
* "9q8yy" narrows it down further
* "9q8yyk" might pinpoint to specific block

Once the locations data is converted into geohash, we can use a regular B-tree index to handle our spatial queries.

The main limitation is that locations near each other in reality might not share similar prefixes if they happen to fall on different sides of major grid division.


#### Quadtrees

They are less common in production databases today.

Start with one square covering entire area. When square contains more than some threshold of points (4-8), split into four equal quadrants. Continue this recursively.

Key advantage is 
* dense area gets subdivided more finely
* Sparse region maintain larger quadrants.

But quadtree require specialized tree structures. This implementation complexity is the reason most modern databases prefer geohash or R-tree.

#### R-Tree

R-tree have emerged as the default spatial index in modern databases.

R-trees work with flexible, overlapping rectangles. It groups nearby pins into one rectangle and then it groups several of those rectangle into a bigger rectangle.

An advantage is R-trees can efficiently handle both points and larger shapes in the same index structure. A single R-tree can index everything from individual restuarant location to delivery zone polygons and road n/w.

A downside is those rectangles can overlap. So the search may have to follow more than one branch


#### Note:

If asked about geospatial indexing in interview, focus on explaining the problem clearly and contrasting a tree-based approach with a hash-based approach

## Inverted Indexes

B-trees fall short when we need to search through text content. Full pattern matching gets slower as text content grows.

An inverted index solves this by flipping the relationship between documents and their content. Instead of storing document with their words, it stores words with their documents.

```
doc1: "B-Tree are fast and reliable"
doc2: "Hash tables are fast but limited"
doc3: "B-trees handle range queries well"
```

Inverted Index creates a mapping:

```
b-trees     -> [doc1, doc3]
fast        -> [doc1, doc2]
reliable    -> [doc1]
hash        -> [doc2]
range       -> [doc3]
```

While the above shows core concept, production inverted indexes are much more sophisticated. When system like Elasticsearch index text, they first run it through an analysis pipeline that process and enriches the content.

1. Breaking text into tokens (words or subwords)
2. Converting to lowercase
3. Removing common stop words like "the" or "and"
4. Applies stemming (reducing word to root form)

We'll see inverted indexes whenever advanced text search is needed.