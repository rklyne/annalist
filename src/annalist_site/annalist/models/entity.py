"""
Common base classes for Annalist stored entities (collections, data, metadata, etc.)

This module implements a common pattern whereby an entity is related to a parent,
with storage directories and URIs allocated by combining the parent entity and a
local identifier (slug) for the descendent.

Part of the purpose of this module is to abstract the underlying storage access
from the Annalist organization of presented entities.
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import os.path
import urlparse
import shutil
import json
import errno

import logging
log = logging.getLogger(__name__)

from django.conf                import settings

from annalist                   import util
from annalist.exceptions        import Annalist_Error
from annalist.identifiers       import ANNAL

from annalist.models.entityroot import EntityRoot

#   -------------------------------------------------------------------------------------------
#
#   Entity
#
#   -------------------------------------------------------------------------------------------

class Entity(EntityRoot):
    """
    This is the base class for all entities managed by Annalist as 
    descendents of some other entity.
    """

    _entitytype = ANNAL.CURIE.Entity
    _entitypath = None          # Relative path from parent to entity (template)
    _entityfile = None          # Relative reference to body file from entity
    _entityref  = None          # Relative reference to entity from body file
    _last_id    = None          # Last ID allocated

    def __init__(self, parent, entityid, altparent=None, idcheck=True):
        """
        Initialize a new Entity object, possibly without values.  The created
        entity is not saved to disk at this stage - see ._save() method.

        parent      is the parent entity from which the new entity is descended.
        entityid    the collection identifier for the collection
        altparent   is an alternative parent entity to search for this entity, using 
                    the alternative path for the entity type: this is used to augment 
                    explicitly created entities in a collection with site-wide 
                    installed metadata entites (i.e. types, views, etc.)
        """
        if idcheck and not util.valid_id(entityid):
            raise ValueError("Invalid entity identifier: %s"%(entityid))
        relpath = self.relpath(entityid)
        super(Entity, self).__init__(parent._entityuri+relpath, parent._entitydir+relpath)
        self._entityalturi = None
        self._entityaltdir = None
        if altparent:
            altpath = self.altpath(entityid)
            self._entityalturi = altparent._entityuri+altpath
            self._entityaltdir = altparent._entitydir+altpath
            log.debug("Entity.__init__: entity alt URI %s, entity alt dir %s"%(self._entityalturi, self._entityaltdir))
        self._entityid = entityid
        self._typeid   = parent.get_id() 
        log.debug("Entity.__init__: entity_id %s, type_id %s"%(self._entityid, self._typeid))
        return

    # I/O helper functions

    # Access functions

    @classmethod
    def allocate_new_id(cls, parent):
        if cls._last_id is None:
            cls._last_id = 1
        while True:
            newid = "%08d"%cls._last_id
            if not cls.exists(parent, newid):
                break
            cls._last_id += 1
        return newid

    @classmethod
    def relpath(cls, entityid):
        """
        Returns parent-relative path string for an identified entity of the given class.

        cls         is the class of the entity whose relative path is returned.
        entityid    is the local identifier (slug) for the entity.
        """
        log.debug("Entity.relpath: entitytype %s, entityid %s"%(cls._entitytype, entityid))
        relpath = (cls._entitypath or "%(id)s")%{'id': entityid}
        log.debug("Entity.relpath: %s"%(relpath))
        return relpath

    @classmethod
    def altpath(cls, entityid):
        """
        Returns parent-relative path string for an identified entity of the given class.

        cls         is the class of the entity whose alternative relative path is returned.
        entityid    is the local identifier (slug) for the entity.
        """
        log.debug("Entity.altpath: entitytype %s, entityid %s"%(cls._entitytype, entityid))
        altpath = (cls._entityaltpath or "%(id)s")%{'id': entityid}
        log.debug("Entity.altpath: %s"%(altpath))
        return altpath

    @classmethod
    def path(cls, parent, entityid):
        """
        Returns path string for accessing the body of the indicated entity.

        cls         is the class of the entity whose path is returned.
        parent      is the parent from which the entity is descended.
        entityid    is the local identifier (slug) for the entity.
        """
        log.debug("Entity.path: entitytype %s, parentdir %s, entityid %s"%
            (cls._entitytype, parent._entitydir, entityid)
            )
        assert cls._entityfile is not None
        p = util.entity_path(parent._entitydir, [cls.relpath(entityid)], cls._entityfile)
        log.debug("Entity.path: %s"%(p))
        return p

    @classmethod
    def create(cls, parent, entityid, entitybody):
        """
        Method creates a new entity.

        cls         is a class value used to construct the new entity value
        parent      is the parent entity from which the new entity is descended.
        entityid    is the local identifier (slug) for the new entity - this is 
                    required to be unique among descendents of a common parent.
        entitybody  is a dictionary of values that are stored for the created entity.

        Returns the created entity as an instance of the supplied class object.
        """
        log.debug("Entity.create: entityid %s"%(entityid))
        e = cls(parent, entityid)
        e.set_values(entitybody)
        e._save()
        return e

    @classmethod
    def _child_entity(cls, parent, entityid, altparent=None):
        """
        Instantiate a child entity (e.g. for create and load methods)
        """
        if altparent:
            e = cls(parent, entityid, altparent=altparent)
        else:
            e = cls(parent, entityid)
        return e

    @classmethod
    def load(cls, parent, entityid, altparent=None):
        """
        Return an entity with given identifier belonging to some given parent,
        or None if there is not such identity.

        cls         is the class of the entity to be loaded
        parent      is the parent from which the entity is descended.
        entityid    is the local identifier (slug) for the entity.
        altparent   is an alternative parent entity to search for the loaded entity, 
                    using the alternative path for the entity type.

        Returns an instance of the indicated class with data loaded from the
        corresponding Annalist storage, or None if there is no such entity.
        """
        log.debug("Entity.load: entitytype %s, parentdir %s, entityid %s"%
            (cls._entitytype, parent._entitydir, entityid)
            )
        e = cls._child_entity(parent, entityid, altparent=altparent)
        v = e._load_values()
        if v:
            e.set_values(v)
        else:
            e = None
        return e

    @classmethod
    def exists(cls, parent, entityid, altparent=None):
        """
        Method tests for existence of identified entity descended from given parent.

        cls         is the class of the entity to be tested
        parent      is the parent from which the entity is descended.
        entityid    is the local identifier (slug) for the entity.
        altparent   is an alternative parent entity to search for the tested entity, 
                    using the alternative path for the entity type.

        Returns True if the entity exists, as determined by existence of the 
        entity description metadata file.
        """
        log.debug("Entity.exists: entitytype %s, parentdir %s, entityid %s"%
            (cls._entitytype, parent._entitydir, entityid)
            )
        e = cls._child_entity(parent, entityid, altparent=altparent)
        return e._exists()

    @classmethod
    def remove(cls, parent, entityid):
        """
        Method removes an entity, deleting its details, data and descendents from Annalist storage.

        cls         is the class of the entity to be removed
        parent      is the parent from which the entity is descended.
        entityid    is the local identifier (slug) for the entity.

        Returns None on sucess, of a status value indicating a reason for value.
        """
        log.debug("Colllection.remove: id %s"%(entityid))
        e = cls.load(parent, entityid)
        if e:
            d = e._entitydir
            # Extra check to guard against accidentally deleting wrong thing
            if e['annal:type'] == cls._entitytype and d.startswith(parent._entitydir):
                shutil.rmtree(d)
            else:
                raise Annalist_Error("Entity %s unexpected type %s or path %s"%(entityid, e['type'], d))
        else:
            return Annalist_Error("Entity %s not found"%(entityid))
        return None

# End.
