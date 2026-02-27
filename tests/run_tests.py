import pytest

from utils.misc import to_os_path

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

    # NewAppWorkflow tests
    # pytest.main(["-s", to_os_path("tests\\test_new_app_workflow.py")])

    # FixBuildWorkflow tests
    # pytest.main(["-s", to_os_path("tests\\test_fix_build_workflow.py")])

    # TestAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_test_agent.py")])

    # Web tools tests
    # pytest.main(["-s", to_os_path("tests\\test_web_tools.py")])

    # FixTestsWorkflow tests
    # pytest.main(["-s", to_os_path("tests\\test_fix_tests_workflow.py")])

    # MonitorBase tests
    # pytest.main(["-s", to_os_path("tests\\test_monitor_base.py")])

    # ModifyCodeWorkflow tests
    # pytest.main(["-s", to_os_path("tests\\test_modify_code_workflow.py")])

    # ModifyAppWorkflow tests
    # pytest.main(["-s", to_os_path("tests\\test_modify_app_workflow.py")])

    # ResearchAgent tests
    # pytest.main(["-s", to_os_path("tests\\test_research_agent.py")])
