from livekit import agents
from livekit.agents import function_tool
from livekit.agents import llm, RoomInputOptions
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, openai, cartesia, silero, noise_cancellation
import asyncio
import json
import requests
from livekit.plugins.turn_detector.multilingual import MultilingualModel


@function_tool(
    name="query_knowledge_base",
    description="Query the knowledge base for salon information.",
)
async def query_knowledge_base(query: str) -> str:
    print(f"Querying knowledge base with: {query}")
    response = requests.get(
        f"http://127.0.0.1:8000/api/knowledge-base/search-query/?query={query}"
    )
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data)
    else:
        print(f"Error querying knowledge base: {response.status_code}")
        return json.dumps({"error": "Failed to query knowledge base"})


@function_tool(
    name="notify_human_operator",
    description="Trigger this when AI doesn't know the answer and needs human help.",
)
async def notify_human_operator(message: str) -> None:

    requests.post(
        "http://127.0.0.1:8000/api/query-request/create-query/",
        json={"user_id": "1", "question": message},
    )

    print(f"Notification sent: {message}")

stt = deepgram.STT(model="nova-3", language="multi")
llm = openai.LLM(model="gpt-4o")
tts = cartesia.TTS()

SYSTEM_PROMPT = """
You are a helpful and professional customer service AI assistant for a Salon.

All responses must be in plain text, suitable for voice output. Do not use asterisks (*), markdown, emojis, bullet points, or line breaks. Speak naturally, clearly, and concisely, as if you're talking to a person over the phone.

            1. Answer user questions based on the knowledge base provided search using 'query_knowledge_base'.
            Based on the response of above knowledge base entries, can the user's query be answered?
            If yes, provide the answer using only information from the knowledge base.
            2. If you don't have the answer, escalate to a human supervisor using 'notify_human_operator'.
            3. Be concise, professional, and friendly in your responses
            4. Stick to facts in the knowledge base without making up information
            5. If the user explicitly asks for a human, escalate immediately
            6. If the user asks to book appointment then ask for details like date, time, and service. If the details valid according to Salon details Say you will check availability and get back to them ASAP and send a notification to the human supervisor using 'notify_human_operator'.

            When answering from the knowledge base, say: "Based on our information, [answer]"
            When escalating, say: "I'll need to check with our team on that. We'll get back to you shortly."
            This the information about the salon:
            """

agent = Agent(
    instructions=SYSTEM_PROMPT,
    tools=[query_knowledge_base, notify_human_operator],
    stt=stt,
    llm=llm,
    tts=tts,
)


async def entrypoint(ctx: agents.JobContext):

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
