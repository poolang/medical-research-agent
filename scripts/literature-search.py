#!/usr/bin/env python3
"""PubMed E-Utilities Literature Search"""
import os, requests
from datetime import datetime
from pathlib import Path

NCBI_API_KEY = os.getenv('NCBI_API_KEY')
BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

SPECIALTY_QUERIES = {
    'cardiology': [
        '(heart failure[Title/Abstract]) AND (randomized controlled trial[Publication Type])',
        '(myocardial infarction[Title/Abstract]) AND (guideline[Publication Type])',
        '(atrial fibrillation[Title/Abstract]) AND (anticoagulation[Title/Abstract])',
    ],
    'oncology': [
        '(immunotherapy[Title/Abstract]) AND (clinical trial[Publication Type])',
        '(targeted therapy[Title/Abstract]) AND (precision medicine[Title/Abstract])',
    ],
    'neurology': [
        '(alzheimer disease[Title/Abstract]) AND (randomized controlled trial[Publication Type])',
        '(stroke[Title/Abstract]) AND (thrombolysis[Title/Abstract])',
    ],
}

def search_pubmed(query, retmax=20):
    params = {'db': 'pubmed', 'term': query, 'retmax': retmax, 'retmode': 'json', 'sort': 'date', 'datetype': 'pdat', 'reldate': 7}
    if NCBI_API_KEY: params['api_key'] = NCBI_API_KEY
    r = requests.get(f'{BASE_URL}/esearch.fcgi', params=params, timeout=30)
    r.raise_for_status()
    return r.json().get('esearchresult', {}).get('idlist', [])

def fetch_summaries(pmids):
    if not pmids: return []
    params = {'db': 'pubmed', 'id': ','.join(pmids), 'retmode': 'json'}
    if NCBI_API_KEY: params['api_key'] = NCBI_API_KEY
    r = requests.get(f'{BASE_URL}/esummary.fcgi', params=params, timeout=30)
    r.raise_for_status()
    return r.json().get('result', {})

def format_article(pmid, summary):
    title = summary.get('title', 'No title')
    authors = summary.get('authors', [])
    author_names = ', '.join([a.get('name', '') for a in authors[:3]])
    if len(authors) > 3: author_names += ' et al.'
    source = summary.get('source', 'Unknown journal')
    pubdate = summary.get('pubdate', 'Unknown date')
    doi = summary.get('elocationid', '')
    return f"""### {title}
- **Authors**: {author_names}
- **Journal**: {source}
- **Date**: {pubdate}
- **PMID**: {pmid}
- **DOI**: {doi}
"""

def main():
    output_dir = Path('literature-updates')
    output_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    all_results = []
    for specialty, queries in SPECIALTY_QUERIES.items():
        specialty_results = []
        for query in queries:
            try:
                pmids = search_pubmed(query)
                if pmids:
                    summaries = fetch_summaries(pmids)
                    for pmid in pmids:
                        if pmid in summaries:
                            specialty_results.append(format_article(pmid, summaries[pmid]))
            except Exception as e:
                print(f'Error searching {specialty}: {e}')
        if specialty_results:
            output_file = output_dir / f'{specialty}-{today}.md'
            with open(output_file, 'w') as f:
                f.write(f'# {specialty.title()} Literature Update - {today}\n\n')
                f.write('\n\n'.join(specialty_results))
            print(f'Wrote {len(specialty_results)} articles to {output_file}')
            all_results.extend(specialty_results)
    if all_results:
        index_file = output_dir / f'index-{today}.md'
        with open(index_file, 'w') as f:
            f.write(f'# Literature Update Index - {today}\n\n')
            f.write(f'Total articles found: {len(all_results)}\n\n')
            for specialty in SPECIALTY_QUERIES:
                f.write(f'- [{specialty.title()}]({specialty}-{today}.md)\n')
        print(f'Wrote index to {index_file}')
    else:
        print('No new articles found this week.')

if __name__ == '__main__':
    main()
