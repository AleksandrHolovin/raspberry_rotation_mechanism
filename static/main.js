const BUTTON_TO_DISABLE = [
  "arrow-left",
  "arrow-right",
  "arrow-up",
  "arrow-down",
];

function disableButtons(exceptButton) {
  BUTTON_TO_DISABLE.forEach((className) => {
    const button = document.querySelector(`button.${className}`);
    if (button && button !== exceptButton) {
      button.disabled = true;
    }
  });
}

function enableButtons() {
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    button.disabled = false;
  });
}

function buttonPress(buttonName) {
  fetch("/button_event", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      button_name: buttonName,
      action: "press",
    }),
  }).then((response) => response.json());
}

function buttonRelease(buttonName) {
  fetch("/button_event", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      button_name: buttonName,
      action: "release",
    }),
  }).then((response) => response.json());
}

function handleArrowPress(buttonName, buttonElement) {
  disableButtons(buttonElement);
  buttonPress(buttonName);
}
function handleArrowRelease(buttonName) {
  enableButtons();
  buttonRelease(buttonName);
}

function fetchAngle() {
  fetch("/get_angles")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("elevation").textContent =
        Number(data.elevation) + 90;
      document.getElementById("azimuth").textContent = data.azimuth;
    });
}

setInterval(fetchAngle, 100);

document.addEventListener("DOMContentLoaded", function () {
  let currentArrowKey = null;

  document.addEventListener("keydown", function (event) {
    if (currentArrowKey !== null) {
      return;
    }

    switch (event.key) {
      case "ArrowUp":
        handleArrowPress("up", this);
        currentArrowKey = "up";
        break;
      case "ArrowDown":
        handleArrowPress("down", this);
        currentArrowKey = "down";
        break;
      case "ArrowLeft":
        handleArrowPress("left", this);
        currentArrowKey = "left";
        break;
      case "ArrowRight":
        handleArrowPress("right", this);
        currentArrowKey = "right";
        break;
    }
  });

  document.addEventListener("keyup", function (event) {
    switch (event.key) {
      case "ArrowUp":
      case "ArrowDown":
      case "ArrowLeft":
      case "ArrowRight":
        handleArrowRelease();
        currentArrowKey = null;
        break;
    }
  });
});
