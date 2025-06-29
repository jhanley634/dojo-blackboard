#! /usr/bin/env python


# from difflib import unified_diff

from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama

from connections.conn_util import get_examples, validate


def get_llm_response(prompt: str, model: str = "phi4") -> str:
    ollama_url = "http://localhost:11434"
    llm = ChatOllama(base_url=ollama_url, model=model)
    result = llm.invoke(prompt)
    assert isinstance(result, AIMessage)
    return f"{result.content}"


def main() -> None:
    df = get_examples()
    validate(df)


if __name__ == "__main__":
    main()
