var STEP = 4e3;
var NUM_OF_STEPS = (8*60*60*1000)/STEP;
var context = cubism.context()

var Chart = function(step, num_of_steps) {

    context = cubism.context()
        .step(STEP)
        .size(960);
    this.context = context;
}

Chart.prototype.bigquery_metric= function(inter, uid, limit) {
    var value = 0,
          values = [],
          i = 0,
          last;

    return context.metric(function(start, stop, step, callback) {
        alert(start +" "+ stop+" "+step)
        var values = [];
        stop = +stop;
        start = +start

        var limit = (stop - start)/STEP;
        d3.xhr('/bigquery/freq/?interconnection='+inter+'&unit_id='+uid+'&limit='+limit+'&start='+start, function(response){
            values=JSON.parse(response.response);
            for(var i=0; i<values.length; i++)
                values[i] = parseFloat(values[i])
            callback(null, values);
        })

    });

}

Chart.prototype.addRow = function(inter, uid) {
    var data = [this.bigquery_metric(inter, uid),]
    var horizon = context.horizon()
        //.mode('mirror')
        .height(300)
        .extent([55,65])
        .colors(["#bdd7e7","#bae4b3"])
    d3.select(".graph").selectAll(".horizon")
        .data(data)
        .enter()
        .insert("div", ".bottom")
            .attr("class", "horizon")
            .call(horizon)
    this.context.on("focus", function(i) {
        d3.selectAll(".value").style("right", i == null ? null : context.size() - i + "px");
    });
}

Chart.prototype.init = function() {
    self = this;
    d3.select(".graph").selectAll(".axis")
        .data(["top", "bottom"])
        .enter().append("div")
            .attr("class", function(d) { return d + " axis"; })
            .each(function(d) { d3.select(this).call(self.context.axis().ticks(12).orient(d)); });

    d3.select(".graph").append("div")
        .attr("class", "rule")
        .call(this.context.rule());


}
