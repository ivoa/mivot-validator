.. mivot-validator documentation master file, created by
   sphinx-quickstart on Fri Dec  1 13:07:28 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mivot-validator's documentation!
===========================================

mivot-validator
===============

Python package for validating VOTables annotated with `MIVOT <https://github.com/ivoa-std/ModelInstanceInVot>`__

The validation process is 2 steps; - VOTable validation (against 1.3) - MIVOT validation

Both must succeed for the file to be considered as valid

The validator can process either individual files or directory contents (no recursivity)

XML Schema Validator
--------------------

Validate an annotated VOTable against both VOTable and MIVOT schemas.
     
.. code:: bash
   :caption: Validate an annotated VOTable against both VOTable and MIVOT schemas

   mivot-validate  PROJECT_DIR/tests/data/gaia_3mags_ok_1.xml 
     
   USAGE: mivot-validate [path]
          Validate against both VOTable and MIVOT schemas
          path: either a simple file or a directory
                all directory XML files are validated
                exit status: 0 in case of success, 1 otherwise
     
.. code:: bash
   :caption: Validate an annotated VOTable against MIVOT schemas

   mivot-validate  PROJECT_DIR/tests/data/gaia_3mags_ok_1.xml 
     
   USAGE: mivot-mapping-validate [path]
          Validate XML files against  MIVOT schema
          path: either a simple file or a directory
                all directory XML files are validated
                exit status: 0 in case of success, 1 otherwise


Model Validation
----------------

This tool checks that mapped classes match the model they refer to. 

- It requires as input an annotated VOTable. 
- This VOTable is parsed with a model viewer issuing a model view on the first data row.
- Each instance of that view is compared with the VODML class definition. 
- This feature works with PhotDM, Meas, Coords and a MANGO draft. 
  Any other model, but ``ivoa`` which is skipped, make the process failing.

.. code:: bash

    mivot-instance-validate <VOTABLE path>
    
    USAGE: mivot-instance-validate [path]
           Validate the mapped instances against the VODML definitions
           path: path to the mapped VOTable to be checked
           exit status: 0 in case of success, 1 otherwise
    

The validation process follows these steps - INPUT: a VOTable annotated with the supported models. - The annotation must have at least one valid TEMPLATES - The current implementation works only with VOTables having one table. - Build a model view of the first data row (``mivot-validator/mivot_validator/instance_checking/xml_interpreter/model_viewer.py``). - All top level INSTANCEs of that model view will be checked one by one. - The XML blocks corresponding to these instances are extracted as etree objects - Get the ``dmtype`` on the instance to validate - build an XML snippets for that class from the VODML file (``mivot-validator/mivot_validator/instance_checking/snippet_builder.py``) - These snippets are stored in ``mivot-validator/mivot_validator/instance_checking/tmp_snippets`` (\*) - The validator checks any component of the mapped instance against the snippet. - if the component is an ATTRIBUTE, both dmtypes and roles are checked - if the component is a COLLECTION, dmrole as well as items dmtypes are checked - if the component is a REFERENCE, dmrole is checked - if the component is an INSTANCE, both dmtypes and roles are checked and the validation loop is run on its components

The validator only checks the model elements that are mapped. It does not care about missing attributes or any other missing class components. MIVOT does not have requirements on the model elements that must be mapped.

(\*) It is to be noted that those snippets can be used to build annotations. If you feed the validator with an empty INSTANCE with the searched dmtype:

::

    <INSTANCE dmtype="model:MyFavouriteType"\>

you get an XML snippet named ``model.MyFavouriteType.xml`` that can be copied and tuned into your VOTable

Types and Roles Checking
------------------------

The validator has a new end point that can check that all ``dmtype`` and ``dmrole`` referenced in the mapping block are known by mapped models. It does not care of the class structures This checking only works with the Meas/Coord/ivoa models, other models are ignored.

.. code:: bash

    types-and-roles-validate <VOTABLE path>
    
    USAGE: types-and-roles-validate [path]
           Validate all dmtypes and dmroles
           exit status: 0 in case of success, 1 otherwise
    


Snippet Generation
==================

To facilitate the production of a VODML file annotated with MIVOT, it can be interesting to work with 
precomputed snippets that can be stacked to build full annotation blocks.

- A snippet is a MIVOT fragment with not-set references and values that represents  a part of a model.
- Snippets can easily be derived from the VODML representation of the model as long as there is no class polymorphism.
  If there are, we provide a tool helping users to resolve abstract components.

There are two types of snippet generators:
 
 - ``mivot-snippet-model``, which allows, for a given model, to generate all 
   non-abstract object and data types.
   it provides a model view directly formatted as MIVOT components.
-  The ``mivot-snippet-instance``, which for a given concrete class name, will generate a 
   snippet usable according to the concrete classes chosen when creating it  

.. code::bash
   :caption: Build all MIVOT snippets for a model
   
   mivot-snippet-model [VODML path or url]
    
   USAGE: mivot-snippet-model [path] [output_dir]
           Create MIVOT snippets from VODML files
           path: either a simple file to any VODML-Model or an ur
           output_dir: (optional) path to the chosen output directory (session working directory by default)"
           exit status: 0 in case of success, 1 otherwise
    

 .. code::bash
    :caption: Build a MIVOT snippet for one model class with resolving abstract types.
 
    $ mivot-snippet-instance coords:TimeSys `pwd`/coords.TimeSys.example \
    -cc dmrole=coords:TimeFrame.refPosition,context=coords:TimeSys,dmtype=coords:RefLocation,class=coords:StdRefLocation\
    -cc dmrole=coords:TimeFrame.refDirection,context=coords:TimeSys,dmtype=coords:RefLocation,class=coords:StdRefLocation
    
In this example the tool will generate on snippet for the object type `coords:TimeSys`.

- The produced file will be located in ``CURRENT_FOLDER/coords.TimeSys.example.xml``.
  If the output is not an absolute path, the output will be located in the session working directory.
- All MIVOT instances of (abstract) type ``coords:RefLocation`` playing the role ``coords:TimeFrame.refPosition``
  and hosted by a class playing the role ``coords:TimeSys``, will be replaced by instances of type ``coords:StdRefLocation``
- All MIVOT instances of (abstract) type ``coords:RefLocation`` playing the role ``coords:TimeFrame.refDirection``
  and hosted by a class playing the role ``coords:TimeSys``, will be replaced by instances of type ``coords:StdRefLocation``

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
