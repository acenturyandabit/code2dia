# NOT ACTUALLY PYTEST YET, just a file I can run to test
import sys
from repositoryMiner import mineFile

print (mineFile(sys.argv[1], sys.argv[2], [], []))