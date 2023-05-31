document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    var digitLabel = document.getElementById("digit-label");
    var saveButton = document.getElementById("save");
    var trainButton = document.getElementById("train");
    var clearButton = document.getElementById("clear");
    var modelNameInput = document.getElementById("model-name");
    var digitProgressBar = document.getElementById("digit-progress");
    var overallProgressBar = document.getElementById("overall-progress");
    var errorLabel = document.getElementById("error-label");


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
        // Code to save the drawn digit goes here
        // You can access the pixel data of the canvas using context.getImageData()
        // Perform any necessary preprocessing or data conversion before saving the digit
        digitLabel.textContent = "Digit Saved!";
        saveButton.disabled = true;
        trainButton.disabled = false;
        digitProgressBar.style.width = "100%";
    }

    function trainModel() {
        // Code to train the model goes here
        // You can use the modelNameInput.value to get the model name
        // Update the progress bars accordingly during the training process
        // Display any errors or success messages using the errorLabel.textContent
    }

    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        digitLabel.textContent = "";
        saveButton.disabled = false;
        trainButton.disabled = true;
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
