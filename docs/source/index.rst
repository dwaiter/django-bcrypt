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

Any new passwords set will be hashed with bcrypt.  Old passwords will still work
fine.


Configuration
-------------

You can configure how django-bcrypt behaves with a few settings in your
``settings.py`` file.

``BCRYPT_ENABLED``
``````````````````

Enables bcrypt hashing when ``User.set_password()`` is called.

Default: ``True``

``BCRYPT_ENABLED_UNDER_TEST``
`````````````````````````````

Enables bcrypt hashing when running inside Django TestCases.

Default: ``False`` (to speed up user creation)

``BCRYPT_ROUNDS``
`````````````````

Number of rounds to use for bcrypt hashing.  Increase this as computers get faster.

You can change the number of rounds without breaking already-hashed passwords.  New
passwords will use the new number of rounds, and old ones will use the old number.

Default: ``12``

``BCRYPT_MIGRATE``
``````````````````

Enables bcrypt password migration on a ``check_password()`` call.

The hash is also migrated when ``BCRYPT_ROUNDS`` changes.

Default: ``False``


Acknowledgements
----------------

This is pretty much a packaged-up version of `this blog post`_ for easier use.

It also depends on the `py-bcrypt`_ library.

.. _this blog post:
   http://kfalck.net/2010/12/27/blogi-linodessa-ja-bcrypt-kaytossa

.. _py-bcrypt:
   http://www.mindrot.org/projects/py-bcrypt/
