## Santa's Sleigh Competition

We need to serve 100,000 locations across the world.

In order to do that we are looking to minimize:

`Weighted Reindeer Weariness = (distance traveled) * (weights carried for that segment)`

From my understanding, this is a twist on the Vehicle Routing Problem.


### First Approach
- Cluster into neighborhoods
- Solve using greedy nearest-neighbor approach

**Results**: Took far too long and still didn't get a good result. The idea behind clustering the world locations on longitude and latitude was to break this down into subproblems that I would try to solve in parallel. Still, the greedy algorithm didn't perform very well.

### Second Approach (Submission)
- Cluster into neighborhoods
- Assign weighted distances and then solve using greedy nearest-neighbor approach
- These weights weren't necessarily distance * gift weight because we needed some sort of inverse estimate here. This is because we were looking to serve the "nearest" location.
- For example: if we were at location (0,0) and had to choose between serving 3 locations (x,y,W): A: (-2,3,3), B: (0,5,5), and C: (7,8,10).
Determining which is the closest by weighted value could be several things:

- A has a distance of ~3.6 and a weight of only 3.
- B has a distance of 5 and a weight of only 5.
- C is far, with a distance of ~10.6 but a heavy weight of 10.

Under the first approach we would first visit A (since it is nearest). The issue is that, we would be carrying around a weight of 10 the whole time (accumulating weariness in the process).
Alternatively we could use some sort of inverse weighting such as:
- `c*(distance/weight)`
where c is a constant that will give importance to either weight or distance.

By doing this we could create "shorter"/"longer" distances between nodes.

**Results**: Slightly better than the first step. Still, no formal optimization method was used so clearly we wouldn't achieve great results. Also, took far too long to complete (almost overnight). This might be resolved by better implementing pandas.

### Third Approach
We will use a heuristic that optimizes neighborhoods.
Since the previous approach was entirely a custom implementation, I will now look to use an existing OR library that can handle the optimization portion.
