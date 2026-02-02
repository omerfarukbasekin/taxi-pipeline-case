from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/{driver_id}/stats")
def driver_stats(driver_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_trips,
            COUNT(*) FILTER (WHERE status='done') AS done_trips,
            COUNT(*) FILTER (WHERE status='not_respond') AS not_respond
        FROM trips
        WHERE driver_id = %s
    """, (driver_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    return {
        "driver_id": driver_id,
        "total_trips": row[0],
        "done": row[1],
        "not_respond": row[2],
    }
