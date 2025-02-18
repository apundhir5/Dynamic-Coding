import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict, Iterator, List, Optional

from pydantic import Field
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.messages.ai import UsageMetadata
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.messages import HumanMessage
    

class NTTHWrapperChatLLM(BaseChatModel):
    """A custom Chat LLM that wraps the provided /auth/appLogin and /chat endpoints."""

    # Pydantic fields (with some default placeholders).
    # You can remove the defaults if you want them to be required at init time.
    id: str = Field("my-app-id", description="App login ID used for authentication.")
    secret: str = Field("my-secret", description="App secret used for authentication.")
    provider: str = Field("openai", description="Provider name.")
    model_name: str = Field("GPT-4o", description="Model name to use.")
    base_url: str = Field("https://api.ntth.ai/v1", description="Base API endpoint.")

    # These fields will be populated at runtime after login.
    token: str = Field("", exclude=True)
    model_id: str = Field("", exclude=True)

    # You can adjust Pydantic's config if needed. For example:
    class Config:
        # Either allow extra fields or forbid them, depending on your preference
        extra = "allow"

    def __init__(self, **kwargs: Any) -> None:
        """Use a Pydantic-compatible constructor and then do custom logic."""
        super().__init__(**kwargs)  # let Pydantic populate the fields

        # Now self.id, self.secret, etc. are available
        self.token = self._login()
        self.model_id = self._get_model_id(self.provider, self.model_name)
        # print('-------------------',self.token)
        # print('-------------------', self.model_id)

    def _login(self) -> str:
        """Authenticate and retrieve the token from the /auth/appLogin endpoint."""
        login_url = f"{self.base_url}/auth/appLogin"
        payload = {
            "id": self.id,
            "secret": self.secret,
        }
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        data = response.json()

        token = data.get("token")
        if not token:
            raise ValueError("No token found in response. Check API response format.")
        return token

    def _get_model_id(self, provider: str, model_name: str) -> str:
        """Get the model ID for a given provider and model name."""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/chat/models?provider={provider}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # print('----------getting model id----------------------', data)

        # Adjust this filter condition if needed:
        model_id = next((m["id"] for m in data if m["name"] == model_name), None)
        if not model_id:
            raise ValueError(f"No model id found for model_name='{model_name}'.")
        return model_id

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Send messages to the /chat endpoint and return a ChatResult."""
        chat_url = f"{self.base_url}/chat"

        # Convert LangChain messages -> your API's JSON structure
        api_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            else:
                role = "user"

            api_messages.append({"role": role, "content": msg.content})

        body = {
            "id": self.id,
            "modelId": self.model_id,
            "messages": api_messages,
            "maxTokens": 2000,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        resp = requests.post(chat_url, headers=headers, json=body)
        resp.raise_for_status()
        result = resp.json()

        # Suppose the response is { "role": "assistant", "content": "answer..." }
        content = result.get("content", "")
        # print('content-------------------------------', result)

        last_message = messages[-1]
        tokens = last_message.content[: 2]
        ct_input_tokens = sum(len(message.content) for message in messages)
        ct_output_tokens = len(tokens)

        ai_message = AIMessage(
            content=content,
            additional_kwargs={},
            usage_metadata={  
                # Add other usage metadata returned by the API
                "input_tokens": ct_input_tokens,
                "output_tokens": ct_output_tokens,
                "total_tokens": ct_input_tokens + ct_output_tokens,
            },
            response_metadata={},
        )

        generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[generation])

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """
        (Optional) Stream the output if your /chat endpoint supports SSE or partial responses.
        If not supported, you can remove or skip implementing this method.
        """
        # Example placeholder that simply yields one chunk
        # In a real implementation, you would read from a streaming endpoint.
        yield ChatGenerationChunk(
            message=AIMessageChunk(content="This model does not currently stream.")
        )

    @property
    def _llm_type(self) -> str:
        """A short string describing the LLM type."""
        return "MyWrapperChatLLM"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying params. Used in callbacks/tracing."""
        return {
            "base_url": self.base_url,
            "provider": self.provider,
            "model_name": self.model_name,
        }


if __name__ == "__main__":
    load_dotenv(override=True)

    my_llm = NTTHWrapperChatLLM(
        id=os.getenv("NTTH_ID"),
        secret=os.getenv("NTTH_SECRET"),
        model_name=os.getenv("NTTH_MODEL"),
        provider=os.getenv("NTTH_PROVIDER"),
        base_url=os.getenv("NTTH_BASE_URL")
    )

    # Then use it in your LangChain flow:
    result = my_llm.invoke([HumanMessage(content="Hello, how are you?")])
    print('--------------------------------', result.content)
    print('--------------------------------', result.usage_metadata)
