import os
import sys
from pathlib import Path

# Ensure project root is on sys.path when running this file directly
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever


def retriver(state: GraphState) -> Dict[str, Any]:
    print("Retrieving documents for question:", state["question"])
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents , "question": question}

if __name__ == "__main__":
    retriver({"question": "What is LangGraph?", "documents": []})