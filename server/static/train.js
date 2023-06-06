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
    const digitProgressBar = document.getElementById("digit-progress");
    const overallProgressBar = document.getElementById("overall-progress");
    const errorLabel = document.getElementById("error-label");

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function startDrawing(e) {
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
                case "0":
                  // Model name is correct
                  saveButton.disabled = false;
                  trainButton.disabled = false;
                  errorLabel.textContent = "";
                  break;
                case "1":
                  // Name is too short
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Name is too short.";
                  break;
                case "2":
                  // Name is already taken
                  saveButton.disabled = true;
                  trainButton.disabled = true;
                  errorLabel.textContent = "Name is already taken.";
                  break;
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

    function saveDigit() {
        sendDigit();
        DigitNumber += 1;
        if (CurrentDigit === MaxDigit && DigitNumber === MaxDigitNum) {
            console.log("All digits have been written");
            // Make train button active
        }
        if (DigitNumber === MaxDigitNum) {
            DigitNumber = 0;
            CurrentDigit += 1;
        }
        console.log(CurrentDigit, DigitNumber);
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
                ModelName: modelNameInput.value + ".db",
                Digit: CurrentDigit,
                imageBase64: dataURL
            }),
            success: function(response) {
                console.log(response)
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }

    function trainModel() {
        $.ajax({
            url: "/train.html",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                MessageType: "StartTrain",
                ModelName: modelNameInput.value + ".db",
            }),
            success: function(response) {
                console.log(response)
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        }).done(function() {
            console.log('Train Started');
        });
    }

    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        digitLabel.textContent = "";
        digitProgressBar.style.width = "0";
        overallProgressBar.style.width = "0";
        errorLabel.textContent = "";
    }

    // Event listeners
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseout", stopDrawing);

    saveButton.addEventListener("click", saveDigit);
    trainButton.addEventListener("click", trainModel);
    clearButton.addEventListener("click", clearCanvas);
});
