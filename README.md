# Happy Places

> An autoethnographic, NFC-powered platform subverting austerity and planned obsolescence with homefulness

Track your belongings, understand their lifecycles, and observe how items move through your daily routines. Happy Places helps you build a mindful relationship with your possessions through spatial awareness and behavioral pattern recognition.

## Features

✅ **Item Lifecycle Tracking** - Monitor age, health, and expected lifespan of durable goods
✅ **Refill Management** - Track consumables with smart refill alerts
✅ **NFC Integration** - Scan physical tags via USB readers or mobile Web NFC
✅ **Spatial Tracking** - Record where items are and how they're distributed
✅ **Routine Analysis** - Understand patterns in how items move through daily life
✅ **Distribution Patterns** - Stack, spread, lose, discard, or intentionally place
✅ **Web Dashboard** - Beautiful, responsive visualization with search and filters
✅ **Complete CLI** - Full terminal interface for all operations
✅ **Backup/Restore** - Timestamped database backups and safe restoration
✅ **Import/Export** - JSON-based data portability

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate demo data
python3 Happy-Places.py demo

# Export for web visualization
python3 Happy-Places.py export

# Open index.html in browser
open index.html
```

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Architecture Documentation](ARCHITECTURE.md)** - Complete system design and technical details

## Item Categories

- **Good Stuff** (Durable Goods) - Tracks lifecycle from purchase to replacement
- **Refillable** (Consumables) - Monitors quantities with usage rate calculations
- **Disposable** - Basic tracking for temporary items

## Distribution Types

Track how items spread across your spaces:
- **Placed** - Intentional positioning
- **Stack** - Organized grouping
- **Spread** - Natural dispersal
- **Lose** - Misplacement patterns
- **Discard** - Removal tracking

## Philosophy

Happy Places opposes:
- **Austerity** - Valuing what you already have rather than constant acquisition
- **Planned Obsolescence** - Understanding true lifecycles vs. manufactured expiration
- **Spatial Alienation** - Knowing where things are creates belonging

By tracking items through routines and motives, you develop autoethnographic insight into your relationship with material possessions.

## Technology

- **Python 3** backend with SQLite database
- **Pure HTML/CSS/JavaScript** frontend (no frameworks)
- **NFC support** via nfcpy (Python) and Web NFC API (browser)
- **GitHub Pages** ready for static deployment
- **Offline-first** - no server required

## CLI Commands

```bash
# Item management
python3 Happy-Places.py add              # Add item interactively
python3 Happy-Places.py add-nfc          # Register via NFC scan
python3 Happy-Places.py update <id>      # Update quantities
python3 Happy-Places.py delete <id>      # Remove items
python3 Happy-Places.py place <id>       # Record placement

# Queries
python3 Happy-Places.py list             # All items
python3 Happy-Places.py status <id>      # Item details
python3 Happy-Places.py attention        # Items needing action
python3 Happy-Places.py patterns         # Distribution analysis
python3 Happy-Places.py routines         # Behavioral patterns

# Data management
python3 Happy-Places.py export           # Export to JSON
python3 Happy-Places.py import [file]    # Import from JSON
python3 Happy-Places.py backup           # Create backup
python3 Happy-Places.py restore <file>   # Restore database
```

## Web Dashboard

Interactive visualization with:
- Real-time search and filtering
- Category-based filters
- Multiple sort options
- Routine insights visualization
- Zone-based organization views
- NFC scanning (Chrome on Android)

## NFC Usage

**Python (USB Readers):**
```bash
pip install nfcpy
python3 Happy-Places.py add-nfc
```

**Web (Mobile):**
- Open dashboard in Chrome on Android
- Click "📱 Scan NFC Tag" button
- Hold phone near tag

## License

Open source - use freely for personal item tracking and research.

## Contributing

This project embodies appropriate technology and intentional simplicity. Contributions should maintain these principles.
