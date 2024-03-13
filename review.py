from bs4 import BeautifulSoup
import urllib.request

f = open('movie_review.txt', 'w')

for i in range(1,10):
    url = 'http://www.cgv.co.kr/movies/detail-view/?midx=88012#'+str(i)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

# 평점 목록 class = movie_point_list_container
    reviewer_name = soup.select('point_col2 > writeinfo > writer-name')
    reviewer_comment = soup.select('box-comment')

    f.write(f'{reviewer_name}\t{reviewer_comment}')

f.close()