from tfuga.auto_automation import AITAutoAutomationKernel, AutomationMode, AutomationNeed


def test_auto_automation_kernel():
    kernel = AITAutoAutomationKernel()
    plans, orders = kernel.run()
    assert plans and orders
    assert "meta_automation_guarded" in kernel.markdown()
    safe = kernel.plan(AutomationNeed("safe reporter", "after build", .5, .8, .1, .8, "evidence"))
    assert safe.mode == AutomationMode.DRY_RUN
    blocked = kernel.plan(AutomationNeed("self loop expander", "after plan", .8, .8, .2, .9, "evidence"))
    assert blocked.mode == AutomationMode.APPROVAL_REQUIRED
