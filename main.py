import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agent import pybot_agent
from rag import index_documents

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ.pop("GEMINI_API_KEY", None)

APP_NAME   = "adk_rag_pybot"
USER_ID    = "sai_vardhan"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
runner          = Runner(
    agent           = pybot_agent,
    app_name        = APP_NAME,
    session_service = session_service,
)

async def chat(message: str):
    content = Content(
        role  = "user",
        parts = [Part(text=message)]
    )

    print("─" * 50)

    final_reply = ""

    async for event in runner.run_async(
        user_id     = USER_ID,
        session_id  = SESSION_ID,
        new_message = content,
    ):
        # Show tool calls
        if event.get_function_calls():
            for call in event.get_function_calls():
                args_preview = list(call.args.values())[0] if call.args else ""
                print(f"  [Tool] {call.name}({str(args_preview)[:60]})")

        # Capture final response — try multiple ways
        if event.is_final_response():
            # Method 1 — standard way
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_reply += part.text

            # Method 2 — fallback via candidates
            if not final_reply and hasattr(event, 'candidates'):
                for candidate in (event.candidates or []):
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in (candidate.content.parts or []):
                            if hasattr(part, 'text') and part.text:
                                final_reply += part.text

    if final_reply:
        print(f"\nPyBot: {final_reply}\n")
    else:
        print(f"\nPyBot: [No response captured — tools ran successfully]\n")

    return final_reply

async def main():
    # Index documents on startup
    print("\n  [Indexing documents...]")
    index_documents()

    # Create session
    await session_service.create_session(
        app_name   = APP_NAME,
        user_id    = USER_ID,
        session_id = SESSION_ID,
    )

    print("\n╔══════════════════════════════════════╗")
    print("║  PyBot — ADK + RAG Agent             ║")
    print("║  Answers from YOUR documents         ║")
    print("║  Type 'quit' to exit                 ║")
    print("╚══════════════════════════════════════╝\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        await chat(user_input)


if __name__ == "__main__":
    asyncio.run(main())