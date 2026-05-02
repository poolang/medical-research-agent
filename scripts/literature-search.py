#!/usr/bin/env python3
"""
Literature search script for medical research agent.
Fetches from PubMed E-utilities and ClinicalTrials.gov API.
"""

import requests
import json
import sys
from typing import List, Dict

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CTGOV_BASE = "https://clinicaltrials.gov/api/v2/studies"

def search_pubmed(query: str, max_results: int = 100) -> List[Dict]:
    """Search PubMed and return article metadata."""
    search_url = f"{PUBMED_BASE}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "date"
    }
    r = requests.get(search_url, params=params, timeout=30)
    data = r.json()
    idlist = data.get("esearchresult", {}).get("idlist", [])
    
    if not idlist:
        return []
    
    summary_url = f"{PUBMED_BASE}/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(idlist),
        "retmode": "json"
    }
    sr = requests.get(summary_url, params=summary_params, timeout=30)
    sdata = sr.json()
    
    results = []
    for pmid in idlist:
        article = sdata.get("result", {}).get(pmid, {})
        results.append({
            "pmid": pmid,
            "title": article.get("title", ""),
            "authors": article.get("authors", []),
            "journal": article.get("fulljournalname", ""),
            "year": article.get("pubdate", "")[:4] if article.get("pubdate") else "",
            "doi": article.get("elocationid", "")
        })
    return results

def search_clinicaltrials(condition: str, status: str = "RECRUITING") -> List[Dict]:
    """Search ClinicalTrials.gov for active trials."""
    params = {
        "query.term": condition,
        "filter.overallStatus": status,
        "pageSize": 100
    }
    r = requests.get(CTGOV_BASE, params=params, timeout=30)
    data = r.json()
    
    results = []
    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status_mod = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        
        results.append({
            "nct_id": ident.get("nctId", ""),
            "title": ident.get("officialTitle", ident.get("briefTitle", "")),
            "status": status_mod.get("overallStatus", ""),
            "phase": design.get("phases", []),
            "enrollment": design.get("enrollmentInfo", {}).get("count", 0)
        })
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Searching PubMed for: {query}")
        results = search_pubmed(query)
        print(json.dumps(results[:10], indent=2))
    else:
        print("Usage: python literature-search.py 'your query'")