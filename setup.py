from setuptools import setup

setup(name="tracemap",
      version="one",
      description="",
      url="",
      author="Aeva Palecek",
      author_email="aeva.ntsc@gmail.com",
      license="GPLv3",
      packages=["tracemap"],
      zip_safe=False,

      entry_points = {
        "console_scripts" : [
            "tracemap=tracemap.tracemap:mains",
            ],
        },

      install_requires = [
        ])
      
