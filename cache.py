import os
import json
CACHE_DIR = "cache"


def getAbsolutePath(relativePath):
    curDir = os.getcwd()
    return os.path.join(curDir, CACHE_DIR, relativePath)


def isRelativePathExists(relativePath):
    return os.path.exists(getAbsolutePath(relativePath))


def createDirWithRelativePath(relativePath):
    dir = getAbsolutePath(relativePath)
    if not os.path.exists(dir):
        os.makedirs(dir)

def getAllCaches(listCache, graphCache):
    if isRelativePathExists(listCache) and isRelativePathExists(graphCache):
        with open(getAbsolutePath(listCache), "r+") as file:
            properties = json.loads(file.read())
        with open(getAbsolutePath(graphCache), "r+") as file:
            graph = json.loads(file.read())
        return properties, graph