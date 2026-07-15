from vibe_check_core.profile.store import ProfileStore


def test_observation_accept_merge_and_reject(tmp_path) -> None:
    store = ProfileStore(tmp_path)
    store.load_profile()

    obs = store.record_observation(
        section="code.css_units",
        value="never px",
        source="test",
    )
    pending = store.list_observations(status="pending")
    assert len(pending) == 1

    accepted = store.accept_observation(obs["id"])
    assert accepted["status"] == "accepted"
    assert store.list_observations(status="pending") == []

    profile = store.load_profile()
    assert profile["code"]["css_units"] == "never px"

    obs2 = store.record_observation(
        section="communication.notes",
        value="too much bold",
        source="test",
    )
    rejected = store.reject_observation(obs2["id"])
    assert rejected["status"] == "rejected"
    profile = store.load_profile()
    assert profile["communication"]["notes"] == ""
