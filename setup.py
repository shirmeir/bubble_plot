import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='dokr',  
     version='0.1',
     scripts=['bubble_plot'] ,
     author="Shir Meir Lador",
     author_email="meir.shir86@gmail.com",
     description="Bubble plot",
     long_description="Bubble plot - data visualization package",
   long_description_content_type="text/markdown",
     url="https://github.com/shirmeir/bubble_plot",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )