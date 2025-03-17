# EECS-4461 Team 11

## Simulation Design & Implementation:

- **System Overview:** two types of agents

  - _Art agent_ (human or ai generated)
  - _Critic agent_ (prefers either human art, ai art, neutral)

- **Simulation Environment:** Network-based simulation

  - Most art agents are connected to other agents, both critics and art.
  - Connections between agents represent closeness in genres/styles of art

- **Agent Design:** At every step, agents decide their next state

  - _Critic agents_ influenced by:
    - Art type of connected art agents
    - Bias towards ai-generated art
  - _Art agents_ influenced by:
    - Art type of connected art agents
    - Art preference of connect critic agents
    - Amount of influence the neighboring agents have

- **Interaction Dynamics:** Manual Activation Schedule

  - Each agent is stored in a list
  - Two types of agents have individual step() functions
  - At every step, the step() function is called for every agent in the list

- **Data Collection & Visualization:**
  - Nodes represent agents
    - Blue for AI-generated art
    - Orange for human-created art
    - Purple for AI-favoring critics
    - Brown for human-favoring critics
    - Gray for neutral critics
  - Connections represent closeness in art style/genre
  - Line graph to show dominant art type over time

## How to Run:

1. Create python virtual environment:
   - `python -m venv venv`
2. Run python virtual environment:
   - `.\venv\Scripts\Activate`
3. Install Dependencies:
   - `pip install -r requirements.txt`

- To run:
  - cd into src directory (`cd src/`)
  - run: `solara run app.py`
