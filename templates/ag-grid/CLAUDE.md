# [PROJECT NAME] - [ONE LINE DESCRIPTION]

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

