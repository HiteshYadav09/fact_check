"""
verifier.py - Core fact-checking logic using OpenAI API.
Orchestrates search + AI analysis to produce structured verdicts.
"""

import os
import json
from typing import Optional
from openai import OpenAI

from search import search_claim, format_search_results
from prompts import SYSTEM_PROMPT, build_analysis_prompt


# Verdict color mapping for UI
VERDICT_CONFIG = {
    "TRUE": {
        "color": "#22c55e",
        "bg": "#052e16",
        "border": "#16a34a",
        "emoji": "✅",
        "label": "TRUE",
    },
    "FALSE": {
        "color": "#ef4444",
        "bg": "#2d0a0a",
        "border": "#dc2626",
        "emoji": "❌",
        "label": "FALSE",
    },
    "MISLEADING": {
        "color": "#f97316",
        "bg": "#1c0f02",
        "border": "#ea580c",
        "emoji": "⚠️",
        "label": "MISLEADING",
    },
    "PARTIALLY TRUE": {
        "color": "#eab308",
        "bg": "#1c1500",
        "border": "#ca8a04",
        "emoji": "🔶",
        "label": "PARTIALLY TRUE",
    },
    "UNVERIFIED": {
        "color": "#94a3b8",
        "bg": "#0f172a",
        "border": "#475569",
        "emoji": "❓",
        "label": "UNVERIFIED",
    },
    "SATIRE": {
        "color": "#a855f7",
        "bg": "#1a0533",
        "border": "#9333ea",
        "emoji": "🎭",
        "label": "SATIRE",
    },
}


def verify_claim(claim: str) -> dict:
    """
    Full pipeline: search → analyze → return structured result.

    Args:
        claim: The claim or statement to fact-check

    Returns:
        dict with verdict, confidence, explanation, sources, etc.
    """
    # Step 1: Validate input
    claim = claim.strip()
    if not claim:
        raise ValueError("Please enter a claim to verify.")
    if len(claim) < 10:
        raise ValueError("Claim is too short. Please provide more detail.")
    if len(claim) > 2000:
        raise ValueError("Claim is too long. Please limit to 2000 characters.")

    # Step 2: Search for evidence
    try:
        search_data = search_claim(claim)
    except RuntimeError as e:
        raise RuntimeError(f"Search failed: {str(e)}")

    # Step 3: Format evidence for AI
    formatted_evidence = format_search_results(search_data)

    # Step 4: Analyze with OpenAI
    analysis = analyze_with_openai(claim, formatted_evidence)

    # Step 5: Attach source metadata
    analysis["sources"] = search_data.get("results", [])
    analysis["search_query"] = claim

    return analysis


def analyze_with_openai(claim: str, evidence: str) -> dict:
    """
    Send claim + evidence to OpenAI for structured analysis.

    Args:
        claim: The original claim
        evidence: Formatted search results

    Returns:
        Parsed analysis dict
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=api_key)

    prompt = build_analysis_prompt(claim, evidence)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,  # Low temperature for factual consistency
            max_tokens=1500,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        result = json.loads(raw)

        # Normalize verdict to uppercase
        result["verdict"] = result.get("verdict", "UNVERIFIED").upper()

        # Clamp confidence score
        score = result.get("confidence_score", 50)
        result["confidence_score"] = max(0, min(100, int(score)))

        # Attach verdict config for UI
        verdict = result["verdict"]
        result["verdict_config"] = VERDICT_CONFIG.get(
            verdict, VERDICT_CONFIG["UNVERIFIED"]
        )

        return result

    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "verdict": "UNVERIFIED",
            "confidence_score": 0,
            "summary": "Analysis could not be completed due to a processing error.",
            "detailed_explanation": "The AI response could not be parsed correctly. Please try again.",
            "key_evidence": [],
            "source_reliability": "Unknown",
            "final_conclusion": "Unable to verify claim at this time.",
            "reasoning_steps": [],
            "verdict_config": VERDICT_CONFIG["UNVERIFIED"],
        }
    except Exception as e:
        raise RuntimeError(f"OpenAI analysis failed: {str(e)}")
