(async() => {
    const res = await requestBackend("test", { "a": "1", "b": "2" })
    console.log(res)
    const data = await res.text()
    console.log(data)
})();

window.addEventListener("beforeunload", (e) => {
    requestBackend("on_close", {})
    e.preventDefault()
})