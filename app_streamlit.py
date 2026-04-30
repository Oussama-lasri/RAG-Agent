import time
import streamlit as st
from graph.graph import app

st.set_page_config(page_title="RAG-Agent", layout="wide")
st.title("RAG-Agent")
st.caption("Advanced RAG with Reflection + Adaptive Retrieval + Self-Correction")
st.markdown("""
**Knowledge sources:**
- [Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- [Adversarial Attacks on LLMs](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/)
""")

# --- Graph image (draw once) ---
if "graph_drawn" not in st.session_state:
    try:
        app.get_graph().draw_mermaid_png(output_file_path="graph.png")
        st.session_state.graph_drawn = True
    except Exception as e:
        st.session_state.graph_drawn = False
        st.session_state.graph_error = str(e)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("Workflow")
    st.markdown("""
    1. Route question  
    2. Retrieve documents  
    3. Grade documents  
    4. Decide to generate / web search  
    5. Generate answer  
    6. Grade hallucination  
    7. Grade answer relevance  
    """)

    if st.session_state.get("graph_drawn"):
        st.image("graph.png", caption="Agent workflow", use_container_width=True)
    elif "graph_error" in st.session_state:
        st.caption(f"Graph render failed: {st.session_state.graph_error}")

    st.divider()

    # Token counter
    if st.session_state.messages:
        total_chars = sum(len(m["content"]) for m in st.session_state.messages)
        st.caption(f"Messages: {len(st.session_state.messages)}  ·  ~{total_chars:,} chars")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Chat history display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input ---
if prompt := st.chat_input("Ask a question about the documents..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        steps_container = st.container()
        answer = None
        start_time = time.time()

        with st.spinner("Agent is thinking..."):
            final_state = None

            for event in app.stream({"question": prompt}, stream_mode="updates"):
                final_state = event
                elapsed = round(time.time() - start_time, 1)

                for node_name, node_output in event.items():

                    # Helper to render a step row
                    def render_step(label, sub, status="info"):
                        icons = {"info": "→", "success": "✓", "error": "✗"}
                        colors = {
                            "info":    ("🔵", "st.info"),
                            "success": ("🟢", "st.success"),
                            "error":   ("🔴", "st.error"),
                        }
                        icon = icons.get(status, "→")
                        with steps_container:
                            cols = st.columns([0.05, 0.8, 0.15])
                            cols[0].markdown(f"**{icon}**")
                            cols[1].markdown(f"**{label}** — {sub}")
                            cols[2].caption(f"{elapsed}s")

                    if node_name in ("retriever", ) or "retrieve" in node_name.lower():
                        docs = node_output.get("documents", [])
                        render_step("Retrieve", f"Fetched {len(docs)} documents", "info")

                    elif node_name == "grade_documents":
                        render_step("Grade documents", "Evaluated relevance", "success")

                    elif node_name == "web_search":
                        render_step("Web search", "Searching external knowledge", "info")

                    elif node_name in ("generate_answer", "generate"):
                        render_step("Generate answer", "Generating response", "success")

                    elif "hallucination" in node_name.lower():
                        grade = node_output.get("hallucination_grade")
                        if grade == "yes":
                            render_step("Hallucination grader", "Answer is grounded", "success")
                        else:
                            render_step("Hallucination grader", "Hallucination detected — retrying", "error")

                    elif "answer_grader" in node_name.lower() or \
                         node_name == "grade_generation_grounded_in_docs_and_questions":
                        render_step("Answer grader", "Checking relevance to question", "info")

        # --- Final answer (outside spinner) ---
        if final_state:
            generation = None
            for value in final_state.values():
                if isinstance(value, dict) and "generation" in value:
                    generation = value["generation"]
                    break
            answer = generation or final_state.get("generation")

        if answer:
            st.divider()
            st.markdown(answer)
        else:
            st.warning("No answer was generated.")
            answer = "No answer was generated."

    st.session_state.messages.append({"role": "assistant", "content": answer})