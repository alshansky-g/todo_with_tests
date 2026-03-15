const initialize = (inputSelector, errorSelector) => {
  const textInput = document.querySelector(inputSelector);
  textInput.oninput = () => {
    const errorMsg = document.querySelector(errorSelector);
    errorMsg.style.display = "none";
    textInput.classList.remove("is-invalid");
  };
};