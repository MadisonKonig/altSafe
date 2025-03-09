import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import Input from "./components/Input";
import Verification from "./components/Verification";
import CheckIn from "./components/CheckIn";

function Prev() {
  const [key, setKey] = useState("email");
  const [showVerification, setShowVerification] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [checkInFrequency, setCheckInFrequency] = useState(0); // For storing check-in frequency

  // Check session state on component mount
  useEffect(() => {
    const sessionActive = localStorage.getItem("sessionActive");
    const storedFrequency = localStorage.getItem("checkInFrequency");
    if (sessionActive) {
      setIsVerified(true); // If session is active, set isVerified to true
    }
    if (storedFrequency) {
      setCheckInFrequency(Number(storedFrequency)); // Retrieve frequency from localStorage
    }
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    const frequencyInput = event.target.elements["frequency"].value;
    console.log(frequencyInput);
    setCheckInFrequency(Number(frequencyInput));
    localStorage.setItem("checkInFrequency", frequencyInput); // Save the frequency to localStorage
    setShowVerification(true);
  };

  const handleVerificationSuccess = () => {
    setIsVerified(true);
    localStorage.setItem("sessionActive", "true"); // Set session active in localStorage
  };

  const handleEndSession = () => {
    // End session and reset verified state
    localStorage.removeItem("sessionActive"); // Remove session from localStorage
    setIsVerified(false); // Set isVerified to false
  };

  return (
    <div className="App d-flex justify-content-center align-items-center vh-100">
      <div
        className="p-4 border rounded shadow-lg bg-light"
        style={{ width: "400px" }}
      >
        <h2 className="text-center mb-3">Check-in Preferences</h2>
        {!isVerified ? (
          <>
            <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-3">
              <Tab eventKey="email" title="Email">
                <Form onSubmit={handleSubmit}>
                  <Input
                    label="Email"
                    type="email"
                    placeholder="Enter your email"
                    required
                  />
                  <Input
                    label="Emergency Contact's Email"
                    type="email"
                    placeholder="Emergency contact's email"
                    required
                  />
                  <Input
                    label="Check-in Frequency (minutes)"
                    type="number"
                    placeholder="Enter frequency in minutes"
                    name="frequency"
                    required
                  />
                  <Button
                    variant="primary"
                    className="mt-3 w-100"
                    type="submit"
                  >
                    Submit
                  </Button>
                </Form>
              </Tab>
              <Tab eventKey="phone" title="Phone">
                <Form onSubmit={handleSubmit}>
                  <Input
                    label="Phone Number"
                    type="tel"
                    placeholder="Enter your phone number"
                    required
                  />
                  <Input
                    label="Emergency Contact's Phone"
                    type="tel"
                    placeholder="Emergency contact's phone number"
                    required
                  />
                  <Input
                    label="Check-in Frequency (minutes)"
                    type="number"
                    placeholder="Enter frequency in minutes"
                    name="frequency"
                    required
                  />
                  <Button
                    variant="primary"
                    className="mt-3 w-100"
                    type="submit"
                  >
                    Submit
                  </Button>
                </Form>
              </Tab>
            </Tabs>
            {showVerification && (
              <Verification onSuccess={handleVerificationSuccess} />
            )}
          </>
        ) : (
          <CheckIn
            onEndSession={handleEndSession}
            checkInFrequency={checkInFrequency}
          /> // Pass frequency to CheckIn
        )}
      </div>
    </div>
  );
}
