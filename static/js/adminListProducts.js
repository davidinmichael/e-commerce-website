import { getCSRFToken, toastAlert, autoFadeAlerts } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const productContainer = document.getElementById("adminProductList");
  const searchProductKeyword = document.getElementById("searchProductKeyword");
  const searchProductCategory = document.getElementById(
    "searchProductCategory"
  );
  const searchProductStatus = document.getElementById("searchProductStatus");
  const searchProductStock = document.getElementById("searchProductStock");

  let allProducts = [];
  let currentPage = 1;
  const perPage = 9;

  // Fetch all products
  async function fetchProducts() {
    try {
      const res = await fetch("/business/admin-products/");
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
      const productHTML = `
		   <div class="col-12 col-md-6 col-lg-4 col-xl-3">
      <div class="card shadow-sm h-100">
        <img
          src="${product.featured_image}"
          class="card-img-top"
          alt="${product.title}"
          style="
            height: 150px;
            object-fit: cover;
            border-bottom: 1px solid #eee;
          "
        />
        <div class="card-body">
          <h6 class="card-title text-truncate mb-2">${product.title}</h6>
          <p class="text-muted small mb-1">₦${price}</p>
          <p class="text-success small mb-1">Discount: ${product.discount}%</p>
          <p class="text-success small mb-1">Stock: ${product.inventory_count}</p>
          <p class="small text-secondary mb-2">Category: ${product.category.name}</p>
          <div class="d-flex">
            <a href="/admin-space/edit-product/${product.slug}/" class="mx-2 btn btn-sm btn-outline-primary"
              ><i class="fa-solid fa-pen-to-square"></i
            ></a>
            <a href="#" class="mx-2 btn btn-sm btn-outline-secondary"
              ><i class="fa-solid fa-eye-slash"></i
            ></a>
            <a href="#" class="mx-2 btn btn-sm btn-outline-danger"
              ><i class="fa-solid fa-trash"></i
            ></a>
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
    const paginationContainer = document.getElementById(
      "adminPaginationContainer"
    );
    if (!paginationContainer) return;

    const totalPages = Math.ceil(totalItems / perPage);
    let buttons = "";

    if (totalPages > 1) {
      buttons += `
        <button class="btn btn-outline-primary me-2" ${
          currentPage === 1 ? "disabled" : ""
        } id="adminProductPrevPage">Prev</button>
        <span>Page ${currentPage} of ${totalPages}</span>
        <button class="btn btn-outline-primary ms-2" ${
          currentPage === totalPages ? "disabled" : ""
        } id="adminProductNextPage">Next</button>
      `;
    }

    paginationContainer.innerHTML = buttons;

    if (totalPages > 1) {
      document
        .getElementById("adminProductPrevPage")
        ?.addEventListener("click", () => {
          if (currentPage > 1) {
            currentPage--;
            displayProducts();
          }
        });
      document
        .getElementById("adminProductNextPage")
        ?.addEventListener("click", () => {
          if (currentPage < totalPages) {
            currentPage++;
            displayProducts();
          }
        });
    }
  }

  // Search + Filter
  searchProductKeyword.addEventListener("input", () => {
    const keyword = searchProductKeyword.value.toLowerCase().trim();
    const category = searchProductCategory.value;

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

  searchProductCategory.addEventListener("change", () => {
    const keyword = searchProductKeyword.value.toLowerCase().trim();
    const category = searchProductCategory.value;

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

  // Common filter function — reuse for all filter changes
  function applyProductFilters() {
    const keyword = searchProductKeyword.value.toLowerCase().trim();
    const category = searchProductCategory.value;
    const status = searchProductStatus.value;
    const stock = searchProductStock.value;

    let filtered = allProducts;

    // Keyword filter
    if (keyword) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(keyword)
      );
    }

    // Category filter
    if (category && category !== "Category") {
      filtered = filtered.filter((p) => {
        const categoryId = p.category?.id || p.category;
        return String(categoryId) === String(category);
      });
    }

    // Status filter (Published / Draft)
    if (status && status !== "Status") {
      const isPublished = status === "true";
      filtered = filtered.filter((p) => p.is_published === isPublished);
    }

    // Stock filter (In Stock / Out of Stock)
    if (stock && stock !== "Stock Status") {
      const inStock = stock === "true";
      filtered = filtered.filter((p) =>
        inStock ? p.inventory_count > 0 : p.inventory_count <= 0
      );
    }

    currentPage = 1;
    displayProducts(filtered);
  }

  // Apply filters on all relevant events
  searchProductKeyword.addEventListener("input", applyProductFilters);
  searchProductCategory.addEventListener("change", applyProductFilters);
  searchProductStatus.addEventListener("change", applyProductFilters);
  searchProductStock.addEventListener("change", applyProductFilters);

  fetchProducts();
  // Page ends
});
