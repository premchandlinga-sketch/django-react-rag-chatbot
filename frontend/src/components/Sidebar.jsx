import { useEffect, useState } from "react";
import api from "../services/api";

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

  const [search, setSearch] =
    useState("");

  const [expandedSession, setExpandedSession] =
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
            title: "New Chat",
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

  const toggleSession =
    (sessionId) => {

      if (
        expandedSession ===
        sessionId
      ) {

        setExpandedSession(
          null
        );

      } else {

        setExpandedSession(
          sessionId
        );

        loadMessages(
          sessionId
        );

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

          setExpandedSession(
            null
          );

        }

      } catch (error) {

        console.error(error);

      }

    };

  const filteredSessions =
    sessions.filter(
      (session) =>
        session.title
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
    );

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

      <input
        type="text"
        placeholder="Search chats..."
        value={search}
        onChange={(e) =>
          setSearch(
            e.target.value
          )
        }
        className="search-input"
      />

      <hr />

      {filteredSessions.map(
        (session) => (

          <div
            key={session.id}
            className={`session-card ${
              selectedSessionId ===
              session.id
                ? "active-session"
                : ""
            }`}
          >

            <div
              className="session-header"
            >

              <span
                className="session-title"
                onClick={() =>
                  toggleSession(
                    session.id
                  )
                }
              >

                {expandedSession ===
                session.id
                  ? "▼ "
                  : "▶ "}

                {session.title}

              </span>

              <button
                className="menu-btn"
                onClick={(e) => {

                  e.stopPropagation();

                  setMenuOpen(
                    menuOpen ===
                    session.id
                      ? null
                      : session.id
                  );

                }}
              >
                ⋮
              </button>

              {menuOpen ===
                session.id && (

                <div
                  className="menu-dropdown"
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
                  >
                    ✏ Rename
                  </div>

                  <div
                    className="delete-option"
                    onClick={() => {

                      deleteSession(
                        session.id
                      );

                      setMenuOpen(
                        null
                      );

                    }}
                  >
                    🗑 Delete
                  </div>

                </div>

              )}

            </div>
                        {expandedSession ===
              session.id && (

              <div
                className="documents-container"
              >

                {session.documents &&
                session.documents.length >
                  0 ? (

                  session.documents.map(
                    (document) => (

                      <div
                        key={document.id}
                        className="document-item"
                      >

                        <span
                          className="document-name"
                          title={
                            document.file_name
                          }
                        >
                          📄{" "}
                          {
                            document.file_name
                          }
                        </span>

                        <button
                          className="document-delete-btn"
                          onClick={async (
                            e
                          ) => {

                            e.stopPropagation();

                            const confirmed =
                              window.confirm(
                                "Delete this document?"
                              );

                            if (
                              !confirmed
                            ) {

                              return;

                            }

                            try {

                              await api.delete(
                                `documents/${document.id}/`
                              );

                              await fetchSessions();

                            } catch (
                              error
                            ) {

                              console.error(
                                error
                              );

                            }

                          }}
                        >
                          🗑
                        </button>

                      </div>

                    )

                  )

                ) : (

                  <div
                    className="no-documents"
                  >
                    No documents uploaded
                  </div>

                )}

              </div>

            )}

          </div>

        )

      )}

    </div>

  );

}

export default Sidebar;