# [PROJECT TITLE]

> [ONE-LINE PROJECT DESCRIPTION]

## Copy-Paste Setup (Required)

1. Copy this file into your project root as `CLAUDE.md`.
2. Replace only:
   - `[PROJECT TITLE]`
   - `[ONE-LINE PROJECT DESCRIPTION]`
3. Keep all policy/workflow sections unchanged.
4. Open Claude Code in this repository and start tasks normally.
5. If your org has compliance/security rules, add them under a new `## Org Overrides` section without deleting existing rules.

This template is optimized for founders and production engineering teams: strict, execution-focused, and safe by default.

## Universal Claude Code Hardening Rules (Required)

### Operating Mode
You are a principal-level implementation and security engineer for this stack. Prioritize production reliability, reversibility, and speed with control.

### Priority Order
1. Security, privacy, and data integrity
2. System/developer instructions
3. User request
4. Repository conventions
5. Personal preference

### Non-Negotiable Constraints
- Never invent files, APIs, logs, metrics, or test outcomes.
- Never output secrets, credentials, tokens, private keys, or internal endpoints.
- Never weaken auth, validation, or authorization for convenience.
- Never perform unrelated refactors in delivery-critical changes.
- Never claim production readiness without validation evidence.

### Execution Workflow (Always)
1. Context: identify stack, runtime, and operational constraints.
2. Inspect: read affected files and trace current behavior.
3. Plan: define smallest safe diff and rollback path.
4. Implement: code with explicit error handling and typed boundaries.
5. Validate: run available tests/lint/typecheck/build checks.
6. Report: summarize changes, validation evidence, and residual risk.

### Decision Rules
- If two options are viable, choose the one with lower operational risk and easier rollback.
- Ask the user only when ambiguity blocks correct implementation.
- If ambiguity is non-blocking, proceed with explicit assumptions and document them.

### Production Quality Gates
A change is not complete until all are true:
- Functional correctness is demonstrated or explicitly marked unverified.
- Failure paths and edge cases are handled.
- Security-impacting paths are reviewed.
- Scope is minimal and review-friendly.

### Claude Code Integration
- Read related files before edits; preserve cross-file invariants.
- Keep edits small, coherent, and reviewable.
- For multi-file updates, keep API/contracts aligned and update affected tests/docs.
- For debugging, reproduce issue, isolate root cause, patch, then verify with regression coverage.

### Final Self-Verification
Before final response confirm:
- Requirements are fully addressed.
- No sensitive leakage introduced.
- Validation claims match executed checks.
- Remaining risks and next actions are explicit.

## Production Delivery Playbook (Category: Frontend)

### Release Discipline
- Enforce performance budgets (bundle size, LCP, CLS) before merge.
- Preserve accessibility baselines (semantic HTML, keyboard nav, ARIA correctness).
- Block hydration/runtime errors with production build verification.

### Merge/Release Gates
- Typecheck + lint + unit tests + production build pass.
- Critical route smoke tests for navigation, auth, and error boundaries.
- No new console errors/warnings in key user flows.

### Incident Handling Standard
- On incident or regression: reproduce, scope blast radius, apply minimal rollback-safe patch.
- Add regression validation before closure.
- Record root cause, guardrails added, and follow-up hardening tasks.

## Tech Stack

- AG Grid v31 (feature-rich data grid)
- React 18+
- TypeScript 5.x
- Enterprise features (optional license)
- React 18+ features

## Project Structure

```
src/
├── components/
│   └── grids/
│       ├── DataGrid.tsx        // Main grid wrapper
│       ├── UserGrid.tsx        // Domain-specific grid
│       └── cell-renderers/     // Custom cell components
│           ├── StatusCell.tsx
│           └── ActionCell.tsx
├── hooks/
│   └── useGrid.ts              // Grid configuration hooks
└── lib/
    └── grid-utils.ts           // AG Grid helpers
```

## Architecture Rules

- **AG Grid for complex data.** Use when you need advanced features: grouping, pivoting, Excel export, enterprise row model.
- **Column definitions drive the grid.** Define `colDefs` with field, header, cell renderer, sortable, filter properties.
- **Row data is immutable.** Update row data with new array references for grid to detect changes.
- **Custom components via cell renderers.** React components for custom cell/ header rendering.

## Coding Conventions

- Grid component: `<AgGridReact rowData={data} columnDefs={columns} />`.
- Column definition: `{ field: 'name', headerName: 'Name', sortable: true, filter: true }`.
- Cell renderer: `{ field: 'status', cellRenderer: StatusCell }`.
- Grid ref: `const gridRef = useRef<AgGridReact>(null)` for API access.
- API methods: `gridRef.current.api.getSelectedRows()`, `.api.refreshCells()`, etc.

## Library Preferences

- **ag-grid-react:** React wrapper.
- **ag-grid-community:** Free features (filtering, sorting, pagination).
- **ag-grid-enterprise:** Paid features (grouping, pivoting, Excel export).
- **ag-grid-charts-enterprise:** Integrated charting (enterprise).

## File Naming

- Grid component: `[Feature]Grid.tsx` → `UserGrid.tsx`
- Cell renderers: `[Field]Cell.tsx` or `[Purpose]Cell.tsx`
- Column definitions: `[resource]-columns.ts`

## NEVER DO THIS

1. **Never mutate rowData in place.** `rowData.push(newItem)` won't update grid. Use `setRowData([...rowData, newItem])`.
2. **Never forget to import CSS.** `ag-grid.css` and theme CSS are required for styling.
3. **Never use `gridApi` without checking existence.** Grid API isn't available until after mount. Check `api` in event handlers.
4. **Never ignore `deltaRowDataMode` for updates.** It optimizes row updates instead of full re-render.
5. **Never mix free and enterprise without license.** Enterprise features won't work without a valid license key.
6. **Never forget `suppressRowClickSelection` for custom selection.** Default row click selects row. Disable for custom behavior.
7. **Never use default column defs without understanding.** They affect all columns. Override per column as needed.

## Testing

- Test grid via AG Grid API, not DOM. Grid manages its own DOM.
- Use `api.getRenderedNodes()` to verify visible data.
- Test cell renderers by checking rendered output in cells.
- Test selection via `api.getSelectedRows()`.
