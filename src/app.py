import math
import solara

from model import ArtCritiqueModel
from agents import ArtAgent, CriticAgent, ArtType, CritiqueType
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

# Agent portrayal function to visualize the agents' types (ArtAgent or CriticAgent)
def agent_portrayal(agent):
    if isinstance(agent, ArtAgent):
        if agent.art_type == ArtType.AI_GENERATED:
            color = "tab:blue"  # Blue for AI-generated art
        else:
            color = "tab:orange"  # Orange for human-created art
    elif isinstance(agent, CriticAgent):
        if agent.critique_type == CritiqueType.AI_FAVORING:
            color = "tab:purple"  # Purple for AI-favoring critics
        elif agent.critique_type == CritiqueType.HUMAN_FAVORING:
            color = "tab:brown"  # Brown for human-favoring critics
        else:
            color = "tab:gray"  # Gray for neutral critics

    return {"color": color, "size": 10}

# Model parameters for customization in Solara UI
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "num_artists": Slider(
        label="Number of Artists",
        value=10,
        min=1,
        max=50,
        step=1,
    ),
    "num_ai_artists": Slider(
        label="Initial AI-Generated Artists",
        value=2,
        min=0,
        max=50,
        step=1,
    ),
    "num_critics": Slider(
        label="Number of Critics",
        value=5,
        min=1,
        max=20,
        step=1,
    ),
    "influence_chance": Slider(
        label="Influence Chance (AI Art)",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "bias_towards_ai": Slider(
        label="Critic Bias Towards AI",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
}

# Visualization of the agent space
SpacePlot = make_space_component(agent_portrayal)

# Line plot to visualize AI vs Human artists & critic biases
def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# of Agents")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

def extract_data(model):
    return model.datacollector.get_model_vars_dataframe()

AgentPlot = make_plot_component(
    {
        "AI Art": "tab:blue",
        "Human Art": "tab:orange",
        "AI-Favoring Critics": "tab:purple",
        "Human-Favoring Critics": "tab:brown",
        "Neutral Critics": "tab:gray",
    },
    post_process=post_process_lineplot,
)

# Create the model
model1 = ArtCritiqueModel()


# Solara page setup with visualization components
page = SolaraViz(
    model1,
    components=[
        SpacePlot,
        AgentPlot, # Line graph tracking agent types over time
    ],
    model_params=model_params,
    name="Art Critique Model",
)

page  # noqa
