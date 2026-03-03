# SQL Workflow Cheat Sheet

## Overview
- Bytebase MCP (`mcp__mcphub__bytebase-execute_sql`) is the authoritative entry point for all business SQL queries in this repo. It is complemented by `search_objects` when you need to inspect tables/columns before writing your query.
- The standard data-analysis flow is: **Bytebase SQL → local aggregation/filtering → Chart MCP visualization → content/reporting** (see `capabilities/mcp-servers.md`).
- Additional references include `workflows/DATA_ANALYSIS.md` (five-phase analysis process with best practices) and `references/FAQ.md` (common Bytebase commands + troubleshooting). These are the sources consolidated here for quick recall.

## Bytebase MCP Workflow
1. **Inspect schema** (optional but recommended):
   ```ts
   mcp__mcphub__bytebase-search_objects({
     object_type: 'table',
     pattern: '%orders%',
     detail_level: 'summary',
   });
   ```
2. **Write the SQL** (use CTEs, limit rows, and only select needed columns):
   ```ts
   mcp__mcphub__bytebase-execute_sql({
     sql: `
       WITH recent_orders AS (
         SELECT user_id, SUM(total) AS revenue
         FROM orders
         WHERE created_at > NOW() - INTERVAL '30 days'
         GROUP BY user_id
       )
       SELECT u.name, ro.revenue
       FROM users u
       JOIN recent_orders ro ON u.id = ro.user_id
       ORDER BY ro.revenue DESC
       LIMIT 20
     `,
   });
   ```
3. **Process the result** locally (aggregate, apply business rules, transform into chart-friendly shape).
4. **Generate visualization** with Chart MCP (`generate_line_chart`, `generate_bar_chart`, etc.) or feed the data to higher-level tooling.
5. **Document the findings** in downstream reports or docs (ex: `workflows/DATA_ANALYSIS.md` sample sections).

### Best Practices
- Pre-filter with a CTE before joins to avoid scanning entire tables (see `workflows/DATA_ANALYSIS.md`).
- Always limit row counts and avoid `SELECT *` unless absolutely necessary.
- Pair SQL queries with Chart MCP snippets when presenting dashboards or analysis write-ups.
- Use the FAQ’s troubleshooting steps (`claude mcp list`, `claude mcp remove`, etc.) when connections misbehave.

## Related Links
- `capabilities/mcp-servers.md` – command reference and sample Bytebase + Chart workflows.
- `workflows/DATA_ANALYSIS.md` – five-phase data-analysis playbook (query → chart → story).
- `references/FAQ.md` – explains Bytebase vs. Honeycomb responsibilities and tear-down steps.

## Missing Resources
So far, there are no existing documentation files covering a “Designclaw sqlite” workflow. If that capability exists elsewhere, please point to the directory or keywords so it can be summarized here.