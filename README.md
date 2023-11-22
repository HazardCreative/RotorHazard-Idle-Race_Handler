# RotorHazard Idle Race Handler
Race management plugin for RotorHazard

Stops, saves, or restarts a race when no passes have arrived in [x] seconds

## Installation

Copy the `idle_race_handler` plugin into the `src/server/plugins` directory in your RotorHazard install. Start RotorHazard.

If installation is successful, the RotorHazard log will contain the message `Loaded plugin module idle_race_handler` at startup.

## Usage

- Set desired idle timeout and behavior within the panel on the `Run` page.
- Idle timeout begins after first lap crossing.
- Behavior activates when timeout expires.