import { getCSRFToken, toastAlert, autoFadeAlerts } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
	const featuresContainer = document.getElementById("featuresContainer");
  const imagesContainer = document.getElementById("imagesContainer");

  // =========================
  // Dynamic Feature Fields
  // =========================
  featuresContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("addFeatureBtn")) {
      e.preventDefault();

      const newIndex =
        featuresContainer.querySelectorAll(".feature-input").length;
      const wrapper = document.createElement("div");
      wrapper.classList.add("input-group", "mb-2");

      wrapper.innerHTML = `
        <input
          type="text"
          name="feature_${newIndex}"
          class="form-control feature-input"
          placeholder="Enter a feature..."
        />
        <button type="button" class="btn btn-outline-danger removeFeatureBtn">–</button>
      `;

      featuresContainer.appendChild(wrapper);
    }

    if (e.target.classList.contains("removeFeatureBtn")) {
      e.preventDefault();
      e.target.closest(".input-group").remove();
    }
  });

  // =========================
  // Dynamic Image Fields
  // =========================
  imagesContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("addImageBtn")) {
      e.preventDefault();

      const newIndex = imagesContainer.querySelectorAll(".image-upload").length;
      const wrapper = document.createElement("div");
      wrapper.classList.add("input-group", "mb-2");

      wrapper.innerHTML = `
        <input
          type="file"
          name="image_${newIndex}"
          class="form-control image-upload"
          accept="image/*"
        />
        <input type="hidden" class="image-url-field" name="image_url_${newIndex}" />
        <button type="button" class="btn btn-outline-danger removeImageBtn">–</button>
      `;

      imagesContainer.appendChild(wrapper);
    }

    if (e.target.classList.contains("removeImageBtn")) {
      e.preventDefault();
      e.target.closest(".input-group").remove();
    }
  });
	// End page
});
