from setuptools import setup, find_packages

setup(
   name='kmake_gql_client',
   version='1.0',
   description='Client for kmake gql server',
   author='Jeremy Marshall',
   author_email='jeremystuartmarshall@gmail.com',
   packages=find_packages(),
   python_requires=">=3.6.9",
   extras_require={
         'test': ['pytest >= 3.10.1']
         },
   include_package_data=False,
   zip_safe=False,
   install_requires=[
       'sgqlc>=v10.1', 
       'pyyaml', 
       'pygments',
       'websocket_client>=0.57.0'], #external packages as dependencies
   entry_points = {
        'console_scripts': ['kmake-gql-client=kmake_gql_client.command_line:main'],
    }
)