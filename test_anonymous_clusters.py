#!/usr/bin/env python3
"""
Test script to verify the anonymous cluster saving functionality.
This test verifies that the fix for numpy serialization works correctly.
"""

import sys
import os
import json
import numpy as np

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice import database

def test_anonymous_cluster_creation_and_saving():
    """Test that anonymous clusters are created and saved to disk correctly."""
    print("🧪 Testing anonymous cluster creation and saving...")
    
    # Reset the database file
    reset_database()
    
    # Load empty database
    database.load_known_users()
    
    # Create a test anonymous cluster
    test_embedding = np.random.rand(128).astype(np.float32)
    cluster_id = database.create_anonymous_cluster(test_embedding)
    
    assert cluster_id is not None, "Cluster creation should return a cluster ID"
    assert cluster_id.startswith("Anonymous_"), "Cluster ID should start with 'Anonymous_'"
    
    # Verify it's saved to disk
    with open('voice_profiles/known_users_v2.json', 'r') as f:
        data = json.load(f)
    
    assert len(data['anonymous_clusters']) == 1, "Should have 1 anonymous cluster saved"
    assert cluster_id in data['anonymous_clusters'], f"Cluster {cluster_id} should be in saved data"
    
    # Test linking to named user
    result = database.link_anonymous_to_named(cluster_id, 'TestUser')
    assert result is True, "Linking should succeed"
    
    # Verify linking worked
    with open('voice_profiles/known_users_v2.json', 'r') as f:
        data = json.load(f)
    
    assert len(data['known_users']) == 1, "Should have 1 known user after linking"
    assert 'TestUser' in data['known_users'], "TestUser should be in known users"
    assert len(data['anonymous_clusters']) == 0, "Anonymous cluster should be removed after linking"
    
    print("✅ All tests passed!")

def reset_database():
    """Reset the database to empty state."""
    empty_db = {
        'known_users': {},
        'anonymous_clusters': {},
        'false_positives': [],
        'last_updated': '2025-07-13T02:41:44.513648',
        'version': '2.1_enhanced_protection'
    }
    
    with open('voice_profiles/known_users_v2.json', 'w') as f:
        json.dump(empty_db, f, indent=2)

if __name__ == "__main__":
    test_anonymous_cluster_creation_and_saving()
    print("🎉 Anonymous cluster functionality test completed successfully!")