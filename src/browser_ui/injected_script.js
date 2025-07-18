globalThis.requestBackend = async function(method, payload=null) {
    return await fetch(`/__method__/${method}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });
}

window.addEventListener("pagehide", (e) => {
    if (e.persisted) return;
    navigator.sendBeacon("/__event__/page_closed")
})
window.addEventListener("DOMContentLoaded", () => {
    fetch("/__event__/page_loaded", {method: "POST"})
})