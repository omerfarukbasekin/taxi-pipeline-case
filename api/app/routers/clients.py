from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/{client_id}/trips")
def client_trips(client_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT trip_id, driver_id, trip_date, status
        FROM trips
        WHERE client_id = %s
        ORDER BY trip_date DESC
    """, (client_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "trip_id": r[0],
            "driver_id": r[1],
            "trip_date": r[2],
            "status": r[3],
        }
        for r in rows
    ]
