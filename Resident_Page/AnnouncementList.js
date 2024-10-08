import React, { useEffect, useState } from "react";
import httpClient from "../httpClient";
import "../Resident_style/AnnouncementList.css"; // Assuming you have some styles

const AnnouncementList = () => {
  const [announcements, setAnnouncements] = useState([]);
  const [selectedAnnouncement, setSelectedAnnouncement] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const fetchAnnouncements = async () => {
      try {
        const response = await httpClient.get("http://localhost:5000/announcementad");
        console.log("Fetched announcements:", response.data); // Debug log
        setAnnouncements(response.data);
      } catch (error) {
        console.error("Error fetching announcements:", error);
      }
    };

    fetchAnnouncements(); // Fetch announcements on component mount
  }, []);

  const openModal = (announcement) => {
    setSelectedAnnouncement(announcement);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelectedAnnouncement(null);
  };

  return (
    <div className="announcement-list">
      <h2>Announcements</h2>
      <ul>
        {announcements.map((announcement) => (
          <li key={announcement.id} onClick={() => openModal(announcement)}>
            <h3>{announcement.title}</h3>
            <p>{announcement.description}</p>
          </li>
        ))}
      </ul>

      {/* Modal for displaying selected announcement details */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            {selectedAnnouncement && (
              <>
                <h2>{selectedAnnouncement.title}</h2>
                <p>{selectedAnnouncement.description}</p>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnnouncementList;
