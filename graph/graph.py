from dotenv import load_dotenv
from langgraph.graph import StateGraph , END , START
from graph.nodes import generate_answer, retriver, web_search, grade_documents
from graph.consts import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEB_SEARCH 
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader

load_dotenv()




# create conditional edge 
def decide_to_generate(state: GraphState) -> str:
    print("---DECIDE TO GENERATE---")
    print("---ASSESS GRADE DOCUMENTS---")
    if state["web_search"]:
        print("DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION")
        return WEB_SEARCH
    else:
        return GENERATE
    
def grade_generation_grounded_in_docs_and_questions(state: GraphState) -> str:
    print("---GRADE GENERATION GROUNDED IN DOCS AND QUESTIONS---")
    question = state["question"]
    generation = state["generation"]
    documents = state["documents"]  
    
    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )   
    # walrus operator
    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
    
workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE , retriver)
workflow.add_node(GRADE_DOCUMENTS , grade_documents)
workflow.add_node(GENERATE , generate_answer)
workflow.add_node(WEB_SEARCH , web_search)

workflow.set_entry_point(RETRIEVE)

workflow.add_edge(RETRIEVE , GRADE_DOCUMENTS )
workflow.add_conditional_edges(GRADE_DOCUMENTS , decide_to_generate , 
#    Possible branches depending on decision result.
    {
    GENERATE: GENERATE,
    WEB_SEARCH: WEB_SEARCH
    }
    )


workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_docs_and_questions,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEB_SEARCH,
    },
)

workflow.add_edge(WEB_SEARCH , GENERATE)
workflow.add_edge(GENERATE , END )


app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")