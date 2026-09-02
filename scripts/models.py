"""
models.py
---------
Core Pydantic v2 data models for StackDiff pSEO Engine.
Defines strict schema and validation for AI tool specifications.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator
import re


class AITool(BaseModel):
    """
    Data model representing a single AI tool specification
    optimized for programmatic SEO (pSEO) comparison and landing page generation.
    """
    id: str = Field(
        ...,
        description="Unique identifier code (e.g., 'elevenlabs', 'cursor')",
        examples=["elevenlabs", "cursor"]
    )
    name: str = Field(
        ...,
        description="Official display name of the tool (e.g., 'ElevenLabs')",
        examples=["ElevenLabs", "Claude 3.5 Sonnet"]
    )
    slug: str = Field(
        ...,
        description="URL-safe slug for pSEO routing (e.g., 'elevenlabs')",
        examples=["elevenlabs", "claude-3-5-sonnet"]
    )
    category: str = Field(
        ...,
        description="Primary functional category (e.g., 'Voice AI', 'Video AI', 'Coding AI', 'LLM')",
        examples=["Voice AI", "Coding AI", "LLM"]
    )
    tagline: str = Field(
        ...,
        description="One-sentence value proposition for meta descriptions and header tags",
        examples=["Industry-leading AI voice generator and voice cloning platform"]
    )
    pricing_model: str = Field(
        ...,
        description="High-level pricing taxonomy (e.g., 'Freemium', 'Paid Only', 'Free & Open Source')",
        examples=["Freemium", "Paid Only", "Free & Open Source"]
    )
    starting_price: str = Field(
        ...,
        description="Entry-level price point (e.g., '$5/mo', '$0', '$20/mo')",
        examples=["$5/mo", "$0", "$20/mo"]
    )
    free_tier: bool = Field(
        ...,
        description="Whether a permanent free tier or recurring free trial quota is provided"
    )
    best_for: str = Field(
        ...,
        description="Target audience / primary ideal customer profile (ICP)",
        examples=["Creators looking for ultra-realistic voice acting"]
    )
    key_features: List[str] = Field(
        ...,
        min_length=3,
        description="List of 4-6 distinct technical/functional capabilities"
    )
    pros: List[str] = Field(
        ...,
        min_length=2,
        description="List of 3-4 core advantages and differentiators"
    )
    cons: List[str] = Field(
        ...,
        min_length=2,
        description="List of 2-3 trade-offs, constraints, or drawbacks"
    )
    supported_platforms: List[str] = Field(
        ...,
        min_length=1,
        description="List of supported environments (e.g., ['Web', 'API', 'Mac', 'Windows'])"
    )
    affiliate_url: str = Field(
        ...,
        description="Official landing page or affiliate placeholder tracking URL"
    )

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
        if not re.match(pattern, v):
            raise ValueError(f"Slug '{v}' must be lowercase alphanumeric with optional single hyphens")
        return v

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"ID '{v}' must be alphanumeric, hyphens, or underscores")
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "id": "elevenlabs",
                "name": "ElevenLabs",
                "slug": "elevenlabs",
                "category": "Voice AI",
                "tagline": "Industry-leading AI voice generator and voice cloning platform",
                "pricing_model": "Freemium",
                "starting_price": "$5/mo",
                "free_tier": True,
                "best_for": "Creators looking for ultra-realistic voice acting",
                "key_features": [
                    "Instant & Professional Voice Cloning",
                    "Multilingual Text-to-Speech (32+ languages)",
                    "AI Dubbing and Video Translation",
                    "Text to Sound Effects Generation"
                ],
                "pros": [
                    "Unmatched emotional nuance and voice naturalness",
                    "Vibrant community voice library",
                    "Robust low-latency developer API"
                ],
                "cons": [
                    "Character usage tiers can get expensive quickly",
                    "Occasional hallucinated accents on niche languages"
                ],
                "supported_platforms": ["Web", "API", "iOS", "Android"],
                "affiliate_url": "https://elevenlabs.io/?via=stackdiff"
            }
        }
