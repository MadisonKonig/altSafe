import Form from "react-bootstrap/Form";

const Input = ({ label, type, comment, id, placeholder, required }) => {
  return (
    <>
      <Form.Label htmlFor="inputPassword5">{label}</Form.Label>
      <Form.Control
        type={type}
        id={id}
        aria-describedby="passwordHelpBlock"
        placeholder={placeholder}
        required={required}
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
