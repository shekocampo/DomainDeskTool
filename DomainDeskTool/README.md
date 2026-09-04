# DomainDesk

An internal tool for Squarespace Associates to research domain issues and generate formatted internal notes.

## What it does

Enter a domain and fill in the relevant sections — DomainDesk will:

- Look up domain registration details automatically via **RDAP** (registrar, status, expiry, nameservers)
- Provide quick-access **propagation tracking links** (WhatsMyDNS, DNSChecker) for NS, CNAME, A, MX, TXT, DMARC, DKIM, and SOA records
- Check for a **Google Workspace** account associated with the domain
- Generate a clean, copy-ready **internal note** summarizing all findings

The generated note supports inline editing, rich-text and plain-text copy, and clickable links.

## Usage

Open `index.html` directly in a browser — no server or build step needed.

1. Enter the customer's domain
2. Fill in the Ticket and Research sections as needed
3. Add any freeform notes (supports bold, italic, underline, and bullet points)
4. Click **Generate Note**
5. Copy the note into your ticket

## Features

- Single-file app (`index.html`) — no dependencies, no install
- Dark mode toggle
- Form state persisted in `localStorage` — your work survives a page refresh
- Auto-links URLs in notes; strips surrounding parentheses from links
- RDAP lookup runs automatically on note generation
- Friendly owl mascot (Dom) with rotating sayings

## Files

| File | Purpose |
|------|---------|
| `index.html` | The entire app — HTML, CSS, and JS in one file |
| `main.py` / `config.py` | Python scripts (separate utility, not required for the web app) |
| `requirements.txt` | Python dependencies for the utility scripts |
