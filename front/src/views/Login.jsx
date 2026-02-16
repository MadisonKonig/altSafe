import React, { useState } from "react";
import styled from "styled-components";
import TopNavbar from "../components/Nav/TopNavbar";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const Login = () => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [step, setStep] = useState(1); // 1: enter phone number, 2: enter verification code
  const [userId, setUserId] = useState(null);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:8000/api/registration/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: phoneNumber }),
      });

      const data = await res.json();
      console.log("User: ", data);
      toast("Sending text successful!");
      setStep(2);

      // 로그인 성공 후 체크인 페이지로 이동
      // navigate("/VerificationCode"); // checkin 페이지로 이동
    } catch (error) {
      console.error("Login failed:", error);
      toast("Login Failed. Please try again.");
    }
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault(); 

    try {
      const res = await fetch("http://127.0.0.1:8000/api/verify_code/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, verification_code: verificationCode }),
      });

      const data = await res.json();
      localStorage.setItem("JWT", JSON.stringify(data["Header"]));
      console.log(data);
      console.log("Verification: ", data);
      toast("Verification successful!");

      // 로그인 성공 후 체크인 페이지로 이동
      navigate("/checkin");
    } catch (error) {
      console.error("Verification failed:", error);
      toast("Verification Failed. Please try again.");
    }
  };

  return (
    <>
      <TopNavbar />
      <Wrapper id="contact">
        <div className="">
          <div className="container">
            <HeaderInfo>
              <h1 className="font40 extraBold">Login</h1>
            </HeaderInfo>
            { step === 1 && (
              <div className="row" style={{ paddingBottom: "30px" }}>
              <div className="">
                <Form>
                  <label className="font13">Phone #:</label>
                  <input
                    type="tel"
                    id="phoneNumber"
                    name="phoneNumber"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className="font20 extraBold"
                  />
                </Form>
                <SumbitWrapper className="flex">
                  <ButtonInput
                    type="submit"
                    value="Login"
                    className="pointer animate radius8"
                    onClick={handleLogin}
                    style={{ maxWidth: "220px" }}
                  />
                </SumbitWrapper>
              </div>
            </div>
            )}
            {step === 2 && (
            <Form>
              <label className="font13">Enter 5-digit Code:</label>
              <input
                type="text"
                maxLength="5"
                id="verificationCode"
                name="verificationCode"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                className="font20 extraBold"
              />
              <SumbitWrapper className="flex">
                <ButtonInput
                  type="submit"
                  value="Verify"
                  className="pointer animate radius8"
                  onClick={handleVerifyCode}
                  style={{ maxWidth: "220px" }}
                />
              </SumbitWrapper>
            </Form>
          )}
          </div>
        </div>
      </Wrapper>
    </>
  );
};

export default Login;
const Wrapper = styled.section`
  width: 100%;
  max-width: 600px;
  padding: rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
`;
const HeaderInfo = styled.div`
  padding: 70px 0 30px 0;
  text-align: center;
  @media (max-width: 860px) {
    text-align: center;
  }
`;
const Form = styled.form`
  padding: 70px 0 30px 0;
  input,
  textarea {
    width: 100%;
    background-color: transparent;
    border: 0px;
    outline: none;
    box-shadow: none;
    border-bottom: 1px solid #707070;
    height: 30px;
    margin-bottom: 30px;
  }
  textarea {
    min-height: 100px;
  }
  @media (max-width: 860px) {
    padding: 30px 0;
  }
`;
const ButtonInput = styled.input`
  border: 1px solid #f7b03d;
  background-color: #f7b03d;
  width: 100%;
  padding: 15px;
  outline: none;
  color: #fff;
  &:hover {
    background-color: #ffc973;
    border: 1px solid #ffc973;
    color: #fff;
  }
  @media (max-width: 991px) {
    margin: 0 auto;
  }
`;

const SumbitWrapper = styled.div`
  @media (max-width: 991px) {
    width: 100%;
    margin-bottom: 50px;
  }
`;
