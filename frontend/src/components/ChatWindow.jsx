import { useEffect, useRef } from "react";
import "../styles/chatwindow.css";

function ChatWindow({
  messages,
  loading,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.map((message) => (
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
          >
            <div className="message-role">
              {message.role}
            </div>

            <div>
              {message.content}
            </div>
          </div>
        </div>
      ))}

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