import os
import shutil
import subprocess
import tempfile

from utils.misc import print_tool_error, print_tool_use


def validate_mermaid(mermaid_code: str) -> str:
    """
    Validates Mermaid diagram syntax by running it through the mermaid-cli (mmdc).

    Returns a success or error message.
    """

    mmdc = shutil.which("mmdc") or shutil.which("mmdc.cmd")
    if not mmdc:
        return "validate_mermaid ERROR: mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli"

    tmp_in_path = None
    tmp_out_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False, encoding="utf-8") as tmp_in:
            tmp_in.write(mermaid_code)
            tmp_in_path = tmp_in.name

        tmp_out_path = tmp_in_path.replace(".mmd", ".svg")

        result = subprocess.run(
            [mmdc, "-i", tmp_in_path, "-o", tmp_out_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print_tool_use("validate_mermaid: Mermaid syntax is valid")
            return "validate_mermaid OK: Mermaid syntax is valid"
        else:
            error = result.stderr.strip() or result.stdout.strip()
            print_tool_error(f"validate_mermaid ERROR: {error}")
            return f"validate_mermaid ERROR: {error}"

    except Exception as e:
        error_msg = f"validate_mermaid ERROR: {e}"
        print_tool_error(error_msg)
        return error_msg
    finally:
        if tmp_in_path and os.path.exists(tmp_in_path):
            os.remove(tmp_in_path)
        if tmp_out_path and os.path.exists(tmp_out_path):
            os.remove(tmp_out_path)
