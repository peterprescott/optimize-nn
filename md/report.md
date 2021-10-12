---
title: Optimizing Nearest Neighbour Search
author: Peter Prescott
date: 2021
---

# The Problem

Given a set of randomly generated latitude/longitude points on the
surface of the globe, the task was to efficently find, for each point,
the index of the nearest neighbour and the distance (km) between that
neighbour and the point. The relevant `haversine` formula for finding
great-circle distances between points on the surface of the sphere is
provided, as is an inefficient `slow` function which generates the
correct solutions by iterating through each point (`i`), and then again
iterating (`j`) through all the points to find the distance between
point `i` and point `j`, recording the relevant index and value if it is
the nearest neighbour so far. This is memory efficient, but in time it
scales like $\mathcal{O}(n^2)$.

A trivial and slightly `less_slow` improvement would be to only iterate
through those points for which we have already calculated the distance,
thus reducing the time to some multiple of $\frac{n}{2}(n-1)$; but this
is still $\mathcal{O}(n^2)$.

![Time taken by Algorithms for Datasets of Different Sizes](../img/comparison.png){#fig:result_fig}

What is needed is some sort of *spatial index* to make it possible to
efficiently find the nearest neighbour without calculating distances
between points which are obviously far away from each other.

# Constructing a KD-Tree

A quick search on @Wikipedia2021 revealed that the K-D Tree is one such
solution. The basic idea is fairly simple: we create a binary tree by
cycling through the dimensions of our space, and partitioning our points
on the median point as sorted by the points' values in that dimension,
and recursively building branching sub-trees on either side of the
partition node. We can then search for the nearest neighbour by using
the tree to guide us towards the desired point. @MSkrodzki2019 gives the
proof that the expected time taken by a single nearest neighbour search
on a kd-tree is $\mathcal{O}(log(n))$ -- and therefore 
$\mathcal{O}(n log(n))$ for the entire dataset.

There are various implementations freely licensed: I found those by
@JVanderPlasEtAl2012 and @Tsoding2017 particularly helpful.

However, in spite of the availability of code demonstrating the general
concept, implementing a two dimensional kd-tree on the surface of the
globe presents a slightly different challenge. 

Firstly, the curvature of the earth complicates matters. Although we can
treat the dimensions of longitude and latitude as our two dimensions on
which we alternately partition our dataset [@D.W.2015], the shortest distance
between a point and its bounding line of longitude is a more subtle
matter than the trivial question of finding distances between points and
dimensional hyperplanes in Euclidean space. 

Secondly, the wrapping of the earth means that if our point or its
nearest neighbour is close to extreme ranges of longitude or latitude,
our kd-tree will direct us to the wrong solution. The solution I
implemented only returns about 75% of the correct answers. @CScheidegger2013
suggests some possible solutions to this, including a 'multicover' of
extra wrapped duplicate points surrounding the primary dataset.

But before I had managed to implement this, it occurred to me that it
would be conceptually simpler and computationally more efficient to work
in three-dimensional Euclidean space, as the symmetry and gentle
curvature of the sphere means that a point's nearest neighbour on the
surface of the sphere is the same as in 3-D Euclidean space.

When I implemented this, I found that my solution was still only
successful for 90% or so of the points in the dataset. On inspection, it
turned out that my algorithm was not successfully handling the case
where a point reached the branch of which the node was itself. The
examples I had based my code on assumed that the point for which one
was finding a nearest neighbour would not be a node on the tree. This
was not the case in my implementation, and I had thought a simple
solution simply returned the other point as the 'closest' if ever the
point itself was being considered as a candidate for its nearest point.
However, this means that the algorithm 'bounces' off a branch on which
the point itself is node, and fails to find the correct
nearest-neighbour if it is on that branch. At the time of writing I
haven't yet debugged this problem, although I think I have correctly
identified it.

```{.table caption="Time (s) taken by Algorithms on Datasets of Different
Sizes {#tbl:results}"
source="../csv/results.csv"}
```

# Comparison of Times

In spite of the bugs remaining in my attempts to implement a kdtree on
the sphere, and a 3-d tree in Euclidean space, we can still see how long
they take to find solutions. The table of results (@Tbl:results) and
accompanying line-plot (@Fig:result_fig) confirm what we know already,
that the `slow` solutions grow quadratically, while the kd-tree
solutions are much more efficient.

For a dataset of just over 1000 points, the 3-d kd-tree already takes 
less than a tenth of the time taken by the `slow` function. For a 
million points the difference would be even more stark.

All the more reason then to debug this code...

# Conclusion

I enjoyed working on this task, and look forward to discussing it on
Wednesday. My code is openly available at
[github.com/peterprescott/optimize-nn](https://github.com/peterprescott/optimize-nn),
structured as a Python package to be `pip install`ed as desired, with
PyTest tests to help make it maintainable (though unfortunately as
mentioned, the kd-tree algorithms are not yet quite passing their tests). 

# References
