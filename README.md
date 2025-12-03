# Savvy-AI
# 🤖 Savvy AI - Next Generation Chatbot Interface

A stunning, modern chatbot interface built with pure HTML, CSS, and JavaScript. Features glassmorphism design, smooth animations, and an attractive user experience that stands out from traditional chatbots.

![Savvy AI](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

## ✨ Features

### 🎨 Visual Design
- **Glassmorphism UI** - Modern frosted glass effect with backdrop blur
- **Animated Background** - 30+ floating particles creating depth and movement
- **Gradient Themes** - Beautiful purple-pink gradients throughout
- **Smooth Animations** - Elegant slide, fade, and pulse effects on all elements
- **Responsive Design** - Works perfectly on desktop and mobile devices

### 🚀 Functionality
- **Real-time Messaging** - Instant message display with smooth animations
- **Typing Indicator** - Animated dots showing AI is processing
- **Quick Suggestions** - Pre-made prompt chips for easy interaction
- **Auto-scroll** - Automatically scrolls to latest messages
- **Timestamps** - Each message displays the time it was sent
- **Online Status** - Live status indicator with blinking animation
- **Smart Input** - Auto-resizing textarea with keyboard shortcuts

### 💬 User Experience
- **Welcome Screen** - Friendly greeting with suggested actions
- **Message Bubbles** - Distinct styling for user and AI messages
- **Custom Scrollbar** - Styled to match the overall theme
- **Hover Effects** - Interactive feedback on all clickable elements
- **Disabled States** - Prevents multiple sends while AI is typing

## 🎯 Quick Start

### Option 1: Direct Use
1. Download the `index.html` file
2. Open it directly in any modern web browser
3. Start chatting!

### Option 2: Local Server
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve

# Then open http://localhost:8000
```

## 🔧 Integration with AI Backend

The chatbot currently runs in demo mode with simulated responses. To integrate with a real AI backend:

### 1. OpenAI API Integration
```javascript
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    addMessage(message, 'user');
    messageInput.value = '';
    showTypingIndicator();
    
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY'
            },
            body: JSON.stringify({
                model: 'gpt-4',
                messages: [{ role: 'user', content: message }]
            })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        addMessage(data.choices[0].message.content, 'ai');
    } catch (error) {
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}
```

### 2. Anthropic Claude API Integration
```javascript
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    addMessage(message, 'user');
    messageInput.value = '';
    showTypingIndicator();
    
    try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': 'YOUR_API_KEY',
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: 'claude-3-opus-20240229',
                max_tokens: 1024,
                messages: [{ role: 'user', content: message }]
            })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        addMessage(data.content[0].text, 'ai');
    } catch (error) {
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}
```

### 3. Custom Backend Integration
```javascript
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    addMessage(message, 'user');
    messageInput.value = '';
    showTypingIndicator();
    
    try {
        const response = await fetch('YOUR_BACKEND_URL/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        addMessage(data.response, 'ai');
    } catch (error) {
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}
```

## 🎨 Customization

### Change Color Scheme
Modify the gradient colors in the CSS:

```css
/* Main background gradient */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Logo and send button gradient */
.logo, .send-btn {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

/* User message gradient */
.message.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Modify Suggestion Chips
Edit the suggestion chips in the HTML:

```html
<div class="suggestions">
    <div class="suggestion-chip" onclick="sendSuggestion('Your custom prompt')">🔥 Your Label</div>
    <!-- Add more chips -->
</div>
```

### Adjust Animation Speed
Change animation durations in CSS:

```css
@keyframes messageSlide {
    /* Adjust from/to values for different effects */
}

.particle {
    animation-duration: 15s; /* Change particle speed */
}
```

## ⌨️ Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line in message
- **Escape** - Clear input (custom implementation needed)

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

⭐ If you found this project helpful, please consider giving it a star!
