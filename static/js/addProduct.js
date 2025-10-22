import {
  getCSRFToken,
  toastAlert,
  autoFadeAlerts,
  bindImageUploader,
} from "/static/js/utils.js";

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

  // Form handling
  const form = document.getElementById("addProductForm");
  const featuredImageInput = document.getElementById("featuredImageInput");
  const featuredImageUrl = document.getElementById("featuredImageUrl");

  // Bind the featured image upload
  bindImageUploader(featuredImageInput, featuredImageUrl, "Featured Image");

  // Rebind Cloudinary upload for dynamically added image fields
  const observeImageUploads = new MutationObserver(() => {
    const imageInputs = imagesContainer.querySelectorAll(".image-upload");
    imageInputs.forEach((fileInput) => {
      const hiddenInput = fileInput
        .closest(".input-group")
        .querySelector(".image-url-field");

      // Prevent rebinding on already observed inputs
      if (!fileInput.dataset.bound) {
        bindImageUploader(fileInput, hiddenInput, "Product Image");
        fileInput.dataset.bound = "true";
      }
    });
  });

  observeImageUploads.observe(imagesContainer, {
    childList: true,
    subtree: true,
  });

  // Manually trigger for initial field
  const firstFileInput = imagesContainer.querySelector(".image-upload");
  if (firstFileInput) {
    const hidden = firstFileInput
      .closest(".input-group")
      .querySelector(".image-url-field");
    bindImageUploader(firstFileInput, hidden, "Product Image");
  }

  // =========================
  // Form Submission
  // =========================
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Ensure Cloudinary uploads are completed
    const featuredUrl = featuredImageUrl.value.trim();
    const imageUrls = Array.from(
      imagesContainer.querySelectorAll(".image-url-field")
    )
      .map((input) => input.value.trim())
      .filter((url) => url !== "");

    if (!featuredUrl) {
      alert("Please upload a featured image before submitting.");
      return;
    }

    // Gather feature fields
    const features = Array.from(document.querySelectorAll(".feature-input"))
      .map((input) => input.value.trim())
      .filter((val) => val !== "");

    // Build payload
    const payload = {
      title: document.getElementById("title").value.trim(),
      category: document.getElementById("category").value || null,
      description: document.getElementById("description").value.trim(),
      features: features,
      price: parseFloat(document.getElementById("price").value || 0),
      discount: parseFloat(document.getElementById("discount").value || 0),
      inventory_count: parseInt(
        document.getElementById("inventory_count").value || 0
      ),
      featured_image: featuredUrl,
      images: imageUrls,
      is_published: document.getElementById("isPublished").checked,
    };

    // Debug log
    console.log("Submitting product payload:", payload);

    try {
      const response = await fetch("/admin-space/products/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Product successfully created!");
        window.location.href = "/business/products/";
      } else {
        console.error("Error response:", data);
        alert(
          `Error creating product: ${data.message || "Something went wrong"}`
        );
      }
    } catch (err) {
      console.error("Request failed:", err);
      alert("An error occurred while submitting the form.");
    }
  });

  // Page end
});
