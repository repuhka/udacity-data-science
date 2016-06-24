d3.csv("data/data.csv", function(d) {
	var format = d3.time.format("%Y");
	return {
		'Year': format.parse(d.year),
		'Carrier Name': d.carrier_name,
		'On time': +d.ontime,
		'Arrivals': +d.arrivals

	};
}, function(data) {
	'use strict';

	//append title
	d3.select('#content')
	.append('h2')
	.attr('id', 'title')
	.text('On time arrival rates for top US Airlines, 2005 - 2015');

	//set svg
	var width = 950,
		height = 650;
	var svg = dimple.newSVG('#content', width, height);
	var myChart = new dimple.chart(svg, data);

	//x axis set up

	var x = myChart.addTimeAxis('x', 'Year');
	x.tickFormat = '%Y';
	x.title = 'Year';

	//y axis
	var minY = 0.5,
		maxY = 1;
	var y = myChart.addMeasureAxis('y', 'On Time');
	y.tickFormat = '%';
	y.overrideMin = minY;
	y.overrideMax = maxY;
	y.title = '% of timely arrivals (15 min tollerance)';

	//series and legend
	var s = myChart.addSeries('Carrier', dimple.plot.scatter);
	var p = myChart.addSeries('Carrier', dimple.plot.line);
	var legend = myChart.addLegend(width*0.6,60,width*0.3,60,'center');

	//draw it!
	myChart.draw();

	//mouse events on grid lines

	y.gridlineShapes.selectAll('line').style('opacity', 0.2)
	.on('mouseover', function(e) {
		d3.select(this)
		  .style('opacity', 1);
	}).on('mouseleave', function(e){
		d3.select(this)
		  .style('opacity',0.2);
	});

	//mouse events on path
	d3.selectAll('path')
	  .style('opacity', 0.2)
	  .on('mouseover', function(e) {
	  	d3.select(this)
	  	  .style('opacity', 1);
	  }).on('mouseleave', function(e){
	  	d3.select(this)
	  	  .style('opacity',0.2)
	  	  .style('stroke-width', '3px')
	  	  .attr('z-index', '0');
	  });
});

<style type="text/css">
	h2 {
  		color: black;
  		text-align: center;
  	}
  </style>