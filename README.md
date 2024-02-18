# Analysing_Citation_Networks
This involves exploring the High-energy physics citation network. Arxiv HEP-PH (high energy physics phenomenology) citation graph is from the e-print arXiv. If a paper i cites paper j, the graph contains directed edge from i to j. If a paper cites, or is cited by, a paper outside the dataset, the graph does not contain any information about this. 


# References

    FOR PLOTTING:
    http://snap.stanford.edu/data/cit-HepPh.html  (citation network of physicists at hep-ph classification)
    https://networkx.org/documentation/stable/auto_examples/drawing/plot_directed.html 

    FOR ANALYSIS: 
    https://www.cs.rice.edu/~nakhleh/COMP571/Slides-Spring2015/GraphTheoreticProperties.pdf 
    https://www.analyticsvidhya.com/blog/2018/04/introduction-to-graph-theory-network-analysis-python-codes/


# Timeline

    - Tried to use snap library but failed due to some version issues to build the graph.
    - used networkx and it worked
    - but the number of nodes obtained is: 34546 and Edges: 420921; the number of edges are less than that mentioned in the dataset doc since there  each unordered pair of nodes is saved once only. therefore it is accounted once only while making the graph.


## STEPS
        - made the graph network using networkx
        - then tried to draw the nodes with different colors based on their degrees to get the density of the graph at the nodes
        - plotting the graph using matplotlib took a lot of time since the dataset is huge. But for a smaller dataset ot was verified well within a second or two. (smaller dataset, a small subset from the original dataset ,stored in Datasets/cit-HepPh.txt/sample.txt)
        - graph plotted with 5000 points taken from the dataset


## Analysis

### Relation of How connected components change over time 
![Relation](./Outputs/scccomp.png)

### Relation of How clustering coefficients change over time 
![Relation](./Outputs/clusteringcoeff.png)

### Relation of How communities change over time 
![Relation](./Outputs/communities.png)


### Average Degree overtime
![Relation](./Outputs/Figure_1.png)

### Degree Coefficients over the Dataset of 10000 samples
![Relation](./Outputs/degree_Distr.png)

## Interesting Finding 
While all the findings are insightful the 2 which piqued me were how the previous year papers affected the current year's papers in terms of citations and the number of total dependencies 

### How each year papers are dependent on the previous one 
### Number of relations
![Relation](./Outputs/nodes_overtime.png)

### Number of citations over time 
![Relation](./Outputs/edges_over_time.png)

It is clear that the number of citations that is the usage of the previous years papers is growing exponentially as seen here.
This is also exemplified by the bar graph of how connected components evolve over time 