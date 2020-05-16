import React, { Component } from "react";
import { Link } from "react-router-dom";
import LayersIcon from "@material-ui/icons/Layers";
import { connect } from "react-redux";
import { logoutUser } from "../../actions/authActions";
import OpenSelect from "./Selection";

class Navbar extends Component {
  onLogoutClick = (e) => {
    e.preventDefault();
    this.props.logoutUser();
  };
  renderAuthenticatedUser() {
    if (this.props.auth.isAuthenticated) {
      return (
        <div>
          <button
            style={{
              width: "10%",
              borderRadius: "3px",
              letterSpacing: "1.5px",
              position: "absolute",
              right: "10px",
            }}
            onClick={this.onLogoutClick}
            className="btn  waves-effect waves-light hoverable blue accent-3"
          >
            Logout
          </button>
          <OpenSelect />
        </div>
      );
    }
  }
  render() {
    return (
      <div className="navbar-fixed">
        <nav className="z-depth-0">
          <div className="nav-wrapper">
            <Link to="/" className="col s5 brand-logo center white-text">
              <LayersIcon />
              PlatIntel
            </Link>
            {this.renderAuthenticatedUser()}
          </div>
        </nav>
      </div>
    );
  }
}
const mapStateToProps = (state) => ({
  auth: state.auth,
});
export default connect(mapStateToProps, { logoutUser })(Navbar);
