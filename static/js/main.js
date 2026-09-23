const toolsById = Object.fromEntries(
  JSON.parse(document.getElementById("tools-data").textContent).map((tool) => [
    tool.id,
    tool,
  ])
);

const modal = document.getElementById("modal");
const modalOpenBtn = document.getElementById("modal-open-btn");
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalCredentials = document.getElementById("modal-credentials");
const modalGuide = document.getElementById("modal-guide");

let pendingUrl = null;

document.querySelectorAll(".tool-card").forEach((card) => {
  card.addEventListener("click", () => {
    const tool = toolsById[card.dataset.toolId];
    const hasCredentials = Boolean(tool.credentials);
    const openUrl = Boolean(tool.open_url);
    const url = tool.url || "";
    const connectionGuide = tool.connection_guide || "";

    if (hasCredentials) {
      pendingUrl = openUrl ? url : null;

      document.getElementById("modal-title").textContent = tool.name;
      document.getElementById("modal-login").textContent = tool.credentials.login;
      document.getElementById("modal-password").textContent = tool.credentials.password;

      modalCredentials.classList.remove("hidden");
      modalGuide.textContent = connectionGuide;

      modalOpenBtn.classList.toggle("hidden", !openUrl);
      modal.classList.add("active");
      return;
    }

    if (connectionGuide) {
      pendingUrl = openUrl ? url : null;

      document.getElementById("modal-title").textContent = tool.name;
      modalCredentials.classList.add("hidden");
      modalGuide.textContent = connectionGuide;

      modalOpenBtn.classList.toggle("hidden", !(openUrl && url));
      modal.classList.add("active");
      return;
    }

    if (url) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  });
});

modalOpenBtn.addEventListener("click", () => {
  if (pendingUrl) {
    window.open(pendingUrl, "_blank", "noopener,noreferrer");
  }
  closeModal();
});

modalCloseBtn.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeModal();
  }
});

document.querySelectorAll(".btn-copy").forEach((button) => {
  button.addEventListener("click", () => {
    const targetId = button.dataset.copyTarget;
    const text = document.getElementById(targetId).textContent;
    navigator.clipboard.writeText(text);
  });
});

function closeModal() {
  modal.classList.remove("active");
  pendingUrl = null;
}
