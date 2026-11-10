"""Static bearer-token auth for the HTTP transport."""

import hmac

from starlette.types import ASGIApp, Receive, Scope, Send


class BearerTokenMiddleware:
    """Reject HTTP requests whose `Authorization: Bearer <token>` does not match."""

    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self._expected = f"Bearer {token}".encode()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        provided = dict(scope["headers"]).get(b"authorization", b"")
        if hmac.compare_digest(provided, self._expected):
            await self.app(scope, receive, send)
            return

        await send(
            {
                "type": "http.response.start",
                "status": 401,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"www-authenticate", b'Bearer realm="vibe-check"'),
                ],
            }
        )
        await send({"type": "http.response.body", "body": b'{"error":"unauthorized"}'})
