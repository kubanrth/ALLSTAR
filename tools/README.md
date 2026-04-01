# Tools

Python scripts for deterministic execution. Each tool handles:
- API calls
- Data transformations
- File operations
- Database queries

## Guidelines

- Each tool should be testable and idempotent where possible
- Read credentials from `.env`
- Log errors clearly
- Return structured output (JSON, CSV, etc.)
