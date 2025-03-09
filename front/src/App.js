import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import Input from "./components/Input";
import Verification from "./components/Verification";
import Session from "./components/Session";
import CheckIn from "./components/CheckIn";

function App() {
  const [key, setKey] = useState("email");
  const [showVerification, setShowVerification] = useState(false);
  const [isVerified, setIsVerified] = useState(false);

  useEffect(() => {
    const sessionActive = localStorage.getItem("sessionActive");
    if (sessionActive) {
      setIsVerified(true);
    }
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    setShowVerification(true);
  };

  const handleVerificationSuccess = () => {
    setIsVerified(true);
    localStorage.setItem("sessionActive", "true");
  };

  const handleLogout = () => {
    // Clear session data
    localStorage.removeItem("sessionActive");
    setIsVerified(false); // Update isVerified state to false
    setShowVerification(false); // Hide verification
  };

  const handleEndSession = () => {
    // End session and reset verified state
    localStorage.removeItem("sessionActive");
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
          <CheckIn onEndSession={handleEndSession} /> // Pass handleEndSession to CheckIn
        )}
      </div>
    </div>
  );
}

export default App;
