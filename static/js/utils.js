export function getCSRFToken() {
  const name = "csrftoken=";
  const decodedCookies = decodeURIComponent(document.cookie).split(";");
  for (let cookie of decodedCookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name)) {
      return cookie.substring(name.length);
    }
  }
  return "";
}

export function toastAlert(msg, style, icon) {
  const toastBox = document.getElementById("toastBox"); // get fresh every time
  if (!toastBox) {
    console.warn("toastBox container not found in DOM.");
    return;
  }

  const toast = document.createElement("div");
  toast.classList.add("toast", style);
  toast.innerHTML = `
    <i class="fa-solid ${icon}"></i>
    <p>${msg}</p>
  `;

  toastBox.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

export function autoFadeAlerts() {
  setTimeout(() => {
    const alerts = document.querySelectorAll(".alert-box");
    alerts.forEach((alert) => {
      alert.style.transition = "opacity 0.5s ease-out";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    });
  }, 3000);
}
