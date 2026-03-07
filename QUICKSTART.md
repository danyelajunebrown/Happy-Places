# Happy Places - Quick Start Guide

## Installation

```bash
# Clone or download the repository
cd Happy-Places

# Install dependencies
pip install -r requirements.txt
```

## First Run - Generate Demo Data

```bash
# Create sample items and placements
python3 Happy-Places.py demo

# Export data for web visualization
python3 Happy-Places.py export

# Open index.html in your browser
open index.html
```

## Common Tasks

### Add Items

**Interactive CLI:**
```bash
python3 Happy-Places.py add
```

**With NFC Tag:**
```bash
python3 Happy-Places.py add-nfc
# Place tag near reader when prompted
```

### Record Item Placement

```bash
python3 Happy-Places.py place <item_id>
# Follow prompts for zone, distribution type, routine, motive
```

### View Information

```bash
# See all items
python3 Happy-Places.py list

# Check specific item
python3 Happy-Places.py status <item_id>

# Items needing attention
python3 Happy-Places.py attention

# See patterns
python3 Happy-Places.py patterns

# See routines
python3 Happy-Places.py routines

# List zones
python3 Happy-Places.py zones
```

### Update Items

```bash
# Update quantity (for refillable items)
python3 Happy-Places.py update <item_id>

# Delete item
python3 Happy-Places.py delete <item_id>
```

### Manage Zones

```bash
# Add new zone
python3 Happy-Places.py add-zone
```

### Backup & Restore

```bash
# Create backup
python3 Happy-Places.py backup

# List backups
python3 Happy-Places.py list-backups

# Restore from backup
python3 Happy-Places.py restore backups/happy_places_YYYYMMDD_HHMMSS.db
```

### Import/Export

```bash
# Export to JSON
python3 Happy-Places.py export

# Import from JSON
python3 Happy-Places.py import happy_places_export.json
```

## Web Dashboard

The web dashboard provides visual analytics and NFC scanning:

1. **Run export** to generate latest data:
   ```bash
   python3 Happy-Places.py export
   ```

2. **Open `index.html`** in your browser

3. **Features:**
   - **Dashboard**: Overview stats and alerts
   - **Items**: Search, filter, sort items
   - **Patterns**: Distribution behavior analysis
   - **Zones**: Spatial organization view
   - **Routines**: Behavioral pattern insights
   - **NFC Scan** (Chrome on Android): Tap items with phone

## NFC Setup

### Python (USB NFC Reader)

1. Install hardware support:
   ```bash
   pip install nfcpy
   ```

2. Connect USB NFC reader

3. Test scanning:
   ```bash
   python3 Happy-Places.py add-nfc
   ```

### Web (Mobile Phone)

1. **Requirements:**
   - Chrome browser on Android
   - HTTPS or localhost
   - NFC-capable phone

2. **Usage:**
   - Open web dashboard
   - Click "📱 Scan NFC Tag" button
   - Grant NFC permissions
   - Hold phone near tag

## Item Categories

### Good Stuff (Durable Goods)
- Tracks lifecycle (purchase date + expected lifespan)
- Calculates health percentage
- Alerts when < 20% life remaining
- Examples: trash cans, wallets, furniture

### Refillable (Consumables)
- Tracks current quantity
- Sets refill threshold
- Estimates days remaining
- Examples: toothbrush heads, salt shakers, soap

### Disposable
- Basic tracking without lifecycle
- Examples: one-time items, packaging

## Distribution Types

- **placed** - Intentionally positioned
- **stack** - Organized, grouped items
- **spread** - Items dispersed across space
- **lose** - Misplaced items
- **discard** - Items marked for removal

## Routines

Track item movements during daily patterns:
- Morning routine
- Night routine
- Clean-up
- Undressing
- Cooking
- Custom routines

## Motives

Record why items move:
- Reachability
- Comfort
- Fatigue
- Convenience
- Organization
- Custom motives

## Tips

1. **Regular exports**: Run `export` after adding/updating items
2. **Backup before changes**: Use `backup` before major updates
3. **Tag items with NFC**: Physical tags make tracking effortless
4. **Track motives**: Understanding *why* items move is key
5. **Review patterns**: Check `routines` tab for insights
6. **Use zones**: Organize by actual physical spaces
7. **Update quantities**: Keep refillables current for accurate alerts

## Troubleshooting

### "Command not found: python"
Use `python3` instead of `python`

### "Data file not found" in web dashboard
Run: `python3 Happy-Places.py export`

### NFC not working (Python)
- Check USB reader is connected
- Install nfcpy: `pip install nfcpy`
- Try different USB port

### Web NFC not working
- Must use Chrome on Android
- Requires HTTPS (except localhost)
- Check phone has NFC enabled
- Grant permissions when prompted

### Database is locked
- Close other instances of the program
- Backup and restore if needed

## Data Location

- **Database**: `happy_places.db` (SQLite)
- **Export**: `happy_places_export.json` (for web)
- **Backups**: `backups/` directory

## Getting Help

Run any command without arguments for usage info:
```bash
python3 Happy-Places.py
```

## Philosophy

Happy Places embraces:
- **Autoethnography** - Understanding your relationship with things
- **Anti-austerity** - Valuing what you have
- **Anti-obsolescence** - Tracking lifecycle, not just acquisition
- **Homefulness** - Creating belonging through spatial awareness

Track not just *what* you have, but *where* it is, *why* it moves, and *how* it serves you.
