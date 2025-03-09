import Form from "react-bootstrap/Form";

const Input = ({ label, type, comment, id, placeholder, required, name }) => {
  return (
    <>
      <Form.Label htmlFor="inputPassword5">{label}</Form.Label>
      <Form.Control
        type={type}
        id={id}
        aria-describedby="passwordHelpBlock"
        placeholder={placeholder}
        required={required}
        name={name}
      />
      {comment ? (
        <Form.Text id={id} muted>
          {comment}
        </Form.Text>
      ) : null}
    </>
  );
};

export default Input;
