function moveToNext(currentInput, nextInputId) {
  // Allow only digits (0-9)
  currentInput.value = currentInput.value.replace(/[^0-9]/g, "");

  // If the input length is more than one, take the last entered character
  if (currentInput.value.length > 1) {
    currentInput.value = currentInput.value.slice(-1); // Keep the last entered character
  }

  // Move to the next input if a number is entered
  if (currentInput.value.length === 1) {
    const nextInput = document.getElementById(nextInputId);
    nextInput.focus();
  }
}

function stopInput(currentInput) {
  // Allow only digits (0-9)
  currentInput.value = currentInput.value.replace(/[^0-9]/g, "");

  // If the input length is more than one, take the last entered character
  if (currentInput.value.length > 1) {
    currentInput.value = currentInput.value.slice(-1); // Keep the last entered character
  }
  // Optionally, blur the last input to stop focus
  currentInput.blur();
}
