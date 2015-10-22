from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import mail
import os
from google.appengine.ext.webapp import template
import settings

class Main(webapp.RequestHandler):
	def get(self):
		key = self.request.get('key')
		if settings.ALLOW_USE_WITHOUT_KEY:
			emailTo = settings.WITHOUT_KEY_EMAIL_TO
			self.sendMail(emailTo)
		elif key and key in settings.KEY_EMAILS_MAP:
			emailTo = settings.KEY_EMAILS_MAP[key]
			self.sendMail(emailTo)
		else:
			path = os.path.join(os.path.dirname(__file__), 'default.html') 
			self.response.out.write(template.render(path, {}))
		
		redirectLink = self.request.get('redirectLink')
		if redirectLink and redirectLink != "":
			self.redirect(redirectLink)

	def sendMail(self, emailTo):
		emailFrom = settings.EMAIL_FROM
		subject = settings.EMAIL_SUBJECT
		body = self.getBody()
		
		try:
			mail.send_mail(sender = emailFrom ,
				  to = emailTo,
				  subject = subject,
				  body = body)
		except:
			pass

	def getBody(self):
		argumentData = ""
		for i in self.request.arguments():
			argumentData += i + ": " + str(self.request.get_all(i)) + '\n'
		data = """Remote Address: %s

Full URL: %s

Headers: %s

Cookies: %s

Arguments:
%s""" % (str(self.request.remote_addr), str(self.request.url), str(self.request.headers), str(self.request.cookies), argumentData)
		return data



application = webapp.WSGIApplication([('/.*', Main)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
