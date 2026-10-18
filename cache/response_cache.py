import re
import time


# ============================================================
# IN-MEMORY RESPONSE CACHE
# ============================================================

class ResponseCache:

    def __init__(self):
        self.cache = {}

    # --------------------------------------------------------
    # NORMALIZE QUERY
    # --------------------------------------------------------

    @staticmethod
    def normalize_query(query: str) -> str:

        query = query.lower().strip()

        # Remove extra whitespace
        query = re.sub(
            r"\s+",
            " ",
            query,
        )

        # Remove common punctuation
        query = re.sub(
            r"[?.!,]+$",
            "",
            query,
        )

        return query

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def get(self, query: str):

        key = self.normalize_query(query)

        if key in self.cache:

            entry = self.cache[key]

            return {
                "hit": True,
                "key": key,
                "response": entry["response"],
                "cached_at": entry["cached_at"],
            }

        return {
            "hit": False,
            "key": key,
            "response": None,
            "cached_at": None,
        }

    # --------------------------------------------------------
    # SET
    # --------------------------------------------------------

    def set(
        self,
        query: str,
        response: dict,
    ):

        key = self.normalize_query(query)

        self.cache[key] = {
            "response": response,
            "cached_at": time.time(),
        }

    # --------------------------------------------------------
    # SIZE
    # --------------------------------------------------------

    def size(self) -> int:

        return len(self.cache)


# ============================================================
# DEMONSTRATION
# ============================================================

if __name__ == "__main__":

    cache = ResponseCache()

    query = "What is the notice period policy?"

    response = {
        "status": "success",
        "response": (
            "The standard notice period is 30 days."
        ),
        "source": "Naukri Knowledge Base",
    }

    print("=" * 70)
    print("NAUKRI RESPONSE CACHE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # BEFORE CACHE
    # --------------------------------------------------------

    print("\nBEFORE CACHING")

    before = cache.get(query)

    print("Cache hit:", before["hit"])
    print("Cache size:", cache.size())

    # --------------------------------------------------------
    # STORE RESPONSE
    # --------------------------------------------------------

    cache.set(
        query,
        response,
    )

    print("\nAFTER STORING RESPONSE")

    print("Cache size:", cache.size())

    # --------------------------------------------------------
    # SECOND REQUEST
    # --------------------------------------------------------

    second_query = "  WHAT IS THE NOTICE PERIOD POLICY?  "

    print("\nSECOND REQUEST")

    print("Original query:", second_query)

    after = cache.get(second_query)

    print("Normalized key:", after["key"])
    print("Cache hit:", after["hit"])
    print("Cached response:", after["response"])

    # --------------------------------------------------------
    # FINAL EVIDENCE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CACHE EVIDENCE")
    print("=" * 70)

    print("Before cache hit :", before["hit"])
    print("After cache hit  :", after["hit"])
    print("Cache size       :", cache.size())

    if not before["hit"] and after["hit"]:

        print("\nCACHE TEST: PASS")

    else:

        print("\nCACHE TEST: REVIEW REQUIRED")