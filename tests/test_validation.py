import pytest
from app.dgii.validation import XSDValidator, get_validator_for

def test_xsd_validator_valid_xml():
    """
    Tests that the XSDValidator correctly validates a valid XML file.
    """
    validator = XSDValidator("ARECF v1.0.xsd")
    xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<ARECF>
    <DetalleAcusedeRecibo>
        <Version>1.0</Version>
        <RNCEmisor>10100000001</RNCEmisor>
        <RNCComprador>10100000002</RNCComprador>
        <eNCF>E310000000001</eNCF>
        <Estado>0</Estado>
        <FechaHoraAcuseRecibo>01-01-2024 12:00:00</FechaHoraAcuseRecibo>
    </DetalleAcusedeRecibo>
</ARECF>
"""
    assert validator.validate_xml(xml_content) is True

def test_xsd_validator_invalid_xml():
    """
    Tests that the XSDValidator correctly identifies an invalid XML file.
    """
    validator = XSDValidator("ARECF v1.0.xsd")
    xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<ARECF>
    <DetalleAcusedeRecibo>
        <Version>1.0</Version>
        <RNCEmisor>10100000001</RNCEmisor>
        <RNCComprador>10100000002</RNCComprador>
        <eNCF>E310000000001</eNCF>
        <Estado>99</Estado> <!-- Invalid state -->
        <FechaHoraAcuseRecibo>01-01-2024 12:00:00</FechaHoraAcuseRecibo>
    </DetalleAcusedeRecibo>
</ARECF>
"""
    assert validator.validate_xml(xml_content) is False

def test_get_validator_for():
    """
    Tests that the get_validator_for factory function returns a validator.
    """
    validator = get_validator_for("31")
    assert isinstance(validator, XSDValidator)

    with pytest.raises(ValueError):
        get_validator_for("99")

def test_xsd_validator_file_not_found():
    """
    Tests that a FileNotFoundError is raised when the XSD file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        XSDValidator("non_existent_schema.xsd")
