import mesa
from mesa import Model
import networkx as nx
from mesa.space import NetworkGrid
from agents import ArtAgent, CriticAgent, ArtType, CritiqueType


def number_art_agents(model):
    return sum(1 for agent in model.schedule if isinstance(agent, ArtAgent))


def number_critics(model):
    return sum(1 for agent in model.schedule if isinstance(agent, CriticAgent))

class ArtCritiqueModel(Model):
    """A model for simulating art production and critiques by AI and human agents."""

    def __init__(
        self,
        num_artists=10,
        num_critics=5,
        num_ai_artists=2,
        influence_chance=0.5,
        bias_towards_ai=0.5,
        seed=None
    ):
        """
        :param num_artists: Number of artist agents in the model.
        :param num_critics: Number of critic agents in the model.
        :param influence_chance: Probability that an artist produces AI-generated art.
        :param bias_towards_ai: Bias of critics towards AI-generated art.
        :param seed: Random seed for reproducibility.
        """
        super().__init__(seed=seed)

        self.num_artists = num_artists
        self.num_ai_artists = (num_ai_artists if num_ai_artists <= num_artists else num_artists)
        self.num_critics = num_critics
        self.influence_chance = influence_chance
        self.bias_towards_ai = bias_towards_ai

        self.schedule = []
        
        # Create the grid (using a simple network as in the Virus model)
        self.G = nx.erdos_renyi_graph(self.num_artists + self.num_critics, 0.2)  # Connect artists and critics
        self.grid = NetworkGrid(self.G)

        # Create art agents (artists)
        for i in range(self.num_artists):
            # Check if it's an AI artist or human artist
            if i < self.num_ai_artists:
                art_agent = ArtAgent(self, ArtType.AI_GENERATED, self.influence_chance)  # AI-generated art
            else:
                art_agent = ArtAgent(self, ArtType.HUMAN, self.influence_chance)  # Human-generated art

            self.schedule.append(art_agent)
            self.grid.place_agent(art_agent, i)  # Place on the network (using the node ID directly)

        # Create critic agents
        for i in range(self.num_artists, self.num_artists + self.num_critics):
            critic_agent = CriticAgent(self, CritiqueType.NEUTRAL, self.bias_towards_ai)
            self.schedule.append(critic_agent)
            self.grid.place_agent(critic_agent, i)  # Place on the network (using the node ID directly)

        # Ensure all ArtAgents are connected to at least one CriticAgent
        for art_agent in self.get_artists():
            art_agent.ensure_connection_to_critic()

        # Data collector
        self.datacollector = mesa.DataCollector(
            {
                "ArtAgents": number_art_agents,
                "CriticAgents": number_critics,
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step."""
        # Manually activate each agent in the schedule
        for agent in self.schedule:
            agent.step()

        # Collect data for each step
        self.datacollector.collect(self)

    def get_artists(self):
        """Return the list of artist agents."""
        return [agent for agent in self.schedule if isinstance(agent, ArtAgent)]

    def get_critics(self):
        """Return the list of critic agents."""
        return [agent for agent in self.schedule if isinstance(agent, CriticAgent)]