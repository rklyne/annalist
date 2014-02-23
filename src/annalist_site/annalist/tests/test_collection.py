"""
Tests for collection module
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import json
import unittest

import logging
log = logging.getLogger(__name__)

from django.conf                import settings
from django.db                  import models
from django.http                import QueryDict
from django.core.urlresolvers   import resolve, reverse
from django.contrib.auth.models import User
from django.test                import TestCase # cf. https://docs.djangoproject.com/en/dev/topics/testing/tools/#assertions
from django.test.client         import Client

# from bs4                        import BeautifulSoup

# from miscutils.MockHttpResources import MockHttpFileResources, MockHttpDictResources

from annalist.identifiers       import ANNAL
from annalist                   import layout
from annalist.site              import Site
from annalist.collection        import Collection

from annalist.views.collection  import CollectionEditView

from tests                      import TestHost, TestHostUri, TestBasePath, TestBaseUri, TestBaseDir
from tests                      import dict_to_str, init_annalist_test_site
from AnnalistTestCase           import AnnalistTestCase

# Test assertion summary from http://docs.python.org/2/library/unittest.html#test-cases
#
# Method                    Checks that             New in
# assertEqual(a, b)         a == b   
# assertNotEqual(a, b)      a != b   
# assertTrue(x)             bool(x) is True  
# assertFalse(x)            bool(x) is False     
# assertIs(a, b)            a is b                  2.7
# assertIsNot(a, b)         a is not b              2.7
# assertIsNone(x)           x is None               2.7
# assertIsNotNone(x)        x is not None           2.7
# assertIn(a, b)            a in b                  2.7
# assertNotIn(a, b)         a not in b              2.7
# assertIsInstance(a, b)    isinstance(a, b)        2.7
# assertNotIsInstance(a, b) not isinstance(a, b)    2.7

class CollectionTest(TestCase):
    """
    Tests for Site object interface
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.testcoll = Collection(self.testsite, "testcoll")
        self.coll1 = (
            { '@id': '../'
            , 'id': 'coll1'
            , 'type': 'annal:Collection'
            , 'title': 'Name collection coll1'
            , 'uri': TestBaseUri+'/collections/coll1/'
            , 'annal:id': 'coll1'
            , 'annal:type': 'annal:Collection'
            , 'rdfs:comment': 'Annalist collection metadata.'
            , 'rdfs:label': 'Name collection coll1'
            })
        self.testcoll_add = (
            { 'rdfs:comment': 'Annalist collection metadata.'
            , 'rdfs:label': 'Name collection testcoll'
            })
        self.type1_add = (
            { 'rdfs:comment': 'Annalist collection1 recordtype1'
            , 'rdfs:label': 'Type testcoll/type1'
            })      
        self.type1 = (
            { '@id': './'
            , 'id': 'type1'
            , 'type': 'annal:RecordType'
            , 'title': 'Type testcoll/type1'
            , 'uri': TestBaseUri+'/collections/testcoll/types/type1/'
            , 'annal:id': 'type1'
            , 'annal:type': 'annal:RecordType'
            , 'rdfs:comment': 'Annalist collection1 recordtype1'
            , 'rdfs:label': 'Type testcoll/type1'
            })      
        self.type2_add = (
            { 'rdfs:comment': 'Annalist collection1 recordtype2'
            , 'rdfs:label': 'Type testcoll/type2'
            })      
        self.type2 = (
            { '@id': './'
            , 'id': 'type2'
            , 'type': 'annal:RecordType'
            , 'title': 'Type testcoll/type2'
            , 'uri': TestBaseUri+'/collections/testcoll/types/type2/'
            , 'annal:id': 'type2'
            , 'annal:type': 'annal:RecordType'
            , 'rdfs:comment': 'Annalist collection1 recordtype2'
            , 'rdfs:label': 'Type testcoll/type2'
            })      
        self.view1_add = (
            { 'rdfs:comment': 'Annalist collection1 recordview1'
            , 'rdfs:label': 'Type testcoll/view1'
            })      
        self.view1 = (
            { '@id': './'
            , 'id': 'view1'
            , 'type': 'annal:RecordView'
            , 'title': 'Type testcoll/view1'
            , 'uri': TestBaseUri+'/collections/testcoll/views/view1/'
            , 'annal:id': 'view1'
            , 'annal:type': 'annal:RecordView'
            , 'rdfs:comment': 'Annalist collection1 recordview1'
            , 'rdfs:label': 'Type testcoll/view1'
            })      
        self.view2_add = (
            { 'rdfs:comment': 'Annalist collection1 recordview2'
            , 'rdfs:label': 'Type testcoll/view2'
            })      
        self.view2 = (
            { '@id': './'
            , 'id': 'view2'
            , 'type': 'annal:RecordView'
            , 'title': 'Type testcoll/view2'
            , 'uri': TestBaseUri+'/collections/testcoll/views/view2/'
            , 'annal:id': 'view2'
            , 'annal:type': 'annal:RecordView'
            , 'rdfs:comment': 'Annalist collection1 recordview2'
            , 'rdfs:label': 'Type testcoll/view2'
            })      
        self.list1_add = (
            { 'rdfs:comment': 'Annalist collection1 recordlist1'
            , 'rdfs:label': 'Type testcoll/list1'
            })      
        self.list1 = (
            { '@id': './'
            , 'id': 'list1'
            , 'type': 'annal:RecordList'
            , 'title': 'Type testcoll/list1'
            , 'uri': TestBaseUri+'/collections/testcoll/lists/list1/'
            , 'annal:id': 'list1'
            , 'annal:type': 'annal:RecordList'
            , 'rdfs:comment': 'Annalist collection1 recordlist1'
            , 'rdfs:label': 'Type testcoll/list1'
            })      
        self.list2_add = (
            { 'rdfs:comment': 'Annalist collection1 recordlist2'
            , 'rdfs:label': 'Type testcoll/list2'
            })      
        self.list2 = (
            { '@id': './'
            , 'id': 'list2'
            , 'type': 'annal:RecordList'
            , 'title': 'Type testcoll/list2'
            , 'uri': TestBaseUri+'/collections/testcoll/lists/list2/'
            , 'annal:id': 'list2'
            , 'annal:type': 'annal:RecordList'
            , 'rdfs:comment': 'Annalist collection1 recordlist2'
            , 'rdfs:label': 'Type testcoll/list2'
            })      
        return

    def tearDown(self):
        return

    def test_CollectionTest(self):
        self.assertEqual(Collection.__name__, "Collection", "Check Collection class name")
        return

    def test_collection_init(self):
        s = Site(TestBaseUri, TestBaseDir)
        c = Collection(s, "testcoll")
        self.assertEqual(c._entitytype,     ANNAL.CURIE.Collection)
        self.assertEqual(c._entityfile,     layout.COLL_META_FILE)
        self.assertEqual(c._entityref,      layout.META_COLL_REF)
        self.assertEqual(c._entityid,       "testcoll")
        self.assertEqual(c._entityuri,      TestBaseUri+"/collections/testcoll/")
        self.assertEqual(c._entitydir,      TestBaseDir+"/collections/testcoll/")
        self.assertEqual(c._values,         None)
        return

    def test_collection_data(self):
        c = self.testcoll
        c.set_values(self.testcoll_add)
        cd = c.get_values()
        self.assertEquals(set(cd.keys()),set(('id', 'type', 'uri', 'title', 'rdfs:label', 'rdfs:comment')))
        self.assertEquals(cd["title"],        "Name collection testcoll")
        self.assertEquals(cd["rdfs:label"],   "Name collection testcoll")
        self.assertEquals(cd["rdfs:comment"], "Annalist collection metadata.")
        return

    # Record types

    def test_add_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        typenames = { t.get_id() for t in self.testcoll.types() }
        self.assertEqual(typenames, set())
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        typenames = { t.get_id() for t in self.testcoll.types() }
        self.assertEqual(typenames, {"type1", "type2"})
        return

    def test_get_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        self.assertEqual(self.testcoll.get_type("type1").get_values(), self.type1)
        self.assertEqual(self.testcoll.get_type("type2").get_values(), self.type2)
        return

    def test_remove_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        typenames =  set([ t.get_id() for t in self.testcoll.types()])
        self.assertEqual(typenames, {"type1", "type2"})
        self.testcoll.remove_type("type1")
        typenames =  set([ t.get_id() for t in self.testcoll.types()])
        self.assertEqual(typenames, {"type2"})
        return

    # Record views

    def test_add_view(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        viewnames = { t.get_id() for t in self.testcoll.views() }
        self.assertEqual(viewnames, set())
        t1 = self.testcoll.add_view("view1", self.view1_add)
        t2 = self.testcoll.add_view("view2", self.view2_add)
        viewnames = { t.get_id() for t in self.testcoll.views() }
        self.assertEqual(viewnames, {"view1", "view2"})
        return

    def test_get_view(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_view("view1", self.view1_add)
        t2 = self.testcoll.add_view("view2", self.view2_add)
        self.assertEqual(self.testcoll.get_view("view1").get_values(), self.view1)
        self.assertEqual(self.testcoll.get_view("view2").get_values(), self.view2)
        return

    def test_remove_view(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_view("view1", self.view1_add)
        t2 = self.testcoll.add_view("view2", self.view2_add)
        viewnames =  set([ t.get_id() for t in self.testcoll.views()])
        self.assertEqual(viewnames, {"view1", "view2"})
        self.testcoll.remove_view("view1")
        viewnames =  set([ t.get_id() for t in self.testcoll.views()])
        self.assertEqual(viewnames, {"view2"})
        return

    # Record lists

    def test_add_list(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        listnames = { t.get_id() for t in self.testcoll.lists() }
        self.assertEqual(listnames, set())
        t1 = self.testcoll.add_list("list1", self.list1_add)
        t2 = self.testcoll.add_list("list2", self.list2_add)
        listnames = { t.get_id() for t in self.testcoll.lists() }
        self.assertEqual(listnames, {"list1", "list2"})
        return

    def test_get_list(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_list("list1", self.list1_add)
        t2 = self.testcoll.add_list("list2", self.list2_add)
        self.assertEqual(self.testcoll.get_list("list1").get_values(), self.list1)
        self.assertEqual(self.testcoll.get_list("list2").get_values(), self.list2)
        return

    def test_remove_list(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_list("list1", self.list1_add)
        t2 = self.testcoll.add_list("list2", self.list2_add)
        listnames =  set([ t.get_id() for t in self.testcoll.lists()])
        self.assertEqual(listnames, {"list1", "list2"})
        self.testcoll.remove_list("list1")
        listnames =  set([ t.get_id() for t in self.testcoll.lists()])
        self.assertEqual(listnames, {"list2"})
        return

#   -----------------------------------------------------------------------------
#
#   CollectionEditView tests
#
#   -----------------------------------------------------------------------------

class CollectionEditViewTest(AnnalistTestCase):
    """
    Tests for Collection views
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.user = User.objects.create_user('testuser', 'user@test.example.com', 'testpassword')
        self.user.save()
        self.uri = reverse("AnnalistCollectionEditView", kwargs={'coll_id': "coll1"})
        self.continuation = "?continuation_uri="+TestHostUri+self.uri
        self.client = Client(HTTP_HOST=TestHost)
        loggedin = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(loggedin)
        return

    def tearDown(self):
        return

    def test_CollectionEditViewTest(self):
        self.assertEqual(CollectionEditView.__name__, "CollectionEditView", "Check CollectionView class name")
        return

    def test_get(self):
        r = self.client.get(self.uri)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, "<title>Annalist data journal test site</title>")
        self.assertContains(r, "<h3>Customize collection coll1</h3>")
        return

    def test_get_context(self):
        r = self.client.get(self.uri)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertEquals(r.context['title'],   "Annalist data journal test site")
        self.assertEquals(r.context['coll_id'], "coll1")
        self.assertEquals(r.context['types'],   ["type1", "type2"])
        self.assertEquals(r.context['lists'],   ["list1", "list2"])
        self.assertEquals(r.context['views'],   ["view1", "view2"])
        self.assertEquals(r.context['select_rows'], "6")
        return

    def test_post_new_type(self):
        form_data = (
            { "type_new":   "New"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        typenewuri = reverse(
            "AnnalistRecordTypeNewView", 
            kwargs={'coll_id': "coll1", 'action': "new"}
            )
        self.assertEqual(r['location'], TestHostUri+typenewuri+self.continuation)
        return

    def test_post_copy_type(self):
        form_data = (
            { "typelist":   "type1"
            , "type_copy":  "Copy"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        typecopyuri = reverse(
            "AnnalistRecordTypeCopyView", 
            kwargs={'coll_id': "coll1", 'type_id': "type1", 'action': "copy"}
            )
        self.assertEqual(r['location'], TestHostUri+typecopyuri+self.continuation)
        return

    def test_post_copy_type_no_selection(self):
        form_data = (
            { "type_copy":  "Copy"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        erroruri = self.uri+r"\?error_head=.*\&error_message=.*"
        self.assertMatch(r['location'], TestHostUri+erroruri)
        return

    def test_post_edit_type(self):
        form_data = (
            { "typelist":   "type1"
            , "type_edit":  "Edit"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        typeedituri = reverse(
            "AnnalistRecordTypeEditView", 
            kwargs={'coll_id': "coll1", 'type_id': "type1", 'action': "edit"}
            )
        self.assertEqual(r['location'], TestHostUri+typeedituri+self.continuation)
        return

    def test_post_edit_type_no_selection(self):
        form_data = (
            { "type_edit":  "Edit"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        erroruri = self.uri+r"\?error_head=.*\&error_message=.*"
        self.assertMatch(r['location'], TestHostUri+erroruri)
        return

    def test_post_delete_type(self):
        form_data = (
            { "typelist":   "type1"
            , "type_delete":  "Delete"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertTemplateUsed(r, "annalist_confirm.html")
        # Check confirmation form content
        complete_action_uri = reverse("AnnalistRecordTypeDeleteView", kwargs={"coll_id": "coll1"})
        self.assertContains(r, """<form method="POST" action="/"""+TestBasePath+"""/confirm/">""", status_code=200)
        self.assertEqual(r.context['complete_action'], complete_action_uri)
        self.assertEqual(r.context['cancel_action'], self.uri)
        action_params = json.loads(r.context['action_params'])
        self.assertEqual(action_params['type_delete'], ["Delete"])
        self.assertEqual(action_params['typelist'],    ["type1"])
        return

    def test_post_delete_type_no_selection(self):
        form_data = (
            { "type_delete":  "Delete"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        erroruri = self.uri+r"\?error_head=.*\&error_message=.*"
        self.assertMatch(r['location'], TestHostUri+erroruri)
        return

    def test_post_close(self):
        form_data = (
            { "close":  "Close"
            })
        r = self.client.post(self.uri, form_data)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        siteviewuri = reverse("AnnalistSiteView")
        self.assertEqual(r['location'], TestHostUri+siteviewuri)
        return

# End.
