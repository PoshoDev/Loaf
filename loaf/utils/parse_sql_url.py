from urllib.parse import urlparse


def parse_sql_url(sql_url):
    parsed_url = urlparse(sql_url)
    userinfo, netloc = parsed_url.netloc.split('@') if '@' in parsed_url.netloc else (None, parsed_url.netloc)
    user, password = userinfo.split(':') if userinfo else (None, None)
    host, port = netloc.split(':') if ':' in netloc else (netloc, None)
    database = parsed_url.path[1:] if parsed_url.path else None
    return {
        'host': host,
        'port': int(port) if port else None,
        'user': user,
        'password': password,
        'database': database
    }
