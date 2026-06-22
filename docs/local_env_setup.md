# Local Environment Setup

## Configure Once

Create `.env.local` in the repository root using `.env.example` as the template:

```dotenv
GEMINI_API_KEY=PASTE_YOUR_KEY_HERE
GEMINI_MODEL=gemini-3.1-flash-lite
GEMINI_REQUEST_SLEEP_SECONDS=5
```

Replace the placeholder only in `.env.local`. Never put a real key in `.env.example`, source control, chat, screenshots, command output, or logs. `.env.local`, `.env`, wildcard `.env.*` files, and `secrets.txt` are ignored by Git; `.env.example` is explicitly retained as the safe template.

## Precedence

API runners load `.env.local` first and then `.env`. A variable already present in the shell environment is never overwritten. Values loaded from `.env.local` also take precedence over values in `.env`.

After creating `.env.local`, run an API script directly without manually exporting variables:

```bash
python run_gemini_trajectory_rater_experiment2_flash_lite.py
```

The loader does not print values and reports only variable names to callers.

## Key Exposure

If an API key was pasted into chat, a terminal transcript, logs, or any tracked file, treat it as exposed: revoke or rotate it with the provider, update the local `.env.local`, and remove the exposed material from applicable history.
