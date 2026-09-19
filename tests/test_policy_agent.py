from src.agents.policy_agent import PolicyAgent
from src.config import POLICYHOLDERS_FILE


def test_filters_city_and_affected_policy_types():
    policyholders = PolicyAgent(POLICYHOLDERS_FILE).find_affected("São Paulo", {"has_risk": True, "affected_policy_types": ["Auto"]})
    assert len(policyholders) == 1
    assert policyholders[0]["nome"] == "Ana Souza"
    assert policyholders[0]["tipo_apolice"] == "Auto"
