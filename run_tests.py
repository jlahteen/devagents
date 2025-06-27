import pytest

from tools.os_tools import to_os_path

if __name__ == "__main__":
    # Run all tests
    pytest.main(["-s", "tests"])

    # BuldAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_build_agent.py")])

    # Shell tools tests
    # pytest.main(["-s", to_os_path("tests\\test_shell_tools.py")])

    # Config tests
    # pytest.main(["-s", to_os_path("tests\\test_config.py")])

    # DeveloperAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_developer_agent.py")])

    # ScaffoldAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_scaffold_agent.py")])

    # NewAppScenario tests
    # pytest.main(["-s", to_os_path("tests\\test_new_app_scenario.py")])

    # FixBuildScenario tests
    # pytest.main(["-s", to_os_path("tests\\test_fix_build_scenario.py")])

    # TestAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_test_agent.py")])

    # Web tools tests
    # pytest.main(["-s", to_os_path("tests\\test_web_tools.py")])

    # FixTestsScenario tests
    # pytest.main(["-s", to_os_path("tests\\test_fix_tests_scenario.py")])

    # ConsoleMonitor tests
    # pytest.main(["-s", to_os_path("tests\\test_monitor_base.py")])
