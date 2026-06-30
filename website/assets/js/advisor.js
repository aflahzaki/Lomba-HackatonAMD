/**
 * LangkahKampus - AI Advisor Chat JavaScript
 * Handles chat interface for AI Advisor feature
 */

// Conversation history for multi-turn chat (max 10 exchanges)
var conversationHistory = [];
// Track the last prediction context to detect changes
var lastPredictionContextKey = null;

document.addEventListener('DOMContentLoaded', function() {
    initChatForm();

    // Auto-send prediction context if navigated from prediksi.php
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('fromPrediction') === '1') {
        var storedPrediction = sessionStorage.getItem('lastPrediction');
        if (storedPrediction) {
            try {
                var predData = JSON.parse(storedPrediction);
                var prob = predData.probability || 0;
                var program = predData.program_name || predData.target_program || 'target';
                var university = predData.university_name || predData.university || '';
                var autoMessage = 'Tolong analisis hasil prediksi SNBP saya. Probabilitas: ' + prob + '%, Program: ' + program + ', Universitas: ' + university + '. Berikan saran untuk meningkatkan peluang saya.';
                setTimeout(function() {
                    sendMessage(autoMessage);
                }, 500);
            } catch (e) {
                // Ignore parse errors
            }
        }
    }
});

/* === Chat Form Initialization === */
function initChatForm() {
    var form = document.getElementById('chatForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        var input = document.getElementById('chatInput');
        var message = input.value.trim();
        if (!message) return;

        sendMessage(message);
        input.value = '';
    });
}

/* === Send Suggestion Chip === */
function sendSuggestion(message) {
    sendMessage(message);
}

/* === Send Message to Backend === */
function sendMessage(message) {
    var chatMessages = document.getElementById('chatMessages');
    var sendBtn = document.getElementById('chatSendBtn');
    var chatInput = document.getElementById('chatInput');

    // Add user message to chat
    appendMessage('user', message);

    // Disable input while waiting
    sendBtn.disabled = true;
    chatInput.disabled = true;

    // Show typing indicator
    var typingId = showTypingIndicator();

    // Build payload
    var payload = {
        message: message
    };

    // Include prediction context if available from sessionStorage
    var predictionContext = sessionStorage.getItem('lastPrediction');
    if (predictionContext) {
        try {
            payload.context = JSON.parse(predictionContext);
        } catch (e) {
            // Ignore invalid stored data
        }
    }

    // Reset conversation history if the prediction context has changed
    var currentContextKey = predictionContext || '';
    if (lastPredictionContextKey !== null && currentContextKey !== lastPredictionContextKey) {
        conversationHistory = [];
    }
    lastPredictionContextKey = currentContextKey;

    // Include conversation history (limit to last 10 exchanges = 20 messages)
    if (conversationHistory.length > 0) {
        payload.history = conversationHistory.slice(-20);
    }

    // Add user message to conversation history
    conversationHistory.push({ role: 'user', content: message });

    // Limit history to last 10 exchanges (20 messages)
    if (conversationHistory.length > 20) {
        conversationHistory = conversationHistory.slice(-20);
    }

    // Send to backend
    ajaxRequest('../api/advisor.php', 'POST', payload, function(error, response) {
        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Re-enable input
        sendBtn.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();

        if (error) {
            appendMessage('bot', 'Maaf, terjadi kesalahan. Silakan coba lagi.');
            return;
        }

        if (response && response.reply) {
            appendMessage('bot', response.reply);

            // Add assistant response to conversation history
            conversationHistory.push({ role: 'assistant', content: response.reply });

            // Limit history to last 10 exchanges (20 messages)
            if (conversationHistory.length > 20) {
                conversationHistory = conversationHistory.slice(-20);
            }

            // Update suggestion chips if available
            if (response.suggestions && response.suggestions.length > 0) {
                updateSuggestions(response.suggestions);
            }
        } else {
            appendMessage('bot', 'Maaf, saya tidak dapat memproses pertanyaan Anda saat ini.');
        }
    });
}

/* === Append Message to Chat === */
function appendMessage(type, text) {
    var chatMessages = document.getElementById('chatMessages');
    var messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message chat-' + type;

    var avatarIcon = type === 'user' ? 'fa-user' : 'fa-robot';
    var avatarHtml = '<div class="chat-avatar"><i class="fas ' + avatarIcon + '"></i></div>';

    var bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'chat-bubble';
    bubbleDiv.innerHTML = formatMessage(text);

    messageDiv.innerHTML = avatarHtml;
    messageDiv.appendChild(bubbleDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* === Format Message Text === */
function formatMessage(text) {
    // Convert newlines to <br>
    text = text.replace(/\n/g, '<br>');

    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convert *italic* to <em>
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Convert bullet lists (lines starting with - )
    text = text.replace(/(?:^|<br>)- (.*?)(?=<br>|$)/g, '<br>&bull; $1');

    return '<p>' + text + '</p>';
}

/* === Typing Indicator === */
function showTypingIndicator() {
    var chatMessages = document.getElementById('chatMessages');
    var typingDiv = document.createElement('div');
    var id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'chat-message chat-bot';
    typingDiv.innerHTML = '<div class="chat-avatar"><i class="fas fa-robot"></i></div>' +
        '<div class="chat-bubble"><p><i class="fas fa-spinner fa-spin"></i> Sedang mengetik...</p></div>';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    var el = document.getElementById(id);
    if (el) el.remove();
}

/* === Update Suggestion Chips === */
function updateSuggestions(suggestions) {
    var container = document.getElementById('suggestionChips');
    if (!container) return;

    container.innerHTML = '';
    suggestions.forEach(function(suggestion) {
        var btn = document.createElement('button');
        btn.className = 'btn btn-outline btn-sm suggestion-chip';
        btn.innerHTML = '<i class="fas fa-comment"></i> ' + suggestion;
        btn.onclick = function() {
            sendSuggestion(suggestion);
        };
        container.appendChild(btn);
    });
}
