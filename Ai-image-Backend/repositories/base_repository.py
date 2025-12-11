"""
Base repository with common CRUD operations
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from bson import ObjectId


class BaseRepository(ABC):
    """Abstract base repository class"""
    
    def __init__(self, collection):
        """
        Initialize repository with MongoDB collection
        
        Args:
            collection: pymongo collection instance
        """
        self.collection = collection
    
    @abstractmethod
    def get_collection_name(self) -> str:
        """Get the collection name"""
        pass
    
    def find_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Find document by ID
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document dict or None if not found
        """
        try:
            return self.collection.find_one({"_id": ObjectId(doc_id)})
        except Exception as e:
            print(f"Error finding document by ID: {e}")
            return None
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find single document matching query
        
        Args:
            query: MongoDB query dict
            
        Returns:
            Document dict or None if not found
        """
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(f"Error finding document: {e}")
            return None
    
    def find_many(
        self,
        query: Dict[str, Any],
        skip: int = 0,
        limit: int = 50,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents matching query
        
        Args:
            query: MongoDB query dict
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort: List of (field, direction) tuples for sorting
            
        Returns:
            List of document dicts
        """
        try:
            cursor = self.collection.find(query)
            
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            return list(cursor)
        except Exception as e:
            print(f"Error finding documents: {e}")
            return []
    
    def count(self, query: Dict[str, Any]) -> int:
        """
        Count documents matching query
        
        Args:
            query: MongoDB query dict
            
        Returns:
            Number of matching documents
        """
        try:
            return self.collection.count_documents(query)
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0
    
    def insert_one(self, document: Dict[str, Any]) -> Optional[str]:
        """
        Insert single document
        
        Args:
            document: Document dict to insert
            
        Returns:
            Inserted document ID as string, or None if failed
        """
        try:
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting document: {e}")
            return None
    
    def update_one(
        self,
        query: Dict[str, Any],
        update: Dict[str, Any]
    ) -> bool:
        """
        Update single document
        
        Args:
            query: MongoDB query dict to find document
            update: Update operations dict
            
        Returns:
            True if updated, False otherwise
        """
        try:
            result = self.collection.update_one(query, update)
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def update_by_id(
        self,
        doc_id: str,
        update: Dict[str, Any]
    ) -> bool:
        """
        Update document by ID
        
        Args:
            doc_id: Document ID
            update: Update operations dict
            
        Returns:
            True if updated, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(doc_id)},
                update
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating document by ID: {e}")
            return False
    
    def delete_one(self, query: Dict[str, Any]) -> bool:
        """
        Delete single document
        
        Args:
            query: MongoDB query dict to find document
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def delete_by_id(self, doc_id: str) -> bool:
        """
        Delete document by ID
        
        Args:
            doc_id: Document ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document by ID: {e}")
            return False
    
    def delete_many(self, query: Dict[str, Any]) -> int:
        """
        Delete multiple documents
        
        Args:
            query: MongoDB query dict to find documents
            
        Returns:
            Number of documents deleted
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0
    
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Run aggregation pipeline
        
        Args:
            pipeline: MongoDB aggregation pipeline
            
        Returns:
            List of aggregation results
        """
        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error running aggregation: {e}")
            return []
    
    def distinct(self, field: str, query: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Get distinct values for a field
        
        Args:
            field: Field name
            query: Optional query to filter documents
            
        Returns:
            List of distinct values
        """
        try:
            if query:
                return self.collection.distinct(field, query)
            return self.collection.distinct(field)
        except Exception as e:
            print(f"Error getting distinct values: {e}")
            return []
