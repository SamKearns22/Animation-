# The chat's own version (written before the helpers ran)

1. One line in CLAUDE.md: no rule without a working check; a rule whose check can't be built says so and names the
   person or step that does it.
2. Audit: every rulebook row and every CLAUDE.md rule gets its check named, or "none"; each "none" or "by hand" goes
   to Sam as a numbered list, worst first, with what a check would be.
3. A gate: the watcher refuses a commit that adds a rule row with no check named.
4. Each check gets a known-bad example in the kit tests that it must catch; a check that can't catch its example is
   marked broken.
Lost: time for the audit (about 2% of a week, unchecked). Added: rules that work without Sam checking.
Other option: fix rules one at a time as they fail.
