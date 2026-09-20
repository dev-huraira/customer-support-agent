import uuid
from graph import graph
from utils import extract_text

def main():
    thread_id= str(uuid.uuid4())
    config={"configurable":{"thread_id":thread_id}}
    print(f"Session started (thread_id: {thread_id})")
    print("Type 'exit' to quit.\n")

    while True:
        user_input=input("You: ")
        if user_input.lower() == "exit":
            break

        result=graph.invoke(
            {
                "messages":[{"role":"user","content":user_input}],
                "user_id":"user_101",
            },
            config=config
        )

        last_message = result["messages"][-1]
        print(f"Agent ({result.get('category', 'unknown')}): {extract_text(last_message.content)}\n")

if __name__ == "__main__":
    main()
