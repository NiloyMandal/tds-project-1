"""App routes module"""

from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse

from .models import Payload, EvaluationData
from .config import Environ
from .helpers import process_request

router = APIRouter()


@router.post("/build")
async def build(request: Payload, tasks: BackgroundTasks):
    """App build endpoint"""

    # Get and validate secret key
    secret_key = Environ.API_SECRET
    if not secret_key:
        raise ValueError("API_SECRET environment variable not set")

    if request.secret != secret_key:
        return JSONResponse(
            content={"message": "Unauthorized: Invalid secret key."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Process task in the background
    tasks.add_task(process_request, request)

    # Return a JSON response confirming receipt
    return JSONResponse(
        content={"message": "Request received. Buildling Application..."},
        status_code=status.HTTP_200_OK,
    )


@router.post("/_eval")
async def evaluate(evaluation_data: EvaluationData):
    """Evaluation endpoint to receive deployment results"""
    
    print(f"📊 Evaluation received for task: {evaluation_data.task}")
    print(f"📧 Email: {evaluation_data.email}")
    print(f"🔗 Repository: {evaluation_data.repo_url}")
    print(f"🌐 Live URL: {evaluation_data.pages_url}")
    print(f"📝 Commit: {evaluation_data.commit_sha}")
    print(f"🎯 Round: {evaluation_data.round}")
    print(f"🔑 Nonce: {evaluation_data.nonce}")
    
    # Here you could save to database, send notifications, etc.
    # For now, just acknowledge receipt
    
    return JSONResponse(
        content={
            "status": "success",
            "message": "Evaluation data received successfully",
            "task": evaluation_data.task,
            "pages_url": evaluation_data.pages_url
        },
        status_code=status.HTTP_200_OK,
    )
