# Saved example: a site refused, and the chat gave up instead of asking Sam (R7 chat 1, 25 Nov)

Session session_01U3pKR21qH3HD4urog8SVBy. Reference photos of people seated:
- Wikimedia Commons search: HTTP 429 (too many requests).
- Openverse API: HTTP 401 (a login needed).
- Unsplash: refused by Claude Code's auto-mode safety check ("Unauthorized Access").
The chat stopped after one try each and told Sam, at the end of the job, "I couldn't get reference photos (the free
photo libraries refused me)", with no question about what would let them through. Sam (25 Nov): "Ask me for image
site permissions" ... "Always ask for permissions when a site fails like that and I'll happily grant it". Rule: Y.
The check owed must catch this: a refused download (403/401/429, a proxy refusal, a safety-check refusal) seen in a
chat's work, with no numbered question to Sam about it in that chat's next message to him.
