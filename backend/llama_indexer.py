from rank_bm25 import BM25Okapi
from typing import List, Dict, Any, Optional
import db
import re

class BM25Index:
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.bm25 = None

    def tokenize(self, text: str) -> List[str]:
        """Simple tokenization - split on whitespace and remove punctuation"""
        return re.findall(r'\b\w+\b', text.lower())

    def build_index(self):
        chunks = db.get_all_chunks()
        self.documents = []
        self.metadata = []
        
        for chunk in chunks:
            # Tokenize the content
            tokens = self.tokenize(chunk['content'])
            self.documents.append(tokens)
            self.metadata.append({
                'id': chunk['id'],
                'file_source': chunk['file_source'],
                'label': chunk['label'],
                'page_number': chunk['page_number'],
                'created_at': chunk['created_at'],
                'author': chunk['author'],
                'category': chunk['category'],
                'tags': chunk['tags'],
                'content': chunk['content']
            })
        
        if self.documents:
            self.bm25 = BM25Okapi(self.documents)

    def search(self, query: str, top_k: int = 50) -> List[Dict[str, Any]]:
        if not self.bm25:
            self.build_index()
        
        if not self.bm25:
            return []
        
        # Tokenize the query
        query_tokens = self.tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)
        
        # Create list of (score, metadata) tuples
        scored_docs = list(zip(scores, self.metadata))
        
        # Sort by score (descending)
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        results = []
        seen = set()
        # Return all relevant chunks (with positive scores) up to top_k, removing duplicates
        for score, meta in scored_docs:
            if score > 0:
                unique_key = (meta['content'], meta['file_source'], meta['label'])
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                results.append({
                    'content': meta['content'],
                    'metadata': {k: v for k, v in meta.items() if k != 'content'},
                    'score': float(score)
                })
                if len(results) >= top_k:
                    break
        
        return results

bm25_index = BM25Index() 