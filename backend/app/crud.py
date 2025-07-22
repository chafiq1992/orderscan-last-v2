from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Scan
from .schemas import ScanIn, ScanOut

def _clean(barcode: str) -> str | None:
    digits = ''.join(filter(str.isdigit, barcode)).lstrip('0')
    if not digits or len(digits) > 6:
        return None
    return '#' + digits

async def append_scan(db: AsyncSession, data: ScanIn) -> ScanOut:
    order_name = _clean(data.barcode)
    if not order_name:
        return ScanOut(result="❌ Invalid barcode")

    tag = None  # TODO: implement your tag detection logic here
    note = "✅ Saved" if tag else "⚠️ No tag"

    db_scan = Scan(order=order_name, tag=tag, result=note)
    db.add(db_scan)
    await db.commit()
    await db.refresh(db_scan)

    return ScanOut(result=note, order=order_name, tag=tag)

async def tag_summary(db: AsyncSession) -> dict[str, int]:
    rows = await db.execute(select(Scan.tag, func.count()).group_by(Scan.tag))
    return {t or "none": c for t, c in rows.all()}
