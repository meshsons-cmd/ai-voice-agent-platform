import json
from openai import OpenAI
from app.core.config import get_settings
from app.tools.registry import TOOL_DEFINITIONS, execute_tool

class OpenAIProvider:
    def __init__(self):
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def respond(self, messages):
        calls = []
        working = list(messages)
        for _ in range(4):
            response = self.client.chat.completions.create(
                model=self.model, messages=working, tools=TOOL_DEFINITIONS, tool_choice="auto"
            )
            message = response.choices[0].message
            if not message.tool_calls:
                return message.content or "", calls
            working.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                try:
                    output = execute_tool(call.function.name, json.loads(call.function.arguments or "{}"))
                except Exception as exc:
                    output = {"error": str(exc)}
                calls.append(call.function.name)
                working.append({"role":"tool","tool_call_id":call.id,"content":json.dumps(output)})
        return "Tool-call limit reached; please try a simpler request.", calls
