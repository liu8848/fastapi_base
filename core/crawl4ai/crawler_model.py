from enum import Enum
from typing import List,Any,Union,Dict,Optional
from pydantic import BaseModel,HttpUrl,Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class CrawlerType(str, Enum):
    BASIC = "basic"
    LLM = "llm"
    COSINE = "cosine"
    JSON_CSS = "json_css"

class ExtractionConfig(BaseModel):
    type: CrawlerType
    params: Dict[str, Any] = None

class CrawlRequest(BaseModel):
    urls: Union[HttpUrl, List[HttpUrl]]
    extraction_config: Optional[ExtractionConfig] = None
    crawler_params: Dict[str, Any] = None
    priority: int = Field(default=5, ge=1, le=10)
    ttl: Optional[int] = 3600
    js_code: Optional[List[str]] = None
    wait_for: Optional[str] = None
    css_selector: Optional[str] = None
    screenshot: bool = False
    magic: bool = False
    extra: Optional[Dict[str, Any]] = None

class UrlModel(BaseModel):
    url: HttpUrl
    forced: bool = False

class CrawlResult(BaseModel):
    url: str
    html: str
    success: bool
    cleaned_html: Optional[str] = None
    media: Dict[str, List[Dict]] = None
    links: Dict[str, List[Dict]] = None
    screenshot: Optional[str] = None
    markdown: Optional[str] = None
    fit_markdown: Optional[str] = None
    fit_html: Optional[str] = None
    extracted_content: Optional[str] = None
    metadata: Optional[dict] = None
    error_message: Optional[str] = None
    session_id: Optional[str] = None
    response_headers: Optional[dict] = None
    status_code: Optional[int] = None