from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from model import AIArtSimulation

# Function to portray agents in visualization
def network_portrayal(G):
    portrayal = {}
    portrayal["nodes"] = [
        {   
            "id": node_id,
            "size": 6,
            "color": "blue" if agent.art_type == ArtType.HUMAN else "red",
            "label": "H" if agent.art_type == ArtType.HUMAN else "AI"
        }
        for node_id, agent in G.nodes.data("agent") if agent
    ]
    
    portrayal["edges"] = [
        {"source": source, "target": target, "color": "gray"}
        for source, target in G.edges
    ]
    return portrayal

# Adjusted size for visualization (ensure it fits your desired view)
network = NetworkModule(network_portrayal, 500, 500)

server = ModularServer(
    AIArtSimulation,
    [network],
    "AI Art Simulation",
    {"num_artists": 10, "num_critics": 5, "ai_art_ratio": 0.5, "critic_bias": 0.5, "influence_chance": 0.3}
)

if __name__ == "__main__":
    server.launch()
