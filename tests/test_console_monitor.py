import asyncio
import io
import sys
import textwrap
import pytest
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient

from config import Config
from utils.misc import Tee
from monitoring.console_monitor import ConsoleMonitor

SKIP_TESTS = False

_multi_line_long_text1 = textwrap.dedent(
    f"""
    word1
    word1 word2
    word1 word2 word3
    word1 word2 word3 word4
    word1 word2 word3 word4 word5
    word1 word2 word3 word4 word5 word6
    word1 word2 word3 word4 word5 word6 word7
    word1 word2 word3 word4 word5 word6 word7 word8
    word1 word2 word3 word4 word5 word6 word7 word8 word9
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14
    """
)

_multi_line_long_text2 = textwrap.dedent(
    f"""
    Text from https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
    The hexagonal architecture divides a system into several loosely-coupled interchangeable components, such as the application core, the database, the user interface, test scripts and interfaces with other systems. This approach is an alternative to the traditional layered architecture.

    Each component is connected to the others through a number of exposed "ports". Communication through these ports follow a given protocol depending on their purpose. Ports and protocols define an abstract API that can be implemented by any suitable technical means (e.g. method invocation in an object-oriented language, remote procedure calls, or Web services).

    The granularity of the ports and their number is not constrained:

    - a single port could in some case be sufficient (e.g. in the ca
    """
)

_multi_line_long_text3 = textwrap.dedent(
    f"""
    Text from https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
    The hexagonal architecture divides a system into several loosely-coupled interchangeable components, such as the application core, the database, the user interface, test scripts and interfaces with other systems. This approach is an alternative to the traditional layered architecture.

    Each component is connected to the others through a number of exposed "ports". Communication through these ports follow a given protocol depending on their purpose. Ports and protocols define an abstract API that can be implemented by any suitable technical means (e.g. method invocation in an object-oriented language, remote procedure calls, or Web services).

    The granularity of the ports and their number is not constrained:

    - a single port could in some case be sufficient (e.g. in the case of a simple service consumer);
    - typically, there are ports for event sources (user interface, automatic feeding), notifications (outgoing notifications), database (in order to interface the component with any suitable DBMS), and administration (for controlling the component);

    In an extreme case, there could be a different port for every use case, if needed.
    Adapters are the glue between components and the outside world. They tailor the exchanges between the external world and the ports that represent the requirements of the inside of the application component. There can be several adapters for one port, for example, data can be provided by a user through a GUI or a command-line interface, by an automated data source, or by test scripts.
    """
)

def cleanup(console_monitor: ConsoleMonitor):

    console_monitor.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_10_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    # Act
    for i in range(10):
        print(f"{i} Hello, World!")
    await asyncio.sleep(2)

    # Assert
    assert len(console_monitor.original_lines) == 11, "Expected 10 original lines in the output console."
    for i in range(10):
        assert (
            console_monitor.original_lines[i] == f"{i} Hello, World!"
        ), f"Expected original line {i} to be '{i} Hello, World!', but got '{console_monitor.original_lines[i]}'"

    assert len(console_monitor.wrapped_lines) == 11, "Expected 10 wrapped lines in the output console."
    for i in range(10):
        assert (
            console_monitor.wrapped_lines[i] == f"{i} Hello, World!"
        ), f"Expected wrapped line {i} to be '{i} Hello, World!', but got '{console_monitor.wrapped_lines[i]}'"

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_full_minus_one_amount_of_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(height - 2):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_full_no_new_line_amount_of_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(height - 2):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    print(f"{i} Scrolling line", end="", flush=True)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_full_amount_of_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(height - 1):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_full_amount_of_lines_with_long_last_line():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(height - 2):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    print(
        "This is a very long line that should wrap to a multiple lines in the console. At least the tester would like this to happend because it should."
    )
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_2_times_full_amount_of_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(2 * (height - 1)):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_full_plus_one_amount_of_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)
    height, _ = console_monitor.stdscr.getmaxyx()

    # Act
    for i in range(height):
        print(f"{i} Scrolling line {i}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_10_long_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    # Act
    for i in range(10):
        print(f"{i} Hello, World!".ljust(100, "x"))  # Pad to 100 characters
    await asyncio.sleep(2)

    # Assert
    assert len(console_monitor.original_lines) == 11, "Expected 10 original lines in the output console."
    for i in range(10):
        assert console_monitor.original_lines[i] == f"{i} Hello, World!".ljust(
            100, "x"
        ), f"Expected original line {i} to be '{i} Hello, World!', but got '{console_monitor.original_lines[i]}'"

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_tee_writes_to_console_monitor():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    for i in range(16):
        print(f"{i} Hello, World!")

    print(f"16 Hello, World!")
    print(f"17 Hello, World!")
    print(f"18 Hello, World!")

    config = Config()
    model_client = ChatCompletionClient.load_component(config.model_client)
    assistant = AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        model_client=model_client,
    )

    s = "Hello, World!"
    for i in range(len(s)):
        print(s[i], end="", flush=True)
        await asyncio.sleep(0.3)
    print()

    # Act: loop 10 times, sending a different message each time
    for i in range(10):
        await Console(
            assistant.on_messages_stream(
                [TextMessage(content=f"Hello! Tell me a funny 'why' joke. [{i}]", source="user")],
                cancellation_token=None,
            )
        )
        await asyncio.sleep(3)  # Allow time for output to be processed

    # Act
    print()
    print("line1\nline2")
    for i in range(10):
        print("Hello, World!")

    await asyncio.sleep(2)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_multi_line_long_lines():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    # Act
    print(_multi_line_long_text3)
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
@pytest.mark.parametrize("test_text", [_multi_line_long_text1, _multi_line_long_text2, _multi_line_long_text3])
async def test_write_multi_line_long_lines_char_by_char_with_spaces_between(test_text):
    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    # Act
    for i in range(len(test_text)):
        c = test_text[i]
        if c == '\n':
            print()
        elif c != ' ':
            print(c, end="", flush=True)
            print(" ", end="", flush=True)
        else:
            print(" ", end="", flush=True)
            print(" ", end="", flush=True)
    await asyncio.sleep(8)

    # Clean up
    cleanup(console_monitor)
    
    
@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test for now")
@pytest.mark.asyncio
async def test_write_line_with_no_new_line_plus_multi_line_text():

    # Arrange
    console_monitor = ConsoleMonitor()
    sys.stdout = Tee(console_monitor)
    sys.stderr = Tee(console_monitor)

    # Act
    print("Where is the cat? ", end="", flush=True)
    print("The cat is in the moon! (This should be in the same line.)\nAt least it was...\nI think.")
    await asyncio.sleep(4)

    # Clean up
    cleanup(console_monitor)
