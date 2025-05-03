import re

class QueryExtractor:
    def extract_search_query(self, command):
        # Basic patterns to remove common phrases
        patterns = [
            r"(can you|please)?\s*(search|find|look for|get)\s*(me|us)?\s*(a|an|some|the)?\s*",  # "Find me a..."
            r"(on youtube|on the internet)?",  # optional trailing
        ]
        query = command.lower()

        for pattern in patterns:
            query = re.sub(pattern, "", query)

        return query.strip()
