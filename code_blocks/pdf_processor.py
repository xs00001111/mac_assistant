# code_blocks/pdf_processor.py
import os
import httpx
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class PDFAnalysisResult(BaseModel):
    """Structure for PDF analysis results"""
    summary: str = Field(..., description="Concise document summary")
    key_points: List[str] = Field(..., description="List of key points")
    document_type: str = Field(..., description="Type of document")
    warnings: Optional[List[str]] = Field(None, description="Potential issues")

class PDFProcessor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel('gemini-2.0-flash-001')
        self.file_service = genai.FilesService()

    def process_pdf(self, source: str) -> PDFAnalysisResult:
        """Handle both local and remote PDF files"""
        if source.startswith(('http://', 'https://')):
            return self._process_remote_pdf(source)
        else:
            return self._process_local_pdf(source)

    def _process_local_pdf(self, file_path: str) -> PDFAnalysisResult:
        """Handle local PDF files with File API"""
        try:
            # Upload file with metadata
            uploaded_file = self.file_service.create(
                file=genai.upload_file(file_path),
                display_name=Path(file_path).name,
                mime_type='application/pdf'
            )
            
            return self._analyze_content(uploaded_file.uri)
            
        except genai.BadRequestException as e:
            if "PDF_TOO_LARGE" in str(e):
                raise ValueError("PDF exceeds 50MB limit") from e
            raise

    def _process_remote_pdf(self, url: str) -> PDFAnalysisResult:
        """Handle remote PDF files directly"""
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
            
            return self._analyze_content(
                file_data={
                    "mime_type": "application/pdf",
                    "data": response.content
                }
            )
            
        except httpx.HTTPError as e:
            raise ConnectionError(f"Failed to download PDF: {str(e)}") from e

    def _analyze_content(self, content_source) -> PDFAnalysisResult:
        """Common analysis logic"""
        try:
            response = self.client.generate_content(
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": "Analyze this document and provide structured insights"},
                            content_source
                        ]
                    }
                ],
                generation_config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                    "response_schema": PDFAnalysisResult.schema()
                }
            )

            if response.candidates[0].finish_reason == "STOP":
                return PDFAnalysisResult.parse_raw(response.text)
                
            raise RuntimeError(f"Analysis failed: {response.candidates[0].finish_reason}")
            
        except genai.APIConnectionError as e:
            raise ConnectionError("API connection failed") from e
        except genai.RateLimitError as e:
            raise RuntimeError("API rate limit exceeded") from e