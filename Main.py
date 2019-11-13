import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Match_history import *
from FIFA_rank import *
from DataEnrichment import *
from ML import *
import time


pd.options.display.max_columns = 100
t1 = time.time()

# fullEnrichmentFlow(scrap_FIFA=True, scrap_matches=False)
# groupStage()
# fullEnrichmentFlow(prefix='group_stage_')

# trainPredict(prefix='group_stage_')
# trainPredict(prefix='')


dataset = pd.read_csv("full_data.csv", index_col=0)
resultPrediction(dataSelection(dataset))

print("Execution Time : " + str(time.time()-t1) + " s")