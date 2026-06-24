import { useState } from "react";
import api from "../services/api";

import "../styles/messageinput.css";

function MessageInput({
  selectedSessionId,
  setMessages,
  setLoading,
  setRefreshSidebar,
}) {

  const [question, setQuestion] =
    useState("");

  const sendMessage = async () => {

    if (!selectedSessionId) {

      alert(
        "Select a chat session"
      );

      return;
    }

    if (!question.trim()) {
      return;
    }

    try {

      setLoading(true);

      await api.post(
        "chat/",
        {
          session_id:
            selectedSessionId,

          question: question,
        }
      );

      setRefreshSidebar(
        (prev) => !prev
      );

      const response =
        await api.get(
          `sessions/${selectedSessionId}/messages/`
        );

      setMessages(
        response.data
      );

      setQuestion("");

      setLoading(false);

    } catch (error) {

      console.error(error);

      setLoading(false);
    }
  };

  return (
    <div className="message-input-container">

      <input
        type="text"
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        onKeyDown={(e) => {

          if (
            e.key === "Enter"
          ) {

            sendMessage();
          }
        }}
        placeholder="Type your message..."
        className="message-input"
      />

      <button
        onClick={sendMessage}
        className="send-btn"
      >
        Send
      </button>

    </div>
  );
}

export default MessageInput;