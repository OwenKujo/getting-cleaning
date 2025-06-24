from bs4 import BeautifulSoup
import re
import csv

# Local HTML file to parse
html_file = '150 คำทำนายฝัน 2568 พร้อมเลขมงคล ฝันแบบไหนถึงเรียกว่ามีโชค!.html'

def fetch_dream_interpretations_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    main_content = soup.find('div', id='article-content')
    if not main_content:
        # Fallback: find the largest div by text length
        candidates = soup.find_all('div')
        main_content = max(candidates, key=lambda d: len(d.get_text(strip=True)), default=None)
        if not main_content:
            print('Could not find main article content.')
            return [], []

    # Extract dream entries
    results = []
    current_category = None
    for tag in main_content.find_all(['h3', 'p'], recursive=True):
        if tag.name == 'h3':
            current_category = tag.get_text(strip=True)
        elif tag.name == 'p':
            text = tag.get_text(" ", strip=True)
            match = re.match(r"(ฝัน(?:ถึง|ว่า|เห็น)?[^\n\r]*?)ทำนายว่า\s*([^\n\r]*?)\s*-\s*เลขเด็ด\s*([\d\s,]+)", text)
            if match:
                dream = match.group(1).strip(' :：.\u000b\n\r')
                interpretation = match.group(2).strip(' :：.\u000b\n\r')
                lucky_numbers = match.group(3).strip(' :：.\u000b\n\r')
                results.append({
                    'category': current_category or '',
                    'dream': dream,
                    'interpretation': interpretation,
                    'lucky_numbers': lucky_numbers,
                    'time': '',
                    'meaning': ''
                })
    print(f"Extracted {len(results)} dream entries.")

    # Extract time meaning section
    found_time_section = False
    for tag in main_content.find_all(['h2', 'ul', 'li', 'p'], recursive=True):
        if tag.name == 'h2' and 'เวลา กับ ความฝัน' in tag.get_text():
            found_time_section = True
        elif found_time_section and tag.name == 'ul':
            for li in tag.find_all('li', recursive=False):
                li_text = li.get_text(" ", strip=True)
                m = re.match(r'(ฝัน[\w\s]+)=?\s*(.*)', li_text)
                if m:
                    time_label = m.group(1).strip(' :：.\u000b\n\r')
                    meaning = m.group(2).strip(' :：.\u000b\n\r')
                    results.append({
                        'category': '',
                        'dream': '',
                        'interpretation': '',
                        'lucky_numbers': '',
                        'time': time_label,
                        'meaning': meaning
                    })
            break
    print(f"Total entries (dreams + time meanings): {len(results)}")
    return results

def main():
    data = fetch_dream_interpretations_from_file(html_file)
    if not data:
        print('No data extracted.')
        return
    with open('dream_interpretations2.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['category', 'dream', 'interpretation', 'lucky_numbers', 'time', 'meaning'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print('Saved to dream_interpretations1.csv')

if __name__ == "__main__":
    main()
