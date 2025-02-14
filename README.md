How to Run:
Install required libraries:
pip install PyQt5 pyinstaller langchain-openai browser-use mlx-use python-dotenv

Create an .env file and enter your OPENAI and GEMINI API KEY 
OPENAI_API_KEY= [Your Key]
GEMINI_API_KEY=[your key]


Run the application:

python agent_ui.py


For Packaging into Executable (Optional): To package the script into a standalone macOS app:
pyinstaller --onefile --windowed agent_ui.py

<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/9fe8c4740ef74b45a6e4e5eeb8338b68?sid=e18c4512-164b-4c39-8529-67501bb90eb5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

