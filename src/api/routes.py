import os
import markdown
from fastapi import APIRouter, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from src.graph import acis_engine
from src.reporter import generate_pdf_report

router = APIRouter()

# Tell FastAPI where your HTML files live
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def load_dashboard(request: Request):
    """Loads the initial empty dashboard."""
    # FIXED: Explicitly declare request and name
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@router.post("/", response_class=HTMLResponse)
async def run_intelligence_cycle(request: Request, topic: str = Form(...)):
    """Receives the form submission, runs the AI, and returns the finished page."""
    if not topic.strip():
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={"error": "Directive cannot be empty."}
        )

    initial_state = {
        "research_topic": topic,
        "scraped_raw_data": [],
        "structured_analytics": [],
        "current_report_draft": "",
        "critic_feedback": [],
        "loop_count": 0
    }

    try:
        # 1. Run the Multi-Agent Loop
        final_state = acis_engine.invoke(initial_state)
        markdown_output = final_state["current_report_draft"]
        
        # 2. Generate PDF
        pdf_filename = generate_pdf_report(markdown_output, topic)

        # 3. Convert Markdown to HTML natively in Python
        html_content = markdown.markdown(markdown_output)

        # 4. Inject the results back into the HTML template
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={
                "topic": topic,
                "result_html": html_content,
                "pdf_url": f"/download/{pdf_filename}"
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={"error": str(e)}
        )

@router.get("/download/{filename}")
def download_pdf(filename: str):
    """Serves the generated PDF file."""
    if not os.path.exists(filename):
        return HTMLResponse("File not found.", status_code=404)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.get("/test")
async def test_route():
    return {"message": "test commit"}