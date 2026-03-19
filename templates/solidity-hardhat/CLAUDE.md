# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Solidity (0.8.20+)
- Hardhat (Ethereum development environment)
- Ethers.js v6
- TypeScript (strict mode)
- OpenZeppelin Contracts
- Chai (Testing framework)

## Project Structure

```
.
├── contracts/               # Solidity smart contracts
│   ├── Token.sol            # ERC20 / ERC721 definitions
│   ├── Vault.sol            # Core logic
│   └── interfaces/          # Contract interfaces (IVault.sol)
├── scripts/                 # Deployment scripts
│   └── deploy.ts            # Ethers v6 deployment script
├── test/                    # Mocha/Chai tests
│   ├── Token.test.ts
│   └── Vault.test.ts
├── cache/                   # Hardhat cache (gitignored)
├── artifacts/               # Compiled ABIs (gitignored)
├── typechain-types/         # Generated TS types (gitignored)
├── hardhat.config.ts        # Hardhat config (networks, optimizations)
└── package.json
```

## Architecture Rules

- **Inheritance vs Interfaces.** Rely on Interfaces (`IVault.sol`) for inter-contract communication to decouple deployments. Use Inheritance mostly for boilerplate standard integrations (like extending `ERC20` or `Ownable`).
- **Use OpenZeppelin heavily.** Never write your own standards (ERC20, ERC721), ownership patterns (`Ownable`), or math libraries if standard OpenZeppelin implementations exist. Inherit their audited contracts.
- **Gas optimization is architecture.** Minimize storage reads/writes (they cost the most gas). Pack variables in structs tightly (e.g. `uint128` beside `uint128`).
- **Events are the API.** Emit events for every state-altering action: `emit Transfer(from, to, amount)`. Off-chain indexing (The Graph, frontends) relies on events entirely. Do not expect clients to poll the contract for state updates.
- **Reentrancy bounds.** Any function that makes external calls or transfers Ether must use the `nonReentrant` modifier from OpenZeppelin, OR apply the Checks-Effects-Interactions pattern strictly.

## Coding Conventions

- **Solidity Version.** Always pin the exact compiler version in production contracts (`pragma solidity 0.8.24;` instead of `^0.8.24`).
- **Custom Errors.** Use custom errors (e.g., `error Unauthorized();` followed by `revert Unauthorized();`) instead of `require(condition, "Long string error");`. Custom errors save massive amounts of deployment and runtime gas.
- **Visibility explicitly stated.** Mark every function and state variable visibility explicitly (`public`, `private`, `external`, `internal`). Prefer `external` over `public` if a function is never called internally (saves gas).
- **TypeScript Deployment.** Write deployment and task scripts strictly in TypeScript, using `TypeChain` to inject static typing for all Contract instances.
- **Natspec.** Use Natspec comments (`/// @notice`, `/// @dev`, `/// @param`) for all public and external functions. This allows automated doc generation and assists Etherscan verifications.

## Library Preferences

- **Environment:** Hardhat (Very stable TS ecosystem). Foundry (Rust-based) is fine too if preferred, but this specifies Hardhat workflows.
- **Contract Interface:** Ethers.js v6. Not Web3.js. Ethers is safer, modular, and natively built for TypeScript.
- **Type Generation:** TypeChain (generates `.d.ts` definitions straight from compiled ABIs).
- **Tooling:** `hardhat-gas-reporter` and `solidity-coverage` are mandatory additions.
- **Audited Libs:** `@openzeppelin/contracts` (standard token implementations and security boundaries). 

## NEVER DO THIS

1. **Never use `transfer()` or `send()` to forward Ether.** They have a fixed hardcoded 2300 gas stipend which breaks if the receiving contract has complex fallback logic or gas costs shift in future forks. Use `call{value: msg.value}("")` and check the boolean return value.
2. **Never violate Checks-Effects-Interactions.** When modifying state based on a required condition, and sending ETH/tokens, rule is: Check conditions (`require`), modify state (`balance[msg.sender] -= amount`), THEN interact (`call{value}`). Violating this is the fundamental cause of Reentrancy hacks.
3. **Never store unnecessary data on-chain.** Do not store large string details or images on chain. Store an IPFS hash. Storage is the most expensive operation on the EVM.
4. **Never use `tx.origin` for authorization.** It can be spoofed by a malicious contract in the middle of a call chain. Always use `msg.sender` for identifying the direct caller.
5. **Never loop over unbounded arrays.** If you iterate an array that users can append to freely, your function will eventually cause an "Out of Gas" exception, permanently locking functionality.
6. **Never leave math unchecked on old compiler versions.** Solidity 0.8.x handles overflows/underflows natively and reverts. But if you rely on older standard implementations, missing SafeMath is catastrophic.
7. **Never push code to Mainnet without Etherscan verification.** Configure the `etherscan` block in `hardhat.config.ts`. The community must be able to read your exact compiled source.

## Testing

- **100% Branch Coverage.** Smart contracts handle actual financial assets. Write edge case tests for every `require`, every modifier, and every boundary. Use `solidity-coverage`.
- Use **Chai matchers for Hardhat.** Native helpers like `await expect(tx).to.emit(...)` or `await expect(tx).to.be.revertedWithCustomError(...)`.
- **Mainnet forking.** When testing interactions with major protocols (Uniswap, Aave), fork Mainnet in your hardhat config instead of deploying complex mocked environments locally.
