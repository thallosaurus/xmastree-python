socket = null;

function initSocket() {
    socket = io();
    socket.on("status", (data) => {
        console.log(data);
        updateInputs(JSON.parse(data));
    });
}