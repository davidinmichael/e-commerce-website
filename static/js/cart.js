import { toastAlert } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const cartKey = "cart";
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("add-to-cart-btn")) {
      const productData = e.target.dataset.product;

      if (!productData) {
        console.warn("No product data found on button.");
        return;
      }

      const product = JSON.parse(productData);

      // Check if already in cart
      const existing = cart.find((item) => item.id === product.id);
      if (existing) {
        toastAlert(
          `${product.title} is already in your cart.`,
          "toast-warning",
          "fa-circle-exclamation"
        );
        console.warn(`${product.title} is already in your cart.`);
        return;
      }

      // Add to cart
      cart.push({
        id: product.id,
        title: product.title,
        price: parseFloat(product.price),
        discount: parseFloat(product.discount),
        featured_image: product.featured_image,
        slug: product.slug,
        quantity: 1,
      });

      // Save to localStorage
      localStorage.setItem("cart", JSON.stringify(cart));

      toastAlert(
        `${product.title} added to cart.`,
        "toast-success",
        "fa-circle-check"
      );

      console.log("Cart:", cart);
    }
  });
});
