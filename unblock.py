import asyncio
import json
from pathlib import Path


class UnblockUnavailable(RuntimeError):
    pass


async def match_id(song_id, source=None) -> dict:
    """Bridge to the existing Node unblockmusic-utils package when available."""
    root = Path(__file__).resolve().parent.parent
    script = """
const { matchID } = require('@neteasecloudmusicapienhanced/unblockmusic-utils');
const id = process.argv[1];
const source = process.argv[2] || undefined;
matchID(id, source)
  .then((result) => {
    process.stdout.write(JSON.stringify(result || {}));
  })
  .catch((error) => {
    process.stderr.write(error && error.message ? error.message : String(error));
    process.exit(1);
  });
"""
    proc = await asyncio.create_subprocess_exec(
        "node",
        "-e",
        script,
        str(song_id or ""),
        str(source or ""),
        cwd=str(root),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        detail = stderr.decode("utf-8", "replace").strip()
        raise UnblockUnavailable(detail or "unblockmusic-utils is unavailable")
    try:
        return json.loads(stdout.decode("utf-8") or "{}")
    except json.JSONDecodeError as exc:
        raise UnblockUnavailable("unblockmusic-utils returned invalid JSON") from exc
