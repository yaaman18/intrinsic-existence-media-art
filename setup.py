from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intrinsic-existence-media-art",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="内在性メディアアート - 写真を初期値として自己参照的な内在性を生成するアートプロジェクト",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaaman18/intrinsic-existence-media-art",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Artistic Software",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
        "cv": [
            "opencv-python>=4.8.0",
            "scikit-image>=0.21.0",
        ],
        "web": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "intrinsic-existence=intrinsic_existence.cli:main",
        ],
    },
)