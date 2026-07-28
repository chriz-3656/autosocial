# Changelog

## [Unreleased]
### Added
- **AI Art Director & Design Generator (`run_design.py`)**: A two-stage pipeline for generating customized, premium designs from a creative brief. The AI acts as an Art Director, outputting a strictly validated JSON `DesignSpec` which is then deterministically rendered using Pillow.
- **Strict JSON Object Mode for Groq**: `FallbackProvider` now natively supports `generate_json` using Groq's `response_format={"type": "json_object"}`.
- **Design Rendering Utilities**: Abstracted gradient rendering, contrast ratio checking, and text-fitting logic.

### Fixed
- **Groq Timeout Issue**: Increased the `httpx` timeout in `GroqProvider` from 5s to 60s to prevent `ReadTimeout` exceptions when generating longer completions.
- **UnboundLocalError**: Fixed a shadowing issue with `PillowPaperNotesRenderer` import in `run_real.py`.
- **Text Readability & Highlights**: Increased the threshold for the `highlight` layout in `PillowPaperNotesRenderer` to 150 characters, ensuring AI-generated quotes consistently trigger the yellow marker and red underline aesthetic.
