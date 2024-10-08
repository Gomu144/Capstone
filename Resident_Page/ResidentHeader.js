import React from "react";
import "../Resident_style/ResidentHeader.css"; // Assuming custom styles for the ResidentHeader
import logo from "../images/logo.png"; // Import the logo image

const ResidentHeader = ({ user, onLogout }) => {
  return (
    <header className="resident-header-container">
      <div className="resident-logo-section">
        <img src={logo} alt="BTRRS Logo" className="resident-logo" /> {/* Add the logo image */}
        <div className="resident-logo-text">
          <h1>BTRRS</h1>
          <p>Barangay TawantawanAAAA</p>
        </div>
      </div>

      <div className="resident-user-section">
        <span className="resident-user-name">{user ? user.full_name : 'Loading...'}</span>
        <span className="resident-user-role">
          {user ? user.role : 'Resident'} 
          <span className="resident-household-icon">👪</span>
        </span>
        <span className="resident-logout-icon" onClick={onLogout} role="button" aria-label="Logout">➔</span>
      </div>
    </header>
  );
};

export default ResidentHeader;
