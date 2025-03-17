
from belaster.engine.rule_applier import RuleApplier
from pytest import fixture



@fixture
def rule_applier():
	return RuleApplier()
