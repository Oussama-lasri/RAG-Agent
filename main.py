from graph.graph import app


def main():
    print("Starting LangGraph application...")
    # print(app.invoke({"question": "What is agent memory?"}))
    print(app.invoke({"question": "How to make pizza?"}))


if __name__ == "__main__":
    main()
