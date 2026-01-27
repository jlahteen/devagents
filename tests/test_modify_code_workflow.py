import os
import textwrap

import pytest

from tests.test_utils import assert_file_contains, setup_test
from utils.config import Config
from workflows.modify_code.modify_code_workflow import ModifyCodeWorkflow

SKIP_TESTS = False

prompt_add_van_to_cars_cs = textwrap.dedent(
    """
    Modify the app in Cars.cs so that add a Van class that inherits from Car.
    """
)

prompt_split_cars_cs_to_separate_cs_files = textwrap.dedent(
    """
    Modify the app in Cars.cs such that each class is in its own file.
    Add also a Van class that inherits from Car in its own Van.cs file.
    Save the main program in Program.cs.
    Remove the existing Cars.cs file.
    """
)


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("modify_code_workflow", "add_van_to_cars_cs", "cars_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_add_van_to_cars_cs__adds_van_class(setup_test):
    # Arrange
    test_run_dir = setup_test
    workflow = ModifyCodeWorkflow(config=Config())

    # Act
    await workflow.run(prompt=prompt_add_van_to_cars_cs)

    # Assert
    assert not os.path.exists(os.path.join(test_run_dir, "Program.cs"))
    assert not os.path.exists(os.path.join(test_run_dir, "Car.cs"))
    assert not os.path.exists(os.path.join(test_run_dir, "ElectricCar.cs"))
    assert not os.path.exists(os.path.join(test_run_dir, "SportsCar.cs"))
    assert not os.path.exists(os.path.join(test_run_dir, "SUV.cs"))
    assert not os.path.exists(os.path.join(test_run_dir, "Van.cs"))
    assert os.path.exists(os.path.join(test_run_dir, "Cars.cs"))
    assert_file_contains(os.path.join(test_run_dir, "Cars.cs"), "public class Van : Car")


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test")
@pytest.mark.parametrize(
    "setup_test",
    [("modify_code_workflow", "split_cars_cs_to_separate_cs_files", "cars_cs_console_app")],
    indirect=True,
)
@pytest.mark.asyncio
async def test_split_cars_cs_to_separate_cs_files__creates_cs_files(setup_test):
    # Arrange
    test_run_dir = setup_test
    workflow = ModifyCodeWorkflow(config=Config())

    # Act
    await workflow.run(prompt=prompt_split_cars_cs_to_separate_cs_files)

    # Assert
    assert os.path.exists(os.path.join(test_run_dir, "Program.cs"))
    assert os.path.exists(os.path.join(test_run_dir, "Car.cs"))
    assert_file_contains(os.path.join(test_run_dir, "Car.cs"), "public class Car")
    assert os.path.exists(os.path.join(test_run_dir, "ElectricCar.cs"))
    assert_file_contains(os.path.join(test_run_dir, "ElectricCar.cs"), "public class ElectricCar : Car")
    assert os.path.exists(os.path.join(test_run_dir, "SportsCar.cs"))
    assert_file_contains(os.path.join(test_run_dir, "SportsCar.cs"), "public class SportsCar : Car")
    assert os.path.exists(os.path.join(test_run_dir, "SUV.cs"))
    assert_file_contains(os.path.join(test_run_dir, "SUV.cs"), "public class SUV : Car")
    assert os.path.exists(os.path.join(test_run_dir, "Van.cs"))
    assert_file_contains(os.path.join(test_run_dir, "Van.cs"), "public class Van : Car")
    assert not os.path.exists(os.path.join(test_run_dir, "Cars.cs"))
