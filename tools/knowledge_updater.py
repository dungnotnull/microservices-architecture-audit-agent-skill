#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_updater.py — Self-improving knowledge crawler for the Microservices / Distributed System Architecture Audit skill.

Pipeline:
  1. Fetch latest papers/docs from domain sources (ArXiv, official docs)
  2. Parse into structured entries (title, authors, date, DOI/URL, abstract, key findings)
  3. Score entries by recency × domain-keyword relevance
  4. Deduplicate entries by URL/DOI hash
  5. Append scored entries to SECOND-KNOWLEDGE-BRAIN.md
  6. Generate update summary statistics

Run weekly via cron or scheduled task.
Requires: pip install crawl4ai requests beautifulsoup4

Usage:
    python knowledge_updater.py [--force] [--dry-run] [--sources <comma_separated_list>]

Options:
    --force: Force update even if last update was < 7 days ago
    --dry-run: Fetch and process but don't write to file
    --sources: Comma-separated list of specific sources to crawl (default: all)

Copyright (c) 2026 Microservices Architecture Audit Skill
Licensed under MIT License
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, List, Optional, Set, Tuple, TypeAlias
from urllib.parse import urlparse

# Optional dependencies - fail gracefully if not installed
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_FETCH_AVAILABLE = True
except ImportError:
    WEB_FETCH_AVAILABLE = False
    print("[warn] requests/BeautifulSoup4 not available - limited functionality")

try:
    from crawl4ai import WebCrawler
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False
    print("[warn] crawl4ai not installed - falling back to requests+BeautifulSoup")

# =============================================================================
# Configuration
# =============================================================================

SKILL_ID = 93
SKILL_SLUG = "microservices-architecture-audit"
SCRIPT_DIR = Path(__file__).parent.parent
BRAIN_FILE = SCRIPT_DIR / "SECOND-KNOWLEDGE-BRAIN.md"
LOG_DIR = SCRIPT_DIR / "logs"
STATE_FILE = SCRIPT_DIR / ".knowledge_updater_state.json"

# Domain keywords for relevance scoring
DOMAIN_KEYWORDS: Tuple[str, ...] = (
    "microservices",
    "distributed systems",
    "resilience patterns",
    "circuit breaker",
    "fault tolerance",
    "observability",
    "service mesh",
    "scalability",
    "elasticity",
    "data consistency",
    "CAP theorem",
    "PACELC",
    "eventual consistency",
    "saga pattern",
    "distributed tracing",
    "open telemetry",
    "SLO",
    "SLI",
    "error budget",
    "site reliability engineering",
    "twelve-factor app",
    "cloud-native",
    "chaos engineering",
    "bulkhead pattern",
    "rate limiting",
    "backpressure",
    "service discovery",
    "API gateway",
    "event sourcing",
    "CQRS",
    "sharding",
    "replication",
    "high availability",
    "disaster recovery",
)

# ArXiv categories to crawl
ARXIV_CATEGORIES: Tuple[str, ...] = (
    "cs.DC",  # Distributed, Parallel, and Cluster Computing
    "cs.SE",  # Software Engineering
    "cs.CR",  # Cryptography and Security
    "cs.DS",  # Data Structures and Algorithms
)

# Search queries for web search
SEARCH_QUERIES: Tuple[str, ...] = (
    "microservices resilience patterns 2026",
    "distributed systems observability",
    "service mesh scalability",
    "fault tolerance microservices",
    "eventual consistency patterns",
)

# Primary sources to crawl
SOURCE_URLS: Tuple[str, ...] = (
    "https://aws.amazon.com/architecture/well-architected/",
    "https://sre.google/books/",
    "https://opentelemetry.io",
    "https://microservices.io",
    "https://www.cloudflare.com/learning/",
    "https://martinfowler.com/articles/microservices.html",
    "https://www.nginx.com/blog/microservices-reference-architecture/",
)

# Relevance score thresholds
MIN_RELEVANCE_SCORE = 0.3
MAX_ENTRIES_PER_RUN = 50


# =============================================================================
# Data Structures
# =============================================================================

class SourceType(Enum):
    """Type of source for an entry."""
    ARXIV = "arxiv"
    WEB_DOCUMENTATION = "web_documentation"
    BLOG = "blog"
    PAPER = "paper"
    NEWS = "news"


@dataclass
class KnowledgeEntry:
    """Structured knowledge entry."""
    title: str
    url: str
    authors: str
    year: int
    abstract: str
    source_type: SourceType
    venue: str = ""
    doi: str = ""
    relevance_score: float = 0.0
    date_added: date = field(default_factory=date.today)

    def to_markdown(self) -> str:
        """Convert entry to markdown format for BRAIN file."""
        today = self.date_added.isoformat()
        hash_val = self._get_hash()
        return (
            f"### [{self.date_added.isoformat()}] {self.title}\n"
            f"- Authors: {self.authors}\n"
            f"- Year: {self.year}\n"
            f"- Venue: {self.venue}\n"
            f"- Link: {self.url}\n"
            f"- DOI: {self.doi}\n"
            f"- Relevance score: {self.relevance_score:.3f}\n"
            f"- Key findings: {(self.abstract or '(abstract pending)')[:500]}\n"
            f"<!--hash:{hash_val}-->\n"
        )

    def _get_hash(self) -> str:
        """Generate hash for deduplication."""
        content = self.url + self.doi
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    def is_valid(self) -> bool:
        """Check if entry has minimum required fields."""
        return bool(self.title and self.url and self.year)


@dataclass
class UpdateState:
    """Persistent state for the knowledge updater."""
    last_update: str = ""
    last_successful_update: str = ""
    total_entries_added: int = 0
    update_history: List[dict] = field(default_factory=list)

    @classmethod
    def load(cls) -> "UpdateState":
        """Load state from file."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"[warn] Failed to load state file: {e}")
        return cls()

    def save(self) -> None:
        """Save state to file."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "last_update": self.last_update,
                "last_successful_update": self.last_successful_update,
                "total_entries_added": self.total_entries_added,
                "update_history": self.update_history[-10:],  # Keep last 10 updates
            }, f, indent=2)


# =============================================================================
# Core Functions
# =============================================================================

def load_seen_hashes() -> Set[str]:
    """Load previously seen URL/DOI hashes from BRAIN file."""
    if not BRAIN_FILE.exists():
        return set()

    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all hash comments
    return set(re.findall(r"<!--hash:([0-9a-f]{16})-->", content))


def relevance_score(entry: KnowledgeEntry) -> float:
    """Calculate relevance score: recency (0-1) × keyword-match (0-1)."""
    if not entry.year:
        return 0.0

    current_year = date.today().year
    # Recency: linear decay over 8 years, floor at 0.3 for older papers
    years_old = current_year - entry.year
    recency = max(0.3, 1.0 - (years_old / 8.0))

    # Keyword match: count domain keywords in title + abstract
    text = (entry.title + " " + entry.abstract).lower()
    keyword_hits = sum(1 for kw in DOMAIN_KEYWORDS if kw.lower() in text)
    keyword_score = min(1.0, keyword_hits / max(1, len(DOMAIN_KEYWORDS) * 0.1))

    # Combined score (weighted toward keyword match for domain relevance)
    return round(recency * 0.4 + keyword_score * 0.6, 3)


def fetch_arxiv_papers() -> List[KnowledgeEntry]:
    """Fetch recent papers from ArXiv categories."""
    entries: List[KnowledgeEntry] = []

    if not WEB_FETCH_AVAILABLE:
        print("[warn] Web fetch not available - skipping ArXiv")
        return entries

    for category in ARXIV_CATEGORIES:
        try:
            # Use ArXiv API
            url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
                link_elem = entry.find("{http://www.w3.org/2005/Atom}id")
                summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
                published_elem = entry.find("{http://www.w3.org/2005/Atom}published")
                authors = entry.findall("{http://www.w3.org/2005/Atom}author")

                if title_elem is None or link_elem is None:
                    continue

                title = title_elem.text.strip().replace("\n", " ")
                url = link_elem.text
                abstract = summary_elem.text.strip() if summary_elem is not None else ""

                # Extract year from published date
                year = date.today().year
                if published_elem is not None and published_elem.text:
                    try:
                        published = datetime.fromisoformat(published_elem.text.replace("Z", "+00:00"))
                        year = published.year
                    except ValueError:
                        pass

                author_list = ", ".join([
                    a.find("{http://www.w3.org/2005/Atom}name").text
                    for a in authors if a.find("{http://www.w3.org/2005/Atom}name") is not None
                ])

                entry = KnowledgeEntry(
                    title=title,
                    url=url,
                    authors=author_list,
                    year=year,
                    abstract=abstract[:500],
                    source_type=SourceType.ARXIV,
                    venue=f"arXiv {category}",
                )
                entry.relevance_score = relevance_score(entry)

                if entry.is_valid() and entry.relevance_score >= MIN_RELEVANCE_SCORE:
                    entries.append(entry)

        except Exception as e:
            print(f"[warn] Failed to fetch arXiv {category}: {e}")

    return entries


def fetch_web_documentation() -> List[KnowledgeEntry]:
    """Fetch documentation from primary sources."""
    entries: List[KnowledgeEntry] = []

    for source_url in SOURCE_URLS:
        try:
            if CRAWL4AI_AVAILABLE:
                crawler = WebCrawler()
                crawler.warmup()
                result = crawler.run(url=source_url)
                content = getattr(result, "markdown", "")
            elif WEB_FETCH_AVAILABLE:
                response = requests.get(source_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                content = soup.get_text()[:2000]
            else:
                continue

            # Create entry for the source
            domain = urlparse(source_url).netloc.replace("www.", "")
            entry = KnowledgeEntry(
                title=f"Documentation update: {domain}",
                url=source_url,
                authors=domain,
                year=date.today().year,
                abstract=content[:500],
                source_type=SourceType.WEB_DOCUMENTATION,
                venue=domain,
            )
            entry.relevance_score = relevance_score(entry)

            if entry.is_valid() and entry.relevance_score >= MIN_RELEVANCE_SCORE:
                entries.append(entry)

        except Exception as e:
            print(f"[warn] Failed to fetch {source_url}: {e}")

    return entries


def append_entries_to_brain(entries: List[KnowledgeEntry], dry_run: bool = False) -> None:
    """Append new entries to the BRAIN file."""
    if not entries:
        print("[info] No new entries to append")
        return

    seen_hashes = load_seen_hashes()
    new_entries: List[KnowledgeEntry] = []

    for entry in entries:
        entry_hash = entry._get_hash()
        if entry_hash not in seen_hashes:
            seen_hashes.add(entry_hash)
            new_entries.append(entry)

    if not new_entries:
        print("[info] All entries already exist in BRAIN file")
        return

    # Sort by relevance score
    new_entries.sort(key=lambda e: e.relevance_score, reverse=True)

    # Prepare markdown content
    today = date.today().isoformat()
    markdown_blocks = [f"\n\n## Automated Crawl Batch — {today}\n\n"]
    markdown_blocks.extend(e.to_markdown() for e in new_entries[:MAX_ENTRIES_PER_RUN])

    if dry_run:
        print(f"[dry-run] Would append {len(new_entries)} entries:")
        for block in markdown_blocks:
            print(block[:200])
        return

    # Append to BRAIN file
    BRAIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BRAIN_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(markdown_blocks))

    print(f"[success] Appended {len(new_entries)} entries to {BRAIN_FILE}")


def generate_update_summary(entries: List[KnowledgeEntry]) -> str:
    """Generate summary statistics for the update."""
    if not entries:
        return "No entries fetched"

    summary = {
        "total_entries": len(entries),
        "by_source": {},
        "avg_relevance": sum(e.relevance_score for e in entries) / len(entries),
        "top_entries": [
            {"title": e.title, "score": e.relevance_score, "url": e.url}
            for e in sorted(entries, key=lambda x: x.relevance_score, reverse=True)[:5]
        ],
    }

    for entry in entries:
        source = entry.source_type.value
        summary["by_source"][source] = summary["by_source"].get(source, 0) + 1

    return json.dumps(summary, indent=2)


def should_update(force: bool = False) -> bool:
    """Check if an update is needed (at least 7 days since last update)."""
    if force:
        return True

    state = UpdateState.load()
    if not state.last_update:
        return True

    try:
        last_update = datetime.fromisoformat(state.last_update)
        days_since = (datetime.now() - last_update).days
        return days_since >= 7
    except ValueError:
        return True


def main() -> int:
    """Main entry point for the knowledge updater."""
    parser = argparse.ArgumentParser(
        description="Update knowledge base for Microservices Architecture Audit skill"
    )
    parser.add_argument("--force", action="store_true", help="Force update even if < 7 days")
    parser.add_argument("--dry-run", action="store_true", help="Fetch but don't write")
    parser.add_argument("--sources", help="Comma-separated list of sources to crawl")
    args = parser.parse_args()

    print(f"[knowledge_updater] Skill #{SKILL_ID} ({SKILL_SLUG})")
    print(f"[info] BRAIN file: {BRAIN_FILE}")

    # Check if update is needed
    if not should_update(args.force):
        last_update = UpdateState.load().last_update
        print(f"[info] Last update was {last_update}, skipping (use --force to override)")
        return 0

    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Update start time
    state = UpdateState.load()
    state.last_update = datetime.now().isoformat()
    state.save()

    try:
        # Fetch entries
        print("[info] Fetching ArXiv papers...")
        arxiv_entries = fetch_arxiv_papers()
        print(f"[info] Found {len(arxiv_entries)} ArXiv entries")

        print("[info] Fetching web documentation...")
        web_entries = fetch_web_documentation()
        print(f"[info] Found {len(web_entries)} web entries")

        all_entries = arxiv_entries + web_entries
        print(f"[info] Total entries fetched: {len(all_entries)}")

        # Append to BRAIN
        append_entries_to_brain(all_entries, args.dry_run)

        # Update state on success
        if not args.dry_run:
            state.last_successful_update = datetime.now().isoformat()
            state.total_entries_added += len(all_entries)
            state.update_history.append({
                "timestamp": datetime.now().isoformat(),
                "entries_added": len(all_entries),
                "sources": {
                    "arxiv": len(arxiv_entries),
                    "web": len(web_entries),
                },
            })
            state.save()

        # Generate summary
        summary = generate_update_summary(all_entries)
        print(f"[summary] {summary}")

        return 0

    except Exception as e:
        print(f"[error] Update failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
