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
