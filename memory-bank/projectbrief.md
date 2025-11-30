# Project Brief: Happy Places

## Overview
Happy Places is an autoethnographic, NFC-powered platform for tracking personal belongings and understanding item ecology. It subverts austerity and planned obsolescence by helping users develop a mindful relationship with their possessions through spatial awareness and behavioral pattern recognition.

## Objectives
- **Primary**: Track items through lifecycle, location, and routine usage patterns to build spatial and material awareness
- **Secondary**: Combat planned obsolescence by monitoring true item lifecycles vs. manufactured expiration
- **Secondary**: Create homefulness through understanding where things are and how they move through daily life
- **Secondary**: Enable autoethnographic research into personal relationships with material possessions

## Success Criteria
- Users can register items with complete lifecycle tracking (purchase date, expected lifespan, health metrics)
- Items can be tracked spatially across zones with distribution type classification
- Behavioral patterns emerge through routine and motive tracking
- NFC integration works seamlessly (both Python hardware and Web NFC)
- Data remains portable via JSON export/import
- System works offline-first with no server dependencies
- Web dashboard provides actionable insights (refill alerts, replacement warnings, pattern analysis)

## Constraints
- **Technical**: Must work offline, no backend server required
- **Technical**: Pure HTML/CSS/JavaScript frontend (no frameworks)
- **Technical**: SQLite database for local storage
- **Technical**: Must support NFC via both Python (nfcpy) and Web NFC API
- **Philosophical**: Embodies appropriate technology and intentional simplicity
- **Deployment**: GitHub Pages ready for static hosting
- **Data**: User owns all data locally

## Target Users
- Individuals interested in autoethnographic research
- People seeking mindful relationships with possessions
- Those opposing consumerism and planned obsolescence
- Users wanting to track belongings and understand spatial patterns
- Researchers studying material culture and domesticity

## Timeline
**Project Status**: ✅ **COMPLETE** (100% architecture built out)

### Completed Milestones (All Achieved):
- ✅ Core database schema with items, placements, co_presence, zones
- ✅ Full CRUD operations for item management
- ✅ Lifecycle tracking with health calculations
- ✅ Refill management with usage rate calculations
- ✅ Zone management and spatial tracking
- ✅ Distribution type classification (placed, stack, spread, lose, discard)
- ✅ Routine and motive tracking
- ✅ NFC integration (Python hardware via nfcpy)
- ✅ Complete CLI interface with 20+ commands
- ✅ Data export/import (JSON)
- ✅ Database backup/restore functionality
- ✅ Web dashboard with 5 tabs (Dashboard, Items, Patterns, Zones, Routines)
- ✅ Real-time search, filtering, and sorting
- ✅ Web NFC API integration (Chrome on Android)
- ✅ Pattern analysis and behavioral insights
- ✅ Demo data generation
- ✅ Comprehensive documentation (README, ARCHITECTURE, QUICKSTART)
- ✅ Infrastructure files (requirements.txt, .gitignore)

## Key Philosophy
Happy Places opposes:
- **Austerity**: Valuing what you already have rather than constant acquisition
- **Planned Obsolescence**: Understanding true lifecycles vs. manufactured expiration
- **Spatial Alienation**: Knowing where things are creates belonging

By tracking items through routines and motives, users develop autoethnographic insight into their relationship with material possessions and home spaces.
