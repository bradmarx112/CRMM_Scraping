from dataclasses import dataclass


class Entity:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    @classmethod
    def from_dependency_chain(cls, dependency_chain):
        parent = 'None'
        for entity_name in dependency_chain[::-1]:  # Reversing to start from the top
            entity = cls(entity_name, parent)
            parent = entity
        return entity

    def get_parent(self):
        return self.parent

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


@dataclass
class ACRRUInput:
    crmm_info: str
    entity: Entity

    def construct_input(self):
        return self.__dict__

@dataclass
class ResearchInput(ACRRUInput):
    cap_info: str

    def construct_input(self):
        return {'crmm_info': self.crmm_info,
                # Entities are at the capability level for research.
                'entity': self.entity.get_parent().name,
                'cap_info': self.cap_info}

@dataclass
class SummaryInput(ACRRUInput):
    agg_lvl: str
    summaries: str

    def construct_input(self):
        return {'crmm_info': self.crmm_info,
                'entity': self.entity.name,
                'agg_lvl': self.agg_lvl,
                'summaries': self.summaries}