import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import httpClient from "../httpClient";
import ResidentAnnouncementModal from "../Resident_Page/ResidentsannouncementModal"; // Updated import for the unique modal
import ResidentHeader from "./ResidentHeader"; // Import ResidentHeader
import "../Resident_style/ResidentDashboard.css"; // Import the updated CSS

const ResidentDashboard = () => {
  const [user, setUser] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false); // Control modal open/close
  const [announcements, setAnnouncements] = useState([]); // Store announcements data
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const resp = await httpClient.get("http://localhost:5000/@me");
        setUser(resp.data);
      } catch (error) {
        console.log("Not authenticated, redirecting to login.");
        navigate("/login");
      }
    };

    fetchUserData();
    fetchAnnouncements(); // Fetch announcements on component mount
  }, [navigate]);

  const fetchAnnouncements = async () => {
    try {
      const response = await httpClient.get("http://localhost:5000/announcementad");
      setAnnouncements(response.data);
      console.log("Fetched announcements:", response.data); // Debug log
      if (response.data.length > 0) {
        setModalOpen(true); // Open modal after fetching announcements
      } else {
        console.log("No announcements available.");
      }
    } catch (error) {
      console.error("Error fetching announcements:", error);
    }
  };

  const logoutUser = async () => {
    await httpClient.post("http://localhost:5000/logout");
    setUser(null);
    navigate("/login");
  };

  if (!user) return <div>Loading...</div>; // Show loading if user data is not available

  return (
    <div className="dashboard-container">
      {/* Resident Header with user info and logout functionality */}
      <ResidentHeader user={user} onLogout={logoutUser} />

      <div className="card-container">
        <div className="dashboard-card">
          <span role="img" aria-label="Household">🏠</span>
          <h3>Household/Residents</h3>
          <button onClick={() => navigate("/household")}>Open</button>
        </div>

        <div className="dashboard-card">
          <span role="img" aria-label="Announcements">📅</span>
          <h3>Announcements</h3>
          <button onClick={() => setModalOpen(true)}>Open</button>
        </div>
      </div>

      {/* Resident Announcement Modal */}
      <ResidentAnnouncementModal 
        isOpen={isModalOpen} 
        onClose={() => setModalOpen(false)} 
        announcements={announcements}  // Pass announcements data to modal
      />
    </div>
  );
};

export default ResidentDashboard;
