import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";
import Sidebar from "./Sidebar"; // Assuming Sidebar is another component
import "../styles/announcementad.css"; // Import CSS

const AnnouncementAd = () => {
  const [adAnnouncements, setAdAnnouncements] = useState([]);
  const [adTitle, setAdTitle] = useState("");
  const [adContent, setAdContent] = useState("");
  const [adError, setAdError] = useState("");
  const [adModalOpen, setAdModalOpen] = useState(false);
  const [adViewModalOpen, setAdViewModalOpen] = useState(false);
  const [selectedAd, setSelectedAd] = useState(null);

  // Fetch announcements on component load
  useEffect(() => {
    const fetchAdAnnouncements = async () => {
      try {
        const resp = await httpClient.get("http://localhost:5000/announcementad"); // Corrected endpoint
        setAdAnnouncements(resp.data);
      } catch (error) {
        console.error("Failed to fetch ads:", error);
      }
    };

    fetchAdAnnouncements();
  }, []);

  const handleAdSubmit = async (e) => {
    e.preventDefault();
    if (!adTitle || !adContent) {
      setAdError("Both title and content are required");
      return;
    }

    try {
      await httpClient.post("http://localhost:5000/announcementad", { // Corrected endpoint
        title: adTitle,
        content: adContent,
      });
      setAdTitle("");
      setAdContent("");
      setAdError("");
      setAdModalOpen(false);

      // Refresh the ads list after submission
      const resp = await httpClient.get("http://localhost:5000/announcementad"); // Corrected endpoint
      setAdAnnouncements(resp.data);
    } catch (error) {
      console.error("Failed to submit ad:", error.response ? error.response.data : error.message);
      setAdError("Failed to submit ad. Please try again.");
    }
  };

  const handleViewAd = (ad) => {
    setSelectedAd(ad);
    setAdViewModalOpen(true);
  };

  return (
    <div className="announcement-ad-page">
      <Sidebar />
      <div className="ad-content">
        <div className="ad-cards-container">
          {/* Card: Create New Ad */}
          <div className="ad-card add-ad-card" onClick={() => setAdModalOpen(true)}>
            <h2>Create New Announcement</h2>
            <p>Click to create a new announcements.</p>
          </div>

          {/* Card: View Ads */}
          <div className="ad-card view-ad-card" onClick={() => setAdViewModalOpen(true)}>
            <h2>View announcements</h2>
            <p>Click to view the announcements.</p>
          </div>
        </div>

        {/* Modal for Adding Ad */}
        {adModalOpen && (
          <div className="ad-modal show">
            <div className="ad-modal-content">
              <span className="ad-close" onClick={() => setAdModalOpen(false)}>&times;</span>
              <h2>Create an announcements</h2>
              <form onSubmit={handleAdSubmit}>
                <input
                  type="text"
                  value={adTitle}
                  onChange={(e) => setAdTitle(e.target.value)}
                  placeholder="Ad Title"
                  required
                />
                <textarea
                  value={adContent}
                  onChange={(e) => setAdContent(e.target.value)}
                  placeholder="Ad Content"
                  required
                />
                <button type="submit" className="ad-btn">Submit Announcements</button>
              </form>
              {adError && <p className="ad-error">{adError}</p>}
            </div>
          </div>
        )}

        {/* Modal for Viewing Ads */}
        {adViewModalOpen && (
          <div className="ad-modal show">
            <div className="ad-modal-content">
              <span className="ad-close" onClick={() => setAdViewModalOpen(false)}>&times;</span>
              <h2>Announcements</h2>
              <div className="ad-list">
                {adAnnouncements.map((ad) => (
                  <div key={ad.id} className="ad-item" onClick={() => handleViewAd(ad)}>
                    <h3>{ad.title}</h3>
                    <p>{ad.content}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Modal for Viewing Selected Ad */}
        {selectedAd && adViewModalOpen && (
          <div className="ad-modal show">
            <div className="ad-modal-content">
              <span className="ad-close" onClick={() => setSelectedAd(null)}>&times;</span>
              <h2>{selectedAd.title}</h2>
              <p>{selectedAd.content}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnnouncementAd;
