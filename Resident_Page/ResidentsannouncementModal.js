import React from "react";
import "../Resident_style/Residentannouncementmodal.css"; // Ensure you reference the unique CSS

const ResidentsAnnouncementModal = ({ isOpen, onClose, announcements }) => {
  if (!isOpen) return null; // Don't render the modal if it's not open

  return (
    <div className="residents-modal-overlay">
      <div className="residents-modal-content">
        <h2>Announcement</h2>
        <button onClick={onClose} className="residents-close-button">Close</button>
        <ul>
          {announcements.map((announcement, index) => (
            <li key={index}>{announcement.title}: {announcement.content}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ResidentsAnnouncementModal;
