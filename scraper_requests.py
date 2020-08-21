from requests_html import HTMLSession

session = HTMLSession()

r = session.get('http://www.krosmoz.com/en/almanax?game=dofustouch')
html_without_js = r.html

r.html.render()
html_with_js = r.html
print(html_with_js)