import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          text: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          text: "Unable to connect to the Enterprise RAG backend. Please make sure the FastAPI server is running.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      askQuestion();
    }
  };

  // Open the PDF at the relevant page
  const openPdf = (source) => {
    const pdfUrl =
      `http://127.0.0.1:8000/documents/${encodeURIComponent(
        source.source
      )}#page=${source.page}`;

    window.open(pdfUrl, "_blank");
  };

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div>
          <h1>Enterprise Multi-Agent RAG</h1>

          <p>
            AI-powered enterprise document assistant
          </p>
        </div>

        <div className="status">

          <span className="status-dot"></span>

          System Online

        </div>

      </header>


      {/* CHAT */}

      <main className="chat-container">

        {messages.length === 0 && (

          <div className="welcome">

            <div className="robot">
              🤖
            </div>

            <h2>
              How can I help you?
            </h2>

            <p>
              Ask questions about the enterprise documents and policies.
            </p>


            <div className="examples">

              <button
                onClick={() =>
                  setQuestion(
                    "What is the remote work policy?"
                  )
                }
              >
                What is the remote work policy?
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "Summarize the remote work policy."
                  )
                }
              >
                Summarize the remote work policy
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "Which document contains the remote work policy?"
                  )
                }
              >
                Which document contains the remote work policy?
              </button>

            </div>

          </div>

        )}


        {/* MESSAGES */}

        <div className="messages">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`message-row ${message.type}`}
            >

              <div className="avatar">

                {message.type === "user"
                  ? "👤"
                  : "🤖"}

              </div>


              <div className="message">

                <div className="message-label">

                  {message.type === "user"
                    ? "You"
                    : "AI Assistant"}

                </div>


                <div className="message-text">

                  {message.text}

                </div>


                {/* SOURCES */}

                {message.type === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (

                    <div className="sources">

                      <div className="sources-title">
                        📚 Sources
                      </div>


                      {message.sources.map(
                        (source, sourceIndex) => (

                          <button
                            className="source-item"
                            key={sourceIndex}
                            onClick={() =>
                              openPdf(source)
                            }
                            title={`Open ${source.source} - Page ${source.page}`}
                          >

                            <span className="source-icon">
                              📄
                            </span>


                            <span className="source-name">
                              {source.source}
                            </span>


                            <span className="source-page">
                              Page {source.page}
                            </span>


                            <span className="source-open">
                              ↗
                            </span>

                          </button>

                        )
                      )}

                    </div>

                  )}

              </div>

            </div>

          ))}


          {/* LOADING */}

          {loading && (

            <div className="message-row assistant">

              <div className="avatar">
                🤖
              </div>


              <div className="message">

                <div className="message-label">
                  AI Assistant
                </div>


                <div className="typing">

                  <span></span>
                  <span></span>
                  <span></span>

                  Thinking...

                </div>

              </div>

            </div>

          )}

        </div>

      </main>


      {/* INPUT */}

      <div className="input-area">

        <div className="input-box">

          <input
            type="text"
            placeholder="Ask something about your enterprise documents..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
          />


          <button
            onClick={askQuestion}
            disabled={
              loading ||
              !question.trim()
            }
          >

            {loading
              ? "..."
              : "Send"}

          </button>

        </div>


        <p className="footer-text">

          Enterprise Multi-Agent RAG • Powered by Llama 3.2 + ChromaDB

        </p>

      </div>

    </div>
  );
}

export default App;