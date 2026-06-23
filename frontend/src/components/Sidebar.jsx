import { useEffect, useState } from "react";
import api from "../services/api";

import UploadPDF from "./UploadPDF";

import "../styles/sidebar.css";

function Sidebar({
  setMessages,
  setSelectedSessionId,
  selectedSessionId,
   refreshSidebar,
}) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchSessions();
  }, [refreshSidebar]);

  const fetchSessions = async () => {
    try {
      const response = await api.get("sessions/");

      setSessions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const createSession = async () => {
    try {
      const response = await api.post(
        "sessions/",
        {
          title: "New Chat",
        }
      );

      fetchSessions();

      loadMessages(response.data.id);

    } catch (error) {
      console.error(error);
    }
  };

  const loadMessages = async (sessionId) => {

    setSelectedSessionId(sessionId);

    try {
      const response = await api.get(
        `sessions/${sessionId}/messages/`
      );

      setMessages(response.data);

    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="sidebar">

      <div className="sidebar-title">
        RAG Chatbot
      </div>

      <button
        className="new-chat-btn"
        onClick={createSession}
      >
        + New Chat
      </button>

      <UploadPDF />

      <hr />

      {sessions.map((session) => (
        <div
          key={session.id}
          onClick={() =>
            loadMessages(session.id)
          }
          className={`session-item ${
            selectedSessionId === session.id
              ? "active-session"
              : ""
          }`}
        >
          {session.title}
        </div>
      ))}
    </div>
  );
}

export default Sidebar;