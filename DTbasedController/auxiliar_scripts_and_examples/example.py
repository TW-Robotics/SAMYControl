from sklearn.linear_model import LogisticRegression

from dtcontrol.benchmark_suite import BenchmarkSuite
from dtcontrol.decision_tree.decision_tree import DecisionTree
from dtcontrol.decision_tree.impurity.entropy import Entropy
from dtcontrol.decision_tree.determinization.max_freq_determinizer import MaxFreqDeterminizer

from dtcontrol.decision_tree.splitting.axis_aligned import AxisAlignedSplittingStrategy
from dtcontrol.decision_tree.splitting.categorical_multi import CategoricalMultiSplittingStrategy
from dtcontrol.decision_tree.splitting.categorical_single import CategoricalSingleSplittingStrategy
from dtcontrol.decision_tree.splitting.linear_classifier import LinearClassifierSplittingStrategy
from dtcontrol.decision_tree.splitting.linear_classifier_only_leaf import LinearClassifierOnlyLeafSplittingStrategy
from dtcontrol.decision_tree.splitting.oc1 import OC1SplittingStrategy
from dtcontrol.decision_tree.splitting.context_aware.richer_domain_splitting_strategy import RicherDomainSplittingStrategy
from dtcontrol.decision_tree.splitting.context_aware.richer_domain_cli_strategy import RicherDomainCliStrategy


suite = BenchmarkSuite(timeout=3600,
                       save_folder='saved_classifiers',
                       benchmark_file='benchmark',
                       rerun=True)

suite.add_datasets(['examples', 'examples/prism', 'examples/storm', 'examples/cps', 'examples/csv'], include=['firewire_abst']) #firewire_abst #cartpole #blocksworld.5 #


aa = AxisAlignedSplittingStrategy()
aa.priority = 1

mc = CategoricalMultiSplittingStrategy()
mc.priority = 1

mc_grouping = CategoricalMultiSplittingStrategy(True)
mc_grouping.priority = 1

sc = CategoricalSingleSplittingStrategy()
sc.priority = 1

logreg = LinearClassifierSplittingStrategy(LogisticRegression, solver='lbfgs', penalty='none')
logreg.priority = 1

oc1 = OC1SplittingStrategy()
oc1.priority = 1

richer = RicherDomainSplittingStrategy(debug=False)
richer.priority = 1

cli = RicherDomainCliStrategy(debug=True)
cli.priority = 1



classifiers = [
    # Interactive
    # DecisionTree([cli], Entropy(), 'interactive'),
  #  DecisionTree([aa], Entropy(), 'aa'),
  #  DecisionTree([mc, aa], Entropy(), 'mc-aa'),
  #  DecisionTree([sc, aa], Entropy(), 'sc-aa'),
  #  DecisionTree([logreg, aa], Entropy(), 'lgreg-aa'),
  #  DecisionTree([oc1], Entropy(), 'oc1')
     DecisionTree([mc_grouping, aa], Entropy(), 'extra3')
]

suite.benchmark(classifiers)
suite.display_html()
