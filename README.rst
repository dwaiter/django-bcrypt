django-bcrypt
=============

`You should be using bcrypt`_.

.. _You should be using bcrypt:
   http://codahale.com/how-to-safely-store-a-password/

django-bcrypt makes it easy to use bcrypt to hash passwords with Django.


Installation and Usage
----------------------

Install the package with `pip`_ and `Mercurial`_ or `git`_::

    pip install -e hg+http://bitbucket.org/dwaiter/django-bcrypt#egg=django-bcrypt
    
    # or ...
    
    pip install -e git://github.com/dwaiter/django-bcrypt.git#egg=django-bcrypt

.. _pip: http://pip.openplans.org/
.. _Mercurial: http://hg-scm.org/
.. _git: http://git-scm.com/

Add ``django_bcrypt`` to your ``INSTALLED_APPS``.

That's it.

Any new passwords set will be hashed with bcrypt.  Old passwords will still
work fine.


Configuration
-------------

You can set ``BCRYPT_ROUNDS`` in ``settings.py`` to change the number of
rounds django-bcrypt uses.  The default is ``12``.

You can change the number of rounds without breaking already-hashed passwords.
New passwords will use the new number of rounds, and old ones will use the old
number.


Acknowledgements
----------------

This is pretty much a packaged-up version of `this blog post`_ for easier
use.

It also depends on the `py-bcrypt`_ library.

.. _this blog post:
   http://kfalck.net/2010/12/27/blogi-linodessa-ja-bcrypt-kaytossa

.. _py-bcrypt:
   http://www.mindrot.org/projects/py-bcrypt/
