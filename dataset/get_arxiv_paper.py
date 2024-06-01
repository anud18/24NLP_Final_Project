import arxiv
import pandas as pd
from datetime import datetime, timedelta

def fetch_arxiv_data(start_date, end_date, max_results=300):
    query = f'submittedDate:[{start_date}0000 TO {end_date}2359]'
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return search.results()

def date_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta

start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 12, 1)
one_month = timedelta(days=30)

cs_count = 5
non_cs_count = 5

cs_titles = []
cs_abstracts = []
cs_dates = []
cs_ids = []
cs_primary_categorys = []

non_cs_titles = []
non_cs_abstracts = []
non_cs_dates = []
non_cs_ids = []
non_cs_primary_categorys = []

for single_date in date_range(start_date, end_date, one_month):
    start_str = single_date.strftime('%Y%m%d')
    end_str = (single_date + one_month - timedelta(days=1)).strftime('%Y%m%d')
    results = fetch_arxiv_data(start_str, end_str)
    
    cs_found = 0
    non_cs_found = 0
    
    for result in results:
        if '$' in result.summary:
          pass
        elif cs_found < cs_count and result.primary_category.startswith('cs.'):
            #cs_ids.append(result.entry_id.replace("http://arxiv.org/abs/", ""))
            cs_ids.append(result.entry_id)
            #cs_titles.append(result.title)
            cs_abstracts.append(result.summary)
            cs_dates.append(result.published.date())
            cs_primary_categorys.append(result.primary_category)
            cs_found += 1
        elif non_cs_found < non_cs_count and not result.primary_category.startswith('cs.'):
            #non_cs_ids.append(result.entry_id.replace("http://arxiv.org/abs/", ""))
            non_cs_ids.append(result.entry_id)
            #non_cs_titles.append(result.title)
            non_cs_abstracts.append(result.summary)
            non_cs_dates.append(result.published.date())
            non_cs_primary_categorys.append(result.primary_category)
            non_cs_found += 1
        if cs_found >= cs_count and non_cs_found >= non_cs_count:
            break

# Create DataFrame
cs_df = pd.DataFrame({
    'Id' : cs_ids,
    'Abstract': cs_abstracts,
    'Date': cs_dates,
    'Primary_category' : cs_primary_categorys
})

non_cs_df = pd.DataFrame({
    'Id' : non_cs_ids,
    'Abstract': non_cs_abstracts,
    'Date': non_cs_dates,
    'Primary_category' : non_cs_primary_categorys
})
combined_df = pd.concat([cs_df, non_cs_df])
combined_df['Methods'] = pd.Series(dtype='float64')
combined_df.to_csv('arxiv_dataset.csv', index=False)

