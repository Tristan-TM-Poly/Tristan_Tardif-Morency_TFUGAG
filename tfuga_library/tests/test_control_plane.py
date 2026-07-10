from tfuga import AITControlPlane, ControlPlaneInput


def test_control_plane_report_contains_layers():
    report = AITControlPlane().run(
        ControlPlaneInput(
            name="tfuga-pr6",
            changed_files=42,
            additions=1570,
            tests_added=8,
            docs_added=8,
        )
    )
    assert report.oak_score > 0
    assert "AIT Control Plane Max Report" in report.final_markdown
    assert "Push / run / publish layer" in report.final_markdown
    assert "Quebec research absorption layer" in report.final_markdown


def test_control_plane_can_skip_research_layer():
    report = AITControlPlane().run(
        ControlPlaneInput(
            name="small",
            changed_files=1,
            additions=20,
            tests_added=1,
            docs_added=1,
            include_quebec_research=False,
        )
    )
    assert report.research_markdown == ""
    assert "Quebec research absorption layer" not in report.final_markdown
