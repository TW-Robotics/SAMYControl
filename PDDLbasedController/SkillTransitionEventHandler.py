import pprint

class SkillTransitionEventHandler(object): 
    """
    Subscription Handler. When we receive an event regarding an skill state transition, we process it
    """

    def __init__( self, setActionEffectsCb_, namespaces_ ):
        self.setActionEffectsCb = setActionEffectsCb_
        self.namespaces = namespaces_

    def datachange_notification(self, node, val, data): # on state change: read new state -> get next action -> perform action
        """
        called for every datachange notification from server
        """
        pass

    def event_notification(self, event):
        """
        called for every event notification from server
        """
        text = event.Message.Text
        words = text.split(" ")
        skillNameCore = words[3] # Hardcoded, not ideal
        previousState = words[6] # Hardcoded, not ideal
        newState = words[len(words)-1]
        agentName = self.namespaces[event.SourceNode.NamespaceIndex]
        self.setActionEffectsCb( agentName, skillNameCore, previousState, newState )

    def status_change_notification(self, status):
        """
        called for every status change notification from server
        """
        pass
