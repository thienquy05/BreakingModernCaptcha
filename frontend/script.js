const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const loadingDiv = document.getElementById("loading");
const resultText = document.getElementById("resultText");
const targetObjectInput = document.getElementById("targetObject");
const imagePreview = document.getElementById("imagePreview");

uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  const targetObject = targetObjectInput.value.trim();

  if (!file) {
    alert("Please select an image!");
    return;
  }

  if (!targetObject) {
    alert("Please enter a target object!");
    return;
  }

  resultText.textContent = "";
  loadingDiv.style.display = "block";
  imagePreview.style.display = "none";

  const formData = new FormData();
  formData.append("image", file);
  formData.append("target", targetObject);

  // Display preview
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded image" />`;
  };
  reader.readAsDataURL(file);

  try {
    const response = await fetch("http://127.0.0.1:9000/predict_captcha", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    loadingDiv.style.display = "none";
    imagePreview.style.display = "block";

    if (data.Error) {
      resultText.style.color = "red";
      resultText.textContent = `Error: ${data.Error}`;
      return;
    }

    const positions = data.matched_positions.map(pos => pos + 1).join(", ");
    if (data.match_found) {
      resultText.style.color = "green";
      resultText.textContent = `Found: ${data.matched_label} at ${positions}`
    } else {
      resultText.style.color = "red";
      resultText.textContent = `Target object not found.`;
    }

  } catch (err) {
    loadingDiv.style.display = "none";
    resultText.style.color = "red";
    resultText.textContent = `Request failed: ${err}`;
  }
});
