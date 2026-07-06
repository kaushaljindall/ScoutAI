"""Merge engine — combines results from multiple providers into a unified list."""
from typing import List
from loguru import logger

from app.providers.base.base_provider import DiscoveredBusiness


def merge_results(all_results: List[List[DiscoveredBusiness]]) -> List[DiscoveredBusiness]:
    """
    Merge results from multiple providers.
    Phase 5B: No deduplication yet — preserve all results with source metadata.
    Deduplication is Phase 5C.
    """
    merged: List[DiscoveredBusiness] = []
    for provider_results in all_results:
        merged.extend(provider_results)

    # Sort by provider_confidence descending
    merged.sort(key=lambda b: b.provider_confidence, reverse=True)
    logger.info(f"[merge] Merged {len(merged)} total results from {len(all_results)} providers")
    return merged
