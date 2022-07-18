# Initial draft of attendee instructions.


TODOS (priority hi->low):
- fill in instructions left out (will need to launch a lab to do these parts to make sure they're accurate).
- fill in instructions on what to do if we run out of environments.
- update link to sheet to sheet that anyone from outside RH can access.
- add images/screenshots.

## 1. Claim an environment from the sheet.

**(Update with instructions for automated ID method).**

### [Current link to sheet](https://docs.google.com/spreadsheets/d/12tr4yU-Rhl78suCeFIJqrQyfvimrOv-HA_1IrDtvMeg/edit#gid=0)

To claim an environment, simply enter your name in the first column of any open row containing environment info. This row will now contain all the links and logins you should need to complete our workshop.

If there are no available environments, ____.

## 2. Connect to the environment.

Now that you have an environment, let's connect to our app and see it in action.

Follow the link to your 'OpenShift Console URL', and log in using the username and password for OpenShift. 

INSTRUCTIONS FOR FINDING THE ROUTE TO THE APP HERE.

## 3. Test the webapp

In the webapp you'll likely be asked to give the app permissions to use your webcam - click allow.

Try taking a picture of yourself or of a water bottle and wait to see if the app predicted a discount on an item on the image. It can detect clothing (on you), water bottles, and footwear. If the model doesn't show a box and a discount around an item the first time, try again. 

## 4. Retrain the model. 

Now, we've recieved new daily data for us to train our discount prediction model.

Open RHODS (Red Hat OpenShift Data Science) by following the link contained in your environment sheet row 'RHODS URL'. Now, login by entering the username and password for RHODS located next to the 'RHODS URL' column. Once in RHODS, we now need to clone our repository so we can do some training. 

Let's log into our Gitea instance, do so by following your 'Gitea URL' in the environment sheet, and then entering the corresponding username and password.

Now, click on the repository called 'rhods-app' (UPDATE THIS WITH CORRECT NAME).

From here, click on the copy button (ADD SCREENSHOT).

Now, go back to your RHODS tab, and click on the Git icon on the left hand side (ADD SCREENSHOT), then click 'Clone Repository', paste the repository link you just copied, then hit clone. While in the git tab, select the 'dev' branch - this is where we'll be working.

Open the Jupyter Notebook called '5_discount_model.ipynb' from the RHODS file system tab - this notebook contains the code for training our discount model. If you have never worked with Jupyter Notebooks before, and need help, follow this link for a tutorial on notebooks (FIND LINK FOR THIS).

In the third cell see how we are using a dataset called 'discount_data/datasets/monday.csv'. Let's replace that with a path to our data from tuesday, type in or copy paste 'discount_data/datasets/tuesday.csv'. Now click on 'Restart Kernel and Run all Cells' (ADD SCREENSHOT) to train our model on the new data.

## 5. Push our changes.

We have now updated our model files as well as our discount model training notebook - we should push our changes that we've made in the dev branch! 

Open up the notebook titled '6_git_commit_and_push.ipynb'. 

## 6. Look at the pipeline builds.

Our dev app should automaticaly rebuild since that we've pushed our changes to the git repository. Navigate to the Pipeline Builds tab in your OpenShift Console tab, and click on the most recent build. 

We can see it's failed! Try clicking on the sanity check step and looking at the logs to find our what went wrong. 

We can see our model failed our check, and stopped the pipeline. 

## 7. Retrain the model (again).

Let's fix this! Clearly we had a problem with our data - luckily we recieved the data from wednesday which our data engineers have promised will be correct. 

Again, go to '5_discount_model.ipynb' notebook in your RHODS tab. Let's use the new data from wednesday, update that same cell with 'discount_data/datasets/tuesday.csv'. Now, rerun the notebook by clicking 'Restart Kernel and Run All'. This will update the discount model with a new discount model trained on wednesday's data.

Run the notebook '6_git_commit_and_push.ipynb' again to commit and push our model changes to our dev git repo. 

## 8. Watch the build.

Let's look at the pipeline build in the OpenShift Console tab. We can see the pipeline build will run now, and can take a look at our sanity check step in the pipeline to see the the log and see our model has passed our predefined tests.

## 9. Git Ops and how it helps to manage ML Model LifeCycle (MLOps way).

Lets look at CICD process and how if follows the GitOps principles. Also walk through the OpenShift Pipeline and OpenShift GitOps console.
OpenShift Pipeline does continuous integration. Once you push your code/model to your respository, it will automatically trigger pipeline to test the new model, build it and deploy it in dev environment. The OpenShift Pipeline do not have any control over deplyment on PROD.
OpenShift GitOps does have control over prod environment, based on the changes to its prod image it will trigger auto deployment of the new image into prod.
You see the CI and CD processes are separately running and OpenShift Pipelines (where dev team works) do not have access to change anything in production project.
Also change in code (e.g. change in image tag in prod using Kustomize) triggers change in prod container update with the new image and new model. 
No one touches the production environment directly and updates the image, rather its all followed through change in code, managed through git and completely auditable and reversible if required.
