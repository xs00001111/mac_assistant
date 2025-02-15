import PyPDF2

def read_pdf(pdf_path):
    """
    Read a PDF file and extract its text content.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content from the PDF
    """
    try:
        # Open the PDF file in binary read mode
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Initialize empty string to store text
            text_content = ""
            
            # Iterate through all pages and extract text
            for page in pdf_reader.pages:
                text_content += page.extract_text()
                
            return text_content
            
    except FileNotFoundError:
        return f"Error: The file {pdf_path} was not found."
    except Exception as e:
        return f"Error occurred while reading the PDF: {str(e)}"
