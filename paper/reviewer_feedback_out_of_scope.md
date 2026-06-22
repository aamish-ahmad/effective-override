# Reviewer Feedback That Is Out of Scope

## Scope Boundary

The TrajectoryCheck / generated-code feedback cluster evaluates a different
technical object: generated program implementations, execution traces,
invariants, and software-testing methods. Agency Trajectory Benchmark evaluates
effective override loss in synthetic human-in-the-loop workflow trajectories.
Shared use of the word “trajectory” does not make the methods interchangeable.

## Out-of-Scope Items for the Current Paper

| TrajectoryCheck item | Why it is out of scope here | Proper destination |
|---|---|---|
| **Generated code implementations** | The current benchmark contains workflow narratives, not executable model-generated programs. | A separate TrajectoryCheck generated-code evaluation. |
| **Invariant extraction** | Effective override labels are defined by an annotation rubric, not extracted program invariants. | TrajectoryCheck method and tooling sections. |
| **Program verification** | The current paper makes no claim about proving software properties. | TrajectoryCheck related work and formal-method positioning. |
| **Property-based testing** | There is no executable system under generated input testing in this benchmark. | TrajectoryCheck baseline evaluation. |
| **Runtime monitors** | The current “rater” classifies supplied trajectories; it is not instrumented runtime verification of software state. | TrajectoryCheck or a separate operational monitoring study. |
| **Formal verification** | No formal specification, proof system, model checker, or verified implementation is evaluated. | TrajectoryCheck comparison and future technical work. |
| **Severity-weighted invariant scoring** | The current four-state rubric and first-crossing rule are not a gate-count stability score. | TrajectoryCheck scoring revision. |
| **Automatic trace generation** | Experiment trajectories are authored synthetic workflow cases, not generated program executions. | TrajectoryCheck benchmark/tool pipeline. |

## Cluster-B Points That Belong to a Separate TrajectoryCheck Paper

- Testing actual LLM-generated implementations with uncontrolled failures.
- Moving beyond three hand-built authentication variants.
- Automating rule-based invariant extraction.
- Comparing against ordinary tests, property-based testing, runtime monitors, and formal verification.
- Replacing equal invariant counts with severity-aware scoring.
- Supporting generated traces and richer temporal properties.
- Connecting invariant maintenance to program-verification literature.
- Building a realistic trajectory-testing benchmark and usable framework.

These are important criticisms and a coherent roadmap for TrajectoryCheck. They
should not be inserted into Agency Trajectory Benchmark's construct, experiments,
results, or claims.

## Limited Transferable Lessons

Three high-level lessons transfer without importing code-specific content:

1. Trajectory framing alone is not enough; evaluation must test unanticipated failures.
2. Small hand-built examples require cautious claims and stronger held-out evaluation.
3. A new method should eventually be compared with credible alternatives.

For Agency Trajectory Benchmark, those lessons motivate independently authored
held-out cases, human/multi-model evaluation, and a stronger temporal baseline
ladder. They do **not** motivate invariant extraction or software-verification
claims in this paper.

## Editorial Rule

If a reviewer comment contains generated code, authentication implementations,
invariants, passed gates, stability scoring, property-based tests, runtime
verification, formal verification, or automatic execution traces, route it to
the separate TrajectoryCheck work unless the current paper explicitly introduces
and evaluates that method in a future version.
