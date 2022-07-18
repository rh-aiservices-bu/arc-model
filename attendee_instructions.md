# AR Coupons Workshop - Instructions

* [Workshop Environment.](#workshop-environment)
  * [for Red Hat Employees](#for-red-hat-employees)
  * [for the general public](#for-the-general-public)
* [Accessing and testing your deployed Application](#accessing-and-testing-your-deployed-application)
* [Retraining the model](#retraining-the-model)
  * [Logging into RHODS](#logging-into-rhods)
  * [Git clone the **arc-model** project](#git-clone-the-arc-model-project)
  * [Retrain the model](#retrain-the-model)
  * [Publish the changes](#publish-the-changes)
* [Reviewing the OpenShift Pipeline](#reviewing-the-openshift-pipeline)
  * [Reviewing the pipeline run](#reviewing-the-pipeline-run)
  * [Retrain the model (again).](#retrain-the-model-again)
  * [Watch the build.](#watch-the-build)
* [GitOps and how it helps to manage ML Model LifeCycle (MLOps way).](#gitops-and-how-it-helps-to-manage-ml-model-lifecycle-mlops-way)



TODOS (priority hi->low):
- fill in instructions left out (will need to launch a lab to do these parts to make sure they're accurate).
- fill in instructions on what to do if we run out of environments.
- update link to sheet to sheet that anyone from outside RH can access.
- add images/screenshots.

## Workshop Environment.

### for Red Hat Employees

If you are a Red Hat employee, you can reserve the workshop environment using the [RHPDS](https://rhpds.redhat.com/) system.

![](instructions/rhpds.png)

### for the general public

If you do not work for Red Hat, an environment will be provided for you as part of the workshop.

**(Update with instructions for automated ID method).**

* [Current link to sheet](https://docs.google.com/spreadsheets/d/12tr4yU-Rhl78suCeFIJqrQyfvimrOv-HA_1IrDtvMeg/edit#gid=0)

To claim an environment, simply enter your name in the first column of any open row containing environment info. This row will now contain all the links and logins you should need to complete our workshop.

If there are no available environments, ____.

## Accessing and testing your deployed Application

As part of the bootstrapping of your environment, an initial instance of your application was deployed.
Let's review it and confirm it works as expected.

1. Follow the link to your 'OpenShift Console URL'
1. Log in using the username and password for the OpenShift admin account
1. Navigate to **Networking**, then **Routes**.
1. Select the project called **rhods-prod**.
1. You will see a route called ****
1. Click on the matching hyperlink
1. This will open the app in your browser.
1. It will ask to use the Webcam. Allow it to do so.
1. If you scan items with the app , you should see something like ...
1. You can also e-mail your App's URL to your phone in order to use it as a scanner.

Try taking a picture of yourself or of a water bottle and wait to see if the app predicted a discount on an item on the image. It can detect clothing (on you), water bottles, and footwear. If the model doesn't show a box and a discount around an item the first time, try again.

We can now move on to the next step.

## Retraining the model

The initial version of the discounting model was built using a dataset called [monday.csv](discount_data/datasets/monday.csv).

In this section, we will:
* log into RHODS
* Clone the project from your on-cluster gitea instance
* Retrain the model with fresher data
* Publish our changes

### Logging into RHODS

* Open RHODS (Red Hat OpenShift Data Science) by following the link contained in your environment sheet row 'RHODS URL'.
* Now, login by entering the username and password for RHODS located next to the 'RHODS URL' column.
* Once in RHODS, we now need to clone our repository so we can do some training.

### Git clone the **arc-model** project

Each provided environment comes with a dedicated instance of **Gitea** so that each student can easily and inpendantly make updates into it.

* In the OpenShift Console, navigate to **Network** and then **Routes**.
* Select the project called .... gitea?
* You should see the gitea URL. Click on the URL.
* Log in to Gitea as user `lab-user` with password `openshift`.
* Navigate to the **arc-model** git repo.
* Click on the link in order to get the Git Clone URL.
* Copy that URL to your clipboard.
* Navigate back to RHODS
* Click on the git icon
* Choose the **Clone** option
* Paste the URL and click Clone.
* Change the branch from `main` to `dev`

### Retrain the model

Now that we've cloned the project, let's retrain the model.

* Open the Notebook called `5_discount_model.ipynb` from the RHODS file system tab
* This notebook contains the code for training our discount model.
* In the third cell see how we are using a dataset called 'discount_data/datasets/monday.csv'.
* Let's replace that with a path to our data from tuesday,
* type in or copy paste 'discount_data/datasets/tuesday.csv'.
* Now click on 'Restart Kernel and Run all Cells' (ADD SCREENSHOT) to train our model on the new data.
* Doing so has update the file .... and ....., but not .....


### Publish the changes

We have now updated our model files as well as our discount model training notebook.
We should push our changes that we've made in the dev branch!

* Open up the notebook titled '6_git_commit_and_push.ipynb'.
* Click on the 'Restart Kernel and Run all Cells'
* Doing this will automatically Commit our changes into the local git repo, and then push those commits back into the Gitea instance.

## Reviewing the OpenShift Pipeline

In the previous steps, we pushed our changes back into the Gitea repo.

In this environment, an OpenShift pipeline has been configure to automatically run every time something is pushed to Gitea.

### Reviewing the pipeline run

Our dev app should automatically rebuild since that we've pushed our changes to the git repository. Navigate to the Pipeline Builds tab in your OpenShift Console tab, and click on the most recent build.

We can see it's failed! Try clicking on the sanity check step and looking at the logs to find our what went wrong.

We can see our model failed our check, and stopped the pipeline.

### Retrain the model (again).

Let's fix this! Clearly we had a problem with our data - luckily we received the data from wednesday which our data engineers have promised will be correct.

Again, go to '5_discount_model.ipynb' notebook in your RHODS tab. Let's use the new data from wednesday, update that same cell with 'discount_data/datasets/tuesday.csv'. Now, rerun the notebook by clicking 'Restart Kernel and Run All'. This will update the discount model with a new discount model trained on wednesday's data.

Run the notebook '6_git_commit_and_push.ipynb' again to commit and push our model changes to our dev git repo.

### Watch the build.

Let's look at the pipeline build in the OpenShift Console tab. We can see the pipeline build will run now, and can take a look at our sanity check step in the pipeline to see the the log and see our model has passed our predefined tests.

## GitOps and how it helps to manage ML Model LifeCycle (MLOps way).

Lets look at CICD process and how if follows the GitOps principles. Also walk through the OpenShift Pipeline and OpenShift GitOps console.

OpenShift Pipeline does continuous integration. Once you push your code/model to your respository, it will automatically trigger pipeline to test the new model, build it and deploy it in dev environment. The OpenShift Pipeline do not have any control over deployment on PROD.

OpenShift GitOps does have control over prod environment, based on the changes to its prod image it will trigger auto deployment of the new image into prod.

You see the CI and CD processes are separately running and OpenShift Pipelines (where dev team works) do not have access to change anything in production project.

Also change in code (e.g. change in image tag in prod using Kustomize) triggers change in prod container update with the new image and new model.

No one touches the production environment directly and updates the image, rather its all followed through change in code, managed through git and completely auditable and reversible if required.
