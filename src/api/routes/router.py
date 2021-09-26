from api.routes.partner import router as partner
from api.routes.health import router as health
from api.routes.home import router as home


routes = [health, home, partner]
