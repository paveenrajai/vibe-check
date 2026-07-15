import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from vibe_check_core.profile.merge import apply_dot_path, parse_observation_value
from vibe_check_core.profile.schema import default_profile
from vibe_check_core.profile.validation import validate_profile


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
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        validate_profile(profile)
        return profile

    def save_profile(self, profile: dict[str, Any], *, source: str) -> None:
        self.ensure_data_dir()
        validate_profile(profile)
        profile["updated_at"] = datetime.now(UTC).isoformat()
        self.profile_path.write_text(
            json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self._append_audit({"action": "save_profile", "source": source})

    def record_observation(
        self,
        *,
        section: str,
        value: str,
        source: str,
        confidence: float = 0.8,
    ) -> dict[str, Any]:
        self.ensure_data_dir()
        observation = {
            "id": f"obs_{uuid4().hex[:12]}",
            "section": section,
            "value": value,
            "source": source,
            "confidence": confidence,
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat(),
        }
        with self.observations_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(observation, ensure_ascii=False) + "\n")
        self._append_audit({"action": "record_observation", "observation_id": observation["id"]})
        return observation

    def list_observations(self, status: str | None = None) -> list[dict[str, Any]]:
        observations = self._read_observations()
        if status is None:
            return observations
        return [obs for obs in observations if obs.get("status") == status]

    def accept_observation(self, observation_id: str) -> dict[str, Any]:
        observations = self._read_observations()
        observation = self._find_observation(observations, observation_id)
        if observation["status"] != "pending":
            msg = f"Observation {observation_id!r} is not pending"
            raise ValueError(msg)

        profile = self.load_profile()
        parsed_value = parse_observation_value(observation["value"])
        apply_dot_path(profile, observation["section"], parsed_value)
        self.save_profile(profile, source=f"accept_observation:{observation_id}")

        observation["status"] = "accepted"
        observation["reviewed_at"] = datetime.now(UTC).isoformat()
        self._write_observations(observations)
        self._append_audit(
            {
                "action": "accept_observation",
                "observation_id": observation_id,
                "section": observation["section"],
            }
        )
        return observation

    def reject_observation(self, observation_id: str) -> dict[str, Any]:
        observations = self._read_observations()
        observation = self._find_observation(observations, observation_id)
        if observation["status"] != "pending":
            msg = f"Observation {observation_id!r} is not pending"
            raise ValueError(msg)

        observation["status"] = "rejected"
        observation["reviewed_at"] = datetime.now(UTC).isoformat()
        self._write_observations(observations)
        self._append_audit({"action": "reject_observation", "observation_id": observation_id})
        return observation

    def _read_observations(self) -> list[dict[str, Any]]:
        self.ensure_data_dir()
        if not self.observations_path.exists():
            return []
        observations: list[dict[str, Any]] = []
        for line in self.observations_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                observations.append(json.loads(line))
        return observations

    def _write_observations(self, observations: list[dict[str, Any]]) -> None:
        self.ensure_data_dir()
        lines = [json.dumps(obs, ensure_ascii=False) for obs in observations]
        content = "\n".join(lines) + ("\n" if lines else "")
        self.observations_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _find_observation(
        observations: list[dict[str, Any]],
        observation_id: str,
    ) -> dict[str, Any]:
        for observation in observations:
            if observation.get("id") == observation_id:
                return observation
        msg = f"Unknown observation: {observation_id!r}"
        raise KeyError(msg)

    def _append_audit(self, event: dict[str, Any]) -> None:
        event = {**event, "at": datetime.now(UTC).isoformat()}
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
