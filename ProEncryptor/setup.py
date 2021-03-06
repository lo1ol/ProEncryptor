from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
        options = {
                    'py2exe': {'bundle_files': 1,
                               'compressed': True
                              }
                  },
        console = [{
                    'script': "ProEncryptor.pyw",
                    'icon_resources': [(0, 'ProEncryptor.ico')]
                  }],
        zipfile = None,
)
