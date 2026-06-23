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

      try {

        const sessionsResponse =
          await api.get(
            "sessions/"
          );

        const currentSession =
          sessionsResponse.data.find(
            (session) =>
              session.id ===
              selectedSessionId
          );

        if (
          currentSession &&
          currentSession.title ===
            "New Chat"
        ) {

          await api.put(
            `sessions/${selectedSessionId}/`,
            {
              title:
                question.length > 40
                  ? question.substring(
                      0,
                      40
                    ) + "..."
                  : question,
            }
          );

          setRefreshSidebar(
            (prev) => !prev
          );
        }

      } catch (error) {

        console.error(
          "Session title update error:",
          error
        );

      }

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