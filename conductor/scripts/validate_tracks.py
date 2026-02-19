#!/usr/bin/env python3
"""Validate Conductor tracks registry and track consistency."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class TrackEntry:
    name: str
    rel_path: str
    phase: Optional[str] = None
    source: str = "unknown"

    @property
    def dir_name(self) -> str:
        return Path(self.rel_path.strip().lstrip("./")).name


def parse_tracks_registry(tracks_md: Path) -> List[TrackEntry]:
    text = tracks_md.read_text(encoding="utf-8", errors="replace")
    entries: List[TrackEntry] = []
    seen = set()

    # Meta-track
    for m in re.finditer(r"Meta-track:\s*\[([^\]]+)\]\(([^)]+)\)", text):
        name, rel = m.group(1).strip(), m.group(2).strip()
        if name not in seen:
            seen.add(name)
            entries.append(TrackEntry(name=name, rel_path=rel, source="meta"))

    # Canonical format:
    # - [ ] **Track: name** (./tracks/name/)
    #   - Phase: 1
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(
            r"^\s*-\s*\[[ xX~]?\]\s*\*\*Track:\s*([^*]+)\*\*\s*\(([^)]+)\)\s*$",
            line,
        )
        if not m:
            i += 1
            continue

        name = m.group(1).strip()
        rel = m.group(2).strip()
        phase = None

        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if re.match(r"^\s*-\s*\[[ xX~]?\]\s*\*\*Track:", nxt):
                break
            pm = re.match(r"^\s*-\s*Phase:\s*(.+?)\s*$", nxt)
            if pm:
                phase = pm.group(1).strip()
            j += 1

        if name not in seen:
            seen.add(name)
            entries.append(TrackEntry(name=name, rel_path=rel, phase=phase, source="canonical"))
        i = j

    # Fallback table format (legacy in repo)
    for m in re.finditer(
        r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\|\s*([^|]+)\|",
        text,
        re.M,
    ):
        name = m.group(1).strip()
        rel = m.group(2).strip()
        phase = m.group(4).strip()
        if name not in seen:
            seen.add(name)
            entries.append(TrackEntry(name=name, rel_path=rel, phase=phase, source="table"))

    return entries


def count_tasks(plan_text: str) -> Tuple[int, int, int]:
    completed = in_progress = pending = 0
    for raw in plan_text.splitlines():
        s = raw.strip()
        if not s:
            continue
        up = s.upper()
        if "IN PROGRESS" in up or "[~]" in s:
            in_progress += 1
        elif "[X]" in up or "COMPLETED" in up or "DONE" in up:
            completed += 1
        elif "[ ]" in s or "PENDING" in up or "TODO" in up or "NOT STARTED" in up:
            pending += 1
    return completed, in_progress, pending


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    conductor = repo_root / "conductor"
    errors: List[str] = []
    warnings: List[str] = []

    required_core = [
        conductor / "tracks.md",
        conductor / "product.md",
        conductor / "tech-stack.md",
        conductor / "workflow.md",
    ]
    for p in required_core:
        if not p.exists():
            errors.append(f"Missing required core file: {p.relative_to(repo_root)}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    tracks_md = conductor / "tracks.md"
    entries = parse_tracks_registry(tracks_md)
    if not entries:
        errors.append("No tracks parsed from conductor/tracks.md")
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    # Validate referenced directories and files.
    all_track_dirs = sorted(p.name for p in (conductor / "tracks").iterdir() if p.is_dir())
    phase_by_track: Dict[str, str] = {}
    metadata_by_track: Dict[str, Dict] = {}

    for entry in entries:
        tdir = (conductor / entry.rel_path.strip().lstrip("./")).resolve()
        if not tdir.exists():
            errors.append(f"{entry.name}: missing track directory {tdir.relative_to(repo_root)}")
            continue

        idx = tdir / "index.md"
        plan = tdir / "plan.md"
        meta = tdir / "metadata.json"
        spec = tdir / "spec.md"

        for req in (idx, plan, meta):
            if not req.exists():
                errors.append(f"{entry.name}: missing {req.name}")

        # Meta-track is allowed to skip spec; all others should have it.
        if entry.name != "health-plugin" and not spec.exists():
            errors.append(f"{entry.name}: missing spec.md")

        if meta.exists():
            try:
                meta_obj = json.loads(meta.read_text(encoding="utf-8", errors="replace"))
            except Exception as exc:
                errors.append(f"{entry.name}: invalid metadata.json ({exc})")
                meta_obj = {}
            metadata_by_track[entry.dir_name] = meta_obj

            track_id = meta_obj.get("track_id")
            if track_id and track_id != entry.dir_name:
                errors.append(
                    f"{entry.name}: metadata track_id '{track_id}' does not match directory '{entry.dir_name}'"
                )

            for dep in meta_obj.get("dependencies", []):
                if dep not in all_track_dirs:
                    errors.append(f"{entry.name}: dependency '{dep}' does not match any track directory")

        # Determine phase for phase integrity checks.
        if entry.phase is not None:
            phase_by_track[entry.dir_name] = entry.phase

        if plan.exists():
            plan_text = plan.read_text(encoding="utf-8", errors="replace")
            _, in_prog, _ = count_tasks(plan_text)
            status = metadata_by_track.get(entry.dir_name, {}).get("status", "")
            if status == "active":
                if in_prog != 1:
                    errors.append(
                        f"{entry.name}: active track must have exactly one IN PROGRESS task (found {in_prog})"
                    )
                if "Owner:" not in plan_text or "Updated:" not in plan_text:
                    errors.append(f"{entry.name}: active plan should include Owner and Updated fields")

            # Jurisdiction references for health standards-aligned plans.
            if "Follows [health skill standards]" in plan_text:
                if "AU/NZ" not in plan_text:
                    errors.append(f"{entry.name}: plan references health standards but lacks AU/NZ guidance")
                if "US/EU-lite" not in plan_text:
                    errors.append(f"{entry.name}: plan references health standards but lacks US/EU-lite guidance")

    # Phase integrity: dependency should not be in later numeric phase.
    def parse_phase(value: Optional[str]) -> Optional[int]:
        if value is None:
            return None
        s = value.strip()
        if s.isdigit():
            return int(s)
        m = re.search(r"\b([1-9])\b", s)
        return int(m.group(1)) if m else None

    phase_num: Dict[str, int] = {}
    for dname, ph in phase_by_track.items():
        n = parse_phase(ph)
        if n is not None:
            phase_num[dname] = n

    for dname, meta in metadata_by_track.items():
        this_phase = phase_num.get(dname)
        if this_phase is None:
            continue
        for dep in meta.get("dependencies", []):
            dep_phase = phase_num.get(dep)
            if dep_phase is None:
                continue
            if dep_phase > this_phase:
                errors.append(
                    f"{dname}: depends on later-phase track '{dep}' ({dep_phase} > {this_phase})"
                )

    # Health standards files must exist.
    standards_root = conductor / "tracks" / "health-plugin"
    for req in (
        standards_root / "skill-standards.md",
        standards_root / "interoperability-standards.md",
        standards_root / "jurisdiction-au-nz.md",
        standards_root / "jurisdiction-us-eu-lite.md",
    ):
        if not req.exists():
            errors.append(f"Missing required health standards file: {req.relative_to(repo_root)}")

    # Show summary.
    print(f"Tracks parsed: {len(entries)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARN: {msg}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
