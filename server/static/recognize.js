// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    // Get canvas element and its context
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
  
    // Set initial values
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
  
    // Event listeners for drawing
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);
  
    // Function to start drawing
    function startDrawing(e) {
      isDrawing = true;
      [lastX, lastY] = [e.offsetX, e.offsetY];
    }
  
    // Function to draw
    function draw(e) {
        if (!isDrawing) return;

        context.beginPath();
        context.moveTo(lastX, lastY);
        context.lineTo(e.offsetX, e.offsetY);
        context.lineWidth = 20; // Constant brush size of 20px
        context.strokeStyle = "#000000"; // Constant brush color
        context.lineCap = "round";
        context.lineJoin = "round";
        context.stroke();

        [lastX, lastY] = [e.offsetX, e.offsetY];
    }
  
    // Function to stop drawing
    function stopDrawing() {
      isDrawing = false;
    }
  
    // Clear canvas
    const clearButton = document.getElementById("clear");
    clearButton.addEventListener("click", function() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      document.getElementById("recognize-digit").textContent = "Result: ";
    });
  
    // Recognize digit
    const recognizeButton = document.getElementById("save");
    recognizeButton.addEventListener("click", function() {
      const imageData = canvas.toDataURL("image/png");
      const model = document.getElementById("model").value;
  
      // Send the image data and model selection to the server for recognition
      // Implement your server-side logic to process the image and return the result
      // You can use AJAX, fetch, or any other method to make the server request
      // Draw the original canvas image onto the temporary canvas with the desired size
      tempContext.drawImage(canvas, 0, 0, 28, 28);
      var dataURL = tempCanvas.toDataURL();
      // Replace the URL with your server endpoint
      fetch("/recognize", {
        method: "POST",
        body: JSON.stringify({ imageBase64: dataURL }),
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(response => response.json())
      .then(function(responseObject) {
        resolve(responseObject.digit);
      })
      .catch(function(error) {
        reject(error);
      });
    });
  });
  
