# README #

one-time use service scripts used for migration of different types of packages.

> All bold words are terms used only within the company

## all_translit
Utility for transliteration of any text in text files.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/all_translit.rst)
## auto_yaml
Utility for automatically generating a yaml file. It tries to find all **openTask**, **openQuizz** and **the key task**. Creates yaml given the specified **directories of classes**.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/auto_yaml.rst)
## csv_encoder
Utility for changing encoding in .csv files, for correct display when opened in Microsoft Excel.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/csv_encoder.rst)
## find_id_content_from_yaml
The utility finds a .yaml file inside the package and finds in it all **imscc_identifier**, creates a folder in the root of the directory **COPIED_FILES**, then recursively traverses all the directories and looks for folders and files whose name consists of **imscc_identifier**. Then copies these files and directories to the folder **COPIED_FILES**.

By specifying the paths to be used, the utility will find all the html files related to the **lessons**, find in them links to the files in **wiki_content** and copy them to the **wiki_content** folder in **COPIED_FILES**.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/find_id_content_from_yaml.rst)
## parser
The utility runs through all the .html files in selected **lessons**, finds all the links leading to the old **Canvas system**, determines the page type, headers and paths, looks for an **id** match in the new **LMS system** and replaces the references to the corresponding JavaScript code. The result is described in the **res** folder in the file **# _log.html**

The utility works with several **lessons**, but within one course, since additional files are downloaded separately for each course.
The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/parser.rst)
## renamer
The utility recursively renames from Russian into translit all directories and files in the directory, as well as transliterates all links with Russian characters in the url paths.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/renamer.rst)
## xmlmergetool
A utility for merging two XML files.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/xmlmergetool.rst)
## yamliddoubles
The utility shows duplicates of **imscc_identifier** in the selected .yaml file.

The full doc [here](https://github.com/4ban/service_utilits/blob/master/meo-doc/source/yamliddoubles.rst)
