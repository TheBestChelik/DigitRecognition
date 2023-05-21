const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
let isDrawing = false;

// Set up event listeners for drawing
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Add event listener for the Recognize Digit button
document.getElementById('save').addEventListener('click', recognizeDigit);

function startDrawing(event) {
    isDrawing = true;
    draw(event);
}

function draw(event) {
    if (!isDrawing) return;
    const x = event.offsetX;
    const y = event.offsetY;
    context.beginPath();
    context.moveTo(x, y);
    context.lineTo(x, y);
    context.lineWidth = 4;
    context.strokeStyle = '#05B8FF';
    context.stroke();
}

function stopDrawing() {
    isDrawing = false;
}

function recognizeDigit() {
    const image = canvas.toDataURL().split(',')[1];  // Extract base64 string
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `image=${image}`,
    }).then(response => response.text())
      .then(data => {
          console.log(data);  // Here you will receive the predicted digit from the server
          displayRecognizedDigit(data);  // Call a function to display the recognized digit on the page
      });
}

function displayRecognizedDigit(digit) {
    const digitDisplay = document.getElementById('digit');
    digitDisplay.textContent = digit;
}

// Add event listener for the Clear Canvas button
document.getElementById('clear').addEventListener('click', clearCanvas);

function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    const digitDisplay = document.getElementById('digit');
    digitDisplay.textContent = '-';
}
