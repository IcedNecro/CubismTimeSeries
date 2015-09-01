var STEP = 4e3;
var NUM_OF_STEPS = (8*60*60*1000)/STEP;
var context = cubism.context()

var Chart = function(step, num_of_steps) {

    var width = parseInt($('#graph-1').css('width'))
    context = cubism.context()
        .step(STEP)
        .size(width);
    this.context = context;
    this.data = [];
    this.dataMap = {};
}

Chart.prototype.bigquery_metric= function(inter, uid, limit) {
    var value = 0,
          values = [],
          i = 0,
          last,
          self = this;


    return context.metric(function(start, stop, step, callback) {
        var values = [];
        stop = +stop;
        start = +start

        var limit = (stop - start)/STEP;
        d3.xhr('/bigquery/freq/?interconnection='+inter+'&unit_id='+uid+'&limit='+limit+'&start='+start, function(response){
            values=JSON.parse(response.response);
            if(self.firstRequest) {
                self.min = Math.min.apply(null, values);
                self.max = Math.max.apply(null, values);
                self.horizon.extent([0,self.max-self.min+2])
                d3.select('.top-limit-value').text('max '+self.max);
                d3.select('.bottom-limit-value').text('min '+self.min);
            }
            for(var i=0; i<values.length; i++)
                values[i] = parseFloat(values[i])-self.min
            callback(null, values);
            if(self.firstRequest) {
                self.firstRequest = false;
                self.context.stop()
            }
        })

    });

}

Chart.prototype.addRow = function(i,inter, uid) {
    var self = this;
    var metric = this.bigquery_metric(inter, uid);
    this.data.push(metric);

    var data = [metric]
    this.horizon = context.horizon()
        //.mode('mirror')
        .height(200)
        .colors(["#bdd7e7","#bae4b3"])

    this.chart = d3.select("#graph-"+i).selectAll(".horizon")
        .data(data)
        .enter()
        .insert("div", ".bottom")
            .attr("class", "horizon")
            .call(this.horizon)

    
    d3.selectAll('.horizon').append('div').append('p').attr('class', 'top-limit-value').text('axis')
    d3.selectAll('.horizon').append('div').append('p').attr('class', 'bottom-limit-value').text('axis')
}

Chart.prototype.init = function(i) {
    self = this;
    var axis = d3.select("#graph-"+i).selectAll(".axis")
        .data(["top", "bottom"])
        .enter().append("div")
            .attr("class", function(d) { return d + " axis"; })
            .each(function(d) { d3.select(this).call(self.context.axis().ticks(20).orient(d)); });

    d3.select("#graph-"+i).append("div")
        .attr("class", "rule")
        .call(this.context.rule());

    this.firstRequest = true;
}
