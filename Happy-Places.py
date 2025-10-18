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

    # ===== DATA EXPORT =====
    
    def export_to_json(self, filepath: str = "happy_places_export.json") -> None:
        """Export all data to JSON file for GitHub Pages"""
        data = {
            "exported_at": datetime.datetime.utcnow().isoformat(),
            "items": [],
            "zones": self.list_zones(),
            "patterns": self.distribution_patterns(),
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


# ===== CLI INTERFACE =====

if __name__ == "__main__":
    import sys
    
    hp = HappyPlaces("happy_places.db")
    
    if len(sys.argv) < 2:
        print("Happy Places - Item Tracking System")
        print("\nUsage:")
        print("  python happy_places.py demo          - Run demo with sample data")
        print("  python happy_places.py export        - Export data to JSON")
        print("  python happy_places.py status <id>   - Get item status")
        print("  python happy_places.py list          - List all items")
        print("  python happy_places.py attention     - Show items needing attention")
        print("  python happy_places.py patterns      - Show distribution patterns")
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
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage.")
