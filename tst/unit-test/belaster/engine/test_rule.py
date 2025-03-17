
from belaster import Rule, TargetDuplicateRuleError
from pytest import raises
from toolkit import application_context, t0, t1, t2, t3



# Test target cannot be duplicated.
def test_error_when_target_duplicate_error(application_context, t0):
	r0 = Rule(targets={t0})
	with raises(TargetDuplicateRuleError) as error:
		r1 = Rule(targets={t0})
		assert error.target == t0
		assert error.rules == {r0, r1}



# Test the detection of the prerequisites.
def test_list_of_prerequisites(application_context, t0, t1, t2, t3):
	r0 = Rule(targets={t0, t1}, prerequisites=[t2, t3])
	assert application_context.all_rules == {r0}
	assert application_context.all_atoms == {t0, t1, t2, t3}
	assert application_context.map_targets_rules == {t0: r0, t1: r0}


# Test the execution of the recipe.
def test_call_0_callback(application_context):
	r = Rule(targets={t0})
	r.run_recipe()


def test_call_1_callback(application_context):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	r = Rule(targets={t0}, recipe=[c0])
	r.run_recipe()

	assert witness[0] == "0"


def test_call_2_callback(application_context):
	witness = {0: ""}

	def c0(env):
		c0.witness[0] += "0"
	c0.witness = witness

	def c1(env):
		c1.witness[0] += "1"
	c1.witness = witness

	r = Rule(targets={t0}, recipe=[c0, c1])
	r.run_recipe()

	assert witness[0] == "01"
