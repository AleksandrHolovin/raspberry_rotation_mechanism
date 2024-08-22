function buttonPress(buttonName) {
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
    .then(response => response.json())
}

function buttonRelease(buttonName) {
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
    .then(response => response.json())
}