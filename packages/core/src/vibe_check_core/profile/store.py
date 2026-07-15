import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vibe_check_core.profile.schema import default_profile


class ProfileStore:
    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.profile_path = self.data_dir / "profile.json"
        self.audit_path = self.data_dir / "audit.jsonl"
        self.observations_path = self.data_dir / "observations.jsonl"

    def ensure_data_dir(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_profile(self) -> dict[str, Any]:
        self.ensure_data_dir()
        if not self.profile_path.exists():
            profile = default_profile()
            self.save_profile(profile, source="bootstrap")
            return profile
        return json.loads(self.profile_path.read_text(encoding="utf-8"))

    def save_profile(self, profile: dict[str, Any], *, source: str) -> None:
        self.ensure_data_dir()
        profile["updated_at"] = datetime.now(UTC).isoformat()
        self.profile_path.write_text(
            json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self._append_audit({"action": "save_profile", "source": source})

    def _append_audit(self, event: dict[str, Any]) -> None:
        event = {**event, "at": datetime.now(UTC).isoformat()}
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
