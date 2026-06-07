"""Test token-based matching in GeoData.get_candidates()"""

from glatteisgeoparser.geodata import GeoData


def test_token_similarity():
    """Test the _token_similarity method directly"""
    geo = GeoData()

    # Test case 1: Exact subset match
    assert geo._token_similarity("den usa", "usa", min_overlap=0.8) == True
    print("✓ Test 1 passed: 'den usa' matches 'usa' (subset)")

    # Test case 2: Exact subset match (reversed order)
    assert geo._token_similarity("new york city", "new york", min_overlap=0.8) == True
    print("✓ Test 2 passed: 'new york city' matches 'new york'")

    # Test case 3: Partial overlap with default threshold (80%)
    assert (
        geo._token_similarity("san francisco ca", "san francisco", min_overlap=0.8)
        == True
    )
    print("✓ Test 3 passed: 'san francisco ca' matches 'san francisco'")

    # Test case 4: No match - different tokens
    assert geo._token_similarity("paris", "london", min_overlap=0.8) == False
    print("✓ Test 4 passed: 'paris' does NOT match 'london'")

    # Test case 5: Partial overlap requiring 50% match
    assert geo._token_similarity("london england", "london", min_overlap=0.5) == True
    print("✓ Test 5 passed: 'london england' matches 'london' with 50% threshold")

    # Test case 6: Single token match
    assert geo._token_similarity("texas", "texas", min_overlap=0.8) == True
    print("✓ Test 6 passed: 'texas' matches 'texas' (exact)")

    # Test case 7: Empty strings
    assert geo._token_similarity("", "", min_overlap=0.8) == True
    print("✓ Test 7 passed: empty strings match")

    # Test case 8: Word order doesn't matter for subset check
    assert geo._token_similarity("york new", "new york", min_overlap=0.8) == True
    print("✓ Test 8 passed: word order doesn't matter for subset tokens")

    print("\nAll token similarity tests passed! ✨")


if __name__ == "__main__":
    test_token_similarity()
