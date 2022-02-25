import nginx

def generate_api_location(upstream_name, location_name):
    return nginx.Location('@%s_proxy_api' % upstream_name,
        nginx.Comment(location_name),
        nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
        nginx.Key('proxy_set_header', 'X-Forwarded-Proto https'),
        nginx.Key('proxy_redirect', 'off'),
        nginx.Key('proxy_pass', 'http://%s' % upstream_name),
        nginx.Key('proxy_http_version', 1.1),
        nginx.Key('proxy_set_header', 'Upgrade $http_upgrade'),
        nginx.Key('proxy_set_header', 'Connection "upgrade"'),
        nginx.Key('proxy_set_header', 'X-real-ip $remote_addr'),
        nginx.Key('proxy_set_header', 'Content-Length ""'),
    )


def generate_upstream_api_location(location_name, endpoint, upstream_name, internal=False):
    proxy_api_name = "$uri @%s_proxy_api" % upstream_name
    configs = [        
        nginx.Comment(location_name),
    ]
    if internal is True:
        configs.append(nginx.Key('internal', ""))

    configs.append(nginx.Key('try_files', proxy_api_name))
    return nginx.Location(endpoint,
        *configs
    )

def generate_rewrite_location(location_name, endpoint, rewrite_point, proxy_pass, internal=False):
    configs = [        
        nginx.Comment(location_name),
        nginx.Key('rewrite', '^/%s(.*) $1 break' % rewrite_point),
        nginx.Key('proxy_pass', proxy_pass)
    ]

    if internal is True:
        configs.insert(1, nginx.Key('internal', ""))
    return nginx.Location(endpoint,
        *configs
    )