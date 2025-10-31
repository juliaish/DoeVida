const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

function showToast(message, type="error") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.classList.add("toast");
    if (type === "success") toast.style.backgroundColor = "#4CAF50";
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 4000);
}

document.addEventListener("DOMContentLoaded", () => {
    const messages = JSON.parse(document.getElementById("flash-messages").textContent || "[]");
    messages.forEach(([category, message]) => showToast(message, category));
});
