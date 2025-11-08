// static/javascript/train.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const fileInput = document.getElementById("fileInput");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      alert("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      // Show loading state
      const button = form.querySelector("button");
      button.disabled = true;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing...`;

      // Send image to backend Flask route
      const response = await fetch("/fire-model", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Server error during analysis");

      const result = await response.json();

      // Show the prediction result
      alert(`Result: ${result.fire_detected}\nConfidence: ${result.confidence}%`);
    } catch (error) {
      console.error(error);
      alert("Error analyzing the image. Check the console for details.");
    } finally {
      const button = form.querySelector("button");
      button.disabled = false;
      button.innerHTML = `<i class="fas fa-search"></i> Analyze Image`;
    }
  });
});
