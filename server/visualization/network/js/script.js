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
    networkSeries.dataFields.linkWith = "linkWith";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.children = "children";
    networkSeries.dataFields.id = "id";
    networkSeries.dataFields.collapsed = "collapsed";
    networkSeries.dataFields.color = "type";

    networkSeries.nodes.template.tooltipText = "{name}";
    networkSeries.nodes.template.fillOpacity = 1;
    networkSeries.linkWithStrength = 0;
    networkSeries.minRadius = am4core.percent(2);
    networkSeries.nodes.template.events.on("hit", function (ev) {
        if (ev.target.dataItem.id.includes("twitter")) {
            window.open("https://" + ev.target.dataItem.id, '_blank');
        }
    });

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 10;

    var linkTemplate = networkSeries.links.template;
    linkTemplate.strokeWidth = 1;
    var linkHoverState = linkTemplate.states.create("hover");
    linkHoverState.properties.strokeOpacity = 1;
    linkHoverState.properties.strokeWidth = 2;


});