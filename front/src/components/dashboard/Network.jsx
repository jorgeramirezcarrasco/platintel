import React, { Component } from "react";

class Network extends Component {
  componentWillUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  }

  render() {
    return <div id="chartdiv" style={{ width: "100%", height: "90vh" }}></div>;
  }
}

export default Network;
