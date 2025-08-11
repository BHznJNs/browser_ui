document.getElementById('fibonacci-btn').addEventListener('click', async () => {
    const btn = document.getElementById('fibonacci-btn');
    const resultDiv = document.getElementById('fibonacci-result');
    
    btn.disabled = true;

    try {
        const fibIter = await requestBackend('fibonacci', 10 );
        for await (const value of fibIter) {
            resultDiv.innerHTML += `<br>Fib number: ${value}`;
        }
    } catch (error) {
        resultDiv.innerHTML += `<br><strong>Error:</strong> ${error.message}`;
    } finally {
        btn.disabled = false;
    }
});