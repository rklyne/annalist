# Installing and setting up Annalist


## Prerequisites

* A Unix-like operating system: Annalist has been tested with MacOS 10.9 and Linux 14.04.  Other versions should be usable.
* Python 2.7 (see [Python beginners guide / download](https://wiki.python.org/moin/BeginnersGuide/Download)).
* virtualenv (includes setuptools and pip; see [virtualenv introduction](http://virtualenv.readthedocs.org/en/latest/virtualenv.html)).


## Installing software

The following assumes that software is installed under a directory called $WORKSPACE; i.e. Annalist software is installed to $WORKSPACE/annalist.  This could be a user home directory.

1.  Check the version of python installed on your system.  An easy way is to just enter the `python` to see a displaty like this:

        $ python
        Python 2.7.5 (default, Aug 25 2013, 00:04:04) 
        [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
        Type "help", "copyright", "credits" or "license" for more information.
        >>> 

    If the default version shown by this command is not 2.7.x, it may still be possible to run a 2.7 version with a command like:

        $ python2.7
        Python 2.7.5 (default, Aug 25 2013, 00:04:04) 
        [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
        Type "help", "copyright", "credits" or "license" for more information.
        >>> 

    (On Linux/Unix systems, typing `python<tab>` may help to shopw what versions are installed.)

    In this case, you will need to use the `-p` option when running `virtualenv` to create a python environment for Annalist (see below).


2.  Go to the workspace directory, create a Python virtual environment and activate it (i.e. make it the current Python environment).  This avids having the Annalist installation stomp over any otrher python installation, and makes it very easy to discard if or when it is not required.

        cd $WORKSPACE
        virtualenv annenv
        source annenv/bin/activate

    In an environment where the are multiple versions of Python installed, a `virtualenv` command like this might be needed to ensure that the appropriate version of Python is used:

        virtualenv -p python2.7 annenv

3.  Obtain a copy of the Annalist distribution kit, e.g. from @@TODO, and copy to a conventient location (e.g., $WORKSPACE/Annalist-0.1.2.tar.gz).  Then install it thus:

        pip install $WORKSPACE/Annalist-0.1.2.tar.gz

4.  Alternatively, install the software from PyPI (@@TODO: will be uploaded to PyPI when the initial release is stabilized):

        pip install annalist

5.  Finally, test the installed software:

        annalist-manager runtests

    The output from this command should look something like this:

        INFO:annalist_site.settings.runtests:Annalist version 0.1.2 (test configuration)
        INFO:annalist_site.settings.runtests:SETTINGS_MODULE: annalist_site.settings.runtests
        INFO:annalist_site.settings.runtests:BASE_DATA_DIR:   /home/annalist/anenv/lib/python2.7/site-packages/annalist_root/sampledata/data
        INFO:annalist_site.settings.runtests:CONFIG_BASE:     /home/annalist/.annalist/
        INFO:annalist_site.settings.runtests:DJANGO_ROOT:     /home/annalist/anenv/lib/python2.7/site-packages/django
        INFO:annalist_site.settings.runtests:SITE_CONFIG_DIR: /home/annalist/anenv/lib/python2.7/site-packages/annalist_root/annalist_site
        INFO:annalist_site.settings.runtests:SITE_SRC_ROOT:   /home/annalist/anenv/lib/python2.7/site-packages/annalist_root
        INFO:annalist_site.settings.runtests:DB PATH:         /home/annalist/anenv/lib/python2.7/site-packages/annalist_root/db.sqlite3
        Creating test database for alias 'default'...
        ..........................................................................................................................................................................................................................................................................................................................................................
        ----------------------------------------------------------------------
        Ran 346 tests in 35.321s

        OK
        Destroying test database for alias 'default'...


## Setting up an Annalist site

Before setting up an Annalist configuration, theer are two issues to be aware of.  Or if you just want a quick installation for evaluation purposes, skip ahead to "Initial site setup",

### Annalist site options

Annalist deploymemnt details are controlled by files in the `src/annalist_rot/annalist_site/settings` directory.  Annalist comes with three pre-defined configurations: deveopment, personal, and shared.  The main differences between these are the location of the Annalist site data files, and the location of certain private configuration files.  (Other configuration options are possible by defining a new settings file.)

**Development**: Annalist site data is kept in a directory within the Annalist software source tree, and configuration files are in subdirectory `.annalist` of the installing user's home directory.

**Personal**: Annalist site data is in a sibdirectory `annalist_site`, and configuration files are in subdirectory `.annalist`, of the installing user's home directory.

**Shared**: Annalist site data is kept in directory `/var/annalist_site`, and configuration files are in subdirectory `/etc/annalist`.  Such an installation will typically require root privileges on the host computer system to complete.

### Analist authentication options

Annalist has been implemented to use federated authentication based on Open ID Connect (http://openid.net/connect/) rather than local user credential management.  Using third party authentication services should facilitate integration with single-sign-on (SSO) services, and avoids the security risks assciated with local password storage.  Unfortunately, installing and configuring a system to use an OpenID Connect authentication service does take some addtional effort to register the installed application with the authentication service.

Annalist currently supports two user authentication mechanisms: OpenID Connect using Google+, and local user login credentials.  (Other OpenID Connect providers may also work, but have not been tested.)


#### OpenID Connect using Google+

Annalist OpenID Connect authentication has been tested with Google+ identity service.  Instructions for configuring a new installation to work with Google+ are in the [Annalist README](https://github.com/gklyne/annalist/blob/master/README.md). (@@TODO: _move to separate document and update link_)

The configuration details for using an OpenID Connect provider are stored in a private area, away from the Annalist source files and site data, since they contain private keying data.  A subdirectory `providers` of the Annalist configuration directory contains a description file for weach supported OpenID Connect provider.  New providers may be supported by adding descrtiption files to this directory.  The provider description for Google may be a useful example for creating descriptions for other providers.  (But be aware that different providers will have different registration procedures, and may require subtlely different forms of configuration information.)


#### Local user database

Annalist can also allow users to log in using locally stored credentials, which may be useful for quick evaluation deployments but is not the recommended mechanism for normal operational use.

When installing Annalist, an administration account may be created using the `annalist-manager` tool.  When logged in to Annalist using this account, the `admin` link in the footer of most Annalist pages will allow new user accounts to be created via the Django admin interface.  More documentation about using this admin intrefcae is in the [The Django Admin Site](http://www.djangobook.com/en/2.0/chapter06.html), which isChapter 6 of [The Django Book](http://www.djangobook.com/en/2.0/index.html).


### Initial site setup

These instructions use the example of a development configuration (`devel`) and a local user database: these options are not suitable for a full deployment, but are probably the least intrusive to use for early evaluation purposes.

1.  The commands must be issued with the annalist python environment activated.  If needed, use a command like this:

        source annenv/bin/activate

2.  Initialize user management database

        annalist-manager initialize --development

3.  Initialize sitedata (don't do this if updating annalist software to use existing site data)

        annalist-manager createsitedata --development

4.  Create admin user

        annalist-manager createadminuser --development

    Respond to the prompts with a username, email address and password.  The username may be up to 30 characters, and may consist of letters, digits and underscores.

5.  Start the Annalist server

        annalist-manager runserver --development

You should now be able to use a browser to view the Annalist server, e.g. at http://localhost:8000.


## Accessing Annalist

The following instructions assume abrowser running on the same host as the Annalistr service.  If a differemnt host is used, replace `localhost` with the name or IP address of the host that is running the Annalist server.

1.  Browse to annalist server at http://localhost:8000 (replacing `localhost` as needed)

    An empty list of collections should be displayed, along with some help text:

    ![Initial front page](screenshots/Front-page-initial.png)

2.  Select the **Login** item from the top menu bar:

    ![Initial login page](screenshots/Login-initial.png)

3.  Select the Local user credentials 'login' link at the bottom of the page:

    ![Django login page](screenshots/Login-django.png)

4.  Enter the admin user credentials specified previously when creating the Annalist admin user, and click the 'Login' button:

5.  Click the **Home** link on the tp menu bar to return to the front page:

    ![Initial front page](screenshots/Front-page-admin.png)

    Note that the front page now shows text entry boxes and a button for creating a new connection.

At this point, the **Admin** link in the page footer can be used to create additional local users via the local administrative interface (which is implemented in the underlying Django web application framework).  Or just continue straight to create an initial dara collection.


## Create a collection

This section assumes you are logged in to an Annalist system.

To create a new _collection_, which is an Annalist unit of adminstratable and copyable data, enter a short name for the collection (consisting of just letters, digits and/or underscorte (`'_'`) characters) and a one-line label or description (which can contain arbitrary characters) into the text boxes presented:

![Front page with details for new collection entered](screenshots/Front-page-collection-details.png)

Now click on the 'New' button:

![Front page showing new collection created](screenshots/Front-page-collection-created.png)

Click on the link in the Id column to view the new collection:

![Initial view of new collection](screenshots/Collection-initial-view.png)

From this screen, you can start to add data to this collection.  For more information, see [Using Annalist](using-annalist.md)

