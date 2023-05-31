document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    var brushSizeInput = document.getElementById("brush-size");
    var brushColorInput = document.getElementById("brush-color");
    var saveButton = document.getElementById("save");
    var clearButton = document.getElementById("clear");

    // Set the initial brush size to 20px
    brushSizeInput.value = 20;

    var isDrawing = false;
    var lastX = 0;
    var lastY = 0;

    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function draw(e) {
        if (!isDrawing) return;

        context.beginPath();
        context.moveTo(lastX, lastY);
        context.lineTo(e.offsetX, e.offsetY);
        context.lineWidth = brushSizeInput.value;
        context.strokeStyle = brushColorInput.value;
        context.lineCap = "round";
        context.lineJoin = "round";
        context.stroke();

        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function recognizeDigit() {
        SendandRecognizeDigit(canvas)
        .then(function(digit) {
          alert("Your digit: " + digit);
        })
        .catch(function(error) {
          console.error("Error:", error);
        });
    }
    function SendandRecognizeDigit(canvas) {
      return new Promise(function(resolve, reject) {
        var tempCanvas = document.createElement('canvas');
        tempCanvas.width = 28;
        tempCanvas.height = 28;
        var tempContext = tempCanvas.getContext('2d');
    
        // Draw the original canvas image onto the temporary canvas with the desired size
        tempContext.drawImage(canvas, 0, 0, 28, 28);
        var dataURL = tempCanvas.toDataURL();
    
        $.ajax({
          type: "POST",
          data: {
            imageBase64: dataURL
          },
          success: function(response) {
            var responseObject = JSON.parse(response);
            resolve(responseObject.digit);
          },
          error: function(xhr, status, error) {
            reject(error);
          }
        }).done(function() {
          console.log('sent');
        });
      });
    }
      
    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Event listeners
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);

    saveButton.addEventListener("click", recognizeDigit);
    clearButton.addEventListener("click", clearCanvas);
});
