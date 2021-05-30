"""
Polygraph simulations and modules.
"""
import torch

from . import core
from . import math


class NoOp(core.PolyGraphOp):
    """
    No operator
    """

    def messagefn(self):
        """
        Message function
        """

        def function(edges):  # pylint: disable=unused-argument
            return {}

        return function

    def reducefn(self):
        """
        Reduce function
        """

        def function(nodes):  # pylint: disable=unused-argument
            return {}

        return function


class BalaGoyalOp(core.PolyGraphOp):
    """
    Learning from neighbours (Bala & Goyal, 1998)
    """

    def filterfn(self):
        """
        Filters out edges whose source has no evidence to report
        """

        def function(edges):
            return torch.gt(edges.src["payoffs"][:, 1], 0.0)

        return function

    def messagefn(self):
        """
        Message function
        """

        def function(edges):
            return {"payoffs": edges.src["payoffs"]}

        return function

    def reducefn(self):
        """
        Reduce function
        """

        def function(nodes):
            return {"payoffs": torch.sum(nodes.mailbox["payoffs"], dim=1)}

        return function

    def applyfn(self):
        """
        Update function
        """

        def function(nodes):
            # A node observes evidence E denoting the number of successful trials (`values`),
            # and the total number of trials (`trials`). The probability of successful trials
            # is given by `logits`.
            logits = nodes.data["logits"]
            values = nodes.data["payoffs"][:, 0]
            trials = nodes.data["payoffs"][:, 1]

            # Prior, P(H) (aka. belief that B is better)
            prior = nodes.data["beliefs"]

            # Posterior, P(H|E)
            posterior = math.bayes(prior, math.Evidence(logits, values, trials))

            # Update node attribute
            return {"beliefs": posterior}

        return function


class OConnorWeatherallOp(core.PolyGraphOp):
    """
    Scientific polarisation (O'Connor & Weatherall, 2018)
    """

    def __init__(self, graph, params):
        super().__init__(graph, params)

        # Multiplier that captures how quickly agents become uncertain about
        # the evidence of their peers as their beliefs diverge.
        self.mistrust = params.mistrust

        # Whether to discount evidence with unti-updating or not
        self.antiupdating = params.antiupdating

    def filterfn(self):
        """
        # Filters out edges whose source has no evidence to report
        """

        def function(edges):
            return torch.gt(edges.src["payoffs"][:, 1], 0.0)

        return function

    def messagefn(self):
        """
        Message function
        """

        def function(edges):
            return {"payoffs": edges.src["payoffs"], "beliefs": edges.src["beliefs"]}

        return function

    def reducefn(self):
        """
        Reduce function
        """

        def function(nodes):
            # Log probability of successful trials
            logits = nodes.data["logits"]
            # Prior, P(H) (aka. belief)
            prior = nodes.data["beliefs"]

            # Number of nodes and number of neighbours per node (incoming messages)
            _, neighbours = nodes.mailbox["beliefs"].shape
            for i in range(neighbours):
                # A node receives evidence E from its i-th neighbour, say Jill, denoting the
                # number of successful trials and the total number of trials she observed
                values = nodes.mailbox["payoffs"][:, i, 0]
                trials = nodes.mailbox["payoffs"][:, i, 1]

                # Evidence, E
                evidence = math.Evidence(logits, values, trials)

                # The difference in belief between an agent and its i-th neighbour
                delta = torch.abs(prior - nodes.mailbox["beliefs"][:, i])

                # Compute belief that the evidence E is real, P(E)(d)
                if self.antiupdating:
                    certainty = torch.max(
                        1.0
                        - delta
                        * self.mistrust
                        * (1.0 - math.marginal(prior, evidence)),
                        torch.zeros((len(nodes),)),
                    )
                else:
                    # Consider an agent u and one of its neighbours, v. As beliefs between u and v
                    # diverge (delta towards 1), agent u simply ignores the evidence of agent v.
                    #
                    # If delta becomes 1, uncertainty ~ marginal. In other words, agent u's belief
                    # remains unchanged in light of agent v's evidence.
                    #
                    # The multiplier simply determines how far apart beliefs have to become before
                    # agent u begins to ignore the evidence of its neighbour, v (since delta never
                    # becomes 1)
                    certainty = 1.0 - torch.min(
                        torch.ones((len(nodes),)), delta * self.mistrust
                    ) * (1.0 - math.marginal(prior, evidence))

                # Update posterior belief, in light of soft uncertainty
                posterior = math.jeffrey(prior, evidence, certainty)

                # Consider next neighbour
                prior = posterior

            # Return posterior beliefs for each neighbour
            return {"beliefs": posterior}

        return function