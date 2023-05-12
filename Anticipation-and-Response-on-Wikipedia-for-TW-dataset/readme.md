# Anticipation and-Response on Wikipedia for TW-dataset.git

Using the method on the paper :
https://ojs.aaai.org/index.php/ICWSM/article/download/18063/17866/21558

on TW political wiki page pageviews data

- Doing: 
  - Check wether the model is suitable for those dataset 
  - Clustering

- About our dataset :
  - our dataset are from ```wikimedia API``` (https://wikimedia.org/api/rest_v1/#/) 
  
  - However, it seens that if wanting to get pageviews by a specific article, it can only get daily pageviews, and it may be a little bit harsh to  meet the requirement of the paper.  
  

### pageview.py:
using ```requests``` to download the pageviews from Rest API for a specific article.

### model.py:
Fitting the parameters : $a_-$, $b_-$, $\tau_-$, $a_+$, $b_+$, $\tau_+$ for purpose of __Checking if it is suitable__ and then __Clustering__. (and, hence, it is Supervised)

- Using ```sklearn.scipy.optmize least_squares``` package to fit the least square fitting data

**Note that we didn't try the prediction application since our mathmatical ability are still not enought to understand how to fit out the parameters $a_+$, $b_+$, $\tau_+$**

If the authors of the above paper are willing to teach us, it will be our pleasure to contact with you. Thanks!

My email: braintsai2000gmail.com

### clustering.ipynb:
for clustering 

### script.ipynb:
for seeing the result.

It is originally for executing some testing code.


