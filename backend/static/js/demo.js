(function detectDevTools() {
  let devtoolsOpen = false;

  const threshold = 160; // height/width threshold for detecting dev tools
  const emitAlert = () => {
      console.log("Developer tools detected!");
      // Optionally send a message to your server here
      fetch('/dev-tools-detected', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: "Developer tools opened" })
      });
  };

  const checkDevTools = () => {
      const widthThreshold = window.outerWidth - window.innerWidth > threshold;
      const heightThreshold = window.outerHeight - window.innerHeight > threshold;
      const isDevToolsOpen = widthThreshold || heightThreshold;

      if (isDevToolsOpen && !devtoolsOpen) {
          devtoolsOpen = true;
          emitAlert();
      } else if (!isDevToolsOpen && devtoolsOpen) {
          devtoolsOpen = false;
      }
  };

  setInterval(checkDevTools, 1000); // Check every second
})();

let isFullscreen = false;

function detectFullscreen() {
    console.log("change")
    const { innerWidth, innerHeight } = window;
    const { width, height } = screen;
    console.log("innerWidth", innerWidth, "innerHeight",innerHeight, "width", width, "height", height)

    // Check if the window size matches the screen size
    const fullscreenNow = innerWidth === width && innerHeight === height;
    console.log("fullscreenNow", fullscreenNow)
    if (fullscreenNow && !isFullscreen) {
        isFullscreen = true;
        console.log("Entered full-screen mode");
        sendFullscreenStatus("Entered full-screen mode");
    } else if (!fullscreenNow && isFullscreen) {
        isFullscreen = false;
        console.log("Exited full-screen mode");
        sendFullscreenStatus("Exited full-screen mode");
    }
}

function sendFullscreenStatus(action) {
    fetch("/log-activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, timestamp: new Date() }),
    }).catch(err => console.error("Error logging full-screen activity:", err));
}

// Monitor resize events
window.addEventListener("resize", detectFullscreen);

// Initial check on page load
detectFullscreen();


let blurCount = 0;

window.addEventListener("blur", () => {
    blurCount++;
    sendAlertToServer(`Tab lost focus ${blurCount} times`);
});

function sendAlertToServer(message) {
    fetch("/log-activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            action: message,
            timestamp: new Date(),
        }),
    }).catch(err => console.error("Error logging activity:", err));
}
