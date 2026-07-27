# AutoSocial AI

AutoSocial is a completely autonomous, AI-powered Instagram engine. It uses a high-end multi-LLM fallback architecture to generate compelling concepts, renders stunning editorial graphics natively in Python, and publishes directly to Instagram with trending music.

## Features

- **Multi-LLM Fallback Engine:** Intelligently switches between OpenAI, Google Gemini, and Groq to ensure 100% uptime for concept and caption generation, automatically bypassing rate limits.
- **Pillow Editorial Engine:** A highly advanced, pure Python graphic renderer that natively draws a complex "Editorial Dispatch" design. It handles dynamic Google font loading, layout auto-fitting, deterministic styling, mesh gradients, and SVG-like concentric seals—all without relying on heavy headless browsers like Playwright.
- **Pollinations AI Fallback:** Seamlessly swaps to unlimited free AI image generation if needed.
- **Instagrapi Publisher:** Automatically uploads generated posts to Instagram and intelligently searches for and attaches matching background music to photos.
- **Beautiful CLI Dashboard:** A polished, gradient-styled terminal dashboard that tracks the orchestration pipeline in real time.

## Installation

1. Clone the repository and navigate into the directory:
   ```bash
   git clone https://github.com/chriz-3656/autosocial.git
   cd autosocial
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Download required fonts (Inter, Fraunces, IBM Plex Mono) for the Pillow renderer:
   ```bash
   python download_fonts.py
   ```

4. Configure environment variables. Create a `.env` file based on `.env.example` and add your API keys:
   ```
   OPENAI_API_KEY=your_key
   GEMINI_API_KEY=your_key
   GROQ_API_KEY=your_key
   INSTAGRAM_USERNAME=your_username
   INSTAGRAM_PASSWORD=your_password
   ```

## Usage

Start the autonomous pipeline using the beautiful terminal UI:

```bash
./start_autosocial.sh
```

## Architecture

- `src/autosocial/core/`: Application settings and centralized configurations.
- `src/autosocial/providers/`: The multi-LLM pipeline orchestration (OpenAI, Gemini, Groq).
- `src/autosocial/renderers/`: The Pillow Editorial engine and Pollinations fallback.
- `src/autosocial/publishers/`: Instagrapi controller for uploading photos and fetching audio tracks.
- `run_real.py`: The main Python orchestrator connecting the components.
- `start_autosocial.sh`: The stylized bash runner.
