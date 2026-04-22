from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional, Any

from langchain.chat_models import init_chat_model

from utils.config_loader import ConfigLoader


class ModelLoader(BaseModel):
    model_provider: Literal["openai", "groq"] = "openai"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def load_llm(self):
        """
        Load and return the LLM model
        """

        print("LLM Loading...")
        print(f"Loading LLM from {self.model_provider}")

        if self.model_provider == "openai":
            model_name = self.config.llm.openai.model_name
        elif self.model_provider == "groq":
            model_name = self.config.llm.groq.model_name
        else:
            raise ValueError(f"Unknown model provider: {self.model_provider}")

        if model_name is not None:
            return init_chat_model(model_name=model_name)
