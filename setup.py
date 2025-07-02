from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='image_editor',
    version='1.0.0',
    author='Ира',
    author_email='ira.fad33va@mail.ru',
    description='Редактор изображений с функциями обработки',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shellie-py/fadeeva_practice2025.git',
    packages=find_packages(include=['editor', 'editor.*']),
    install_requires=[
        'opencv-python>=4.5.5',
        'Pillow>=9.0.1',
        'numpy>=1.21.5'
    ],
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'image-editor=editor.app:main',
        ],
    },
    keywords='image editor opencv tkinter',
)