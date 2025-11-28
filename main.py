from graph.graph import app


def main():
    print("Starting LangGraph application...")
    print(app.invoke({"question": "What is agent memory?"}))


if __name__ == "__main__":
    main()
