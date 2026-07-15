import os
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Config:
    data_dir: str
    transport: Literal["stdio", "http"]
    host: str
    port: int
    auth_token: str | None


def get_config() -> Config:
    transport = os.environ.get("VIBE_CHECK_TRANSPORT", "stdio")
    if transport not in ("stdio", "http"):
        msg = f"Invalid VIBE_CHECK_TRANSPORT: {transport!r}"
        raise ValueError(msg)

    return Config(
        data_dir=os.environ.get("VIBE_CHECK_DATA_DIR", "./data"),
        transport=transport,  # type: ignore[arg-type]
        host=os.environ.get("VIBE_CHECK_HOST", "0.0.0.0"),
        port=int(os.environ.get("VIBE_CHECK_PORT", "3100")),
        auth_token=os.environ.get("VIBE_CHECK_AUTH_TOKEN"),
    )
