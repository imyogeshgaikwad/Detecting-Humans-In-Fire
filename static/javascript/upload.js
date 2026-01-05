import { showNotification } from "./notification.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const fileInput = document.getElementById("fileInput");
  const uploadSubtext = document.querySelector(".upload-subtext");

  // -----------------------------
  // Show selected file name
  // -----------------------------
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      uploadSubtext.textContent = fileInput.files[0].name;
    } else {
      uploadSubtext.textContent = "or click to browse files";
    }
  });

  // -----------------------------
  // Handle form submission
  // -----------------------------
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      alert("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    const button = form.querySelector("button");
    try {
      // Show loading state
      button.disabled = true;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing...`;

      // Send image to backend Flask route
      const response = await fetch("/detect", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Server error during analysis");

      const result = await response.json();

      // Show the prediction result using your existing notification
      showNotification(result);

    } catch (error) {
      console.error(error);
      alert("Error analyzing the image. Check the console for details.");
    } finally {
      // Reset button state
      button.disabled = false;
      button.innerHTML = `<i class="fas fa-search"></i> Analyze Image`;
    }
  });
});
