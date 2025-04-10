jQuery(document).ready(function($) {
    const messagesContainer = $('#llm-assistant-messages');
    const queryInput = $('#llm-assistant-query');
    const sendButton = $('#llm-assistant-send');
    
    // Function to add a message to the UI
    function addMessage(text, isUser) {
        const messageDiv = $('<div></div>');
        messageDiv.addClass(isUser ? 'user-message' : 'assistant-message');
        messageDiv.text(text);
        messagesContainer.append(messageDiv);
        messagesContainer.scrollTop(messagesContainer[0].scrollHeight);
    }
    
    // Function to send query to the assistant API
    function sendQuery(query) {
        addMessage(query, true);
        
        // Show typing indicator
        const typingDiv = $('<div></div>');
        typingDiv.addClass('assistant-typing');
        typingDiv.text('Thinking...');
        messagesContainer.append(typingDiv);
        
        $.ajax({
            url: llmAssistant.apiUrl,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: query }),
            success: function(data) {
                // Remove typing indicator
                typingDiv.remove();
                
                // Add assistant's response
                addMessage(data.response, false);
            },
            error: function(xhr, status, error) {
                // Remove typing indicator
                typingDiv.remove();
                
                // Show error
                addMessage('Sorry, I it seems my working hours are over. I am joking ! My server is down...', false);
                console.error('Error:', error);
            }
        });
    }
    
    // Event listeners
    sendButton.on('click', function() {
        const query = queryInput.val().trim();
        if (query) {
            sendQuery(query);
            queryInput.val('');
        }
    });
    
    queryInput.on('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = queryInput.val().trim();
            if (query) {
                sendQuery(query);
                queryInput.val('');
            }
        }
    });
    
    // Initial greeting
    setTimeout(() => {
        addMessage("Hello! I\'m Roman's personal AI assistant. I can help you answer questions about him.", false);
    }, 500);
});