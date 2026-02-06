# Weather Chatbot Project

This project is a **Weather Chatbot** built using **Streamlit** and **Google ADK**. The chatbot provides weather-related information such as current weather conditions, temperature, wind speed, sunrise/sunset times, and more for specific cities or places. It uses Google Cloud's Vertex AI for natural language processing and integrates with Open-Meteo API for weather data.

---

## Features
- Interactive chatbot interface using **Streamlit**.
- Context-aware responses for weather-related queries.
- Integration with Google Cloud's **Vertex AI** for language processing.
- Fetches real-time weather data using the **Open-Meteo API**.
- Supports session-based context management for maintaining conversation history.

---

## Prerequisites

### 1. Install Required Tools
- **Python 3.9+**: Ensure Python is installed on your system.
- **Google Cloud CLI (gcloud)**: Install the Google Cloud CLI to authenticate and manage Google Cloud resources.

### 2. Google Cloud Setup
- **Enable Vertex AI API**:
  - Go to the [Google Cloud Console](https://console.cloud.google.com/).
  - Enable the **Vertex AI API** for your project.
- **Add Permissions**:
  - Assign the **Vertex AI User** role to your Google Cloud account.

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd weather_chatbot_project
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
- Create a `.env` file in the `weather_support` directory (if not already present).
- Add the following environment variables:
  ```plaintext
  GOOGLE_GENAI_USE_VERTEXAI=1
  GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>
  GOOGLE_CLOUD_LOCATION=global
  MODEL_NAME=gemini-2.0-flash
  TEMPERATURE=0.7
  ```

---

## Google Cloud Authentication

### 1. Install Google Cloud CLI
Follow the instructions to install the **gcloud CLI**:  
[Install Google Cloud CLI](https://cloud.google.com/sdk/docs/install)

### 2. Authenticate with Google Cloud
Run the following commands to authenticate:
```bash
gcloud auth login
gcloud auth application-default login
```

### 3. Add Permissions
Ensure your Google Cloud account has the **Vertex AI User** role:
```bash
gcloud projects add-iam-policy-binding <your-gcp-project-id> \
  --member="user:<your-email>" \
  --role="roles/aiplatform.user"
```

---

## Running the Application

1. **Start the Streamlit App**:
   ```bash
   streamlit run main.py
   ```

2. **Interact with the Chatbot**:
   - Open the URL displayed in the terminal (usually `http://localhost:8501`).
   - Ask weather-related queries like:
     - "What is the current weather in New York?"
     - "Tell me the weather in Sydney."

---

## Project Structure

```
weather_chatbot_project/
├── README.md                      # Project documentation
├── main.py                        # Streamlit app entry point
├── requirements.txt               # Python dependencies
├── weather_support/               # Core logic for the chatbot
│   ├── agent.py                   # Orchestrator agent
│   ├── tools/                     # Tools and utilities
│   ├── sub_agents/                # Sub-agents for specific tasks
│   └── .env                       # Environment variables
├── Weather_Chatbot_sample_output.pdf   # Sample output file demonstrating chatbot responses
```

---

## Notes

- Ensure your Google Cloud project is active and properly configured.
- The chatbot uses **Vertex AI** for natural language processing, so make sure the API is enabled and your account has the necessary permissions.
- The weather data is fetched using the **Open-Meteo API**, so ensure you have internet access while running the app.

---

## Troubleshooting

1. **Authentication Issues**:
   - Ensure you have logged in to Google Cloud using the `gcloud auth login` and `gcloud auth application-default login` commands.

2. **Vertex AI Errors**:
   - Verify that the **Vertex AI API** is enabled for your Google Cloud project.
   - Ensure your account has the **Vertex AI User** role.

3. **Streamlit App Not Starting**:
   - Ensure all dependencies are installed using `pip install -r requirements.txt`.
   - Check if the virtual environment is activated.

---

## License
This project is licensed under the MIT License.

# Project Overview

This repository contains a weather chatbot application that integrates Open-Meteo API for real-time weather data and Google Cloud Vertex AI for natural language processing. The project is designed to provide users with detailed weather reports and a conversational interface for weather-related queries.

## Folder Structure

- `main.py`: Entry point for the Streamlit application.
- `requirements.txt`: Lists all dependencies required for the project.
- `weather_support/`: Contains the core logic and support modules for the chatbot.
  - `agent.py`: Orchestrator logic for the chatbot.
  - `sub_agents/`: Contains specialized agents for query rewriting and weather data handling.
  - `tools/`: Utility functions and constants.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```env
   GCP_PROJECT_ID=<your-gcp-project-id>
   GCP_REGION=<your-gcp-region>
   OPEN_METEO_API_KEY=<your-api-key>
   ```
5. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage

- Open the Streamlit application in your browser.
- Interact with the chatbot to get weather updates and detailed reports.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

## Sample Output File

- The project includes a sample output file (`Weather_Chatbot_sample_output.pdf`) located in the root folder. This file demonstrates the structure and format of the weather data provided by the chatbot.
- Use this file as a reference for understanding the chatbot's response format and for testing purposes.
