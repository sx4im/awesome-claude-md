# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Rust (nightly for some embedded features, or stable with minimal feature gates)
- `no_std` + `no_main` environment
- [HAL: embassy-stm32 / embassy-nrf / esp-hal / rp-hal] for hardware abstraction
- Embassy async runtime (or RTIC for interrupt-driven designs)
- probe-rs for flashing and debugging
- [TARGET: thumbv7em-none-eabihf / riscv32imc-unknown-none-elf]

## Project Structure

```
src/
├── main.rs                   # #[embassy_executor::main] entry, task spawning, peripheral init
├── tasks/
│   ├── mod.rs                # Task module declarations
│   ├── sensors.rs            # Sensor reading tasks (async loops, timers)
│   ├── comms.rs              # Communication tasks (UART, SPI, I2C handlers)
│   └── control.rs            # Control loop tasks (PID, state machines)
├── drivers/
│   ├── mod.rs                # Custom peripheral driver definitions
│   └── [DEVICE].rs           # Device-specific drivers (LCD, sensor ICs, motor controllers)
├── config/
│   ├── mod.rs                # Hardware configuration, pin assignments
│   └── constants.rs          # System constants (frequencies, thresholds, buffer sizes)
├── types/
│   └── mod.rs                # Shared types, error enums, measurement structs
├── util/
│   └── mod.rs                # Math helpers, fixed-point, CRC, encoding utilities
.cargo/
└── config.toml               # Target triple, linker, probe-rs runner
Cargo.toml                    # Dependencies, features, profile.release optimizations
memory.x                      # Linker script: FLASH and RAM memory regions
build.rs                      # Build script (if needed for linker script copying)
```

## Architecture Rules

- **`no_std` means no heap by default.** No `Vec`, no `String`, no `Box` unless you set up an allocator (don't, unless you have a very good reason). Use fixed-size arrays, `heapless::Vec`, `heapless::String`, and stack allocation. If you need dynamic collections, use `heapless` with compile-time capacity.
- **Embassy tasks are the concurrency model.** Each independent concern (sensor polling, UART RX, control loop) is an `#[embassy_executor::task]` async function. Tasks yield at `.await` points. Never block in a task; use `Timer::after()` instead of busy-wait loops.
- **Peripherals are owned, not shared.** Embassy's HAL takes ownership of peripheral singletons at init. Pass peripherals into the tasks that use them. If two tasks need the same peripheral, use `embassy_sync::Mutex` (not `core::sync`). Sharing via `static mut` is undefined behavior.
- **Interrupts are abstracted by the HAL.** Embassy and RTIC handle interrupt routing. Never write raw interrupt handlers unless the HAL genuinely doesn't support your peripheral. If you must, use `#[interrupt]` with critical sections via `cortex_m::interrupt::free()`.
- **All errors are handled, never unwrapped.** In embedded, a panic halts the device with no recovery. Use `Result<T, E>` everywhere. Implement a `#[panic_handler]` that does something useful (blink an LED, write to UART, trigger watchdog reset). Never `.unwrap()` in production code.

## Coding Conventions

- **Pin configuration is centralized in `config/`.** All pin assignments (`PA5`, `PB3`, etc.) are defined in one place with descriptive names: `const LED_PIN: PA5 = ...`. Never hardcode pin identifiers in driver or task code.
- **Use type-state patterns for hardware modes.** A GPIO pin configured as output has a different type than input. The HAL enforces this at compile time. Never try to read from an output pin or write to an input pin; the type system prevents it.
- **Fixed-point math over floating-point on Cortex-M0/M3.** Targets without FPU use software float emulation, which is slow. Use integer math with fixed-point scaling (multiply by 1000, divide at the boundary). On Cortex-M4F and above, hardware float is fine.
- **DMA for bulk transfers.** Use DMA-backed UART, SPI, and I2C transfers for anything over a few bytes. Embassy's HAL provides async DMA methods. Never bit-bang or busy-loop on byte-by-byte transfers for bulk data.
- **Logging uses `defmt`, not `println!`.** `defmt` is a deferred formatting framework that sends format string indices over the wire (minimal bandwidth). Use `defmt::info!()`, `defmt::error!()`. Never use `core::fmt` or `alloc::format!` (too large for flash).

## Library Preferences

- **Async runtime:** Embassy for new projects. RTIC if you prefer a purely interrupt-driven model without async. Not bare-metal polling loops (hard to maintain, no concurrency story).
- **HAL:** `embassy-stm32` / `embassy-nrf` / `esp-hal` matching your target. Not raw PAC register manipulation unless the HAL doesn't cover your peripheral.
- **Collections:** `heapless` for `Vec`, `String`, `Queue`, `FnvIndexMap` with fixed capacity. Not `alloc` (heap fragmentation on embedded is fatal).
- **Serialization:** `postcard` (no_std serde, compact binary). Not `serde_json` (requires alloc, verbose for constrained bandwidth).
- **Logging:** `defmt` + `defmt-rtt` for development. `defmt-serial` for UART logging in production. Not `log` crate (too heavyweight, string formatting bloats flash).
- **Testing on host:** `embedded-hal-mock` for mocking HAL traits in unit tests.

## File Naming

- Tasks: `snake_case.rs` describing the concern → `sensor_poll.rs`, `uart_rx.rs`, `motor_control.rs`
- Drivers: `snake_case.rs` matching the device → `bme280.rs`, `ssd1306.rs`, `drv8825.rs`
- Config: `snake_case.rs` → `pin_config.rs`, `constants.rs`
- Cargo target: defined in `.cargo/config.toml`, not in `Cargo.toml`

## NEVER DO THIS

1. **Never use `std`.** There is no operating system. `use std::*` will not compile. All imports come from `core`, `alloc` (if you set up an allocator), or `no_std`-compatible crates.
2. **Never `.unwrap()` or `.expect()` in production firmware.** A panic in embedded halts the device. There is no stack trace, no error recovery. Use `match`, `if let`, or `unwrap_or()` with a safe default. Reserve `.unwrap()` for values proven at compile time.
3. **Never use `static mut`.** It is unsound and requires `unsafe` for every access. Use `embassy_sync::Mutex`, `embassy_sync::Signal`, or `embassy_sync::Channel` for shared state between tasks. For interrupt-safe sharing in RTIC, use resources.
4. **Never busy-wait in an async task.** `loop { if pin.is_high() { break; } }` blocks the executor and starves other tasks. Use `pin.wait_for_high().await` or `Timer::after(Duration::from_millis(10)).await` for polling.
5. **Never ignore flash and RAM sizes.** Embedded targets have kilobytes, not gigabytes. Check `cargo size` output after every dependency addition. A single `format!()` call can add 20KB of flash usage. Set `opt-level = "z"` and `lto = true` in release profile.
6. **Never assume peripheral clock speeds.** Always configure clocks explicitly in `main()` before initializing peripherals. Default clock configurations vary between chip revisions and boards. A UART configured for 115200 baud at the wrong clock speed produces garbage.
7. **Never allocate large buffers on the stack.** Embedded stacks are typically 4-16KB. A `[u8; 4096]` local variable can overflow the stack silently, corrupting adjacent memory. Use `static` buffers or `heapless` containers.

## Testing

- Use `cargo test` with `#[cfg(test)]` modules for pure logic (math, encoding, state machines). These run on the host, not the target.
- Use `embedded-hal-mock` to mock I2C, SPI, UART traits for driver unit tests on the host.
- Integration test on real hardware with `probe-rs run`. Create test firmware that exercises peripherals and reports results over UART/defmt.
- Use `defmt-test` for on-target test frameworks that run tests on the microcontroller and report via defmt.
- Monitor stack usage with `flip-link` (linker wrapper that puts the stack at the bottom of RAM so overflow triggers a hard fault instead of silent corruption).
