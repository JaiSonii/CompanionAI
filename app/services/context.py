from app.config import settings
from langchain_core.messages import BaseMessage
from app.services.summarizer import Summarizer
import asyncio

class Context:
    def __init__(self):
        self._max_size = settings.CONTEXT_WINDOW
        self._history: list[BaseMessage] = []
        self._evicted: list[BaseMessage] = []
        self.summary = ""
        self._summarizer = Summarizer(model=settings.SUMMARIZATION_MODEL)

    def _summarize(self):
        if not self._evicted:
            return

        async def summarize_evicted():
            return await self._summarizer.invoke(messages=self._evicted)

        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(summarize_evicted())
            task.add_done_callback(lambda t: setattr(self, "summary", t.result().get("output", "")))
        except RuntimeError:
            result = asyncio.run(summarize_evicted())
            self.summary = result.get("output", "")

        self._evicted = []

    def __iadd__(self, message: BaseMessage) -> "Context":
        self._history.append(message)
        if len(self._history) > self._max_size:
            self._evicted.append(self._history.pop(0))

        if len(self._evicted) >= self._max_size // 2:
            self._summarize()

        return self

    @property
    def history(self) -> dict:
        return {
            "history": [msg.model_dump() for msg in self._history],
            "summary": self.summary
        }
