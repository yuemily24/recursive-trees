import json
data = json.load(open('year_paper_rect.json', 'r'))
print(json.dumps(data, sort_keys=True, indent=4))