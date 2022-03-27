from enum import Enum

from collections import namedtuple


Type = Enum("Type", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    iterable2 = iter(iterable)
    return zip(iterable2, iterable2)


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Type.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    updated_agents = []
    non_changed_types = [Type.HEALTHY, Type.DEAD]
    non_changed_agents = [
        agent for agent in agent_listing if agent.category in non_changed_types]
    changed_agents = [
        agent for agent in agent_listing if agent.category not in non_changed_types]
    for agent1, agent2 in pairwise(changed_agents):
        updated_agents += meeting(agent1, agent2)
    if(len(changed_agents) % 2 == 1):
        updated_agents.append(changed_agents[-1])
    return non_changed_agents + updated_agents


def meeting(first_agent: Agent, second_agent: Agent):
    if (first_agent.category == Type.CURE or second_agent.category == Type.CURE):
        return [cure(first_agent),  cure(second_agent)]
    else:
        return [make_sick(first_agent), make_sick(second_agent)]


def cure(agent: Agent):
    if(agent.category == Type.CURE):
        return agent
    return Agent(agent.name, Type(agent.category.value - 1))


def make_sick(agent: Agent):
    return Agent(agent.name, Type(agent.category.value + 1))
