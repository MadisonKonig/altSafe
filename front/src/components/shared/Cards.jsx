import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Card } from "react-bootstrap";

// Reusable Card Component
const CustomCard = ({ icon, title, description, bgColor }) => {
  return (
    <Card className={`shadow-lg ${bgColor} text-black w-100 h-100`}> 
      <Card.Body>
        <div className="mb-3 display-4">{icon}</div>
        <Card.Title className="text-primary">{title}</Card.Title>
        <Card.Text className="text-muted mt-2">{description}</Card.Text>
      </Card.Body>
    </Card>
  );
};

// Main Layout Component
const Cards = () => {
  const cards = [
    { icon: "⚠️", title: "Alert", description: "Triggers an emergency alert.", bgColor: "" },  //Add bg color
    { icon: "⏳", title: "Meeting Timer", description: "Set a timer for safety.", bgColor: "" },
    { icon: "📸", title: "Evidence Gathering", description: "Record evidence automatically.", bgColor: "" },
    { icon: "📍", title: "Journey", description: "Track your journey for safety.", bgColor: "" }
  ];

  return (
    <div className="container mt-4">
      <div className="row g-4 justify-content-center">
        {cards.map((card, index) => (
          <div key={index} className="col-12 col-sm-6 col-lg-3">
            <CustomCard {...card} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Cards;
