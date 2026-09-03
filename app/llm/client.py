import os
import json
import asyncio
from pathlib import Path
from openai import AsyncOpenAI, APIError, RateLimitError, APITimeoutError
from app.llm.schemas import EnrichRequest, EnrichResponse, BookCategory

# Load versioned prompt template
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "enrich-v1.md"

def load_system_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return """You are a precise book classification assistant.
Return valid JSON with keys: category, confidence, themes, one_sentence_summary, quality_flags.
Valid categories are: Software Engineering, Non-Fiction, Fiction, Self-Help, Other."""

async def call_llm_enrichment(payload: EnrichRequest) -> tuple[EnrichResponse, dict]:
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY", "missing_key")
    base_url = os.getenv("LLM_BASE_URL")
    
    client = AsyncOpenAI(
        base_url=base_url if base_url else None,
        api_key=api_key,
        timeout=30.0
    )

    system_prompt = load_system_prompt()
    user_prompt = f"Title: {payload.title}\nDescription: {payload.description}"

    max_retries = 2
    delay = 1.0

    for attempt in range(max_retries + 1):
        try:
            raw_response = await client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "openrouter/free"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            break
            
        except (RateLimitError, APITimeoutError) as e:
            if attempt == max_retries:
                raise Exception("Upstream LLM timed out or hit rate limits.") from e
            await asyncio.sleep(delay)
            delay *= 2
            
        except APIError as e:
            if getattr(e, "status_code", None) in [400, 401, 403]:
                raise ValueError(f"Non-retryable LLM error ({e.status_code}): {e.message}") from e
            if attempt == max_retries:
                raise Exception("Upstream LLM provider failed after retries.") from e
            await asyncio.sleep(delay)

    # Extract usage metrics
    usage = raw_response.usage
    usage_data = {
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "repair_count": 0
    }

    # Extract content and parse into Pydantic schema
    content = raw_response.choices[0].message.content
    try:
        parsed_json = json.loads(content)

        # Normalize category field to prevent None or missing values
        valid_categories = [c.value for c in BookCategory]
        category_val = parsed_json.get("category")

        if not category_val or category_val not in valid_categories:
            parsed_json["category"] = BookCategory.OTHER.value
            parsed_json["confidence"] = min(float(parsed_json.get("confidence", 0.3)), 0.4)
            flags = parsed_json.get("quality_flags", [])
            if "fallback_category" not in flags:
                flags.append("fallback_category")
            parsed_json["quality_flags"] = flags

        parsed_response = EnrichResponse(**parsed_json)

    except Exception as e:
        # Quarantine raw payload if structure is completely unparseable
        quarantine_path = Path("logs/quarantine.jsonl")
        quarantine_path.parent.mkdir(parents=True, exist_ok=True)
        with open(quarantine_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"input": payload.model_dump(), "raw_output": content, "error": str(e)}) + "\n")
        
        # Fallback response for malformed JSON output
        parsed_response = EnrichResponse(
            category=BookCategory.OTHER,
            confidence=0.1,
            themes=["unstructured"],
            one_sentence_summary="Unable to parse structured metadata.",
            quality_flags=["json_parse_fallback"]
        )

    return parsed_response, usage_data