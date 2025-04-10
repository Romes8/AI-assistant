# How to operate: 

## Deployment/Start:  (using podman locally)
1. podman-compose build
2. podman-compose up
3. Check for status of the system - 
    Ollama - http://localhost:11434/api/tags
    API (Ollama needs to run )- http://127.0.0.1:5000/api/health
    CHAT - curl --location 'http://localhost:5000/api/chat' \ --header 'Content-Type: application/json' \ --data '{"message":"What degree does Roman have?"}'

## Integration with Wordpress/Elementor page:
1. Make a .zip file from "wordpress-llm-plugin"
2. Upload it as a cusotm plugin
3. (optional) check the plugin for the correct API connection to the API server
4. Go to the page where we want to place the text window
5. Add "Shortcode" onto the page
6. Insert [llm_assistant] and save
7. Chat looking section should appear

## Adding data
Upload daat in form of .pdf .md .html into data folder. For sefety these files are ignored. 

## Trouble shooting
in case of bad files FTP connection is needed to the hosting portal. Edit the files through FTP and problem should be solved.