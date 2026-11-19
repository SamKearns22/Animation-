# The chat's own version (written before the helpers ran)

Extend the existing Stop hook (propose.py hook) with a shape check, and fix the route's own output to match.

1. When the hook finds a system-change ask (the same `questions` / `is_change` test, or a named proposal), it also
   reads the message around it and requires, per option: a short plain problem (one or two sentences), numbered
   steps (lines starting "1." "2." ...), a "Why" part, a "You'd notice" part, an "Other option" part, one "Lost:" and
   one "Added:" line.
2. Words: a list of project words Sam has not been taught (guard, hook, pre-flight, kit, ledger, named line, kittest,
   rig, verdict, helper, judge, chain, any file name or code name with _ . / or CamelCase). Each one that appears must
   be followed within the same sentence by an explanation in brackets or after a comma/"which"/"meaning". File names
   and code names are refused outright (the rule says no code names).
3. Blocked replies get the list of what is missing; the second try is still let through but logged (as now).
4. judge.md's "For Sam" shape and `show` change to the full plain shape, so the route's output already passes.
5. Tests in kittests: the Milburn review's lesson list is blocked; a full plain-format message passes; routine
   animatic and clip asks are untouched.

Lost: a little more writing per ask. Added: every system ask in the plain shape.
Other option: a separate "plain.py" tool the chat runs before sending (relies on the chat remembering).
