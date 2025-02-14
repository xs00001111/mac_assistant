How to Run:
Install required libraries:

bash
Copy
pip install PyQt5 pyinstaller langchain-openai browser-use mlx-use python-dotenv
Run the application:

bash
Copy
python agent_ui.py
For Packaging into Executable (Optional): To package the script into a standalone macOS app:

bash
Copy
pyinstaller --onefile --windowed agent_ui.py
