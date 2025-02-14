## Introduction

This project is focused on building a macOS AI agent that leverages both local software and web capabilities. It is powered by [browser-use](https://github.com/browser-use/browser-use) and [macOS-use](https://github.com/browser-use/macOS-use). Currently, the agent supports OpenAI and GEMINI API keys, with plans to soon support local LLMs running with Ollama. 

The AI agent is particularly effective at performing simple tasks such as clicking buttons on the web and in applications, thanks to its strong integration with the DOM tree and OS accessibility. However, its ability to perform operations on files like Google Docs and PDFs is currently limited. Future updates will allow the AI to leverage additional tools to improve its performance in these areas.


#Demo

[![Agent UI use Calculator](https://cdn.loom.com/sessions/thumbnails/9fe8c4740ef74b45a6e4e5eeb8338b68-0b5c1fd76d8732f4-full-play.gif)](https://www.loom.com/share/9fe8c4740ef74b45a6e4e5eeb8338b68)

<p style="text-align:center;margin-top:10px;">
  <a href="https://www.loom.com/share/9fe8c4740ef74b45a6e4e5eeb8338b68" target="_blank">
    🔗 Click to View full Video
  </a>
</p>



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
