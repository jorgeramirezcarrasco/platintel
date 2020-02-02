am4core.ready(function () {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);
    chart.legend = new am4charts.Legend();
    var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
    chart.dataSource.url = "/data";
    chart.dataSource.parser = new am4core.JSONParser();
    //chart.data = []


    networkSeries.dataFields.value = "value";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.children = "children";
    networkSeries.dataFields.collapsed = "collapsed";

    networkSeries.nodes.template.tooltipText = "{name}";
    networkSeries.nodes.template.fillOpacity = 1;
    networkSeries.manyBodyStrength = -20;
    networkSeries.links.template.strength = 0.8;
    networkSeries.minRadius = am4core.percent(2);
    networkSeries.nodes.template.events.on("hit", function (ev) {
        if (ev.target.dataItem.name.includes("twitter")) {
            window.open("https://" + ev.target.dataItem.name, '_blank');
        }
    });

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 10;

}); // end am4core.ready()