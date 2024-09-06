# Personal Email Assistant

This project is a simple personal email assistant built with LangGraph that helps you interact with your inbox through a web interface. It allows you to retrieve and summarize emails based on specific criteria, making email management easier and more efficient.

## Prerequisites

Before you start, make sure you have the following set up:

### 1. Gmail App Password Setup
If you're using Gmail, you'll need to create an app password for secure access to your inbox. Follow these steps:

- Go to [App Passwords](https://myaccount.google.com/apppasswords).
- You may need to sign in again.
- Select a suitable app name (For eg. personal-email-assistant) and generate a password (you'll use it in the `.env` file).

For more detailed instructions, refer to [Google's documentation](https://support.google.com/mail/answer/185833?hl=en).

### 2. Groq API Key Setup
Groq is used for LLMs (Large Language Models) in this project. To set up and add your Groq API key:

- Go to the [Groq website](https://groq.com/) and sign in to your account.
- Navigate to the API section and generate a new API key.
- Copy the API key.


### 3. Populate the `.env` File
Create a `.env` file in the project root directory with the following variables:

```plaintext
LANGSMITH_API_KEY=your_langsmith_api_key
GROQ_API_KEY=your_groq_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_app_password
EMAIL_HOST=imap.gmail.com
```

## Installation and Setup

### 1. Create a Conda Environment
To isolate dependencies, create and activate a Conda environment:
conda create -n pea python=3.12.5
conda activate pea

### 2. Install the Required Packages
Navigate to the main directory and install the required Python packages:
```bash
pip install -e .
```

### 3. Run the Streamlit App
Navigate to the src directory and launch the web application using Streamlit:
```bash
cd src
streamlit run pea/app.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Groq](https://groq.com/)

## Contact
If you have any questions or suggestions, feel free to reach out. You can contact me at mehersaipreetam@gmail.com. I’ll be happy to assist!
