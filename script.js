const form = document.getElementById("feedback-form");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const messageInput = document.getElementById("message");
const submitButton = document.getElementById("submit-btn");
const statusMessage = document.getElementById("status-message");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateForm() {
  const isNameValid = nameInput.value.trim().length >= 2;
  const isEmailValid = emailRegex.test(emailInput.value.trim());
  const isMessageValid = messageInput.value.trim().length >= 5;

  submitButton.disabled = !(isNameValid && isEmailValid && isMessageValid);
}

form.addEventListener("input", () => {
  statusMessage.textContent = "";
  validateForm();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (submitButton.disabled) {
    return;
  }

  const author = nameInput.value.trim();
  statusMessage.textContent = `Thanks, ${author}! Form submitted.`;
  form.reset();
  submitButton.disabled = true;
});

validateForm();
