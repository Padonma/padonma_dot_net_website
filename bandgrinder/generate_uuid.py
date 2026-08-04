# Generated via Clauda 2025-09-01

import uuid


def generate_random_uuid():
    """Generate a random UUID4."""
    return str(uuid.uuid4())

def generate_multiple_uuids(count=1):
    """Generate multiple random UUIDs."""
    return [str(uuid.uuid4()) for _ in range(count)]

if __name__ == "__main__":
    # Generate a single UUID
    random_uuid = generate_random_uuid()
    print(f"Random UUID: {random_uuid}")
    
    # Generate multiple UUIDs
    print("\nGenerating 5 random UUIDs:")
    multiple_uuids = generate_multiple_uuids(5)
    for i, uid in enumerate(multiple_uuids, 1):
        print(f"{i}. {uid}")
    
    # Different UUID formats
    print(f"\nDifferent formats:")
    base_uuid = uuid.uuid4()
    print(f"Standard: {base_uuid}")
    print(f"Uppercase: {str(base_uuid).upper()}")
    print(f"No hyphens: {str(base_uuid).replace('-', '')}")
    print(f"Hex only: {base_uuid.hex}")
