-- ============================================================================
-- ComicCraft Relational Database Schema Blueprint (Future Roadmap Specification)
-- Target RDBMS: PostgreSQL 14+ / SQLite 3.35+
-- ============================================================================

-- 1. Users Table (To be completed for multi-tenant authentication)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Comics Table (Stores overarching comic master metadata)
CREATE TABLE IF NOT EXISTS comics (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    character_name VARCHAR(120) NOT NULL,
    setting VARCHAR(200) NOT NULL,
    tone VARCHAR(100) NOT NULL,
    art_style VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Comic Panels Table (Stores individual panels 1 through 5)
CREATE TABLE IF NOT EXISTS comic_panels (
    id VARCHAR(36) PRIMARY KEY,
    comic_id VARCHAR(36) NOT NULL REFERENCES comics(id) ON DELETE CASCADE,
    panel_number INT NOT NULL CHECK (panel_number BETWEEN 1 AND 10),
    title VARCHAR(255) NOT NULL,
    scene_description TEXT NOT NULL,
    caption TEXT,
    narration TEXT,
    dialogue TEXT,
    image_prompt TEXT NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    image_engine VARCHAR(50) DEFAULT 'pillow_scenic',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Comic Exports Table (Tracks compiled PDF issues)
CREATE TABLE IF NOT EXISTS comic_exports (
    id VARCHAR(36) PRIMARY KEY,
    comic_id VARCHAR(36) REFERENCES comics(id) ON DELETE CASCADE,
    pdf_filename VARCHAR(255) NOT NULL,
    pdf_path VARCHAR(500) NOT NULL,
    file_size_kb FLOAT NOT NULL,
    page_count INT DEFAULT 5,
    download_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_comics_user ON comics(user_id);
CREATE INDEX IF NOT EXISTS idx_panels_comic ON comic_panels(comic_id);
CREATE INDEX IF NOT EXISTS idx_exports_comic ON comic_exports(comic_id);
