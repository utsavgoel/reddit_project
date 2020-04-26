# reddit_project

This project is aimed to predict the flair of a reddit post. Currently, it is trained only on the r/india posts.<br><br>

Input to the system: URL to an r/india post.<br>
Output: A JSON object containing the URL and flair corresponding to the post.<br>
Project is live at: https://afternoon-falls-83076.herokuapp.com/<br><br>

To reproduce:
1. Clone the repository and install the requirements, 'pip install requirements.txt'.
2. Unzip the classifier model in  classifier_website/res directory.
3. Run Django server, 'python manage.py runserver' (Default opens at port 8000, 127.0.0.1:8000)

Known Issues:
Accuracy can be improved.




