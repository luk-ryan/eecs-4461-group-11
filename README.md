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
    - 🔵 AI-generated art
    - 🟠 Human-created art
    - 🟣 AI-favoring critics
    - 🟤 Human-favoring critics
    - ⚪ Neutral critics
  - Connections represent closeness in art style/genre
  - Line graph to show dominant art type over time

## How to Run:

### **1. Create a Python virtual environment:**

```sh
python -m venv venv
```

### **2. Activate the virtual environment:**

#### Windows

```sh
.\venv\Scripts\Activate
```

#### Mac/Linux

```sh
source venv/bin/activate
```

### **3. Install dependencies:**

```sh
pip install -r requirements.txt
```

### **4. Run the simulation:**

```sh
cd src/
solara run app.py
```
