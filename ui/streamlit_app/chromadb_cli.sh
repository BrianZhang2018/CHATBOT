#!/bin/bash

# ChromaDB Command Line Tools
# Various ways to interact with the vector database

echo "🗄️ ChromaDB Vector Database CLI Tools"
echo "======================================"

# Database location
DB_PATH="/Users/brianzhang/ai/chatbot/rag/data/embeddings"
SQLITE_FILE="$DB_PATH/chroma.sqlite3"

echo "📁 Database location: $DB_PATH"
echo "💾 SQLite file: $SQLITE_FILE"

# Check if database exists
if [ -f "$SQLITE_FILE" ]; then
    echo "✅ Database exists"
    
    # Get database size
    DB_SIZE=$(du -sh "$DB_PATH" | cut -f1)
    echo "📊 Database size: $DB_SIZE"
    
    # Count tables in SQLite
    echo "📋 SQLite tables:"
    sqlite3 "$SQLITE_FILE" ".tables"
    
    echo ""
    echo "📈 Database stats:"
    sqlite3 "$SQLITE_FILE" "SELECT name FROM sqlite_master WHERE type='table';" | while read table; do
        count=$(sqlite3 "$SQLITE_FILE" "SELECT COUNT(*) FROM $table;" 2>/dev/null || echo "0")
        echo "   $table: $count rows"
    done
    
else
    echo "❌ Database not found"
fi

echo ""
echo "🔧 Available commands:"
echo "   1. Connect with Python: python connect_to_chromadb.py"
echo "   2. Connect via RAG: python rag_database_config.py"
echo "   3. View SQLite directly: sqlite3 '$SQLITE_FILE'"
echo "   4. Start document manager: streamlit run document_manager.py"

echo ""
echo "📱 Web interfaces:"
echo "   - Document Manager: http://localhost:8501"
echo "   - Vector DB Playground: python vector_db_playground_with_chromadb.py"


