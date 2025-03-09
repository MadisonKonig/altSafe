import React from "react";
import BootstrapButton from "react-bootstrap/Button";

const Button = ({ label, color }) => {
  return <BootstrapButton style={color}>{label}</BootstrapButton>;
};

export default Button;
