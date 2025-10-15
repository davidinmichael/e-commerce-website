import { getCSRFToken, toastAlert, autoFadeAlerts } from "/static/js/utils.js";

document.addEventListener("DOMContentLoaded", function () {
  autoFadeAlerts();
  toastAlert(
    `Product added to cart (soon...)`,
    "toast-success",
    "fa-circle-check"
  );
});
