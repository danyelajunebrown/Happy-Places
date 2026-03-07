"""
happy_places.py - Complete Happy Places (BelongOS) System
Empowers via autoethnography toward the end of austerity and planned obsolescence.

Features:
- Item registration with categories (good_stuff, refillable, disposable)
- Placement tracking with zones, routines, motives
- Distribution types (stack, spread, lose, discard)
- Lifecycle tracking (lifespan for good stuff, refill tracking for refillables)
- Pattern analysis
- Co-presence tracking

Usage:
    from happy_places import HappyPlaces
    
    hp = HappyPlaces("happy_places.db")
    
    # Register an item
    hp.register_item("trash_can_bathroom", 
                     label="Bathroom Trash Can",
                     category="good_stuff",
                     purchase_date="2023-01-15",
                     expected_lifespan_years=5)
    
    # Record a placement
    hp.record_placement("trash_can_bathroom",
                       zone="bathroom_left_side",
                       distribution_type="placed",
                       routine="night routine",
                       motive="reachability")
    
    # Query item
    print(hp.item_status("trash_can_bathroom"))
    
    # Analyze patterns
    print(hp.distribution_patterns())
"""

import sqlite3
import datetime
import json
import shutil
import os
from typing import Optional, List, Dict, Any
from dateutil.relativedelta import relativedelta


class HappyPlaces:
    def __init__(self, db_path: str = "happy_places.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database schema"""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    item_id TEXT PRIMARY KEY,
                    label TEXT,
                    category TEXT CHECK(category IN ('good_stuff', 'refillable', 'disposable')),
                    purchase_date TEXT,
                    expected_lifespan_years REAL,
                    current_quantity INTEGER,
                    refill_threshold INTEGER,
                    usage_rate_per_day REAL,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS placements (
                    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT,
                    zone TEXT,
                    distribution_type TEXT CHECK(distribution_type IN ('stack', 'spread', 'lose', 'discard', 'placed')),
                    routine TEXT,
                    motive TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY(item_id) REFERENCES items(item_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS co_presence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_a TEXT,
                    item_b TEXT,
                    zone TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(item_a) REFERENCES items(item_id),
                    FOREIGN KEY(item_b) REFERENCES items(item_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS zones (
                    zone_id TEXT PRIMARY KEY,
                    zone_name TEXT,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    # ===== ITEM REGISTRATION =====
    
    def register_item(self,
                     item_id: str,
                     label: str,
                     category: str,
                     purchase_date: Optional[str] = None,
                     expected_lifespan_years: Optional[float] = None,
                     current_quantity: Optional[int] = None,
                     refill_threshold: Optional[int] = None,
                     usage_rate_per_day: Optional[float] = None,
                     metadata: Optional[Dict] = None) -> None:
        """
        Register a new item.
        
        Args:
            item_id: Unique identifier (e.g., NFC tag ID)
            label: Human-readable name
            category: 'good_stuff', 'refillable', or 'disposable'
            purchase_date: ISO date string (for lifecycle tracking)
            expected_lifespan_years: For good_stuff (e.g., 5.0)
            current_quantity: For refillable/disposable
            refill_threshold: When to alert for refill
            usage_rate_per_day: For estimating when refill needed
            metadata: Additional custom data
        """
        with self._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO items 
                (item_id, label, category, purchase_date, expected_lifespan_years,
                 current_quantity, refill_threshold, usage_rate_per_day, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (item_id, label, category, purchase_date, expected_lifespan_years,
                  current_quantity, refill_threshold, usage_rate_per_day,
                  json.dumps(metadata or {})))
            conn.commit()

    # ===== PLACEMENT TRACKING =====
    
    def record_placement(self,
                        item_id: str,
                        zone: str,
                        distribution_type: str = "placed",
                        routine: Optional[str] = None,
                        motive: Optional[str] = None,
                        seen_with: Optional[List[str]] = None,
                        timestamp: Optional[str] = None,
                        metadata: Optional[Dict] = None) -> None:
        """
        Record where an item is placed and how it's distributed.
        
        Args:
            item_id: The item being placed
            zone: Location name (e.g., "bathroom_left_side")
            distribution_type: 'stack', 'spread', 'lose', 'discard', 'placed'
            routine: Context (e.g., "night routine", "clean-up")
            motive: Why it moved (e.g., "reachability", "comfort")
            seen_with: List of other item_ids present at same time
            timestamp: ISO timestamp (defaults to now)
            metadata: Additional custom data
        """
        if timestamp is None:
            timestamp = datetime.datetime.utcnow().isoformat()
        
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO placements 
                (item_id, zone, distribution_type, routine, motive, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item_id, zone, distribution_type, routine, motive, timestamp,
                  json.dumps(metadata or {})))
            
            # Record co-presence if seen with other items
            if seen_with:
                for other_id in seen_with:
                    conn.execute("""
                        INSERT INTO co_presence (item_a, item_b, zone, timestamp)
                        VALUES (?, ?, ?, ?)
                    """, (item_id, other_id, zone, timestamp))
                    # Record reverse for easier querying
                    conn.execute("""
                        INSERT INTO co_presence (item_a, item_b, zone, timestamp)
                        VALUES (?, ?, ?, ?)
                    """, (other_id, item_id, zone, timestamp))
            
            conn.commit()

    # ===== ZONE MANAGEMENT =====
    
    def register_zone(self, zone_id: str, zone_name: str, description: str = "") -> None:
        """Register a new zone/space"""
        with self._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO zones (zone_id, zone_name, description)
                VALUES (?, ?, ?)
            """, (zone_id, zone_name, description))
            conn.commit()

    def list_zones(self) -> List[Dict]:
        """Get all registered zones"""
        with self._connect() as conn:
            rows = conn.execute("SELECT zone_id, zone_name, description FROM zones").fetchall()
            return [{"zone_id": r[0], "zone_name": r[1], "description": r[2]} for r in rows]

    # ===== QUERIES =====
    
    def item_status(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of an item including lifecycle info"""
        with self._connect() as conn:
            # Get item details
            item = conn.execute("""
                SELECT label, category, purchase_date, expected_lifespan_years,
                       current_quantity, refill_threshold, usage_rate_per_day, metadata
                FROM items WHERE item_id = ?
            """, (item_id,)).fetchone()
            
            if not item:
                return None
            
            # Get latest placement
            placement = conn.execute("""
                SELECT zone, distribution_type, routine, motive, timestamp
                FROM placements WHERE item_id = ?
                ORDER BY timestamp DESC LIMIT 1
            """, (item_id,)).fetchone()
            
            result = {
                "item_id": item_id,
                "label": item[0],
                "category": item[1],
                "metadata": json.loads(item[7])
            }
            
            # Add lifecycle info based on category
            if item[1] == "good_stuff" and item[2] and item[3]:
                purchase = datetime.datetime.fromisoformat(item[2])
                lifespan_years = item[3]
                age_years = (datetime.datetime.now() - purchase).days / 365.25
                remaining_years = max(0, lifespan_years - age_years)
                
                result["lifecycle"] = {
                    "purchase_date": item[2],
                    "age_years": round(age_years, 1),
                    "expected_lifespan_years": lifespan_years,
                    "remaining_years": round(remaining_years, 1),
                    "health_percent": round((remaining_years / lifespan_years) * 100, 1)
                }
            
            elif item[1] == "refillable":
                quantity = item[4] or 0
                threshold = item[5] or 0
                usage_rate = item[6] or 0
                
                days_remaining = (quantity / usage_rate) if usage_rate > 0 else None
                
                result["refill_status"] = {
                    "current_quantity": quantity,
                    "refill_threshold": threshold,
                    "needs_refill": quantity <= threshold,
                    "days_remaining": round(days_remaining, 1) if days_remaining else None
                }
            
            # Add current placement
            if placement:
                result["current_placement"] = {
                    "zone": placement[0],
                    "distribution_type": placement[1],
                    "routine": placement[2],
                    "motive": placement[3],
                    "timestamp": placement[4]
                }
            
            return result

    def placement_history(self, item_id: str, limit: int = 20) -> List[Dict]:
        """Get movement history for an item"""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT zone, distribution_type, routine, motive, timestamp, metadata
                FROM placements WHERE item_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (item_id, limit)).fetchall()
            
            return [{
                "zone": r[0],
                "distribution_type": r[1],
                "routine": r[2],
                "motive": r[3],
                "timestamp": r[4],
                "metadata": json.loads(r[5])
            } for r in rows]

    def recent_neighbors(self, item_id: str, limit: int = 10) -> List[Dict]:
        """Get items recently seen with this item"""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT DISTINCT c.item_b, i.label, c.zone, c.timestamp
                FROM co_presence c
                JOIN items i ON c.item_b = i.item_id
                WHERE c.item_a = ?
                ORDER BY c.timestamp DESC LIMIT ?
            """, (item_id, limit)).fetchall()
            
            return [{
                "item_id": r[0],
                "label": r[1],
                "zone": r[2],
                "timestamp": r[3]
            } for r in rows]

    def items_in_zone(self, zone: str) -> List[Dict]:
        """Get all items currently in a zone"""
        with self._connect() as conn:
            # Get latest placement for each item in this zone
            rows = conn.execute("""
                SELECT DISTINCT i.item_id, i.label, i.category,
                       p.distribution_type, p.timestamp
                FROM items i
                JOIN placements p ON i.item_id = p.item_id
                WHERE p.zone = ?
                AND p.timestamp = (
                    SELECT MAX(timestamp) FROM placements 
                    WHERE item_id = i.item_id
                )
            """, (zone,)).fetchall()
            
            return [{
                "item_id": r[0],
                "label": r[1],
                "category": r[2],
                "distribution_type": r[3],
                "last_updated": r[4]
            } for r in rows]

    # ===== PATTERN ANALYSIS =====
    
    def distribution_patterns(self) -> Dict[str, Any]:
        """Analyze how items are distributed (stack, spread, etc.)"""
        with self._connect() as conn:
            # Count by distribution type
            counts = conn.execute("""
                SELECT distribution_type, COUNT(*) as count
                FROM placements
                GROUP BY distribution_type
            """).fetchall()
            
            # Distribution by zone
            by_zone = conn.execute("""
                SELECT zone, distribution_type, COUNT(*) as count
                FROM placements
                GROUP BY zone, distribution_type
            """).fetchall()
            
            return {
                "overall_counts": {r[0]: r[1] for r in counts},
                "by_zone": [{
                    "zone": r[0],
                    "distribution_type": r[1],
                    "count": r[2]
                } for r in by_zone]
            }

    def routine_insights(self) -> List[Dict]:
        """Find patterns in routines and motives"""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT routine, motive, COUNT(*) as frequency,
                       GROUP_CONCAT(DISTINCT zone) as zones
                FROM placements
                WHERE routine IS NOT NULL
                GROUP BY routine, motive
                ORDER BY frequency DESC
            """).fetchall()
            
            return [{
                "routine": r[0],
                "motive": r[1],
                "frequency": r[2],
                "zones": r[3].split(',') if r[3] else []
            } for r in rows]

    def items_needing_attention(self) -> Dict[str, List[Dict]]:
        """Get items that need refill or replacement soon"""
        attention = {"refill_needed": [], "replacement_soon": []}
        
        with self._connect() as conn:
            # Check refillables
            refillables = conn.execute("""
                SELECT item_id, label, current_quantity, refill_threshold
                FROM items
                WHERE category = 'refillable'
                AND current_quantity <= refill_threshold
            """).fetchall()
            
            attention["refill_needed"] = [{
                "item_id": r[0],
                "label": r[1],
                "current_quantity": r[2],
                "threshold": r[3]
            } for r in refillables]
            
            # Check good_stuff nearing end of life
            aging = conn.execute("""
                SELECT item_id, label, purchase_date, expected_lifespan_years
                FROM items
                WHERE category = 'good_stuff'
                AND purchase_date IS NOT NULL
                AND expected_lifespan_years IS NOT NULL
            """).fetchall()
            
            for item in aging:
                purchase = datetime.datetime.fromisoformat(item[2])
                lifespan_years = item[3]
                age_years = (datetime.datetime.now() - purchase).days / 365.25
                remaining_years = lifespan_years - age_years
                
                # Alert if less than 20% life remaining
                if remaining_years < (lifespan_years * 0.2) and remaining_years > 0:
                    attention["replacement_soon"].append({
                        "item_id": item[0],
                        "label": item[1],
                        "remaining_years": round(remaining_years, 1),
                        "health_percent": round((remaining_years / lifespan_years) * 100, 1)
                    })
        
        return attention

    def all_items(self) -> List[Dict]:
        """Get all registered items"""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT item_id, label, category
                FROM items
                ORDER BY label
            """).fetchall()

            return [{
                "item_id": r[0],
                "label": r[1],
                "category": r[2]
            } for r in rows]

    # ===== ITEM UPDATES =====

    def update_item(self, item_id: str, **kwargs) -> bool:
        """Update item fields. Returns True if successful."""
        allowed_fields = {
            'label', 'category', 'purchase_date', 'expected_lifespan_years',
            'current_quantity', 'refill_threshold', 'usage_rate_per_day', 'metadata'
        }

        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False

        # Convert metadata dict to JSON string if present
        if 'metadata' in updates and isinstance(updates['metadata'], dict):
            updates['metadata'] = json.dumps(updates['metadata'])

        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [item_id]

        with self._connect() as conn:
            cursor = conn.execute(
                f"UPDATE items SET {set_clause} WHERE item_id = ?",
                values
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_quantity(self, item_id: str, new_quantity: int) -> bool:
        """Update quantity for refillable/disposable items"""
        return self.update_item(item_id, current_quantity=new_quantity)

    def delete_item(self, item_id: str) -> bool:
        """Delete an item and all its placements"""
        with self._connect() as conn:
            # Delete related records first (foreign key constraints)
            conn.execute("DELETE FROM placements WHERE item_id = ?", (item_id,))
            conn.execute("DELETE FROM co_presence WHERE item_a = ? OR item_b = ?",
                        (item_id, item_id))
            cursor = conn.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ===== DATA EXPORT =====
    
    def export_to_json(self, filepath: str = "happy_places_export.json") -> None:
        """Export all data to JSON file for GitHub Pages"""
        data = {
            "exported_at": datetime.datetime.utcnow().isoformat(),
            "items": [],
            "zones": self.list_zones(),
            "patterns": self.distribution_patterns(),
            "routines": self.routine_insights(),
            "attention": self.items_needing_attention()
        }

        # Export each item with full status
        for item in self.all_items():
            status = self.item_status(item["item_id"])
            if status:
                data["items"].append(status)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported to {filepath}")

    def import_from_json(self, filepath: str = "happy_places_export.json") -> None:
        """Import data from JSON file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Import file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Import zones first
        for zone in data.get("zones", []):
            self.register_zone(zone["zone_id"], zone["zone_name"],
                             zone.get("description", ""))

        # Import items
        for item in data.get("items", []):
            # Extract core item data
            item_data = {
                "item_id": item["item_id"],
                "label": item["label"],
                "category": item["category"],
                "metadata": item.get("metadata", {})
            }

            # Add lifecycle data if present
            if "lifecycle" in item:
                item_data["purchase_date"] = item["lifecycle"].get("purchase_date")
                item_data["expected_lifespan_years"] = item["lifecycle"].get("expected_lifespan_years")

            # Add refill data if present
            if "refill_status" in item:
                item_data["current_quantity"] = item["refill_status"].get("current_quantity")
                item_data["refill_threshold"] = item["refill_status"].get("refill_threshold")
                # Calculate usage rate from days_remaining if available
                days = item["refill_status"].get("days_remaining")
                qty = item["refill_status"].get("current_quantity", 0)
                if days and days > 0:
                    item_data["usage_rate_per_day"] = qty / days

            self.register_item(**item_data)

            # Import current placement if present
            if "current_placement" in item:
                placement = item["current_placement"]
                self.record_placement(
                    item["item_id"],
                    zone=placement.get("zone", "unknown"),
                    distribution_type=placement.get("distribution_type", "placed"),
                    routine=placement.get("routine"),
                    motive=placement.get("motive"),
                    timestamp=placement.get("timestamp")
                )

        print(f"✓ Imported data from {filepath}")

    # ===== BACKUP & RESTORE =====

    def backup_database(self, backup_dir: str = "backups") -> str:
        """Create a timestamped backup of the database"""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"happy_places_{timestamp}.db")

        shutil.copy2(self.db_path, backup_path)
        print(f"✓ Database backed up to {backup_path}")
        return backup_path

    def restore_database(self, backup_path: str) -> None:
        """Restore database from a backup file"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Create a backup of current database before restoring
        current_backup = self.backup_database(backup_dir="backups/pre_restore")

        shutil.copy2(backup_path, self.db_path)
        print(f"✓ Database restored from {backup_path}")
        print(f"  Previous database backed up to {current_backup}")

    def list_backups(self, backup_dir: str = "backups") -> List[Dict]:
        """List available database backups"""
        if not os.path.exists(backup_dir):
            return []

        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith(".db"):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    "filename": filename,
                    "filepath": filepath,
                    "size_bytes": stat.st_size,
                    "created_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        return sorted(backups, key=lambda x: x["created_at"], reverse=True)


# ===== NFC INTEGRATION =====

class NFCReader:
    """
    NFC tag reading functionality for item identification.
    Requires nfcpy library and compatible NFC reader hardware.
    """

    @staticmethod
    def is_available() -> bool:
        """Check if NFC hardware is available"""
        try:
            import nfc
            clf = nfc.ContactlessFrontend()
            available = clf is not None
            if clf:
                clf.close()
            return available
        except (ImportError, Exception):
            return False

    @staticmethod
    def read_tag(timeout: int = 10) -> Optional[str]:
        """
        Read an NFC tag and return its UID as a string.

        Args:
            timeout: Seconds to wait for a tag (default 10)

        Returns:
            Tag UID as hex string, or None if timeout/error
        """
        try:
            import nfc

            def on_connect(tag):
                """Callback when tag is detected"""
                return tag.identifier.hex()

            clf = nfc.ContactlessFrontend()
            if not clf:
                print("⚠️  No NFC reader found")
                return None

            print(f"Waiting for NFC tag (timeout: {timeout}s)...")
            tag_id = clf.connect(rdwr={'on-connect': on_connect}, terminate=lambda: False)
            clf.close()

            if tag_id:
                print(f"✓ Tag detected: {tag_id}")
                return tag_id
            else:
                print("⚠️  No tag detected within timeout")
                return None

        except ImportError:
            print("⚠️  nfcpy library not installed. Run: pip install nfcpy")
            return None
        except Exception as e:
            print(f"⚠️  NFC read error: {e}")
            return None

    @staticmethod
    def scan_and_register(hp: 'HappyPlaces', label: str, category: str, **kwargs) -> Optional[str]:
        """
        Scan an NFC tag and register it as an item.

        Args:
            hp: HappyPlaces instance
            label: Item label
            category: Item category
            **kwargs: Additional item parameters

        Returns:
            Item ID (tag UID) if successful, None otherwise
        """
        tag_id = NFCReader.read_tag()
        if tag_id:
            hp.register_item(tag_id, label, category, **kwargs)
            print(f"✓ Item '{label}' registered with NFC tag {tag_id}")
            return tag_id
        return None


# ===== CLI INTERFACE =====

if __name__ == "__main__":
    import sys

    hp = HappyPlaces("happy_places.db")

    if len(sys.argv) < 2:
        print("Happy Places - Item Tracking System")
        print("\nUsage:")
        print("  python happy_places.py demo             - Run demo with sample data")
        print("  python happy_places.py export           - Export data to JSON")
        print("  python happy_places.py import [file]    - Import data from JSON")
        print("  python happy_places.py status <id>      - Get item status")
        print("  python happy_places.py list             - List all items")
        print("  python happy_places.py attention        - Show items needing attention")
        print("  python happy_places.py patterns         - Show distribution patterns")
        print("  python happy_places.py routines         - Show routine insights")
        print("\nItem Management:")
        print("  python happy_places.py add              - Add item interactively")
        print("  python happy_places.py add-nfc          - Add item via NFC scan")
        print("  python happy_places.py update <id>      - Update item quantity")
        print("  python happy_places.py delete <id>      - Delete an item")
        print("  python happy_places.py place <id>       - Record item placement")
        print("\nZone Management:")
        print("  python happy_places.py zones            - List all zones")
        print("  python happy_places.py add-zone         - Add zone interactively")
        print("\nBackup & Restore:")
        print("  python happy_places.py backup           - Create database backup")
        print("  python happy_places.py restore <file>   - Restore from backup")
        print("  python happy_places.py list-backups     - List available backups")
        sys.exit(0)

    command = sys.argv[1]
    
    if command == "demo":
        print("Running Happy Places demo...\n")
        
        # Register some zones
        hp.register_zone("bathroom_left_side", "Bathroom Left Side", "Near sink")
        hp.register_zone("bathroom_right_side", "Bathroom Right Side", "Near toilet")
        hp.register_zone("bedroom_floor", "Bedroom Floor")
        hp.register_zone("kitchen_table", "Kitchen Table")
        hp.register_zone("kitchen_counter", "Kitchen Counter")
        
        # Register items
        hp.register_item(
            "trash_can_bathroom",
            label="Bathroom Trash Can",
            category="good_stuff",
            purchase_date="2023-01-15",
            expected_lifespan_years=5
        )
        
        hp.register_item(
            "toothbrush",
            label="Electric Toothbrush",
            category="refillable",
            current_quantity=45,
            refill_threshold=10,
            usage_rate_per_day=1
        )
        
        hp.register_item(
            "left_sock",
            label="Left Sock (Blue)",
            category="good_stuff",
            purchase_date="2024-06-01",
            expected_lifespan_years=2
        )
        
        hp.register_item(
            "wallet",
            label="Leather Wallet",
            category="good_stuff",
            purchase_date="2020-03-10",
            expected_lifespan_years=8
        )
        
        hp.register_item(
            "salt_shaker",
            label="Salt Shaker",
            category="refillable",
            current_quantity=20,
            refill_threshold=15,
            usage_rate_per_day=0.5
        )
        
        # Record some placements
        hp.record_placement(
            "trash_can_bathroom",
            zone="bathroom_left_side",
            distribution_type="placed",
            routine="night routine",
            motive="reachability"
        )
        
        hp.record_placement(
            "toothbrush",
            zone="bathroom_left_side",
            distribution_type="placed",
            routine="morning routine",
            seen_with=["trash_can_bathroom"]
        )
        
        hp.record_placement(
            "left_sock",
            zone="bedroom_floor",
            distribution_type="spread",
            routine="undressing",
            motive="fatigue"
        )
        
        hp.record_placement(
            "wallet",
            zone="kitchen_table",
            distribution_type="stack",
            seen_with=["left_sock"],
            motive="convenience"
        )
        
        hp.record_placement(
            "salt_shaker",
            zone="kitchen_counter",
            distribution_type="placed"
        )
        
        print("✓ Demo data created!")
        print("\nTry these commands:")
        print("  python happy_places.py status trash_can_bathroom")
        print("  python happy_places.py list")
        print("  python happy_places.py patterns")
        print("  python happy_places.py export")
    
    elif command == "export":
        hp.export_to_json()
    
    elif command == "status" and len(sys.argv) > 2:
        item_id = sys.argv[2]
        status = hp.item_status(item_id)
        if status:
            print(json.dumps(status, indent=2))
        else:
            print(f"Item '{item_id}' not found")
    
    elif command == "list":
        items = hp.all_items()
        print(f"\nTotal items: {len(items)}\n")
        for item in items:
            print(f"  • {item['label']} ({item['item_id']}) - {item['category']}")
    
    elif command == "attention":
        attention = hp.items_needing_attention()
        print("\n=== Items Needing Attention ===\n")
        
        if attention["refill_needed"]:
            print("Refill Needed:")
            for item in attention["refill_needed"]:
                print(f"  • {item['label']}: {item['current_quantity']} remaining")
        
        if attention["replacement_soon"]:
            print("\nReplacement Soon:")
            for item in attention["replacement_soon"]:
                print(f"  • {item['label']}: {item['health_percent']}% life remaining")
        
        if not attention["refill_needed"] and not attention["replacement_soon"]:
            print("All items in good shape! ✓")
    
    elif command == "patterns":
        patterns = hp.distribution_patterns()
        print("\n=== Distribution Patterns ===\n")
        print("Overall:")
        for dist_type, count in patterns["overall_counts"].items():
            print(f"  {dist_type}: {count}")

        print("\nBy Zone:")
        for entry in patterns["by_zone"]:
            print(f"  {entry['zone']} - {entry['distribution_type']}: {entry['count']}")

    elif command == "routines":
        routines = hp.routine_insights()
        print("\n=== Routine Insights ===\n")
        if routines:
            for routine in routines:
                print(f"  {routine['routine']} ({routine['motive'] or 'no motive'})")
                print(f"    Frequency: {routine['frequency']} times")
                print(f"    Zones: {', '.join(routine['zones'])}")
                print()
        else:
            print("No routine patterns recorded yet.")

    elif command == "import":
        filepath = sys.argv[2] if len(sys.argv) > 2 else "happy_places_export.json"
        try:
            hp.import_from_json(filepath)
        except Exception as e:
            print(f"Import failed: {e}")

    elif command == "add":
        print("\n=== Add New Item ===\n")
        item_id = input("Item ID (or press Enter to generate): ").strip()
        if not item_id:
            import uuid
            item_id = str(uuid.uuid4())[:8]
            print(f"Generated ID: {item_id}")

        label = input("Label: ").strip()
        if not label:
            print("Label is required!")
            sys.exit(1)

        print("\nCategory:")
        print("  1. good_stuff (durable goods)")
        print("  2. refillable (consumables)")
        print("  3. disposable")
        category_choice = input("Choice (1-3): ").strip()
        category_map = {"1": "good_stuff", "2": "refillable", "3": "disposable"}
        category = category_map.get(category_choice, "good_stuff")

        item_data = {"item_id": item_id, "label": label, "category": category}

        if category == "good_stuff":
            purchase_date = input("Purchase date (YYYY-MM-DD, optional): ").strip()
            lifespan = input("Expected lifespan in years (optional): ").strip()
            if purchase_date:
                item_data["purchase_date"] = purchase_date
            if lifespan:
                item_data["expected_lifespan_years"] = float(lifespan)

        elif category == "refillable":
            quantity = input("Current quantity: ").strip()
            threshold = input("Refill threshold: ").strip()
            usage = input("Usage rate per day: ").strip()
            if quantity:
                item_data["current_quantity"] = int(quantity)
            if threshold:
                item_data["refill_threshold"] = int(threshold)
            if usage:
                item_data["usage_rate_per_day"] = float(usage)

        hp.register_item(**item_data)
        print(f"\n✓ Item '{label}' added with ID: {item_id}")

    elif command == "add-nfc":
        if not NFCReader.is_available():
            print("⚠️  NFC hardware not available")
            print("Make sure you have:")
            print("  1. nfcpy installed: pip install nfcpy")
            print("  2. NFC reader hardware connected")
            sys.exit(1)

        print("\n=== Add Item via NFC ===\n")
        label = input("Label: ").strip()
        if not label:
            print("Label is required!")
            sys.exit(1)

        print("\nCategory:")
        print("  1. good_stuff (durable goods)")
        print("  2. refillable (consumables)")
        print("  3. disposable")
        category_choice = input("Choice (1-3): ").strip()
        category_map = {"1": "good_stuff", "2": "refillable", "3": "disposable"}
        category = category_map.get(category_choice, "good_stuff")

        print("\nPlace NFC tag near reader...")
        tag_id = NFCReader.scan_and_register(hp, label, category)
        if not tag_id:
            print("Failed to register item")
            sys.exit(1)

    elif command == "update" and len(sys.argv) > 2:
        item_id = sys.argv[2]
        quantity = input(f"New quantity for '{item_id}': ").strip()
        if quantity:
            if hp.update_quantity(item_id, int(quantity)):
                print(f"✓ Updated quantity for {item_id}")
            else:
                print(f"Item '{item_id}' not found")

    elif command == "delete" and len(sys.argv) > 2:
        item_id = sys.argv[2]
        confirm = input(f"Delete '{item_id}' and all its placements? (yes/no): ").strip().lower()
        if confirm == "yes":
            if hp.delete_item(item_id):
                print(f"✓ Deleted item '{item_id}'")
            else:
                print(f"Item '{item_id}' not found")

    elif command == "place" and len(sys.argv) > 2:
        item_id = sys.argv[2]
        print(f"\n=== Record Placement for '{item_id}' ===\n")

        zone = input("Zone: ").strip()
        if not zone:
            print("Zone is required!")
            sys.exit(1)

        print("\nDistribution type:")
        print("  1. placed")
        print("  2. stack")
        print("  3. spread")
        print("  4. lose")
        print("  5. discard")
        dist_choice = input("Choice (1-5): ").strip()
        dist_map = {"1": "placed", "2": "stack", "3": "spread", "4": "lose", "5": "discard"}
        distribution_type = dist_map.get(dist_choice, "placed")

        routine = input("Routine (optional): ").strip() or None
        motive = input("Motive (optional): ").strip() or None

        hp.record_placement(item_id, zone, distribution_type, routine, motive)
        print(f"\n✓ Placement recorded for '{item_id}'")

    elif command == "zones":
        zones = hp.list_zones()
        print(f"\n=== Zones ({len(zones)}) ===\n")
        for zone in zones:
            print(f"  • {zone['zone_name']} ({zone['zone_id']})")
            if zone['description']:
                print(f"    {zone['description']}")

    elif command == "add-zone":
        print("\n=== Add New Zone ===\n")
        zone_id = input("Zone ID: ").strip()
        zone_name = input("Zone Name: ").strip()
        description = input("Description (optional): ").strip()

        if zone_id and zone_name:
            hp.register_zone(zone_id, zone_name, description)
            print(f"\n✓ Zone '{zone_name}' registered")
        else:
            print("Zone ID and name are required!")

    elif command == "backup":
        hp.backup_database()

    elif command == "restore" and len(sys.argv) > 2:
        backup_path = sys.argv[2]
        confirm = input(f"Restore from '{backup_path}'? Current data will be backed up. (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                hp.restore_database(backup_path)
            except Exception as e:
                print(f"Restore failed: {e}")

    elif command == "list-backups":
        backups = hp.list_backups()
        print(f"\n=== Available Backups ({len(backups)}) ===\n")
        for backup in backups:
            size_mb = backup['size_bytes'] / 1024 / 1024
            print(f"  • {backup['filename']}")
            print(f"    Created: {backup['created_at']}")
            print(f"    Size: {size_mb:.2f} MB")
            print(f"    Path: {backup['filepath']}")
            print()

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage.")
