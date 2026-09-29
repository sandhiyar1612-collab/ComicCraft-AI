# 🗄️ Database & Storage Subsystem

## Overview
ComicCraft currently operates with a zero-friction, portable **File-Based Storage Architecture**. This package provides filesystem management and storage abstraction while providing a complete blueprint for future relational database migration.

---

## Storage Subsystems

1. **Active Engine (`storage_manager.py`)**:
   - Manages scanning and listing generated PDF issues in `static/exports/`.
   - Protects downloads with directory traversal path validation.
   - Provides safe file retrieval and metadata extraction.

2. **Future SQL Blueprint (`schema.sql`)**:
   - *Status*: **To be completed** in future roadmap for user account management.
   - Ready-to-apply SQL DDL for PostgreSQL and SQLite supporting `users`, `comics`, `comic_panels`, and `comic_exports`.
