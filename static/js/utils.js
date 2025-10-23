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
  toast.classList.add("app-toast", style);
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
const uploadPreset = "e_commerce_website";

/**
 * Bind an <input type="file"> to auto-upload to Cloudinary.
 * Automatically updates a hidden field with the uploaded image URL.
 *
 * @param {HTMLInputElement} fileInput - The visible <input type="file">
 * @param {HTMLInputElement} hiddenInput - The hidden <input> for the image URL
 * @param {string} label - Descriptive label for error messages (e.g., "Featured Image")
 */
export function bindImageUploader(fileInput, hiddenInput, label = "Image") {
  if (!fileInput) return;

  fileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Restrict file type
    if (!file.type.startsWith("image/")) {
      alert(`${label} must be an image file.`);
      fileInput.value = "";
      return;
    }

    // Restrict file size (5MB max)
    const maxSizeMB = 5;
    if (file.size > maxSizeMB * 1024 * 1024) {
      alert(`${label} is too large. Maximum size is ${maxSizeMB}MB.`);
      fileInput.value = "";
      return;
    }

    // Display loading indicator (optional)
    const originalBtnText = fileInput.nextElementSibling?.innerText;
    fileInput.disabled = true;
    if (fileInput.closest(".input-group")) {
      fileInput.closest(".input-group").classList.add("opacity-50");
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", uploadPreset);

    try {
      const response = await fetch(
        `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
        { method: "POST", body: formData }
      );

      const data = await response.json();

      if (data.secure_url) {
        hiddenInput.value = data.secure_url;
        console.log(`${label} uploaded:`, data.secure_url);
      } else {
        console.error(`${label} upload failed:`, data);
        alert(`${label} upload failed. Try again.`);
      }
    } catch (error) {
      console.error(`Error uploading ${label}:`, error);
      alert(`An error occurred while uploading the ${label}.`);
    } finally {
      fileInput.disabled = false;
      if (fileInput.closest(".input-group")) {
        fileInput.closest(".input-group").classList.remove("opacity-50");
      }
      if (originalBtnText) {
        fileInput.nextElementSibling.innerText = originalBtnText;
      }
    }
  });
}
