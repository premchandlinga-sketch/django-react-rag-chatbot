import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";

import "./styles/app.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshSidebar, setRefreshSidebar] =
  useState(false);

  return (
    <div className="app-container">
      <div className="sidebar-container">
        <Sidebar
          setMessages={setMessages}
          setSelectedSessionId={setSelectedSessionId}
          selectedSessionId={selectedSessionId}
          refreshSidebar={refreshSidebar}
          setRefreshSidebar={setRefreshSidebar}
        />
      </div>

      <div className="chat-container">
        <ChatWindow
          messages={messages}
          loading={loading}
        />

        <MessageInput
          selectedSessionId={selectedSessionId}
          setMessages={setMessages}
          setLoading={setLoading}
          setRefreshSidebar={setRefreshSidebar}
        />
      </div>
    </div>
  );
}

export default App;