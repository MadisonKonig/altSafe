import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const Verification = ({ onSuccess }) => {
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedCode, setGeneratedCode] = useState("");

  useEffect(() => {
    // 임시 인증 코드를 생성하여 저장
    const code = Math.floor(100000 + Math.random() * 900000); // 6자리 코드
    setGeneratedCode(code);
    console.log("Generated code:", code); // 콘솔에 생성된 코드 출력 (디버깅용)
  }, []);

  const handleVerification = (event) => {
    event.preventDefault();
    setLoading(true);
    setErrorMessage("");

    // 인증 코드 검증 (서버 없이 프론트엔드에서만 처리)
    if (parseInt(code) === generatedCode) {
      onSuccess(); // 인증 성공
    } else {
      setErrorMessage("Invalid verification code. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="verification">
      <h3 className="text-center">Enter Your Verification Code</h3>
      <Form onSubmit={handleVerification}>
        <Form.Group controlId="verificationCode">
          <Form.Label>Verification Code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter your code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
          />
        </Form.Group>
        {errorMessage && <p className="text-danger">{errorMessage}</p>}
        <Button
          variant="primary"
          className="mt-3 w-100"
          type="submit"
          disabled={loading}
        >
          {loading ? "Verifying..." : "Verify Code"}
        </Button>
      </Form>
    </div>
  );
};

export default Verification;
