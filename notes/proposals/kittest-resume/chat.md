# The chat's own idea (R7 chat 3, written before the helpers)
1. kittests.py writes each test's result as it ends to a per-run file (notes/logs/kittests-run-ID.jsonl: name, pass,
   detail, seconds, the hash of the kit files it imports), flushed at once.
2. On start, if the newest run file is unfinished and the shared code is unchanged since it began (same git tree hash
   of source/), it skips the tests already recorded and runs only the rest; a changed kit starts a fresh run.
3. At the end it writes the summary line into kittests-last.log as now, so handover.py and the watcher need no change.
4. Kittest: a fake run killed after 3 tests, restarted, runs only the remaining ones and ends with the full list.
