# College Finder Chatbot

## Overview
The **College Finder Chatbot** is an intelligent AI-powered chatbot designed to help students find the best colleges based on their preferences. Using various Large Language Models (LLMs) such as Gemini, ChatGPT, Flan-T5, phi3 model to convert natural language queries into SQL queries. The chatbot is built with **Streamlit** for an interactive and user-friendly interface.

## Features
- **Natural Language Processing:** Converts user queries into SQL commands dynamically.
- **Multiple LLMs Supported:** Uses Gemini, ChatGPT, Flan-T5, and llama model for query understanding.
- **Dynamic Filtering:** Searches a CSV dataset containing 57 rows with multiple parameters (e.g., Name, GPA, Package, etc.).
- **Streamlit UI:** Provides an interactive web-based chatbot experience.

## Tech Stack
- **Python**
- **Streamlit** (for UI development)
- **LLM APIs** (Gemini, ChatGPT, Flan-T5,Llama and some other failed to giving right output)
- **SQL** (for structured queries)
- **Pandas** (for CSV data handling)


## Video Demonstration



https://github.com/user-attachments/assets/c51cb500-b2a2-4884-a022-10316c89f6eb




## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/college-finder-chatbot.git
   cd college-finder-chatbot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```sh
   python -m streamlit run app.py
   ```

## Usage
1. Open the chatbot interface in a browser.
2. Enter your query in natural language (e.g., *"Find me universities that accept a GPA above 3.5 with a high placement package"*).
3. The chatbot converts the query into SQL and fetches relevant results from the dataset.
4. View the results in a user-friendly format.


## Future Enhancements
- Integrating more LLMs for better query understanding.
- Expanding the dataset to include more universities and parameters.
- Deploying the chatbot as a web service.

## Contributing
Feel free to open issues or submit pull requests to improve the chatbot.

## License
This project is licensed under the MIT License.
## IMPORTANT
The given data by this application is not Authentic , As this data(in csv)was created by ai and contains error in differet locations but it was just created to learn and implement my project 

