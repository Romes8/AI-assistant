<?php
/**
 * Plugin Name: LLM Assistant Integration
 * Description: Integrates your WordPress site with your personal LLM assistant
 * Version: 1.0.0
 * Author: Your Name
 */

// Exit if accessed directly
if (!defined('ABSPATH')) exit;

// Register scripts
function llm_assistant_register_scripts() {
    wp_register_script(
        'llm-assistant-js',
        plugin_dir_url(__FILE__) . 'assets/js/assistant.js',
        ['jquery'],
        'time()',
        true
    );
    
    wp_register_style(
        'llm-assistant-css',
        plugin_dir_url(__FILE__) . 'assets/css/assistant.css',
        [],
        '1.0.0'
    );
    
    // Pass variables to JavaScript
    wp_localize_script(
        'llm-assistant-js',
        'llmAssistant',
        [
            'apiUrl' => get_option('llm_assistant_api_url', 'http://localhost:5000/api/chat'),
        ]
    );
}
add_action('wp_enqueue_scripts', 'llm_assistant_register_scripts');

// Add inline CSS for styling the assistant
function llm_assistant_inline_css() {
    echo '<style>
       .llm-assistant-container {
        width: 100%;
        max-width: 500px;
        height: 500px;
        border: none;
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        margin: 0 auto;
        background: rgba(252, 236, 212, 0.92); /* #fcecd4 with transparency */
        backdrop-filter: blur(5px);
       }

        .llm-assistant-header {
            background-color: #f18430; /* second color */
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 3px solid #204617; /* third color */
        }

        .llm-assistant-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: rgba(252, 236, 212, 0.7);
        }

        .llm-assistant-input {
            display: flex;
            border-top: 1px solid rgba(241, 132, 48, 0.3); /* semi-transparent second color */
            padding: 15px;
            background: rgba(252, 236, 212, 0.95); /* slightly darker main color */
        }

        .llm-assistant-input input {
            flex: 1;
            border: 1px solid #f18430; /* second color */
            border-radius: 20px 0 0 20px;
            padding: 12px 15px;
            margin-right: 0;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }

        .llm-assistant-input input:focus {
            outline: none;
            border-color: #204617; /* third color */
            box-shadow: 0 0 0 1px rgba(32, 70, 23, 0.3); /* third color with transparency */
        }

        .llm-assistant-input button {
            background: #f18430; /* second color */
            color: white;
            border: none;
            border-radius: 0 20px 20px 0;
            padding: 12px 20px;
            cursor: pointer;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .llm-assistant-input button:hover {
            background: #204617; /* third color */
        }

        .user-message {
            background: #f18430; /* second color */
            color: white;
            padding: 12px 18px;
            border-radius: 18px 18px 0 18px;
            margin-bottom: 15px;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
            text-align: right;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
            animation: fadeIn 0.3s;
        }

        .user-message::after {
            content: "";
            position: absolute;
            right: -8px;
            bottom: 0;
            border: 8px solid transparent;
            border-bottom-color: #f18430; /* second color */
            border-left: 0;
            border-bottom: 0;
        }

        .assistant-message {
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 12px 18px;
            border-radius: 18px 18px 18px 0;
            margin-bottom: 15px;
            max-width: 80%;
            border-left: 3px solid #204617; /* third color */
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
            animation: fadeIn 0.3s;
        }

        .assistant-message::after {
            content: "";
            position: absolute;
            left: -8px;
            bottom: 0;
            border: 8px solid transparent;
            border-right-color: rgba(255, 255, 255, 0.9);
            border-bottom: 0;
        }

        .assistant-typing {
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
            padding: 12px 18px;
            background: rgba(255, 255, 255, 0.7);
            max-width: 50%;
            border-radius: 18px;
        }

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .llm-assistant-container {
                max-width: 100%;
                height: 400px;
            }

            .llm-assistant-input {
                padding: 10px;
            }

            .llm-assistant-input input {
                padding: 10px;
            }

            .llm-assistant-input button {
                padding: 10px 15px;
                font-size: 12px;
            }
        }

        /* Custom scrollbar */
        .llm-assistant-messages::-webkit-scrollbar {
            width: 6px;
        }

        .llm-assistant-messages::-webkit-scrollbar-track {
            background: rgba(252, 236, 212, 0.5); /* semi-transparent main color */
        }

        .llm-assistant-messages::-webkit-scrollbar-thumb {
            background: #f18430; /* second color */
            border-radius: 3px;
        }

        .llm-assistant-messages::-webkit-scrollbar-thumb:hover {
            background: #204617; /* third color */
        }

        /* Add a typing animation */
        .typing-dots span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background-color: #f18430; /* second color */
            border-radius: 50%;
            margin-right: 3px;
            animation: typing 1.4s infinite ease-in-out both;
        }

        .typing-dots span:nth-child(1) {
            animation-delay: 0s;
        }

        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>';
}
add_action('wp_head', 'llm_assistant_inline_css');


// Add shortcode for assistant widget
function llm_assistant_shortcode() {
    // Enqueue required scripts and styles
    wp_enqueue_script('llm-assistant-js');
    wp_enqueue_style('llm-assistant-css');
    
    ob_start();
    ?>
    <div class="llm-assistant-container">
        <div class="llm-assistant-header">AI Assistant</div>
        <div class="llm-assistant-messages" id="llm-assistant-messages"></div>
        <div class="llm-assistant-input">
            <input type="text" id="llm-assistant-query" placeholder="Ask me anything...">
            <button id="llm-assistant-send">Send</button>
        </div>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('llm_assistant', 'llm_assistant_shortcode');

// Add settings page
function llm_assistant_add_admin_menu() {
    add_options_page(
        'LLM Assistant Settings',
        'LLM Assistant',
        'manage_options',
        'llm-assistant',
        'llm_assistant_options_page'
    );
}
add_action('admin_menu', 'llm_assistant_add_admin_menu');

// Register settings
function llm_assistant_settings_init() {
    register_setting('llmAssistantPlugin', 'llm_assistant_api_url');
    
    add_settings_section(
        'llm_assistant_section',
        'API Settings',
        'llm_assistant_section_callback',
        'llmAssistantPlugin'
    );
    
    add_settings_field(
        'llm_assistant_api_url',
        'API URL',
        'llm_assistant_api_url_render',
        'llmAssistantPlugin',
        'llm_assistant_section'
    );
}
add_action('admin_init', 'llm_assistant_settings_init');

function llm_assistant_section_callback() {
    echo 'Configure your LLM Assistant settings below:';
}

function llm_assistant_api_url_render() {
    $value = get_option('llm_assistant_api_url', 'http://localhost:5000/api/chat');
    ?>
    <input type='text' name='llm_assistant_api_url' value='<?php echo esc_attr($value); ?>' style="width: 100%; max-width: 400px;">
    <p class="description">The URL to your LLM Assistant API endpoint</p>
    <?php
}

function llm_assistant_options_page() {
    ?>
    <form action='options.php' method='post'>
        <h2>LLM Assistant Settings</h2>
        <?php
        settings_fields('llmAssistantPlugin');
        do_settings_sections('llmAssistantPlugin');
        submit_button();
        ?>
    </form>
    <?php
}