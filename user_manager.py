import reddit_classes
import urllib.request
from bs4 import BeautifulSoup

def main():
    url = input("Enter url: ")
    scrape_comments(url)

# scrape_url COMMENTS
def scrape_comments(url):
    opened_url = urllib.request.urlopen(url)
    soup = BeautifulSoup(opened_url)
    comment_html_blocks = soup.findAll('div', {'class': 'noncollapsed'}) 
    for comment_block in comment_html_blocks:

        p_block = comment_block.findAll('div', {'class':'md'})
        href_block = comment_block.findAll('a', {'class': 'bylink'})

        comment_text_soup = BeautifulSoup(str(p_block))
        url_soup = BeautifulSoup(str(href_block))
        print(url_soup.prettify())
        text = comment_text_soup.p.text
        print("\n*********************************************************** \n")


if __name__ == '__main__':
    main()
