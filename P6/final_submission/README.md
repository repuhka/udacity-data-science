## Data Visualization: On-time arrival performance for top 5 U.S. Domestic Airlines, 2005-2016


### Summary

This data visualization incorporates different charts for U.S. airlines' on-time performance within the period 2005-2016. The data used is collected from [RITA](http://www.transtats.bts.gov/) website.
 It indicates each airlines' annual average of on-time arrivals. 

 The on-time arrivals were chosen as a metric to be displayed as this is an extremely important passanger experience measure which all airlines need to closely monitor. And from a passangers' point of view it is also an important metric as arriving on time is one of the major factors considered when choosing an airline to fly with. 

 ### Story

 This graph represents one aspect of the evolution of the commercial aviation, in particular on time arrivals for top 5 US airline carriers during the period Jan.2005 - Jan.2016, selected based on their monthly gross number of flights. 

Based the variable evolution during the period, I came up with some conclusions:

- Constant increase of the % of flights on time for 3 out of the top 5 airlines: a probable reason for this would be the technological evolution in the industry providing better information as well as technologically enhanced aircrafts. Airlines compete each other to reach as high number of timely arrived flights as possible. An interesting fact here would be the missing data for American Eaglle Airlines since 2014, it could be easily suggested that the carrier was unable to sustain competition, however upon further research it seems that it was just rebranded to Envoy Airlines in this period. 

- Growing pressure to improve efficiency: Airlines are making large & ongoing improvements to operate more efficiently, visible by the increasing proportion of on-time arrivals. Our exclusion here is SkyWest Airlines, showing a decreasing trend. An explanation to this trend can be found in the several accuisitions and restructures happened in the period 2005 - Nov. 2012. Also we can attribute part of this trend to the constant fleet renewal happened in this company between 2012 - 2015, personnel need time to be trained to operate the new vehicles as well as to get accustomed to them. With a good amount of certainty, we can expect that this trend will be turned in the next 2 - 4 years and start to increase again.  

- Market/economic fragmentation: What happened between 2006 - 2008 and then again between 2013 - 2014? What can explain the sudden drops? 

First drop in the on time performance can be attributed to the global economic crisis started in 2006, all of the top 5 airlines in question suffered financial difficulties, thus we cannot expect that their on time arrival performance doesn't suffer. At the same period 4 out of the 5 top airlines grouneded some of their fleets & reduced capacity in order to free up cash. Which again has direct relationship with the number of on-time arrivals. 

If we turn to the next drop 2013 - 2014, there aren't such major economic events like in the previously examined period. Though, airline ontime operational performance is impacted in the short-term both by individual carrier issues (ex. AMR's bankrupcy & the relaunch of American Airlines) as well as air traffic control decisions, caused by airline accidents (ex. Southwest's flight N753SW). 

### Design

#### Exploratory Data Analysis and Cleaning (R)

The data is downloaded from RITA, selecting a dataset that included flights from all carriers to and from all airports from January 2005 through January 2016. 
Exploratory data analysis was conducted using R, and is detailed in data.Rmd and data.html. 
While studying the data, I hypothesized that there might be trends in individual airline performance (# arrivals delayed / # total arrivals) over the period as well as distinct differences between carriers.

So my natural choice of first visualization was a line chart with multiple series to compare trends between different airlines & highlight deviations. 


![Initial R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph1.jpg)

This is clearly way too busy! There were 27 airlines, and the line chart is ineffective in displaying any distinguishable trends. 

In order to provide the readers with airlines that would be most relevant, I reduced the data set to feature only the 5 most active airlines, i.e. those with the highest gross number of flights on a monthly basis. 

Based on the new data set, 2 plots were created:
-	Re-do of the first line chart
-	Chart showing the total annual flights


![Second R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph2.jpg)
![Third R Plot](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph3.jpg)

My initial evaluation of these charts were that they were satisfactory in visualizing the different trends of these 5 airlines.  It shows how various airlines improved or worsened over time, and which airlines were currently performing the best, as of 2016.  

They also showed the general trends that all 5 airlines experienced: an aggregate dip in performance from 2006 to 2008, individual peaks from 2010 to 2012, and a more recent drop from 2012 to 2014.

Initially I thought these charts were satisfactory in visualizing the different trends of the 5 airlines. It shows how various airlines improved or worsened over time, and which airlines were currently performing the best. It also showed the general trends that all 5 airlines experienced: dip in performance between 2006 - 2008, sharp peak in 2012 (known as the world's highest year of on-time arrivals in the industry), followed by a very distinct drop in 2013 - 2014.

After some thought I decided to use performance trends rather than gross number of flights, as those will assist me in finding the answer to "With which airlines are you more likely to be on time?"


#### Data Visualization (dimple.js)

I decided to enhance my initial data visualization as I implemented it with D3.js & dimple.js in the following areas:

-	Fix the scaling in the '% On Time' axis, particularly setting the maximum at 100% in order to display what the disparity from the maximum.
-	Scatter plot points to emphasize as well on each airline's individual data points.
-	Added transparency, as some areas of the graph (2010-2012) have a considerable overlap.

I re-evaluated the design decisions that I made during the EDA phase, and still considered a line chart as the best alternative to visualize the trends per carrier over time. Coloring each line series was also a good way to visually encode and distinguish airlines. I also moved the legend to the top right, as this provides a closer proximity to the interesting data points. 

I am a little concerned with the 'Lie Factor' and truncating the y-axis minimum at a non-zero value. I chose to truncate it just below the lowest 'valley', as I feared that a 0-100% scale would have obfuscated any trends.

This initial iteration can be viewed at index.html, as well as below:


![First Chart](https://raw.githubusercontent.com/repuhka/udacity-data-science/master/P6/final_submission/charts/graph4.jpg)


Below is the final data visualization created based on the feedback received from the interviews:

![Final Chart](https://github.com/repuhka/udacity-data-science/blob/master/P6/final_submission/charts/graph5.jpg)


### Feedback

I interviewed 3 individuals in person, and asked for their feedback on the data visualization after prompting them with some background information (shown in the summary section) and used the initially provided example questions. 

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

### Post-feedback Changes

Based on the interviews feedback I did a couple of changes:

-	I muted the grid lines.
-	Changed the chart title in order to make it more consistent with the data displayed.
-	I added a mouseover event for the lines, so it would 'pop' it out and emphasize the path. 
-	I polished the tooltip variable names to be more user friendly.

I chose not to include any additional arrival data and raw numbers. In my opinion this would blur the focus of the chart, or have any positive impact on the understanding of airline on-time arrival rates.

### Resources

- [dimple.js Documentation](http://dimplejs.org/)
- [Data Visualization and D3.js (Udacity)](https://www.udacity.com/course/viewer#!/c-ud507-nd)
- [D3 multi-series line chart with tooltips and legend](http://bl.ocks.org/Matthew-Weber/5645518)
- Various [Stack Overflow](http://stackoverflow.com/search?q=dimple.js) posts

### Data

- `data/334221194_112014_3544_airline_delay_causes.csv`: original downloaded dataset
- `data/data.csv`: cleaned and truncated dataset, utilized in final dimple.js implementation