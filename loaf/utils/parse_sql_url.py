from urllib.parse import urlparse
from .creds import Creds

def parse_sql_url(creds: Creds, sql_url: str):
    # Parsing.
    parsed_url = urlparse(sql_url)
    userinfo, netloc = parsed_url.netloc.split('@') if '@' in parsed_url.netloc else (None, parsed_url.netloc)
    user, password = userinfo.split(':') if userinfo else (None, None)
    host, port = netloc.split(':') if ':' in netloc else (netloc, None)
    database = parsed_url.path[1:] if parsed_url.path else None
    # Assignment.
    creds.host = host
    creds.port = int(port) if port else None,
    creds.user = user
    creds.password = password
    creds.database = database