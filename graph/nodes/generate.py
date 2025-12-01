from typing import Any, Dict
from graph.chains.generation import generation_chain 
from graph.state import GraphState

def generate_answer(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE ANSWER---")
    question = state["question"]
    context = state["documents"]

    generation = generation_chain.invoke(
        {"question": question, "context": context}
    )
    return {"generation": generation, "question": question, "documents": context}