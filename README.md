# AB Test - Wedding Booking Application

## Overview
AB Testing is used to assess whether a change in a system has led to an improvement. This project looks at the result of an A/B test to see if some changes should be made permanent. Two changes were analyzed (1 and 2) against a control variant (0).  

## Purpose
The purpose of this project is to experiment with an A/B test dataset, and create some reusable code if this task is encountered again.

## Independent Features
The key independent features are shown below. In this A/B test these features should be unchanged across the test variants. For example, we shouldn't expect to see a change in the 'device' type distribution across test variants (this might influence the results). The AB_test class plots the distribution of these features (for each test variant) to see if there is any change.

**regTime** (timestamp of when the user registered). **primaryAccount** (True if the user registered without being invited to collaborate on an existing wedding), **device**: (device used when registering), **ap**p: (whether or not the app was used (as opposed to website)), **browser**: (browser type), **screenHeight**, **screenWidth**, **authMethod**	(authentication method used when registering, **locationStep**	(whether the user saw/skipped/completed the location step on onboarding), **addedCity**	(whether the user added city or county level information when adding location information (0: False, 1: True)), **addedGuestCount**	(whether the user added guest count estimate on onboarding (0: False, 1: True)), **addedBudget**	(whether the user added budget estimate on onboarding (0: False, 1: True)), **invitedCollaborator**	(whether the user invited a collaborator to the profile during onboarding), **addedNames**	(whether the user entered the names of the couple during onboarding).

## Dependent Features
The dependent features are outcomes which the tests are trying to improve. In this specific test the aim is to improve the number of searches / user engagement. The features are shown below.

**searchCTA** (whether the user used the search CTA on the final screen of onboarding (0: False, 1: True)), **venEnq** (number of enquiries sent to venues by the user in their first week), **venSearch**	(number of searches for venues performed by the user in their first week), **venViews**	(number of venue profile views performed by the user in their first week), **sessions**	(number of sessions the user had in their first week).

## Usage
The class **AB_test** contains all of the functionality for the AB_test. It has three key methods
- **ind_feature_plots()**: This plots the distribution for the independent variables for each test variant.
- **dep_feature_analysis()**: This returns statistics for each of the dependent features for each test variant.
- **one_tail_binomial_AB_test()**: This conducts a one-tail binomial test on the probability of success (suitable for binary outcomes).

Usage of the AB_test is shown below.
```
data = AB_test(df)
data.ind_feature_plots("testVariant", shape = (3,4), figsize = (19,14), remove = ['testVariant', 'locationStep', 'addedCity',
                     'finOnb', 'searchCTA', 'venEnq', 'venSearch', 'venViews','sessions'])
data.dep_feature_analysis('testVariant', ['searchCTA', 'venEnq', 'venSearch', 'venViews','sessions'])
```

## Results
**Independent features** - The independent features for each test variant were all very similar in their distributions. This means that changes in the dependent features are most likely to be driven by the A/B test.

**Test 1** - The probability of a user searching for venues after onboarding was 0.461 (the control variant was 0.453). However, the average number of enquiries a user makes dropped to 0.875 (from 0.921). 

**Test 2** - The probability of a user searching for venues after onboarding was 0.52 (the control variant was 0.453). However, the average number of enquiries a user makes dropped to 0.688 (from 0.921).

**Summary** - There is little evidence of a significant improvement in the A/B test. Although some dependent features improve, the key metric of venue enquiries does not improve. 





