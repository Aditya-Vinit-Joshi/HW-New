// Search functionality
$(document).ready(function() {
    const searchInput = $('#search-input');
    const suggestionsContainer = $('#search-suggestions');
    
    searchInput.on('input', function() {
        const query = $(this).val();
        
        if (query.length < 2) {
            suggestionsContainer.empty().hide();
            return;
        }
        
        $.get('/search/suggestions/', { q: query }, function(data) {
            suggestionsContainer.empty();
            
            if (data.suggestions.length > 0) {
                data.suggestions.forEach(function(suggestion) {
                    suggestionsContainer.append(
                        $('<div>').addClass('suggestion-item')
                            .text(suggestion)
                            .click(function() {
                                searchInput.val(suggestion);
                                suggestionsContainer.empty().hide();
                                $('#search-form').submit();
                            })
                    );
                });
                suggestionsContainer.show();
            } else {
                suggestionsContainer.hide();
            }
        });
    });
    
    $(document).click(function(e) {
        if (!$(e.target).closest('.search-container').length) {
            suggestionsContainer.empty().hide();
        }
    });
});

// Resource interactions
function likeResource(resourceId) {
    $.post(`/resources/${resourceId}/like/`, function(data) {
        const likeButton = $(`#like-button-${resourceId}`);
        const likeCount = $(`#like-count-${resourceId}`);
        
        if (data.liked) {
            likeButton.addClass('liked');
        } else {
            likeButton.removeClass('liked');
        }
        
        likeCount.text(data.count);
    });
}

function saveResource(resourceId) {
    $.post(`/resources/${resourceId}/save/`, function(data) {
        const saveButton = $(`#save-button-${resourceId}`);
        
        if (data.saved) {
            saveButton.addClass('saved').text('Saved');
        } else {
            saveButton.removeClass('saved').text('Save');
        }
    });
}

// Rating functionality
$('.rating-input').on('change', function() {
    $(this).closest('form').submit();
});

// Chat functionality
let chatSession = null;

function startChatSession() {
    $.post('/chatbot/start-session/', function(data) {
        chatSession = data.session_id;
        $('#chat-container').show();
        $('#start-chat').hide();
    });
}

function sendMessage() {
    const messageInput = $('#message-input');
    const message = messageInput.val().trim();
    
    if (!message) return;
    
    messageInput.val('');
    appendMessage('user', message);
    
    $.post('/chatbot/send-message/', {
        session_id: chatSession,
        message: message
    }, function(data) {
        if (data.error) {
            appendMessage('error', 'Error: ' + data.error);
        } else {
            appendMessage('bot', data.message);
        }
    });
}

function appendMessage(type, content) {
    const messageContainer = $('#messages');
    const messageDiv = $('<div>').addClass(`message ${type}-message`).text(content);
    messageContainer.append(messageDiv);
    messageContainer.scrollTop(messageContainer[0].scrollHeight);
}

// GitHub repository interactions
function saveRepo(repoId) {
    $.post(`/github/repo/${repoId}/save/`, function(data) {
        const saveButton = $(`#repo-save-button-${repoId}`);
        
        if (data.saved) {
            saveButton.addClass('saved').text('Saved');
        } else {
            saveButton.removeClass('saved').text('Save');
        }
    });
}

// Form validation
$(document).ready(function() {
    $('form').on('submit', function() {
        const requiredFields = $(this).find('[required]');
        let isValid = true;
        
        requiredFields.each(function() {
            if (!$(this).val()) {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        return isValid;
    });
});

// Infinite scroll for resource and repo lists
$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
        loadMoreItems();
    }
});

function loadMoreItems() {
    const nextPage = $('#load-more').data('next-page');
    if (!nextPage) return;
    
    $.get(window.location.pathname, { page: nextPage }, function(data) {
        $('#items-container').append(data.items);
        $('#load-more').data('next-page', data.next_page);
    });
}

// Initialize Bootstrap components
$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();
    $('[data-bs-toggle="popover"]').popover();
}); 