---
title: Creating web apps with Flask in Azure
description: A tutorial that introduces you to running a Flask Python web app on Azure.
services: app-service\web
documentationcenter: python
tags: python
author: Cody Farmer
manager:
editor: ''

ms.assetid: b7f4ca3a-0b52-4108-90a7-f7e07ac73da0
ms.service: app-service-web
ms.workload: web
ms.tgt_pltfrm: na
ms.devlang: python
ms.topic: article
ms.date: 07/18/2017
ms.author: cofarm

---
<<<<<<< HEAD
=======

>>>>>>> origin/master
# WORK IN PROGRESS
# Creating web apps with Flask in Azure
This tutorial describes how to get started running Python with Flask in [Azure App Service Web Apps](http://go.microsoft.com/fwlink/?LinkId=529714). Web Apps provides limited free hosting and rapid deployment, and you can use Python!  As your app grows, you can switch to paid hosting, and easily integrate with other Azure service offerings.

You will create an application named using the Flask web framework, a popular lightweight framework for Python web development. Other popular choices include Django and Bottle. We suggest reading our comprehensive guide on [managing Python on Azure App Service](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-on-azure-app-service), but this tutorial will cover the required portions to get your Flask application running. This application will be named FlaskWeb, and be deployed from your local Git repository.

[!INCLUDE [create-account-and-websites-note](../../includes/create-account-and-websites-note.md)]

> [!NOTE]
> If you want to get started with Azure App Service before signing up for an Azure account, go to [Try App Service](https://azure.microsoft.com/try/app-service/), where you can immediately create a short-lived starter web app in App Service. No credit cards required; no commitments.
>
>

## Prerequisites
* Windows, Mac or Linux
* Git
* Text/Code Editor (Notebook, atom.io, Visual Studio Code, etc.)
* [Python Tools for Visual Studio][Python Tools for Visual Studio] (PTVS) - Note: Optional, only for Visual Studio users

For Git on Windows, we recommend [Git for Windows] or [GitHub for Windows].  If you use Visual Studio, you can also use the integrated Git support. You will need to create a local Git repository that we will later use to deploy your Web App. For this example, we're naming the repository **FlaskWeb**.

We also recommend installing [Python Tools 2.2 for Visual Studio](https://github.com/Microsoft/PTVS/releases/v2.2.6).  This is optional, but if you have [Visual Studio], including the free Visual Studio Community 2016 or Visual Studio Express 2016 for Web, then this will give you a great Python IDE.


## Create a Web App in the Azure Portal
The first step in creating your app is to create the web app via the [Azure Portal](https://portal.azure.com). This can also be done with Azure CLI, but we won't be covering that here.

1. Log into the Azure Portal and click the **NEW** button in the bottom left corner.
2. Click **Web + Mobile**.
3. Click **Web App**.
4. Configure the Web App, such as creating a new App Service plan and a new resource group for it. Then, click **Create**.
5. Configure Git publishing for your newly created web app by following the instructions at [Local Git Deployment to Azure App Service](app-service-deploy-local-git.md).

## Python Configuration
Now that your web application is launched, we can begin customizing it for Flask. Our first task is to install the Python version of your choice. You can view the details of this in the [managing Python documentation](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-on-azure-app-service#choosing-a-python-version-through-the-azure-portal).

1. On the overview page, scroll down to **Development Tools**.
2. Select **Extensions > Add**.
3. Scroll through the list to find the version of Python you want. For this tutorial, we will be going with **Python 3.6.1 x64**.

## Environment
### Web Application Configuration Files
Our Flask Deployment will use Fast CGI to interface with the server. In order to accomplish this, we will need to add two files. One, a FastCGI interface file. We will create this file and name it **FlaskWeb.wsgi\_app**. Copy the following code into FlaskWeb.wsgi_app within your local Github repository for this project:
```python
    from FlaskWeb import app

    if __name__ == '__main__':
		from fcgi import WSGIServer
		WSGIServer(app).run()
```

Next we'll add a web.config file to your repository to tell Azure how your application is being run. Copy this XML into your **web.config** file:
```xml
    <?xml version="1.0" encoding="utf-8"?>
    <configuration>
      <appSettings>
    	<add key="PYTHONPATH" value="D:\home\site\wwwroot"/>
	    <add key="WSGI_HANDLER" value="FlaskWeb.wsgi_app"/>
	    <add key="WSGI_LOG" value="D:\home\LogFiles\wfastcgi.log"/>
      </appSettings>
      <system.webServer>
    	<handlers>
      		<add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" scriptProcessor="D:\home\Python361x64\python.exe|D:\home\Python361x64\wfastcgi.py" resourceType="Unspecified" requireAccess="Script"/>
    	</handlers>
      </system.webServer>
    </configuration>
```
This file references the specific file path that you have setup. If you weren't using Python3.6.1 then you will need to change the paths that use that folder - such as the scriptProcessor argument.



In order to easily configure the environment on the Web Application service to contain our dependencies, we will use a requirements.txt file to have the Pip installation installed with Python take care of the packages our application needs. The below code should be copied into a requirements.txt file in your repository:
    click==6.7
    Flask==0.12.2
    itsdangerous==0.24
    Jinja2==2.9.6
    MarkupSafe==1.0
    Werkzeug==0.12.2



With these files, we will be able to quickly configure the Azure Web App instance once we have pushed our Git Repository to Azure.

## Flask Development
Now we're ready to create our Flask application! For the purposes of our example, we're going to make a very simple Flask application.

Flask can be setup in a lot of different ways, and here we'll be making a very minimal application. There is a [tutorial here](http://flask.pocoo.org/docs/0.12/tutorial/) for Flask in general, that you may find instructive.

In the root of your Git repository (along with your configuration files), create a *FlaskWeb* folder. Underneath this folder, you should create a *static* and *templates* folder to look like this:

    /FlaskWeb
    	/Static
    	/Templates

In the FlaskWeb folder we're going to create two files - one to initialize our app and one to define it's actions. Create **__init__.py ** (two underscores on each side) and **views.py**.

*\_\_init__.py*
```python
"""
The flask application package.
"""
from flask import Flask
app = Flask(__name__)
import FlaskWeb.views
```
*views.py*
```python
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWeb import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
```

> [!NOTE]
> Indentation is important in Python!

These two files establish the package **FlaskWeb** so we can import it, and provide routing for our requests to render templates using Jinja2.

As you may have guessed from the above code, we're going to create three pages - all based off one shared template.
*layout.html*
```xml
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My Flask Application</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
     crossorigin="anonymous">
     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"
     integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">Application name</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="{{ url_for('home') }}">Home</a></li>
                    <li><a href="{{ url_for('about') }}">About</a></li>
                    <li><a href="{{ url_for('contact') }}">Contact</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {% block content %}{% endblock %}
        <hr />
        <footer>
            <p>&copy; {{ year }} - My Flask Application</p>
        </footer>
    </div>

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
     crossorigin="anonymous"></script>
    {% block scripts %}{% endblock %}

</body>
</html>
```


## Troubleshooting - Package Installation
[!INCLUDE [web-sites-python-troubleshooting-package-installation](../../includes/web-sites-python-troubleshooting-package-installation.md)]

## Troubleshooting - Virtual Environment
[!INCLUDE [web-sites-python-troubleshooting-virtual-environment](../../includes/web-sites-python-troubleshooting-virtual-environment.md)]

## Next Steps
Follow these links to learn more about Flask and Python Tools for Visual Studio:

* [Flask Documentation]
* [Python Tools for Visual Studio Documentation]

For information on using Azure Table Storage and MongoDB:

* [Flask and MongoDB on Azure with Python Tools for Visual Studio]
* [Flask and Azure Table Storage on Azure with Python Tools for Visual Studio]

For more information, see also the [Python Developer Center](/develop/python/).

<!--Link references-->
[Flask and MongoDB on Azure with Python Tools for Visual Studio]: https://github.com/microsoft/ptvs/wiki/Flask-and-MongoDB-on-Azure
[Flask and Azure Table Storage on Azure with Python Tools for Visual Studio]: web-sites-python-ptvs-flask-table-storage.md

<!--External Link references-->
[Azure SDK for Python 2.7]: http://go.microsoft.com/fwlink/?linkid=254281
[Azure SDK for Python 3.4]: http://go.microsoft.com/fwlink/?linkid=516990
[python.org]: http://www.python.org/
[Git for Windows]: http://msysgit.github.io/
[GitHub for Windows]: https://windows.github.com/
[Python Tools for Visual Studio]: http://aka.ms/ptvs
[Python Tools 2.2 for Visual Studio]: http://go.microsoft.com/fwlink/?LinkID=624025
[Visual Studio]: http://www.visualstudio.com/
[Python Tools for Visual Studio Documentation]: http://aka.ms/ptvsdocs
[Flask Documentation]: http://flask.pocoo.org/
