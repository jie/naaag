from api import server_api
from api import location_api
from api import upstream_api
from api import gateway


routes = [
    (r'/naaag/api/server/create', server_api.CreateAPI),
    (r'/naaag/api/server/update', server_api.UpdateAPI),
    (r'/naaag/api/server/delete', server_api.DeleteAPI),
    (r'/naaag/api/server/get', server_api.GetAPI),
    (r'/naaag/api/location/create', location_api.CreateAPI),
    (r'/naaag/api/location/update', location_api.UpdateAPI),
    (r'/naaag/api/location/delete', location_api.DeleteAPI),
    (r'/naaag/api/location/get', location_api.GetAPI),
    (r'/naaag/api/location/list', location_api.ListAPI),
    (r'/naaag/api/upstream/create', upstream_api.CreateAPI),
    (r'/naaag/api/upstream/update', upstream_api.UpdateAPI),
    (r'/naaag/api/upstream/delete', upstream_api.DeleteAPI),
    (r'/naaag/api/upstream/get', upstream_api.GetAPI),
    # (r'/_gateway', gateway.TestAPI),
    (r'/_gateway/(.*)', gateway.TestAPI),
]
