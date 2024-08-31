function disableButtons(exceptButton) {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button !== exceptButton) {
            button.disabled = true;
            button.style.opacity = '0.5';
        }
    });
}

function enableButtons() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.disabled = false;
        button.style.opacity = '1';
    });
}

function buttonPress(buttonName, buttonElement) {
    disableButtons(buttonElement);
    fetch('/button_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            button_name: buttonName,
            action: 'press'
        }),
    })
    .then(response => response.json());
}

function buttonRelease(buttonName) {
    enableButtons();
    fetch('/button_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            button_name: buttonName,
            action: 'release'
        }),
    })
    .then(response => response.json());
}

function fetchAngle() {
    fetch('/get_angles')
        .then(response => response.json())
        .then(data => {
            document.getElementById('elevation').textContent = Number(data.elevation) + 90;
            document.getElementById('azimuth').textContent = data.azimuth;
        });
}

setInterval(fetchAngle, 100);
