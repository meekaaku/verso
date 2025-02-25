function onConnectClick() {
    console.log("Connecting...");
    ws = new WebSocket('ws://rook:8765');

    ws.onopen = () => {
        console.log("Connected");
    };

    ws.onmessage = (event) => {
        console.log("Received message", event.data);
    };
}


function onServoButtonClick(servo, direction) {
    ws.send(JSON.stringify({servo: servo, direction: direction}));
}

function onServoButtonMouseDown(servo, direction) {
    ws.send(JSON.stringify({servo: servo, direction: direction}));
}

function onServoButtonMouseUp(servo, direction) {
    ws.send(JSON.stringify({servo: servo, direction: direction}));
}
