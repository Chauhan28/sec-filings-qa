let currentAnswer = "";
let isTyping = false;

// Create silver sparkles
function createSparkles() {
  const sparklesContainer = document.getElementById('sparkles');
  const sparkleCount = window.innerWidth < 600 ? 8 : 12;

  for (let i = 0; i < sparkleCount; i++) {
    const sparkle = document.createElement('div');
    sparkle.classList.add('sparkle');

    const size = Math.random() * 4 + 2;
    const posX = Math.random() * 100;
    const duration = Math.random() * 15 + 10;
    const delay = Math.random() * 5;
    const opacity = Math.random() * 0.3 + 0.2;

    sparkle.style.width = `${size}px`;
    sparkle.style.height = `${size}px`;
    sparkle.style.left = `${posX}%`;
    sparkle.style.opacity = opacity;
    sparkle.style.animationDuration = `${duration}s`;
    sparkle.style.animationDelay = `${delay}s`;

    sparklesContainer.appendChild(sparkle);
  }
}

// Initialize sparkles
createSparkles();

// Called when user clicks send or presses Enter
function sendMessage() {
  const input = document.getElementById("chatInput");
  const answerBox = document.getElementById("answerBox");
  const text = input.value.trim();

  if (!text || isTyping) return;

  input.value = "";
  answerBox.innerHTML = "";
  simulateTyping(text);
}

// Show typing animation and fetch real answer from backend
function simulateTyping(question) {
  isTyping = true;
  const answerBox = document.getElementById("answerBox");
  answerBox.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

  fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  })
    .then(response => response.json())
    .then(data => {
      displayAnswer(data.answer);
    })
    .catch(error => {
      answerBox.innerHTML = "❌ Error: " + error.message;
    })
    .finally(() => {
      isTyping = false;
    });
}

// Show each word one-by-one for smooth animation
function displayAnswer(answer) {
  const answerBox = document.getElementById("answerBox");
  answerBox.innerHTML = "";
  answerBox.classList.add("active");

  const words = answer.split(" ");
  let wordIndex = 0;

  const interval = setInterval(() => {
    if (wordIndex < words.length) {
      answerBox.innerHTML += words[wordIndex] + " ";
      wordIndex++;
    } else {
      clearInterval(interval);
    }
  }, 50);
}

function newChat() {
  if (isTyping) return;
  const answerBox = document.getElementById("answerBox");
  answerBox.innerHTML = "Your answers will be displayed here.";
  answerBox.classList.remove("active");
  currentAnswer = "";
  document.getElementById("chatInput").value = "";
}

function clearChat() {
  newChat();
}

function copyToClipboard() {
  if (!currentAnswer) return;
  navigator.clipboard.writeText(currentAnswer).then(() => {
    const notification = document.createElement("div");
    notification.className = "copy-notification";
    notification.textContent = "Copied!";
    document.body.appendChild(notification);
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 2300);
  });
}

// Update time in header
document.addEventListener('DOMContentLoaded', () => {
  const dateTimeElement = document.querySelector('.header-datetime');
  const now = new Date();
  const options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZone: 'America/Chicago',
    timeZoneName: 'short'
  };
  dateTimeElement.textContent = now.toLocaleString('en-US', options);
});
