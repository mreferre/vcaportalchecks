import base64
import httplib2
import xml.etree.ElementTree as ET
import time
import datetime
import boto

def VcaPortalCheck(event, context):
    # we login into the vca root service 
    h = httplib2.Http()
    # NOTE: make sure you are using a proper combination of vCA userid and password in the following statement  
    auth = base64.encodestring('<userid>' + ':' + '<password>')
    (response, content) = h.request('https://vca.vmware.com/api/iam/login', 'POST', headers = {'Authorization':'Basic ' + auth,'Accept':'application/xml;version=5.7'})
    
    # we save the response status of the login call 
    status = response['status']

    # we get the timestamp (st) and we format it properly to express a date (st) 
    ts = time.time() 
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # we check the value of the variables   
    print ts	
    print st
    print status

    # we connect to dynamodb using boto
    # NOTE: make sure you are using a proper combination of AWS access key and secret access key in the following statement  
    # NOTE: this AWS user must have been granted access to the VcaPortalChecks table    
    conn = boto.connect_dynamodb(aws_access_key_id='<XXXXXXXXXXXXXXXXXXXX>',aws_secret_access_key='<XXXXXXXXXXXXXXXXXXXX>')
    
    # we set the table context to the table we previously created  
    table = conn.get_table('VcaPortalChecks')

    # we set the date attribute to be inserted into the item  
    item_data = {
        'date': st,
    }

    # we prepare the new item that includes status, timestamp and the date   
    item = table.new_item(
        # Our hash key is 'status'
        hash_key=status,
        # Our range key is timestamp
        range_key=ts,
        # This has the
        attrs=item_data
    )
    
    # we save the item   
    item.put()

    return status, ts, st 

# only needed when Python code is run interactively (i.e. outside of the Lambda context)
# not required for running the VcaPortalCheck function in Lambda (but it doesn't fail if it's left uncommented) 
# note we are passing a fake (1,1) as function arguments because when the function is invoked by lambda the "event" and the "context" details are passed  
VcaPortalCheck(1,1)
