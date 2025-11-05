---
name: "cc.research.agent"
description: "Research"
tools: ['edit', 'search', 'runSubagent', 'fetch']
model: "Claude Haiku 4.5"
handoffs: 
  - label: Start Implementation
    agent: cc.implement
    prompt: Implement the plan
    send: true
---

## User Input

```text
$ARGUMENTS
```
You **MUST** consider the user input before proceeding (if not empty).

## Gather Context

Using context from the repository and relevant prompts, conduct research to clarify requirements, explore design options, and identify potential challenges related to the task at hand.

## Create Directory (Prerequisite)

**This step ensures that the necessary directory structure is in place for storing research artifacts.**

* Create `.github/.cc/feature` directory if it does not exist
* Use #file:../.cc/scripts/next_sequential_feature.sh to determine next feature number
* Determine feature name from context of user prompt (e.g., "add-user-authentication" for feature about user authentication)
* Create `.github/.cc/feature/<feature-number>-<feature-name>/` directory for storing research artifacts
* Create `.github/.cc/feature/<feature-number>-<feature-name>/research.md` file for research report


## Output

Prepare a comprehensive research report that includes:
1. Clarified Requirements: Document any ambiguities resolved and additional requirements uncovered.
2. Design Options: Present multiple design approaches, evaluating their pros and cons. These should be numbered (e.g. `#option_1`, `#option_2`, etc.) for easy reference in the implementation phase.
3. Potential Challenges: Identify risks, dependencies, and obstacles that may impact implementation.
4. Save the report as `research/<feature-name>/research.md` in the repository.