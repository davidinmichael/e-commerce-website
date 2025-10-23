import {
  getCSRFToken,
  toastAlert,
  bindImageUploader,
  autoFadeAlerts,
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

  async function updateProduct(slug) {
    const form = document.getElementById("editProductForm");
    const imagesContainer = document.getElementById("imagesContainer");
    const featuredImageInput = document.getElementById("featuredImageInput");
    const featuredImageUrl = document.getElementById("featuredImageUrl");

    // Rebind Cloudinary upload for featured image
    bindImageUploader(featuredImageInput, featuredImageUrl, "Featured Image");

    // Observe and rebind dynamically added image fields
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

    // Initial binding for the first field
    const firstFileInput = imagesContainer.querySelector(".image-upload");
    if (firstFileInput) {
      const hidden = firstFileInput
        .closest(".input-group")
        .querySelector(".image-url-field");
      bindImageUploader(firstFileInput, hidden, "Product Image");
    }

    // Handle form submission
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Wait for Cloudinary uploads to finish
      const featuredUrl = featuredImageUrl.value.trim();
      const imageUrls = Array.from(
        imagesContainer.querySelectorAll(".image-url-field")
      )
        .map((input) => input.value.trim())
        .filter((url) => url !== "");

      // Collect feature inputs
      const features = Array.from(form.querySelectorAll(".feature-input"))
        .map((input) => input.value.trim())
        .filter((val) => val !== "");

      // Build payload
      const existingImagesElement = document.getElementById("product-images");
      const existingImages = existingImagesElement
        ? JSON.parse(existingImagesElement.textContent)
        : [];

      const payload = {
        title: form.title.value.trim(),
        category: form.category.value,
        description: form.description.value.trim(),
        features,
        price: parseFloat(form.price.value || 0),
        discount: parseFloat(form.discount.value || 0),
        inventory_count: parseInt(form.inventory_count.value || 0),
        featured_image: featuredUrl || form.featured_image.value,
        images: imageUrls.length > 0 ? imageUrls : existingImages,
        is_published: form.is_published.checked,
      };

      console.log("Submitting payload:", payload);

      try {
        const response = await fetch(`/business/admin-product/edit/${slug}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (response.ok) {
          toastAlert(
            "Product updated successfully!",
            "toast-success",
            "fa-circle-check"
          );
        } else {
          console.error(result);
          toastAlert(
            "Error updating product. Check console for details!",
            "toast-error",
            "fa-triangle-exclamation"
          );
        }
      } catch (error) {
        console.error("Error:", error);
        toastAlert(
          "Something went wrong. Try again!",
          "toast-error",
          "fa-triangle-exclamation"
        );
      }
    });
  }

  const slug = document.getElementById("editProductForm")?.dataset.slug;
  if (slug) updateProduct(slug);
  // End page
});
