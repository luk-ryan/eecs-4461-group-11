from enum import Enum
from mesa import Agent
import random


class ArtType(Enum):
    """Enum representing different types of art."""
    HUMAN = 0
    AI_GENERATED = 1


class CritiqueType(Enum):
    """Enum representing different types of critiques."""
    NEUTRAL = 0
    AI_FAVORING = 1
    HUMAN_FAVORING = 2


class ArtAgent(Agent):
    """Represents an artist (human or AI) in the system."""
    
    def __init__(self, model, art_type, influence_chance):
        """
        :param model: The model this agent belongs to.
        :param art_type: The type of art the agent creates (human or AI-generated).
        :param influence_chance: The chance that an artist will create AI-generated art.
        """
        super().__init__(model)
        self.art_type = art_type  # Human or AI-generated artist
        self.influence_chance = influence_chance  # Chance of producing AI-generated art
        self.art_created = None  # Track what type of art the agent produces
        self.connected_critics = []  # List to hold connected critics

    def ensure_connection_to_critic(self):
        """ Ensures this ArtAgent is connected to at least one CriticAgent. """
        if not self.connected_critics:  # If no critics are connected
            available_critics = self.model.get_critics()  # Assuming you have a list of all CriticAgents in the model
            if available_critics:
                critic = random.choice(available_critics)  # Randomly choose a critic from available critics
                self.connect_to_critic(critic)

    def connect_to_critic(self, critic):
        """ Establishes a connection between this ArtAgent and a CriticAgent. """
        if critic not in self.connected_critics:
            self.connected_critics.append(critic)
            # Optional: You can also implement two-way connection by adding this ArtAgent to the critic's connected list
            critic.connect_to_art(self)

    def produce_art(self):
        """
        Artists create art, which could influence critics.
        The type of art depends on the influence chance, the art agent's type, and the influence of connected critics.
        """
        # Get the list of connected critics
        connected_critics = self.model.grid.get_neighbors(self.pos, include_center=False)

        # Loop through connected critics and check if they influence the art production
        critic_influence = 0
        for critic in connected_critics:
            if isinstance(critic, CriticAgent):
                # If the critic favors AI art, increase the chance of producing AI-generated art
                if critic.bias_towards_ai:
                    critic_influence += 0.1  # Influence factor, adjust based on how strong you want the impact

        # Add the critic influence to the base influence chance of the artist
        final_influence_chance = self.influence_chance + critic_influence

        # Ensure the final chance does not exceed 1
        final_influence_chance = min(1.0, final_influence_chance)
        if self.random.random() < self.influence_chance:
            self.art_created = ArtType.AI_GENERATED
        else:
            self.art_created = ArtType.HUMAN

    def step(self):
        """Each step, the agent produces art."""
        self.produce_art()
        # Optionally, you can add logic for sending the art to critics or other agents.


class CriticAgent(Agent):
    """Represents an AI art critic in the system."""
    
    def __init__(self, model, critique_type, bias_towards_ai):
        """
        :param model: The model this agent belongs to.
        :param critique_type: The initial type of critique the agent gives (neutral, AI, or human).
        :param bias_towards_ai: The critic's bias toward AI-generated art.
        """
        super().__init__(model)
        self.critique_type = critique_type  # AI-favoring, human-favoring, or neutral
        self.bias_towards_ai = bias_towards_ai  # The critic's bias towards AI art
        self.connected_art = []  # List to hold connected art agents

    def connect_to_art(self, art_agent):
        """ Connect this CriticAgent to an ArtAgent. """
        if art_agent not in self.connected_art:
            self.connected_art.append(art_agent)

    def critique_art(self, art_agent):
        """
        Critiques the art produced by an artist.
        The critique type may change based on the art and the critic's bias.
        """
        if art_agent.art_created == ArtType.AI_GENERATED:
            if self.bias_towards_ai:
                self.critique_type = CritiqueType.AI_FAVORING
            else:
                self.critique_type = CritiqueType.HUMAN_FAVORING
        elif art_agent.art_created == ArtType.HUMAN:
            if not self.bias_towards_ai:
                self.critique_type = CritiqueType.HUMAN_FAVORING
            else:
                self.critique_type = CritiqueType.AI_FAVORING
        else:
            self.critique_type = CritiqueType.NEUTRAL

    def step(self):
        """Each step, the critic randomly critiques an artist's work."""
        # Find a random artist agent in the model
        selected_artist = self.random.choice(self.model.schedule)
        if isinstance(selected_artist, ArtAgent):
            self.critique_art(selected_artist)
