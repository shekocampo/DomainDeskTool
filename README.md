# DomainDeskTool

Introducing DomainDesk — a single-file browser tool for researching domain information and generating a formatted summary note.

## Install & Run

No install required. This is a plain HTML file that runs directly in your browser.

1. Download or clone this repository
2. Open `index.html` in your browser (double-click it, or drag it into Chrome/Safari/Firefox)
3. Start using it — no server, no dependencies, no setup

## Usage

1. Enter the domain at the top
2. Fill in the Research sections
3. Add freeform notes (supports **bold**, *italic*, underline, and bullet points with `*` or `-`)
4. Click **Generate Note**
5. Your note is ready for copying and pasting!

## Features

- Single-file app — everything is in `index.html`
- Dark mode toggle
- Auto-saves form state in `localStorage` — survives page refreshes
- RDAP lookup runs automatically on note generation (registrar, status, expiry, nameservers)
- Quick-access propagation links for A, CNAME, DKIM, DMARC, MX, NS, SOA, and TXT records
- Google Workspace Admin Toolbox link auto-fills with the entered domain
- Auto-links URLs in notes; strips surrounding parentheses from links
- Rich-text and plain-text copy for the generated note
- Dom the Owl mascot with rotating sayings

## Tips

- **Bold/Italic/Underline:** `Cmd+B`, `Cmd+I`, `Cmd+U` in the Notes field
- **Bullets:** Start a line with `*` or `-` followed by a space
- **Paste:** Pasting from external sources strips formatting automatically
- **Dark mode:** Toggle with the button in the top right
