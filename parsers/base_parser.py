from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_output: Any) -> List[Dict[str, Any]]:
        """Parse raw scanner output into standardized Finding format."""
        pass
