from dotenv import load_dotenv
from langgraph.graph import StateGraph , END , START
from graph.nodes import generate_answer, retriver, web_search, grade_documents
from graph.consts import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEB_SEARCH 
from graph.state import GraphState
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
    
workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE , retriver)
workflow.add_node(GRADE_DOCUMENTS , grade_documents)
workflow.add_node(GENERATE , generate_answer)
workflow.add_node(WEB_SEARCH , web_search)

workflow.set_entry_point(RETRIEVE)

workflow.add_edge(RETRIEVE , GRADE_DOCUMENTS )
workflow.add_conditional_edges(GRADE_DOCUMENTS , decide_to_generate , {
    GENERATE: GENERATE,
    WEB_SEARCH: WEB_SEARCH
})

workflow.add_edge(WEB_SEARCH , GENERATE)
workflow.add_edge(GENERATE , END )


app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")