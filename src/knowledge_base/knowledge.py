# knowledge_base/knowledge.py
import traceback
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os
from src.model_helpers import KnowledgeBaseTypeOptions, QueryRequestStatusOptions, SourceOptions
from src.models import KnowledgeBase as KnowledgeBaseModel
import logging

logger = logging.getLogger("app_logger")

class KnowledgeBase:
    """Manages the knowledge base for the AI agent."""

    def __init__(self):
        """Initialize with database connection and optional initial knowledge."""
        self.knowledge_collection = KnowledgeBaseModel.objects.all()

    def get_system_information(self) -> Dict[str, Any]:
        """Retrieve system information from the knowledge base."""
        try:
            all_information = {}
            system_info = self.knowledge_collection.filter(type=KnowledgeBaseTypeOptions.INFO)
            if system_info:
                for info in system_info:
                    if info.description:
                        all_information.update(info.description)
                return all_information

            else:
                return "No system information available."
        except Exception as e:
            logger.error(f"Error retrieving system information: {traceback.format_exc()}")
            return str(e)

    def add_or_update_knowledge(
        self,
        question: str = "",
        answer: str = "",
        source: SourceOptions = SourceOptions.INITIAL,
        type: KnowledgeBaseTypeOptions = KnowledgeBaseTypeOptions.QUERY,
        description: Optional[dict] = None,
        description_key: Optional[str] = None,
        query_request_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[bool, str]:
        """Add or update knowledge in the database."""
        try:
            if type == KnowledgeBaseTypeOptions.INFO:
                if not description or not isinstance(description, dict):
                    return False, "Description is required for INFO type."
                if not description_key:
                    return False, "Description key is required for INFO type."

                existing_entry = self.knowledge_collection.filter(
                    description__has_key=description_key
                ).first()
                if existing_entry:
                    existing_entry.description[description_key] = description[
                        description_key
                    ]
                    existing_entry.save()
                    return True, existing_entry.id

                knowledge_entry = KnowledgeBaseModel.objects.create(
                    question=question,
                    answer=answer,
                    type=type,
                    description=description,
                    source=source,
                )
                return True, knowledge_entry.id
            else:
                if not question:
                    return False, "Question is required for QUERY type."
                if not answer:
                    return False, "Answer is required for QUERY type."

                # Check if the entry already exists
                existing_entry = self.knowledge_collection.filter(
                    question=question, type=type
                ).first()
                if existing_entry:
                    existing_entry.answer = answer
                    existing_entry.source = source
                    existing_entry.save()
                    return True, "Knowledge updated successfully."

                # Create new knowledge entry with an empty description {} if none provided
                knowledge_entry = KnowledgeBaseModel.objects.create(
                    question=question,
                    answer=answer,
                    type=type,
                    description=description or {},
                    source=source,
                    query_request_id=query_request_id,
                )
                return True, knowledge_entry.id
        except Exception as e:
            print(f"Error adding/updating knowledge: {traceback.format_exc()}")
            return False, str(e)

    def _find_similar_entries(self, question: str) -> List[Dict[str, Any]]:
        """Find knowledge base entries similar to the question."""
        try:
            # Get all query type entries from the knowledge base
            all_queries = self.knowledge_collection.filter(type=KnowledgeBaseTypeOptions.QUERY)
            
            # Calculate similarity scores for each entry
            similar_entries = []
            for entry in all_queries:
                if not entry.question:
                    continue
                    
                similarity_score = self._calculate_similarity(entry.question, question)
                
                if similarity_score > 0.3:  # Threshold for similarity
                    similar_entries.append({
                        "question": entry.question,
                        "answer": entry.answer,
                        "score": similarity_score,
                        "id": str(entry.id)
                    })
            
            # Sort by similarity score in descending order and return top 5
            similar_entries.sort(key=lambda x: x["score"], reverse=True)
            return similar_entries[:5]
            
        except Exception as e:
            print(f"Error finding similar entries: {traceback.format_exc()}")
            return []

    def _calculate_similarity(self, db_question: str, user_question: str) -> float:
        """
        Calculate similarity between database question and user question.
        Returns a float value between 0 and 1, where 1 means identical.
        """
        try:
            # Convert questions to lowercase for better comparison
            db_question_lower = db_question.lower()
            user_question_lower = user_question.lower()
            
            # Simple word overlap similarity
            db_words = set(db_question_lower.split())
            user_words = set(user_question_lower.split())
            
            # Check for empty sets to avoid division by zero
            if not db_words or not user_words:
                return 0.0
                
            # Calculate Jaccard similarity (intersection over union)
            intersection = len(db_words.intersection(user_words))
            union = len(db_words.union(user_words))
            
            jaccard_similarity = intersection / union if union > 0 else 0
            
            # Simple exact match bonus
            exact_match_bonus = 0.3 if db_question_lower == user_question_lower else 0
            
            # Calculate final similarity score (capped at 1.0)
            similarity = min(jaccard_similarity + exact_match_bonus, 1.0)
            
            return similarity
            
        except Exception as e:
            print(f"Error calculating similarity: {traceback.format_exc()}")
            return 0.0

    def get_resolved_queries(self) -> List[Dict[str, Any]]:
        """Retrieve all resolved queries from the knowledge base."""
        try:
            resolved_queries = self.knowledge_collection.filter(
                query_request__status=QueryRequestStatusOptions.RESOLVED,
                source=SourceOptions.SUPERVISOR,
            )
            return [
                {
                    "question": query.question,
                    "answer": query.answer,
                    "resolved_at": query.updated_at,
                    "id": str(query.id),
                }
                for query in resolved_queries
            ]
        except Exception as e:
            print(f"Error retrieving resolved queries: {traceback.format_exc()}")
            return []