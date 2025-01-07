from enums.agent_type import AgentType

class Agent:
    def __init__(self, id, agent_type, placement=None):
        self.id = id
        self.agent_type = agent_type
        self.set_placement(placement=placement)

    def set_placement(self, placement):
        self.placement = placement
