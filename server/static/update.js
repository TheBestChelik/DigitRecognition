document.addEventListener("DOMContentLoaded", function() {
    const modelNameSelect = document.getElementById("model");
    const SaveButton = document.getElementById("save");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    const clearButton = document.getElementById("clear");
    const retrainButton = document.getElementById("retrain");
  
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;


    fetch("/update.html/data", {
      method: "GET",
    })
      .then(function(response) {
        if (!response.ok) {
          throw new Error('Error making GET request');
        }
        return response.text();
      })
      .then(function(data) {
        // This function will be executed when the GET request is successful
        const array = JSON.parse(data);
        if(array.length == 0){
          alert("You have no editable models!\nTrain some models at first");
        }
        array.forEach((option) => {
          const newOption = document.createElement('option');
          newOption.text = option;
          newOption.value = option;
        
          // Append the new option to the select element
          modelNameSelect.appendChild(newOption);
        });
      })
      .catch(function(error) {
        // This function will be executed if the request encounters an error
        console.error(error);
      });
  
      function startDrawing(e) {
        if( e.button === 1) return;
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
      }
  
    function draw(e) {
      if (!isDrawing || e.button === 1) return;

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
  
    function stopDrawing(event) {

      isDrawing = false;
      if(event.button === 0){
        RecognizeDigit();
      }
    }
  
    function clearCanvas(){
      context.clearRect(0, 0, canvas.width, canvas.height);
      document.getElementById("digit").value = ""
    }
  
    function RecognizeDigit(){
      const model = document.getElementById("model").value;
  
      // Send the image data and model selection to the server for recognition
      // Implement your server-side logic to process the image and return the result
      // You can use AJAX, fetch, or any other method to make the server request
      // Draw the original canvas image onto the temporary canvas with the desired size
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 28;
      tempCanvas.height = 28;
      const tempContext = tempCanvas.getContext('2d');
      tempContext.drawImage(canvas, 0, 0, 28, 28);
      var dataURL = tempCanvas.toDataURL();
      // Replace the URL with your server endpoint
      fetch("/update.html", {
        method: "POST",
        body: JSON.stringify({ 
          cmd: "Recognise",
          model:  modelNameSelect.value,
          imageBase64: dataURL}),
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(response => response.json())
      .then(function(responseObject) {
        document.getElementById("digit").value = responseObject.digit;
      })
    }


    function retrainModel() {
      $.ajax({
        url: "/update.html",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          cmd: "Retrain",
          ModelName: modelNameSelect.value,
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
  
    function saveDigit(){
      const tempCanvas = document.createElement('canvas');
        tempCanvas.width = 28;
        tempCanvas.height = 28;
        const tempContext = tempCanvas.getContext('2d');

        // Draw the original canvas image onto the temporary canvas with the desired size
        tempContext.drawImage(canvas, 0, 0, 28, 28);
        const dataURL = tempCanvas.toDataURL();
      $.ajax({
        url: "/update.html",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          cmd: "SaveImage",
          ModelName: modelNameSelect.value,
          imageBase64: dataURL,
          Digit: document.getElementById("digit").value
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
    }
    // Event listeners
    SaveButton.addEventListener("click", function() {
      saveDigit();
      clearCanvas();
    });
  
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);
    canvas.addEventListener("contextmenu", function(event) {
      // Prevent the default right-click behavior (e.g., showing the context menu)
      event.preventDefault();
      
      clearCanvas()
    });
  
    clearButton.addEventListener("click", clearCanvas);
    retrainButton.addEventListener("click", retrainModel);
  });
  
