#!/usr/bin/env python3
"""
Create Sample Data for ChromaDB Playground
"""

import chromadb
from chromadb.config import Settings
import numpy as np
import os
from datetime import datetime
import json

def init_chromadb():
    """Initialize ChromaDB client."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("./playground_data", exist_ok=True)
        
        client = chromadb.PersistentClient(
            path="./playground_data",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name="playground_vectors",
            metadata={"hnsw:space": "cosine"}
        )
        
        return client, collection
    except Exception as e:
        print(f"Failed to initialize ChromaDB: {str(e)}")
        return None, None

def create_ai_ml_data():
    """Create AI/ML related data."""
    return [
        {
            "text": "Machine learning algorithms can be supervised, unsupervised, or reinforcement learning",
            "category": "AI/ML",
            "subcategory": "Machine Learning",
            "difficulty": "Intermediate"
        },
        {
            "text": "Deep learning uses neural networks with multiple hidden layers for complex pattern recognition",
            "category": "AI/ML", 
            "subcategory": "Deep Learning",
            "difficulty": "Advanced"
        },
        {
            "text": "Natural language processing enables computers to understand and generate human language",
            "category": "AI/ML",
            "subcategory": "NLP",
            "difficulty": "Intermediate"
        },
        {
            "text": "Computer vision allows machines to interpret and analyze visual information from images",
            "category": "AI/ML",
            "subcategory": "Computer Vision", 
            "difficulty": "Intermediate"
        },
        {
            "text": "Reinforcement learning agents learn optimal behavior through trial and error with rewards",
            "category": "AI/ML",
            "subcategory": "Reinforcement Learning",
            "difficulty": "Advanced"
        },
        {
            "text": "Supervised learning requires labeled training data to learn input-output mappings",
            "category": "AI/ML",
            "subcategory": "Machine Learning",
            "difficulty": "Beginner"
        },
        {
            "text": "Unsupervised learning discovers hidden patterns in data without predefined labels",
            "category": "AI/ML",
            "subcategory": "Machine Learning", 
            "difficulty": "Intermediate"
        },
        {
            "text": "Transfer learning leverages knowledge from pre-trained models for new tasks",
            "category": "AI/ML",
            "subcategory": "Deep Learning",
            "difficulty": "Advanced"
        }
    ]

def create_programming_data():
    """Create programming related data."""
    return [
        {
            "text": "Python is a high-level programming language known for its simplicity and readability",
            "category": "Programming",
            "subcategory": "Python",
            "difficulty": "Beginner"
        },
        {
            "text": "JavaScript is a dynamic programming language used for web development and beyond",
            "category": "Programming",
            "subcategory": "JavaScript", 
            "difficulty": "Beginner"
        },
        {
            "text": "React is a JavaScript library for building user interfaces with component-based architecture",
            "category": "Programming",
            "subcategory": "Frontend",
            "difficulty": "Intermediate"
        },
        {
            "text": "Docker containers package applications with their dependencies for consistent deployment",
            "category": "Programming",
            "subcategory": "DevOps",
            "difficulty": "Intermediate"
        },
        {
            "text": "Git is a distributed version control system for tracking changes in source code",
            "category": "Programming",
            "subcategory": "Version Control",
            "difficulty": "Beginner"
        },
        {
            "text": "REST APIs use HTTP methods to enable communication between different software systems",
            "category": "Programming",
            "subcategory": "APIs",
            "difficulty": "Intermediate"
        },
        {
            "text": "GraphQL provides a query language for APIs with flexible data fetching capabilities",
            "category": "Programming",
            "subcategory": "APIs",
            "difficulty": "Advanced"
        },
        {
            "text": "Microservices architecture breaks applications into small, independent services",
            "category": "Programming",
            "subcategory": "Architecture",
            "difficulty": "Advanced"
        }
    ]

def create_data_science_data():
    """Create data science related data."""
    return [
        {
            "text": "Pandas is a powerful Python library for data manipulation and analysis",
            "category": "Data Science",
            "subcategory": "Data Manipulation",
            "difficulty": "Beginner"
        },
        {
            "text": "NumPy provides efficient array operations and mathematical functions for scientific computing",
            "category": "Data Science",
            "subcategory": "Numerical Computing",
            "difficulty": "Beginner"
        },
        {
            "text": "Matplotlib and Seaborn are popular libraries for creating data visualizations in Python",
            "category": "Data Science",
            "subcategory": "Visualization",
            "difficulty": "Intermediate"
        },
        {
            "text": "Scikit-learn offers machine learning algorithms and tools for data preprocessing",
            "category": "Data Science",
            "subcategory": "Machine Learning",
            "difficulty": "Intermediate"
        },
        {
            "text": "Jupyter notebooks provide an interactive environment for data analysis and documentation",
            "category": "Data Science",
            "subcategory": "Tools",
            "difficulty": "Beginner"
        },
        {
            "text": "Feature engineering transforms raw data into features that improve model performance",
            "category": "Data Science",
            "subcategory": "Feature Engineering",
            "difficulty": "Advanced"
        },
        {
            "text": "Cross-validation techniques help assess model performance and prevent overfitting",
            "category": "Data Science",
            "subcategory": "Model Evaluation",
            "difficulty": "Intermediate"
        },
        {
            "text": "Big data technologies like Hadoop and Spark handle large-scale data processing",
            "category": "Data Science",
            "subcategory": "Big Data",
            "difficulty": "Advanced"
        }
    ]

def create_tech_trends_data():
    """Create technology trends data."""
    return [
        {
            "text": "Large language models like GPT and BERT have revolutionized natural language processing",
            "category": "Tech Trends",
            "subcategory": "LLMs",
            "difficulty": "Advanced"
        },
        {
            "text": "Edge computing brings computation closer to data sources for faster processing",
            "category": "Tech Trends",
            "subcategory": "Edge Computing",
            "difficulty": "Intermediate"
        },
        {
            "text": "Blockchain technology provides decentralized and secure transaction recording",
            "category": "Tech Trends",
            "subcategory": "Blockchain",
            "difficulty": "Advanced"
        },
        {
            "text": "Internet of Things connects physical devices to collect and exchange data",
            "category": "Tech Trends",
            "subcategory": "IoT",
            "difficulty": "Intermediate"
        },
        {
            "text": "5G networks offer faster speeds and lower latency for mobile communications",
            "category": "Tech Trends",
            "subcategory": "Networking",
            "difficulty": "Intermediate"
        },
        {
            "text": "Quantum computing uses quantum mechanics to solve complex computational problems",
            "category": "Tech Trends",
            "subcategory": "Quantum Computing",
            "difficulty": "Advanced"
        },
        {
            "text": "Augmented reality overlays digital information onto the real world",
            "category": "Tech Trends",
            "subcategory": "AR/VR",
            "difficulty": "Intermediate"
        },
        {
            "text": "Serverless computing abstracts infrastructure management for developers",
            "category": "Tech Trends",
            "subcategory": "Cloud Computing",
            "difficulty": "Intermediate"
        }
    ]

def create_software_engineering_data():
    """Create software engineering data."""
    return [
        {
            "text": "Test-driven development writes tests before implementing features",
            "category": "Software Engineering",
            "subcategory": "Testing",
            "difficulty": "Intermediate"
        },
        {
            "text": "Continuous integration automates building and testing code changes",
            "category": "Software Engineering",
            "subcategory": "CI/CD",
            "difficulty": "Intermediate"
        },
        {
            "text": "Agile methodology emphasizes iterative development and customer collaboration",
            "category": "Software Engineering",
            "subcategory": "Methodology",
            "difficulty": "Beginner"
        },
        {
            "text": "Design patterns provide reusable solutions to common software design problems",
            "category": "Software Engineering",
            "subcategory": "Design",
            "difficulty": "Advanced"
        },
        {
            "text": "Code review processes improve code quality through peer feedback",
            "category": "Software Engineering",
            "subcategory": "Quality",
            "difficulty": "Beginner"
        },
        {
            "text": "Refactoring improves code structure without changing external behavior",
            "category": "Software Engineering",
            "subcategory": "Maintenance",
            "difficulty": "Intermediate"
        },
        {
            "text": "Performance optimization techniques improve application speed and efficiency",
            "category": "Software Engineering",
            "subcategory": "Performance",
            "difficulty": "Advanced"
        },
        {
            "text": "Security best practices protect applications from vulnerabilities and attacks",
            "category": "Software Engineering",
            "subcategory": "Security",
            "difficulty": "Intermediate"
        }
    ]

def generate_embeddings(text, seed=None):
    """Generate simulated embeddings for text."""
    if seed is not None:
        np.random.seed(seed)
    
    # Create a deterministic vector based on text content
    text_hash = hash(text) % (2**32)
    np.random.seed(text_hash)
    
    # Generate 128-dimensional vector
    vector = np.random.randn(128)
    vector = vector / np.linalg.norm(vector)  # Normalize
    
    return vector.tolist()

def create_sample_data():
    """Create comprehensive sample data for ChromaDB."""
    print("🚀 Creating sample data for ChromaDB playground...")
    
    # Initialize ChromaDB
    client, collection = init_chromadb()
    if not collection:
        print("❌ Failed to initialize ChromaDB")
        return False
    
    # Clear existing data
    try:
        collection.delete(where={})
        print("🗑️ Cleared existing data")
    except:
        pass
    
    # Collect all data
    all_data = []
    all_data.extend(create_ai_ml_data())
    all_data.extend(create_programming_data())
    all_data.extend(create_data_science_data())
    all_data.extend(create_tech_trends_data())
    all_data.extend(create_software_engineering_data())
    
    print(f"📊 Generated {len(all_data)} data points across 5 categories")
    
    # Prepare data for ChromaDB
    vectors = []
    ids = []
    metadatas = []
    
    for i, data in enumerate(all_data):
        vector_id = f"doc_{i:03d}"
        
        # Generate embedding
        vector = generate_embeddings(data["text"], seed=i)
        
        vectors.append(vector)
        ids.append(vector_id)
        
        # Create metadata
        metadata = {
            'text': data["text"],
            'category': data["category"],
            'subcategory': data["subcategory"],
            'difficulty': data["difficulty"],
            'created_at': datetime.now().isoformat(),
            'vector_dim': 128,
            'doc_id': vector_id
        }
        metadatas.append(metadata)
    
    # Add to ChromaDB
    try:
        collection.add(
            embeddings=vectors,
            ids=ids,
            metadatas=metadatas
        )
        
        print("✅ Successfully added data to ChromaDB!")
        
        # Show statistics
        count = collection.count()
        print(f"📈 Total vectors in database: {count}")
        
        # Show category distribution
        categories = {}
        for metadata in metadatas:
            cat = metadata['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 Category Distribution:")
        for category, count in categories.items():
            print(f"  {category}: {count} documents")
        
        # Show difficulty distribution
        difficulties = {}
        for metadata in metadatas:
            diff = metadata['difficulty']
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        print("\n🎯 Difficulty Distribution:")
        for difficulty, count in difficulties.items():
            print(f"  {difficulty}: {count} documents")
        
        print(f"\n🎉 Sample data created successfully!")
        print(f"🌐 Open http://localhost:8506 to explore the data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding data to ChromaDB: {str(e)}")
        return False

def test_search():
    """Test search functionality."""
    print("\n🔍 Testing search functionality...")
    
    client, collection = init_chromadb()
    if not collection:
        return False
    
    # Test queries
    test_queries = [
        "machine learning algorithms",
        "Python programming",
        "data visualization",
        "artificial intelligence",
        "web development"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Searching for: '{query}'")
        
        # Generate query vector
        query_vector = generate_embeddings(query)
        
        # Search
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=3,
            include=["metadatas", "distances"]
        )
        
        if results and 'ids' in results and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                similarity = 1 - distance
                
                print(f"  {i+1}. {metadata['text'][:60]}... (Similarity: {similarity:.3f})")
        else:
            print("  No results found")

if __name__ == "__main__":
    print("🧠 ChromaDB Sample Data Creator")
    print("=" * 50)
    
    # Create data
    success = create_sample_data()
    
    if success:
        # Test search
        test_search()
        
        print("\n" + "=" * 50)
        print("🎯 Ready to play! Open the ChromaDB playground at:")
        print("   http://localhost:8506")
        print("\n💡 Try searching for:")
        print("   - 'machine learning'")
        print("   - 'Python programming'") 
        print("   - 'data science'")
        print("   - 'artificial intelligence'")
        print("   - 'web development'")
    else:
        print("❌ Failed to create sample data")
