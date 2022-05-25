from operator import itemgetter

import requests
from plotly import offline

# Make an API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:10]:
    # Make a separate API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                          reverse=True)
titles, comments, labels = [], [], []
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")
    title = submission_dict['title']
    link = submission_dict['hn_link']
    label = f"<a href= '{link}'>{title}</a>"
    labels.append(label)
    comments.append(submission_dict['comments'])
    titles.append(submission_dict['title'])

# Create Bar Graph
data = [{
    'type':'bar',
    'x': titles,
    'y': comments,
    'hovertext': labels,
    'marker': {
        'color': 'rgb(55,22,72)',
        'line': {'width': 1.7, 'color': 'rgb(55,55,78)'}
    }
}]

my_layout = {
    'title': 'Most Active Discussions',
    'titlefont': {'size': 24},
    'xaxis': {
        'title': 'TITLES',
        'titlefont': {'size': 24},
    },
    'yaxis': {
        'title': '# of Comments',
        'titlefont': {'size': 24},
    }
}

# Output data
fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='Hacker_News_Most_comments.html')