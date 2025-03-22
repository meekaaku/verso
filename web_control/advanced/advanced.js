function startConnection() {
    const socket = new WebSocket('ws://rook:8765');

    telemetry._status = 'connecting...';
    updateTelemetry();

    // WebSocket event handlers
    socket.onopen = () => {
        telemetry._status = 'connected';
        updateTelemetry();
    };

    socket.onmessage = (event) => {
	const message = JSON.parse(event.data);
	console.log("Received command", message.command);
	if(message.command == "telemetry") {
		telemetry = message.data;
		telemetry._status = "connected"
		updateTelemetry()

	}
    };

    socket.onclose = () => {
        telemetry.status = 'Disconnected';
        updateTelemetry();
    };

    socket.onclose = () => {
        telemetry._status = 'connecting...'
        updateTelemetry();
        
        setTimeout(() => {
            window.location.reload();
        }, 5000);
    };
    // Function to send slider data
    return socket; 

}


function updateTelemetry() {
    const telemetryElement = document.querySelector('.telemetry');
	const sorted = Object.entries(telemetry).sort((a,b) => a[0] < b[0] ? -1 : 1)
    telemetryElement.innerHTML = sorted.map(([key, value]) => `<div>${key}: ${value}</div>`).join("");
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
