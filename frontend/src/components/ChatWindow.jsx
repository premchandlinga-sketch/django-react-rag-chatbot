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
                position: "relative",
              }}
            >

              <div
                className="message-role"
              >
                {message.role}
              </div>

              <div>

                {message.content}

                {message.role ===
                  "assistant" &&
                  message.sources &&
                  message.sources.length >
                    0 && (

                  <div
                    style={{
                      marginTop:
                        "15px",
                      paddingTop:
                        "10px",
                      borderTop:
                        "1px solid #444",
                    }}
                  >

                    <div
                      style={{
                        fontWeight:
                          "bold",
                        marginBottom:
                          "8px",
                        color:
                          "#8ab4f8",
                      }}
                    >
                      📚 Sources
                    </div>

                    {message.sources.map(
                      (
                        source,
                        index
                      ) => (

                        <div
                          key={index}
                          style={{
                            fontSize:
                              "13px",
                            color:
                              "#cccccc",
                            marginBottom:
                              "6px",
                          }}
                        >
                          📄{" "}
                          {source.file}
                          {" — "}
                          Page{" "}
                          {source.page}
                        </div>

                      )
                    )}

                  </div>

                )}

              </div>

              <button
                onClick={() =>
                  deleteMessage(
                    message.id
                  )
                }
                style={{
                  position:
                    "absolute",
                  top: "10px",
                  right: "10px",
                  border: "none",
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