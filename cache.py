import os
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
