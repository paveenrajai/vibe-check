import json

from vibe_check_core.profile.store import ProfileStore


def test_load_profile_creates_default(tmp_path) -> None:
    store = ProfileStore(tmp_path)
    profile = store.load_profile()

    assert profile["$schema"] == "vibe-check/profile/v1"
    assert store.profile_path.exists()
    assert json.loads(store.profile_path.read_text(encoding="utf-8")) == profile
