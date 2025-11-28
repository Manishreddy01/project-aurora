const fileInput = document.getElementById("fileInput");
const questionInput = document.getElementById("questionInput");
const submitBtn = document.getElementById("submitBtn");
const loadingText = document.getElementById("loadingText");
const responseBox = document.getElementById("responseBox");

const BACKEND_URL = "http://127.0.0.1:8000"; // adjust if running elsewhere

function generateConversationId() {
  return Math.floor(Math.random() * 1000000).toString();
}

submitBtn.onclick = async () => {
  const question = questionInput.value.trim();
  const files = fileInput.files;
  const conversationId = generateConversationId();

  loadingText.style.display = "block";
  responseBox.textContent = "";

  try {
    // If files selected → upload first
    if (files.length > 0) {
      const formData = new FormData();
      for (const file of files) {
        formData.append("files", file);
      }
      formData.append("conversationId", conversationId);

      const uploadResp = await fetch(`${BACKEND_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!uploadResp.ok) throw new Error("Upload failed.");
    }

    // Then send the question to /query
    if (question) {
      const queryResp = await fetch(`${BACKEND_URL}/query/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          conversationId,
        }),
      });

      const data = await queryResp.json();

      if (!queryResp.ok) throw new Error(data.detail || "Query failed.");

      responseBox.textContent = `
🔹 Answer: ${data.answer}
🔹 Source Type: ${data.type}
🔹 Confidence: ${data.confidence}
🔹 Sources: ${data.sources.join(", ")}
      `.trim();
    }
  } catch (err) {
    responseBox.textContent = "❌ Error: " + err.message;
  } finally {
    loadingText.style.display = "none";
  }
};
