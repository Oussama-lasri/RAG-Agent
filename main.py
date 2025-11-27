from langchain import hub


prompt = hub.pull("rlm/rag-prompt") 


def main():
    print(prompt)
    print("Hello from rag-agent!")


if __name__ == "__main__":
    main()
