import { useState } from "react";
import api from "../services/api";

function UploadPDF({
  selectedSessionId,
}) {
  const [file, setFile] =
    useState(null);

  const uploadFile = async () => {

    if (!selectedSessionId) {

      alert(
        "Select a chat session first"
      );

      return;
    }

    if (!file) {

      alert("Select a PDF");

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

      const response =
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
        response.data.message
      );

    } catch (error) {

      console.error(error);

    }
  };

  return (
    <div
      style={{
        marginBottom: "20px",
      }}
    >
      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={uploadFile}
        style={{
          marginLeft: "10px",
        }}
      >
        Upload
      </button>
    </div>
  );
}

export default UploadPDF;