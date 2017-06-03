from itertools import ifilter
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


def regroupelog():
    with open("/var/log/auth.log", 'rb') as f, open("/var/log/logssh_trier.txt", 'wb') as g:
        g.writelines(ifilter(lambda line: 'sshd' in line, f))
        print ('/var/log/ssh_trier.txt')


def affiche_contenu():
    with open("/var/log/logssh_trier.txt", 'r') as contenu:
        print contenu.read()


def email():
    fromaddr = "adresse d'envoi"
    toaddr = "adresse destinataire"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "log ssh du jour"

    body = "log ssh du jour envoyer par l'adresse wll.l@live.fr"

    msg.attach(MIMEText(body, 'plain'))

    filename = "logssh_trier.txt"
    attachment = open("/var/log/logssh_trier.txt", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(fromaddr, "mot de passe de l'adresse émettrice")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

