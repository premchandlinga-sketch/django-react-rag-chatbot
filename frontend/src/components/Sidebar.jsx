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

  const [sessions, setSessions] =
    useState([]);

  const [menuOpen, setMenuOpen] =
    useState(null);

  useEffect(() => {
    fetchSessions();
  }, [refreshSidebar]);

  const fetchSessions = async () => {

    try {

      const response =
        await api.get(
          "sessions/"
        );

      setSessions(
        response.data
      );

    } catch (error) {

      console.error(error);

    }
  };

  const createSession = async () => {

    try {

      const response =
        await api.post(
          "sessions/",
          {
            title:
              "New Chat",
          }
        );

      await fetchSessions();

      loadMessages(
        response.data.id
      );

    } catch (error) {

      console.error(error);

    }
  };

  const loadMessages = async (
    sessionId
  ) => {

    setSelectedSessionId(
      sessionId
    );

    try {

      const response =
        await api.get(
          `sessions/${sessionId}/messages/`
        );

      setMessages(
        response.data
      );

    } catch (error) {

      console.error(error);

    }
  };

  const renameSession =
    async (session) => {

      const newTitle =
        prompt(
          "Enter new title",
          session.title
        );

      if (
        !newTitle ||
        newTitle.trim() === ""
      ) {
        return;
      }

      try {

        await api.put(
          `sessions/${session.id}/`,
          {
            title:
              newTitle.trim(),
          }
        );

        await fetchSessions();

      } catch (error) {

        console.error(error);

      }
    };

  const deleteSession =
    async (sessionId) => {

      const confirmed =
        window.confirm(
          "Delete this session?"
        );

      if (!confirmed) {
        return;
      }

      try {

        await api.delete(
          `sessions/${sessionId}/`
        );

        await fetchSessions();

        if (
          selectedSessionId ===
          sessionId
        ) {

          setMessages([]);

          setSelectedSessionId(
            null
          );
        }

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

      <UploadPDF
        selectedSessionId={
          selectedSessionId
        }
      />

      <hr />

      {sessions.map(
        (session) => (
          <div
            key={session.id}
            className={`session-item ${
              selectedSessionId ===
              session.id
                ? "active-session"
                : ""
            }`}
            style={{
              display: "flex",
              justifyContent:
                "space-between",
              alignItems:
                "center",
              position:
                "relative",
            }}
          >

            <span
              style={{
                flex: 1,
                cursor:
                  "pointer",
              }}
              onClick={() =>
                loadMessages(
                  session.id
                )
              }
            >
              {session.title}
            </span>

            <button
              onClick={(e) => {

                e.stopPropagation();

                setMenuOpen(
                  menuOpen ===
                    session.id
                    ? null
                    : session.id
                );
              }}
              style={{
                background:
                  "transparent",
                border:
                  "none",
                cursor:
                  "pointer",
                fontSize:
                  "18px",
                color: 
                  "white",  
              }}
            >
              ⋮
            </button>

            {menuOpen ===
              session.id && (

              <div
                style={{
                  position:
                    "absolute",
                  right: 0,
                  top: "35px",
                  background:
                    "white",
                  border:
                    "1px solid #ddd",
                  borderRadius:
                    "8px",
                  boxShadow:
                    "0 2px 10px rgba(0,0,0,0.1)",
                  zIndex: 100,
                  minWidth:
                    "120px",
                }}
              >

                <div
                  onClick={() => {

                    renameSession(
                      session
                    );

                    setMenuOpen(
                      null
                    );
                  }}
                  style={{
                    padding:
                      "10px",
                    cursor:
                      "pointer",
                    color:
                      "black",  
                  }}
                >
                  ✏ Rename
                </div>

                <div
                  onClick={() => {

                    deleteSession(
                      session.id
                    );

                    setMenuOpen(
                      null
                    );
                  }}
                  style={{
                    padding:
                      "10px",
                    cursor:
                      "pointer",
                    color:
                      "red",
                  }}
                >
                  🗑 Delete
                </div>

              </div>
            )}

          </div>
        )
      )}

    </div>
  );
}

export default Sidebar;