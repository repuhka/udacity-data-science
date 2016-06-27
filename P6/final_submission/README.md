## Data Visualization: U.S. Domestic Airline Performance, 2005-2016


### Summary

This data visualization incorporates different charts for U.S. airlines' performance within the period 2005-2015. The data used is collected from [RITA](http://www.transtats.bts.gov/) website.
 It indicates each airlines' annual average of on-time arrivals.

### Design

#### Exploratory Data Analysis and Cleaning (R)

The data is downloaded from RITA, selecting a dataset that included flights from all carriers to and from airports from January 2005 through January 2016. 
Exploratory data analysis was conducted using R, and is detailed in EDA/data.Rmd and EDA/data.html. 
While studying the data, I hypothesized that there might be trends in individual airline performance (# arrivals delayed / # total arrivals) over the period. 
So my natural choice of first visualization was a line chart with multiple series to compare trends between different airlines & highlight deviations. 


![Initial R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph1.jpg)

This is clearly too busy! There were 27 airlines, and the line chart is ineffective in displaying any distinguishable trends. 
In order to provide the readers with airlines that would be most relevant, I reduced the data set to feature only the 5 most active airlines, i.e. the 5 airlines with the highest gross number of flights on a monthly basis. Based on the new data set, 2 plots were created
-	Re-do of the first line chart
-	Chart showing the total annual flights


![Second R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph2.jpg)
![Third R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph3.jpg)

My initial evaluation of these charts were that they were satisfactory in visualizing the different trends of these 5 airlines.  It shows how various airlines improved or worsened over time, and which airlines were currently performing the best, as of 2014.  It also showed the general trends that all 5 airlines experienced: an aggregate dip in performance from 2006 to 2008, individual peaks from 2010 to 2012, and a more recent drop from 2012 to 2014.

Initially I thought these charts were satisfactory in visualizing the different trends of the 5 airlines. It shows how various airlines improved or worsened over time, and which airlines were currently performing the best. It also showed the general trends that all 5 airlines experienced: dip in performance between 2006 - 2008, sharp peak in 2012, followed by a very distinct drop in 2014.

After some thought I decided to use performance trends rather than gross number of flights, as those will assist me in finding the answer to "Which airlines are you more likely to be on time with?"


#### Data Visualization (dimple.js)

I decided to enhance my initial data visualization as I implemented it with D3.js & dimple.js in the following areas:

-	Fix the scaling in the 'On Time Percentage' axis, particularly setting the maximum at 100% in order to display what the disparity from the maximum.
-	Scatter plot points to emphasize on each airline's individual data points per each year.
-	Added transparency, as some areas of the graph (2010-2012) have a considerable overlap.

I re-evaluated the design decisions that I made during the EDA phase, and still considered a line chart as the best alternative to visualize the trends per airline over time. Coloring each line series was also a good way to visually encode and distinguish airlines. I also moved the legend to the top right, as this provides a closer proximity to the interesting data points. 

I am a little concerned with the 'Lie Factor' and truncating the y-axis minimum at a non-zero value. I chose to truncate it just below the lowest 'valley', as I feared that a 0-100% scale would have obfuscated any trends.

This initial iteration can be viewed at index.html, as well as below:


![First Chart](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph4.jpg)

### Feedback

I interviewed 3 individuals in person, and asked for their feedback on the data visualization after prompting them with some background information and used the initially provided example questions. 

#### Interview #1

> I immediately noticed the large dip in in 2007 that 3 of the showcased airlines experienced in performance. Also it would be interesting, what caused the significant drop of on-time flights during 2012-2014? On second glance, I saw that the percentage ranged from 65% to 100%. Would it be more user friendly by showing the full scale?
> 
> It's strange that in the period 2009-2011 all companies have roughly the same percentage of flights on time - something changed in their service or it's a data bug?
> 
> I think the main takeaway is that the competition is still "fair", in the sense that achieving the best performance is still a close match.

#### Interview #2

> Hovering over the points was interesting, but I kind of wanted to see some of the additional data, like how many flights each airline had.
> 
> I liked that there were lines.  It made it easier to follow each "path" of points.  I could see how this would have been a lot more confusing if it were just the circles.
> 
> Honestly, after I got a grasp of what the chart was, I looked all the way to the right, because I wanted to see how these airlines were performing today.

#### Interview #3

> Even though the lines and points are colored differently, I think it would be really nice to highlight or emphasize individual airlines when you select them.  It's a bit hard to follow a specific trend line.
> 
> I really liked the graph, the design is simple, emphasizing on the data. It made it easier to follow each "path" of points.
>
> What I am missing here are any of the factors that cause the change in the percentage of on-time arrival flights are not clear from this graph. 

### Post-feedback Design

Based on the feedback I did a couple of changes:

-	I muted the grid lines.
-	Changed the chart title in order to make it more consistent with the data displayed.
-	I added a mouseover event for the lines, so it would 'pop' it out and emphasize the path. 
-	I polished the tooltip variable names to be more user friendly.

I chose not to include any additional arrival data and raw numbers. In my opinion this would blur the focus of the chart, or have any positive impact on the understanding of airline on-time arrival rates.

Below is the final data visualization:


![Final Chart](https://github.com/repuhka/udacity-data-science/blob/master/P6/final_submission/charts/graph5.jpg)

### Resources

- [dimple.js Documentation](http://dimplejs.org/)
- [Data Visualization and D3.js (Udacity)](https://www.udacity.com/course/viewer#!/c-ud507-nd)
- [D3 multi-series line chart with tooltips and legend](http://bl.ocks.org/Matthew-Weber/5645518)
- Various [Stack Overflow](http://stackoverflow.com/search?q=dimple.js) posts

### Data

- `data/334221194_112014_3544_airline_delay_causes.csv`: original downloaded dataset
- `data/data.csv`: cleaned and truncated dataset, utilized in final dimple.js implementation