import { useRef, useState } from "react";
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

  const fileInputRef =
    useRef(null);

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

  const uploadPDF =
    async (event) => {

      const file =
        event.target.files[0];

      if (!file) {
        return;
      }

      if (!selectedSessionId) {

        alert(
          "Select a chat session first."
        );

        return;
      }

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      formData.append(
        "session_id",
        selectedSessionId
      );

      try {

        await api.post(
          "upload/",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );

        alert(
          "PDF uploaded successfully!"
        );

        setRefreshSidebar(
          (prev) => !prev
        );

      } catch (error) {

        console.error(error);

      }

    };

  return (

    <div
      className="message-input-container"
    >

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        style={{
          display: "none",
        }}
        onChange={uploadPDF}
      />

      <button
        onClick={() =>
          fileInputRef.current.click()
        }
        style={{
          width: "42px",
          height: "42px",
          borderRadius: "50%",
          border: "none",
          background: "#2b2b2b",
          color: "white",
          cursor: "pointer",
          fontSize: "24px",
          marginRight: "10px",
        }}
      >
        +
      </button>

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