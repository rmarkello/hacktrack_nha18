// REFERENCE: https://anisha.pizza/nhw2017_d3/
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// setup x
var xValue = function(d) { return d.additions;}, // data -> value
    xScale = d3.scaleLinear().range([0, width]), // value -> display
    xMap = function(d) { return xScale(xValue(d));}, // data -> display
    xAxis = d3.axisBottom(xScale).tickSizeOuter(0);

// setup y
var yValue = function(d) { return d.deletions;}, // data -> value
    yScale = d3.scaleLinear().range([height, 0]), // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.axisLeft(yScale).ticks(5).tickSizeOuter(0);

// setup fill color
var cValue = function(d) { return d.author;},
    color = d3.scaleOrdinal(d3.schemeCategory20);

// add the graph canvas to the body of the webpage
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// x-axis
svg
    .append('g')
    .attr('class', 'x axis')
    // take X to bottom of SVG
    .attr('transform', 'translate(0,' + height + ')')
    .call(xAxis)
    .append('text')
    .attr('class', 'label')
    .attr('x', width / 2)
    .attr('y', 25)
    .attr('font-size', '1em')
    .style('text-anchor', 'end')
    .style('fill', 'black')
    .text('Additions');

// y-axis
svg
    .append('g')
    .attr('class', 'y axis')
    .call(yAxis)
    .append('text')
    .attr('class', 'label')
    .attr('transform', 'rotate(-90)')
    .attr('y', -50)
    .attr('x', -height / 2)
    .attr('dy', '.71em')
    .attr('font-size', '1em')
    .style('text-anchor', 'end')
    .style('fill', 'black')
    .text('Deletions');

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

d3.json('/data').then(function(data){
    // don't want dots overlapping axis, so add in buffer to data domain
    xScale.domain([d3.min(d3.values(xValue(data))), d3.max(d3.values(xValue(data)))]);
    yScale.domain([d3.min(d3.values(yValue(data))), d3.max(d3.values(yValue(data)))]);

    // draw dots
    svg.selectAll("dot")
       .data(data)
       .enter()
       .append("circle")
       .attr("class", "dot")
       .attr("r", 3.5)
       .attr("cx", xMap)
       .attr("cy", yMap)
       .style('fill', 'black')

    console.log(data)
       // .style("fill", function(d) { return color(cValue(d));})
       // .on("mouseover", function(d) {
       //   tooltip.transition()
       //        .duration(200)
       //        .style("opacity", .9);
       //   tooltip.html(d.author + "<br/> (" + xValue(d)
       //     + ", " + yValue(d) + ")")
       //        .style("left", (d3.event.pageX + 5) + "px")
       //        .style("top", (d3.event.pageY - 28) + "px");
       // })
       // .on("mouseout", function(d) {
       //   tooltip.transition()
       //        .duration(500)
       //        .style("opacity", 0);
       // });

    // // draw legend
    // var legend = svg.selectAll(".legend")
    //   .data(color.domain())
    // .enter().append("g")
    //   .attr("class", "legend")
    //   .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });
    //
    // // draw legend colored rectangles
    // legend.append("rect")
    //   .attr("x", width - 18)
    //   .attr("width", 18)
    //   .attr("height", 18)
    //   .style("fill", color);
    //
    // // draw legend text
    // legend.append("text")
    //   .attr("x", width - 24)
    //   .attr("y", 9)
    //   .attr("dy", ".35em")
    //   .style("text-anchor", "end")
    //   .text(function(d) { return d;})
});
    //
    // // D3 version
    // var elements = d3.select('#d3chart')
    //                  .selectAll('.bar')
    //                  .data(data);
    // elements
    //   .enter()
    //   .append('div')
    //   .attr('class', 'bar')
    //   .style('width', function(d, i){
    //     return d.y + 'px';
    //   })
    //   .text(function(d, i){
    //       return d.y
    //   })
    //   .on('mouseover', function(d, i){
    //       var msg = 'You\'ve selected bar number ' + (i + 1) + '.';
    //       d3.select(this)
    //         .attr('class', 'bar selectedBar');
    //       d3.select('#selected').text(msg);
    //   })
    //   .on('mouseout', function(d, i){
    //       d3.select(this)
    //         .attr('class', 'bar');
    //       // d3.select('#selected').text('');
    //   })
    //   .on('click', function(d, i){
    //       d.y += 50;
    //       d3.select(this)
    //         .transition()
    //         .duration(1000)
    //         .style('width', d.y + 'px')
    //         .text(d.y);
    //   });
// });
