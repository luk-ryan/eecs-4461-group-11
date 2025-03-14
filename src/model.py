import networkx as nx
import mesa
from mesa import Model
from agents import ArtAgent, CriticAgent, ArtType, CritiqueType

class AIArtSimulation(Model):
    """A simulation model for AI and human artists, and AI critics."""
    
    def __init__(
        self,
        num_artists=10,
        num_critics=5,
        ai_art_ratio=0.5,
        critic_bias=0.5,
        influence_chance=0.3,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.num_artists = num_artists
        self.num_critics = num_critics
        self.ai_art_ratio = ai_art_ratio
        self.critic_bias = critic_bias
        self.influence_chance = influence_chance
        
        self.G = nx.erdos_renyi_graph(n=self.num_artists + self.num_critics, p=0.3)
        self.grid = mesa.space.NetworkGrid(self.G)
        
        # Create artist agents
        num_ai_artists = int(self.num_artists * self.ai_art_ratio)
        num_human_artists = self.num_artists - num_ai_artists
        
        for i in range(num_human_artists):
            agent = ArtAgent(self, ArtType.HUMAN, self.influence_chance)
            self.grid.place_agent(agent, i)
        
        for i in range(num_ai_artists):
            agent = ArtAgent(self, ArtType.AI_GENERATED, self.influence_chance)
            self.grid.place_agent(agent, num_human_artists + i)
        
        # Create critic agents
        for i in range(self.num_critics):
            critique_type = CritiqueType.AI_FAVORING if self.random.random() < self.critic_bias else CritiqueType.HUMAN_FAVORING
            agent = CriticAgent(self, critique_type, self.critic_bias)
            self.grid.place_agent(agent, self.num_artists + i)
        
        self.running = True
    
    def step(self):
        self.schedule.step()