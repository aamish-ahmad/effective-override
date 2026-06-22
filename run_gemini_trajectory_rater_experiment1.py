"""Run Gemini full-trajectory ratings for the validated Experiment 1 dataset."""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "experiment1.csv"
PROMPT_PATH = ROOT / "prompts" / "blind_rater_prompt.md"
RESPONSES_PATH = ROOT / "data" / "experiment1_trajectory_rater_responses.md"
ERRORS_PATH = ROOT / "data" / "experiment1_trajectory_rater_errors.md"
VALIDATOR_PATH = ROOT / "scripts" / "check_experiment1.py"
DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_SLEEP_SECONDS = 45.0
MAX_RATE_LIMIT_ATTEMPTS = 3

REQUIRED_FIELDS = {
    "trajectory_id",
    "crossing_present",
    "crossing_step",
    "state_sequence",
    "override_attempt",
    "system_structure",
    "downstream_constraint",
    "reason",
    "confidence",
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "trajectory_id": {"type": "string"},
        "crossing_present": {
            "type": "string",
            "enum": ["yes", "no", "uncertain"],
        },
        "crossing_step": {
            "anyOf": [{"type": "integer"}, {"type": "null"}]
        },
        "state_sequence": {
            "type": "array",
            "items": {"type": "integer", "enum": [0, 1, 2, 3]},
        },
        "override_attempt": {"type": "string"},
        "system_structure": {"type": "string"},
        "downstream_constraint": {"type": "string"},
        "reason": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": sorted(REQUIRED_FIELDS),
    "additionalProperties": False,
}

JSON_ONLY_RETRY = """

Your previous response was not valid against the required JSON format. Return exactly
one JSON object and nothing else. Do not use Markdown fences or explanatory text.
Include every required field with the requested types.
"""


def validate_dataset() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode:
        raise RuntimeError("Experiment 1 validation failed; no API calls were made")


def load_trajectories() -> list[dict[str, object]]:
    trajectories = []
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            steps = json.loads(row["steps_json"])
            if not isinstance(steps, list) or not steps:
                raise ValueError(f"{row['trajectory_id']}: steps_json is not a nonempty list")
            trajectories.append(
                {"trajectory_id": row["trajectory_id"], "steps": steps}
            )
    return trajectories


def build_prompt(template: str, trajectory: dict[str, object]) -> str:
    steps = trajectory["steps"]
    numbered_steps = "\n".join(
        f"{index}. {step}" for index, step in enumerate(steps, start=1)
    )
    prompt = template.replace("{{TRAJECTORY_STEPS}}", numbered_steps)
    return f"{prompt.rstrip()}\n\ntrajectory_id: {trajectory['trajectory_id']}\n"


def validate_response(value: object, trajectory_id: str, step_count: int) -> dict:
    if not isinstance(value, dict):
        raise ValueError("response is not a JSON object")
    missing = REQUIRED_FIELDS - value.keys()
    extra = value.keys() - REQUIRED_FIELDS
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    if extra:
        raise ValueError(f"unexpected fields: {sorted(extra)}")
    if value["trajectory_id"] != trajectory_id:
        raise ValueError(f"trajectory_id must equal {trajectory_id}")

    label = str(value["crossing_present"]).strip().lower()
    if label not in {"yes", "no", "uncertain"}:
        raise ValueError("crossing_present must be yes, no, or uncertain")
    value["crossing_present"] = label
    crossing_step = value["crossing_step"]
    if label == "yes":
        if isinstance(crossing_step, bool) or not isinstance(crossing_step, int):
            raise ValueError("yes requires an integer crossing_step")
        if not 1 <= crossing_step <= step_count:
            raise ValueError("crossing_step is outside the trajectory")
    elif crossing_step is not None:
        raise ValueError("no or uncertain requires crossing_step=null")

    states = value["state_sequence"]
    if not isinstance(states, list) or len(states) != step_count:
        raise ValueError(f"state_sequence must contain {step_count} states")
    if any(isinstance(state, bool) or state not in {0, 1, 2, 3} for state in states):
        raise ValueError("state_sequence contains a state outside 0-3")
    if label == "yes" and states[crossing_step - 1] != 3:
        raise ValueError("crossing_step must identify a state 3")
    if label == "yes" and 3 in states and crossing_step != states.index(3) + 1:
        raise ValueError("crossing_step must be the first state 3")
    if label != "yes" and 3 in states:
        raise ValueError("no or uncertain response cannot contain state 3")

    for field in (
        "override_attempt", "system_structure", "downstream_constraint", "reason"
    ):
        if not isinstance(value[field], str):
            raise ValueError(f"{field} must be a string")
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be numeric")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return value


def write_markdown(path: Path, entries: list[tuple[str, str]]) -> None:
    content = "".join(
        f"## {trajectory_id}\n\n{body.strip()}\n\n"
        for trajectory_id, body in entries
    )
    path.write_text(content, encoding="utf-8")


def read_markdown_sections(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8-sig")
    header = re.compile(r"(?m)^##\s+([A-Za-z0-9_-]+)\s*$")
    matches = list(header.finditer(content))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections[match.group(1)] = content[match.end():end].strip()
    return sections


def append_markdown(path: Path, trajectory_id: str, body: str) -> None:
    prefix = ""
    if path.exists() and path.stat().st_size:
        prefix = "\n"
    with path.open("a", encoding="utf-8", newline="") as destination:
        destination.write(f"{prefix}## {trajectory_id}\n\n{body.strip()}\n")


def remove_markdown_section(path: Path, trajectory_id: str) -> None:
    sections = read_markdown_sections(path)
    if trajectory_id not in sections:
        return
    del sections[trajectory_id]
    if sections:
        write_markdown(path, list(sections.items()))
    else:
        path.unlink(missing_ok=True)


def load_completed_ids(
    trajectories: list[dict[str, object]],
) -> set[str]:
    by_id = {str(item["trajectory_id"]): item for item in trajectories}
    completed = set()
    for trajectory_id, body in read_markdown_sections(RESPONSES_PATH).items():
        trajectory = by_id.get(trajectory_id)
        if trajectory is None:
            print(f"WARNING: ignoring response for unknown ID {trajectory_id}")
            continue
        try:
            parsed = json.loads(body)
            validate_response(parsed, trajectory_id, len(trajectory["steps"]))
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"WARNING: existing response for {trajectory_id} is invalid: {error}")
            continue
        completed.add(trajectory_id)
    return completed


def request_sleep_seconds() -> float:
    raw_value = os.getenv("GEMINI_REQUEST_SLEEP_SECONDS", str(DEFAULT_SLEEP_SECONDS))
    try:
        value = float(raw_value)
    except ValueError as error:
        raise ValueError("GEMINI_REQUEST_SLEEP_SECONDS must be numeric") from error
    if value < 0:
        raise ValueError("GEMINI_REQUEST_SLEEP_SECONDS cannot be negative")
    return value


def is_rate_limit_error(error: Exception) -> bool:
    message = str(error).lower()
    return "429" in message or "resource_exhausted" in message


def is_daily_quota_error(error: Exception) -> bool:
    if not is_rate_limit_error(error):
        return False
    message = str(error).lower()
    return (
        "generaterequestsperdayperprojectpermodel-freetier" in message
        or "daily quota" in message
        or ("per day" in message and "quota" in message)
        or ("perday" in message and "quota" in message)
    )


class DailyQuotaExhausted(RuntimeError):
    """Signal that retrying this run cannot succeed until daily quota resets."""


def retry_delay_seconds(error: Exception) -> float:
    message = str(error)
    patterns = (
        r"retry(?:\s+in|\s+after|Delay[^0-9]*)\s*([0-9]+(?:\.[0-9]+)?)\s*s",
        r"retryDelay[^0-9]*([0-9]+(?:\.[0-9]+)?)\s*s",
        r"retry_delay[^0-9]*seconds[^0-9]*([0-9]+(?:\.[0-9]+)?)",
    )
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return float(match.group(1))
    return DEFAULT_SLEEP_SECONDS


class PacedGenerator:
    def __init__(self, client, model: str, sleep_seconds: float):
        self.client = client
        self.model = model
        self.sleep_seconds = sleep_seconds
        self.last_successful_call: float | None = None

    def _pace(self) -> None:
        if self.last_successful_call is None:
            return
        elapsed = time.monotonic() - self.last_successful_call
        remaining = self.sleep_seconds - elapsed
        if remaining > 0:
            print(f"Sleeping {remaining:.1f} seconds before the next API call")
            time.sleep(remaining)

    def generate(self, prompt: str):
        last_error: Exception | None = None
        for attempt in range(1, MAX_RATE_LIMIT_ATTEMPTS + 1):
            self._pace()
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": RESPONSE_SCHEMA,
                    },
                )
                self.last_successful_call = time.monotonic()
                return response
            except Exception as error:
                last_error = error
                if is_daily_quota_error(error):
                    raise DailyQuotaExhausted(str(error)) from error
                if not is_rate_limit_error(error) or attempt == MAX_RATE_LIMIT_ATTEMPTS:
                    raise
                delay = retry_delay_seconds(error)
                print(
                    f"Rate limited (attempt {attempt}/{MAX_RATE_LIMIT_ATTEMPTS}); "
                    f"sleeping {delay:.1f} seconds before retry"
                )
                time.sleep(delay)
        raise last_error  # pragma: no cover


def main() -> int:
    validate_dataset()
    trajectories = load_trajectories()
    template = PROMPT_PATH.read_text(encoding="utf-8-sig")

    load_dotenv(ROOT / ".env")
    completed_ids = load_completed_ids(trajectories)
    remaining = [
        trajectory
        for trajectory in trajectories
        if str(trajectory["trajectory_id"]) not in completed_ids
    ]
    sleep_seconds = request_sleep_seconds()
    print(f"Already completed: {len(completed_ids)}")
    print(f"Remaining: {len(remaining)}")
    print(f"API request sleep delay: {sleep_seconds:.1f} seconds")

    if not remaining:
        print("All trajectories are already complete; no API calls were made.")
        return 0

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set; no API calls were made.")
        return 2

    from google import genai

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = genai.Client(api_key=api_key)
    generator = PacedGenerator(client, model, sleep_seconds)
    successes = 0
    failures = 0
    existing_errors = read_markdown_sections(ERRORS_PATH)
    daily_quota_exhausted = False

    for trajectory in remaining:
        trajectory_id = str(trajectory["trajectory_id"])
        prompt = build_prompt(template, trajectory)
        raw_outputs: list[str] = []
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                response = generator.generate(
                    prompt if attempt == 0 else prompt + JSON_ONLY_RETRY,
                )
                raw = response.text or ""
                raw_outputs.append(raw)
                parsed = json.loads(raw)
                validated = validate_response(
                    parsed, trajectory_id, len(trajectory["steps"])
                )
                append_markdown(
                    RESPONSES_PATH,
                    trajectory_id,
                    json.dumps(validated, indent=2, ensure_ascii=False),
                )
                remove_markdown_section(ERRORS_PATH, trajectory_id)
                successes += 1
                print(f"Rated {trajectory_id}")
                last_error = None
                break
            except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
                last_error = error
                if attempt == 0:
                    print(f"Retrying {trajectory_id} after invalid JSON response")
                    continue
            except DailyQuotaExhausted as error:
                last_error = error
                daily_quota_exhausted = True
                break
            except Exception as error:
                last_error = error
                break

        if last_error is not None:
            error_body = (
                f"Error: {type(last_error).__name__}: {last_error}\n\n"
                + "\n\n--- Retry output ---\n\n".join(
                    output or "(empty output)" for output in raw_outputs
                )
            )
            if trajectory_id not in existing_errors:
                append_markdown(ERRORS_PATH, trajectory_id, error_body)
                existing_errors[trajectory_id] = error_body
            failures += 1
            print(f"ERROR {trajectory_id}: {type(last_error).__name__}: {last_error}")
        if daily_quota_exhausted:
            completed_count = len(completed_ids) + successes
            print("Daily quota exhausted")
            print(f"Completed: {completed_count}")
            print(f"Remaining: {len(trajectories) - completed_count}")
            break

    print(f"Already completed: {len(completed_ids)}")
    print(f"Rows attempted this run: {len(remaining)}")
    print(f"Successful JSON responses this run: {successes}")
    print(f"Errors this run: {failures}")
    print(f"Output path: {RESPONSES_PATH}")
    return 2 if daily_quota_exhausted else (0 if not failures else 1)


if __name__ == "__main__":
    raise SystemExit(main())
