import pytest
from definitions.guitar_rig.button import buildButton
from definitions.guitar_rig.encoder import buildEncoder
from definitions.projection.button import buildProjectionButton
from definitions.projection.encoder import buildProjectionEncoder

def test_button_builder():
    """Test that button builder generates correct structure"""
    button = buildButton(
        id=1,
        controllerCoordinates="[1/1/1]",
        channel=0,
        group="g0",
        controllerType="Button",
        tags=["bank1", "button"],
        controller_number=0,
        disableFeedback=False,
        toggleButton=True,
        depth=1
    )

    assert "id = \"gfx_Button0\"" in button
    assert "name = \"Button [1/1/1]\"" in button
    assert "tags = {\"button\",}" in button
    assert "kind = \"Virtual\"" in button

def test_encoder_builder():
    """Test that encoder builder generates correct structure"""
    encoder = buildEncoder(
        id=1,
        controllerCoordinates="[1/1/1]",
        channel=0,
        group="g1",
        controllerType="Encoder",
        tags=["bank1", "encoder"],
        controller_number=0,
        disableFeedback=False,
        depth=1
    )

    assert "id = \"gfx_Encoder0\"" in encoder
    assert "name = \"Encoder [1/1/1]\"" in encoder
    assert "kind = \"Virtual\"" in encoder

def test_projection_button_builder():
    """Test that projection button builder generates correct structure"""
    button = buildProjectionButton(
        id=1,
        controller_number=0,
        buttonSizeW=130,
        buttonSizeH=40,
        rowOffset=220,
        colOffset=220,
        depth=1
    )

    assert "id = \"Button0\"" in button
    assert "height = 40" in button
    assert "width = 130" in button
    assert "shape = \"rectangle\"" in button

def test_projection_encoder_builder():
    """Test that projection encoder builder generates correct structure"""
    encoder = buildProjectionEncoder(
        id=1,
        encoder_type="Encoder",
        controller_number=0,
        knobSizeW=80,
        knobSizeH=80,
        rowOffset=220,
        colOffset=220,
        xOffset=0,
        yOffset=60,
        depth=1
    )

    assert "id = \"Encoder0\"" in encoder
    assert "height = 80" in encoder
    assert "width = 80" in encoder
    assert "shape = \"circle\"" in encoder

def test_builder_depth_indentation():
    """Test that builders handle indentation depth correctly"""
    depths = [0, 1, 2, 3]
    for depth in depths:
        button = buildProjectionButton(
            id=1,
            controller_number=0,
            buttonSizeW=130,
            buttonSizeH=40,
            rowOffset=220,
            colOffset=220,
            depth=depth
        )
        # Check that indentation matches depth
        first_line = button.split('\n')[0]
        assert first_line.count('\t') == depth, f"Incorrect indentation at depth {depth}"