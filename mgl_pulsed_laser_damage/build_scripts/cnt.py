import content, re
from collections import Counter
print(Counter(b[0] for b in content.B))
w=sum(len(b[1].split()) for b in content.B if b[0] in ('p','abstract'))
print('words (raw tokens)',w)
