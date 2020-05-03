import React, { Component } from "react";
import { Link } from "react-router-dom";
class GenericNotFound extends Component {
  render() {
    return (
      <div>
        <Link to="/" className="col s5 brand-logo center white-text">
          <p>Ups.. Page not found. Return to Home</p>
        </Link>
      </div>
    );
  }
}

export default GenericNotFound;
