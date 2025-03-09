import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import useInterval from "../components/hooks/useInterval";

function CheckIn({ onEndSession }) {
  const [location, setLocation] = useState(null); // User location
  const [lastCheckInTime, setLastCheckInTime] = useState(null); // Last check-in time
  const [remainingTime, setRemainingTime] = useState(0); // Remaining time in seconds
  const [isSessionActive, setIsSessionActive] = useState(true); // Session status
  const [isCheckingIn, setIsCheckingIn] = useState(false); // Check-in progress status
  const [checkInAvailable, setCheckInAvailable] = useState(true); // Track if check-in is available
  const [checkInButtonClicked, setCheckInButtonClicked] = useState(false); // Track if button has been clicked
  const [locationFetched, setLocationFetched] = useState(false); // Track if location has been fetched

  const checkInFrequency =
    Number(localStorage.getItem("checkInFrequency")) || 0; // Get check-in frequency from local storage (in minutes)

  // Convert check-in frequency from minutes to seconds
  const checkInFrequencyInSeconds = checkInFrequency * 60;

  // Get user's location using geolocation API
  const getLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation(position.coords); // Store location
        setLastCheckInTime(new Date()); // Record check-in time
        setLocationFetched(true); // Mark location as fetched
      },
      (error) => {
        console.log("Geolocation error:", error); // Handle location error
      }
    );
  };

  const sendEmergencyAlert = () => {
    console.log("Emergency Alert: You missed a check-in!");
    // Add logic to send email or SMS here (e.g., integrate an email API)
  };

  // Automatically attempt check-in (interval setup)
  useInterval(() => {
    if (
      isSessionActive &&
      locationFetched &&
      checkInFrequency > 0 &&
      lastCheckInTime
    ) {
      const now = new Date();
      const timeDiff = now - lastCheckInTime; // Time difference in milliseconds
      const timeLeft = checkInFrequencyInSeconds - Math.floor(timeDiff / 1000); // Time left in seconds

      // If time is up, send an alert and reset check-in time
      if (timeDiff > checkInFrequencyInSeconds * 1000) {
        sendEmergencyAlert();
        setLastCheckInTime(now); // Reset last check-in time after alert
      }

      // Ensure remainingTime does not go below 0
      if (timeLeft >= 0) {
        setRemainingTime(timeLeft); // Update remaining time
      } else {
        setRemainingTime(0); // If time left is negative, set it to 0
      }
    }
  }, 1000); // Check every second (1000 ms)

  // Triggered when Start check-in button is clicked
  const handleCheckIn = () => {
    setIsCheckingIn(true); // Change to checking in state
    getLocation(); // Request location
    setRemainingTime(checkInFrequencyInSeconds); // Set initial remaining time
    setCheckInButtonClicked(true); // Mark that the button has been clicked
  };

  // Handle session end
  const handleEndSession = () => {
    setIsSessionActive(false); // Change to session inactive state
    onEndSession(); // Request session end from App.js
  };

  // Handle reactivation of button when remaining time is 0
  useEffect(() => {
    if (remainingTime === 0 && isSessionActive) {
      // Reactivate the button when remaining time is 0
      setCheckInAvailable(true); // Make "Start Check-in" button available again
      setIsCheckingIn(false); // Reset checking in state
    }
  }, [remainingTime, isSessionActive]);

  // Handle check-in availability timeout (20 seconds window)
  useEffect(() => {
    if (checkInButtonClicked) {
      // Set a timeout for 20 seconds after the check-in button is clicked
      const timeout = setTimeout(() => {
        if (!checkInAvailable) {
          sendEmergencyAlert(); // Send an email alert if button was not pressed in time
        }
      }, 20000); // 20 seconds timeout

      return () => clearTimeout(timeout); // Clean up the timeout when the component unmounts or state changes
    }
  }, [checkInButtonClicked, checkInAvailable]);

  // Format remaining time as minutes:seconds
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const sec = seconds % 60;
    return `${minutes}:${sec < 10 ? "0" + sec : sec}`; // Ensure two digits for seconds
  };

  return (
    <div className="check-in">
      <h3>Check-in</h3>

      {/* Start Check-in button */}
      {isSessionActive && !isCheckingIn ? (
        <Button onClick={handleCheckIn} disabled={!checkInAvailable}>
          {checkInAvailable ? "Start Check-in" : "Waiting..."}
        </Button>
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
      <p>Remaining Time: {formatTime(remainingTime)}</p>

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
