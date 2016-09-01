## Data Analyst Dry Run Interview questions


### Question 1 - Describe a data project you worked on recently.

The most recent project I worked on was a data visualization, I had to select a dataset and create a graphic based on it. I chose to work with the flights data provided by the RITA agency. I chose to plot the on-time flight performance for the top 5 domestic airlines based on their gross number of monthly flights. First of all I found out that their performance was quite similar and was significantly impaceted by the economic situation. 

In order to create that visualization I used the dimple javascript library but it ended up as not being sufficient to cover my needes so I supplemented with another library called d3. 

For my visualization I used a simple line chart as I felt it best represented the development of on-time performance as a KPI over time. In order to be visualy distinguisheable I chose separate colors for each carrier. 

It was a very interesting project for me as the data was related to something people really cared about - whether or not they are likely to arrive on time.  


### Question 2 - You are given a ten piece box of chocolate truffles.

At the beginning there would be 6 orange filling truffles left, opposed to 4 coconut. So the probability to get piece out as orange would be 6/10 = 0.6, which would remain 5 oranges & 4 coconuts. Then if we try to get a second orange, we'll end up with the probability of 5/9 = 0.56 and 4 pieces of each kind. At this point we're left with 8 truffles - 4 of a flavour. So the probability of pulling out a coconut one would be 4/8 = 1/2 = 0.5 and we'll end up with 7 pieces. The probability of pulling out a cocnut one as the last one would be 3/7 = 0.43. 

So the total probability to end up to:

0.6 * 0.56 * 0.5 * 0.43 = 0.07


### Follow up question:

If you were given an identical box of chocolates and again eat four 
pieces in a row, what is the probability that exactly two contain 
coconut filling?

In this case we have exactly 6 combos ending up with 2 truffels with coconut. 

C C O O
O C C O
O O C C
C O O C
C O C O
O C O C

In this case we can calculate the probability of all of them and add up. 


```python
import operator

def take_one(box, trffl):
	total_trffl = sum(box.values())
	prob = (0. + box[trffl])/total_trffl
	if box[trffl]:
		box[trffl] -=1
	return prob, box

def take_sq(box, sq):
	probs = []
	for trffl in sq:
		p, box = take_one(box, trffl)
		probs.append(p)
	return reduce(operator.mul, probs, 1)

if __name__ == '__main__':
	total_prb = 0
	for seq in ['CCOO', 'OCCO', 'OOCC', 'COOC', 'COCO', 'OCOC']:
		box = {'O':6, 'C':4}
		ps = take_sq(box, sq)
		print '- {}: {}'.format(sq, ps)
		total_prb += ps
	print 'Ends up with', total_prb
```

### Question 3 - Given the table users:

        Table "users"        
| Column      | Type      |
|-------------|-----------|
| id          | integer   |
| username    | character |
| email       | character |
| city        | character |
| state       | character |
| zip         | integer   |
| active      | boolean   |

construct a query to find the top 5 states with the highest number of 
active users. Include the number for each state in the query result.
Example result:

| state      | num_active_users |
|------------|------------------|
| New Mexico | 502              |
| Alabama    | 495              |
| California | 300              |
| Maine      | 201              |
| Texas      | 189              |



```sql
select state, count(id) as num_active_users
from users
where active = 1
group by state
order by num_active_users desc
limit 5;
```


### Question 4 - Define a function first_unique

that takes a string as input and returns the first non-repeated (unique)
character in the input string. If there are no unique characters return
None. Note: Your code should be in Python.

```python
def first_unique(string):
	seen = set([])
	for i in range(len(string)):
		letter = string[i]
		if letter not in seen and letter not in string[i+1:]:
			return letter
		seen.add(letter)
    return None
```

> first_unique('aabbcdd123')
> c

> first_unique('a')
> a

> first_unique('112233')
> None

This solution is quite easy to understand, however the complexity is high - O(N^2). This can be explained by the fact that we're doing the look-ahead through the string for
every letter, slightly mitigating by the seen check. 

### Question 5 - What are underfitting and overfitting in the context of Machine Learning? How might you balance them?

Underfitting = model is not capturing trends well even on the training set --> performance is not good. 
Overfitting = good results on the training set & very poor results on the new data. Validation & cross-validation are the usual paths towards fix.

Probable causes for underfitting:
1) too simple model
2) features are not enough
3) poor choise of parameters

Causes that might lead to overfitting:
1) too many features
2) noise in data
3) too few data points

### Question 6 - If you were to start your data analyst position today, what would be your goals a year from now?

http://decisionsource.com/job-listings.html?t=5&i1=PUBLIC&i2=143826639040871&i3=DETAIL&i4=143826639040871&i8=7%2f3%2f2016%2011:58:01%20PM&hash=1758073145&i10=&pcr-id=bVrVvgJeZjNgzEXJRHDQ%2fG%2fxnVmsD1hscMkizX9cdJULioEmqx7Chlj9dFeueFE4L1IHkHGBtu%2fJ510eOb4ungJvHocxr%2bV2IbZYK5XdMgqYdbZF&referrer=http%3A%2F%2Fwww.indeed.com%2Fq-Data-Analyst-Tableau-jobs.html


A year from now I'd like to be able to effectively work with Tableau software.
I am aiming to achieve this through learning mainly from the existing code (found in dedicated software forums) as well as the technical documentation. This is a new system in our coporate environment & we're struggling with it on daily basis. We're spending huge amount of time on fixing customer issues that most probably could be prevented by increasing the stability & reliability of our internal systems using Tableau. I would most definitely call it a win if we manage to have a "bug day" in our visualizations once every two weeks or rarely. 
