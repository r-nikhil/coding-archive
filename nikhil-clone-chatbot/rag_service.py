import os
import logging
import yaml
import re
import chromadb
from chromadb.config import Settings
from openai import OpenAI
import glob
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.blog_posts_path = "blog_posts"
        self.data_path = "data"
        
    def initialize(self):
        """Initialize ChromaDB and process blog posts"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(self.data_path, exist_ok=True)
            
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(path=self.data_path)
            self.collection = self.client.get_or_create_collection(
                name="blog_posts",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Process blog posts if collection is empty
            if self.collection.count() == 0:
                self._process_blog_posts()
                
            logger.info(f"RAG service initialized with {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            raise
    
    def _process_blog_posts(self):
        """Process markdown files and create embeddings"""
        try:
            # Create blog_posts directory if it doesn't exist
            os.makedirs(self.blog_posts_path, exist_ok=True)
            
            # Find all markdown files
            markdown_files = glob.glob(os.path.join(self.blog_posts_path, "*.md"))
            
            if not markdown_files:
                logger.warning("No markdown files found in blog_posts directory")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for i, file_path in enumerate(markdown_files):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse frontmatter manually
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            yaml_content = parts[1].strip()
                            post_content = parts[2].strip()
                            try:
                                post_metadata = yaml.safe_load(yaml_content) or {}
                            except yaml.YAMLError:
                                post_metadata = {}
                        else:
                            post_metadata = {}
                            post_content = content
                    else:
                        post_metadata = {}
                        post_content = content
                    
                    # Extract metadata (ChromaDB only accepts str, int, float, bool)
                    categories = post_metadata.get("categories", [])
                    if isinstance(categories, list):
                        categories_str = ", ".join(str(cat) for cat in categories)
                    else:
                        categories_str = str(categories)
                    
                    metadata = {
                        "title": str(post_metadata.get("title", "Untitled")),
                        "categories": categories_str,
                        "date": str(post_metadata.get("date", "")),
                        "file_path": str(file_path)
                    }
                    
                    # Create document ID
                    doc_id = f"post_{i}"
                    
                    # Add to collections
                    documents.append(post_content)
                    metadatas.append(metadata)
                    ids.append(doc_id)
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                    continue
            
            if documents:
                # Generate embeddings and add to collection
                self._add_documents_to_collection(documents, metadatas, ids)
                logger.info(f"Processed {len(documents)} blog posts")
            
        except Exception as e:
            logger.error(f"Error processing blog posts: {e}")
            raise
    
    def _add_documents_to_collection(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents to ChromaDB collection with embeddings"""
        try:
            # Generate embeddings using OpenAI
            embeddings = []
            for doc in documents:
                embedding = self._get_embedding(doc)
                embeddings.append(embedding)
            
            # Add to collection
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
        except Exception as e:
            logger.error(f"Error adding documents to collection: {e}")
            raise
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI's text-embedding-ada-002"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def search_relevant_content(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant content using semantic similarity"""
        try:
            if not self.collection:
                logger.warning("Collection not initialized")
                return []
            
            # Generate embedding for query
            query_embedding = self._get_embedding(query)
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            relevant_content = []
            for i in range(len(results["documents"][0])):
                content = {
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
                }
                relevant_content.append(content)
            
            return relevant_content
            
        except Exception as e:
            logger.error(f"Error searching relevant content: {e}")
            return []
    
    def is_healthy(self) -> bool:
        """Check if RAG service is healthy"""
        try:
            return self.client is not None and self.collection is not None
        except:
            return False
    
    def add_new_post(self, file_path: str):
        """Add a new blog post to the collection"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter manually
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    post_content = parts[2].strip()
                    try:
                        post_metadata = yaml.safe_load(yaml_content) or {}
                    except yaml.YAMLError:
                        post_metadata = {}
                else:
                    post_metadata = {}
                    post_content = content
            else:
                post_metadata = {}
                post_content = content
            
            # Extract metadata (ChromaDB only accepts str, int, float, bool)
            categories = post_metadata.get("categories", [])
            if isinstance(categories, list):
                categories_str = ", ".join(str(cat) for cat in categories)
            else:
                categories_str = str(categories)
            
            metadata = {
                "title": str(post_metadata.get("title", "Untitled")),
                "categories": categories_str,
                "date": str(post_metadata.get("date", "")),
                "file_path": str(file_path)
            }
            
            # Generate unique ID
            doc_id = f"post_{self.collection.count()}"
            
            # Generate embedding
            embedding = self._get_embedding(post_content)
            
            # Add to collection
            self.collection.add(
                documents=[post_content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Added new post: {metadata['title']}")
            
        except Exception as e:
            logger.error(f"Error adding new post: {e}")
            raise
