# Technical Context

## Technology Stack

### Languages
- **Python 3.x** (Backend, CLI, NFC integration)
  - Version: Python 3.7+ recommended
  - Core language for all data operations
- **HTML5** (Frontend structure)
  - Semantic markup
  - Web NFC API support
- **CSS3** (Frontend styling)
  - Grid and Flexbox layouts
  - Custom properties (variables)
  - Responsive design
- **JavaScript ES6+** (Frontend logic)
  - Modern syntax (const/let, arrow functions, template literals)
  - Fetch API for data loading
  - Web NFC API integration

### Frameworks & Libraries

#### Backend (Python)
- **python-dateutil** (v2.8.0+)
  - Purpose: Date calculations and parsing
  - Used for: Lifecycle age calculations, date arithmetic
- **nfcpy** (v1.0.4+)
  - Purpose: NFC hardware support
  - Used for: USB NFC reader integration
  - Optional: System works without it

#### Frontend (None - Vanilla JavaScript)
- **No frameworks**: Pure HTML/CSS/JavaScript
- **No build tools**: Direct browser execution
- **No transpilation**: Modern browser features only
- **Philosophy**: Appropriate technology, intentional simplicity

### Database
- **SQLite3** (Built into Python)
  - Embedded, serverless database
  - Single file storage (`happy_places.db`)
  - ACID compliant
  - Foreign key support enabled

### Infrastructure
- **Git** - Version control
- **GitHub** - Repository hosting
- **GitHub Pages** - Static site deployment (ready)

## Development Tools

### IDE/Editor
- **Visual Studio Code** (Primary development environment)
- **Any text editor** (Project uses no IDE-specific features)

### Version Control
- **Git** - Local version control
- **GitHub** - Remote repository
  - Repository: https://github.com/danyelajunebrown/Happy-Places.git
  - Latest commit: f407e9595071603f6b75fcd27ee2fef648cc59e1

### Package Manager
- **pip** - Python package installer
- **requirements.txt** - Dependency specification

### Terminal
- **Default Shell**: /bin/zsh (macOS)
- **Python Command**: `python3` (not `python`)

## Build Process

### No Build Step Required
This project intentionally avoids build tools:
- Frontend runs directly in browser
- No compilation or transpilation
- No bundling or minification
- No node_modules directory

### Setup Process
```bash
# 1. Clone repository
git clone https://github.com/danyelajunebrown/Happy-Places.git
cd Happy-Places

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run demo (optional)
python3 Happy-Places.py demo

# 4. Export data for web
python3 Happy-Places.py export

# 5. Open web dashboard
open index.html
```

## Deployment

### Local Development
```bash
# Start using immediately (no dev server needed)
python3 Happy-Places.py list
open index.html
```

### GitHub Pages Deployment
```bash
# 1. Push repository to GitHub
git add .
git commit -m "Update data"
git push origin main

# 2. Enable GitHub Pages in repository settings
# Settings → Pages → Source: main branch

# 3. Export data locally before pushing
python3 Happy-Places.py export
git add happy_places_export.json
git commit -m "Update exported data"
git push origin main

# 4. Access at:
# https://username.github.io/Happy-Places/
```

### Static Hosting (Any Provider)
- Upload all files to web host
- Ensure `happy_places_export.json` is current
- No server-side processing required
- Works on any static file host

## Dependencies

### Python Dependencies (requirements.txt)
```
python-dateutil>=2.8.0
nfcpy>=1.0.4
```

### Installation
```bash
pip install -r requirements.txt
```

### Optional Dependencies
- **nfcpy**: Only needed for USB NFC readers
  - Can skip if using Web NFC only
  - System gracefully degrades without it

### System Dependencies
- **Python 3.7+**: Core requirement
- **SQLite3**: Built into Python (no separate install)
- **USB drivers**: Only if using NFC hardware

## Environment Setup

### macOS (Current Development Environment)
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Install dependencies
pip3 install -r requirements.txt

# For NFC support (optional)
pip3 install nfcpy

# Run application
python3 Happy-Places.py
```

### Linux
```bash
# Install Python 3
sudo apt-get install python3 python3-pip

# Install dependencies
pip3 install -r requirements.txt

# For NFC support
pip3 install nfcpy
# May need: sudo apt-get install libusb-1.0-0-dev
```

### Windows
```bash
# Install Python 3 from python.org
# Add to PATH during installation

# Install dependencies
pip install -r requirements.txt

# For NFC support
pip install nfcpy
# May need additional USB drivers
```

## Testing

### Framework
- **None**: Manual testing approach
- **Philosophy**: Appropriate complexity for project scale

### Testing Strategy
1. **Manual CLI Testing**: Run all commands with various inputs
2. **Database Verification**: Check SQLite directly with `sqlite3`
3. **Web Testing**: Open dashboard in multiple browsers
4. **NFC Testing**: Physical tag scanning when hardware available

### Test Commands
```bash
# Generate test data
python3 Happy-Places.py demo

# Verify all commands work
python3 Happy-Places.py list
python3 Happy-Places.py attention
python3 Happy-Places.py patterns
python3 Happy-Places.py routines

# Test export/import cycle
python3 Happy-Places.py export
python3 Happy-Places.py import happy_places_export.json

# Test backup/restore
python3 Happy-Places.py backup
python3 Happy-Places.py restore backups/happy_places_YYYYMMDD_HHMMSS.db
```

### Browser Testing
- **Chrome**: Web NFC support (Android only)
- **Safari**: Standard features work
- **Firefox**: Standard features work
- **Edge**: Standard features work

### NFC Testing

#### Python NFC Testing
```bash
# Check if nfcpy is installed
pip show nfcpy

# Test NFC scanning
python3 Happy-Places.py add-nfc
# Place tag near USB reader when prompted
```

#### Web NFC Testing
1. Open dashboard in Chrome on Android
2. Enable NFC in phone settings
3. Click "📱 Scan NFC Tag" button
4. Grant NFC permissions
5. Hold phone near tag

## File Structure

```
Happy-Places/
├── Happy-Places.py              # Python backend (1064 lines)
├── index.html                   # Web frontend (683 lines)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore patterns
├── README.md                    # Project overview
├── ARCHITECTURE.md              # Technical documentation
├── QUICKSTART.md                # Getting started guide
├── happy_places.db              # SQLite database (created at runtime)
├── happy_places_export.json    # JSON export for web (generated)
├── backups/                     # Database backups (created by backup command)
│   └── happy_places_YYYYMMDD_HHMMSS.db
├── memory-bank/                 # Memory Bank documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md          # This file
│   ├── activeContext.md
│   └── progress.md
└── .git/                        # Git repository
```

## Database Details

### File
- **Location**: `happy_places.db` (project root)
- **Format**: SQLite 3
- **Size**: Typically < 1 MB for personal use
- **Backup**: Manual via `backup` command

### Schema Version
- **Current**: 1.0 (initial schema)
- **Migration**: Not implemented (fresh schema on init)
- **Compatibility**: Forward-compatible design

### Access
```bash
# Direct SQLite access
sqlite3 happy_places.db

# View schema
.schema

# Query items
SELECT * FROM items;

# Exit
.quit
```

## Performance Specifications

### Expected Scale
- **Items**: 100-1000 typical, 10,000+ supported
- **Placements**: 1,000-10,000 typical
- **Zones**: 5-50 typical
- **Database Size**: < 10 MB typical

### Response Times (Typical)
- **CLI Commands**: < 100ms
- **Database Queries**: < 50ms
- **JSON Export**: < 1 second
- **Web Dashboard Load**: < 500ms
- **Search/Filter**: < 100ms (client-side)
- **NFC Scan**: < 1 second

### Limitations
- **SQLite**: Single-writer limitation (not an issue for single-user)
- **Frontend**: Client-side filtering (may slow with 10,000+ items)
- **NFC**: Requires physical proximity to tags

## Browser Compatibility

### Required Features
- **HTML5**: All modern browsers
- **CSS3 Grid**: All modern browsers (2017+)
- **ES6 JavaScript**: All modern browsers (2015+)
- **Fetch API**: All modern browsers (2015+)

### Optional Features
- **Web NFC API**: Chrome on Android only (as of 2024)
- **Graceful Degradation**: Hide NFC button if unsupported

### Tested Browsers
- ✅ Chrome 90+ (desktop and Android)
- ✅ Safari 14+ (macOS and iOS)
- ✅ Firefox 88+
- ✅ Edge 90+

### Mobile Support
- ✅ Responsive design works on all screen sizes
- ✅ Touch-friendly interface
- ⚠️ Web NFC only on Android (iOS doesn't support Web NFC API)

## Security Configuration

### Database Security
- **File Permissions**: Relies on OS-level file permissions
- **Encryption**: Not implemented (local-only use case)
- **Backups**: User-managed security

### Web Security
- **HTTPS**: Required for Web NFC (automatic on GitHub Pages)
- **Localhost**: Works without HTTPS
- **CSP**: Not implemented (could be added)
- **CORS**: Not applicable (same-origin only)

### NFC Security
- **Tag IDs**: Not encrypted
- **Physical Access**: Required for scanning
- **Privacy**: All data remains local

## Development Workflow

### Typical Development Session
```bash
# 1. Make changes to Happy-Places.py or index.html
code Happy-Places.py

# 2. Test changes
python3 Happy-Places.py demo
python3 Happy-Places.py export

# 3. View in browser
open index.html

# 4. Commit changes
git add .
git commit -m "Description of changes"
git push origin main
```

### Adding New Features
1. Update database schema in `_init_db()` if needed
2. Add new methods to `HappyPlaces` class
3. Add CLI command handler
4. Update main() command routing
5. Update export format if needed
6. Update web dashboard rendering
7. Test all paths
8. Update documentation

### Debugging Tools
- **Python**: `print()` statements, `pdb` debugger
- **JavaScript**: Browser DevTools console
- **Database**: `sqlite3` CLI tool
- **NFC**: USB reader LED indicators

## Known Technical Constraints

### Python-to-Web Gap
- **Manual Export**: Must run `export` command after data changes
- **No Real-time**: Web dashboard shows snapshot, not live data
- **Workaround**: Re-export and refresh browser

### NFC Hardware
- **Platform-Specific**: Different drivers for different OS
- **USB Only**: Python NFC limited to USB readers
- **Web NFC**: Android only, HTTPS required

### SQLite Limitations
- **Single Writer**: Only one process can write at a time
- **Not Multi-user**: No concurrent user support
- **Local Only**: No network access

### Browser Limitations
- **Local File Access**: `file://` protocol has CORS restrictions
- **Solution**: Use `http://localhost` or deploy to web server
- **Web NFC**: Chrome on Android only

## IDE Configuration

### Visual Studio Code
- **Extensions**: None required
- **Settings**: Default Python and JavaScript support
- **Terminal**: Integrated terminal works perfectly

### Recommended VS Code Extensions (Optional)
- **Python**: Microsoft Python extension
- **SQLite**: SQLite Viewer for database inspection
- **Git Lens**: Enhanced git integration

## Environment Variables
- **None Required**: All configuration is file-based
- **Database Path**: Hardcoded as `happy_places.db`
- **Future**: Could support `DB_PATH` environment variable

## Logging
- **Current**: Print statements to stdout
- **Errors**: Print to stderr
- **Future**: Could implement proper logging module

## Data Formats

### JSON Export Format
```json
{
  "items": [...],
  "placements": [...],
  "zones": [...],
  "patterns": {...},
  "routines": {...},
  "export_timestamp": "2024-11-30T16:44:00"
}
```

### Date Format
- **Storage**: ISO 8601 (YYYY-MM-DD)
- **Display**: Human-readable format
- **Parsing**: python-dateutil for flexibility

## API Interfaces

### No REST API
- **Philosophy**: Local-first, no server
- **Data Access**: Direct database or JSON export
- **Future**: Could add optional REST API layer

### CLI Interface
- **Entry Point**: `main()` function
- **Arguments**: `sys.argv`
- **Output**: stdout (data) and stderr (errors)

## Monitoring
- **Not Implemented**: No metrics or monitoring
- **Philosophy**: Appropriate for single-user tool
- **Debugging**: Standard output and error messages
