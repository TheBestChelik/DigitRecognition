document.addEventListener("DOMContentLoaded", function() {
    const modelNameInput = document.getElementById("model-name");
    const updateButton = document.getElementById("update");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    const clearButton = document.getElementById("clear");
    const retrainButton = document.getElementById("retrain");
    const errorLabel = document.getElementById("error-label");
  
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
  
    function startDrawing(e) {
      isDrawing = true;
      [lastX, lastY] = [e.offsetX, e.offsetY];
    }
  
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
  
    function stopDrawing() {
      isDrawing = false;
    }
  
    function clearCanvas() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      errorLabel.textContent = "";
    }
  
    function retrainModel() {
      $.ajax({
        url: "/update.html",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          MessageType: "StartRetrain",
          ModelName: modelNameInput.value + ".db",
        }),
        success: function(response) {
          console.log(response);
        },
        error: function(xhr, status, error) {
          console.log(error);
        }
      }).done(function() {
        console.log('Retraining Started');
      });
    }
  
    // Event listeners
    updateButton.addEventListener("click", function() {
      // Save the current canvas drawing as an image before updating the model
      const dataURL = canvas.toDataURL();
  
      $.ajax({
        url: "/update.html",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          MessageType: "Image",
          ModelName: modelNameInput.value + ".db",
          imageBase64: dataURL
        }),
        success: function(response) {
          console.log(response);
        },
        error: function(xhr, status, error) {
          console.log(error);
        }
      }).done(function() {
        console.log('Image Saved');
      });
    });
  
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);
  
    clearButton.addEventListener("click", clearCanvas);
    retrainButton.addEventListener("click", retrainModel);
  });
  
