# way to run the script
################
# python2 ami_backup.py ipaddress 
################

import boto
import boto.ec2
import sys
import time
import datetime
import dateutil.parser
from boto import ec2
from boto.ec2 import connect_to_region
from datetime import date, timedelta

img_list = []
conn = ec2.connect_to_region('us-west-2')

def ami_creation():
	try:
		date = str(time.strftime("%b-%d-%Y"))
		reservations = conn.get_all_instances()
		for reservation in reservations:
			for instances in reservation.instances:
				ipaddress = instances.ip_address
				name = instances.id
				state = instances.state
				#if ipaddress == ip:
				if state == 'running':
					print('\n')
					print(" CREATTING AMI OF ",name)
					print('\n')
					ami_name = str(ipaddress)+'-'+date
					ami_id = instances.create_image(ami_name, description='Created by AMIBackup', no_reboot=True, dry_run=True)
					success = ' CREATTING AMI OF ',str(name)
					img_list.append(success)
	except Exception as e:
		print(e)
		error = 'ERROR WHILE CREATING BACKUP OF ',name
		print(error)
		img_list.append(error)
		img_list.append('\n')
		img_list.append(e)
		
		


def ami_deletion():
    print("I am in deletion")
    flag = 0
    #images = sorted(connect_to_region('us-west-2').get_all_images(owners='self'))
    images = conn.get_all_images(owners='self')
    img_list.append('\n')
    img_list.append('REMOVING FOLLOWING OLD AMI')
    img_list.append('\n')
    for img in images:

        img_date = img.creationDate
        img_desc = img.description
        img_date = dateutil.parser.parse(img_date).date()
        today = datetime.date.today()
        differnce = today - img_date
        if differnce.days >= 10 and img_desc == 'Created by AMIBackup':
            flag += 1
            img_list.append(img.name)
            print (" Deleting the AMI ",img)

            img_list.append('\n')
            print('\n')
            conn.deregister_image(img.id, dry_run=True)

    if flag == 0:
        img_list.append("No older backups")
        print(" No older backups")

ami_creation()
ami_deletion()
