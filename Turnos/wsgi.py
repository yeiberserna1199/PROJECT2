import sys
path = '/workspaces/PROJECT2/Turnos'
if path not in sys.path:
   sys.path.insert(0, path)

from Turnos import app as application