# Annalist v0.5 release notes

Annalist release 0.5.x is a candidate feature-complete minimal viable product for an eventual version 1 release.

A summary of issues intended to be resolved for product release can be seen in the [issues list for the first alpha release milestone](https://github.com/gklyne/annalist/milestones/V0.x%20alpha).  See also the file [documents/TODO.md](https://github.com/gklyne/annalist/blob/develop/documents/TODO.md) on the "develop" branch.


## Release: 0.5.10

This is a maintenance release, with no substantial changes in functionality.  Form rendering and test cases have been restructured, some view fields renamed, and some property URIs renamed.

Access to values in `bound_field` has been changed so field definition references must use `_field_definition` attribute, or special methods/attributres for a few common cases.  This makes it clearer in calling code what is being acessed, and simplified the implemenation of `bound_field`.  Many tests have been revamped to compare the generated view context with a value generated locally by support functions.  This reduces the efford of revising tests to follow changes in the view context structure.


## Status

The Annalist software is now believed to offer a level of functionality that will be incorporated in an initial full software release.  The primary goals of Annalist are to make it easy for people to create and share linked data on the web, without programming:

* Easy data: out-of-box data acquisition, modification and organization of small data records.
* Flexible data: new record types and fields can be added as-required.
* Sharable data: use textual, easy to read file formats that can be shared by web, email, file transfer, version management system, memory stick, etc.
* Remixable data: records that can be first class participants in a wider ecosystem of linked data on the web, with links in and links out.

Key features implemented:

* Simple installation and setup procedure to quickly get a working installation
* Highly configurable form interface for entering, presenting and modifying data records, built using self-maintained configuration data.  The core presentation engine is substantially complete, but additional field renderers are still required to support a wider range of basic data types.
* Grid-based responsive layout engine (currently using Zurb Foundation)
* File based, versioning-friendly, textual data storage model;  data design is RDF-based, and uses JSON-LD elements.  JSON-LD contextx are automatically generated as needed for each collection to allow ingest as RDF.
* Ability to create new entity record types, views and listing formats on-the-fly as data is being prepared
* Authentication with 3rd party IDP authentication (current implementation uses OAuth2/OpenID Connect, tested with Google, but should be usable with other OpenID Connect identity providers).  (Note access control is separate.)
* Authorization framework for access control, applied mainly per-collection but with site-wide defaults.
* Support for uploading, importing and linking to, and annotating, binary objects such as images.
* Image rendering
* Audio clip rendering (via HTML5 capabilities)

Intended core features not yet fully implemented but which are under consideration for future releases:

* Full linked data support, recognizing a range of linked data formats and facilitating the creation of links in and out.  (Links can be created, but it's currently a mostly manual process.)
* Serve and access underlying data through a standard HTTP server using LDP and/or SoLiD protocols (the current implementation uses direct file access).
* Grid view (e.g. for photo+metadata galleries).
* Data bridges to other data sources, in particular to allow Annalist to work with existing spreadhseet and other data.

See the [list of outstanding issues for initial release](https://github.com/gklyne/annalist/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22V0.x+alpha%22) for more details on planned features still to be implemented.

There are many other features noted on the project roadmap that are not yet planned for inclusion as core features.  As far as possible, future development will be guided by actual requirements from applications that use the Annalist platform.


## Feedback

The main purpose of this release is to be a viable platform for getting feedback from potential users of the software.  In particular, I'd like to hear:

* If installation and getting a running service on a computer meeting the indicated prerequisites takes longer than 10 minutes.  What were the stumbling points?
* Any problems that occur whle trying to use the software.
* Ways in which the software does not meet preferred workflows for collecting data.
* Any must-have features for the software to be useful.
* Any other thoughts, ideas, or difficulties you care to report.

If you have a github account, feedback can be provided through the [github issue tracker](https://github.com/gklyne/annalist/issues).  Otherwise, by message to the [annalist-discuss forum](https://groups.google.com/forum/#!forum/annalist-discuss) at Google Groups.


## Development

Active development takes place on the [`develop` branch](https://github.com/gklyne/annalist/tree/develop) of the GitHub repository.  The `master` branch is intended for stable releases, and is not used for active development.  It would be appreciated if any pull requests submitted can against the `develop` branch.


# Further information

(Many of these documents are still work-in-progress)

* [Annalist overview](../introduction.md)
* [Installing and setting up Annalist](../installing-annalist.md)
* [Getting started with Annalist](../getting-started.md)
* [Guide to using Annalist](../using-annalist.adoc)
* [Simple demonstration sequence](../demo-script.md)
* [Frequently asked questions](../faq.md)
* [Developer information](../developer-info.md)
* [Development roadmap](../roadmap.md)


# History

See also previous release notes:

- [Release 0.1.x](./release-v0.1.md)


## Release: 0.5.10

This is a maintenance release, with no substantial changes in functionality.  Form rendering and test case have been restructured, some view fields renamed, and some property URIs renamed.

Access to values in `bound_field` has been changed so field definition references must use `_field_definition` attribute, or special methods/attributres for a few common cases.  This makes it clearer in calling code what is being acessed, and simplified the implemenation of `bound_field`.  Many tests have been revamped to compare the generated view context with a value generated locally by support functions.  This reduces the efford of revising tests to follow changes in the view context structure.


# Version 0.5.9, towards 0.5.10

- [x] Flush collection caches on loading customize page rather than view page
- [x] Bound_field access to FieldDecription: use methods not dictionary
    - [x] Update test case context checking (see bound_field holding comments)
    - [x] Use 'entity_testfielddesc' methods in `entity_testtypedata`
    - [x] Use 'entity_testfielddesc' methods in `entity_testviewdata`
    - [x] Use 'entity_testfielddesc' methods in `entity_testvocabdata`
    - [x] Various test modules _check_context_fields use 'entity_testfielddesc' methods
    - [x] Rename *_context_data contruction methods
    - [x] Rename *_form_data contruction methods
- [x] Test code general cleanup
    - [x] replace <field>.description['field_id'] with .field_id
    - [x] replace <field>.description['field_name'] with .field_name
    - [x] replace <field>.description['field_label'] with .field_label
    - [x] Refactoring view context tests: new module entityfielddesc has field details, and creating and/or editing functions to create context structures for comparison in tests.
- [x] View_field_sel change label to "Field ref".
- [x] Render modes:  instead of a separate function for each mode, pass parameter to each renderer and select at the point of rendering (e.g. see render_fieldvalue.render_mode)
    - this reduces of wrapping and duplication of render mode functions.
- [x] In render_select.py, and elsewhere: remove references to {{field.field_value_link_continuation}} and use locally generated {{field_labelval}}, etc.
- [x] Rename fields/properties:
    - "annal:record_type" -> "annal:list_entity_type" (for list target type)
    - "annal:record_type" -> "annal:view_entity_type" (for view target type)
    - "annal:record_type" -> "annal:group_entity_type" (for field group target type)
    - Group_target_type -> Group_entity_type
    - List_target_type -> List_entity_type
    - View_target_type -> View_entity_type
    - [x] Add migraton in RecordList, RecordView, RecordGroup
    - [x] Add migration tests
- [x] In entityedit, fix up population of context 'record_type'
- [x] entity_testentitydata.specified_view_context_data add type URI param
- [x] Allow field `annal:task_buttons` in view definition to define buttons for both entity edit and view displays
- [x] Update Annalist_schema to reflect changes
- [x] Update RDF schema to use different properties for subclass and subproperty relations between Annalist `Class`/`Property` entities describing them.  Add aliases to support migration.
- [x] migrate content of all installable collections


## Release: 0.5.8

This release primarily adds support for sub/superproperty URI relations declared in field definitions, and adds logic to access entity values using subproperties of a specified field property URI.  This is intended to make it easier to work with structured vocabularies like CIDOC CRM, and to facilitate some kinds of data evolution.  These changes have prompted some further codebase refactoring.

This release also includes numerous bug fixes, and changes to some messages.


# Version 0.5.7, towards 0.5.8

- [x] BUG: delete list view while viewing that list results in obscure error message.
    - Improve error handling to use alternative list/view definition
- [x] BUG: Turtle generation from "Smoke" collection journal entry causes internal errors
    - Error reading bad context file, caused by Annalist data errors, which have been fixed.
    - Also caused by trailing spoace on URL: need to check valid URLs; can catch errors?
    - Added logic to flag error and add details to output.
- [x] Fix some test cases that were failing due to message text changes.
    - NOTE: `test_entitydefaultlist` and `test_entitygenericlist` now have logic to test messages using definitions in `message`.  In the longer term, all test cases should do this so they don't fail if the language is changed.
- [x] Review message text; update more tests to expect text as defined in messages module.
- [x] Introduce superproperty/ies field and button to create subproperty field definition
    - [x] Collection methods to access field definitions (model on types)
    - [x] Cache classes for fields (model on types)
    - [x] RecordField hook to update collection cache
    - [x] Test cases for new classes and methods
    - [x] Update collection to use field cache
    - [x] Update cache flush logic where used
    - [x] Test suite provide default property URIs 
    - [x] RecordField accesses should use collecton cache
    - [x] Cacheing site values separately: no need to flush as they don't change
    - [x] Field definition to include superproperty URI list
    - [x] When selecting data element to display in a field, look for subproperties as well as the specified field property.
        - [x] Add subproperty discovery logic to bound_field
        - [x] Update fieldvaluemap.map_form_to_entity so it looks for subproperty to update.
        - [x] Update field mappers to make 'map_form_to_entity_repeated_item' implementations more consistent.
    - [x] Review abstractions and interactions around:
        - [x] bound_field, add:
            - [x] 'render' (ref field_renderer)
            - [x] 'value_mapper'
        - [x] New field_renderer object accessed by bound_field for field rendering
        - [x] Rework field rendering logic to use new structure
        - [x] Remove rendering methods from field description
        - [x] Eliminate render mode logic in render_fieldvalue
    - [x] Add test cases for subproperty access
    - [x] Add test cases for subproperty list field access/update (with subproperty values)
    - [x] Add "define subproperty" task button to field definition.
    - [x] Add test case for "define subproperty" task button
- [x] Add property hierarchy to CIDOC CRM definitions (https://github.com/gklyne/CIDOC_CRM_core_defs)
- [x] Create FAQ for defining subproperties


## Release: 0.5.6

This release primarily addresses some performance issues that were noted when working with complex structures with a deep class hierarchy (specifically, CIDOC CRM).  It introduces a per collection cache for entity type definitions, and precalculated super-/sub- type closures to speed up discovery of subtypes of a desired target type.  It also adds a namespece vocbulary cache, which is used to expand namespace prefixes when rendering Web link fields.  These changes have included some extensive refactoring of the codebase.

This release also includes numerous bug fixes, and some small changes to the user interface.


## Version 0.5.5, towards 0.5.6

- [x] BUG: show warning when accessing collection with missing parent.
    - The implementation of this fix has involved a significant refactoring of error reporting and entity delete confirmation logic, to use more common code in DisplayInfo.
    - In some cases, continuation URLs used have changed
- [x] BUG: define repeat field task should use same property URI (without suffix)
- [x] BUG: deleting field definition from "Smoke" collection causes internal errors
- [x] BUG: Customize window doesn't return to previous URL after data migration.
- [x] BUG: `Journal_refs` field in `Journal_defs` collection was causing context generation errors
    - These in turn caused Turtle output generation server errors (500).
    - Changed property URI `annal:member` to `coll:Journal_refs` for field `Journal_defs`
    - This may affect collections that use this field (e.g. `IG_Philadelphia_Project`).
- [x] BUG: Login sequence from authz error page does not always return to original page viewed
- [x] BUG: changing view and/or list from default values causes 500 Server Error; but nothing shows in log; e.g.
    - 500: Server error
    - u'frbr:Group_1_entity' - see server log for details
    - Seems to occur while (re)generating context
    - Maybe related to removal of a supertype rather than view/list
    - Or related to copy type then change URI?
    - Tracked down to removal of type URI->Id entty in CollectionTypeCache.remove_type
    - Replaced `del` dictionary entry with `.pop()` operation so no error if the key missing.
- [x] BUG: define repeat field: should use base type for value and entity type
- [x] BUG: editing details of parent collection in another browser tab can leave inhertiting collection view "stuck" with old cached values.
    - At minimum, need an easy way to force cache-refresh.
    - Better: invalidate caches for dependent collections when invalidating parent.
    - NOTE: type update does not do complete cache flush - maybe it should?
    - NOTE: collection-level type cache is not currently called anywhere apart from tests
    - For now, displaying a default collection view (e.g. from list of collections, or from menu bar) causes all collection caches to be flushed.
- [x] BUG: in 'cgreenhalgh_annalist_performance_archive', linked audio example is displayed twice in list, but only one instance exists.  Something similar happens if example linked image is created.
    - Occurred when corresponding type is defined by multiple parent collections.
    - Fixed logic in `Entity._children`
- [x] BUG: create subtype of parent type, and rename, then attempt to create view+list before saving: generates an error message, e.g. "Record type meld_Motivation_sub in collection MELD_Climb_performance already exists".  It's possible it's because the new name already exists, but the old one is reported here. Bug is an error in the message rather than a deeper logic problem. 
- [x] Add Entity_uri field definition to site data.
- [x] Make labels for enumeration/choice render types more usefully descriptive.
- [x] Review form of URI used for Resource_defs internal types (coll: namespace?).  Add built-in support to generate prefix mapping in context.
- [x] Improve styling for printed form of Annalist pages (currently it looks a mess: uses small-screen layout)
- [x] Generate README for collection incorporating description from coll-meta (as part of context generation?).
- [x] Improve performance of mechanisms used for finding type information
    - (working with CIDOC-CRM deeply nested type hierarchy gets very slow)
    - Create cache and update hooks for type information, including calculation of transitive closure.
- [x] Use transitive closure when locating entities of a designated type (for selecting applicable fields).
    - [x] Update EntityTypeInfo (get_all_type_uris) to use collection cache methods.
- [x] Show type URIs in type list
- [x] When rendering link, expand prefix in href if defined in collection
    - [x] introduce vocab namespace cache (collectionvocabcache)
    - [x] hook in RecordVocab
    - [x] hook in Collection (and other places where CollectionTypeCache is referenced)
    - [x] update render_uri_link
- [x] Boolean renderer: not recognizing "Y"; don't need label?
- [x] Refactor common logic in collectiontypecache and collectionvocabcache.
- [x] When generating subtype (task button), don't include supertypes


## Release: 0.5.4

This release contains some significant changes to simplify workflows used when creating definitons that use structured ontology terms, based on some experiences using Annalist to create CIDOC CRM data.  It also provides options for generating Turtle data output.  There are numerous bug fixes, which are described in the notes below for release 0.5.3.

Specific visible changes include:

* Turtle data output for entities and entity lists, to make it easier to share Annalist data with other linked data applications.
* New facility to create a subtype with key values inherited or derived from the parent type.
* Revised creation of view and list definitions for a type, to work more easily for subtypes.  Fields from existing type view and list definitions, or from the default view and list definitions, are copied into the new definitions created.
* Changes to help text, diagnostics and other messages.

There is some extensive internal refactoring in the view logic used to generate data outputs, and the links used to access data outputs.


## Version 0.5.3, towards 0.5.4

- [x] BUG: copy entity and Id change (or copy and something) causes errors on save.
- [x] BUG: When accessing JSON-LD from `.../v/<view-id>/...` form of URL (e.g. `.../c/EMLO_in_CRM_samples/v/Linked_image/Linked_image/image_00000026/`), the relative reference to retrieve the JSON-LD does not work.
- [x] BUG: software update zaps default user permissions (e.g. CREATE_COLLECTION)
    - introduced _site_default_user_perms which are consulted in preference to _default_user_perms, but not overridden on update
- [x] BUG: when default view references non-accessible entity: 
    - if default view/list unavailable, revert to default list
- [x] BUG: create subtype without login generates unhelpful error response
- [x] BUG: display list with no fields generates error
- [x] BUG: define view+list with none selected generates invalid list (and unhelpful view?)
- [x] BUG: field pos/size dropdown doesn't display properly on Chinese language Chrome
    - Changed characters used, but haven't yet been able to retest with Chinese language browser
- [x] BUG: data links for collection metadata are broken (since changes to entity_data_ref?)
- [x] Is there a way to allow multiple literal fields with the same property (cf. crm:P3_has_note)?  YES: use field URI "@value" inthe repeat field definition.
- [x] Make it easier to create subtype + view + list...
    - Provide "Create subtype" button and copy view information, supertypes, etc from supertype
    - Enhance create view+list logic to copy previous view+list definitions as defaults
- [x] Separate buttons for create list- and multiple-value fields (seq vs set)
- [x] When creating a repeat field, be more helpful in creating the help and tooltip text
- [x] Default type list/view and subtype comments: include link to type
- [x] Create FAQ for defining subtypes
- [x] For missing field definition, improve text and try to include field name referenced
- [x] Identifier values (URI/CURIE) should have leading/trailing spaces stripped on entry.
- [x] When inheriting definitions, also use parent collection default view if none defined locally.
- [x] Turtle rendering
    - Turtle output generated by parsing JSON-LD and outputing as Turtle using rdflib
    - Implement Turtle output for entity data views
    - Implement Turtle output for entity list views
    - Extensive refactoring of data view logic:
        - common logic to handle different return types (JSON-LD and Turtle)
        - common logic for entity and list data.
        - updated logic for adding "Link" headers to HTTP response
    - Add Turtle redirect calls alongside JSON-LD redirects
        - entityedit.py, form_render
        - entitylist.py, get
    - Create test cases for Turtle output (based on JSON-LD test cases)


## Version 0.5.2

This is mainly a maintenance release to fix some bugs that were introduced (or first noticed) in version 0.5.0.  It also contains some minor presentation, help text and documentation enhncements (including an initial set of FAQs).

The other technical change is some internal code refactoring to move towards possible per-entity access control (currently implemented on an ad hoc basis for default and unknown user permissions).


## Version 0.5.1, towards 0.5.2

- [x] BUG: edit collection metadata fails on save with
    - Original form is not providing correct original collection id
    - Added logic to entitytypeinfo to handle special case of collection ancestor id
    - Modified entityedit GET handler to use entitytypeinfo to access ancestor id
    - Added new test case that detects the original problem
- [x] BUG: failed to migrate linked data tools cleanly 
    - Returns error when trying to view tool:
    - Field See_also_r is missing 'group_field_list' value
    - Caused by earlier migration failure; possible from an attempt to hand-edit data
    - Fixed by removing old collection configuration data; no software change
- [x] BUG: migrating data doesn't update software version in data
    - also: editing collection metadata doesn't update collection s/w version
    - currently save logic of edit form handler calls viewinfo.update_coll_version()
    - [x] Redefine software compatibility version update as Collection method
    - [x] DisplayInfo updated to use new method
    - [x] Collection data migration updated to call new method
    - [-] Special case of editing collection metadata.  This would need a new set of logic (possibly in entitytypeinfo.py) to distinguish between a containing collection and ancestor for any entity (in almost all cases these would be the same), for very little practical benefit. So, for the time being, this is not being fixed.
- [x] BUG: Exception in RenderMultiFields_value.renderAttributeError
    - ("'NoneType' object has no attribute 'get'",)
    - this is caused by a reference to a non-existent field within a repeated field group: the error is in the data, due to old (erroneous) definitions not being removed, but the software reporting of this is unhelpful.
    - it turns out some earlier tests to provide improved reporting had been skipped; these tests have been reactivated and reports are somewhat more helpful.
- [x] BUG: OIDC login sequence returns wrong message if there is email address mismatch (e.g., logged in to wrong Google account)
    - instead of "email address mismatch", reports "was not authenticated".
    - but if different user id is selected, login propceeds OK
    - email address check in OIDC handler removed - this is handled and reported by the calling code
- [x] "Type definition" help text is a little confusing (cf 'Entity types ...').
- [x] Lay groundwork in EntityTypeInfo for access control possibly defined per-entity.
    - Currently used with ad-hoc logic for allowing view of default and unknown users
    - Replaces similar ad-hoc logic previously in DisplayInfo
    - Re-worked other direct references to EntityTypeInfo.permissions_map
- [x] See_also_r field duplicated in field options list
        - [x] Definitions in Resource_defs have been removed.
        - NOTE: See_also_r defined and referenced by:
            - Carolan_Guitar -> this will be a migration case study
            - Performance_defs -> (ditto?)
- [x] Tweak rendering of empty repeat-group


## Version 0.5.0

This release contains candidate feature-complete functionality for an Annalist V1 software release.  The aim has beemn to complete features that are seen as likely to affect the stored data structures used by Annalist, to minimize future data migration requirements.  The intent is that this release will be used in actual projects to test if it offers minimal viable product functionality for its imntended use.  Meanwhile, planned developments will focus more on documentation, stability, security and performance concerns.

### Revised view definition interface

Extensive changes that aim to simplify the user interface for defining entity views (specifically, fields that contain repeating groups of values) by eliminating the use of separate field group entities.  This in turn has led to changes in the underlying view and field definition structures used by Annalist.

Also added are data migration capabilities for existing data collections that use record groups. These have been used to migrate installable collection data.

The `Annalist_schema` instalable collection data (which provides RDF-schema based definitions for the Annalist-specific vocabulary terms) has been updated to reflect the field group changes.

### Other features

- popup help for view fields (tooltip text) is defined seperately from for general help text in a field definition.  (HTML5 tooltips don't support rich text formatting, so thios was limiting what could be included in the field definition help descriptions.)

- the installable collection `Journal_defs` has been split into two, with the aim of improving ease of sharing common definitions:
    - `Resource_defs` provides field and view definitions for uploaded, imported and linked media resources (currently image and audio), and annoted references to arbitrary web resources.  It also provides a number of commionly used namespace definitions (dc, foaf, and a namespace for local names without global URIs).
    - `Journal_defs` (which uses media definitions imported from `Resource_defs`) now provides just the (mainly) narrative journal structure that has been found useful for capturing some kinds of activity description.

- An `annalist-manager` subcommand (`migrateallcollections`) has been aded to migrate data for all collections in a site.

### Bug fixes

- Editing an entity inherited from another collection (which is supposed to create a new copy of that entity in the current collection) was generating an error when saving the edted entity.  The fix to this involved extensive refactoring of the entity editing and save logic to keep better track of the collection from which the original entity data was obtained.

- Fixed site data and installable collection data so that entity selection for inclusion in fields presenting drop-down selection lists would operate more consistently.


