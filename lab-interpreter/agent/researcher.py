"""
PubMed Research Module
Fetches relevant research articles from PubMed E-utilities API (free, no key needed)
"""
import requests
import time
from typing import List, Dict, Optional


class PubMedResearcher:
    """Fetch biomarker research from PubMed E-utilities"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    RATE_LIMIT_DELAY = 0.5  # seconds between requests
    
    def __init__(self):
        """Initialize researcher with cache"""
        self.cache: Dict[str, List[Dict]] = {}
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce rate limiting (0.5s between requests)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()
    
    def fetch_pubmed_studies(self, biomarker_name: str, status: str) -> List[Dict]:
        """
        Fetch PubMed studies for a biomarker with given status.
        
        Args:
            biomarker_name: Name of the biomarker (e.g., "HbA1c")
            status: Status from parser (e.g., "high", "low", "borderline_high")
            
        Returns:
            List of study dicts: {pmid, title, abstract_snippet, pubmed_url}
        """
        # Check cache first
        cache_key = f"{biomarker_name}_{status}".lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Build search query
            query = f"{biomarker_name} {status} lifestyle intervention diet exercise"
            
            # Search for PMIDs
            pmids = self._search_pubmed(query, max_results=5)
            
            if not pmids:
                self.cache[cache_key] = []
                return []
            
            # Fetch details for each PMID
            studies = []
            for pmid in pmids:
                self._rate_limit()
                study = self._fetch_article_details(pmid)
                if study:
                    studies.append(study)
            
            # Cache results
            self.cache[cache_key] = studies
            return studies
        
        except Exception as e:
            print(f"Error fetching studies for {biomarker_name}: {str(e)}")
            return []
    
    def _search_pubmed(self, query: str, max_results: int = 5) -> List[str]:
        """
        Search PubMed and return top PMIDs.
        
        Args:
            query: Search query string
            max_results: Maximum results to fetch
            
        Returns:
            List of PMIDs (strings)
        """
        try:
            self._rate_limit()
            
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json"
            }
            
            url = f"{self.BASE_URL}/esearch.fcgi"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])
            
            return pmids
        
        except requests.RequestException as e:
            print(f"PubMed search error: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in search_pubmed: {str(e)}")
            return []
    
    def _fetch_article_details(self, pmid: str) -> Optional[Dict]:
        """
        Fetch abstract and metadata for a single PMID.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            Dict with {pmid, title, abstract_snippet, pubmed_url} or None
        """
        try:
            self._rate_limit()
            
            params = {
                "db": "pubmed",
                "id": pmid,
                "rettype": "abstract",
                "retmode": "text"
            }
            
            url = f"{self.BASE_URL}/efetch.fcgi"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            text = response.text
            
            # Parse title and abstract from response
            title = self._extract_title(text)
            abstract = self._extract_abstract(text)
            abstract_snippet = abstract[:300] + "..." if len(abstract) > 300 else abstract
            
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            
            return {
                "pmid": pmid,
                "title": title,
                "abstract_snippet": abstract_snippet,
                "pubmed_url": pubmed_url
            }
        
        except requests.RequestException as e:
            print(f"Error fetching PMID {pmid}: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching article {pmid}: {str(e)}")
            return None
    
    def _extract_title(self, text: str) -> str:
        """Extract title from PubMed response text"""
        try:
            # PubMed abstract format has "TI  - " for title
            lines = text.split('\n')
            title_lines = []
            in_title = False
            
            for line in lines:
                if line.startswith('TI  - '):
                    in_title = True
                    title_lines.append(line[6:].strip())
                elif in_title:
                    if line.startswith('AB  - ') or line.startswith('FAU ') or line.startswith('AU  '):
                        break
                    if line.strip() and not line[0].isspace():
                        break
                    if line.strip():
                        title_lines.append(line.strip())
            
            return ' '.join(title_lines) if title_lines else "No title"
        
        except Exception:
            return "No title"
    
    def _extract_abstract(self, text: str) -> str:
        """Extract abstract from PubMed response text"""
        try:
            # PubMed abstract format has "AB  - " for abstract
            lines = text.split('\n')
            abstract_lines = []
            in_abstract = False
            
            for line in lines:
                if line.startswith('AB  - '):
                    in_abstract = True
                    abstract_lines.append(line[6:].strip())
                elif in_abstract:
                    # Stop at next section
                    if line.startswith('FAU ') or line.startswith('AU  ') or line.startswith('TI  - '):
                        break
                    if line.strip() and not line[0].isspace():
                        break
                    if line.strip():
                        abstract_lines.append(line.strip())
            
            return ' '.join(abstract_lines) if abstract_lines else "No abstract available"
        
        except Exception:
            return "No abstract available"


def research_flagged_biomarkers(flagged_list: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Research biomarkers with abnormal status.
    
    Args:
        flagged_list: List of biomarker dicts from parser
        
    Returns:
        Dict mapping biomarker names to list of studies
    """
    researcher = PubMedResearcher()
    results = {}
    
    # Filter for abnormal biomarkers
    abnormal_biomarkers = [
        b for b in flagged_list
        if b.get('status') in ['high', 'low', 'borderline_high', 'borderline_low']
    ]
    
    if not abnormal_biomarkers:
        print("No abnormal biomarkers to research")
        return {}
    
    print(f"\n🔬 Researching {len(abnormal_biomarkers)} abnormal biomarkers...")
    
    for biomarker in abnormal_biomarkers:
        name = biomarker.get('name', 'Unknown')
        status = biomarker.get('status', 'unknown')
        
        print(f"  • Searching PubMed for {name} ({status})...", end=" ", flush=True)
        
        studies = researcher.fetch_pubmed_studies(name, status)
        
        if studies:
            results[name] = studies
            print(f"✓ Found {len(studies)} studies")
        else:
            print("✗ No studies found")
    
    return results
