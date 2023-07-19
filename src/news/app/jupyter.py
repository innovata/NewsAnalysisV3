
#============================================================
"""복사-붙여넣기로 사용해라.
사용 후 모듈에선 삭제해라."""
#============================================================

import os
os.getcwd()
import sys
sys.path.append("/Users/sambong/pjts/inews/env/lib/python3.7/site-packages")
sys.path.append("/Users/sambong/pjts/libs/i-nlp")
sys.path.append("/Users/sambong/pjts/libs/idebug")
sys.path
other_pjts = ['stock']
for other in other_pjts:
    path = f"/Users/sambong/pjts/{other}/env/lib/python3.7/site-packages"
    sys.path.remove(path)
sorted(sys.path)
%env GOOGLE_AUTH_PATH=/Users/sambong/pjts/libs/igoogle/igoogle-auth.json
%env ETRI_ACCESS_KEY=8393a2fc-eb89-4bf3-993f-a35f9df007a0
import pprint
pp = pprint.PrettyPrinter(indent=2)
