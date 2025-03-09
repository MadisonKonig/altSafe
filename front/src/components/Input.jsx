import Form from "react-bootstrap/Form";

const Input = ({ label, type, comment, id, placeholder, required, name }) => {
  const inputProps = {
    type,
    id,
    placeholder,
    required,
    name,
  };

  // If the type is 'number', set min and defaultValue
  if (type === "number") {
    inputProps.min = 0;
    inputProps.defaultValue = 10;
  }

  return (
    <>
      <Form.Label htmlFor={id}>{label}</Form.Label>
      <Form.Control {...inputProps} />
      {comment ? (
        <Form.Text id={id} muted>
          {comment}
        </Form.Text>
      ) : null}
    </>
  );
};

export default Input;
