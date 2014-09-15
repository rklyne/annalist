"""
Create Annalist/Django site data.
"""

from __future__ import print_function

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import sys
import logging
import subprocess
import importlib
import shutil

log = logging.getLogger(__name__)

from utils.SetcwdContext    import ChangeCurrentDir

from annalist.layout        import Layout

import am_errors
from am_settings            import am_get_settings

def am_createsite(annroot, userhome, options):
    """
    Create Annalistr/Django superuser account.  

    Once created, this can be used to create additional users through the 
    site 'admin' link.

    annroot     is the root directory for theannalist software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    settings = am_get_settings(annroot, userhome, options)
    if not settings:
        print("Settings not found (%s)"%(options.configuration), file=sys.stderr)
        return am_errors.AM_NOSETTINGS
    options.configuration = "runtests"
    testsettings = am_get_settings(annroot, "/nouser/", options)
    if not testsettings:
        print("Settings not found (%s)"%("runtests"), file=sys.stderr)
        return am_errors.AM_NOSETTINGS
    if len(options.args) > 0:
        print("Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), file=sys.stderr)
        return am_errors.AM_UNEXPECTEDARGS
    status = am_errors.AM_SUCCESS
    emptysitedir = os.path.join(annroot, "sampledata/empty/annalist_site")
    sitesettings = importlib.import_module(settings.modulename)
    sitebasedir  = os.path.join(sitesettings.BASE_DATA_DIR, "annalist_site")
    # Test if old site exists
    if os.path.exists(sitebasedir):
        if options.force:
            # --- Remove old site data from target area
            print("Removing old Annalist site at %s"%(sitebasedir))
            log.info("rmtree: %s"%(sitebasedir))
            shutil.rmtree(sitebasedir, ignore_errors=True)
        else:
            print("Old data already exists at %s (use --force lor -f to overwrite)"%(sitebasedir), file=sys.stderr)
            return am_errors.AM_EXISTS
    # --- Copy empty site data to target area
    print("Initializing Annalist site in %s"%(sitebasedir))
    log.info("copytree: %s to %s"%(emptysitedir, sitebasedir))
    shutil.copytree(emptysitedir, sitebasedir)
    # --- Copy built-in types and views data to target area
    site_layout = Layout(sitesettings.BASE_DATA_DIR)
    sitedatasrc = os.path.join(annroot, "annalist/sitedata")
    sitedatatgt = os.path.join(sitebasedir, site_layout.SITEDATA_DIR)
    print("Copy Annalist site data from %s to %s"%(sitedatasrc, sitedatatgt))
    for sdir in ("types", "lists", "views", "fields", "enums"):
        s = os.path.join(sitedatasrc, sdir)
        d = os.path.join(sitedatatgt, sdir)
        print("- %s -> %s"%(sdir, d))
        shutil.copytree(s, d)
    return status

# End.