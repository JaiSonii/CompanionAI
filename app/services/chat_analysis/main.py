from app.services.base_ai import BaseAI
from langchain_google_genai import ChatGoogleGenerativeAI
from .models import StructuredChatAnalysis
from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from .prompts import CHAT_ANALYSIS_SYSTEM_PROMPT, CHAT_ANALYSIS_HUMAN_PROMPT

class ChatAnalysis(BaseAI):
    def __init__(self, model: str) -> None:
        super().__init__(model, StructuredChatAnalysis)

    def _build_messages(self, chat_history: List[dict])->List[BaseMessage]:
        messages: List[BaseMessage] = [
            SystemMessage(content=CHAT_ANALYSIS_SYSTEM_PROMPT),
            HumanMessage(content=CHAT_ANALYSIS_HUMAN_PROMPT.format(chat_history=chat_history))
        ]
        return messages

    async def invoke(self, **kwargs):
        chat_history = kwargs.get("chat_history", [])
        if not chat_history:
            raise ValueError("chat_history is required")
        
        messages: List[BaseMessage] = self._build_messages(chat_history)
        return await self._model.ainvoke(input=messages)