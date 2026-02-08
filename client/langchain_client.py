import asyncio
import websockets
import json
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    async with websockets.connect("ws://server:8001/ws") as websocket:
        await websocket.send(json.dumps({"tool": "add", "params": {"a": a, "b": b}}))
        result = await websocket.recv()
        return json.loads(result)["result"]

async def main():
    llm = ChatOllama(model="mistral", base_url="http://ollama:11434")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, [add], prompt)
    executor = AgentExecutor(agent=agent, tools=[add])
    
    result = await executor.ainvoke({"input": "What is 15 + 27?"})
    print(result["output"])

if __name__ == "__main__":
    asyncio.run(main())
