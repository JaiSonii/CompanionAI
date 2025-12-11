from pydantic import BaseModel, Field

class UserPreference(BaseModel):
    item: str = Field(..., description="The user preference item")
    reasoning: str = Field(..., description="Reasoning behind identifying this as a user preference")

class EmotionalPattern(BaseModel):
    pattern: str = Field(..., description="The emotional pattern identified")
    reasoning: str = Field(..., description="Reasoning behind identifying this emotional pattern")

class MemorableFact(BaseModel):
    fact: str = Field(..., description="The fact worth remembering")
    reasoning: str = Field(..., description="Reasoning behind identifying this fact as worth remembering")


class StructuredChatAnalysis(BaseModel):
    user_preferences: list[UserPreference] = Field(..., description="Extracted user preferences from the chat history")
    emotional_patterns: list[EmotionalPattern] = Field(..., description="Identified emotional patterns in the chat history")
    memorable_facts: list[MemorableFact] = Field(..., description="List of facts worth remembering from the chat history")
