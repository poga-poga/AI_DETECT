from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    content = await file.read()

    text = content.decode("utf-8", errors="ignore")
    lines = text.splitlines()

    events = []
    failed_login_count = 0

    for line in lines:
        lower_line = line.lower()

        if "failed login" in lower_line or "failed password" in lower_line:
            failed_login_count += 1

            events.append({"type": "failed_login", "severity": "medium", "line": line})

        elif "error" in lower_line:
            events.append({"type": "error", "severity": "low", "line": line})

        elif "warning" in lower_line:
            events.append({"type": "warning", "severity": "low", "line": line})

    if failed_login_count >= 3:
        for event in events:
            if event["type"] == "failed_login":
                event["severity"] = "high"

    summary = "No major security issue detected."
    recommended_action = "No action required."

    overall_severity = "low"

    if failed_login_count >= 3:
        summary = "Multiple failed login attempts detected."
        recommended_action = (
            "Review the source of the login attempts "
            "and verify the affected account."
        )
        overall_severity = "high"

    return {
        "filename": file.filename,
        "size": len(content),
        "total_lines": len(lines),
        "event_count": len(events),
        "failed_login_count": failed_login_count,
        "summary": summary,
        "recommended_action": recommended_action,
        "events": events,
        "overall_severity": overall_severity,
    }
