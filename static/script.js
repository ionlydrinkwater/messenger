const messagesEl = document.getElementById('messages');
const form = document.getElementById('message-form');
const nameInput = document.getElementById('name');
const messageInput = document.getElementById('message');

function renderMessages(items) {
  if (!items || items.length === 0) {
    messagesEl.innerHTML = '<div class="empty-state">No messages yet. Be the first to send one.</div>';
    return;
  }

  messagesEl.innerHTML = items
    .slice()
    .reverse()
    .map(
      (msg) => `
        <article class="message">
          <div class="message-header">
            <span class="message-name">${escapeHtml(msg.name)}</span>
            <span class="message-time">${escapeHtml(msg.timestamp)}</span>
          </div>
          <div>${escapeHtml(msg.message).replace(/\n/g, '<br>')}</div>
        </article>
      `
    )
    .join('');
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function loadMessages() {
  try {
    const response = await fetch('/messages');
    if (!response.ok) {
      throw new Error('Could not load messages');
    }
    const data = await response.json();
    renderMessages(data.messages || []);
  } catch (error) {
    console.error(error);
    messagesEl.innerHTML = '<div class="empty-state">Unable to load messages right now.</div>';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    name: nameInput.value.trim(),
    message: messageInput.value.trim(),
  };

  if (!payload.name || !payload.message) {
    alert('Please enter both your name and a message.');
    return;
  }

  try {
    const response = await fetch('/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || 'Failed to send message');
    }

    form.reset();
    renderMessages(result.messages || []);
  } catch (error) {
    alert(error.message);
  }
});

loadMessages();
setInterval(loadMessages, 2000);
