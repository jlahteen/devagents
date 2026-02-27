from enum import Enum
from typing import Final

BUILD_AGENT_SUCCESSFUL: Final[str] = "BUILD_AGENT SUCCESSFUL"
BUILD_AGENT_FAILED: Final[str] = "BUILD_AGENT FAILED"
TEST_AGENT_SUCCESSFUL: Final[str] = "TEST_AGENT SUCCESSFUL"
TEST_AGENT_FAILED: Final[str] = "TEST_AGENT FAILED"
SCAFFOLD_AGENT_DONE: Final[str] = "SCAFFOLD_AGENT DONE"
DEVELOPER_AGENT_DONE: Final[str] = "DEVELOPER_AGENT DONE"
OUTPUT_AGENT_DONE: Final[str] = "OUTPUT_AGENT DONE"

REVIEW_RESULT_APPROVED: Final[str] = "REVIEW RESULT: APPROVED"
REVIEW_RESULT_CHANGES_REQUIRED: Final[str] = "REVIEW RESULT: CHANGES REQUIRED"

JUDGE_AGENT_APPROVED: Final[str] = "JUDGE AGENT: APPROVED"
JUDGE_AGENT_CHANGES_REQUIRED: Final[str] = "JUDGE AGENT: CHANGES REQUIRED"

# Default number of iterations to keep conversation history in inner teams
DEFAULT_MAX_HISTORY_ITERATIONS: Final[int] = 2

# Maximum number of pages to load during web research
MAX_PAGE_LOADS: Final[int] = 8

# Maximum number of Google searches to perform during web research
MAX_GOOGLE_SEARCHES: Final[int] = 4


class WorkflowType(Enum):
    NEW_CODE = 200
    MODIFY_CODE = 300
    NEW_APP = 400
    MODIFY_APP = 500
    FIX_BUILD = 600
    FIX_TESTS = 700
