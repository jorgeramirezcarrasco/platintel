import React from "react";
import Select from "react-select";
import axios from "axios";
import drawGraph from "../../utils/drawGraph";

class Selection extends React.Component {
  state = {
    analyses: [],
    selectedOption: null,
  };
  handleChange = (selectedOption) => {
    const API_ENDPOINT =
      process.env.REACT_APP_API_ENDPOINT ||
      "https://platintel-back.herokuapp.com";
    this.setState({ selectedOption }, () => {
      axios.defaults.headers.common["Authorization"] = localStorage.jwtToken;
      axios
        .post(API_ENDPOINT + "/api/analyses/data", {
          analysis: this.state.selectedOption.label,
        })
        .then((res) => {
          console.log(res.data);
          drawGraph(res.data);
        });
    });
  };

  componentDidMount() {
    const API_ENDPOINT =
      process.env.REACT_APP_API_ENDPOINT ||
      "https://platintel-back.herokuapp.com";

    axios.defaults.headers.common["Authorization"] = localStorage.jwtToken;
    axios.get(API_ENDPOINT + "/api/analyses/list").then((res) => {
      var x;
      for (x in res.data) {
        this.state.analyses.push({ value: x, label: res.data[x]["analysis"] });
      }
    });
  }

  render() {
    const { selectedOption } = this.state;

    const customStyles = {
      option: (styles, { data, isDisabled, isFocused, isSelected }) => {
        return {
          ...styles,
          backgroundColor: isFocused ? "blue" : "#30303d",
        };
      },
      singleValue: (style) => {
        return {
          ...style,
          color: "#fff",
        };
      },
    };

    return (
      <div
        className="analysis-select"
        style={{
          width: "20%",
          marginLeft: "10px",
        }}
      >
        <p>Analysis</p>
        <Select
          id="analysis"
          styles={customStyles}
          value={selectedOption}
          onChange={this.handleChange}
          options={this.state.analyses}
        />
      </div>
    );
  }
}

export default Selection;
