from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

from langchain_anthropic import ChatAnthropic

# Fix: Use correct Claude model name
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # Correct model name
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3 from their official pricing pages",
        llm=llm,
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 