import { getCSRFToken, toastAlert, autoFadeAlerts } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const cartKey = "cart";
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  // cart.js

  function clearCart() {
    localStorage.removeItem(cartKey);
    cart = [];
    renderCart();
  }


  const cartContainer = document.getElementById("cartItems");

  // Utility: format currency
  const formatCurrency = (amount) => {
    return "₦" + Number(amount).toLocaleString();
  };

  // Render the cart items
  function renderCart() {
    if (!cartContainer) return;
    cartContainer.innerHTML = ""; // Clear before re-rendering

    if (cart.length === 0) {
      cartContainer.innerHTML = `
      <div class="text-center">
        <p>Your cart is empty.</p>
        <a href="/products/" class="btn btn-primary">Continue Shopping</a>
      </div>
    `;
      return;
    }

    let totalAmount = 0;

    cart.forEach((item, index) => {
      const itemTotal = item.price * item.quantity;
      totalAmount += itemTotal;

      const itemHTML = `
      <div class="col-12 mb-3">
        <div class="card p-3 d-flex flex-row align-items-center justify-content-between cart-card">
          <div class="d-flex align-items-center">
            <img src="${item.featured_image}" alt="${
        item.name
      }" class="me-3" style="width:80px; height:80px; object-fit:cover; border-radius:8px;">
            <div>
              <h5 class="mb-1">${item.title}</h5>
              <p class="mb-0 text-muted">${formatCurrency(item.price)}</p>
            </div>
          </div>

          <div class="d-flex align-items-center">
            <button class="btn btn-sm btn-outline-secondary me-2 decrease" data-index="${index}">-</button>
            <span class="fw-bold">${item.quantity}</span>
            <button class="btn btn-sm btn-outline-secondary ms-2 increase" data-index="${index}">+</button>
          </div>

          <div class="price-section">
            <p class="fw-bold mb-0">${formatCurrency(itemTotal)}</p>
            <button class="btn btn-sm btn-outline-danger mt-2 remove" data-index="${index}">
              Remove
            </button>
          </div>
        </div>
      </div>
    `;

      cartContainer.insertAdjacentHTML("beforeend", itemHTML);
    });

    // Add total summary at the bottom
    const summaryHTML = `
    <div class="col-12 mt-4">
      <div class="card p-3">
        <h4>Total: <span class="fw-bold">${formatCurrency(
          totalAmount
        )}</span></h4>
        <button class="btn btn-success mt-3" id="checkoutBtn">Proceed to Checkout</button>
      </div>
    </div>
  `;

    cartContainer.insertAdjacentHTML("beforeend", summaryHTML);

    attachEventListeners();
  }

  // Handle increment/decrement/remove
  function attachEventListeners() {
    const increaseBtns = document.querySelectorAll(".increase");
    const decreaseBtns = document.querySelectorAll(".decrease");
    const removeBtns = document.querySelectorAll(".remove");

    increaseBtns.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const index = e.target.dataset.index;
        cart[index].quantity += 1;
        saveAndRender();
      })
    );

    decreaseBtns.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const index = e.target.dataset.index;
        if (cart[index].quantity > 1) {
          cart[index].quantity -= 1;
        } else {
          cart.splice(index, 1);
        }
        saveAndRender();
      })
    );

    removeBtns.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const index = e.target.dataset.index;
        cart.splice(index, 1);
        saveAndRender();
      })
    );
  }

  // Save cart to localStorage and re-render
  function saveAndRender() {
    localStorage.setItem(cartKey, JSON.stringify(cart));
    renderCart();
  }

  // Initialize
  renderCart();

  const checkoutBtn = document.getElementById("checkoutBtn");
  if (!checkoutBtn) return;

  checkoutBtn.addEventListener("click", () => {

    if (cart.length === 0) {
      toastAlert(
        "Your cart is empty!",
        "toast-warning",
        "fa-circle-exclamation"
      );
      return;
    }

    if (window.APP_CONFIG.ENABLE_ONLINE_PAYMENTS) {
      // Redirect to Paystack checkout page
      window.location.href = "/";
    } else {
      // Redirect to WhatsApp with message
      const messageLines = cart.map(
        (item, index) =>
          `${index + 1}. ${item.title}\n   Price: ₦${item.price} x ${
            item.quantity
          } = ₦${(item.price * item.quantity).toLocaleString()}`
      );

      const total = cart
        .reduce((sum, item) => sum + item.price * item.quantity, 0)
        .toLocaleString();

      const message = `Hello, I'm interested in these products:\n\n${messageLines.join(
        "\n\n"
      )}\n\n*Total:* ₦${total}`;

      const encodedMessage = encodeURIComponent(message);
      const whatsappNumber = window.APP_CONFIG.WHATSAPP_NUMBER;

      window.open(
        `https://wa.me/${whatsappNumber}?text=${encodedMessage}`,
        "_blank"
      );
    }
    clearCart();
  });
});
