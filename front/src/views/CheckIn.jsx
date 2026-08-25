import React, { useState } from "react";
import styled from "styled-components";
import TopNavbar from "../components/Nav/TopNavbar";
import FullButton from "../components/Buttons/FullButton";

const CheckIn = () => {
  const [emergencyPhone, setEmergencyPhone] = useState(""); // 문자를 받을 사람 번호
  const [intervalTime, setIntervalTime] = useState(""); // 체크인 주기 (분)
  const [isCheckedIn, setIsCheckedIn] = useState(false);

  const handleCheckIn = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/session/start/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          //TODO: add phone number for lookup from cookies
          emergency_phone: emergencyPhone,
          interval_time: intervalTime,
        }),
      });

      const data = await res.json();

      if (data.success) {
        setIsCheckedIn(true);
        alert("You have successfully checked in!");
      } else {
        alert("Check-in failed. Please try again.");
      }
    } catch (error) {
      console.error("Error checking in:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <>
      <TopNavbar />
      <Wrapper>
        <div className="container">
          <HeaderInfo>
            <h1 className="font40 extraBold">Session Info</h1>
          </HeaderInfo>
          <div className="" style={{ paddingBottom: "30px" }}>
            <div className="">
              <Form onSubmit={handleCheckIn}>
                <CheckInMessage>
                  {isCheckedIn ? (
                    <p>You have successfully checked in!</p>
                  ) : (
                    <p>Please enter the information below to start a session.</p>
                  )}
                </CheckInMessage>

                <InputWrapper>
                  <label>Emergency Contact's Phone Number</label>
                  <input
                    type="tel"
                    value={emergencyPhone}
                    onChange={(e) => setEmergencyPhone(e.target.value)}
                    required
                    placeholder="Enter emergency contact's phone number"
                  />
                </InputWrapper>

                <InputWrapper>
                  <label>Interval Time (in minutes)</label>
                  <input
                    type="number"
                    value={intervalTime}
                    onChange={(e) => setIntervalTime(e.target.value)}
                    min={0}
                    required
                    placeholder="Enter check-in interval (minutes)"
                  />
                </InputWrapper>

                <SumbitWrapper>
                  <FullButton type="submit" title="Check In" />
                </SumbitWrapper>
              </Form>
            </div>
          </div>
        </div>
      </Wrapper>
    </>
  );
};

export default CheckIn;

const Wrapper = styled.section`
  width: 100%;
  max-width: 600px;
  padding: 3rem;
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
  width: 100%;
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
  }
`;

const CheckInMessage = styled.div`
  text-align: center;
  margin-bottom: 20px;
  font-size: 18px;
`;

const InputWrapper = styled.div`
  margin-bottom: 20px;
  label {
    font-size: 14px;
    font-weight: bold;
  }
  input {
    font-size: 16px;
    padding: 10px;
  }
`;

const SumbitWrapper = styled.div`
  @media (max-width: 991px) {
    width: 100%;
    margin-bottom: 50px;
  }
`;
