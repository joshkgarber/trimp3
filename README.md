# trimp3

A simple Python CLI tool to trim silence from the beginning and end of MP3 audio files.

## Features

- Automatically detects and removes leading and trailing silence
- Batch processes entire directories of MP3 files
- Smart tracking: uses ID3 tags to avoid re-processing already-trimmed files
- Configurable silence threshold (-50 dBFS default)

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd trimp3

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Usage

```bash
uv run python main.py <directory_path>
```

### Example

```bash
uv run python main.py ./my-recordings/
```

The tool will:
1. Find all `.mp3` files in the directory
2. Skip files already marked with `silence_trimmed` tag
3. Trim silence from start and end of each file
4. Save trimmed audio (overwrites original)
5. Add `silence_trimmed` ID3 tag

## How It Works

- Scans audio in 5ms chunks to find first/last sound
- Detects silence below -50 dBFS threshold
- Uses `pydub` for audio manipulation
- Uses `mutagen` for ID3 metadata tagging

## Dependencies

- `pydub` >= 0.25.1 — Audio processing
- `mutagen` >= 1.47.0 — Metadata handling

## Project Structure

```
trimp3/
├── main.py           # Main application
├── pyproject.toml    # Project config & dependencies
├── uv.lock          # Locked dependencies
└── README.md        # This file
```

## Development

```bash
# Run with uv
uv run python main.py <path>

# Or activate venv
source .venv/bin/activate
python main.py <path>
```

## License

MIT License - see [LICENSE](LICENSE) for details.
