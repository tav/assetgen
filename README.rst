Assetgen is intended as a replacement for the various ad-hoc scripts that often
get written to build/manage JavaScript/CSS files.

**Features**

The default support includes:

* Compiling CoffeeScript/TypeScript source files into JavaScript.

* Minifying with UglifyJS/UglifyJS2 -- including constant folding support.

* Generating source maps for TypeScript and minified JavaScript sources.

* Compiling and minifying CSS from Less, SASS, SCSS and Stylus source files.

* Generating variants of the same stylesheet for internationalisation
  (flipping left to right).

* Embedding image/font resources as ``data:`` URIs within CSS stylesheets to
  minimise latency.

* Concatenating multiple source files into one file to minimise the number of
  HTTP requests.

* Creating distinct files with the hash of the content embedded in the filename
  so as to work effectively with web caches.

* Dynamically fetching source files and embedded resources from HTTP/HTTPS URLs.

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
         - https://raw.github.com/tav/jsutil/master/define.coffee
         - static/js/Models.coffee
         - static/js/Views.coffee
         - static/js/Maps.coffee
       uglify.bin: uglifyjs
       uglify:
         - --define-from-module
         - consts
       profile.dev:
         uglify:
           - --define-from-module
           - consts-dev

   - js/encoder.js:
       source:
         - encoder/detect.ts
         - encoder/format.ts
         - encoder/encode.ts
       sourcemaps: true

   - gfx/*:
       source: static/gfx/*
       type: binary

   - css/site.css:
       source:
         - raw: |
             // Public Domain (-) 2012 The Ampify Authors.
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
       compress: false

   - static/js/consts-dev.js:
       source: static/js/consts-dev.coffee
       compress: false

   env:
     NODE_PATH.prefix: static/js

   output.directory: appengine/static
   output.hashed: true
   output.manifest: appengine/assets.json

   profile.dev:
     css.compress: false
     js.compress: false

To take advantage of the embedding within stylesheets just replace ``url()``
entries with ``embed()`` entries in your source stylesheet files -- whether
that is less, sass, scss, stylus or plain old CSS.

You can control which config options gets used by specifying the ``--profile``
parameter. This will override default values with the values specified for the
given profile. So, in the above example, specifying ``--profile dev`` will use
all the ``profile.dev`` options.

And, whilst you are developing, you can use the ``--watch`` command-line
parameter to tell ``assetgen`` to monitor file changes and rebuild all
appropriate files. Watch also monitors changes to the ``assetgen.yaml`` file,
so you can update the config without having to restart ``assetgen``.

During development, one often runs ``--watch`` with a dev profile, e.g.

::

    assetgen --profile dev --watch

Then, to create the release/production builds, just remove the built files and
regenerate, i.e.

::

    assetgen --clean && assetgen

The above commands assume that you've commited an ``assetgen.yaml`` file into
a git repository. Assetgen will then use ``git`` to auto-detect the file from
within the current repository. If you are not using git or haven't committed
the config file, you can of course specify it explicitly, e.g.

::

    assetgen assetgen.yaml --profile dev --watch
    assetgen assetgen.yaml --clean && assetgen assetgen.yaml

If you are using ``bash``, you can take advantage of the tab-completion for
command line parameters support within ``assetgen`` by adding the following to
your ``~/.bashrc`` or equivalent::

    _assetgen_completion() {
        COMPREPLY=( $( \
        COMP_LINE=$COMP_LINE  COMP_POINT=$COMP_POINT \
        COMP_WORDS="${COMP_WORDS[*]}"  COMP_CWORD=$COMP_CWORD \
        OPTPARSE_AUTO_COMPLETE=1 $1 ) )
    }

    complete -o default -F _assetgen_completion assetgen

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

        And if you specify a URL as a `source`, then it will be
        downloaded to ~/.assetgen -- you can override this by
        setting the env variable $ASSETGEN_DOWNLOADS

    Options:
      -h, --help        show this help message and exit
      -v, --version     show program's version number and exit
      --clean           remove all generated files
      --debug           set debug mode
      --extension=PATH  specify a python extension file (may be repeated)
      --force           force rebuild of all files
      --nuke            remove all generated and downloaded files
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
