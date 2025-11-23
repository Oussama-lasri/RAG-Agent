from typing import Any, Dict

from state import GraphState
from ingestion import retriever


def retriver(state: GraphState) -> Dict[str, Any]:
    print("Retrieving documents for question:", state["question"])
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents , "question": question}