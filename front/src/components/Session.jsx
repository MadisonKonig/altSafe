import Button from "react-bootstrap/Button";

function Session({ onLogout }) {
  return (
    <div className="text-center">
      <h3 className="text-success">Session Started!</h3>
      <Button variant="danger" className="mt-3 w-100" onClick={onLogout}>
        End Session
      </Button>
    </div>
  );
}

export default Session;
