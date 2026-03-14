"""
PubMed Research Module
Fetches relevant research articles from PubMed API
"""
import requests
from typing import List, Dict


class PubMedResearcher:
    """Fetch biomarker research from PubMed"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, email: str = ""):
        """Initialize with email for NCBI"""
        self.email = email
    
    def search_biomarker(self, biomarker_name: str, max_results: int = 5) -> List[Dict]:
        """Search PubMed for biomarker studies"""
        try:
            params = {
                "db": "pubmed",
                "term": f"{biomarker_name} blood test",
                "retmax": max_results,
                "rettype": "json",
                "email": self.email
            }
            
            # Search endpoint
            search_url = f"{self.BASE_URL}/esearch.fcgi"
            response = requests.get(search_url, params=params)
            
            if response.status_code != 200:
                return []
            
            search_data = response.json()
            return search_data.get("esearchresult", {}).get("idlist", [])
        
        except Exception as e:
            print(f"Error searching PubMed: {str(e)}")
            return []
    
    def fetch_article_details(self, article_ids: List[str]) -> List[Dict]:
        """Fetch details for article IDs"""
        try:
            params = {
                "db": "pubmed",
                "id": ",".join(article_ids),
                "rettype": "json",
                "email": self.email
            }
            
            # Fetch endpoint
            fetch_url = f"{self.BASE_URL}/efetch.fcgi"
            response = requests.get(fetch_url, params=params)
            
            if response.status_code != 200:
                return []
            
            return response.json().get("result", {})
        
        except Exception as e:
            print(f"Error fetching article details: {str(e)}")
            return []
