def test_import_apps():
    import src.apps.factory_qa_agent as qa
    import src.apps.manipulation_service as manip
    import src.apps.sim2real_orchestrator as sim

    assert hasattr(qa, "main")
    assert hasattr(manip, "app")
    assert hasattr(sim, "main")
