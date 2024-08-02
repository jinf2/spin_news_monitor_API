#This code is from https://gist.github.com/huksley/bc3cb046157a99cd9d1517b32f91a99e
#This script decodes Google News generated encoded, internal URLs for RSS items
import requests
import base64

def fetch_decoded_batch_execute(id):
    s = (
        '[[["Fbv4je","[\\"garturlreq\\",[[\\"en-US\\",\\"US\\",[\\"FINANCE_TOP_INDICES\\",\\"WEB_TEST_1_0_0\\"],'
        'null,null,1,1,\\"US:en\\",null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],'
        '\\"en-US\\",\\"US\\",1,[2,3,4,8],1,0,\\"655000234\\",0,0,null,0],\\"' +
        id +
        '\\"]",null,"generic"]]]'
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Referer": "https://news.google.com/"
    }

    response = requests.post(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
        headers=headers,
        data={"f.req": s}
    )

    if response.status_code != 200:
        raise Exception("Failed to fetch data from Google.")

    text = response.text
    header = '[\\"garturlres\\",\\"'
    footer = '\\",'
    if header not in text:
        raise Exception(f"Header not found in response: {text}")
    start = text.split(header, 1)[1]
    if footer not in start:
        raise Exception("Footer not found in response.")
    url = start.split(footer, 1)[0]
    return url

def decode_google_news_url(source_url):
    url = requests.utils.urlparse(source_url)
    path = url.path.split("/")
    if url.hostname == "news.google.com" and len(path) > 1 and path[-2] == "articles":
        base64_str = path[-1]
        decoded_bytes = base64.urlsafe_b64decode(base64_str + '==')
        decoded_str = decoded_bytes.decode('latin1')

        prefix = b'\x08\x13\x22'.decode('latin1')
        if decoded_str.startswith(prefix):
            decoded_str = decoded_str[len(prefix):]

        suffix = b'\xd2\x01\x00'.decode('latin1')
        if decoded_str.endswith(suffix):
            decoded_str = decoded_str[:-len(suffix)]

        bytes_array = bytearray(decoded_str, 'latin1')
        length = bytes_array[0]
        if length >= 0x80:
            decoded_str = decoded_str[2:length+1]
        else:
            decoded_str = decoded_str[1:length+1]

        if decoded_str.startswith("AU_yqL"):
            return fetch_decoded_batch_execute(base64_str)

        return decoded_str
    else:
        return source_url

# Example usage
if __name__ == "__main__":
    source_url = 'https://news.google.com/rss/articles/CBMiYWh0dHBzOi8vZWNlLmVuZ2luLnVtaWNoLmVkdS9zdG9yaWVzL21pY2hpZ2FuLXBsYXNtYS1wcml6ZS1ob25vcnMtdW5pdmVyc2l0eS1vZi1pbGxpbm9pcy1wcm9mZXNzb3LSAQA?oc=5'
    decoded_url = decode_google_news_url(source_url)
    print("source_url:")
    print(source_url)
    print("decoded_url:")
    print(decoded_url)