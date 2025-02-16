# code_blocks/pdf_processor.py
import os
import httpx
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

class PDFAnalysisResult(BaseModel):
    """Structure for PDF analysis results"""
    summary: str = Field(..., description="Concise document summary")
    key_points: List[str] = Field(..., description="List of key points")
    document_type: str = Field(..., description="Type of document")
    warnings: Optional[List[str]] = Field(None, description="Potential issues")



@dataclass
class PDFContentResult:
    """
    PDF处理结果数据类
    包含DeepSeek-R1项目中的文档分析经验（见知识库内容1）
    """
    content_type: str  # 内容类型：full_text/summary/table
    pages: int         # 总页数
    content: str       # 实际内容（全文或摘要）
    summary: str       # 摘要（基于知识库内容2的摘要生成要求）
    key_points: List[str]  # 关键点列表
    warnings: List[str]    # 处理过程中的警告信息
    truncated: bool = False  # 内容是否被截断（参考知识库3中的长度控制）

    def to_dict(self) -> dict:
        """转换为字典格式（用于LLM输入）"""
        return {
            "content_type": self.content_type,
            "pages": self.pages,
            "content": self.content,
            "summary": self.summary,
            "key_points": self.key_points,
            "warnings": self.warnings,
            "truncated": self.truncated
        }

    @classmethod
    def create_error_result(cls, error_msg: str) -> "PDFContentResult":
        """创建错误结果（参考知识库4中的错误处理规范）"""
        return cls(
            content_type="error",
            pages=0,
            content="",
            summary=f"Processing Error: {error_msg}",
            key_points=[],
            warnings=[error_msg],
            truncated=False
        )


class PDFProcessor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel('gemini-2.0-flash-001')

    def process_pdf(self, file_path: str) -> PDFContentResult:
        try:
            # 实际处理逻辑...
            return PDFContentResult(
                content_type="full_text",
                pages=42,
                content=extracted_text,
                summary=generate_summary(extracted_text),
                key_points=extract_key_points(extracted_text),
                warnings=["Low resolution images detected"],
                truncated=len(extracted_text) > 5000
            )
        except Exception as e:
            return PDFContentResult.create_error_result(str(e))

    def _process_local_pdf(self, file_path: str) -> PDFAnalysisResult:
        """Handle local PDF files with File API"""
        try:
            # Upload file with metadata
            uploaded_file = genai.upload_file(path=file_path)
            
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