# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- TanStack Table v8 (headless table library)
- React 18+
- TypeScript 5.x
- React 18+ features
- Any UI library (or unstyled)

## Project Structure

```
src/
├── components/
│   ├── table/                  // Table components
│   │   ├── DataTable.tsx       // Main table component
│   │   ├── TablePagination.tsx
│   │   └── TableSorting.tsx
│   └── ui/
│       └── Table.tsx           // UI primitives
├── hooks/
│   └── useDataTable.ts         // Table configuration hooks
└── lib/
    └── table-utils.ts          // Table helpers
```

## Architecture Rules

- **Headless table logic.** TanStack Table provides state management, sorting, filtering, pagination. You provide the UI.
- **Column definitions central.** Define columns with `columnHelper` or array syntax. Include accessor, header, cell renderers.
- **State controlled or uncontrolled.** Table can manage its own state or receive state from parent.
- **FlexTable or React Table API.** Choose between `useReactTable` (full control) or `useTable` (simpler).

## Coding Conventions

- Create table: `const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })`.
- Define columns: `const columns = [{ accessorKey: 'name', header: 'Name', cell: info => info.getValue() }]`.
- Render rows: `table.getRowModel().rows.map(row => ...)`.
- Render cells: `row.getVisibleCells().map(cell => flexRender(cell.column.columnDef.cell, cell.getContext()))`.
- Sorting: `column.getToggleSortingHandler()`, `column.getIsSorted()`.

## Library Preferences

- **@tanstack/react-table:** Core React integration.
- **@tanstack/table-core:** Headless core if building custom framework adapter.
- **Any UI library:** MUI, Chakra, Tailwind, etc. TanStack Table is headless.

## File Naming

- Table component: `DataTable.tsx`, `[Feature]Table.tsx`
- Column definitions: `[resource]-columns.ts` → `user-columns.ts`
- Hooks: `use[Feature]Table.ts`

## NEVER DO THIS

1. **Never use TanStack Table v7 syntax in v8.** v8 is a complete rewrite. APIs are different.
2. **Never forget row models.** `getCoreRowModel()`, `getSortedRowModel()`, etc. are required for features.
3. **Never render without `flexRender`.** `cell.getValue()` is raw data. `flexRender` handles custom cell components.
4. **Never mutate table data directly.** Update your source data, table re-renders with new reference.
5. **Never ignore `meta` for custom data.** Pass custom data to cells via `meta` in column definition.
6. **Never skip pagination row models.** Without `getPaginationRowModel()`, pagination won't work.
7. **Never use `useMemo` incorrectly.** Data and columns should be memoized to prevent unnecessary re-renders.

## Testing

- Test table logic without UI. TanStack Table is pure JavaScript.
- Test sorting by calling `column.toggleSorting()` and checking row order.
- Test filtering by setting filter values and checking filtered rows.
- Test pagination by navigating pages and checking row count.

