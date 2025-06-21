from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    model="gpt-4.1-nano",
    instructions="你是一隻貓，請用貓的講話方式",
)

result = Runner.run_sync(agent, "跟我說個關於貓的笑話")
print(result.final_output)
