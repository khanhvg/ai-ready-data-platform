"""Private HTTP admission independent of the later portal/BFF."""
from __future__ import annotations
import http.server, json, os, pathlib, secrets
from collections import Counter
from .registry import validate_request

BODY_LIMIT = 16_384
HOST = "runner.local"


class TransportError(ValueError):
    pass


def admit(*, method: str, headers: list[tuple[str, str]], body: bytes, bearer: str, csrf: str, peer_uid: int, effective_uid: int, expected_host: str=HOST) -> dict[str, object]:
    normalized = [(k.lower(), v) for k, v in headers]
    counts = Counter(k for k, _ in normalized)
    if any(v > 1 for v in counts.values()):
        raise TransportError("RUNNER_HEADER_AMBIGUOUS")
    h = dict(normalized)
    if peer_uid != effective_uid:
        raise TransportError("RUNNER_PEER_FORBIDDEN")
    if method != "POST":
        raise TransportError("RUNNER_METHOD_FORBIDDEN")
    if h.get("host") != expected_host:
        raise TransportError("RUNNER_HOST_FORBIDDEN")
    if h.get("origin", "") or "cookie" in h or "sec-fetch-site" in h or "access-control-request-method" in h:
        raise TransportError("RUNNER_BROWSER_REQUEST_FORBIDDEN")
    if h.get("authorization") != f"Bearer {bearer}" or h.get("x-runner-csrf") != csrf:
        raise TransportError("RUNNER_ADMISSION_SECRET_INVALID")
    if h.get("content-type") != "application/json":
        raise TransportError("RUNNER_CONTENT_TYPE_INVALID")
    if "transfer-encoding" in h or "content-length" not in h:
        raise TransportError("RUNNER_FRAMING_INVALID")
    try:
        length = int(h["content-length"])
    except ValueError as exc:
        raise TransportError("RUNNER_FRAMING_INVALID") from exc
    if length != len(body) or length > BODY_LIMIT:
        raise TransportError("RUNNER_BODY_TOO_LARGE")
    try:
        value = json.loads(body.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransportError("RUNNER_JSON_INVALID") from exc
    return validate_request(value)


def serve_loopback(service: object, control_file: pathlib.Path) -> None:
    bearer=secrets.token_urlsafe(32); csrf=secrets.token_urlsafe(32)
    class Handler(http.server.BaseHTTPRequestHandler):
        server_version=""; sys_version=""
        def do_OPTIONS(self)->None:self._reject(403,"RUNNER_BROWSER_REQUEST_FORBIDDEN")
        def do_GET(self)->None:self._reject(405,"RUNNER_METHOD_FORBIDDEN")
        def do_POST(self)->None:
            try:
                raw_length=self.headers.get("Content-Length")
                if raw_length is None or not raw_length.isdigit() or int(raw_length)>BODY_LIMIT:
                    raise TransportError("RUNNER_BODY_TOO_LARGE")
                body=self.rfile.read(int(raw_length)+1)
                if len(body)!=int(raw_length):raise TransportError("RUNNER_FRAMING_INVALID")
                expected=f"127.0.0.1:{self.server.server_port}"
                request=admit(method="POST",headers=list(self.headers.raw_items()),body=body,bearer=bearer,csrf=csrf,peer_uid=os.geteuid(),effective_uid=os.geteuid(),expected_host=expected)
                result=service.run(request)
                self._json(200,result)
            except Exception as exc:self._reject(400,str(exc))
        def _reject(self,status:int,code:str)->None:self._json(status,{"status":"fail","failureCode":code[:128]})
        def _json(self,status:int,value:dict[str,object])->None:
            raw=json.dumps(value,sort_keys=True,separators=(",",":")).encode()+b"\n"
            self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(raw)
        def log_message(self,*_:object)->None:return
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),Handler)
    value={"schemaVersion":"runner-private-control-v1","host":f"127.0.0.1:{server.server_port}","bearer":bearer,"csrf":csrf}
    control_file.parent.mkdir(mode=0o700,parents=True,exist_ok=True);control_file.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n");os.chmod(control_file,0o600)
    try:server.serve_forever(poll_interval=.1)
    finally:server.server_close();control_file.unlink(missing_ok=True)
