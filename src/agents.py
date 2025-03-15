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
        self.previous_art_type = art_type
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
        connected_agents = self.model.grid.get_neighbors(self.pos, include_center=False)
        print("===\nArt Type:", self.art_type, "\nconnected agents: ", connected_agents)
        
        # Count the number of human vs AI critics and art agents connected
        human_count = 0
        ai_count = 0

        for agent in connected_agents:
            if isinstance(agent, CriticAgent):
                if agent.critique_type == CritiqueType.AI_FAVORING:
                    ai_count += 2  # Critics count as 2 for influencing AI art
                elif agent.critique_type == CritiqueType.HUMAN_FAVORING:
                    human_count += 2
                print("Critic:", agent.critique_type, "- ai count:", ai_count, "human count:", human_count)
            else:
                if agent.art_type == ArtType.AI_GENERATED:
                    ai_count += 1
                else:
                    human_count += 1
                print("Art:", agent.art_type, "- ai count:", ai_count, "human count:", human_count)
        
        print("human count:", human_count, "ai count:", ai_count)

        # Adjust influence chance based on the ratio of AI vs human agents
        total_count = human_count + ai_count
        adjusted_influence_chance = self.influence_chance  # Start with base influence chance
        if total_count > 0:
            print("ratio ai to human:", ai_count, "/", total_count, "=", ai_count / total_count)
            # Influence chance will be temporarily adjusted by the ratio difference
            if self.art_type == ArtType.HUMAN:
                adjusted_influence_chance *= ai_count / total_count  # If the ratio is close to 50/50, no adjustment
                # Now, produce art based on the adjusted influence chance
                if self.random.random() < adjusted_influence_chance:
                    self.art_type = ArtType.AI_GENERATED
                else:
                    self.art_type = ArtType.HUMAN
            else:
                adjusted_influence_chance *= (1 - ai_count / total_count)
                
                # Now, produce art based on the adjusted influence chance
                if self.random.random() < adjusted_influence_chance:
                    self.art_type = ArtType.HUMAN
                else:
                    self.art_type = ArtType.AI_GENERATED
        
        print("Art Type:", self.art_type, adjusted_influence_chance)

    def step(self):
        """Each step, the agent produces art."""
        self.produce_art()


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

    def critique_art(self):
        """
        Critiques the art produced by connected ArtAgents.
        The critique type may change based on the art and the critic's bias.
        """
        human_count = 0
        ai_count = 0

        # Check all connected art agents
        for art_agent in self.connected_art:
            if art_agent.art_type== ArtType.AI_GENERATED:
                # Check if the critic values AI art
                if self.random.random() < self.bias_towards_ai:
                    ai_count += 1
            elif art_agent.art_type == ArtType.HUMAN:
                # Check if the critic values human art
                if self.random.random() < (1 - self.bias_towards_ai):
                    human_count += 1

        # Determine the critique type based on the counts
        if ai_count > human_count:
            self.critique_type = CritiqueType.AI_FAVORING
        elif human_count > ai_count:
            self.critique_type = CritiqueType.HUMAN_FAVORING
        else:
            self.critique_type = CritiqueType.NEUTRAL

    def step(self):
        """Each step, the critic critiques the connected art agents' work."""
        self.critique_art()