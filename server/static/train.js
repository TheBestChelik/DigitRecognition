let CurrentDigit = 0;
let DigitNumber = 0;
const MaxDigitNum = 10;
const MaxDigit = 9;

document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    const digitLabel = document.getElementById("digit-label");
    const saveButton = document.getElementById("save");
    const trainButton = document.getElementById("train");
    const clearButton = document.getElementById("clear");
    const modelNameInput = document.getElementById("model-name");
    const DigitToDraw = document.getElementById("digit-to-draw");
    const digitProgress =  document.getElementById("progress");
    const overallProgressBar = document.getElementById("overall-progress");
    const errorLabel = document.getElementById("ErrorLabel");

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function startDrawing(e) {
        if( e.button === 1) return;
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    $(document).ready(function() {
        $('#model-name').on('input', function() {
          const text = $(this).val();

          // Create the AJAX request
          $.ajax({
            url: '/train.html',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({ MessageType: "ModelName", text: text }),
            success: function(response) {
              // Request was successful, do something with the response
              switch (response.Code) {
                case 0:
                  // Model name is correct
                  saveButton.disabled = false;
                  errorLabel.textContent = "";
                  DigitToDraw.textContent = "0";
                  break;
                case 1:
                  // Name is too short
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Name is too short.";
                  DigitToDraw.textContent = "";
                  break;
                case 2:
                  // Name is already taken
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Name is already taken.";
                  DigitToDraw.textContent = "";
                  break;
                case 3:
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Spaces are not allowed.";
                  DigitToDraw.textContent = "";
                  break;
                case 4:
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Name can not start with digit.";
                  DigitToDraw.textContent = "";
              }
            },
            error: function(xhr, status, error) {
              // Handle the error
              console.log(error);
            }
          });
        });
    });

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

    function stopDrawing() {
        isDrawing = false;
      }

    function saveDigit() {
        modelNameInput.disabled = true;
        sendDigit();
        DigitNumber += 1;
        if (CurrentDigit === MaxDigit && DigitNumber === MaxDigitNum) {
            console.log("All digits have been written");
            saveButton.disabled = true;
            trainButton.disabled = false;
            // Make train button active
        }
        if (DigitNumber === MaxDigitNum) {
            DigitNumber = 0;
            CurrentDigit += 1;
        }
        DigitToDraw.textContent = CurrentDigit;
        var value = (CurrentDigit*MaxDigitNum+DigitNumber)/((MaxDigit+1)*MaxDigitNum) * 100;
        value = Math.round(value)
        console.log(value)
        overallProgressBar.value = value;
        digitProgress.textContent = "Progress: "+value+"%";
        clearCanvas();
    }

    function sendDigit() {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = 28;
        tempCanvas.height = 28;
        const tempContext = tempCanvas.getContext('2d');

        // Draw the original canvas image onto the temporary canvas with the desired size
        tempContext.drawImage(canvas, 0, 0, 28, 28);
        const dataURL = tempCanvas.toDataURL();

        $.ajax({
            url: "/train.html",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                MessageType: "Image",
                ModelName: modelNameInput.value,
                Digit: CurrentDigit,
                imageBase64: dataURL
            }),
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }

    function trainModel() {
        trainButton.disabled = true;
        $.ajax({
            url: "/train.html",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                MessageType: "StartTrain",
                ModelName: modelNameInput.value,
            }),
            error: function(xhr, status, error) {
                console.log(error);
            }
        })
    }

    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Event listeners
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);
    canvas.addEventListener("contextmenu", function(event) {
      // Prevent the default right-click behavior (e.g., showing the context menu)
      event.preventDefault();
      
      clearCanvas()
    });

    saveButton.addEventListener("click", saveDigit);
    trainButton.addEventListener("click", trainModel);
    clearButton.addEventListener("click", clearCanvas);
});
