# Sam's messages, chat cse_01J1JB7YavKKmix5DmAqXf5d (handover.py log)

### 2026-11-27T10:38:25
Continue weekly spike analysis chat and incorporate the following message.

Provide report


Problem:

Why routine fixing cost so much:
1. The fixing chats spent most of their steps searching our shared tools, not the film. These are the drawing and checking tools every film uses. In the four fixing chats, 48–95 of every ~140 steps went on that search. Only 13–22 went on the film itself. Those tools are now about 200,000 lines, and a fix to a face or a seat has to be traced through many checks before it's safe.
2. Every step re-reads the whole chat so far. A chat starts with about 85,000 words' worth of rules before it does anything, and grows to 200,000–300,000 by the end. Chat 30 read about 27 million words' worth in total to write about 77,000. So the number of steps is what drives the cost.
3. Reading the rules at the start was a quarter to a third of every fixing chat, and that was paid again in all 10 chats.
4. The animatic chat ran on the expensive model. It was set up on the cheaper one and switched partway. It then spent 3 hours mostly discussing how to test our fault-spotting, which isn't film work. It restarted 5 times, and each restart paid to re-read everything. Our rule says a routine chat on the wrong model should stop and hand on; it didn't.
5. Our cost log undercounts. It estimated chat 36 at $4.71; the app says $12.50. So the early warnings saw less than was really spent.
Compared with before: each step costs about the same as on the Milburn and Grand Theft Autism films. What grew is the number of steps per fix: chat 30 took about 35 steps per note. I can't give a reliable steps-per-note figure for older films from the records, so I can't say exactly how much it grew.

Summary: the code search tool was designed to save on usage and use instead caused a major expense spike. Nothing can be accomplished until this is in control and achieving what it set out to.

Propose a solution that condenses and organises shared tools so the code search tool doesn’t have to work so hard, read so much, and do so many steps per edit.

Propose your own ideas, research solutions — anything to get this urgent problem solved.

This is google’s suggestion:

Step 0: Verify the 85,000-Word Floor Before Touching Configs
Claude Code’s native system prompt and built-in tools normally take ~15k–25k tokens (~11k–19k words), not 85,000 words (~110k+ tokens). Before treating that startup cost as an unchangeable Anthropic tax, run /context on turn 1 of a fresh session.
* If MCP tools or Memory/Custom instructions are huge: You have connected MCP servers, global ~/.claude/CLAUDE.md files, or startup hooks injecting massive schemas/rules. Disable unused MCP servers for routine fixing (claude mcp remove or a stripped-down .mcp.jsonpassed via --mcp-config) to immediately slash your startup floor. 
* If System prompt + System tools truly account for the bulk of it: Treat the baseline as a fixed per-step tax and focus strictly on cutting step count and keeping prompt caches warm.



1. Replace LLM Tool-Searching with a Deterministic Map (Bottleneck #1)
* Why: Spending 48–95 of every ~140 steps grepping 200,000 lines of shared drawing/checking tools is your biggest cost multiplier—and delegating that search to a cheaper model (like Haiku) risks missed dependencies that force your main model to re-search anyway.
* The Fix: Write a small Python/AST or ripgrep script (run outside Claude, costing $0.00) that parses your 200k-line toolset and generates a static, flat TOOL_MAP.md (or tool_index.json) mapping:
    * Film element / asset type (e.g., face, seat, rig, animatic)
    * Which checking functions validate it + exact file:line locations
    * Input/output signatures
* Instruct Claude in your project rules to read TOOL_MAP.md first and jump straight to the exact file:line instead of running open-ended Grep loops across 200k lines.



2. Cut Step Count & Protect Prompt Caching (Bottlenecks #2 & #3)
* Keep Sessions Continuous Within the Cache Window: With a massive starting context, every restart or idle gap longer than Claude’s prompt-cache TTL (~5 minutes) forces you to pay full cache-write prices on all 85,000 words again (as happened across the 5 restarts in your animatic chat). Batch 2–3 related notes back-to-back in one warm session rather than restarting between notes.
* Enforce a Hard Turn Budget (--max-turns): Because every step re-reads the growing transcript (up to 200k–300k words), cap routine fixing runs using Claude Code’s CLI flag (e.g., claude -p ... --max-turns 45). If a note isn't solved in 45 steps, stop and inspect why instead of letting it spiral to 140 steps.
* Keep the Top of Your Context Static: Never inject dynamic timestamps, git hashes, or note IDs into CLAUDE.md or early system messages—any change at the top invalidates Anthropic's prefix cache for the entire session.



3. Hard-Lock Models & Fix Cost Telemetry (Bottlenecks #4 & #5)
* Enforce Model Tier in CLI/Settings, Not Prompts: An LLM inside a debugging loop will routinely ignore a text rule telling it to abort if it's on Opus. Enforce your cheaper model at the infrastructure level using claude --model sonnet in your launch wrapper and "model": "sonnet" in .claude/settings.json.
* Switch to Native Billing Telemetry: Stop estimating cost from word counts (which missed the hidden ~110k system/tool tokens and cache writes, causing the $4.71 vs. $12.50 gap). Read exact session spend directly from Claude Code’s --output-format json(total_cost_usd) or enable Claude Code’s OpenTelemetry (OTEL) metrics to trigger real-time spend alerts.



Execution Order (Highest ROI First)
1. Run /context on a blank session to check if MCP servers are inflating the 85k-word floor.
2. Lock --model sonnet and --max-turns 45 in your launch wrapper, and switch your spend alert to total_cost_usd (fixes Bottlenecks #4 and #5 immediately).
3. Generate TOOL_MAP.md with a static script so fixing chats drop from ~35 steps/note down to ~10–15 steps/note (fixes Bottlenecks #1, #2, and #3).
If Google advice bad, disregard
(handover log: not found in the chat record after 20 s; saved as Sam's)

### 2026-11-27T10:48:27
Y
Y 
Report back on how solved the problem is once done

