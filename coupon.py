
import requests
import time
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Resource:
	def __init__(self,data):
		self.quantity=data["Quantity"]
		self.label = data["Sw_Resource"]["Label"]
	def __repr__(self):
		return "x"+self.quantity + " " + self.label

class Coupon:
	def __init__(self,data):
		self.label = data["Label"]
		self.status = data["Status"]
		self.resources = [Resource(item) for item in data["Resources"]]
	def __repr__(self):
		message=""
		message+= "Coupon: "+self.label+"\n\n"
		message+="http://withhive.me/313/"+self.label+"\n\n"
		message+="Resources:\n"
		for resource in self.resources[:-1]:
			message+=resource.__repr__() + "\n"
		message+=self.resources[-1].__repr__()
		return message


class Bot:
	def __init__(self):
		self.URL = "https://swq.jp/_special/rest/Sw/Coupon"
		self.chatURL = "https://api.telegram.org/bot"+os.environ["BOT_TOKEN"]+"/sendMessage"
		response = requests.get(self.URL)
		data = response.json()["data"]
		self.coupons = [Coupon(item) for item in data if item["Status"]=="verified" and item["Score"]>100]
		print(logTime()+" Bot running")
	def notify(self,coupons):
		for coupon in coupons:
			dataObj={
				"chat_id":os.environ["CHAT_ID"],
				"text": coupon.__repr__()
			}
			requests.post(self.chatURL,data=dataObj)
			print(logTime()+" Coupon found!")
			print("-------------------------------")
			print(coupon)
			print("-------------------------------\n")

	def run(self):
		while True:
			try:
				response = requests.get(self.URL)
				data = response.json()["data"]
				coupons = [Coupon(item) for item in data if item["Status"]=="verified" and item["Score"]>100]
				oldLabels =[item.label for item in self.coupons]
				newCoupons =[item for item in coupons if item.label not in oldLabels]
				if(len(newCoupons)>0):
					self.notify(newCoupons)
				self.coupons=coupons
				time.sleep(900)
			except:
				print(logTime()+" exception ocurred")
def logTime():
	return "["+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]"

if __name__ == "__main__":
	Bot().run()
