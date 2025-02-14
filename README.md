#Demo
```html
<div style="position: relative; padding-bottom: 62.5%; height: 0;"> <iframe src="https://www.loom.com/embed/9fe8c4740ef74b45a6e4e5eeb8338b68?sid=e18c4512-164b-4c39-8529-67501bb90eb5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe> </div>
```


# Application Setup and Usage

This application provides an easy-to-use interface to interact with agents and APIs. Follow the steps below to set up and run the application, and optionally package it into a standalone executable for macOS.

## How to Run

### Step 1: Install Required Libraries

To get started, install the necessary libraries by running the following command:

```bash
pip install PyQt5 pyinstaller langchain-openai browser-use mlx-use python-dotenv
```

### Step 2: Create .env file 

OPENAI_API_KEY=[Your OpenAI Key]
GEMINI_API_KEY=[Your Gemini Key]


### Step 3: Run application

```bash
python agent_ui.py

```
