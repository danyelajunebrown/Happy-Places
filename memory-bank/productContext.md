# Product Context

## User Stories

### Core Item Tracking
- As a user, I want to register items with their purchase date and expected lifespan, so that I can track when they need replacement
- As a user, I want to track consumable quantities and refill thresholds, so that I never run out of essential items
- As a user, I want to use NFC tags to quickly identify items, so that tracking is effortless and physical

### Spatial Awareness
- As a user, I want to record where items are located, so that I can find them when needed
- As a user, I want to understand distribution patterns (placed, stacked, spread, lost), so that I can see how items organize themselves
- As a user, I want to track zones in my home, so that I can understand spatial organization

### Behavioral Insights
- As a user, I want to record item movements during routines, so that I can understand my daily patterns
- As a user, I want to track motives for item placement (comfort, fatigue, reachability), so that I understand why things move
- As a user, I want to see co-presence patterns, so that I know which items are used together

### Data Management
- As a user, I want to export my data to JSON, so that I can visualize it in a web dashboard
- As a user, I want to backup my database, so that I don't lose tracking history
- As a user, I want to import/export data, so that I can migrate between devices

### Visualization
- As a user, I want a web dashboard that shows my items, so that I can browse without the CLI
- As a user, I want to see alerts for items needing attention, so that I can act proactively
- As a user, I want to analyze patterns and routines visually, so that I can gain insights into my behavior

## Business Requirements

### Philosophical Alignment
- **Anti-austerity**: System must help users value existing possessions, not encourage acquisition
- **Anti-obsolescence**: Tracking must reveal true lifecycles vs. manufactured expiration dates
- **Homefulness**: Create belonging through spatial awareness and understanding

### Data Ownership
- All data must remain local by default
- User has complete control over their tracking data
- No cloud dependencies or data sharing
- Export/import enables user-controlled migration

### Accessibility
- CLI interface for power users and automated workflows
- Web dashboard for visual browsing and insights
- Works offline without internet connection
- No account creation or authentication barriers

### Simplicity
- Minimal dependencies (only essential Python packages)
- No build tools or complex setup
- Pure HTML/CSS/JavaScript (no frameworks)
- Static deployment ready for GitHub Pages

## UX Goals

### Effortless Tracking
- NFC scanning reduces friction for item registration
- CLI commands are intuitive and well-documented
- Demo data helps users understand the system quickly
- Interactive prompts guide users through complex operations

### Actionable Insights
- Dashboard shows items needing attention immediately
- Pattern analysis reveals distribution behaviors
- Routine tracking exposes daily habits
- Refill alerts prevent running out of consumables

### Visual Clarity
- Category badges make item types instantly recognizable
- Color-coded health indicators show lifecycle status
- Distribution types have clear, descriptive names
- Zone grouping provides spatial context

### Progressive Disclosure
- Basic features work without advanced setup
- NFC is optional (graceful degradation)
- Web dashboard enhances but doesn't replace CLI
- Advanced analytics available but not overwhelming

## Feature Priorities

### Must Have Features (All Implemented ✅)
1. **Item Registration**: Full CRUD with lifecycle tracking
2. **Categories**: good_stuff (durable), refillable (consumables), disposable
3. **Spatial Tracking**: Zone-based placement recording
4. **Distribution Types**: placed, stack, spread, lose, discard
5. **CLI Interface**: Complete command set for all operations
6. **Data Export**: JSON export for web visualization
7. **Web Dashboard**: Basic viewing and filtering
8. **Backup/Restore**: Database protection

### Should Have Features (All Implemented ✅)
1. **NFC Integration**: Python hardware support via nfcpy
2. **Refill Management**: Quantity tracking with threshold alerts
3. **Routine Tracking**: Behavioral pattern recording
4. **Motive Context**: Why items move
5. **Pattern Analysis**: Distribution and routine insights
6. **Search/Filter**: Real-time item finding in web dashboard
7. **Web NFC**: Browser-based tag scanning (Chrome on Android)
8. **Demo Data**: Sample data generation for testing

### Nice to Have Features (Future Enhancements)
1. **Real-time Updates**: WebSocket for live dashboard sync
2. **Mobile Native Apps**: iOS/Android native versions
3. **Cloud Sync**: Optional cloud backup and sync
4. **Image Attachments**: Photos of items
5. **Time-series Analytics**: Historical trend visualization
6. **Predictive Refill**: ML-based usage prediction
7. **Multi-user Support**: Shared household tracking
8. **Voice Commands**: Voice-based item registration

## Known Pain Points

### Problems We're Solving

#### Material Alienation
- **Pain**: Not knowing what you have or where it is
- **Solution**: Spatial tracking with zone organization

#### Planned Obsolescence
- **Pain**: Items "expire" before actual end of life
- **Solution**: Lifecycle tracking shows real health vs. arbitrary dates

#### Reactive Refills
- **Pain**: Running out of consumables unexpectedly
- **Solution**: Threshold alerts with usage rate calculations

#### Lost Items
- **Pain**: Forgetting where things were placed
- **Solution**: Placement history with distribution type classification

#### Behavioral Blindness
- **Pain**: Not understanding daily patterns and habits
- **Solution**: Routine and motive tracking reveals behaviors

#### Data Lock-in
- **Pain**: Tracking apps that trap your data
- **Solution**: JSON export/import with full data portability

### User Experience Issues

#### Setup Friction (Solved)
- **Original Pain**: Complex setup might deter users
- **Solution**: Demo data generator, clear quick start guide

#### CLI Intimidation (Addressed)
- **Original Pain**: Command-line might scare non-technical users
- **Solution**: Web dashboard provides visual alternative

#### NFC Hardware Requirement (Mitigated)
- **Original Pain**: Not everyone has NFC readers
- **Solution**: NFC is optional; manual entry works fine

#### Mobile Access (Partially Solved)
- **Current State**: Web dashboard works on mobile, Web NFC on Android
- **Future**: Native apps could improve mobile UX

## Target User Segments

### Primary Segment: Autoethnographers
- **Characteristics**: Interested in self-study and material culture research
- **Needs**: Deep behavioral insights, pattern analysis, exportable data
- **Usage**: Regular tracking, routine analysis, academic research

### Secondary Segment: Mindful Minimalists
- **Characteristics**: Value possessions, oppose consumerism
- **Needs**: Lifecycle tracking, replacement awareness, spatial organization
- **Usage**: Long-term item monitoring, anti-obsolescence tracking

### Secondary Segment: Home Organizers
- **Characteristics**: Want spatial awareness and findability
- **Needs**: Zone management, item location tracking, quick lookup
- **Usage**: NFC scanning, dashboard browsing, placement tracking

### Tertiary Segment: Tech Enthusiasts
- **Characteristics**: Enjoy self-tracking and quantified self
- **Needs**: Data visualization, pattern recognition, NFC integration
- **Usage**: CLI power user, data export, dashboard analytics

## Success Metrics (How We Measure)

### Usage Indicators
- Items registered and actively tracked
- Placements recorded regularly
- Routines analyzed and understood
- NFC tags successfully scanned

### Value Delivered
- Items replaced based on actual lifecycle (not arbitrary dates)
- Consumables refilled before running out
- Lost items found through placement history
- Behavioral insights leading to better organization

### System Health
- Database backups created regularly
- Data exports successful
- No data loss incidents
- Documentation comprehension (users self-serve)

## Competitive Landscape

### What Sets Happy Places Apart
- **Philosophical Foundation**: Built on anti-austerity, anti-obsolescence principles
- **Data Ownership**: No cloud, no accounts, complete user control
- **Offline-First**: Works without internet or servers
- **Appropriate Technology**: Intentionally simple, no framework bloat
- **Autoethnographic Focus**: Designed for self-research and insight
- **Distribution Types**: Unique classification (placed, stack, spread, lose, discard)
- **Routine/Motive Tracking**: Behavioral context, not just inventory

### Alternative Approaches
- **Home Inventory Apps**: Focus on insurance/valuation, not spatial awareness
- **Smart Home Systems**: Require expensive hardware, cloud dependencies
- **Barcode Scanners**: Commercial focus, not personal ecology
- **Spreadsheets**: No spatial/behavioral context, manual effort

Happy Places fills a unique niche: personal item ecology with autoethnographic depth.
