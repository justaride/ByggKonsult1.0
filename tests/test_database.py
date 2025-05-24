#!/usr/bin/env python3
"""
Test suite for Oslo Planning Premium database functionality
"""

import pytest
import tempfile
import os
from oslo_planning_premium import OsloPlanningPremium


class TestOsloPlanningDatabase:
    """Test cases for the Oslo Planning Premium database"""
    
    def setup_method(self):
        """Set up test database with temporary file"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.system = OsloPlanningPremium(self.temp_db.name)
    
    def teardown_method(self):
        """Clean up test database"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test that database initializes correctly"""
        docs = self.system.get_all_documents()
        categories = self.system.get_categories()
        
        # Basic assertions
        assert len(docs) > 0, "Database should contain documents"
        assert len(categories) > 0, "Database should contain categories"
        
        # Check for required columns
        required_doc_columns = ['title', 'category', 'status', 'url', 'description']
        for col in required_doc_columns:
            assert col in docs.columns, f"Missing required column: {col}"
        
        required_cat_columns = ['category_name', 'icon', 'description']
        for col in required_cat_columns:
            assert col in categories.columns, f"Missing required column: {col}"
    
    def test_no_duplicates(self):
        """Test that there are no duplicate documents"""
        docs = self.system.get_all_documents()
        
        # Check for duplicate titles
        duplicate_titles = docs['title'].duplicated().sum()
        assert duplicate_titles == 0, f"Found {duplicate_titles} duplicate titles"
        
        # Check for unique document hashes
        unique_hashes = docs['document_hash'].nunique()
        assert unique_hashes == len(docs), "Document hashes should be unique"
    
    def test_url_format(self):
        """Test that all URLs are properly formatted"""
        docs = self.system.get_all_documents()
        
        # Check that all URLs are present
        missing_urls = docs['url'].isna().sum()
        assert missing_urls == 0, f"Found {missing_urls} documents without URLs"
        
        # Check URL format
        for _, doc in docs.iterrows():
            url = doc['url']
            assert url.startswith('https://oslo.kommune.no'), f"Invalid URL format: {url}"
    
    def test_category_coverage(self):
        """Test that all categories are properly covered"""
        docs = self.system.get_all_documents()
        categories = self.system.get_categories()
        
        # Get unique categories from documents
        doc_categories = set(docs['category'].unique())
        cat_names = set(categories['category_name'].unique())
        
        # Check that all document categories exist in categories table
        missing_categories = doc_categories - cat_names
        assert len(missing_categories) == 0, f"Missing categories: {missing_categories}"
    
    def test_data_quality(self):
        """Test data quality metrics"""
        docs = self.system.get_all_documents()
        
        # Check title quality
        short_titles = docs[docs['title'].str.len() < 10]
        assert len(short_titles) == 0, "All titles should be descriptive (>10 chars)"
        
        # Check description quality
        short_descriptions = docs[docs['description'].str.len() < 20]
        assert len(short_descriptions) == 0, "All descriptions should be informative (>20 chars)"
        
        # Check department assignment
        missing_departments = docs['responsible_department'].isna().sum()
        assert missing_departments == 0, "All documents should have assigned departments"
    
    def test_search_functionality(self):
        """Test search functionality"""
        # Test basic search
        results = self.system.search_documents("kommuneplan")
        assert len(results) > 0, "Search should return results for 'kommuneplan'"
        
        # Verify search results contain the search term
        found_term = False
        for _, doc in results.iterrows():
            if "kommuneplan" in doc['title'].lower() or "kommuneplan" in doc['description'].lower():
                found_term = True
                break
        assert found_term, "Search results should contain the search term"
        
        # Test empty search
        empty_results = self.system.search_documents("nonexistent_term_12345")
        assert len(empty_results) == 0, "Search for non-existent term should return empty results"
    
    def test_category_filtering(self):
        """Test category-based document filtering"""
        categories = self.system.get_categories()
        
        # Test filtering by each category
        for _, category in categories.iterrows():
            cat_name = category['category_name']
            filtered_docs = self.system.get_documents_by_category(cat_name)
            
            # Check that all returned documents belong to the category
            for _, doc in filtered_docs.iterrows():
                assert doc['category'] == cat_name, f"Document {doc['title']} should be in category {cat_name}"
    
    def test_document_priorities(self):
        """Test document priority assignment"""
        docs = self.system.get_all_documents()
        
        # Check priority range
        priorities = docs['priority'].unique()
        valid_priorities = {1, 2, 3}
        invalid_priorities = set(priorities) - valid_priorities
        assert len(invalid_priorities) == 0, f"Invalid priorities found: {invalid_priorities}"
        
        # Check that high priority documents exist
        high_priority = docs[docs['priority'] >= 3]
        assert len(high_priority) > 0, "Should have high priority documents"
    
    def test_status_values(self):
        """Test document status values"""
        docs = self.system.get_all_documents()
        
        # Check valid status values
        valid_statuses = {'Vedtatt', 'Under behandling', 'Under revisjon', 'Høring'}
        doc_statuses = set(docs['status'].unique())
        invalid_statuses = doc_statuses - valid_statuses
        assert len(invalid_statuses) == 0, f"Invalid statuses found: {invalid_statuses}"
    
    def test_date_formats(self):
        """Test date format consistency"""
        docs = self.system.get_all_documents()
        
        # Check date format (YYYY-MM-DD)
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        
        for _, doc in docs.iterrows():
            if doc['date_published']:
                assert re.match(date_pattern, doc['date_published']), f"Invalid date format: {doc['date_published']}"


class TestSystemIntegration:
    """Integration tests for the complete system"""
    
    def test_system_memory_usage(self):
        """Test system memory usage with in-memory database"""
        # Use in-memory database for speed
        system = OsloPlanningPremium(":memory:")
        
        # Test multiple operations
        docs = system.get_all_documents()
        categories = system.get_categories()
        search_results = system.search_documents("oslo")
        filtered_docs = system.get_documents_by_category(categories.iloc[0]['category_name'])
        
        # Basic assertions to ensure operations work
        assert len(docs) > 0
        assert len(categories) > 0
        assert isinstance(search_results, type(docs))
        assert isinstance(filtered_docs, type(docs))
    
    def test_concurrent_access(self):
        """Test concurrent database access"""
        import threading
        import time
        
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            # Create initial database
            system1 = OsloPlanningPremium(temp_db.name)
            
            results = []
            
            def read_database():
                system = OsloPlanningPremium(temp_db.name)
                docs = system.get_all_documents()
                results.append(len(docs))
            
            # Start multiple threads
            threads = []
            for _ in range(3):
                thread = threading.Thread(target=read_database)
                threads.append(thread)
                thread.start()
            
            # Wait for completion
            for thread in threads:
                thread.join()
            
            # Check results
            assert len(results) == 3, "All threads should complete"
            assert all(r > 0 for r in results), "All threads should get data"
            
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])