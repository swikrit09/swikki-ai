# Swikki AI

Swikki AI is a voice assistant project designed to enhance productivity and streamline tasks using AI-powered tools.

## Features

- **Speech Recognition**: Converts spoken language into text.
- **Text-to-Speech (TTS)**: Reads text responses aloud.
- **Natural Language Processing (NLP)**: Understands and processes user commands.
- **Task Automation**: Executes tasks such as opening applications, searching the web, and managing reminders.
- **Custom Commands**: Allows users to define and trigger personalized actions.
- **Integration APIs**: Connects with third-party services for extended functionality.

## Tool

- open_website
- send_email
- run_python_script
- increase_volume
- decrease_volume
- mute_volume
- unmute_volume
- shutdown_system
- restart_system
- get_battery_status
- empty_recycle_bin
- take_screenshot
- search_wikipedia
- play_on_youtube
- DuckDuckGoSearchRun().as_tool()

## Get Your Own

1. **Clone the repository:**
    ```bash
    git clone https://github.com/swikrit09/swikki-ai.git
    cd swikki-ai
    ```

2. **Install `uv` (Python package manager):**
    ```bash
    pip install uv
    ```

3. **Create a virtual environment:**
    ```bash
    uv venv venv
    ```

4. **Activate the virtual environment:**  
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

6. **Set up environment variables:**  
   Create a `.env` file in the project root with the following content:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    SMTP_USERNAME=your_smtp_username_here
    SMTP_EMAIL_ID=your_email@example.com
    SMTP_PASSWORD=your_smtp_password_here
    ```

7. **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.