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
        // Code to recognize the digit goes here
        // You can access the pixel data of the canvas using context.getImageData()
        // Perform any necessary preprocessing or data conversion before passing it to the recognition algorithm
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
