import urllib.request
import zipfile

from dagster import asset

@asset
def cereal_ratings_zip() -> None:
    urllib.request.urlretrieve(
        "https://dagster-git-tutorial-nothing-elementl.vercel.app/assets/cereal-ratings.csv.zip",
        "cereal-ratings.csv.zip",
    )

@asset(non_argument_deps={"cereal_ratings_zip"})
def cereal_ratings_csv() -> None:
    with zipfile.ZipFile("cereal-ratings.csv.zip", "r") as zip_ref:
        zip_ref.extractall(".")