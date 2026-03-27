# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Nix v2.20+ with flakes and the new nix CLI enabled
- Nixpkgs 24.05 (stable) or nixpkgs-unstable as the primary package source
- flake-utils or flake-parts for multi-system flake scaffolding
- devenv or devShells for reproducible development environments
- NixOS modules for system configuration and service declarations
- home-manager for user-level dotfile and tool management
- nix-darwin for macOS system configuration alongside NixOS
- cachix or Attic for binary cache hosting

## Project Structure

```
.
├── flake.nix
├── flake.lock
├── lib/
│   ├── default.nix
│   └── helpers.nix
├── packages/
│   ├── my-app/
│   │   └── default.nix
│   └── my-tool/
│       └── default.nix
├── modules/
│   ├── nixos/
│   │   ├── common.nix
│   │   ├── networking.nix
│   │   └── services/
│   │       ├── postgres.nix
│   │       └── nginx.nix
│   └── home-manager/
│       ├── shell.nix
│       ├── git.nix
│       └── editor.nix
├── overlays/
│   └── default.nix
├── hosts/
│   ├── server-01/
│   │   ├── default.nix
│   │   ├── hardware-configuration.nix
│   │   └── disk-config.nix
│   └── workstation/
│       └── default.nix
├── shells/
│   └── default.nix
└── checks/
    └── default.nix
```

## Architecture Rules

- The flake.nix must be the single entry point; all imports flow through it using the inputs system
- Use flake-parts or flake-utils to generate outputs for all supported systems: x86_64-linux, aarch64-linux, x86_64-darwin, aarch64-darwin
- Pin nixpkgs to a specific commit via flake.lock; run nix flake update on a weekly cadence with CI verification
- All packages must be buildable with nix build .#packageName and testable with nix flake check
- NixOS modules must use the options/config pattern with mkOption and mkEnableOption for all configurable values
- devShells must include all build dependencies so that nix develop provides a complete working environment
- Overlays must be composed in a single overlays/default.nix and applied via nixpkgs.overlays in the flake

## Coding Conventions

- Use the lib.mkOption pattern with explicit type, default, and description for every NixOS module option
- Prefer callPackage over raw import for package definitions to enable dependency injection
- Use rec only when truly needed for self-referential sets; prefer let bindings for local variables
- String interpolation: use double-single-quoted strings ''...'' for multiline, regular quotes for single-line
- Use lib.mkIf and lib.mkMerge for conditional configuration in modules; never use raw if-then-else at the module level
- Attribute paths use camelCase for custom options: services.myApp.enableMetrics
- List all runtime dependencies in buildInputs and build-time-only tools in nativeBuildInputs

## Library Preferences

- Use flake-parts over raw flake outputs for cleaner multi-system support
- Use dream2nix or buildNpmPackage for Node.js projects, poetry2nix for Python projects
- Use crane or naersk for Rust projects; crane is preferred for workspace-aware builds
- Use gomod2nix or buildGoModule for Go projects
- Use treefmt-nix for unified formatting (nixfmt-rfc-style for Nix, prettier for JS/TS, black for Python)
- Use pre-commit-hooks.nix for Git hook management within the flake
- Use disko for declarative disk partitioning on NixOS hosts

## File Naming

- Package derivations: packages/{name}/default.nix
- NixOS modules: modules/nixos/{concern}.nix or modules/nixos/services/{service}.nix
- Home-manager modules: modules/home-manager/{tool}.nix
- Host configurations: hosts/{hostname}/default.nix
- Dev shells: shells/default.nix or shells/{purpose}.nix
- Overlay files: overlays/default.nix (aggregator) with individual overlays as functions

## NEVER DO THIS

1. Never use with pkgs; at the top level of a module; it pollutes the namespace and makes attribute origins untraceable
2. Never use builtins.fetchTarball or builtins.fetchGit in a flake; use flake inputs for all external dependencies
3. Never commit a flake.lock with unfixed narHash values; always run nix flake lock after adding inputs
4. Never use nix-env -i for package installation; use declarative profiles or devShells
5. Never put secrets in Nix files; use agenix or sops-nix for secret management with age or GPG encryption
6. Never use rec {} for the top-level package set; it causes infinite recursion and is a common source of evaluation errors
7. Never mix tabs and spaces; Nix files must use 2-space indentation exclusively

## Testing

- Run nix flake check on every PR to validate all packages, devShells, NixOS configurations, and custom checks
- Write nix build tests for every package and verify they produce expected outputs in a CI sandbox
- NixOS modules must have NixOS VM tests using nixos/lib/testing-python.nix that spin up VMs and run assertions
- Use nix fmt to enforce consistent formatting with nixfmt-rfc-style; fail CI on formatting violations
- Test devShells by running nix develop --command bash -c "command --version" for each expected tool
- Pin CI to the same nixpkgs revision as flake.lock to ensure reproducibility
- Use nix-diff to compare derivations between flake.lock updates and review dependency changes
