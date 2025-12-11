from app.services.base_ai import BaseAI
from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from ..context import Context
from .prompts import PERSONAS

class PersonalityEngine(BaseAI):
    def __init__(self, model: str, persona : str) -> None:
        super().__init__(model)
        self.persona_prompt = PERSONAS.get(persona)
        self._context: Context = Context()

    def _build_messages(self)->List[BaseMessage]:
        context_data = self._context.history
        system_prompt = SystemMessage(content=self.persona_prompt)
        history_msgs = []
        for msg in context_data.get("history", []):
            if msg.get('type') == 'human':
                history_msgs.append(HumanMessage(content=msg.get('content')))
            elif msg.get('type') == 'ai':
                history_msgs.append(AIMessage(content=msg.get('content')))
        messages: list[BaseMessage] = [
            system_prompt,
            HumanMessage(content=f"Context Summary: {context_data['summary']}"),
            *history_msgs
        ]
        return messages

    async def invoke(self, **kwargs):
        user_message = kwargs.get('user_message', None)
        if user_message is None:
            raise ValueError("user_message is required")
        self._context += user_message
        messages = self._build_messages()
        response = await self._model.ainvoke(input=messages)
        self._context += response
        return response
        
