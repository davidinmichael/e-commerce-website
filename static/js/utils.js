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


const cloudName = "dskpdlvxu";
const uploadPreset = "unsigned_dbookdraft";

/**
 * Binds an input file element to upload to Cloudinary
 * @param {string} fileInputId - ID of the <input type="file">
 * @param {string} hiddenInputId - ID of the hidden input where the uploaded URL should go
 * @param {string} label - Label for logs / error messages (e.g. "Logo", "Signature")
 */
export function bindImageUploader(fileInputId, hiddenInputId, label) {
  const input = document.getElementById(fileInputId);
  if (!input) return;

  input.addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", uploadPreset);

    try {
      const response = await fetch(
        `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (data.secure_url) {
        document.getElementById(hiddenInputId).value = data.secure_url;
        console.log(`${label} uploaded:`, data.secure_url);
      } else {
        console.error(`${label} upload failed:`, data);
        alert(`${label} upload failed. Try again.`);
      }
    } catch (error) {
      console.error(`Error uploading ${label}:`, error);
      alert(`An error occurred while uploading the ${label}.`);
    }
  });
}


