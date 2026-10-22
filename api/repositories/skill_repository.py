
import re
from functools import lru_cache

from api.skills_database import SKILLS


# Compile skill patterns once instead of rebuilding them
# for every job description.
SKILL_PATTERNS = []

for skill, keywords in SKILLS.items():
    patterns = []

    for keyword in keywords:
        normalized_keyword = keyword.lower().strip()

        if not normalized_keyword:
            continue

        pattern = re.compile(
            r"(?<!\w)"
            + re.escape(normalized_keyword)
            + r"(?!\w)"
        )

        patterns.append(pattern)

    if patterns:
        SKILL_PATTERNS.append((skill, patterns))


@lru_cache(maxsize=4096)
def _extract_skills_cached(text: str) -> tuple[str, ...]:
    """
    Extract skills from normalized text and cache the result.
    """
    extracted_skills = set()

    for skill, patterns in SKILL_PATTERNS:
        for pattern in patterns:
            if pattern.search(text):
                extracted_skills.add(skill)
                break

    return tuple(sorted(extracted_skills))


def extract_skills(text: str) -> list[str]:
    """
    Extract normalized skills from resume or job-description text.
    Uses compiled regex patterns and caching for performance.
    """
    normalized_text = (text or "").lower()

    if not normalized_text:
        return []

    return list(_extract_skills_cached(normalized_text))
