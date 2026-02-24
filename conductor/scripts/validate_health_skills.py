#!/usr/bin/env python3
"""Validate health plugin skills against quality standards.

This script validates health skills against the 14-section architecture
defined in conductor/tracks/health-plugin/skill-standards.md.

Usage:
    python validate_health_skills.py [skill_path]

    If skill_path is provided, validates only that skill.
    Otherwise, validates all skills in health/skills/.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ValidationError:
    """Represents a validation error."""

    skill_name: str
    section: str
    message: str
    severity: str = "ERROR"


@dataclass
class SkillValidationResult:
    """Results of validating a single skill."""

    skill_name: str
    skill_path: Path
    line_count: int = 0
    sections_found: Set[str] = field(default_factory=set)
    sections_required: Set[str] = field(default_factory=set)
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def missing_sections(self) -> Set[str]:
        return self.sections_required - self.sections_found


class HealthSkillValidator:
    """Validator for health plugin skills."""

    REQUIRED_SECTIONS = {
        "When to Use This Skill",
        "Regulatory Context",
        "Confidence Indicators",
        "Detailed Guidance",
        "Documentation Requirements",
        "Common Mistakes",
        "When to Escalate",
        "Privacy Considerations",
        "Standard and Lite Modes",
        "Tool Requirements",
        "Success Indicators",
        "Related Skills",
    }

    PLACEHOLDER_PATTERNS = [
        r"\bTODO\b",
        r"\bTBD\b",
        r"\bFIXME\b",
        r"\bXXX\b",
        r"\[placeholder\]",
        r"\{placeholder\}",
        r"\[to be determined\]",
        r"\[insert",
        r"\[describe",
    ]

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results: List[SkillValidationResult] = []

    def validate_all_skills(self) -> List[SkillValidationResult]:
        health_skills_dir = self.repo_root / "health" / "skills"

        if not health_skills_dir.exists():
            print(f"ERROR: Health skills directory not found: {health_skills_dir}")
            return []

        skill_dirs = [
            d
            for d in health_skills_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        print(f"Found {len(skill_dirs)} health skill directories")

        for skill_dir in sorted(skill_dirs):
            result = self.validate_skill(skill_dir)
            self.results.append(result)

        return self.results

    def validate_skill(self, skill_dir: Path) -> SkillValidationResult:
        skill_name = skill_dir.name
        skill_file = skill_dir / "SKILL.md"

        result = SkillValidationResult(
            skill_name=skill_name,
            skill_path=skill_file,
            sections_required=self.REQUIRED_SECTIONS.copy(),
        )

        if not skill_file.exists():
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="File",
                    message=f"SKILL.md not found in {skill_dir.relative_to(self.repo_root)}",
                )
            )
            return result

        content = skill_file.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        result.line_count = len(lines)

        self._validate_frontmatter(content, result)
        self._validate_sections(content, result)
        self._validate_content_requirements(content, result)
        self._validate_jurisdiction_requirements(content, result)
        self._validate_privacy_requirements(content, result)
        self._validate_no_placeholders(content, result)
        self._validate_minimum_length(result)

        return result

    def _validate_frontmatter(
        self, content: str, result: SkillValidationResult
    ) -> None:
        skill_name = result.skill_name

        if not content.startswith("---"):
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Frontmatter",
                    message="Missing YAML frontmatter (should start with ---)",
                )
            )
            return

        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Frontmatter",
                    message="Invalid frontmatter format",
                )
            )
            return

        frontmatter = fm_match.group(1)

        if "name:" not in frontmatter:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Frontmatter",
                    message="Missing 'name' field in frontmatter",
                )
            )
        else:
            name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            if name_match:
                name_value = name_match.group(1).strip()
                result.metadata["name"] = name_value
                if not name_value.startswith("health/"):
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Frontmatter",
                            message=f"Name should start with 'health/': {name_value}",
                            severity="WARNING",
                        )
                    )

        if "description:" not in frontmatter:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Frontmatter",
                    message="Missing 'description' field in frontmatter",
                )
            )
        else:
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
            if desc_match:
                desc_value = desc_match.group(1).strip()
                result.metadata["description"] = desc_value
                if not desc_value.startswith("This skill should be used when"):
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Frontmatter",
                            message="Description should start with 'This skill should be used when'",
                            severity="WARNING",
                        )
                    )

        if "version:" not in frontmatter:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Frontmatter",
                    message="Missing 'version' field in frontmatter",
                )
            )
        else:
            version_match = re.search(r"^version:\s*(.+)$", frontmatter, re.MULTILINE)
            if version_match:
                version_value = version_match.group(1).strip()
                result.metadata["version"] = version_value
                if not re.match(r"^\d+\.\d+\.\d+", version_value):
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Frontmatter",
                            message=f"Version should follow semantic versioning (X.Y.Z): {version_value}",
                            severity="WARNING",
                        )
                    )

    def _validate_sections(self, content: str, result: SkillValidationResult) -> None:
        skill_name = result.skill_name

        section_mappings = {
            r"^##\s+When to Use": "When to Use This Skill",
            r"^##\s+Regulatory Context": "Regulatory Context",
            r"^##\s+Confidence Indicators": "Confidence Indicators",
            r"^##\s+Quick Reference": "Quick Reference",
            r"^##\s+Detailed Guidance": "Detailed Guidance",
            r"^##\s+Documentation Requirements": "Documentation Requirements",
            r"^##\s+Common Mistakes": "Common Mistakes",
            r"^##\s+When to Escalate": "When to Escalate",
            r"^##\s+Privacy Considerations": "Privacy Considerations",
            r"^##\s+(Standard and Lite|Operating) Modes": "Standard and Lite Modes",
            r"^##\s+Tool Requirements": "Tool Requirements",
            r"^##\s+Success Indicators": "Success Indicators",
            r"^##\s+Related Skills": "Related Skills",
        }

        for pattern, section_name in section_mappings.items():
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                result.sections_found.add(section_name)

        for section in self.REQUIRED_SECTIONS:
            if section not in result.sections_found:
                if (
                    section == "Standard and Lite Modes"
                    and "Operating Modes" in result.sections_found
                ):
                    result.sections_found.add(section)
                else:
                    result.errors.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Structure",
                            message=f"Missing required section: {section}",
                        )
                    )

    def _validate_content_requirements(
        self, content: str, result: SkillValidationResult
    ) -> None:
        skill_name = result.skill_name

        if "Common Mistakes" in result.sections_found:
            mistakes_table = re.search(
                r"##\s+Common Mistakes\s*\n.*?\|.*\|.*\|", content, re.DOTALL
            )
            if mistakes_table:
                table_content = mistakes_table.group(0)
                row_count = len(re.findall(r"\n\|", table_content)) - 1
                if row_count < 5:
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Common Mistakes",
                            message=f"Should have at least 5 mistakes documented (found {row_count})",
                            severity="WARNING",
                        )
                    )

        if "Confidence Indicators" in result.sections_found:
            confidence_table = re.search(
                r"##\s+Confidence Indicators\s*\n.*?\|.*\|.*\|", content, re.DOTALL
            )
            if confidence_table:
                table_content = confidence_table.group(0)
                row_count = len(re.findall(r"\n\|", table_content)) - 1
                if row_count < 3:
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Confidence Indicators",
                            message=f"Should have at least 3 scenarios (found {row_count})",
                            severity="WARNING",
                        )
                    )

                if (
                    "High" not in table_content
                    or "Medium" not in table_content
                    or "Low" not in table_content
                ):
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Confidence Indicators",
                            message="Table should include High, Medium, and Low confidence levels",
                            severity="WARNING",
                        )
                    )

        if "Related Skills" in result.sections_found:
            related_skills_section = re.search(
                r"##\s+Related Skills\s*\n(.*?)(?=##|$)", content, re.DOTALL
            )
            if related_skills_section:
                section_content = related_skills_section.group(1)
                skill_refs = re.findall(r"~~\w+/", section_content)
                if len(skill_refs) < 2:
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Related Skills",
                            message=f"Should reference at least 2 related skills (found {len(skill_refs)})",
                            severity="WARNING",
                        )
                    )

        if "Success Indicators" in result.sections_found:
            success_section = re.search(
                r"##\s+Success Indicators\s*\n(.*?)(?=##|$)", content, re.DOTALL
            )
            if success_section:
                section_content = success_section.group(1)
                indicators = re.findall(r"- \[ \]", section_content)
                if len(indicators) < 3:
                    result.warnings.append(
                        ValidationError(
                            skill_name=skill_name,
                            section="Success Indicators",
                            message=f"Should have at least 3 success indicators (found {len(indicators)})",
                            severity="WARNING",
                        )
                    )

        if "Important" not in content and "disclaimer" not in content.lower():
            result.warnings.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Content",
                    message="Should include healthcare disclaimer",
                    severity="WARNING",
                )
            )

    def _validate_jurisdiction_requirements(
        self, content: str, result: SkillValidationResult
    ) -> None:
        skill_name = result.skill_name

        au_nz_patterns = [
            r"Australia.*New Zealand",
            r"AU.*NZ",
            r"AU/NZ",
            r"NSQHS",
            r"ACHS",
            r"HQSC",
        ]
        has_au_nz = any(
            re.search(pattern, content, re.IGNORECASE) for pattern in au_nz_patterns
        )

        if not has_au_nz:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Regulatory Context",
                    message="Missing AU/NZ-default jurisdiction references",
                )
            )

        us_eu_patterns = [
            r"US.*EU",
            r"US/EU",
            r"United States",
            r"European Union",
            r"HIPAA",
            r"Joint Commission",
            r"GDPR",
        ]
        has_us_eu = any(
            re.search(pattern, content, re.IGNORECASE) for pattern in us_eu_patterns
        )

        if not has_us_eu:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Regulatory Context",
                    message="Missing US/EU-lite portability guidance",
                )
            )

        if "Jurisdiction" in content and "Applicable Regulator" in content:
            pass
        else:
            result.warnings.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Regulatory Context",
                    message="Should include jurisdiction matrix table",
                    severity="WARNING",
                )
            )

    def _validate_privacy_requirements(
        self, content: str, result: SkillValidationResult
    ) -> None:
        skill_name = result.skill_name

        if "PHI" not in content and "PII" not in content:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Privacy Considerations",
                    message="Missing PHI/PII references in Privacy Considerations",
                )
            )

        guardrail_patterns = [
            (r"No Logging", "No Logging of PHI guidance"),
            (r"Minimum Necessary", "Minimum necessary data guidance"),
            (r"De-identification", "De-identification guidance"),
        ]

        for pattern, description in guardrail_patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                result.warnings.append(
                    ValidationError(
                        skill_name=skill_name,
                        section="Privacy Considerations",
                        message=f"Missing: {description}",
                        severity="WARNING",
                    )
                )

    def _validate_no_placeholders(
        self, content: str, result: SkillValidationResult
    ) -> None:
        skill_name = result.skill_name

        for pattern in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                result.errors.append(
                    ValidationError(
                        skill_name=skill_name,
                        section="Content",
                        message=f"Placeholder content detected: '{match}'",
                    )
                )

    def _validate_minimum_length(self, result: SkillValidationResult) -> None:
        skill_name = result.skill_name

        if result.line_count < 300:
            result.errors.append(
                ValidationError(
                    skill_name=skill_name,
                    section="Length",
                    message=f"Skill is too short ({result.line_count} lines, minimum 300 required)",
                )
            )


def print_validation_report(results: List[SkillValidationResult]) -> int:
    total_errors = 0
    total_warnings = 0

    print("=" * 80)
    print("HEALTH SKILL VALIDATION REPORT")
    print("=" * 80)
    print()

    for result in results:
        print(f"\n{'=' * 80}")
        print(f"Skill: {result.skill_name}")
        print(f"Path: {result.skill_path.relative_to(result.skill_path.parents[2])}")
        print(f"Lines: {result.line_count}")
        print(f"Sections: {len(result.sections_found)}/12 required")

        if result.missing_sections:
            print(f"Missing: {', '.join(sorted(result.missing_sections))}")

        if result.is_valid and not result.warnings:
            print("Status: PASS")
        elif result.is_valid:
            print("Status: PASS (with warnings)")
        else:
            print("Status: FAIL")

        if result.errors:
            print("\n  ERRORS:")
            for error in result.errors:
                print(f"    [{error.section}] {error.message}")
            total_errors += len(result.errors)

        if result.warnings:
            print("\n  WARNINGS:")
            for warning in result.warnings:
                print(f"    [{warning.section}] {warning.message}")
            total_warnings += len(result.warnings)

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Skills validated: {len(results)}")
    print(f"Passed: {sum(1 for r in results if r.is_valid)}/{len(results)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    print()

    if total_errors == 0:
        print("All validations passed!")
        return 0
    else:
        print(f"Validation failed with {total_errors} errors.")
        return 1


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]

    if len(sys.argv) > 1:
        skill_path = Path(sys.argv[1])
        if not skill_path.is_absolute():
            skill_path = repo_root / skill_path

        if not skill_path.exists():
            print(f"ERROR: Skill path not found: {skill_path}")
            return 1

        validator = HealthSkillValidator(repo_root)

        if skill_path.is_dir():
            result = validator.validate_skill(skill_path)
        else:
            result = validator.validate_skill(skill_path.parent)

        return print_validation_report([result])
    else:
        validator = HealthSkillValidator(repo_root)
        results = validator.validate_all_skills()

        if not results:
            print("No health skills found to validate.")
            return 0

        return print_validation_report(results)


if __name__ == "__main__":
    sys.exit(main())
