const API_URL = window.EMAIL_API_URL || "http://127.0.0.1:8000/process-email";

const form = document.getElementById("emailForm");
const emailTextInput = document.getElementById("emailText");
const fileInput = document.getElementById("emailFile");
const submitBtn = document.getElementById("submitBtn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const resultBox = document.getElementById("resultBox");
const categoryBadge = document.getElementById("categoryBadge");
const replyText = document.getElementById("replyText");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearFeedback();

  const emailText = emailTextInput.value.trim();
  const file = fileInput.files[0] || null;

  if (emailText && file) {
    showError("Envie apenas texto ou arquivo. Nao envie os dois juntos.");
    return;
  }

  if (!emailText && !file) {
    showError("Informe o texto do email ou selecione um arquivo .txt/.pdf.");
    return;
  }

  setLoading(true);

  try {
    const response = await sendToApi({ emailText, file });
    renderResult(response);
  } catch (error) {
    showError(error.message || "Nao foi possivel processar o email.");
  } finally {
    setLoading(false);
  }
});

async function sendToApi({ emailText, file }) {
  let fetchOptions;

  if (file) {
    const formData = new FormData();
    formData.append("file", file);
    fetchOptions = {
      method: "POST",
      body: formData,
    };
  } else {
    fetchOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email_text: emailText }),
    };
  }

  const response = await fetch(API_URL, fetchOptions);
  const payload = await parseJsonSafely(response);

  if (!response.ok) {
    const detail = payload?.detail || "Erro ao processar email.";
    throw new Error(detail);
  }

  if (!payload || !payload.category || !payload.reply) {
    throw new Error("Resposta da API em formato inesperado.");
  }

  return payload;
}

async function parseJsonSafely(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function renderResult(data) {
  categoryBadge.textContent = data.category;
  replyText.textContent = data.reply;

  categoryBadge.classList.remove("produtivo", "improdutivo");
  if (data.category === "Produtivo") {
    categoryBadge.classList.add("produtivo");
  } else {
    categoryBadge.classList.add("improdutivo");
  }

  resultBox.classList.remove("hidden");
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  loading.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function clearFeedback() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
  resultBox.classList.add("hidden");
}

