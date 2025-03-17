
from belaster import Rule
from belaster.engine.rule_applier import RuleApplierNotInitializedError
from pytest import raises
from toolkit import application_context, rule_applier, t0, t1, t2, t3, t4, t5, t6



# Test on no rules.
def test_empty(rule_applier):
	with raises(RuleApplierNotInitializedError):
		rule_applier.apply()


# Test on one rule.
def test_1_rule_no_goal(rule_applier, t0):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	Rule(targets={t0}, recipe=[c0])
	rule_applier.initialize([])
	rule_applier.apply()

	assert witness[0] == ""


def test_1_rule_1_goal(rule_applier, t0):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	Rule(targets={t0}, recipe=[c0])
	rule_applier.initialize([t0])
	rule_applier.apply()

	assert witness[0] == "0"


def test_1_rule_2_goals(rule_applier, t0):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	Rule(targets={t0}, recipe=[c0])
	rule_applier.initialize([t0, t0])
	rule_applier.apply()

	assert witness[0] == "0"


# Test on 2 rules.
def test_2_rules_parallel_1_goal(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	rule_applier.initialize([t0])
	rule_applier.apply()

	assert witness[0] == "0"


def test_2_rules_parallel_2_goals(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	rule_applier.initialize([t0, t1])
	rule_applier.apply()

	assert witness[0] == "01"


def test_2_rules_parallel_3_goals_0(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	rule_applier.initialize([t0, t1, t0])
	rule_applier.apply()

	assert witness[0] == "01"


def test_2_rules_parallel_3_goals_1(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	rule_applier.initialize([t0, t1, t1])
	rule_applier.apply()

	assert witness[0] == "01"


def test_2_rules_sequential_1_final_goal(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	rule_applier.initialize([t1])
	rule_applier.apply()

	assert witness[0] == "01"


def test_2_rules_sequential_1_intermediate_goal(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	rule_applier.initialize([t0])
	rule_applier.apply()

	assert witness[0] == "0"


def test_2_rules_sequential_2_goals_intermediate_final(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	rule_applier.initialize([t0, t1])
	rule_applier.apply()

	assert witness[0] == "01"


def test_2_rules_sequential_2_goals_final_intermediate(rule_applier, t0, t1):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	rule_applier.initialize([t1, t0])
	rule_applier.apply()

	assert witness[0] == "01"


# Test on 3 rules.
def test_3_rules_sequential_1_final_goal(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	Rule(targets={t2}, prerequisites=[t1], recipe=[c2])
	rule_applier.initialize([t2])
	rule_applier.apply()

	assert witness[0] == "012"


def test_3_rules_sequential_1_intermediate_goal_1(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	Rule(targets={t2}, prerequisites=[t1], recipe=[c2])
	rule_applier.initialize([t1])
	rule_applier.apply()

	assert witness[0] == "01"


def test_3_rules_sequential_1_intermediate_goal_0(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	Rule(targets={t2}, prerequisites=[t1], recipe=[c2])
	rule_applier.initialize([t0])
	rule_applier.apply()

	assert witness[0] == "0"


def test_3_rules_sequential_2_goals_intermediate_goal_0_final(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	Rule(targets={t2}, prerequisites=[t1], recipe=[c2])
	rule_applier.initialize([t0, t2])
	rule_applier.apply()

	assert witness[0] == "012"


def test_3_rules_sequential_2_goals_intermediate_goals_10(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, prerequisites=[t0], recipe=[c1])
	Rule(targets={t2}, prerequisites=[t1], recipe=[c2])
	rule_applier.initialize([t1, t0])
	rule_applier.apply()

	assert witness[0] == "01"


def test_3_rules_V_1_final_goal(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	Rule(targets={t2}, prerequisites=[t0, t1], recipe=[c2])
	rule_applier.initialize([t2])
	rule_applier.apply()

	assert witness[0] == "012"


def test_3_rules_V_1_intermediate_goal_0(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	Rule(targets={t2}, prerequisites=[t0, t1], recipe=[c2])
	rule_applier.initialize([t0])
	rule_applier.apply()

	assert witness[0] == "0"


def test_3_rules_V_1_intermediate_goal_1(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	Rule(targets={t2}, prerequisites=[t0, t1], recipe=[c2])
	rule_applier.initialize([t1])
	rule_applier.apply()

	assert witness[0] == "1"


def test_3_rules_V_3_intermediate_goals_10_final(rule_applier, t0, t1, t2):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	def c2(env):
		c2.witness[0] += "2"
	c2.witness = witness

	Rule(targets={t0}, recipe=[c0])
	Rule(targets={t1}, recipe=[c1])
	Rule(targets={t2}, prerequisites=[t0, t1], recipe=[c2])
	rule_applier.initialize([t1, t0, t2])
	rule_applier.apply()

	assert witness[0] == "102"
