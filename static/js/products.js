import { getCSRFToken, toastAlert, autoFadeAlerts } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const productContainer = document.getElementById("productList");
  const searchBtn = document.getElementById("searchBtn");
  const searchKeyword = document.getElementById("searchKeyword");
  const searchCategory = document.getElementById("searchCategory");

  let allProducts = [];
  let currentPage = 1;
  const perPage = 9;

  // Fetch all products
  async function fetchProducts() {
    try {
      const res = await fetch("/business/products/");
      if (!res.ok) throw new Error("Failed to fetch products");
      const data = await res.json();
      allProducts = data;
      displayProducts();
    } catch (error) {
      console.error(error);
      toastAlert("error", "Error loading products");
    }
  }

  // Display products (based on pagination)
  function displayProducts(products = allProducts) {
    productContainer.innerHTML = "";

    const start = (currentPage - 1) * perPage;
    const end = start + perPage;
    const paginated = products.slice(start, end);

    if (paginated.length === 0) {
      productContainer.innerHTML = `<p class="text-center">No products found.</p>`;
      return;
    }

    paginated.forEach((product) => {
      const price = Number(product.price).toLocaleString();
      const images = Array.isArray(product.images) ? product.images : [];
      const imgUrl = images.length > 0 ? images[0] : "/static/img/default.png";

      const productHTML = `
  <div class="col-lg-4 col-md-6 mb-4">
    <div class="card border-0 shadow-sm d-flex flex-column h-100">
      <div class="position-relative overflow-hidden">
        <img src="${imgUrl}" class="card-img-top" alt="${product.title}" />
      </div>

      <div class="card-body d-flex flex-column justify-content-between p-4">
        <div>
          <h5 class="card-title mb-2">${product.title}</h5>
          <p class="text-primary fw-bold mb-3">₦${price}</p>
        </div>

        <div class="d-flex gap-2 align-items-stretch mt-3">
          <a
            href="/product/${product.slug}/"
            class="btn btn-outline-dark d-flex align-items-center justify-content-center flex-fill view-details-btn"
            role="button"
          >
            View Details
          </a>

          <button
            class="btn btn-dark d-flex align-items-center justify-content-center flex-fill add-to-cart-btn"
            data-id="${product.id}"
            type="button"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  </div>
`;

      productContainer.insertAdjacentHTML("beforeend", productHTML);
    });

    setupPagination(products.length);
  }

  // Pagination
  function setupPagination(totalItems) {
    const paginationContainer = document.getElementById("paginationContainer");
    if (!paginationContainer) return;

    const totalPages = Math.ceil(totalItems / perPage);
    let buttons = "";

    if (totalPages > 1) {
      buttons += `
        <button class="btn btn-outline-primary me-2" ${
          currentPage === 1 ? "disabled" : ""
        } id="prevPage">Prev</button>
        <span>Page ${currentPage} of ${totalPages}</span>
        <button class="btn btn-outline-primary ms-2" ${
          currentPage === totalPages ? "disabled" : ""
        } id="nextPage">Next</button>
      `;
    }

    paginationContainer.innerHTML = buttons;

    if (totalPages > 1) {
      document.getElementById("prevPage")?.addEventListener("click", () => {
        if (currentPage > 1) {
          currentPage--;
          displayProducts();
        }
      });
      document.getElementById("nextPage")?.addEventListener("click", () => {
        if (currentPage < totalPages) {
          currentPage++;
          displayProducts();
        }
      });
    }
  }

  // Search + Filter
  searchKeyword.addEventListener("input", () => {
    const keyword = searchKeyword.value.toLowerCase().trim();
    const category = searchCategory.value;

    let filtered = allProducts;

    if (keyword) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(keyword)
      );
    }

    if (category && category !== "Category") {
      filtered = filtered.filter(
        (p) => String(p.category) === String(category)
      );
    }

    currentPage = 1;
    displayProducts(filtered);
  });

  searchCategory.addEventListener("change", () => {
    const keyword = searchKeyword.value.toLowerCase().trim();
    const category = searchCategory.value;

    let filtered = allProducts;

    if (keyword) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(keyword)
      );
    }

    if (category && category !== "Category") {
      filtered = filtered.filter((p) => {
        const categoryId = p.category?.id || p.category;
        return String(categoryId) === String(category);
      });
    }

    currentPage = 1;
    displayProducts(filtered);
  });

  // Add to Cart (placeholder logic)
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("add-to-cart-btn")) {
      const id = e.target.dataset.id;
      toastAlert("success", `Product ${id} added to cart (soon...)`);
    }
  });

  // Initialize
  fetchProducts();
  autoFadeAlerts();
});
