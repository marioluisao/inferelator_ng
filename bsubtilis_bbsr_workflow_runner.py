from inferelator_ng.bsubtilis_bbsr_workflow import Bsubtilis_Bbsr_Workflow

workflow = Bsubtilis_Bbsr_Workflow()
# Common configuration parameters
workflow.input_dir = 'data/bsubtilis'
workflow.num_bootstraps = 2
workflow.delTmax = 60
workflow.delTmin = 15
workflow.tau = 15
workflow.run() 
