import React from "react";
import styled from "styled-components";

export default function FullButton({ title, action, border }) {
  return (
    <Wrapper
      className="animate pointer radius8"
      onClick={action ? () => action() : null}
      border={border}
    >
      {title}
    </Wrapper>
  );
}

const Wrapper = styled.button`
  border: 1px solid ${(props) => (props.border ? "#707070" : "#F7B03D")};
  background-color: ${(props) => (props.border ? "transparent" : "#F7B03D")};
  width: 100%;
  padding: 15px;
  outline: none;
  color: ${(props) => (props.border ? "#707070" : "#fff")};
  &:hover {
    background-color: ${(props) => (props.border ? "transparent" : "#FFC973")};
    border: 1px solid #ffc973;
    color: ${(props) => (props.border ? "#FFC973" : "#fff")};
  }
`;
