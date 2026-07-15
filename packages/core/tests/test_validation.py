import pytest
from vibe_check_core.profile.schema import default_profile
from vibe_check_core.profile.store import ProfileStore
from vibe_check_core.profile.validation import ProfileValidationError, validate_profile


def test_default_profile_passes_validation() -> None:
    validate_profile(default_profile())


def test_save_profile_rejects_invalid_document(tmp_path) -> None:
    store = ProfileStore(tmp_path)
    profile = default_profile()
    profile["unknown_key"] = "nope"

    with pytest.raises(ProfileValidationError):
        store.save_profile(profile, source="test")


def test_load_profile_rejects_corrupt_file(tmp_path) -> None:
    store = ProfileStore(tmp_path)
    store.ensure_data_dir()
    store.profile_path.write_text('{"$schema": "wrong"}\n', encoding="utf-8")

    with pytest.raises(ProfileValidationError):
        store.load_profile()
