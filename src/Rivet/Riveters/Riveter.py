#Parent class for all riveter types
sessionRiveters = []
# @author MWK

def getRiveters():
    for sr in sessionRiveters:
        sr.scream()
    return sessionRiveters

class Riveter:
    def __init__(self):
        pass
    @classmethod
    def analyze(cls, column): pass

    @classmethod
    def apply(cls, column): pass

    @classmethod
    def scream(cls):pass

    def register(self):
        sessionRiveters.append(self)
        print(sessionRiveters)

