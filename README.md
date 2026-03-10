# ieee-support

## Setup

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install reportlab Pillow
```

## Usage

```bash
source venv/bin/activate
python format_google_chats.py
```

By default, the script reads from `sample_messages/messages_more_pages.json` and outputs `sample_output.pdf`. Edit the variables at the top of `format_google_chats.py` to change the input/output paths and subtitle.
