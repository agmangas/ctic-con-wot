from setuptools import find_packages, setup

setup(
    name="sensorsapp",
    version="0.1.0",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==2.0.2",
        "coloredlogs==15.0.1",
        "Flask-Cors==3.0.10",
        "eventlet==0.30.2",
        "gunicorn[eventlet]==20.1.0",
        "jsonschema[format]==4.2.1",
        "arrow==1.2.1",
        "paho-mqtt==1.6.1"
    ],
    extras_require={"dev": ["black", "pylint", "rope", "pytest", "freezegun"]},
    entry_points={"console_scripts": []},
)
