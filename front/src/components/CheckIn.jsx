import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import useInterval from "../components/hooks/useInterval";

function CheckIn({ onEndSession }) {
  const [location, setLocation] = useState(null); // 사용자 위치
  const [lastCheckInTime, setLastCheckInTime] = useState(null); // 마지막 체크인 시간
  const [remainingTime, setRemainingTime] = useState(0); // 남은 시간
  const [isSessionActive, setIsSessionActive] = useState(true); // 세션 상태
  const [isCheckingIn, setIsCheckingIn] = useState(false); // 체크인 진행 상태

  const checkInFrequency =
    Number(localStorage.getItem("checkInFrequency")) || 0; // 로컬 스토리지에서 체크인 주기 가져오기

  // Get user's location using geolocation API
  const getLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation(position.coords); // 위치 저장
        setLastCheckInTime(new Date()); // 체크인 시간 기록
      },
      (error) => {
        console.log("Geolocation error:", error); // 위치 에러 처리
      }
    );
  };

  const sendEmergencyAlert = () => {
    console.log("Emergency Alert: You missed a check-in!");
    // 여기에 이메일 또는 SMS 보내는 로직을 추가할 수 있음
  };

  // 자동으로 체크인 시도 (interval 설정)
  useInterval(() => {
    if (isSessionActive && checkInFrequency > 0) {
      const now = new Date();
      if (
        lastCheckInTime &&
        now - lastCheckInTime > checkInFrequency * 60 * 1000
      ) {
        // 체크인 주기를 초과하면 실패로 간주하고 알림 보내기
        sendEmergencyAlert(); // 알림 전송
        setLastCheckInTime(now); // 알림 후 체크인 시간 리셋
      }

      // 남은 시간 계산
      const timeLeft =
        checkInFrequency - Math.floor((now - lastCheckInTime) / (60 * 1000)); // 남은 시간(분 단위)
      setRemainingTime(timeLeft >= 0 ? timeLeft : 0); // 남은 시간이 0 이하가 되지 않도록 처리
    }
  }, 60 * 1000); // 1분마다 체크

  // Start check-in 버튼 클릭 시 실행
  const handleCheckIn = () => {
    setIsCheckingIn(true); // 체크인 시작 상태로 변경
    getLocation(); // 위치 요청
  };

  // 세션 종료 처리
  const handleEndSession = () => {
    setIsSessionActive(false); // 세션 종료 상태로 변경
    onEndSession(); // App.js에 세션 종료 요청
  };

  // 체크인 주기가 설정되었을 때 초기화
  useEffect(() => {
    if (checkInFrequency > 0) {
      setLastCheckInTime(new Date()); // 체크인 시작 시점 설정
    }
  }, [checkInFrequency]);

  return (
    <div className="check-in">
      <h3>Check-in</h3>

      {/* Start Check-in 버튼 */}
      {!isSessionActive ? (
        <Button onClick={handleEndSession}>End Session</Button>
      ) : !isCheckingIn ? (
        <Button onClick={handleCheckIn}>Start Check-in</Button>
      ) : (
        <p>Checking in...</p>
      )}

      {location && (
        <div>
          <p>
            Location: {location.latitude}, {location.longitude}
          </p>
          <p>Last Check-in: {lastCheckInTime?.toLocaleTimeString()}</p>
        </div>
      )}

      {/* Remaining time display */}
      <p>Remaining Time: {remainingTime} minutes</p>

      {/* End Session button */}
      {isSessionActive && (
        <Button variant="danger" onClick={handleEndSession} className="mt-3">
          End Session
        </Button>
      )}
    </div>
  );
}

export default CheckIn;
