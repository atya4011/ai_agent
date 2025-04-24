import time
from julep import Julep
import yaml

# Step 1: Connect to Julep
client = Julep(api_key="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTA1OTEyNTUsImlhdCI6MTc0NTQwNzI1NSwic3ViIjoiYmQwNDEyZDEtYmI1Yy01NDg4LWE3ZjItMzFjMDUzNDUyYjQ4In0.mg3NMbTqq9JYW0_1Rhnko9C5Wxbf2aSkKEltRHs18e6FGFA7gS5NF-E8tEvrq8LlIr_AjRXRdMkYQuuHAqF1lg")  # Replace with your actual API key

# Step 2: Create the Research Agent
agent = client.agents.create(
    name="Research Assistant",
    model="claude-3.5-sonnet",  # You can swap model if needed
    about="A helpful research assistant that finds concise, structured information on topics."
)

# Step 3: Define the research task (in YAML for clarity)
task_definition = yaml.safe_load("""
name: Research Task
description: Research a topic and present it in a specified format
main:
- prompt:
  - role: system
    content: |
      You are a helpful research assistant. Your goal is to find concise information on topics provided by the user.
      When given a topic and an output format (e.g., 'summary', 'bullet points', 'short report'), you must gather relevant information and structure it accordingly.
      Maintain a neutral, objective tone. Strictly follow the output format:
      - Summary: 3-4 sentences
      - Bullet Points: max 5 concise points
      - Short Report: under 150 words
      If reliable info cannot be found, state that clearly.
  - role: user
    content: |
      Topic: ${steps[0].input.topic}
      Format: ${steps[0].input.format}
""")

# Step 4: Create the Task
task = client.tasks.create(
    agent_id=agent.id,
    **task_definition
)

# Step 5: Provide input topic + format
execution = client.executions.create(
    task_id=task.id,
    input={
        "topic": "India’s Semiconductor Mission",
        "format": "bullet points"  # Try also: "summary" or "short report"
    }
)

# Step 6: Wait and fetch the result
while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
    print(result.status)
    time.sleep(1)

# Step 7: Print output
if result.status == "succeeded":
    print(result.output)
else:
    print(f"Error: {result.error}")
import time
from julep import Julep
import yaml

client = Julep(api_key="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTA1OTEyNTUsImlhdCI6MTc0NTQwNzI1NSwic3ViIjoiYmQwNDEyZDEtYmI1Yy01NDg4LWE3ZjItMzFjMDUzNDUyYjQ4In0.mg3NMbTqq9JYW0_1Rhnko9C5Wxbf2aSkKEltRHs18e6FGFA7gS5NF-E8tEvrq8LlIr_AjRXRdMkYQuuHAqF1lg")  # Replace with your actual API key


# Step 1: Create Agent
agent = client.agents.create(
    name="Research Assistant",
    model="claude-3.5-sonnet",
    about="A helpful research assistant that finds concise, structured information on topics."
)

# Step 2: Input (you can make this dynamic)
topic = "India’s Semiconductor Mission"
format_type = "bullet points"

# Step 3: Generate YAML with the topic/format injected directly
task_yaml = f"""
name: Research Task
description: Research a topic and present it in a specified format
main:
- prompt:
  - role: system
    content: |
      You are a helpful research assistant. Your goal is to find concise information on topics provided by the user.
      When given a topic and an output format (e.g., 'summary', 'bullet points', 'short report'), you must gather relevant information and structure it accordingly.
      Maintain a neutral, objective tone. Strictly follow the output format:
      - Summary: 3-4 sentences
      - Bullet Points: max 5 concise points
      - Short Report: under 150 words
      If reliable info cannot be found, state that clearly.
  - role: user
    content: |
      Topic: {topic}
      Format: {format_type}
"""

task_definition = yaml.safe_load(task_yaml)

# Step 4: Create the Task
task = client.tasks.create(agent_id=agent.id, **task_definition)

# Step 5: Execute
# Step 5: Execute (with empty input since we used f-strings in the YAML)
execution = client.executions.create(task_id=task.id, input={})


# Step 6: Wait for completion
while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
    print(result.status)
    time.sleep(1)

# Step 7: Output
if result.status == "succeeded":
    print("\n--- Output ---")
    print(result.output)
else:
    print(f"\nError: {result.error}")

