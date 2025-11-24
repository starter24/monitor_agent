document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusSpan = document.getElementById('status');
    const tableBody = document.querySelector('#monitorTable tbody');

    // WebSocket Connection
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const monitorSocket = new WebSocket(
        wsScheme + '://' + window.location.host + '/ws/monitor/'
    );

    monitorSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        addTableRow(data);
    };

    monitorSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    // API Controls
    startBtn.addEventListener('click', () => {
        fetch('/api/start/', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                updateStatus(true);
            });
    });

    stopBtn.addEventListener('click', () => {
        fetch('/api/stop/', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                updateStatus(false);
            });
    });

    function updateStatus(running) {
        if (running) {
            statusSpan.textContent = "Status: Monitoring...";
            statusSpan.classList.add('running');
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            statusSpan.textContent = "Status: Idle";
            statusSpan.classList.remove('running');
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    }

    function addTableRow(data) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.timestamp}</td>
            <td class="transcript">${data.transcript}</td>
            <td class="summary">${data.summary}</td>
        `;
        // Prepend to show newest first
        tableBody.insertBefore(row, tableBody.firstChild);
    }

    // Check initial status
    fetch('/api/status/')
        .then(response => response.json())
        .then(data => {
            updateStatus(data.running);
        });
});
