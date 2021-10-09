# Nearest Neighbour Optimization Exercise 

This is a synthetic test using generated data. When given a list of
points on the world how would you quickly and efficiently find out the
distance to the nearest point and the index of that nearest point for
each point. 

You have been given a function called `make_data`
that generates a random set of points and stores them in a Pandas
DataFrame with two extra columns, `distance_km` and `neighbour_index`.
Your task is to fill in these columns as efficiently as possible. 

A working, but deliberately very slow, implementation is provided in two
functions, the first  is called `slow` which calls a function called
`haversine`, both are included. This can be used to check the results of
your work, if your approach does not produce the same results as this
version (or something with 0.1% of these results) then it does not work!

Here are some questions to consider when working on the problem:

- Why is the current method so slow? 
- Where is the best place to focus your time on speeding it up?
- What approach did you try? 
- What is the fastest version you can make without loops, what about the
  fastest with a loop? 
- Did everything you tried work? 
- What didn’t work? 
- In big O notation how fast is the slow method? 
- How fast is your method? 
- If you had to process 1,000 points, would you use the same approach as
  if you had to process 1,000,000 points? 
- How much faster is your version relative to the slow one? 

You will be evaluated on: 
- The clarity and thoughtfulness of your approach 
- The performance of your final solution 
- The clarity of your code and code comments 
- How easy it would be to maintain your code 
- The insightfulness of any graphs or charts (but not how pretty they
  are)

