import re
import requests

def get_url_from_gdrive_confirmation(contents):
    url = ""
    for line in contents.splitlines():
        m = re.search(r'href="(\/uc\?export=download[^"]+)', line)
        if m:
            url = "https://docs.google.com" + m.groups()[0]
            url = url.replace("&amp;", "&")
            break
        m = re.search('id="downloadForm" action="(.+?)"', line)
        if m:
            url = m.groups()[0]
            url = url.replace("&amp;", "&")
            break
        m = re.search('"downloadUrl":"([^"]+)', line)
        if m:
            url = m.groups()[0]
            url = url.replace("\\u003d", "=")
            url = url.replace("\\u0026", "&")
            break
        m = re.search('<p class="uc-error-subcaption">(.*)</p>', line)
        if m:
            error = m.groups()[0]
            raise RuntimeError(error)
    if not url:
        return RuntimeError(
            "Cannot retrieve the public link of the file. "
            "You may need to change the permission to "
            "'Anyone with the link', or have had many accesses."
        )
    return url

def get_file_details(url):
    sess = requests.session()
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
    res  = sess.get(url, headers=headers, stream=True, verify=True)

    if 'drive.google.com' in url:
        url = get_url_from_gdrive_confirmation(res.text)
    elif 'temp.sh' in url:
        url = url
    res  = sess.get(url, headers=headers, stream=True, verify=True)

    size = str(int(res.headers.get('Content-Length')) / (1024*1024))[0:5] + " MB"

    name = ((res.headers.get('Content-Disposition')).split("'"))[-1]
    details = {
        'name' : name,
        'size' : size,
    }
    return details