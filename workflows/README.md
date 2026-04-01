# Workflows

Markdown SOPs (Standard Operating Procedures) that define how to accomplish specific tasks.

## Workflow Structure

Each workflow should include:
1. **Objective** - What are we trying to do?
2. **Required Inputs** - What data/parameters are needed?
3. **Required Tools** - Which Python scripts are required?
4. **Steps** - The actual execution sequence
5. **Expected Output** - What should we get?
6. **Error Handling** - What do we do if something breaks?
7. **Notes** - Constraints, rate limits, timing quirks

## Example Workflow Template

```markdown
# Workflow: [Name]

## Objective
[What this workflow does]

## Required Inputs
- Input 1: [description]
- Input 2: [description]

## Required Tools
- `tools/script_name.py`

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Output
[What you should have at the end]

## Error Handling
- If [error], then [action]

## Notes
- [Any special considerations]
```
