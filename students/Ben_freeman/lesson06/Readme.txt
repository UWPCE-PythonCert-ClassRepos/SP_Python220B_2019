As can be seen in the log files, good_perf is about .4 faster than poor_perf per run.
The only step that does not see a signifigent increase in performance seems to the original filtering step.
This might have to do with the fact that the poor perf code does not actually filter and instead passes every item.