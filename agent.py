import os
from dotenv import load_dotenv
import warnings

from db import get_schema, run_query
from prompts import SQL_AGENT_INSTRUCTIONS

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallRequest
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
from langgraph.types import Command
from langchain_core._api import LangChainBetaWarning

warnings.filterwarnings("ignore", category=LangChainBetaWarning)

load_dotenv()
os.environ["LANGSMITH_PROJECT"] = "supply-chain-sql-agent"

# Helper function to determine if the agent generated a non-SELECT query
def is_write_query(request: ToolCallRequest) -> bool:
    """Pause SQL that isn't a read-only SELECT."""
    query = request.tool_call["args"].get("query", "")
    return not query.lstrip().upper().startswith("SELECT")

# Helper function to build the agent
def build_agent():
    llm = ChatOpenAI(model=os.getenv("MODEL_NAME"))

    memory = InMemorySaver()

    return create_agent(
        model=llm,
        tools=[get_schema, run_query],
        system_prompt=SQL_AGENT_INSTRUCTIONS,
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "run_query": {
                        "allowed_decisions": ["approve", "reject", "respond"],
                        "when": is_write_query
                    },
                },
            ),
        ],
        checkpointer=memory,
    )

# Helper function to stream the output
def print_stream(stream):
    for message in stream.messages:
        for token in message.text:
            print(token, end="", flush=True)

# Helper function to handle interrupts
def handle_interrupts(agent, stream, thread_config):
    while stream.interrupted:
        print(f"\n\nExecution paused: Approval required for Non-SELECT (write) query.")
        query = stream.interrupts[0].value["action_requests"][0]["args"]["query"]
        print(f"Query: {query}")
        print("Allowed decisions: ['approve', 'reject', 'respond']")

        # Ask user for user input
        action = input("[You] Action (approve/reject/respond): ").strip().lower()
        if action == "approve":
            command = Command(resume={"decisions": [{"type": "approve"}]})
        elif action == "reject":
            command = Command(resume={"decisions": [{"type": "reject", "message": "User rejected this action. Do not retry this tool call."}]})
        elif action == "respond":
            feedback = input("[You] Feedback for the query: ").strip()
            command = Command(resume={"decisions": [{"type": "respond", "message": feedback}]})
        else:
            print(f"Unrecognized action '{action}', defaulting to reject.")
            command = Command(resume={"decisions": [{"type": "reject", "message": "Unrecognized action."}]})

        print("\n[Agent]: ", end="")
        stream = agent.stream_events(
            command,
            config=thread_config,
            version="v3",
        )
        print_stream(stream)

def run_agent():
    agent = build_agent()

    thread_config = {"configurable": {"thread_id": str(uuid7())}}

    print("SQL Agent Ready! (Type 'q' or 'exit' to quit)")
    while True:
        user_input = input("\n[You]: ").strip()
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("\n[Agent]: Goodbye!")
            break
        if not user_input:
            continue

        # Stream the output
        print("\n[Agent]: ", end="")
        stream = agent.stream_events(
            {"messages": [HumanMessage(content=user_input)]},
            config=thread_config,
            version="v3",
        )

        print_stream(stream)
        stream = handle_interrupts(agent, stream, thread_config)
        print()

if __name__ == "__main__":
    run_agent()