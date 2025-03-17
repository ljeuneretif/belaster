
from belaster import Rule, TargetDuplicateRuleError
from pytest import raises
from toolkit import application_context, t0, t1, t2, t3, t4, t5



# Test when empty.
def test_empty(application_context):
	assert application_context.all_rules == set()
	assert application_context.all_targets == set()
	assert application_context.all_atoms == set()
	assert application_context.map_targets_rules == {}


# Test building the sets of rules and the set of targets.
def test_index_targets_rules_1_rule_no_target_no_prerequisite(application_context):
	r = Rule()
	assert application_context.all_rules == {r}
	assert application_context.all_targets == set()
	assert application_context.all_atoms == set()


def test_index_targets_rules_1_rule_no_target(application_context, t0):
	r0 = Rule(prerequisites=[t0])
	assert application_context.all_rules == {r0}
	assert application_context.all_targets == set()
	assert application_context.all_atoms == {t0}


def test_index_targets_rules_1_rule_no_prerequisite(application_context, t0):
	r0 = Rule(targets={t0})
	assert application_context.all_rules == {r0}
	assert application_context.all_targets == {t0}
	assert application_context.all_atoms == {t0}


def test_index_targets_rules_1_rule(application_context, t0, t1):
	r0 = Rule(targets={t0}, prerequisites=[t1])
	assert application_context.all_rules == {r0}
	assert application_context.all_targets == {t0}
	assert application_context.all_atoms == {t0, t1}


def test_index_targets_rules_2_rules(application_context, t0, t1, t2, t3):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t3}, prerequisites=[t2])
	assert application_context.all_rules == {r0, r1}
	assert application_context.all_targets == {t1, t3}
	assert application_context.all_atoms == {t0, t1, t2, t3}


# Test the mapping from targets to rules.
def test_1_rule_0_target_0_prerequisite(application_context):
	Rule()
	assert application_context.map_targets_rules == {}


def test_1_rule_0_prerequisite(application_context, t0):
	r0 = Rule(targets={t0})
	assert application_context.map_targets_rules == {t0: r0}


def test_1_rule_0_target(application_context, t0):
	Rule(prerequisites=[t0])
	assert application_context.map_targets_rules == {}


def test_1_rule_2_targets(application_context, t0, t1, t2):
	r0 = Rule(targets={t0, t1}, prerequisites=[t2])
	assert application_context.map_targets_rules == {t0: r0, t1: r0}


def test_2_rules_chaining(application_context, t0, t1, t2, t3, t4, t5):
	r0 = Rule(targets={t0, t1}, prerequisites=[t2, t5])
	r1 = Rule(targets={t2, t3}, prerequisites=[t4])
	assert application_context.map_targets_rules == {t0: r0, t1: r0, t2: r1, t3: r1}


def test_2_rules_mixed_targets(application_context, t0, t1, t2, t3, t4):
	r0 = Rule(targets={t0, t1}, prerequisites=[t2])
	with raises(TargetDuplicateRuleError) as error:
		r1 = Rule(targets={t1, t3}, prerequisites=[t2, t4])
		assert error.target == t1
		assert error.rules == {r0, r1}
