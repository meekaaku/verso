function startConnection() {
    ws = new WebSocket('ws://rook:8765');

    telemetry.status = 'Connecting...';
    updateTelemetry();

    // WebSocket event handlers
    ws.onopen = () => {
        telemetry.status = 'Connected';
        updateTelemetry();
    };

    ws.onmessage = (event) => {
        console.log("Received message", event.data);
    };

    ws.onclose = () => {
        telemetry.status = 'Disconnected';
        updateTelemetry();
    };

    ws.onclose = () => {
        telemetry.status = 'Connecting...'
        updateTelemetry();
        
        setTimeout(() => {
            window.location.reload();
        }, 5000);
    };
    // Function to send slider data
    

}


function updateTelemetry() {
    const telemetryElement = document.querySelector('.telemetry');
    telemetryElement.innerHTML = Object.entries(telemetry).map(([key, value]) => `<div>${key}: ${value}</div>`).join("");
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
