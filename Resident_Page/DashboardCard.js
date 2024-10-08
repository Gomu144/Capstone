import React from "react";
import "../Resident_style/DashboardCard.css"; // Link to CSS for the card

const DashboardCard = ({ title, icon, onClick }) => {
  return (
    <div className="dashboard-card" onClick={onClick}>
      <div className="icon-section">{icon}</div>
      <div className="text-section">
        <h3>{title}</h3>
        <button className="open-button">Open</button>
      </div>
    </div>
  );
};

export default DashboardCard;
