
from belaster import DependencyHypergraphLoopError, Rule
from pytest import raises
from toolkit import application_context, dependency_hypergraph, t0, t1, t2, t3, t4, t5, t6



# Build the dependency graph from the rules.
def test_build_empty(dependency_hypergraph):
	assert dependency_hypergraph.hyperedges == set()
	assert dependency_hypergraph.vertice == set()
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {}
	assert dependency_hypergraph.vertice_to_rules_where_target == {}


def test_build_1_rule_1_target(dependency_hypergraph, t0):
	r0 = Rule(targets={t0})
	dependency_hypergraph.add_rule(r0)
	assert dependency_hypergraph.hyperedges == {r0}
	assert dependency_hypergraph.vertice == {t0}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t0: r0}


def test_build_1_rule_1_target_1_prerequisite(dependency_hypergraph, t0, t1):
	r0 = Rule(targets={t0}, prerequisites=[t1])
	dependency_hypergraph.add_rule(r0)
	assert dependency_hypergraph.hyperedges == {r0}
	assert dependency_hypergraph.vertice == {t0, t1}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {t1: {r0}}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t0: r0}


def test_build_1_rule_2_target_2_prerequisite(dependency_hypergraph, t1, t2, t3):
	r0 = Rule(targets={t0, t1}, prerequisites=[t2, t3])
	dependency_hypergraph.add_rule(r0)
	assert dependency_hypergraph.hyperedges == {r0}
	assert dependency_hypergraph.vertice == {t0, t1, t2, t3}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {t2: {r0}, t3: {r0}}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t0: r0, t1: r0}


def test_build_2_rule_2_target_2_prerequisite(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t0}, prerequisites=[t2])
	r1 = Rule(targets={t1}, prerequisites=[t3])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	assert dependency_hypergraph.hyperedges == {r0, r1}
	assert dependency_hypergraph.vertice == {t0, t1, t2, t3}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {t2: {r0}, t3: {r1}}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t0: r0, t1: r1}


def test_build_2_rule_4_target_4_prerequisite(dependency_hypergraph, t0, t1, t2, t3, t4, t5, t6):
	r0 = Rule(targets={t0, t2}, prerequisites=[t3, t5])
	r1 = Rule(targets={t1, t6}, prerequisites=[t4, t5])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	assert dependency_hypergraph.hyperedges == {r0, r1}
	assert dependency_hypergraph.vertice == {t0, t1, t2, t3, t4, t5, t6}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {t3: {r0}, t4: {r1}, t5: {r0, r1}}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t0: r0, t1: r1, t2: r0, t6: r1}


def test_build_2_rule_chain_target_prerequisite(dependency_hypergraph, t0, t1, t2):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t2}, prerequisites=[t1])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	assert dependency_hypergraph.hyperedges == {r0, r1}
	assert dependency_hypergraph.vertice == {t0, t1, t2}
	assert dependency_hypergraph.vertice_to_rules_where_prerequisite == {t0: {r0}, t1: {r1}}
	assert dependency_hypergraph.vertice_to_rules_where_target == {t1: r0, t2: r1}


# Topological sorting of rules and loop detection.
def test_topo_empty(dependency_hypergraph):
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges == []


def test_topo_1_rule_loop(dependency_hypergraph):
	r0 = Rule(targets={t0}, prerequisites=[t0])
	dependency_hypergraph.add_rule(r0)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		assert error.looping_hyeredges == {r0}


def test_topo_1_rule_no_prerequisites(dependency_hypergraph):
	r0 = Rule(targets={t0})
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges == [r0]


def test_topo_1_rule_no_targets(dependency_hypergraph):
	r0 = Rule(prerequisites=[t0])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges == [r0]


def test_topo_1_rule(dependency_hypergraph, t0, t1):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges == [r0]


def test_topo_2_rules_loop(dependency_hypergraph, t0, t1):
	r0 = Rule(targets={t0}, prerequisites=[t1])
	r1 = Rule(targets={t1}, prerequisites=[t0])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		assert error.looping_hyperedges == {r0, r1}


def test_topo_2_rules_side_by_side(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t3}, prerequisites=[t2])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges in [[r0, r1], [r1, r0]]


def test_topo_2_rules_dependent(dependency_hypergraph, t0, t1, t2):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t2}, prerequisites=[t1])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.build_topological_ordering_of_hyperedges()
	assert dependency_hypergraph.topological_ordering_of_hyperedges == [r0, r1]


def test_topo_3_rules_loop_size_2_parallel(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t3}, prerequisites=[t2])
	r2 = Rule(targets={t2}, prerequisites=[t3])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r1, r2}


def test_topo_3_rules_loop_size_2_branch_in(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t3}, prerequisites=[t0])
	r1 = Rule(targets={t1}, prerequisites=[t2, t3])
	r2 = Rule(targets={t2}, prerequisites=[t1])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r1, r2}


def test_topo_3_rules_loop_size_2_branch_out(dependency_hypergraph, t0, t1, t2):
	r0 = Rule(targets={t0}, prerequisites=[t1])
	r1 = Rule(targets={t1}, prerequisites=[t2])
	r2 = Rule(targets={t2}, prerequisites=[t1])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r1, r2}


def test_topo_3_rules_loop_size_3(dependency_hypergraph, t0, t1, t2):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t2}, prerequisites=[t1])
	r2 = Rule(targets={t0}, prerequisites=[t2])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r0, r1, r2}


def test_topo_4_rules_2_loops_parallel(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t0}, prerequisites=[t1])
	r2 = Rule(targets={t3}, prerequisites=[t2])
	r3 = Rule(targets={t2}, prerequisites=[t3])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	dependency_hypergraph.add_rule(r3)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r0, r1, r2, r3}


def test_topo_4_rules_2_loops_bound_by_prerequisite(dependency_hypergraph, t0, t1, t2, t3):
	r0 = Rule(targets={t1}, prerequisites=[t0])
	r1 = Rule(targets={t0}, prerequisites=[t1, t2])
	r2 = Rule(targets={t3}, prerequisites=[t2])
	r3 = Rule(targets={t2}, prerequisites=[t3])
	dependency_hypergraph.add_rule(r0)
	dependency_hypergraph.add_rule(r1)
	dependency_hypergraph.add_rule(r2)
	dependency_hypergraph.add_rule(r3)
	with raises(DependencyHypergraphLoopError) as error:
		dependency_hypergraph.build_topological_ordering_of_hyperedges()
		error.looping_hyperedges == {r0, r1, r2, r3}
