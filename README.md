# mivot-validator

This package has 2 purposes:

- Validation of VOTables annotated with IVOA recommendation [MIVOT](https://ivoa.net/documents/MIVOT/20230620/index.html)
- MIVOT serialization of model components (snippets) that can be used to build annotations

## Installation

The validator is distributed as a Python package.

```bash
$ pip install mivot-validator
```

## Scripts for Validating Annotated VOTables

There are 2 validation levels:

- against the XML schemas (VOTable and MIVOT)
- against the model itself as it is defined in VODML

### XML Schema Validation

Validation of an annotated VOTable against both VOTable and MIVOT schemas:

```bash
$ mivot-validate  PROJECT_DIR/tests/data/gaia_3mags_ok_1.xml

USAGE: mivot-validate [path]
       Validate against both VOTable and MIVOT schemas
       path: either a simple file or a directory
             all directory XML files are validated
       exit status: 0 in case of success, 1 otherwise
```

Validation of an annotated VOTable against the MIVOT schema only:
    
```bash 
$ mivot-mapping-validate  PROJECT_DIR/tests/data/gaia_3mags_ok_1.xml 

USAGE: mivot-mapping-validate [path]
       Validate XML files against  MIVOT schema
       path: either a simple file or a directory
             all directory XML files are validated
       exit status: 0 in case of success, 1 otherwise
```

### Model Validation

This tool checks that mapped classes match the model they refer to. 

```bash 
$ mivot-instance-validate <VOTABLE path>
    
USAGE: mivot-instance-validate [path]
       Validate the mapped instances against the VODML definitions
       path: path to the mapped VOTable to be checked
       exit status: 0 in case of success, 1 otherwise
```

### Types and Roles Checking

The validation tool below checks that all `dmtype` and `dmrole` referenced in the mapping block 
are known by mapped models; it does not care of the class structures. 
This checking only works with the *PhotDM/MANGO/Meas/Coord/ivoa* models, other models are ignored.

```bash
$ types-and-roles-validate <VOTABLE path>
    
USAGE: types-and-roles-validate [path]
       Validate all dmtypes and dmroles
       exit status: 0 in case of success, 1 otherwise
```
       
## Snippet Generation

To facilitate the MIVOT annotation of VODML files, it can be convenient to work with 
pre-computed snippets that can be stacked to build full annotation blocks.

- A snippet is a MIVOT fragment, where values and references are not set, that represents a component of a model.
- Snippets can easily be derived from the VODML representation of the model as long as there is no class polymorphism.
  If there is some, we provide a tool helping users to resolve abstract components.

There are two snippet generators available in this package:
 
- `mivot-snippet-model` which allows, for a given model, to generate all 
   non-abstract object and data types as MIVOT components.
-  The `mivot-snippet-instance` which generate, for a given concrete class name, a 
   usable snippet including the concrete classes given either as user input or as command line parameters. 
       
### Build all MIVOT snippets for a model

```bash   
$ mivot-snippet-model [VODML path or url]
    
USAGE: mivot-snippet-model [url] [output_dir]
       Create MIVOT snippets from VODML files
       url: url of any VODML-Model (must be prefixed with file:// in case of local file)
       output_dir: path to the chosen output directory (session working directory by default)
       exit status: 0 in case of success, 1 otherwise
```

### Build the MIVOT snippet for one model class with resolving abstract types:

```bash 
$ mivot-snippet-instance coords:TimeSys `pwd`/coords.TimeSys.example \
   -cc dmrole=coords:TimeFrame.refPosition,context=coords:TimeSys,dmtype=coords:RefLocation,class=coords:StdRefLocation\
   -cc dmrole=coords:TimeFrame.refDirection,context=coords:TimeSys,dmtype=coords:RefLocation,class=coords:StdRefLocation
```
    
In this example the tool will generate one snippet for the object type `coords:TimeSys`.

- The produced file will be located in `CURRENT_FOLDER/coords.TimeSys.example.xml`.
  If the output is not an absolute path, it will be located in the session working directory.
- All MIVOT instances of (abstract) type `coords:RefLocation` playing the role `coords:TimeFrame.refPosition`
  and hosted by a class playing the role `coords:TimeSys`, will be replaced by instances of type `coords:StdRefLocation`
- All MIVOT instances of (abstract) type `coords:RefLocation` playing the role `coords:TimeFrame.refDirection`
  and hosted by a class playing the role `coords:TimeSys`, will be replaced by instances of type `coords:StdRefLocation`
