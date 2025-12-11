"""
Models package

This package contains database models and schema definitions.

Modules:
    - database: MongoDB connection and management
    - schema: Database schema documentation and validation

Usage:
    from models.database import db
    from models.schema import AdDocumentSchema, validate_ad_document
"""

from .database import db

__all__ = ['db']
