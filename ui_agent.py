import sys
import os
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit, QRadioButton, QButtonGroup, QGroupBox, QFormLayout, QFileDialog
from PyQt5.QtCore import Qt
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from mlx_use import Agent as MlxAgent
from browser_use import Agent as BrowserAgent
from mlx_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from dotenv import load_dotenv, set_key
from code_blocks.read_pdf import read_pdf

# Load environment variables from .env file
load_dotenv()

# Set LLM provider
def set_llm(llm_provider: str = None):
    if not llm_provider:
        raise ValueError("No llm provider was set")

    if llm_provider == "OAI":
        try:
            api_key = os.getenv('OPENAI_API_KEY')
        except Exception as e:
            print(f"Error while getting API key: {e}")
            api_key = None
        return ChatOpenAI(model='gpt-4o', api_key=SecretStr(api_key))

    if llm_provider == "google":
        try:
            api_key = os.getenv('GEMINI_API_KEY')
        except Exception as e:
            print(f"Error while getting API key: {e}")
            api_key = None
        return ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

class AgentUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agent UI')

        # Main layout
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        # Task input field
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Enter the task...')
        self.task_input.setFixedHeight(40)  # Give it some height for better user experience

        # LLM provider selection dropdown
        self.llm_provider = QComboBox(self)
        self.llm_provider.addItem('google')
        self.llm_provider.addItem('OAI')

        # Web vs Mac selection using Radio Buttons
        self.web_radio = QRadioButton("Web (browser-use)", self)
        self.mac_radio = QRadioButton("Mac (mlx-use)", self)
        self.web_radio.setChecked(True)  # Default to web
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.web_radio)
        self.radio_group.addButton(self.mac_radio)

        # Run button
        self.run_button = QPushButton('Run Task', self)
        self.run_button.clicked.connect(self.run_task)

        # Output display area
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        # Adding widgets to layout
        input_layout.addWidget(QLabel('Select LLM Provider:'))
        input_layout.addWidget(self.llm_provider)

        layout.addWidget(QLabel('Enter Task:'))
        layout.addWidget(self.task_input)
        layout.addLayout(input_layout)

        layout.addWidget(QLabel('Choose Platform:'))
        layout.addWidget(self.web_radio)
        layout.addWidget(self.mac_radio)

        layout.addWidget(self.run_button)
        layout.addWidget(self.output_area)

        # Context Section (multi-line input)
        self.context_group = QGroupBox("Context (optional)", self)
        self.context_layout = QVBoxLayout(self.context_group)

        self.context_label = QLabel("Add more context on your tasks (for example, login needed, info to fill, etc.):", self)
        self.context_input = QTextEdit(self)
        self.context_input.setPlaceholderText("Add more context on your tasks, for example, log in needed, info to fill etc...")
        self.context_input.setFixedHeight(100)  # Give it a fixed height for context input

        self.context_layout.addWidget(self.context_label)
        self.context_layout.addWidget(self.context_input)

        # Initially hide context section
        self.context_group.setVisible(False)

        # Advanced Settings Button
        self.advanced_button = QPushButton('Advanced Settings', self)
        self.advanced_button.clicked.connect(self.toggle_advanced_settings)

        # Add everything to layout
        layout.addWidget(self.context_group)
        layout.addWidget(self.advanced_button)

        self.setLayout(layout)
        self.setGeometry(100, 100, 500, 600)

    def toggle_advanced_settings(self):
        # Toggle visibility of the context section
        current_visibility = self.context_group.isVisible()
        self.context_group.setVisible(not current_visibility)

    def run_task(self):
        task = self.task_input.text()
        llm_provider = self.llm_provider.currentText()
        context = self.context_input.toPlainText()  # Get the context input

        # Check if task involves PDF
        if 'pdf' in task.lower():
            # Open file dialog to select PDF
            pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF Files (*.pdf)")
            if pdf_path:
                pdf_content = read_pdf(pdf_path)
                task = f"{task}\nPDF Content: {pdf_content}"

        # Set LLM
        try:
            llm = set_llm(llm_provider)
        except Exception as e:
            self.output_area.setText(f"Error setting LLM: {e}")
            return

        # Append context to task prompt if provided
        if context:
            task = f"{task}\nContext: {context}"

        # Save user login details to .env file
        self.save_personal_info()

        # Determine platform (Web or Mac)
        if self.web_radio.isChecked():
            self.run_browser_task(task, llm)
        else:
            self.run_mac_task(task, llm)

    def run_browser_task(self, task, llm):
        async def run_browser_agent():
            try:
                browser = Browser(config=BrowserConfig(
                chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                disable_security=True,))
                agent = BrowserAgent(
                    task=task,
                    llm=llm,
                    browser=browser
                )
                result = await agent.run()
                self.output_area.append(f"Task completed: {result}")
            except Exception as e:
                self.output_area.append(f"Error running browser task: {e}")

        asyncio.run(run_browser_agent())

    def run_mac_task(self, task, llm):
        async def run_mac_agent():
            try:
                controller = Controller()
                agent = MlxAgent(
                    task=task,
                    llm=llm,
                    controller=controller,
                    use_vision=False,
                    max_actions_per_step=1,
                    max_failures=5
                )
                await agent.run(max_steps=25)
                self.output_area.append("Task completed successfully on macOS!")
            except Exception as e:
                self.output_area.append(f"Error running mac task: {e}")

        asyncio.run(run_mac_agent())

    def save_personal_info(self):
        context = self.context_input.toPlainText()  # Get multi-line context input

        # Save to .env file
        try:
            if context:
                set_key('.env', 'USER_CONTEXT', context)
            
            self.output_area.setText("Context info saved successfully!")
        except Exception as e:
            self.output_area.setText(f"Error saving context info: {e}")


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    agent_ui = AgentUI()
    agent_ui.show()
    sys.exit(app.exec_())