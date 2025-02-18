from config.app import app
from routes.PublicRoutes import BP_Public

bp = app

bp.register_blueprint(BP_Public)


#from routes.Dispositivo import BP_dispositivo
from routes.SystemServ import BP_System
#from routes.Cliente import BP_Clientes
#from routes.Administrador import BP_Administracion
#from routes.Capturista import BP_Capturista

app.register_blueprint(BP_System)
#app.register_blueprint(BP_dispositivo)
#app.register_blueprint(BP_Clientes)
#app.register_blueprint(BP_Administracion)
#app.register_blueprint(BP_Capturista)
