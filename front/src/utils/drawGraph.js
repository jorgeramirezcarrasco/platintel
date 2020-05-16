import * as am4core from "@amcharts/amcharts4/core";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import * as am4plugins_forceDirected from "@amcharts/amcharts4/plugins/forceDirected";

const drawGraph = (data) => {
  am4core.useTheme(am4themes_animated);
  let chart = am4core.create(
    "chartdiv",
    am4plugins_forceDirected.ForceDirectedTree
  );
  //chart.legend = new am4charts.Legend();
  let networkSeries = chart.series.push(
    new am4plugins_forceDirected.ForceDirectedSeries()
  );

  chart.data = data;

  networkSeries.dataFields.value = "value";
  networkSeries.dataFields.linkWith = "linkWith";
  networkSeries.dataFields.name = "name";
  networkSeries.dataFields.children = "children";
  networkSeries.dataFields.id = "id";
  networkSeries.dataFields.collapsed = "collapsed";
  networkSeries.dataFields.color = "type";

  networkSeries.nodes.template.tooltipText = "{name}";
  networkSeries.nodes.template.fillOpacity = 1;
  networkSeries.linkWithStrength = 0.2;
  networkSeries.minRadius = am4core.percent(1.5);
  networkSeries.nodes.template.events.on("hit", function (ev) {
    if (ev.target.dataItem.id.includes("twitter")) {
      window.open("https://" + ev.target.dataItem.id, "_blank");
    }
  });
  networkSeries.events.on("inited", function () {
    networkSeries.animate(
      {
        property: "velocityDecay",
        to: 1,
      },
      30000
    );
  });
  networkSeries.nodes.template.label.text = "{name}";
  networkSeries.fontSize = 10;

  let linkTemplate = networkSeries.links.template;
  linkTemplate.strokeWidth = 1;
  let linkHoverState = linkTemplate.states.create("hover");
  linkHoverState.properties.strokeOpacity = 1;
  linkHoverState.properties.strokeWidth = 2;
};

export default drawGraph;
