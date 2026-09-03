import os
from fastapi import APIRouter, HTTPException, status
from app.llm.schemas import EnrichRequest, EnrichResponse, BookCategory
from app.llm.client import call_llm_enrichment

router = APIRouter(prefix="/enrich", tags=["LLM Enrichment"])

@router.post("", response_model=EnrichResponse)
async def enrich_book(payload: EnrichRequest):
    # Kill Switch Check
    if os.getenv("LLM_ENABLED", "true").lower() == "false":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM feature is currently disabled."
        )

    # Stub Mode Check
    if os.getenv("LLM_STUB", "0") == "1":
        return EnrichResponse(
            category=BookCategory.FICTION,
            confidence=0.98,
            themes=["classic", "dystopian"],
            one_sentence_summary=f"A quick summary for '{payload.title}'.",
            quality_flags=["stub_data"]
        )

    # Live Execution
    try:
        response, usage_data = await call_llm_enrichment(payload)
        
        # Log cost metrics
        print(f"[COST LOG] Model: {os.getenv('LLM_MODEL')} | Prompt Tokens: {usage_data['prompt_tokens']} | Completion Tokens: {usage_data['completion_tokens']} | Repair Retries: {usage_data['repair_count']}")
        
        return response
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err)
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM processing failed: {str(err)}"
        )