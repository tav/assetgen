Assetgen is intended as a replacement for the various ad-hoc scripts that often
get written to build/manage JavaScript/CSS files.

**Features**

The default support includes:

* Compiling CoffeeScript source files into JavaScript.

* Minifying JavaScript through UglifyJS -- including the new constant folding
  support.

* Compiling and minifying SASS stylesheets into CSS.

* Generating variants of the same stylesheet for both internationalisation
  (flipping left to right) and for automatically embedding images as ``data:``
  URIs to minimise latency.

* Concatenating multiple source files into one file to minimise the number of
  HTTP requests.

* Creating distinct files with the hash of the content embedded in the filename
  so as to work effectively with web caches.

* Creating a JSON manifest file for use in your web app's static handlers.

The tool is driven by the configuration you specify in an ``assetgen.yaml``
file, e.g.

::

   # Example assetgen.yaml configuration

   generate:

   - js/base.js:
       source:
         - %(AMPIFY_ROOT)s/third_party/jslibs/json.js

   - js/app.js:
       source:
         - static/js/Models.coffee
         - static/js/Views.coffee
         - static/js/Maps.coffee
       uglify:
         - --define-from-module
         - consts
       profile.dev:
         uglify:
           - --define-from-module
           - consts-dev

   - gfx/*:
       source: static/gfx/*
       type: binary

   - css/site.css:
       source:
         - raw: |
             // Public Domain (-) 2011 The Ampify Authors.
             // See the Ampify UNLICENSE file for details.
         - static/css/site.sass
       depends:
         - static/css/*.sass
         - static/gfx/*
       bidi: true
       embed.path.root: static
       embed.url.base: /.static/

   prereqs:

   - static/js/consts.js:
       source: static/js/consts.coffee
       compressed: false

   - static/js/consts-dev.js:
       source: static/js/consts-dev.coffee
       compressed: false

   env:
     NODE_PATH.prefix: static/js

   output.directory: appengine/static
   output.hashed: true
   output.manifest: appengine/assets.json

   profile.dev:
     css.compressed: false
     js.compressed: false

You can even control which config options gets used by specifying the
``--profile`` parameter. This will override default values with the values
specified for the given profile. So, in the above example, specifying
``--profile dev`` will use all the ``profile.dev`` options.

And, finally, you can specify custom handlers for ``assetgen`` to call when
generating a file of a given ``type``. For example, to override the builtin
``js`` handler with one which just lower-cases all the source content, create
your extension, e.g. ``kickass-extension.py``::

   class KickassAsset(Asset):

       def generate(self):
           content = ''.join(read(source).lower() for source in self.sources)
           self.emit(self.path, content)

   register_handler('js', KickassAsset)

Then run ``assetgen`` with the ``--extension path/to/kickass-extension.py``
parameter specified.

**Usage**

::

   Usage: assetgen [<path/to/assetgen.yaml> ...] [options]

   Note:
       If you don't specify assetgen.yaml file paths, then `git
       ls-files *assetgen.yaml` will be used to detect all config
       files in the current repository. So you need to be inside
       a git repository's working tree.

   Options:
     -h, --help        show this help message and exit
     -v, --version     show program's version number and exit
     --clean           remove all generated files
     --debug           set debug mode
     --extension=PATH  specify a python extension file (may be repeated)
     --force           force rebuild of all files
     --profile=NAME    specify a profile to use
     --watch           keep running assetgen on a loop

**Contribute**

To contribute any patches simply fork the repository using GitHub and send a
pull request to https://github.com/tav, thanks!

**License**

All of the code has been released into the `Public Domain
<https://github.com/tav/assetgen/raw/master/UNLICENSE>`_. Do with it as you
please.

-- 
Enjoy, tav <tav@espians.com>
