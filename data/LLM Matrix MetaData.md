<h1 style="text-align:center;">
LLM Matrix Data Dictionary
</h1> 
<h5 style="text-align:center;">  The Methodolgy: What is each column and how was it caluculated? </h5>
<br>

| Section | Column Name | Description |
|---------|-------------|-------------|
|**Model Info** | 
| | **model** | The name of the model |
|    |organisation | The organisation that created the model |
|    |specialisation | What is the models specialisation, e.g. Finance, Medicine, General Purpose Model  |
|    |created_at | The release date of the model |
|**Bussiness Readiness** |
| Credibility | cred_track_record | Looking at the organisations reputation, and any other projects they have done and how successful they've been <br> <br> _Score between 0 - 4   (0 = bad ; 4 = good)_ |
| ^| cred_endorsements | Well known/ Prominent people or business have used it and said positive things about the model <br> <br> _Score between 0 - 4   (0 = bad ; 4 = good)_  |
| ^ | cred_recognition | Have the model recieved any awards? Are there anny mentions of the model in well known/ popular AI or tech spaces <br> <br> _Score between 0 - 4   (0 = bad ; 4 = good)_ |
| ^ | _cred_score_ | Takes the average of `cred_track_record`, `cred_endorsemnets`, `cred_recognition` <br> <br> _Score between 0 - 4   (0 = bad credability ; 4 = good credability)_ |
| Harmfulness | harm_incidents | Are there any reports or mentions of any incidents or mistakes made by the model? <br> <br> _Score between 0 - 4   (0 = bad - alot of incidents ; 4 = good - no incidents)_ |
| ^ | harm_safeguards | What measures have the organisation taken to improve the outputs of the model so that less mistakes are made? <br> <br>  _Score between 0 - 4   (0 = bad - no safeguards ; 4 = good - lots of safeguards)_ |
| ^ | _harm_score_ | Takes the average of `harm_incidents`, `harm_safeguards` <br> <br> _Score between 0 - 4   (0 = very harmful ; 4 = not harmful)_ |
| Accuracy | accuracy_perc | An average accuracy, as a percentage, found from the internet. <br> This was dependant on the specialisation of the model: if the model is a 'General Purpose Model' an average accross many different tasks were taken, if the model is specialised in a field, e.g. Finance, we took the accuracy related to Financial Tasks |
| ^ | accuracy_estimate | For Models where no data could be found regarding their accuaracy, an estimate was taken based on qualitative comparisons found online. If other versions of the product exist we looked at their accuracy score too. |
| ^ | _accuracy_score_ | Takes an average of `accuracy_perc`, `accuracy_estimate` - (Equal to the value in the column that exists) - and multiplies by 4  <br> <br> _Score between 0 - 4   (0 = low accuarcy ; 4 = high accuarcy)_ |
| Benchmark | GLUE | The `Score` from the [GLUE Leaderboard](https://gluebenchmark.com/leaderboard) as a percentage (divide by 100) |
| ^ | SUPERGLUE | The `Score` from the [SuperGLUE Leaderboard](https://super.gluebenchmark.com/leaderboard) as a percentage (divide by 100) |
| ^ | SQuAD | The average accuracy scores take from the specific model pages/papers on [Papers With Code](https://paperswithcode.com/) as a percentage |
| ^ | HELM_accuracy | The `Mean win rate` taken from the 'Accuracy' Tab on the [HELM Leaderboard](https://crfm.stanford.edu/helm/lite/latest/#/leaderboard) as a percentage (divide by 100) |
| ^ | HELM_efficiency | The `Mean win rate` taken from the 'Efficiency' Tab on the [HELM Leaderboard](https://crfm.stanford.edu/helm/lite/latest/#/leaderboard) as a percentage (divide by 100) |
| ^ | hugging_face_open_llm | The `Average ⬆️` taken from the [Open LLM Leaderboard on Hugging Face](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) as a percentage (divide by 100)|
| ^ | vellum | The `Average` taken from [vellum's LLM Leaderboard](https://www.vellum.ai/llm-leaderboard) as a percentage (divide by 100)|
| ^ | other | The accuracy percentages taken from other sources with benchmark data, e.g. The model's website, other reasearch papers, etc. |
| ^ | estimated | For models where no accuracy measures could be found an estimate was made based off of other models produced by the organisation, qualitative comparisons found online. |
| ^ | _bench_score_ | Takes an average of `GLUE`, `SUPERGLUE`, `SQuAD`, `HELM_accuracy`, `HELM_efficiency`, `hugging_face_open_llm`, `vellum`, `other`, `estimated` and multiplies by 4 <br> <br> _Score between 0 - 4   (0 = low accuarcy ; 4 = high accuarcy)_ |
|  | **x_score** | Calculation: $0.4 *$ `cred_score` $+ 0.3 *$ `harm_score` $+ 0.15 *$ `accuracy_score` $+ 0.15 *$ `bench_score` <br> <br> _Score between 0 - 4   (0 = low performance ; 4 = high performance)_|
|**Pecieved Bussiness Value** |
| Capabalities | _capabailities_ | How many different features does the model have and how well do they perform <br> <br> _Score between 0 - 4   (0 = low capability ; 4 = high capability)_ |
| Success Stories | _success stories_ | How many positive reviews are there after using the model? Carry out a qualatative analysis on how successful the product has been (make sure to look at any fails too) <br> <br> _Score between 0 - 4   (0 = less successful ; 4 = successful)_ |
| Popularity | pop_activity | How many active users does the model have? <br> <br> _Score between 0 - 4   (0 = no users ; 4 = many users)_ |
| ^ | pop_growth_rate | What does the models growth rate look like in the past year and since its release? <br> <br> _Score between 0 - 4   (0 = low growth rate ; 4 = high growth rate)_ |
| ^ | pop_variety | How many different industries and applications can we use the model in? <br> <br> _Score between 0 - 4   (0 = very few ; 4 = many!)_ |
| ^ | _pop_score_ | Takes an average of `pop_activity`, `pop_growth_rate`, `pop_variety` <br> <br> _Score between 0 - 4   (0 = not popular ; 4 = very popular)_ |
| | **y_score** | Calculation: $0.5 *$ `capabailities`$+ 0.25 *$ `success stories`$+0.25 *$ `pop_score` <br> <br> _Score between 0 - 4   (0 = low potential ; 4 = high potential)_ |
