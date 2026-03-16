from services.pipeline import process_repository

def test_pipeline():

    repo = "https://github.com/psf/requests"

    process_repository(repo)

    print("Pipeline test completed")