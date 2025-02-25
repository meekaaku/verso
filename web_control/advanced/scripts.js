function startConnection() {
    ws = new WebSocket('ws://rook:8765');
    const statusElement = document.getElementById('connection-status');

    // WebSocket event handlers
    ws.onopen = () => {
        statusElement.textContent = 'Connected';
        statusElement.classList.remove('disconnected');
        statusElement.classList.add('connected');
    };

    ws.onmessage = (event) => {
        console.log("Received message", event.data);
    };

    ws.onclose = () => {
        statusElement.textContent = 'Disconnected';
        statusElement.classList.remove('connected');
        statusElement.classList.add('disconnected');
    };

    ws.onclose = () => {
        statusElement.textContent = 'Disconnected - Attempting to reconnect...';
        statusElement.classList.remove('connected');
        statusElement.classList.add('disconnected');
        
        setTimeout(() => {
            window.location.reload();
        }, 5000);
    };
    // Function to send slider data
    

}

function sendSliderData(n) {
    console.log("Sending slider data", n);
    const valueElement = document.getElementById('value' + n);
    const sliderElement = document.getElementById('slider' + n);
    valueElement.textContent = sliderElement.value;
    if (ws.readyState === WebSocket.OPEN) {
        const data = {
            joint: n,
            value: Number(sliderElement.value)
        };
        ws.send(JSON.stringify(data));
    }
}
