"""
FOLIO Platform - Multimedia & Document Processing Utilities.
Handles PDF, Word (.docx), HTML, TXT text extraction & chunking,
as well as video frame sampling and image processing.
"""

import os
import io
import re
import zipfile
import base64
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import List, Optional, Union, Tuple
from PIL import Image

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None

try:
    import cv2
except ImportError:
    cv2 = None

import streamlit as st


class HTMLTextExtractor(HTMLParser):
    """Clean plain-text extractor from HTML documents."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._ignore = False

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "head"]:
            self._ignore = True
        elif tag in ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "div", "br"]:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ["script", "style", "head"]:
            self._ignore = False
        elif tag in ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "div"]:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if not self._ignore:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned + " ")

    def get_text(self) -> str:
        raw = "".join(self.text_parts)
        # Collapse multiple newlines
        return re.sub(r'\n\s*\n', '\n\n', raw).strip()


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    """Splits raw text into overlapping semantic chunks."""
    if not text or not text.strip():
        return []
    chunks = []
    step = max(100, chunk_size - chunk_overlap)
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def process_pdf(uploaded_file, chunk_size: int = 1000, chunk_overlap: int = 150) -> Optional[List[str]]:
    """Extracts text from a PDF and splits it into overlapping semantic chunks."""
    if PdfReader is None:
        st.error("PDF processing library (pypdf/PyPDF2) is not installed.")
        return None

    text = ""
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        pdf_reader = PdfReader(uploaded_file)
        
        for page_idx, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text += f"\n[Page {page_idx + 1}]\n" + page_text.strip() + "\n"
        
        if not text.strip():
            st.warning("No readable text found in PDF. Scanned images may require OCR.")
            return []
            
        return chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return None


def process_docx(uploaded_file, chunk_size: int = 1000, chunk_overlap: int = 150) -> Optional[List[str]]:
    """Extracts text from a Word document (.docx) and splits it into semantic chunks."""
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        
        file_bytes = uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file
        bio = io.BytesIO(file_bytes)
        
        with zipfile.ZipFile(bio) as docx_zip:
            xml_content = docx_zip.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Extract paragraphs
            paragraphs = []
            # WordprocessingML namespace
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            for p in tree.iterfind('.//w:p', ns):
                texts = [node.text for node in p.iterfind('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            
            full_text = '\n\n'.join(paragraphs)
            return chunk_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    except Exception as e:
        st.error(f"Failed to read Word (.docx) document: {e}")
        return None


def process_html(uploaded_file, chunk_size: int = 1000, chunk_overlap: int = 150) -> Optional[List[str]]:
    """Extracts clean text from an HTML document and splits it into semantic chunks."""
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
            
        raw_bytes = uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file
        try:
            html_content = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            html_content = raw_bytes.decode('latin-1', errors='ignore')
            
        parser = HTMLTextExtractor()
        parser.feed(html_content)
        plain_text = parser.get_text()
        
        return chunk_text(plain_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    except Exception as e:
        st.error(f"Failed to read HTML document: {e}")
        return None


def process_txt(uploaded_file, chunk_size: int = 1000, chunk_overlap: int = 150) -> Optional[List[str]]:
    """Extracts text from a plain text (.txt / .md) document and splits it into semantic chunks."""
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
            
        raw_bytes = uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file
        try:
            plain_text = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            plain_text = raw_bytes.decode('latin-1', errors='ignore')
            
        return chunk_text(plain_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    except Exception as e:
        st.error(f"Failed to read text document: {e}")
        return None


def process_document_by_type(uploaded_file, filename: str) -> Tuple[Optional[List[str]], str]:
    """
    Unified router to extract chunks and full text from PDF, Word (.docx), HTML, or TXT.
    Returns: (chunks, extracted_full_text)
    """
    fn = filename.lower()
    chunks = None
    
    if fn.endswith('.pdf'):
        chunks = process_pdf(uploaded_file)
    elif fn.endswith(('.docx', '.doc')):
        chunks = process_docx(uploaded_file)
    elif fn.endswith(('.html', '.htm')):
        chunks = process_html(uploaded_file)
    elif fn.endswith(('.txt', '.md', '.rtf', '.csv', '.tsv')):
        chunks = process_txt(uploaded_file)
    else:
        # Generic text fallback
        chunks = process_txt(uploaded_file)
        
    full_text = "\n\n".join(chunks) if chunks else ""
    return chunks, full_text


def process_video(uploaded_file, interval_seconds: int = 5) -> List[Image.Image]:
    """Extracts key frames from a video file at regular time intervals."""
    if cv2 is None:
        st.error("OpenCV (cv2) is not installed. Video frame extraction requires opencv-python.")
        return []

    frames = []
    suffix = ".mp4"
    if hasattr(uploaded_file, "name") and "." in uploaded_file.name:
        suffix = "." + uploaded_file.name.split(".")[-1]

    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tfile:
        tfile.write(uploaded_file.read())
        temp_file_path = tfile.name

    video_capture = None
    try:
        video_capture = cv2.VideoCapture(temp_file_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        if not fps or fps <= 0:
            fps = 30.0
            
        frame_interval = int(fps * interval_seconds)
        if frame_interval <= 0:
            frame_interval = 30
            
        frame_count = 0
        max_frames = 20  # Safeguard to prevent memory exhaustion
        
        while video_capture.isOpened() and len(frames) < max_frames:
            ret, frame = video_capture.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                pil_img.thumbnail((800, 800))
                frames.append(pil_img)
            frame_count += 1
    except Exception as e:
        st.error(f"Failed to process video: {e}")
    finally:
        if video_capture is not None:
            video_capture.release()
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

    return frames


def process_image(uploaded_file) -> Optional[Image.Image]:
    """Opens and normalizes an uploaded image file."""
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img
    except Exception as e:
        st.error(f"Failed to load image: {e}")
        return None


def encode_image_to_base64(image_or_file: Union[Image.Image, io.BytesIO, bytes], format: str = "JPEG") -> str:
    """Encodes a PIL image or bytes into a base64 Data URI string for OpenRouter/OpenAI vision models."""
    if isinstance(image_or_file, bytes):
        b64_str = base64.b64encode(image_or_file).decode("utf-8")
        return f"data:image/jpeg;base64,{b64_str}"
        
    if isinstance(image_or_file, Image.Image):
        buffered = io.BytesIO()
        image_or_file.save(buffered, format=format)
        b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64_str}"
        
    if hasattr(image_or_file, "read"):
        if hasattr(image_or_file, "seek"):
            image_or_file.seek(0)
        b64_str = base64.b64encode(image_or_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64_str}"
        
    return ""
