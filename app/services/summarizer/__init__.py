from app.services.base_ai import BaseAI
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage

class Summarizer(BaseAI):
    def __init__(self, model: str):
        super().__init__(model)

    def _build_messages(self, messages: list[BaseMessage], summary:str) -> list[BaseMessage]:
        system_prompt = SystemMessage(content="You are a summarization engine.You will get the summary till now and the further conversations after it. Summarize the following conversation succinctly.")
        formatted = "\n".join(
            f"{msg.__class__.__name__.replace('Message', '')}: {msg.content}"
            for msg in messages
        )
        message_list: list[BaseMessage] = [
            system_prompt,
            AIMessage(content=f"Summary till now: {summary}"),
            HumanMessage(content=f"Further conversations:\n{formatted}"),
        ]
        return message_list

    async def invoke(self, **kwargs):
        evicted_messages: list[BaseMessage] = kwargs.get("messages", []) 
        summary_till_now: str = kwargs.get("summary", "")
        if not evicted_messages:
            raise ValueError("messages are required for summarization")
        messages = self._build_messages(evicted_messages, summary_till_now)
        return await self._model.ainvoke(input=messages)