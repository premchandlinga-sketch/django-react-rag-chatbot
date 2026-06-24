import { useEffect, useRef } from "react";
import api from "../services/api";

import "../styles/chatwindow.css";

function ChatWindow({
  messages,
  loading,
  selectedSessionId,
  setMessages,
}) {

  const bottomRef = useRef(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);

  const refreshMessages =
    async () => {

      const response =
        await api.get(
          `sessions/${selectedSessionId}/messages/`
        );

      setMessages(
        response.data
      );
    };

  const deleteMessage =
    async (messageId) => {

      const confirmed =
        window.confirm(
          "Delete this message?"
        );

      if (!confirmed) {
        return;
      }

      try {

        await api.delete(
          `sessions/${selectedSessionId}/messages/${messageId}/`
        );

        await refreshMessages();

      } catch (error) {

        console.error(error);

      }
    };

  const editMessage =
    async (message) => {

      const newContent =
        prompt(
          "Edit message",
          message.content
        );

      if (
        !newContent ||
        newContent.trim() === ""
      ) {
        return;
      }

      try {

        await api.put(
          `sessions/${selectedSessionId}/messages/${message.id}/`,
          {
            content:
              newContent,
          }
        );

        await refreshMessages();

      } catch (error) {

        console.error(error);

      }
    };

  return (
    <div className="chat-window">

      {messages.map(
        (message) => (

          <div
            key={message.id}
            className={`message-row ${
              message.role === "user"
                ? "user-row"
                : "assistant-row"
            }`}
          >

            <div
              className={`message-bubble ${
                message.role === "user"
                  ? "user-bubble"
                  : "assistant-bubble"
              }`}
              style={{
                position:
                  "relative",
              }}
            >

              <div
                className="message-role"
              >
                {message.role}
              </div>

              <div>
                {message.content}
              </div>

              <div
                style={{
                  position:
                    "absolute",
                  top: "10px",
                  right: "10px",
                  display:
                    "flex",
                  gap: "8px",
                }}
              >

                {message.role ===
                  "user" && (

                  <button
                    onClick={() =>
                      editMessage(
                        message
                      )
                    }
                    style={{
                      border:
                        "none",
                      background:
                        "transparent",
                      cursor:
                        "pointer",
                      fontSize:
                        "16px",
                    }}
                  >
                    ✏
                  </button>

                )}

                <button
                  onClick={() =>
                    deleteMessage(
                      message.id
                    )
                  }
                  style={{
                    border:
                      "none",
                    background:
                      "transparent",
                    cursor:
                      "pointer",
                    fontSize:
                      "16px",
                  }}
                >
                  🗑
                </button>

              </div>

            </div>

          </div>
        )
      )}

      {loading && (

        <div className="thinking">
          🤖 Thinking...
        </div>

      )}

      <div ref={bottomRef}></div>

    </div>
  );
}

export default ChatWindow;