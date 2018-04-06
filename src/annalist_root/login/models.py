"""
OAuth2 / OpenID Connect authentication related models

NOTE: the database creation logic appears to be sensitive to the name of thos module!!
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, 2016, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import base64
import pickle

from django.db import models
from django.contrib.auth.models import User

# =============================================================================
#
#   The following storage and field classes have been copied from
#   the now-deprecated oauth2client package.  They provide mechanisms 
#   for storing OAuth2 credential informnation in a Django database.
#
#   To this end, Annalist uses an additional model, "CredentialsModel", which
#   associates an OAuth2 credential (containing an authenticated email address)
#   with a Django user.
#
# =============================================================================

class BaseStorage(object):
        """
        Base class for all Storage objects.

        Store and retrieve a single credential. This class supports locking
        such that multiple processes and threads can operate on a single
        store.
        """

        def acquire_lock(self):
                """Acquires any lock necessary to access this Storage.

                This lock is not reentrant.
                """
                pass

        def release_lock(self):
                """Release the Storage lock.

                Trying to release a lock that isn't held will result in a
                RuntimeError.
                """
                pass

        def locked_get(self):
                """Retrieve credential.

                The Storage lock must be held when this is called.

                Returns:
                        oauth2client.client.Credentials
                """
                _abstract()

        def locked_put(self, credentials):
                """Write a credential.

                The Storage lock must be held when this is called.

                Args:
                        credentials: Credentials, the credentials to store.
                """
                _abstract()

        def locked_delete(self):
                """Delete a credential.

                The Storage lock must be held when this is called.
                """
                _abstract()

        def get(self):
                """Retrieve credential.

                The Storage lock must *not* be held when this is called.

                Returns:
                        oauth2client.client.Credentials
                """
                self.acquire_lock()
                try:
                        return self.locked_get()
                finally:
                        self.release_lock()

        def put(self, credentials):
                """Write a credential.

                The Storage lock must be held when this is called.

                Args:
                        credentials: Credentials, the credentials to store.
                """
                self.acquire_lock()
                try:
                        self.locked_put(credentials)
                finally:
                        self.release_lock()

        def delete(self):
                """Delete credential.

                Frees any resources associated with storing the credential.
                The Storage lock must *not* be held when this is called.

                Returns:
                        None
                """
                self.acquire_lock()
                try:
                        return self.locked_delete()
                finally:
                        self.release_lock()

class Storage(BaseStorage):
    """
    Store and retrieve a single credential to and from
    the datastore.

    This Storage helper presumes the Credentials
    have been stored as a CredenialsField
    on a db model class.
    """

    def __init__(self, model_class, key_name, key_value, property_name):
        """Constructor for Storage.

        Args:
            model: db.Model, model class
            key_name: string, key name for the entity that has the credentials
            key_value: string, key value for the entity that has the credentials
            property_name: string, name of the property that is an CredentialsProperty
        """
        self.model_class = model_class
        self.key_name = key_name
        self.key_value = key_value
        self.property_name = property_name

    def locked_get(self):
        """Retrieve Credential from datastore.

        Returns:
            oauth2client.Credentials
        """
        credential = None

        query = {self.key_name: self.key_value}
        entities = self.model_class.objects.filter(**query)
        if len(entities) > 0:
            credential = getattr(entities[0], self.property_name)
            if credential and hasattr(credential, 'set_store'):
                credential.set_store(self)
        return credential

    def locked_put(self, credentials):
        """Write a Credentials to the datastore.

        Args:
            credentials: Credentials, the credentials to store.
        """
        args = {self.key_name: self.key_value}
        entity = self.model_class(**args)
        setattr(entity, self.property_name, credentials)
        entity.save()

    def locked_delete(self):
        """Delete Credentials from the datastore."""

        query = {self.key_name: self.key_value}
        entities = self.model_class.objects.filter(**query).delete()

class CredentialsField(models.Field):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(CredentialsField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if value is None:
            return None
        # if isinstance(value, oauth2client.client.Credentials):
        #   return value
        return pickle.loads(base64.b64decode(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return base64.b64encode(pickle.dumps(value))

# =============================================================================
#
#   Here, we define the model that assocuates an OAuth2 credential with a User,
#   and provides a mathod to access the credential.
#
# =============================================================================

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

def get_user_credential(userid):
    storage = Storage(CredentialsModel, 'id', userid, 'credential')
    return storage.get()

# End.
