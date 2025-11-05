---
description: "Trivial agent to show how handoffs and subagents work"
tools: ['search', 'edit', 'fetch']
model: "Claude Haiku 4.5"
handoffs: 
  - label: Start Implementation
    agent: cc.implement
    prompt: Implement the plan
    send: false
---

# Research Agent

Do a bit of research.