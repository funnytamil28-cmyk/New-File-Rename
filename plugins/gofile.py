import requests

def upload_gofile(file_path, token=None, folder_id=None):
    """
    Uploads a file to GoFile server using their REST API v2.
    """
    try:
        # Get best upload server
        srv_resp = requests.get("https://api.gofile.io/getServer").json()
        if srv_resp.get("status") != "ok":
            return None
        
        server = srv_resp["data"]["server"]
        url = f"https://{server}.gofile.io/uploadFile"
        
        data = {}
        if token: 
            data['token'] = token
        if folder_id: 
            data['folderId'] = folder_id
        
        with open(file_path, 'rb') as f:
            res = requests.post(url, data=data, files={'file': f}).json()
            
        if res.get("status") == "ok":
            return res["data"]["downloadPage"]
            
    except Exception as e:
        print("GoFile Upload Error:", e)
        
    return None
  
