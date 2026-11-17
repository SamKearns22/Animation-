# The chat's own idea (written before the helpers run)
A "health check" run automatically at every chat's start (setup.sh) and end (handover.py end): one line per important
system, each a small live test with a pass number: message log saved today; model the chat runs on matches its stage;
finder used per note fixed; kittests quick set passes; kit catalogue statuses match Sam's recorded Y's. Any failure
prints "BROKEN: X" and goes into Sam's next message as one plain line ("Broken: the message saver hasn't saved since
yesterday; fixing it first"), plus a push notification. A weekly summary of what failed and for how long.
Cost: ~1.5-2% of a week to build; a few seconds per chat.
