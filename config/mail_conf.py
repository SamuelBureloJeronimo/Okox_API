from config.app import app
from flask_mail import Mail

# Configuración del servidor SMTP
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "santorosario0608@gmail.com" #Es el correo electrónico del remitente (el que envía el correo).
app.config["MAIL_PASSWORD"] = "lnlj hdqs yjkv rpzp" #Es la contraseña que se usa para autenticarse en el servidor SMTP.
app.config["MAIL_DEFAULT_SENDER"] = ("Okox Service", "santorosario0608@gmail.com") #Define el correo que aparecerá como remitente en los emails.

mail = Mail(app)