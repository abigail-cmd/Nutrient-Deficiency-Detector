document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form[action='/result']");
    const overlay = document.getElementById("loadingOverlay");

    if (form && overlay) {
        form.addEventListener("submit", function () {
            overlay.classList.remove("d-none");
        });
    }
});