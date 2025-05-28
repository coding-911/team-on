import pytest
import sys
from pathlib import Path

# 테스트 디렉토리의 상위 디렉토리(src)를 Python 경로에 추가
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.append(src_path) 