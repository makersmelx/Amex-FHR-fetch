from cache import *
from fhr import *
from interaction import *

if __name__ == "__main__":
    properties, graph = pullProperties()
    mainInteraction(properties, graph)
