const eventList = document.getElementById('event-list');
globalThis.backendListener.on("message", (data) => {
    const newItem = document.createElement('li');
    newItem.textContent = `Message: ${data}`;
    eventList.appendChild(newItem);
});
globalThis.backendListener.on("greeting", (data) => {
    const newItem = document.createElement('li');
    newItem.textContent = `Greeting: ${data}`;
    eventList.appendChild(newItem);
});