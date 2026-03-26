import requests
from typing import List, Set, Optional, Dict, Any
from urllib.parse import urlparse

class P2PClient:
    def __init__(self):
        self.nodes: Set[str] = set()

    def register_node(self, node_url: str):
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    def fetch_chain(self, node: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"http://{node}/chain", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None
