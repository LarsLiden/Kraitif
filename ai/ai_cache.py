"""
AI Response Cache Module

Provides disk-based caching for AI responses to speed up development and reduce API calls.
Uses SHA-256 hashing of prompts to create cache keys.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class AIResponseCache:
    """Manages disk-based caching of AI responses."""

    def __init__(self, cache_dir: str = "data/ai_cache"):
        """
        Initialize the AI response cache.

        Args:
            cache_dir: Directory to store cache files (default: data/ai_cache)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _hash_prompt(self, prompt: str) -> str:
        """
        Create a SHA-256 hash of the prompt for use as cache key.

        Args:
            prompt: The prompt text to hash

        Returns:
            Hexadecimal string representation of the hash
        """
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def _get_cache_path(self, prompt_hash: str) -> Path:
        """
        Get the file path for a cached response.

        Args:
            prompt_hash: The hash of the prompt

        Returns:
            Path object for the cache file
        """
        return self.cache_dir / f"{prompt_hash}.json"

    def get(self, prompt: str) -> Optional[str]:
        """
        Retrieve a cached response for the given prompt.

        Args:
            prompt: The prompt text to look up

        Returns:
            Cached response string if found, None otherwise
        """
        prompt_hash = self._hash_prompt(prompt)
        cache_path = self._get_cache_path(prompt_hash)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Return the cached response
            return cache_data.get("response")

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to read cache file {cache_path}: {e}")
            return None

    def set(self, prompt: str, response: str) -> None:
        """
        Store a response in the cache.

        Args:
            prompt: The prompt text (will be hashed for the key)
            response: The AI response to cache
        """
        prompt_hash = self._hash_prompt(prompt)
        cache_path = self._get_cache_path(prompt_hash)

        cache_data = {
            "prompt_hash": prompt_hash,
            "prompt": prompt,  # Store full prompt for debugging
            "response": response,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

        except IOError as e:
            print(f"Warning: Failed to write cache file {cache_path}: {e}")

    def clear(self) -> int:
        """
        Clear all cached responses.

        Returns:
            Number of cache files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except OSError:
                pass
        return count

    def stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats (count, total_size_bytes)
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files if f.exists())

        return {
            "count": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_dir": str(self.cache_dir.absolute()),
        }


# Global cache instance
_cache = None


def get_cache() -> AIResponseCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = AIResponseCache()
    return _cache
