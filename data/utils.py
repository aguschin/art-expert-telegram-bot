import logging
import requests
import multiprocessing as mp


def async_requests(services, image, n_jobs = None):
    pool = mp.Pool(n_jobs or len(services))
    result = pool.starmap(
        get_prediction,
        [(u, image) for u in services],
    )
    pool.close()
    return result


def get_prediction(url, img_path):
    try:
        response = requests.post(
            url, 
            files = {'file': open(img_path, "rb")},
            timeout=2,
        )
    except Exception as exc:
        # logging.warning(exc)
        return
    else:
        if response and response.status_code == 200 and "price" in response.json():
            return response.json()["price"]
